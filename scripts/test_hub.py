#!/usr/bin/env python3
"""Targeted DOCS-HUB-01C static compatibility checks."""
from pathlib import Path
from html.parser import HTMLParser
import json,re
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
CAT=json.loads((ROOT/'docs/hub.json').read_text('utf-8'))
SRC=json.loads((ROOT/'docs/source-registry.json').read_text('utf-8'))
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.h1=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='h1':self.h1+=1
        if tag=='a':self.links.append(d.get('href'))
assert CAT['edition']=='DOCS-HUB-01C'
assert [x['id'] for x in CAT['domains']]==['corpus','sdk','api','guides','releases']
assert [x['state'] for x in CAT['domains']]==['available','inventory','experimental','planned','planned']
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
    for klass in ('available','inventory','experimental'):
        assert page.count('hub-domain-'+klass)==1
    assert page.count('hub-domain-planned')==2
    assert f'/{lang}/sdk.html' in links.links
    assert f'/{lang}/api.html' in links.links
    assert f'/{other}/hub.html' in links.links
    assert not any('guides.html' in (x or '') or 'releases.html' in (x or '') for x in links.links)
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
print('DOCS_HUB_01C_COMPAT_PASS locales=2 domains=5 api_refs=1 sdk_refs=0')
