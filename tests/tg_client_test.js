// Ilovaning Telegram qismi: ulash, eslatma turlari, pochta qutisini qo'llash
const fs=require('fs'),vm=require('vm');
const SRC=fs.readFileSync(process.env.APP_JS||'/tmp/t.js','utf8');
const ok=(l,c)=>{console.log((c?'PASS ':'FAIL ')+l);if(!c)process.exitCode=1};
const clone=o=>JSON.parse(JSON.stringify(o));
const tables={app_config:[],tg_links:[],tg_codes:[],tg_inbox:[],reminders:[]};let failKind=false,opened=[];
function builder(t){const st={f:[],ins:[],op:'select',row:null,ord:null,lim:null};
  const exec=()=>{const T=tables[t]=tables[t]||[];const m=r=>st.f.every(([c,v,k])=>k==='in'?v.includes(r[c]):r[c]===v);
    if(st.op==='insert'){if(t==='reminders'&&failKind&&st.row.some&&st.row.some(x=>'kind' in x))return{data:null,error:{message:"Could not find the 'kind' column of 'reminders' in the schema cache"}};
      (Array.isArray(st.row)?st.row:[st.row]).forEach(r=>T.push({id:(T.length||0)+1+Math.random(),...r}));return{data:null,error:null}}
    if(st.op==='delete'){tables[t]=T.filter(r=>!m(r));return{data:null,error:null}}
    let rows=T.filter(m);if(st.ord)rows=rows.slice().sort((a,b)=>st.ord.asc?a[st.ord.c]-b[st.ord.c]:b[st.ord.c]-a[st.ord.c]);if(st.lim)rows=rows.slice(0,st.lim);return{data:rows,error:null}};
  const b={select:()=>b,eq:(c,v)=>{st.f.push([c,v]);return b},in:(c,v)=>{st.f.push([c,v,'in']);return b},order:(c,o)=>{st.ord={c,asc:o&&o.ascending!==false};return b},limit:n=>{st.lim=n;return b},
    insert:r=>{st.op='insert';st.row=r;return b},delete:()=>{st.op='delete';return b},maybeSingle:async()=>{const r=exec();return{data:(r.data||[])[0]||null,error:r.error}},then:(res,rej)=>Promise.resolve(exec()).then(res,rej)};return b}
function makeDevice(){
  const ls={};const toasts=[];
  const sb={auth:{getSession:async()=>({data:{session:null}}),signOut:async()=>{}},rpc:async()=>({data:{ok:true,rev:1}}),from:t=>builder(t),storage:{from:()=>({})}};
  const app={_h:'',classList:{add(){},remove(){}},offsetWidth:0,set innerHTML(v){this._h=v},get innerHTML(){return this._h}};
  const mk=()=>({id:'',style:{},dataset:{},classList:{add(){},remove(){}},_h:'',set innerHTML(v){this._h=v},get innerHTML(){return this._h},remove(){},addEventListener(){},querySelector:()=>null});
  const win={addEventListener(){},scrollY:0,innerWidth:390,innerHeight:800,scrollTo(){},supabase:{createClient:()=>sb},open:(u,t)=>{opened.push(u)}};
  const sandbox={localStorage:{getItem:k=>ls[k]===undefined?null:ls[k],setItem:(k,v)=>{ls[k]=String(v)},removeItem:k=>{delete ls[k]}},window:win,supabase:win.supabase,console,JSON,Date,Math,Promise,Object,Array,Set,Map,String,Number,parseInt,parseFloat,isNaN,Intl,RegExp,Error,Symbol,Uint8Array,encodeURIComponent,decodeURIComponent,URL,Blob,TextEncoder,TextDecoder,
    crypto:{getRandomValues:a=>{for(let i=0;i<a.length;i++)a[i]=Math.floor(Math.random()*256);return a}},
    setTimeout:()=>0,clearTimeout(){},setInterval:()=>1,clearInterval(){},requestAnimationFrame:()=>0,confirm:()=>true,alert(){},scrollTo(){},matchMedia:()=>({matches:false,addEventListener(){}}),
    navigator:{onLine:true,vibrate(){},storage:{},userAgent:'T'},
    document:{addEventListener(){},documentElement:{setAttribute(){},removeAttribute(){},classList:{add(){},remove(){}}},body:{appendChild(){},style:{}},querySelector:s=>s==='#app'?app:({value:'',content:'',innerHTML:''}),querySelectorAll:()=>[],activeElement:null,getElementById:()=>null,createElement:()=>mk(),head:{appendChild(){}}}};
  sandbox.globalThis=sandbox;vm.createContext(sandbox);
  vm.runInContext(SRC+`;S=load();UID='u1';S.ob=1;S.ts=1;globalThis.T={get S(){return S},set S(v){S=v},get TGB(){return TGB},get TGL(){return TGL},get TGW(){return TGW},tgInit,tgLink,tgUnlink,tgApply,tgBlock,remRows,syncRem,remCard,dk,nmOne,ptTimes,bl,render}`,sandbox);
  const T=sandbox.T;T.ls=ls;return T}
