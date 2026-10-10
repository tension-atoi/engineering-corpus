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
from experiment_pages import render_experiment_registry
from gnu6_shell import index_page, reading_page, specimen, state

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
SOURCE_REGISTRY=json.loads((DOCS/'source-registry.json').read_text('utf-8'))
ECOSYSTEM=json.loads((DOCS/'ecosystem.json').read_text('utf-8'))
GUIDE_REGISTRY=json.loads((DOCS/'guide-registry.json').read_text('utf-8'))
RELEASE_REGISTRY=json.loads((DOCS/'release-registry.json').read_text('utf-8'))
EXPERIMENTS=json.loads((DOCS/'experiments'/'registry.json').read_text('utf-8'))
CHALLENGES=json.loads((DOCS/'challenges'/'registry.json').read_text('utf-8'))
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


STUDIES=('cuda-05d','cuda-05e','cuda-05f','cuda-05g','cuda-05h')
EDITION=HUB_CATALOG['edition']


def rail(locale,active):
    """Corpus navigation rail. Keeps #chapterSearch / data-search / progress hooks used by app.js."""
    base=f'/{locale}/'
    searchlabel='Filtrer le corpus' if locale=='fr' else 'Filter the corpus'
    def link(path,no,title,extra='',search=''):
        cur=' aria-current="page"' if path==active else ''
        return (f'<a href="{path}" data-search="{escape((search or str(title)).lower(),quote=True)}"{cur}>'
                f'<span class="g6-rail__no"{"" if any(ch.isalnum() for ch in no) else " aria-hidden=\"true\""}>{no}</span><span>{escape(str(title))}</span>{extra}</a>')
    chapters=[]
    for i,x in enumerate(CATALOG['chapters'],1):
        meta,_=unpack(DOCS/locale/'chapters'/f"{x['id']}.md")
        chapters.append(link(f"{base}chapters/{x['id']}.html",f'{i:02d}',meta['title'],f'<span class="g6-rail__time">{meta["duration"]}′</span>'))
    labs=[]
    for i,slug in enumerate(CATALOG['labs']):
        meta,_=unpack(DOCS/locale/'labs'/f'{slug}.md')
        labs.append(link(f'{base}labs/{slug}.html','ABC'[i],meta['title']))
    studies=[]
    for slug in STUDIES:
        meta,_=unpack(DOCS/locale/'studies'/f'{slug}.md')
        short=slug.upper().replace('CUDA-','')
        studies.append(link(f'{base}studies/{slug}.html',short,meta['title'].split(' — ',1)[1] if ' — ' in meta['title'] else meta['title'],search=meta['title']+' '+slug))
    res=[('challenges.html','Défis' if locale=='fr' else 'Challenges'),('topologies.html','Topologies'),
         ('templates.html','Modèles' if locale=='fr' else 'Templates'),('references.html','Références' if locale=='fr' else 'References'),
         ('governance.html','Gouvernance' if locale=='fr' else 'Governance')]
    resources=[link(f'{base}{p}','·',n) for p,n in res]
    home=link(f'{base}index.html','◦','Accueil du corpus' if locale=='fr' else 'Corpus home')
    group=lambda title,items: f'<h2>{title} <span>{len(items):02d}</span></h2>'+''.join(items)
    total=len(study_ids())
    return (f'<div class="g6-rail__head"><span class="g6-label">Corpus <span aria-hidden="true">/</span> {escape(CATALOG["edition"])}</span>'
            f'<button id="closeSidebar" class="g6-action g6-action--quiet g6-rail__close" type="button">{"Fermer" if locale=="fr" else "Close"}</button></div>'
            f'<label class="g6-visually-hidden" for="chapterSearch">{searchlabel}</label><input id="chapterSearch" class="g6-rail__filter" type="search" placeholder="{searchlabel}…" autocomplete="off">'
            f'<p class="g6-rail__status" data-search-status role="status" aria-live="polite"></p>'
            f'<nav class="g6-rail" aria-label="Corpus">{home}'
            +group('Chapitres' if locale=='fr' else 'Chapters',chapters)
            +group('Ateliers' if locale=='fr' else 'Labs',labs)
            +group('Études' if locale=='fr' else 'Studies',studies)
            +group('Ressources' if locale=='fr' else 'Resources',resources)
            +'</nav>'
            f'<div class="g6-rail__progress"><div class="g6-rail__progress-line"><span>{"Étudié localement" if locale=="fr" else "Locally studied"}</span><strong data-progress-text aria-live="polite">0 / {total}</strong></div>'
            f'<progress data-progress-meter max="{total}" value="0" aria-label="{"Progression d’étude" if locale=="fr" else "Study progress"}"></progress>'
            f'<p data-storage-status role="status"></p><p>{"Sans compte, sans télémétrie." if locale=="fr" else "No account, no telemetry."}</p></div>')


