# Dizayn: Klassik (standart) va Yangi uslub almashtirish, rang, matn o'lchami, animatsiya, kontrast, gorizontal toshib ketmaslik.
import sys, json
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
def lum(h):
    h = h.lstrip('#'); h = ''.join(c * 2 for c in h) if len(h) == 3 else h; r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def cr(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb) + .05) / (min(la, lb) + .05)
with Run('dizayn', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("()=>{localStorage.clear();localStorage.setItem('trk_bg','o');dzApply();document.documentElement.dataset.theme='light';S.hab=[{id:'h1',t:'Kitob'}];tab='s';render()}"); pg.wait_for_timeout(150)
    H = lambda: ev("document.documentElement.classList.contains('ui2')")
    chk('the CLASSIC look is the default: the new-design class is not set and the accent defaults to "zumrad"', H() is False and ev("document.documentElement.dataset.acc") == 'zumrad')
    ev("document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('Dizayn'))d.open=true})"); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('Sozlama has "🎨 Dizayn" with THREE different style cards (Klassik, Yangi, Liquid Glass), colour choices, text size and animations', 'Dizayn' in t and ev("[...document.querySelectorAll('.dzp b')].map(b=>b.textContent)") == ['Klassik', 'Yangi', 'Liquid Glass'] and ev("document.querySelectorAll('#app details .rwch .chip').length") >= 6 and all(s in t for s in ['Matn o‘lchami', 'Animatsiyalar', 'Kichik', 'Juda katta']))
    chk('Klassik is shown as selected', ev("[...document.querySelectorAll('.dzp')].map(b=>b.classList.contains('on'))") == [True, False, False])
    ev("()=>{tab='h';BV='m';render()}"); pg.wait_for_timeout(100)
    cl = ev("(()=>{const h=document.querySelector('#app .hero'),n=document.querySelector('nav div');return [getComputedStyle(h).borderRadius,getComputedStyle(n).borderRadius,getComputedStyle(document.querySelector('nav')).borderTopWidth]})()")
    S0 = ev("JSON.stringify(S)"); chk('classic computed look (hero 24 px radius, flat full-width bottom bar with a top border)', cl[0] == '24px' and cl[1] in ('0px', '') and cl[2] == '1px', cl)
    ev("dzSet('ui','2')"); pg.wait_for_timeout(120)
    nw = ev("(()=>{const h=document.querySelector('#app .hero'),n=document.querySelector('nav div');return [getComputedStyle(h).borderRadius,getComputedStyle(n).borderRadius,getComputedStyle(document.querySelector('nav')).borderTopWidth,getComputedStyle(n).position]})()")
    chk('switching to Yangi sets the class, saves it on this device and changes the look (hero 28 px, floating rounded glass bar without the old top border)', H() and ev("uiG('trk_ui')") == '2' and nw[0] == '28px' and nw[1] == '28px' and nw[2] == '0px', nw)
    chk('the switch never touches the user\u2019s data', ev("JSON.stringify(S)") == S0)
    ev("document.documentElement.classList.remove('ui2');dzApply()"); chk('after an app restart (re-applying the saved choice) the new style is back', H())
    ev("dzSet('ui','1')"); pg.wait_for_timeout(100)
    cl2 = ev("(()=>{const h=document.querySelector('#app .hero'),n=document.querySelector('nav div');return [getComputedStyle(h).borderRadius,getComputedStyle(n).borderRadius,getComputedStyle(document.querySelector('nav')).borderTopWidth]})()")
    chk('switching back to Klassik restores exactly the old look', H() is False and cl2 == cl, cl2)
    # ---------- rang ----------
    css = lambda: ev("getComputedStyle(document.documentElement).getPropertyValue('--ac').trim()")
    ev("dzSet('acc','kok')"); chk('in Klassik the accent choice changes nothing (the original green stays)', css() == '#17604a' and ev("document.documentElement.dataset.acc") == 'kok')
    ev("dzSet('ui','2')"); chk('in Yangi + light theme the "kok" accent is #1f5fbf', css() == '#1f5fbf', css())
    ev("document.documentElement.dataset.theme='dark'"); chk('...and the dark variant is lighter (#62a5f5)', css() == '#62a5f5', css()); ev("document.documentElement.dataset.theme='light'")
    # ---------- kontrast: har bir rang x rejim ----------
    rows, fails = [], []
    for th in ('light', 'dark'):
        for acc, *_ in [('zumrad',), ('kok',), ('binafsha',), ('atirgul',), ('oltin',), ('grafit',)]:
            v = ev("(a)=>{const d=document.documentElement;d.dataset.theme=a[0];d.dataset.acc=a[1];const g=k=>getComputedStyle(d).getPropertyValue(k).trim();return {tx:g('--tx'),bg:g('--bg'),c1:g('--c1'),mu:g('--mu'),ac:g('--ac'),go:g('--go'),onac:g('--on-ac'),ongo:g('--on-go'),hbg:g('--hbg'),htx:g('--htx')}}", [th, acc])
            ch = [('text on page', cr(v['tx'], v['bg']), 7), ('text on card', cr(v['tx'], v['c1']), 7), ('muted text on card', cr(v['mu'], v['c1']), 4.5), ('accent button label', cr(v['onac'], v['ac']), 4.5), ('CTA button label', cr(v['ongo'], v['go']), 4.5), ('hero text on hero', cr(v['htx'], v['hbg']), 4.5), ('accent as text on card', cr(v['ac'], v['c1']), 3)]
            for n, r, mn in ch:
                if r < mn: fails.append('%s/%s %s %.2f<%.1f' % (th, acc, n, r, mn))
    chk('colour contrast (WCAG) holds in all 12 theme x accent combinations: text 7:1, muted text 4.5:1, button labels 4.5:1, hero text 4.5:1, accent text 3:1', not fails, fails[:8])
    ev("document.documentElement.dataset.acc='zumrad';document.documentElement.dataset.theme='light'")
    # ---------- matn o'lchami va animatsiya ----------
    z = lambda: ev("getComputedStyle(document.getElementById('app')).zoom")
    ev("dzSet('fs','l')"); a = z(); ev("dzSet('fs','xl')"); b = z(); ev("dzSet('fs','s')"); c = z(); ev("dzSet('fs','m')"); d_ = z()
    chk('text size works through the app: Kichik 0.94, Katta 1.08, Juda katta 1.16, O‘rta 1', (a, b, c, d_) == ('1.08', '1.16', '0.94', '1'), (a, b, c, d_))
    ev("dzSet('ui','1')"); ev("dzSet('fs','l')"); chk('text size also works in the Klassik style', z() == '1.08'); ev("dzSet('fs','m')"); ev("dzSet('ui','2')")
    ev("dzSet('mo','0')"); chk('"Animatsiyalar: O‘chirilgan" switches every transition and animation off', ev("document.documentElement.dataset.mo") == 'off' and ev("getComputedStyle(document.querySelector('nav button')).transitionDuration") == '0s'); ev("dzSet('mo','1')"); chk('...and back on', ev("document.documentElement.dataset.mo") == 'on')
    # ---------- hech narsa toshib ketmaydi ----------
    SC = [("Bugun", "tab='h';BV='m'"), ("Odatlar", "tab='o';OT='j'"), ("Uyqu", "tab='o';OT='u'"), ("Qur'on", "tab='q';QT='y'"), ("Maqsad", "tab='m'"), ("IELTS", "tab='e';EV='i';IVW='b'"), ("Mashq", "tab='e';EV='i';IVW='m'"), ("Pul", "tab='p';PV='b'"), ("Pul reja", "tab='p';PV='r'"), ("Sozlama", "tab='s'")]
    bad = []
    for th in ('light', 'dark'):
        ev("(t)=>{document.documentElement.dataset.theme=t}", th)
        for n, s in SC:
            ev("()=>{%s;render()}" % s); pg.wait_for_timeout(60)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(th + ':' + n)
    chk('in the new style no main screen scrolls sideways on a phone (10 screens, light and dark)', not bad, bad)
    # ---------- LIQUID GLASS ----------
    ev("dzSet('ui','3')"); pg.wait_for_timeout(100)
    cls = lambda: ev("[document.documentElement.classList.contains('ui2'),document.documentElement.classList.contains('glass')]")
    chk('Liquid Glass sets both classes (it builds on the new style), is saved on this device and survives a restart', cls() == [True, True] and ev("uiG('trk_ui')") == '3' and ev("(()=>{document.documentElement.classList.remove('ui2','glass');dzApply();return document.documentElement.classList.contains('glass')})()"))
    ev("()=>{tab='h';BV='m';render()}"); pg.wait_for_timeout(100)
    bf = ev("(()=>{const g=document.querySelector('#app .goal')||document.querySelector('#app .sum div'),n=document.querySelector('nav div');return [getComputedStyle(n).backdropFilter||getComputedStyle(n).webkitBackdropFilter,getComputedStyle(n).borderRadius,getComputedStyle(document.querySelector('#app .hero')).borderRadius]})()")
    chk('the bottom bar is frosted glass (backdrop blur), more rounded than in Yangi; the hero card has a 34 px radius', 'blur' in bf[0] and bf[1] == '36px' and bf[2] == '34px', bf)
    ev("dzSet('ui','2')"); bf2 = ev("getComputedStyle(document.querySelector('nav div')).backdropFilter"); ev("dzSet('ui','1')"); bf1 = ev("getComputedStyle(document.querySelector('nav div')).backdropFilter||'none'")
    chk('Yangi keeps its lighter blur (not the glass one) and Klassik has no blur at all', cls() == [False, False] and bf1 in ('none', '') and 'blur(22px)' in bf2.replace(' ', '') or (bf1 in ('none', '') and 'blur' in bf2), (bf1, bf2))
    ev("dzSet('ui','3')")
    gl = lambda v: (ev("(v)=>{dzSet('gl',v);return getComputedStyle(document.documentElement).getPropertyValue('--gl-b').trim()}", v))
    chk('"Shisha kuchi" changes the blur: Yengil 10 px, O‘rta 22 px, Kuchli 34 px', (gl('s'), gl('m'), gl('h')) == ('10px', '22px', '34px'))
    ev("()=>{tab='s';render();document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('Dizayn'))d.open=true})}"); pg.wait_for_timeout(80)
    chk('the "Shisha kuchi" row is shown only while Liquid Glass is selected', 'Shisha kuchi' in pg.inner_text('#app') and ev("[...document.querySelectorAll('.dzp')].map(b=>b.classList.contains('on'))") == [False, False, True])
    ev("dzSet('ui','2')"); pg.wait_for_timeout(60); chk('...and hidden in Yangi', 'Shisha kuchi' not in pg.inner_text('#app')); ev("dzSet('ui','3')")
    # shisha ustida matn o'qilishi: eng yomon holat (aksent dog'i ustidagi shisha)
    mix = lambda c1, a, c2: [round(a * x + (1 - a) * y) for x, y in zip(c1, c2)]
    hx = lambda h: (lambda h: [int(h[i:i + 2], 16) for i in (0, 2, 4)])(''.join(c * 2 for c in h.lstrip('#')) if len(h.lstrip('#')) == 3 else h.lstrip('#'))
    fails, worst = [], 99
    for th in ('light', 'dark'):
        for acc in ('zumrad', 'kok', 'binafsha', 'atirgul', 'oltin', 'grafit'):
            for st in ('s', 'm', 'h'):
                v = ev("(a)=>{const d=document.documentElement;d.dataset.theme=a[0];d.dataset.acc=a[1];d.dataset.gl=a[2];const g=k=>getComputedStyle(d).getPropertyValue(k).trim();return {tx:g('--tx'),mu:g('--mu'),bg:g('--bg'),ac:g('--ac'),w:parseFloat(g('--gl-w')),wd:parseFloat(g('--gl-wd')),ba:parseFloat(g('--gl-ba')),bad:parseFloat(g('--gl-bad'))}}", [th, acc, st])
                aw, ab = (v['w'], v['ba']) if th == 'light' else (v['wd'], v['bad'])
                base = mix(hx(v['ac']), ab, hx(v['bg'])); card = mix([255, 255, 255], aw, base); chex = '#%02x%02x%02x' % tuple(card)
                for nm, col, mn in (('text', v['tx'], 4.5), ('muted', v['mu'], 3.0)):
                    r = cr(col, chex); worst = min(worst, r) if nm == 'text' else worst
                    if r < mn: fails.append('%s/%s/%s %s %.2f' % (th, acc, st, nm, r))
    chk('text on a glass card stays readable even in the worst case (card over the strongest accent blob): text at least 4.5:1, muted 3:1, in 36 theme x colour x strength combinations', not fails, (fails[:6], round(worst, 2)))
    ev("()=>{document.documentElement.dataset.acc='zumrad';document.documentElement.dataset.gl='m';document.documentElement.dataset.theme='light'}")
    import re as _re
    css = open('/mnt/user-data/outputs/src/css/91-glass.css', encoding='utf-8').read()
    chk('safety nets exist: reduced-transparency setting and browsers without backdrop-filter fall back to solid cards', '@media(prefers-reduced-transparency:reduce)' in css and '@supports not ((backdrop-filter:blur(1px))' in css)
    bad = []
    for th in ('light', 'dark'):
        ev("(t)=>{document.documentElement.dataset.theme=t}", th)
        for n, sc in SC:
            ev("()=>{%s;render()}" % sc); pg.wait_for_timeout(50)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(th + ':' + n)
    chk('in Liquid Glass no main screen scrolls sideways on a phone (10 screens, light and dark)', not bad, bad)
    ev("dzSet('ui','1')"); ev("document.documentElement.dataset.theme='light'")
    chk('back to Klassik: no new-design class is left', cls() == [False, False])
