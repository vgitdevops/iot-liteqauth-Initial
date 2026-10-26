"""Experiment 6: create reproducibility metadata and artifact manifest."""
import platform, sys, hashlib, json, subprocess
from experiments.common import ROOT, dump_json, RESULTS

def run():
    manifest=[]
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and "results" not in p.parts and "__pycache__" not in p.parts and p.name!="manifest.json":
            manifest.append({"path":str(p.relative_to(ROOT)),
                             "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
                             "bytes":p.stat().st_size})
    result={"experiment":6,"name":"reproducibility_manifest",
            "python_version":sys.version,"platform":platform.platform(),
            "files":len(manifest),"manifest":manifest,
            "requirements":"Python 3.10+ standard library for demo",
            "research_status":"metadata generated; external reference cryptography not integrated"}
    dump_json("exp6_manifest.json",result); print({"experiment":6,"files":len(manifest),"platform":result["platform"]}); return result
if __name__=="__main__": run()