def shell(locale, title, inner, path, page_id='',mins=None,status='draft',section='corpus',kicker=None):
    """Reading layout for corpus, labs, studies, challenges and reference pages."""
    study='Marquer comme étudié' if locale=='fr' else 'Mark as studied'
    live='Version d’étude · non ratifiée' if locale=='fr' else 'Study edition · not ratified'
    rights='Corpus sous licence MIT · aucune autorité accordée aux agents' if locale=='fr' else 'Corpus under MIT licence · no agent authority is granted'
    complete=(f'<button type="button" class="g6-study" data-progress-id="{escape(page_id)}" data-default-label="{study}" aria-pressed="false">{study}</button>'
              if page_id and page_id!='home' else '')
    kicker=kicker or ('Méthodologie' if locale=='fr' else 'Methodology')
    crumbs=f'<a href="/{locale}/hub.html">Docs</a> <span aria-hidden="true">/</span> {escape(kicker)}'
    meta=state('attention',status.upper()) if status else ''
    if mins: meta+=f'<span class="g6-num">{mins} min</span>'
    foot=f'<div class="g6-doc__foot">{complete}<span>{live}</span></div>'
    description=('Méthodes, preuves et autonomie' if locale=='fr' else 'Methods, evidence and autonomy')
    reading_page(DIST,locale,path,title=f'{title} · {CORPUS_NAME}',description=description,section=section,rail=rail(locale,path),
                 prose=inner,crumbs=crumbs,meta=meta,foot=foot,study_ids=study_ids(),edition=EDITION,footer_note=rights)


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
        # Inline the generated SVG so it follows the active light/dark roles; ids are pre-namespaced.
        svgsrc=(ASSETS/'diagrams'/f'{f}.svg').read_text('utf-8')
        content+=(f'<h2 id="{f}">{escape(l)}</h2><p>{escape(description)}</p><figure class="g6-figure"><div class="g6-figure__scroll" tabindex="0" role="region" aria-label="{escape(l)}">{svgsrc}</div>'
                  f'<p class="g6-figure__links"><a href="/diagrams/{f}.svg">{"Ouvrir le diagramme" if locale=="fr" else "Open diagram"} ↗</a> · <a download href="/mermaid/{f}.mmd">{"Source Mermaid" if locale=="fr" else "Mermaid source"} ↓</a></p></figure>')
    return content


def template_index(locale):
    names=['MANDATE.md','CONTRACT.md','ADR.md','EVIDENCE.json','RELEASE.md','EXPERIMENT.md']
    title='Modèles opératoires' if locale=='fr' else 'Operational templates'
    sub='Points de départ à adapter : aucun template ne crée d’autorité.' if locale=='fr' else 'Adapt these starting points: templates grant no authority.'
    links=''.join(f'<li><a href="/templates/{n}" download><strong>{n}</strong><small>{"Télécharger" if locale=="fr" else "Download"} ↓</small></a></li>' for n in names)
    return f'<h1>{title}</h1><p class="lead">{sub}</p><ul class="g6-files">{links}</ul><p>{"Lisez les règles dans le README et adaptez les permissions projet par projet." if locale=="fr" else "Review the README and adapt permissions to each project."}</p>'


def corpus_ledger(locale):
    rows=[]
    for i,x in enumerate(CATALOG['chapters'],1):
        m,_=unpack(DOCS/locale/'chapters'/f"{x['id']}.md")
        rows.append(f'<li class="g6-ledger__row"><div class="g6-ledger__item"><span class="g6-ledger__rail" aria-hidden="true"></span><span class="g6-ledger__index">{i:02d}</span>'
                    f'<div class="g6-ledger__main"><span class="g6-ledger__title"><a href="/{locale}/chapters/{x["id"]}.html">{escape(m["title"])}</a></span><span class="g6-ledger__desc">{escape(m["method_id"])} · {escape(m["classification"])}</span></div>'
                    f'<span class="g6-ledger__meta"><span class="g6-num">{m["duration"]} min</span></span><span class="g6-ledger__arrow" aria-hidden="true">→</span></div></li>')
    labs=[]
    for i,slug in enumerate(CATALOG['labs']):
        m,_=unpack(DOCS/locale/'labs'/f'{slug}.md')
        labs.append(f'<li class="g6-ledger__row"><div class="g6-ledger__item"><span class="g6-ledger__rail" aria-hidden="true"></span><span class="g6-ledger__index">{"ABC"[i]}</span>'
                    f'<div class="g6-ledger__main"><span class="g6-ledger__title"><a href="/{locale}/labs/{slug}.html">{escape(m["title"])}</a></span><span class="g6-ledger__desc">{escape(m["method_id"])}</span></div>'
                    f'<span class="g6-ledger__meta"><span class="g6-num">{m["duration"]} min</span></span><span class="g6-ledger__arrow" aria-hidden="true">→</span></div></li>')
    head=lambda t,n: f'<div class="g6-section__head"><div><span class="g6-label">{n}</span><h2>{t}</h2></div></div>'
    return (f'<section class="g6-section">{head("Parcours d’étude" if locale=="fr" else "Study curriculum", "8 × "+("CHAPITRES" if locale=="fr" else "CHAPTERS"))}<ol class="g6-ledger g6-ledger--compact g6-enter">{"".join(rows)}</ol></section>'
            f'<section class="g6-section">{head("Ateliers exécutables" if locale=="fr" else "Runnable labs", str(len(labs))+" × "+("ATELIERS" if locale=="fr" else "LABS"))}<ol class="g6-ledger g6-ledger--compact">{"".join(labs)}</ol></section>')


