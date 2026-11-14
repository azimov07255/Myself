# -*- coding: utf-8 -*-
import sys, io, base64, html, os
sys.path.insert(0, '/tmp/guide')
from content import SL
from PIL import Image
E = html.escape
def img(k):
    im = Image.open('/tmp/guide/shots/%s.png' % k).convert('RGB').resize((390, 844), Image.LANCZOS); b = io.BytesIO(); im.save(b, 'JPEG', quality=70, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
parts = []; seen = {}
for i, S in enumerate(SL):
    if S[1] not in seen: seen[S[1]] = 'p%d' % len(seen); parts.append((seen[S[1]], S[1]))
check = SL[1][4]
out = ['''<!doctype html><html lang="uz"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kunlik tizim: to‘liq qo‘llanma</title><style>
:root{--bg:#f7f3ea;--c:#fffdf8;--tx:#1d2a24;--mu:#5d6b64;--go:#1f5a4a;--ac:#e07a3f;--ln:#e5dfd0}
@media(prefers-color-scheme:dark){:root{--bg:#0e1a16;--c:#14251f;--tx:#efeadc;--mu:#a9b8b0;--go:#4fbf8b;--ac:#f08a4b;--ln:#24382f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header,main,footer{max-width:860px;margin:0 auto;padding:0 16px}header{padding-top:28px}h1{font-size:30px;margin:0 0 6px}h2.part{margin:34px 0 10px;padding-top:6px;color:var(--ac);font-size:15px;letter-spacing:.06em}
.lead{color:var(--mu);margin:0 0 14px}nav.toc{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}nav.toc a{padding:8px 12px;border:1px solid var(--ln);border-radius:999px;color:var(--tx);text-decoration:none;font-size:14px;background:var(--c)}
.card{background:var(--c);border:1px solid var(--ln);border-radius:18px;padding:16px;margin:12px 0}.card h3{margin:0 0 4px;font-size:21px}.where{color:var(--ac);font-weight:700;margin:0 0 10px;font-size:15px}
.row{display:flex;gap:18px;align-items:flex-start}.row img{width:230px;max-width:42%;border-radius:18px;border:1px solid var(--ln);flex:0 0 auto}
ol{margin:0;padding-left:22px}li{margin:0 0 8px}.tip{margin-top:12px;padding:10px 12px;border-left:4px solid var(--ac);background:rgba(224,122,63,.1);border-radius:0 10px 10px 0;font-size:15px}
.chk label{display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-bottom:1px solid var(--ln);cursor:pointer}.chk input{margin-top:5px;width:18px;height:18px}
.note{font-size:14px;color:var(--mu)}footer{padding:24px 16px 50px;color:var(--mu);font-size:14px}
@media(max-width:560px){.row{flex-direction:column}.row img{width:100%;max-width:300px;align-self:center}}</style></head><body>
<header><h1>Kunlik tizim: to‘liq qo‘llanma</h1><p class="lead">Ilovaning hamma bo‘limi, nimani qayerga yozish va kunlik tartib. Rasmlar namuna ma‘lumot bilan olingan.</p>
<p class="note">Bu sahifaning videosi ham bor: <b>qollanma-video.mp4</b> (ovozsiz, matnli, taxminan 11 daqiqa).</p><nav class="toc">''']
for pid, name in parts: out.append('<a href="#%s">%s</a>' % (pid, E(name.split(' · ')[0] if ' · ' in name else name)))
out.append('</nav></header><main>')
out.append('<h2 class="part" id="boshla">BIRINCHI KUN: NIMALARNI QILISH KERAK (belgilab bor)</h2><div class="card chk"><div class="where">Har bandni bajargach belgila. Belgilar shu qurilmada saqlanadi.</div>')
for n, t in enumerate(check): out.append('<label><input type="checkbox" data-k="c%d"><span>%s</span></label>' % (n, E(t)))
out.append('</div>')
cur = None
for i, (k, part, title, where, steps, tip) in enumerate(SL):
    if i in (0, 1): continue
    if part != cur:
        cur = part; out.append('<h2 class="part" id="%s">%s</h2>' % (seen[part], E(part)))
    out.append('<section class="card"><h3>%s</h3>' % E(title))
    if where: out.append('<p class="where">Qayerda: %s</p>' % E(where))
    body = '<ol>' + ''.join('<li>%s</li>' % E(s) for s in steps) + '</ol>' if k else '<ul>' + ''.join('<li>%s</li>' % E(s) for s in steps) + '</ul>'
    if k: out.append('<div class="row"><img loading="lazy" alt="%s" src="%s"><div>%s%s</div></div>' % (E(title), img(k), body, '<div class="tip"><b>Maslahat:</b> %s</div>' % E(tip) if tip else ''))
    else: out.append(body)
    out.append('</section>')
out.append('</main><footer>Kunlik tizim qo‘llanmasi. Yangi funksiyalar ro‘yxati ilovaning o‘zida: Sozlama → Yangiliklar va qo‘llanma.</footer>')
out.append('<script>try{document.querySelectorAll(".chk input").forEach(function(c){var k="qg_"+c.dataset.k;c.checked=localStorage.getItem(k)==="1";c.onchange=function(){localStorage.setItem(k,c.checked?"1":"0")}})}catch(e){}</script></body></html>')
open('/tmp/guide/qollanma.html', 'w', encoding='utf-8').write(''.join(out))
print('html KB', round(os.path.getsize('/tmp/guide/qollanma.html') / 1024), 'images', sum(1 for s in SL if s[0]))
