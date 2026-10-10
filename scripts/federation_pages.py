"""Deterministic project federation pages from reviewed, pinned Markdown snapshots."""
from __future__ import annotations
import html
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit

from gnu6_shell import index_page, state

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "federation" / "gnostral"
MANIFEST = BASE / "manifest.json"
PAGES = (
    ("overview", "docs/START_HERE.md", "Vue d’ensemble", "Overview"),
    ("capabilities", "docs/CAPABILITY_MATRIX.md", "Capacités et preuves", "Capabilities and evidence"),
    ("questlog", "QUESTLOG.md", "Journal des quêtes", "Questlog"),
    ("roadmap", "docs/ROADMAP.md", "Feuille de route", "Roadmap"),
    ("architecture", "docs/ARCHITECTURE.md", "Architecture", "Architecture"),
    ("reproducibility", "docs/REPRODUCIBILITY.md", "Reproduction", "Reproduction"),
)
PATHROOT = "projects/gnostral"
BRANCH = "main"
REL_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
MD_H1 = re.compile(r"^# [^\n]+\n?",re.M)

def verify_snapshot():
    from federate_gnostral import verify
    return verify()

def source_href(manifest, path):
    return manifest["repository"]+"/blob/"+manifest["source_ref"]+"/"+path

def rewrite_links(body: str, path: str, manifest: dict) -> str:
    """Non-network rewriting: absolute internal gnostral Markdown paths → pinned source."""
    def repl(m):
        label,target=m.group(1),m.group(2)
        if target.startswith(("#", "https://", "http://", "mailto:")):
            return m.group(0)
        parts=urlsplit(target)
        if parts.scheme or parts.netloc or target.startswith("/"):
            raise ValueError("unsupported source-relative link: "+target)
        # source Markdown paths refer to the gnostral git root or their directory.
        rooted=posixpath.normpath(posixpath.join(posixpath.dirname(path),parts.path))
        if rooted.startswith("../"):
            raise ValueError("source-relative link escapes project")
        href=source_href(manifest,rooted)
        if parts.fragment:
            href+="#"+parts.fragment
        return "["+label+"]("+href+")"
    return REL_LINK.sub(repl,body)

def navigation(locale):
    labels={
        "fr":("Projet","Vue d’ensemble","Capacités","QUESTLOG","Roadmap","Architecture","Reproduction"),
        "en":("Project","Overview","Capabilities","QUESTLOG","Roadmap","Architecture","Reproduction"),
    }[locale]
    links=[("index",labels[0])]+[(key,name) for (key,*_),name in zip(PAGES,labels[1:])]
    out=[]
    for key,name in links:
        filename="index.html" if key=="index" else key+".html"
        out.append(f'<a class="g6-action g6-action--quiet" href="/{locale}/{PATHROOT}/{filename}">{html.escape(name)} →</a>')
    return '<nav class="g6-record__links" aria-label="'+("Parcours Gnostral" if locale=="fr" else "Gnostral documentation")+'">'+''.join(out)+'</nav>'

def landing(locale,manifest):
    fr=locale=="fr"
    title="gnostral.rs — inférence Rust, preuves réelles" if fr else "gnostral.rs — Rust inference, real evidence"
    intro=("Un laboratoire ouvert sur RTX 3070 8 Gio : exécution quantifiée, récupération des ressources, cycles de vie et vérification indépendante. Pas encore un serveur multi-modèle de production."
        if fr else "An open RTX 3070 8 GiB laboratory: low-bit inference, resource recovery, model lifecycles and independent verification. Not yet a production multi-model server.")
    facts=[
        ("Q-010","2,12×","Médiane MoE CPU : 9,51 → 20,18 tok/s" if fr else "CPU MoE median: 9.51 → 20.18 tok/s"),
        ("Q-012","3/3 PASS","Dense, embeddings et MoE successifs" if fr else "Sequential dense, embeddings and MoE"),
        ("Q-013C","+8 Mio" if fr else "+8 MiB","Delta VRAM ambiante après arrêt du pilote dense" if fr else "Ambient VRAM delta after dense pilot shutdown"),
    ]
    cards=''.join(
        f'<article class="g6-record"><div class="g6-record__head">{state("experimental",key)}'
        '<span class="g6-label">RTX 3070 · LOCAL</span></div>'
        f'<h2>{html.escape(number)}</h2><p>{html.escape(desc)}</p></article>'
        for key,number,desc in facts)
    source=source_href(manifest,"docs/START_HERE.md")
    pin=manifest["source_ref"]
    text=("Le dépôt gnostral.rs reste propriétaire de ses documents. Ces pages sont construites depuis un instantané approuvé, et non depuis un flux GitHub non vérifié. Les benchmarks ne démontrent ni hot-swap, ni service permanent."
        if fr else "The gnostral.rs repository owns its documentation. These pages are built from a reviewed snapshot, not a mutable GitHub feed. The benchmarks do not prove hot swap or persistent serving.")
    body=(f'<section class="g6-section"><div class="g6-record__links"><a class="g6-action" href="/{locale}/{PATHROOT}/overview.html">'
          +("Lire la documentation" if fr else "Read the documentation")
          +f' →</a><a class="g6-action g6-action--quiet" href="{html.escape(source,quote=True)}">'
          +("Source GitHub exacte" if fr else "Exact GitHub source")
          +'</a></div></section>'
          +f'<section class="g6-section" aria-label="{"Résultats" if fr else "Results"}"><div class="g6-ledger">{cards}</div></section>'
          +'<section class="g6-section">'+navigation(locale)+'</section>'
          +'<section class="g6-notice"><span class="g6-label">Source / SHA-256</span>'
          +f'<p>{html.escape(text)}</p><p><code>{pin}</code> · '
          +f'<a href="/registry/federation-gnostral.json">{"Manifeste vérifiable" if fr else "Verifiable manifest"} ↗</a></p></section>')
    return title,intro,body

