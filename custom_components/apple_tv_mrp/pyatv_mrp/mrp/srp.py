"""Prototype code for MRP."""

import os
import uuid
import binascii
import hashlib
import logging

import curve25519
from srptools import (SRPContext, SRPClientSession, constants)
from ed25519.keys import SigningKey, VerifyingKey

from .. import exceptions
from ..log import log_binary
from . import (tlv8, chacha20)

_LOGGER = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class Credentials:
    """Identifiers and encryption keys used by MRP."""

    def __init__(self, ltpk, ltsk, atv_id, client_id):
        """Initialize a new Credentials."""
        self.ltpk = ltpk
        self.ltsk = ltsk
        self.atv_id = atv_id
        self.client_id = client_id

    @classmethod
    def parse(cls, detail_string):
        """Parse a string represention of Credentials."""
        split = detail_string.split(':')
        if len(split) != 4:
            raise Exception('invalid credentials')  # TODO: other exception

        ltpk = binascii.unhexlify(split[0])
        ltsk = binascii.unhexlify(split[1])
        atv_id = binascii.unhexlify(split[2])
        client_id = binascii.unhexlify(split[3])
        return Credentials(ltpk, ltsk, atv_id, client_id)

    def __str__(self):
        """Return a string representation of credentials."""
        return '{0}:{1}:{2}:{3}'.format(
            binascii.hexlify(self.ltpk).decode('utf-8'),
            binascii.hexlify(self.ltsk).decode('utf-8'),
            binascii.hexlify(self.atv_id).decode('utf-8'),
            binascii.hexlify(self.client_id).decode('utf-8'))


def hkdf_expand(salt, info, shared_secret):
    """Derive encryption keys from shared secret."""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.backends import default_backend
    hkdf = HKDF(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt.encode(),
        info=info.encode(),
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)


