#!/usr/bin/env python3
"""Erzeugt das Provisorium von Niners Faithful Europe als statische Seiten (DE und EN)."""
import json, os, shutil, sys
from figs import fig
from html import escape as E

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'site')
# Pfad, unter dem die Seite liegt: auf GitHub Pages /niners-faithful-europe, mit eigener Domain leer
P = os.environ.get('NFE_BASE', '').rstrip('/')

PAGES = {'kickoff': '', 'playbook': 'playbook/', 'stats': 'stat-sheet/', 'lineup': 'line-up/', 'roster': 'roster/', 'plan': 'game-plan/', 'article': 'playbook/career-any-a/', 'inbox': 'inbox/'}
def url(lang, key): return f'{P}/{lang}/{PAGES[key]}'

T = {
 'de': dict(nav=[('kickoff', 'Kickoff'), ('playbook', 'Playbook'), ('stats', 'Stat Sheet'), ('lineup', 'Line-up'), ('roster', 'Roster'), ('plan', 'Game Plan')],
            navlabel='Hauptnavigation', langlabel='Sprache', skip='Zum Inhalt springen',
            proto='Provisorium: Diese Seite ist ein Entwurf und noch nicht offiziell gestartet.',
            footer='Unabhängiges Fanprojekt, keine Verbindung zur NFL oder zu den San Francisco 49ers.', footer2='Provisorium'),
 'en': dict(nav=[('kickoff', 'Kickoff'), ('playbook', 'Playbook'), ('stats', 'Stat Sheet'), ('lineup', 'Line-up'), ('roster', 'Roster'), ('plan', 'Game Plan')],
            navlabel='Main navigation', langlabel='Language', skip='Skip to content',
            proto='Preview: this site is a draft and has not officially launched yet.',
            footer='Independent fan project, not affiliated with the NFL or the San Francisco 49ers.', footer2='Preview'),
}

