"""Constants used in the public API."""

MAJOR_VERSION = 0
MINOR_VERSION = 4
PATCH_VERSION = '0.dev0'
__short_version__ = '{}.{}'.format(MAJOR_VERSION, MINOR_VERSION)
__version__ = '{}.{}'.format(__short_version__, PATCH_VERSION)


# Protocol types

#: Protocol is DMAP (Apple TV 1, 2 and 3)
PROTOCOL_DMAP = 1

#: Protocol is MediaRemote (Apple TV 4 and later)
PROTOCOL_MRP = 2

#: Protocol is AirPlay
PROTOCOL_AIRPLAY = 3


# Media types

#: Media type is unknown
MEDIA_TYPE_UNKNOWN = 1

#: Media type is video
MEDIA_TYPE_VIDEO = 2

#: Media type is music
MEDIA_TYPE_MUSIC = 3

#: Media type is TV
MEDIA_TYPE_TV = 4


# Play states

#: Device is in idle state
PLAY_STATE_IDLE = 0

#: No media is currently select/playing
PLAY_STATE_NO_MEDIA = 1

#: Media is loading/buffering
PLAY_STATE_LOADING = 2

#: Media is paused
PLAY_STATE_PAUSED = 3

#: Media is playing
PLAY_STATE_PLAYING = 4

#: Media is being fast forwarded
PLAY_STATE_FAST_FORWARD = 5

#: Media is being rewinded
PLAY_STATE_FAST_BACKWARD = 6


# Repeat states

#: No repeat
REPEAT_STATE_OFF = 0

#: Repeat current track
REPEAT_STATE_TRACK = 1

#: Repeat all tracks
REPEAT_STATE_ALL = 2
