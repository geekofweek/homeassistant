"""Parser and data extractor for raw DMAP data.

DMAP is basically TLV (see Wikipedia) where the key is a 4 byte ASCII value,
a four byte big endian unsigned int as length and the data as data. So:

  +---------------+------------------+--------------------+
  | Key (4 bytes) | Length (4 bytes) | Data (Length bytes |
  +---------------+------------------+--------------------+
"""

from collections import namedtuple

from .. import exceptions
from .tags import (read_str, read_uint, read_bplist)


class DmapTag(namedtuple('DmapTag', ['type', 'name'])):
    """Represention of a DMAP tag used when defining a protocol."""

    __slots__ = ()

    def __str__(self):
        """Return a string representation of this tag."""
        if isinstance(self.type, str):
            type_name = self.type
        else:
            type_name = self.type.__name__[5:]
        return '[{}, {}]'.format(type_name, self.name)


def _parse(data, data_len, tag_lookup, pos, ctx=None):
    if ctx is None:
        ctx = []
    if pos >= data_len:
        return ctx

    f_name = read_str(data, pos, 4)
    f_len = read_uint(data, pos+4, 4)
    pos += 8

    tag = tag_lookup(f_name)
    if tag.type == 'container':
        ctx.append({f_name:
                    _parse(data, pos+f_len, tag_lookup, pos, ctx=[])})
    else:
        ctx.append({f_name: tag.type(data, pos, f_len)})

    return _parse(data, data_len, tag_lookup, pos+f_len, ctx)


def parse(data, tag_lookup):
    """Parse raw DAAP data and returns it as a python object."""
    return _parse(data, len(data), tag_lookup, 0, [])


def first(dmap_data, *path):
    """Look up a value given a path in some parsed DMAP data."""
    if not (path and isinstance(dmap_data, list)):
        return dmap_data

    for key in dmap_data:
        if path[0] in key:
            return first(key[path[0]], *path[1:])

    return None


# #TODO: Also a bad method that should be re-written
def pprint(data, tag_lookup, indent=0):
    """Return a pretty formatted string of parsed DMAP data."""
    output = ''
    if isinstance(data, dict):
        for key, value in data.items():
            tag = tag_lookup(key)
            if isinstance(value, (dict, list)) and tag.type is not read_bplist:
                output += '{0}{1}: {2}\n'.format(indent*' ', key, tag)
                output += pprint(value, tag_lookup, indent+2)
            else:
                output += '{0}{1}: {2} {3}\n'.format(
                    indent*' ', key, str(value), tag)
    elif isinstance(data, list):
        for elem in data:
            output += pprint(elem, tag_lookup, indent)
    else:
        raise exceptions.InvalidDmapDataError(
            'invalid dmap data: ' + str(data))
    return output
