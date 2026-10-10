"""gnu6-design adapter for docs.gnu6.live: one shell for every generated page.

The shared contract (system bar, masthead, footer, ledger, state, record, notice) lives in
the vendored gnu6-design package under site/gnu6/. This module only maps the corpus' data
to that markup. It never fetches, never inlines styles, and keeps the strict static CSP.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = json.loads((ROOT / "site" / "gnu6" / "gnu6-design.lock.json").read_text("utf-8"))
DESIGN_VERSION = DESIGN["version"]
CSS = f"/gnu6/gnu6.css?v={DESIGN_VERSION}"
SITE_CSS = f"/style.css?v={DESIGN_VERSION}"
GNU6 = "https://gnu6.live"
CODE = "https://github.com/tension-atoi"
DOCS_ORIGIN = "https://docs.gnu6.live"

# Public external hrefs the shared shell itself emits (allow-listed by scripts/validate.py).
SYSTEM_LINKS = (f"{GNU6}/", f"{GNU6}/?lang=en", f"{GNU6}/login", f"{GNU6}/login?lang=en", f"{GNU6}/motion/index.html", CODE)

STATE = {
    # hub/registry state -> gnu6-design state modifier (shape + colour + text)
    "available": "stable",
    "experimental": "attention",
    "guide": "attention",
    "inventory": "empty",
    "planned": "planned",
}


def t(locale: str, fr: str, en: str) -> str:
    return fr if locale == "fr" else en


def state(kind: str, label: str) -> str:
    return f'<span class="g6-state g6-state--{STATE.get(kind, kind)}">{escape(label)}</span>'


def label(text: str, *, sep: str | None = None) -> str:
    if sep:
        a, b = text.split(sep, 1)
        return f'<span class="g6-label">{escape(a.strip())} <span aria-hidden="true">/</span> {escape(b.strip())}</span>'
    return f'<span class="g6-label">{escape(text)}</span>'


def _csp(scripts: bool) -> str:
    script = "script-src 'self'; "
    return (f"default-src 'none'; style-src 'self'; {script}img-src 'self'; font-src 'self'; "
            "connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'")


def head(locale: str, path: str, alt_path: str, title: str, description: str, *, scripts: bool, og: str) -> str:
    other = "en" if locale == "fr" else "fr"
    return f"""<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{_csp(scripts)}"><meta name="referrer" content="no-referrer">
<meta name="color-scheme" content="dark light"><meta name="theme-color" media="(prefers-color-scheme: dark)" content="#111418"><meta name="theme-color" media="(prefers-color-scheme: light)" content="#F7F3ED">
<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:image" content="{DOCS_ORIGIN}/gnu6/social/{og}"><meta property="og:url" content="{DOCS_ORIGIN}{escape(path, quote=True)}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="64x64" href="/gnu6/identity/gnuinlabs-64.png"><link rel="apple-touch-icon" href="/gnu6/identity/gnuinlabs-128.png">
<link rel="stylesheet" href="{CSS}"><link rel="stylesheet" href="{SITE_CSS}"><link rel="stylesheet" href="/spine.css"><script src="/spine-map.js" defer></script><script src="/spine.js" defer></script>{'<script src="/app.js" defer></script>' if scripts else ''}
<link rel="alternate" hreflang="{locale}" href="{escape(path, quote=True)}"><link rel="alternate" hreflang="{other}" href="{escape(alt_path, quote=True)}"></head>"""


def system_bar(locale: str, alt_path: str) -> str:
    """Identical GNU6 system bar; on docs the 'Docs' destination is current."""
    other = "en" if locale == "fr" else "fr"
    q = "?lang=en" if locale == "en" else ""
    home = f"{GNU6}/{q}"
    hub = f"/{locale}/hub.html"
    portal = f"{GNU6}/login{q}"
    lang_name = t(locale, "View in English", "Voir en français")
    items = [
        (home, t(locale, "Accueil", "Home"), False, False),
        (hub, "Docs", True, False),
        (f"{GNU6}/motion/index.html", "Motion", False, True),
        (CODE, "Code", False, True),
    ]
    inline = "".join(
        f'<a href="{escape(h, quote=True)}"{" aria-current=\"true\"" if cur else ""}>{escape(n)}'
        f'{" <span class=\"g6-ext\" aria-hidden=\"true\">↗</span>" if ext else ""}</a>'
        for h, n, cur, ext in items
    )
    panel = "".join(
        f'<a href="{escape(h, quote=True)}"{" aria-current=\"page\"" if cur else ""}><span>{escape(n)}</span>'
        f'<span aria-hidden="true">{"↗" if ext else "→"}</span></a>'
        for h, n, cur, ext in items
    )
    panel += (f'<a href="{escape(alt_path, quote=True)}" hreflang="{other}" lang="{other}"><span>{escape(lang_name)}</span>'
              f'<span aria-hidden="true">{other.upper()}</span></a>')
    return f"""<header class="g6-sysbar"><div class="g6-frame g6-sysbar__inner">
