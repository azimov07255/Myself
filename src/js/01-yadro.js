
// 1) Supabase kalitini shu yerga qo‘ying (Project Settings → API → anon public key)
const CFG={url:'https://dsfwagfsehpugjkervqc.supabase.co',key:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRzZndhZ2ZzZWhwdWdqa2VydnFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3MjcwNTksImV4cCI6MjEwODMwMzA1OX0.-fUlJz-VU3Y3_PkpfHsbFkCFsRTCBeJJ5qXs-ZiAMq8'};
const sb=(CFG.key&&window.supabase)?supabase.createClient(CFG.url,CFG.key):null;

const DAYS=['Yakshanba','Dushanba','Seshanba','Chorshanba','Payshanba','Juma','Shanba'];
const MON=['yanvar','fevral','mart','aprel','may','iyun','iyul','avgust','sentabr','oktyabr','noyabr','dekabr'];
const M=(h,m=0)=>h*60+m;
const ALL=[0,1,2,3,4,5,6],WD=[1,2,3,4,5],GYM=[1,3,5,6],NG=[0,2,4];
// Jadval: s/e daqiqada, e>1440 bo‘lsa yarim tundan o‘tadi. Hamma narsa shu yerda o‘zgartiriladi.
const BL=[
{id:'uyg',t:'Uyg‘onish',n:'Tur, tahorat, namoz, suv ich.',s:M(5),e:M(6),d:ALL},
{id:'qur',t:'Qur‘on',n:'3 bet yodlash, takror, kunlik hatm.',s:M(6),e:M(9),d:ALL},
{id:'dok',t:'Dokon',n:'Mijoz kam paytda IELTS listening va lug‘at.',s:M(9),e:M(17),d:ALL},
{id:'yol',t:'Yo‘l va ovqat',n:'Univerga tayyorlan.',s:M(17),e:M(18),d:WD},
{id:'uni',t:'Univer',n:'Darsda to‘liq qatnash.',s:M(18),e:M(20,50),d:WD},
{id:'dam',t:'Ovqat va dam',n:'Yengil ovqat, 20 daqiqa dam.',s:M(20,50),e:M(21,15),d:WD},
{id:'iel',t:'IELTS',n:'Reading yoki writing mashqi.',s:M(21,15),e:M(22),d:WD},
{id:'zal',t:'Zal',n:'Mashq, cho‘zilish, suv.',s:M(22),e:M(24),d:GYM},
{id:'mol',t:'Pul hisobi va ertangi reja',n:'Kirim-chiqimni yoz, ertangi 3 ta ishni belgila.',s:M(22),e:M(22,45),d:[2,4]},
{id:'hft',t:'Haftalik tahlil',n:'Haftani ko‘rib chiq, keyingi haftani rejala.',s:M(18),e:M(19),d:[0]},
{id:'uyqu1',t:'Uxlash',n:'Telefon chetga. Ertaga 05:00.',s:M(23),e:M(29),d:NG},
{id:'uyqu2',t:'Uxlash',n:'Telefon chetga. Ertaga 05:00.',s:M(24),e:M(29),d:GYM}
];
const RULES=[{id:'ig',t:'Instagramsiz kun'},{id:'ph',t:'Yotishdan oldin 30 daqiqa telefonsiz'},{id:'sl',t:'Rejadagi vaqtda uxlashga yotdim'}];
const GOALS=['Hofizi Qur‘on bo‘lish','IELTS 8–9 ball','O‘qituvchi bo‘lib ishlash','Prava olish','Zalda yaxshi tana qurish'];

const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const pad=n=>String(n).padStart(2,'0');
const hm=m=>pad(Math.floor(m/60)%24)+':'+pad(m%60);
const dk=()=>new Date().toLocaleDateString('sv');
const fmt=m=>m>=60?Math.floor(m/60)+' soat '+(m%60?m%60+' daqiqa':''):m+' daqiqa';
const num=n=>Number(n).toLocaleString('ru-RU');
const blank=()=>({ts:0,done:{},tasks:{},rules:{},wake:{},goals:[],ob:0,md:{cur:'Asosiy',sets:{}},money:[],name:'',main:0,ai:{chat:[],sh:{core:1,quran:1,study:1,health:1,money:0},tip:{}},debts:[],rz:{start:'',fast:{},tar:{},debt:0,log:[]},pt:{loc:'Toshkent',lat:41.2995,lon:69.2401,tune:{},cache:null},nh:{p:0,c:0,log:[],hist:[],pr:'fajr'},sg:0,kt:{books:[],log:[],goal:20},nm:{d:{},debt:{},log:[],qb:{}},ie:{words:[],mock:[],wr:[],target:7,ex:'',tests:[],dp:{},dr:''},un:{tasks:[],exams:[],subj:[],tt:{},gr:{},ab:{}},qa:{list:[],rate:1,rep:'off'},dz:{d:{}},tgd:[],pr:{er:{},pm:18,st:['Nazariy kursga yozilish','Nazariy testlarni ishlash','Nazariy imtihonni topshirish','Amaliy mashg‘ulotlar','Amaliy imtihonni topshirish','Pravani olish'].map(t=>({t,x:0})),tests:[],exam:''},iso:{lim:60,m:{},log:[]},rem:{on:false,tg:false,yo:false,zk:false,rz:false,zam:'06:30',zpm:'18:30',blk:true,off:5,close:true,ct:'21:30',wake:true,custom:[],sd:''},top:{},close:{},gym:{log:[],body:[],ex:[],plan:{},pass:null,past:[],food:{goal:{kcal:2500,p:150,f:70,c:300},log:{}}},fin:{budget:0,goal:{t:'',a:0,s:0},open:{p:{cash:0,card:0},d:{cash:0,card:0}},sg:[]},hab:[],hb:{},mood:{},water:{},note:{},fm:{},bl:null,wk:{base:0,start:null},q:{ppd:3,cur:0,m:{},ord:[],rv:0,rg:5,rd:{},hp:0,hg:20,hc:0,hd:{}},z:{sel:0,c:{}}});

let BV='j',SDO={},IVW='b',IK='L',IQ=null,IQS='',WE={k:2,p:'',run:false,end:0,open:0},SPQ=null,IT=null,URG=null,PSim=null,PSel=[],PTB=false,RM=0,RMN=false,CRS=-1,NMo=0,EV='i',IR=0,PULLED=!sb,OB=1,OBN='',OBC='',OBG=[],OBP='talaba';
let OT='j',WK=0,FC=0,GN='',GS='',GR='',GK='',BW='',BC='',BB='',BA='';
let VD=null,WO=0,HMo=0,YS=-1,YA=1,YB=3,LJ=false,FL=25,FE=0,FS=1500,FR=null;
let QT='y',LO=false,ED=null,ALLV=false;
let OW=null,OL='',OP='',ON='',OE='',OC=null;
let S=blank(),UID=null,tab='h',W='p',K='out',FA='',FN='',tm=null;
const KEY=()=>'trk_'+(UID||'local');
const isObj=x=>x&&typeof x==='object'&&!Array.isArray(x);
function fillDef(a,b){for(const k in b){if(a[k]===undefined)a[k]=JSON.parse(JSON.stringify(b[k]));else if(isObj(a[k])&&isObj(b[k]))fillDef(a[k],b[k])}return a}
const norm=o=>syIds(fillDef(o,blank()));
function load(){try{return norm(Object.assign(blank(),JSON.parse(localStorage.getItem(KEY())||'{}')))}catch(e){return blank()}}
function save(){rwReset();syIds(S);S.ts=Date.now();try{localStorage.setItem(KEY(),JSON.stringify(S))}catch(e){}clearTimeout(tm);tm=setTimeout(push,700);if(S.rem&&(S.rem.on||S.rem.tg))remSoon();render();if(!CELB){CELB=1;setTimeout(()=>{CELB=0;try{celeb()}catch(e){}},200)}}
const APP_VER='2026.12.19-5';
const APP_BUILD='{{BUILD}}'; // yig'ishda (tools/build_app.py) o'zgarmas identifikatorga almashadi; ilova shuni version.json bilan solishtirib, yangi versiya borligini biladi
// Mushaf bo‘limi: 'all' = yoqilgan, 'off' = butunlay o‘chirilgan (do‘stlarga beriladigan versiyada shu qatorni 'off' qiling).
const MUSHAF_MODE='all';
const lsGet=k=>{try{return localStorage.getItem(k)}catch(e){return null}},lsSet=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}},lsRm=k=>{try{localStorage.removeItem(k)}catch(e){}};
let REV=null,NORPC=false,SYNCING=false,PUSHQ=false,MERGED=0,LPL=0;
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b),idArr=a=>Array.isArray(a)&&a.every(x=>isObj(x)&&x.id!==undefined);
// Uch tomonlama birlashtirish: B = oxirgi sinxronlangan nusxa, L = shu qurilma, R = server. O‘chirishlar ham hisobga olinadi.
function mrg(B,L,R){
  if(same(L,R))return L;
  if(same(B,L))return R;
  if(same(B,R))return L;
  if(isObj(L)&&isObj(R)){const b=isObj(B)?B:{},o={};
    for(const k of new Set([...Object.keys(L),...Object.keys(R)])){const inL=k in L,inR=k in R,inB=k in b;
      if(inL&&inR)o[k]=mrg(b[k],L[k],R[k]);
      else if(inL){if(inB&&same(b[k],L[k]))continue;o[k]=L[k]}
      else{if(inB&&same(b[k],R[k]))continue;o[k]=R[k]}}
    return o}
  if(idArr(L)&&idArr(R)){const Bb=idArr(B)?B:[],mb=new Map(Bb.map(x=>[x.id,x])),ml=new Map(L.map(x=>[x.id,x])),mr=new Map(R.map(x=>[x.id,x])),out=[];
    for(const id of [...R.map(x=>x.id),...L.filter(x=>!mr.has(x.id)).map(x=>x.id)]){const inL=ml.has(id),inR=mr.has(id),inB=mb.has(id);
      if(inL&&inR)out.push(mrg(mb.get(id),ml.get(id),mr.get(id)));
      else if(inR){if(inB&&same(mb.get(id),mr.get(id)))continue;out.push(mr.get(id))}
      else{if(inB&&same(mb.get(id),ml.get(id)))continue;out.push(ml.get(id))}}
    return out}
  return L}
