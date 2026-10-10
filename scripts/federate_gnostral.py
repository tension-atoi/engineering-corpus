#!/usr/bin/env python3
"""Pinned, offline, review-gated federation of public gnostral.rs Markdown.

--sync requires exact commit + local Git checkout; --verify is network-free;
--check-upstream *reports* drift and never changes deployed docs.
This tool does not deploy, merge, or follow mutable branch content at page load.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "federation" / "gnostral"
MANIFEST = BASE / "manifest.json"
PUBLIC_REPOSITORY = "https://github.com/tension-atoi/gnostral.rs"
PATHS = (
    "README.md",
    "QUESTLOG.md",
    "docs/START_HERE.md",
    "docs/CAPABILITY_MATRIX.md",
    "docs/ROADMAP.md",
    "docs/ARCHITECTURE.md",
    "docs/REPRODUCIBILITY.md",
)
SHA40 = re.compile(r"^[a-f0-9]{40}$")
SHA64 = re.compile(r"^[a-f0-9]{64}$")

def git(checkout, *args):
    result = subprocess.run(["git", "-C", str(checkout), *args], capture_output=True, check=True)
    return result.stdout

def load():
    return json.loads(MANIFEST.read_text("utf-8"))

def validate_schema(manifest):
    if manifest.get("schema") != "gnu6.federation.pinned-markdown.v1":
        raise ValueError("unrecognized federation schema")
    if manifest.get("repository") != PUBLIC_REPOSITORY:
        raise ValueError("unexpected upstream owner")
    if not SHA40.fullmatch(manifest.get("source_ref", "")):
        raise ValueError("source must be exact commit")
    files = manifest.get("files")
    if not isinstance(files, dict) or set(files) != set(PATHS):
        raise ValueError("source path allowlist mismatch")
    if not all(SHA64.fullmatch(v) for v in files.values()):
        raise ValueError("invalid pinned SHA-256")

def verify():
    manifest = load()
    validate_schema(manifest)
    for rel, digest in manifest["files"].items():
        src = BASE / "content" / rel
        if not src.is_file() or src.is_symlink() or len(src.read_bytes()) > 128000:
            raise ValueError("missing/unbounded snapshot: " + rel)
        if hashlib.sha256(src.read_bytes()).hexdigest() != digest:
            raise ValueError("snapshot content drift: " + rel)
    return manifest

def sync(checkout, ref):
    if not SHA40.fullmatch(ref):
        raise ValueError("ref must be exact 40-character commit")
    actual = git(checkout, "rev-parse", "--verify", ref+"^{commit}").decode().strip()
    if actual != ref:
        raise ValueError("source ref not a resolvable commit")
    contents = {}
    for rel in PATHS:
        data = git(checkout, "show", ref+":"+rel)
        if len(data) > 128000 or not data or b"\0" in data:
            raise ValueError("source content invalid/unbounded: " + rel)
        if not data.startswith(b"# ") and rel != "QUESTLOG.md":
            raise ValueError("expected Markdown heading: " + rel)
        contents[rel] = data
    new_manifest = {
        "schema": "gnu6.federation.pinned-markdown.v1",
        "repository": PUBLIC_REPOSITORY,
        "source_ref": ref,
        "branch_observed": "main",
        "mode": "reviewed-snapshot; offline static rendering; no live fetch or auto-promotion",
        "files": {k: hashlib.sha256(v).hexdigest() for k,v in contents.items()},
    }
    for rel, data in contents.items():
        dest = BASE / "content" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(new_manifest, sort_keys=True, indent=2)+"\n")
    verify()

def check_upstream(checkout):
    manifest = verify()
    # Network-free when local refs have been explicitly fetched by a reviewer.
    current = git(checkout, "rev-parse", "refs/remotes/origin/main").decode().strip()
    if current == manifest["source_ref"]:
        print("FEDERATION_UPSTREAM_CURRENT", current)
        return 0
    print("FEDERATION_UPDATE_CANDIDATE", "deployed_source="+manifest["source_ref"],
          "latest_fetched_origin_main="+current)
    return 10

def main():
    p=argparse.ArgumentParser(description=__doc__)
    modes=p.add_mutually_exclusive_group(required=True)
    modes.add_argument("--sync", action="store_true")
    modes.add_argument("--verify", action="store_true")
    modes.add_argument("--check-upstream", action="store_true")
    p.add_argument("--source-checkout", type=Path)
    p.add_argument("--ref")
    args=p.parse_args()
    try:
        if args.sync:
            if args.source_checkout is None or args.ref is None:
                p.error("--sync requires --source-checkout and --ref")
            sync(args.source_checkout,args.ref)
        elif args.check_upstream:
            if args.source_checkout is None: p.error("--check-upstream needs checkout")
            return check_upstream(args.source_checkout)
        else:
            verify()
    except (OSError,subprocess.CalledProcessError,ValueError,KeyError) as exc:
        print("FEDERATION_REFUSED",str(exc),file=sys.stderr)
        return 2
    result = verify()
    print("FEDERATION_PINNED_PASS",result["source_ref"],len(PATHS),"Markdown sources")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
