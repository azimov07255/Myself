# Azimov uslubi (ui4): sozlamadan tanlanadi, qorong'i/yorug' rang, kontrast, hamma asosiy ekranlar toshib ketmaydi, klassik o'zgarmaydi. Soat: 2026-11-21 (shanba) 10:00.
import sys, os
sys.path.insert(0, os.environ.get('KT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tests')
from _pw import Run
def lum(h):
    h = h.strip().lstrip('#'); h = ''.join(c * 2 for c in h) if len(h) == 3 else h
    r = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]; r = [c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4 for c in r]
    return .2126 * r[0] + .7152 * r[1] + .0722 * r[2]
def cr(a, b):
    x, y = lum(a), lum(b); x, y = max(x, y), min(x, y); return (x + .05) / (y + .05)
with Run('azimov', when=(2026, 11, 21, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-11-21T10:00:00')
    ev("()=>{window.toast=()=>{};localStorage.removeItem('trk_3d');S.fin={open:{p:{cash:1600000,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[],wr:[]};S.money=[];tab='s';render()}"); pg.wait_for_timeout(120)
    cls = lambda: ev("['ui2','glass','az'].map(c=>document.documentElement.classList.contains(c))")
    chk('default is Klassik: no new-style classes', cls() == [False, False, False])
    ev("dzSet('ui','4')"); pg.wait_for_timeout(100)
    chk('Azimov sets ui2 + az (it builds on the new design), not glass; it is saved on this device', cls() == [True, False, True] and ev("uiG('trk_ui')") == '4')
    chk('the Sozlamalar style row shows 4 cards and the Azimov one is selected', ev("[...document.querySelectorAll('.dzp')].map(b=>b.classList.contains('on'))") == [False, False, False, True])
    # ---------- ranglar ----------
    g = lambda th: ev("(t)=>{const d=document.documentElement;d.dataset.theme=t;const c=getComputedStyle(d),v=k=>c.getPropertyValue(k).trim();return {tx:v('--tx'),bg:v('--bg'),c1:v('--c1'),mu:v('--mu'),ac:v('--ac'),go:v('--go'),onac:v('--on-ac'),htx:v('--htx'),hbg:v('--hbg')}}", th)
    d, l = g('dark'), g('light')
    chk('dark = Azimov navy (#0a0c16 background), light = IELTS lavender (#f4f2ff)', d['bg'] == '#0a0c16' and l['bg'] == '#f4f2ff', (d['bg'], l['bg']))
    fails = []
    for nm, v in (('dark', d), ('light', l)):
        for n, a, b, mn in (('text/page', v['tx'], v['bg'], 7), ('text/card', v['tx'], v['c1'], 7), ('muted/card', v['mu'], v['c1'], 4.5), ('accent as text on card', v['ac'], v['c1'], 3)):
            r = cr(a, b)
            if r < mn: fails.append('%s %s %.2f<%s' % (nm, n, r, mn))
    chk('text, muted text and accent colours keep their contrast in both themes', not fails, fails)
    bt = ev("(()=>{const d=document.documentElement;d.dataset.theme='dark';return getComputedStyle(d).getPropertyValue('--az-g')})()")
    stops = [x for x in __import__('re').findall(r'#[0-9a-fA-F]{6}', bt)]
    chk('white labels on the gradient buttons stay readable at every stop (≥3:1, large bold text)', stops and all(cr('#ffffff', c) >= 3 for c in stops), [(c, round(cr('#ffffff', c), 2)) for c in stops])
    ev("document.documentElement.dataset.theme='light'")
    # ---------- ekranlar toshib ketmaydi ----------
    shots = []
    for th in ('dark', 'light'):
        ev("(t)=>{document.documentElement.dataset.theme=t}", th)
        for nm, js in (('Bugun', "()=>{tab='h';BV='m';render()}"), ('Pul Bosh', "()=>{tab='p';W='p';PV='b';render()}"), ('Pul Hisobot', "()=>{tab='p';PV='h';render()}"), ('Pul Biznes', "()=>{tab='p';PV='x';render()}"), ('Sozlamalar', "()=>{tab='s';render()}"), ('Qur\'on', "()=>{tab='q';render()}")):
            ev(js); pg.wait_for_timeout(120)
            ok = pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")
            hero = pg.evaluate("(()=>{const e=document.querySelector('#app .hero');return e?getComputedStyle(e).backgroundImage.includes('gradient'):true})()")
            if not (ok and hero): shots.append('%s/%s overflow=%s hero=%s' % (th, nm, not ok, hero))
    chk('Bugun, Pul (3 tabs), Sozlamalar, Qur\'on: no horizontal overflow and the hero is a gradient (dark and light)', not shots, shots)
    ev("document.documentElement.dataset.theme='dark'; tab='h'; render()"); pg.wait_for_timeout(100)
    chk('the bottom bar centre button is the gradient rounded square', ev("(()=>{const e=document.querySelector('.navai');if(!e)return true;const s=getComputedStyle(e);return s.backgroundImage.includes('gradient')&&parseFloat(s.borderRadius)<28})()"))
    # ---------- qaytish ----------
    ev("dzSet('ui','2')"); chk('switching to Yangi drops the az class (the old look is one tap away)', cls() == [True, False, False])
    ev("dzSet('ui','1')"); pg.wait_for_timeout(80); chk('Klassik is restored exactly: no ui2/glass/az and nothing else changed', cls() == [False, False, False] and ev("S.fin.open.p.cash") == 1600000)
    print('\n%d passed, %d failed' % (R.ok, R.bad))
