"""Experiment 5: demo timing/throughput for identical per-device workload."""
import time, statistics, json
from experiments.common import make_devices, signer_factory, dump_json, dump_csv, RESULTS
from paper2.protocol import GroupLeader
from paper2.metrics import summarize

def run():
    rows=[]
    for n in [100,250,500,750,1000]:
        trial_times=[]; accepted=[]; throughputs=[]
        for trial in range(10):
            devices, keys=make_devices(n)
            reqs=[d.make_request(f"device={i};temp=21.5".encode()) for i,d in enumerate(devices)]
            gl=GroupLeader(signer_factory(keys))
            t=time.perf_counter(); out=gl.process_batch(reqs); elapsed=time.perf_counter()-t
            trial_times.append(elapsed); accepted.append(out["accepted"])
            throughputs.append(n/elapsed if elapsed else 0)
        row={"devices":n,"trials":len(trial_times),
             "latency_mean_s":statistics.mean(trial_times),
             "latency_median_s":statistics.median(trial_times),
             "latency_stdev_s":statistics.stdev(trial_times),
             "throughput_mean_devices_s":statistics.mean(throughputs),
             "accepted_mean":statistics.mean(accepted),
             "adapter":"DEMO_ONLY_HMAC_NOT_LITEQSIGN",
             "status":"measured_demo_not_journal_claim"}
        rows.append(row)
    dump_csv("exp5_scalability.csv",rows)
    result={"experiment":5,"name":"scalability_demo","rows":rows,
            "note":"Host-machine timings only; not MCU energy, not real LiteQSign, not cryptographic aggregation."}
    dump_json("exp5_scalability.json",result); print(json.dumps(result,indent=2)); return result
if __name__=="__main__": run()
