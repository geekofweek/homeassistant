"""API exposed by the library."""

import re
import inspect
import hashlib

from abc import (ABCMeta, abstractmethod, abstractproperty)

from . import (convert, exceptions)


# TODO: make these methods more pretty and safe
def _get_first_sentence_in_pydoc(obj):
    doc = obj.__doc__
    index = doc.find('.')
    if index == -1:
        # Here we have no leading . so return everything
        return doc

    # Try to find the first complete sentence and respect
    # abbreviations correctly
    match = re.findall(r'(.*\.[^A-Z]*)\.(?: [A-Z].*|)', doc)
    if len(match) == 1:
        return match[0]
    return doc[0:index]


def retrieve_commands(obj):
    """Retrieve all commands and help texts from an API object."""
    commands = {}  # Name and help
    for func in obj.__dict__:
        if not inspect.isfunction(obj.__dict__[func]) and \
           not isinstance(obj.__dict__[func], property):
            continue
        if func.startswith('_'):
            continue
        commands[func] = _get_first_sentence_in_pydoc(
            obj.__dict__[func])
    return commands


class PairingHandler:
    """Base class for API used to pair with an Apple TV."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def pin(self, pin):
        """Pin code used for pairing."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def device_provides_pin(self):
        """Return True if remote device presents PIN code, else False."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def has_paired(self):
        """If a successful pairing has been performed.

        The value will be reset when stop() is called.
        """
        raise exceptions.NotSupportedError

    @abstractproperty
    def credentials(self):
        """Credentials that were generated during pairing."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def start(self, **kwargs):
        """Start pairing process."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def stop(self, **kwargs):
        """Stop pairing process."""
        raise exceptions.NotSupportedError


class RemoteControl:
    """Base class for API used to control an Apple TV."""

    __metaclass__ = ABCMeta

    # pylint: disable=invalid-name
    @abstractmethod
    def up(self):
        """Press key up."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def down(self):
        """Press key down."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def left(self):
        """Press key left."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def right(self):
        """Press key right."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def play(self):
        """Press key play."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def pause(self):
        """Press key play."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def stop(self):
        """Press key stop."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def next(self):
        """Press key next."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def previous(self):
        """Press key previous."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def select(self):
        """Press key select."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def menu(self):
        """Press key menu."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def top_menu(self):
        """Go to main menu (long press menu)."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def suspend(self):
        """Suspend the device."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def set_position(self, pos):
        """Seek in the current playing media."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def set_shuffle(self, is_on):
        """Change shuffle mode to on or off."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def set_repeat(self, repeat_mode):
        """Change repeat mode."""
        raise exceptions.NotSupportedError


class Playing:
    """Base class for retrieving what is currently playing."""

    __metaclass__ = ABCMeta

    def __str__(self):
        """Convert this playing object to a readable string."""
        output = []
        output.append('Media type: {0}'.format(
            convert.media_type_str(self.media_type)))
        output.append('Play state: {0}'.format(
            convert.playstate_str(self.play_state)))

        if self.title is not None:
            output.append('     Title: {0}'.format(self.title))

        if self.artist is not None:
            output.append('    Artist: {0}'.format(self.artist))

        if self.album is not None:
            output.append('     Album: {0}'.format(self.album))

        if self.genre is not None:
            output.append('     Genre: {0}'.format(self.genre))

        position = self.position
        total_time = self.total_time
        if position is not None and total_time is not None and total_time != 0:
            output.append('  Position: {0}/{1}s ({2:.1%})'.format(
                position, total_time, float(position)/float(total_time)))
        elif position is not None and position != 0:
            output.append('  Position: {0}s'.format(position))
        elif total_time is not None and position != 0:
            output.append('Total time: {0}s'.format(total_time))

        if self.repeat is not None:
            output.append('    Repeat: {0}'.format(
                convert.repeat_str(self.repeat)))

        if self.shuffle is not None:
            output.append('   Shuffle: {0}'.format(self.shuffle))

        return '\n'.join(output)

    @property
    def hash(self):
        """Create a unique hash for what is currently playing.

        The hash is based on title, artist, album and total time. It should
        always be the same for the same content, but it is not guaranteed.
        """
        base = '{0}{1}{2}{3}'.format(
            self.title, self.artist, self.album, self.total_time)
        return hashlib.sha256(base.encode('utf-8')).hexdigest()

    @abstractproperty
    def media_type(self):
        """Type of media is currently playing, e.g. video, music."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def play_state(self):
        """Play state, e.g. playing or paused."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def title(self):
        """Title of the current media, e.g. movie or song name."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def artist(self):
        """Artist of the currently playing song."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def album(self):
        """Album of the currently playing song."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def genre(self):
        """Genre of the currently playing song."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def total_time(self):
        """Total play time in seconds."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def position(self):
        """Position in the playing media (seconds)."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def shuffle(self):
        """If shuffle is enabled or not."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def repeat(self):
        """Repeat mode."""
        raise exceptions.NotSupportedError


class Metadata:
    """Base class for retrieving metadata from an Apple TV."""

    __metaclass__ = ABCMeta

    @abstractproperty
    def device_id(self):
        """Return a unique identifier for current device."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def artwork(self):
        """Return artwork for what is currently playing (or None)."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def artwork_url(self):
        """Return artwork URL for what is currently playing."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def playing(self):
        """Return what is currently playing."""
        raise exceptions.NotSupportedError


