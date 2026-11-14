const fs=require('fs');
const old={ob:1,ts:5,name:'Aziz',goals:[],ie:{words:[],mock:[],wr:[],target:7},pr:{st:[],tests:[],exam:''},q:{ppd:3,cur:0,m:{},ord:[],rv:0,rg:5,rd:{},hp:0,hg:20,hc:0,hd:{}},fin:{budget:0,goal:{t:'',a:0,s:0}},money:[],hab:[{id:'h1',t:'Kitob',e:'📚'}],iso:{lim:60,m:{},log:[]},gym:{log:[],body:[]}};
const store={trk_local:JSON.stringify(old)};global.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=v},removeItem:k=>{delete store[k]}};
const FORM={},FILES={};let invokes=[],uploads=[],removed=[],al=[],toasts=[];
const fakeSb={createClient:()=>({from:()=>({select:()=>({eq:()=>({maybeSingle:async()=>({data:null})})}),upsert:async()=>({}),delete:()=>({eq:async()=>({})}),insert:async()=>({})}),auth:{getSession:async()=>({data:{session:{access_token:'tok'}}}),signOut:async()=>{}},
 storage:{from:()=>({upload:async(p,f)=>{uploads.push(p);return{}},remove:async p=>{removed.push(p);return{}},download:async()=>({error:true})})},
 functions:{invoke:async(n,o)=>{invokes.push(o.body);if(o.body.action==='food')return{data:{text:'```json\n{\"items\":[{\"name\":\"Osh\",\"grams\":300,\"kcal\":620,\"p\":22,\"f\":28,\"c\":70},{\"name\":\"Non\",\"grams\":60,\"kcal\":160,\"p\":5,\"f\":1,\"c\":32}],\"note\":\"Taxminiy hisob\"}\n```'}};if(o.body.action==='transcribe')return{data:{text:'Bugun zalga boraman'}};return{data:{text:'x'}}}}})};
global.supabase=fakeSb;global.window={addEventListener(){},supabase:fakeSb,scrollY:0,innerWidth:390,innerHeight:800,devicePixelRatio:1,scrollTo(){},AudioContext:class{decodeAudioData(b,res){res({duration:0.5})}close(){}},OfflineAudioContext:class{constructor(c,l,sr){this.l=l}createBufferSource(){return{connect(){},start(){}}}get destination(){return{}}async startRendering(){return{getChannelData:()=>new Float32Array(this.l).map((_,i)=>Math.sin(i/10))}}},MediaRecorder:undefined};
global.scrollTo=()=>{};global.confirm=()=>true;global.alert=m=>al.push(m);
const app={_h:'',classList:{add(){},remove(){}},offsetWidth:0,set innerHTML(v){this._h=v},get innerHTML(){return this._h}};global.matchMedia=()=>({matches:false,addEventListener(){}});
const nodes={};const mk=()=>({id:'',style:{},dataset:{},classList:{add(){},remove(){}},scrollTop:0,scrollHeight:9,value:'',textContent:'',_h:'',set innerHTML(v){this._h=v;['aic','aiq','aii','aimic'].forEach(i=>{if(v.includes('id="'+i+'"'))nodes[i]=mk()})},get innerHTML(){return this._h},remove(){},addEventListener(){}});
const ctx2=new Proxy({},{get:(t,k)=>k==='createLinearGradient'?()=>({addColorStop(){}}):()=>{}});
global.document={addEventListener(){},documentElement:{setAttribute(){},removeAttribute(){}},querySelector:s=>s==='#app'?app:({value:FORM[s.slice(1)]??'',files:FILES[s.slice(1)]||null,content:'',innerHTML:''}),querySelectorAll:()=>[],activeElement:null,getElementById:id=>nodes[id]||null,
 createElement:t=>{const e=mk();if(t==='canvas'){e.getContext=()=>ctx2;e.toBlob=cb=>cb(new Blob(['x']));e.remove=()=>{}}if(t==='a')e.click=()=>{};return e},body:{appendChild:e=>{if(e.id)nodes[e.id]=e}},head:{appendChild(){}}};
global.navigator={onLine:true,vibrate(){}};global.requestAnimationFrame=()=>0;global.setInterval=()=>1;global.clearInterval=()=>{};const realST=global.setTimeout;global.setTimeout=()=>0;
global.fetch=async(u,o)=>{const b=JSON.parse((o&&o.body)||'{}');
 const R=obj=>({ok:true,status:200,text:async()=>JSON.stringify(obj),json:async()=>obj,headers:{get:()=>'application/json'}});
 if(b.action==='food'){invokes.push(b);return R({text:'```json\n{\"items\":[{\"name\":\"Osh\",\"grams\":300,\"kcal\":620,\"p\":22,\"f\":28,\"c\":70},{\"name\":\"Non\",\"grams\":60,\"kcal\":160,\"p\":5,\"f\":1,\"c\":32}],\"note\":\"Taxminiy hisob\"}\n```'})}
 if(b.action==='transcribe'){invokes.push(b);return R({text:'Bugun zalga boraman'})}
 const enc=new TextEncoder();return{ok:true,status:200,headers:{get:()=>'text/plain'},body:new ReadableStream({start(c){c.enqueue(enc.encode('Mayli.'));c.close()}})}};
