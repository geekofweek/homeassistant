"""Various types of extraction and conversion functions."""

from . import (const, exceptions)


def media_kind(kind):
    """Convert iTunes media kind to API representation."""
    if kind in [1]:
        return const.MEDIA_TYPE_UNKNOWN
    if kind in [3, 7, 11, 12, 13, 18, 32]:
        return const.MEDIA_TYPE_VIDEO
    if kind in [2, 4, 10, 14, 17, 21, 36]:
        return const.MEDIA_TYPE_MUSIC
    if kind in [8, 64]:
        return const.MEDIA_TYPE_TV

    raise exceptions.UnknownMediaKind('Unknown media kind: ' + str(kind))


def media_type_str(mediatype):
    """Convert internal API media type to string."""
    if mediatype == const.MEDIA_TYPE_UNKNOWN:
        return 'Unknown'
    if mediatype == const.MEDIA_TYPE_VIDEO:
        return 'Video'
    if mediatype == const.MEDIA_TYPE_MUSIC:
        return 'Music'
    if mediatype == const.MEDIA_TYPE_TV:
        return 'TV'
    return 'Unsupported'


def playstate(state):
    """Convert iTunes playstate to API representation."""
    # pylint: disable=too-many-return-statements
    if state is None:
        return const.PLAY_STATE_NO_MEDIA
    if state == 0:
        return const.PLAY_STATE_IDLE
    if state == 1:
        return const.PLAY_STATE_LOADING
    if state == 3:
        return const.PLAY_STATE_PAUSED
    if state == 4:
        return const.PLAY_STATE_PLAYING
    if state == 5:
        return const.PLAY_STATE_FAST_FORWARD
    if state == 6:
        return const.PLAY_STATE_FAST_BACKWARD

    raise exceptions.UnknownPlayState('Unknown playstate: ' + str(state))


# pylint: disable=too-many-return-statements
def playstate_str(state):
    """Convert internal API playstate to string."""
    if state == const.PLAY_STATE_NO_MEDIA:
        return 'No media'
    if state == const.PLAY_STATE_IDLE:
        return 'Idle'
    if state == const.PLAY_STATE_LOADING:
        return 'Loading'
    if state == const.PLAY_STATE_PAUSED:
        return 'Paused'
    if state == const.PLAY_STATE_PLAYING:
        return 'Playing'
    if state == const.PLAY_STATE_FAST_FORWARD:
        return 'Fast forward'
    if state == const.PLAY_STATE_FAST_BACKWARD:
        return 'Fast backward'
    return 'Unsupported'


def repeat_str(state):
    """Convert internal API repeat state to string."""
    if state == const.REPEAT_STATE_OFF:
        return 'Off'
    if state == const.REPEAT_STATE_TRACK:
        return 'Track'
    if state == const.REPEAT_STATE_ALL:
        return 'All'
    return 'Unsupported'


def ms_to_s(time):
    """Convert time in ms to seconds."""
    if time is None:
        return 0

    # Happens in some special cases, just return 0
    if time >= (2**32 - 1):
        return 0
    return round(time / 1000.0)


def protocol_str(protocol):
    """Convert internal API protocol to string."""
    if protocol == const.PROTOCOL_MRP:
        return 'MRP'
    if protocol == const.PROTOCOL_DMAP:
        return 'DMAP'
    if protocol == const.PROTOCOL_AIRPLAY:
        return 'AirPlay'
    return 'Unknown'
