#!/usr/bin/env python3
"""Build a network-free, deterministic static study corpus from Markdown.
Only writes under dist/. Does not read Gnosix or any external workspace.
"""
from __future__ import annotations
from html import escape
from pathlib import Path
from shutil import copy2, copytree, rmtree
import json
import re
import shutil

try:
    import yaml
    from markdown_it import MarkdownIt
except ImportError as exc:
    raise SystemExit('Missing local dependencies: create .venv and pip install -r requirements.txt') from exc

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
DOCS=ROOT/'docs'
SITE=ROOT/'site'
ASSETS=ROOT/'assets'
CATALOG=json.loads((DOCS/'catalog.json').read_text('utf-8'))
M=MarkdownIt('commonmark',{'html':True,'linkify':False,'typographer':True}).enable('table')


def unpack(path):
    raw=path.read_text('utf-8')
    if raw.startswith('---\n'):
        _, metadata, body=raw.split('---\n',2)
        return yaml.safe_load(metadata),body
    return {},raw


def render_markdown(body):
    # Syntax fence 'mermaid' intentionally shows inspectable Mermaid SOURCE.
    # Accessible diagrams are generated SVGs on the topology page.
    return M.render(body)


def nav(locale,active):
    base=f'/{locale}/'
    lablabel='Ateliers' if locale=='fr' else 'Labs'
    rootlabel='Corpus' if locale=='fr' else 'Corpus'
    searchlabel='Filtrer les chapitres' if locale=='fr' else 'Filter chapters'
    entries=[]
    for x in CATALOG['chapters']:
        meta,_=unpack(DOCS/locale/'chapters'/f"{x['id']}.md")
        path=f"{base}chapters/{x['id']}.html"
        css='active' if path==active else ''
        entries.append(f'<a class="navlink {css}" href="{path}" data-search="{escape(str(meta["title"]).lower())}" aria-current="{"page" if css else "false"}"><span class="nav-number">{len(entries)+1:02d}</span>{escape(meta["title"])} <span class="nav-duration">{meta["duration"]}m</span></a>')
    labs=[]
    for slug in CATALOG['labs']:
        meta,_=unpack(DOCS/locale/'labs'/f'{slug}.md')
        path=f'{base}labs/{slug}.html'
        css='active' if path==active else ''
        labs.append(f'<a class="navlink {css}" href="{path}" data-search="{escape(str(meta["title"]).lower())}"><span class="nav-number">↗</span>{escape(meta["title"])}</a>')
    return f'''<div class="sidebar-head"><span class="eyebrow">{rootlabel} / 0.1-draft</span><a class="close-sidebar" href="#content">✕</a></div>
    <label class="search-label" for="chapterSearch">{searchlabel}</label><input id="chapterSearch" type="search" placeholder="{searchlabel}…" autocomplete="off" />
    <nav aria-label="{rootlabel}"><h3>{rootlabel} <span>08</span></h3>{''.join(entries)}<h3>{lablabel} <span>02</span></h3>{''.join(labs)}
    <a class="navlink" href="{base}topologies.html" data-search="topologies diagrammes diagrams"><span class="nav-number">◇</span>Topologies</a>
    <a class="navlink" href="{base}templates.html" data-search="templates modèles"><span class="nav-number">≡</span>{'Modèles' if locale=='fr' else 'Templates'}</a></nav>
    <div class="rail-bottom"><div class="progress-label"><span>{'Étudié localement' if locale=='fr' else 'Locally studied'}</span><strong data-progress-text>0 / 10</strong></div><div class="meter"><div data-progress-meter></div></div><p>{'Sans compte, sans télémétrie.' if locale=='fr' else 'No account, no telemetry.'}</p></div>'''


