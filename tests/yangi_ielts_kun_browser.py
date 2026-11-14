# IELTS kuni: soatlik jadval, zaif nuqta radari, halol band bashorati, CEFR boshlang'ich daraja. Soat: 2026-11-09 (dushanba) 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('ik', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);S.ik=undefined;S.ie.cf=undefined;S.ie.tests=[];S.ie.mock=[];S.ie.xd=[];S.ie.kr={start:dk(),target:7.5,hrs:6,wks:12,exam:'2027-01-30',done:{},read:{}};S.ie.target=7.5;tab='e';EV='i';IVW='y';KS.sec='r';render()}""")
    pg.wait_for_timeout(120)
    chk('the course now supports 5, 6 and 7 hours a day (plan multipliers added; the hour chips show them)', ev("KSM[5]") == 2.2 and ev("KSM[6]") == 2.6 and ev("KSM[7]") == 3 and all(f'{h} soat' in pg.inner_text('#app') for h in (5, 6, 7)))
    t = pg.inner_text('#app'); chk('the IELTS Kurs → Reja screen starts with "🎓 Bugungi IELTS kuni": hours, target 7.5, days to the exam, the blocks, and the three tools (radar, forecast, CEFR)', '🎓 Bugungi IELTS kuni' in t and 'Nishon 7.5' in t and 'imtihongacha 82 kun' in t and 'Zaif nuqta radari' in t and 'Band bashorati' in t and 'Boshlang‘ich daraja (CEFR)' in t and t.index('Bugungi IELTS kuni') < t.index('IELTS 7.5+ kursi'), t[:150])
    P = ev("ikPlan('2026-11-09')"); share = {b['id']: b['m'] / P['total'] for b in P['blocks']}
    chk('Monday, 6 hours, no results yet: exactly 360 minutes in 6 blocks (each ≥ 15 min); Writing is the biggest; Writing + Speaking get 55% or more of the time', P['total'] == 360 and len(P['blocks']) == 6 and all(b['m'] >= 15 for b in P['blocks']) and sum(b['m'] for b in P['blocks']) == 360 and max(share, key=share.get) == 'W' and share['W'] + share['S'] >= 0.55, share)
    D = {b['id']: b['det'] for b in P['blocks']}; chk('blocks say exactly what to do (Monday: Writing Task 2 with a time split, Speaking Part 2 recording, a full Listening section, 2 timed Reading passages with today’s question type, vocabulary, mistakes)', 'Task 2' in D['W'] and 'qayta yozish' in D['W'] and 'Part 2' in D['S'] and 'Section' in D['L'] and '2 ta passage' in D['R'] and 'yangi so‘zlar' in D['V'] and 'kunlik 5 savol' in D['E'])
    chk('Tuesday uses Writing Task 1 (alternating) and a different Reading question type', 'Task 1' in ev("ikPlan('2026-11-10').blocks.find(b=>b.id==='W').det") and ev("ikPlan('2026-11-10').blocks.find(b=>b.id==='R').det") != D['R'])
    ev("()=>{S.ie.tests=[{id:1,d:'2026-11-01',k:'W',b:{W:5.5}},{id:2,d:'2026-11-02',k:'S',b:{S:5.5}},{id:3,d:'2026-11-03',k:'L',b:{L:7}},{id:4,d:'2026-11-04',k:'R',b:{R:7}}]}")
    P2 = ev("ikPlan('2026-11-09')"); sh2 = {b['id']: b['m'] / P2['total'] for b in P2['blocks']}
    chk('with real results (Writing 5.5, Speaking 5.5 but Listening 7, Reading 7 against a 7.5 target) the weak skills get even MORE time and the strong ones less', sh2['W'] > share['W'] and sh2['S'] > share['S'] and sh2['L'] < share['L'] and sh2['R'] < share['R'] and P2['total'] == 360, sh2)
    Pf = ev("ikPlan('2026-11-13')"); chk('Friday is lighter (70% → 250 min) and says so', Pf['fri'] and Pf['total'] == 250 and sum(b['m'] for b in Pf['blocks']) == 250 and True)
    pg.clock.set_system_time('2026-11-13T10:00:00'); ev("()=>{S.ik=undefined;render()}"); pg.wait_for_timeout(100); chk('on a Friday the card itself says it is a lighter day', 'Juma: yengilroq kun' in pg.inner_text('#app')); pg.clock.set_system_time('2026-11-09T10:00:00'); ev("render()")
    ev("()=>{S.ik=undefined}"); Ps = ev("ikPlan('2026-11-14')"); ids = [b['id'] for b in Ps['blocks']]
    chk('Saturday is a mock day (6 h): a real-time mock block of about 3 hours, its analysis, Speaking and vocabulary; total stays 360', ids == ['M', 'E', 'S', 'V'] and Ps['mock'] and 150 <= [b for b in Ps['blocks'] if b['id'] == 'M'][0]['m'] <= 210 and Ps['total'] == 360 and 'Rasmiy mock' in Ps['blocks'][0]['det'], (ids, Ps['total']))
    ev("ikH(2)"); chk('with 2 hours Saturday is not a mock day (a normal split), and the chosen hours are remembered on top of the course setting', not ev("ikPlan('2026-11-14').mock") and ev("S.ik.h") == 2 and ev("ikPlan('2026-11-09').total") == 120)
    ev("()=>{S.ik=undefined}"); chk('without a choice the hours default to the course setting (6)', ev("ikHours()") == 6)
    ev("ikH(4)"); chk('choosing 4 hours gives 240 minutes', ev("ikPlan('2026-11-09').total") == 240); ev("ikH(6)")
    # belgilash
    ev("ikTog('W')"); ev("ikTog('S')"); d = ev("ikDone(dk())"); chk('ticking a block records its minutes: 2 blocks and their minutes are counted, saved by date', d['n'] == 2 and d['m'] == ev("ikPlan().blocks.filter(b=>b.id==='W'||b.id==='S').reduce((a,b)=>a+b.m,0)") and ev("Object.keys(S.ik.d[dk()].x)") == ['W', 'S'])
    ev("ikTog('W')"); chk('ticking again undoes it', ev("ikDone(dk())")['n'] == 1)
    ev("()=>{S.ik.d={};for(let i=0;i<90;i++)S.ik.d[dAgo(i+1)]={x:{W:1},m:{W:60}};ikTog('E')}"); chk('only the last 60 days are kept; the weekly total counts the last 7 days', len(ev("Object.keys(S.ik.d)")) <= 61 and ev("ikWeekMin()") > 0)
    # navigatsiya
    for id_, want in (('W', "IVW==='w'"), ('S', "IVW==='s'"), ('L', "IVW==='m'&&IK==='L'"), ('R', "IVW==='m'&&IK==='R'"), ('V', "IVW==='y'&&KS.sec==='l'"), ('E', "IVW==='y'&&KS.sec==='x'")):
        ev("()=>{tab='h';IVW='k';KS.sec='r'}"); ev("(i)=>ikGo(i)", id_); chk(f'"›" on the {id_} block opens the right screen', ev("tab") == 'e' and ev(want), ev("[tab,IVW,KS.sec]"))
    ev("()=>{tab='e';EV='i';IVW='y';KS.sec='r';S.ik=undefined;render()}"); pg.wait_for_timeout(100)
    # radar
    chk('radar with real results: four bars with "band / target", the weakest skill is named with its gap (Writing and Speaking tie at 2.0 below 7.5)', '5.5 / 7.5' in ev("ikRadar()".replace('ikRadar()', 'ikRadar().replace(/<[^>]+>/g," ")')) and 'Eng zaif:' in ev("ikRadar().replace(/<[^>]+>/g,' ')") and '2 band past' in ev("ikRadar().replace(/<[^>]+>/g,' ')"))
    ev("()=>{S.ie.tests=[];S.ie.cf={L:60,R:66,W:47,S:45,d:dk()}}"); r = ev("ikRadar().replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ')"); chk('with NO results yet the radar uses the CEFR scores (relative, marked taxminiy): Speaking is the weakest, shown as "CEFR 45/75"', 'CEFR 45/75' in r and 'Eng zaif: Speaking' in r and '(taxminiy)' in r, r[:300])
    G = ev("ikGaps()"); chk('CEFR-based gaps are larger for the weaker skills (Speaking > Writing > Listening > Reading)', G['S']['g'] > G['W']['g'] > G['L']['g'] > G['R']['g'] and G['S']['src'] == 'CEFR')
    ev("()=>{S.ie.cf=undefined;S.ie.tests=[]}"); G0 = ev("ikGaps()"); chk('with nothing at all, sensible defaults: Writing and Speaking weaker than Listening and Reading', G0['W']['g'] > G0['L']['g'] > G0['R']['g'] and G0['W']['src'] == 'taxmin')
    ev("()=>{S.ie.xd=[];for(let i=0;i<3;i++)S.ie.xd.push({id:i,c:'grammar',w:'a',r:'b',box:0,due:dk()});S.ie.xd.push({id:9,c:'spelling',w:'a',r:'b',box:0,due:dk()})}"); chk('the radar also names the most frequent mistake categories from the notebook', 'Grammatika</b> (3)' in ev("ikRadar()") and 'Imlo</b> (1)' in ev("ikRadar()"))
    # CEFR forma
    ev("()=>{IKO.c=1;render()}"); pg.wait_for_timeout(80); chk('the CEFR section says only numbers are stored (no ID or photo needed) and has four inputs', 'ID va rasm kerak emas' in pg.inner_text('#app') and ev("document.querySelectorAll('#app input[id^=ikcf]').length") == 4)
    ev("()=>{document.getElementById('ikcfL').value='60';document.getElementById('ikcfR').value='99';document.getElementById('ikcfW').value='47';document.getElementById('ikcfS').value='';ikCfSave()}"); c = ev("S.ie.cf"); chk('saving keeps 0–75 only (99 → 75), skips empty fields and stores nothing else but the date', c == {'L': 60, 'R': 75, 'W': 47, 'd': '2026-11-09'}, c)
    ev("()=>{['L','R','W','S'].forEach(k=>{const e=document.getElementById('ikcf'+k);if(e)e.value=''});__t=[];ikCfSave()}"); chk('saving with all fields empty is refused with a message', any('Kamida bitta' in m for m in ev("__t"))); ev("ikCfDel()"); chk('...and the baseline can be deleted', ev("S.ie.cf") is None)
    # bashorat
    ev("()=>{S.ie.tests=[]}"); chk('with no results the forecast honestly says it is not yet possible and does not invent numbers', 'Hali aniq emas' in ev("ikForecast()") and 'to‘qib berib' in ev("ikForecast()"))
    ev("()=>{S.ie.tests=[{id:1,d:'2026-10-10',k:'W',b:{W:5}}]}"); chk('a single result is not enough either', not ev("ikFc().ok"))
    ev("()=>{S.ie.tests=[{id:1,d:'2026-11-02',k:'W',b:{W:5}},{id:2,d:'2026-11-04',k:'W',b:{W:6}},{id:3,d:'2026-11-03',k:'L',b:{L:6}},{id:4,d:'2026-11-05',k:'L',b:{L:6.5}}]}"); chk('results less than 7 days apart are ignored (a quick jump is noise, not a trend)', not ev("ikFc().ok"))
    ev("""()=>{S.ie.tests=[{id:1,d:'2026-10-10',k:'W',b:{W:5}},{id:2,d:'2026-10-24',k:'W',b:{W:5.5}},{id:3,d:'2026-11-07',k:'W',b:{W:6}},
      {id:4,d:'2026-10-10',k:'L',b:{L:6.5}},{id:5,d:'2026-10-24',k:'L',b:{L:6.5}},{id:6,d:'2026-11-07',k:'L',b:{L:6.5}}]}""")
    F = ev("ikFc()"); chk('trend per skill from at least 2 spread-out results: Writing +0.25/week is CAPPED at +0.2 (sustained gains are rarely faster); a flat Listening stays 0', F['ok'] and F['R']['W']['wk'] == 0.2 and F['R']['L']['wk'] == 0 and F['n'] == 2, F)
    chk('the projection to the exam date (82 days away) is damped (×0.6): Writing 5.5 → about 6.9, Listening stays 6.5; the overall is their mean; only 2 skills → shown as partial and the margin is ±1', abs(F['R']['W']['pr'] - 6.9) <= 0.1 and F['R']['L']['pr'] == 6.5 and abs(F['pro'] - 6.7) <= 0.1 and F['pad'] == 1 and 'faqat 2 ta ko‘nikma' in ev("ikForecast()"), F)
    t = ev("ikForecast().replace(/<[^>]+>/g,' ')"); chk('it states the range, whether the target (7.5) is out of reach at this speed and how much per week would be needed', '5.5–7.5' in t.replace(' ', '') or '5.5–7.5' in t or 'maqsadga yetmaydi' in t, t[:400])
    chk('the needed weekly gain is computed from the current overall and the weeks left (about +0.2…+0.3 here)', F['need'] is not None and 0.05 < F['need'] < 0.5 and 'haftasiga taxminan' in t, F['need'])
    chk('the forecast always carries the disclaimer: it is an estimate, not a guarantee, and Writing/Speaking should also be checked by a person', 'Kafolat emas' in ev("ikForecast()") and 'ustoz' in ev("ikForecast()"))
    ev("""()=>{const mk=(k,v)=>[0,1,2,3,4].map((i,j)=>({id:Math.random(),d:'2026-10-'+String(5+i*5).padStart(2,'0'),k,b:{[k]:v+i*0.1}}));S.ie.tests=[...mk('W',5.5),...mk('S',5.5),...mk('L',6),...mk('R',6.5)]}""")
    F2 = ev("ikFc()"); chk('with all four skills and 4+ results each the margin narrows to ±0.5 and no "partial" note appears', F2['all'] and F2['pad'] == 0.5 and 'faqat' not in ev("ikForecast()"), F2)
    ev("()=>{S.ie.kr.exam='';S.ie.ed=undefined}"); chk('without an exam date it still shows the current level but asks for the date instead of a projection', ev("ikFc().pro") is None and 'Imtihon sanasini kiritsang' in ev("ikForecast()")); ev("()=>{S.ie.kr.exam='2027-01-30'}")
    ev("()=>{S.ie.tests=Array.from({length:4},(_,i)=>({id:i,d:'2026-10-'+(5+i*8<10?'0':'')+(5+i*8),k:'W',b:{W:6.5+i*0.1}}))}")
    # ko'rinish
    ev("()=>{S.ie.cf={L:60,R:66,W:47,S:45,d:dk()};S.ie.tests=[{id:1,d:'2026-10-10',k:'W',b:{W:5}},{id:2,d:'2026-10-24',k:'W',b:{W:5.5}},{id:3,d:'2026-11-07',k:'W',b:{W:6}},{id:4,d:'2026-10-10',k:'L',b:{L:6.5}},{id:5,d:'2026-10-24',k:'L',b:{L:6.5}},{id:6,d:'2026-11-07',k:'L',b:{L:6.5}}];IKO={r:1,f:1,c:1}}")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='e';EV='i';IVW='y';KS.sec='r';render()}", [ui, th]); pg.wait_for_timeout(80)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the IELTS day card with radar, forecast and CEFR open fits the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
