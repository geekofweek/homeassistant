"""Network layer for MRP."""

import asyncio
import logging

from ..log import log_binary
from . import chacha20
from . import protobuf
from .variant import (read_variant, write_variant)

_LOGGER = logging.getLogger(__name__)


class MrpConnection(asyncio.Protocol):
    """Network layer that encryptes/decryptes and (de)serializes messages."""

    def __init__(self, host, port, loop):
        """Initialize a new MrpConnection."""
        self.host = str(host)  # TODO: which datatype do I want here?
        self.port = port
        self.loop = loop
        self.listener = None
        self._buffer = b''
        self._chacha = None
        self._transport = None

    def connection_made(self, transport):
        """Device connection was made."""
        _LOGGER.debug('Connected to device')
        self._transport = transport

    def connection_lost(self, exc):
        """Device connection was dropped."""
        _LOGGER.debug('Disconnected from device: %s', exc)
        self._transport = None

    def enable_encryption(self, output_key, input_key):
        """Enable encryption with the specified keys."""
        self._chacha = chacha20.Chacha20Cipher(output_key, input_key)

    @property
    def connected(self):
        """If a connection is open or not."""
        return self._transport is not None

    def connect(self):
        """Connect to device."""
        return self.loop.create_connection(lambda: self, self.host, self.port)

    def close(self):
        """Close connection to device."""
        if self._transport:
            self._transport.close()
        self._transport = None
        self._chacha = None

    def send(self, message):
        """Send message to device."""
        serialized = message.SerializeToString()

        log_binary(_LOGGER, '>> Send', Data=serialized)
        if self._chacha:
            serialized = self._chacha.encrypt(serialized)
            log_binary(_LOGGER, '>> Send', Encrypted=serialized)

        data = write_variant(len(serialized)) + serialized
        self._transport.write(data)
        _LOGGER.debug('>> Send: Protobuf=%s', message)

    # TODO: read messages from buffer with loop
    def data_received(self, data):
        """Message was received from device."""
        # A message might be split over several reads, so we store a buffer and
        # try to decode messages from that buffer
        self._buffer += data
        log_binary(_LOGGER, '<< Receive', Data=data)

        while self._buffer:
            # The variant tells us how much data must follow
            length, raw = read_variant(self._buffer)
            if len(raw) < length:
                _LOGGER.debug(
                    'Require %d bytes but only %d in buffer', length, len(raw))
                break

            data = raw[:length]  # Incoming message (might be encrypted)
            self._buffer = raw[length:]  # Buffer, might contain more messages

            try:
                self._handle_message(data)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.error('Failed to handle message')

    def _handle_message(self, data):
        if self._chacha:
            data = self._chacha.decrypt(data)
            log_binary(_LOGGER, '<< Receive', Decrypted=data)

        parsed = protobuf.ProtocolMessage()
        parsed.ParseFromString(data)
        _LOGGER.debug('<< Receive: Protobuf=%s', parsed)
        if self.listener:
            self.listener.message_received(parsed)
