"""Additional logging methods."""

import logging
import binascii


# Special log method to avoid hexlify conversion if debug is off
def log_binary(logger, message, **kwargs):
    """Log binary data if debug is enabled."""
    if logger.isEnabledFor(logging.DEBUG):
        output = ('{0}={1}'.format(k, binascii.hexlify(
            bytearray(v)).decode()) for k, v in sorted(kwargs.items()))
        logger.debug('%s (%s)', message, ', '.join(output))
