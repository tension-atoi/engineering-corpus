"""NO-VEIL-02: static Docs never masks document navigation, including BFCache."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    for root in ("site", "dist"):
        css = (ROOT / root / "motion/g6-motion.css").read_text()
        js = (ROOT / root / "motion/g6-motion.js").read_text()
        adapter = (ROOT / root / "context/context-adapter.js").read_text()
        assert "html[data-g6-bridge]::after" not in css
        assert "170vmax" not in css
        assert "get active() { return false; }" in js
        assert "cover() { return Promise.resolve(); }" in js
        assert 'window.addEventListener("pageshow", clearOldOverlay)' in js
        assert 'window.addEventListener("pagehide", clearOldOverlay)' in js
        assert 'root.dataset.g6Bridge = "covered"' not in js
        assert "Motion.arrival = Motion.arc" not in js
        assert "beginCrossDomainHandoff" not in adapter
    print("DOCS_NO_VEIL_BFCACHE_PASS source_and_dist=2")

if __name__ == "__main__":
    main()