const IDB={};
eval(fs.readFileSync('/tmp/t.js','utf8')+`;S=load();S.ob=1;S.ts=1;UID='u1';idbSet=async(k,v)=>{IDB[k]=v};idbGet=async k=>IDB[k];idbDel=async k=>{delete IDB[k]};exThumb2=async()=>'data:image/jpeg;base64,AAAA';
globalThis.T={get S(){return S},go,get app(){return app},set ZV(v){ZV=v},set PLD(v){PLD=v},exAdd,exMedia,exView,exClose,plAdd,plSet,plRm,zwStart,zwTick,zwEnd,get ZWK(){return ZWK},psNew,psAuto,psV,psStat,dueCard,fdAI,fdAdd,fdMul,get FDR(){return FDR},set FDI(v){FDI=v},parseJson,toWav,b64,aiMic,aiS,wrapped,yStats,shareYear,set RY(v){RY=v},zal,dk,nxtDay,dl,exDel,zFood,zReja,zPass,zLib}`);
const T=globalThis.T,S=T.S,w=ms=>new Promise(r=>realST(r,ms));const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
(async()=>{
 S.hab=[{id:'h1',t:'Kitob',e:'📚'}];
 // ---- library + media ----
 FORM.exn='Bench press';FORM.exs='4';FORM.exr='8';FORM.exw='60';FORM.exo='Yelka tushiq';FILES.exf=[{name:'v.mp4',type:'video/mp4',size:5e6,arrayBuffer:async()=>new ArrayBuffer(8)}];
 await T.exAdd();const e=S.gym.ex[0];
 ok('exercise saved with name, sets/reps/kg',e&&e.n==='Bench press'&&e.s===4&&e.r===8&&e.w===60);
 ok('video stored on device (IndexedDB) with thumbnail and uploaded to cloud',e.m&&e.m.k==='video'&&e.m.th&&IDB['x'+e.id]&&e.m.cloud===1&&uploads[0]==='u1/x/'+e.id);
 FILES.exf=null;FORM.exn='Squat';await T.exAdd();FORM.exn='Plank';await T.exAdd();
 await T.exMedia({name:'big.mp4',type:'video/mp4',size:80e6,arrayBuffer:async()=>new ArrayBuffer(8)},S.gym.ex[1].id);
 ok('video over 50 MB is refused with a clear message',al.some(m=>/50 MB/.test(m))&&!S.gym.ex[1].m);
 T.ZV='m';let h=T.zal();ok('library shows exercises and media status',h.includes('Bench press')&&h.includes('Bulutda saqlangan')&&h.includes('Video yoki rasm yo‘q')===false?true:h.includes('Rasm yoki video yo‘q'));
 await T.exView(e.id);const xv=nodes.xv;ok('tapping the thumbnail opens the video player',xv&&xv.innerHTML.includes('<video')&&xv.innerHTML.includes('Bench press'));
 // ---- weekly plan ----
 const day=new Date().getDay();T.PLD=day;FORM.pls=e.id;T.plAdd(day);FORM.pls=S.gym.ex[1].id;T.plAdd(day);T.plSet(day,0,'s','5');
 ok('plan: exercises added to the day with sets×reps×kg from the library',S.gym.plan[day].ex.length===2&&S.gym.plan[day].ex[0].s===5&&S.gym.plan[day].ex[0].r===8&&S.gym.plan[day].ex[0].w===60);
 T.ZV='r';h=T.zal();ok('plan view: week strip, place chips, exercises with thumbnails, start button on today',h.includes('wkp')&&h.includes('🏋️ Zal')&&h.includes('exth')&&h.includes('Bugungi mashg‘ulotni boshlash'));
 // ---- subscription ----
 const T0=T.dk(),end=T.nxtDay(T.nxtDay(T.nxtDay(T.nxtDay(T0))));FORM.pss=T0;FORM.pse=end;FORM.pst='12';FORM.psn='Fit Zone';T.psNew();
 let st=T.psStat();ok('12 visits, 5 days left -> burn warning ('+st.rem+' left, '+st.days+' days, burn '+st.burn+')',st.rem===12&&st.days===5&&st.burn===7);
 T.ZV='a';h=T.zal();ok('subscription screen warns that visits will burn',h.includes('kuyadi')&&h.includes('<small>/ 12'));
 // ---- workout flow marks attendance ----
 T.ZV='r';T.zwStart();T.zwTick(0,0);T.zwTick(0,1);T.zwTick(1,0);ok('workout: sets ticked',T.ZWK.items[0].done.length===2&&T.ZWK.items[1].done.length===1);
 h=T.zal();ok('workout screen shows progress 3 / 9',h.includes('3 / 9 set')&&h.includes('Yakunlash'));
 T.zwEnd();ok('workout saved to journal (2 exercises) and visit auto-marked ✓ in subscription',S.gym.log.length===2&&S.gym.log[0].s===2&&S.gym.pass.v[T0]==='d');
 st=T.psStat();ok('done count 1, remaining 11',st.done===1&&st.rem===11);
 // ---- auto plan ----
 S.gym.pass.t=3;T.psAuto();let pl=Object.keys(S.gym.pass.v).filter(k=>S.gym.pass.v[k]==='p');ok('auto-plan spreads the remaining visits over free days: '+pl.length+' planned',pl.length===2&&pl.every(k=>k>T0));
 T.psV(pl[0]);T.psV(pl[0]);ok('tap cycle p -> d -> m',S.gym.pass.v[pl[0]]==='m');
 S.gym.pass.v[T0]='p';let dc=T.dueCard();ok('today planned visit shows in Bugun alerts',dc.includes('Zalga borish'));S.gym.pass.v[T0]='d';
 // ---- food ----
 FORM.fdt='300 g osh va non';await T.fdAI();ok('AI food: parsed JSON even with code fences, 2 items',T.FDR&&T.FDR.items.length===2&&T.FDR.items[0].kcal===620&&invokes.slice(-1)[0].action==='food');
 T.fdMul(0.5);T.zal;T.ZV='o';h=T.zal();ok('preview shows scaled total (×0.5 = 390 kkal)',h.includes('390 kkal'));
 T.fdAdd();const L=S.gym.food.log[T0];ok('added to today log with scaled macros: '+L.map(x=>x.n+' '+x.kcal).join(', '),L.length===2&&L[0].kcal===310&&L[1].kcal===80);
 h=T.zal();ok('totals vs goal: 390 / 2500 kkal and macro bars',h.includes('2500 kkal')&&h.includes('>390<')&&h.includes('Oqsil')&&h.includes('Tushlik'));
 T.FDI='QUJD';FORM.fdt='';await T.fdAI();ok('photo-only request sends the image to the server',invokes.slice(-1)[0].image==='QUJD'&&invokes.slice(-1)[0].mime==='image/jpeg');
 ok('parseJson tolerant of extra text',T.parseJson('Mana: {"a":1} tamom').a===1&&T.parseJson('yo‘q')===null);
 // ---- voice ----
 const wav=await T.toWav({arrayBuffer:async()=>new ArrayBuffer(10)});const dv=new DataView(wav),tx=(o,n)=>String.fromCharCode(...[...Array(n)].map((_,i)=>dv.getUint8(o+i)));
 ok('voice -> valid 16 kHz mono WAV ('+wav.byteLength+' bytes)',tx(0,4)==='RIFF'&&tx(8,4)==='WAVE'&&dv.getUint32(24,true)===16000&&dv.getUint16(22,true)===1&&wav.byteLength===44+8000*2);
 class MR{constructor(){this.mimeType='audio/mp4'}start(){}stop(){this.ondataavailable({data:{size:5000}});realST(()=>this.onstop(),0)}}
 window.MediaRecorder=MR;global.MediaRecorder=MR;global.navigator.mediaDevices={getUserMedia:async()=>({getTracks:()=>[{stop(){}}]})};
 const BM=global.Blob;global.Blob=class extends BM{get size(){return 5000}};
 await T.aiMic();await w(5);const rb=nodes.aimic;await T.aiMic();await w(60);
 ok('voice flow: recorded, converted, sent as transcribe, text becomes the question',invokes.some(i=>i.action==='transcribe'&&i.mime==='audio/wav'&&i.audio.length>100)&&T.aiS().chat.some(m=>m.r==='user'&&m.t==='Bugun zalga boraman'));
 global.Blob=BM;
 // ---- Wrapped ----
 for(let i=1;i<=40;i++){const d=new Date(Date.now()-i*864e5).toLocaleDateString('sv');S.hb[d]={h1:1};S.fm[d]=25}
 T.RY='y';const oyh=eval('oy()');ok('Odat→Oy has Oylik / Yillik toggle and the yearly summary',oyh.includes('Yillik (Wrapped)')&&oyh.includes('YILIM')&&oyh.includes('Yil raqamlarda')&&oyh.includes('Eng yaxshi oy'));
 const ys=T.yStats(new Date().getFullYear());ok('year stats aggregated: '+ys.dz+' days, avg '+ys.avg+'%, top habit '+ys.hl[0].t,ys.dz>0&&ys.hl[0].n>=1);
 await T.shareYear();ok('year image generated without errors',true);
 // delete exercise cleans plan, device and cloud
 T.exDel(e.id);ok('deleting an exercise removes it from library, plan, device and cloud',!S.gym.ex.some(x=>x.id===e.id)&&S.gym.plan[day].ex.every(x=>x.id!==e.id)&&!IDB['x'+e.id]&&removed.some(p=>p[0]==='u1/x/'+e.id));
 let bad=0;for(const x of ['h','q','o','m','e','p','s'])try{T.go(x)}catch(er){bad++;console.log('FAIL',x,er.message)}
 for(const z of ['r','a','m','o','j'])try{T.ZV=z;T.zal()}catch(er){bad++;console.log('FAIL zal',z,er.message)}
 console.log(bad?bad+' FAILED':'all screens ok');process.exit(0)})();