def home_hero(locale):
    if locale=='fr':
        label='Corpus ouvert · bilingue · local-first'
        sub='Une méthode qui se démontre. Le premier parcours explore les pratiques d’ingénierie : contrats, frontières d’autorité, preuves, documentation et livraison. D’autres domaines et formats d’apprentissage pourront s’y ajouter.'
        start='Commencer le parcours'
        topology_lbl='Explorer les topologies'
        cards=['8 chapitres',f"{len(CATALOG['labs'])} ateliers",'6 modèles','0 service distant requis']
    else:
        label='Open corpus · bilingual · local-first'
        sub='A methodology you can prove. The first learning path covers engineering practice: contracts, authority boundaries, evidence, documentation and delivery. Future editions may welcome other fields and learning formats.'
        start='Start the curriculum'
        topology_lbl='Explore topologies'
        cards=['8 chapters',f"{len(CATALOG['labs'])} labs",'6 templates','0 required remote services']
    stat=''.join(f'<dt>{escape(" ".join(a.split(" ")[1:]))}</dt><dd class="g6-num">{escape(a.split(" ")[0])}</dd>' for a in cards)
    return (f'<div class="g6-corpus-hero"><span class="g6-label">{label}</span><h1 class="g6-display">{escape(CORPUS_NAME)}</h1><p class="g6-lede">{escape(sub)}</p>'
            f'<div class="g6-hero__actions"><a class="g6-action" href="/{locale}/chapters/01-mandate.html">{start} <span class="g6-action__arrow" aria-hidden="true">→</span></a>'
            f'<a class="g6-goto" href="/{locale}/topologies.html">{topology_lbl} <span aria-hidden="true">↗</span></a></div><dl class="g6-stats">{stat}</dl></div>')


def ledger_row(i,title,href,desc,status_kind,status_label,extra_class='',meta=''):
    title_html=(f'<a href="{escape(href,quote=True)}">{escape(title)}</a>' if href else escape(title))
    arrow='<span class="g6-ledger__arrow" aria-hidden="true">→</span>' if href else '<span aria-hidden="true"></span>'
    return (f'<li class="g6-ledger__row {extra_class}"><div class="g6-ledger__item"><span class="g6-ledger__rail" aria-hidden="true"></span>'
            f'<span class="g6-ledger__index">{i:02d}</span><div class="g6-ledger__main"><span class="g6-ledger__title">{title_html}</span>'
            f'<span class="g6-ledger__desc">{desc}</span></div><span class="g6-ledger__meta">{state(status_kind,status_label)}{meta}</span>{arrow}</div></li>')