<a class="g6-brand" href="{hub}" aria-label="docs.gnu6.live"><img src="/gnu6/identity/gnuinlabs-64.png" width="28" height="28" alt=""><span class="g6-brand__word">docs.gnu6.live</span></a>
<nav class="g6-sysnav" aria-label="{t(locale, 'Navigation principale', 'Main navigation')}">{inline}</nav>
<div class="g6-sysbar__end"><a class="g6-lang lang" href="{escape(alt_path, quote=True)}" hreflang="{other}" lang="{other}" aria-label="{escape(lang_name)}">{other.upper()}</a>
<a class="g6-action g6-action--portal" href="{portal}">{t(locale, 'Portail', 'Portal')}</a>
<details class="g6-sysmenu"><summary>Menu</summary><nav class="g6-sysmenu__panel" aria-label="{t(locale, 'Navigation compacte', 'Compact navigation')}">{panel}</nav></details></div>
</div></header>"""


MASTHEAD = (
    ("hub", "/{l}/hub.html", "Index", "Index"),
    ("corpus", "/{l}/index.html", "Corpus", "Corpus"),
    ("experiments", "/{l}/experiments.html", "Expériences", "Experiments"),
    ("challenges", "/{l}/challenges.html", "Défis", "Challenges"),
    ("references", "/{l}/api.html", "API & SDK", "API & SDK"),
    ("ecosystem", "/{l}/ecosystem.html", "Écosystème", "Ecosystem"),
)


def masthead(locale: str, section: str) -> str:
    links = "".join(
        f'<a href="{href.format(l=locale)}"{" aria-current=\"page\"" if key == section else ""}>{escape(t(locale, fr, en))}</a>'
        for key, href, fr, en in MASTHEAD
    )
    return f"""<div class="g6-masthead"><div class="g6-frame g6-masthead__inner">
