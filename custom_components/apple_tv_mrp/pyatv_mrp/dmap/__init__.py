"""Implementation of the DMAP protocol used by ATV 1, 2 and 3."""

import logging
import asyncio
import hashlib

from urllib.parse import urlparse

from .. import (const, exceptions, convert)
from . import (pairing, parser, tags)
from .daap import DaapRequester
from ..net import HttpSession
from ..interface import (AppleTV, RemoteControl, Metadata,
                             Playing, PushUpdater)

_LOGGER = logging.getLogger(__name__)

_PSU_CMD = 'ctrl-int/1/playstatusupdate?[AUTH]&revision-number={0}'
_ARTWORK_CMD = 'ctrl-int/1/nowplayingartwork?mw=1024&mh=576&[AUTH]'
_CTRL_PROMPT_CMD = 'ctrl-int/1/controlpromptentry?[AUTH]&prompt-id=0'


class BaseDmapAppleTV:
    """Common protocol logic used to interact with an Apple TV."""

    def __init__(self, requester):
        """Initialize a new Apple TV base implemenation."""
        self.daap = requester
        self.playstatus_revision = 0

    async def playstatus(self, use_revision=False, timeout=None):
        """Request raw data about what is currently playing.

        If use_revision=True, this command will "block" until playstatus
        changes on the device.

        Must be logged in.
        """
        cmd_url = _PSU_CMD.format(
            self.playstatus_revision if use_revision else 0)
        resp = await self.daap.get(cmd_url, timeout=timeout)
        self.playstatus_revision = parser.first(resp, 'cmst', 'cmsr')
        return resp

    def artwork_url(self):
        """Return URL to current artwork.

        As as valid session id is necessary, the URL will only be valid
        if logged in.
        """
        return self.daap.get_url(_ARTWORK_CMD)

    async def artwork(self):
        """Return an image file (png) for what is currently playing.

        None is returned if no artwork is available. Must be logged in.
        """
        art = await self.daap.get(_ARTWORK_CMD, daap_data=False)
        return art if art != b'' else None

    def playqueue(self):
        """Return current playqueue. Must be logged in."""
        return self.daap.post('playqueue-contents?[AUTH]')

    def ctrl_int_cmd(self, cmd):
        """Perform a "ctrl-int" command."""
        cmd_url = 'ctrl-int/1/{}?[AUTH]&prompt-id=0'.format(cmd)
        return self.daap.post(cmd_url)

    def controlprompt_cmd(self, cmd):
        """Perform a "controlpromptentry" command."""
        data = tags.string_tag('cmbe', cmd) + tags.uint8_tag('cmcc', 0)
        return self.daap.post(_CTRL_PROMPT_CMD, data=data)

    def controlprompt_data(self, data):
        """Perform a "controlpromptentry" command."""
        return self.daap.post(_CTRL_PROMPT_CMD, data=data)

    def set_property(self, prop, value):
        """Change value of a DAAP property, e.g. volume or media position."""
        cmd_url = 'ctrl-int/1/setproperty?{}={}&[AUTH]'.format(
            prop, value)
        return self.daap.post(cmd_url)


