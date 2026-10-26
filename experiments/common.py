from pathlib import Path
import sys, json, csv, secrets, hashlib
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from paper2.adapters import DemoHMACAdapter
from paper2.protocol import Device, GroupLeader, HostNetwork

RESULTS = ROOT/"results"
RESULTS.mkdir(exist_ok=True)

def make_devices(n):
    secrets_by_id = {f"dev-{i:05d}": secrets.token_bytes(32) for i in range(n)}
    devices = [Device(did, sec) for did, sec in secrets_by_id.items()]
    return devices, secrets_by_id

def signer_factory(secrets_by_id):
    return lambda did: DemoHMACAdapter(secrets_by_id[did])

def dump_json(name, obj):
    (RESULTS/name).write_text(json.dumps(obj, indent=2), encoding="utf-8")

def dump_csv(name, rows):
    path=RESULTS/name
    if not rows:
        path.write_text("", encoding="utf-8"); return
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
