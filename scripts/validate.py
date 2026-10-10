"""Bounded source/static checks; not an editorial or accessibility certification."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlsplit
import yaml
from gnu6_shell import SYSTEM_LINKS


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.ids, self.headings, self.resources = [], [], [], []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': self.lang = attrs.get('lang')
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'h1': self.headings.append(tag)
        for key in ('href', 'src'):
            if attrs.get(key):
                self.refs.append((tag, key, attrs[key]))
                if key == 'src' or tag == 'link': self.resources.append(attrs[key])


def metadata(path):
    raw = path.read_text('utf-8')
    if not raw.startswith('---\n'): raise ValueError('missing frontmatter')
    _, front, body = raw.split('---\n', 2)
    data = yaml.safe_load(front)
    if not isinstance(data, dict): raise ValueError('metadata must be mapping')
    return data, body


def check(root):
    errors = []
    def require(ok, message):
        if not ok: errors.append(message)
    docs, dist = root/'docs', root/'dist'
    catalog = json.loads((docs/'catalog.json').read_text())
    units = [('chapters', x['id']) for x in catalog['chapters']] + [('labs', x) for x in catalog['labs']]
    identities = {}
    for directory, slug in units:
        pair = []
        for lang in catalog['locales']:
            path = docs/lang/directory/f'{slug}.md'
            try:
                meta, body = metadata(path)
                for key in ('id', 'title', 'duration', 'status', 'category', 'method_id', 'classification',
                            'prerequisites', 'artifacts', 'success_criteria', 'references'):
                    require(key in meta, f'{path.relative_to(root)} missing {key}')
                require(meta.get('status') in catalog['statuses'], f'{path} invalid status')
                require(meta.get('classification') in ('proposed-principle','recommendation','external-standard','ratified-decision'), f'{path} invalid classification')
                require(isinstance(meta.get('duration'), int) and meta['duration'] > 0, f'{path} invalid duration')
                require(meta.get('category') == ('core' if directory=='chapters' else 'lab'), f'{path} invalid category')
                require(meta.get('id') == (slug if directory=='chapters' else 'lab-'+{'01-change':'change','02-api':'api','03-workspace':'workspace'}[slug]), f'{path} wrong identity')
                for key in ('prerequisites','artifacts','success_criteria','references'):
                    require(isinstance(meta.get(key),list) and bool(meta[key]) and all(isinstance(v,str) and v for v in meta[key]), f'{path} invalid {key}')
                require(body.count('```') % 2 == 0, f'{path} unbalanced fences')
                outside_fences = ''.join(body.split('```')[::2])
                require(len(re.findall(r'^# ', outside_fences, re.MULTILINE)) == 1, f'{path} expected one H1')
                require('<details>' in body and '<summary>' in body, f'{path} missing self-assessment')
                if meta.get('classification') == 'ratified-decision':
                    for key in ('decision_owner','decision_date','decision_scope','decision_adr'):
                        require(bool(meta.get(key)), f'{path} ratification missing {key}')
                pair.append(meta)
            except (OSError, ValueError, yaml.YAMLError) as exc: errors.append(f'{path}: {exc}')
        if len(pair)==2:
            for key in ('id','method_id','status','duration','category','classification','references'):
                require(pair[0].get(key)==pair[1].get(key), f'{slug} FR/EN drift in {key}')
            identity=pair[0].get('method_id')
            require(identity not in identities, f'duplicate method identity {identity}')
            identities[identity]=slug
    expected={'index.html','404.html'}
    for lang in catalog['locales']:
        expected.add(f'{lang}/hub.html')
        expected.add(f'{lang}/projects.html')
        expected.add(f'{lang}/projects/gnostral/index.html')
        expected.update(f'{lang}/projects/gnostral/{name}.html' for name in ('overview','capabilities','questlog','roadmap','architecture','reproducibility'))
        expected.add(f'{lang}/ecosystem.html')
        expected.update((f'{lang}/guides.html', f'{lang}/guides/api-verification.html', f'{lang}/releases.html'))
        expected.add(f'{lang}/studies/cuda-05d.html')
        expected.add(f'{lang}/studies/cuda-05e.html')
        expected.add(f'{lang}/studies/cuda-05f.html')
        expected.add(f'{lang}/studies/cuda-05g.html')
        expected.add(f'{lang}/studies/cuda-05h.html')
        expected.add(f'{lang}/studies/gnostral-rtx3070.html')
        expected.add(f'{lang}/experiments.html')
        expected.add(f'{lang}/challenges.html')
        expected.update((f'{lang}/sdk.html',f'{lang}/api.html'))
        expected.update(f'{lang}/{directory}/{slug}.html' for directory,slug in units)
        expected.update(f'{lang}/{slug}.html' for slug in ('index','topologies','templates','governance','references'))
        for slug in ('index','governance','references'):
            try:
                m,_=metadata(docs/lang/f'{slug}.md')
                require(m.get('status') in catalog['statuses'], f'{lang}/{slug} invalid status')
            except (OSError,ValueError) as exc: errors.append(str(exc))
    actual={str(p.relative_to(dist)) for p in dist.rglob('*.html')}
    require(actual==expected, f'page inventory missing={sorted(expected-actual)} extra={sorted(actual-expected)}')
    pages={}
    for rel in sorted(actual):
        page=Page(); page.feed((dist/rel).read_text('utf-8'));pages[rel]=page
        require(len(page.ids)==len(set(page.ids)),f'{rel} duplicate HTML ids')
        if '/' in rel:
            require(page.lang==rel.split('/')[0], f'{rel} wrong HTML language')
            require(len(page.headings)==1,f'{rel} expected one H1')
        for resource in page.resources:
            require(not urlsplit(resource).scheme and not resource.startswith('//'),f'{rel} external resource {resource}')
    for rel,page in pages.items():
        for tag,key,ref in page.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc:
                if tag=='a' and key=='href' and ref in SYSTEM_LINKS:
                    continue  # ADR-0001: exact GNU6 system-bar links, identical on every page
                require(tag=='a' and key=='href' and url.scheme=='https' and (rel.endswith('/references.html') or (rel.endswith('/api.html') and url.netloc=='github.com') or (rel.endswith('/guides/api-verification.html') and url.netloc=='github.com') or (rel.endswith('/challenges.html') and url.netloc=='github.com' and url.path.startswith('/tension-atoi/engineering-corpus')) or (rel.endswith('/studies/cuda-05g.html') and url.netloc=='github.com' and url.path.startswith('/tension-atoi/engineering-corpus')) or (rel.endswith('/studies/cuda-05h.html') and url.netloc=='github.com' and url.path.startswith('/tension-atoi/engineering-corpus')) or (rel.startswith(('fr/projects/gnostral/','en/projects/gnostral/')) and url.netloc=='github.com' and url.path.startswith('/tension-atoi/gnostral.rs'))), f'{rel} unexpected external reference {ref}')
                continue
            raw=unquote(url.path)
            target=(dist/raw.lstrip('/') if raw.startswith('/') else (dist/rel).parent/raw) if raw else dist/rel
            target=target.resolve()
            require(target.is_relative_to(dist.resolve()),f'{rel} escaping link {ref}')
            if target.is_dir(): target=target/'index.html'
            require(target.is_file(),f'{rel} broken link {ref}')
            if url.fragment and target.suffix=='.html' and target.is_relative_to(dist.resolve()):
                linked=pages.get(str(target.relative_to(dist.resolve())))
                require(linked is not None and unquote(url.fragment) in linked.ids, f'{rel} broken fragment {ref}')
        for resource in page.resources:
            require('javascript:' not in resource.lower(), f'{rel} script URL')
    for directory,slug in units:
        for lang in catalog['locales']:
            try:
                meta,_=metadata(docs/lang/directory/f'{slug}.md')
                for ref in meta.get('references',[]):
                    require(ref in pages[f'{lang}/references.html'].ids,f'{slug} unknown reference {ref}')
            except (OSError,ValueError,KeyError): pass
    for name in ('lifecycle','authority','knowledge'):
        require((docs/'diagrams'/f'{name}.mmd').is_file(), f'missing Mermaid {name}')
        require((root/'assets/diagrams'/f'{name}.svg').is_file(), f'missing SVG {name}')
    for p in dist.rglob('*'):
        if p.is_file() and p.suffix in ('.html','.js','.svg','.json','.md','.py'):
            text=p.read_text('utf-8')
            require(not re.search(r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----|sk-proj-[A-Za-z0-9]{10,}',text),f'credential pattern {p}')
        if p.is_file() and p.suffix=='.css':
            text=p.read_text('utf-8')
            for raw in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',text):
                url=urlsplit(raw.strip())
                require(not url.scheme and not url.netloc,f'{p.name} external CSS resource {raw}')
                target=dist/url.path.lstrip('/') if url.path.startswith('/') else p.parent/url.path
                require(target.resolve().is_relative_to(dist.resolve()) and target.is_file(),f'{p.name} missing CSS resource {raw}')
        if p.is_file() and p.suffix=='.svg':
            for raw in re.findall(r'(?:href|src)=[\"\']([^\"\']+)',p.read_text('utf-8')):
                require(not urlsplit(raw).scheme and not raw.startswith('//'),f'{p.name} external SVG resource {raw}')
            svg=ET.fromstring(p.read_text('utf-8'))
            bounds=svg.attrib.get('viewBox','').split()
            if len(bounds)==4:
                _,_,width,height=map(float,bounds)
                for node in svg.iter('{http://www.w3.org/2000/svg}rect'):
                    w=node.attrib.get('width','0');h=node.attrib.get('height','0')
                    if '%' not in w+h:
                        require(float(node.attrib.get('x',0))+float(w)<=width and float(node.attrib.get('y',0))+float(h)<=height,
                                f'{p.name} rectangle clipped by viewBox')
    return errors, {'locales':len(catalog['locales']),'chapters':len(catalog['chapters']),'labs':len(catalog['labs']),'html':len(actual)}