(async()=>{
 const D=makeDevice();const today=D.dk();
 // 1) bot not configured -> UI hidden
 await D.tgInit();ok('no bot configured (app_config empty) -> Telegram UI is hidden',D.TGB===''&&D.tgBlock()==='');
 // 2) configured, not linked
 tables.app_config=[{key:'tg_bot',value:'KunlikTizimBot'}];await D.tgInit();
 ok('bot username is read from the server; not linked yet -> "Telegramga ulash" button',D.TGB==='KunlikTizimBot'&&D.TGL===false&&/Telegramga ulash/.test(D.tgBlock()));
 // 3) link: code + deep link
 await D.tgLink();const c=tables.tg_codes[0];
 ok('link creates a one-time code (8 safe chars, user, timezone, expires within 20 min)',c&&/^[A-HJ-NP-Z2-9]{8}$/.test(c.code)&&c.user_id==='u1'&&typeof c.tz==='number'&&new Date(c.expires_at)-Date.now()<=20*60000+1000&&new Date(c.expires_at)>new Date());
 ok('opens Telegram with the deep link https://t.me/BOT?start=CODE',opened[0]==='https://t.me/KunlikTizimBot?start='+c.code&&D.TGW===true);
 // 4) the bot links the chat -> app notices on return
 tables.tg_links=[{user_id:'u1',chat_id:111}];await D.tgInit();
 ok('after the bot links the chat, the app switches Telegram reminders on',D.TGL===true&&D.S.rem.tg===true&&D.TGW===false&&/Telegram ulangan/.test(D.tgBlock()));
 ok('reminders sync even though web push is off (rows reach the server)',tables.reminders.length>0);
 const kinds=tables.reminders.map(r=>r.kind||'');
 ok('reminder rows carry a kind: namoz -> nm:fajr…, schedule blocks -> blk:<id> ('+[...new Set(kinds.map(k=>k.split(':')[0]))].join(',')+')',kinds.some(k=>/^nm:(fajr|dhuhr|asr|maghrib|isha)$/.test(k))&&kinds.some(k=>/^blk:[\w-]+$/.test(k)));
 ok('closing-the-day / custom reminders have no kind (no buttons)',tables.reminders.some(r=>r.title==='Kunni yopish vaqti'&&!r.kind));
 // 5) older database without the kind column
 tables.reminders=[];failKind=true;D.ls['trk_remsig']='';await D.syncRem(true);
 ok('database without the new "kind" column: reminders still sync (retried without kind)',tables.reminders.length>0&&tables.reminders.every(r=>!('kind' in r)));failKind=false;
 // 6) inbox -> state
 D.S.nm.d[today]={fajr:2};D.S.nm.debt.fajr=1;D.S.nm.log.push({id:1,d:today,p:'fajr',k:'miss',n:1});const bid=D.bl()[0].id;
 tables.tg_inbox=[{id:11,user_id:'u1',kind:'nm',payload:{d:today,p:'fajr'},applied:false},{id:12,user_id:'u1',kind:'nm',payload:{d:today,p:'asr'},applied:false},
   {id:13,user_id:'u1',kind:'blk',payload:{d:today,id:bid},applied:false},{id:14,user_id:'u1',kind:'task',payload:{d:today,t:'Telegramdan vazifa'},applied:false},
   {id:15,user_id:'u1',kind:'water',payload:{d:today,n:1},applied:false},{id:16,user_id:'u1',kind:'water',payload:{d:today,n:1},applied:false},
   {id:17,user_id:'u1',kind:'nm',payload:{d:today,p:'../evil'},applied:false},{id:18,user_id:'u1',kind:'blk',payload:{d:today,id:'a b;x'},applied:false},
   {id:19,user_id:'u1',kind:'nm',payload:{d:'2099-01-01',p:'isha'},applied:false},{id:20,user_id:'u1',kind:'hack',payload:{},applied:false}];
 await D.tgApply();const S=D.S;
 ok('prayer button -> prayed (1); a previously missed (qazo) fajr is corrected and its debt/log removed',S.nm.d[today].fajr===1&&S.nm.debt.fajr===0&&!S.nm.log.some(x=>x.p==='fajr'&&x.k==='miss'));
 ok('another prayer marked (asr)',S.nm.d[today].asr===1);
 ok('schedule block marked done',S.done[today]&&S.done[today][bid]===true);
 ok('task added to today\'s list',(S.tasks[today]||[]).some(t=>t.t==='Telegramdan vazifa'&&t.x===0));
 ok('two water messages -> +2 glasses',S.water[today]===2);
 ok('malformed prayer / block ids, future dates and unknown kinds are ignored',!S.nm.d[today]['../evil']&&!(S.done[today]||{})['a b;x']&&!(S.nm.d['2099-01-01'])&&Object.keys(S.nm.d[today]).every(k=>/^(fajr|asr)$/.test(k)));
 ok('processed inbox rows are deleted from the server',tables.tg_inbox.length===0&&S.tgd.length===10);
 // 7) idempotent: same rows delivered again must not double count
 tables.tg_inbox=[{id:15,user_id:'u1',kind:'water',payload:{d:today,n:1},applied:false},{id:14,user_id:'u1',kind:'task',payload:{d:today,t:'Telegramdan vazifa'},applied:false}];
 await D.tgApply();ok('re-delivered rows (same ids) are not applied twice',S.water[today]===2&&S.tasks[today].filter(t=>t.t==='Telegramdan vazifa').length===1&&tables.tg_inbox.length===0);
 // 8) not linked -> nothing happens
 const E=makeDevice();tables.tg_inbox=[{id:30,user_id:'u1',kind:'water',payload:{d:today,n:1},applied:false}];await E.tgApply();ok('without a linked Telegram the inbox is left untouched',tables.tg_inbox.length===1&&!(E.S.water[today]));
 // 9) unlink
 tables.reminders=[{user_id:'u1',x:1}];await D.tgUnlink();ok('unlink removes the link, switches Telegram reminders off and clears reminder rows',tables.tg_links.length===0&&D.S.rem.tg===false&&D.TGL===false&&tables.reminders.length===0);
 // 10) settings card shows both options
 const html=D.remCard();ok('reminders card offers the push button and the Telegram button when nothing is on',/Bildirishnomani yoqish/.test(html)&&/Telegramga ulash/.test(html));

 // ================= zikr + fasting =================
 {
 const Z=makeDevice();Z.S.rem.tg=true;tables.tg_links=[{user_id:'u1',chat_id:1}];tables.app_config=[{key:'tg_bot',value:'B'}];await Z.tgInit();const day=Z.dk();
 Z.S.rem.zk=true;Z.S.rem.on=false;let rows=Z.remRows();const zr=rows.filter(r=>/^zk:/.test(r.kind||''));
 ok('zikr toggle -> two reminder rows: 06:30 zk:sb and 18:30 zk:sh',zr.length===2&&zr.some(r=>r.kind==='zk:sb'&&r.hhmm==='06:30')&&zr.some(r=>r.kind==='zk:sh'&&r.hhmm==='18:30'));
 Z.S.rem.zk=false;ok('zikr toggle off -> no zikr rows',Z.remRows().every(r=>!/^zk:/.test(r.kind||'')));
 Z.S.rem.rz=true;Z.S.rz.start='2000-01-01';ok('fasting reminder is NOT created outside Ramadan',Z.remRows().every(r=>r.kind!=='rz'));
 const st=new Date();st.setDate(st.getDate()-5);Z.S.rz.start=st.toLocaleDateString('sv');rows=Z.remRows();
 ok('during Ramadan the fasting reminder (21:30, kind rz) is created',rows.some(r=>r.kind==='rz'&&r.hhmm==='21:30'));
 // apply
 tables.tg_inbox=[{id:51,user_id:'u1',kind:'zk',payload:{d:day,c:'sb'},applied:false},{id:52,user_id:'u1',kind:'rz',payload:{d:day,v:1},applied:false},{id:53,user_id:'u1',kind:'zk',payload:{d:day,c:'zz'},applied:false},{id:54,user_id:'u1',kind:'rz',payload:{d:day,v:9},applied:false}];
 await Z.tgApply();const D=Z.S.dz.d[day]||{};const sbItems=Z.S.dz&&Object.keys(D).filter(k=>k.endsWith('@sb')).length;
 ok('zikr button marks the whole morning set as done (every item reaches its target)',sbItems>=8&&Object.entries(D).filter(([k])=>k.endsWith('@sb')).every(([k,v])=>v>=1));
 ok('evening set untouched; invalid category ignored',!Object.keys(D).some(k=>k.endsWith('@sh')||k.endsWith('@zz')));
 ok('fasting "Tutdim" button -> today marked as fasted (1); invalid value ignored',Z.S.rz.fast[day]===1);
 tables.tg_inbox=[{id:61,user_id:'u1',kind:'rz',payload:{d:day,v:2},applied:false}];await Z.tgApply();
 ok('fasting "Tutolmadim" -> qazo (2): debt +1 and logged',Z.S.rz.fast[day]===2&&Z.S.rz.debt===1&&Z.S.rz.log.some(x=>x.d===day&&x.k==='miss'));
 tables.tg_inbox=[{id:62,user_id:'u1',kind:'rz',payload:{d:day,v:1},applied:false}];await Z.tgApply();
 ok('changing qazo back to fasted removes the debt and the log entry',Z.S.rz.fast[day]===1&&Z.S.rz.debt===0&&!Z.S.rz.log.some(x=>x.d===day&&x.k==='miss'));
 ok('settings card shows both new toggles',/Ertalabki va kechki zikr/.test(Z.remCard())&&/ro‘za belgilash/.test(Z.remCard()));
 }
})();
