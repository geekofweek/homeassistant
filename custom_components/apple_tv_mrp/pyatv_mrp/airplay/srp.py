"""Implementation of SRP used by AirPlay device authtentication."""

import os
import hashlib
import binascii
import logging

import curve25519
from ed25519.keys import SigningKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from srptools import (SRPContext, SRPClientSession, constants)

from ..log import log_binary
from ..exceptions import (NoCredentialsError, AuthenticationError)

_LOGGER = logging.getLogger(__name__)


def hash_sha512(*indata):
    """Create SHA512 hash for input arguments."""
    hasher = hashlib.sha512()
    for data in indata:
        if isinstance(data, str):
            hasher.update(data.encode('utf-8'))
        elif isinstance(data, bytes):
            hasher.update(data)
        else:
            raise Exception('invalid input data: ' + str(data))
    return hasher.digest()


def aes_encrypt(mode, aes_key, aes_iv, *data):
    """Encrypt data with AES in specified mode."""
    encryptor = Cipher(
        algorithms.AES(aes_key),
        mode(aes_iv),
        backend=default_backend()).encryptor()

    result = None
    for value in data:
        result = encryptor.update(value)
    encryptor.finalize()

    return result, None if not hasattr(encryptor, 'tag') else encryptor.tag


def new_credentials():
    """Generate a new identifier and seed for authentication.

    Use the returned values in the following way:
    * The identifier shall be passed as username to SRPAuthHandler.step1
    * Seed shall be passed to SRPAuthHandler constructor
    """
    identifier = binascii.b2a_hex(os.urandom(8)).decode().upper()
    seed = binascii.b2a_hex(os.urandom(32))  # Corresponds to private key
    return identifier, seed


class AtvSRPContext(SRPContext):
    """Custom context implementation for Apple TV."""

    def get_common_session_key(self, premaster_secret):
        """K = H(S).

        Special implementation for Apple TV.
        """
        k_1 = self.hash(premaster_secret, b'\x00\x00\x00\x00', as_bytes=True)
        k_2 = self.hash(premaster_secret, b'\x00\x00\x00\x01', as_bytes=True)
        return k_1 + k_2


class SRPAuthHandler:
    """Handle SRP data and crypto routines for auth and verification."""

    def __init__(self):
        """Initialize a new SRPAuthHandler."""
        self.seed = None
        self.session = None
        self.client_session_key = None  # TODO: can this be removed?
        self._auth_private = None
        self._auth_public = None
        self._verify_private = None
        self._verify_public = None

    def initialize(self, seed=None):
        """Initialize handler operation.

        This method will generate new encryption keys and must be called prior
        to doing authentication or verification.
        """
        self.seed = seed or os.urandom(32)  # Generate new seed if not provided
        signing_key = SigningKey(self.seed)
        verifying_key = signing_key.get_verifying_key()
        self._auth_private = signing_key.to_seed()
        self._auth_public = verifying_key.to_bytes()
        log_binary(_LOGGER,
                   'Authentication keys',
                   Private=self._auth_private,
                   Public=self._auth_public)

    def verify1(self):
        """First device verification step."""
        self._check_initialized()
        self._verify_private = curve25519.Private(secret=self.seed)
        self._verify_public = self._verify_private.get_public()
        log_binary(_LOGGER,
                   'Verification keys',
                   Private=self._verify_private.serialize(),
                   Public=self._verify_public.serialize())
        verify_public = self._verify_public.serialize()
        return b'\x01\x00\x00\x00' + verify_public + self._auth_public

    def verify2(self, atv_public_key, data):
        """Last device verification step."""
        self._check_initialized()
        log_binary(_LOGGER, 'Verify', PublicSecret=atv_public_key, Data=data)

        # Generate a shared secret key
        public = curve25519.Public(atv_public_key)
        shared = self._verify_private.get_shared_key(
            public, hashfunc=lambda x: x)  # No additional hashing used
        log_binary(_LOGGER, 'Shared secret', Secret=shared)

        # Derive new AES key and IV from shared key
        aes_key = hash_sha512('Pair-Verify-AES-Key', shared)[0:16]
        aes_iv = hash_sha512('Pair-Verify-AES-IV', shared)[0:16]
        log_binary(_LOGGER, 'Pair-Verify-AES', Key=aes_key, IV=aes_iv)

        # Sign public keys and encrypt with AES
        signer = SigningKey(self._auth_private)
        signed = signer.sign(self._verify_public.serialize() + atv_public_key)
        signature, _ = aes_encrypt(modes.CTR, aes_key, aes_iv, data, signed)
        log_binary(_LOGGER, 'Signature', Signature=signature)

        # Signature is prepended with 0x00000000 (alignment?)
        return b'\x00\x00\x00\x00' + signature

    def step1(self, username, password):
        """First authentication step."""
        self._check_initialized()
        context = AtvSRPContext(
            str(username), str(password),
            prime=constants.PRIME_2048,
            generator=constants.PRIME_2048_GEN)
        self.session = SRPClientSession(
            context, binascii.hexlify(self._auth_private).decode())

    def step2(self, pub_key, salt):
        """Second authentication step."""
        self._check_initialized()
        pk_str = binascii.hexlify(pub_key).decode()
        salt = binascii.hexlify(salt).decode()
        self.client_session_key, _, _ = self.session.process(pk_str, salt)
        _LOGGER.debug('Client session key: %s', self.client_session_key)

        # Generate client public and session key proof.
        client_public = self.session.public
        client_session_key_proof = self.session.key_proof
        _LOGGER.debug('Client public: %s, proof: %s',
                      client_public, client_session_key_proof)

        if not self.session.verify_proof(self.session.key_proof_hash):
            raise AuthenticationError('proofs do not match (mitm?)')
        return client_public, client_session_key_proof

    def step3(self):
        """Last authentication step."""
        self._check_initialized()
        # TODO: verify: self.client_session_key same as self.session.key_b64()?
        session_key = binascii.unhexlify(self.client_session_key)

        aes_key = hash_sha512('Pair-Setup-AES-Key', session_key)[0:16]
        tmp = bytearray(hash_sha512('Pair-Setup-AES-IV', session_key)[0:16])
        tmp[-1] = tmp[-1] + 1  # Last byte must be increased by 1
        aes_iv = bytes(tmp)
        log_binary(_LOGGER, 'Pair-Setup-AES', Key=aes_key, IV=aes_iv)

        epk, tag = aes_encrypt(modes.GCM, aes_key, aes_iv, self._auth_public)
        log_binary(_LOGGER, 'Pair-Setup EPK+Tag', EPK=epk, Tag=tag)

        return epk, tag

    def _check_initialized(self):
        if not self.seed:
            raise NoCredentialsError()