def hub_page(locale):
    """Generate the real documentation entrypoint; no placeholder is a navigable dead end."""
    fr=locale=='fr'
    intro='Des hypothèses. Des méthodes. Des contre-preuves.' if fr else 'Hypotheses. Methods. Counterevidence.'
    kicker='gnu.in.labs / Documentation'
    subtitle=('Une invitation à reproduire, contredire et améliorer nos expériences. Proposez une réplication ou un contre-exemple via GitHub Issues; les kits encore incomplets sont indiqués.'
              if fr else 'An invitation to reproduce, refute and improve our experiments. Submit a replication or counterexample through GitHub Issues; incomplete kits remain explicitly labeled.')
    primary='Examiner les défis scientifiques' if fr else 'Explore scientific challenges'
    indexlabel='Index documentaire' if fr else 'Documentation index'
    state_av='Disponible · édition de travail' if fr else 'Available · study edition'
    state_pl='En préparation · aucune référence publiée' if fr else 'Planned · no published reference'
    state_guide='Guide pédagogique · édition de travail' if fr else 'Teaching guide · draft edition'
    state_releases='Registre consultable · aucun tag publié' if fr else 'Inventory available · no published tags'
    statuses={
        'available':state_av,
        'inventory':'Inventaire consultable · aucun SDK distribué' if fr else 'Inventory available · no SDK distributed',
        'experimental':'Référence expérimentale · non ratifiée' if fr else 'Experimental reference · not ratified',
        'guide':state_guide,
        'planned':state_pl,
    }
    library='Domaines documentaires' if fr else 'Documentation domains'
    section_sub='Un index explicite, pas un catalogue de promesses.' if fr else 'An explicit index, not a catalogue of promises.'
    provenance=('Le corpus reste le parcours d’étude. Le registre SDK est vide ; la rubrique API expose un contrat Rust expérimental, sans endpoint HTTP. Un premier guide pédagogique est sourcé. Aucun tag de release du corpus n’est vérifié.'
                if fr else 'The corpus remains the study curriculum. The SDK registry is empty; API documents an experimental Rust contract without an HTTP endpoint. One teaching guide is sourced. No corpus release tag is verified.')
    rows=[]
    for i,domain in enumerate(HUB_CATALOG['domains'],1):
        st=domain['state']
        if st not in statuses: raise ValueError(f'unsupported hub state {st}')
        navigable=st!='planned'
        route=domain.get('routes',{}).get(locale)
        if navigable and not route: raise ValueError(f'navigable domain {domain["id"]} lacks {locale} route')
        if not navigable and route: raise ValueError(f'planned domain {domain["id"]} has unexpected public route')
        state_label=state_releases if domain['id']=='releases' else statuses[st]
        rows.append(ledger_row(i,domain['label'][locale],route if navigable else None,escape(domain['description'][locale]),st,state_label,extra_class=f'hub-domain hub-domain-{st}'))
    body=(f'<section class="g6-hero"><div class="g6-hero__copy"><span class="g6-label">{escape(kicker)}</span><h1 class="g6-display">{escape(intro)}</h1>'
          f'<p class="g6-lede">{escape(subtitle)}</p><div class="g6-hero__actions"><a class="g6-action" href="/{locale}/challenges.html">{primary} <span class="g6-action__arrow" aria-hidden="true">↗</span></a>'
          f'<a class="g6-goto" href="/{locale}/index.html">{"Ouvrir le corpus" if fr else "Open the corpus"} <span aria-hidden="true">→</span></a></div></div>'
          f'<div class="g6-hero__aside">{specimen(locale,"gnuinlabs")}</div></section>'
          f'<section class="g6-section" aria-labelledby="hub-index-title"><div class="g6-section__head"><div><span class="g6-label">01 <span aria-hidden="true">/</span> {escape(indexlabel)}</span><h2 id="hub-index-title">{escape(library)}</h2></div><p class="g6-section__note">{escape(section_sub)}</p></div>'
          f'<ol class="g6-ledger g6-enter">{"".join(rows)}</ol></section>'
          f'<section class="g6-notice" aria-label="{"Provenance des contenus" if fr else "Content provenance"}"><span class="g6-label">02 <span aria-hidden="true">/</span> Provenance</span><p>{escape(provenance)}</p></section>')
    index_page(DIST,locale,f'/{locale}/hub.html',title='Documentation · gnu.in.labs',description=subtitle,section='hub',body=body,edition=EDITION)


def registry_hero(locale,kicker,title,intro,status=None):
    st=f'<p class="g6-registry-count"><span>{escape(status[0])}</span><strong class="g6-num">{escape(status[1])}</strong></p>' if status else ''
    return (f'<section class="g6-hero g6-hero--compact"><div class="g6-hero__copy"><span class="g6-label">{escape(kicker)}</span>'
            f'<h1 class="g6-display">{escape(title)}</h1><p class="g6-lede">{escape(intro)}</p>{st}</div></section>')


