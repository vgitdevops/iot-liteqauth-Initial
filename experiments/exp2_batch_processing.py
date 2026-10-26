"""Experiment 2: per-device verification and batch summary, not crypto aggregation."""
from experiments.common import make_devices, signer_factory, dump_json
from paper2.protocol import GroupLeader

def run(n=100):
    devices, keys=make_devices(n)
    requests=[d.make_request(f"payload-{i}".encode()) for i,d in enumerate(devices)]
    gl=GroupLeader(signer_factory(keys))
    result=gl.process_batch(requests)
    result.update({"experiment":2,"name":"per_device_batch_processing",
                   "cryptographic_aggregation":False,
                   "research_status":"DEMO_ONLY"})
    dump_json("exp2_batch.json",result); print({k:v for k,v in result.items() if k!="individual_results"}); return result
if __name__=="__main__": run()
