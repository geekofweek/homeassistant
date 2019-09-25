"""Transparent encryption layer using Chacha20_Pooly1305."""
from tlslite.utils.chacha20_poly1305 import CHACHA20_POLY1305


class Chacha20Cipher:
    """CHACHA20 encryption/decryption layer."""

    def __init__(self, out_key, in_key):
        """Initialize a new Chacha20Cipher."""
        self._enc_out = CHACHA20_POLY1305(out_key, 'python')
        self._enc_in = CHACHA20_POLY1305(in_key, 'python')
        self._out_counter = 0
        self._in_counter = 0

    def encrypt(self, data, nounce=None):
        """Encrypt data with counter or specified nounce."""
        if nounce is None:
            nounce = self._out_counter.to_bytes(length=8, byteorder='little')
            self._out_counter += 1

        return self._enc_out.seal(b'\x00\x00\x00\x00' + nounce, data, bytes())

    def decrypt(self, data, nounce=None):
        """Decrypt data with counter or specified nounce."""
        if nounce is None:
            nounce = self._in_counter.to_bytes(length=8, byteorder='little')
            self._in_counter += 1

        decrypted = self._enc_in.open(
            b'\x00\x00\x00\x00' + nounce, data, bytes())

        if not decrypted:
            raise Exception('data decrypt failed')  # TODO: new exception

        return bytes(decrypted)
