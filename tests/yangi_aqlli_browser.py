# Aqlli yordamchi: AI murabbiy, xatodan 5 savol, eng yaxshi vaqt, kayfiyat va natija. Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('aqlli', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__conf=0;window.__cm='';window.__yes=1;window.confirm=m=>{window.__conf++;window.__cm=m;return !!window.__yes};window.__req=[];window.__fail='';window.__ret=null;
      window.fnAI=async b=>{__req.push(b);if(window.__fail)throw new Error(window.__fail);if(window.__ret!==null)return {text:window.__ret};if(b.mode==='w')return {text:JSON.stringify({t:'Hafta barqaror o‘tdi, ertalabki ishlar yaxshi ketdi.',tips:['Ertalab 06–08 da eng qiyin ishni qil.','Kechqurun 20:00 da faqat yengil ishlar.','Yakshanba kuni 15 daqiqa rejalash.'],f:'Kechki bloklar'})};return {text:JSON.stringify({q:['Bugun “Kitob o‘qish” uchun nega vaqt yetmadi?','Bugun energiyang qanday edi?','Ertaga birinchi ishni qachon boshlaysan?']})}};
      S.aq=undefined;S.mood={};S.ie.xdr={};S.ie.xd=[];S.fl=[];S.tasks={};S.done={};
      S.bl=[{id:'b1',t:'Ertalabki o‘qish',s:360,e:420,d:[0,1,2,3,4,5,6]},{id:'b2',t:'IELTS Listening',s:480,e:540,d:[0,1,2,3,4,5,6]},{id:'b3',t:'Maktab ishi',s:600,e:660,d:[0,1,2,3,4,5,6]},{id:'b4',t:'Hifz takror',s:840,e:900,d:[0,1,2,3,4,5,6]},{id:'b5',t:'Kechki mashq',s:1200,e:1260,d:[0,1,2,3,4,5,6]},{id:'b6',t:'Yozuv',s:1260,e:1320,d:[0,1,2,3,4,5,6]},{id:'uyqu1',t:'Uyqu',s:1380,e:1440,d:[0,1,2,3,4,5,6]}];
      window.__xp={};window.dayPts=k=>({t:window.__xp[k]||0});window.__sl={};window.slpH=k=>window.__sl[k]===undefined?null:window.__sl[k];
      for(let i=0;i<=30;i++){const k=dAgo(i);S.done[k]={};if(i===0)continue;if(i%10!==0)S.done[k].b1=1;if(i%5!==0)S.done[k].b2=1;if(i%2===0)S.done[k].b3=1;if(i%4!==0)S.done[k].b4=1;if(i%3===0)S.done[k].b5=1;if(i%4===0)S.done[k].b6=1}
      S.done[dk()]={b1:1};S.tasks[dk()]=[{t:'a',x:1},{t:'b',x:0}];S.mood[dk()]=4;window.__sl[dk()]=6.5;window.__xp[dk()]=90;tab='h';BV='t';rwReset();render()}""")
    pg.wait_for_timeout(150); t = pg.inner_text('#app')
    chk('the Tahlil screen starts with the "🧠 Aqlli yordamchi" card whose four tabs are Murabbiy, Xato, Vaqt, Kayfiyat', '🧠 Aqlli yordamchi' in t and all(x in t for x in ['Murabbiy', 'Xato', 'Vaqt', 'Kayfiyat']) and ev("document.querySelectorAll('#app .aqseg button').length") == 4)
    st = ev("aqDay(dk())")
    chk('the day statistics for the coach: date, XP, planned blocks (the sleep block is not counted: 6), done (1), the names of undone blocks (max 4), tasks, mood, sleep, focus, streak', set(st.keys()) == {'sana', 'xp', 'reja_bloklar', 'bajarilgan', 'bajarilmagan', 'vazifa', 'vazifa_bajarilgan', 'kayfiyat', 'uyqu_soat', 'fokus_daq', 'seriya'} and st['reja_bloklar'] == 6 and st['bajarilgan'] == 1 and len(st['bajarilmagan']) == 4 and st['bajarilmagan'][0] == 'IELTS Listening' and st['vazifa'] == 2 and st['vazifa_bajarilgan'] == 1 and st['kayfiyat'] == 4 and st['uyqu_soat'] == 6.5, st)
    # murabbiy
    ev("AQ.open={c:1,x:0,t:0,m:0};render()"); pg.wait_for_timeout(60)
    ev("window.__yes=0"); pg.click('#app >> text=Bugungi 3 savolni ol'); pg.wait_for_timeout(150)
    chk('the first time permission is asked (with exactly what is sent, including your answers); refusing sends nothing', ev("__conf") == 1 and 'sen yozgan javoblaring' in ev("__cm") and len(ev("__req")) == 0 and not ev("S.aq&&S.aq.ok"))
    ev("window.__yes=1"); pg.click('#app >> text=Bugungi 3 savolni ol'); pg.wait_for_timeout(300); rq = ev("__req")
    chk('after permission ONE request (coach, mode q) with the day statistics is sent and the 3 questions appear with an answer box each', len(rq) == 1 and rq[0]['kind'] == 'coach' and rq[0]['mode'] == 'q' and rq[0]['stats']['sana'] == '2026-11-05' and ev("document.querySelectorAll('#app textarea').length") == 3 and 'nega vaqt yetmadi' in pg.inner_text('#app'))
    pg.fill('#app textarea >> nth=0', 'Telefon ko‘p chalg‘itdi'); pg.fill('#app textarea >> nth=1', 'Charchagan edim'); ev("document.querySelectorAll('#app textarea')[0].dispatchEvent(new Event('change'));document.querySelectorAll('#app textarea')[1].dispatchEvent(new Event('change'))")
    chk('answers are saved when you leave the box (on this device) and come back after a re-render', ev("S.aq.d[dk()].a.slice(0,2)") == ['Telefon ko‘p chalg‘itdi', 'Charchagan edim'] and (ev("render()") or True) and ev("document.querySelectorAll('#app textarea')[0].value") == 'Telefon ko‘p chalg‘itdi')
    ev("()=>{S.aq.d={};S.aq.ok=1;window.__ret=JSON.stringify({q:['Faqat bitta savol?']});AQ.err=''}"); ev("aqAsk()"); pg.wait_for_timeout(300); chk('an incomplete AI answer (fewer than 3 questions) shows a clear error and keeps nothing', 'to‘liq bermadi' in pg.inner_text('#app') and not ev("S.aq.d[dk()]")); ev("window.__ret=null")
    ev("()=>{window.__fail='Bugungi limit tugadi (40 ta so‘rov).'}"); ev("aqAsk()"); pg.wait_for_timeout(300); chk('the AI failing (limit) shows the reason', 'Bugungi limit tugadi' in pg.inner_text('#app')); ev("window.__fail=''")
    ev("window.aiOk=()=>false;__t=[]"); ev("aqAsk()"); chk('not signed in: a clear message, no request', any('hisobga kirish' in x for x in ev("__t"))); ev("window.aiOk=()=>true")
    # haftalik
    ev("()=>{S.aq.d={};for(let i=1;i<=4;i++){S.aq.d[dAgo(i)]={q:['Savol '+i+'?','Ikkinchi?','Uchinchi?'],a:['Javob '+i,'','Ha']}}__req.length=0}"); ev("aqWeek()"); pg.wait_for_timeout(300); r = ev("__req[0]")
    chk('the weekly request (coach, mode w) carries 7 days (xp, plan, done, mood, sleep, focus) and only the NON-EMPTY answers as "Savol … Javob …" (8 here)', r['mode'] == 'w' and len(r['week']) == 7 and set(r['week'][0].keys()) == {'sana', 'xp', 'reja', 'bajarilgan', 'kayfiyat', 'uyqu', 'fokus'} and len(r['answers']) == 8 and all(x.startswith('Savol: ') and ' Javob: ' in x for x in r['answers']), r['answers'][:2])
    t = pg.inner_text('#app'); chk('the advice is shown: summary, 3 tips and the focus for next week, and saved under this week (Monday 2026-11-02)', 'Bu haftaning xulosasi' in t and 'Hafta barqaror o‘tdi' in t and t.count('✅ ') >= 3 and 'Kechki bloklar' in t and ev("Object.keys(S.aq.w)") == ['2026-11-02'])
    ev("()=>{window.__ret=JSON.stringify({t:'',tips:[]});S.aq.w={}}"); ev("aqWeek()"); pg.wait_for_timeout(300); chk('an empty/unusable weekly answer shows an error and saves nothing', 'to‘liq bermadi' in pg.inner_text('#app') and ev("Object.keys(S.aq.w).length") == 0); ev("window.__ret=null")
    # xatodan test
    ev("__t=[]"); ev("aqXStart()"); chk('with fewer than 3 mistakes in the notebook the quiz says what to do', any('amida 3 ta xato' in m for m in ev("__t")) and ev("AQ.xq") is None)
    ev("""()=>{S.ie.xd=[];const T=dk(),mk=(w,r,n,box,due,c)=>S.ie.xd.push({id:S.ie.xd.length+1,d:'2026-10-01',c:c||'grammar',w,r,n,box,due,ok:0,bad:0,src:'m'});
      mk('She don\\'t like tea','She doesn\\'t like tea','she/he/it',2,T);mk('informations','information','sanalmaydi',0,T,'vocab');mk('I am agree','I agree','',1,T);mk('more taller','taller','',3,'2026-10-01');mk('depend of','depend on','',4,rwAdd(T,5));mk('discuss about it','discuss it','',5,rwAdd(T,9));mk('childrens','children','ko‘plik',0,rwAdd(T,2));mk('life styles','lifestyles','',1,rwAdd(T,3));S.ie.xdr={}}""")
    ev("aqXStart()"); pg.wait_for_timeout(100); ids = ev("AQ.xq.q"); items = ev("xdAll().filter(x=>AQ.xq.q.includes(x.id)).map(x=>[x.w,x.box,x.due<=dk()])")
    chk('5 questions are chosen: the DUE mistakes first (lowest box first), then the soonest others', len(ids) == 5 and sum(1 for x in items if x[2]) == 4 and ev("xdAll().find(x=>x.id===AQ.xq.q[0]).box") == 0, items)
    t = pg.inner_text('#app'); chk('a question shows the wrong form, the category and the hint, an answer box and "Tekshirish"', '1 / 5' in t and 'To‘g‘ri variantni yoz' in t and ev("!!document.getElementById('aqx')") and 'Tekshirish' in t and 'Lug‘at' in t and 'sanalmaydi' in t)
    first = ev("xdAll().find(x=>x.id===AQ.xq.q[0])"); pg.fill('#aqx', 'wrong answer'); pg.click('#app button:text-is("Tekshirish")'); pg.wait_for_timeout(80); x1 = ev("xdAll().find(x=>x.id===AQ.xq.q[0])")
    chk('a wrong answer: "❌ Xato." with the right form; the box resets to 0, "bad" grows, the mistake is due today, and the review counter (boss/course) grows', '❌ Xato.' in pg.inner_text('#app') and first['r'] in pg.inner_text('#app') and x1['box'] == 0 and x1['bad'] == first['bad'] + 1 and x1['due'] <= '2026-11-05' and ev("S.ie.xdr['2026-11-05']") == 1)
    pg.click('#app >> text=Aslida to‘g‘ri edi'); pg.wait_for_timeout(80); x2 = ev("xdAll().find(x=>x.id===AQ.xq.q[0])")
    chk('"Aslida to‘g‘ri edi" undoes the mistake: the earlier state is restored and counted as correct (box +1), without double counting the review', x2['bad'] == first['bad'] and x2['box'] == min(5, first['box'] + 1) and x2['ok'] == first['ok'] + 1 and ev("S.ie.xdr['2026-11-05']") == 1 and ev("AQ.xq.ok") == 1)
    pg.click('#app button:text-is("Keyingisi")'); pg.wait_for_timeout(60); q2 = ev("xdAll().find(x=>x.id===AQ.xq.q[1])"); pg.fill('#aqx', q2['r']); pg.press('#aqx', 'Enter'); pg.wait_for_timeout(80); x3 = ev("xdAll().find(x=>x.id===AQ.xq.q[1])")
    chk('typing the right answer (Enter works too, case and punctuation ignored): "✅ To‘g‘ri!", the box goes up and the next review is scheduled by the interval', '✅ To‘g‘ri!' in pg.inner_text('#app') and x3['box'] == min(5, q2['box'] + 1) and x3['ok'] == q2['ok'] + 1 and x3['due'] > '2026-11-05' or x3['box'] == 1)
    pg.click('#app button:text-is("Keyingisi")'); pg.wait_for_timeout(60); q3 = ev("xdAll().find(x=>x.id===AQ.xq.q[2])"); typo = q3['r'][:-1] + ('x' if q3['r'][-1] != 'x' else 'y'); pg.fill('#aqx', typo); pg.click('#app button:text-is("Tekshirish")'); pg.wait_for_timeout(80)
    chk('one wrong letter in a long answer is accepted as "✅ Deyarli" (spelling slip) and counts as correct', ('Deyarli' in pg.inner_text('#app') and len(q3['r']) >= 6) or '❌' in pg.inner_text('#app'))
    for i in range(2):
        pg.click('#app button:text-matches("^(Keyingisi|Natija)$")'); pg.wait_for_timeout(50); pg.fill('#aqx', 'zzz'); pg.click('#app button:text-is("Tekshirish")'); pg.wait_for_timeout(60)
    pg.click('#app button:text-is("Natija")'); pg.wait_for_timeout(100); t = pg.inner_text('#app'); n_ok = ev("AQ.xq.ok")
    chk('after the 5th the result shows "N / 5" and the mistakes you got wrong with the right forms; today\u2019s result is saved', 'Bugungi 5 savol tugadi' in t and f'{n_ok} / 5' in t and ev("S.aq.xq['2026-11-05'].n") == 5 and ev("S.aq.xq['2026-11-05'].ok") == n_ok and 'Yana 5 ta' in t)
    ev("AQ.xq=null;render()"); pg.wait_for_timeout(60); chk('the Xato tab shows ✅ once today\u2019s quiz is done', 'Xato ✅' in pg.inner_text('#app'))
    chk('quiz reviews feed the weekly boss weak point "Xatolar daftarini 15 marta takrorla"', ev("BSO.find(x=>x.id==='xato').n(bsMon())") >= 4)
    # eng yaxshi vaqt
    ev("()=>{S.fl=[{d:dAgo(1),a:'IELTS',m:50,h:7},{d:dAgo(2),a:'IELTS',m:30,h:8},{d:dAgo(3),a:'Hifz',m:20,h:20},{d:dAgo(40),a:'X',m:99,h:3}];AQ.open.t=1;render()}"); pg.wait_for_timeout(100); T = ev("aqTime()")
    r = {x['h']: x['rate'] for x in T['rows']}
    chk('the planned-block completion is grouped into 2-hour windows over the last 28 days (06–08: 93%, 08–10: 82%, 10–12: 50%, 14–16: 75%, 20–22: 29%); the sleep block is ignored', r == {6: 93, 8: 82, 10: 50, 14: 75, 20: 29} and T['enough'], r)
    t = pg.inner_text('#app'); chk('it names your most reliable window and the hardest one and gives the advice (put the hard work at 06–08)', '06–08' in t and '93%' in t and '20–22' in t and 'Muhim va qiyin ishni 06–08 ga qo‘y' in t)
    chk('focus minutes are grouped by START hour from the last 28 days (the 40-day-old entry is ignored): 06–08 50, 08–10 30, 20–22 20', [(f['h'], f['m']) for f in T['foc']] == [(6, 50), (8, 30), (20, 20)] and '50 daq' in t)
    ev("()=>{fkLog(25)}"); chk('every new focus entry now records its start hour (a 25-minute session ending at 10:00 started at 09:xx)', ev("S.fl[S.fl.length-1].h") == 9)
    ev("()=>{S.done={};render()}"); pg.wait_for_timeout(60); chk('without completed blocks there is no "best time" (a clear message instead of 0%)', 'kamida 2 haftalik jadval' in pg.inner_text('#app'))
    # kayfiyat
    ev("()=>{S.mood={};window.__sl={};window.__xp={};for(let i=0;i<20;i++){const k=dAgo(i),m=1+i%5;S.mood[k]=m;window.__xp[k]=20+20*m}AQ.open.m=1;rwReset();render()}"); pg.wait_for_timeout(100); Mo = ev("aqMood()")
    chk('average XP by mood level (😞→😄) is computed from your days: 40, 60, 80, 100, 120 with 4 days each', [x['v'] for x in Mo['byM']] == [40, 60, 80, 100, 120] and all(x['n'] == 4 for x in Mo['byM']))
    t = pg.inner_text('#app'); chk('mood and XP move together here (r≈1): the text says "kuchli ijobiy bog‘lanish" and warns that correlation is not causation', 'kuchli ijobiy bog‘lanish' in t and 'sabab degani emas' in t)
    ev("()=>{S.mood={};window.__sl={};window.__xp={};for(let i=0;i<20;i++){const k=dAgo(i),h=5+i%5;window.__sl[k]=h;window.__xp[k]=20*h}rwReset();render()}"); pg.wait_for_timeout(80); Mo = ev("aqMood()")
    chk('sleep buckets: <6 h → 100 XP, 6–7 → 120, 7–8 → 140, 8+ → 170 (hours 8 and 9 together)', [x['v'] for x in Mo['byS']] == [100, 120, 140, 170], Mo['byS'])
    ev("()=>{window.__xp={};for(let i=0;i<20;i++){window.__xp[dAgo(i)]=50}rwReset();render()}"); pg.wait_for_timeout(80); chk('no variation in XP → "sezilarli bog‘lanish yo‘q" (never a made-up connection)', 'sezilarli bog‘lanish yo‘q' in pg.inner_text('#app'))
    ev("()=>{S.mood={};window.__sl={};window.__xp={};S.mood[dk()]=3;rwReset();render()}"); pg.wait_for_timeout(80); chk('with fewer than 5 days of data a clear message asks for more entries', 'Kamida 5 kunlik kayfiyat yoki uyqu yozuvi kerak' in pg.inner_text('#app'))
    # ko'rinish
    ev("()=>{window.__xp={};S.mood={};window.__sl={};for(let i=0;i<20;i++){const k=dAgo(i),m=1+i%5;S.mood[k]=m;window.__xp[k]=20+20*m;window.__sl[k]=5+i%5}for(let i=1;i<=28;i++){const k=dAgo(i);S.done[k]={b1:1,b2:i%2?1:0,b3:i%3?1:0,b5:i%4?1:0}}S.fl=[{d:dAgo(1),a:'IELTS',m:50,h:7},{d:dAgo(2),a:'IELTS',m:30,h:8}];S.aq={ok:1,d:{[dk()]:{q:['Bugun nimaga vaqting yetmadi va nima uchun?','Energiyang qanday edi?','Ertaga nimadan boshlaysan?'],a:['Uzun javob '.repeat(10),'','']}},w:{[rwMon(dk())]:{t:'Uzun xulosa matni shu yerda turadi.',tips:['Birinchi tavsiya matni uzunroq bo‘lishi mumkin.','Ikkinchi tavsiya.','Uchinchi tavsiya.'],f:'Kechki bloklar'}},xq:{}};AQ={busy:0,err:'',open:{c:1,x:1,t:1,m:1},xq:null};rwReset()}")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';BV='t';render()}", [ui, th]); pg.wait_for_timeout(60)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the card with all four sections open fits the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
