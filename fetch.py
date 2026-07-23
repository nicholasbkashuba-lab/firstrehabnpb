import re, os, json, urllib.request, ssl

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,*/*'}
ctx = ssl.create_default_context()
for d in ('out/html', 'out/photos', 'out/bios'):
    os.makedirs(d, exist_ok=True)


def get(u, t=45):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t, context=ctx).read()


pages = {}


def try_page(key, u):
    try:
        h = get(u).decode('utf-8', 'ignore')
        pages[key] = h
        open('out/html/%s.html' % key, 'w', encoding='utf-8').write(h)
        print('OK', key, len(h), u)
        return True
    except Exception as e:
        print('FAIL', key, u, repr(e)[:140])
        return False


def archive_of(path):
    try:
        av = json.loads(get('https://archive.org/wayback/available?url=palmbeachneurology.com/%s' % path, 30).decode())
        return av.get('archived_snapshots', {}).get('closest', {}).get('url', '')
    except Exception as e:
        print('archfail', path, repr(e)[:140])
        return ''


slugs = ['winner', 'stone', 'dasilva', 'becker', 'coppola', 'korb', 'alosilla', 'sadowsky', 'zuniga']
for s in slugs:
    if not try_page(s + '.live', 'https://www.palmbeachneurology.com/about-%s' % s):
        snap = archive_of('about-%s' % s)
        if snap:
            try_page(s + '.arch', snap)
for nm, path in [('our-doctors', 'our-doctors'), ('home', '')]:
    if not try_page(nm + '.live', 'https://www.palmbeachneurology.com/%s' % path):
        snap = archive_of(path)
        if snap:
            try_page(nm + '.arch', snap)


def textify(h):
    h = re.sub(r'(?is)<script.*?</script>', ' ', h)
    h = re.sub(r'(?is)<style.*?</style>', ' ', h)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)).strip()


for k, h in pages.items():
    open('out/bios/%s.txt' % k, 'w', encoding='utf-8').write(textify(h)[:15000])


def origurl(u):
    u = u.replace('&amp;', '&')
    return re.split(r'/v1/', u)[0]


for k, h in pages.items():
    m = re.search(r'(?is)<meta[^>]+og:image[^>]+content=["\']([^"\']+)', h)
    if not m:
        m = re.search(r'(?is)content=["\']([^"\']+)["\'][^>]*og:image', h)
    if m:
        try:
            open('out/photos/OG-%s.jpg' % k, 'wb').write(get(origurl(m.group(1))))
            print('OG', k, m.group(1))
        except Exception as e:
            print('ogfail', k, repr(e)[:140])

allimg = []
for h in pages.values():
    allimg += re.findall(r'https://static\.wixstatic\.com/media/[A-Za-z0-9_~./%\-]+', h)
seen = []
for x in allimg:
    if x not in seen:
        seen.append(x)
for i, u in enumerate(seen[:60]):
    try:
        open('out/photos/img-%03d.jpg' % i, 'wb').write(get(origurl(u)))
        open('out/photos/img-%03d.url.txt' % i, 'w').write(origurl(u))
    except Exception as e:
        print('imgfail', i, repr(e)[:120])

print('SUMMARY pages=%d images=%d' % (len(pages), len(seen)))
