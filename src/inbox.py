#!/usr/bin/env python3
"""Freigabe über GitHub-Issues.

  python3 src/inbox.py open     legt für jeden Entwurf ohne Issue eines an (Häkchen für Format, Rubrik, Autor)
  python3 src/inbox.py review   wertet ein geschlossenes Issue aus (Event-Datei aus GITHUB_EVENT_PATH):
                                "Close as completed" = freigeben, "Close as not planned" = ablehnen
  python3 src/inbox.py author   verarbeitet ein Issue aus dem Formular "Autor anlegen oder ändern"

Braucht GITHUB_TOKEN und GITHUB_REPOSITORY (in GitHub Actions vorhanden).
"""
import json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(os.path.dirname(HERE), 'data', 'articles.json')
AUT = os.path.join(os.path.dirname(HERE), 'data', 'authors.json')
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


def load_authors():
    return json.load(open(AUT, encoding='utf-8'))


def save_authors(auts):
    json.dump(auts, open(AUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def authors(arts=None):
    """Alle Autoren aus data/authors.json (Kürzel, Name), NEG als Platzhalter zuletzt."""
    return sorted(((x['aut'], x['name']) for x in load_authors()), key=lambda x: x[1]) + [('NEG', 'Niner Empire Germany (Autor unbekannt)')]


def new_code(name, auts):
    """Kürzel aus den Initialen, bei Bedarf mit Ziffer eindeutig gemacht."""
    parts = re.findall(r'[A-Za-zÄÖÜäöü]+', name) or ['X']
    base = (parts[0][0] + (parts[-1][0] if len(parts) > 1 else parts[0][1:2])).upper().replace('Ä', 'A').replace('Ö', 'O').replace('Ü', 'U')
    taken = {x['aut'] for x in auts} | {'NEG'}
    code, n = base, 2
    while code in taken:
        code, n = f'{base}{n}', n + 1
    return code


def find_or_create(name, auts):
    """Autor per Name finden oder als neues Profil (nur mit Namen) anlegen."""
    hit = next((x for x in auts if x['name'].lower() == name.lower()), None)
    if hit:
        return hit, False
    x = dict(aut=new_code(name, auts), name=name)
    auts.append(x)
    return x, True


def boxes(options, current):
    return '\n'.join(f"- [{'x' if k == current else ' '}] {label}" for k, label in options)


def body(a, arts):
    y, m, d = a['date'].split('-') if a.get('date') else ('', '1', '')
    date = f'{int(d)}. {MON[int(m) - 1]} {y}' if d else 'ohne Datum'
    teaser = '\n'.join('> ' + line for line in (a['teaser']['de'] or '(kein Anriss)').splitlines())
    return f"""**{a['src']}**  |  {date}
**Original:** {a['link']['de']}

{teaser}

**So geht's:** Häkchen einfach direkt anklicken (kein Bearbeiten nötig), dann
- **Freigeben:** Issue schließen mit **Close as completed**
- **Ablehnen:** Issue schließen mit **Close as not planned**

**Anderer Autor oder englische Fassung?** Vor dem Schließen einen Kommentar schreiben, z. B.
```
Autor: Vorname Nachname
Titel EN: English title
Teaser EN: One or two sentences in English.
```
Ein neuer Name wird dabei gleich als Autor angelegt.

### Format
{boxes(FMT, a['fmt'])}

### Rubrik
{boxes(RUB, a['rub'])}

### Autor
{boxes(authors(arts), a['aut'])}

<!-- nfe-id: {a['id']} -->
<!-- nfe-v2 -->"""


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


def cmd_refresh():
    """Ältere Freigabe-Tickets einmalig auf die aktuelle Fassung bringen (angeklickte Häkchen bleiben bei neuen Tickets unberührt)."""
    arts = load()
    for a in arts:
        n = a.get('imported', {}).get('issue')
        if a['status'] != 'entwurf' or not n:
            continue
        cur = api('GET', f'/issues/{n}')
        if cur['state'] == 'open' and '<!-- nfe-v2 -->' not in (cur.get('body') or ''):
            api('PATCH', f'/issues/{n}', {'body': body(a, arts)})
            print(f'Ticket #{n} aktualisiert')


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
        notes = '\n'.join(c['body'] for c in api('GET', f"/issues/{iss['number']}/comments?per_page=100"))
        def note(key):
            hits = re.findall(rf'^\s*{key}\s*:[ \t]*(.+)$', notes, re.M | re.I)
            return hits[-1].strip() if hits else ''
        if note('Titel EN'): a['title']['en'] = note('Titel EN')
        if note('Teaser EN'): a['teaser']['en'] = note('Teaser EN')
        nm = re.search(r'^Neuer Autor[^:]*:[ \t]*(.+)$', section(text, 'Autor'), re.M)
        if note('Autor'):
            nm = re.match(r'(.+)', note('Autor'))
        if nm and nm.group(1).strip():
            people = load_authors()
            x, created = find_or_create(nm.group(1).strip(), people)
            if created:
                save_authors(people)
            a['aut'], a['author'] = x['aut'], x['name']
        en = section(text, 'Englische Fassung')
        t = re.search(r'^Titel:[ \t]*(.+)$', en, re.M); z = re.search(r'^Teaser:[ \t]*(.+)$', en, re.M)
        if t: a['title']['en'] = t.group(1).strip()
        if z: a['teaser']['en'] = z.group(1).strip()
        a['status'] = 'live'; msg = 'Freigegeben. Die Seite wird in ein bis zwei Minuten neu veröffentlicht.'
    save(arts)
    api('POST', f"/issues/{iss['number']}/comments", {'body': msg})
    print(msg)


def form(text):
    """Felder eines Issue-Formulars: Überschrift -> Inhalt (leer bei '_No response_')."""
    out = {}
    for m in re.finditer(r'^### (.+?)\n+(.*?)(?=^### |\Z)', text, re.S | re.M):
        v = m.group(2).strip()
        out[m.group(1).strip()] = '' if v == '_No response_' else v
    return out


def cmd_author():
    ev = json.load(open(os.environ['GITHUB_EVENT_PATH'], encoding='utf-8'))
    iss = ev['issue']
    if 'autor' not in [l['name'] for l in iss.get('labels', [])]:
        print('Kein Autoren-Issue.'); return
    f = form(iss.get('body') or '')
    auts = load_authors()
    name, code = f.get('Name', ''), f.get('Kürzel', '').upper()
    hit = next((x for x in auts if code and x['aut'] == code), None) or next((x for x in auts if name and x['name'].lower() == name.lower()), None)
    if f.get('Aktion', '').startswith('Entfernen'):
        if not hit:
            msg = f'Kein Autor mit Kürzel „{code}“ oder Namen „{name}“ gefunden, nichts geändert.'
        else:
            auts.remove(hit); msg = f'{hit["name"]} ({hit["aut"]}) wurde aus dem Line-up entfernt. Bestehende Beiträge bleiben erhalten.'
    else:
        x = hit or dict(aut=new_code(name, auts), name=name)
        if not hit:
            auts.append(x)
        if name: x['name'] = name
        if f.get('Website') and f['Website'] != x.get('url'):
            x['url'] = f['Website']; x.pop('url_label', None)  # Button heißt dann "Zur Website"
        for key, field in [('sub', 'Verein oder Kanal'), ('channels', 'Kanäle')]:
            if f.get(field): x[key] = f[field]
        for key, de, en in [('bio', 'Kurzprofil (Deutsch)', 'Kurzprofil (Englisch)'), ('focus', 'Schwerpunkt (Deutsch)', 'Schwerpunkt (Englisch)')]:
            cur = x.setdefault(key, {})
            if f.get(de): cur['de'] = f[de]
            if f.get(en): cur['en'] = f[en]
        msg = (f'{x["name"]} wurde geändert' if hit else f'{x["name"]} wurde angelegt') + f' (Kürzel {x["aut"]}). Das Line-up wird in ein bis zwei Minuten neu veröffentlicht.'
        # Name auch in bestehenden Beiträgen nachziehen
        arts = load(); ch = False
        for a in arts:
            if a['aut'] == x['aut'] and a['author'] != x['name']:
                a['author'] = x['name']; ch = True
        if ch: save(arts)
    save_authors(auts)
    api('POST', f"/issues/{iss['number']}/comments", {'body': msg})
    api('PATCH', f"/issues/{iss['number']}", {'state': 'closed', 'state_reason': 'completed'})
    print(msg)


if __name__ == '__main__':
    {'open': cmd_open, 'refresh': cmd_refresh, 'review': cmd_review, 'author': cmd_author}[sys.argv[1]]()
