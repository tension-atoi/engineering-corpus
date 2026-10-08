from pathlib import Path
from html import escape
P=Path(__file__).parent

def svg(name,title,nodes,arrows,notes,width=1160,height=306):
    out=[f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(notes)}</desc>
<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7" fill="none" stroke="#aaf184" stroke-width="1.3"/></marker></defs>
<rect width="100%" height="100%" fill="#101714" rx="10"/><text x="30" y="41" fill="#b3f47c" font-family="monospace" font-weight="600" font-size="13" letter-spacing="2">{escape(title.upper())}</text>''']
    for (x1,y1,x2,y2) in arrows:
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#aaf184" stroke-width="1.7" marker-end="url(#arrow)"/>')
    for x,y,w,h,label,sub,kind in nodes:
        accent={'main':'#aef587','alt':'#89acff','gate':'#ffc18b','muted':'#7eaa8b'}[kind]
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1a231d" stroke="{accent}" stroke-width="1.2" rx="8"/>')
        for i,s in enumerate(label.split('|')):
            out.append(f'<text x="{x+w/2}" y="{y+35+i*21}" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="16" fill="#f0f7ed">{escape(s)}</text>')
        out.append(f'<text x="{x+w/2}" y="{y+h-18}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#a9bcae">{escape(sub)}</text>')
    out.append(f'<text x="30" y="{height-15}" fill="#789383" font-family="monospace" font-size="11">gnu.in.labs / Engineering Corpus · diagram v0.1 · normative source: docs/diagrams/{name}.mmd</text></svg>')
    (P/f'{name}.svg').write_text('\n'.join(out),encoding='utf-8')
svg('lifecycle','01 / Engineering lifecycle',[(30+i*166,96,146,122,a,b,c) for i,(a,b,c) in enumerate([
('Mandate','scope','main'),('Contract','invariants','alt'),('Slice','isolated work','main'),('Verify','local gates','main'),('Evidence','provenance','alt'),('Review','decision','gate'),('Release','separate grant','gate')])],[(176+i*166,157,30+(i+1)*166-10,157) for i in range(6)],'intent, contract, local implementation, verification, evidence, approval and separate release')
svg('authority','02 / Authority boundaries',[(30,94,230,114,'Operator','mandate owner','main'),(340,94,230,114,'Scoped grant','resource + ops + expiry','alt'),(650,94,230,114,'Agent','no ambient authority','main'),(900,94,230,114,'Review gate','independent decision','gate')],[(260,151,328,151),(570,151,638,151),(880,151,888,151)],'operator issues scoped grant; agent proposes; independent review gates any mutation')
svg('knowledge','03 / Source to public knowledge',[(30+i*224,98,200,122,a,b,c) for i,(a,b,c) in enumerate([
('Versioned|code','fixed commit','main'),('Deterministic|extraction','symbols + tests','alt'),('Local LLM|proposal','non-authoritative','muted'),('Validation','compile + provenance','gate'),('Public corpus','reviewed only','main')])],[(230+i*224,160,30+(i+1)*224-10,160) for i in range(4)],'versioned sources and verified extraction precede local LLM drafting and human publication review')
print('SVG generated',len(list(P.glob('*.svg'))))
