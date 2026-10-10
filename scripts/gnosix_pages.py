"""GNOSIX source-owned technical pages in the GNU6 federation portal."""
from __future__ import annotations
import html
import json
from pathlib import Path
import re

from gnu6_shell import index_page, state
from federation_pages import hero, rewrite_links, source_href

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"docs/federation/gnosix"
SOURCE_DOCS=(
  ("overview","README.md","Vue générale","Overview"),
  ("status","docs/status/STATUS.md","Statut actuel","Current status"),
  ("roadmap","docs/status/ROADMAP.md","Feuille de route","Roadmap"),
  ("evidence","docs/evidence/CURRENT.md","Preuves courantes","Current evidence"),
  ("methodology","docs/evidence/README.md","Modèle de preuves","Evidence model"),
)
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
TITLE = re.compile(r"^# [^\n]*\n?",re.M)

def verify():
    from federate_gnosix import verify as source_verify
    return source_verify()

def nav(lang):
    fr=lang=="fr"
    parts=[("index","Projet" if fr else "Project")]+[(key,f if fr else en) for key,_,f,en in SOURCE_DOCS]
    return ('<nav class="g6-record__links" aria-label="gnosix source navigation">'+
            ''.join(f'<a class="g6-action g6-action--quiet" href="/{lang}/projects/gnosix/{key}.html">{html.escape(label)} →</a>'
                   for key,label in parts)+'</nav>')

def landing(lang,m):
    fr=lang=="fr"
    title="Gnosix — plateforme Linux locale expérimentale" if fr else "Gnosix — experimental local-first Linux platform"
    description=("Rust, Wayland et GPUI : surfaces natives, identité de session, profils et autorités bornées. Logiciel expérimental, sans acceptation globale de release."
                 if fr else "Rust, Wayland and GPUI: native surfaces, session identity, profiles and bounded authorities. Experimental software; whole-product release acceptance remains open.")
    records=[
      ("PROVEN","Native Bar / Dock / Workspace / AppStack" if fr else "Native Bar / Dock / Workspace / AppStack",
        "Limites du chemin installé dans le registre de preuves." if fr else "Bounded installed-path claims in the evidence ledger."),
      ("SOURCE-QUALIFIED","Identité logique durable" if fr else "Durable logical identity",
        "Contrat source; pas une identité de matériel physique." if fr else "Source contract, not physical hardware identity."),
      ("OPEN","Acceptation de release complète" if fr else "Whole-product release acceptance",
        "R19 et revue humaine d'accessibilité restent ouverts." if fr else "R19 and human accessibility review remain open."),
    ]
    cards=''.join('<article class="g6-record"><div class="g6-record__head">'+
        state("experimental",status)+'</div><h2>'+html.escape(name)+'</h2><p>'+
        html.escape(detail)+'</p></article>' for status,name,detail in records)
    license_warning=("À réconcilier dans le dépôt source : README et LICENSE déclarent la GPL-3.0-or-later, tandis que la page STATUS énumère encore une ratification de licence inachevée. Le portail ne prend pas position sur la clôture de cette obligation."
       if fr else "Source discrepancy pending reconciliation: README and LICENSE declare GPL-3.0-or-later, while STATUS still lists license ratification as unfinished. The portal does not close that upstream obligation.")
    info=("Documents originaux en anglais, liés au commit exact et validés par SHA-256. Les reçus d'exécution privés ne sont pas republiés."
          if fr else "Original English source documents, commit-pinned and SHA-256 verified. Private runtime receipts are not republished.")
    body=(f'<section class="g6-section"><div class="g6-ledger">{cards}</div></section>'
          f'<section class="g6-section">{nav(lang)}</section>'
          '<section class="g6-notice"><span class="g6-label">EXPERIMENTAL · SOURCE-OWNED</span>'
          f'<p>{html.escape(info)}</p><p><code>{m["source_ref"]}</code> · '
          '<a href="/registry/federation-gnosix.json">SHA-256 / manifest →</a></p></section>'
          '<section class="g6-notice"><span class="g6-label">EDITORIAL DISCREPANCY</span>'
          f'<p>{html.escape(license_warning)}</p></section>')
    return title,description,body

def build_pages(dist,locales,edition,render_markdown):
    m=verify()
    for lang in locales:
        title,description,body=landing(lang,m)
        index_page(dist,lang,f'/{lang}/projects/gnosix/index.html',title=title,description=description,
                   section="ecosystem",body=hero(title,description)+body,edition=edition)
        for key,source,fr,en in SOURCE_DOCS:
            original=(BASE/"content"/source).read_text("utf-8")
            # Source image assets are not part of the approved 5-document hash
            # allowlist: omit them rather than embedding unqualified remote bytes.
            body=IMAGE.sub("",original)
            body=TITLE.sub("",body,count=1)
            body=rewrite_links(body,source,m)
            rendered=render_markdown(body)
            label=fr if lang=="fr" else en
            page_title="Gnosix / "+label
            desc=("Document technique source en anglais, version Git exacte. Statut expérimental; aucune release stable."
                  if lang=="fr" else "Original English source, exact pinned Git revision. Experimental; no stable release.")
            provenance=('<section class="g6-notice"><span class="g6-label">SOURCE / GPL-3.0-or-later</span>'
                       f'<p><code>{m["source_ref"]}</code> · <code>sha256:{m["files"][source]}</code></p>'
                       f'<p><a href="{html.escape(source_href(m,source),quote=True)}">{"Source GitHub" if lang=="fr" else "Original GitHub source"}</a> · '
                       f'<a href="{html.escape(source_href(m,"LICENSE"),quote=True)}">GPL-3.0-or-later / licence upstream</a></p>'
                       '</section>')
            notice=('<section class="g6-section"><p class="g6-label">'+
                    ("Document source anglais (original, non traduit)" if lang=="fr"
                       else "Exact English original from pinned source")+'</p>'+
                    nav(lang)+'</section>')
            index_page(dist,lang,f'/{lang}/projects/gnosix/{key}.html',
                       title=page_title,description=desc,section="ecosystem",
                       body=hero(page_title,desc)+notice+
                         f'<section class="g6-section"><article class="g6-prose">{rendered}</article></section>'+
                         provenance,edition=edition)
    (dist/"registry").mkdir(exist_ok=True)
    (dist/"registry/federation-gnosix.json").write_text(json.dumps(m,indent=2,sort_keys=True)+"\n")
