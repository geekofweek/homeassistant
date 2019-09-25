"""Implementation of TLV8 used by MRP/HomeKit pairing process.

Note that this implementation only supports one level of value, i.e. no dicts
in dicts.
"""

# Some of the defined tags used by the pairing process
TLV_METHOD = '0'
TLV_IDENTIFIER = '1'
TLV_SALT = '2'
TLV_PUBLIC_KEY = '3'
TLV_PROOF = '4'
TLV_ENCRYPTED_DATA = '5'
TLV_SEQ_NO = '6'
TLV_BACK_OFF = '8'
TLV_SIGNATURE = '10'


def read_tlv(data):
    """Parse TLV8 bytes into a dict.

    If value is larger than 255 bytes, it is split up in multiple chunks. So
    the same tag might occurr several times.
    """
    def _parse(data, pos, size, result=None):
        if result is None:
            result = {}
        if pos >= size:
            return result

        tag = str(data[pos])
        length = data[pos+1]
        value = data[pos+2:pos+2+length]

        if tag in result:
            result[tag] += value  # value > 255 is split up
        else:
            result[tag] = value
        return _parse(data, pos+2+length, size, result)

    return _parse(data, 0, len(data))


def write_tlv(data):
    """Convert a dict to TLV8 bytes."""
    tlv = b''
    for key, value in data.items():
        tag = bytes([int(key)])
        length = len(value)
        pos = 0

        # A tag with length > 255 is added multiple times and concatenated into
        # one buffer when reading the TLV again.
        while pos < len(value):
            size = min(length, 255)
            tlv += tag
            tlv += bytes([size])
            tlv += value[pos:pos+size]
            pos += size
            length -= size
    return tlv