def project_index(locale):
    fr=locale=="fr"
    title="Projets et sources" if fr else "Projects and sources"
    intro=("Des portes d’entrée vers les dépôts qualifiés. Chaque fiche indique sa provenance plutôt que promettre une fonctionnalité non publiée."
        if fr else "Entry points to qualified public sources. Each project cites its provenance instead of promising unreleased capabilities.")
    summary=("Inférence locale en Rust, quantification et enveloppe d’exécution contrôlée, qualification expérimentale et documentation liée aux commits."
        if fr else "Local Rust inference, quantization and bounded execution, experimental qualification with commit-linked documentation.")
    body=(f'<section class="g6-section"><article class="g6-record"><div class="g6-record__head">{state("experimental","RESEARCH · EXPERIMENTAL")}</div>'
          f'<h2>gnostral.rs</h2><p>{html.escape(summary)}</p><div class="g6-record__links">'
          f'<a class="g6-action" href="/{locale}/{PATHROOT}/index.html">{"Explorer le projet" if fr else "Explore project"} →</a></div></article></section>'
          '<section class="g6-notice"><span class="g6-label">Source / Autorité</span><p>'
          +("Un dépôt public n’est pas automatiquement un produit déployé. Aucun SDK n’est annoncé ici."
            if fr else "A public repository is not automatically a deployed product. No SDK is announced here.")
          +'</p></section>')
    return title,intro,body

def hero(title: str, description: str) -> str:
    return (f'<section class="g6-hero g6-hero--compact"><div class="g6-hero__copy">'
            f'<span class="g6-label">gnu.in.labs / FEDERATED SOURCE</span>'
            f'<h1 class="g6-display">{html.escape(title)}</h1>'
            f'<p class="g6-lede">{html.escape(description)}</p></div></section>')

def build_pages(dist,locales,edition,render_markdown):
    manifest=verify_snapshot()
    for locale in locales:
        title,intro,body=project_index(locale)
        index_page(dist,locale,f'/{locale}/projects.html',title=title,description=intro,
                   section='ecosystem',body=hero(title,intro)+body,edition=edition)
        title,intro,body=landing(locale,manifest)
        index_page(dist,locale,f'/{locale}/{PATHROOT}/index.html',title=title,
                   description=intro,section='ecosystem',body=hero(title,intro)+body,edition=edition)
        for key,source,fr,en in PAGES:
            body=(BASE/"content"/source).read_text("utf-8")
            body=MD_H1.sub("",body,count=1)
            body=rewrite_links(body,source,manifest)
            rendered=render_markdown(body)
            label=fr if locale=="fr" else en
            heading="Document source en anglais (version exacte du dépôt)" if locale=="fr" else "Original upstream English source (exact revision)"
            prefix=f'<section class="g6-section"><p class="g6-label">{html.escape(heading)}</p>{navigation(locale)}</section>'
            href=source_href(manifest,source)
            provenance=(f'<section class="g6-notice"><span class="g6-label">GIT / SOURCE</span><p><code>{manifest["source_ref"]}</code> · '
                        f'<code>sha256:{manifest["files"][source]}</code></p>'
                        f'<p><a href="{html.escape(href,quote=True)}" rel="noopener noreferrer">'
                        +("Voir le Markdown original" if locale=="fr" else "Read original Markdown")
                        +'</a></p></section>')
            description=("Documentation reprise depuis le dépôt public avec commit et SHA vérifiés. Contenu technique anglais original."
                         if locale=="fr" else "Exact source-backed documentation snapshot, pinned to a public commit and SHA.")
            index_page(dist,locale,f'/{locale}/{PATHROOT}/{key}.html',
                       title="gnostral.rs / "+label, description=description,section='ecosystem',
                       body=hero('gnostral.rs / '+label,description)+prefix+f'<section class="g6-section"><article class="g6-prose">{rendered}</article></section>'+provenance,
                       edition=edition)
    (dist/"registry").mkdir(exist_ok=True)
    (dist/"registry"/"federation-gnostral.json").write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n")
