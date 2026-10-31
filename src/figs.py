# Bildkatalog fuer die Rubriken: je eine Illustration im Plakat-Stil (600 x 260).
import math, random

R, RD, G, GP, CR, K, K2, K3 = '#C8102E', '#9E0C24', '#E4C06E', '#F0CF84', '#F6E9C8', '#141416', '#232326', '#2E2E32'
FONT = 'font-family="Hanken Grotesk, Arial, sans-serif" font-weight="700"'


def frame(p, inner, label):
    """Gemeinsamer Rahmen: dunkler Grund, Flutlicht-Schein, Rubrik-Etikett."""
    return (f'<svg viewBox="0 0 600 260" width="100%" height="100%" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<defs><linearGradient id="{p}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1E1E22"/><stop offset="1" stop-color="#0E0E10"/></linearGradient>'
            f'<radialGradient id="{p}l" cx=".5" cy="0" r=".95"><stop offset="0" stop-color="{G}" stop-opacity=".16"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></radialGradient>'
            f'<marker id="{p}a" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker></defs>'
            f'<rect width="600" height="260" fill="url(#{p}g)"/><rect width="600" height="260" fill="url(#{p}l)"/>{inner}'
            f'<g {FONT} font-size="11" letter-spacing="2.4"><rect x="16" y="16" width="{len(label) * 9 + 22}" height="22" rx="3" fill="{R}"/>'
            f'<text x="27" y="31" fill="#FFFFFF">{label}</text></g></svg>')


def field(p, top=118, tint='#17261C'):
    """Spielfeld in Perspektive mit Yardlinien."""
    o = f'<path d="M150 {top} L450 {top} L680 260 L-80 260 Z" fill="{tint}"/>'
    for k in range(1, 11):
        t = (k / 10) ** 1.5
        y = top + (260 - top) * t
        xl, xr = 150 - 230 * t, 450 + 230 * t
        o += f'<path d="M{xl:.0f} {y:.1f} L{xr:.0f} {y:.1f}" stroke="{CR}" stroke-opacity="{.10 + .12 * t:.2f}" stroke-width="{.8 + t:.1f}"/>'
    return o


def scheme(lbl):
    p = 'fs'
    o = ''.join(f'<path d="M{x} 40 V250" stroke="{CR}" stroke-opacity=".05"/>' for x in range(30, 600, 45))
    o += ''.join(f'<path d="M{x} 150 v6 M{x} 60 v6" stroke="{CR}" stroke-opacity=".18"/>' for x in range(20, 600, 20))
    o += f'<path d="M20 152 H580" stroke="{G}" stroke-opacity=".5" stroke-dasharray="4 6"/>'
    # Defense
    xs = [(245, 136), (285, 136), (325, 136), (362, 136), (225, 100), (300, 96), (375, 100), (90, 112), (520, 112), (215, 56), (395, 56)]
    o += ''.join(f'<path d="M{x - 7} {y - 7} l14 14 M{x + 7} {y - 7} l-14 14" stroke="{R}" stroke-width="3" stroke-linecap="round"/>' for x, y in xs)
    # Routen
    st = f'fill="none" stroke="{G}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#{p}a)"'
    o += f'<path d="M85 166 V96 L150 50" {st}/><path d="M470 166 Q462 142 400 140 L270 132" {st}/><path d="M410 166 L414 104 L478 62" {st}/>'
    o += f'<path d="M300 210 Q350 226 430 214 L470 196" fill="none" stroke="{CR}" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round" marker-end="url(#{p}a)"/>'
    o += f'<path d="M300 238 Q250 236 200 212" fill="none" stroke="{R}" stroke-width="3.5" stroke-linecap="round" marker-end="url(#{p}a)"/>'
    o += f'<path d="M540 166 Q520 182 490 174" fill="none" stroke="{CR}" stroke-opacity=".6" stroke-width="2" stroke-dasharray="5 5"/>'
    # Offense
    os_ = [(230, 166), (265, 166), (300, 166), (335, 166), (370, 166), (410, 166), (85, 166), (470, 166), (300, 206), (300, 238)]
    o += ''.join(f'<circle cx="{x}" cy="{y}" r="10" fill="{K}" stroke="{CR}" stroke-width="2.6"/>' for x, y in os_)
    o += f'<circle cx="300" cy="166" r="10" fill="{CR}"/>'
    o += f'<text x="584" y="244" {FONT} font-size="11" letter-spacing="2" fill="{G}" text-anchor="end" opacity=".85">OUTSIDE ZONE  |  BOOT</text>'
    return frame(p, o, lbl)