function dedupeHab(s){const seen=new Set();s.hab=(s.hab||[]).filter(x=>{const k=hnorm(x.t||'');if(seen.has(k))return false;seen.add(k);return true})}
const baseKey=()=>'trk_base_'+UID,getBase=()=>{try{return JSON.parse(lsGet(baseKey())||'null')}catch(e){return null}};
function setBase(s){lsSet(baseKey(),JSON.stringify(s));lsSet('trk_rev_'+UID,String(REV));lsSet('trk_sts_'+UID,String(s.ts||0))}
const isNoRpc=e=>e&&(e.code==='PGRST202'||/Could not find the function|save_state|schema cache/i.test(e.message||''));
let SYNC=navigator.onLine===false?'off':'ok';
async function push(){
  if(!(sb&&UID))return;if(SYNCING){PUSHQ=true;return}SYNCING=true;
  try{for(let i=0;i<4;i++){
      const snap=JSON.parse(JSON.stringify(S));
      if(NORPC){const r=await sb.from('app_state').upsert({user_id:UID,data:snap,updated_at:new Date().toISOString()});if(r&&r.error)throw r.error;SYNC='ok';lsRm('trk_dirty');break}
      const r=await sb.rpc('save_state',{p_data:snap,p_base:REV});
      if(r.error){if(isNoRpc(r.error)){NORPC=true;continue}throw r.error}
      const d=r.data;
      if(d&&d.ok){REV=d.rev;setBase(snap);SYNC='ok';lsRm('trk_dirty');break}
      const R=norm(Object.assign(blank(),(d&&d.data)||{})),m=mrg(getBase()||{},S,R);   // asos bo‘lmasa, hech narsa yo‘qolmaydi (birlashtiriladi)
      S=norm(Object.assign(blank(),m));dedupeHab(S);S.ts=Date.now();REV=d.rev;lsSet(KEY(),JSON.stringify(S));MERGED=1}}
  catch(e){SYNC='wait';lsSet('trk_dirty','1')}
  SYNCING=false;
  if(MERGED){MERGED=0;try{toast('Boshqa qurilmadagi o‘zgarishlar qo‘shildi')}catch(e){}render()}
  if(PUSHQ){PUSHQ=false;push()}}
async function pull(){
  if(!sb||!UID)return false;
  try{let r=null;
    if(!NORPC){r=await sb.from('app_state').select('data,rev').eq('user_id',UID).maybeSingle();if(r.error&&/rev/.test(r.error.message||'')){NORPC=true;r=null}}
    if(!r)r=await sb.from('app_state').select('data').eq('user_id',UID).maybeSingle();
    if(r.error)return false;PULLED=true;
    const row=r.data,d=row&&row.data;
    if(!d||!Object.keys(d).length){if(S.ts)push();return false}
    const srv=row.rev!=null?row.rev:null;
    if(NORPC||srv==null){if((d.ts||0)>(S.ts||0)){S=norm(Object.assign(blank(),d));return true}if(S.ts)push();return false}
    const sts=+lsGet('trk_sts_'+UID)||0,unsynced=(S.ts||0)>sts,R=norm(Object.assign(blank(),d));
    if(REV===srv){if(unsynced)push();return false}
    if(REV==null){REV=srv;if((d.ts||0)>(S.ts||0)){S=R;setBase(S);lsSet(KEY(),JSON.stringify(S));return true}push();return false}
    if(!unsynced){S=R;REV=srv;setBase(S);lsSet(KEY(),JSON.stringify(S));return true}
    S=norm(Object.assign(blank(),mrg(getBase()||{},S,R)));dedupeHab(S);S.ts=Date.now();REV=srv;lsSet(KEY(),JSON.stringify(S));push();return true
  }catch(e){return false}}

