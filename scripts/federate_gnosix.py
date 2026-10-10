#!/usr/bin/env python3
"""Pinned GPLv3 Gnosix Markdown snapshots; no mutable refs or runtime fetching."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1] / "docs/federation/gnosix"
MANIFEST = BASE / "manifest.json"
REPO = "https://github.com/tension-atoi/gnosix"
FILES = ("README.md", "docs/status/STATUS.md", "docs/status/ROADMAP.md",
         "docs/evidence/CURRENT.md", "docs/evidence/README.md")
SHA40 = re.compile(r"^[a-f0-9]{40}$")
SHA64 = re.compile(r"^[a-f0-9]{64}$")
def run(*args):
    return subprocess.run(args, check=True, capture_output=True,timeout=30).stdout

def validate(manifest):
    if manifest.get("schema")!="gnu6.federation.pinned-markdown.v1" or manifest.get("repository")!=REPO:
        raise ValueError("unapproved Gnosix repository/schema")
    if not SHA40.fullmatch(manifest.get("source_ref","")):
        raise ValueError("must pin exact SHA")
    files=manifest.get("files")
    if not isinstance(files,dict) or set(files)!=set(FILES) or not all(SHA64.fullmatch(x) for x in files.values()):
        raise ValueError("Gnosix Markdown allowlist or SHA drift")
    if manifest.get("source_license") != "GPL-3.0-or-later":
        raise ValueError("missing source attribution/license boundary")

def verify():
    manifest=json.loads(MANIFEST.read_text())
    validate(manifest)
    for rel,digest in manifest["files"].items():
        path=BASE/"content"/rel
        if not path.is_file() or path.is_symlink():
            raise ValueError("missing snapshot "+rel)
        data=path.read_bytes()
        if not data or len(data)>128000 or hashlib.sha256(data).hexdigest()!=digest:
            raise ValueError("snapshot tampered "+rel)
        data.decode("utf-8")
    return manifest

def sync(checkout, ref):
    if not SHA40.fullmatch(ref) or run("git","-C",str(checkout),"rev-parse",ref+"^{commit}").decode().strip()!=ref:
        raise ValueError("unverified commit identity")
    origin=run("git","-C",str(checkout),"remote","get-url","origin").decode().strip()
    if origin not in (REPO,REPO+".git","git@github.com:tension-atoi/gnosix.git"):
        raise ValueError("source origin not canonical")
    if run("git","-C",str(checkout),"ls-tree",ref,"LICENSE").split()[1] != b"blob":
        raise ValueError("source LICENSE absent")
    blobs={}
    for rel in FILES:
        row=run("git","-C",str(checkout),"ls-tree",ref,"--",rel).decode().split()
        if not row or row[0]!="100644" or row[1]!="blob":
            raise ValueError("Markdown must be a regular non-executable blob: "+rel)
        data=run("git","-C",str(checkout),"show",ref+":"+rel)
        if not data.startswith((b"# ",b"![gnosix")) or len(data)>128000:
            raise ValueError("invalid Markdown source: "+rel)
        data.decode("utf-8")
        blobs[rel]=data
    manifest={"schema":"gnu6.federation.pinned-markdown.v1","repository":REPO,"source_ref":ref,
       "branch_observed":"main","source_license":"GPL-3.0-or-later",
       "mode":"reviewed immutable GitHub snapshot; no live fetch or automatic publishing",
       "files":{rel:hashlib.sha256(data).hexdigest() for rel,data in blobs.items()}}
    for rel,data in blobs.items():
        dest=BASE/"content"/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
    MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
    verify()

def main():
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify",action="store_true")
    group.add_argument("--sync",action="store_true")
    p.add_argument("--source-checkout",type=Path)
    p.add_argument("--ref")
    a=p.parse_args()
    try:
        if a.sync:
            if not a.source_checkout or not a.ref:p.error("need --source-checkout and --ref")
            sync(a.source_checkout,a.ref)
        receipt=verify()
    except (ValueError,OSError,subprocess.CalledProcessError,UnicodeError,IndexError) as e:
        print("GNOSIX_FEDERATION_REFUSED",str(e),file=sys.stderr)
        return 2
    print("GNOSIX_SOURCE_PIN_PASS",receipt["source_ref"],len(FILES),"Markdown files")
    return 0
if __name__=="__main__": raise SystemExit(main())
