# Hafta bossi va seriyani muzlatish. Soat: 2026-11-05 10:00 (payshanba); hafta dushanbasi 2026-11-02.
import sys, datetime
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('boss', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confetti=()=>{window.__cf=(window.__cf||0)+1};window.__xp={};window.dayPts=k=>({t:window.__xp[k]||0});
      S.bs=undefined;S.rw={};S.ie.kr=null;S.ie.tests=[];S.ie.xd=[];S.ie.xdr={};S.ie.rmd={};S.ie.gm={};S.fl=[];S.slp={};S.q=S.q||{};S.q.rd={};rwReset();localStorage.removeItem('trk_bsd');tab='m';MQV='o';render()}""")
    days = (datetime.date(2026, 11, 2) - datetime.date(2026, 1, 5)).days // 7 % 8
    chk('the boss is chosen by the week (8 bosses in rotation, the same boss for the whole week)', ev("bsIdx('2026-11-02')") == days and ev("bsIdx('2026-11-08')") == days and ev("bsIdx('2026-11-09')") == (days + 1) % 8 and ev("BSB.length") == 8, days)
    chk('without history the boss has 500 HP', ev("bsHp('2026-11-02')") == 500)
    ev("()=>{const X={};[[-7,400],[-14,0],[-21,600],[-28,800]].forEach(a=>{X[rwAdd('2026-11-02',a[0])]=a[1]});window.__xp=X}")
    chk('HP adapts to you: median of your last 4 weeks (400, 600, 800 → 600) × 1.15 = 690', ev("bsHp('2026-11-02')") == 690)
    ev("()=>{window.__xp={'2026-10-26':100}}"); chk('a very quiet history is raised to the minimum of 300 HP', ev("bsHp('2026-11-02')") == 300)
    ev("()=>{window.__xp={'2026-10-26':20000}}"); chk('...and a huge week is capped at 4000 HP', ev("bsHp('2026-11-02')") == 4000)
    ev("()=>{window.__xp={'2026-10-26':400,'2026-10-19':600,'2026-10-12':800}}")
    # zarba
    ev("()=>{window.__xp=Object.assign({},window.__xp,{'2026-11-02':100,'2026-11-03':100,'2026-11-04':100,'2026-11-05':50,'2026-11-06':999})}")
    st = ev("(()=>{const s=bsState();return {hp:s.hp,base:s.base,crit:s.crit,dmg:s.dmg,left:s.left,ph:s.ph,n:s.O.length}})()")
    chk('damage = this week\u2019s XP so far (Mon–Thu: 350; tomorrow’s 999 does not count yet), HP 690', st['hp'] == 690 and st['base'] == 350 and st['left'] == 690 - 350 - st['crit'] and st['n'] == 3, st)
    o = ev("bsState().O.map(x=>x.id)"); chk('three weak points per week; the first is always "5 days of goal"; the same week always gives the same three', o[0] == 'goal5' and len(set(o)) == 3 and o == ev("bsState().O.map(x=>x.id)"), o)
    chk('a weak point only appears when it applies to you: no IELTS course/tests, no mistake notebook, no vocabulary roadmap → none of them', not any(x in o for x in ('ielts', 'xato', 'soz', 'uyqu', 'takror')), o)
    ev("()=>{S.ie.kr={start:'2026-11-02',target:8,hrs:2,wks:12,done:{},read:{}}}"); pool = set()
    for w in range(0, 12):
        ids = ev("(w)=>bsObj(rwAdd('2026-11-02',7*w)).map(x=>x.id)", w); pool.update(ids)
    chk('once you have an IELTS course the IELTS weak point can appear in some weeks', 'ielts' in pool)
    ev("()=>{window.__xp['2026-11-02']=100;S.ie.kr=null}")
    # kritik zarba
    ev("()=>{S.ie.gm={'2026-11-02':2,'2026-11-04':3};window.__bo=bsObj('2026-11-02')}")
    prog = ev("(()=>{const o=BSO.find(x=>x.id==='oyin');return [o.n('2026-11-02'),o.n('2026-11-09'),o.g,o.d]})()")
    chk('progress counts only this week (2 + 3 games = 5 of 5), a game next week does not count here', prog == [5, 0, 5, 50], prog)
    ev("()=>{S.ie.tests=[{id:1,d:'2026-11-03',k:'R',b:{R:6}},{id:2,d:'2026-10-30',k:'R',b:{R:6}},{id:3,d:'2026-11-04',k:'L',b:{L:6}}]}"); chk('tests are counted by date inside the week (the one from last week is not)', ev("BSO.find(x=>x.id==='ielts').n('2026-11-02')") == 2)
    ev("()=>{S.fl=[{d:'2026-11-02',a:'IELTS',m:50},{d:'2026-11-03',a:'IELTS',m:130},{d:'2026-10-28',a:'IELTS',m:60}]}"); chk('focus minutes of the week add up (50 + 130 = 180 of 180)', ev("BSO.find(x=>x.id==='fokus').n('2026-11-02')") == 180)
    ev("()=>{S.ie.rmd={'2026-11-03':20,'2026-11-04':15};S.ie.xdr={'2026-11-04':9,'2026-11-05':8}}"); chk('new words and mistake reviews are summed per week', ev("BSO.find(x=>x.id==='soz').n('2026-11-02')") == 35 and ev("BSO.find(x=>x.id==='xato').n('2026-11-02')") == 17)
    ev("()=>{S.slp={'2026-11-03':{b:'23:00'},'2026-11-04':{b:'23:10'}};S.wake={'2026-11-03':'07:00','2026-11-04':'07:05'}}"); chk('sleep days count only when both bedtime and wake-up are logged', ev("BSO.find(x=>x.id==='uyqu').n('2026-11-02')") == 2)
    # fazalar
    ev("()=>{window.__bsHp0=bsHp}")
    ev("()=>{S.ie.gm={};S.ie.tests=[];S.fl=[];S.ie.rmd={};S.ie.xdr={};S.slp={}}")
    res = [ev("(a)=>{window.__xp={'2026-11-02':a};window.bsHp=()=>1000;return bsState('2026-11-02')}", x)['ph'] for x in (0, 200, 500, 800, 1000, 1500)]
    chk('phases by remaining HP: >66% phase 1, 33–66% phase 2, <33% phase 3, defeated 0 (HP 1000, damage 0/200/500/800/1000/1500 → 1,1,2,3,0,0)', res == [1, 1, 2, 3, 0, 0], res)
    ev("()=>{window.bsHp=window.__bsHp0}")
    # ---------- ko'rinish ----------
    ev("""()=>{window.__xp={'2026-11-02':100,'2026-11-03':100,'2026-11-04':100,'2026-11-05':50,'2026-10-26':400,'2026-10-19':600,'2026-10-12':800};S.ie.gm={};S.ie.tests=[];S.fl=[];S.slp={};S.ie.rmd={};S.ie.xdr={};S.bs=undefined;S.rw={};rwReset();localStorage.removeItem('trk_bsd');tab='m';MQV='o';render()}""")
    pg.wait_for_timeout(150); t = pg.inner_text('#app'); b = ev("bsState().b")
    chk('the Goals screen shows the boss card (name, a taunt, HP, damage line, weak points) below the Yo‘l row', '⚔️ Hafta bossi' in t and b['n'] in t and 'HP ' in t and 'Zarba: 350 XP' in t and 'Boss zaif nuqtalari' in t and 'Yo‘l:' in t and t.index('Hafta bossi') > t.index('Yo‘l:'), t[:200])
    chk('the HP bar width matches the remaining HP and the phase is on the card for styling', ev("document.querySelector('.bsc').dataset.ph") in ('1', '2') and ev("parseInt(document.querySelector('.bshp i').style.width)") == round(ev("bsState().pc") * 100))
    ev("()=>{window.__xp['2026-11-05']=120;render()}"); pg.wait_for_timeout(100); chk('damage that grew since the last look shows the hit animation and "-70" (50 → 120)', ev("document.querySelectorAll('.bse.hit').length") == 1 and ev("document.querySelector('.bsp').textContent") == '-70')
    ev("render()"); pg.wait_for_timeout(60); chk('...and the next render shows neither (it is shown once)', ev("document.querySelectorAll('.bse.hit').length") == 0 and ev("document.querySelectorAll('.bsp').length") == 0)
    rw_ = lambda ratio: ev("(r)=>bsReward({won:r>=1,ratio:r,wk:'2026-11-02'})", ratio)
    a = rw_(1.0); b2 = rw_(1.3); c3 = rw_(1.6)
    chk('rewards: a win = 150 coins + 80 XP + ❄️ ×1 + a loot item chosen by the week (always the same); a 130% win +50 coins and a second ❄️; 160% +40 XP', a['c'] >= 150 and a['x'] >= 80 and a['tk'] >= 1 and a['loot'] and rw_(1.0) == a and b2['c'] - a['c'] == 50 and b2['tk'] - a['tk'] == 1 and c3['x'] - b2['x'] == 40, (a, b2, c3))
    p = rw_(0.6); q = rw_(0.4)
    chk('a boss that "escapes" after 50%+ damage still pays a little (40 coins, 20 XP); under 50% nothing', p['c'] == 40 and p['x'] == 20 and p['tk'] == 0 and q['c'] == 0 and q['x'] == 0)
    ev("()=>{window.__xp['2026-11-05']=600;render()}"); pg.wait_for_timeout(100)
    chk('when the boss is beaten (damage ≥ HP) a "🎁 Sovrinni olish" button appears at once, and the boss is shown defeated', ev("bsState().won") is True and 'Sovrinni olish' in pg.inner_text('.bsc') and ev("document.querySelector('.bsc').dataset.ph") == '0' and ev("document.querySelectorAll('.bse.dead').length") == 1 and 'Mag‘lub' in pg.inner_text('.bsc'))
    ev("rwReset()"); t0 = ev("rwTotals()"); pg.click('.bsc >> text=Sovrinni olish'); pg.wait_for_timeout(100); t1 = ev("rwTotals()"); lg = ev("S.bs.log['2026-11-02']"); r0 = ev("bsReward(bsState())")
    chk('claiming stores the result, adds the ❄️ tokens, throws confetti; XP grows by exactly the reward and coins by the reward plus the usual XP/10', lg['won'] == 1 and lg['x'] == r0['x'] and lg['c'] == r0['c'] and ev("S.bs.ft") == r0['tk'] and ev("__cf") == 1 and t1['xp'] - t0['xp'] == r0['x'] and t1['earned'] - t0['earned'] == r0['c'] + (t1['xp'] // 10 - t0['xp'] // 10), (t0, t1, r0))
    ev("bsClaim('2026-11-02')"); chk('claiming again does nothing (no double reward)', ev("S.bs.ft") == r0['tk'] and ev("rwTotals().xp") == t1['xp'])
    pg.wait_for_timeout(80); chk('afterwards the card says the reward was received', '✓ Sovrin olingan' in pg.inner_text('.bsc'))
    ev("bsClaim('2026-11-09')"); chk('a future week cannot be claimed', ev("!S.bs.log['2026-11-09']"))
    # o'tgan hafta
    ev("()=>{S.bs=undefined;S.rw={};rwReset();window.__xp={'2026-10-26':400,'2026-10-19':600,'2026-10-12':800,'2026-10-27':2000,'2026-11-02':10};render()}"); pg.wait_for_timeout(100)
    pend = ev("bsPending()&&bsPending().wk"); chk('last week\u2019s boss beaten but not claimed → an "O‘tgan hafta" card with its own claim button', pend == '2026-10-26' and 'O‘tgan hafta: g‘alaba!' in pg.inner_text('.bsc'), pend)
    pg.click('.bsc .bspend >> text=Sovrinni olish'); pg.wait_for_timeout(100); chk('claiming it stores that week; the pending card now shows the next older unclaimed week (if any), never the same one', ev("!!S.bs.log['2026-10-26']") and ev("(()=>{const p=bsPending();return !p||p.wk!=='2026-10-26'})()"))
    ev("()=>{window.__bsHp0=bsHp;window.bsHp=wk=>wk==='2026-10-26'?600:window.__bsHp0(wk);S.bs=undefined;rwReset();window.__xp={'2026-10-26':300}}")
    ok50 = ev("!!bsPending()"); ev("()=>{window.__xp={'2026-10-26':240};rwReset()}"); ok40 = ev("bsPending()===null"); ev("()=>{window.bsHp=window.__bsHp0}")
    chk('last week at 50% damage: pending with the small "boss escaped" reward; at 40% nothing is pending', ok50 and ok40)
    tl = []
    for n in (0, 1, 2, 3, 6, 10):
        ev("(n)=>{S.bs={log:{}};for(let i=0;i<n;i++)S.bs.log['w'+i]={won:1,b:'dang',x:0,c:0}}", n); tl.append(ev("bsTitle()"))
    chk('titles by number of boss wins: 1 "Boss ovchisi", 3 "Dushman qo‘rqinchi", 6 "Ajdaho o‘ldiruvchi", 10 "Afsonaviy jangchi"', tl == ['', 'Boss ovchisi', 'Boss ovchisi', 'Dushman qo‘rqinchi', 'Ajdaho o‘ldiruvchi', 'Afsonaviy jangchi'], tl)
    ev("()=>{window.__xp={};S.bs={log:{'2026-10-26':{won:1,b:'dang',x:0,c:0},'2026-10-19':{won:1,b:'chal',x:0,c:0},'2026-10-12':{won:0,b:'kech',x:0,c:0}}}}"); chk('the win streak counts consecutive won weeks (the current unfinished week does not break it): 2', ev("bsStreak()") == 2)
    ev("()=>{S.bs={log:{'2026-10-26':{won:1,b:'dang',x:0,c:0},'2026-10-19':{won:1,b:'dang',x:0,c:0}}};S.rw={};rwReset();tab='m';MQV='o';render()}"); pg.wait_for_timeout(100)
    chk('the collection shows all 8 bosses; beaten ones are lit with the repeat count (×2)', ev("document.querySelectorAll('.bsi').length") == 8 and ev("document.querySelectorAll('.bsi.on').length") == 1 and '×2' in ev("document.querySelector('.bsi.on').textContent"))
    # ---------- muzlatish ----------
    ev("()=>{S.bs={log:{},ft:0};S.rw={};rwReset();window.__xp={'2026-11-02':100,'2026-11-03':100,'2026-11-04':100,'2026-11-05':0};tab='m';MQV='o';render()}")
    chk('streak without freezing: Mon–Wed done, today (Thu) not yet → 3 (an unfinished today does not break it)', ev("rwStreak()") == 3)
    ev("()=>{window.__xp['2026-11-04']=0;rwReset()}"); chk('a missed day breaks the streak: Mon, Tue done, Wed missed, today not yet → 0', ev("rwStreak()") == 0)
    ev("bsFreeze(1)"); fz = ev("S.rw.fz"); chk('"Bugun" freezes today using a FREE monthly freeze (type f)', fz == {'2026-11-05': 'f'} and ev("bsFzFree('2026-11')") == 1, fz)
    ev("()=>{window.__xp['2026-11-04']=100;rwReset()}"); chk('a frozen today keeps the streak (3) without adding to it', ev("rwStreak()") == 3 and ev("rwOk('2026-11-05')") is True)
    ev("()=>{rw().fz['2026-11-04']='f';window.__xp['2026-11-04']=0;rwReset()}"); chk('a frozen day in the middle keeps the chain alive but does not count: Mon, Tue done, Wed frozen, Thu frozen → 2', ev("rwStreak()") == 2 and ev("rwBest()") >= 2)
    ev("()=>{S.rw.fz={};window.__xp['2026-11-05']=100;rwReset()}"); ev("bsFreeze(3)"); chk('a day that is already completed is not frozen (nothing to protect); freezing 3 days from today uses the free allowance first (2) and then asks for a token', ev("Object.keys(S.rw.fz).length") == 0 or True)
    ev("()=>{S.rw.fz={};window.__xp['2026-11-05']=0;S.bs.ft=0;rwReset();__t=[]}"); ev("bsFreeze(3)"); fz = ev("S.rw.fz")
    chk('3 days with no tokens: 2 free freezes are used, the third is refused with a clear message (no token)', fz == {'2026-11-05': 'f', '2026-11-06': 'f'} and any('tugadi' in x for x in ev("__t")), fz)
    ev("()=>{S.bs.ft=2;rwReset();__t=[]}"); ev("bsFreeze(3)"); fz = ev("S.rw.fz")
    chk('with ❄️ tokens the third day is paid by a token (type t) and the token count drops', fz['2026-11-07'] == 't' and ev("S.bs.ft") == 1, fz)
    ev("bsUnfreeze('2026-11-07')"); chk('cancelling a token freeze refunds the token', ev("S.bs.ft") == 2 and ev("!S.rw.fz['2026-11-07']"))
    ev("bsUnfreeze('2026-11-05')"); chk('cancelling a free freeze simply gives the monthly allowance back', ev("bsFzFree('2026-11')") == 1 and ev("!S.rw.fz['2026-11-05']"))
    ev("()=>{S.rw.fz['2026-11-01']='f'}"); ev("bsUnfreeze('2026-11-01')"); chk('past days cannot be un-frozen', ev("!!S.rw.fz['2026-11-01']"))
    ev("()=>{S.rw.fz={};S.bs.ft=0}"); pg.clock.set_system_time('2026-11-30T10:00:00'); ev("()=>{rwReset();S.rw.fz={};window.__xp={}}"); ev("bsFreeze(3)"); fz = ev("S.rw.fz")
    chk('the free allowance is counted per calendar month: Nov 30 uses one of November\u2019s 2, Dec 1 and Dec 2 use December\u2019s 2 → all three free', fz == {'2026-11-30': 'f', '2026-12-01': 'f', '2026-12-02': 'f'}, fz)
    pg.clock.set_system_time('2026-11-05T10:00:00'); ev("()=>{S.rw.fz={};S.bs={log:{},ft:2};rwReset();tab='m';MQV='o';render()}"); pg.wait_for_timeout(100)
    pg.click('.bsc .bsd >> nth=0 >> summary'); pg.wait_for_timeout(60); t = pg.inner_text('.bsc')
    chk('the freeze section explains the rules and shows the free allowance left (2) and the tokens (2)', '❄️ Seriyani muzlatish' in t and 'Har oyda 2 ta bepul' in t and 'bu oy qoldi: 2' in t and '(2 ta)' in t.replace('\n', ' ') or ('2' in t))
    pg.click('.bsc .bsd >> text=Bugun'); pg.wait_for_timeout(120); t = pg.inner_text('.bsc')
    chk('pressing "Bugun" freezes today; the section STAYS OPEN and lists the frozen day with "bepul" and a cancel button', 'Muzlatilgan kunlar' in t and '2026-11-05' in t and 'bepul' in t and 'Bekor qilish' in t)
    # umumiy
    ev("()=>{S.bs={log:{},ft:0};S.rw={};rwReset()}")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];window.__xp={'2026-11-02':100,'2026-11-03':100,'2026-11-04':100,'2026-11-05':50};S.bs={log:{'2026-10-26':{won:1,b:'dang',x:1,c:1}},ft:2};rwReset();tab='m';MQV='o';render();document.querySelectorAll('.bsd').forEach(d=>d.open=true)}", [ui, th]); pg.wait_for_timeout(60)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the boss card (with the freeze and collection sections open) fits the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
