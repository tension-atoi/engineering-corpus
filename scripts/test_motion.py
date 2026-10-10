"""GNU6 direct top-level handoff: pinned upstream, all pages and CSP."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / 'site/motion/motion.lock.json').read_text())
def main():
    assert LOCK['design'] == 'gnu6-design@1.1.1'
    assert LOCK['transport'] == 'G6Motion v1 fragment, isolated top-level origins'
    for name,digest in LOCK['files'].items():
        for folder in ('site','dist'):
            item = ROOT / folder / 'motion' / name
            assert hashlib.sha256(item.read_bytes()).hexdigest() == digest, item
    pages = list((ROOT/'dist').glob('fr/**/*.html')) + list((ROOT/'dist').glob('en/**/*.html'))
    assert len(pages) >= 90, len(pages)
    for page in pages:
        html = page.read_text('utf-8')
        assert html.count('/motion/domain.js') == 1, page
        assert html.index('/motion/domain.js') < html.index('/motion/g6-motion.js'), page
        assert html.count('/motion/g6-motion.js') == 1, page
        assert html.count('/motion/g6-motion.css') == 1, page
        assert html.count('/motion/receiver.js') == 1, page
        assert html.index('/motion/g6-motion.js') < html.index('</head>'), page
        assert "script-src 'self'" in html, page
        assert "connect-src 'none'" in html, page
    print('GNU6_MOTION_CROSS_DOMAIN_DOCS_PASS',len(pages),'pages',len(LOCK['files']),'assets')
if __name__=='__main__': main()