function nowInfo(){
  const d=new Date(),n=d.getHours()*60+d.getMinutes(),today=rjDay(dk());
  for(const b of today){
    if(n>=b.s&&n<b.e)return{b,nn:n};
    if(n+1440>=b.s&&n+1440<b.e)return{b,nn:n+1440};
  }
  return{nx:today.filter(b=>b.s>n).sort((a,c)=>a.s-c.s)[0],n};
}

const QUOTES=['Ilm olish — beshikdan qabrgacha.','Kichik qadamlar har kuni, katta natija har yili.','Bugungi ish ertaga qolmasin.','Sabr bilan qilingan mehnat so‘nmaydi.','Vaqt — eng qimmat omonat.'];
function scoreOf(k){const day=new Date(k+'T12:00').getDay(),dn=S.done[k]||{},rd=S.rules[k]||{},hb=S.hb[k]||{},tk_=(S.tasks[k]||[]).concat(S.top[k]||[]);
  const c=bl().filter(b=>rjIn(b,k,day)&&!b.id.startsWith('uyqu')),tot=c.length+RULES.length+S.hab.length+tk_.length;
  const got=c.filter(b=>dn[b.id]).length+RULES.filter(r=>rd[r.id]).length+S.hab.filter(h=>hb[h.id]).length+tk_.filter(t=>t.x).length;
  return{tot,got,p:tot?Math.round(got/tot*100):0}}

