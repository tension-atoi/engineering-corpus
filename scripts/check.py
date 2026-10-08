#!/usr/bin/env python3
"""Read-only document and generated site consistency checks."""
from __future__ import annotations
from pathlib import Path
from html.parser import HTMLParser
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
DIST=ROOT/'dist'
CAT=json.loads((DOCS/'catalog.json').read_text('utf-8'))
errors=[]
def assert_(yes,message):
    if not yes: errors.append(message)
for lang in CAT['locales']:
    assert_((DOCS/lang/'index.md').exists(),f'missing {lang} homepage')
    for chapter in CAT['chapters']:
        p=DOCS/lang/'chapters'/f"{chapter['id']}.md"
        assert_(p.exists(),f'missing {p}')
        if p.exists():
            txt=p.read_text('utf-8')
            for field in ['id:', 'title:', 'duration:', 'status:', 'category:']:
                assert_(field in txt[:300],f'missing {field} in {p}')
            assert_(txt.count('```')%2==0,f'unbalanced fences in {p}')
            assert_('Auto-évaluation' in txt or 'Self-check' in txt,f'no exercise answer in {p}')
    for lab in CAT['labs']:
        assert_((DOCS/lang/'labs'/f'{lab}.md').exists(),f'missing lab {lang}/{lab}')
for name in ('lifecycle','authority','knowledge'):
    assert_((DOCS/'diagrams'/f'{name}.mmd').exists(),f'missing Mermaid {name}')
    assert_((ROOT/'assets/diagrams'/f'{name}.svg').exists(),f'missing SVG {name}')
class Refs(HTMLParser):
    def __init__(self): super().__init__();self.refs=[];self.external=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:
                if v.startswith(('http://','https://','//')):self.external.append((tag,k,v))
                elif v.startswith('/'):self.refs.append(v.split('#')[0].split('?')[0])
count=0
if DIST.exists():
    for path in DIST.rglob('*.html'):
        count+=1
        s=path.read_text('utf-8')
        x=Refs();x.feed(s)
        for link in x.refs:
            assert_((DIST/link.lstrip('/')).exists(),f'broken local ref {path.relative_to(DIST)} -> {link}')
        assert_(not x.external,f'external resource/link in offline portal {path.name}: {x.external[:2]}')
    for pattern in (r'apikey_[A-Za-z0-9_]{16,}',r'sk-proj-[A-Za-z0-9]{10,}',r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----'):
        for p in DIST.rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.html','.js','.md','.json','.svg'):
                assert_(not re.search(pattern,p.read_text('utf-8',errors='ignore')),f'potential credential in {p}')
assert_(count>=24,f'expected >=24 html files, found {count}')
if errors:
    for e in errors: print('FAIL',e)
    sys.exit(1)
print('CORPUS_CHECK_OK',f'locales={len(CAT["locales"])}',f'chapters={len(CAT["chapters"])}',f'labs={len(CAT["labs"])}',f'html={count}','no_external_site_requests=true')
