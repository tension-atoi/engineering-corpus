"""GNU6 Spine adapter immutable asset lock and generated-page contracts."""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]
LOCK=json.loads((ROOT/'site/spine-adapter.lock.json').read_text('utf-8'))


def main():
    assert LOCK['component']=='gnu6-spine-adapter' and LOCK['version']=='1.0.0'
    for rel,digest in LOCK['files'].items():
        for folder in (ROOT/'site',ROOT/'dist'):
            assert hashlib.sha256((folder/rel).read_bytes()).hexdigest()==digest,(str(folder),rel)
    pages=list((ROOT/'dist').glob('fr/**/*.html'))+list((ROOT/'dist').glob('en/**/*.html'))
    assert len(pages)>=62,len(pages)
    for page in pages:
        src=page.read_text('utf-8')
        assert src.count('class="g6-spine-shell"')==1,page
        assert src.count('id="gnu6-spine"')==1,page
        assert '/spine.js' in src and '/spine-map.js' in src,page
        assert 'script-src &#x27;unsafe-inline&#x27;' not in src,page
    print('GNU6_SPINE_DOCS_PASS',len(pages),'pages',len(LOCK['files']),'assets')

if __name__=='__main__':main()