class DmapRemoteControl(RemoteControl):
    """Implementation of API for controlling an Apple TV."""

    def __init__(self, apple_tv):
        """Initialize remote control instance."""
        super().__init__()
        self.apple_tv = apple_tv

    async def up(self):
        """Press key up."""
        await self._send_commands(
            self._move('Down', 0, 20, 275),
            self._move('Move', 1, 20, 270),
            self._move('Move', 2, 20, 265),
            self._move('Move', 3, 20, 260),
            self._move('Move', 4, 20, 255),
            self._move('Move', 5, 20, 250),
            self._move('Up', 6, 20, 250))

    async def down(self):
        """Press key down."""
        await self._send_commands(
            self._move('Down', 0, 20, 250),
            self._move('Move', 1, 20, 255),
            self._move('Move', 2, 20, 260),
            self._move('Move', 3, 20, 265),
            self._move('Move', 4, 20, 270),
            self._move('Move', 5, 20, 275),
            self._move('Up', 6, 20, 275))

    async def left(self):
        """Press key left."""
        await self._send_commands(
            self._move('Down', 0, 75, 100),
            self._move('Move', 1, 70, 100),
            self._move('Move', 3, 65, 100),
            self._move('Move', 4, 60, 100),
            self._move('Move', 5, 55, 100),
            self._move('Move', 6, 50, 100),
            self._move('Up', 7, 50, 100))

    async def right(self):
        """Press key right."""
        await self._send_commands(
            self._move('Down', 0, 50, 100),
            self._move('Move', 1, 55, 100),
            self._move('Move', 3, 60, 100),
            self._move('Move', 4, 65, 100),
            self._move('Move', 5, 70, 100),
            self._move('Move', 6, 75, 100),
            self._move('Up', 7, 75, 100))

    @staticmethod
    def _move(direction, time, point1, point2):
        data = 'touch{0}&time={1}&point={2},{3}'.format(
            direction, time, point1, point2)
        return tags.uint8_tag('cmcc', 0x30) + tags.string_tag('cmbe', data)

    async def _send_commands(self, *cmds):
        for cmd in cmds:
            await self.apple_tv.controlprompt_data(cmd)

    def play(self):
        """Press key play."""
        return self.apple_tv.ctrl_int_cmd('play')

    def pause(self):
        """Press key pause."""
        return self.apple_tv.ctrl_int_cmd('pause')

    def stop(self):
        """Press key stop."""
        return self.apple_tv.ctrl_int_cmd('stop')

    def next(self):
        """Press key next."""
        return self.apple_tv.ctrl_int_cmd('nextitem')

    def previous(self):
        """Press key previous."""
        return self.apple_tv.ctrl_int_cmd('previtem')

    def select(self):
        """Press key select."""
        return self.apple_tv.controlprompt_cmd('select')

    def menu(self):
        """Press key menu."""
        return self.apple_tv.controlprompt_cmd('menu')

    def top_menu(self):
        """Press key topmenu."""
        return self.apple_tv.controlprompt_cmd('topmenu')

    async def suspend(self):
        """Suspend the device."""
        # Not supported by DMAP
        raise exceptions.NotSupportedError

    def set_position(self, pos):
        """Seek in the current playing media."""
        time_in_ms = int(pos)*1000
        return self.apple_tv.set_property('dacp.playingtime', time_in_ms)

    def set_shuffle(self, is_on):
        """Change shuffle mode to on or off."""
        state = 1 if is_on else 0
        return self.apple_tv.set_property('dacp.shufflestate', state)

    def set_repeat(self, repeat_mode):
        """Change repeat mode."""
        return self.apple_tv.set_property('dacp.repeatstate', repeat_mode)


class DmapPlaying(Playing):
    """Implementation of API for retrieving what is playing."""

    def __init__(self, playstatus):
        """Initialize playing instance."""
        super().__init__()
        self.playstatus = playstatus

    @property
    def media_type(self):
        """Type of media is currently playing, e.g. video, music."""
        state = parser.first(self.playstatus, 'cmst', 'caps')
        if not state:
            return const.MEDIA_TYPE_UNKNOWN

        mediakind = parser.first(self.playstatus, 'cmst', 'cmmk')
        if mediakind is not None:
            return convert.media_kind(mediakind)

        # Fallback: if artist or album exists we assume music (not present
        # for video)
        if self.artist or self.album:
            return const.MEDIA_TYPE_MUSIC

        return const.MEDIA_TYPE_VIDEO

    @property
    def play_state(self):
        """Play state, e.g. playing or paused."""
        state = parser.first(self.playstatus, 'cmst', 'caps')
        return convert.playstate(state)

    @property
    def title(self):
        """Title of the current media, e.g. movie or song name."""
        return parser.first(self.playstatus, 'cmst', 'cann')

    @property
    def artist(self):
        """Arist of the currently playing song."""
        return parser.first(self.playstatus, 'cmst', 'cana')

    @property
    def album(self):
        """Album of the currently playing song."""
        return parser.first(self.playstatus, 'cmst', 'canl')

    @property
    def genre(self):
        """Genre of the currently playing song."""
        return parser.first(self.playstatus, 'cmst', 'cang')

    @property
    def total_time(self):
        """Total play time in seconds."""
        return self._get_time_in_seconds('cast')

    @property
    def position(self):
        """Position in the playing media (seconds)."""
        return self.total_time - self._get_time_in_seconds('cant')

    @property
    def shuffle(self):
        """If shuffle is enabled or not."""
        return bool(parser.first(self.playstatus, 'cmst', 'cash'))

    @property
    def repeat(self):
        """Repeat mode."""
        return parser.first(self.playstatus, 'cmst', 'carp')

    def _get_time_in_seconds(self, tag):
        time = parser.first(self.playstatus, 'cmst', tag)
        return convert.ms_to_s(time)


