#!/usr/bin/env python3
"""Independent docs source/build consistency & GPU contract falsifiers."""
from hashlib import sha256
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
PINNED={
    "CUDA-05D":("ee0ea36bae0950c04e13100c7f53cf7e643c82c4",
                "184dd111bb2d364306cdf5abfe315e0b46405f4e"),
    "CUDA-05E":("84f82a786d80981edd824a2d9c81f4bbfd105c71",
                "f458c47dae8ffe67272d2a947d3ac022a2a79b74"),
    "CUDA-05F":("03ba7945fe6740b2cf35dc28656ba866f66c33fb",
                "7fa4596705f8611a5440a97d5a4556cdf64ac407"),
}
STATUS={"CUDA-05D":("distinct_service_identity_gate","NOT_QUALIFIED"),
        "CUDA-05E":("host_service_principal","PASS")}
def sha(data):return sha256(data).hexdigest()
def check_gpu(record,payload):
    assert payload["schema"]=="gnu6.gpu-evidence-public.v1"
    contract_file=ROOT/"docs"/"experiments"/"GPU-EVIDENCE-CONTRACT-v1.json"
    contract_bytes=contract_file.read_bytes()
    contract=json.loads(contract_bytes)
    assert contract["schema"]=="gnu6.gpu-evidence-contract.v1"
    assert contract["contract_version"]=="1.0.0"
    assert contract["experiment"]=="CUDA-05F-P01"
    assert payload["experiment_id"]==contract["experiment"]
    assert payload["contract_sha256"]==sha(contract_bytes)
    assert set(payload)==set(contract["public_allowlist"])
    assert set(payload["gates"])==set(contract["required_gates"])
    assert all(gate["state"] in contract["allowed_gate_states"]
               for gate in payload["gates"].values())
    for key,gate in payload["gates"].items():
        assert isinstance(gate["observation_ids"],list)
        assert gate["state"]==("NOT_QUALIFIED" if key=="release_authority" else "PASS")
    assert payload["review_status"]=="draft"
    assert payload["production_authorization"]=="DENIED"
    assert record["decision"]=="BOUNDED_OPERATIONAL_PASS_RELEASE_NOT_QUALIFIED"
    assert record["production_authorization"]=="DENIED"
    assert (ROOT/"dist"/"experiments"/contract_file.name).read_bytes()==contract_bytes
    receipt=ROOT/"docs"/"evidence"/"cuda-05f-manifest.json"
    m=json.loads(receipt.read_text())
    assert m["schema"]=="gnu6.evidence-receipt.v1"
    assert m["experiment_id"]==record["id"]
    assert m["source_commit"]==record["source_commit"]
    assert m["protocol_commit"]==record["protocol_commit"]
    assert m["raw_sha256"]==payload["raw_sha256"]
    assert m["public_sha256"]==record["public_sha256"]
    assert m["contract_sha256"]==payload["contract_sha256"]
    assert m["review_status"]=="draft"
    assert m["release_authority"]=="NOT_QUALIFIED"
    assert m["production_authorization"]=="DENIED"
    assert m["external_reproduction"]=="not demonstrated"
    assert (ROOT/"dist"/"evidence"/receipt.name).read_bytes()==receipt.read_bytes()
def assess(reg):
    assert reg["schema"]=="gnu6.experiments.v1"
    assert reg["registry_version"]=="2026-10-09.2"
    assert reg["review_status"]=="draft"
    assert len(reg["entries"])==len(PINNED)==3
    assert [item["id"] for item in reg["entries"]]==list(PINNED)
    seen=set()
    for item in reg["entries"]:
        identifier=item["id"]
        assert identifier in PINNED and identifier not in seen
        seen.add(identifier)
        protocol,source=PINNED[identifier]
        assert item["protocol_commit"]==protocol
        assert item["source_commit"]==source
        assert item["status"]=="draft"
        assert item["review"]=="internal-automated-checks-only"
        assert item["revision"]=="1.0.0-experimental"
        assert item["production_authorization"]=="DENIED"
        assert item["source_visibility"]=="private"
        assert item["external_reproduction"]=="not demonstrated"
        assert item["evidence_class"].startswith("E4 / internal")
        assert re.fullmatch("[0-9a-f]{64}",item["public_sha256"])
        assert re.fullmatch("[0-9a-f]{64}",item["raw_sha256"])
        expected=f'/evidence/{identifier.lower()}-public-results.json'
        assert item["source_file"]==expected
        source_bytes=(ROOT/"docs"/expected.lstrip("/")).read_bytes()
        assert (ROOT/"dist"/expected.lstrip("/")).read_bytes()==source_bytes
        assert sha(source_bytes)==item["public_sha256"]
        payload=json.loads(source_bytes)
        assert payload["protocol_commit"]==protocol
        assert payload["raw_sha256"]==item["raw_sha256"]
        assert payload["production_authorization"]=="DENIED"
        if identifier in STATUS:
            key,value=STATUS[identifier]
            assert payload[key]==value
        else:
            check_gpu(item,payload)
        for locale in ("fr","en"):
            assert item["pages"][locale]==f"/{locale}/studies/{identifier.lower()}.html"
            assert len(item["claim"][locale])>25
            assert len(item["scope"][locale])>20
            study=(ROOT/"dist"/locale/"studies"/(identifier.lower()+".html")).read_text()
            assert identifier+"-P01" in study
            assert f'<html lang="{locale}" data-g6-domain="docs">' in study
            assert item["source_file"] in study
            assert "<h1" in study
            assert "tension_atoi" not in study and "/mnt/workbench" not in study
            page=(ROOT/"dist"/locale/"experiments.html").read_text()
            assert f'<html lang="{locale}" data-g6-domain="docs">' in page
            assert identifier in page and item["pages"][locale] in page
            assert item["source_file"] in page
            assert "DENIED" in page
    assert seen==set(PINNED)
    assert (ROOT/"dist"/"experiments"/"registry.json").read_bytes()==(
        ROOT/"docs"/"experiments"/"registry.json").read_bytes()
def main():
    registry=json.loads((ROOT/"docs"/"experiments"/"registry.json").read_text())
    assess(registry)
    cases=[
        ("production",lambda x:x["entries"][2].__setitem__("production_authorization","APPROVED")),
        ("checksum",lambda x:x["entries"][2].__setitem__("public_sha256","0"*64)),
        ("protocol",lambda x:x["entries"][2].__setitem__("protocol_commit","0"*40)),
        ("inventory",lambda x:x["entries"].pop(2)),
    ]
    for label,mutate in cases:
        forged=json.loads(json.dumps(registry))
        mutate(forged)
        try:assess(forged)
        except (AssertionError,KeyError,ValueError):pass
        else:raise AssertionError(f"falsifier {label} accepted")
    print("EXPERIMENT_REGISTRY_PASS entries=3 locales=2 sources=3 gates=11 authority=DENIED falsifiers=4 rejected")
if __name__=="__main__":main()
