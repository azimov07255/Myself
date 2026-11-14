# Kunlik nasihatchi. Soat: 2026-11-06 (JUMA) 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('nasihat', when=(2026, 11, 6, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__nsH=nsHijri;window.__t=[];window.toast=m=>window.__t.push(m);S.ns=undefined;S.ny=undefined;S.hab=[];tab='h';BV='j';render()}""")
    d = ev("""(()=>{const bad=[],ids=new Set(),SRC=new Set(['','Buxoriy, Muslim','Buxoriy','Muslim','Tirmiziy, Nasoiy','Hokim, Nasoiy','Abu Dovud']);NSD.forEach(D=>{[...D.sun].concat(NSALL).forEach(x=>{if(!SRC.has(x.s))bad.push('src:'+x.s);if(ids.has(x.id)&&!NSALL.includes(x))bad.push('dupe:'+x.id);ids.add(x.id)});if(!D.n||!D.tag||!D.b||!D.tav.length)bad.push('day:'+D.n)});const q=NSQ.filter(x=>!(/^(Qur‘on, \\d+:\\d+(–\\d+)?|Hadis: (Buxoriy, Muslim|Buxoriy|Muslim|Tirmiziy)|Hikmat)$/.test(x[1])));return {bad,days:NSD.length,fri:NSD[5].sun.map(x=>x.id),thu:NSD[4].sun.map(x=>x.id),mon:NSD[1].sun.map(x=>x.id),badq:q.map(x=>x[1]),nq:NSQ.length,nm:NSM.length}})()""")
    chk('the content tables are clean: 7 days (Sunday first), every day has a title, a short brief and tips; every sourced item cites only Buxoriy, Muslim, Tirmiziy, Nasoiy, Hokim or Abu Dovud; no duplicate ids', d['days'] == 7 and d['bad'] == [], d['bad'])
    chk('Friday has the 8 well-known Jumu‘a sunnahs (ghusl, clean clothes/perfume/miswak, going early, listening to the khutba, Surah Kahf, many salawat, the hour of response, the sunnah prayers after); Thursday starts Kahf and fasting; Monday fasting', d['fri'] == ['j1', 'j2', 'j3', 'j4', 'j5', 'j6', 'j7', 'j8'] and d['thu'] == ['pr', 'pk'] and d['mon'] == ['dr'])
    chk('the reminders are all sourced as Qur‘on (sura:ayah), Hadis (Buxoriy/Muslim/Tirmiziy) or plain Hikmat (30 of them: 18 from Qur‘an and hadith), and there are 16 nafs exercises', d['badq'] == [] and d['nq'] >= 28 and d['nm'] == 16, (d['badq'], d['nq']))
    it = ev("(()=>{const x=nsItems('2026-11-06');return {n:x.D.n,sun:x.sun.length,tav:x.tav.length,ids:x.sun.map(s=>s.id)}})()")
    chk('today (Friday 2026-11-06): the 8 Friday sunnahs plus the two daily ones (prayer on time, morning/evening dhikr) and 4 tips', it['n'] == 'Juma' and it['sun'] == 10 and it['tav'] == 4 and it['ids'][-2:] == ['nm', 'zk'], it)
    pg.wait_for_timeout(120); t = pg.inner_text('#app')
    chk('Bugun shows a one-line "Bugun juma · 0/14" card with the day’s brief (it opens the advisor)', 'Bugun juma' in t and '0/14' in t and 'ijobat soatida duo' in t)
    ev("()=>{[...document.querySelectorAll('#app button.nsm')][0].click()}"); pg.wait_for_timeout(150)
    chk('tapping it opens Maqsad → 🌙 Kun with the full advisor first', ev("tab") == 'm' and ev("MQV") == 'k' and '🌿 Kunlik nasihatchi' in pg.inner_text('#app') and pg.inner_text('#app').index('Kunlik nasihatchi') < pg.inner_text('#app').index('Niyat va muhosaba'))
    t = pg.inner_text('#app'); h = ev("nsHijri(new Date('2026-11-06T12:00:00'))")
    chk('the card shows Juma, its tagline, today’s Hijri date marked as approximate, the checklist with sources, the nafs exercise, a reminder and the "not a fatwa" note', 'Juma' in t and 'kichik hayit' in t and (h is None or ('taxminiy' in t and h['y'] in (1447, 1448, 1449))) and 'G‘usl qil' in t and 'Buxoriy, Muslim' in t and 'Hokim, Nasoiy' in t and 'Bugungi nafs mashqi' in t and 'Bu fatvo emas' in t, h)
    pg.click('#app .nsc >> text=G‘usl qil'); pg.wait_for_timeout(100); chk('tapping an item ticks it (saved by date), progress becomes 1/14, accessible role is set', ev("S.ns.d['2026-11-06'].a") == ['j1'] and '1/14' in pg.inner_text('#app .nsc') and ev("document.querySelector('#app .nsc .ck').getAttribute('aria-checked')") == 'true')
    pg.click('#app .nsc >> text=G‘usl qil'); pg.wait_for_timeout(60); chk('tapping again unticks it', ev("S.ns.d['2026-11-06'].a") == [] and '0/14' in pg.inner_text('#app .nsc'))
    ev("()=>{['j1','j2','j5'].forEach(nsTog)}"); chk('three ticks make today count for the streak (the chip appears from 2 days)', ev("nsStreak()") == 1 and '🔥' not in pg.inner_text('#app .nsc').split('Bugungi amallar')[0])
    ev("()=>{S.ns.d[dAgo(1)]={a:['x','y','z'],m:0,q:0};S.ns.d[dAgo(2)]={a:['x','y','z','w'],m:0,q:0};S.ns.d[dAgo(3)]={a:['x'],m:0,q:0};render()}"); pg.wait_for_timeout(60); chk('streak counts consecutive days with 3+ ticks (3 days; a day with 1 tick breaks it) and shows "🔥 3 kun"', ev("nsStreak()") == 3 and '🔥 3 kun' in pg.inner_text('#app .nsc'))
    ev("()=>{S.ns.d={};for(let i=0;i<90;i++)S.ns.d[dAgo(i)]={a:['a'],m:0,q:0};nsTog('j1')}"); chk('only the last 60 days are kept', len(ev("Object.keys(S.ns.d)")) <= 61)
    # hijri maxsus
    sp = lambda d, m: ev("(a)=>nsSpecial({d:a[0],m:a[1],y:1448})", [d, m])
    chk('special Hijri days: 13–15 → white days fast recommended (not in Ramadan, not on 13 Dhul Hijjah); Ashura 10 Muharram; Tasu‘a 9; Arafa 9 Dhul Hijjah; Eids → NO fasting; Tashriq 11–13 → no fasting; Shawwal 2–7 six days; Ramadan month note; ordinary day none', any('oq kunlari' in x for x in sp(14, 5)) and not any('oq kunlari' in x for x in sp(14, 9)) and not any('oq kunlari' in x for x in sp(13, 12)) and any('Ashuro' in x for x in sp(10, 1)) and any('Tosuo' in x for x in sp(9, 1)) and any('Arafa' in x for x in sp(9, 12)) and any('ro‘za tutilmaydi' in x for x in sp(10, 12)) and any('ro‘za tutilmaydi' in x for x in sp(1, 10)) and any('Tashriq' in x for x in sp(12, 12)) and any('olti kunlik' in x for x in sp(3, 10)) and any('Ramazon oyi' in x for x in sp(5, 9)) and sp(5, 5) == [] and ev("nsSpecial(null)") == [])
    ev("()=>{window.nsHijri=()=>({d:14,m:5,y:1448});render()}"); pg.wait_for_timeout(80); t = pg.inner_text('#app .nsc')
    chk('a special day is shown on the card ("✨ …") together with the Hijri date in Uzbek month names (14 Jumadul avval 1448-yil)', '✨ Oyning “oq kunlari”' in t and '14 Jumadul avval 1448-yil (taxminiy)' in t)
    ev("()=>{window.nsHijri=()=>null;render()}"); pg.wait_for_timeout(60); chk('where the browser cannot compute Hijri dates the card simply omits the line (no wrong date)', '-yil (taxminiy)' not in pg.inner_text('#app .nsc'))
    # nafs mashqi
    P0 = ev("nsPickM('2026-11-06')"); P1 = ev("nsPickM('2026-11-06')"); chk('without a weakness the nafs exercise is the same all day (chosen by the date) and has no "muhosabangdan" badge', P0['m']['t'] == P1['m']['t'] and not P0['fromWeak'])
    ev("()=>{S.ny={d:{[dAgo(1)]:{e:'Telefon ko‘p chalg‘itdi; kech yotdim'}}};render()}"); pg.wait_for_timeout(60); P = ev("nsPickM('2026-11-06')")
    chk('if your reflection of the last 7 days names a weakness (“telefon”, “kech yotdim”) the exercise targets it and says "muhosabangdan"', P['fromWeak'] and ('telefon' in P['m']['t'].lower() or 'erta yot' in P['m']['t'].lower()) and 'muhosabangdan' in pg.inner_text('#app .nsc'), P)
    ev("()=>{S.ny={d:{[dAgo(1)]:{e:'G‘azab qildim'}}};render()}"); chk('anger → the anger exercise', 'G‘azab kelsa' in ev("nsPickM('2026-11-06').m.t"))
    ev("()=>{S.ny={d:{[dAgo(10)]:{e:'telefon'}}};render()}"); chk('a weakness older than 7 days is ignored', not ev("nsPickM('2026-11-06').fromWeak"))
    pg.click('#app .nsn >> text=Bajardim'); pg.wait_for_timeout(80); chk('"Bajardim" marks the exercise done ("✅ Bajarildi, barakalloh!") and can be undone', ev("S.ns.d['2026-11-06'].m") == 1 and 'Bajarildi, barakalloh' in pg.inner_text('#app .nsn')); ev("nsMash()"); chk('...undo works', ev("S.ns.d['2026-11-06'].m") == 0)
    # eslatma
    q0 = ev("nsPickQ('2026-11-06',0)"); q1 = ev("nsPickQ('2026-11-06',1)"); chk('the daily reminder is chosen by the date (same all day) and "↻ Boshqa eslatma" moves to the next one (and wraps around)', ev("nsPickQ('2026-11-06',0)") == q0 and q1 != q0 and ev("nsPickQ('2026-11-06',%d)" % ev("NSQ.length")) == q0)
    ev("()=>{S.ns.d[dk()]={a:[],m:0,q:0};render()}"); pg.wait_for_timeout(60); before = pg.inner_text('#app .nsq'); pg.click('#app .nsq >> text=Boshqa eslatma'); pg.wait_for_timeout(80); chk('pressing it shows a different reminder with its source', pg.inner_text('#app .nsq') != before and ev("S.ns.d[dk()].q") == 1)
    chk('the advisor line is part of the morning briefing', 'Bugun juma' in ev("nbText()") and 'ijobat soatida duo' in ev("nbText()"))
    # boshqa kunlar
    ev("()=>{window.nsHijri=window.__nsH}")
    days = {}
    for dt, nm in (('2026-11-02T12:00:00', 'Dushanba'), ('2026-11-05T12:00:00', 'Payshanba'), ('2026-11-08T12:00:00', 'Yakshanba')):
        pg.clock.set_system_time(dt); ev("render()"); pg.wait_for_timeout(40); days[nm] = ev("nsItems(dk()).D.n")
    chk('other days follow the calendar (Monday / Thursday / Sunday)', days == {'Dushanba': 'Dushanba', 'Payshanba': 'Payshanba', 'Yakshanba': 'Yakshanba'}, days)
    pg.clock.set_system_time('2026-11-05T12:00:00'); ev("()=>{tab='m';MQV='k';render()}"); pg.wait_for_timeout(60); t = pg.inner_text('#app .nsc'); chk('Thursday shows the fasting and Kahf-start items and the Jumu‘a preparation tip', 'Payshanba kuni nafl ro‘za tut' in t and 'Kahf surasini payshanba shomidan' in t and 'Jumaga toza kiyim' in t)
    pg.clock.set_system_time('2026-11-06T10:00:00')
    bad = []
    ev("()=>{S.ns={d:{[dk()]:{a:['j1','j2','j3','j4','j5','j6','j7','j8'],m:1,q:3}}};window.nsHijri=()=>({d:14,m:12,y:1448});S.ny={d:{[dAgo(1)]:{e:'telefon'}}}}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='m';MQV='k';render()}", [ui, th]); pg.wait_for_timeout(60)
            ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            ev("()=>{tab='h';BV='j';render()}"); pg.wait_for_timeout(60)
            if not (ok1 and ev("document.documentElement.scrollWidth<=window.innerWidth+1")): bad.append(ui + th)
    chk('the advisor card and the Bugun one-liner fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
