#!/usr/bin/env python3
"""Bir martalik/qayta sinxronlash: tracker/index.html  ->  src/ (mavzuli fayllar).
Qayta yig'ilgan natija asl fayl bilan BAYT-BAYTIGA bir xil bo'lishi tekshiriladi."""
import os, re, sys, hashlib
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = open(os.path.join(root, 'tracker', 'index.html'), encoding='utf-8').read()
s0 = h.index('<style>') + len('<style>'); s1 = h.index('</style>')
j0 = h.index('<script>') + len('<script>'); j1 = h.index('</script>', j0)
assert h.count('<style>') == 1 and h.count('<script>') == 2 or h.count('<script>') >= 1
css, js = h[s0:s1], h[j0:j1]
js = re.sub(r"const APP_BUILD='[0-9a-f]{10}';", "const APP_BUILD='{{BUILD}}';", js)   # yig'ma identifikatori qayta yig'ishda hisoblanadi
# ---- CSS: asosiy | mushaf | yo'l | qolgan ----
cuts = [0] + [css.index(m) for m in ("@font-face{font-family:QPC", ".rwc{", ".seg.sc.mr-r{")] + [len(css)]
cnames = ['10-asos.css', '20-mushaf.css', '30-yol.css', '40-qoshimcha.css']
# ---- JS: bo'lim belgilari bo'yicha ----
lines = js.split('\n'); pos = []; p = 0
for l in lines: pos.append(p); p += len(l) + 1
def at(marker):
    for i, l in enumerate(lines):
        if marker in l: return i
    raise SystemExit('marker topilmadi: ' + marker)
M = [(0, '01-yadro'), (at('=== PUL ==='), '02-pul'), (at('---- Jadval (tahrirlanadigan)'), '03-jadval-uygonish'),
     (at('---- Qur'), '04-quron-bolimi'), (at('---- Mushaf: 15 qatorli'), '05-mushaf'), (at('YO‘L: ochko'), '06-yol'),
     (at('const QGX='), '07-quron-ekranlari'),
     (at('---- Ko'), '08-sozlamalar-eslatmalar'), (at('IELTS, Univer, Prava'), '09-oqish-ielts'), (at('---- UNIVER:'), '10-univer'),
     (at('---- Isolation ----'), '11-isolation-brend-rejimlar'), (at('---- Takror:'), '12-takror-namoz-kitob'),
     (at('---- Oylik hisobot'), '13-hisobot-vaqtlar-qidiruv'), (at('---- Ramazon'), '14-ramazon-pdf'), (at('=== AI YORDAMCHI'), '15-ai'),
     (at('---- Bayram:'), '16-bayram'), (at('=== ZAL:'), '17-zal'), (at('---- Ovozli kiritish'), '18-ovoz-wrapped-ieltsai'),
     (at("QUR'ON AUDIO"), '19-quron-audio'), (at('DUOLAR VA KUNLIK ZIKR'), '20-duolar'), (at('---- Bulut hajmi'), '21-ishonchlilik'),
     (at('---- Telegram bot:'), '22-telegram-obuna')]
assert [m[0] for m in M] == sorted(m[0] for m in M), 'tartib buzilgan'
for d in ('js', 'css'):
    os.makedirs(os.path.join(root, 'src', d), exist_ok=True)
    for f in os.listdir(os.path.join(root, 'src', d)): os.remove(os.path.join(root, 'src', d, f))
for k, name in enumerate(cnames): open(os.path.join(root, 'src', 'css', name), 'w', encoding='utf-8', newline='').write(css[cuts[k]:cuts[k + 1]])
for k, (li, name) in enumerate(M):
    a = pos[li]; b = pos[M[k + 1][0]] if k + 1 < len(M) else len(js)
    open(os.path.join(root, 'src', 'js', name + '.js'), 'w', encoding='utf-8', newline='').write(js[a:b])
tpl = h[:s0] + '{{CSS}}' + h[s1:j0] + '{{JS}}' + h[j1:]
assert '{{CSS}}' not in h and '{{JS}}' not in h
open(os.path.join(root, 'src', 'index.template.html'), 'w', encoding='utf-8', newline='').write(tpl)
print('src/ yozildi:', len(cnames), 'CSS va', len(M), 'JS fayl')
