#!/usr/bin/env python3
"""DOCS-FEDERATION-04: public-only, stdlib, read-only GitHub drift watcher.

Runs as a low-memory systemd user oneshot. Never imports/deploys/merges or
requests credentials. Exact source allowlist and pinned SHA-256 are enforced.
"""
from __future__ import annotations
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SHA40 = re.compile(r"^[a-f0-9]{40}$")
SHA64 = re.compile(r"^[a-f0-9]{64}$")
REPO = re.compile(r"^tension-atoi/[a-zA-Z0-9_.-]+$")
UA = "gnu6-docs-federation-readonly/1.0"
API = "https://api.github.com"
MAX_JSON = 256_000
MAX_DOC = 128_000

class WatchRefused(ValueError):
    pass

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def fetch_json(url: str, *, limit: int = MAX_JSON) -> dict:
    if not url.startswith(API + "/repos/tension-atoi/") or "?" not in url and "/commits/main" not in url:
        raise WatchRefused("request outside exact public GitHub API allowlist")
    request = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": UA,
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urlopen(request, timeout=12) as response:
        if response.geturl().split("/")[2] != "api.github.com":
            raise WatchRefused("unexpected cross-host redirect")
        body = response.read(limit + 1)
        if len(body) > limit:
            raise WatchRefused("API document exceeds fixed size")
    result = json.loads(body)
    if not isinstance(result, dict):
        raise WatchRefused("unexpected GitHub API response type")
    return result

def get_head(repository: str, branch: str) -> str:
    # Only public main is qualified in this first edition.
    if branch != "main" or not REPO.fullmatch(repository):
        raise WatchRefused("unapproved source or branch")
    result = fetch_json(f"{API}/repos/{repository}/commits/main")
    sha = result.get("sha")
    if not isinstance(sha, str) or not SHA40.fullmatch(sha):
        raise WatchRefused("missing exact public commit SHA")
    return sha

def get_blob(repository: str, sha: str, path: str) -> bytes:
    if not REPO.fullmatch(repository) or not SHA40.fullmatch(sha):
        raise WatchRefused("invalid repo or source identity")
    parts = PurePosixPath(path)
    if parts.is_absolute() or ".." in parts.parts or not path.endswith(".md"):
        raise WatchRefused("source path outside Markdown allowlist")
    result = fetch_json(f"{API}/repos/{repository}/contents/{path}?ref={sha}")
    if result.get("type") != "file" or result.get("encoding") != "base64":
        raise WatchRefused("source is not a regular blob")
    if not isinstance(result.get("size"), int) or not 0 < result["size"] <= MAX_DOC:
        raise WatchRefused("source exceeds budget")
    data = base64.b64decode(result.get("content", ""), validate=False)
    if len(data) != result["size"] or len(data) > MAX_DOC:
        raise WatchRefused("decoded blob differs from API size")
    blob_id = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if blob_id != result.get("sha"):
        raise WatchRefused("Git blob integrity check failed")
    if b"\0" in data:
        raise WatchRefused("binary source in Markdown allowlist")
    data.decode("utf-8")
    return data

