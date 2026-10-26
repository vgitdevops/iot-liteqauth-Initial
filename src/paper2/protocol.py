from __future__ import annotations
import hashlib, json, secrets, time
from dataclasses import dataclass, asdict
from .adapters import DemoHMACAdapter, DemoKEM, DemoAEAD

@dataclass
class DeviceRecord:
    device_id: str
    secret_hex: str
    revoked: bool = False
    last_sequence: int = -1

class Device:
    def __init__(self, device_id: str, secret: bytes, signer=None):
        self.device_id = device_id
        self.secret = secret
        self.signer = signer or DemoHMACAdapter(secret)
        self.sequence = 0

    def make_request(self, payload: bytes):
        self.sequence += 1
        msg_obj = {
            "device_id": self.device_id,
            "sequence": self.sequence,
            "nonce": secrets.token_hex(12),
            "payload_sha256": hashlib.sha256(payload).hexdigest(),
            "payload": payload.hex(),
        }
        message = json.dumps(msg_obj, sort_keys=True, separators=(",", ":")).encode()
        signature = self.signer.sign(message)
        return {"device_id": self.device_id, "sequence": self.sequence,
                "message": message, "signature": signature, "payload": payload}

class GroupLeader:
    """Per-device verification + batch summary; no cryptographic aggregation."""
    def __init__(self, signer_factory, revoked_ids=None):
        self.signer_factory = signer_factory
        self.revoked_ids = set(revoked_ids or [])
        self.last_sequence = {}

    def verify_one(self, request):
        did = request["device_id"]
        if did in self.revoked_ids:
            return False, "revoked"
        seq = request["sequence"]
        if seq <= self.last_sequence.get(did, 0):
            return False, "replay_or_stale_sequence"
        verifier = self.signer_factory(did)
        if not verifier.verify(request["message"], request["signature"]):
            return False, "invalid_signature"
        self.last_sequence[did] = seq
        return True, "accepted"

    def process_batch(self, requests):
        started = time.perf_counter()
        rows = []
        for req in requests:
            ok, reason = self.verify_one(req)
            rows.append({"device_id": req["device_id"], "accepted": ok, "reason": reason})
        elapsed = time.perf_counter() - started
        return {
            "members": len(requests),
            "accepted": sum(r["accepted"] for r in rows),
            "rejected": sum(not r["accepted"] for r in rows),
            "elapsed_seconds": elapsed,
            "members_per_second": len(requests) / elapsed if elapsed else None,
            "individual_results": rows,
        }

class HostNetwork:
    def __init__(self):
        self.kem = DemoKEM()
        self.aead = DemoAEAD()

    def establish_demo_session(self):
        # Shared secret injection is only for workflow testing, not real key establishment.
        test_shared = secrets.token_bytes(32)
        ciphertext, device_secret = self.kem.encapsulate(test_shared)
        host_secret = self.kem.decapsulate(ciphertext, test_shared)
        if device_secret != host_secret:
            raise RuntimeError("key mismatch")
        session_key = hashlib.sha256(b"Paper2-demo-session-v1" + host_secret).digest()
        return session_key, ciphertext

    def encrypt_demo_message(self, session_key: bytes, payload: bytes):
        nonce = secrets.token_bytes(12)
        envelope = self.aead.seal(session_key, nonce, payload, b"Paper2-demo")
        return nonce, envelope

    def decrypt_demo_message(self, session_key: bytes, nonce: bytes, envelope: bytes):
        return self.aead.open(session_key, nonce, envelope, b"Paper2-demo")
