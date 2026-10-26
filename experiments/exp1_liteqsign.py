"""Experiment 1: signature interface/state/tampering plumbing (demo adapter only)."""
import hashlib
from experiments.common import make_devices, dump_json
from paper2.adapters import DemoHMACAdapter

def run():
    devices, keys = make_devices(1)
    d=devices[0]
    msg=b"temperature=21.5"
    sig=d.signer.sign(msg)
    good=d.signer.verify(msg,sig)
    tampered=d.signer.verify(msg+b";tampered",sig)
    result={"experiment":1,"name":"signature_interface_demo",
            "adapter":d.signer.name,"valid_signature_accepted":good,
            "tampered_message_rejected":not tampered,
            "signature_bytes":len(sig),
            "research_status":"DEMO_ONLY_NOT_LITEQSIGN_NOT_POST_QUANTUM"}
    dump_json("exp1_signature.json",result); print(result); return result
if __name__=="__main__": run()