def spieler(lbl):
    p = 'fp'
    o = field(p, 112)
    qx, qy = 190, 250
    rnd = random.Random(7)
    pts = [(rnd.uniform(40, 340), rnd.uniform(122, 228)) for _ in range(26)]
    for k, (x, y) in enumerate(pts):
        ok = k % 4 != 3
        if k % 3 == 0:
            o += f'<path d="M{qx} {qy} Q{(qx + x) / 2:.0f} {min(y, qy) - 70:.0f} {x:.0f} {y:.0f}" fill="none" stroke="{G if ok else R}" stroke-opacity=".45" stroke-width="1.4"/>'
        o += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{G}"/>' if ok else f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="none" stroke="{R}" stroke-width="2.2"/>')
    o += f'<circle cx="{qx}" cy="{qy - 6}" r="8" fill="{CR}"/>'
    # Bestenliste
    o += f'<rect x="372" y="44" width="212" height="200" rx="8" fill="{K}" stroke="{K3}"/>'
    o += f'<text x="388" y="68" {FONT} font-size="11" letter-spacing="2" fill="{CR}" opacity=".7">CAREER LEADERS</text>'
    vals = [7.8, 7.6, 7.4, 7.2, 7.0, 6.8]
    for k, v in enumerate(vals):
        y = 84 + k * 26; hi = k == 2
        w = (v - 5.5) / 2.4 * 120
        o += f'<text x="388" y="{y + 12}" {FONT} font-size="12" fill="{R if hi else CR}" opacity="{1 if hi else .55}">{k + 1}</text>'
        o += f'<rect x="408" y="{y + 2}" width="{w:.0f}" height="12" rx="2" fill="{G if hi else K3}"/>'
        o += f'<text x="572" y="{y + 12}" {FONT} font-size="12" fill="{G if hi else CR}" text-anchor="end" opacity="{1 if hi else .6}">{v:.1f}</text>'
    return frame(p, o, lbl)


def team(lbl):
    p = 'ft'
    rnd = random.Random(3)
    vals = sorted([rnd.uniform(-.18, .22) for _ in range(32)], reverse=True)
    x0, w, base, sc = 34, 15.6, 168, 360
    o = f'<path d="M24 {base} H580" stroke="{CR}" stroke-opacity=".35"/>'
    for y in (88, 128, 208):
        o += f'<path d="M24 {y} H580" stroke="{CR}" stroke-opacity=".07"/>'
    for k, v in enumerate(vals):
        h = v * sc; hi = k == 6
        y = base - h if h > 0 else base
        o += f'<rect x="{x0 + k * 17.2:.1f}" y="{y:.1f}" width="{w}" height="{abs(h):.1f}" rx="2" fill="{R if hi else (K3 if v < 0 else "#4A4A52")}"/>'
        if hi:
            cx = x0 + k * 17.2 + w / 2
            o += f'<circle cx="{cx:.1f}" cy="{y - 14:.1f}" r="5" fill="{G}"/><path d="M{cx:.1f} {y - 20:.1f} V62" stroke="{G}" stroke-width="1.5"/>'
            o += f'<text x="{cx + 10:.1f}" y="66" {FONT} font-size="12" letter-spacing="1.5" fill="{G}">RANG 7  |  +0,14</text>'
    o += f'<path d="M24 158 H580" stroke="{G}" stroke-opacity=".6" stroke-dasharray="3 5"/>'
    o += f'<text x="584" y="244" {FONT} font-size="11" letter-spacing="2" fill="{CR}" text-anchor="end" opacity=".6">EPA / PLAY  |  32 TEAMS</text>'
    return frame(p, o, lbl)


def draft(lbl):
    p = 'fd'
    o = f'<rect x="24" y="50" width="552" height="196" rx="6" fill="#1A1A1D" stroke="{K3}"/>'
    pos = ['EDGE', 'WR', 'OT', 'CB', 'QB', 'LB', 'S', 'TE', 'DT', 'RB', 'IOL', 'K']
    for r in range(3):
        for c in range(4):
            k = r * 4 + c; x = 40 + c * 134; y = 62 + r * 60
            hi = k == 5
            o += f'<g transform="rotate({(k % 3 - 1) * .8} {x + 60} {y + 25})"><rect x="{x}" y="{y}" width="120" height="50" rx="3" fill="{CR}" stroke="{G if hi else "none"}" stroke-width="3"/>'
            o += f'<rect x="{x}" y="{y}" width="120" height="9" rx="2" fill="{R if hi else RD}"/>'
            o += f'<text x="{x + 8}" y="{y + 28}" {FONT} font-size="12" letter-spacing="1" fill="{K}">{pos[k]}</text>'
            o += f'<rect x="{x + 8}" y="{y + 36}" width="{60 + (k * 13) % 40}" height="5" rx="2" fill="#8E8572"/>'
            o += f'<text x="{x + 112}" y="{y + 28}" {FONT} font-size="11" fill="#8E8572" text-anchor="end">R{r + 1}</text>'
            o += f'<circle cx="{x + 60}" cy="{y + 2}" r="4" fill="{G if hi else "#55555C"}"/></g>'
    return frame(p, o, lbl)