function vd(k){VD=k===dk()?null:k;render();scrollTo(0,0)}
function pn(i){S.main=i;save()}
function hozir(){
  const T0=dk(),k=cd(),isT=k===T0,fu=k>T0,dn=S.done[k]||{},rd=S.rules[k]||{},hb=S.hb[k]||{},tasks=S.tasks[k]||[],d=new Date(k+'T12:00'),I=nowInfo(),day=d.getDay(),hr=new Date().getHours();
  const all=bl().map((b,i)=>({b:rjOv(b,k),i})),td=all.filter(x=>rjIn(x.b,k,day)).sort((a,c)=>a.b.s-c.b.s),list=ALLV?all.slice().sort((a,c)=>a.b.s-c.b.s):td;
  const{tot,got,p:sc}=scoreOf(k),C=2*Math.PI*20,X=isT?xpInfo():null;
  const act=(f)=>fu?'':f;
  let hero;
  if(isT&&I.b){const b=I.b,sl=b.id.startsWith('uyqu'),fr=Math.min(1,(I.nn-b.s)/(b.e-b.s)),R=2*Math.PI*30,nx=td.find(x=>x.b.s>=b.e&&!x.b.id.startsWith('uyqu'));
    hero=`<section class="hero"><div style="display:flex;justify-content:space-between;gap:12px"><div><p class="lab">Hozir</p><h1>${esc(b.t)}</h1><p>${b.pt?hm(b.s)+' da':hm(b.s)+' dan '+hm(b.e)+' gacha'}</p></div>${b.pt?'<span style="font-size:46px">📍</span>':`<svg width="76" height="76" viewBox="0 0 76 76"><circle cx="38" cy="38" r="30" fill="none" stroke="rgba(128,128,128,.3)" stroke-width="6"/><circle cx="38" cy="38" r="30" fill="none" stroke="var(--hlab)" stroke-width="6" stroke-linecap="round" stroke-dasharray="${R*fr} ${R}" transform="rotate(-90 38 38)"/><text x="38" y="43" text-anchor="middle" font-size="14" font-weight="700" fill="var(--htx)">${Math.round(fr*100)}%</text></svg>`}</div><p class="mu">${b.pt?'':fmt(b.e-I.nn)+' qoldi. '}${esc(b.n||'')}</p>${nx?`<p class="mu">Keyingisi: ${esc(nx.b.t)}, ${hm(nx.b.s)} da${nx.b.tr?' · 🚶 '+hm(nx.b.s-nx.b.tr)+' da yo‘lga chiq':''}</p>`:''}${sl?'':`<div class="hbt"><button class="big ${dn[b.id]?'ok':''}" onclick="tg('${b.id}')">${dn[b.id]?'Bajarildi':'Bajardim'}</button>${dn[b.id]?'':`<button class="hbs" onclick="f5Start(this.dataset.t)" data-t="${esc(b.t)}" aria-label="Faqat 5 daqiqa">⚡ 5 daq</button><button class="hbs" onclick="rjShift(30)" aria-label="Kechikdim: 30 daqiqa">⏩ +30</button>${ttOn()?`<button class="hbs" onclick="jdTimer('${b.id}')" aria-label="Taymer bilan boshlash">⏱ Taymer</button>`:''}`}</div>`}</section>`;
  }else if(isT)hero=`<section class="hero"><p class="lab">Hozir</p><h1>Bo‘sh vaqt</h1><p class="mu">${I.nx?`Keyingisi: ${esc(I.nx.t)}, ${hm(I.nx.s)} da.`:'Bugungi jadval tugadi.'}</p></section>`;
  else hero=`<section class="hero"><p class="lab">${fu?'Kelgusi kun rejasi':'O‘tgan kun'}</p><h1>${d.getDate()} ${MON[d.getMonth()]}</h1><p>${DAYS[day]}</p><p class="mu">${tot} ta belgi, ${got} tasi bajarilgan, ball ${sc}%</p><button class="big" onclick="vd('${T0}')">Bugunga qaytish</button></section>`;
  const nmn=new Date(),nowM=nmn.getHours()*60+nmn.getMinutes(),part=s=>s<720?'Ertalab':s<1080?'Kunduzi':s<1320?'Kechqurun':'Tun';
  let cD=0,cM=0,cL=0,lastP='',lineDone=false,ix=0;
  const rowsA=list.map(({b,i})=>{
    const x=dn[b.id],sl=b.id.startsWith('uyqu'),cur=isT&&I.b&&I.b.id===b.id,ended=isT?(b.e<=nowM):!fu,miss=ended&&!x&&!sl&&!cur,f=act(`tg('${b.id}')`);
    if(!sl){if(x)cD++;else if(miss)cM++;else cL++}
    let st='';
    if(x)st='Bajarildi';else if(cur)st=b.pt?'Hozir vaqti keldi':fmt(b.e-I.nn).trim()+' qoldi';else if(miss)st='O‘tkazib yuborilgan';else if(isT&&b.s>nowM&&b.s-nowM<=180)st=fmt(b.s-nowM).trim()+'dan keyin';
    let o='';
    if(part(b.s)!==lastP){lastP=part(b.s);o+=`<p class="mu pt">${lastP}</p>`}
    if(isT&&!I.b&&!lineDone&&b.s>nowM){lineDone=true;o+=`<div class="nowl"><span>${hm(nowM)}</span></div>`}
    const fr=cur?Math.min(100,(I.nn-b.s)/(b.e-b.s)*100):0;
    return {b,o,miss,h:`<div class="tl ${x?'done':cur?'now':miss?'miss':''}" data-ty="${rjTy(b)}" data-bid="${b.id}" data-k="${k}" style="--ty:${rjCol(b)};animation-delay:${Math.min(ix++,10)*.05+.15}s"><div class="tt"><b>${hm(b.s)}</b><span>${b.pt?'📍 lahza':fmt(b.e-b.s).trim()}</span></div><div class="tc"><span class="ck" onclick="${f}">${x?'✓':''}</span></div><div class="tb"><div style="display:flex;justify-content:space-between;gap:8px"><span class="t" onclick="${f}">${rjIc(b)}${esc(b.t)}</span>${jdMv(b)}<button class="x" onclick="eb(${i})">✎</button></div>${st?`<p class="mu" style="margin:2px 0 0;font-size:13px${miss?';color:var(--bad)':''}">${st}</p>`:''}${ALLV?`<p class="mu" style="margin:2px 0 0;font-size:12px">${b.d.length===7?'Har kuni':b.d.map(j=>DAYS[j].slice(0,2)).join(' ')}</p>`:''}${cur&&!b.pt?`<div class="bar" style="margin-top:8px"><i style="width:${fr}%"></i></div>`:''}</div></div>`}}); const rows=jdGroup(rowsA,k,isT,I,nowM); const sm=`<div style="margin-bottom:4px"><span class="chip" style="color:var(--ac)">${cD} bajarildi</span><span class="chip">${cL} qoldi</span>${cM?`<span class="chip bad">${cM} o‘tkazildi</span>`:''}</div>`;
  const chk=(on,fn,t)=>`<button class="row ${on?'done':''}" onclick="${act(fn)}"><span class="ck">${on?'✓':''}</span><span class="t">${esc(t)}</span></button>`;
  const hh=S.hab.length?S.hab.map(x=>chk(hb[x.id],`hbT('${x.id}','${k}')`,(x.e?x.e+' ':'')+x.t+(!hb[x.id]&&hkOn(k,x.id)?' · dam kuni':''))).join('')+hbRest(k):'<p class="mu">Odat bo‘limida o‘z odatlaringni yoz, ular shu yerda ko‘rinadi.</p>';
  const rr=RULES.map(r=>chk(rd[r.id],`rl('${r.id}')`,r.t)).join('');
  const nmB=PR.map(([pp,t])=>{const s_=((S.nm.d[k]||{})[pp])||0;return `<button class="${s_===1?'on':s_===2?'bad':''}" onclick="nmS('${k}','${pp}')">${s_===1?'✓ ':s_===2?'✗ ':''}${t}${ptT(PK[pp])?`<small>${ptT(PK[pp])}</small>`:''}</button>`}).join(''),qzT=Object.values(S.nm.debt).reduce((a,c)=>a+c,0);
  const tt=tasks.map((t,i)=>`<div class="row ${t.x?'done':''}"><span class="ck" onclick="tk(${i})">${t.x?'✓':''}</span><span class="t" onclick="tk(${i})">${esc(t.t)}</span><button class="x" onclick="dt(${i})">×</button></div>`).join('');
  const bs=new Date();bs.setDate(bs.getDate()+WO*7);const w0=(bs.getDay()+6)%7;
  const wk=[...Array(7)].map((_,i)=>{const x=new Date(bs.getFullYear(),bs.getMonth(),bs.getDate()-w0+i),kk=x.toLocaleDateString('sv');return `<button class="wd ${kk===k?'on':''} ${kk===T0?'t':''}" onclick="vd('${kk}')"><span>${DAYS[x.getDay()].slice(0,2)}</span><b>${x.getDate()}</b><i class="dot ${scoreOf(kk).p>0?'y':''}"></i></button>`}).join('');
  const mv=S.mood[k]||0,wt_=S.water[k]||0,fm=S.fm[k]||0,left=Math.max(0,FR?Math.ceil((FE-Date.now())/1000):FS);
  const faces=['😞','🙁','😐','🙂','😄'].map((f,i)=>`<button class="${mv===i+1?'on':''}" onclick="S.mood[cd()]=${i+1};save()">${f}</button>`).join('');
  const gls=[...Array(8)].map((_,i)=>`<button class="gl ${i<wt_?'on':''}" onclick="wt(${i<wt_?i:i+1})"></button>`).join('');
  let avg=0;const bars=[...Array(14)].map((_,i)=>{const kk=dAgo(13-i),p=scoreOf(kk).p;avg+=p;return `<div style="flex:1;text-align:center"><div style="height:80px;display:flex;align-items:flex-end"><div style="width:100%;height:${Math.max(4,p*.8)}px;background:${i===13?'var(--go)':'var(--ac)'};opacity:${i===13?1:.7};border-radius:4px"></div></div><span class="mu" style="font-size:11px">${DAYS[new Date(kk+'T12:00').getDay()].slice(0,2)}</span></div>`}).join('');
  const nm=new Date();const np=isT?(nm.getHours()*60+nm.getMinutes()-300)/1140*100:-1;
  const path=td.filter(x=>!x.b.id.startsWith('uyqu')).map(({b})=>{const s=Math.max(300,b.s),e=Math.min(1440,b.e);return `<i class="${dn[b.id]?'':'n'}" data-ty="${rjTy(b)}" style="--ty:${rjCol(b)};left:${(s-300)/11.4}%;width:${Math.max(.5,(e-s)/11.4)}%"></i>`}).join('')+(np>=0&&np<=100?`<u style="left:${np}%"></u>`:'');
  const mg=S.goals[S.main],mn=mg&&(mg.ms||[]).find(m=>!m.x);
  const msg=sc>=100?'Mashallah, kun mukammal!':sc>=60?`Zo‘r ketyapsan. Yana ${tot-got} ta belgi qoldi.`:sc>0?`Boshlading, davom et. Qolgan: ${tot-got} ta.`:'Kun endigina boshlandi. Birinchi belgini hozir qo‘y.';
  const head=isT?`<p class="mu" style="margin:0">${d.getDate()} ${MON[d.getMonth()]}, ${DAYS[day]}${navigator.onLine===false?' <span class="chip bad">internet yo‘q</span>':''}${subChip()}</p><h1 class="gr">${hr<12?'Xayrli tong':hr<18?'Xayrli kun':'Xayrli kech'}${S.name?', '+esc(S.name):''}</h1><p class="mu qt">“${QUOTES[Math.floor(Date.now()/864e5)%QUOTES.length]}”</p>`:`<p class="mu" style="margin:0">${fu?'Rejalashtirish':'Kunni ko‘rish'}</p><h1 class="gr">${DAYS[day]}, ${d.getDate()} ${MON[d.getMonth()]}</h1>`;
  const topC=topCard(k,fu),rit=isT&&(hr>=20||(S.close[k]||{}).d)?ritual(k,sc):'';
  const wkTop=isT&&hr<11&&!S.wake[k]?wakeC():'';
  const mgRow=mg?`<button class="row" style="margin-top:10px;border-left-color:var(--go)" onclick="go('m')"><span style="font-size:22px">🎯</span><span class="t"><span class="mu" style="font-size:12px">Asosiy maqsad, ${gpct(mg)}%</span><br>${esc(mg.t)}${mn?`<br><span class="mu" style="font-size:12px">Keyingi qadam: ${esc(mn.t)}</span>`:''}</span></button>`:'';
  const focus=isT?`<section class="hero" style="margin-top:14px"><p class="lab">Fokus taymer</p><h1 id="ft" style="font-size:54px">${fmtT(left)}</h1><p class="mu">Bugun: ${fm} daqiqa</p>${fkUi()}<div class="in" style="margin-top:10px">${[15,25,50].map(m=>`<button class="btn s" style="${FL===m?'outline:2px solid var(--hlab)':''}" onclick="fset(${m})">${m} daq</button>`).join('')}</div><button class="big" style="margin-top:0" onclick="fgo()">${FR?'To‘xtatish':'Boshlash'}</button><button class="ghost" style="color:var(--htx)" onclick="frs()">Qayta</button></section>`:'';
  const jadval=`<h2>Kun yo‘li</h2><div class="path">${path}</div><div class="h mu" style="display:flex;justify-content:space-between;font-size:12px;margin-top:4px"><span>05:00</span><span>24:00</span></div>
  <h2>${ALLV?'Barcha rejalar':'Kun jadvali'}</h2>${sm}${ALLV?'':(isT?swHint():'')+rjDayInfo(k,isT)}${rows}
  <div class="in"><button class="btn s" onclick="eb(-1)">Reja qo‘shish</button><button class="btn s" onclick="eb1()">＋ Faqat shu kunga</button><button class="btn s" onclick="ALLV=!ALLV;render()">${ALLV?'Faqat bu kun':'Barcha rejalar'}</button></div>`;
  const kunlik=`<h2>Namozlar</h2>${ptNext()?`<p class="mu" style="margin:0 0 8px">Keyingi namoz: <b style="color:var(--tx)">${ptNext().n} ${hm(ptNext().t)}</b>, ${fmt(ptNext().left).trim()} qoldi</p>`:''}<div class="np">${nmB}</div><p class="mu" style="margin:6px 0 0">Bir bosish: o‘qildi, ikki: qazo, uch: bekor.${qzT?` Qazo qarzi: ${qzT} ta.`:''}</p>
  <h2>Odatlar</h2>${hh}<h2>Kun qoidalari</h2>${rr}
  <h2>Qo‘shimcha vazifalar</h2>${tt}<div class="in"><input id="nt" placeholder="Yangi vazifa" onkeydown="if(event.key==='Enter')addT()"><button class="btn" onclick="addT()">Qo‘sh</button></div>`;
  const holat=`${isT&&!wkTop?wakeC():''}${focus}${fu?'':`<h2>Kayfiyat</h2><div class="mood">${faces}</div><h2>Suv: ${wt_} / 8 stakan</h2><div class="in" style="justify-content:space-between">${gls}</div><h2>Kun xulosasi</h2><textarea placeholder="Nimani o‘rgandim? Nima uchun minnatdorman?" onchange="S.note[cd()]=this.value;save()">${esc(S.note[k]||'')}</textarea>`}`;
  const tahlil=`${X?`<div class="st"><div><b>${X.st} kun</b>ketma-ket faol</div><div><b>${X.L}-daraja</b>${X.name}</div><div><b>${sc}%</b>bugungi ball</div></div><div class="bar" style="margin:10px 0 4px"><i style="width:${X.pc}%"></i></div><p class="mu" style="margin:0;font-size:13px">Keyingi darajagacha ${100-X.pc}%. ${msg}</p>`:''}
  <h2>So‘nggi 14 kun <span class="mu" style="font-size:14px;font-family:Figtree,system-ui">o‘rtacha ${Math.round(avg/14)}%</span></h2><div style="display:flex;gap:3px">${bars}</div>${badgeHtml()}`;
  const bvs=[['j','📅 Jadval'],...(bgOn()?[['k','🧩 Kun']]:[]),['m','✅ Kunlik'],['h','💚 Holat'],['t','📊 Tahlil']].map(x=>`<button class="${BV===x[0]?'on':''}" style="font-size:13px;padding:9px 2px" onclick="BV='${x[0]}';render()">${x[1]}</button>`).join('');
  return `<div class="top"><div>${head}</div>
  <svg width="64" height="64" viewBox="0 0 48 48"><circle cx="24" cy="24" r="20" fill="none" stroke="var(--c2)" stroke-width="5"/><circle cx="24" cy="24" r="20" fill="none" stroke="var(--ac)" stroke-width="5" stroke-linecap="round" stroke-dasharray="${C*sc/100} ${C}" transform="rotate(-90 24 24)"/><text x="24" y="28" text-anchor="middle" font-size="12" font-weight="700" fill="var(--tx)">${sc}%</text></svg></div>
  <div class="wk">${wk}</div><div class="in" style="margin-top:6px"><button class="btn s" onclick="WO--;render()">‹</button><button class="btn s" onclick="WO=0;vd('${T0}')">Bugun</button><button class="btn s" onclick="WO++;render()">›</button></div>${(btFold()&&BV!=='j'&&BV!=='k')?btTabs(bvs):btHead(bvs,k,isT)}${edForm()}${(btFold()&&BV!=='j'&&BV!=='k')?'':bgCards(1,[['hero',hero],['rt',isT?rtCard():''],['n3',isT?rjNext3(k,isT):''],['dc',dcCard(k,isT,fu)],['qr',isT?qrCard():'']])+(isT&&bgBars()?bkBar()+wrBar():'')+bgCards(2,[['rw',isT?rwCard():''],['co',isT?coBar():''],['md',mdBar()],['ns',isT?nsMini():''],['ib',isT&&ibN()?ibMini():''],['kc',isT&&new Date().getHours()>=18&&!((S.kc||{})[T0])?kcMini():''],['ey',eyCard(k,isT)],['tq',isT?tqRowToday():''],['km',isT?kmRow():''],['tt',isT?ttRow():''],['cb',isT?cbRow():''],['ml',isT?mlCard():''],['sos',isT?sosCard():''],['zn',isT?znCard():''],['zj',isT?zjCard():''],['st',isT&&[0,6].includes(new Date().getDay())?stMini():''],['rit',rit],['ap',apCard(k,fu)],['wk',wkTop],['rz',rzCard()],['top',topC],['due',dueCard()],['uni',uniCard()],['zk',zkCard()],['mg',mgRow],['ai',aiCard()]])+btFoot(bvs)}${BV==='j'?jadval:BV==='k'?'':BV==='m'?kunlik:BV==='h'?holat:aqCard()+tahlil+wrCard()+hpCard()+askCard()}`;
}

