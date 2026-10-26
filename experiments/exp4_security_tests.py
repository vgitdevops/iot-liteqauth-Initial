"""Experiment 4: negative tests for demo protocol plumbing."""
from experiments.common import make_devices, signer_factory, dump_json
from paper2.protocol import GroupLeader, HostNetwork

def run():
    devices, keys=make_devices(3)
    reqs=[d.make_request(f"payload-{i}".encode()) for i,d in enumerate(devices)]
    # Tamper a signature
    bad=dict(reqs[1]); bad["signature"]=bytes([reqs[1]["signature"][0]^1])+reqs[1]["signature"][1:]
    # Replay first valid request after it has already been accepted
    gl=GroupLeader(signer_factory(keys))
    first=gl.process_batch([reqs[0]])
    replay_ok, replay_reason=gl.verify_one(reqs[0])
    # Revocation
    gl_rev=GroupLeader(signer_factory(keys), revoked_ids={reqs[2]["device_id"]})
    revoked_ok, revoked_reason=gl_rev.verify_one(reqs[2])
    # Invalid signature
    gl_bad=GroupLeader(signer_factory(keys))
    bad_ok, bad_reason=gl_bad.verify_one(bad)
    # Tamper demo envelope
    hn=HostNetwork(); key,_=hn.establish_demo_session()
    nonce, env=hn.encrypt_demo_message(key,b"abc")
    altered=env[:-1]+bytes([env[-1]^1])
    try: hn.decrypt_demo_message(key,nonce,altered); envelope_rejected=False
    except ValueError: envelope_rejected=True
    result={"experiment":4,"name":"negative_protocol_tests",
      "invalid_signature_rejected":not bad_ok,
      "replay_rejected":not replay_ok,
      "revoked_device_rejected":not revoked_ok,
      "altered_envelope_rejected":envelope_rejected,
      "replay_reason":replay_reason,"revocation_reason":revoked_reason,"invalid_reason":bad_reason,
      "research_status":"DEMO_ONLY"}
    dump_json("exp4_security_tests.json",result); print(result); return result
if __name__=="__main__": run()
