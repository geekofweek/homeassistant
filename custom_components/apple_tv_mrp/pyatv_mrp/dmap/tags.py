"""Util functions for extracting and constructing DMAP data."""

import plistlib


def read_str(data, start, length):
    """Extract a string from a position in a sequence."""
    return data[start:start+length].decode('utf-8')


def read_uint(data, start, length):
    """Extract a uint from a position in a sequence."""
    return int.from_bytes(data[start:start+length], byteorder='big')


def read_bool(data, start, length):
    """Extract a boolean from a position in a sequence."""
    return read_uint(data, start, length) == 1


def read_bplist(data, start, length):
    """Extract a binary plist from a position in a sequence."""
    # TODO: pylint doesn't find FMT_BINARY, why?
    # pylint: disable=no-member
    return plistlib.loads(data[start:start+length],
                          fmt=plistlib.FMT_BINARY)


# pylint: disable=unused-argument
def read_ignore(data, start, length):
    """Use this to ignore data for all input."""


def uint8_tag(name, value):
    """Create a DMAP tag with uint8 data."""
    return name.encode('utf-8') + \
        b'\x00\x00\x00\x01' + \
        value.to_bytes(1, byteorder='big')


def uint16_tag(name, value):
    """Create a DMAP tag with uint16 data."""
    return name.encode('utf-8') + \
        b'\x00\x00\x00\x02' + \
        value.to_bytes(2, byteorder='big')


def uint32_tag(name, value):
    """Create a DMAP tag with uint32 data."""
    return name.encode('utf-8') + \
        b'\x00\x00\x00\x04' + \
        value.to_bytes(4, byteorder='big')


def uint64_tag(name, value):
    """Create a DMAP tag with uint64 data."""
    return name.encode('utf-8') + \
        b'\x00\x00\x00\x08' + \
        value.to_bytes(8, byteorder='big')


def bool_tag(name, value):
    """Create a DMAP tag with boolean data."""
    return name.encode('utf-8') + \
        b'\x00\x00\x00\x01' + \
        (b'\x01' if value else b'\x00')


def raw_tag(name, value):
    """Create a DMAP tag with raw data."""
    return name.encode('utf-8') + \
        len(value).to_bytes(4, byteorder='big') + \
        value


def string_tag(name, value):
    """Create a DMAP tag with string data."""
    return name.encode('utf-8') + \
        len(value).to_bytes(4, byteorder='big') + \
        value.encode('utf-8')


def container_tag(name, data):
    """Create a DMAP tag with string data."""
    return raw_tag(name, data)  # Same as raw
