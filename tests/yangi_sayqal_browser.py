# Dizayn sayqali (html.pl): yoqilgan/avvalgidek, Odat'da telefon tugmalari, 3 uslub x yorug'/qorong'u, toshib ketmaslik. Soat: 2026-10-31 10:00.
import sys
import os
sys.path.insert(0, os.environ.get('KT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tests')
from _pw import Run
with Run('sayqal') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    def go(pl, tab='h', cls='', th='light'):
        ev("(a)=>{localStorage.removeItem('trk_pl');if(a[0]!==null)uiS('trk_pl',a[0]);setTh(a[3]);document.documentElement.className=a[2];dzApply();S.hab=[{id:'h1',t:'Suv'}];tab=a[1];PV='b';render()}", [pl, tab, cls, th]); pg.wait_for_timeout(120)
    st = lambda sel, prop: pg.evaluate("([s,p])=>{const e=document.querySelector(s);return e?getComputedStyle(e)[p]:null}", [sel, prop])
    go(None); chk('default (no saved choice): the polish is ON ("pl" class)', ev("document.documentElement.classList.contains('pl')"))
    on = {'nav': st('nav', 'backdropFilter') or st('nav', 'webkitBackdropFilter'), 'goal': st('#app .hero', 'boxShadow')}
    chk('polish ON: the bottom menu is frosted (backdrop blur) and the hero has a soft shadow', ('blur' in str(on['nav'])) and on['goal'] not in (None, 'none'), on)
    go('0'); off = {'nav': st('nav', 'backdropFilter'), 'goal': st('#app .hero', 'boxShadow')}
    chk('"Avvalgidek": the class is removed and the look is back to flat (no blur, no hero shadow)', (not ev("document.documentElement.classList.contains('pl')")) and off['nav'] in ('none', None) and off['goal'] in ('none', None), off)
    ev("()=>{uiS('trk_pl','1');SDO={dz:1,w_v:1};tab='s';render()}"); pg.wait_for_timeout(100)
    chk('Sozlamalar → Dizayn has "Sayqal" with Yoqilgan / Avvalgidek', 'Sayqal' in pg.inner_text('#app') and ev("plJl().includes('Avvalgidek')"))
    ev("dzSet('pl','0')"); chk('pressing "Avvalgidek" in Settings turns it off and saves the choice', ev("uiG('trk_pl')") == '0' and not ev("document.documentElement.classList.contains('pl')"))
    ev("dzSet('pl','1')"); chk('pressing "Yoqilgan" turns it back on', ev("document.documentElement.classList.contains('pl')"))
    # Odat: telefon tugmalari
    go('1', 'o'); vis = lambda: ev("[...document.querySelectorAll('#app .hbcol,#app .hbwide')].filter(e=>e.getBoundingClientRect().width>0).length")
    chk('Odat on a phone with polish: "Ustun / Tor / Keng" and "Keng ekran" are hidden, "Ixcham" stays', vis() == 0 and 'Ixcham' in pg.inner_text('#app') and 'Keng ekran' not in pg.inner_text('#app'))
    go('0', 'o'); chk('Odat with "Avvalgidek": all of them are shown again', vis() == 3 + 1 + 0 or vis() >= 4, vis())
    # uslublar x rejimlar x ekranlar
    for th in ('light', 'dark'):
        for cls, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
            bad = []
            for tab in ('h', 'q', 'o', 'm', 'e', 'p', 's'):
                go('1', tab, cls, th)
                if not pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(tab)
            chk('%s / %s with polish: no screen overflows sideways (Bugun, Qur\'on, Odat, Maqsad, O\'qish, Pul, Sozlamalar)' % (th, nm), not bad, bad)
    go('1', 'h', '', 'light'); chk('the bottom menu buttons are still big enough to tap (>= 44px tall)', ev("[...document.querySelectorAll('nav button')].every(b=>b.getBoundingClientRect().height>=44)"))
    chk('the main "Bajardim" button is at least 44px tall and visible', ev("(()=>{const b=[...document.querySelectorAll('#app button')].find(x=>x.textContent.trim()==='Bajardim');if(!b)return false;const r=b.getBoundingClientRect();return r.height>=44&&r.width>60})()"))
    print('\n%d passed, %d failed' % (R.ok, R.bad))
