import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Bugun tepasi: ixtiyoriy ixcham ko'rinish (salomlashish, doira, hafta chizig'i, shior). Soat: 2026-10-31 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('bugun_tepa') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    def go(cls=''):
        ev("(c)=>{['trk_btc','trk_bqt'].forEach(k=>localStorage.removeItem(k));document.documentElement.className=c;tab='h';BV='j';dzApply();render()}", cls); pg.wait_for_timeout(150)
    def M():
        return pg.evaluate("""()=>{const q=s=>document.querySelector(s),r=e=>e?e.getBoundingClientRect():null,h=q('#app .top h1.gr'),qt=q('#app .top .qt'),sv=q('#app .top svg'),hero=q('#app .hero'),wd=q('#app .wk .wd');
          return {cls:document.documentElement.className,gr:h?parseFloat(getComputedStyle(h).fontSize):0,qtShown:!!qt&&getComputedStyle(qt).display!=='none',qtH:qt?r(qt).height:0,qtFs:qt?parseFloat(getComputedStyle(qt).fontSize):0,svg:sv?r(sv).width:0,heroTop:hero?r(hero).top:0,wdH:wd?r(wd).height:0,ow:document.documentElement.scrollWidth<=window.innerWidth+1,
          btn:(()=>{const b=[...document.querySelectorAll('#app button')].find(x=>x.textContent.trim()==='Bajardim');return b?r(b).bottom:0})()}}""")
    go(); d = M()
    chk('default is the old look: no "btc" class, greeting 28px, quote visible, ring 64px', 'btc' not in d['cls'] and d['gr'] >= 28 and d['qtShown'] and d['svg'] >= 60, d)
    ev("bmOpt('btc','1')"); pg.wait_for_timeout(150); c = M()
    chk('compact: "btc" class is on', 'btc' in c['cls'], c)
    chk('compact: greeting 20px, ring 44px, week strip cells are shorter', c['gr'] == 20 and abs(c['svg'] - 44) < 1 and c['wdH'] < d['wdH'] - 15, (c['gr'], c['svg'], c['wdH'], d['wdH']))
    chk('compact: the quote is still shown, small (12px) and on ONE line', c['qtShown'] and c['qtFs'] == 12 and c['qtH'] < 20, c)
    chk('compact: the "Hozir" card starts at least 50px higher than before (shior kept: ~56px)', d['heroTop'] - c['heroTop'] >= 50, (d['heroTop'], c['heroTop']))
    chk('compact: the "Bajardim" button is fully on the first screen (above the bottom navigation)', 0 < c['btn'] < 844 - 90, c['btn'])
    ev("bmOpt('bqt','0')"); pg.wait_for_timeout(120); q = M()
    chk('quote hidden option: the quote disappears and the card moves up a bit more', not q['qtShown'] and q['heroTop'] < c['heroTop'], q)
    ev("bmOpt('bqt','1')"); chk('the quote can be shown again', M()['qtShown'])
    ev("bmOpt('btc','0')"); pg.wait_for_timeout(120); b = M()
    chk('switching back restores exactly the old look (same measurements as the default)', 'btc' not in b['cls'] and b['gr'] == d['gr'] and b['svg'] == d['svg'] and abs(b['heroTop'] - d['heroTop']) < 1 and b['qtShown'], b)
    ev("()=>{tab='s';render()}"); pg.wait_for_timeout(120)
    ev("()=>{document.querySelectorAll('#app details').forEach(x=>{if(/Bugun ko‘rinishi/.test(x.textContent.slice(0,60)))x.open=true})}")
    t = pg.inner_text('#app')
    chk('Sozlamalar → Bugun ko‘rinishi lists "Bugun tepasi" with Hozirgidek / Ixcham', 'Bugun tepasi' in t and 'Ixcham' in t)
    ev("bmOpt('btc','1')"); pg.wait_for_timeout(120); t = pg.inner_text('#app')
    chk('the shior option appears only in compact mode', 'Kunlik shior' in t); ev("bmOpt('btc','0')"); chk('...and disappears when not compact', 'Kunlik shior' not in pg.inner_text('#app'))
    # boshqa ekranlar tegilmagan
    ev("()=>{uiS('trk_btc','1');dzApply();tab='p';render()}"); pg.wait_for_timeout(120)
    chk('other screens are unchanged by it (Pul title keeps its size, no overflow)', pg.evaluate("parseFloat(getComputedStyle(document.querySelector('#app .top .d')).fontSize)") == 22 and M()['ow'])
    # 3 uslub
    for cls, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        go(cls); a = M(); ev("bmOpt('btc','1')"); pg.wait_for_timeout(120); z = M()
        chk(nm + ' style: compact moves the Hozir card up by 40px or more and does not overflow sideways', a['heroTop'] - z['heroTop'] >= 40 and z['ow'], (a['heroTop'], z['heroTop'], z['ow']))
        chk(nm + ' style: the "Bajardim" button is on the first screen', 0 < z['btn'] < 844 - 90, z['btn'])
    # tor ekran (320)
    pg.set_viewport_size({'width': 320, 'height': 700}); go(); ev("bmOpt('btc','1')"); pg.wait_for_timeout(150)
    chk('narrow phone (320px): no horizontal overflow and the quote stays on one line', M()['ow'] and M()['qtH'] < 20, M())
    print('\n%d passed, %d failed' % (R.ok, R.bad))
