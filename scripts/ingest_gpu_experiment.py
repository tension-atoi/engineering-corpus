#!/usr/bin/env python3
"""Fail-closed, local-only ingestion of externally qualified GPU research evidence.

An internal report can be indexed without authorizing public deployment.
No raw private data is copied to public docs. --write changes only this local worktree.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REL="experiments/blobin-next-01/CUDA-05/methodology"
NAME="CUDA-05F"
PROTOCOL="03ba7945fe6740b2cf35dc28656ba866f66c33fb"
def hashbytes(data): return sha256(data).hexdigest()
def read_git_bytes(repo,rev,path):
    return subprocess.check_output(["git","-C",str(repo),"show",f"{rev}:{path}"])
def validate(source,commit):
    source=source.resolve()
    evidence=source/"evidence"/"05F"
    contract=(ROOT/"docs"/"experiments"/"GPU-EVIDENCE-CONTRACT-v1.json").read_bytes()
    assert contract==(source/"GPU-EVIDENCE-CONTRACT-v1.json").read_bytes(), "contract mismatch"
    specification=json.loads(contract)
    assert specification["schema"]=="gnu6.gpu-evidence-contract.v1"
    assert specification["experiment"]=="CUDA-05F-P01"
    assert specification["contract_version"]=="1.0.0"
    repo=subprocess.check_output(["git","-C",str(source),"rev-parse","--show-toplevel"],
        text=True).strip()
    assert read_git_bytes(repo,commit,REL+"/evidence/05F/05F-public.json")==(
        evidence/"05F-public.json").read_bytes(), "candidate differs from source commit"
    prereg=read_git_bytes(repo,PROTOCOL,REL+"/05F-PREREG.md")
    assert prereg==(source/"05F-PREREG.md").read_bytes()
    # Independent private oracle, not a green summary exported by the producer.
    check=subprocess.run(["python3",str(source/"validate05f.py")],
        capture_output=True,text=True,timeout=15)
    assert check.returncode==0 and "CUDA05F_INDEPENDENT_PASS" in check.stdout, (
        "source independent validator failed: "+check.stdout[-220:]+check.stderr[-220:])
    raw=(evidence/"05F-raw.json").read_bytes()
    raw_data=json.loads(raw)
    assert raw_data["schema"]=="CUDA05F.RAW.v1"
    assert raw_data["experiment_id"]==specification["experiment"]
    published=(evidence/"05F-public.json").read_bytes()
    payload=json.loads(published)
    assert set(payload)==set(specification["public_allowlist"])
    assert payload["schema"]=="gnu6.gpu-evidence-public.v1"
    assert payload["experiment_id"]==specification["experiment"]
    assert payload["contract_sha256"]==hashbytes(contract)
    assert payload["protocol_commit"]==PROTOCOL
    assert payload["raw_sha256"]==hashbytes(raw)
    assert payload["production_authorization"]=="DENIED"
    assert payload["review_status"]=="draft"
    assert set(payload["gates"])==set(specification["required_gates"])
    states={key:value["state"] for key,value in payload["gates"].items()}
    assert all(state in specification["allowed_gate_states"] for state in states.values())
    assert states["release_authority"]=="NOT_QUALIFIED"
    assert all(state=="PASS" for key,state in states.items() if key!="release_authority")
    assert all(isinstance(v["observation_ids"],list) for v in payload["gates"].values())
    forbidden=("/mnt/workbench","tension_atoi","peer_uid=","SERVICE_OBS","socket_owner",
               "host_uid_quad","authorized_uid")
    assert all(word not in published.decode() for word in forbidden)
    return payload,published,raw_data["timestamp_utc"]

def record(payload,body,commit,observed_utc):
    return {
        "id":NAME,"revision":"1.0.0-experimental",
        "date_utc":observed_utc,
        "status":"draft","review":"internal-automated-checks-only",
        "source_commit":commit,"protocol_commit":payload["protocol_commit"],
        "raw_sha256":payload["raw_sha256"],"public_sha256":hashbytes(body),
        "evidence_class":"E4 / internal single observation",
        "decision":"BOUNDED_OPERATIONAL_PASS_RELEASE_NOT_QUALIFIED",
        "production_authorization":"DENIED","source_visibility":"private",
        "external_reproduction":"not demonstrated",
        "claim":{
            "fr":"Le superviseur Rust intégré sous UID hôte distinct exécute CUDA/Vulkan et récupère après pannes de workers dans le laboratoire.",
            "en":"The integrated Rust supervisor under a distinct host UID rendered on CUDA/Vulkan and recovered after worker faults in the lab.",
        },
        "scope":{
            "fr":"Quatre acquisitions conservées, dont trois incomplètes ou négatives; 10 gates de laboratoire réussis, autorité de production refusée.",
            "en":"Four acquisitions retained, three negative or incomplete; ten operational lab gates passed, production authority denied.",
        },
        "source_file":"/evidence/cuda-05f-public-results.json",
        "pages":{lang:f"/{lang}/studies/cuda-05f.html" for lang in ("fr","en")}
    }
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--source-commit",required=True)
    ap.add_argument("--write",action="store_true")
    args=ap.parse_args()
    assert len(args.source_commit)==40 and all(c in "0123456789abcdef" for c in args.source_commit)
    payload,body,observed_utc=validate(args.source,args.source_commit)
    dest=ROOT/"docs"/"evidence"/"cuda-05f-public-results.json"
    receipt_path=ROOT/"docs"/"evidence"/"cuda-05f-manifest.json"
    receipt={"schema":"gnu6.evidence-receipt.v1","experiment_id":NAME,
        "source_commit":args.source_commit,"protocol_commit":payload["protocol_commit"],
        "contract_sha256":payload["contract_sha256"],"raw_sha256":payload["raw_sha256"],
        "public_sha256":hashbytes(body),"observed_utc":observed_utc,
        "operational_gates":"10/10 PASS in one amended lab acquisition",
        "release_authority":"NOT_QUALIFIED", "production_authorization":"DENIED",
        "review_status":"draft","private_raw_access":"not available from public site",
        "external_reproduction":"not demonstrated"}
    receipt_bytes=(json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True)+"\n").encode()
    index=ROOT/"docs"/"experiments"/"registry.json"
    registry=json.loads(index.read_text())
    assert registry["schema"]=="gnu6.experiments.v1" and registry["review_status"]=="draft"
    current={item["id"]:item for item in registry["entries"]}
    assert len(current)==len(registry["entries"])
    current[NAME]=record(payload,body,args.source_commit,observed_utc)
    assert set(current)=={"CUDA-05D","CUDA-05E","CUDA-05F"}
    registry["entries"]=[current[key] for key in ("CUDA-05D","CUDA-05E","CUDA-05F")]
    registry["registry_version"]="2026-10-09.2"
    serialized=json.dumps(registry,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if args.write:
        dest.write_bytes(body)
        receipt_path.write_bytes(receipt_bytes)
        index.write_text(serialized)
        print("DOCS_01G_INGEST_WRITTEN contract="+payload["contract_sha256"][:12]+
              " source_commit="+args.source_commit[:12]+" gate_authority=DENIED")
    else:
        if dest.exists():
            assert dest.read_bytes()==body and receipt_path.read_bytes()==receipt_bytes
            assert index.read_text()==serialized
        print("DOCS_01G_INGEST_CHECK_PASS changes="+("0" if dest.exists() else "pending")+
              " release=DENIED")
if __name__=="__main__":main()