const GT={'Hofizi Qur‘on bo‘lish':['Juz Amma (30-pora) yodlash','5 pora yodlash','10 pora yodlash','20 pora yodlash','30 pora to‘liq yodlash'],'IELTS 8–9 ball':['Diagnostik test topshirish','1000 ta akademik so‘z yodlash','Haftasiga 2 ta Writing','5 ta to‘liq mock test','Imtihonga ro‘yxatdan o‘tish'],'O‘qituvchi bo‘lib ishlash':['Fan va yo‘nalishni aniqlash','Pedagogik kurs yoki sertifikat','Birinchi dars rejasini tayyorlash','Sinov darsi o‘tkazish','Doimiy ish topish'],'Prava olish':['Nazariy kursga yozilish','Nazariy testdan o‘tish','Amaliy mashg‘ulotlar','Imtihonga yozilish','Pravani olish'],'Zalda yaxshi tana qurish':['Mashq dasturini tuzish','Haftasiga 3 marta zalga borish (4 hafta)','Vazn va o‘lchamlarni yozib borish','Oyiga +1 kg mushak','3 oy izchil mashq']};
function gmt(i,j){const g=S.goals[i],t=GT[g.t][j];g.ms=g.ms||[];if(!g.ms.some(m=>m.t===t))g.ms.push({t,x:0});save()}
const GCOL=['var(--ac)','var(--go)','#6f9fd8','#b27ad6','#d96f8f'],GEM=['📖','🎓','🧑‍🏫','🚗','💪'];
function maqsad(){
  let tm=0,td_=0,sp_=0,nd=null;
  const g=S.goals.map((x,i)=>{const ms=x.ms||[],pc=gpct(x),lf=x.dl?Math.ceil((new Date(x.dl)-new Date(dk()))/864e5):null,col=GCOL[i%5],mn=ms.find(m=>!m.x),R=2*Math.PI*26;
    tm+=ms.length;td_+=ms.filter(m=>m.x).length;sp_+=pc;if(lf!==null&&lf>=0&&(nd===null||lf<nd))nd=lf;
    const ml=ms.map((m,j)=>`<div class="row ${m.x?'done':''}"><span class="ck" onclick="gm(${i},${j})">${m.x?'✓':''}</span><span class="t" onclick="gm(${i},${j})">${esc(m.t)}</span><button class="x" onclick="gmd(${i},${j})">×</button></div>`).join('');
    return `<div class="goal" style="border-left:4px solid ${col}"><div class="h"><b style="font:700 19px Fraunces,serif">${x.e||GEM[i]||'🎯'} ${esc(x.t)}</b><span><button class="x" style="font-size:16px;${S.main===i?'color:var(--go)':''}" onclick="pn(${i})">${S.main===i?'★':'☆'}</button><button class="x" onclick="dg(${i})">×</button></span></div>
    <div class="gh"><svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="26" fill="none" stroke="var(--c2)" stroke-width="7"/><circle cx="32" cy="32" r="26" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-dasharray="${R*pc/100} ${R}" transform="rotate(-90 32 32)"/><text x="32" y="37" text-anchor="middle" font-size="14" font-weight="700" fill="var(--tx)">${pc}%</text></svg>
    <div>${x.why?`<p class="mu" style="margin:0 0 6px">Nega: ${esc(x.why)}</p>`:''}<span class="chip">${ms.filter(m=>m.x).length}/${ms.length} bosqich</span><span class="chip ${lf!==null&&lf<0?'bad':''}">${lf===null?'Muddat yo‘q':lf>=0?lf+' kun qoldi':'Muddat o‘tdi'}</span>${pc>=100&&ms.length?'<span class="chip" style="color:var(--ac)">Bajarildi</span>':''}</div></div>
    ${glkUi(x,i)}${mn?`<p style="margin:0 0 8px">Keyingi qadam: <b>${esc(mn.t)}</b></p>`:''}<p style="margin:0 0 8px"><button class="chip" style="border:0;font:inherit" onclick="grw(${i})">🎁 ${x.rw?'Mukofot: '+esc(x.rw):'Mukofot qo‘sh'}</button></p><div class="in"><input type="date" value="${x.dl||''}" onchange="gdl(${i},this.value)"></div>${ml}<div class="in"><input id="gm${i}" placeholder="Yangi bosqich" onkeydown="if(event.key==='Enter')gma(${i})"><button class="btn" onclick="gma(${i})">+</button></div>${ms.length?'':`<p class="mu" style="margin:0 0 6px">Foiz bosqichlardan o‘zi hisoblanadi. Pastga bosqich yoz yoki tayyorini tanla:</p><div class="chips">${(GT[x.t]||[]).map((t,j)=>`<button onclick="gmt(${i},${j})">${esc(t)}</button>`).join('')}</div>`}</div>`}).join('');
  const av=S.goals.length?Math.round(sp_/S.goals.length):0,mm=av>=100?'Hammasi bajarildi. Yangi maqsad qo‘y!':av>=60?'Marraga yaqinsan, to‘xtama.':av>=20?'Yaxshi ketyapsan, bosqichma-bosqich.':'Yo‘l endi boshlandi. Birinchi bosqichni bugun yop.';
  return `<p class="mu" style="margin:0">Maqsadlar</p><h1 class="gr">Katta orzular, kichik bosqichlar</h1>
  ${mqSeg()}${MQV==='g'?`<section class="hero" style="margin-top:12px"><p class="lab">Umumiy jarayon</p><h1 style="font-size:44px">${av}%</h1><div class="bar" style="margin:8px 0"><i style="width:${av}%"></i></div><p class="mu">${S.goals.length} maqsad, ${td_}/${tm} bosqich bajarilgan${nd!==null?`. Eng yaqin muddat: ${nd} kun`:''}. ${mm}</p></section>
  <p class="mu" style="margin:14px 0 8px">Yulduzcha bosilgan maqsad Hozir ekranida asosiy maqsad bo‘lib chiqadi.</p>${(()=>{const X=xpInfo();return `<button class="row" style="margin:10px 0" onclick="rwOpen()"><span class="t">🏆 Yo‘l: ${X.L}-daraja, 🔥 ${X.st} kun, 🪙 ${rwTotals().coins}<br><small class="mu">Bosqich tugatsang +${RWP.ms} XP</small></span><span class="tm">ochish</span></button>`})()}${dualPanel()}${g} <div class="goal"><b>Yangi maqsad</b><div class="in" style="margin-top:8px"><input id="ng" placeholder="Maqsad nomi"></div><div class="in"><input id="nw" placeholder="Nega kerak? (ixtiyoriy)"></div><button class="btn" onclick="addG()">Qo‘shish</button></div>`:MQV==='o'?`${(()=>{const X=xpInfo();return `<button class="row" style="margin:10px 0" onclick="rwOpen()"><span class="t">🏆 Yo‘l: ${X.L}-daraja, 🔥 ${X.st} kun, 🪙 ${rwTotals().coins}<br><small class="mu">Bosqich tugatsang +${RWP.ms} XP</small></span><span class="tm">ochish</span></button>`})()}${bsCard()}${srCard()}${mqLinks()}`:MQV==='f'?`${ttCard()}${pmCard()}`:MQV==='k'?`${nsCard()}${stCard()}${ibCard()}${roCard()}${nyCard()}${hsCard()}${klxCard()}`:MQV==='n'?nafsTab():`${gdCard()}${hwCard()}${scCard()}`}
  `;
}


