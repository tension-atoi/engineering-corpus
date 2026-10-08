#!/usr/bin/env python3
"""Targeted compatibility assertions for DOCS-HUB-01B (no production calls)."""
from pathlib import Path
from html.parser import HTMLParser
import json

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
CAT=json.loads((ROOT/'docs/hub.json').read_text('utf-8'))
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.h1=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='h1':self.h1+=1
        if tag=='a':self.links.append(d.get('href'))

assert CAT['edition']=='DOCS-HUB-01B'
assert [d['id'] for d in CAT['domains']]==['corpus','sdk','api','guides','releases']
assert [d['state'] for d in CAT['domains']]==['available','planned','planned','planned','planned']
assert set(CAT['domains'][0]['routes'])=={'fr','en'}
assert all('routes' not in d for d in CAT['domains'][1:])
assert 'url=/fr/hub.html' in (DIST/'index.html').read_text('utf-8')
assert "engineering-corpus:study:v0.1" in (ROOT/'site/app.js').read_text('utf-8')
for lang,other in [('fr','en'),('en','fr')]:
    portal=(DIST/lang/'hub.html').read_text('utf-8')
    parsed=Links();parsed.feed(portal)
    assert parsed.h1==1,(lang,parsed.h1)
    assert f'href="/{other}/hub.html"' in portal
    assert f'href="/{lang}/index.html"' in portal
    assert f'href="/{lang}/hub.html"' in portal
    assert portal.count('hub-domain-available')==1
    assert portal.count('hub-domain-planned')==4
    assert f'href="/{lang}/sdk.html"' not in portal
    assert f'href="/{lang}/api.html"' not in portal
    assert f'href="/{lang}/guides.html"' not in portal
    assert f'href="/{lang}/releases.html"' not in portal
    assert set(parsed.links) <= {f'/{lang}/hub.html',f'/{other}/hub.html',f'/{lang}/index.html',
                                 f'/{lang}/governance.html','#content'}
    assert f'href="/{lang}/hub.html"' in (DIST/lang/'index.html').read_text('utf-8')
    assert (DIST/lang/'chapters/01-mandate.html').is_file()
    assert (DIST/lang/'index.html').is_file()
print('DOCS_HUB_01B_COMPAT_PASS locales=2 domains=5 available=1 planned=4')
