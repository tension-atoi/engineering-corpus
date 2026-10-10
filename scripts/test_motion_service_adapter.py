#!/usr/bin/env python3
"""MOTION-SERVICE-ADAPTER-02: real Docs identity, link integrity and owner boundary.

This checks generated *native top-level* Docs, not the illustrative iframe shell.
"""
from html.parser import HTMLParser
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SITE = ROOT / "site"
MOTION = "https://gnu6.live/motion/index.html"
IDENTITY = "/gnu6/identity/gnuinlabs-64.png"
APPLE = "/gnu6/identity/gnuinlabs-128.png"

class Probe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.icons = []
        self.headers = []
        self.frames = []
        self.script = []
        self.brand = []
        self.inside_brand = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") in ("icon", "apple-touch-icon"):
            self.icons.append(a)
        if tag == "a":
            self.links.append(a)
            if a.get("class") == "g6-bar__title":
                self.brand.append(a)
        if tag == "header" and a.get("class") == "g6-sysbar":
            self.headers.append(a)
        if tag == "iframe":
            self.frames.append(a)
        if tag == "script":
            self.script.append(a)

def main():
    assert (SITE / IDENTITY.lstrip("/")).exists(), IDENTITY
    assert (SITE / APPLE.lstrip("/")).exists(), APPLE
    pages = sorted((DIST / "fr").rglob("*.html")) + sorted((DIST / "en").rglob("*.html"))
    assert len(pages) >= 63, len(pages)
    en = fr = 0
    for page in pages:
        html = page.read_text(encoding="utf-8")
        probe = Probe()
        probe.feed(html)
        assert len(probe.headers) == 1, page
        assert len(probe.brand) == 1, page
        locale = page.relative_to(DIST).parts[0]
        expected_hub = f"/{locale}/hub.html"
        assert probe.brand[0]["href"] == expected_hub, page
        assert probe.brand[0]["aria-label"] == "docs.gnu6.live", page
        assert '<span class="g6-tw">docs.gnu6.live</span>' in html, page
        assert '<html lang="' + locale + '" data-g6-domain="docs">' in html, page
        assert html.count('data-g6-site-nav>') == 1, page
        assert 'name="g6-site-mode" value="full"' in html and 'name="g6-site-mode" value="off"' in html, page
        assert 'name="g6-site-mode" value="calm"' not in html, page
        assert '/motion/g6-site-nav.js' in html, page
        assert len([item for item in probe.links if item.get("data-g6-nav-destination") == "live"]) == 2, page
        assert any(link.get("href") == MOTION for link in probe.links), page
        assert sum(1 for link in probe.links if link.get("href") == MOTION) == 2, page  # wide + mobile
        assert sum(1 for icon in probe.icons if icon["rel"] == "icon") == 1, page
        assert sum(1 for icon in probe.icons if icon["rel"] == "apple-touch-icon") == 1, page
        assert next(icon for icon in probe.icons if icon["rel"] == "icon")["href"] == IDENTITY, page
        assert next(icon for icon in probe.icons if icon["rel"] == "apple-touch-icon")["href"] == APPLE, page
        assert (DIST / IDENTITY.lstrip("/")).read_bytes() == (SITE / IDENTITY.lstrip("/")).read_bytes()
        assert not probe.frames, ("cross-service iframes are not approved", page)
        assert "/spine.js" in html and "/spine-map.js" in html, page
        assert "/motion/shell.js" not in html, page
        assert 'script-src \'self\'' in html and 'connect-src \'none\'' in html, page
        fr += (locale == "fr")
        en += (locale == "en")
    css = (SITE / "style.css").read_text("utf-8")
    assert ".g6-site--docs .g6-sysbar .g6-tw:not([data-g6-tw-domain])" in css
    assert (SITE / "motion/g6-site-nav.js").read_bytes() == (DIST / "motion/g6-site-nav.js").read_bytes()
    assert (SITE / "motion/g6-site-nav.css").read_bytes() == (DIST / "motion/g6-site-nav.css").read_bytes()
    assert "var(--g6-accent-labs-text)" in css
    assert hashlib.sha256((DIST / IDENTITY.lstrip("/")).read_bytes()).hexdigest() == "14b67e37a197156d5df65fec3bb3d27ed2405da3b427e862fd2489e912d21e0a"
    import json
    lock = json.loads((SITE / "motion/global-nav.lock.json").read_text("utf-8"))
    assert lock["component"] == "gnu6-global-site-navigation"
    assert lock["adapterVersion"] == "0.2.0"
    assert lock["designSourceCommit"] == "17ffabcd69def9d1f8f2e83dd1f211ef3087a189"
    assert lock["eligibleRealOrigins"] == ["gnu6.live", "docs.gnu6.live"]
    assert lock["displayedModes"] == ["full", "off"]
    assert "gnosix.gnu6.live" in lock["plannedIdentityNotNavigable"]
    for name,digest in lock["sourceSHA256"].items():
        for folder in (SITE, DIST):
            actual=hashlib.sha256((folder/"motion"/name).read_bytes()).hexdigest()
            assert actual == digest, (folder,name)
    assert (SITE/"motion/global-nav.lock.json").read_bytes() == (DIST/"motion/global-nav.lock.json").read_bytes()
    print("MOTION_SERVICE_ADAPTER_02_DOCS PASS", len(pages), "pages", fr, "FR", en, "EN", "real native domains / no framing / identity green")

if __name__ == "__main__":
    main()