def shell(locale, title, inner, path, page_id='',mins=None,status='draft'):
    opposite='en' if locale=='fr' else 'fr'
    path_tail=path[len(f'/{locale}/'):]
    en=f'/{opposite}/{path_tail}'
    subtitle='Méthodes, preuves et autonomie' if locale=='fr' else 'Methods, evidence and autonomy'
    home='Accueil' if locale=='fr' else 'Home'
    study='Marquer comme étudié' if locale=='fr' else 'Mark as studied'
    live='Version d’étude · non ratifiée' if locale=='fr' else 'Study edition · not ratified'
    rights='Aucune autorité accordée aux agents.' if locale=='fr' else 'No agent authority is granted.'
    complete=f'<button type="button" class="study-button" data-progress-id="{escape(page_id)}" data-default-label="{study}">{study}</button>' if page_id and page_id != 'home' else ''
    minsblock=f'<span class="time-tag">{mins} min</span>' if mins else ''
    langname='English' if locale=='fr' else 'Français'
    page=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="color-scheme" content="dark" /><meta name="referrer" content="no-referrer" />
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; script-src 'self'; img-src 'self'; font-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'" />
    <meta name="description" content="{escape(subtitle)}"/><title>{escape(title)} · Engineering Corpus</title>
    <link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script>
    <link rel="alternate" hreflang="{opposite}" href="{en}"><link rel="alternate" hreflang="{locale}" href="{path}">
    </head><body data-locale="{locale}">
    <a class="skip" href="#content">{'Aller au contenu' if locale=='fr' else 'Skip to content'}</a>
    <header class="topbar"><a class="brand" href="/{locale}/index.html" aria-label="Engineering Corpus, {home}"><span class="brandmark">&gt;#</span><span>gnu.in.labs <em>/</em> <strong>Engineering Corpus</strong></span></a>
    <div class="top-right"><span class="top-status">0.1 · DRAFT</span><a class="lang" href="{en}" lang="{opposite}">{langname} ↗</a><button id="toggleSidebar" type="button" aria-label="Menu" aria-expanded="false">☰</button></div></header>
    <div class="layout"><aside id="sidebar" class="sidebar">{nav(locale,path)}</aside><main id="content" class="main" tabindex="-1">
    <div class="chapter-meta"><span class="eyebrow">GNU.IN.LABS / {'MÉTHODOLOGIE' if locale=='fr' else 'METHODOLOGY'}</span><span class="meta-right"><span class="status">{escape(status.upper())}</span>{minsblock}</span></div>
    <article class="prose">{inner}</article>
    <div class="lesson-foot">{complete}<span>{live}</span></div>
    <footer><span>© 2026 gnu.in.labs · MIT</span><span>{rights}</span><a href="/{locale}/templates.html">{'Règles de contribution' if locale=='fr' else 'Contribution rules'} →</a></footer>
    </main></div></body></html>'''
    (DIST/path.lstrip('/')).parent.mkdir(parents=True,exist_ok=True)
    (DIST/path.lstrip('/')).write_text(page,encoding='utf-8')


def topology(locale):
    intro='Visualiser les responsabilités et les barrières de promotion' if locale=='fr' else 'Visualize responsibilities and promotion gates'
    expl='Les schémas SVG sont consultables hors ligne ; les sources Mermaid correspondantes restent modifiables et inspectables.' if locale=='fr' else 'SVG diagrams work offline; their corresponding Mermaid sources remain editable and inspectable.'
    content=f'<h1>Topologies</h1><p class="lead">{intro}.</p><p>{expl}</p>'
    labels=[('lifecycle','01 / Work lifecycle'),('authority','02 / Authority boundaries'),('knowledge','03 / Documentation truth chain')]
    for f,l in labels:
        content+=f'<section class="topology-block"><h2>{l}</h2><img class="topology" src="/diagrams/{f}.svg" alt="{escape(l)}" loading="lazy"><p><a download href="/mermaid/{f}.mmd">{'Source Mermaid' if locale=="fr" else "Mermaid source"} ↓</a></p></section>'
    return content


def template_index(locale):
    names=['MANDATE.md','CONTRACT.md','ADR.md','EVIDENCE.json','RELEASE.md']
    title='Modèles opératoires' if locale=='fr' else 'Operational templates'
    sub='Points de départ à adapter : aucun template ne crée d’autorité.' if locale=='fr' else 'Adapt these starting points: templates grant no authority.'
    links=''.join(f'<a class="template-card" href="/templates/{n}" download><span>↓</span><strong>{n}</strong><small>{"Télécharger" if locale=="fr" else "Download"}</small></a>' for n in names)
    return f'<h1>{title}</h1><p class="lead">{sub}</p><div class="template-grid">{links}</div><p>{"Lisez les règles dans le README et adaptez les permissions projet par projet." if locale=="fr" else "Review the README and adapt permissions to each project."}</p>'


def home_cards(locale):
    cards=[]
    for x in CATALOG['chapters']:
        m,_=unpack(DOCS/locale/'chapters'/f"{x['id']}.md")
        i=len(cards)+1
        cards.append(f'<a class="chapter-card" href="/{locale}/chapters/{x["id"]}.html"><span class="card-no">{i:02d} / 08</span><strong>{escape(m["title"])}</strong><span class="card-bottom"><span>{m["duration"]} MIN</span><span aria-hidden="true">↗</span></span></a>')
    label='Parcours d’étude' if locale=='fr' else 'Study curriculum'
    return f'<section class="course-section"><div class="section-top"><h2>{label}</h2><span>8 × {'CHAPITRES' if locale=="fr" else "CHAPTERS"}</span></div><div class="chapter-grid">{"".join(cards)}</div></section>'


def home_hero(locale):
    if locale=='fr':
        label='CORPUS OUVERT · BILINGUE · LOCAL-FIRST'
        title='Une méthode qui se démontre.'
        sub='Étudier, appliquer, contester et reproduire les pratiques d’ingénierie : contrats, frontières d’autorité, preuves, documentation et livraison.'
        start='Commencer le parcours'
        topology_lbl='Explorer les topologies'
        cards=['8 chapitres','2 ateliers','5 modèles','0 service distant requis']
    else:
        label='OPEN CORPUS · BILINGUAL · LOCAL-FIRST'
        title='A methodology you can prove.'
        sub='Study, apply, challenge and reproduce engineering practices: contracts, authority boundaries, evidence, documentation and delivery.'
        start='Start the curriculum'
        topology_lbl='Explore topologies'
        cards=['8 chapters','2 labs','5 templates','0 required remote services']
    stat=''.join(f'<div><strong>{escape(a.split(" ")[0])}</strong><span>{escape(" ".join(a.split(" ")[1:]))}</span></div>' for a in cards)
    return f'''<div class="hero"><span class="eyebrow">{label}</span><h1>{title}</h1><p>{sub}</p><div class="hero-actions"><a class="primary" href="/{locale}/chapters/01-mandate.html">{start} →</a><a class="outline" href="/{locale}/topologies.html">{topology_lbl} ↗</a></div><div class="stats">{stat}</div></div>'''


def build():
    if DIST.exists(): rmtree(DIST)
    DIST.mkdir(parents=True)
    for file in ('style.css','app.js'):
        copy2(SITE/file,DIST/file)
    copytree(ASSETS/'diagrams',DIST/'diagrams')
    copytree(DOCS/'diagrams',DIST/'mermaid')
    copytree(DOCS/'templates',DIST/'templates')
    for locale in CATALOG['locales']:
        for path in [DOCS/locale/'index.md',*sorted((DOCS/locale/'chapters').glob('*.md')),*sorted((DOCS/locale/'labs').glob('*.md'))]:
            m,body=unpack(path)
            page_id=m['id']
            inner=render_markdown(body)
            if page_id=='home':
                inner=home_hero(locale)+home_cards(locale)+f'<section class="home-note">{inner}</section>'
            section='' if path.name=='index.md' else path.parent.name+'/'
            htmlpath=f'/{locale}/{section}{path.stem}.html'
            shell(locale,str(m.get('title','Engineering Corpus')),inner,htmlpath,page_id,m.get('duration'),m.get('status','draft'))
        shell(locale,'Topologies',topology(locale),f'/{locale}/topologies.html')
        shell(locale,'Modèles' if locale=='fr' else 'Templates',template_index(locale),f'/{locale}/templates.html')
    (DIST/'index.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/fr/index.html"><title>Engineering Corpus</title></head><body><a href="/fr/index.html">Français →</a></body></html>',encoding='utf-8')
    (DIST/'404.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/fr/index.html"><title>Engineering Corpus</title></head><body><a href="/fr/index.html">Corpus →</a></body></html>',encoding='utf-8')
    print(f'BUILD_OK pages={len(list(DIST.rglob("*.html")))} assets={len(list(DIST.rglob("*.svg")))}')

if __name__=='__main__':
    build()
