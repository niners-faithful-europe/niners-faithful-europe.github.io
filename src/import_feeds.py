#!/usr/bin/env python3
"""Holt neue Beiträge aus den Quellen in data/sources.json und legt sie als Entwurf in data/articles.json an.

Aufruf: python3 import_feeds.py [--feed-file DATEI]   (--feed-file ersetzt den RSS-Abruf, zum Testen)
Bestehende Einträge werden nie verändert; erkannt wird ein Beitrag an seinem Link.
"""
import html, json, os, re, sys, urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
ART = os.path.join(DATA, 'articles.json')
SRC = os.path.join(DATA, 'sources.json')
DIAG = {}
KNOWN = set()  # bereits erfasste Links, damit bekannte Artikelseiten nicht erneut geladen werden
SEEN = {}  # Autorennamen je Feed, für data/import-status.json
NS = {'dc': 'http://purl.org/dc/elements/1.1/', 'content': 'http://purl.org/rss/1.0/modules/content/'}

# Vorschläge für Rubrik und Format: erstes passendes Stichwort gewinnt, die Redaktion bestätigt bei der Freigabe.
RUB_HINTS = [('nachbericht', ['nachbericht', 'recap', 'review', 'sieg gegen', 'niederlage', 'gameday']),
             ('vorschau', ['vorschau', 'preview', 'matchup', 'week ', 'woche ']),
             ('draft', ['draft', 'pick', 'roster', 'kader', '53-man', 'free agency', 'rookie']),
             ('scheme', ['scheme', 'playbook', 'coaching', 'shanahan', 'saleh', 'tape', 'play-action', 'zone']),
             ('spieler', ['purdy', 'quarterback', 'passer', 'any/a', 'qbr', 'karriere', 'career', 'spieler']),
             ('team', ['team', 'offense', 'defense', 'season stats', 'epa', 'index', 'saison'])]
FMT_HINTS = [('grafik', ['grafik', 'chart', 'index', 'stats', 'rangliste', 'interaktiv']),
             ('fantext', ['meinung', 'kommentar', 'prediction', 'prognose', 'fan', 'kolumne'])]


def guess(text, hints, default):
    t = text.lower()
    return next((k for k, words in hints if any(w in t for w in words)), default)


def norm(url):
    """Link-Vergleich unabhängig von Domain-Variante, Schema und Schrägstrich am Ende."""
    u = re.sub(r'^https?://(www\.)?', '', (url or '').strip().lower()).replace('cp7.online/', 'cp7.beer/')
    return u.rstrip('/')


def plain(s, limit=240):
    """HTML entfernen und auf einen Anriss kürzen, möglichst am Satzende."""
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))
    s = re.sub(r'\s+', ' ', s).replace('[…]', '').replace('[&hellip;]', '').strip()
    s = re.sub(r'\s*(Der Beitrag|The post) .*? erschien zuerst auf .*$', '', s)
    if len(s) <= limit: return s
    cut = s[:limit]
    end = max(cut.rfind('. '), cut.rfind('? '), cut.rfind('! '))
    return cut[:end + 1] if end > 80 else cut.rsplit(' ', 1)[0] + ' …'


def slug(url):
    return re.sub(r'[^a-z0-9-]+', '-', norm(url).rsplit('/', 1)[-1])[:60].strip('-') or 'beitrag'


def entry(source, url, title, teaser, date, who):
    text = f'{title} {teaser}'
    return dict(id=slug(url), status='entwurf', date=date, fmt=guess(text, FMT_HINTS, 'analyse'), rub=guess(text, RUB_HINTS, 'team'),
                aut=who['aut'], author=who['author'], src=source['name'],
                title=dict(de=title, en=None), teaser=dict(de=teaser, en=None), link=dict(de=url, en=None),
                imported=dict(source=source['id']))