function odatTab(){ const isA=OT==='w'||OT==='o'||OT==='a',seg=[['j','✅ Odatlar'],['a','📊 Tahlil'],['z','💪 Zal'],['u','😴 Uyqu'],['i','🧘 Isolation']].map(x=>`<button class="${(x[0]==='a'?isA:OT===x[0])?'on':''}" onclick="OT='${x[0]==='a'?(OT==='o'?'o':'w'):x[0]}';render()">${x[1]}</button>`).join(''),sw=isA?`<div class="seg" style="margin-top:8px"><button class="${OT!=='o'?'on':''}" onclick="OT='w';render()">Hafta</button><button class="${OT==='o'?'on':''}" onclick="OT='o';render()">Oy va yil</button></div>`:''; return `<div class="seg">${seg}</div>${sw}${OT==='j'?odatlar():OT==='w'||OT==='a'?hafta():OT==='o'?oy():OT==='z'?zal():OT==='u'?slpView():iso()}`}
function hafta(){
  const b=new Date();b.setDate(b.getDate()+WK*7);const w0=(b.getDay()+6)%7,T0=dk(),q=S.q;
  const days=[...Array(7)].map((_,i)=>new Date(b.getFullYear(),b.getMonth(),b.getDate()-w0+i).toLocaleDateString('sv'));
  const past=days.filter(k=>k<=T0),sc=days.map(k=>k>T0?null:scoreOf(k).p),vs=sc.filter(v=>v!==null),avg=vs.length?Math.round(vs.reduce((a,c)=>a+c,0)/vs.length):0;
  const sum=f=>past.reduce((a,k)=>a+(f(k)||0),0);
  const wl=past.filter(k=>S.wake[k]),wavg=wl.length?Math.round(wl.reduce((a,k)=>a+t2m(S.wake[k]),0)/wl.length):0,hit=S.wk.start?wl.filter(k=>t2m(S.wake[k])<=tgtFor(k)).length:0;
  const ig=sum(k=>(S.rules[k]||{}).ig?1:0),hp=sum(k=>q.hd[k]),rv=r1(sum(k=>q.rd[k])),ay=sum(k=>((q.ty||{})[k]||[]).filter(e=>e.x).reduce((a,e)=>a+e.b-e.a+1,0)),zk=sum(k=>Object.values(S.z.c[k]||{}).reduce((a,c)=>a+c,0)),fc=sum(k=>S.fm[k]);
  const pm=S.money.filter(m=>m.w==='p'&&days.includes(m.d)),pin=pm.filter(m=>m.k==='in').reduce((a,m)=>a+m.a,0),pout=pm.filter(m=>m.k==='out').reduce((a,m)=>a+m.a,0);
  const gd=new Set(S.gym.log.filter(x=>days.includes(x.d)).map(x=>x.d)).size;
  const rate=[...RULES.map(r=>({t:r.t,n:past.filter(k=>(S.rules[k]||{})[r.id]).length})),...S.hab.map(h=>({t:h.t,n:past.filter(k=>(S.hb[k]||{})[h.id]).length}))].sort((a,c)=>c.n-a.n);
  const d0=new Date(days[0]+'T12:00'),d6=new Date(days[6]+'T12:00'),N=past.length||1;
  const bars=days.map((k,i)=>{const p=sc[i];return `<div style="flex:1;text-align:center"><div style="height:90px;display:flex;align-items:flex-end"><div style="width:100%;height:${p===null?2:Math.max(4,p*.9)}px;background:${k===T0?'var(--go)':'var(--ac)'};opacity:${p===null?.2:.85};border-radius:4px"></div></div><span class="mu" style="font-size:11px">${DAYS[new Date(k+'T12:00').getDay()].slice(0,2)}</span><br><span style="font-size:11px">${p===null?'':p+'%'}</span></div>`}).join('');
  const R=(l,v)=>`<div class="row"><span class="t">${l}</span><b>${v}</b></div>`;
  const rr=rate.map(r=>`<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between"><span>${esc(r.t)}</span><span class="mu">${r.n}/${N} kun</span></div><div class="bar"><i style="width:${r.n/N*100}%"></i></div></div>`).join('');
  const strong=rate[0],weak=rate[rate.length-1];
  return `<div class="in"><button class="btn s" onclick="WK--;render()">‹</button><button class="btn s" onclick="WK=0;render()">Shu hafta</button><button class="btn s" onclick="WK++;render()">›</button></div>
  <section class="hero"><p class="lab">${d0.getDate()} ${MON[d0.getMonth()]} dan ${d6.getDate()} ${MON[d6.getMonth()]} gacha</p><h1 style="font-size:44px">${avg}%</h1><p class="mu">Haftalik o‘rtacha ball. ${vs.length?'Eng yaxshi kun: '+DAYS[new Date(days[sc.indexOf(Math.max(...vs))]+'T12:00').getDay()]+' ('+Math.max(...vs)+'%).':'Bu hafta hali boshlanmagan.'}</p></section>
  <h2>Kunlar bo‘yicha</h2><div style="display:flex;gap:4px">${bars}</div>
  <h2>Hafta raqamlarda</h2>${R('Uyg‘onish',wl.length?`${wl.length} kun, o‘rtacha ${hm(wavg)}${S.wk.start?`, maqsadga ${hit} marta`:''}`:'yozilmagan')}${R('Instagramsiz kunlar',ig+' kun')}${R('Qur‘on',`hatm ${hp} bet, takror ${rv} bet, ${ay} oyat yodlandi`)}${R('Zikr',zk+' marta')}${R('Fokus',fc+' daqiqa')}${R('Zal',gd+' / 4 kun')}${R('Shaxsiy pul',`+${num(pin)} / −${num(pout)}`)}
  ${rate.length?`<h2>Odat va qoidalar</h2>${rr}<h2>Xulosa</h2><p>Kuchli tomon: <b>${esc(strong.t)}</b> (${strong.n}/${N} kun).</p><p>Keyingi hafta e‘tibor: <b>${esc(weak.t)}</b> (${weak.n}/${N} kun). Shuni birinchi o‘ringa qo‘y.</p>`:'<p class="mu">Odat qo‘shsang, xulosa shu yerda chiqadi.</p>'}`;
}
function addGl(){const n=GN.trim(),s=+GS,r=+GR,w=+GK;if(!n||!s||!r)return;S.gym.log.push({id:Date.now(),d:dk(),n,s,r,w:w||0});GS=GR=GK='';save()}
function delGl(id){S.gym.log=S.gym.log.filter(x=>x.id!==id);save()}
function addBd(){const w=+BW;if(!w)return;S.gym.body.push({id:Date.now(),d:dk(),w,c:+BC||0,b:+BB||0,a:+BA||0});BW=BC=BB=BA='';save()}
function delBd(id){S.gym.body=S.gym.body.filter(x=>x.id!==id);save()}
function zalOld(){
  const g=S.gym,T0=dk(),b=new Date(),w0=(b.getDay()+6)%7,wk=[...Array(7)].map((_,i)=>new Date(b.getFullYear(),b.getMonth(),b.getDate()-w0+i).toLocaleDateString('sv'));
  const wd=new Set(g.log.filter(x=>wk.includes(x.d)).map(x=>x.d)).size,pr={};g.log.forEach(x=>{const n=x.n.toLowerCase();pr[n]=Math.max(pr[n]||0,x.w)});
  const names=[...new Set(g.log.map(x=>x.n))].slice(-12).map(n=>`<option value="${esc(n)}">`).join('');
  const lg=g.log.slice().sort((a,c)=>c.id-a.id).slice(0,12).map(x=>`<div class="row"><span class="t">${esc(x.n)}<br><span class="mu">${x.d.slice(8)}.${x.d.slice(5,7)}, ${x.s}×${x.r}${x.w?', '+x.w+' kg':''}${x.w&&x.w===pr[x.n.toLowerCase()]?' · rekord':''}</span></span><button class="x" onclick="delGl(${x.id})">×</button></div>`).join('');
  const bd=g.body,last=bd[bd.length-1],first=bd[0],ws=bd.slice(-10).map(x=>x.w),mn=Math.min(...ws),mx=Math.max(...ws);
  const spark=ws.length>1?`<svg viewBox="0 0 300 60" width="100%" height="60" style="margin:8px 0"><polyline fill="none" stroke="var(--ac)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="${ws.map((v,i)=>`${i*300/(ws.length-1)},${55-(mx===mn?25:(v-mn)/(mx-mn)*50)}`).join(' ')}"/></svg>`:'';
  const bl_=bd.slice().reverse().slice(0,6).map(x=>`<div class="row"><span class="t">${x.w} kg<br><span class="mu">${x.d.slice(8)}.${x.d.slice(5,7)}${x.c?', ko‘krak '+x.c:''}${x.b?', bel '+x.b:''}${x.a?', qo‘l '+x.a:''}</span></span><button class="x" onclick="delBd(${x.id})">×</button></div>`).join('');
  const ni=(ph,v,f)=>`<input type="number" inputmode="decimal" placeholder="${ph}" value="${v}" oninput="${f}=this.value">`;
  return `<section class="hero"><p class="lab">Zal jurnali</p><h1 style="font-size:34px">${wd} / 4 kun</h1><div class="bar" style="margin:8px 0"><i style="width:${Math.min(100,wd/4*100)}%"></i></div><p class="mu">Bu haftada mashq qilingan kunlar. Mashqlarni quyida yoz, rekordlar o‘zi belgilanadi.</p></section>
  <h2>Mashq yozish</h2><datalist id="gnl">${names}</datalist><div class="in"><input list="gnl" placeholder="Mashq nomi, masalan: Bench press" value="${esc(GN)}" oninput="GN=this.value"></div><div class="in">${ni('Set',GS,'GS')}${ni('Takror',GR,'GR')}${ni('Kg',GK,'GK')}<button class="btn" onclick="addGl()">Yoz</button></div>${lg||'<p class="mu">Hali mashq yozilmagan.</p>'}
  <h2>Vazn va o‘lchamlar</h2>${last?`<p class="mu" style="margin:0">Hozirgi vazn: <b style="color:var(--tx)">${last.w} kg</b>${bd.length>1?`, boshlanishdan ${r1(last.w-first.w)>0?'+':''}${r1(last.w-first.w)} kg`:''}</p>${spark}`:''}
  <div class="in">${ni('Vazn, kg',BW,'BW')}${ni('Ko‘krak',BC,'BC')}</div><div class="in">${ni('Bel',BB,'BB')}${ni('Qo‘l',BA,'BA')}<button class="btn" onclick="addBd()">Yoz</button></div>${bl_||'<p class="mu">Hali o‘lcham yozilmagan.</p>'}`;
}

