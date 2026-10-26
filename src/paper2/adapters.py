"""Demo adapters only. Replace these with reviewed cryptographic implementations.

DemoHMACAdapter is deliberately NOT a digital signature and NOT LiteQSign.
It demonstrates module plumbing and negative tests only.
"""
from __future__ import annotations
import hashlib, hmac, secrets

class DemoHMACAdapter:
    name = "DEMO_ONLY_HMAC_NOT_LITEQSIGN"
    signature_bytes = 32

    def __init__(self, secret: bytes):
        self._secret = secret

    def sign(self, message: bytes) -> bytes:
        return hmac.new(self._secret, message, hashlib.sha3_256).digest()

    def verify(self, message: bytes, signature: bytes) -> bool:
        expected = self.sign(message)
        return hmac.compare_digest(expected, signature)

class DemoKEM:
    """Toy key agreement for integration testing; NOT a KEM and NOT secure."""
    name = "DEMO_ONLY_TOY_KEM"

    @staticmethod
    def encapsulate(shared_secret: bytes | None = None):
        # The shared secret is supplied to both endpoints only to test the workflow.
        secret = shared_secret or secrets.token_bytes(32)
        ciphertext = b"DEMO-KEM:" + hashlib.sha256(secret).digest()
        return ciphertext, secret

    @staticmethod
    def decapsulate(ciphertext: bytes, shared_secret: bytes):
        expected = b"DEMO-KEM:" + hashlib.sha256(shared_secret).digest()
        if not hmac.compare_digest(ciphertext, expected):
            raise ValueError("invalid demo KEM ciphertext")
        return shared_secret

class DemoAEAD:
    """Integrity-protected demo envelope using HMAC; NOT AES-GCM or encryption."""
    name = "DEMO_ONLY_HMAC_ENVELOPE_NOT_AEAD"

    @staticmethod
    def seal(key: bytes, nonce: bytes, plaintext: bytes, aad: bytes = b"") -> bytes:
        # Not confidential. For plumbing tests only.
        body = plaintext
        tag = hmac.new(key, nonce + aad + body, hashlib.sha256).digest()
        return body + tag

    @staticmethod
    def open(key: bytes, nonce: bytes, envelope: bytes, aad: bytes = b"") -> bytes:
        if len(envelope) < 32:
            raise ValueError("invalid envelope")
        body, tag = envelope[:-32], envelope[-32:]
        expected = hmac.new(key, nonce + aad + body, hashlib.sha256).digest()
        if not hmac.compare_digest(tag, expected):
            raise ValueError("authentication failed")
        return body
