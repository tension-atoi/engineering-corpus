#!/usr/bin/env python3
"""Source-backed, bilingual study register renderer; no live data or runtime claims."""
from html import escape
from pathlib import Path

def render_experiment_registry(dist:Path, registry:dict, locale:str)->None:
    fr=locale=="fr"
    other="en" if fr else "fr"
    title="Registre des expériences" if fr else "Experiment registry"
    intro=("Chaque ligne distingue protocole, observation, limites et revue. Un statut local ne vaut pas certification."
           if fr else "Every record separates protocol, observation, limits and review. Local status is not a certification.")
    rows=[]
    for record in registry["entries"]:
        statement=record["claim"][locale]
        description=record["scope"][locale]
        page=record["pages"][locale]
        evidence=record["source_file"]
        banner=("OBSERVATION BORNÉE / BROUILLON" if fr else "BOUNDED OBSERVATION / DRAFT")
        unavailable=("Preuves brutes privées · reproduction externe non démontrée"
                     if fr else "Raw evidence private · external replication not demonstrated")
        level=record["evidence_class"].split(" / ",1)[0]
        evidence_caption="observation interne ponctuelle" if fr else "single internal observation"
        review_caption="brouillon" if fr else record["status"]
        page_label="Lire l’étude" if fr else "Read study"
        data_label="Données assainies" if fr else "Sanitized data"
        rows.append(f'''<article class="registry-entry" id="{escape(record["id"],quote=True)}">
<div class="registry-entry-head"><span class="registry-kicker">{banner}</span>
<span class="registry-version">{escape(record["revision"])} · {escape(level)} / {escape(evidence_caption)}</span></div>
<h2>{escape(record["id"])} — {escape(statement)}</h2><p>{escape(description)}</p>
<dl class="registry-facts">
<dt>{'Protocole figé' if fr else 'Frozen protocol'}</dt><dd><code>{escape(record["protocol_commit"][:12])}</code></dd>
<dt>{'Source de l’analyse' if fr else 'Analysis source'}</dt><dd><code>{escape(record["source_commit"][:12])}</code></dd>
<dt>{'Gate production' if fr else 'Production gate'}</dt><dd>{escape(record["production_authorization"])}</dd>
<dt>{'Statut de revue' if fr else 'Review status'}</dt><dd>{escape(review_caption)}</dd>
</dl><p class="ecosystem-evidence">{escape(unavailable)}</p>
<div class="registry-links"><a href="{escape(page,quote=True)}">{page_label} ↗</a>
<a href="{escape(evidence,quote=True)}">{data_label} ↗</a></div></article>''')
    itemlist="".join(rows)
    study=('<article class="registry-entry"><h2>Gnostral / RTX 3070 · Q-010 &amp; Q-011</h2>'
           '<p>'+('Recherche locale reproductible sous contraintes : copies MoE et placement CPU/GPU. Revues externes en attente.' if fr else
                   'Bounded local inference research: MoE weight copies and CPU/GPU placement. External review pending.')
           +'</p><div class="registry-links"><a href="/'+locale+'/studies/gnostral-rtx3070.html">'
           +('Lire l étude' if fr else 'Read study')+' ↗</a>'
           '<a href="/evidence/gnostral-rtx3070-public-results.json">'
           +('Données assainies' if fr else 'Sanitized observations')+' ↗</a></div></article>')

    other_label="English" if fr else "Français"
    index_label="Retour au portail" if fr else "Back to portal"
    policy=("Données nettoyées; les journaux originaux restent internes. Les hashes de données privées ne rendent pas les échantillons accessibles. Aucune autorisation de production."
            if fr else "Sanitized data; original logs remain internal. Private-data digests do not make observations accessible. No production authorization.")
    html=f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark">
<meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; script-src 'self'; img-src 'self'; font-src 'self'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'">
<title>{escape(title)} · gnu.in.labs</title><link rel="stylesheet" href="/style.css">
<link rel="alternate" hreflang="{other}" href="/{other}/experiments.html">
<link rel="alternate" hreflang="{locale}" href="/{locale}/experiments.html"></head>
<body class="hub-page"><a class="skip" href="#content">{'Aller au contenu' if fr else 'Skip to content'}</a>
<header class="hub-header"><a class="hub-logo" href="/{locale}/hub.html"><strong>gnu.in.labs</strong><span>/</span><span>docs</span></a>
<nav class="hub-global-nav" aria-label="{'Navigation principale' if fr else 'Primary navigation'}">
<a href="/{locale}/hub.html">{'Portail' if fr else 'Portal'}</a>
<a href="/{locale}/index.html">Corpus</a>
<a href="/{locale}/ecosystem.html">{'Écosystème' if fr else 'Ecosystem'}</a></nav>
<a class="hub-language" lang="{other}" href="/{other}/experiments.html">{other_label} ↗</a></header>
<main class="hub-main registry-main" id="content" tabindex="-1">
<a class="registry-back" href="/{locale}/hub.html">← {index_label}</a>
<header class="registry-hero"><span class="hub-kicker">GNU.IN.LABS / {'RECHERCHE & PREUVES' if fr else 'RESEARCH & EVIDENCE'}</span>
<h1>{escape(title)}</h1><p class="hub-lede">{escape(intro)}</p>
<div class="registry-status"><span>{escape(registry["registry_version"])}</span>
<strong>{len(registry["entries"]):02d} / {'EXPÉRIENCES' if fr else 'EXPERIMENTS'}</strong></div></header>
<section class="registry-entries" aria-label="{escape(title)}">{itemlist}{study}</section>
<section class="hub-policy"><span class="hub-kicker">{'PREUVES / AUTORITÉ' if fr else 'EVIDENCE / AUTHORITY'}</span>
<p>{escape(policy)} <a href="/experiments/registry.json">{'Registre JSON' if fr else 'Machine-readable registry'} ↗</a>
 · <a href="/templates/EXPERIMENT.md">{'Modèle de recherche' if fr else 'Research contract'} ↗</a>
 · <a href="/experiments/PIPELINE.md">{'Pipeline de preuves' if fr else 'Evidence pipeline' } ↗</a></p></section>
<footer class="hub-footer"><span>gnu.in.labs · DOCS-HUB-01G</span>
<span>{'Études non ratifiées' if fr else 'Unratified studies'}</span></footer></main></body></html>'''
    page=dist/locale/"experiments.html"
    page.parent.mkdir(parents=True,exist_ok=True)
    page.write_text(html,encoding="utf-8")
