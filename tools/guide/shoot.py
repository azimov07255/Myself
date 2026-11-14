import sys, json
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
SEED = r"""()=>{window.confirm=()=>true;window.toast=()=>{};localStorage.setItem('trk_bk',dk());
 const rnd=(()=>{let s=777;return()=>{s=(s*1103515245+12345)&0x7fffffff;return s/0x7fffffff}})();
 S.hab=[{id:'h1700000000001',t:'Qur‘on hifz: 3 bet',e:'📖'},{id:'h1700000000002',t:'Kitob: 20 bet',e:'📚'},{id:'h1700000000003',t:'2 litr suv',e:'💧'},{id:'h1700000000004',t:'Zal',e:'🏋️',f:4},{id:'h1700000000005',t:'Yugurish',e:'🏃',f:3},{id:'h1700000000006',t:'20 ta yangi so‘z',e:'🔤'},{id:'h1700000000007',t:'Erta uxlash',e:'🌙',rt:'22:30'},{id:'h1700000000008',t:'Zikr',e:'📿'}];
 S.hb={};S.hk={};S.nm=S.nm||{d:{}};S.nm.d={};S.q.ny={};S.fm={};S.mood={};S.water={};S.note={};S.top={};S.fl=[];
 const P=['fajr','dhuhr','asr','maghrib','isha','vitr'];
 for(let i=0;i<40;i++){const k=dAgo(i);S.hb[k]={};S.hab.forEach((x,j)=>{if(rnd()<(i===0?.35:.68))S.hb[k][x.id]=true});S.nm.d[k]={};P.forEach(p=>{if(i>0||p==='fajr'||p==='dhuhr')S.nm.d[k][p]=rnd()<.8?1:2});if(rnd()<.7)S.q.ny[k]=1+Math.floor(rnd()*3);S.fm[k]=Math.floor(rnd()*80);S.mood[k]=2+Math.floor(rnd()*4);S.water[k]=3+Math.floor(rnd()*6);if(rnd()<.5)S.fl.push({d:k,a:['IELTS','Qur‘on','Univer','Ish'][i%4],m:25})}
 S.hk[dAgo(2)]={h1700000000004:1};S.hb[dAgo(2)].h1700000000004=false;
 S.q.ppd=3;S.q.hp=142;S.q.hs=dAgo(55);S.q.h0=60;S.q.ht='2027-03-01';S.q.hg=3;S.top[dk()]=[{t:'Fizika laboratoriya ishi',x:1},{t:'IELTS Reading: 1 ta matn',x:0},{t:'Hifz: yangi sahifa',x:0}];
 S.goals=[{t:'IELTS 7.0 olish',why:'Chet elda o‘qish uchun',dl:'2026-12-20',ms:[{t:'1-hafta: Diagnostika — mock test ishla',x:1,xd:dAgo(9)},{t:'2-hafta: Reading — 3 ta matn',x:1,xd:dAgo(3)},{t:'3-hafta: Writing — 2 ta insho',x:0},{t:'4-hafta: Speaking — 5 ta mashq',x:0}],p:0},{t:'Baqara surasini yodlash',why:'',dl:'2027-03-01',ms:[{t:'1-juz tugatish',x:1,xd:dAgo(20)},{t:'2-juz tugatish',x:0}],p:0},{t:'Zalda 75 kg ga yetish',why:'',dl:'2027-01-15',ms:[{t:'Haftada 4 mashg‘ulot',x:0}],p:0}];
 S.money=[];const C=CATS;let id=1;for(let i=0;i<45;i++){const d=dAgo(Math.floor(rnd()*40)),o=rnd()<.82;S.money.push({id:id++,d,k:o?'out':'in',a:o?5000*(1+Math.floor(rnd()*40)):[2500000,300000,150000][Math.floor(rnd()*3)],c:o?C[Math.floor(rnd()*C.length)]:'Maosh',n:o?['Tushlik','Taksi','Kofe','Bozor','Kitob','Internet'][Math.floor(rnd()*6)]:'Maosh',w:'p',ac:rnd()<.5?'cash':'card',t:o&&rnd()<.6?['z','x','k'][Math.floor(rnd()*3)]:undefined})}
 S.money.push({id:id++,d:dk(),k:'out',a:35000,c:'Ovqat',n:'Tushlik',w:'p',ac:'cash',t:'z'},{id:id++,d:dk(),k:'out',a:15000,c:'Ovqat',n:'Kofe',w:'p',ac:'card',t:'x'});
 S.money.push({id:901,d:'2026-11-01',k:'in',a:2500000,c:'Maosh',n:'Maosh',w:'p',ac:'card'},{id:902,d:'2026-11-01',k:'out',a:120000,c:'Ovqat',n:'Bozor',w:'p',ac:'cash',t:'z'},{id:903,d:'2026-11-02',k:'out',a:65000,c:'Transport',n:'Taksi',w:'p',ac:'cash',t:'x'},{id:904,d:'2026-11-02',k:'out',a:90000,c:'Ovqat',n:'Restoran',w:'p',ac:'card',t:'k'});
 S.fin={open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:3000000,sg:[{id:1,t:'Yangi noutbuk',a:8000000,s:2400000}],cb:{p:{Ovqat:900000,Transport:300000,Kiyim:500000}},rc:[{id:'r1',w:'p',k:'out',a:350000,ac:'card',c:'Aloqa',n:'Internet',day:5,from:'2026-12',last:'2026-11',on:1}],wl:[{id:1,t:'Simsiz quloqchin',a:450000,at:Date.now()-3600000*5}],wlSaved:300000};
 S.ie.words=['mitigate|yumshatmoq|C1','sustain|qo‘llab-quvvatlamoq|B2','comprehensive|keng qamrovli|B2','scarce|kam uchraydigan|C1','advocate|himoya qilmoq|C1','deteriorate|yomonlashmoq|C1','inevitable|muqarrar|B2','prevalent|keng tarqalgan|C1','subsequent|keyingi|B2','substantial|sezilarli|B2','enhance|yaxshilamoq|B1','tackle|hal qilmoq|B2','adequate|yetarli|B1','tend to|moyil bo‘lmoq|B1','plays a crucial role|muhim rol o‘ynaydi|B2'].map((s,i)=>{const p=s.split('|');return{id:i+1,w:p[0],m:p[1],u:p[1],d:'definition of '+p[0],e:'This is an example sentence with '+p[0]+'.',lv:p[2],k:i===14?'c':'w',box:i%5,due:i<6?dk():dAgo(-(i%5)),t:1}});
 S.ie.mat=[{id:1,t:'The Future of Urban Transport',k:'a',x:'Cities around the world are investing in public transport to reduce traffic congestion. Experts argue that electric buses and metro systems can substantially cut pollution. However, critics point out that the cost is high and the benefits depend on how many people actually use them. In the long term, planners hope that cleaner and faster transport will change how people live and work.',c:[],au:0,d:dk(),an:null},{id:2,t:'BBC 6 Minute English: Sleep',k:'p',x:'Today we talk about sleep and why it matters for learning.',c:[],au:0,d:dk(),an:null}];
 S.ie.ex='2026-12-20';S.ie.target=7;S.ie.tests=[{id:1,d:dAgo(30),k:'M',b:{L:6,R:5.5,W:5.5,S:6}},{id:2,d:dAgo(14),k:'M',b:{L:6.5,R:6,W:6,S:6}},{id:3,d:dAgo(4),k:'M',b:{L:7,R:6.5,W:6,S:6.5}}];
 S.ie.pr=[1,2,3,4].map(i=>({id:i,d:dAgo(i),k:'R',s:5+i%3,n:8}));S.ie.lp=[{id:1,d:dAgo(2),s:6,n:8}];S.ie.wr=[{id:1,d:dAgo(3),k:2,t:'Some people think...',x:'Sample essay text',sc:6.5}];S.ie.pt=[{d:dAgo(1),p:84,n:10}];S.ie.pz=[];
 S.rem=S.rem||{};S.rem.on=true;tab='h';BV='j';render()}"""
