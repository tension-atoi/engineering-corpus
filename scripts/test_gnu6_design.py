#!/usr/bin/env python3
"""Vendored gnu6-design: lock integrity and the Amendment 01 orange rule."""
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "site" / "gnu6"
ORANGE = re.compile(r"var\(--(g6-signal|g6-action-signal|g6-identity-gnosix|gnosix-signalOrange-[a-z0-9]+)\)")


def main():
    lock = json.loads((VENDOR / "gnu6-design.lock.json").read_text("utf-8"))
    for rel, digest in lock["files"].items():
        assert hashlib.sha256((VENDOR / rel).read_bytes()).hexdigest() == digest, f"vendored drift {rel}"
    present = sorted(str(p.relative_to(VENDOR)) for p in VENDOR.rglob("*") if p.is_file() and p.name != "gnu6-design.lock.json")
    assert present == sorted(lock["files"]), "unlisted vendored files"
    css = re.sub(r"/\*.*?\*/", "", (VENDOR / "gnu6.css").read_text("utf-8"), flags=re.S)
    site = (ROOT / "site" / "style.css").read_text("utf-8")
    offenders = []
    for source in (css, site):
        for selector, block in re.findall(r"([^{}]+)\{([^{}]*)\}", source):
            if any(re.match(r"\s*background(-color|-image)?\s*:", d) and ORANGE.search(d) for d in block.split(";")):
                offenders += [s.strip() for s in selector.split(",") if not re.search(r"::?(before|after)$", s.strip())]
    assert not offenders, f"orange text surface: {offenders}"
    print(f"GNU6_DESIGN_PASS version={lock['version']} files={len(lock['files'])} orange_fills=0")


if __name__ == "__main__":
    main()
