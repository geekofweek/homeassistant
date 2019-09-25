"""Module to read and write Google protobuf variants."""


def read_variant(variant):
    """Read and parse a binary protobuf variant value."""
    result = 0
    cnt = 0
    for data in variant:
        result |= (data & 0x7f) << (7 * cnt)
        cnt += 1
        if not data & 0x80:
            return result, variant[cnt:]
    raise Exception('invalid variant')


def write_variant(number):
    """Convert an integer to a protobuf variant binary buffer."""
    if number < 128:
        return bytes([number])
    return bytes([(number & 0x7f) | 0x80]) + write_variant(number >> 7)
