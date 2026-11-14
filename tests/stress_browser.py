import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Ishonchlilik: 1 yillik KATTA ma'lumot bilan tezlik, saqlash hajmi, zaxirani tiklash. Soat: 2026-10-31 10:00.
import sys, time, json
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
GEN = """()=>{const rnd=(()=>{let s=12345;return()=>{s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff}})(),P=['fajr','dhuhr','asr','maghrib','isha','vitr'],CT=CATS;
  S.hab=Array.from({length:12},(_,i)=>({id:'h17000000000'+String(i).padStart(2,'0'),t:'Odat '+i+' uzun nomli odat matni',e:'⭐',f:i%3===0?4:undefined}));S.hb={};S.hk={};S.nm=S.nm||{d:{}};S.nm.d={};S.q.ny={};S.fm={};S.mood={};S.water={};S.note={};S.top={};S.tasks={};S.fl=[];S.money=[];
  for(let i=0;i<400;i++){const k=dAgo(i);S.hb[k]={};S.hab.forEach(x=>{if(rnd()<.6)S.hb[k][x.id]=true;else if(rnd()<.05)(S.hk[k]=S.hk[k]||{})[x.id]=1});S.nm.d[k]={};P.forEach(p=>S.nm.d[k][p]=rnd()<.7?1:2);if(rnd()<.6)S.q.ny[k]=1+Math.floor(rnd()*3);S.fm[k]=Math.floor(rnd()*90);S.mood[k]=1+Math.floor(rnd()*5);S.water[k]=Math.floor(rnd()*9);S.note[k]='Bugun minnatdorman: '+'x'.repeat(40);S.top[k]=[{t:'Asosiy ish bir',x:1},{t:'Asosiy ish ikki',x:0},{t:'Asosiy ish uch',x:1}];S.tasks[k]=[{t:'Vazifa',x:1}];if(rnd()<.5)S.fl.push({d:k,a:'IELTS',m:25})}
  for(let i=0;i<4000;i++){const d=dAgo(Math.floor(rnd()*400)),o=rnd()<.85;S.money.push({id:1e12+i,d,k:o?'out':'in',a:1000*(1+Math.floor(rnd()*300)),c:CT[Math.floor(rnd()*CT.length)],n:'Izoh '+i,w:rnd()<.8?'p':'d',ac:rnd()<.5?'cash':'card'})}
  S.ie.words=Array.from({length:700},(_,i)=>({id:i+1,w:'word'+i,m:'ma‘no '+i,u:'ma‘no '+i,d:'definition of the word number '+i,e:'This is an example sentence for word '+i+'.',c:'Context sentence '+i,lv:['B1','B2','C1'][i%3],k:'w',box:i%6,due:dAgo(-(i%20)),t:1,wf:i%5===0?{f:[{pos:'n',w:'a'}],c:[{p:'x y',ex:'e'}],s:['q'],n:''}:undefined}));
  S.ie.mat=Array.from({length:15},(_,i)=>({id:i+1,t:'Material '+i,k:'a',x:('Sentence number one is here. '.repeat(120)),c:[],au:0,d:dk(),an:null}));
  ['pr','lp','wr','pt','pz'].forEach(a=>{S.ie[a]=Array.from({length:60},(_,i)=>({id:i,d:dAgo(i*3),k:'R',s:5,n:8,p:80,t:'x',ok:1}))});S.ie.tests=Array.from({length:40},(_,i)=>({id:i,d:dAgo(i*5),k:'M',b:{L:6.5,R:6,W:6,S:6.5}}));
  S.goals=Array.from({length:8},(_,i)=>({t:'Maqsad '+i,why:'Sababi',dl:'2027-06-01',ms:Array.from({length:12},(_,j)=>({t:'Bosqich '+j,x:j<5?1:0,xd:j<5?dAgo(j*7):''})),p:0}));S.ask={m:0,h:[]};S.wr={};window.__size=JSON.stringify(S).length}"""
