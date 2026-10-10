"""Generate the three topology diagrams.

Colours are gnosix_DS tokens (dark substrate) as presentation attributes so the standalone
SVG files render on their own. Every element also carries a g6-dia-* class: when the
topology page inlines a diagram, gnu6-design CSS re-maps those classes to the active
light/dark roles. Text is Space Grotesk (gnosix_DS TYP-001) with system fallbacks.
"""
from pathlib import Path
from html import escape

P = Path(__file__).parent
FONT = "Space Grotesk, ui-sans-serif, system-ui, sans-serif"
INK = {"bg": "#111418", "node": "#1A1D21", "text": "#F7F3ED", "sub": "#A1A6AD", "rule": "#A1A6AD"}
KIND = {"main": "#8DA982", "alt": "#87A0F4", "gate": "#FF8E40", "muted": "#A1A6AD"}


def svg(name, title, nodes, arrows, notes, width=1160, height=306):
    width = max(width, max(x + w for x, y, w, h, *_ in nodes) + 30)
    t, d, a = f"{name}-title", f"{name}-desc", f"{name}-arrow"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{t} {d}" class="g6-dia">'
        f'<title id="{t}">{escape(title)}</title><desc id="{d}">{escape(notes)}</desc>',
        f'<defs><marker id="{a}" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path class="g6-dia-arrowhead" d="M0 0 L7 3.5 L0 7" fill="none" stroke="{INK["rule"]}" stroke-width="1.3"/></marker></defs>',
        f'<rect class="g6-dia-bg" width="100%" height="100%" fill="{INK["bg"]}" rx="10"/>'
        f'<text class="g6-dia-kicker" x="30" y="41" fill="{INK["sub"]}" font-family="{FONT}" font-weight="600" font-size="13" letter-spacing="2">{escape(title.upper())}</text>',
    ]
    for (x1, y1, x2, y2) in arrows:
        out.append(f'<line class="g6-dia-edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK["rule"]}" stroke-width="1.6" marker-end="url(#{a})"/>')
    for x, y, w, h, label, sub, kind in nodes:
        out.append(f'<rect class="g6-dia-node g6-dia-{kind}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{INK["node"]}" stroke="{KIND[kind]}" stroke-width="1.4" rx="6"/>')
        out.append(f'<rect class="g6-dia-tab g6-dia-{kind}" x="{x}" y="{y}" width="4" height="{h}" fill="{KIND[kind]}" rx="2"/>')
        for i, s in enumerate(label.split("|")):
            out.append(f'<text class="g6-dia-label" x="{x + w / 2}" y="{y + 35 + i * 21}" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="16" fill="{INK["text"]}">{escape(s)}</text>')
        out.append(f'<text class="g6-dia-sub" x="{x + w / 2}" y="{y + h - 18}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{INK["sub"]}">{escape(sub)}</text>')
    out.append(
        f'<text class="g6-dia-sub" x="30" y="{height - 15}" fill="{INK["sub"]}" font-family="{FONT}" font-size="11">'
        f"gnu.in.labs / Engineering Corpus · diagram v0.2 · gnu6-design 1.0.0 · editable source: docs/diagrams/{name}.mmd</text></svg>"
    )
    (P / f"{name}.svg").write_text("\n".join(out), encoding="utf-8")


svg('lifecycle','01 / Engineering lifecycle',[(30+i*166,96,146,122,a,b,c) for i,(a,b,c) in enumerate([
('Mandate','scope','main'),('Contract','invariants','alt'),('Slice','isolated work','main'),('Verify','local gates','main'),('Evidence','provenance','alt'),('Review','decision','gate'),('Release','separate grant','gate')])],[(176+i*166,157,30+(i+1)*166-10,157) for i in range(6)],'intent, contract, local implementation, verification, evidence, approval and separate release')
svg('authority','02 / Authority boundaries',[(30,94,230,114,'Operator','mandate owner','main'),(340,94,230,114,'Scoped grant','resource + ops + expiry','alt'),(650,94,230,114,'Agent','no ambient authority','main'),(900,94,230,114,'Review gate','independent decision','gate')],[(260,151,328,151),(570,151,638,151),(880,151,888,151)],'operator issues scoped grant; agent proposes; independent review gates any mutation')
svg('knowledge','03 / Source to public knowledge',[(30+i*224,98,200,122,a,b,c) for i,(a,b,c) in enumerate([
('Versioned|code','fixed commit','main'),('Deterministic|extraction','symbols + tests','alt'),('Local LLM|proposal','non-authoritative','muted'),('Validation','compile + provenance','gate'),('Public corpus','reviewed only','main')])],[(230+i*224,160,30+(i+1)*224-10,160) for i in range(4)],'versioned sources and verified extraction precede local LLM drafting and human publication review')
print('SVG generated',len(list(P.glob('*.svg'))))
