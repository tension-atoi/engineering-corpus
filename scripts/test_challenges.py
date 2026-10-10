#!/usr/bin/env python3
"""Public scientific challenge readiness is separate from lab pass / deploy authority."""
from pathlib import Path
import json
from hashlib import sha256
ROOT=Path(__file__).resolve().parents[1]
def audit(manifest):
    assert manifest["schema"]=="gnu6.public-challenges.v1"
    assert manifest["publication_status"]=="DRAFT_OPEN_FOR_REVIEW"
    forge=manifest["forge"]
    assert forge["service"]=="GitHub" and forge["url"]=="https://github.com/tension-atoi/engineering-corpus"
    # Reject impossible public contribution claims until HTTP/DNS/auth and repo tests pass.
    assert forge["anonymous_read"]=="AVAILABLE"
    assert forge["public_submissions"]=="AVAILABLE_VIA_GITHUB_ACCOUNT"
    assert manifest["mirror"]["service"]=="Gitea"
    assert manifest["mirror"]["state"]=="NOT_CONFIGURED_AS_PUBLIC_MIRROR"
    expected=["CUDA-05D","CUDA-05E","CUDA-05F","CUDA-05H"]
    assert [c["id"] for c in manifest["challenges"]]==expected
    assert len(manifest["challenges"])==4
    for c in manifest["challenges"]:
        assert c["public_kit"] in ("INCOMPLETE","PARTIAL_ORIGINAL_WITH_OPEN_IPC_FIXTURE","PARTIAL_PROTOCOL_NO_RUNTIME_SOURCE","OPEN_INDEPENDENT_COMPUTE_WITNESS_NOT_PRIVATE_RUNTIME")
        assert len(c["required_artifacts"])>=5
        for lang in ("fr","en"):
            assert len(c["hypothesis"][lang])>=30
            assert len(c["counterexample"][lang])>=30
    fixture=next(x for x in manifest["challenges"] if x["id"]=="CUDA-05E")
    assert fixture["replication_kit"]["experiment_id"]=="CUDA-05G-P01"
    assert fixture["replication_kit"]["status"]=="LOCAL_PASS_EXTERNAL_REPLICATION_PENDING"
    assert fixture["replication_kit"]["original_cuda05f_runtime_replicated"] is False
    gpu=next(c for c in manifest["challenges"] if c["id"]=="CUDA-05H")
    assert gpu["replication_kit"]["experiment_id"]=="CUDA-05H-P01"
    assert gpu["replication_kit"]["status"]=="ONE_LOCAL_PASS_EXTERNAL_REPLICATION_PENDING"
    assert gpu["replication_kit"]["original_cuda05f_runtime_replicated"] is False
    assert gpu["public_kit"]=="OPEN_INDEPENDENT_COMPUTE_WITNESS_NOT_PRIVATE_RUNTIME"
    for lang in ("fr","en"):
        output=(ROOT/"dist"/lang/"challenges.html").read_text()
        assert f'<html lang="{lang}" data-g6-domain="docs">' in output
        assert all(name in output for name in expected)
        assert "/challenges/registry.json" in output
        assert "/challenges/CONTRIBUTING.md" in output
        assert "GitHub" in output
        assert "production" in output
        hub=(ROOT/"dist"/lang/"hub.html").read_text()
        assert f'/{lang}/challenges.html' in hub
        assert f'/{lang}/guides.html' in hub
        assert f'/{lang}/releases.html' in hub
    assert (ROOT/"dist"/"challenges"/"registry.json").read_bytes()==(
        ROOT/"docs"/"challenges"/"registry.json").read_bytes()
    assert (ROOT/"dist"/"challenges"/"CONTRIBUTING.md").read_bytes()==(
        ROOT/"docs"/"challenges"/"CONTRIBUTING.md").read_bytes()
    prov=json.loads((ROOT/"docs"/"challenges"/"PROVENANCE.json").read_text())
    assert prov["schema"]=="gnu6.public-protocol-provenance.v1"
    assert set(prov["protocols"])=={"CUDA-05E","CUDA-05F"}
    expected_hash={"CUDA-05E":"2e83c87c7c409fee84faf037e76ce9f8eda8e95724d1625fa3004c7fa6b6cc60",
                   "CUDA-05F":"f59e14252120bb6e66883c955b4193d25fd49e995b87c988307d62b9f22f0a5a"}
    for id, entry in prov["protocols"].items():
        rel=entry["path"].lstrip("/")
        original=(ROOT/"docs"/rel).read_bytes()
        built=(ROOT/"dist"/rel).read_bytes()
        assert original==built and sha256(original).hexdigest()==entry["sha256"]==expected_hash[id]
        assert entry["runtime_source_public"] is False
    assert (ROOT/"dist"/"challenges"/"PROVENANCE.json").read_bytes()==(
        ROOT/"docs"/"challenges"/"PROVENANCE.json").read_bytes()
    for filename in ("replication.yml","counterexample.yml","config.yml"):
        assert (ROOT/".github"/"ISSUE_TEMPLATE"/filename).is_file()
    experimental=json.loads((ROOT/"docs"/"experiments"/"registry.json").read_text())
    assert [record["id"] for record in experimental["entries"]]==expected[:3]
    assert all(record["production_authorization"]=="DENIED" for record in experimental["entries"])
def main():
    manifest=json.loads((ROOT/"docs"/"challenges"/"registry.json").read_text())
    audit(manifest)
    forged=json.loads(json.dumps(manifest))
    forged["forge"]["anonymous_read"]="BLOCKED"
    try:audit(forged)
    except AssertionError:pass
    else:raise AssertionError("unexpected GitHub public-read state accepted")
    forged=json.loads(json.dumps(manifest))
    forged["challenges"][2]["public_kit"]="OPEN"
    try:audit(forged)
    except AssertionError:pass
    else:raise AssertionError("fabricated public reproducibility kit accepted")
    print("SCIENTIFIC_CHALLENGES_PASS studies=4 locales=2 forge=GITHUB_PUBLIC kits=PARTIAL falsifiers=2 rejected")
if __name__=="__main__":main()
