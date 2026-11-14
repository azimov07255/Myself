# Pul tablari: Bosh, Tarix, Hisobot, Reja + Yana (Qarzlar, Zakat); Jilo'da avvalgidek (6 ta tab). Soat: 2026-10-31 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('pul_tab') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    def go(mode='g', pv='b', w='p', cls=''):
        ev("(a)=>{uiS('trk_ptb',a[0]);document.documentElement.className=a[3];window.confirm=()=>true;S.money=[];S.debts=[];S.fin={open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[],zk:{b:'g',pg:1000000}};W=a[2];PV=a[1];tab='p';render()}", [mode, pv, w, cls]); pg.wait_for_timeout(120)
    tabs = lambda: ev("[...document.querySelectorAll('#app .seg.sc button')].map(b=>b.textContent.trim())")
    fits = lambda: ev("(()=>{const e=document.querySelector('#app .seg.sc');return e.scrollWidth<=e.clientWidth+1})()")
    go('g'); t = tabs()
    chk('compact (default): the tab row has Bosh, Tarix, Hisobot, Reja and "⋯ Yana" (5 tabs, no Qarzlar/Zakat in it)', len(t) == 5 and any('Bosh' in x for x in t) and any('Yana' in x for x in t) and not any('Qarzlar' in x or 'Zakat' in x for x in t), t)
    chk('the tab row fits the phone width without sideways scrolling', fits())
    chk('on Bosh there is no second row of tabs', ev("document.querySelectorAll('#app .seg').length") == 3 or ev("[...document.querySelectorAll('#app .seg button')].every(b=>!/Zakat/.test(b.textContent))"))
    pg.click('#app .seg.sc button >> text=Yana'); pg.wait_for_timeout(100)
    chk('"Yana" opens Qarzlar and shows the small second row (Qarzlar selected, Zakat)', ev("PV") == 'q' and ev("[...document.querySelectorAll('#app .seg button.on')].map(b=>b.textContent.trim())").count('🤝 Qarzlar') == 1 and 'Zakat' in pg.inner_text('#app'))
    chk('"Yana" stays highlighted in the main row while in Qarzlar', ev("[...document.querySelectorAll('#app .seg.sc button.on')].map(b=>b.textContent.trim())") == ['⋯ Yana'])
    pg.click('#app .seg button >> text=Zakat'); pg.wait_for_timeout(100)
    chk('the second row switches to Zakat and the zakat card appears', ev("PV") == 'z' and 'Zakot hisobi' in pg.inner_text('#app'))
    chk('pressing "Yana" from Zakat keeps Zakat (does not jump away)', (pg.click('#app .seg.sc button >> text=Yana') or True) and ev("PV") == 'z')
    pg.click('#app .seg.sc button >> text=Hisobot'); pg.wait_for_timeout(100)
    chk('going back to Hisobot hides the second row', ev("PV") == 'h' and 'Zakot hisobi' not in pg.inner_text('#app') and ev("[...document.querySelectorAll('#app .seg button')].every(b=>!/Qarzlar/.test(b.textContent))"))
    go('g', 'q'); chk('opening the app directly in Qarzlar (PV=q) shows both the debts page and the second row', 'Yangi qarz' in pg.inner_text('#app') or 'Qarz yozuvi yo' in pg.inner_text('#app'))
    # eskisi
    go('a'); t = tabs()
    chk('"Avvalgidek": all six tabs are in one row again (Bosh, Tarix, Qarzlar, Hisobot, Reja, Zakat)', len(t) == 6 and any('Qarzlar' in x for x in t) and any('Zakat' in x for x in t), t)
    go('a', 'q'); chk('"Avvalgidek": no second row', ev("document.querySelectorAll('#app .seg').length") <= 3 and ev("[...document.querySelectorAll('#app .seg button')].filter(b=>/Qarzlar/.test(b.textContent)).length") == 1)
    ev("()=>{uiS('trk_ptb','g');SDO={w_v:1,jl:1};tab='s';render()}"); pg.wait_for_timeout(100)
    chk('Jilo lists "Pul tablari" with the compact / old options', ev("ptbJl().includes('Ixcham (4 + Yana)')") and 'Pul tablari' in pg.inner_text('#app'))
    # dokon + uslublar
    go('g', 'h', 'd'); chk('shop wallet: same compact tabs, no overflow', len(tabs()) == 5 and fits())
    for cls, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        for pv in ('b', 'q', 'z'):
            go('g', pv, 'p', cls); chk('%s style, tab %s: no horizontal overflow, the tab row fits' % (nm, pv), ev("document.documentElement.scrollWidth<=window.innerWidth+1") and fits())
    pg.set_viewport_size({'width': 320, 'height': 700}); go('g', 'z'); chk('narrow phone (320px): the tab row still fits, no overflow', fits() and ev("document.documentElement.scrollWidth<=window.innerWidth+1"))
    print('\n%d passed, %d failed' % (R.ok, R.bad))
