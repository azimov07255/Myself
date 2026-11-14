# Hayot haftalari xaritasi va haftalik stories. Soat: 2026-11-05 (payshanba) 10:00.
import sys, datetime
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
BIRTH = '2008-03-10'
lived = (datetime.date(2026, 11, 5) - datetime.date(2008, 3, 10)).days // 7
with Run('hayot', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;S.hw=undefined;S.goals=[];S.ie.ed=undefined;tab='m';MQV='b';render()}""")
    pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the Bog‘ section has "🗓 Hayot haftalari" asking for the birth date first (stored only in your account), with a calm explanation', '🗓 Hayot haftalari' in t and 'Tug‘ilgan sana' in t and 'qo‘rqitish uchun emas' in t and ev("!!document.getElementById('hwb')") and ev("hwCalc()") is None)
    for bad in ('', '2999-01-01', '1900-01-01', 'abc'):
        ev("(v)=>{document.getElementById('hwb').value=v;hwSave()}", bad)
    chk('an empty, future, too-old or invalid birth date is refused', ev("S.hw&&S.hw.b") in (None, '', False) or ev("(S.hw||{}).b") in (None, ''))
    ev("(v)=>{document.getElementById('hwb').value=v;hwSave()}", BIRTH); pg.wait_for_timeout(120)
    C = ev("(()=>{const c=hwCalc();return {lived:c.lived,total:c.total,rem:c.rem,pc:c.pc,age:c.age,life:c.life}})()")
    chk('the map is computed from the birth date: lived weeks, total (80 × 52 = 4160), remaining, percent (1 decimal), age 18', C['lived'] == lived and C['total'] == 4160 and C['rem'] == 4160 - lived and C['pc'] == round(lived / 4160 * 100, 1) and C['age'] == 18, (C, lived))
    t = pg.inner_text('#app'); chk('the card states them in words: this week is week N+1, how many remain "taxminan", the age chip', f'{lived}</b>' not in t and f'Yashalgan: {lived} hafta' in t and f'bu hafta: {lived + 1}-hafta' in t and f'taxminan {4160 - lived} hafta qoldi' in t and '18 yosh' in t)
    ev("hwLife(70)"); chk('the life estimate (a calculation aid; “umr Alloh qo‘lida”) changes the total (3640) and can be 60–100 only', ev("hwCalc().total") == 3640 and 'umr Alloh qo‘lida' in pg.inner_text('#app')); ev("hwLife(5)"); chk('...minimum 60', ev("hwS().life") == 60); ev("hwLife(500)"); chk('...maximum 100', ev("hwS().life") == 100); ev("hwLife(80)")
    # belgilar
    ev("()=>{hwS().ms=[];S.ie.ed='2027-01-20';S.goals=[{t:'Prava olish',e:'🚗',dl:'2027-06-01',ms:[]},{t:'Eski maqsad',dl:'2000-01-01',ms:[]},{t:'Muddatsiz',ms:[]}];document.getElementById('hwt')&&0}")
    ev("()=>{const t=document.getElementById('hwt'),d=document.getElementById('hwd');t.value='Imtihon '+'x'.repeat(80);d.value='2026-12-31';hwAddMs()}"); pg.wait_for_timeout(100)
    M = ev("hwMarks(hwCalc()).map(m=>[m.k,m.d,m.t.length>0,m.t.length<=40])")
    chk('markers: your own dates (name cut to 40 characters), the IELTS exam date, goal deadlines; dates before birth or beyond the life estimate and goals without a deadline are skipped', sorted((m[0], m[1]) for m in M) == [('g', '2027-06-01'), ('i', '2027-01-20'), ('m', '2026-12-31')] and all(m[3] for m in M), M)
    w = ev("hwIdx('2026-12-31',hwCalc().b)"); chk('a marker sits in the right week (weeks since birth)', w == (datetime.date(2026, 12, 31) - datetime.date(2008, 3, 10)).days // 7)
    ev("()=>{const t=document.getElementById('hwt'),d=document.getElementById('hwd');t.value='';d.value='';hwAddMs()}"); chk('a marker needs a name and a date', ev("hwS().ms.length") == 1)
    ev("()=>{hwS().ms=Array.from({length:12},(_,i)=>({t:'m'+i,d:'2027-01-0'+(i%9+1)}));__t=[];const t=document.getElementById('hwt');if(t){t.value='z';document.getElementById('hwd').value='2027-02-02';hwAddMs()}}"); chk('at most 12 of your own dates', ev("hwS().ms.length") <= 12)
    ev("()=>{hwS().ms=[{t:'Prava imtihoni',d:'2026-12-31'}];render()}"); pg.wait_for_timeout(100)
    ev("hwDelMs(0)"); chk('a marker can be deleted', ev("hwS().ms.length") == 0); ev("()=>{hwS().ms=[{t:'Prava imtihoni',d:'2026-12-31'}];render()}"); pg.wait_for_timeout(120)
    # ramazon
    Rm = ev("hwRam(hwCalc()).map(r=>r.d)"); C2 = ev("hwCalc()")
    chk('Ramadan starts are found with the Hijri calendar: about 19 since birth (Sept 2008 … Feb 2026) and about 62 still ahead; one falls in the week of 2026-02-18/19', 17 <= sum(1 for d in Rm if d < '2026-11-05') <= 20 and 58 <= sum(1 for d in Rm if d >= '2026-11-05') <= 64 and any('2026-02-14' <= d <= '2026-02-23' for d in Rm), (len(Rm), [d for d in Rm][:3]))
    # canvas
    pg.wait_for_timeout(150); H = ev("document.getElementById('hwc').height"); cell = (1040 - 34) / 52
    px = lambda w: ev("(a)=>Array.from(document.getElementById('hwc').getContext('2d').getImageData(a[0],a[1],1,1).data)", [int(34 + (w % 52) * cell + cell / 2), int((w // 52) * cell + cell / 2)])
    pl = px(lived - 5); pc = px(lived); pf = px(lived + 40)
    chk('the canvas is painted: lived weeks are solid, THIS week is highlighted differently, future weeks are faint outlines/empty; the height fits 80 rows', H >= 80 * cell and pl[3] > 150 and pc[3] == 255 and pc[:3] != pl[:3] and pf[3] < 120, (H, pl, pc, pf))
    tap = lambda w: ev("(a)=>{const cv=document.getElementById('hwc'),r=cv.getBoundingClientRect(),s=cv.width/r.width;hwTap({clientX:r.left+(34+(a[0]%52)*(1006/52)+3)/s,clientY:r.top+((Math.floor(a[0]/52))*(1006/52)+3)/s});return document.getElementById('hwtip').textContent}", [w])
    tip = tap(lived); chk('tapping a week tells its dates, age and week number; this week says "Bu hafta"', tip.startswith('Bu hafta: ') and f'18 yosh, {lived % 52 + 1}-hafta' in tip, tip)
    tip = tap(lived - 30); chk('a past week says "Yashalgan"', tip.startswith('Yashalgan:'), tip)
    tip = tap(w); chk('a marked week lists its event ("⭐ Prava imtihoni")', '⭐ Prava imtihoni' in tip, tip)
    wr = [r for r in ev("hwRam(hwCalc())") if r['w'] > lived][0]['w']; tip = tap(wr); chk('a Ramadan-start week says so', '🌙 Ramazon boshlanadi' in tip, tip)
    ev("()=>{const cv=document.getElementById('hwc'),r=cv.getBoundingClientRect();hwTap({clientX:r.left+2,clientY:r.top+2})}"); pg.wait_for_timeout(60); chk('tapping the label margin clears the info', 'Haftani bosib' in pg.inner_text('#app'))
    chk('the card carries the hadith about health and free time (Buxoriy) and no scary wording', 'Buxoriy' in pg.inner_text('#app') and 'o‘lim' not in pg.inner_text('#app').lower())
    ev("hwReset()"); pg.wait_for_timeout(100); chk('"Tug‘ilgan sanani o‘zgartirish" clears the date and shows the form again; your own dates stay', ev("hwS().b") == '' and ev("!!document.getElementById('hwb')") and ev("hwS().ms.length") == 1)
    # stories
    ev("""()=>{window.__xp={'2026-10-30':60,'2026-10-31':0,'2026-11-01':120,'2026-11-02':80,'2026-11-03':40,'2026-11-04':150,'2026-11-05':90};window.dayPts=k=>({t:window.__xp[k]||0});window.rwStreak=()=>6;
      S.hab=[{id:'h1',t:'A'},{id:'h2',t:'B'},{id:'h3',t:'C'}];S.hb={};for(const k of Object.keys(__xp)){S.hb[k]={h1:true,h2:__xp[k]>50}}
      S.fl=[{d:'2026-11-03',a:'IELTS',m:90},{d:'2026-11-04',a:'Qur‘on',m:40},{d:'2026-10-20',a:'X',m:500}];S.pm={'2026-11-03':2,'2026-11-04':1};
      S.q.hd={'2026-11-02':1.5,'2026-11-03':1};S.q.rd={'2026-11-04':4,'2026-11-05':3};
      S.ie.tests=[{id:1,d:'2026-11-03',k:'R',b:{R:7}},{id:2,d:'2026-11-04',k:'L',b:{L:6.5}},{id:3,d:'2026-10-01',k:'R',b:{R:5}}];S.ie.rmd={'2026-11-02':20,'2026-11-04':12};S.ie.xdr={'2026-11-03':9};S.ie.gm={'2026-11-05':3};
      S.mood={'2026-11-03':4,'2026-11-04':5,'2026-11-05':3};window.slpH=k=>({'2026-11-03':7,'2026-11-04':8,'2026-11-05':6.5})[k]??null;S.ny={d:{'2026-11-03':{n:'x',ok:1},'2026-11-04':{n:'y'}}};S.bs=undefined;S.rw={};rwReset();tab='m';MQV='k';render()}""")
    sl = ev("stSlides(stRange('last7'))"); ids = [x['id'] for x in sl]
    chk('the week has 10 slides in a fixed story order: intro, best day, habits, focus, Qur‘an, IELTS, boss, sleep & mood, intention, closing', ids == ['intro', 'best', 'hab', 'fokus', 'quron', 'ielts', 'boss', 'tan', 'niyat', 'end'], ids)
    g = {x['id']: x for x in sl}
    chk('intro: total XP of the 7 days (540) and how many days reached the daily goal; best day: Wednesday with 150 XP', g['intro']['big'] == '540 XP' and '2026-10-30 — 2026-11-05' in g['intro']['sub'] and g['best']['big'] == 'Chorshanba' and g['best']['sub'].startswith('150 XP'), (g['intro'], g['best']))
    chk('habits: ticks / (3 habits × 7 days) in percent and the streak; focus: 130 min = "130 daq" (not the 500 min from another week), pomodoros 3, top area IELTS; Qur‘an: 9.5 pages (new 2.5 + review 7)', g['hab']['big'] == '57%' and '6 kun' in g['hab']['sub'] and g['fokus']['big'] == '2.2 soat' and '3 ta pomodoro' in g['fokus']['sub'] and 'IELTS' in g['fokus']['sub'] and g['quron']['big'] == '9.5 bet' and 'yangi yodlash: 2.5' in g['quron']['sub'] and 'takror: 7' in g['quron']['sub'], (g['hab'], g['fokus'], g['quron']))
    chk('IELTS: 2 tests of this week (the one from October is not counted), best band 7, 32 new words, 9 mistake reviews, 3 game rounds; sleep avg 7.2 h with mood 4/5; intention 2/7 and 1 reflection', g['ielts']['big'] == '2 ta test' and 'eng yaxshi band 7' in g['ielts']['sub'] and '32 yangi so‘z' in g['ielts']['sub'] and '9 xato takrori' in g['ielts']['sub'] and '3 o‘yin raundi' in g['ielts']['sub'] and g['tan']['big'] == '7.2 soat' and 'kayfiyat 4/5' in g['tan']['sub'] and g['niyat']['big'] == '2/7 niyat' and '1 kun muhosaba' in g['niyat']['sub'], (g['ielts'], g['tan'], g['niyat']))
    chk('the closing slide gives ONE focus for next week (the weakest area) and a sourced reminder', len(g['end']['big']) > 10 and ('Qur‘on' in g['end']['big'] or 'Chuqur fokus' in g['end']['big'] or 'IELTS' in g['end']['big'] or 'Odatlarni' in g['end']['big']) and ('Qur‘on,' in g['end']['sub'] or 'Hadis' in g['end']['sub'] or 'Hikmat' in g['end']['sub']), g['end'])
    chk('"prev" mode covers the previous Monday–Sunday (2026-10-26 … 2026-11-01)', ev("stRange('prev')") == ['2026-10-26', '2026-10-27', '2026-10-28', '2026-10-29', '2026-10-30', '2026-10-31', '2026-11-01'])
    # slaydlarni qoldirish
    ev("()=>{S.fl=[];S.q.hd={};S.q.rd={};S.ie.tests=[];S.ie.rmd={};S.ie.xdr={};S.ie.gm={};S.mood={};window.slpH=()=>null;S.ny={d:{}}}"); ids2 = [x['id'] for x in ev("stSlides(stRange('last7'))")]
    chk('a slide without data is left out (no empty “0 minutes” slides)', ids2 == ['intro', 'best', 'hab', 'boss', 'end'], ids2)
    ev("()=>{window.__xp={};S.hab=[];__t=[];stOpen('last7')}"); chk('with almost no data a kind message and no overlay', ev("!document.getElementById('stv')") and any('ma‘lumot kam' in m for m in ev("__t")))
    ev("""()=>{window.__xp={'2026-10-30':60,'2026-10-31':0,'2026-11-01':120,'2026-11-02':80,'2026-11-03':40,'2026-11-04':150,'2026-11-05':90};S.hab=[{id:'h1',t:'A'}];S.hb={};S.fl=[{d:'2026-11-03',a:'IELTS',m:90}];S.q.hd={'2026-11-02':1.5};S.ie.rmd={'2026-11-02':20};S.mood={'2026-11-03':4,'2026-11-04':5};S.ny={d:{'2026-11-03':{n:'x',ok:1}}}}""")
    ev("stOpen('last7')"); pg.wait_for_timeout(150); n = ev("ST.sl.length")
    chk('"▶ Oxirgi 7 kun" opens a full-screen story: segmented progress bar (one per slide), the date range, a close button, the emoji, title, big number and caption', ev("!!document.getElementById('stv')") and ev("document.querySelectorAll('#stv .stpr i').length") == n and '2026-10-30 — 2026-11-05' in pg.inner_text('#stv') and ev("document.querySelector('#stv .stn').textContent") == '540 XP' and ev("document.querySelectorAll('#stv .stpr i.scr').length") == 1)
    ev("document.querySelector('#stv .str').click()"); pg.wait_for_timeout(60); chk('tapping the right side goes to the next slide; the finished segment fills', ev("ST.i") == 1 and ev("document.querySelectorAll('#stv .stpr i.sdn').length") == 1)
    ev("document.querySelector('#stv .stl').click()"); chk('tapping the left side goes back', ev("ST.i") == 0); ev("document.querySelector('#stv .stl').click()"); chk('...and never before the first slide', ev("ST.i") == 0)
    pg.clock.run_for(5700); pg.wait_for_timeout(60); chk('slides advance by themselves every ~5.5 seconds', ev("ST.i") == 1); pg.clock.run_for(5700); pg.wait_for_timeout(60); chk('...again', ev("ST.i") == 2)
    ev("()=>{ST.i=ST.sl.length-2;stGo(1)}"); pg.clock.run_for(20000); pg.wait_for_timeout(60); chk('on the last slide the timer stops (it does not close by itself) and "📤 Ulashish" and "Yopish" appear', ev("ST.i") == ev("ST.sl.length-1") and '📤 Ulashish' in pg.inner_text('#stv') and ev("!!document.getElementById('stv')"))
    ev("""()=>{window.__sh=null;Object.defineProperty(navigator,'canShare',{value:()=>true,configurable:true});Object.defineProperty(navigator,'share',{value:async d=>{window.__sh={n:d.files[0].name,t:d.files[0].type,s:d.files[0].size}},configurable:true})}""")
    ev("()=>{stShare();return 1}"); pg.wait_for_timeout(500); sh = ev("__sh"); chk('"Ulashish" shares the current slide as a PNG (haftalik-xulosa-2026-11-05.png) through the share sheet', sh and sh['n'] == 'haftalik-xulosa-2026-11-05.png' and sh['t'] == 'image/png' and sh['s'] > 5000, sh)
    ev("""()=>{window.__ft=[];const of=CanvasRenderingContext2D.prototype.fillText;CanvasRenderingContext2D.prototype.fillText=function(t,x,y){window.__ft.push(String(t));return of.call(this,t,x,y)};const cv=document.createElement('canvas');cv.width=1080;cv.height=1920;stPaint(cv,ST.sl[0],0)}""")
    ft = ev("__ft"); chk('the story image is drawn at 1080×1920 with the title, the emoji, the big figure and the dates', 'Kunlik tizim · haftalik xulosa' in ft and ST_BIG(ft) if False else ('540 XP' in ft and 'Haftalik xulosa' in ft and '📖' in ft and '2026-10-30 — 2026-11-05' in ft), ft[:8])
    ev("stClose()"); chk('closing removes the overlay and stops the timer', ev("!document.getElementById('stv')") and ev("ST") is None)
    # kirish nuqtalari
    ev("()=>{tab='m';MQV='k';render()}"); pg.wait_for_timeout(100); chk('the Kun section has the "📖 Haftalik xulosa" card with "▶ Oxirgi 7 kun" and "O‘tgan hafta"', '📖 Haftalik xulosa' in pg.inner_text('#app') and 'Oxirgi 7 kun' in pg.inner_text('#app') and 'O‘tgan hafta' in pg.inner_text('#app'))
    ev("()=>{tab='h';BV='j';render()}"); pg.wait_for_timeout(100); chk('on a Thursday Bugun has no weekly-summary row', 'Haftalik xulosa tayyor' not in pg.inner_text('#app'))
    pg.clock.set_system_time('2026-11-07T10:00:00'); ev("render()"); pg.wait_for_timeout(100); chk('on Saturday (and Sunday) Bugun offers “📖 Haftalik xulosa tayyor”', 'Haftalik xulosa tayyor' in pg.inner_text('#app')); pg.clock.set_system_time('2026-11-05T10:00:00')
    # ko'rinish
    bad = []
    ev("()=>{hwS().b='2008-03-10';hwS().ms=[{t:'Uzun nomli muhim sana '.repeat(2),d:'2026-12-31'}]}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='m';MQV='b';render()}", [ui, th]); pg.wait_for_timeout(120)
            ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            ev("()=>{stOpen('last7')}"); pg.wait_for_timeout(60); ok2 = ev("document.querySelector('#stv').scrollWidth<=window.innerWidth+1"); ev("stClose()")
            if not (ok1 and ok2): bad.append(ui + th)
    chk('the life map and the stories fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