NEG = 'https://theninerempiregermany.de/'
DATA = os.path.join(ROOT, 'data', 'articles.json')
MON = (['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sept.', 'Okt.', 'Nov.', 'Dez.'],
       ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
def fdate(iso):
    y, m, d = (int(v) for v in iso.split('-'))
    return (f'{d}. {MON[0][m - 1]} {y}', f'{MON[1][m - 1]} {d}, {y}')
def load(status):
    """Beiträge aus data/articles.json, neueste zuerst, in der Form, die die Seiten erwarten."""
    out = []
    for x in json.load(open(DATA, encoding='utf-8')):
        if x.get('status') != status: continue
        t, z = x['title'], x.get('teaser') or {}
        out.append(dict(x, date=fdate(x['date']), iso=x['date'], title=(t['de'], t.get('en') or t['de']),
                        teaser=(z.get('de', ''), z.get('en') or z.get('de', '')), de=x['link']['de'], en=x['link'].get('en')))
    return sorted(out, key=lambda a: a['iso'], reverse=True)
ART = load('live')
DRAFTS = load('entwurf')
ART_BY = {a['id']: a for a in ART}
FMT = {'fantext': ('Fantext', 'Fan piece'), 'analyse': ('Analyse', 'Analysis'), 'grafik': ('Grafik', 'Graphic')}
RUB = [('vorschau', 'Spielvorschau', 'Game previews'), ('nachbericht', 'Spielnachbericht', 'Game reviews'), ('team', 'Team-Stats', 'Team stats'),
       ('spieler', 'Spieler-Stats', 'Player stats'), ('draft', 'Draft und Kader', 'Draft and roster'), ('scheme', 'Scheme und Tape', 'Scheme and tape')]
RUBN = {k: (d, e) for k, d, e in RUB}
I = lambda lang: 0 if lang == 'de' else 1

def art_link(a, lang):
    """Link eines Beitrags: DE immer zum Original, EN zur englischen Fassung, sonst zum deutschen Original."""
    if lang == 'de': return a['de'], True
    if a['en'] == 'article': return url('en', 'article'), False
    if a['en']: return a['en'], True
    return a['de'], True

def ext(href): return ' rel="noopener" target="_blank"' if href.startswith('http') else ''

ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
BACK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>'
PLAY = ('<svg viewBox="0 0 600 260" width="100%" height="100%" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><line x1="0" y1="190" x2="600" y2="190" stroke="#2E2E2E"/>'
        '<g fill="none" stroke="#F5F3EE" stroke-width="2.5"><circle cx="210" cy="190" r="10"/><circle cx="250" cy="190" r="10"/><circle cx="290" cy="190" r="10"/><circle cx="330" cy="190" r="10"/><circle cx="370" cy="190" r="10"/><circle cx="290" cy="232" r="10"/></g>'
        '<g fill="none" stroke="#E4C06E" stroke-width="3" stroke-linecap="round"><path d="M290 222 Q400 222 450 150 Q470 110 500 80"/><path d="M488 84 L500 80 L498 93"/></g>'
        '<g fill="none" stroke="#C8102E" stroke-width="3" stroke-linecap="round"><path d="M210 180 Q150 140 120 70"/><path d="M114 84 L120 70 L131 80"/></g></svg>')

def page(lang, key, title, desc, body):
    t = T[lang]; other = 'en' if lang == 'de' else 'de'
    nav = ''.join(f'<a href="{url(lang, k)}"' + (' aria-current="page"' if (k == key or (key == 'article' and k == 'playbook')) else '') + f'>{E(lbl)}</a>' for k, lbl in t['nav'])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | Niners Faithful Europe</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="alternate" hreflang="{lang}" href="{url(lang, key)}">
<link rel="alternate" hreflang="{other}" href="{url(other, key)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Young+Serif&family=Hanken+Grotesk:wght@300..700&display=swap">
<link rel="stylesheet" href="{P}/assets/site.css">
<script src="{P}/assets/site.js" defer></script>
</head>
<body{' class="wm"' if key != 'kickoff' else ''}>
<a class="skip" href="#main">{t['skip']}</a>
<div class="proto">{t['proto']}</div>
<header class="site-head"><div class="wrap">
<a class="brand" href="{url(lang, 'kickoff')}">Niners Faithful <span>Europe</span></a>
<nav class="nav" aria-label="{t['navlabel']}">{nav}</nav>
<div class="lang" role="group" aria-label="{t['langlabel']}"><a href="{url('de', key)}" lang="de"{' aria-current="true"' if lang == 'de' else ''}>DE</a><a href="{url('en', key)}" lang="en"{' aria-current="true"' if lang == 'en' else ''}>EN</a></div>
</div></header>
{body}
<footer class="site-foot"><div class="wrap"><span>{t['footer']}</span><span>{t['footer2']}</span></div></footer>
</body>
</html>
'''

def meta(a, lang):
    return f'<span class="meta"><b>{FMT[a["fmt"]][I(lang)]}</b>  |  {E(a["author"])}, {E(a["src"])}  |  {a["date"][I(lang)]}</span>'

# ---------------- Kickoff ----------------
def kickoff(lang):
    i = I(lang)
    svg = open(os.path.join(HERE, f'poster_{lang}.svg.txt'), encoding='utf-8').read()
    # Aufmacher: der neueste Beitrag, auf Englisch der neueste mit englischer Fassung
    lead = ART[0] if lang == 'de' else next((a for a in ART if a['en']), ART[0])
    side = [a for a in ART if a is not lead][:3]
    href, isext = art_link(lead, lang)
    seen = {lead['rub']: 0}
    def crop(r):
        seen[r] = seen.get(r, -1) + 1
        return seen[r]
    sides = ''.join(f'<a class="story side spot" href="{art_link(a, lang)[0]}"{ext(art_link(a, lang)[0])}><span class="side-fig">{fig(a["rub"], RUBN[a["rub"]][i], lang, f"s{n}", crop(a["rub"]))}</span><span class="side-t"><h3>{E(a["title"][i])}</h3>{meta(a, lang)}</span></a>' for n, a in enumerate(side))
    counts = {k: sum(1 for a in ART if a['rub'] == k) for k, _, _ in RUB}
    rubs = ''.join(f'<a class="idx spot" href="{url(lang, "playbook")}?rub={k}"><span>{E((d, e)[i])}</span><span class="n">{counts[k]}</span></a>' for k, d, e in RUB)
    people = [('Chris Pracher', 'Niner Empire Germany, cp7'), ('Lukas', 'Niner Empire Germany'), (('Dein Name hier', 'Your name here')[i], ('Wien, Zürich, Hamburg ...', 'Vienna, Zurich, Hamburg ...')[i])]
    lineup = ''.join(f'<a class="idx spot" href="{url(lang, "lineup")}"><span>{E(n)}</span><span class="w">{E(w)}</span></a>' for n, w in people)
    L = {
      'de': dict(h1='Von Europa <span>an die Bay.</span>', sub='Analysen, Fantexte und Statistik-Grafiken über die 49ers. Geschrieben in Deutschland, Österreich und der Schweiz, auf Englisch für die Faithful in aller Welt.',
                 b1='Ins Playbook', b2='Der Game Plan', alt='Plakat: links Hamburg, Köln, München und Wien vor den Alpen, in der Mitte die Golden Gate Bridge vor der untergehenden Sonne, rechts San Francisco und das Stadion mit Leuchtband. Ein Segelboot fährt von Europa zur Bay.',
                 latest='Neu im Playbook', all='Zum Playbook', rubs='Rubriken', lu='Das Line-up', cta='Du schreibst über Football auf Deutsch?', ctab='Zum Tryout'),
      'en': dict(h1='From Europe <span>to the Bay.</span>', sub='Analysis, fan writing and stat graphics on the 49ers. Written in Germany, Austria and Switzerland, translated for the Faithful around the world.',
                 b1='Open the playbook', b2='The game plan', alt='Poster: on the left Hamburg, Cologne, Munich and Vienna in front of the Alps, in the middle the Golden Gate Bridge against the setting sun, on the right San Francisco and the stadium with a ticker. A sailboat travels from Europe to the Bay.',
                 latest='New in the playbook', all='Open the playbook', rubs='Sections', lu='The line-up', cta='Know a German-speaking writer we should feature?', ctab='Get in touch'),
    }[lang]
    body = f'''<main id="main">
<section class="wrap hero"><h1>{L['h1']}</h1><p>{L['sub']}</p><div class="actions" style="justify-content:center"><a class="btn btn-primary" href="{url(lang, 'playbook')}">{L['b1']}</a><a class="btn btn-ghost" href="{url(lang, 'plan')}">{L['b2']}</a></div></section>
<section class="poster">
<svg viewBox="0 110 1600 790" preserveAspectRatio="xMidYMax slice" role="img" aria-label="{E(L['alt'])}">{svg}</svg>
<div class="grain" aria-hidden="true"></div>
</section>
<section class="wrap" style="padding-top:40px" aria-labelledby="neu">
<div class="section-head"><h2 id="neu">{L['latest']}</h2><a href="{url(lang, 'playbook')}">{L['all']}</a></div>
<div class="news">
<a class="story lead spot" href="{href}"{ext(href)}><div class="figure-dark">{fig(lead["rub"], RUBN[lead["rub"]][i], lang)}</div><h2>{E(lead['title'][i])}</h2><p>{E(lead['teaser'][i])}</p>{meta(lead, lang)}</a>
<div class="aside">{sides}</div>
</div></section>
<section class="wrap idx-wrap"><div><h2>{L['rubs']}</h2>{rubs}</div><div><h2>{L['lu']}</h2>{lineup}</div></section>
<section class="cta-band"><div class="wrap"><h2>{L['cta']}</h2><a class="btn btn-primary" href="{url(lang, 'plan')}#tryout">{L['ctab']}</a></div></section>
</main>'''
    return page(lang, 'kickoff', ('Von Europa an die Bay', 'From Europe to the Bay')[i], L['sub'], body)

# ---------------- Playbook ----------------
def playbook(lang):
    i = I(lang)
    L = {
      'de': dict(title='Playbook', intro='Alle Spielzüge an einem Ort: Fantexte, Analysen und Grafiken. Filtere nach Format, Rubrik oder Autor, oder suche nach einem Stichwort. Die Beiträge führen zum Original beim Autor.',
                 fmt='Format', all='Alle', rub='Rubrik', allrub='Alle Rubriken', aut='Autor', allaut='Alle Autoren', q='Suche', qph='Titel oder Stichwort', one='Beitrag', many='Beiträge',
                 emptyt='Keine Treffer', emptyp='Für diese Filter gibt es noch keine Beiträge.', reset='Filter zurücksetzen', de_only=''),
      'en': dict(title='Playbook', intro='Every play in one place: fan pieces, analysis and graphics. Filter by format, section or author, or search for a keyword. English versions are added step by step; until then, items link to the German original.',
                 fmt='Format', all='All', rub='Section', allrub='All sections', aut='Author', allaut='All authors', q='Search', qph='Title or keyword', one='article', many='articles',
                 emptyt='No results', emptyp='There are no articles for these filters yet.', reset='Reset filters', de_only='German original'),
    }[lang]
    btns = f'<button type="button" data-fmt="all" aria-pressed="true">{L["all"]}</button>' + ''.join(f'<button type="button" data-fmt="{k}" aria-pressed="false">{v[i]}</button>' for k, v in FMT.items())
    autopts = ''.join(f'<option value="{k}">{E(n)}</option>' for k, n in sorted({(a['aut'], a['author']) for a in ART}, key=lambda x: x[1]))
    rubopts = f'<option value="all">{L["allrub"]}</option>' + ''.join(f'<option value="{k}">{E((d, e)[i])}</option>' for k, d, e in RUB)
    rows = ''
    for a in ART:
        href, isext = art_link(a, lang)
        hasen = bool(a['en'])
        langs = '<span class="langs"><span' + (' class="on"' if lang == 'de' else '') + '>DE</span>' + ('<span' + (' class="on"' if lang == 'en' else '') + '>EN</span>' if hasen else '') + '</span>'
        if lang == 'en' and not hasen: langs = f'<span class="langs"><span>{L["de_only"]}</span></span>'
        text = ' '.join([a['title'][0], a['title'][1], a['author'], a['src'], RUBN[a['rub']][i]]).lower()
        thumb = '<span class="thumb" aria-hidden="true"><i style="width:94%"></i><i style="width:82%"></i><i style="width:74%"></i><i style="width:64%"></i></span>' if a['fmt'] == 'grafik' else ''
        rows += (f'<a class="row spot{" g" if thumb else ""}" data-row data-fmt="{a["fmt"]}" data-rub="{a["rub"]}" data-aut="{a["aut"]}" data-text="{E(text)}" href="{href}"{ext(href)}>{thumb}'
                 f'<span class="t"><h2>{E(a["title"][i])}</h2><span class="tz">{E(a["teaser"][i])}</span><span class="meta"><b>{FMT[a["fmt"]][i]}</b>  |  {E(RUBN[a["rub"]][i])}  |  {E(a["author"])}, {E(a["src"])}  |  {a["date"][i]}</span></span>{langs}</a>')
    body = f'''<main id="main" class="wrap page" data-playbook>
<h1 class="page-title">{L['title']}</h1><p class="lead-text">{L['intro']}</p>
<div class="filters"><span id="fmt" class="meta" style="font-weight:600">{L['fmt']}</span><div class="seg" role="group" aria-labelledby="fmt">{btns}</div></div>
<div class="fields">
<div class="field"><label for="f-rub">{L['rub']}</label><select id="f-rub">{rubopts}</select></div>
<div class="field"><label for="f-aut">{L['aut']}</label><select id="f-aut"><option value="all">{L['allaut']}</option>{autopts}</select></div>
<div class="field"><label for="f-q">{L['q']}</label><input id="f-q" type="search" placeholder="{L['qph']}" autocomplete="off"></div>
</div>
<p class="count" aria-live="polite" data-count data-one="{L['one']}" data-many="{L['many']}">{len(ART)} {L['many']}</p>
<div class="rows">{rows}</div>
<div class="empty" data-empty hidden><h2 style="font-size:28px">{L['emptyt']}</h2><p class="meta">{L['emptyp']}</p><button type="button" class="btn btn-ghost" data-reset style="margin-top:8px">{L['reset']}</button></div>
</main>'''
    return page(lang, 'playbook', L['title'], L['intro'], body)

# ---------------- Artikel Career ANY/A ----------------
def article(lang):
    a = ART_BY['career-any-a']; i = I(lang)
    if lang == 'en':
        inner = f'''<p class="pill-note">English version by the author</p>
<div class="body">
<p>Brock Purdy leads the all-time list in Adjusted Net Yards per Pass Attempt with 8.00, and his margin of 0.61 over Patrick Mahomes is almost as large as the entire gap between Mahomes in second place and Russell Wilson in 16th (0.64). In early October Purdy even stood at 8.04, before two games at his normal level of around 7.0 pulled him back down a little.</p>
<p>Anyone who hastily concludes from this that the last pick of the 2022 draft is the most efficient quarterback in NFL history should first take a look at what this number actually captures and, just as importantly, what it deliberately leaves out.</p>
</div>
<aside class="keybox" style="margin:44px 0 8px"><h2>KEY TAKEAWAY</h2><p>Purdy’s lead is real across several metrics, but his sample is still short: he only passed the 1,500-attempt minimum in October 2026.</p></aside>
<div class="body"><p>Two details are also important for understanding the table. First, Pro Football Reference requires at least 1,500 pass attempts for the career list, a mark Purdy only passed this October: after six games of the 2026 season he stands at 1,524 attempts and 86 sacks, that is, 1,610 dropbacks. Second, sack data is only available from the early 1960s on, which is why Otto Graham or Sammy Baugh cannot appear at all.</p></div>
<div class="actions" style="margin-top:32px"><a class="btn btn-primary" href="https://cp7.beer/projects/career-any-a-en/" rel="noopener" target="_blank">Read the full dossier</a></div>'''
        origin = ('Original in German', 'This article first appeared in German with Chris Pracher on cp7.', 'Read the German original', a['de'])
        basis = ('Data basis and method', 'Career ANY/A from Pro Football Reference, minimum 1,500 pass attempts, data as of October 20, 2026. Passer rating and ESPN Total QBR as cross-checks.')
        back = 'Back to the playbook'
    else:
        inner = f'''<p class="teaser-big">{E(a['teaser'][0])}</p>
<aside class="keybox" style="margin:40px 0 8px"><h2>KERNAUSSAGE</h2><p>Purdys Vorsprung zeigt sich in mehreren Kennzahlen, die Stichprobe ist aber noch kurz: Die Mindestmarke von 1.500 Passversuchen hat er erst im Oktober 2026 überschritten.</p></aside>'''
        origin = ('Das Original liegt beim Autor', 'Den vollständigen Text liest du bei Chris Pracher auf cp7. Die englische Fassung gibt es hier.', 'Original auf cp7 lesen', a['de'])
        basis = ('Datenbasis und Methodik', 'Karriere-ANY/A nach Pro Football Reference, mindestens 1.500 Passversuche, Datenstand 20. Oktober 2026. Ergänzend Passer Rating und ESPN Total QBR.')
        back = 'Zurück zum Playbook'
    other = url('en', 'article') if lang == 'de' else None
    body = f'''<main id="main" class="wrap page"><div class="article">
<a class="back" href="{url(lang, 'playbook')}">{BACK}{back}</a>
<p class="meta" style="margin-top:28px"><b>{FMT['analyse'][i]}</b>  |  {E(RUBN['spieler'][i])}  |  Chris Pracher, cp7  |  {a['date'][i]}</p>
<h1>{E(a['title'][i])}</h1>
{inner}
<section class="note" style="margin-top:40px"><h2>{basis[0]}</h2><p>{basis[1]}</p></section>
<section class="panel-tint" style="margin-top:24px"><h2 style="font-size:28px">{origin[0]}</h2><p class="meta" style="font-size:17px">{origin[1]}</p>
<div class="actions"><a class="btn btn-primary" href="{origin[3]}" rel="noopener" target="_blank">{origin[2]}</a>{f'<a class="btn btn-ghost" href="{other}" lang="en">English version</a>' if other else ''}</div></section>
<p class="meta" style="margin-top:48px;padding-top:16px;border-top:2px solid var(--border);font-size:13px">Niners Faithful Europe  |  Chris Pracher  |  {a['date'][i]}</p>
</div></main>'''
    return page(lang, 'article', a['title'][i], a['teaser'][i], body)

# ---------------- Stat Sheet ----------------
def stats(lang):
    i = I(lang)
    vals = [('Brock Purdy', 8.00), ('Patrick Mahomes', 7.39), ('Lamar Jackson', 7.32), ('Peyton Manning', 7.17), ('Aaron Rodgers', 7.14)]
    fmtv = (lambda v: f'{v:.2f}'.replace('.', ',')) if lang == 'de' else (lambda v: f'{v:.2f}')
    bars = ''.join(f'<div class="bar"><span>{n}</span><span class="track"><span class="fill" style="width:{round(v / 8.4 * 100)}%;animation-delay:{k * 60}ms">{fmtv(v)}</span></span></div>' for k, (n, v) in enumerate(vals))
    rows = ''.join(f'<tr><td>{n}</td><td>{fmtv(v)}</td></tr>' for n, v in vals)
    L = {
      'de': dict(title='Stat Sheet', intro='Statistik-Grafiken mit kurzer Einordnung, zum Teilen gemacht. Jede Grafik nennt Quelle und Datenstand.',
                 ct='Die ewige ANY/A-Bestenliste', cs='Adjusted Net Yards per Pass Attempt, Karriere, mindestens 1.500 Passversuche',
                 alt='Balkendiagramm: Brock Purdy führt mit 8,00 vor Patrick Mahomes (7,39), Lamar Jackson (7,32), Peyton Manning (7,17) und Aaron Rodgers (7,14).',
                 src='Quelle: Pro Football Reference  |  Datenstand: 20. Oktober 2026', note='Purdys Vorsprung von 0,61 auf Mahomes ist fast so groß wie der Abstand zwischen Mahomes auf Platz 2 und Russell Wilson auf Platz 16. Die 1.500er-Marke hat er aber erst im Oktober 2026 überschritten.',
                 credit='Beim Teilen bitte die Quelle nennen: Niners Faithful Europe, Chris Pracher, mit Link zu dieser Seite.', copy='Link kopieren', copied='Link kopiert', more='Zur Analyse', table='Daten als Tabelle', col='Quarterback',
                 inter='Interaktive Grafiken', c1='Karriere-QBR aller Quarterbacks mit mehr als 1.500 Pässen seit 2006, mit Streudiagramm und Saisonverlauf.', c2='Success Rate, Explosive Rate und EPA/Play als Index für alle 32 Teams, mit verstellbarer Gewichtung.', open='Öffnen'),
      'en': dict(title='Stat Sheet', intro='Stat graphics with a short explanation, made for sharing. Every graphic names its source and data date.',
                 ct='The all-time ANY/A leaderboard', cs='Adjusted net yards per pass attempt, career, minimum 1,500 attempts',
                 alt='Bar chart: Brock Purdy leads with 8.00 ahead of Patrick Mahomes (7.39), Lamar Jackson (7.32), Peyton Manning (7.17) and Aaron Rodgers (7.14).',
                 src='Source: Pro Football Reference  |  Data as of: October 20, 2026', note='Purdy’s margin of 0.61 over Mahomes is almost as large as the gap between Mahomes in second and Russell Wilson in 16th. He only passed the 1,500-attempt mark in October 2026, though.',
                 credit='When sharing, please credit Niners Faithful Europe, Chris Pracher, with a link to this page.', copy='Copy link', copied='Link copied', more='Read the analysis', table='Data as a table', col='Quarterback',
                 inter='Interactive graphics', c1='Career QBR of every quarterback with more than 1,500 passes since 2006, with scatter plot and season view.', c2='Success rate, explosive rate and EPA/play as an index for all 32 teams, with adjustable weights.', open='Open'),
    }[lang]
    body = f'''<main id="main" class="wrap page">
<h1 class="page-title">{L['title']}</h1><p class="lead-text">{L['intro']}</p>
<div style="max-width:920px">
<figure class="chart" role="img" aria-label="{E(L['alt'])}" style="margin-left:0;margin-right:0">
<div><span style="font-family:var(--serif);font-size:26px;display:block">{L['ct']}</span><span class="meta" style="font-size:15px">{L['cs']}</span></div>
<div style="display:flex;flex-direction:column;gap:12px">{bars}</div>
<div class="meta" style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;padding-top:14px;border-top:1px solid var(--border);font-size:13px"><span>{L['src']}</span><span style="font-family:var(--serif);color:var(--fg)">Niners Faithful <span style="color:var(--primary)">Europe</span></span></div>
</figure>
<p style="margin-top:32px;font-size:21px;line-height:1.55;max-width:62ch">{L['note']}</p>
<div class="actions" style="margin-top:28px"><a class="btn btn-primary" href="{url(lang, 'article')}">{L['more']}</a><button type="button" class="btn btn-ghost" data-copy data-copied="{L['copied']}">{L['copy']}</button></div>
<p class="meta" style="margin-top:16px">{L['credit']}</p>
<details style="margin-top:28px;max-width:520px"><summary>{L['table']}</summary><table><thead><tr><th scope="col">{L['col']}</th><th scope="col">ANY/A</th></tr></thead><tbody>{rows}</tbody></table></details>
</div>
<section style="margin-top:88px"><div class="section-head"><h2>{L['inter']}</h2></div>
<div class="cards">
<a class="card spot" href="https://cp7.beer/projects/qbr-career-stats/" rel="noopener" target="_blank"><span class="meta"><b>{FMT['grafik'][i]}</b>  |  Chris Pracher, cp7</span><h3>QBR Career Stats</h3><p>{L['c1']}</p><span class="meta" style="color:var(--primary);font-weight:600">{L['open']} {ARROW}</span></a>
<a class="card spot" href="https://cp7.beer/projects/supplex-index-2026/" rel="noopener" target="_blank"><span class="meta"><b>{FMT['grafik'][i]}</b>  |  Chris Pracher, cp7</span><h3>SUPPLEX+ Index 2026</h3><p>{L['c2']}</p><span class="meta" style="color:var(--primary);font-weight:600">{L['open']} {ARROW}</span></a>
</div></section>
</main>'''
    return page(lang, 'stats', L['title'], L['intro'], body)

# ---------------- Line-up und Roster ----------------
def picker_page(lang, key, title, intro, items, square):
    i = I(lang)
    btns, panels = '', ''
    for it in items:
        sq = ' sq' if square else ''
        btns += (f'<button type="button" class="person" data-pick="{it["id"]}" aria-pressed="false"><span class="mono{sq} {it["cls"]}" aria-hidden="true">{E(it["mono"])}</span>'
                 f'<span><span class="nm">{E(it["name"])}</span><span class="sub">{E(it["sub"])}</span></span>{it["right"]}</button>')
        posts = ''.join(f'<a class="post" href="{h}"{ext(h)}><span class="t">{E(t_)}</span><span class="meta"><b>{E(f)}</b>  |  {E(d)}</span></a>' for t_, f, d, h in it['posts'])
        facts = ''.join(f'<div><span>{E(k)}</span>{E(v)}</div>' for k, v in it['facts'])
        panels += (f'<article class="profile" data-panel="{it["id"]}"><div class="top"><span class="mono{sq} big {it["cls"]}" aria-hidden="true">{E(it["mono"])}</span>'
                   f'<div><h2>{E(it["name"])}</h2><span class="meta" style="font-size:15px">{E(it["sub"])}</span></div></div>'
                   f'<p class="bio">{E(it["bio"])}</p><div class="actions"><a class="btn btn-primary" href="{it["href"]}"{ext(it["href"])}>{E(it["cta"])}</a></div>'
                   + (f'<div class="facts">{facts}</div>' if facts else '') + (f'<div class="posts">{posts}</div>' if posts else '') + '</article>')
    body = f'''<main id="main" class="wrap page"><h1 class="page-title">{title}</h1><p class="lead-text">{intro}</p>
<div class="layout"><div class="picker" role="group" data-picker>{btns}</div><div aria-live="polite">{panels}</div></div></main>'''
    return page(lang, key, title, intro, body)

def posts_of(aut=None, src=None, lang='de'):
    i = I(lang); out = []
    for a in ART:
        if (aut and a['aut'] != aut) or (src and a['src'] != src): continue
        out.append((a['title'][i], FMT[a['fmt']][i], a['date'][i], art_link(a, lang)[0]))
    return out

def lineup(lang):
    i = I(lang)
    count = lambda n: f'{n} ' + (('Beitrag', 'article') if n == 1 else ('Beiträge', 'articles'))[i]
    items = [
      dict(id='cp', mono='C', cls='m-red', name='Chris Pracher', sub='Niner Empire Germany e.V., cp7', right=f'<span class="meta" style="color:var(--gold);font-weight:700">{count(len(posts_of("CP", lang=lang)))}</span>',
           bio=('Schreibt für The Niner Empire Germany e.V. und auf cp7 über die 49ers: Quarterback-Statistiken, Draft-Bilanzen, Season Stats und die Offense von Kyle Shanahan.',
                'Writes about the 49ers for The Niner Empire Germany e.V. and on cp7: quarterback stats, draft records, season stats and Kyle Shanahan’s offense.')[i],
           href='https://cp7.beer/', cta=('Zu cp7', 'Visit cp7')[i], facts=[(('Schwerpunkt', 'Focus')[i], ('Statistik, Draft und Scheme', 'Stats, draft and scheme')[i]), (('Kanäle', 'Channels')[i], 'theninerempiregermany.de, cp7.beer')], posts=posts_of('CP', lang=lang)),
      dict(id='lu', mono='L', cls='m-ink', name='Lukas', sub='Niner Empire Germany e.V.', right=f'<span class="meta" style="color:var(--gold);font-weight:700">{count(1)}</span>',
           bio=('Schreibt für The Niner Empire Germany e.V. über den Kader der 49ers, etwa mit Roster-Prognosen vor dem Training Camp.', 'Writes about the 49ers roster for The Niner Empire Germany e.V., for example with roster predictions before training camp.')[i],
           href=NEG, cta=('Zum Niner Empire Germany', 'Visit Niner Empire Germany')[i], facts=[(('Schwerpunkt', 'Focus')[i], ('Kader und Roster', 'Roster')[i])], posts=posts_of('LU', lang=lang)),
      dict(id='you', mono='+', cls='m-tint', name=('Dein Platz', 'Your spot')[i], sub=('Deutschland, Österreich, Schweiz', 'Germany, Austria, Switzerland')[i], right=f'<span class="badge badge-open">{("Frei", "Open")[i]}</span>',
           bio=('Du schreibst über die 49ers oder die NFL auf Deutsch? Hier ist Platz für dich. Deine Texte bleiben bei dir, wir kümmern uns um Teaser, englische Fassung und Reichweite.',
                'Do you write about the 49ers or the NFL in German? There is a spot for you here. Your work stays yours; we handle the teaser, the English version and the reach.')[i],
           href=url(lang, 'plan') + '#tryout', cta=('Zum Tryout', 'Sign up for a tryout')[i], facts=[], posts=[]),
    ]
    return picker_page(lang, 'lineup', ('Das Line-up', 'The line-up')[i],
                       ('Jeder Autor behält seinen Kanal und seine Rechte. Hier findest du alle an einem Ort, mit ihren Beiträgen.', 'Every author keeps their own channel and rights. Here you find all of them in one place, with their work.')[i], items, False)

def roster(lang):
    i = I(lang)
    st = {'in': ('Im Roster', 'On the roster', 'badge-ink'), 'talks': ('Im Gespräch', 'In talks', 'badge-soft'), 'open': ('Platz frei', 'Open spot', 'badge-open')}
    b = lambda k: f'<span class="badge {st[k][2]}">{st[k][i]}</span>'
    n_neg = sum(1 for a in ART if a['src'] == 'Niner Empire Germany'); n_cp7 = sum(1 for a in ART if a['src'] == 'cp7')
    cnt = lambda n: f'{n} ' + (('Beitrag', 'article') if n == 1 else ('Beiträge', 'articles'))[i]
    lu, pb = ('Im Line-up', 'In the line-up')[i], ('Im Playbook', 'In the playbook')[i]
    items = [
      dict(id='neg', mono='NEG', cls='m-red', name='The Niner Empire Germany e.V.', sub=('Fanclub und Verein  |  Deutschland', 'Fan club  |  Germany')[i], right=b('in'),
           bio=('Deutscher Fanclub der San Francisco 49ers mit Spielanalysen, Draft-Berichten, Season Stats und Roster-Prognosen. Initiator der Collab.', 'German fan club of the San Francisco 49ers with game analysis, draft reports, season stats and roster predictions. Started the collaboration.')[i],
           href=NEG, cta=('Zur Seite', 'Visit site')[i], facts=[(lu, 'Chris Pracher, Lukas'), (pb, cnt(n_neg))], posts=posts_of(src='Niner Empire Germany', lang=lang)[:3]),
      dict(id='cp7', mono='cp7', cls='m-ink', name='cp7', sub=('Statistik-Projekte  |  Deutschland', 'Stats projects  |  Germany')[i], right=b('in'),
           bio=('Interaktive Statistik-Projekte und Dossiers, etwa Career ANY/A, QBR Career Stats und der SUPPLEX+ Index.', 'Interactive stats projects and dossiers such as Career ANY/A, QBR Career Stats and the SUPPLEX+ Index.')[i],
           href='https://cp7.beer/', cta=('Zur Seite', 'Visit site')[i], facts=[(lu, 'Chris Pracher'), (pb, cnt(n_cp7))], posts=posts_of(src='cp7', lang=lang)),
      dict(id='ggs', mono='GGS', cls='m-gold', name='Golden Gate Stats', sub=('Statistik-Grafiken  |  Deutschland', 'Stat graphics  |  Germany')[i], right=b('talks'),
           bio=('Zweisprachige Seite mit Statistik-Grafiken zu den 49ers: Spielvorschauen, Nachberichte, Team- und Spieler-Stats.', 'Bilingual site with 49ers stat graphics: game previews, game reviews, team and player stats.')[i],
           href='https://goldengatestats.com/', cta=('Zur Seite', 'Visit site')[i], facts=[(pb, ('Noch keine Beiträge', 'No articles yet')[i])], posts=[]),
      dict(id='you', mono='+', cls='m-tint', name=('Dein Kanal', 'Your channel')[i], sub=('Blog, Podcast, Newsletter', 'Blog, podcast, newsletter')[i], right=b('open'),
           bio=('Fanclub, Blog, Podcast, Newsletter oder Statistik-Projekt aus dem deutschsprachigen Raum: Hier ist Platz für dich im Roster.', 'A fan club, blog, podcast, newsletter or stats project from the German-speaking world? There is a spot for you on the roster.')[i],
           href=url(lang, 'plan') + '#tryout', cta=('Zum Tryout', 'Sign up for a tryout')[i], facts=[], posts=[]),
    ]
    return picker_page(lang, 'roster', ('Der Roster', 'The roster')[i],
                       ('Niners Faithful Europe ist eine Collab. Diese Vereine, Seiten und Projekte stehen im Roster und bringen ihre Beiträge ein. Jeder behält seine eigene Seite, seine Marke und seine Rechte.',
                        'Niners Faithful Europe is a collaboration. These clubs, sites and projects are on the roster and contribute their work. Each keeps its own site, brand and rights.')[i], items, True)

# ---------------- Game Plan ----------------
def plan(lang):
    D = {
      'de': dict(h1='Der Game Plan von <span style="color:var(--primary)">Niners Faithful Europe</span>', intro='Wir bündeln die Arbeit deutschsprachiger Football-Autoren und machen sie international auffindbar. Gestartet aus dem Umfeld des Niner Empire Germany e.V., offen für alle Autoren aus Deutschland, Österreich und der Schweiz.',
                 steps=[('Du veröffentlichst wie bisher', 'Substack, X oder die eigene Website bleiben der Ort deines deutschen Originals.'), ('Wir zeigen den Teaser', 'Titel, kurzer Anriss und Link zu deinem Original, sortiert nach Format, Rubrik und Autor. Grafiken erscheinen komplett, mit Quelle und Datenstand.'), ('Die englische Fassung folgt', 'Eine KI-Übersetzung mit Football-Glossar, von dir oder der Redaktion geprüft, dann im Volltext veröffentlicht.')],
                 trio=[('DEINE RECHTE', 'Texte und Grafiken bleiben bei dir. Einzelne Beiträge lassen sich jederzeit entfernen.'), ('KEINE COOKIES', 'Gehostet bei Cloudflare, keine Cookies, keine Tracker.'), ('UNABHÄNGIG', 'Ein Fanprojekt ohne Verbindung zur NFL oder zu den San Francisco 49ers.')],
                 tt='Zum Tryout', tp='Du schreibst über die 49ers oder die NFL auf Deutsch, analysierst Tape oder baust Statistik-Grafiken? Erzähl uns kurz, wo du veröffentlichst.',
                 ln='Name oder Pseudonym', en='Bitte gib einen Namen an.', lu='Link zu deinem Kanal', hu='Substack, X, eigene Website oder Podcast', eu='Bitte einen Link angeben, der mit https:// beginnt.',
                 lf='Was schreibst du vor allem?', opts=['Fantexte', 'Analysen zu Statistik und Tape', 'Statistik-Grafiken', 'Von allem etwas'], lm='Nachricht (optional)', send='Zum Tryout anmelden',
                 thx='Danke,', done='Im Provisorium wird die Anmeldung noch nicht verschickt. Melde dich bis zum Start bitte direkt beim Niner Empire Germany.', again='Weitere Anmeldung'),
      'en': dict(h1='The game plan of <span style="color:var(--primary)">Niners Faithful Europe</span>', intro='We bring together the work of German-speaking football writers and make it easy to find internationally. Started by people around the Niner Empire Germany e.V., open to every writer from Germany, Austria and Switzerland.',
                 steps=[('You publish as before', 'Substack, X or your own website stay the home of your German original.'), ('We show the teaser', 'Title, a short summary and a link to your original, sorted by format, section and author. Graphics appear in full, with source and data date.'), ('The English version follows', 'An AI translation with a football glossary, checked by you or the editors, then published in full.')],
                 trio=[('YOUR RIGHTS', 'Your texts and graphics stay yours. Any article can be removed at any time.'), ('NO COOKIES', 'Hosted on Cloudflare, no cookies, no trackers.'), ('INDEPENDENT', 'A fan project with no ties to the NFL or the San Francisco 49ers.')],
                 tt='Sign up for a tryout', tp='You write about the 49ers or the NFL in German, break down tape or build stat graphics? Tell us briefly where you publish.',
                 ln='Name or pen name', en='Please enter a name.', lu='Link to your channel', hu='Substack, X, your own website or podcast', eu='Please enter a link starting with https://.',
                 lf='What do you mostly write?', opts=['Fan pieces', 'Stats and tape analysis', 'Stat graphics', 'A bit of everything'], lm='Message (optional)', send='Sign up',
                 thx='Thanks,', done='In this preview the sign-up is not sent yet. Until launch, please contact the Niner Empire Germany directly.', again='Another sign-up'),
    }[lang]
    steps = ''.join(f'<div class="step"><span class="n" aria-hidden="true">{k + 1}</span><h2>{E(a)}</h2><p>{E(b)}</p></div>' for k, (a, b) in enumerate(D['steps']))
    trio = ''.join(f'<div><h2>{a}</h2><p>{E(b)}</p></div>' for a, b in D['trio'])
    opts = ''.join(f'<option>{E(o)}</option>' for o in D['opts'])
    body = f'''<main id="main" class="wrap page">
<h1 class="page-title" style="max-width:16ch">{D['h1']}</h1><p class="lead-text">{D['intro']}</p>
<div class="steps">{steps}</div>
<section class="trio">{trio}</section>
<section class="tryout" id="tryout" aria-labelledby="tt">
<div style="display:flex;flex-direction:column;gap:14px"><h2 id="tt">{D['tt']}</h2><p class="meta" style="font-size:18px;max-width:44ch">{D['tp']}</p></div>
<div>
<form class="form" data-tryout novalidate>
<div class="field"><label for="f-name">{D['ln']}</label><input id="f-name" type="text" autocomplete="name" aria-describedby="e-name"><span id="e-name" class="err" hidden>{D['en']}</span></div>
<div class="field"><label for="f-url">{D['lu']}</label><input id="f-url" type="url" inputmode="url" placeholder="https://" aria-describedby="h-url e-url"><span id="h-url" class="hint">{D['hu']}</span><span id="e-url" class="err" hidden>{D['eu']}</span></div>
<div class="field"><label for="f-fmt">{D['lf']}</label><select id="f-fmt">{opts}</select></div>
<div class="field"><label for="f-msg">{D['lm']}</label><textarea id="f-msg"></textarea></div>
<button type="submit" class="btn btn-primary" style="align-self:flex-start">{D['send']}</button>
</form>
<div class="done" data-done role="status" tabindex="-1" hidden><h3 style="font-size:28px">{D['thx']} <span data-name></span>!</h3><p class="meta" style="font-size:16px">{D['done']}</p>
<div class="actions"><a class="btn btn-primary" href="{NEG}" rel="noopener" target="_blank">Niner Empire Germany</a><button type="button" class="btn btn-ghost" data-again>{D['again']}</button></div></div>
</div>
</section>
</main>'''
    return page(lang, 'plan', 'Game Plan', D['intro'], body)


# ---------------- Inbox (intern, nicht verlinkt) ----------------
EDIT = 'https://github.com/cpracher-cloud/niners-faithful-europe/edit/main/data/articles.json'
def inbox(lang):
    rows = ''.join(
        f'<a class="row spot" href="{a["de"]}" rel="noopener" target="_blank"><span class="t"><h2>{E(a["title"][0])}</h2><span class="tz">{E(a["teaser"][0])}</span>'
        f'<span class="meta"><b>Vorschlag: {FMT[a["fmt"]][0]}</b>  |  {E(RUBN[a["rub"]][0])}  |  {E(a["author"])}, {E(a["src"])}  |  {a["date"][0]}  |  id: {E(a["id"])}</span></span></a>'
        for a in DRAFTS) or '<p class="meta">Keine offenen Entwürfe. Der Import läuft täglich um 6:17 Uhr.</p>'
    body = f'''<main id="main" class="wrap page"><h1 class="page-title">Inbox</h1>
<p class="lead-text">{len(DRAFTS)} neue Beiträge aus den Feeds warten auf Freigabe. Rubrik und Format sind Vorschläge. Zum Freigeben in der Datendatei beim Beitrag <code>"status": "entwurf"</code> auf <code>"live"</code> setzen (ablehnen: <code>"abgelehnt"</code>), dabei Rubrik und Format prüfen. Die Seite baut sich danach von selbst neu.</p>
<div class="actions" style="margin:24px 0 8px"><a class="btn btn-primary" href="{EDIT}" rel="noopener" target="_blank">Datendatei bearbeiten</a></div>
<div class="rows">{rows}</div></main>'''
    return page(lang, 'inbox', 'Inbox', 'Entwürfe aus dem Feed-Import', body)

# ---------------- Ausgabe ----------------
if os.path.isdir(OUT):
    for name in os.listdir(OUT):
        p = os.path.join(OUT, name)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
shutil.copy(os.path.join(HERE, 'site.css'), os.path.join(OUT, 'assets', 'site.css'))
shutil.copy(os.path.join(HERE, 'site.js'), os.path.join(OUT, 'assets', 'site.js'))
shutil.copy(os.path.join(HERE, 'watermark.svg'), os.path.join(OUT, 'assets', 'watermark.svg'))
for lang in ('de', 'en'):
    for key, fn in [('kickoff', kickoff), ('playbook', playbook), ('article', article), ('stats', stats), ('lineup', lineup), ('roster', roster), ('plan', plan)]:
        d = os.path.join(OUT, lang, PAGES[key]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(fn(lang))
for lang in ('de', 'en'):
    d = os.path.join(OUT, lang, PAGES['inbox']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(inbox(lang))
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Niners Faithful Europe</title>
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url={P}/de/">
<script>location.replace((navigator.language || 'de').toLowerCase().indexOf('de') === 0 ? '{P}/de/' : '{P}/en/');</script>
</head>
<body><p><a href="{P}/de/">Deutsch</a> | <a href="{P}/en/">English</a></p></body>
</html>
''')
print('gebaut:', OUT)