<a class="g6-masthead__title" href="/{locale}/hub.html"><img src="/gnu6/identity/gnuinlabs-64.png" width="22" height="22" alt="">gnu.in.labs <span aria-hidden="true">/</span> <span class="g6-masthead__sub">{t(locale, 'Documentation', 'Documentation')}</span></a>
<nav class="g6-masthead__nav" aria-label="{t(locale, 'Documentation', 'Documentation')}">{links}</nav>
</div></div>"""



def spine(locale: str, path: str) -> str:
    """Domain-specific GNU6 Spine: real anchors, no JavaScript required for links."""
    hub = f"/{locale}/hub.html"
    en = locale == "en"
    items = (
        ("01", hub, "Index documentaire" if not en else "Documentation index"),
        ("02", f"/{locale}/api.html", "Références API" if not en else "API references"),
        ("03", f"/{locale}/sdk.html", "Inventaire SDK" if not en else "SDK inventory"),
        ("04", f"/{locale}/guides.html", "Guides"),
        ("05", f"/{locale}/index.html", "Corpus méthodologique" if not en else "Methodological corpus"),
        ("06", f"/{locale}/experiments.html", "Expériences" if not en else "Experiments"),
        ("07", f"/{locale}/releases.html", "Versions" if not en else "Releases"),
    )
    links = "".join(
        f'<a href="{href}"' + (' aria-current="page"' if href == path else '')
        + f'><span aria-hidden="true">{num}</span>{escape(name)}</a>'
        for num, href, name in items
    )
    live = f"{GNU6}/" + ("?lang=en" if en else "")
    search = "Rechercher" if not en else "Search"
    atlas = "Explorer" if not en else "Explore"
    return (f'<aside class="g6-spine" id="gnu6-spine" aria-label="'
            + ("Navigation GNU6 et Docs" if not en else "GNU6 and Docs navigation") + '">'
            + '<div class="g6-spine__header"><span class="g6-spine__brand">ESPACE / GNU6</span>'
            + f'<div class="g6-spine__domains"><a href="{live}">GNU6</a>'
            + f'<a data-domain-active="true" href="{hub}">Docs</a></div></div>'
            + '<div class="g6-spine__actions"><button type="button" class="g6-spine__control" '
            + f'data-g6-open-search>{search} <kbd>/</kbd></button><button type="button" '
            + f'class="g6-spine__control" data-g6-open-atlas>{atlas} ▦</button></div>'
            + '<nav class="g6-spine__group" aria-label="'
            + ("Parcours documentaires" if not en else "Documentation paths") + '">'
            + '<span class="g6-spine__label">' + ("PARCOURIR" if not en else "BROWSE") + '</span>'
            + links + '</nav></aside>')


def spine_mobile(locale: str) -> str:
    return ('<div class="g6-spine__mobile-wrap"><button type="button" '
            'class="g6-spine__mobile" data-g6-spine-toggle aria-controls="gnu6-spine" '
            'aria-expanded="false">☰ ' + ("Navigation" if locale == "fr" else "Navigation")
            + '</button></div>')

def footer(locale: str, edition: str, note: str | None = None) -> str:
    q = "?lang=en" if locale == "en" else ""
    note = note or t(locale, "Édition de travail · non ratifiée", "Draft study edition · not ratified")
    return f"""<footer class="g6-footer"><div class="g6-frame g6-footer__inner">