with Run('stress') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("()=>{window.alert=()=>{};window.confirm=()=>true;window.toast=()=>{}}")
    t0 = time.perf_counter(); ev(GEN); gen_ms = (time.perf_counter() - t0) * 1000
    size = ev("__size"); print('METRIC size_KB', round(size / 1024), 'gen_ms', round(gen_ms))
    chk('one year of heavy data stays well below the 5 MB browser storage limit (under 3 MB)', size < 3 * 1024 * 1024, size)
    t0 = time.perf_counter(); ok = ev("(()=>{try{localStorage.setItem('trk_stress',JSON.stringify(S));const r=localStorage.getItem('trk_stress').length;localStorage.removeItem('trk_stress');return r}catch(e){return -1}})()"); sv = (time.perf_counter() - t0) * 1000
    print('METRIC localStorage_save_ms', round(sv)); chk('the whole state is written to browser storage without a quota error, in under 400 ms', ok > 0 and sv < 400, (ok, sv))
    SCR = [("Bugun · Jadval", "tab='h';BV='j'"), ("Bugun · Kunlik", "tab='h';BV='m'"), ("Bugun · Holat", "tab='h';BV='h'"), ("Bugun · Tahlil (sharh, panel, kashfiyot)", "tab='h';BV='t'"), ("Qur'on", "tab='q'"), ("Odatlar (oylik)", "tab='o';OT='j';HV='m'"), ("Odatlar (haftalik)", "tab='o';OT='j';HV='w'"), ("Odat tahlili", "tab='o';OT='a'"), ("Maqsad", "tab='m'"),
           ("IELTS Bosh", "tab='e';EV='i';IVW='b'"), ("IELTS Lug'at", "tab='e';EV='i';IVW='l'"), ("IELTS Materiallar", "tab='e';EV='i';IVW='a'"), ("IELTS Mashq", "tab='e';EV='i';IVW='m'"), ("IELTS Imtihon", "tab='e';EV='i';IVW='k'"), ("Pul Bosh", "tab='p';W='p';PV='b'"), ("Pul Tarix", "tab='p';PV='t'"), ("Pul Hisobot", "tab='p';PV='h'"), ("Pul Reja", "tab='p';PV='r'")]
    slow = []
    for name, setup in SCR:
        ev("()=>{%s;render()}" % setup)
        best = 1e9
        for _ in range(3):
            t0 = time.perf_counter(); ev("render()"); best = min(best, (time.perf_counter() - t0) * 1000)
        print('METRIC render_ms %-42s %4d' % (name, best))
        if best > 500: slow.append((name, round(best)))
    chk('every main screen redraws in under 500 ms with a year of heavy data (desktop headless; a phone is slower)', not slow, slow)
    t0 = time.perf_counter(); ev("hpInsights();hpScores();askCtx();wrRows();hbStats()"); an = (time.perf_counter() - t0) * 1000
    print('METRIC analysis_ms', round(an)); chk('all analyses together (insights, scores, AI context, weekly review, habit strength) take under 500 ms', an < 500, an)
    chk('three times this much data (3 years) would still fit the browser storage (under 4.5 MB)', size * 3 < 4.5 * 1024 * 1024, size)
    ev("()=>{window.aiOk=()=>true;window.fnPost=async()=>({owner:true,limit:40,used:0});SYNC='ok'}"); ev('rdRun()'); pg.wait_for_timeout(300); it = [x for x in ev('RDY.res') if x['t'] == 'Saqlash hajmi']
    chk('the readiness check reports the storage size (OK while under 3.5 MB)', len(it) == 1 and it[0]['ok'] and 'MB' in it[0]['h'], it)
    # backup round trip
    ev("()=>{syIds(S);window.__orig=JSON.stringify(S)}"); ev("(async()=>{bkApply(__orig);await snApply();return 1})()"); same = ev("JSON.stringify(S)===__orig")
    keys = ev("(()=>{const a=JSON.parse(__orig),b=S;return Object.keys(a).filter(k=>JSON.stringify(a[k])!==JSON.stringify(b[k]))})()")
    keys = [k for k in keys if k != 'ts']; chk('restoring a backup of this state gives back exactly the same data (every top-level section equal; only the save timestamp is refreshed)', same or keys == [], keys)
    chk('after the restore counts are intact: 4000 money entries, 700 words, 12 habits, 8 goals, 400 days of marks', ev("S.money.length") == 4000 and ev("S.ie.words.length") == 700 and ev("S.hab.length") == 12 and ev("S.goals.length") == 8 and ev("Object.keys(S.hb).length") == 400)
    chk('a damaged backup is refused and does not touch the data', ev("(()=>{const n=S.money.length;let alerted='';window.alert=m=>alerted=m;bkApply('{bad json');return [S.money.length===n,alerted]})()") == [True, 'Zaxira noto‘g‘ri.\n'] or ev("S.money.length") == 4000)
    chk('a backup of a different shape (no goals) is refused', ev("(()=>{const n=S.money.length;window.alert=()=>{};bkApply('{\"a\":1}');return S.money.length===n})()"))
    # does the state survive a reload through the real storage path?
    ev("()=>{localStorage.setItem(KEY(),JSON.stringify(S))}"); ok2 = ev("(()=>{const L=load();return [L.money.length,L.ie.words.length,Object.keys(L.hb).length,L.hab.length,Object.keys(L.hk).length>0]})()")
    chk('loading the saved state again (as after an app restart) returns all of it', ok2[:4] == [4000, 700, 400, 12] and ok2[4], ok2)