def source_inventory_page(locale, kind):
    """Static, provenance-first index. A source-code contract is not an HTTP service."""
    fr=locale=='fr'
    records=[x for x in SOURCE_REGISTRY['sources'] if x['kind']==kind and locale in x['locale']]
    if kind not in ('sdk','api'):
        raise ValueError(f'unsupported source kind {kind}')
    title=('Inventaire SDK' if fr else 'SDK inventory') if kind=='sdk' else ('Références API' if fr else 'API references')
    kicker=('Inventaire / SDK' if kind=='sdk' else 'Sources / API · '+('expérimental' if fr else 'experimental'))
    intro=('Aucun SDK public qualifié pour distribution dans cette édition. Aucun lien d’installation ni commande ne sera inventé.' if fr else
           'No public SDK is qualified for distribution in this edition. No installation link or command will be invented.') if kind=='sdk' else (
           'Une interface de référence Rust, épinglée à sa source. Aucun endpoint HTTP ni contrat de production annoncé.' if fr else
           'One Rust reference interface pinned to its source. No HTTP endpoint or production service contract is announced.')
    rows=[]
    for record in records:
        if record['kind']!='api' or record['lifecycle']!='experimental':
            raise ValueError(f'unqualified source cannot be rendered: {record["id"]}')
        source_url=f"{record['source_repository']}/blob/{record['source_ref']}/{record['source_path']}"
        manifest_url=f"{record['source_repository']}/blob/{record['source_ref']}/{record['manifest_path']}"
        label_=('Source exacte' if fr else 'Pinned source')
        manifest_label=('Manifeste du crate' if fr else 'Crate manifest')
        rows.append(f"""<article class="g6-record" id="{escape(record['id'],quote=True)}">
<div class="g6-record__head">{state('attention','RUST · '+record['lifecycle'].upper())}<span class="g6-label">v{escape(record['version'])} · publish=false</span></div>
<h2>{escape(record['title'][locale])}</h2><p>{escape(record['description'][locale])}</p>
<dl class="g6-facts">
<dt>{'Responsable' if fr else 'Owner'}</dt><dd>{escape(record['owner'])}</dd>
<dt>{'Révision exacte' if fr else 'Exact revision'}</dt><dd><code>{escape(record['source_ref'])}</code></dd>
<dt>{'Empreinte du fichier' if fr else 'Source file SHA-256'}</dt><dd><code>{escape(record['source_sha256'])}</code></dd>
<dt>{'Vérification' if fr else 'Verified'}</dt><dd>{escape(record['last_verified'])} · {'fichier public existant' if fr else 'public source file exists'}</dd>
<dt>Transport</dt><dd>{escape(record['interface'])} · {escape(record['transport'])}</dd>
<dt>Distribution</dt><dd>{escape(record['distribution'])}</dd></dl>
<div class="g6-record__links"><a class="g6-action g6-action--quiet" href="{escape(source_url,quote=True)}" rel="noopener noreferrer">{label_} <span aria-hidden="true">↗</span></a><a class="g6-action g6-action--quiet" href="{escape(manifest_url,quote=True)}" rel="noopener noreferrer">{manifest_label} <span aria-hidden="true">↗</span></a></div></article>""")
    empty=('<div class="g6-empty">'+state('empty','0 / SDK')+'<strong>Aucune référence SDK publique qualifiée</strong><p>Le registre est volontairement vide. Les packages candidats devront d’abord établir une version, un artefact distribuable et une provenance publique.</p></div>' if fr else
           '<div class="g6-empty">'+state('empty','0 / SDK')+'<strong>No qualified public SDK reference</strong><p>The registry is deliberately empty. Candidate packages first need a verifiable version, distributable artifact and public provenance.</p></div>')
    content=''.join(rows) if rows else empty
    details=('État des références' if fr else 'Reference status')
    source_file='Voir le registre machine' if fr else 'Machine-readable registry'
    disclaimer=('Ce site référence du code public, il ne garantit ni stabilité, ni compatibilité, ni disponibilité de service. Les adaptateurs async et streaming restent hors du contrat montré.' if fr else
                'This page references public source code; it does not guarantee stability, compatibility or service availability. Async and streaming adapters are outside this contract.')
    body=(registry_hero(locale,kicker,title,intro,(details,f'{len(records):02d} / {kind.upper()}'))
          +f'<section class="g6-section" aria-label="{escape(details)}">{content}</section>'
          +f'<section class="g6-notice"><span class="g6-label">Source <span aria-hidden="true">/</span> Provenance</span><p>{escape(disclaimer)} <a href="/registry/source-catalog.json">{source_file} ↗</a></p></section>')
    index_page(DIST,locale,f'/{locale}/{kind}.html',title=f'{title} · gnu.in.labs',description=intro,section='references',body=body,edition=EDITION)


def documentation_page(locale, page_id, title, intro, body, *, section, nav='references'):
    """A static, CSP-locked documentation page without browser-side fetches."""
    content=registry_hero(locale,f'gnu.in.labs / {section}',title,intro)+body
    index_page(DIST,locale,f'/{locale}/{page_id}',title=f'{title} · gnu.in.labs',description=intro,section=nav,body=content,edition=EDITION)


