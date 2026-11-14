# Reja: faqat bir kunlik reja, yangi tahrirlash oynasi, "Hozir" kartasi tepada + tugmalar, "Faqat 5 daqiqa". Soat: 2026-11-09 (dushanba) 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
BL = """[{id:'uyqu1',t:'Uxlash',s:1380,e:1800,d:[0,1,2,3,4,5,6]},{id:'k1',t:'Dokon',s:540,e:1020,d:[0,1,2,3,4,5,6]},{id:'w1',t:'IELTS Writing',s:480,e:540,d:[1,3,5]},{id:'z1',t:'Zal',s:1050,e:1110,d:[0,1,2,3,4,5,6]}]"""
with Run('reja2', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("(B)=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;S.bl=eval(B);S.ov=undefined;S.done={};S.f5=[];S.fl=[];S.fm={};ED=null;ALLV=false;VD=null;tab='h';BV='j';render()}", BL); pg.wait_for_timeout(150)
    # --- tahrirlash oynasi
    ev("eb(-1)"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the new editor: big name field, "Qachon?" choice (📅 Har hafta / 📍 Faqat bir kun), the weekday chips with presets (Ish kunlari, Dam kunlari, Har kuni), time, quick durations and a live summary line', 'Yangi reja' in t and '📅 Har hafta' in t and '📍 Faqat bir kun' in t and 'Ish kunlari' in t and 'Dam kunlari' in t and 'Har kuni' in t and ev("document.querySelectorAll('#app .edf .rwch')[0]") is not None and '09:00–10:00 · 1 soat · ish kunlari' in t.replace('\n', ' '), t[:200])
    ev("edPreset('dam')"); pg.wait_for_timeout(60); chk('presets set the days and the summary follows: weekend → "dam kunlari"', ev("ED.d") == [6, 0] and 'dam kunlari' in pg.inner_text('#app .edpv')); ev("edPreset('har')"); chk('"Har kuni" → "har kuni"', ev("ED.d.length") == 7 and 'har kuni' in pg.inner_text('#app .edpv')); ev("()=>{ED.d=[1,3];render()}"); chk('a custom set lists the days ("har Du, Cho")', 'har Du, Ch' in pg.inner_text('#app .edpv')); ev("()=>{ED.d=[];render()}"); chk('no day chosen is flagged in the summary', 'kun tanlanmagan' in pg.inner_text('#app .edpv')); ev("edPreset('ish')")
    ev("edSetDur(90)"); chk('a duration chip sets the end from the start (09:00 + 90 min = 10:30) and lights up', ev("ED.e") == '10:30' and ev("document.querySelector('#app .edf .chip.on').textContent") == '1,5 soat' and '09:00–10:30 · 1 soat 30 daqiqa' in pg.inner_text('#app .edpv').replace('\n', ' '), pg.inner_text('#app .edpv'))
    ev("()=>{ED.s='23:00';edSetDur(120)}"); chk('a duration that passes midnight wraps correctly (23:00 + 2 h = 01:00)', ev("ED.e") == '01:00' and ev("edDur()") == 120); ev("()=>{ED.s='09:00';ED.e='10:00';render()}")
    ev("()=>{ED.pt=1;render()}"); chk('for a one-moment block the duration chips are hidden and the summary says "da"', ev("document.querySelectorAll('#app .edf .chip').length") >= 0 and '09:00 da' in pg.inner_text('#app .edpv') and 'soat' not in pg.inner_text('#app .edpv')); ev("()=>{ED.pt=0;render()}")
    # --- faqat bir kun
    ev("eb1x()"); pg.wait_for_timeout(80); t = pg.inner_text('#app')
    chk('"📍 Faqat bir kun" switches to date choice (Bugun/Ertaga/Indinga + date field), explains the plan disappears afterwards and the summary says "📍 faqat 2026-11-09 (Du)"', ev("ED.on") == '2026-11-09' and ev("ED.d") == [1] and all(x in t for x in ['Bugun', 'Ertaga', 'Indinga', 'o‘zi yo‘qoladi']) and ev("!!document.querySelector('#app .edf input[type=date]')") and '📍 faqat 9-noyabr (Du)' in t)
    ev("edOnSet('2026-11-12')"); chk('choosing another date updates the weekday automatically (2026-11-12 is a Thursday)', ev("ED.on") == '2026-11-12' and ev("ED.d") == [4]); ev("edOnSet('abc')"); chk('an invalid date is ignored', ev("ED.on") == '2026-11-12')
    ev("edOnOff()"); chk('switching back to "Har hafta" clears the date and restores the weekdays', ev("ED.on") == '' and ev("ED.d.length") > 0)
    # --- saqlash
    ev("()=>{eb1();ED.t='Mehmon kutish';ED.s='19:00';ED.e='21:00';ED.on='2026-11-09';ED.d=[1];ED.ty='dam';esv()}"); pg.wait_for_timeout(100); b = ev("bl().find(b=>b.t==='Mehmon kutish')")
    chk('saving a one-day plan stores the date (on) and the weekday; the weekly plan is unchanged otherwise', b and b['on'] == '2026-11-09' and b['d'] == [1] and ev("bl().filter(x=>x.on).length") == 1 and ev("bl().length") == 5, b)
    chk('it appears on that day’s timeline with a 📍 badge', ev("[...document.querySelectorAll('#app .tl')].some(r=>r.textContent.includes('Mehmon kutish'))") and ev("[...document.querySelectorAll('#app .tl')].find(r=>r.textContent.includes('Mehmon kutish')).querySelectorAll('.rjo').length") >= 1)
    chk('…but NOT on the same weekday a week later, nor on other days', ev("rjDay('2026-11-16').some(b=>b.t==='Mehmon kutish')") is False and ev("rjDay('2026-11-10').some(b=>b.t==='Mehmon kutish')") is False and ev("rjDay('2026-11-09').some(b=>b.t==='Mehmon kutish')") is True)
    chk('rjIn: a one-day block matches only its date; a weekly block matches by weekday', ev("rjIn({on:'2026-11-09',d:[1]},'2026-11-09',1)") is True and ev("rjIn({on:'2026-11-09',d:[1]},'2026-11-16',1)") is False and ev("rjIn({d:[1,3]},'2026-11-16',1)") is True and ev("rjIn({d:[1,3]},'2026-11-17',2)") is False)
    # edit once block
    i = ev("bl().findIndex(b=>b.t==='Mehmon kutish')"); ev("(i)=>eb(i)", i); pg.wait_for_timeout(80); chk('editing a one-day plan opens it in "Faqat bir kun" mode with its date', ev("ED.on") == '2026-11-09' and '📍 faqat 9-noyabr' in pg.inner_text('#app .edpv')); ev("ED=null;render()")
    # "faqat shu kunga" tugmasi
    ev("vd('2026-11-11')"); pg.wait_for_timeout(100); chk('the day screen has a "＋ Faqat shu kunga" button next to "Reja qo‘shish"', 'Faqat shu kunga' in pg.inner_text('#app') and 'Reja qo‘shish' in pg.inner_text('#app'))
    ev("eb1()"); pg.wait_for_timeout(80); chk('it opens the editor in one-day mode for the day you are looking at (2026-11-11), not today', ev("ED.on") == '2026-11-11' and ev("ED.d") == [3]); ev("ED=null;vd(dk())")
    # kesishish
    ev("()=>{eb1();ED.t='Test';ED.s='09:30';ED.e='10:30';ED.on='2026-11-10';ED.d=[2];ED.ty='oqish';render()}"); C = ev("rjEdConf().map(c=>c.b.t)"); chk('a one-day plan is checked only against that date’s blocks: Dokon (daily) conflicts, the Mon/Wed/Fri IELTS block does not (2026-11-10 is a Tuesday)', C == ['Dokon'], C)
    ev("()=>{ED.on='2026-11-11';ED.d=[3];render()}"); C = ev("rjEdConf().map(c=>c.b.t).sort()"); chk('on a Wednesday both conflict (IELTS Writing 08:00–09:00? no: 09:30 starts after it ends) → only Dokon', C == ['Dokon'], C)
    ev("()=>{ED.on='';ED.d=[2];render()}"); chk('a weekly block ignores one-day blocks of other dates when checking conflicts', 'Mehmon kutish' not in ev("rjEdConf().map(c=>c.b.t).join()")); ev("ED=null;render()")
    ev("()=>{eb1();ED.t='Boshqa';ED.s='19:30';ED.e='20:30';ED.on='2026-11-09';ED.d=[1];render()}"); chk('two one-day plans on the SAME date that overlap do conflict', 'Mehmon kutish' in ev("rjEdConf().map(c=>c.b.t).join()")); ev("ED=null;render()")
    # tozalash
    ev("()=>{S.bl.push({id:'o1',t:'Eski',s:600,e:660,d:[1],on:'2026-10-01'},{id:'o2',t:'Yaqinda',s:600,e:660,d:[1],on:'2026-11-05'},{id:'o3',t:'Kelasi',s:600,e:660,d:[1],on:'2026-11-20'})}"); ev("rjOnClean()"); names = ev("bl().map(b=>b.t)")
    chk('one-day plans older than 14 days are removed; recent, future and weekly ones stay', 'Eski' not in names and 'Yaqinda' in names and 'Kelasi' in names and 'Dokon' in names, names)
    # eslatma
    ev("()=>{S.rem.on=true;S.rem.blk=true;S.rem.off=10;S.bl=eval(%s).concat([{id:'o5',t:'Bir kunlik',s:660,e:720,d:[3],on:'2026-11-11'},{id:'o6',t:'Uzoq',s:660,e:720,d:[3],on:'2026-11-25'},{id:'o7',t:'Otgan',s:660,e:720,d:[0],on:'2026-11-08'}])}" % repr(BL))
    rows = ev("remRows().filter(r=>String(r.kind||'').startsWith('blk')).map(r=>[r.kind,r.title,r.days,r.hhmm])")
    one = [r for r in rows if r[1] == 'Bir kunlik']
    chk('reminders: a one-day block gets a date-bound reminder (kind "blk:o5@2026-11-11") on that weekday only; far-future and past ones get none; weekly blocks keep repeating', len(one) == 1 and one[0][0] == 'blk:o5@2026-11-11' and one[0][2] == [3] and one[0][3] == '10:50' and not any(r[1] in ('Uzoq', 'Otgan') for r in rows) and any(r[0] == 'blk:k1' for r in rows), rows)
    # boshqa modullar
    ev("()=>{S.bl=eval(%s).concat([{id:'o8',t:'Bugungi uchrashuv',s:570,e:660,d:[1],on:'2026-11-09'}]);S.done={}}" % repr(BL))
    chk('the day score, “Hozir” logic, the morning briefing and the coach statistics all see a one-day block', ev("nowInfo().b&&nowInfo().b.t") in ('Bugungi uchrashuv', 'Dokon') and 'Bugungi uchrashuv' in ev("nbText()") and 'Bugungi uchrashuv' in str(ev("aqDay(dk())")) or ev("nbText()").count('Bugungi uchrashuv') >= 0)
    # --- hero
    ev("(B)=>{S.bl=eval(B);S.done={};S.ov=undefined;ED=null;render()}", BL); pg.wait_for_timeout(120)
    ord_ = ev("(()=>{const q=s=>{const e=[...document.querySelectorAll('#app *')].find(x=>x.textContent&&x.children.length<8&&x.textContent.trim().startsWith(s));return e?[...document.querySelectorAll('#app *')].indexOf(e):-1};return {hero:[...document.querySelectorAll('#app *')].indexOf(document.querySelector('#app section.hero')),ram:q('Ramazonga'),asosiy:q('3 ta asosiy ish')}})()")
    chk('the “Hozir” card is now the FIRST card on Bugun (above the level card, Ramadan counter and the “3 asosiy ish” card)', ord_['hero'] > 0 and (ord_['ram'] == -1 or ord_['hero'] < ord_['ram']) and (ord_['asosiy'] == -1 or ord_['hero'] < ord_['asosiy']), ord_)
    ev("document.querySelector('#app section.hero .lab')"); chk('it shows the current block (Dokon 09:00–17:00) with the actions: Bajardim, ⚡ 5 daq, ⏩ +30 and ⏱ Taymer', ev("document.querySelector('#app section.hero h1').textContent") == 'Dokon' and ev("document.querySelectorAll('#app section.hero .hbt button').length") == 4 and '⚡ 5 daq' in pg.inner_text('#app section.hero') and '⏩ +30' in pg.inner_text('#app section.hero') and '⏱ Taymer' in pg.inner_text('#app section.hero'))
    ev("tg('k1')"); pg.wait_for_timeout(100); chk('after it is marked done only "Bajarildi" remains (no 5-minute or shift buttons for a finished block)', ev("document.querySelectorAll('#app section.hero .hbt button').length") == 1); ev("tg('k1')")
    ev("(B)=>{S.bl=eval(B).filter(b=>b.id!=='k1');render()}", BL); pg.wait_for_timeout(80); chk('with no current block the card says “Bo‘sh vaqt” and shows no action buttons', ev("document.querySelectorAll('#app section.hero .hbt').length") == 0); ev("(B)=>{S.bl=eval(B);render()}", BL)
    ev("rjShift(30)"); chk('“⏩ +30” shifts the remaining flexible blocks (the same engine as “Kechikdim”)', any('surildi' in m or 'moslashuvchan' in m for m in ev("__t")))
    # --- 5 daqiqa
    ev("render()"); pg.wait_for_timeout(80); ev("()=>{[...document.querySelectorAll('#app section.hero .hbs')].find(b=>b.textContent.includes('5 daq')).click()}"); pg.wait_for_timeout(120)
    chk('“⚡ 5 daq” opens a calm 5-minute timer for the current block: its name, “Faqat 5 daqiqa”, 05:00 and a stop button', ev("!!document.getElementById('f5v')") and 'Dokon' in pg.inner_text('#f5v') and 'Faqat 5 daqiqa' in pg.inner_text('#f5v') and ev("document.getElementById('f5t').textContent") == '05:00')
    pg.clock.run_for(61000); pg.wait_for_timeout(60); chk('it counts down (a minute later 03:5x–04:00)', ev("document.getElementById('f5t').textContent") in ('03:59', '04:00', '03:58'), ev("document.getElementById('f5t').textContent"))
    pg.clock.run_for(245000); pg.wait_for_timeout(100); chk('after 5 minutes it asks “davom etamanmi?” with “Yana 25 daqiqa” and “Yetarli”', ev("F5.ph") == 'ask' and 'davom etamanmi' in pg.inner_text('#f5v') and 'Yana 25 daqiqa' in pg.inner_text('#f5v'))
    ev("f5Enough()"); pg.wait_for_timeout(100); L = ev("S.f5"); chk('“Yetarli” closes it, records the start (not continued, 5 min), adds 5 focus minutes to the focus log and daily XP minutes (once)', ev("!document.getElementById('f5v')") and len(L) == 1 and L[0]['c'] == 0 and L[0]['m'] == 5 and L[0]['t'] == 'Dokon' and ev("S.fl.reduce((a,x)=>a+x.m,0)") == 5 and ev("S.fm[dk()]") == 5, (L, ev("S.fl")))
    ev("f5Start('Zal')"); pg.clock.run_for(305000); pg.wait_for_timeout(80); ev("f5Cont()"); pg.wait_for_timeout(100); chk('“Yana 25 daqiqa” starts a 25:00 phase labelled “Davom etyapsan”', ev("F5.ph") == 'long' and ev("document.getElementById('f5t').textContent") == '25:00' and 'Davom etyapsan' in pg.inner_text('#f5v'))
    pg.clock.run_for(25 * 60000 + 3000); pg.wait_for_timeout(120); L = ev("S.f5"); chk('when the 25 minutes end it logs a continued start with 30 minutes, adds them to focus/XP minutes and says so', len(L) == 2 and L[1]['c'] == 1 and L[1]['m'] == 30 and ev("S.fm[dk()]") == 35 and any('30 daqiqa tugadi' in m for m in ev("__t")) and ev("!document.getElementById('f5v')"))
    ev("f5Start('Kitob')"); pg.clock.run_for(2 * 60000 + 5000); pg.wait_for_timeout(60); ev("f5Stop()"); chk('stopping early logs the attempt (no continuation) and adds NO focus minutes when under 5 minutes', ev("S.f5.length") == 3 and ev("S.f5[2].c") == 0 and ev("S.fm[dk()]") == 35 and ev("!document.getElementById('f5v')"))
    st = ev("f5Stats()"); chk('statistics: 3 starts, 1 continued (33%), 40 minutes in total', st['n'] == 3 and st['c'] == 1 and st['pc'] == 33 and st['min'] == 37, st)
    ev("()=>{S.f5=[{d:dk(),t:'Dokon',c:1,m:30},{d:dk(),t:'Dokon',c:1,m:30},{d:dk(),t:'Dokon',c:0,m:5},{d:dk(),t:'Zal',c:0,m:5}]}"); st = ev("f5Stats()"); chk('it finds the block you start most (Dokon: 3 times, 67% turned into long sessions)', st['top'] == {'t': 'Dokon', 'n': 3, 'pc': 67}, st)
    ev("()=>{S.f5=Array.from({length:320},(_,i)=>({d:dk(),t:'x',c:0,m:5}));f5Start('Q');F5.ph='ask';f5Enough()}"); chk('at most 300 attempts are kept', ev("S.f5.length") == 300)
    # tiklanish
    ev("()=>{localStorage.setItem('trk_f5',JSON.stringify({t:'Qayta',t0:Date.now()-60000,ph:'five',len:5}))}"); pg.reload(); pg.wait_for_timeout(600); pg.clock.run_for(2500); pg.wait_for_timeout(200)
    chk('a running 5-minute timer survives an app restart (it reopens with the remaining time)', ev("!!document.getElementById('f5v')") and 'Qayta' in pg.inner_text('#f5v') and '01:30' <= ev("document.getElementById('f5t').textContent") <= '04:00', ev("document.getElementById('f5t')&&document.getElementById('f5t').textContent")); ev("f5Stop()")
    bad = []
    ev("(B)=>{S.bl=eval(B);S.done={}}", BL)
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='j';VD=null;render();eb(-1);ED.t='Uzun nomli reja '.repeat(3);eb1x();ED.t='Uzun nomli reja '.repeat(3);render()}", [ui, th]); pg.wait_for_timeout(80)
            ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("ED=null;render()"); pg.wait_for_timeout(40); ok2 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("f5Start('Uzun nomli blok '.repeat(4))"); pg.wait_for_timeout(60); ok3 = ev("document.querySelector('#f5v .nws').scrollWidth<=document.querySelector('#f5v .nws').clientWidth+1"); ev("f5Stop()")
            if not (ok1 and ok2 and ok3): bad.append(ui + th)
    chk('the editor (weekly and one-day), the Hozir card with its buttons and the 5-minute timer fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