class DmapMetadata(Metadata):
    """Implementation of API for retrieving metadata from an Apple TV."""

    def __init__(self, apple_tv, daap):
        """Initialize metadata instance."""
        super().__init__()
        self.apple_tv = apple_tv

        # Extract hostname and use that as base for hash
        address = urlparse(daap.base_url).hostname
        self._device_id = hashlib.sha256(address.encode('utf-8')).hexdigest()

    @property
    def device_id(self):
        """Return a unique identifier for current device."""
        return self._device_id

    def artwork(self):
        """Return artwork for what is currently playing (or None)."""
        return self.apple_tv.artwork()

    async def artwork_url(self):
        """Return artwork URL for what is currently playing."""
        return self.apple_tv.artwork_url()

    async def playing(self):
        """Return current device state."""
        playstatus = await self.apple_tv.playstatus()
        return DmapPlaying(playstatus)


class DmapPushUpdater(PushUpdater):
    """Implementation of API for handling push update from an Apple TV."""

    def __init__(self, loop, apple_tv):
        """Initialize a new DmapPushUpdater instance."""
        super().__init__()
        self._loop = loop
        self._atv = apple_tv
        self._future = None

    def start(self, initial_delay=0):
        """Wait for push updates from device.

        Will throw NoAsyncListenerError if no listner has been set.
        """
        if self.listener is None:
            raise exceptions.NoAsyncListenerError
        elif self._future is not None:
            return None

        # Always start with 0 to trigger an immediate response for the
        # first request
        self._atv.playstatus_revision = 0

        # This for some reason fails on travis but not in other places.
        # Why is that (same python version)?
        # pylint: disable=deprecated-method
        self._future = asyncio.ensure_future(
            self._poller(initial_delay), loop=self._loop)
        return self._future

    def stop(self):
        """No longer wait for push updates."""
        if self._future is not None:
            # TODO: pylint does not seem to figure out that cancel exists?
            self._future.cancel()  # pylint: disable=no-member
            self._future = None

    async def _poller(self, initial_delay):
        # Sleep some time before waiting for updates
        if initial_delay > 0:
            _LOGGER.debug('Initial delay set to %d', initial_delay)
            await asyncio.sleep(initial_delay, loop=self._loop)

        while True:
            try:
                _LOGGER.debug('Waiting for playstatus updates')
                playstatus = await self._atv.playstatus(
                    use_revision=True, timeout=0)

                self._loop.call_soon(self.listener.playstatus_update,
                                     self, DmapPlaying(playstatus))
            except asyncio.CancelledError:
                break

            # It is not pretty to disable pylint here, but we must catch _all_
            # exceptions to keep the API.
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.debug('Playstatus error occurred: %s', ex)
                self._loop.call_soon(self.listener.playstatus_error, self, ex)
                break

        self._future = None


class DmapAppleTV(AppleTV):
    """Implementation of API support for Apple TV."""

    # This is a container class so it's OK with many attributes
    # pylint: disable=too-many-instance-attributes
    def __init__(self, loop, session, details, airplay):
        """Initialize a new Apple TV."""
        super().__init__()
        self._session = session

        self._dmap_service = details.get_service(const.PROTOCOL_DMAP)
        daap_http = HttpSession(
            session,
            'http://{0}:{1}/'.format(details.address, self._dmap_service.port))
        self._requester = DaapRequester(
            daap_http, self._dmap_service.device_credentials)

        self._apple_tv = BaseDmapAppleTV(self._requester)
        self._dmap_remote = DmapRemoteControl(self._apple_tv)
        self._dmap_metadata = DmapMetadata(self._apple_tv, daap_http)
        self._dmap_push_updater = DmapPushUpdater(loop, self._apple_tv)
        self._dmap_pairing = pairing.DmapPairingHandler(loop)
        self._airplay = airplay

    def login(self):
        """Perform an explicit login.

        Not needed as login is performed automatically.
        """
        return self._requester.login()

    async def logout(self):
        """Perform an explicit logout.

        Must be done when session is no longer needed to not leak resources.
        """
        await self._session.close()

    @property
    def service(self):
        """Return service used to connect to the Apple TV.."""
        return self._dmap_service

    @property
    def pairing(self):
        """Return API for pairing with the Apple TV."""
        return self._dmap_pairing

    @property
    def remote_control(self):
        """Return API for controlling the Apple TV."""
        return self._dmap_remote

    @property
    def metadata(self):
        """Return API for retrieving metadata from Apple TV."""
        return self._dmap_metadata

    @property
    def push_updater(self):
        """Return API for handling push update from the Apple TV."""
        return self._dmap_push_updater

    @property
    def airplay(self):
        """Return API for working with AirPlay."""
        return self._airplay
