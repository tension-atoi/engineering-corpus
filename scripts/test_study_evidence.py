#!/usr/bin/env python3
"""Publication gate for CUDA-05D: assert claims, privacy projection, paired pages."""
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs"/"evidence"
DIST=ROOT/"dist"/"evidence"
COMMIT="ee0ea36bae0950c04e13100c7f53cf7e643c82c4"
EXPECTED_PUBLIC={
    "schema","protocol_commit","observed_utc","baseline_control",
    "namespace_root_probe","namespace_inside_root","namespace_distinct_host_uid",
    "subordinate_mapping","subordinate_peer_distinct_host_uid",
    "distinct_service_identity_gate","production_authorization","raw_sha256",
    "source_visibility","limits",
}
def check(data,manifest):
    assert set(data)==EXPECTED_PUBLIC
    assert data["schema"]=="CUDA05D.PUBLIC.v1"
    assert data["protocol_commit"]==manifest["preregistration_commit"]==COMMIT
    assert data["baseline_control"]=="PASS"
    assert data["namespace_root_probe"]=="OBSERVED"
    assert data["namespace_inside_root"] is True
    assert data["namespace_distinct_host_uid"] is False
    assert data["subordinate_mapping"]=="mapping_or_connect_unavailable"
    assert data["subordinate_peer_distinct_host_uid"] is False
    assert data["distinct_service_identity_gate"]=="NOT_QUALIFIED"
    assert data["production_authorization"]=="DENIED"
    assert manifest["production_authorization"]=="denied"
    assert manifest["document_status"]=="draft"
    assert manifest["independent_reproduction"]=="unverified-external"
    assert manifest["evidence_visibility"]=="sanitized-public-projection-only"
    assert manifest["underlying_raw_sha256"]==data["raw_sha256"]
    assert re.fullmatch("[0-9a-f]{64}",data["raw_sha256"])
    assert re.fullmatch("[0-9a-f]{64}",manifest["data_sha256"])
    assert "kernel_peer" not in json.dumps(data)
    assert "host_euid" not in json.dumps(data)
    assert "1000" not in json.dumps(data)
    assert "tension_atoi" not in json.dumps(data)
def main():
    datafile=DOC/"cuda-05d-public-results.json"
    manifestfile=DOC/"cuda-05d-manifest.json"
    source=datafile.read_bytes()
    data=json.loads(source)
    manifest=json.loads(manifestfile.read_text())
    check(data,manifest)
    assert manifest["data_sha256"]==hashlib.sha256(source).hexdigest()
    for name in ("cuda-05d-public-results.json","cuda-05d-manifest.json"):
        assert (DIST/name).read_bytes()==(DOC/name).read_bytes()
    for locale in ("fr","en"):
        page=(ROOT/"dist"/locale/"studies"/"cuda-05d.html").read_text()
        sourcepage=(ROOT/"docs"/locale/"studies"/"cuda-05d.md").read_text()
        assert len(re.findall(r"<h1[^>]*>",page))==1
        assert f'<html lang="{locale}" data-g6-domain="docs">' in page
        assert "CUDA-05D-P01" in page and COMMIT in page
        assert "/evidence/cuda-05d-public-results.json" in page
        assert "/evidence/cuda-05d-manifest.json" in page
        assert "/templates/EXPERIMENT.md" in page
        assert "NOT_QUALIFIED" in sourcepage and "DENIED" in sourcepage
        assert "status: draft" in sourcepage
        assert "tension_atoi" not in page
        assert "uid=1000" not in page and "pid=" not in page
    assert (ROOT/"dist"/"templates"/"EXPERIMENT.md").is_file()
    changed=dict(data,distinct_service_identity_gate="QUALIFIED")
    try:check(changed,manifest)
    except AssertionError:pass
    else:raise AssertionError("tampered identity gate accepted")
    broken=dict(manifest,data_sha256="0"*64)
    try:assert broken["data_sha256"]==hashlib.sha256(source).hexdigest()
    except AssertionError:pass
    else:raise AssertionError("tampered digest accepted")
    print("STUDY_EVIDENCE_PASS bilingual=2 artifacts=2 prereg=PINNED privacy=PASS tamper=REJECTED status=DRAFT")

if __name__=="__main__":
    main()
