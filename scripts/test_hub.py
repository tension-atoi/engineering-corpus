#!/usr/bin/env python3
"""Targeted DOCS-HUB-01C static compatibility checks."""
from pathlib import Path
from html.parser import HTMLParser
import json,re,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
CAT=json.loads((ROOT/'docs/hub.json').read_text('utf-8'))
SRC=json.loads((ROOT/'docs/source-registry.json').read_text('utf-8'))
GUIDES=json.loads((ROOT/'docs/guide-registry.json').read_text('utf-8'))
RELEASES=json.loads((ROOT/'docs/release-registry.json').read_text('utf-8'))
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.h1=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='h1':self.h1+=1
        if tag=='a':self.links.append(d.get('href'))
assert CAT['edition']=='DOCS-HUB-01D'
assert [x['id'] for x in CAT['domains']]==['corpus','sdk','api','guides','releases']
assert [x['state'] for x in CAT['domains']]==['available','inventory','experimental','guide','inventory']
assert SRC['schema_version']==1 and len(SRC['sources'])==1
item=SRC['sources'][0]
assert item['kind']=='api' and item['lifecycle']=='experimental'
assert item['visibility']=='public' and item['transport']=='no HTTP endpoint'
assert item['source_repository']=='https://github.com/tension-atoi/gnostral.rs'
assert re.fullmatch('[0-9a-f]{40}',item['source_ref'])
assert re.fullmatch('[0-9a-f]{64}',item['source_sha256'])
assert re.fullmatch('[0-9a-f]{64}',item['manifest_sha256'])
assert item['distribution'].endswith('publish = false)')
assert SRC==json.loads((DIST/'registry/source-catalog.json').read_text('utf-8'))
assert 'url=/fr/hub.html' in (DIST/'index.html').read_text('utf-8')
assert "engineering-corpus:study:v0.1" in (ROOT/'site/app.js').read_text('utf-8')
for lang,other in [('fr','en'),('en','fr')]:
    page=(DIST/lang/'hub.html').read_text('utf-8')
    links=Links();links.feed(page)
    assert links.h1==1
    for klass in ('available','experimental','guide'):
        assert page.count('hub-domain-'+klass)==1
    assert page.count('hub-domain-guide')==1
    assert page.count('hub-domain-inventory')==2
    assert page.count('hub-domain-planned')==0
    assert f'/{lang}/sdk.html' in links.links
    assert f'/{lang}/api.html' in links.links
    assert f'/{other}/hub.html' in links.links
    assert f'/{lang}/guides.html' in links.links
    assert f'/{lang}/releases.html' in links.links
    assert f'/{lang}/guides/api-verification.html' in (DIST/lang/'guides.html').read_text('utf-8')
    for kind in ('sdk','api'):
        html=(DIST/lang/f'{kind}.html').read_text('utf-8')
        refs=Links();refs.feed(html)
        assert refs.h1==1
        assert f'/{other}/{kind}.html' in refs.links
        assert '/registry/source-catalog.json' in refs.links
        if kind=='sdk':
            assert not any(r['kind']=='sdk' for r in SRC['sources'])
            assert not any((x or '').startswith('https://') for x in refs.links)
        else:
            source=f"{item['source_repository']}/blob/{item['source_ref']}/{item['source_path']}"
            assert source in refs.links
            assert item['source_sha256'] in html and item['source_ref'] in html
            assert 'publish=false' in html
    assert (DIST/lang/'index.html').exists()

# DOCS-HUB-01D: source-backed draft teaching guide, verified empty release registry.
assert GUIDES['schema_version']==1 and len(GUIDES['guides'])==1
guide=GUIDES['guides'][0]
assert guide['id']=='api-verification' and guide['kind']=='guide'
assert guide['lifecycle']=='draft' and guide['distribution'].startswith('published teaching content')
assert guide['source_repository']=='https://github.com/tension-atoi/engineering-corpus'
assert re.fullmatch('[0-9a-f]{40}',guide['source_ref'])
assert 'public' not in guide.get('distribution','') or 'SDK' in guide['distribution']
assert GUIDES==json.loads((DIST/'registry/guide-catalog.json').read_text('utf-8'))
assert RELEASES==json.loads((DIST/'registry/release-catalog.json').read_text('utf-8'))
assert RELEASES['schema_version']==1 and RELEASES['releases']==[]
assert RELEASES['checked_ref']==guide['source_ref']
assert 'zero refs' in RELEASES['verification']
assert len(guide['source_paths'])==4

for path,digest in guide['source_paths'].items():
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    assert re.fullmatch('[0-9a-f]{64}',digest)
    blob=subprocess.run(['git','show',f'{guide["source_ref"]}:{path}'],cwd=ROOT,capture_output=True,check=True).stdout
    assert hashlib.sha256(blob).hexdigest()==digest, f'pin mismatch {path}'
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest, f'guide source drift {path}'

for lang,other in [('fr','en'),('en','fr')]:
    route=guide['route'][lang]
    assert route==f'/{lang}/guides/api-verification.html'
    assert guide['related_lab'][lang]==f'/{lang}/labs/02-api.html'
    page=(DIST/lang/'guides'/'api-verification.html').read_text('utf-8')
    parsed=Links();parsed.feed(page)
    assert parsed.h1==1
    assert f'/{other}/guides/api-verification.html' in parsed.links
    assert '/registry/guide-catalog.json' in parsed.links
    assert '/examples/api_lab.py' in parsed.links
    assert f'/{lang}/api.html' in parsed.links
    assert f'/{lang}/labs/02-api.html' in parsed.links
    assert guide['source_ref'] in page
    assert 'Queue.morph_to' in page and 'Queue.enqueue' in page
    assert 'EngineProvider v0' in page
    assert 'sdk' in (DIST/lang/'sdk.html').read_text('utf-8').lower()
    empty=(DIST/lang/'releases.html').read_text('utf-8')
    links=Links();links.feed(empty)
    assert links.h1==1 and f'/{other}/releases.html' in links.links
    assert '/registry/release-catalog.json' in links.links
    assert RELEASES['checked_ref'] in empty and '0 / TAGS' in empty
print('DOCS_HUB_01D_PASS locales=2 guide_refs=1 guide_source_paths=4 release_tags=0 api_refs=1 sdk_refs=0')
