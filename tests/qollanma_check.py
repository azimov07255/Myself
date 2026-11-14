import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Qo'llanma sahifasi: mazmun to'liqligi, rasmlar ichiga joylangan, tashqi so'rov yo'q, belgilar saqlanadi, zip va ilova havolasi.
import sys, re, zipfile, os, base64
sys.path.insert(0, (ROOT + '/tools/guide'))
from content import SL
from playwright.sync_api import sync_playwright
OUT = ROOT; ok = bad = 0
def chk(l, c, d=''):
    global ok, bad
    if c: ok += 1; print('PASS', l)
    else: bad += 1; print('FAIL', l, d)
h = open(OUT + '/tracker/qollanma.html', encoding='utf-8').read()
chk('the guide page exists and stays under 3 MB', 0 < len(h.encode()) < 3 * 1024 * 1024, len(h) // 1024)
miss = [s[2] for s in SL[2:] if s[2].replace('&', '&amp;') not in h and s[2] not in h]
chk('every slide of the video has its section in the page (same titles)', not miss, miss)
chk('all %d screenshots are embedded as images (no separate files)' % sum(1 for s in SL if s[0]), h.count('data:image/jpeg;base64,') == sum(1 for s in SL if s[0]))
ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', h)
chk('no external resources: the page works offline and sends no requests', not ext, ext)
bs = re.findall(r'base64,([A-Za-z0-9+/=]+)', h)
chk('the embedded images are real JPEGs', all(base64.b64decode(b)[:3] == b'\xff\xd8\xff' for b in bs))
chk('the page has the first-day checklist with 9 items and the parts navigation', h.count('type="checkbox"') == len(SL[1][4]) == 9 and 'id="p1"' in h and 'id="p6"' in h)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); reqs = []; pg.on('request', lambda r: reqs.append(r.url))
    pg.goto('file://' + OUT + '/tracker/qollanma.html'); pg.wait_for_timeout(300)
    chk('the page opens without errors and loads nothing from the network', not errs and all(u.startswith(('file:', 'data:')) for u in reqs), (errs, reqs[:3]))
    pg.click('.chk label >> nth=2'); pg.reload(); pg.wait_for_timeout(200)
    chk('a ticked checklist item is remembered after reload', pg.evaluate("document.querySelectorAll('.chk input')[2].checked") is True and pg.evaluate("document.querySelectorAll('.chk input:checked').length") == 1)
    chk('on a phone nothing overflows sideways', pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    b.close()
z = zipfile.ZipFile(OUT + '/mushaf-yuklash.zip'); chk('the main zip ships qollanma.html next to index.html', 'qollanma.html' in z.namelist() and 'index.html' in z.namelist())
app = open(OUT + '/tracker/index.html', encoding='utf-8').read(); chk('Sozlama → Yangiliklar links to the guide', 'href="qollanma.html"' in app and 'Rasmli to‘liq qo‘llanma' in app)
print('%d passed, %d failed' % (ok, bad))
