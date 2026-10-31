#!/usr/bin/env python3
"""Liest alle NEG-Beiträge ab einem Datum über die WordPress-API (Fallback: RSS-Seiten) und schreibt scan/neg-archive.json."""
import html, json, os, re, sys, urllib.request

BASE = 'https://theninerempiregermany.de'
AFTER = sys.argv[1] if len(sys.argv) > 1 else '2024-11-01'
UA = {'User-Agent': 'NinersFaithfulEurope-Import/1.0 (+https://cpracher-cloud.github.io/niners-faithful-europe/)'}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def plain(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s or ''))).strip()


out, cats, err = [], {}, None
try:
    page = 1
    while True:
        rows = json.loads(get(f'{BASE}/wp-json/wp/v2/posts?per_page=100&page={page}&after={AFTER}T00:00:00&_fields=id,date,link,title,excerpt,categories,tags,author'))
        if not rows: break
        out += rows; page += 1
        if len(rows) < 100: break
    for c in json.loads(get(f'{BASE}/wp-json/wp/v2/categories?per_page=100&_fields=id,name')):
        cats[c['id']] = c['name']
except Exception as ex:
    err = f'API: {ex}'
items = [dict(date=r['date'][:10], link=r['link'], title=plain(r['title']['rendered']), excerpt=plain(r['excerpt']['rendered'])[:400],
              categories=[cats.get(c, c) for c in r.get('categories', [])], author=r.get('author')) for r in out]
os.makedirs('scan', exist_ok=True)
json.dump(dict(after=AFTER, count=len(items), error=err, items=items), open('scan/neg-archive.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(items), err)