def from_rss(source, feed_file=None):
    if feed_file:
        raw = open(feed_file, 'rb').read()
    else:
        req = urllib.request.Request(source['url'], headers={'User-Agent': 'NinersFaithfulEurope-Import/1.0 (+https://cp7.beer)'})
        raw = urllib.request.urlopen(req, timeout=30).read()
    root = ET.fromstring(raw)
    items = list(root.iter('item'))
    DIAG[source['id']] = dict(eintraege=len(items), felder=sorted({c.tag for c in items[0]}) if items else [], titel=[i.findtext('title') for i in items[:5]])
    for it in root.iter('item'):
        who_raw = (it.findtext('dc:creator', '', NS) or it.findtext('author', '') or '').strip()
        link = (it.findtext('link') or '').strip()
        title = html.unescape((it.findtext('title') or '').strip())
        if any(re.search(p, title) for p in source.get('skip_titles', [])):
            continue
        if not who_raw and source.get('author_from_page') and norm(link) not in KNOWN:
            who_raw = page_author(link)  # Feed ohne Autorennamen: auf der Artikelseite nachsehen
        SEEN.setdefault(source['id'], set()).add(who_raw)
        who = source.get('authors', {}).get(who_raw) or source.get('fallback_author')
        if not who:
            continue
        date = parsedate_to_datetime(it.findtext('pubDate')).date().isoformat() if it.findtext('pubDate') else ''
        teaser = plain(it.findtext('description') or it.findtext('content:encoded', '', NS))
        yield entry(source, link, title, teaser, date, who)


def page_author(url):
    """Autorenname aus der Artikelseite: Meta-Tag author, sonst Yoast-Schema (Person)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NinersFaithfulEurope-Import/1.0 (+https://cp7.beer)'})
        page = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
    except Exception:
        return ''
    for pat in (r'<meta[^>]+name=["\']author["\'][^>]+content=["\']([^"\']+)', r'"@type":"Person"[^{}]*?"name":"([^"]+)"',
):
        m = re.search(pat, page)
        if m:
            return html.unescape(m.group(1)).strip()
    return ''


def from_cp7(source):
    req = urllib.request.Request(source['url'], headers={'User-Agent': 'NinersFaithfulEurope-Import/1.0'})
    for p in json.load(urllib.request.urlopen(req, timeout=30)):
        text = f"{p.get('title', '')} {p.get('description', '')}".lower()
        if p['slug'] in source.get('exclude', []) or p['slug'].endswith('-en'):
            continue
        if not any(re.search(r'(?<![a-z0-9])' + re.escape(k) + r'(?![a-z0-9])', text) for k in source['keywords']):
            continue
        yield entry(source, source['base'] + p['slug'] + '/', p['title'], p.get('description', ''), p.get('date', ''), source['author'])


def main():
    feed_file = sys.argv[sys.argv.index('--feed-file') + 1] if '--feed-file' in sys.argv else None
    arts = json.load(open(ART, encoding='utf-8'))
    known = {norm(a['link']['de']) for a in arts} | {norm(a['link'].get('en') or '') for a in arts}
    KNOWN.update(known)
    ids = {a['id'] for a in arts}
    new, errors = [], []
    for s in json.load(open(SRC, encoding='utf-8'))['sources']:
        try:
            items = from_rss(s, feed_file) if s['type'] == 'rss' else from_cp7(s)
            for e in items:
                if norm(e['link']['de']) in known: continue
                while e['id'] in ids: e['id'] += '-2'
                known.add(norm(e['link']['de'])); ids.add(e['id']); new.append(e)
        except Exception as ex:  # eine kaputte Quelle soll die anderen nicht aufhalten
            errors.append(f"{s['id']}: {ex}")
    if new:
        json.dump(arts + new, open(ART, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    status = dict(neue_entwuerfe=len(new), fehler=errors, autoren_in_feeds={k: sorted(v) for k, v in SEEN.items()}, feeds=DIAG)
    json.dump(status, open(os.path.join(DATA, 'import-status.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for e in new:
        print(f"neu (Entwurf): {e['id']}  |  {e['src']}  |  {e['title']['de']}")
    for e in errors:
        print(f'Fehler: {e}', file=sys.stderr)
    print(f'{len(new)} neue Entwürfe, {len(errors)} Fehler')


if __name__ == '__main__':
    main()
