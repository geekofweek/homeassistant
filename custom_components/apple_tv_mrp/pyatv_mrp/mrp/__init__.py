"""Implementation of the MediaRemoteTV Protocol used by ATV4 and later."""

import logging

from .. import (const, exceptions)
from . import (messages, protobuf)
from .srp import SRPAuthHandler
from .connection import MrpConnection
from .protocol import MrpProtocol
from .protobuf import CommandInfo_pb2
from .pairing import MrpPairingProcedure
from ..interface import (AppleTV, RemoteControl, Metadata,
                             Playing, PushUpdater, PairingHandler)


_LOGGER = logging.getLogger(__name__)

# Source: https://github.com/Daij-Djan/DDHidLib/blob/master/usb_hid_usages.txt
_KEY_LOOKUP = {
    # name: [usage_page, usage]
    'up': [1, 0x8C],
    'down': [1, 0x8D],
    'left': [1, 0x8B],
    'right': [1, 0x8A],
    'stop': [12, 0xB7],
    'next': [12, 0xB5],
    'previous': [12, 0xB6],
    'select': [1, 0x89],
    'menu': [1, 0x86],
    'top_menu': [12, 0x60],
    'suspend': [1, 0x82],

    # 'mic': [12, 0x04]  # Siri
}


class MrpRemoteControl(RemoteControl):
    """Implementation of API for controlling an Apple TV."""

    def __init__(self, loop, protocol):
        """Initialize a new MrpRemoteControl."""
        self.loop = loop
        self.protocol = protocol

    async def _press_key(self, key):
        lookup = _KEY_LOOKUP.get(key, None)
        if lookup:
            await self.protocol.send(
                messages.send_hid_event(lookup[0], lookup[1], True))
            await self.protocol.send(
                messages.send_hid_event(lookup[0], lookup[1], False))
        else:
            raise Exception('unknown key: ' + key)

    def up(self):
        """Press key up."""
        return self._press_key('up')

    def down(self):
        """Press key down."""
        return self._press_key('down')

    def left(self):
        """Press key left."""
        return self._press_key('left')

    def right(self):
        """Press key right."""
        return self._press_key('right')

    def play(self):
        """Press key play."""
        return self.protocol.send(messages.command(CommandInfo_pb2.Play))

    def pause(self):
        """Press key play."""
        return self.protocol.send(messages.command(CommandInfo_pb2.Pause))

    def stop(self):
        """Press key stop."""
        return self.protocol.send(messages.command(CommandInfo_pb2.Stop))

    def next(self):
        """Press key next."""
        return self.protocol.send(messages.command(CommandInfo_pb2.NextTrack))

    def previous(self):
        """Press key previous."""
        return self.protocol.send(
            messages.command(CommandInfo_pb2.PreviousTrack))

    def select(self):
        """Press key select."""
        return self._press_key('select')

    def menu(self):
        """Press key menu."""
        return self._press_key('menu')

    def top_menu(self):
        """Go to main menu (long press menu)."""
        return self._press_key('top_menu')

    def suspend(self):
        """Suspend the device."""
        return self._press_key('suspend')

    def set_position(self, pos):
        """Seek in the current playing media."""
        return self.protocol.send(messages.seek_to_position(pos))

    def set_shuffle(self, is_on):
        """Change shuffle mode to on or off."""
        return self.protocol.send(messages.shuffle(is_on))

    def set_repeat(self, repeat_mode):
        """Change repeat mode."""
        # TODO: extract to convert module
        if int(repeat_mode) == const.REPEAT_STATE_OFF:
            state = 1
        elif int(repeat_mode) == const.REPEAT_STATE_ALL:
            state = 2
        elif int(repeat_mode) == const.REPEAT_STATE_TRACK:
            state = 3
        else:
            raise ValueError('Invalid repeat mode: ' + str(repeat_mode))

        return self.protocol.send(messages.repeat(state))


