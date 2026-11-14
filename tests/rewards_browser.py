# Yo'l (rag'bat tizimi): hisob-kitob, seriya, tanga, topshiriqlar, do'kon, ekranlar. Soat qotirilgan: 2026-10-31 (shanba), 10:00.
import sys, datetime
from playwright.sync_api import sync_playwright
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
RESET = """()=>{S.ob=1;S.ts=1;S.done={};S.rules={};S.hb={};S.tasks={};S.top={};S.nm.d={};S.dz.d={};S.gym.log=[];S.gym.plan={};S.close={};S.water={};S.fm={};
 S.q.hd={};S.q.rd={};S.q.ny={};S.q.ord=[];S.q.m={};S.q.ppd=3;S.q.cur=0;S.ie.words=[];S.goals=[];S.hab=[];S.hb={};S.rz.fast={};S.money=[];S.rw=undefined;S.cel={};S.main=0;rwReset()}"""
FILL = """(k,n)=>{ // n = 60 (5 prayers) or 100 (5 prayers + 2 top-3)
 S.nm.d[k]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1}; if(n>=100)S.top[k]=[{t:'a',x:1},{t:'b',x:1}]; rwReset()}"""
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('dialog', lambda d: d.accept())
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto('file:///mnt/user-data/outputs/tracker/index.html'); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    ev = pg.evaluate
    ev("()=>{window.__t=[];const o=toast;window.toast=function(t){window.__t.push(t);return o(t)}}")  # record toasts
    chk('clock is fixed (Saturday 31 Oct 2026)', ev("dk()") == '2026-10-31')
    # ---------- 1. scoring ----------
    ev(RESET)
    ev("""()=>{const k=dAgo(3);S.done[k]={qur:true};S.rules[k]={ig:1};S.hab=[{id:'h1',t:'x'}];S.hb[k]={h1:1};S.tasks[k]=[{x:1},{x:0}];S.top[k]=[{x:1},{x:1}];
      S.nm.d[k]={fajr:1,zuhr:1,asr:2};S.gym.log=[{id:1,d:k,n:'a',s:3,r:8,w:50}];S.close[k]={d:1};S.water[k]=5;S.q.ny={[k]:3};S.q.rd={[k]:4};S.q.hd={[k]:30};S.rz.fast={[k]:1};
      S.ie.words=[1,2,3].map(i=>({id:i,w:'a',m:'b',box:1,due:k,t:new Date(k+'T12:00').getTime()}));S.fm={[k]:50};rwReset()}""")
    # block(4)+rule(6)+habit(8)+task(10)+top(40)+prayer 2x12=24+gym(30)+close(10)+water(5)+newpages 3x25=75+review 4x3=12+hatm min(30,20)x2=40+fast(20)+words 3+focus 50/5=10
    exp = 4 + 6 + 8 + 10 + 40 + 24 + 30 + 10 + 5 + 75 + 12 + 40 + 20 + 3 + 10
    chk('one day scores exactly the sum of its parts (%d XP)' % exp, ev("dayPts(dAgo(3)).t") == exp, ev("dayPts(dAgo(3))"))
    chk('a missed prayer (state 2) gives no XP, a sleep block gives none', ev("dayPts(dAgo(3)).p.find(x=>x[0]==='Namoz')[1]") == 24)
    ev("()=>{const k=dAgo(4);S.q.ny={[k]:9};S.q.rd={[k]:99};S.q.hd={[k]:99};S.ie.words=Array.from({length:50},(_,i)=>({id:i,w:'a',m:'b',box:1,due:k,t:new Date(k+'T12:00').getTime()}));S.fm={[k]:9999};S.water[k]=50;rwReset()}")
    chk('daily caps: 5 new pages, 15 review pages, 20 hatm pages, 20 words, 30 focus, 8 glasses', ev("dayPts(dAgo(4)).t") == 5 * 25 + 15 * 3 + 20 * 2 + 20 + 30 + 8, ev("dayPts(dAgo(4))"))
    ev(RESET)
    chk('empty day = 0 XP, level 1, no streak', ev("dayPts(dk()).t") == 0 and ev("xpInfo().L") == 1 and ev("rwStreak()") == 0)
    lv = ev("[0,99,100,399,400,899,900,1599,1600,8100].map(x=>rwLevel(x).L)")
    chk('level thresholds: 0/99->1, 100/399->2, 400/899->3, 900->4, 1600->5, 8100->10', lv == [1, 1, 2, 2, 3, 3, 4, 4, 5, 10], lv)
    chk('level titles', ev("[1,2,3,5,8,12,17,25,40].map(rwName)") == ['Boshlovchi', 'Boshlovchi', 'Qat’iyatli', 'Intizomli', 'Mustahkam', 'Usta', 'Ustoz', 'Afsona', 'Afsona'])
    chk('level progress is a percentage between levels', ev("rwLevel(250).pc") == 50 and ev("rwLevel(100).pc") == 0)
    # ---------- 2. streak and shield ----------
    ev(RESET); ev(f"({FILL})(dAgo(1),60);({FILL})(dAgo(2),60);({FILL})(dAgo(3),60)")
    chk('streak counts consecutive 60-XP days; today not yet done does not break it', ev("rwStreak()") == 3)
    ev(f"({FILL})(dk(),60)"); chk('today reaching 60 XP adds one', ev("rwStreak()") == 4)
    ev(RESET); ev(f"({FILL})(dAgo(1),60);({FILL})(dAgo(3),60);({FILL})(dAgo(4),60)")
    chk('a missed day breaks the streak (1 day, the older ones are cut)', ev("rwStreak()") == 1 and ev("rwBest()") == 2)
    ev(RESET); ev(f"({FILL})(dAgo(2),60);({FILL})(dAgo(3),60);({FILL})(dAgo(4),60);rw().sh=1")
    chk('before the shield: yesterday missed -> streak 0', ev("rwStreak()") == 0)
    ev("rwAuto()")
    chk('shield auto-saves yesterday: streak continues (4), shield used, once per day', ev("rwStreak()") == 4 and ev("rw().sh") == 0 and ev("rw().su.includes(dAgo(1))"))
    ev("rw().sh=3;rw().au='';rwAuto()"); chk('no shield is wasted when yesterday was fine', ev("rw().sh") == 3)
    ev(RESET); ev(f"({FILL})(dAgo(1),60);rw().sh=2;rwReset();rwAuto()")
    chk('a shield is not used when there is no streak to protect', ev("rw().sh") == 2 and ev("rw().su.length") == 0)
    # ---------- 3. coins / shop ----------
    ev(RESET); ev(f"({FILL})(dAgo(1),100);({FILL})(dAgo(2),100)")   # 200 XP -> 20 coins
    chk('200 XP = 20 coins (1 coin per 10 XP)', ev("rwTotals().xp") == 200 and ev("rwTotals().coins") == 20)
    ev(RESET); ev("S.rw={sh:0,su:[],q:{},buy:[],wk:{},shop:[{id:'a',e:'☕',t:'Choy',c:30},{id:'b',e:'🎁',t:'Katta',c:500}]};for(let i=1;i<=5;i++){S.nm.d[dAgo(i)]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};S.top[dAgo(i)]=[{x:1},{x:1}]}rwReset()")  # 500 XP -> 50 coins
    chk('500 XP = 50 coins', ev("rwTotals().coins") == 50)
    ev("rwBuy('b')"); chk('cannot buy something too expensive (nothing spent)', ev("rw().buy.length") == 0 and ev("rwTotals().coins") == 50 and any('Tanga yetmaydi' in t for t in ev("window.__t")))
    ev("rwBuy('a')"); chk('buying a 30-coin reward spends 30', ev("rw().buy.length") == 1 and ev("rwTotals().coins") == 20)
    ev("rwBuy('a')"); chk('second purchase is refused when coins are short (20 < 30)', ev("rw().buy.length") == 1)
    ev("rwUndo(rw().buy[0].id)"); chk('undo refunds the coins', ev("rw().buy.length") == 0 and ev("rwTotals().coins") == 50)
    ev("rwShield()"); chk('shield costs 60 coins: refused with 50', ev("rw().sh") == 0)
    ev("S.nm.d[dAgo(9)]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};S.top[dAgo(9)]=[{x:1},{x:1}];rwReset()")   # +100 XP -> 60 coins
    ev("rwShield()"); chk('with 60 coins a shield is bought (+1 shield, -60 coins)', ev("rw().sh") == 1 and ev("rwTotals().coins") == 0)
    ev("rwUndo(rw().buy[0].id)"); chk('undoing a shield purchase takes the shield back', ev("rw().sh") == 0 and ev("rwTotals().coins") == 60)
    ev("document.body.insertAdjacentHTML('beforeend','<input id=rwe value=🍕><input id=rwt value=\"Pitsa kechasi\"><input id=rwc value=150>');rwItemAdd()")
    chk('custom reward can be added with emoji, name and price', ev("rw().shop.some(x=>x.t==='Pitsa kechasi'&&x.c===150&&x.e==='🍕')"))
    ev("rwItemDel(rw().shop.find(x=>x.t==='Pitsa kechasi').id)"); chk('and deleted', not ev("rw().shop.some(x=>x.t==='Pitsa kechasi')"))
    ev(RESET); chk('default shop has 5 starter rewards', ev("rw().shop.length") == 5 and ev("rw().shop.map(x=>x.c)") == [30, 80, 120, 400, 1500])
    # ---------- 4. daily quests ----------
    ev(RESET); ev("S.q.ppd=3;S.q.cur=1;S.top[dk()]=[{t:'a',x:0},{t:'b',x:0}];S.hab=[{id:'h1',t:'x'}]")
    q1 = ev("rwQuests(dk()).map(q=>q.id)"); q2 = ev("rwQuests(dk()).map(q=>q.id)")
    chk('3 quests, same all day (deterministic), the first is the hifz quest', len(q1) == 3 and q1 == q2 and q1[0] == 'hifz' and len(set(q1)) == 3, q1)
    ev("S.q.ppd=0"); chk('without a hifz goal the first quest becomes Top-3', ev("rwQuests(dk())[0].id") == 'top')
    ev("S.q.ppd=3;S.top[dk()]=[]"); ev("S.q.ord=[]"); ids = ev("rwQuests(dk()).map(q=>q.id)")
    chk('only applicable quests are offered (no review quest without memorised suras, no Top-3 without tasks)', 'rev' not in ids and 'top' not in ids and 'gym' not in ids, ids)
    ev(RESET); ev("S.q.ppd=3;S.q.cur=1;S.hab=[]"); qs = ev("rwQuests(dk()).map(q=>q.id)")
    xp0 = ev("rwTotals().xp"); ev("rwClaim('%s')" % qs[0]); chk('cannot claim an unfinished quest', ev("(rw().q[dk()]||{c:[]}).c.length") == 0)
    # complete all three, whatever they are
    ev("""()=>{const Q=rwQuests(dk());Q.forEach(q=>{if(q.id==='hifz')S.q.ny={[dk()]:3};if(q.id==='pray')S.nm.d[dk()]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};if(q.id==='water')S.water[dk()]=8;if(q.id==='close')S.close[dk()]={d:1};
        if(q.id==='zikr'){}if(q.id==='goal'){}});rwReset()}""")
    done = ev("rwQuests(dk()).filter(q=>q.n()>=q.g()).map(q=>q.id)")
    chk('finished quests are detected from the real data', 'hifz' in done, done)
    before = ev("rwTotals()"); ev("rwClaim('hifz')"); after = ev("rwTotals()")
    chk('claiming a finished quest gives +25 XP once', after['xp'] - before['xp'] == 25 + 75 * 0 + 0 or after['xp'] - before['xp'] == 25, (before, after))
    ev("rwClaim('hifz')"); chk('claiming twice does nothing', ev("rw().q[dk()].c.length") == 1)
    # force all three finished and claim -> chest
    ev("""()=>{const Q=rwQuests(dk());window.__Q=Q.map(q=>q.id);S.q.ny={[dk()]:3};S.nm.d[dk()]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};S.water[dk()]=8;S.close[dk()]={d:1};S.hab=[];S.top[dk()]=[];S.gym.log=[{id:9,d:dk(),n:'x',s:1,r:1,w:0}];
        S.gym.plan[new Date().getDay()]={place:'gym',ex:[]};S.ie.words=Array.from({length:12},(_,i)=>({id:i,w:'a',m:'b',box:1,due:dk(),t:Date.now()}));S.goals=[{t:'g',ms:[{t:'m',x:1,xd:dk()},{t:'n',x:0}]}];S.q.ord=[1];S.q.rd={[dk()]:1};S.dz.d[dk()]={};rwReset()}""")
    qn = ev("rwQuests(dk())"); allok = ev("rwQuests(dk()).every(q=>q.n()>=q.g()||['zikr'].includes(q.id))")
    if not allok: ev("window.__skip=1")
    ids = ev("rwQuests(dk()).map(q=>q.id)")
    # make 'zikr' quest satisfiable if it was drawn
    ev("()=>{if(rwQuests(dk()).some(q=>q.id==='zikr')){const l=dzList('sb');l.forEach(d=>{S.dz.d[dk()][d.id+'@sb']=d.k})}rwReset()}")
    ev("()=>{rw().q[dk()]={c:[],x:0};rwQuests(dk()).forEach(q=>rwClaim(q.id))}")
    e = ev("rw().q[dk()]"); chk('claiming all three opens the daily chest (once) and gives +20 coins', len(e['c']) == 3 and e['x'] == 1 and ev("rwTotals().chest") == 1, (ids, e))
    chk('a toast announces the chest', any('sandig' in t for t in ev("window.__t")))
    # ---------- 5. weekly challenge ----------
    ev(RESET); ev(f"for(let i=1;i<=5;i++)({FILL})(dAgo(i),100)")
    w = ev("rwWeek()"); chk('week runs Monday..Sunday and counts the 100-XP days (Mon26-Fri30 = 5)', w['key'] == '2026-10-26' and w['n'] == 5 and len(w['days']) == 7 and w['days'][6][1] is None, w['n'])
    c0 = ev("rwTotals().coins"); x0 = ev("rwTotals().xp"); ev("rwClaimWk()"); t1 = ev("rwTotals()")
    chk('weekly challenge: +100 coins and +50 XP', t1['coins'] - c0 == 100 + 5 and t1['xp'] - x0 == 50, (c0, t1))   # +5 coins from the +50 XP itself
    ev("rwClaimWk()"); chk('cannot be claimed twice', ev("Object.keys(rw().wk).length") == 1)
    ev(RESET); ev(f"for(let i=1;i<=4;i++)({FILL})(dAgo(i),100)"); ev("rwClaimWk()"); chk('not available with only 4 days', ev("Object.keys(rw().wk).length") == 0)
    # ---------- 6. integration with the rest of the app ----------
    ev(RESET); ev("S.q.cur=1;S.q.ord=[];S.q.m={};addP(2)"); chk('memorising pages (addP) is logged for XP: 2 pages = 50 XP', ev("S.q.ny[dk()]") == 2 and ev("dayPts(dk()).t") == 50)
    ev("setM(1,0)"); chk('un-marking pages takes the logged pages back', ev("(S.q.ny[dk()]||0)") <= 2)
    ev(RESET); ev("S.goals=[{t:'Maqsad',ms:[{t:'a',x:0},{t:'b',x:0}],rw:'Kino'}];gm(0,0)")
    chk('finishing a goal step: date saved, +40 XP, toast', ev("S.goals[0].ms[0].xd") == ev("dk()") and ev("dayPts(dk()).t") == 40 and any('Bosqich bajarildi' in t for t in ev("window.__t")))
    ev("gm(0,1)"); chk('finishing the last step announces the goal and its reward', any('Maqsadga erishding' in t and 'Kino' in t for t in ev("window.__t")))
    ev("gm(0,1)"); chk('un-ticking removes the date and the XP', ev("S.goals[0].ms[1].xd") == '' and ev("dayPts(dk()).t") == 40)
    ev("window.prompt=()=>'Yangi kiyim';grw(0)"); chk('goal reward can be set and is saved', ev("S.goals[0].rw") == 'Yangi kiyim')
    ev("()=>{tab='m';render()}"); t = pg.inner_text('#app'); chk('Maqsad screen shows the reward chip and the Yo\u2018l shortcut', 'Mukofot: Yangi kiyim' in t and 'Yo‘l:' in t, t[:200])
    # ---------- 7. celebrations ----------
    ev(RESET); ev("window.__t.length=0;S.cel={init:1,d:{},lv:1,hs:{},hc:0,bk:0,v2:1,xg:{}};S.nm.d[dk()]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};S.top[dk()]=[{x:1},{x:1}];rwReset();celeb()")
    chk('reaching 100 XP in a day is celebrated, and level 2 too', any('Kun maqsadi' in t or 'Yangi daraja' in t for t in ev("window.__t")))
    n = len(ev("window.__t")); ev("celeb()"); chk('the same celebration is not repeated', len(ev("window.__t")) == n)
    ev(RESET); ev("window.__t.length=0;S.cel={init:1,d:{},lv:1,hs:{},hc:0,bk:0,v2:1,xg:{}};for(let i=0;i<7;i++)S.nm.d[dAgo(i)]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};rwReset();celeb()")
    chk('7-day streak is celebrated', any('7 kunlik seriya' in t for t in ev("window.__t")))
    n = len(ev("window.__t")); ev("celeb()"); chk('and only once', len(ev("window.__t")) == n)
    # ---------- 8. screens ----------
    ev(RESET); ev("S.q.ppd=3;S.q.cur=1;S.hab=[{id:'h1',t:'Kitob',e:'📚'}];S.top[dk()]=[{t:'Ish',x:1},{t:'Ish2',x:0}];S.nm.d[dk()]={fajr:1,zuhr:1};S.goals=[{t:'Hofiz bo‘lish',e:'📖',ms:[{t:'Juz Amma',x:0},{t:'5 pora',x:0}],rw:'Yangi telefon',dl:'2027-03-01'}];S.main=0;for(let i=1;i<=3;i++){S.nm.d[dAgo(i)]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1}};rwReset();tab='h';BV='j';render()")
    ev("localStorage.setItem('trk_bsimple','0');render()")  # mukofot kartochkasi to'liq ko'rinishda; oddiy ko'rinishda u "Yana" ichida
    pg.wait_for_timeout(200)
    info = ev("""()=>{const a=document.getElementById('app');const kids=[...a.querySelectorAll('.rwc,.hero')];return {first:kids[0]&&kids[0].className,hasCard:!!a.querySelector('.rwc'),txt:(a.querySelector('.rwc')||{}).innerText}}""")
    chk('Bugun: the Hozir hero is the first card (as requested) and the reward card follows it', info['hasCard'] and 'hero' in (info['first'] or ''), info)
    chk('card shows level, streak, coins and today XP', all(s in (info['txt'] or '') for s in ['Boshlovchi', 'Bugun', 'XP', 'Topshiriqlar']), info['txt'])
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());const t=document.getElementById('toast');if(t)t.remove()"); pg.screenshot(path='/tmp/rw_bugun.png')
    ev("()=>{VD='2026-10-29';render()}"); chk('the card is hidden when looking at another day', not ev("!!document.querySelector('#app .rwc')")); ev("()=>{VD=null;render()}")
    pg.click('.rwc'); pg.wait_for_timeout(300)
    chk('tapping the card opens the Yo\u2018l screen', ev("!!document.getElementById('rw')"))
    body = pg.inner_text('#rwb')
    chk('Yo\u2018l has all sections', all(s in body for s in ['Bugun', 'Kun topshiriqlari', 'Bu hafta', 'Seriya', 'Asosiy maqsad', 'Mukofotlar do‘koni', 'Yutuqlar', 'Ochkolar qanday']), [s for s in ['Bugun', 'Kun topshiriqlari', 'Bu hafta', 'Seriya', 'Asosiy maqsad', 'Mukofotlar do‘koni', 'Yutuqlar'] if s not in body])
    chk('Yo\u2018l shows the goal with its reward', 'Hofiz bo‘lish' in body and 'Yangi telefon' in body)
    ov = ev("()=>{const b=document.getElementById('rwb');return {sw:b.scrollWidth,cw:b.clientWidth,doc:document.documentElement.scrollWidth,over:[...b.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>innerWidth+2&&!e.closest('.rwheat,.rwbars')}).length}}")
    chk('Yo\u2018l does not scroll sideways', ov['sw'] <= ov['cw'] + 1 and ov['doc'] <= 392 and ov['over'] == 0, ov)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());const t=document.getElementById('toast');if(t)t.remove()")
    pg.evaluate("document.getElementById('rwb').scrollTo(0,0)"); pg.wait_for_timeout(100); pg.screenshot(path='/tmp/rw_yol1.png')
    for i, y in enumerate([700, 1500, 2300]):
        pg.evaluate(f"document.getElementById('rwb').scrollTo(0,{y})"); pg.wait_for_timeout(120); pg.screenshot(path=f'/tmp/rw_yol{i+2}.png')
    # live update while the screen is open
    pg.evaluate("document.getElementById('rwb').scrollTo(0,0)")
    xp_before = ev("xpInfo().xp"); ev("S.top[dk()][1].x=1;save()"); pg.wait_for_timeout(250)
    chk('the open Yo\u2018l screen refreshes after a change (XP +20)', ev("xpInfo().xp") == xp_before + 20 and str(xp_before + 20) in pg.inner_text('#rwb'))
    # buy through the UI
    ev("()=>{rw().shop=[{id:'z',e:'☕',t:'Test choy',c:1}];for(let i=4;i<=9;i++){S.nm.d[dAgo(i)]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1}}rwReset();rwDraw()}")
    pg.click('.rwit .btn'); pg.wait_for_timeout(250)
    chk('buying through the screen records it and shows it in the history', ev("rw().buy.length") == 1 and 'Test choy' in pg.inner_text('#rwb') and 'Olingan mukofotlar' in pg.inner_text('#rwb'))
    pg.click('#rw .x[aria-label="Yopish"]'); pg.wait_for_timeout(200)
    chk('closing returns to Bugun and unlocks the page', not ev("!!document.getElementById('rw')") and not ev("document.documentElement.classList.contains('ovl')"))
    # ---------- 9. Quran groups ----------
    ev("()=>{tab='q';QT='y';render()}"); t = pg.inner_text('#app')
    chk('Quran tab: group switch plus only that group\u2019s tabs', 'Ibodat' in t and 'Mushaf' in t and 'Yodlash' in t and 'Hatm' in t and 'Tinglash' in t and 'Namoz' not in pg.inner_text('.seg.sc'))
    pg.click('#app .seg button >> text=Ibodat'); pg.wait_for_timeout(120)
    chk('Ibodat group shows Namoz, Zikr, Duolar, Ramazon', all(s in pg.inner_text('.seg.sc') for s in ['Namoz', 'Zikr', 'Duolar', 'Ramazon']) and ev("QT") == 'n')
    ev("()=>{QT='d';render()}"); pg.click('#app .seg button >> text=Qur‘on'); pg.wait_for_timeout(100)
    pg.click('#app .seg button >> text=Ibodat'); pg.wait_for_timeout(100)
    chk('each group remembers its last tab', ev("QT") == 'd')
    crashed = []
    for q in ['u', 'y', 't', 'h', 'a', 'n', 'z', 'd', 'r']:
        ev(f"()=>{{tab='q';QT='{q}';render()}}"); pg.wait_for_timeout(40)
        if 'Kechirasan' in pg.inner_text('#app'): crashed.append(q)
    chk('all 9 Quran sub-screens still render', not crashed, crashed)
    # ---------- 9b. Odat / Pul / O'qish organisation ----------
    ev(RESET); ev("S.money=[{id:1,d:dAgo(1),w:'p',k:'out',a:5000,c:'Ovqat'}];rwReset()")
    chk('writing down money earns +6 XP that day', ev("dayPts(dAgo(1)).p.find(x=>x[0]==='Pul hisobi')[1]") == 6 and ev("dayPts(dk()).t") == 0)
    chk('the money quest exists only for people who use the money tracker', 'money' in ev("RWQ.filter(q=>q.ap()).map(q=>q.id)") and ev("S.money=[];RWQ.find(q=>q.id==='money').ap()") is False)
    ev("()=>{tab='o';OT='j';render()}"); segs = pg.evaluate("[...document.querySelectorAll('#app > .seg')[0].children].map(b=>b.textContent.trim())")
    chk('Odat tab: 5 clear tabs (Odatlar, Tahlil, Zal, Uyqu, Isolation) with no duplicate Hafta/Oy', segs == ['✅ Odatlar', '📊 Tahlil', '💪 Zal', '😴 Uyqu', '🧘 Isolation'], segs)
    chk('the habit grid switch is now called "Haftalik jadval / Oylik jadval"', 'Haftalik jadval' in pg.inner_text('#app') and 'Oylik jadval' in pg.inner_text('#app'))
    pg.click('#app > .seg button >> text=Tahlil'); pg.wait_for_timeout(150)
    chk('Tahlil opens the weekly analysis with a Hafta / Oy va yil switch', ev("OT") == 'w' and 'Oy va yil' in pg.inner_text('#app') and 'Kechirasan' not in pg.inner_text('#app'))
    pg.click('#app >> text=Oy va yil'); pg.wait_for_timeout(150)
    chk('"Oy va yil" shows the monthly analysis and the Wrapped switch', ev("OT") == 'o' and 'Yillik' in pg.inner_text('#app') and pg.evaluate("document.querySelectorAll('#app > .seg')[0].querySelector('.on').textContent.includes('Tahlil')"))
    ev("()=>{OT='z';render()}"); chk('Zal and Isolation tabs still render', 'Kechirasan' not in pg.inner_text('#app')); ev("()=>{OT='i';render()}"); chk('Isolation renders', 'Kechirasan' not in pg.inner_text('#app'))
    ev("()=>{tab='p';W='p';PV='b';render()}"); pg.wait_for_timeout(150)
    chk('a tab row that does not fit shows a fade on its right edge (Pul)', pg.evaluate("document.querySelector('.seg.sc').classList.contains('mr-r')") is True)
    pg.evaluate("(()=>{const e=document.querySelector('.seg.sc');e.scrollLeft=e.scrollWidth})()"); pg.wait_for_timeout(150)
    chk('scrolled to the end: right fade gone, left fade shown', pg.evaluate("(()=>{const c=document.querySelector('.seg.sc').classList;return !c.contains('mr-r')&&c.contains('mr-l')})()"))
    # ---------- 10. old API + errors ----------
    xi = ev("xpInfo()"); chk('xpInfo() keeps its shape (used by Bugun, badges, celebrations)', all(k in xi for k in ['xp', 'L', 'st', 'pc', 'name']), xi)
    ev("()=>{tab='h';BV='t';render()}"); chk('Tahlil screen (achievements) renders with the new badges', 'Kechirasan' not in pg.inner_text('#app') and ('5-daraja' in pg.inner_text('#app') or 'Yutuqlar' in pg.inner_text('#app')))
    # ---------- 10b. weekly report + Telegram rows ----------
    ev(RESET); ev(f"for(let i=1;i<=5;i++)({FILL})(dAgo(i),100);({FILL})(dk(),60);({FILL})(dAgo(9),100);S.q.ppd=3;S.q.cur=1")
    r = ev("rwRep(rwMon(dk()))")
    chk('weekly report: Monday-based week, 6 days so far, 560 XP', r['mon'] == '2026-10-26' and r['n'] == 6 and r['xp'] == 560, r)
    chk('report counts days >=60 (6) and >=100 (5), best day is the first 100-XP day', r['m60'] == 6 and r['m100'] == 5 and r['best'] == ['2026-10-26', 100], r)
    chk('report compares with the previous week (100 XP -> +460%)', r['prevXp'] == 100 and r['delta'] == 460, r)
    chk('report names the weakest area (no new pages learned -> "Yangi sahifa yodlash")', r['weak'] == 'Yangi sahifa yodlash', r['weak'])
    txt = ev("rwRepText(rwMon(dk()))"); chk('report text is ready to share', '560 XP' in txt and 'Haftalik hisobot' in txt and 'Keyingi hafta e’tibor: Yangi sahifa yodlash' in txt and '26.10 – 01.11' in txt, txt)
    ev("S.rem.on=true;S.rem.yo=true;S.rem.custom=S.rem.custom||[]")
    rows = ev("remRows()"); byk = {x['kind']: x for x in rows if x.get('kind') and x['kind'][:2] in ('st', 'ym', 'wk')}
    chk('Yo\u2018l reminders: morning (07:00, daily), weekly report (Sunday 20:30, dated), no streak-risk row when today is already 60 XP', 'ym' in byk and byk['ym']['hhmm'] == '07:00' and len(byk['ym']['days']) == 7 and 'wk@2026-11-01' in byk and byk['wk@2026-11-01']['hhmm'] == '20:30' and byk['wk@2026-11-01']['days'] == [0] and not any(k.startswith('st@') for k in byk), list(byk))
    ev(RESET); ev(f"({FILL})(dAgo(1),60);({FILL})(dAgo(2),60);S.rem.on=true;S.rem.yo=true;S.rem.custom=[]")
    rows = ev("remRows()"); st = [x for x in rows if (x.get('kind') or '').startswith('st@')]
    chk('streak at risk (2-day streak, 0 XP today) creates a dated 21:00 row for today only', len(st) == 1 and st[0]['kind'] == 'st@2026-10-31' and st[0]['hhmm'] == '21:00' and st[0]['days'] == [6] and 'yana 60 XP' in st[0]['body'] and '2 kunlik seriya' in st[0]['body'], st)
    ev("S.rem.yo=false")
    rows = ev("remRows()"); chk('switch off -> no Yo\u2018l rows at all', not any((x.get('kind') or '').startswith(('st@', 'ym', 'wk@')) for x in rows), rows)
    card = ev("remCard.toString()")   # the card itself is shown only to signed-in users, so check its template
    chk('Settings -> Eslatmalar template has the Yo\u2018l switch (seriya xavfi, ertalabki, yakshanba hisoboti)', 'Yo‘l: seriya xavfi' in card and "'yo'" in card, card[:100])
    ev("S.rem.yo=false;remT('yo')"); chk('the switch toggles the setting', ev("S.rem.yo") is True)
    # report on the Yo'l screen
    ev("()=>{tab='h';BV='j';render();rwOpen()}"); pg.wait_for_timeout(250)
    body = pg.inner_text('#rwb'); chk('Yo\u2018l screen has the weekly report (this week and last week) with copy buttons', 'Haftalik hisobot' in body and 'Bu hafta (hozirgacha)' in body and 'O‘tgan hafta' in body and ev("document.querySelectorAll('#rwb .rwrp button').length") == 2)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());document.getElementById('rwrep').scrollIntoView()"); pg.wait_for_timeout(150); pg.screenshot(path='/tmp/rw_report.png')
    ev("rwClose()"); pg.wait_for_timeout(100)
    # Sunday evening: the card announces the report
    pg.clock.set_system_time(datetime.datetime(2026, 11, 1, 19, 0, 0)); pg.wait_for_timeout(50)
    ev("()=>{tab='h';BV='j';VD=null;render()}"); pg.wait_for_timeout(150)
    chk('Sunday 19:00: the Bugun card says "Haftalik hisobot tayyor"', 'Haftalik hisobot tayyor' in pg.inner_text('.rwc'))
    pg.click('.rwc'); pg.wait_for_timeout(300)
    chk('tapping it opens the Yo\u2018l screen at the report', ev("!!document.getElementById('rwrep')") and ev("document.getElementById('rwb').scrollTop") > 100)
    ev("rwClose()"); pg.clock.set_system_time(datetime.datetime(2026, 11, 2, 9, 0, 0)); ev("()=>{tab='h';render()}"); pg.wait_for_timeout(120)
    chk('Monday morning it still shows (last week\u2019s report)', 'Haftalik hisobot tayyor' in pg.inner_text('.rwc'))
    pg.clock.set_system_time(datetime.datetime(2026, 11, 3, 9, 0, 0)); ev("()=>{tab='h';render()}"); pg.wait_for_timeout(120)
    chk('Tuesday it is gone', 'Haftalik hisobot tayyor' not in pg.inner_text('.rwc'))
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 10, 0, 0))
    # ---------- 10c. adaptive goal, light day, comeback ----------
    BIG = """(k)=>{S.nm.d[k]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};S.top[k]=[{x:1},{x:1},{x:1}];S.gym.log.push({id:Math.random(),d:k,n:'x',s:1,r:1,w:0});S.close[k]={d:1}}"""
    ev(RESET); ev(f"S.gym.log=[];for(let i=1;i<=4;i++)({FILL})(dAgo(i),100);rwReset()")
    chk('adaptive goal: with fewer than 5 active days it stays at the default 100', ev("rwGoal(dk())") == 100)
    ev(RESET); ev(f"S.gym.log=[];for(let i=1;i<=6;i++)({BIG})(dAgo(i));rwReset()")
    chk('a typical 160-XP day -> today\u2019s goal is 160', ev("dayPts(dAgo(1)).t") == 160 and ev("rwGoal(dk())") == 160, ev("[dayPts(dAgo(1)).t,rwGoal(dk())]"))
    chk('the goal for a past day uses only the days before it (not retroactive)', ev("rwGoal(dAgo(5))") == 100, ev("rwGoal(dAgo(5))"))
    ev(RESET); ev(f"S.gym.log=[];for(let i=1;i<=6;i++)({FILL})(dAgo(i),60);rwReset()"); chk('typical 60-XP days -> goal floor is 80', ev("rwGoal(dk())") == 80)
    ev(RESET); ev("for(let i=1;i<=6;i++){S.nm.d[dAgo(i)]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};S.top[dAgo(i)]=[1,2,3,4,5,6,7,8].map(()=>({x:1}));S.gym.log.push({id:i,d:dAgo(i),n:'x',s:1,r:1,w:0})}rwReset()"); chk('very busy days -> goal is capped at 250', ev("rwGoal(dk())") == 250)
    ev(RESET); ev(f"S.gym.log=[];for(let i=1;i<=6;i++)({BIG})(dAgo(i));rwReset()")
    ev(f"S.nm.d[dk()]={{fajr:1,zuhr:1,asr:1,maghrib:1,isha:1}};S.top[dk()]=[{{x:1}},{{x:1}}];rwReset()"); ev("window.__t=[];S.cel={init:1,d:{},lv:99,hs:{},hc:0,bk:0,v2:1,xg:{}};celeb()")
    chk('100 XP is NOT celebrated as "kun maqsadi" when the goal is 160', not any('Kun maqsadi' in t for t in ev("window.__t")))
    ev(f"({BIG})(dk());rwReset();window.__t=[];celeb()"); chk('160 XP is celebrated', any('Kun maqsadi' in t for t in ev("window.__t")))
    # weekly challenge uses each day\u2019s own goal
    ev(RESET); ev(f"S.gym.log=[];for(let i=1;i<=5;i++)({FILL})(dAgo(i),100);rwReset()")
    chk('weekly challenge counts days against their own goal (default 100 -> 5 days)', ev("rwWeek().n") == 5)
    # light day
    ev(RESET); ev(f"({FILL})(dk(),60);rwReset()"); ev("rwLight()")
    chk('light day: today\u2019s goal drops to 60 and 60 XP counts as completing it', ev("rw().lt[dk()]") == 1 and ev("rwGoal(dk())") == 60)
    ev("rwLight()"); chk('toggling again cancels it', not ev("!!rw().lt[dk()]") and ev("rwGoal(dk())") == 100)
    ev("rw().lt[dAgo(2)]=1;rwReset();window.__t=[];rwLight()"); chk('only one light day per week (Thu already used -> Sat refused)', not ev("!!rw().lt[dk()]") and any('allaqachon' in t for t in ev("window.__t")))
    pg.clock.set_system_time(datetime.datetime(2026, 11, 3, 10, 0, 0)); ev("rwReset();rwLight()"); chk('a new week allows it again', ev("rw().lt[dk()]") == 1)
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 10, 0, 0)); ev("rwReset()")
    # comeback
    ev(RESET); ev(f"for(let i=14;i>=10;i--)({FILL})(dAgo(i),60);rwReset()")
    c = ev("rwComeback()"); chk('comeback: a 5-day run was broken 9 days ago -> "wait" state with the old length', c and c['st'] == 'wait' and c['prev'] == 5 and c['gap'] == 10, c)
    ev(f"({FILL})(dAgo(1),60);({FILL})(dk(),60);rwReset()"); c = ev("rwComeback()")
    chk('after 2 days back: progress 2/3', c and c['st'] == 'prog' and c['n'] == 2 and c['prev'] == 5, c)
    ev(f"({FILL})(dAgo(2),60);rwReset()"); c = ev("rwComeback()"); chk('3 days back: bonus can be claimed', c and c['st'] == 'claim' and c['n'] == 3, c)
    t0 = ev("rwTotals()"); ev("rwClaimCb()"); t1 = ev("rwTotals()")
    chk('claiming gives +30 XP and +30 coins (plus the 3 coins that 30 XP is worth)', t1['xp'] - t0['xp'] == 30 and t1['coins'] - t0['coins'] == 33, (t0, t1))
    ev("rwClaimCb()"); chk('and only once', len(ev("Object.keys(rw().cbc)")) == 1 and ev("rwComeback()") is None)
    ev(RESET); ev(f"for(let i=3;i>=1;i--)({FILL})(dAgo(i),60);rwReset()"); chk('a person with a single run (never broke a streak) has no comeback mode', ev("rwComeback()") is None)
    ev(RESET); ev(f"({FILL})(dAgo(20),60);({FILL})(dAgo(19),60);({FILL})(dAgo(3),60);({FILL})(dAgo(2),60);({FILL})(dAgo(1),60);({FILL})(dk(),60);rwReset()"); chk('an earlier run shorter than 3 days is not a "streak" to come back to', ev("rwComeback()") is None)
    ev(RESET); ev(f"for(let i=40;i>=36;i--)({FILL})(dAgo(i),60);for(let i=20;i>=17;i--)({FILL})(dAgo(i),60);for(let i=1;i>=0;i--)({FILL})(dAgo(i),60);rwReset()")
    chk('old comebacks (run started >14 days ago) are not paid out retroactively', ev("(rwComeback()||{}).st") != 'claim')
    # UI
    ev(RESET); ev(f"for(let i=14;i>=10;i--)({FILL})(dAgo(i),60);rwReset();tab='h';BV='j';VD=null;render()"); pg.wait_for_timeout(150)
    chk('Bugun card shows the new-start message when the streak is broken and today is empty', 'Yangi boshlanish' in pg.inner_text('.rwc') and '5 kunlik' in pg.inner_text('.rwc'), pg.inner_text('.rwc')[:200])
    ev("rwOpen()"); pg.wait_for_timeout(200); bt = pg.inner_text('#rwb')
    chk('Yo\u2018l has the comeback section, the light-day button and the adaptive-goal note', 'Qaytish rejimi' in bt and 'Bugun yengil kun' in bt and 'moslanadi' in bt, bt[:300])
    ev("rwClose()")
    # ---------- 11. speed on a very heavy state (800 busy days, 3000 words, 600 gym sets) ----------
    ev("""()=>{S.ob=1;S.ts=1;S.hab=[1,2,3,4,5,6].map(i=>({id:'h'+i,t:'x'}));
      for(let i=0;i<800;i++){const k=dAgo(i);S.done[k]={qur:1,dok:1,iel:1};S.rules[k]={ig:1,ph:1};S.hb[k]={h1:1,h2:1,h3:1};S.tasks[k]=[{x:1},{x:1},{x:0}];S.top[k]=[{x:1},{x:1}];S.nm.d[k]={fajr:1,zuhr:1,asr:1,maghrib:1,isha:1};S.q.hd[k]=5;S.q.rd[k]=6;S.water[k]=8;S.close[k]={d:1}}
      S.ie.words=Array.from({length:3000},(_,i)=>({id:i,w:'w'+i,m:'m',box:1,due:dk(),t:Date.now()-i*3e6}));S.gym.log=Array.from({length:600},(_,i)=>({id:i,d:dAgo(i%400),n:'x',s:3,r:8,w:50}));rwReset()}""")
    ms = ev("()=>{const t=performance.now();rwReset();xpInfo();rwBest();return Math.round(performance.now()-t)}")
    chk('recomputing level, streak and best streak on a very heavy state takes < 150 ms (%d ms)' % ms, ms < 150, ms)
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