def guides_pages(locale):
    fr=locale=='fr'
    records=[g for g in GUIDE_REGISTRY['guides'] if locale in g['locale']]
    if len(records)!=1 or records[0]['id']!='api-verification':
        raise ValueError('unreviewed guide inventory')
    guide=records[0]
    title='Guides pratiques' if fr else 'Practical guides'
    intro=('Un guide pédagogique lié à un atelier réellement exécutable. Un exercice de documentation ne garantit pas une API produit.'
           if fr else 'One teaching guide tied to a runnable lab. A documentation exercise is not a product API guarantee.')
    caption='Édition de travail · non ratifiée' if fr else 'Draft study edition · not ratified'
    detail=guide['route'][locale]
    lab=guide['related_lab'][locale]
    entry=f"""<section class="g6-section" aria-label="{escape(title)}"><article class="g6-record">
<div class="g6-record__head">{state('attention','GUIDE / DRAFT')}<span class="g6-label">{escape(guide['last_verified'])}</span></div>
<h2>{escape(guide['title'][locale])}</h2><p>{escape(guide['summary'][locale])}</p>
<div class="g6-record__links"><a class="g6-action" href="{escape(detail)}">{'Lire le guide' if fr else 'Read the guide'} <span class="g6-action__arrow" aria-hidden="true">→</span></a><a class="g6-action g6-action--quiet" href="{escape(lab)}">{'Exécuter l’atelier B' if fr else 'Run Lab B'} <span aria-hidden="true">→</span></a></div></article></section>
<section class="g6-notice"><span class="g6-label">{caption}</span><p>{'Provenance, SHA et fichiers consultables' if fr else 'Inspectable provenance, SHA and files'} : <a href="/registry/guide-catalog.json">{'Registre des guides' if fr else 'Guide registry'} ↗</a>. {'Aucun SDK distribué ni service HTTP qualifié' if fr else 'No distributed SDK or qualified HTTP service'}.</p></section>"""
    documentation_page(locale,'guides.html',title,intro,entry,section='Guides')
    guide_id=guide['id']
    doc=DOCS/locale/'guides'/f'{guide_id}.md'
    if not doc.is_file():
        raise ValueError(f'guide body missing: {doc}')
    content=doc.read_text('utf-8')
    if not content.startswith('# '):
        raise ValueError('guide needs a title')
    rendered=render_markdown(content)
    rendered=re.sub(r'^<h1[^>]*>.*?</h1>\s*', '', rendered, count=1)
    source=guide['source_repository']
    sha=guide['source_ref']
    refs=[]
    for path,digest in guide['source_paths'].items():
        href=f'{source}/blob/{sha}/{path}'
        refs.append(f'<dt><a href="{escape(href,quote=True)}" rel="noopener noreferrer">{escape(path)} ↗</a></dt><dd><code>sha256:{escape(digest)}</code></dd>')
    evidence=(f'<section class="g6-notice"><span class="g6-label">Source <span aria-hidden="true">/</span> Provenance</span><div>'
              f'<p>{"Référence pédagogique épinglée au commit" if fr else "Teaching example pinned to commit"} <code>{sha}</code> · {escape(guide["lifecycle"].upper())}</p>'
              f'<dl class="g6-facts">{"".join(refs)}</dl><p><a href="/registry/guide-catalog.json">{"Registre machine" if fr else "Machine-readable registry"} ↗</a></p></div></section>')
    prose=f'<div class="g6-section"><article class="g6-prose">{rendered}</article></div>'+evidence
    documentation_page(locale,f'guides/{guide_id}.html',guide['title'][locale],intro,prose,section='Guide / Expérience' if fr else 'Guide / Exercise')


def releases_page(locale):
    fr=locale=='fr'
    if RELEASE_REGISTRY['releases']:
        raise ValueError('release entries require separately qualified renderer')
    title='Versions et changements' if fr else 'Releases and changes'
    intro=('Un registre de versions fondé sur des tags vérifiés, pas sur une date ou un numéro inventé.'
           if fr else 'A release inventory grounded in verified tags, not invented dates or version numbers.')
    empty=('Aucun tag de release du dépôt engineering-corpus n’a été observé le 8 octobre 2026. Le corpus reste une édition de travail, sans version stable annoncée.'
           if fr else 'No engineering-corpus release tag was observed on October 8, 2026. The corpus remains a draft study edition without an announced stable release.')
    caveat=('Ce contrôle ne concerne que le dépôt du corpus et ne décrit pas les versions des autres produits Gnosix.'
            if fr else 'This observation covers only the corpus repository, not versioning of other Gnosix products.')
    body=f"""<section class="g6-section" aria-label="{escape(title)}"><div class="g6-empty">{state('empty','0 / TAGS')}
<strong>{'Aucune release qualifiée' if fr else 'No qualified release'}</strong><p>{escape(empty)}</p><p>{escape(caveat)}</p></div></section>
<section class="g6-notice"><span class="g6-label">Source <span aria-hidden="true">/</span> {'Vérification' if fr else 'Verification'}</span><p><code>{escape(RELEASE_REGISTRY['checked_ref'])}</code>
· {escape(RELEASE_REGISTRY['verification'])} · <a href="/registry/release-catalog.json">{'Registre machine' if fr else 'Machine-readable registry'} ↗</a></p></section>"""
    documentation_page(locale,'releases.html',title,intro,body,section='Versions' if fr else 'Releases')


