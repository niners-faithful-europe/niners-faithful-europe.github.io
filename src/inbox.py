#!/usr/bin/env python3
"""Freigabe über GitHub-Issues.

  python3 src/inbox.py open     legt für jeden Entwurf ohne Issue eines an (Häkchen für Format, Rubrik, Autor)
  python3 src/inbox.py review   wertet ein geschlossenes Issue aus (Event-Datei aus GITHUB_EVENT_PATH):
                                "Close as completed" = freigeben, "Close as not planned" = ablehnen

Braucht GITHUB_TOKEN und GITHUB_REPOSITORY (in GitHub Actions vorhanden).
"""
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(os.path.dirname(HERE), 'data', 'articles.json')
MARK = re.compile(r'<!-- nfe-id: ([^ ]+) -->')

FMT = [('analyse', 'Analyse'), ('fantext', 'Fantext'), ('grafik', 'Grafik')]
RUB = [('vorschau', 'Spielvorschau'), ('nachbericht', 'Spielnachbericht'), ('team', 'Team-Stats'),
       ('spieler', 'Spieler-Stats'), ('draft', 'Draft und Kader'), ('scheme', 'Scheme und Tape')]
MON = ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sept.', 'Okt.', 'Nov.', 'Dez.']


def api(method, path, body=None):
    req = urllib.request.Request(f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Authorization': f"Bearer {os.environ['GITHUB_TOKEN']}", 'Accept': 'application/vnd.github+json',
                                          'Content-Type': 'application/json', 'User-Agent': 'nfe-inbox'})
    return json.load(urllib.request.urlopen(req, timeout=30))


def load():
    return json.load(open(ART, encoding='utf-8'))


def save(arts):
    json.dump(arts, open(ART, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def authors(arts):
    """Alle bekannten Autoren (Kürzel, Name), NEG als Platzhalter zuletzt."""
    seen = {(a['aut'], a['author']) for a in arts if a['aut'] != 'NEG'}
    return sorted(seen, key=lambda x: x[1]) + [('NEG', 'Niner Empire Germany (Autor unbekannt)')]


def boxes(options, current):
    return '\n'.join(f"- [{'x' if k == current else ' '}] {label}" for k, label in options)


def body(a, arts):
    y, m, d = a['date'].split('-') if a.get('date') else ('', '1', '')
    date = f'{int(d)}. {MON[int(m) - 1]} {y}' if d else 'ohne Datum'
    teaser = '\n'.join('> ' + line for line in (a['teaser']['de'] or '(kein Anriss)').splitlines())
    return f"""**{a['src']}**  |  {date}
**Original:** {a['link']['de']}

{teaser}

Häkchen bei Bedarf umsetzen (je Abschnitt eins; den Vorschlag musst du nicht abhaken), dann:
- **Freigeben:** Issue schließen mit **Close as completed**
- **Ablehnen:** Issue schließen mit **Close as not planned**

### Format
{boxes(FMT, a['fmt'])}

### Rubrik
{boxes(RUB, a['rub'])}

### Autor
{boxes(authors(arts), a['aut'])}

### Englische Fassung (optional)
Titel:
Teaser:

<!-- nfe-id: {a['id']} -->"""


def cmd_open():
    arts = load(); changed = False
    for a in arts:
        if a['status'] != 'entwurf' or a.get('imported', {}).get('issue'):
            continue
        issue = api('POST', '/issues', {'title': f"Freigabe: {a['title']['de']}", 'body': body(a, arts)})
        a.setdefault('imported', {})['issue'] = issue['number']; changed = True
        print(f"Issue #{issue['number']} für {a['id']}")
    if changed:
        save(arts)


def section(text, name):
    m = re.search(rf'### {re.escape(name)}[^\n]*\n(.*?)(?=\n### |\n<!--|\Z)', text, re.S)
    return m.group(1) if m else ''


def checked(text, name, options, current=None):
    """Angehaktes Feld eines Abschnitts. Sind mehrere angehakt, gewinnt das, was vom Vorschlag abweicht."""
    labels = {label.lower(): k for k, label in options}
    hits = [labels[m.group(1).strip().lower()] for m in re.finditer(r'- \[[xX]\] (.+)', section(text, name)) if m.group(1).strip().lower() in labels]
    changed = [k for k in hits if k != current]
    return (changed or hits or [None])[0]


def cmd_review():
    ev = json.load(open(os.environ['GITHUB_EVENT_PATH'], encoding='utf-8'))
    iss = ev['issue']; text = iss.get('body') or ''
    m = MARK.search(text)
    if not m:
        print('Kein Freigabe-Issue.'); return
    arts = load()
    a = next((x for x in arts if x['id'] == m.group(1)), None)
    if not a or a['status'] != 'entwurf':
        print('Beitrag nicht gefunden oder schon bearbeitet.'); return
    if iss.get('state_reason') == 'not_planned':
        a['status'] = 'abgelehnt'; msg = 'Abgelehnt. Der Beitrag wird nicht erneut importiert.'
    else:
        a['fmt'] = checked(text, 'Format', FMT, a['fmt']) or a['fmt']
        a['rub'] = checked(text, 'Rubrik', RUB, a['rub']) or a['rub']
        auts = authors(arts)
        k = checked(text, 'Autor', auts, a['aut'])
        if k:
            a['aut'] = k
            a['author'] = 'Niner Empire Germany' if k == 'NEG' else dict(auts)[k]
        en = section(text, 'Englische Fassung')
        t = re.search(r'^Titel:[ \t]*(.+)$', en, re.M); z = re.search(r'^Teaser:[ \t]*(.+)$', en, re.M)
        if t: a['title']['en'] = t.group(1).strip()
        if z: a['teaser']['en'] = z.group(1).strip()
        a['status'] = 'live'; msg = 'Freigegeben. Die Seite wird in ein bis zwei Minuten neu veröffentlicht.'
    save(arts)
    api('POST', f"/issues/{iss['number']}/comments", {'body': msg})
    print(msg)


if __name__ == '__main__':
    {'open': cmd_open, 'review': cmd_review}[sys.argv[1]]()