class PushUpdater:
    """Base class for push/async updates from an Apple TV."""

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initialize a new PushUpdater."""
        self.__listener = None

    @property
    def listener(self):
        """Object (PushUpdaterListener) that receives updates."""
        return self.__listener

    @listener.setter  # type: ignore
    def listener(self, listener):
        """Object that receives updates.

        This should be an object implementing two methods:
        - playstatus_update(updater, playstatus)
        - playstatus_error(updater, exception)

        The first method is called when a new update happens and the second one
        is called if an error occurs. Please note that if an error happens,
        push updates will be stopped. So they will need to be enabled again,
        e.g. from the error method. A delay should preferably be passed to
        start() to avoid an infinite error-loop.
        """
        self.__listener = listener

    @abstractmethod
    def start(self, initial_delay=0):
        """Begin to listen to updates.

        If an error occurs, start must be called again.
        """
        raise exceptions.NotSupportedError

    @abstractmethod
    def stop(self):
        """No longer listen for updates."""
        raise exceptions.NotSupportedError


class AirPlay:
    """Base class for AirPlay functionality."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_credentials(self):
        """Create new credentials for authentication.

        Credentials that have been authenticated shall be saved and loaded with
        load_credentials before playing anything. If credentials are lost,
        authentication must be performed again.
        """
        raise exceptions.NotSupportedError

    @abstractmethod
    def load_credentials(self, credentials):
        """Load existing credentials."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def verify_authenticated(self):
        """Check if loaded credentials are verified."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def start_authentication(self):
        """Begin authentication proces (show PIN on screen)."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def finish_authentication(self, pin):
        """End authentication process with PIN code."""
        raise exceptions.NotSupportedError

    @abstractmethod
    def play_url(self, url, **kwargs):
        """Play media from an URL on the device."""
        raise exceptions.NotSupportedError


class AppleTV:
    """Base class representing an Apple TV."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def login(self):
        """Perform an explicit login.

        Not needed as login is performed automatically.
        """
        raise exceptions.NotSupportedError

    @abstractmethod
    def logout(self):
        """Perform an explicit logout.

        Must be done when session is no longer needed to not leak resources.
        """
        raise exceptions.NotSupportedError

    @abstractproperty
    def service(self):
        """Return service used to connect to the Apple TV.."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def pairing(self):
        """Return API for pairing with the Apple TV."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def remote_control(self):
        """Return API for controlling the Apple TV."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def metadata(self):
        """Return API for retrieving metadata from the Apple TV."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def push_updater(self):
        """Return API for handling push update from the Apple TV."""
        raise exceptions.NotSupportedError

    @abstractproperty
    def airplay(self):
        """Return API for working with AirPlay."""
        raise exceptions.NotSupportedError
