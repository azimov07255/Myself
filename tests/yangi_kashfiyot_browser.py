import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Mening ko'rsatkichlarim va Kashfiyotlar. Soat: 2026-11-09 (dushanba) 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('kf', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;window.__xp={};window.__sl={};window.dayPts=k=>({t:window.__xp[k]||0});window.slpH=k=>window.__sl[k]===undefined?null:window.__sl[k];
      S.km=[];S.kv={};S.mood={};S.fl=[];S.pm={};S.hab=[];S.hb={};S.f5=[];S.done={};S.bl=[];S.ik=undefined;S.q.tk=undefined;KMD='';KMF={t:'',ty:'num',u:'',g:0,dir:'up',o:0};tab='m';MQV='n';render()}""")
    pg.wait_for_timeout(120); t = pg.inner_text('#app'); chk('the Nafs tab has the two new cards: “🧮 Mening ko‘rsatkichlarim” and “🧬 Kashfiyotlar”', '🧮 Mening ko‘rsatkichlarim' in t and '🧬 Kashfiyotlar' in t and 'Hali ko‘rsatkich yo‘q' in t)
    # ---------- ko'rsatkichlar
    ev("kmPre(0)"); ev("kmPre(2)"); ev("kmPre(5)"); L = ev("S.km")
    chk('quick presets create metrics with the right type, unit, goal and direction: 💧 Suv (number, stakan, ≥8), 📵 Telefon (minutes, ≤120), 🙏 Zikr (yes/no)', [(m['t'], m['ty'], m['u'], m['g'], m['dir']) for m in L] == [('💧 Suv', 'num', 'stakan', 8, 'up'), ('📵 Telefon', 'min', 'daq', 120, 'down'), ('🙏 Zikr', 'yn', '', 1, 'up')] and len({m['id'] for m in L}) == 3, L)
    ev("()=>{KMF={t:'  🥗 Sabzavot  ',ty:'num',u:'porsiya',g:3,dir:'up',o:0};kmSub()}"); chk('a custom metric is created from the form (name trimmed)', ev("S.km[3].t") == '🥗 Sabzavot' and ev("S.km[3].u") == 'porsiya')
    ev("__t=[]"); chk('an empty name or an unknown type is refused', ev("kmAdd({t:'',ty:'num'})") is False and ev("kmAdd({t:'x',ty:'zzz'})") is False and len(ev("S.km")) == 4)
    ev("()=>{for(let i=0;i<20;i++)kmAdd({t:'M'+i,ty:'num'})}"); chk('at most 12 metrics', len(ev("S.km")) == 12 and any('12 tagacha' in m for m in ev("__t")))
    ev("S.km=S.km.slice(0,4)")
    ids = ev("S.km.map(m=>m.id)"); suv, tel, zikr, veg = ids
    ev("(a)=>{kmSet(a[0],1);kmSet(a[1],0);kmSet(a[2],0)}", [zikr, tel, suv]); chk('yes/no: 1 = yes, 0 = no (a zero is a real answer and is kept)', ev("kmGet(dk(),'%s')" % zikr) == 1 and ev("kmGet(dk(),'%s')" % tel) == 0)
    ev("kmSet('%s',0)" % zikr); chk('…switching to “Yo‘q” stores 0', ev("kmGet(dk(),'%s')" % zikr) == 0)
    ev("(a)=>{kmStep(a,1);kmStep(a,1);kmStep(a,1)}", suv); chk('number + and − buttons step by 1; below zero is not allowed', ev("kmGet(dk(),'%s')" % suv) == 3); ev("(a)=>{for(let i=0;i<5;i++)kmStep(a,-1)}", suv); chk('…stays at 0', ev("kmGet(dk(),'%s')" % suv) == 0)
    ev("(a)=>kmStep(a,1)", tel); ev("(a)=>kmStep(a,5)", tel); chk('minutes step by 5', ev("kmGet(dk(),'%s')" % tel) == 5 or ev("kmGet(dk(),'%s')" % tel) == 6)
    ev("kmSet('%s',2.456)" % suv); chk('decimals are rounded to 2 places', ev("kmGet(dk(),'%s')" % suv) == 2.46)
    ev("kmSet('%s','')" % suv); chk('an empty value clears the entry for that day', ev("kmGet(dk(),'%s')" % suv) is None)
    for bad in ('-3', 'abc', '100001'):
        ev("kmSet('%s','%s')" % (suv, bad))
    chk('negative numbers, text and absurdly large values are ignored', ev("kmGet(dk(),'%s')" % suv) is None)
    ev("()=>{S.km.push({id:'rt',t:'😴 Sifat',ty:'rate',u:'',g:4,dir:'up'})}"); ev("kmSet('rt',4)"); chk('rating 1–5 stores the number', ev("kmGet(dk(),'rt')") == 4); ev("kmSet('rt',4)"); chk('pressing the same number again clears it', ev("kmGet(dk(),'rt')") is None); ev("kmSet('rt',9)"); chk('a rating above 5 is clamped to 5', ev("kmGet(dk(),'rt')") == 5); ev("S.km=S.km.filter(m=>m.id!=='rt');delete S.kv[dk()].rt")
    ev("KMD='2026-11-08'"); ev("kmSet('%s',6)" % suv); chk('“Kecha” logs on yesterday', ev("kmGet('2026-11-08','%s')" % suv) == 6 and ev("kmGet(dk(),'%s')" % suv) is None); ev("KMD='2026-11-12'"); ev("kmSet('%s',3)" % suv); chk('a future date never accepts values', ev("kmGet('2026-11-12','%s')" % suv) is None); ev("KMD=''")
    suvm, telm = ev("S.km[0]"), ev("S.km[1]")
    chk('goal logic: Suv ≥ 8 → 8 is met, 7 not; Telefon ≤ 120 → 100 met, 130 not; yes/no met only for 1; no goal → undefined (null)', [ev("(a)=>kmMet(a[0],a[1])", [suvm, 8]), ev("(a)=>kmMet(a[0],a[1])", [suvm, 7]), ev("(a)=>kmMet(a[0],a[1])", [telm, 100]), ev("(a)=>kmMet(a[0],a[1])", [telm, 130]), ev("(a)=>kmMet(a[0],a[1])", [ev("S.km[2]"), 1]), ev("(a)=>kmMet(a[0],a[1])", [ev("S.km[2]"), 0]), ev("(a)=>kmMet(a[0],a[1])", [{'ty': 'num', 'g': 0, 'dir': 'up'}, 5]), ev("(a)=>kmMet(a[0],a[1])", [suvm, None])] == [True, False, True, False, True, False, None, None])
    ev("()=>{S.kv={};const T=dk();kmDate();[['T',100],[1,90],[2,80],[3,130],[4,60]].forEach(([d,v])=>{const k=d==='T'?T:rwAdd(T,-d);(S.kv[k]=S.kv[k]||{})[S.km[1].id]=v})}"); St = ev("kmStats(S.km[1])")
    chk('streak counts consecutive days at the goal (Telefon ≤ 120): today 100, yesterday 90, 80, then 130 breaks it → 3 days; the 7-day average and the number of logged days are computed', St['st'] == 3 and St['n'] == 5 and abs(St['avg'] - 92) < 0.01 and len(St['vals']) == 14, St)
    ev("()=>{delete S.kv[dk()]}"); St = ev("kmStats(S.km[1])"); chk('if today is not logged yet the streak is counted from yesterday (2 days), not reset', St['st'] == 2, St)
    ev("()=>{S.kv={};tab='m';MQV='n';KMD='';render()}"); ev("kmSet('%s',5)" % suv); ev("kmSet('%s',100)" % tel); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the card shows each metric with its type/unit/goal, today’s control, a 14-day mini chart, the 7-day average and how many of 14 days are logged', 'Suv' in t and 'maqsad ≥ 8' in t and 'maqsad ≤ 120' in t and ev("document.querySelectorAll('#app .kms').length") == 4 and ev("document.querySelector('#app .kms').children.length") == 14 and '7 kun o‘rtachasi' in t and '1/14 kun yozilgan' in t)
    chk('a metric whose goal is met today shows ✅ and one that is not shows ⚠️', ev("document.querySelectorAll('#app [aria-label=\"Maqsad bajarilmadi\"]').length") == 1 and ev("document.querySelectorAll('#app [aria-label=\"Maqsad bajarildi\"]').length") == 1)
    ev("kmSet('%s',130)" % tel); pg.wait_for_timeout(80); chk('in the mini chart days over the limit are drawn in the warning colour', ev("document.querySelectorAll('#app .kms i[data-b]').length") >= 1)
    ev("__t=[]"); ev("kmDel('%s')" % veg); chk('deleting a metric removes it', len(ev("S.km")) == 3)
    ev("()=>{window.confirm=()=>false}"); ev("kmDel('%s')" % tel); chk('…but declining the question keeps it', len(ev("S.km")) == 3); ev("()=>{window.confirm=()=>true}")
    ev("kmDel('%s')" % tel); chk('deleting also removes all values of that metric from the history', not any(tel in v for v in ev("Object.values(S.kv).map(o=>Object.keys(o).join())")))
    # Bugun qatori
    ev("()=>{S.kv={};kmSet(S.km[0].id,3);tab='h';BV='j';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Bugun shows “🧮 Ko‘rsatkichlar: 1/2 kiritildi” with the names of the missing ones until everything is entered', 'Ko‘rsatkichlar: 1/2 kiritildi' in t)
    ev("()=>{kmSet(S.km[1].id,1);render()}"); pg.wait_for_timeout(60); chk('…and the row disappears when all are entered', 'Ko‘rsatkichlar:' not in pg.inner_text('#app'))
    ev("()=>{S.kv={};render()}"); pg.wait_for_timeout(60); ev("()=>{[...document.querySelectorAll('#app button.row')].find(b=>b.textContent.includes('Ko‘rsatkichlar')).click()}"); pg.wait_for_timeout(100); chk('tapping the row opens Maqsad → Nafs', ev("tab") == 'm' and ev("MQV") == 'n')
    ev("()=>{S.km=[];render()}"); pg.wait_for_timeout(60); ev("()=>{tab='h';render()}"); chk('with no metrics Bugun shows nothing about them', 'Ko‘rsatkichlar:' not in pg.inner_text('#app'))
    # ---------- kashfiyotlar
    chk('Pearson correlation: perfectly linear data → 1; perfectly opposite → −1; no variation → null', abs(ev("kfR([1,2,3,4,5],[2,4,6,8,10])") - 1) < 1e-9 and abs(ev("kfR([1,2,3,4,5],[10,8,6,4,2])") + 1) < 1e-9 and ev("kfR([1,1,1],[1,2,3])") is None)
    def build(js):
        ev("(()=>{S.km=[];S.kv={};S.mood={};window.__xp={};window.__sl={};S.fl=[];S.pm={};S.f5=[];S.hab=[];S.hb={};" + js + ";})()")
    build("for(let i=1;i<=40;i++){const k=dAgo(i),good=i%2?8:6;window.__sl[k]=good;window.__xp[k]=60+(good>=7?60:0)+(i%3);S.mood[k]=((i>>1)%2)+2}")
    R_ = ev("kfAll(60)"); F = R_['F']; f = [x for x in F if x['X'] == 'slp' and x['Y'] == 'xp']
    chk('synthetic proof: with XP always about 60 higher on 8-hour nights, the engine finds “Uyqu → XP” (same day), r above 0,9, 40 days, high confidence; days of data = 40', len(f) == 1 and f[0]['lag'] == 0 and f[0]['r'] > 0.9 and f[0]['n'] == 40 and f[0]['conf'] == 'yuqori' and f[0]['diff'] > 55 and R_['days'] == 40, f)
    txt = ev("(f)=>kfText(f)", f[0]); chk('the sentence is human: “Uyqu (soat) yuqori (≥ 8) kunlarda XP o‘rtacha 120…, pastroq kunlarda 60 (farq +60)” (≥ is used when the median splits the days evenly)', 'Uyqu (soat) yuqori (≥ 8) kunlarda XP' in txt and '121' in txt and '61,1' in txt and 'farq +59,9' in txt, txt)
    chk('an unrelated pair (mood in a 0,0,1,1 pattern vs sleep alternating) is NOT reported', not any({x['X'], x['Y']} == {'mood', 'slp'} for x in F) and not any({x['X'], x['Y']} == {'mood', 'xp'} for x in F))
    chk('each pair appears once (no “XP → Uyqu” duplicate of the same finding)', len([x for x in F if {x['X'], x['Y']} == {'slp', 'xp'}]) == 1)
    build("for(let i=1;i<=40;i++){const k=dAgo(i);window.__xp[k]=50+(i%2)*40;S.fl.push({d:k,a:'x',m:20+(i%2)*40});S.pm[k]=i%2*3}")
    chk('trivial same-family pairs are not reported on the same day: XP vs focus minutes vs pomodoros (they build each other) give no finding even though they move together', not any(x['lag'] == 0 and {x['X'], x['Y']} <= {'xp', 'fok', 'pom'} for x in ev("kfAll(60).F")))
    build("S.km=[{id:'suv',t:'💧 Suv',ty:'num',u:'stakan',g:8,dir:'up'}];for(let i=1;i<=41;i++){const k=dAgo(i);S.kv[k]={suv:(i%3===0?8:3)}}for(let i=1;i<=40;i++){const k=dAgo(i);window.__xp[k]=50+(((i+1)%3===0)?60:0)+(i%2)}")
    F = ev("kfAll(60).F"); f = [x for x in F if x['X'] == 'm:suv' and x['Y'] == 'xp']
    chk('a NEXT-DAY effect is found too: XP is higher the day after you drank 8 glasses (your own metric “💧 Suv” feeds the engine), phrased “Kecha 💧 Suv yuqori … bo‘lsa, bugun XP …”', len(f) == 1 and f[0]['lag'] == 1 and f[0]['r'] > 0.9 and ev("(f)=>kfText(f)", f[0]).startswith("Kecha 💧 Suv yuqori") , f)
    def tail(n, extra=''):
        build("for(let i=1;i<=%d;i++){const k=dAgo(i),good=i%%2?8:6;window.__sl[k]=good;window.__xp[k]=60+(good>=7?60:0)+(i%%3)}%s" % (n, extra))
        return ev("kfAll(60)")
    r13 = tail(13); chk('with only 13 days of paired data nothing is reported (the minimum is 14), and the card says how many days exist', r13['F'] == [] and r13['days'] == 13)
    r14 = tail(14); chk('with 14 days the same pattern is reported, with “o‘rta” (medium) confidence', len(r14['F']) == 1 and r14['F'][0]['n'] == 14 and r14['F'][0]['conf'] == 'o‘rta', r14['F'])
    tail(40, "window.__sl[dk()]=1;window.__xp[dk()]=999;S.mood[dk()]=1"); r = ev("kfAll(60)"); chk('today is never used (a wild value today changes nothing)', r['F'] and r['F'][0]['n'] == 40 and r['days'] == 40)
    build("for(let i=1;i<=30;i++){const k=dAgo(i);window.__xp[k]=70+(i*7)%11}"); r = ev("kfAll(60)"); chk('with no lifestyle data the engine finds nothing and says so politely', r['F'] == [])
    build("S.km=[{id:'zk',t:'🙏 Zikr',ty:'yn',u:'',g:1,dir:'up'},{id:'su',t:'💧 Suv',ty:'num',u:'stakan',g:8,dir:'up'}];for(let i=1;i<=30;i++){const k=dAgo(i);S.kv[k]={su:5};if(i%2)S.kv[k].zk=1;window.__xp[k]=40+(i%2?50:0)}")
    d1 = ev("kfDay(dAgo(1))"); d2 = ev("kfDay(dAgo(2))"); chk('a yes/no metric that was only ticked “yes” counts as 0 on days when you logged other things (so “no” is not lost), and stays empty on days with no entries at all', d1['m:zk'] == 1 and d2['m:zk'] == 0 and ev("kfDay(dAgo(40))")['m:zk'] is None)
    ev("(()=>{S.km=[];S.kv={};S.mood={};window.__xp={};window.__sl={};S.fl=[];S.pm={};S.f5=[];S.hab=[];S.hb={};for(let i=1;i<=14;i++){const k=dAgo(i);window.__sl[k]=i%2?8:6;window.__xp[k]=60+(i%2?60:0)}tab='m';MQV='n';render()})()"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the card shows the finding, “14 kun · bog‘lanish r = 1 · ishonch: o‘rta”, the day count and the warning that this is correlation, not cause', 'Uyqu (soat) yuqori' in t and '14 kun · bog‘lanish r = 1' in t and 'ishonch: o‘rta' in t and '14 kun ma’lumot' in t and 'sabab emas' in t, t[t.find('🧬'):][:300])
    ev("(()=>{window.__sl={};window.__xp={};render()})()"); pg.wait_for_timeout(60); chk('with no data the card explains it needs at least 14 days of paired data', 'kamida 14 kunlik' in pg.inner_text('#app'))
    ev("(()=>{for(let i=1;i<=20;i++){const k=dAgo(i);window.__xp[k]=50+(i*7)%13;window.__sl[k]=6+(i*5)%3}render()})()"); pg.wait_for_timeout(60); t = pg.inner_text('#app'); chk('with enough data but no strong link it says so (“Hozircha kuchli bog‘lanish topilmadi”)', 'Hozircha kuchli bog‘lanish topilmadi' in t or 'Uyqu' in t)
    ev("(()=>{S.km=[{id:'x',t:'<img src=x onerror=alert(1)>',ty:'num',u:'<b>',g:1,dir:'up'}];render()})()"); pg.wait_for_timeout(60); chk('names and units typed by you are shown as plain text', ev("document.querySelectorAll('#app img[src=x]').length") == 0 and ev("document.querySelectorAll('#app section b').length") >= 0)
    bad = []
    ev("(()=>{S.km=[{id:'a',t:'💧 Juda uzun nomli ko‘rsatkich sarlavhasi bor',ty:'num',u:'stakan',g:8,dir:'up'},{id:'b',t:'⭐ Baho',ty:'rate',u:'',g:4,dir:'up'},{id:'c',t:'✅ Ha yo‘q',ty:'yn',u:'',g:1,dir:'up'},{id:'d',t:'⏱ Daqiqa',ty:'min',u:'daq',g:30,dir:'down'}];for(let i=1;i<=14;i++){const k=dAgo(i);S.kv[k]={a:i%9,b:(i%5)+1,c:i%2,d:i*3}}KMF.o=1;tab='m';MQV='n'})()")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='m';MQV='n';render()}", [ui, th]); pg.wait_for_timeout(80)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('both cards with four metrics of every type and the open form fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