function odatlar(){
  const now=new Date(),d0=new Date(now.getFullYear(),now.getMonth()+HMo,1),y=d0.getFullYear(),m=d0.getMonth(),n=new Date(y,m+1,0).getDate(),today=dk(),key=x=>`${y}-${pad(m+1)}-${pad(x)}`;
  let tot=0,got=0,best=0,bn='',perfect=0;
  const w0=new Date();w0.setDate(w0.getDate()-((w0.getDay()+6)%7));const wkKeys=[...Array(7)].map((_,i)=>new Date(w0.getFullYear(),w0.getMonth(),w0.getDate()+i).toLocaleDateString('sv'));
  for(let d=1;d<=n;d++){const k=key(d);if(k<=today&&S.hab.length&&S.hab.every(x=>(S.hb[k]||{})[x.id]||hkOn(k,x.id)))perfect++}
  const NL=[];
  const body=S.hab.map((x,hi)=>{const st=hst(x.id);if(st>best){best=st;bn=x.t}const wn=wkKeys.filter(k=>(S.hb[k]||{})[x.id]).length,col=HC[hi%HC.length];
    const cs=[...Array(n)].map((_,q)=>{const k=key(q+1),on=(S.hb[k]||{})[x.id],fu=k>today;if(!fu&&!(!on&&hkOn(k,x.id))){tot++;if(on)got++}return `<td class="${gCls(y,m,q+1,today)}"><button class="cell ${on?'on':hkOn(k,x.id)?'hsk':''}" style="--hc:${col}" ${fu?'disabled':''} onclick="hbC('${x.id}','${k}')"></button></td>`}).join('');
    NL.push(`<div class="mr">${x.e?`<span style="margin-right:6px">${x.e}</span>`:`<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${col};margin-right:6px"></span>`}<span onclick="hbE(${hi})" style="cursor:pointer;border-bottom:1px dotted var(--mu)">${esc(x.t)}</span><br><span class="mu" style="font-size:12px">🔥 ${st}&nbsp; ${hbMeta(x,wn)} <button class="x" style="font-size:15px" onclick="delH(${hi})">×</button></span></div>`);return `<tr style="height:64px">${cs}</tr>`}).join('');
  return `<p class="mu" style="margin:0">Odatlar jadvali</p><h1 class="gr">${MON[m][0].toUpperCase()+MON[m].slice(1)} ${y}</h1><p class="mu" style="margin:0 0 4px">Bugun: ${now.getDate()}-${MON[now.getMonth()]}, ${DAYS[now.getDay()]}</p>
  ${habNav()}${hbCtl()}
  <div class="sum"><div><span class="mu">Oylik bajarilish</span><b>${tot?Math.round(got/tot*100):0}%</b></div><div><span class="mu">Mukammal kunlar</span><b>${perfect}</b><span class="mu" style="font-size:12px">barcha odatlar belgilangan</span></div><div><span class="mu">Eng uzun seriya</span><b>${best} kun</b><span class="mu" style="font-size:12px">${esc(bn)}</span></div><div><span class="mu">Faol odatlar</span><b>${S.hab.length}</b></div></div>
  ${!S.hab.length?'<p class="mu">Hali odat yo‘q. Pastdan birinchi odatingni yoz.</p>':HV==='w'?habWeek(today):`${mgrid(NL,gHead(y,m,n,today,1),body,'j',64)}`}
  <div class="in" style="margin-top:14px"><input id="ne" placeholder="🙂" style="flex:0 0 58px;text-align:center"><input id="nh" placeholder="Yangi odat, masalan: 20 bet kitob" onkeydown="if(event.key==='Enter')addH()"><button class="btn" onclick="addH()">Qo‘sh</button></div>${habInsUi()}${habArcUi()}${suggCard()}`;
}