SHOTS = [
 ('bugun_jadval', "tab='h';BV='j'", 0), ('bugun_kunlik', "tab='h';BV='m'", 0), ('bugun_holat', "tab='h';BV='h'", '#ft'),
 ('bugun_tahlil', "tab='h';BV='t';S.wrd=''", '#wrc'), ('hayot', "tab='h';BV='t'", 'Hayot paneli'), ('quron', "tab='q';QT='y'", 0),
 ('odatlar', "tab='o';OT='j';HV='m'", 0), ('odat_tahrir', "tab='o';OT='j';HV='m';hbE(0)", 0), ('maqsad', "tab='m'", 0), ('maqsad_dvigatel', "tab='m'", 'Maqsad dvigateli'),
 ('ielts_bosh', "tab='e';EV='i';IVW='b'", 0), ('ielts_lugat', "tab='e';EV='i';IVW='l'", 0), ('ielts_mat', "tab='e';EV='i';IVW='a'", 0), ('ielts_natija', "tab='e';EV='i';IVW='m'", 0), ('ielts_writing', "tab='e';EV='i';IVW='w'", 0),
 ('ielts_speaking', "tab='e';EV='i';IVW='s';spPick(2)", 0), ('ielts_ai', "tab='e';EV='i';IVW='x';AXO.l=true;AXO.t=true", 0), ('ielts_imtihon', "tab='e';EV='i';IVW='k'", 0),
 ('pul_bosh', "tab='p';W='p';PV='b'", 0), ('pul_tarix', "tab='p';PV='t'", 0), ('pul_hisobot', "tab='p';PV='h'", 0), ('pul_reja', "tab='p';PV='r'", 0), ('pul_xohish', "tab='p';PV='b'", 'Xohish ro‘yxati'),
 ('takror', "tab='q';QT='t'", 0), ('xarita', "tab='q';QT='x'", 0), ('namoz', "tab='q';QT='n'", 0), ('zikr', "tab='q';QT='z'", 0), ('sozlama', "tab='s'", 0), ('sozlama_tayyor', "tab='s'", 'Ishga tayyormi?'), ('sozlama_yangi', "tab='s'", 'Yangiliklar va qo‘llanma'), ('sozlama_vidjet', "tab='s'", 'Vidjet (iPhone)'),
]
with Run('guide', when=(2026, 11, 3, 10, 0, 0)) as R:
    ev, pg = R.ev, R.pg
    ev(SEED); pg.wait_for_timeout(300)
    ev("()=>{window.wdDb=()=>({from:()=>({upsert:async()=>({error:null}),delete:()=>({eq:async()=>({})})})});UID='11111111-2222-3333-4444-555555555555';S.wd={on:1,t:'a1b2c3d4e5f60718293a4b5c6d7e8f90'};WDG.ok='10:05';window.fnPost=async()=>({owner:true,limit:40,used:7});SYNC='ok';window.aiOk=()=>true}")
    ev("()=>{tab='s';render();rdRun()}"); pg.wait_for_timeout(500)
    for key, setup, scr in SHOTS:
        try:
            ev("()=>{document.querySelectorAll('#hbs,#iemz,#fkb,#prn').forEach(e=>e.remove());%s;render()}" % setup); pg.wait_for_timeout(250)
            if scr:
                ev("""(t)=>{document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes(t))d.open=true});if(t[0]==='#'){const e=document.querySelector(t);if(e)(e.closest('.hero')||e).scrollIntoView({block:'start'});return}const els=[...document.querySelectorAll('#app h2,#app summary')].filter(e=>e.textContent.includes(t));if(els[0])els[0].scrollIntoView({block:'start'});}""", scr); pg.wait_for_timeout(250)
                ev("window.scrollBy(0,-70)")
            else: ev("window.scrollTo(0,0)")
            pg.wait_for_timeout(120); pg.screenshot(path='/tmp/guide/shots/%s.png' % key)
        except Exception as e: print('ERR', key, str(e)[:120])
    # kun yopish (21:00)
    R.at(2026, 11, 3, 21, 0, 0); ev("()=>{tab='h';BV='m';S.close={};render()}"); pg.wait_for_timeout(300)
    ev("(()=>{const e=[...document.querySelectorAll('#app .hero')].find(x=>x.textContent.includes('Kunni yopish'));if(e)e.scrollIntoView({block:'start'});window.scrollBy(0,-60)})()"); pg.wait_for_timeout(200); pg.screenshot(path='/tmp/guide/shots/kun_yopish.png')
    R.at(2026, 11, 3, 10, 0, 0)
    # AI chat
    ev("()=>{tab='h';BV='m';render()}"); pg.wait_for_timeout(200)
    ok = ev("(()=>{aiOpen();return 1})()"); pg.wait_for_timeout(500); pg.screenshot(path='/tmp/guide/shots/ai_chat.png'); print('ai click', ok)
    print('errors', R.errs[:3])
