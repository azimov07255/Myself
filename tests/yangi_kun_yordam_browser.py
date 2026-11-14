import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Hozir nima qilay, brifing, soya bilan poyga, niyat va muhosaba, bog'. Soat: 2026-11-05 (payshanba) 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('kun', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.__xp={};window.dayPts=k=>({t:window.__xp[k]||0});window.__sp=[];window.__cx=0;window.__vo=[{name:'Ava',lang:'en-US'},{name:'Uzbek',lang:'uz-UZ'}];window.__tts={getVoices:()=>window.__vo,speak:u=>__sp.push(u),cancel:()=>{window.__cx++}};window.SpeechSynthesisUtterance=function(t){this.text=t};
      S.bl=[{id:'b2',t:'IELTS Listening',s:480,e:540,d:[0,1,2,3,4,5,6]},{id:'b3',t:'Maktab ishi',s:570,e:630,d:[0,1,2,3,4,5,6]},{id:'b4',t:'Hifz takror',s:840,e:900,d:[0,1,2,3,4,5,6]}];S.done={};
      S.hab=[{id:'h1',t:'Kitob o‘qish'},{id:'h2',t:'Suv ichish'},{id:'h3',t:'Zal'}];S.hb={};S.q.m={};S.q.ord=[];S.q.rs={};S.ie.words=[];S.ie.xd=[];S.ie.gm={};S.ie.xdr={};S.fl=[];S.bs=undefined;S.ny=undefined;S.rw={};rwReset();tab='h';BV='j';render()}""")
    chk('the top bar has a 🎯 "Hozir nima qilay?" button on every screen (next to ＋, search and settings)', ev("document.querySelectorAll('.tbar .tbb').length") == 4 and ev("!!document.querySelector('.tbar [aria-label=\"Hozir nima qilay\"]')"))
    pg.click('.tbar [aria-label="Hozir nima qilay"]'); pg.wait_for_timeout(120); t = pg.inner_text('#nwo')
    chk('it opens a sheet: today\u2019s XP/streak line, the time choices (5/15/30/60 min, 15 selected) and ONE suggestion with "Boshlash"', '🎯 Hozir nima qilay?' in t and 'Qancha vaqting bor?' in t and all(f'{m} daq' in t for m in (5, 15, 30, 60)) and ev("document.querySelector('#nwo .chip.on').textContent") == '15 daq' and 'Boshlash' in t and ev("document.querySelectorAll('#nwo .nwc').length") == 1)
    c0 = ev("NW.c[0]"); chk('the block you are in RIGHT NOW (09:30–10:30 "Maktab ishi") comes first, with the time window as the reason', c0['t'] == 'Maktab ishi' and c0['s'] == 100 and 'Hozir rejadagi vaqting: 09:30–10:30' in c0['w'] and c0['m'] <= 15, c0)
    ev("nwSet(5)"); chk('with only 5 minutes the active block is shortened to fit (it still comes first)', ev("NW.c[0].t") == 'Maktab ishi' and ev("NW.c[0].m") == 5)
    ev("()=>{S.done[dk()]={b3:1};S.q.m={113:1,112:1};S.q.ord=[113,112];S.q.rs={113:{box:0,due:dk(),last:dk(),weak:true},112:{box:1,due:dk(),last:dk()}};S.ie.xd=[{id:1,d:dk(),c:'grammar',w:'a',r:'b',n:'',box:0,due:dk(),ok:0,bad:0},{id:2,d:dk(),c:'grammar',w:'c',r:'d',n:'',box:1,due:dk(),ok:0,bad:0}];nwSet(15)}")
    c = ev("NW.c.map(x=>x.id)"); chk('after the block is done: the Qur‘an reviews that are due (a weak sura) come first; then the mistakes, boss weak points, habits, focus and a game follow, all within about 15 minutes', ev("NW.c[0].id") == 'quran' and ev("NW.c[0].s") == 90 and ev("SN[113]") in ev("NW.c[0].t") and 'xato' in c and any(x.startswith('boss') for x in c) and any(x.startswith('hab') for x in c) and 'oyin' in c, c)
    ev("nwSet(5)"); chk('with 5 minutes the 10-minute Qur‘an review is skipped for a 5-minute item (mistakes quiz)', ev("NW.c[0].id") == 'xato' and ev("NW.c.every(x=>x.m<=7)"))
    ev("nwSet(15)"); t1 = ev("NW.c[0].t"); pg.click('#nwo >> text=↻ Boshqa'); pg.wait_for_timeout(60); t2 = ev("document.querySelector('#nwo .nwc b').textContent"); chk('"↻ Boshqa" shows the next-best suggestion (and the others are listed below)', t1 != t2 and 'Boshqa variantlar' in pg.inner_text('#nwo'))
    ev("nwSet(15)"); pg.click('#nwo >> text=Boshlash'); pg.wait_for_timeout(100); chk('"Boshlash" closes the sheet and takes you there: the Qur‘an Takror tab', ev("tab") == 'q' and ev("QT") == 't' and ev("!document.getElementById('nwo')"))
    ev("()=>{tab='h';nwOpen();S.q.ord=[];S.q.m={};S.q.rs={};rwReset();nwSet(5)}"); c = ev("NW.c[0]"); chk('with nothing due, the mistakes quiz still leads (5 min)', c['id'] == 'xato'); ev("()=>{S.ie.xd=[];nwSet(5)}")
    ev("()=>{window.__xp[dk()]=0}"); pg.clock.set_system_time('2026-11-05T19:00:00'); ev("()=>{rwReset();nwSet(15)}"); t = pg.inner_text('#nwo')
    chk('in the evening with the daily goal not reached the sheet warns about the streak (XP still needed) and short items get a priority boost', 'seriyani saqlash uchun hali' in t and ev("NW.c[0].m") <= 15)
    ev("nwClose()"); pg.clock.set_system_time('2026-11-05T10:00:00'); chk('closing removes the sheet', ev("!document.getElementById('nwo')"))
    # brifing
    ev("()=>{S.done={};S.q.m={113:1};S.q.ord=[113];S.q.rs={113:{box:0,due:dk(),last:dk()}};S.ie.xd=[{id:1,d:dk(),c:'grammar',w:'a',r:'b',n:'',box:0,due:dk(),ok:0,bad:0}];S.ie.words=[{w:'cat',m:'mushuk',box:1,due:dk(),k:'m'}];rwReset()}"); t = ev("nbText()")
    chk('the briefing: greeting by time, the weekday, the next plan items with times, Qur‘an due count, words/mistakes waiting, the boss, the streak and a closing', t.startswith('Xayrli tong! Bugun payshanba.') and '14:00 da Hifz takror' in t and '09:30 da Maktab ishi' in t and 'ta suraning takrori kerak' in t and 'takrorni kutmoqda' in t and 'Hafta bossi' in t and 'Seriyang' in t and t.endswith('Bismillah, boshlaymiz.'), t)
    ev("()=>{nwOpen();nbSpeak()}"); sp = ev("__sp.map(u=>[u.text,u.voice&&u.voice.lang,u.lang])")
    chk('speaking: it prefers an Uzbek voice (uz-UZ) over others and says the briefing line by line', len(sp) >= 6 and all(x[1] == 'uz-UZ' and x[2] == 'uz-UZ' for x in sp) and sp[0][0].startswith('Xayrli tong'))
    ev("()=>{window.__vo=[{name:'Ava',lang:'en-US'},{name:'Turk',lang:'tr-TR'}];__sp.length=0;nbSpeak()}"); chk('without an Uzbek voice a Turkish voice is used (it reads Uzbek Latin well)', ev("__sp.length") >= 6 and ev("__sp[0].voice.lang") == 'tr-TR')
    ev("()=>{window.__vo=[{name:'Ava',lang:'en-US'}];__sp.length=0;__t=[];nbSpeak()}"); chk('with neither, a clear message and no speech (the text can still be read)', ev("__sp.length") == 0 and any('o‘zbekcha yoki turkcha ovoz topilmadi' in m for m in ev("__t")))
    ev("()=>{window.__vo=[{name:'Uzbek',lang:'uz-UZ'}];__cx=0;nbStop()}"); chk('"⏹ To‘xtatish" cancels the speech', ev("__cx") >= 1); ev("nwClose()")
    # soya
    ev("""()=>{window.__xp={'2026-10-19':200,'2026-10-20':150,'2026-10-21':100,'2026-10-22':50,'2026-10-23':100,'2026-10-25':100,'2026-10-26':100,'2026-10-27':100,'2026-10-28':100,'2026-10-29':100,'2026-11-02':150,'2026-11-03':100,'2026-11-04':120,'2026-11-05':60};tab='m';MQV='o';render()}""")
    pg.wait_for_timeout(100); s = ev("srState()"); t = pg.inner_text('#app')
    chk('the shadow is your BEST of the last 8 weeks (week of Oct 19: 700 XP), not the current week; cumulative by weekday: 200, 350, 450, 500, 600, 600, 700', s['best']['wk'] == '2026-10-19' and s['best']['tot'] == 700 and s['sh'] == [200, 350, 450, 500, 600, 600, 700], s['sh'])
    chk('you: 150, 250, 370, 430 so far (Mon–Thu) and 70 XP behind the shadow; the card says how much to catch up today', s['cu'][:4] == [150, 250, 370, 430] and s['cu'][4] is None and s['diff'] == -70 and '👣 Soyadan 70 XP orqadasan' in t and 'eng yaxshi haftang: 700 XP' in t)
    chk('the chart has 7 day columns; future days show no "you" bar', ev("document.querySelectorAll('#app .srk').length") == 7 and ev("document.querySelectorAll('#app .sry.srn').length") == 3)
    ev("()=>{window.__xp['2026-11-05']=140;rwReset();render()}"); pg.wait_for_timeout(80); chk('ahead of the shadow: "🔥 Soyadan 10 XP oldindasan"', '🔥 Soyadan 10 XP oldindasan' in pg.inner_text('#app'))
    ev("()=>{window.__xp={'2026-11-02':100};render()}"); pg.wait_for_timeout(80); chk('with no earlier week to race against, the card is not shown (nothing to compare)', 'Soya bilan poyga' not in pg.inner_text('#app'))
    # niyat
    ev("()=>{S.ny=undefined;S.hb={};S.hb[dk()]={h1:true};window.__xp={};rwReset();tab='m';MQV='k';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the "🌙 Niyat va muhosaba" card: an intention box with ready phrases, the status chip, the evening reflection and the weekly review', '🌙 Niyat va muhosaba' in t and 'niyat yo‘q · muhosaba yo‘q' in t and 'Vaqtimni to‘g‘ri ishlataman' in t and 'Kechki muhosaba' in t and 'Haftalik muhosaba (0/7 niyat · 0/7 muhosaba)' in t)
    pg.click('#app .goal >> text=Hifzni takrorlayman'); pg.wait_for_timeout(80); chk('a ready phrase becomes today\u2019s intention and the chip says "niyat ✓"', ev("S.ny.d[dk()].n") == 'Hifzni takrorlayman' and 'niyat ✓' in pg.inner_text('#app'))
    ev("()=>{const i=document.getElementById('nyn');i.value='  '+'x'.repeat(300)+'  ';i.dispatchEvent(new Event('change'))}"); chk('typing saves on leaving the box, trimmed and cut to 200 characters', len(ev("S.ny.d[dk()].n")) == 200)
    ev("()=>{document.querySelector('#app section[aria-label=\"Niyat va muhosaba\"] details.sd').open=true}"); chk('the reflection offers chips from today: finished habits for "good", unfinished for "lacking"', ev("[...document.querySelector('#app section[aria-label=\"Niyat va muhosaba\"] details.sd').querySelectorAll('.chip')].map(c=>c.textContent)") == ['+ Kitob o‘qish', '+ Suv ichish', '+ Zal'])
    ev("nyAdd('y','Kitob o‘qish')"); ev("nyAdd('y','Kitob o‘qish')"); ev("nyAdd('y','Hifz')"); chk('adding chips appends with "; " and never twice', ev("S.ny.d[dk()].y") == 'Kitob o‘qish; Hifz')
    ev("nyDone()"); chk('"Muhosabani saqlash" marks the reflection done (chip "muhosaba ✓")', ev("S.ny.d[dk()].ok") == 1 and 'muhosaba ✓' in pg.inner_text('#app'))
    ev("()=>{S.ny.d={'2026-11-01':{n:'a',e:'Telefon; Uyqu'},'2026-11-02':{n:'b',e:'telefon'},'2026-11-03':{e:'Telefon; kech yotish',y:'x',ok:1},'2026-11-05':{n:'c'}};render()}"); W = ev("nyWeek()")
    chk('the weekly review counts days with an intention (3/7) and a reflection (3/7) and flags what keeps coming back (“telefon” 3 times; case ignored)', W['n'] == 3 and W['m'] == 3 and W['rep'][0] == ['telefon', 3], W)
    ev("()=>{S.ny.d={};for(let i=0;i<80;i++){const d=new Date('2026-08-01T12:00');d.setDate(d.getDate()+i);S.ny.d[d.toLocaleDateString('sv')]={n:'x'}}nySet('n','y')}"); chk('only the last 60 days are kept', len(ev("Object.keys(S.ny.d)")) <= 61)
    ev("()=>{S.ny.d={};S.ny.d[dk()]={n:'<img src=x onerror=alert(1)>',y:'<b>x</b>'};render()}"); pg.wait_for_timeout(60); chk('texts are escaped (no HTML runs)', ev("document.querySelectorAll('#app .goal img').length") == 0)
    # bog'
    ev("""()=>{S.hab=[{id:'h1',t:'Kitob'},{id:'h2',t:'Suv'},{id:'h3',t:'Zal'}];S.hb={};for(let i=0;i<30;i++){const k=dAgo(i);S.hb[k]={h1:true};if(i<10)S.hb[k].h2=true}S.q.ord=[1,2];S.q.m={1:20,2:3};S.ie.words=Array.from({length:23},(_,i)=>({w:'w'+i,m:'m',box:4,due:dk(),k:'m'}));window.__xp={};tab='m';MQV='b';render()}""")
    pg.wait_for_timeout(100); st = ev("[...document.querySelectorAll('#app .gdt')].map(e=>+e.dataset.st)")
    chk('one tree per habit; its stage follows the last-30-day consistency: every day (100%) → flowering tree 4; 10 of 30 (33%) → young tree 2; none → seedling 0', st == [4, 2, 0], st)
    chk('a habit with no activity in the last 7 days is only "resting": dimmed (never removed or shamed)', ev("document.querySelectorAll('#app .gdt')[2].getAttribute('opacity')") == '.5' and ev("document.querySelector('#app [aria-label=\"Bog‘im\"]').textContent.includes('dam olmoqda')"))
    chk('hifz fruit: 23 memorized pages → 4 fruits (1 per 5 pages); words: 23 learned → 5 flowers (1 per 5 words)', ev("document.querySelectorAll('#app .gdf').length") == 4 and ev("document.querySelectorAll('#app .gdw').length") == 5 and '23 bet' in pg.inner_text('#app') and '23 ta' in pg.inner_text('#app'))
    chk('the picture is described for screen readers and the chip summarizes it', 'ta odat daraxti' in ev("document.querySelector('#app svg[role=img]').getAttribute('aria-label')") and '3 daraxt · 4 meva · 5 gul' in pg.inner_text('#app'))
    ev("()=>{S.q.ord=[1];S.q.m={1:900};S.ie.words=Array.from({length:900},(_,i)=>({w:'w'+i,m:'m',box:5,due:dk(),k:'m'}));render()}"); pg.wait_for_timeout(80); chk('fruits and flowers are capped (40 and 48) so the picture never overflows', ev("document.querySelectorAll('#app .gdf').length") <= 40 and ev("document.querySelectorAll('#app .gdw').length") == 48)
    sky = {}
    for h, want in ((2, 'night'), (6, 'dawn'), (10, 'day'), (18, 'dusk')):
        pg.clock.set_system_time('2026-11-05T%02d:00:00' % h); ev("render()"); pg.wait_for_timeout(50); sky[h] = ev("document.querySelector('#app svg[role=img]').dataset.sky")
    chk('the sky follows the hour: night / dawn / day / dusk', sky == {2: 'night', 6: 'dawn', 10: 'day', 18: 'dusk'}, sky)
    pg.clock.set_system_time('2026-11-05T14:00:00'); ev("()=>{window.__xp={};rwReset();render()}"); pg.wait_for_timeout(60); cl = ev("document.querySelectorAll('#app svg[role=img] ellipse').length"); ev("()=>{window.__xp[dk()]=80;rwReset();render()}"); pg.wait_for_timeout(60)
    chk('a cloudy sky only when nothing was done by the afternoon; with activity it is clear', cl >= 3 and ev("document.querySelectorAll('#app svg[role=img] ellipse').length") == 0); pg.clock.set_system_time('2026-11-05T10:00:00')
    ev("()=>{S.hab=[];S.q.ord=[];S.q.m={};S.ie.words=[];render()}"); pg.wait_for_timeout(60); chk('with no habits, hifz or words the garden still draws and invites you to add a habit (no crash)', 'Odat qo‘shsang daraxt o‘sa boshlaydi' in pg.inner_text('#app') and ev("!!document.querySelector('#app svg[role=img]')"))
    bad = []
    ev("()=>{S.hab=[{id:'h1',t:'Kitob'},{id:'h2',t:'Suv'}];S.hb={};S.hb[dk()]={h1:true};S.q.ord=[1];S.q.m={1:20};window.__xp={'2026-10-19':200,'2026-11-02':100};S.ny.d[dk()]={n:'Uzun niyat '.repeat(12)}}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='m';MQV='b';render();nwOpen()}", [ui, th]); pg.wait_for_timeout(60)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1 && document.querySelector('#nwo .nws').scrollWidth<=document.querySelector('#nwo .nws').clientWidth+1"): bad.append(ui + th)
            ev("nwClose()")
    chk('the sheet, shadow race, reflection and garden fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