# pylint: disable=too-many-instance-attributes
class SRPAuthHandler:
    """Handle SRP crypto routines for auth and key derivation."""

    def __init__(self):
        """Initialize a new SRPAuthHandler."""
        self.pairing_id = str(uuid.uuid4()).encode()
        self._signing_key = None
        self._auth_private = None
        self._auth_public = None
        self._verify_private = None
        self._verify_public = None
        self._session = None
        self._shared = None
        self._session_key = None
        self._client_session_key = None  # TODO: can remove?

    def initialize(self):
        """Initialize operation by generating new keys."""
        self._signing_key = SigningKey(os.urandom(32))
        self._auth_private = self._signing_key.to_seed()
        self._auth_public = self._signing_key.get_verifying_key().to_bytes()
        self._verify_private = curve25519.Private(secret=os.urandom(32))
        self._verify_public = self._verify_private.get_public()
        return self._auth_public, self._verify_public.serialize()

    def verify1(self, credentials, session_pub_key, encrypted):
        """First verification step."""
        # No additional hashing used
        self._shared = self._verify_private.get_shared_key(
            curve25519.Public(session_pub_key), hashfunc=lambda x: x)

        session_key = hkdf_expand('Pair-Verify-Encrypt-Salt',
                                  'Pair-Verify-Encrypt-Info',
                                  self._shared)

        chacha = chacha20.Chacha20Cipher(session_key, session_key)
        decrypted_tlv = tlv8.read_tlv(
            chacha.decrypt(encrypted, nounce='PV-Msg02'.encode()))

        identifier = decrypted_tlv[tlv8.TLV_IDENTIFIER]
        signature = decrypted_tlv[tlv8.TLV_SIGNATURE]

        if identifier != credentials.atv_id:
            raise Exception('incorrect device response')  # TODO: new exception

        info = session_pub_key + \
            bytes(identifier) + self._verify_public.serialize()
        ltpk = VerifyingKey(bytes(credentials.ltpk))
        ltpk.verify(bytes(signature), bytes(info))  # throws if no match

        device_info = self._verify_public.serialize() + \
            credentials.client_id + session_pub_key

        device_signature = SigningKey(credentials.ltsk).sign(device_info)

        tlv = tlv8.write_tlv({tlv8.TLV_IDENTIFIER: credentials.client_id,
                              tlv8.TLV_SIGNATURE: device_signature})

        return chacha.encrypt(tlv, nounce='PV-Msg03'.encode())

    def verify2(self):
        """Last verification step.

        The derived keys (output, input) are returned here.
        """
        output_key = hkdf_expand('MediaRemote-Salt',
                                 'MediaRemote-Write-Encryption-Key',
                                 self._shared)

        input_key = hkdf_expand('MediaRemote-Salt',
                                'MediaRemote-Read-Encryption-Key',
                                self._shared)

        log_binary(_LOGGER, 'Keys', Output=output_key, Input=input_key)
        return output_key, input_key

    def step1(self, pin):
        """First pairing step."""
        context = SRPContext(
            'Pair-Setup', str(pin),
            prime=constants.PRIME_3072,
            generator=constants.PRIME_3072_GEN,
            hash_func=hashlib.sha512)
        self._session = SRPClientSession(
            context, binascii.hexlify(self._auth_private).decode())

    def step2(self, atv_pub_key, atv_salt):
        """Second pairing step."""
        pk_str = binascii.hexlify(atv_pub_key).decode()
        salt = binascii.hexlify(atv_salt).decode()
        self._client_session_key, _, _ = self._session.process(pk_str, salt)

        if not self._session.verify_proof(self._session.key_proof_hash):
            raise exceptions.AuthenticationError('proofs do not match (mitm?)')

        pub_key = binascii.unhexlify(self._session.public)
        proof = binascii.unhexlify(self._session.key_proof)
        log_binary(_LOGGER, 'Client', Public=pub_key, Proof=proof)
        return pub_key, proof

    def step3(self):
        """Third pairing step."""
        ios_device_x = hkdf_expand(
            'Pair-Setup-Controller-Sign-Salt',
            'Pair-Setup-Controller-Sign-Info',
            binascii.unhexlify(self._client_session_key))

        self._session_key = hkdf_expand(
            'Pair-Setup-Encrypt-Salt',
            'Pair-Setup-Encrypt-Info',
            binascii.unhexlify(self._client_session_key))

        device_info = ios_device_x + self.pairing_id + self._auth_public
        device_signature = self._signing_key.sign(device_info)

        tlv = tlv8.write_tlv({tlv8.TLV_IDENTIFIER: self.pairing_id,
                              tlv8.TLV_PUBLIC_KEY: self._auth_public,
                              tlv8.TLV_SIGNATURE: device_signature})

        chacha = chacha20.Chacha20Cipher(self._session_key, self._session_key)
        encrypted_data = chacha.encrypt(tlv, nounce='PS-Msg05'.encode())
        log_binary(_LOGGER, 'Data', Encrypted=encrypted_data)
        return encrypted_data

    def step4(self, encrypted_data):
        """Last pairing step."""
        chacha = chacha20.Chacha20Cipher(self._session_key, self._session_key)
        decrypted_tlv_bytes = chacha.decrypt(
            encrypted_data, nounce='PS-Msg06'.encode())
        if not decrypted_tlv_bytes:
            raise Exception('data decrypt failed')  # TODO: new exception
        decrypted_tlv = tlv8.read_tlv(decrypted_tlv_bytes)
        _LOGGER.debug('PS-Msg06: %s', decrypted_tlv)

        atv_identifier = decrypted_tlv[tlv8.TLV_IDENTIFIER]
        atv_signature = decrypted_tlv[tlv8.TLV_SIGNATURE]
        atv_pub_key = decrypted_tlv[tlv8.TLV_PUBLIC_KEY]
        log_binary(_LOGGER,
                   'Device',
                   Identifier=atv_identifier,
                   Signature=atv_signature,
                   Public=atv_pub_key)

        # TODO: verify signature here

        return Credentials(atv_pub_key, self._signing_key.to_seed(),
                           atv_identifier, self.pairing_id)