def read_sources(registry: Path) -> list[dict]:
    doc = json.loads(registry.read_text("utf-8"))
    if doc.get("schema") != "gnu6.federation.public-sources.v1":
        raise WatchRefused("unknown source registry schema")
    if not isinstance(doc.get("sources"), list) or not 1 <= len(doc["sources"]) <= 12:
        raise WatchRefused("unbounded source registry")
    ids: set[str] = set()
    enabled = []
    for source in doc["sources"]:
        sid,kind,repo = source.get("id"),source.get("kind"),source.get("repository")
        if not isinstance(sid,str) or not re.fullmatch(r"[a-z][a-z0-9-]{1,42}",sid) or sid in ids:
            raise WatchRefused("invalid or duplicate source ID")
        ids.add(sid)
        if not isinstance(repo,str) or not REPO.fullmatch(repo):
            raise WatchRefused("source repository outside public owner allowlist")
        if source.get("branch") != "main" or kind not in ("upstream","publisher"):
            raise WatchRefused("unsupported source role or branch")
        if kind == "publisher" and source.get("enabled"):
            raise WatchRefused("circular publisher self-ingestion denied")
        if kind == "upstream" and source.get("enabled") is True:
            path = source.get("manifest")
            if not isinstance(path,str) or path != f"{sid}/manifest.json":
                raise WatchRefused("manifest path not derived from source ID")
            manifest_file = registry.parent / path
            manifest = json.loads(manifest_file.read_text("utf-8"))
            if manifest.get("schema")!="gnu6.federation.pinned-markdown.v1":
                raise WatchRefused("unqualified manifest schema")
            if manifest.get("repository") != "https://github.com/" + repo:
                raise WatchRefused("source manifest owner mismatch")
            if not SHA40.fullmatch(manifest.get("source_ref","")):
                raise WatchRefused("source manifest missing pinned commit")
            hashes=manifest.get("files")
            if not isinstance(hashes,dict) or not 1 <= len(hashes) <= 24:
                raise WatchRefused("unbounded document allowlist")
            for rel,digest in hashes.items():
                parts=PurePosixPath(rel)
                if (not isinstance(rel,str) or parts.is_absolute() or ".." in parts.parts
                        or not rel.endswith(".md") or not SHA64.fullmatch(digest)):
                    raise WatchRefused("unqualified Markdown path or digest")
            enabled.append({"id":sid,"repository":repo,"branch":"main",
                            "pinned_sha":manifest["source_ref"],"files":hashes})
    if not enabled:
        raise WatchRefused("no approved public upstream")
    return enabled

def inspect(source: dict) -> dict:
    sha = get_head(source["repository"],source["branch"])
    prior = source["pinned_sha"]
    changed=[]
    if sha != prior:
        for rel, digest in source["files"].items():
            data=get_blob(source["repository"],sha,rel)
            now=sha256(data)
            if now != digest:
                changed.append({"path":rel,"before_sha256":digest,"after_sha256":now})
        # This also catches the head moving during the read.
        if get_head(source["repository"],source["branch"]) != sha:
            raise WatchRefused("upstream branch moved during inspection")
    return {"id":source["id"],"repository":source["repository"],
            "pinned_ref":prior,"observed_ref":sha,
            "status":"CURRENT" if sha==prior else
                     "DOC_UPDATE_CANDIDATE" if changed else "SOURCE_AHEAD_NO_DOC_CHANGE",
            "changed_documents":changed,"changed_count":len(changed)}

def save_atomic(dest: Path, payload: dict) -> None:
    dest.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    os.chmod(dest.parent,0o700)
    raw=(json.dumps(payload,indent=2,sort_keys=True)+"\n").encode()
    fd,name=tempfile.mkstemp(prefix=".federation-",dir=dest.parent)
    try:
        os.fchmod(fd,0o600)
        with os.fdopen(fd,"wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name,dest)
    finally:
        if os.path.exists(name):os.unlink(name)

def watch(registry: Path, state: Path) -> dict:
    sources=read_sources(registry)
    rows=[inspect(source) for source in sources]
    status="DOC_UPDATE_CANDIDATE" if any(
        x["status"]=="DOC_UPDATE_CANDIDATE" for x in rows) else "CURRENT"
    out={"schema":"gnu6.federation.vps-readonly-watch.v1",
         "observed_utc":datetime.now(timezone.utc).isoformat(),
         "verdict":status,"sources":rows,"read_only":True,
         "pr_creation":False,"auto_merge":False,"auto_deploy":False,
         "public_docs_owner":"tension-atoi/engineering-corpus"}
    save_atomic(state/"latest.json",out)
    if status=="DOC_UPDATE_CANDIDATE":
        save_atomic(state/"candidate.json",out)
    elif (state/"candidate.json").exists():
        (state/"candidate.json").unlink()
    return out

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--registry",type=Path,required=True)
    p.add_argument("--state",type=Path,required=True)
    args=p.parse_args()
    try:
        out=watch(args.registry,args.state)
    except (OSError, ValueError, URLError, HTTPError, KeyError) as exc:
        print("FEDERATION_WATCH_REFUSED",type(exc).__name__,str(exc)[:160],file=sys.stderr)
        return 2
    for row in out["sources"]:
        print("FEDERATION_SOURCE",row["id"],row["status"],
              row["pinned_ref"][:12],row["observed_ref"][:12],
              "changed_docs",row["changed_count"])
    print("FEDERATION_WATCH",out["verdict"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