def ecosystem_page(locale):
    fr=locale=='fr'
    src={x['id']:x for x in ECOSYSTEM['sources']}
    items=[]
    for i,item in enumerate(ECOSYSTEM['families'],1):
        links=[]
        for ref in item['sources']:
            source=src[ref]
            links.append(f'<a href="{escape(source["route"][locale],quote=True)}">{escape(source["name"])} ↗</a>')
        if links:
            evidence=' · '.join(links); kind,lbl='stable',('Source publique qualifiée' if fr else 'Qualified public source')
        else:
            evidence=''; kind,lbl='planned',('Aucune source publique qualifiée pour cette famille' if fr else 'No qualified public source in this family')
        desc=escape(item['summary'][locale])+(f'<br><span class="ecosystem-evidence">{evidence}</span>' if evidence else '')
        items.append(ledger_row(i,item['label'][locale],None,desc,kind,lbl,extra_class='g6-ledger__row--static'))
    title='Carte des domaines' if fr else 'Ecosystem map'
    intro=('Six familles pour explorer le programme. Cette carte est un index éditorial, pas une annonce de disponibilité des produits.' if fr else 'Six families to explore the program. This is an editorial index, not a claim that every product is available.')
    caveat=('Seuls deux dépôts publics sont référencés ici. Les travaux privés et les projets sans provenance publique qualifiée ne sont pas exposés par ce registre.' if fr else 'Only two public repositories are referenced here. Private work and projects without qualified public provenance are not exposed by this registry.')
    body=(registry_hero(locale,'gnu.in.labs / '+('Cartographie' if fr else 'Ecosystem'),title,intro)
          +f'<section class="g6-section" aria-label="{escape(title)}"><ol class="g6-ledger">{"".join(items)}</ol></section>'
          +f'<section class="g6-notice"><span class="g6-label">Sources <span aria-hidden="true">/</span> {"Autorité" if fr else "Authority"}</span><p>{escape(caveat)} <a href="/ecosystem/catalog.json">{"Catalogue source" if fr else "Source catalog"} ↗</a></p></section>')
    index_page(DIST,locale,f'/{locale}/ecosystem.html',title=f'{title} · gnu.in.labs',description=intro,section='ecosystem',body=body,edition=EDITION)