class MrpPlaying(Playing):
    """Implementation of API for retrieving what is playing."""

    def __init__(self, setstate, metadata):
        """Initialize a new MrpPlaying."""
        self._setstate = setstate
        self._metadata = metadata

    @property
    def media_type(self):
        """Type of media is currently playing, e.g. video, music."""
        return const.MEDIA_TYPE_UNKNOWN

    @property
    def play_state(self):
        """Play state, e.g. playing or paused."""
        # TODO: extract to a convert module
        state = self._setstate.playbackState
        if state == 1:
            return const.PLAY_STATE_PLAYING
        if state == 2:
            return const.PLAY_STATE_PAUSED

        return const.PLAY_STATE_PAUSED

    @property
    def title(self):
        """Title of the current media, e.g. movie or song name."""
        return self._setstate.nowPlayingInfo.title or None

    @property
    def artist(self):
        """Artist of the currently playing song."""
        return self._setstate.nowPlayingInfo.artist or None

    @property
    def album(self):
        """Album of the currently playing song."""
        return self._setstate.nowPlayingInfo.album or None

    @property
    def genre(self):
        """Genre of the currently playing song."""
        if self._metadata:
            from pyatv.mrp.protobuf import ContentItem_pb2
            transaction = ContentItem_pb2.ContentItem()
            transaction.ParseFromString(self._metadata)
            # TODO: implement this

    @property
    def total_time(self):
        """Total play time in seconds."""
        now_playing = self._setstate.nowPlayingInfo
        if now_playing.HasField('duration'):
            return int(now_playing.duration)

        return None

    @property
    def position(self):
        """Position in the playing media (seconds)."""
        now_playing = self._setstate.nowPlayingInfo
        if now_playing.HasField('elapsedTime'):
            return int(now_playing.elapsedTime)

        return None

    def _get_command_info(self, command):
        for cmd in self._setstate.supportedCommands.supportedCommands:
            if cmd.command == command:
                return cmd
        return None

    @property
    def shuffle(self):
        """If shuffle is enabled or not."""
        info = self._get_command_info(CommandInfo_pb2.ChangeShuffleMode)
        return None if info is None else info.shuffleMode

    @property
    def repeat(self):
        """Repeat mode."""
        info = self._get_command_info(CommandInfo_pb2.ChangeRepeatMode)
        return None if info is None else info.repeatMode


class MrpMetadata(Metadata):
    """Implementation of API for retrieving metadata."""

    def __init__(self, protocol):
        """Initialize a new MrpPlaying."""
        self.protocol = protocol
        self.protocol.add_listener(
            self._handle_set_state, protobuf.SET_STATE_MESSAGE)
        self.protocol.add_listener(
            self._handle_transaction, protobuf.TRANSACTION_MESSAGE)
        self._setstate = None
        self._nowplaying = None

    async def _handle_set_state(self, message, _):
        self._setstate = message.inner()

    async def _handle_transaction(self, message, _):
        packet = message.inner().packets.packets[0].packetData
        self._nowplaying = packet  # .contentItem.metadata.nowPlayingInfo

    @property
    def device_id(self):
        """Return a unique identifier for current device."""
        raise exceptions.NotSupportedError

    async def artwork(self):
        """Return artwork for what is currently playing (or None)."""
        return None

    async def artwork_url(self):
        """Return artwork URL for what is currently playing."""
        return None

    async def playing(self):
        """Return what is currently playing."""
        # TODO: This is hack-ish
        if self._setstate is None:
            await self.protocol.start()

        # No SET_STATE_MESSAGE received yet, use default
        if self._setstate is None:
            return MrpPlaying(protobuf.SetStateMessage(), None)

        return MrpPlaying(self._setstate, self._nowplaying)


