"""Definitions of DMAP tags used by various applications."""

import logging
from .parser import DmapTag
from .tags import (
    read_bool, read_uint, read_str, read_ignore, read_bplist)

_LOGGER = logging.getLogger(__name__)


# Internal version that works like read_ignore, but also logs
def _read_unknown(data, start, length):
    _LOGGER.warning('Unknown data: %s', str(data[start-8:start+length+8]))


# These are the tags that we know about so far
# pylint: disable=bad-whitespace
_TAGS = {
    'aeFP': DmapTag(read_uint,   'com.apple.itunes.req-fplay'),
    'aeSV': DmapTag(read_uint,   'com.apple.itunes.music-sharing-version'),
    'apro': DmapTag(read_uint,   'daap.protocolversion'),
    'asgr': DmapTag(read_uint,   'com.apple.itunes.gapless-resy'),
    'ated': DmapTag(read_bool,   'daap.supportsextradata'),
    'caar': DmapTag(read_uint,   'dacp.albumrepeat'),
    'caas': DmapTag(read_uint,   'dacp.albumshuffle'),
    'caci': DmapTag('container', 'dacp.controlint'),
    'cafe': DmapTag(read_bool,   'dacp.fullscreenenabled'),
    'cafs': DmapTag(read_uint,   'dacp.fullscreen'),
    'cana': DmapTag(read_str,    'daap.nowplayingartist'),
    'cang': DmapTag(read_str,    'dacp.nowplayinggenre'),
    'canl': DmapTag(read_str,    'daap.nowplayingalbum'),
    'cann': DmapTag(read_str,    'daap.nowplayingtrack'),
    'cant': DmapTag(read_uint,   'dacp.remainingtime'),
    'capr': DmapTag(read_uint,   'dacp.protocolversion'),
    'caps': DmapTag(read_uint,   'dacp.playstatus'),
    'carp': DmapTag(read_uint,   'dacp.repeatstate'),
    'cash': DmapTag(read_uint,   'dacp.shufflestate'),
    'cast': DmapTag(read_uint,   'dacp.tracklength'),
    'casu': DmapTag(read_uint,   'dacp.su'),
    'cavc': DmapTag(read_bool,   'dacp.volumecontrollable'),
    'cave': DmapTag(read_bool,   'dacp.dacpvisualizerenabled'),
    'cavs': DmapTag(read_uint,   'dacp.visualizer'),
    'ceQR': DmapTag('container', 'com.apple.itunes.playqueue-contents-response'),  # NOQA
    'ceSD': DmapTag(read_bplist, 'playing metadata'),
    'cmcp': DmapTag('container', 'dmcp.controlprompt'),
    'cmmk': DmapTag(read_uint,   'dmcp.mediakind'),
    'cmnm': DmapTag(read_str,    'dacp.devicename'),
    'cmpa': DmapTag('container', 'dacp.pairinganswer'),
    'cmpg': DmapTag(read_uint,   'dacp.pairingguid'),
    'cmpr': DmapTag(read_uint,   'dmcp.protocolversion'),
    'cmsr': DmapTag(read_uint,   'dmcp.serverrevision'),
    'cmst': DmapTag('container', 'dmcp.playstatus'),
    'cmty': DmapTag(read_str,    'dacp.devicetype'),
    'mdcl': DmapTag('container', 'dmap.dictionary'),
    'miid': DmapTag(read_uint,   'dmap.itemid'),
    'minm': DmapTag(read_str,    'dmap.itemname'),
    'mlcl': DmapTag('container', 'dmap.listing'),
    'mlid': DmapTag(read_uint,   'dmap.sessionid'),
    'mlit': DmapTag('container', 'dmap.listingitem'),
    'mlog': DmapTag('container', 'dmap.loginresponse'),
    'mpro': DmapTag(read_uint,   'dmap.protocolversion'),
    'mrco': DmapTag(read_uint,   'dmap.returnedcount'),
    'msal': DmapTag(read_bool,   'dmap.supportsautologout'),
    'msbr': DmapTag(read_bool,   'dmap.supportsbrowse'),
    'msdc': DmapTag(read_uint,   'dmap.databasescount'),
    'msed': DmapTag(read_bool,   'dmap.supportsedit'),
    'msex': DmapTag(read_bool,   'dmap.supportsextensions'),
    'msix': DmapTag(read_bool,   'dmap.supportsindex'),
    'mslr': DmapTag(read_bool,   'dmap.loginrequired'),
    'mspi': DmapTag(read_bool,   'dmap.supportspersistentids'),
    'msqy': DmapTag(read_bool,   'dmap.supportsquery'),
    'msrv': DmapTag('container', 'dmap.serverinforesponse'),
    'mstc': DmapTag(read_uint,   'dmap.utctime'),
    'mstm': DmapTag(read_uint,   'dmap.timeoutinterval'),
    'msto': DmapTag(read_uint,   'dmap.utcoffset'),
    'mstt': DmapTag(read_uint,   'dmap.status'),
    'msup': DmapTag(read_bool,   'dmap.supportsupdate'),
    'mtco': DmapTag(read_uint,   'dmap.containercount'),

    # Tags with (yet) unknown purpose
    'aeFR': DmapTag(read_uint,   'unknown tag'),
    'aeSX': DmapTag(read_uint,   'unknown tag'),
    'asse': DmapTag(read_uint,   'unknown tag'),
    'atCV': DmapTag(read_uint,   'unknown tag'),
    'atSV': DmapTag(read_uint,   'unknown tag'),
    'caks': DmapTag(read_uint,   'unknown tag'),
    'caov': DmapTag(read_uint,   'unknown tag'),
    'casc': DmapTag(read_uint,   'unknown tag'),
    'cass': DmapTag(read_uint,   'unknown tag'),
    'ceQA': DmapTag(read_uint,   'unknown tag'),
    'cmbe': DmapTag(read_str,    'unknown tag'),
    'cmcc': DmapTag(read_str,    'unknown tag'),
    'cmce': DmapTag(read_str,    'unknown tag'),
    'cmcv': DmapTag(read_ignore, 'unknown tag'),
    'cmik': DmapTag(read_uint,   'unknown tag'),
    'cmsb': DmapTag(read_uint,   'unknown tag'),
    'cmsc': DmapTag(read_uint,   'unknown tag'),
    'cmsp': DmapTag(read_uint,   'unknown tag'),
    'cmsv': DmapTag(read_uint,   'unknown tag'),
    'cmte': DmapTag(read_str,    'unknown tag'),
    'mscu': DmapTag(read_uint,   'unknown tag'),
}


def lookup_tag(name):
    """Look up a tag based on its key. Returns a DmapTag."""
    return next((_TAGS[t] for t in _TAGS if t == name),
                DmapTag(_read_unknown, 'unknown tag'))