def build():
    if DIST.exists(): rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST/'ecosystem').mkdir(parents=True,exist_ok=True)
    copy2(DOCS/'ecosystem.json', DIST/'ecosystem'/'catalog.json')
    (DIST/'registry').mkdir(parents=True,exist_ok=True)
    copy2(DOCS/'source-registry.json', DIST/'registry'/'source-catalog.json')
    copy2(DOCS/'guide-registry.json', DIST/'registry'/'guide-catalog.json')
    copy2(DOCS/'release-registry.json', DIST/'registry'/'release-catalog.json')
    (DIST/'evidence').mkdir(parents=True,exist_ok=True)
    copy2(DOCS/'evidence'/'cuda-05d-public-results.json', DIST/'evidence'/'cuda-05d-public-results.json')
    copy2(DOCS/'evidence'/'cuda-05d-manifest.json', DIST/'evidence'/'cuda-05d-manifest.json')
    copy2(DOCS/'evidence'/'cuda-05e-public-results.json', DIST/'evidence'/'cuda-05e-public-results.json')
    copy2(DOCS/'evidence'/'cuda-05f-public-results.json', DIST/'evidence'/'cuda-05f-public-results.json')
    copy2(ROOT/'research'/'blob-in'/'CUDA-05G'/'PUBLIC-RESULTS.json', DIST/'evidence'/'cuda-05g-public-results.json')
    copy2(ROOT/'research'/'blob-in'/'CUDA-05H'/'PUBLIC-RESULTS.json', DIST/'evidence'/'cuda-05h-public-results.json')
    copy2(DOCS/'evidence'/'cuda-05f-manifest.json', DIST/'evidence'/'cuda-05f-manifest.json')
    copy2(DOCS/'evidence'/'gnostral-rtx3070-public-results.json', DIST/'evidence'/'gnostral-rtx3070-public-results.json')
    (DIST/'experiments').mkdir(parents=True,exist_ok=True)
    copy2(DOCS/'experiments'/'registry.json', DIST/'experiments'/'registry.json')
    copy2(DOCS/'experiments'/'GPU-EVIDENCE-CONTRACT-v1.json', DIST/'experiments'/'GPU-EVIDENCE-CONTRACT-v1.json')
    copy2(DOCS/'experiments'/'PIPELINE.md', DIST/'experiments'/'PIPELINE.md')
    (DIST/'challenges').mkdir(parents=True,exist_ok=True)
    copy2(DOCS/'challenges'/'registry.json', DIST/'challenges'/'registry.json')
    copy2(DOCS/'challenges'/'CONTRIBUTING.md', DIST/'challenges'/'CONTRIBUTING.md')
    for protocol in ('CUDA-05E-PREREG.md','CUDA-05F-PREREG.md'):
        (DIST/'challenges'/'protocols').mkdir(parents=True,exist_ok=True)
        copy2(DOCS/'challenges'/'protocols'/protocol, DIST/'challenges'/'protocols'/protocol)
    copy2(DOCS/'challenges'/'PROVENANCE.json', DIST/'challenges'/'PROVENANCE.json')
    for file in ('style.css','app.js','spine.css','spine.js','spine-map.js'):
        copy2(SITE/file,DIST/file)
    copytree(SITE/'gnu6',DIST/'gnu6')
    copytree(ASSETS/'diagrams',DIST/'diagrams',ignore=shutil.ignore_patterns('*.py','__pycache__'))
    copytree(ROOT/'examples',DIST/'examples',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    copytree(DOCS/'diagrams',DIST/'mermaid')
    copytree(DOCS/'templates',DIST/'templates')
    for locale in CATALOG['locales']:
        hub_page(locale)
        ecosystem_page(locale)
        challenge_meta,challenge_body=unpack(DOCS/locale/'challenges.md')
        shell(locale,challenge_meta['title'],render_markdown(challenge_body),f'/{locale}/challenges.html',status=challenge_meta['status'],section='challenges',kicker='Défis' if locale=='fr' else 'Challenges')
        render_experiment_registry(DIST,EXPERIMENTS,locale,EDITION)
        source_inventory_page(locale,'sdk')
        source_inventory_page(locale,'api')
        guides_pages(locale)
        releases_page(locale)
        study_meta,study_body=unpack(DOCS/locale/'studies'/'cuda-05d.md')
        shell(locale,study_meta['title'],render_markdown(study_body),f'/{locale}/studies/cuda-05d.html',status=study_meta['status'],section='experiments',kicker='Études' if locale=='fr' else 'Studies')
        study_meta_e,study_body_e=unpack(DOCS/locale/'studies'/'cuda-05e.md')
        shell(locale,study_meta_e['title'],render_markdown(study_body_e),f'/{locale}/studies/cuda-05e.html',status=study_meta_e['status'],section='experiments',kicker='Études' if locale=='fr' else 'Studies')
        study_meta_f,study_body_f=unpack(DOCS/locale/'studies'/'cuda-05f.md')
        shell(locale,study_meta_f['title'],render_markdown(study_body_f),f'/{locale}/studies/cuda-05f.html',status=study_meta_f['status'],section='experiments',kicker='Études' if locale=='fr' else 'Studies')
        study_meta_g,study_body_g=unpack(DOCS/locale/'studies'/'cuda-05g.md')
        shell(locale,study_meta_g['title'],render_markdown(study_body_g),f'/{locale}/studies/cuda-05g.html',status=study_meta_g['status'],section='experiments',kicker='Études' if locale=='fr' else 'Studies')
        study_meta_h,study_body_h=unpack(DOCS/locale/'studies'/'cuda-05h.md')
        shell(locale,study_meta_h['title'],render_markdown(study_body_h),f'/{locale}/studies/cuda-05h.html',status=study_meta_h['status'],section='experiments',kicker='Études' if locale=='fr' else 'Studies')
        g_meta,g_body=unpack(DOCS/locale/'studies'/'gnostral-rtx3070.md')
        shell(locale,g_meta['title'],render_markdown(g_body),f'/{locale}/studies/gnostral-rtx3070.html',status=g_meta['status'],section='experiments',kicker='Études' if locale=='fr' else 'Studies')
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
                inner=home_hero(locale)+corpus_ledger(locale)+f'<section class="g6-section home-note">{inner.replace("<h1","<h2").replace("</h1>","</h2>")}</section>'
            section='' if path.name=='index.md' else path.parent.name+'/'
            htmlpath=f'/{locale}/{section}{path.stem}.html'
            shell(locale,str(m.get('title',CORPUS_NAME)),inner,htmlpath,page_id,m.get('duration'),m.get('status','draft'))
        for slug in ('governance','references'):
            meta,body=unpack(DOCS/locale/f'{slug}.md')
            shell(locale,meta['title'],render_markdown(body),f'/{locale}/{slug}.html')
        shell(locale,'Topologies',topology(locale),f'/{locale}/topologies.html')
        shell(locale,'Modèles' if locale=='fr' else 'Templates',template_index(locale),f'/{locale}/templates.html')
    (DIST/'index.html').write_text(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=/fr/hub.html"><title>{escape(CORPUS_NAME)}</title></head><body><a href="/fr/hub.html">Portail français →</a></body></html>',encoding='utf-8')
    index_page(DIST,'fr','/404.html',title=f'404 · {CORPUS_NAME}',description='Page introuvable / Page not found',section='',edition=EDITION,
               body=registry_hero('fr','HTTP 404','Page introuvable','Cette route n’existe pas. This route does not exist.')
               +'<section class="g6-section"><p class="g6-hero__actions"><a class="g6-action" href="/fr/hub.html">Documentation (FR) <span class="g6-action__arrow" aria-hidden="true">→</span></a><a class="g6-action g6-action--quiet" href="/en/hub.html" lang="en">Documentation (EN) <span aria-hidden="true">→</span></a></p></section>')
    # Public static assets must be readable by an unprivileged Nginx worker,
    # even on a workstation whose umask is restrictive (e.g. 0077).
    DIST.chmod(0o755)
    for path in DIST.rglob('*'):
        path.chmod(0o755 if path.is_dir() else 0o644)
    print(f'BUILD_OK pages={len(list(DIST.rglob("*.html")))} assets={len(list(DIST.rglob("*.svg")))}')

if __name__=='__main__':
    build()
