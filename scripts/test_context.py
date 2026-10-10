"""CONTEXT-02: source-locked common core and every generated Docs page."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / 'site/context/context.lock.json').read_text())
def main():
    assert LOCK['component'] == 'gnu6-context-core' and LOCK['version'] == '1.0.3' and LOCK['gnu6_design'] == '1.1.1'
    for name, digest in LOCK['files'].items():
        for folder in ('site', 'dist'):
            path = ROOT / folder / 'context' / name
            assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
    pages = list((ROOT / 'dist').glob('fr/**/*.html')) + list((ROOT / 'dist').glob('en/**/*.html'))
    assert len(pages) >= 62, len(pages)
    for page in pages:
        content = page.read_text('utf-8')
        assert content.count('/context/context-adapter.js') == 1, page
        assert content.count('/context/context-menu.css') == 1, page
        assert "script-src 'self'" in content, page
        assert "connect-src 'none'" in content, page
    print('GNU6_CONTEXT_DOCS_PASS', len(pages), 'pages', len(LOCK['files']), 'assets')
if __name__ == '__main__': main()
