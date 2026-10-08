#!/usr/bin/env python3
"""Build a network-free, deterministic static study corpus from Markdown.
Only writes under dist/. Does not read any external workspace.
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
HUB_CATALOG=json.loads((DOCS/'hub.json').read_text('utf-8'))
CORPUS_NAME=CATALOG['product']['name']
M=MarkdownIt('commonmark',{'html':True,'linkify':False,'typographer':False}).enable('table')


def unpack(path):
    raw=path.read_text('utf-8')
    if raw.startswith('---\n'):
        _, metadata, body=raw.split('---\n',2)
        return yaml.safe_load(metadata),body
    return {},raw


def render_markdown(body):
    # Syntax fence 'mermaid' intentionally shows inspectable Mermaid SOURCE.
    # Accessible diagrams are generated SVGs on the topology page.
    tokens=M.parse(body)
    section=0
    for token in tokens:
        if token.type=='heading_open':
            section+=1
            token.attrSet('id',f'section-{section}')
        if token.type in ('table_open','fence'):
            token.attrSet('tabindex','0')
    return M.renderer.render(tokens,M.options,{})


def study_ids():
    return [x['id'] for x in CATALOG['chapters']]+[unpack(DOCS/'fr'/'labs'/f'{slug}.md')[0]['id'] for slug in CATALOG['labs']]


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
        labs.append(f'<a class="navlink {css}" href="{path}" data-search="{escape(str(meta["title"]).lower())}" aria-current="{"page" if css else "false"}"><span class="nav-number">↗</span>{escape(meta["title"])}</a>')
    return f'''<div class="sidebar-head"><span class="eyebrow">{rootlabel} / 0.1-draft</span><button id="closeSidebar" class="close-sidebar" type="button" aria-label="{'Fermer le menu' if locale=='fr' else 'Close menu'}">✕</button></div>
    <label class="search-label" for="chapterSearch">{searchlabel}</label><input id="chapterSearch" type="search" placeholder="{searchlabel}…" autocomplete="off" />
    <p data-search-status role="status" aria-live="polite"></p><nav aria-label="{rootlabel}"><h2>{rootlabel} <span>{len(CATALOG['chapters']):02d}</span></h2>{''.join(entries)}<h2>{lablabel} <span>{len(CATALOG['labs']):02d}</span></h2>{''.join(labs)}
    <a class="navlink" href="{base}topologies.html" data-search="topologies diagrammes diagrams"><span class="nav-number">◇</span>Topologies</a>
    <a class="navlink" href="{base}templates.html" data-search="templates modèles"><span class="nav-number">≡</span>{'Modèles' if locale=='fr' else 'Templates'}</a></nav>
    <div class="rail-bottom"><div class="progress-label"><span>{'Étudié localement' if locale=='fr' else 'Locally studied'}</span><strong data-progress-text aria-live="polite">0 / {len(study_ids())}</strong></div><progress class="meter" data-progress-meter max="{len(study_ids())}" value="0" aria-label="{'Progression d’étude' if locale=='fr' else 'Study progress'}"></progress><p data-storage-status role="status"></p><p>{'Sans compte, sans télémétrie.' if locale=='fr' else 'No account, no telemetry.'}</p></div>'''


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
    <link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="color-scheme" content="dark" /><meta name="referrer" content="no-referrer" />
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; script-src 'self'; img-src 'self'; font-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'" />
    <meta name="description" content="{escape(subtitle)}"/><title>{escape(title)} · {escape(CORPUS_NAME)}</title>
    <link rel="stylesheet" href="/style.css"><script src="/app.js" defer></script>
    <link rel="alternate" hreflang="{opposite}" href="{en}"><link rel="alternate" hreflang="{locale}" href="{path}">
    </head><body data-locale="{locale}" data-study-ids="{escape(json.dumps(study_ids()),quote=True)}">
    <a class="skip" href="#content">{'Aller au contenu' if locale=='fr' else 'Skip to content'}</a>
    <header class="topbar"><a class="brand" href="/{locale}/index.html" aria-label="{escape(CORPUS_NAME)}, {home}"><span>gnu.in.labs <em>/</em> <strong>{escape(CORPUS_NAME)}</strong></span></a>
    <div class="top-right"><span class="top-status">0.1 · DRAFT</span><a class="lang" href="{en}" lang="{opposite}">{langname} ↗</a><button id="toggleSidebar" type="button" aria-label="Menu" aria-expanded="false" aria-controls="sidebar">☰</button></div></header>
    <div class="layout"><aside id="sidebar" class="sidebar">{nav(locale,path)}</aside><main id="content" class="main" tabindex="-1">
    <div class="chapter-meta"><span class="eyebrow"><a class="hub-return" href="/{locale}/hub.html">{'← Portail' if locale=='fr' else '← Portal'}</a><span class="hub-separator"> / </span>{'MÉTHODOLOGIE' if locale=='fr' else 'METHODOLOGY'}</span><span class="meta-right"><span class="status">{escape(status.upper())}</span>{minsblock}</span></div>
    <article class="prose">{inner}</article>
    <div class="lesson-foot">{complete}<span>{live}</span></div>
    <footer><span>© 2026 gnu.in.labs · MIT</span><span>{rights}</span><a href="/{locale}/governance.html">{'Règles de contribution' if locale=='fr' else 'Contribution rules'} →</a></footer>
    </main></div></body></html>'''
    (DIST/path.lstrip('/')).parent.mkdir(parents=True,exist_ok=True)
    (DIST/path.lstrip('/')).write_text(page,encoding='utf-8')


def topology(locale):
    intro='Visualiser les responsabilités et les barrières de promotion' if locale=='fr' else 'Visualize responsibilities and promotion gates'
    expl='Les schémas SVG sont consultables hors ligne ; les sources Mermaid correspondantes restent modifiables et inspectables.' if locale=='fr' else 'SVG diagrams work offline; their corresponding Mermaid sources remain editable and inspectable.'
    content=f'<h1>Topologies</h1><p class="lead">{intro}.</p><p>{expl}</p>'
    labels=[
        ('lifecycle','Cycle de travail' if locale=='fr' else 'Work lifecycle',
         'Baseline → test causal → correction → vérification → preuve → revue → livraison.' if locale=='fr' else 'Baseline → causal test → fix → verification → evidence → review → delivery.'),
        ('authority','Frontières d’autorité' if locale=='fr' else 'Authority boundaries',
         'Un opérateur octroie des droits bornés ; un agent observe ou propose ; une revue distincte décide de l’intégration.' if locale=='fr' else 'An operator grants scoped rights; an agent observes or proposes; a separate review decides integration.'),
        ('knowledge','Chaîne documentaire' if locale=='fr' else 'Documentation chain',
         'Code versionné → extraction → proposition → validation → revue humaine → édition statique.' if locale=='fr' else 'Versioned code → extraction → proposal → validation → human review → static edition.')]
    for f,l,description in labels:
        content+=f'<section class="topology-block"><h2>{escape(l)}</h2><p>{escape(description)}</p><div class="diagram-scroll" tabindex="0" role="region" aria-label="{escape(l)}"><img class="topology" src="/diagrams/{f}.svg" alt="{escape(description)}" loading="eager"></div><p><a href="/diagrams/{f}.svg">{"Ouvrir le diagramme" if locale=="fr" else "Open diagram"} ↗</a> · <a download href="/mermaid/{f}.mmd">{"Source Mermaid" if locale=="fr" else "Mermaid source"} ↓</a></p></section>'
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
        title=CORPUS_NAME
        sub='Une méthode qui se démontre. Le premier parcours explore les pratiques d’ingénierie : contrats, frontières d’autorité, preuves, documentation et livraison. D’autres domaines et formats d’apprentissage pourront s’y ajouter.'
        start='Commencer le parcours'
        topology_lbl='Explorer les topologies'
        cards=['8 chapitres',f"{len(CATALOG['labs'])} ateliers",'5 modèles','0 service distant requis']
    else:
        label='OPEN CORPUS · BILINGUAL · LOCAL-FIRST'
        title=CORPUS_NAME
        sub='A methodology you can prove. The first learning path covers engineering practice: contracts, authority boundaries, evidence, documentation and delivery. Future editions may welcome other fields and learning formats.'
        start='Start the curriculum'
        topology_lbl='Explore topologies'
        cards=['8 chapters',f"{len(CATALOG['labs'])} labs",'5 templates','0 required remote services']
    stat=''.join(f'<div><strong>{escape(a.split(" ")[0])}</strong><span>{escape(" ".join(a.split(" ")[1:]))}</span></div>' for a in cards)
    return f'''<div class="hero"><span class="eyebrow">{label}</span><h1>{escape(title)}</h1><p>{escape(sub)}</p><div class="hero-actions"><a class="primary" href="/{locale}/chapters/01-mandate.html">{start} →</a><a class="outline" href="/{locale}/topologies.html">{topology_lbl} ↗</a></div><div class="stats">{stat}</div></div>'''



def hub_page(locale):
    """Generate the real documentation entrypoint; no placeholder is a navigable dead end."""
    opposite='en' if locale=='fr' else 'fr'
    fr=locale=='fr'
    name='Documentation · gnu.in.labs'
    intro='Des sources. Des méthodes. Des preuves.' if fr else 'Sources. Methods. Evidence.'
    kicker='PORTAIL DOCUMENTAIRE / GNU.IN.LABS' if fr else 'DOCUMENTATION PORTAL / GNU.IN.LABS'
    subtitle=('Une porte d’entrée vers les connaissances publiées, les contrats techniques et leurs sources. Chaque domaine distingue ce qui est disponible de ce qui reste à documenter.'
              if fr else 'An entry point to published knowledge, technical contracts and their sources. Every section distinguishes what is available from what is still being documented.')
    primary='Explorer le corpus' if fr else 'Explore the corpus'
    language='English' if fr else 'Français'
    indexlabel='Index documentaire' if fr else 'Documentation index'
    availability='Disponibilité vérifiée dans cette édition' if fr else 'Availability in this edition'
    state_av='Disponible · édition de travail' if fr else 'Available · study edition'
    state_pl='En préparation · aucune référence publiée' if fr else 'Planned · no published reference'
    library='Domaines documentaires' if fr else 'Documentation domains'
    section_sub='Un index explicite, pas un catalogue de promesses.' if fr else 'An explicit index, not a catalogue of promises.'
    provenance=('Le corpus est le seul domaine actuellement publié. Les références SDK, API, guides et releases seront ajoutées depuis des sources publiques versionnées, après vérification de leur provenance.'
                if fr else 'The corpus is the only currently published domain. SDK references, APIs, guides and releases will be added from versioned public sources after verifying provenance.')
    rows=[]
    for i,domain in enumerate(HUB_CATALOG['domains'],1):
        published=domain['state']=='available'
        title=domain['label'][locale]
        desc=domain['description'][locale]
        route=domain.get('routes',{}).get(locale)
        if published:
            if not route: raise ValueError(f'available domain {domain["id"]} lacks {locale} route')
            label=f'<a class="hub-domain-name" href="{escape(route,quote=True)}">{escape(title)} <span aria-hidden="true">↗</span></a>'
        else:
            if route: raise ValueError(f'planned domain {domain["id"]} has unexpected public route')
            label=f'<span class="hub-domain-name">{escape(title)}</span>'
        state=state_av if published else state_pl
        rows.append(f'<li class="hub-domain {"hub-domain-available" if published else "hub-domain-planned"}"><span class="hub-number">{i:02d}</span><div class="hub-domain-copy">{label}<p>{escape(desc)}</p></div><span class="hub-domain-status">{escape(state)}</span></li>')
    cards=''.join(rows)
    main=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/favicon.svg"><meta name="color-scheme" content="dark"><meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; img-src 'self'; font-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'">
<meta name="description" content="{escape(subtitle,quote=True)}"><title>{escape(name)}</title>
<link rel="stylesheet" href="/style.css"><link rel="alternate" hreflang="{locale}" href="/{locale}/hub.html"><link rel="alternate" hreflang="{opposite}" href="/{opposite}/hub.html"></head>
<body class="hub-page"><a class="skip" href="#content">{'Aller au contenu' if fr else 'Skip to content'}</a>
<header class="hub-header"><a class="hub-logo" href="/{locale}/hub.html" aria-label="gnu.in.labs — {escape(indexlabel)}"><strong>gnu.in.labs</strong><span>/</span><span>docs</span></a>
<nav class="hub-global-nav" aria-label="{'Navigation principale' if fr else 'Primary navigation'}"><a aria-current="page" href="/{locale}/hub.html">{'Portail' if fr else 'Portal'}</a><a href="/{locale}/index.html">Corpus</a></nav>
<a class="hub-language" href="/{opposite}/hub.html" lang="{opposite}">{language} ↗</a></header>
<main class="hub-main" id="content" tabindex="-1">
<div class="hub-hero"><div class="hub-intro"><span class="hub-kicker">{escape(kicker)}</span><h1>{escape(intro)}</h1><p class="hub-lede">{escape(subtitle)}</p>
<a class="hub-primary" href="/{locale}/index.html">{primary}<span aria-hidden="true">↗</span></a></div>
<aside class="hub-proof" aria-label="{escape(availability)}"><span class="hub-proof-label">01 / 05</span><strong>Corpus Méthodologique &amp; Hygiène Mental</strong><p>{'8 chapitres · 3 ateliers · FR/EN' if fr else '8 chapters · 3 labs · FR/EN'}</p><span class="hub-proof-state">{escape(state_av)}</span></aside></div>
<section class="hub-index" aria-labelledby="hub-index-title"><div class="hub-section-head"><div><span class="hub-kicker">{escape(indexlabel)}</span><h2 id="hub-index-title">{escape(library)}</h2></div><p>{escape(section_sub)}</p></div><ol class="hub-domains">{cards}</ol></section>
<section class="hub-policy" aria-label="{'Provenance des contenus' if fr else 'Content provenance'}"><span class="hub-kicker">{'PROVENANCE / PUBLICATION' if fr else 'PROVENANCE / PUBLICATION'}</span><p>{escape(provenance)}</p></section>
<footer class="hub-footer"><span>© 2026 gnu.in.labs</span><span>{'Corpus : édition de travail non ratifiée' if fr else 'Corpus: draft study edition, not ratified'}</span><a href="/{locale}/governance.html">{'Règles du corpus' if fr else 'Corpus governance'} ↗</a></footer>
</main></body></html>'''
    file=DIST/locale/'hub.html'
    file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(main,encoding='utf-8')

def build():
    if DIST.exists(): rmtree(DIST)
    DIST.mkdir(parents=True)
    for file in ('style.css','app.js','favicon.svg','design-tokens.css'):
        copy2(SITE/file,DIST/file)
    copytree(ASSETS/'diagrams',DIST/'diagrams',ignore=shutil.ignore_patterns('*.py','__pycache__'))
    copytree(ROOT/'examples',DIST/'examples',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    copytree(SITE/'fonts',DIST/'fonts')
    copytree(DOCS/'diagrams',DIST/'mermaid')
    copytree(DOCS/'templates',DIST/'templates')
    for locale in CATALOG['locales']:
        hub_page(locale)
        for path in [DOCS/locale/'index.md',*sorted((DOCS/locale/'chapters').glob('*.md')),*sorted((DOCS/locale/'labs').glob('*.md'))]:
            m,body=unpack(path)
            page_id=m['id']
            inner=render_markdown(body)
            if m.get('method_id'):
                labels=('Identité','Classification','Prérequis','Artefacts','Réussite') if locale=='fr' else ('Identity','Classification','Prerequisites','Artifacts','Success')
                values=[m['method_id'],m['classification'],', '.join(m['prerequisites']),'; '.join(m['artifacts']),'; '.join(m['success_criteria'])]
                card='<dl class="method-meta">'+''.join(f'<dt>{label}</dt><dd>{escape(str(value))}</dd>' for label,value in zip(labels,values))+'</dl>'
                inner=inner.replace('</h1>','</h1>'+card,1)
                inner+='<h2>'+('Références' if locale=='fr' else 'References')+'</h2><ul>'+''.join(f'<li><a href="/{locale}/references.html#{ref}">{ref}</a></li>' for ref in m['references'])+'</ul>'
            if page_id=='home':
                inner=home_hero(locale)+home_cards(locale)+f'<section class="home-note">{inner.replace("<h1","<h2").replace("</h1>","</h2>")}</section>'
            section='' if path.name=='index.md' else path.parent.name+'/'
            htmlpath=f'/{locale}/{section}{path.stem}.html'
            shell(locale,str(m.get('title',CORPUS_NAME)),inner,htmlpath,page_id,m.get('duration'),m.get('status','draft'))
        for slug in ('governance','references'):
            meta,body=unpack(DOCS/locale/f'{slug}.md')
            shell(locale,meta['title'],render_markdown(body),f'/{locale}/{slug}.html')
        shell(locale,'Topologies',topology(locale),f'/{locale}/topologies.html')
        shell(locale,'Modèles' if locale=='fr' else 'Templates',template_index(locale),f'/{locale}/templates.html')
    (DIST/'index.html').write_text(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/fr/hub.html"><title>{escape(CORPUS_NAME)}</title></head><body><a href="/fr/hub.html">Portail français →</a></body></html>',encoding='utf-8')
    (DIST/'404.html').write_text(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>404 · {escape(CORPUS_NAME)}</title><link rel="stylesheet" href="/style.css"></head><body><main class="main"><h1>404 — Page introuvable / Page not found</h1><p>Cette route n’existe pas. This route does not exist.</p><p><a href="/fr/hub.html">Portail français</a> · <a href="/en/hub.html">English portal</a></p></main></body></html>',encoding='utf-8')
    print(f'BUILD_OK pages={len(list(DIST.rglob("*.html")))} assets={len(list(DIST.rglob("*.svg")))}')

if __name__=='__main__':
    build()
