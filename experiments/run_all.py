"""Collective implementation: executes all six modules and writes a common summary."""
import json, time, csv
from experiments.common import dump_json, dump_csv, RESULTS
from experiments import exp1_liteqsign, exp2_batch_processing, exp3_key_establishment
from experiments import exp4_security_tests, exp5_benchmark, exp6_reproducibility

def run():
    start=time.perf_counter()
    r1=exp1_liteqsign.run()
    r2=exp2_batch_processing.run(n=1000)
    r3=exp3_key_establishment.run()
    r4=exp4_security_tests.run()
    r5=exp5_benchmark.run()
    r6=exp6_reproducibility.run()
    common={
      "mode":"DEMO_ONLY",
      "common_workload":"device identity + sequence + nonce + payload digest + signature; group processing; session/channel plumbing",
      "individual_experiments_completed":6,
      "signature_demo_pass":r1["valid_signature_accepted"] and r1["tampered_message_rejected"],
      "batch_all_accepted":r2["accepted"]==1000 and r2["rejected"]==0,
      "session_demo_pass":r3["key_agreement_workflow_completed"] and r3["payload_round_trip"],
      "negative_tests_pass":all([r4["invalid_signature_rejected"],r4["replay_rejected"],r4["revoked_device_rejected"],r4["altered_envelope_rejected"]]),
      "scalability_rows":len(r5["rows"]),
      "reproducibility_manifest_files":r6["files"],
      "collective_elapsed_seconds":time.perf_counter()-start,
      "not_established":["actual LiteQSign correctness/security","SIS aggregation","ML-KEM interoperability","AES-256-GCM","MCU energy","post-quantum security","journal-grade performance"]
    }
    dump_json("collective_summary.json",common)
    rows=[
      {"experiment":1,"result":"valid accepted and tampered message rejected" if common["signature_demo_pass"] else "FAIL","status":"demo measured"},
      {"experiment":2,"result":f"{r2['accepted']}/{r2['members']} accepted in 1000-device demo batch","status":"demo measured; individual verification"},
      {"experiment":3,"result":"session workflow and payload round-trip passed" if common["session_demo_pass"] else "FAIL","status":"demo only; not real KEM/AES-GCM"},
      {"experiment":4,"result":"invalid signature, replay, revocation and tampering rejected" if common["negative_tests_pass"] else "FAIL","status":"demo tests"},
      {"experiment":5,"result":f"{len(r5['rows'])} workload sizes benchmarked","status":"host demo timings; not journal claims"},
      {"experiment":6,"result":f"{r6['files']} source files hashed in manifest","status":"reproducibility metadata"}
    ]
    dump_csv("experiment_results_table.csv",rows)
    print("\\nCOLLECTIVE SUMMARY\\n"+json.dumps(common,indent=2))
    return common
if __name__=="__main__": run()
