#!/usr/bin/env python3
"""DOCS-FEDERATION-03: fail-closed drift detection and review-PR preparation.

No app deployment, merges, branch protection changes or automatic release.
No access to models, credentials, or arbitrary repositories from source docs.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import federate_gnostral as federation

CANONICAL = "https://github.com/tension-atoi/gnostral.rs"
TARGET_REPO = "tension-atoi/engineering-corpus"
SHA40 = re.compile(r"^[a-f0-9]{40}$")
BRANCH = "docs/gnostral-refresh-"
GATE = ("scripts/build.py", "scripts/check.py")
PYTHON = sys.executable

class Refused(ValueError):
    pass

def run(*cmd: str, cwd: Path | None = None) -> str:
    return subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True, timeout=150).stdout.strip()

def is_ancestor(checkout: Path, old: str, new: str) -> bool:
    return subprocess.run(["git", "-C", str(checkout), "merge-base", "--is-ancestor", old, new],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,timeout=10).returncode == 0

def check_source_remote(checkout: Path) -> None:
    remote = run("git", "-C", str(checkout), "remote", "get-url", "origin")
    if remote not in (CANONICAL, CANONICAL+".git", "git@github.com:tension-atoi/gnostral.rs.git"):
        raise Refused("source checkout origin is not the canonical public repository")

def source_bytes(checkout: Path, sha: str, path: str) -> bytes:
    mode = run("git", "-C", str(checkout), "ls-tree", sha, "--", path).split()
    if len(mode)<3 or mode[0]!="100644" or mode[1]!="blob":
        raise Refused(f"{path}: missing regular, non-executable Markdown blob")
    raw = subprocess.run(["git", "-C", str(checkout), "show", sha+":"+path],
                         check=True,capture_output=True,timeout=20).stdout
    if not raw or len(raw) > 128000 or b"\0" in raw:
        raise Refused(f"{path}: invalid size or binary content")
    # Source is never run. Reject raw active HTML and non-HTTPS markdown links
    # before it can be included in the public website.
    text = raw.decode("utf-8")
    if re.search(r"<\s*(script|iframe|object|embed|form|svg|style)\b", text,re.I):
        raise Refused(f"{path}: active HTML must be reviewed as source only")
    if re.search(r"\]\(\s*(javascript:|data:|file:)",text,re.I):
        raise Refused(f"{path}: unsafe Markdown URL scheme")
    if len(re.findall(r"^# ",text,re.M)) == 0:
        raise Refused(f"{path}: missing Markdown title")
    return raw

def inspect(checkout: Path, *, target: str | None = None) -> dict:
    pinned = federation.verify()
    old = pinned["source_ref"]
    check_source_remote(checkout)
    head = target or run("git","-C",str(checkout),"rev-parse","refs/remotes/origin/main")
    if not SHA40.fullmatch(head):
        raise Refused("candidate must be an exact 40-character SHA")
    if run("git","-C",str(checkout),"rev-parse","--verify",head+"^{commit}") != head:
        raise Refused("candidate is not a local verified commit")
    if not is_ancestor(checkout,old,head):
        raise Refused("non-fast-forward source history: manual review required")
    changed = []
    for rel in federation.PATHS:
        raw=source_bytes(checkout,head,rel)
        digest=hashlib.sha256(raw).hexdigest()
        if pinned["files"][rel]!=digest:
            changed.append({"path":rel,"before_sha256":pinned["files"][rel],"after_sha256":digest})
    status = ("CURRENT" if old==head else
              "SOURCE_AHEAD_NO_DOC_CHANGE" if not changed else "DOC_UPDATE_CANDIDATE")
    return {"schema":"gnu6.federation.update-candidate.v1", "repository":CANONICAL,
            "docs_main_source_ref":old,"source_head":head,"status":status,
            "changed_documents":changed,"changed_count":len(changed),
            "requires_review":bool(changed),"auto_merge":False,"auto_deploy":False}

def prepare(checkout: Path, *, destination: Path, candidate: dict,
            docs_repo: Path, python: str=PYTHON) -> dict:
    if candidate["status"] != "DOC_UPDATE_CANDIDATE":
        raise Refused("no relevant changed documents for a proposal")
    if destination.exists():
        raise Refused("destination already exists: never overwrite worktrees")
    if run("git","-C",str(docs_repo),"status","--porcelain"):
        raise Refused("documentation base checkout is dirty")
    docs_origin = run("git","-C",str(docs_repo),"remote","get-url","origin")
    if not (docs_origin.endswith("/tension-atoi/engineering-corpus.git")
            or docs_origin.endswith("/tension-atoi/engineering-corpus")):
        raise Refused("documentation origin is not canonical")
    current=run("git","-C",str(docs_repo),"rev-parse","refs/remotes/origin/main")
    # Rejection if the pinned public docs state has moved since inspect().
    previous=federation.load()
    if previous["source_ref"] != candidate["docs_main_source_ref"]:
        raise Refused("public docs source changed since candidate inspection")
    branch=BRANCH+candidate["source_head"][:12]
    if subprocess.run(["git","-C",str(docs_repo),"show-ref","--verify","--quiet",
                       "refs/heads/"+branch],timeout=10).returncode == 0:
        raise Refused("candidate branch already exists")
    destination.parent.mkdir(parents=True,exist_ok=True)
    run("git","-C",str(docs_repo),"worktree","add","-b",branch,str(destination),current)
    try:
        script=destination/"scripts/federate_gnostral.py"
        run(python,str(script),"--sync","--source-checkout",str(checkout),
            "--ref",candidate["source_head"],cwd=destination)
        for rel in GATE:
            run(python,str(destination/rel),cwd=destination)
        tests=sorted((destination/"scripts").glob("test_*.py"))
        if len(tests)<10:
            raise Refused("documentation qualification suites missing")
        for test in tests:
            run(python,str(test),cwd=destination)
        staged = ("docs/federation/gnostral", "dist", "docs/source-registry.json")
        # The existing source registry's Q007 SHA is also derived from source
        # and needs exact update if its lib.rs changed (not in 7 docs paths).
        run("git","-C",str(destination),"add","--",*staged)
        if not run("git","-C",str(destination),"diff","--cached","--name-only"):
            raise Refused("candidate produced no changes")
        run("git","-C",str(destination),"diff","--cached","--check")
        evidence = {"schema":"gnu6.federation.review-branch.v1",
                    "docs_base_sha":current,"candidate":candidate,
                    "branch":branch,"qualification":["build","site-check","all-local-documentation-tests"],
                    "git_worktree":str(destination),"requires_review":True}
        return evidence
    except Exception:
        # Deliberately retain the rejected worktree for investigation; never push.
        raise

def print_report(report:dict, out: Path | None):
    serialized=json.dumps(report,sort_keys=True,indent=2)+"\n"
    if out is not None:
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open("x") as f:f.write(serialized)
    print("FEDERATION_STATUS",report["status"],report["source_head"],
          "changed_docs",report["changed_count"])
    for item in report["changed_documents"]:
        print("DOC_DIFF",item["path"],item["before_sha256"][:12],item["after_sha256"][:12])

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-checkout",type=Path,required=True)
    p.add_argument("--target-ref")
    p.add_argument("--report",type=Path)
    p.add_argument("--prepare-worktree",type=Path)
    p.add_argument("--docs-repo",type=Path)
    p.add_argument("--proposal",type=Path)
    p.add_argument("--refresh",action="store_true",help="fetch public origin/main before examining the exact commit")
    args=p.parse_args()
    try:
        if args.prepare_worktree is not None and (args.docs_repo is None or args.proposal is None):
            p.error("--prepare-worktree needs --docs-repo and --proposal")
        if args.refresh:
            check_source_remote(args.source_checkout)
            run("git","-C",str(args.source_checkout),"fetch","--no-tags","origin","main")
        if args.prepare_worktree is not None:
            run("git","-C",str(args.docs_repo),"fetch","--no-tags","origin","main")
        current=inspect(args.source_checkout,target=args.target_ref)
        print_report(current,args.report)
        if args.prepare_worktree is not None:
            candidate=prepare(args.source_checkout,destination=args.prepare_worktree,
                              candidate=current,docs_repo=args.docs_repo)
            args.proposal.parent.mkdir(parents=True,exist_ok=True)
            with args.proposal.open("x") as stream:
                json.dump(candidate,stream,sort_keys=True,indent=2)
                stream.write("\n")
            print("FEDERATION_REVIEW_BRANCH_READY",candidate["branch"])
        return 10 if current["status"]=="DOC_UPDATE_CANDIDATE" and args.prepare_worktree is None else 0
    except (OSError,ValueError,UnicodeError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
        print("FEDERATION_REFUSED",str(exc),file=sys.stderr)
        return 2

if __name__=="__main__":raise SystemExit(main())