<div class="g6-footer__org"><img src="/gnu6/identity/gnuinlabs-64.png" width="20" height="20" alt=""><span>gnu.in.labs · Montréal</span></div>
<p>{escape(note)} · {escape(edition)} · gnu6-design {escape(DESIGN_VERSION)}</p>
<nav class="g6-footer__links" aria-label="{t(locale, 'Pied de page', 'Footer')}"><a href="{GNU6}/{q}">gnu6.live</a><a href="/{locale}/governance.html">{t(locale, 'Gouvernance', 'Governance')}</a><a href="/registry/source-catalog.json">{t(locale, 'Provenance', 'Provenance')}</a><a href="{CODE}">Code <span aria-hidden="true">↗</span></a></nav>
</div></footer>"""


def write(dist: Path, path: str, html: str) -> None:
    file = dist / path.lstrip("/")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(html, encoding="utf-8")


def index_page(dist: Path, locale: str, path: str, *, title: str, description: str, section: str, body: str,
               edition: str, footer_note: str | None = None, og: str = "docs-og.png") -> None:
    """Index layout: system bar, masthead, full-width frame. `body` contains the single H1."""
    alt = path.replace(f"/{locale}/", f"/{'en' if locale == 'fr' else 'fr'}/", 1)
    html = (head(locale, path, alt, title, description, scripts=False, og=og)
            + f'<body class="g6-site g6-site--docs"><a class="g6-skip" href="#content">{t(locale, "Aller au contenu", "Skip to content")}</a>'
            + system_bar(locale, alt) + spine_mobile(locale)
            + f'<div class="g6-spine-shell">{spine(locale, path)}<div class="g6-spine__main">'
            + f'<main id="content" class="g6-frame g6-page" tabindex="-1">{body}</main></div></div>'
            + footer(locale, edition, footer_note) + "</body></html>")
    write(dist, path, html)


_H2 = re.compile(r'<h2 id="([^"]+)">(.*?)</h2>', re.S)


def toc(locale: str, prose: str) -> tuple[str, str]:
    entries = [(i, re.sub(r"<[^>]+>", "", txt).strip()) for i, txt in _H2.findall(prose)]
    if len(entries) < 3:
        return "", ""
    items = "".join(f'<li><a href="#{escape(i, quote=True)}">{escape(txt)}</a></li>' for i, txt in entries)
    title = t(locale, "Sur cette page", "On this page")
    side = f'<nav class="g6-toc" aria-label="{title}"><p class="g6-toc__title g6-label">{title}</p><ol>{items}</ol></nav>'
    inline = f'<details class="g6-toc-inline"><summary>{title}</summary><div class="g6-toc"><ol>{items}</ol></div></details>'
    return side, inline


def reading_page(dist: Path, locale: str, path: str, *, title: str, description: str, section: str, rail: str,
                 prose: str, crumbs: str, meta: str, foot: str, study_ids: list[str], edition: str,
                 footer_note: str | None = None, og: str = "docs-og.png") -> None:
    """Reading layout: rail (#sidebar), measured prose, on-page contents. Scripts: progress, filter, drawer."""
    alt = path.replace(f"/{locale}/", f"/{'en' if locale == 'fr' else 'fr'}/", 1)
    side_toc, inline_toc = toc(locale, prose)
    menu = t(locale, "Sommaire du corpus", "Corpus contents")
    html = (head(locale, path, alt, title, description, scripts=True, og=og)
            + f'<body class="g6-site g6-site--docs" data-locale="{locale}" data-study-ids="{escape(json.dumps(study_ids), quote=True)}">'
            + f'<a class="g6-skip" href="#content">{t(locale, "Aller au contenu", "Skip to content")}</a>'
            + system_bar(locale, alt) + spine_mobile(locale)
            + f'<div class="g6-spine-shell">{spine(locale, path)}<div class="g6-spine__main">'
            + f'<div class="g6-frame g6-doc"><aside id="sidebar" class="g6-doc__nav" aria-label="{menu}">{rail}</aside>'
            + f'<main id="content" class="g6-doc__body" tabindex="-1">'
            + f'<div class="g6-doc__crumbs"><span class="g6-label">{crumbs}</span><span class="g6-doc__meta">{meta}'
            + f'<button id="toggleSidebar" class="g6-action g6-action--quiet g6-doc__menu" type="button" aria-expanded="false" aria-controls="sidebar">{menu}</button></span></div>'
            + inline_toc + f'<article class="g6-prose">{prose}</article>{foot}</main>'
            + (f'<aside class="g6-doc__toc">{side_toc}</aside>' if side_toc else '<div class="g6-doc__toc" aria-hidden="true"></div>')
            + "</div></div></div>" + footer(locale, edition, footer_note) + "</body></html>")
    write(dist, path, html)


def specimen(locale: str, identity: str) -> str:
    """Ratified cube held still in a registration frame, captioned from gnosix_DS IDENTITY.md."""
    data = {
        "gnuinlabs": ("gnu.in.labs", ">#", t(locale, "dessus", "top"), "Beret Green"),
        "gnu6-live": ("gnu6.live", ">$", t(locale, "gauche", "left"), "Royal Blue"),
    }[identity]
    rows = [(t(locale, "Identité", "Identity"), data[0]), (t(locale, "Symbole", "Symbol"), data[1]),
            (t(locale, "Face sombre", "Dark face"), data[2]), (t(locale, "Famille", "Family"), data[3])]
    caption = "".join(f"<dt>{escape(a)}</dt><dd>{escape(b)}</dd>" for a, b in rows)
    return (f'<figure class="g6-specimen"><div class="g6-specimen__frame"><img src="/gnu6/identity/{identity}-512.png" '
            f'width="512" height="512" alt="{escape(t(locale, "Cube ratifié", "Ratified cube"))} {escape(data[0])}"></div>'
            f'<dl class="g6-specimen__caption">{caption}</dl></figure>')
