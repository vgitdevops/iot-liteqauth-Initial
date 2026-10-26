"""Experiment 3: test key/session interface only; demo KEM is not a real KEM."""
from experiments.common import dump_json
from paper2.protocol import HostNetwork

def run():
    hn=HostNetwork()
    key, ct=hn.establish_demo_session()
    payload=b"Paper2 test sensor payload"
    nonce, envelope=hn.encrypt_demo_message(key,payload)
    recovered=hn.decrypt_demo_message(key,nonce,envelope)
    result={"experiment":3,"name":"session_and_channel_demo",
            "key_agreement_workflow_completed":True,
            "payload_round_trip":recovered==payload,
            "ciphertext_bytes_demo_envelope":len(envelope),
            "research_status":"DEMO_ONLY_NOT_MLKEM_NOT_AES_GCM"}
    dump_json("exp3_session.json",result); print(result); return result
if __name__=="__main__": run()
