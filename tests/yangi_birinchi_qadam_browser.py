# Birinchi qadam: bo'sh Odat va bo'sh IELTS ekranlarida nol raqamlar o'rniga yo'l-yo'riq; Jilo'da eskisi. Soat: 2026-10-31 10:00.
import sys, os
sys.path.insert(0, os.environ.get('KT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tests')
from _pw import Run
with Run('birinchi_qadam') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    def go(fq, tab, habs=None, ie=None):
        ev("(a)=>{localStorage.removeItem('trk_fqd');if(a[0]!==null)uiS('trk_fqd',a[0]);S.hab=a[2]||[];if(a[3])Object.assign(S.ie,a[3]);else{S.ie.words=[];S.ie.mat=[];S.ie.ex='';S.ie.tests=[];S.ie.mock=[]}tab=a[1];IVW='b';render()}", [fq, tab, habs, ie]); pg.wait_for_timeout(150)
    txt = lambda: pg.inner_text('#app')
    # ---------- Odat ----------
    go(None, 'o'); t = txt()
    chk('Odat with no habits (default): "Birinchi qadam" card with ready-made habit suggestions', 'Birinchi qadam' in t and 'Suv ichish' in t and 'Kitob o‘qish' in t, t[:200])
    chk('...and the four zero statistics and the column controls are not shown', pg.evaluate("[...document.querySelectorAll('#app .hbsum')].every(e=>e.getBoundingClientRect().height===0)") and 'Mukammal kunlar' not in t.replace('\n', ' ') or pg.evaluate("document.querySelector('#app .hbsum').getBoundingClientRect().height")==0)
    pg.click('#app .fqd .chip >> text=Suv ichish'); pg.wait_for_timeout(150)
    h = ev("S.hab.map(x=>x.t+'|'+x.e)")
    chk('one tap adds the habit (with its emoji) and the card disappears', h == ['Suv ichish|💧'] and 'Birinchi qadam' not in txt(), h)
    chk('after the first habit the normal Odat screen is back: statistics visible, the habit is in the table', pg.evaluate("document.querySelector('#app .hbsum').getBoundingClientRect().height>0") and 'Suv ichish' in txt())
    ev("fqdAdd('💧','Suv ichish')"); chk('adding the same habit twice does not duplicate it', ev("S.hab.length") == 1)
    go(None, 'o', [{'id': 'h1', 't': 'Kitob'}]); chk('with a habit already there: no "Birinchi qadam" card', 'Birinchi qadam' not in txt())
    go('0', 'o'); t = txt()
    chk('"Yo‘q (avvalgidek)": the old empty Odat screen: zero statistics and the old hint, no card', 'Birinchi qadam' not in t and 'Hali odat yo‘q. Pastdan birinchi odatingni yoz.' in t and pg.evaluate("document.querySelector('#app .hbsum').getBoundingClientRect().height>0"))
    # ---------- IELTS ----------
    go(None, 'e'); t = txt()
    chk('IELTS Bosh with nothing entered: "IELTS: birinchi qadam" with 3 steps instead of the zero bars', 'IELTS: birinchi qadam' in t and '1. Birinchi maqolani qo‘sh' in t and '2. 5 ta so‘z o‘rgan' in t and '3. Kurs rejasini tuz' in t and 'Izchillik (14 kun)' not in t, t[:300])
    pg.click('#app .row >> text=Birinchi maqolani'); pg.wait_for_timeout(120)
    chk('step 1 opens Materiallar', ev("IVW") == 'a')
    go(None, 'e'); pg.click('#app .row >> text=5 ta so‘z'); pg.wait_for_timeout(120); chk('step 2 opens Lug‘at', ev("IVW") == 'l')
    go(None, 'e'); pg.click('#app .row >> text=Kurs rejasini'); pg.wait_for_timeout(120); chk('step 3 opens Kurs', ev("IVW") == 'y')
    go(None, 'e', None, {'ex': '2027-03-01'}); chk('as soon as an exam date is set the usual readiness card is shown', 'IELTS tayyorgarligi' in txt() and 'IELTS: birinchi qadam' not in txt())
    go('0', 'e'); chk('"Yo‘q (avvalgidek)": the old IELTS card with its zero bars', 'IELTS tayyorgarligi' in txt() and 'Izchillik (14 kun)' in txt())
    # ---------- Jilo ----------
    ev("()=>{uiS('trk_fqd','1');SDO={w_v:1,jl:1};tab='s';render()}"); pg.wait_for_timeout(100)
    chk('Jilo lists "Bo‘sh ekranlarda Birinchi qadam" with both options', ev("fqdJl().includes('Ko‘rinsin')") and 'Birinchi qadam' in txt())
    # ---------- uslublar ----------
    for cls, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        for tab in ('o', 'e'):
            ev("(a)=>{document.documentElement.className=a;dzApply()}", cls); go(None, tab)
            chk('%s style, tab %s: the card fits the phone width' % (nm, tab), pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    print('\n%d passed, %d failed' % (R.ok, R.bad))
