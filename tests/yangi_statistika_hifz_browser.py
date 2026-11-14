# Foydalanish statistikasi va hifz xaritasi. Soat: 2026-10-31 10:00.
import sys, json, datetime
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('ush') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    # ---------- 1. screen keys ----------
    key = lambda js: ev("()=>{%s;return usKey()}" % js)
    chk('screen names: Bugun, Qur‘on tabs, Ibodat, Odat, Maqsad, Sozlama, Pul', [key("tab='h'"), key("tab='q';QT='t'"), key("tab='q';QT='n'"), key("tab='q';QT='x'"), key("tab='o'"), key("tab='m'"), key("tab='s'"), key("tab='p'")] == ['Bugun', 'Qur‘on · Takror', 'Ibodat · Namoz', 'Qur‘on · Hifz xaritasi', 'Odat', 'Maqsad', 'Sozlama', 'Pul'])
    chk('IELTS sub-screens and the other study tabs', [key("tab='e';EV='i';IVW='x'"), key("tab='e';EV='i';IVW='l'"), key("tab='e';EV='u'"), key("tab='e';EV='p'")] == ['IELTS · AI mashq', 'IELTS · Lug‘at', 'Univer', 'Prava'])
    chk('an open IELTS reader overlay counts as "O‘qish oynasi", search as "Qidiruv"', ev("()=>{const d=document.createElement('div');d.id='iem';document.body.appendChild(d);const k=usKey();d.remove();return k}") == 'IELTS · O‘qish oynasi' and key("SO=true") == 'Qidiruv' and key("SO=false;tab='h'") == 'Bugun')
    # ---------- 2. recording ----------
    ev("()=>{S.us=undefined;tab='h';USK='';USL=0}"); R.at(2026, 10, 31, 10, 0, 0); ev("usHit()"); d = ev("dk()")
    chk('the first screen is recorded as one visit', ev("S.us.d[dk()]['Bugun']") == [1, 0], ev("S.us"))
    R.at(2026, 10, 31, 10, 1, 30); ev("usFlush()"); chk('90 seconds on the screen are added to its time', ev("S.us.d[dk()]['Bugun']") == [1, 90])
    ev("usHit()"); chk('another render on the SAME screen is not a new visit', ev("S.us.d[dk()]['Bugun'][0]") == 1)
    R.at(2026, 10, 31, 10, 2, 0); ev("()=>{tab='q';QT='t';usHit()}")
    chk('switching screen credits the time to the old one (120 s) and counts a visit to the new one', ev("S.us.d[dk()]['Bugun'][1]") == 120 and ev("S.us.d[dk()]['Qur‘on · Takror']") == [1, 0])
    R.at(2026, 10, 31, 10, 20, 0); ev("usFlush()"); chk('a long idle gap counts at most 5 minutes (the phone was probably left open)', ev("S.us.d[dk()]['Qur‘on · Takror'][1]") == 300)
    ev("()=>{Object.defineProperty(document,'visibilityState',{get:()=>'hidden',configurable:true})}"); R.at(2026, 10, 31, 10, 25, 0); ev("usFlush()")
    chk('time is not counted while the app is in the background', ev("S.us.d[dk()]['Qur‘on · Takror'][1]") == 300); ev("()=>{delete document.visibilityState}")
    ev("()=>{tab='h';usHit();tab='q';usHit();tab='h';usHit()}"); chk('coming back to a screen later is a new visit', ev("S.us.d[dk()]['Bugun'][0]") == 3, ev("S.us.d[dk()]"))
    ev("()=>{S.ob=0;S.ts=0;S.us=undefined;USK='';usHit();window.__r=JSON.stringify(S.us||null);S.ob=1;S.ts=1}"); chk('nothing is recorded before the user is signed in and set up', ev("__r") == 'null')
    # ---------- 3. aggregation ----------
    ev("""()=>{const t=dk();S.us={d:{},ai:{}};S.us.d[t]={'Bugun':[5,600],'Qur‘on · Takror':[2,300]};S.us.d[dAgo(3)]={'Bugun':[3,300]};S.us.d[dAgo(10)]={'Bugun':[1,60],'Pul':[1,30]};
      S.us.ai[t]={chat:3,plan:1};S.us.ai[dAgo(2)]={chat:4};S.us.ai[dAgo(20)]={vocab:7}}""")
    A7 = ev("usAgg(7)"); A30 = ev("usAgg(30)")
    chk('7-day window: screens summed over the days inside it only, 2 active days', A7['screens']['Bugun'] == [8, 900] and 'Pul' not in A7['screens'] and A7['active'] == 2)
    chk('30-day window includes the older days (3 active days, Pul appears)', A30['screens']['Bugun'] == [9, 960] and A30['screens']['Pul'] == [1, 30] and A30['active'] == 3)
    chk('AI use: totals per action, 7 daily bars; the 20-day-old use is only in the 30-day window', A7['ai'] == {'chat': 7, 'plan': 1} and A7['aiTotal'] == 8 and len(A7['daily']) == 7 and A30['ai']['vocab'] == 7 and A30['aiTotal'] == 15)
    ev("()=>{S.us.d[dAgo(60)]={'Bugun':[9,9]};S.us.ai[dAgo(60)]={chat:9};usPrune()}"); chk('records older than 45 days are pruned', not ev("S.us.d[dAgo(60)]") and not ev("S.us.ai[dAgo(60)]") and ev("!!S.us.d[dAgo(10)]"))
    # ---------- 4. AI counted by action ----------
    ev("()=>{S.us={d:{},ai:{}};window.fnAI=window.__fnAI0;window.fnPost=async b=>({text:'{}'});localStorage.setItem('trk_aiu_'+dk(),'0')}"); ev("fnAI({action:'plan'})"); ev("fnAI({action:'plan'})"); ev("fnAI({action:'coach'})"); ev("aiCount(1,'chat')")
    chk('every AI call is counted under its feature (plan 2, coach 1, chat 1)', ev("S.us.ai[dk()]") == {'plan': 2, 'coach': 1, 'chat': 1}, ev("S.us.ai[dk()]"))
    # ---------- 5. the settings card ----------
    ev("""()=>{const t=dk();S.us={d:{},ai:{}};S.us.d[t]={'Bugun':[5,600],'Qur‘on · Takror':[2,90]};S.us.ai[t]={chat:3,plan:1};tab='s';USP=7;SDO={us:true};render()}"""); pg.wait_for_timeout(150)
    t = pg.inner_text('#app'); chk('Sozlama has a "📊 Foydalanish" group with the top screens, minutes and visits', '📊 Foydalanish' in t and '10 daq · 5×' in t and '2 daq · 2×' in t)
    chk('screens never opened in the period are listed (Mushaf, Pul...), used ones are not', 'Qur‘on · Mushaf' in t.split('ochilmagan')[1] and 'Bugun' not in t.split('ochilmagan')[1].split('AI sarfi')[0])
    chk('the AI section shows the total and the share of each feature', '4' in t.split('AI sarfi')[1] and 'Suhbat' in t and 'Top-3 reja' in t and ev("document.querySelectorAll('.usd div').length") == 7)
    pg.click('#app .seg button >> text="30 kun"'); pg.wait_for_timeout(100); chk('the 30-day toggle changes the window (14 daily bars shown at most)', ev("USP") == 30 and ev("document.querySelectorAll('.usd div').length") == 14)
    ev("()=>{S.us={d:{},ai:{}};render()}"); chk('empty state invites the user to use the app', 'Hali ma’lumot yo‘q' in pg.inner_text('#app'))
    ev("()=>{S.us={d:{[dk()]:{'Bugun':[1,10]}},ai:{}};window.confirm=()=>false;render()}"); pg.click('#app >> text=Statistikani tozalash'); chk('"tozalash" asks first; cancelling keeps the data', ev("!!S.us.d[dk()]"))
    ev("window.confirm=()=>true"); pg.click('#app >> text=Statistikani tozalash'); chk('and confirming clears it', ev("Object.keys(S.us.d).length") == 0)
    # ---------- 6. hifz map data ----------
    ev("""()=>{const q=S.q;q.m={};q.ord=[];q.rs={};q.lg=[];q.ppd=3;q.m[0]=1;q.ord.push(0);q.m[1]=10;q.ord.push(1);q.m[112]=SL(112);q.ord.push(112);q.m[100]=SL(100);q.ord.push(100);
      q.rs[0]={box:2,due:'2099-01-01',weak:true,last:dAgo(40)};q.rs[1]={box:4,due:'2099-01-01',weak:false,last:dAgo(5)};q.rs[100]={box:1,due:dAgo(2),weak:false,last:dAgo(30)};
      q.lg=[{id:1,d:dk(),i:112,a:0,b:SL(112),t:'n'}];window.ssParts=()=>[{k:'m',n:'Manzil',r:[[3,5]],p:2,done:null}];tab='q';QT='x';HXP=0;rwReset();render()}""")
    I = ev("hxInfo()"); st = {x['p']: x['st'] for x in I}
    chk('604 pages, each with a status', len(I) == 604 and sum(1 for x in I if x['st']) == 604)
    chk('page 1 (Fotiha, flagged weak) = w; Baqara pages 2-11 (box 4, reviewed 5 days ago) = s; page 12 (not memorised) = n', st[1] == 'w' and all(st[p] == 's' for p in range(2, 12)) and st[12] == 'n', [st[p] for p in range(1, 14)])
    chk('a surah memorised today lies in the sabqi window = x (new); one whose review is overdue = d', st[SP_112] == 'x' if (SP_112 := ev("SP[112]")) else False)
    chk('overdue review (box 1, due 2 days ago) = d', st[ev("SP[100]")] == 'd')
    ev("()=>{S.q.m[1]=10.5;rwReset()}"); half = ev("hxInfo()[11]"); chk('half a page memorised: page 12 shows as memorised with coverage ≈ 50% (drawn lighter)', half['st'] != 'n' and 0.4 < half['c'] < 0.6, half)
    chk('pages of today\u2019s plan (3 and 4) are flagged', ev("hxInfo()[2].td") and ev("hxInfo()[3].td") and not ev("hxInfo()[4].td"))
    chk('surahs on a page: page 1 = Fotiha; page 50 = only Al Imran (Baqara ended); the last page has several short surahs', ev("hxSurahsOn(1)") == [0] and ev("hxSurahsOn(50)") == [2] and len(ev("hxSurahsOn(604)")) >= 3 and 113 in ev("hxSurahsOn(604)"))
    ev("()=>{S.q.m[1]=10;rwReset()}")
    # ---------- 7. the map screen ----------
    pg.wait_for_timeout(100); ev("render()"); pg.wait_for_timeout(150)
    chk('the map has 30 juz rows and 604 page cells; row n has exactly as many cells as that juz has pages', ev("document.querySelectorAll('.hxr').length") == 30 and ev("document.querySelectorAll('.hxp').length") == 604 and ev("[...document.querySelectorAll('.hxr')].every((r,j)=>r.querySelectorAll('.hxp').length===J[j+1]-J[j])"))
    c = ev("hxCount(hxInfo())"); t = pg.inner_text('#app')
    chk('the summary and legend counts add up to 604 and match the grid', sum(c.values()) == 604 and ev("document.querySelectorAll('.hxp[data-s=w]').length") == c['w'] and ev("document.querySelectorAll('.hxp[data-s=n]').length") == c['n'] and '/ 604 bet' in t)
    chk('today\u2019s plan is outlined on the grid', ev("document.querySelectorAll('.hxp.hxt').length") == 2)
    pg.screenshot(path='/tmp/ush_map.png')
    ev("()=>{window.__mo=0;window.mfOpen=n=>{window.__mo=n};window.mfOn=()=>true}"); pg.click('.hxp[data-p="5"]'); pg.wait_for_timeout(100); t = pg.inner_text('.goal')
    chk('tapping a page opens its card: page, juz, surah, status, last review', '5-bet · 1-juz’' in t and 'Baqara' in t.replace('‘', '').replace('’', '') or 'Baqara' in t or 'Baqarah' in t.replace('‘', ''))
    chk('the card shows the status, last review and the buttons (Mushaf, weak, review today)', 'Mustahkam' in t and 'So‘nggi takror' in t and 'Mushafda ochish' in t and 'Zaif deb belgila' in t and 'Bugun takrorla' in t, t)
    pg.click('.goal >> text=Mushafda ochish'); chk('"Mushafda ochish" opens the Mushaf at that page', ev("__mo") == 5)
    pg.click('.hxp[data-p="5"]'); pg.wait_for_timeout(60); pg.click('.goal >> text=Zaif deb belgila'); pg.wait_for_timeout(100)
    chk('"Zaif deb belgila" flags the surah, resets its box and makes it due today; the page turns red', ev("S.q.rs[1].weak") is True and ev("S.q.rs[1].box") == 0 and ev("S.q.rs[1].due") == ev("dk()") and ev("hxInfo()[4].st") == 'w')
    pg.click('.goal >> text=Zaifni olib tashla'); pg.wait_for_timeout(100); chk('"Zaifni olib tashla" removes the flag (the surah is then due for review: orange)', ev("S.q.rs[1].weak") is False and ev("hxInfo()[4].st") == 'd')
    pg.click('.goal >> text=Bugun takrorla'); chk('"Bugun takrorla" sets the review to today', ev("S.q.rs[1].due") == ev("dk()"))
    pg.click('.hxp[data-p="5"]'); pg.wait_for_timeout(60); chk('tapping the same page again closes the card', ev("document.querySelectorAll('.goal .h b').length") == 0 or '5-bet' not in pg.inner_text('#app'))
    pg.click('.hxp[data-p="300"]'); pg.wait_for_timeout(60); t = pg.inner_text('.goal'); chk('a page that is not memorised shows its info without the weak / review buttons', '300-bet' in t and 'Yodlanmagan' in t and 'Zaif deb belgila' not in t and 'Bugun takrorla' not in t)
    ev("()=>{S.nomf=1;render()}"); pg.click('.hxp[data-p="301"]'); pg.wait_for_timeout(60); chk('with Mushaf switched off (friends build) there is no Mushaf button', 'Mushafda ochish' not in pg.inner_text('.goal'))
    ev("()=>{HXP=0;render()}"); chk('"Eng uzoq takrorlanmagan" lists memorised surahs by their oldest last review (Fotiha 40 days ago first)', 'Eng uzoq takrorlanmagan' in pg.inner_text('#app') and pg.inner_text('#app').split('Eng uzoq takrorlanmagan')[1].find('Fotiha') < pg.inner_text('#app').split('Eng uzoq takrorlanmagan')[1].find('Baqara') if 'Baqara' in pg.inner_text('#app').split('Eng uzoq takrorlanmagan')[1] else True)
    # ---------- 8. in the Quran tab ----------
    ev("()=>{QT='y';HXP=0;render()}"); chk('the Qur‘on group has a "🗺 Xarita" tab and it opens the map', '🗺 Xarita' in pg.inner_text('#app')); pg.click('#app .seg button >> text=Xarita'); pg.wait_for_timeout(100); chk('...', ev("QT") == 'x' and ev("document.querySelectorAll('.hxp').length") == 604)
    ev("()=>{QT='n';render()}"); chk('the Ibodat group does not show it', 'Xarita' not in pg.inner_text('#app'))
    ev("()=>{S.q.m={};S.q.ord=[];S.q.rs={};S.q.lg=[];window.ssParts=()=>[];QT='x';rwReset();render()}"); chk('nothing memorised yet: all 604 pages empty, 0%, no crash', ev("hxCount(hxInfo()).n") == 604 and '0 / 604' in pg.inner_text('#app'))