def vorschau(lbl):
    p = 'fv'
    o = field(p, 150, '#141F17')
    o += f'<path d="M0 40 L330 40 L270 196 L0 196 Z" fill="{R}"/><path d="M330 40 L600 40 L600 196 L270 196 Z" fill="{K2}"/>'
    o += f'<path d="M0 40 L330 40 L318 72 L0 72 Z" fill="#FFFFFF" opacity=".06"/>'
    o += f'<circle cx="300" cy="118" r="34" fill="{K}" stroke="{G}" stroke-width="3"/><text x="300" y="127" {FONT} font-size="24" fill="{G}" text-anchor="middle">VS</text>'
    for k, (a, b) in enumerate([(.72, .55), (.6, .66), (.8, .5)]):
        y = 92 + k * 26
        o += f'<rect x="{230 - a * 180:.0f}" y="{y}" width="{a * 180:.0f}" height="10" rx="2" fill="{CR}" opacity=".9"/>'
        o += f'<rect x="370" y="{y}" width="{b * 180:.0f}" height="10" rx="2" fill="#6A6A72"/>'
    o += f'<text x="584" y="31" {FONT} font-size="11" letter-spacing="2.4" fill="{G}" text-anchor="end">WEEK 9</text>'
    o += f'<rect x="232" y="212" width="136" height="34" rx="4" fill="{K}" stroke="{K3}"/><text x="300" y="235" {FONT} font-size="16" letter-spacing="3" fill="{G}" text-anchor="middle">22:25</text>'
    return frame(p, o, lbl)


def nachbericht(lbl):
    p = 'fn'
    o = f'<rect x="40" y="52" width="290" height="120" rx="6" fill="{K}" stroke="{K3}"/>'
    o += f'<text x="58" y="76" {FONT} font-size="11" letter-spacing="3" fill="{G}">FINAL</text>'
    cols = ['1', '2', '3', '4', 'T']
    for c, t in enumerate(cols):
        o += f'<text x="{150 + c * 36}" y="76" {FONT} font-size="11" fill="{CR}" opacity=".5" text-anchor="middle">{t}</text>'
    rows = [('SF', [7, 10, 0, 10, 27], R), ('OPP', [3, 7, 7, 3, 20], '#55555C')]
    for r, (n, sc, col) in enumerate(rows):
        y = 104 + r * 40
        o += f'<rect x="58" y="{y - 18}" width="58" height="26" rx="3" fill="{col}"/><text x="87" y="{y}" {FONT} font-size="14" letter-spacing="1" fill="#FFFFFF" text-anchor="middle">{n}</text>'
        for c, v in enumerate(sc):
            last = c == 4
            o += f'<text x="{150 + c * 36}" y="{y}" {FONT} font-size="{20 if last else 16}" fill="{(G if r == 0 else CR) if last else CR}" opacity="{1 if last else .8}" text-anchor="middle">{v}</text>'
    # Siegwahrscheinlichkeit
    pts = [.5, .46, .58, .64, .7, .62, .55, .6, .52, .48, .57, .66, .72, .8, .76, .86, .9, .94, .97, 1]
    xs = [350 + k * 11.5 for k in range(len(pts))]
    ys = [222 - v * 160 for v in pts]
    d = ' '.join(f'{"M" if k == 0 else "L"}{x:.1f} {y:.1f}' for k, (x, y) in enumerate(zip(xs, ys)))
    o += f'<path d="M350 142 H580" stroke="{CR}" stroke-opacity=".25" stroke-dasharray="3 5"/>'
    o += f'<path d="{d} L{xs[-1]:.1f} 222 L350 222 Z" fill="{R}" opacity=".22"/><path d="{d}" fill="none" stroke="{G}" stroke-width="3" stroke-linejoin="round"/>'
    o += f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="5" fill="{G}"/>'
    o += f'<text x="350" y="244" {FONT} font-size="11" letter-spacing="2" fill="{CR}" opacity=".6">WIN PROBABILITY</text>'
    return frame(p, o, lbl)


BUILD = {'scheme': scheme, 'spieler': spieler, 'team': team, 'draft': draft, 'vorschau': vorschau, 'nachbericht': nachbericht}


PFX = {'scheme': 'fs', 'spieler': 'fp', 'team': 'ft', 'draft': 'fd', 'vorschau': 'fv', 'nachbericht': 'fn'}


CROPS = {'spieler': ['20 110 300 197', '372 44 212 140'], 'team': ['24 40 340 224', '250 60 330 217'],
         'draft': ['30 55 290 190', '296 55 290 190'], 'scheme': ['150 40 300 197', '40 40 300 197'],
         'vorschau': ['150 40 300 197', '0 40 300 197'], 'nachbericht': ['340 60 250 165', '40 50 300 197']}


def fig(rub, label, lang='de', uid='', crop=None):
    """Illustration einer Rubrik; mit crop ein Ausschnitt ohne Etikett fuer kleine Vorschaubilder."""
    s = BUILD[rub](label.upper())
    if crop is not None:
        s = s.replace('viewBox="0 0 600 260"', f'viewBox="{CROPS[rub][crop % len(CROPS[rub])]}"', 1)
        s = s[:s.rindex('<g font-family')] + '</svg>'
    if lang == 'en':
        s = s.replace('RANG 7  |  +0,14', 'RANK 7  |  +0.14')
    if uid:
        p = PFX[rub]
        s = s.replace(f'id="{p}', f'id="{p}{uid}').replace(f'#{p}', f'#{p}{uid}')
    return s