class MrpPushUpdater(PushUpdater):
    """Implementation of API for handling push update from an Apple TV."""

    def __init__(self, loop, metadata, protocol):
        """Initialize a new MrpPushUpdater instance."""
        super().__init__()
        self.loop = loop
        self.metadata = metadata
        self.protocol = protocol
        self.protocol.add_listener(
            self._handle_update, protobuf.SET_STATE_MESSAGE)
        self.protocol.add_listener(
            self._handle_update, protobuf.TRANSACTION_MESSAGE)
        self._enabled = False

    def start(self, initial_delay=0):
        """Wait for push updates from device.

        Will throw NoAsyncListenerError if no listner has been set.
        """
        if self.listener is None:
            raise exceptions.NoAsyncListenerError
        elif self._enabled:
            return

        self._enabled = True

    def stop(self):
        """No longer wait for push updates."""
        self._enabled = False

    async def _handle_update(self, *_):
        if self._enabled:
            playstatus = await self.metadata.playing()
            self.loop.call_soon(
                self.listener.playstatus_update, self, playstatus)


class MrpPairingHandler(PairingHandler):
    """Base class for API used to pair with an Apple TV."""

    def __init__(self, protocol, srp, service):
        """Initialize a new MrpPairingHandler."""
        self.pairing_procedure = MrpPairingProcedure(protocol, srp)
        self.service = service
        self._pin_code = None

    @property
    def has_paired(self):
        """If a successful pairing has been performed."""
        return self.service.device_credentials is not None

    @property
    def credentials(self):
        """Credentials that were generated during pairing."""
        return str(self.service.device_credentials)

    async def start(self, **kwargs):
        """Start pairing process."""
        await self.pairing_procedure.start_pairing()

    async def stop(self, **kwargs):
        """Stop pairing process."""
        if not self._pin_code:
            raise Exception('no pin given')  # TODO: new exception

        self.service.device_credentials = \
            await self.pairing_procedure.finish_pairing(self._pin_code)

    def pin(self, pin):
        """Pin code used for pairing."""
        self._pin_code = pin

    @property
    def device_provides_pin(self):
        """Return True if remote device presents PIN code, else False."""
        return True


class MrpAppleTV(AppleTV):
    """Implementation of API support for Apple TV."""

    # This is a container class so it's OK with many attributes
    # pylint: disable=too-many-instance-attributes
    def __init__(self, loop, session, details, airplay):
        """Initialize a new Apple TV."""
        super().__init__()

        self._session = session
        self._mrp_service = details.get_service(const.PROTOCOL_MRP)

        self._connection = MrpConnection(
            details.address, self._mrp_service.port, loop)
        self._srp = SRPAuthHandler()
        self._protocol = MrpProtocol(
            loop, self._connection, self._srp, self._mrp_service)

        self._mrp_remote = MrpRemoteControl(loop, self._protocol)
        self._mrp_metadata = MrpMetadata(self._protocol)
        self._mrp_push_updater = MrpPushUpdater(
            loop, self._mrp_metadata, self._protocol)
        self._mrp_pairing = MrpPairingHandler(
            self._protocol, self._srp, self._mrp_service)
        self._airplay = airplay

    async def login(self):
        """Perform an explicit login."""
        await self._protocol.start()

    async def logout(self):
        """Perform an explicit logout.

        Must be done when session is no longer needed to not leak resources.
        """
        await self._session.close()
        self._protocol.stop()

    @property
    def service(self):
        """Return service used to connect to the Apple TV.."""
        return self._mrp_service

    @property
    def pairing(self):
        """Return API for pairing with the Apple TV."""
        return self._mrp_pairing

    @property
    def remote_control(self):
        """Return API for controlling the Apple TV."""
        return self._mrp_remote

    @property
    def metadata(self):
        """Return API for retrieving metadata from Apple TV."""
        return self._mrp_metadata

    @property
    def push_updater(self):
        """Return API for handling push update from the Apple TV."""
        return self._mrp_push_updater

    @property
    def airplay(self):
        """Return API for working with AirPlay."""
        return self._airplay
