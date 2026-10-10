#!/usr/bin/env python3
"""Source-backed, bilingual study register renderer; no live data or runtime claims."""
from html import escape
from pathlib import Path

from gnu6_shell import index_page, state


def render_experiment_registry(dist:Path, registry:dict, locale:str, edition:str="")->None:
    fr=locale=="fr"
    title="Registre des expériences" if fr else "Experiment registry"
    intro=("Chaque ligne distingue protocole, observation, limites et revue. Un statut local ne vaut pas certification."
           if fr else "Every record separates protocol, observation, limits and review. Local status is not a certification.")
    rows=[]
    for record in registry["entries"]:
        statement=record["claim"][locale]
        description=record["scope"][locale]
        page=record["pages"][locale]
        evidence=record["source_file"]
        banner=("Observation bornée / brouillon" if fr else "Bounded observation / draft")
        unavailable=("Preuves brutes privées · reproduction externe non démontrée"
                     if fr else "Raw evidence private · external replication not demonstrated")
        level=record["evidence_class"].split(" / ",1)[0]
        evidence_caption="observation interne ponctuelle" if fr else "single internal observation"
        review_caption="brouillon" if fr else record["status"]
        page_label="Lire l’étude" if fr else "Read study"
        data_label="Données assainies" if fr else "Sanitized data"
        rows.append(f'''<article class="g6-record" id="{escape(record["id"],quote=True)}">
<div class="g6-record__head">{state("attention",banner)}
<span class="g6-label">{escape(record["revision"])} · {escape(level)} / {escape(evidence_caption)}</span></div>
<h2>{escape(record["id"])} — {escape(statement)}</h2><p>{escape(description)}</p>
<dl class="g6-facts">
<dt>{'Protocole figé' if fr else 'Frozen protocol'}</dt><dd><code>{escape(record["protocol_commit"][:12])}</code></dd>
<dt>{'Source de l’analyse' if fr else 'Analysis source'}</dt><dd><code>{escape(record["source_commit"][:12])}</code></dd>
<dt>{'Gate production' if fr else 'Production gate'}</dt><dd>{state("attention",record["production_authorization"])}</dd>
<dt>{'Statut de revue' if fr else 'Review status'}</dt><dd>{escape(review_caption)}</dd>
<dt>{'Accès aux preuves' if fr else 'Evidence access'}</dt><dd>{escape(unavailable)}</dd>
</dl>
<div class="g6-record__links"><a class="g6-action" href="{escape(page,quote=True)}">{page_label} <span class="g6-action__arrow" aria-hidden="true">→</span></a>
<a class="g6-action g6-action--quiet" href="{escape(evidence,quote=True)}">{data_label} <span aria-hidden="true">↓</span></a></div></article>''')
    policy=("Données nettoyées; les journaux originaux restent internes. Les hashes de données privées ne rendent pas les échantillons accessibles. Aucune autorisation de production."
            if fr else "Sanitized data; original logs remain internal. Private-data digests do not make observations accessible. No production authorization.")
    body=(f'<section class="g6-hero g6-hero--compact"><div class="g6-hero__copy"><span class="g6-label">gnu.in.labs <span aria-hidden="true">/</span> {"Recherche & preuves" if fr else "Research & evidence"}</span>'
          f'<h1 class="g6-display">{escape(title)}</h1><p class="g6-lede">{escape(intro)}</p>'
          f'<p class="g6-registry-count"><span>{escape(registry["registry_version"])}</span><strong class="g6-num">{len(registry["entries"]):02d} / {"EXPÉRIENCES" if fr else "EXPERIMENTS"}</strong></p></div></section>'
          f'<section class="g6-section" aria-label="{escape(title)}">{"".join(rows)}</section>'
          f'<section class="g6-notice"><span class="g6-label">{"Preuves / autorité" if fr else "Evidence / authority"}</span>'
          f'<p>{escape(policy)} <a href="/experiments/registry.json">{"Registre JSON" if fr else "Machine-readable registry"} ↗</a>'
          f' · <a href="/templates/EXPERIMENT.md">{"Modèle de recherche" if fr else "Research contract"} ↗</a>'
          f' · <a href="/experiments/PIPELINE.md">{"Pipeline de preuves" if fr else "Evidence pipeline"} ↗</a></p></section>')
    index_page(dist,locale,f"/{locale}/experiments.html",title=f"{title} · gnu.in.labs",description=intro,section="experiments",
               body=body,edition=edition,footer_note=("Études non ratifiées" if fr else "Unratified studies"))
