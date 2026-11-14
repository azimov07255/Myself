const fs=require('fs');
const old={ob:1,ts:5,name:'Aziz',goals:[],ie:{words:[],mock:[],wr:[],tests:[],target:7,dr:''},pr:{st:[],tests:[],exam:''},q:{ppd:3,cur:0,m:{},ord:[],rv:0,rg:5,rd:{},hp:0,hg:20,hc:0,hd:{}},fin:{budget:0,goal:{t:'',a:0,s:0}},money:[],hab:[],iso:{lim:60,m:{},log:[]},gym:{log:[],body:[]}};
const store={trk_local:JSON.stringify(old)};global.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=v},removeItem:k=>{delete store[k]}};
let al=[],reqs=[];
const fakeSb={createClient:()=>({from:()=>({select:()=>({eq:()=>({maybeSingle:async()=>({data:null})})}),upsert:async()=>({}),delete:()=>({eq:async()=>({})}),insert:async()=>({})}),auth:{getSession:async()=>({data:{session:{access_token:'tok'}}}),signOut:async()=>{}},storage:{from:()=>({})},functions:{invoke:async()=>({error:{message:'should not be used'}})}})};
global.supabase=fakeSb;global.window={addEventListener(){},supabase:fakeSb,scrollY:0,innerWidth:390,innerHeight:800,devicePixelRatio:1,scrollTo(){},AudioContext:class{decodeAudioData(b,res){res({duration:2})}close(){}},OfflineAudioContext:class{constructor(c,l,sr){this.l=l;this.sr=sr}createBufferSource(){return{connect(){},start(){}}}get destination(){return{}}async startRendering(){return{getChannelData:()=>new Float32Array(this.l)}}}};
global.scrollTo=()=>{};global.confirm=()=>true;global.alert=m=>al.push(m);
const app={_h:'',classList:{add(){},remove(){}},offsetWidth:0,set innerHTML(v){this._h=v},get innerHTML(){return this._h}};global.matchMedia=()=>({matches:false,addEventListener(){}});
const nodes={};const mk=()=>({id:'',style:{},dataset:{},classList:{add(){},remove(){}},scrollTop:0,scrollHeight:9,value:'',textContent:'',_h:'',set innerHTML(v){this._h=v;['aic','aiq','aii','aimic','sprb'].forEach(i=>{if(v.includes('id="'+i+'"'))nodes[i]=mk()})},get innerHTML(){return this._h},remove(){},addEventListener(){},querySelector:()=>null});
global.document={addEventListener(){},documentElement:{setAttribute(){},removeAttribute(){},classList:{add(){},remove(){}}},body:{appendChild:e=>{if(e.id)nodes[e.id]=e},style:{}},querySelector:s=>s==='#app'?app:({value:'',content:'',innerHTML:''}),querySelectorAll:()=>[],activeElement:null,getElementById:id=>nodes[id]||null,createElement:()=>mk(),head:{appendChild(){}}};
global.navigator={onLine:true,vibrate(){}};global.requestAnimationFrame=()=>0;global.setInterval=()=>1;global.clearInterval=()=>{};const realST=global.setTimeout;global.setTimeout=()=>0;
const FB={band:6.5,transcript:'I like reading books because...',criteria:[{k:'Task Response',b:6.5,n:'Yaxshi'},{k:'Lexical Resource',b:6,n:'Oddiy'}],errors:[{o:'people is',c:'people are',w:'Kelishuv xatosi'}],strengths:['Aniq tuzilma'],improve:['Kollokatsiyalar'],better:'Better text.',vocab:[{w:'mitigate',m:'yumshatmoq'},{w:'abundant',m:'mo‘l'}]};
let mode={};
global.fetch=async(u,o)=>{const b=JSON.parse(o.body||'{}');reqs.push(b);
 const R=(st,obj)=>({ok:st<400,status:st,text:async()=>JSON.stringify(obj),json:async()=>obj,headers:{get:()=>'application/json'}});
 if(mode.net)throw new TypeError('Failed to fetch');
 if(mode.st)return R(mode.st,mode.body||{});
 if(b.action==='ielts')return R(200,{text:JSON.stringify(FB)});
 if(b.action==='videos')return R(200,mode.key?{videos:[{id:'abc',t:'IELTS Writing Task 2 full lesson',ch:'IELTS Liz',th:'http://t.jpg'}]}:{videos:[],nokey:true});
 if(b.action==='chat'&&b.web)return R(200,{text:'Mana tavsiya.',sources:[{t:'British Council',u:'https://britishcouncil.org/x'},{t:'',u:'https://ielts.org/page'}]});
 if(b.action==='chat'){const enc=new TextEncoder();return{ok:true,status:200,headers:{get:n=>n==='content-type'?'text/plain':null},body:new ReadableStream({start(c){c.enqueue(enc.encode('Salom!'));c.close()}})}}
 return R(200,{text:'x'})};
eval(fs.readFileSync('/tmp/t.js','utf8')+`;S=load();S.ob=1;S.ts=1;UID='u1';
globalThis.T={get S(){return S},go,get app(){return app},fnPost,fnAI,wAI,wSave,spRec,spSaveAI,ieFb,fbWord,aiOpen,aiGo,aiS,aiSend,aiExtra,get WFB(){return WFB},get SFB(){return SFB},set SPQ(v){SPQ=v},set WE_k(v){WE.k=v},set tab_(v){tab=v},ieWrite,ieSpeak,fdAI,get FDR(){return FDR},toWav}`);
const T=globalThis.T,S=T.S,w=ms=>new Promise(r=>realST(r,ms));const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
(async()=>{
 // --- error messages (the food bug) ---
 mode={st:400,body:{error:'Savol topilmadi.'}};let e1=await T.fnAI({action:'food',text:'osh'}).catch(e=>e.message);ok('old server (no food action) -> clear "redeploy" hint: '+e1,/qayta Deploy/.test(e1));
 mode={st:404,body:{code:'NOT_FOUND'}};e1=await T.fnAI({action:'food',text:'osh'}).catch(e=>e.message);ok('404 -> function not found message',/topilmadi/.test(e1));
 mode={st:429,body:{error:'AI hozir band (bepul daqiqalik limit). 23 soniyadan keyin qayta urinib ko‘ring.'}};e1=await T.fnAI({action:'food',text:'osh'}).catch(e=>e.message);ok('429 -> server message shown as is',/23 soniyadan/.test(e1));
 mode={net:1};e1=await T.fnAI({action:'food',text:'osh'}).catch(e=>e.message);ok('network failure -> clear message',/ulanib bo‘lmadi/.test(e1));
 mode={st:500,body:{}};e1=await T.fnAI({action:'food'}).catch(e=>e.message);ok('unknown 500 -> shows status instead of blank "AI javob bermadi": '+e1,/500/.test(e1));
 mode={};
 // --- writing ---
 S.ie.dr='In recent years, many people argue that technology has changed education. '.repeat(8);T.WE_k=2;
 await T.wAI();ok('writing: AI feedback received and stored (band '+T.WFB.band+')',T.WFB&&T.WFB.band===6.5&&reqs.slice(-1)[0].action==='ielts'&&reqs.slice(-1)[0].kind==='writing'&&reqs.slice(-1)[0].task===2);
 let h=T.ieWrite();ok('writing screen shows AI result: band, criteria, errors, vocab buttons',h.includes('6.5')&&h.includes('Task Response')&&h.includes('people is')&&h.includes('people are')&&h.includes('fbWord(\'w\',0)'));
 T.fbWord('w',0);T.fbWord('w',0);ok('vocab button adds the word once to the dictionary',S.ie.words.filter(x=>x.w==='mitigate').length===1&&S.ie.words[0].m==='yumshatmoq');
 T.wSave();const es=S.ie.wr.slice(-1)[0];ok('saved essay keeps AI feedback; AI band used as score and logged as a test',es.fb&&es.fb.band===6.5&&es.sc===6.5&&S.ie.tests.some(t=>t.k==='W'&&t.b.W===6.5&&/AI/.test(t.src)));
 ok('saved essay shows feedback when opened',(()=>{const hh=T.ieFb(es.fb,String(es.id));return hh.includes('Aniq tuzilma')&&hh.includes('Better text.')})());
 S.ie.dr='short';al=[];await T.wAI();ok('too-short essay refused before calling the server',al.some(m=>/kamida 40/.test(m)));
 // --- speaking ---
 T.SPQ={part:2,q:'Describe a book you enjoyed.',ph:0};
 class MR{constructor(){this.mimeType='audio/mp4'}start(){}stop(){this.ondataavailable({data:{size:9000}});realST(()=>this.onstop(),0)}}
 window.MediaRecorder=MR;global.MediaRecorder=MR;global.navigator.mediaDevices={getUserMedia:async()=>({getTracks:()=>[{stop(){}}]})};const BM=global.Blob;global.Blob=class extends BM{get size(){return 9000}};
 await T.spRec();await T.spRec();await w(60);global.Blob=BM;const sq=reqs.filter(r=>r.kind==='speaking').slice(-1)[0];
 ok('speaking: recording sent with part, question and 12 kHz WAV audio',sq&&sq.part===2&&/book/.test(sq.question)&&sq.mime==='audio/wav'&&sq.audio.length>100);
 ok('speaking feedback + transcript shown',T.SFB&&T.SFB.band===6.5&&T.ieFb(T.SFB,'s').includes('Sen aytganing')&&T.ieFb(T.SFB,'s').includes('I like reading'));
 T.SPQ={part:2,q:'x',ph:0};T.spSaveAI();ok('speaking result saved with AI note',S.ie.tests.some(t=>t.k==='S'&&t.fb&&t.b.S===6.5&&/AI/.test(t.src)));
 // --- chat: web search + videos ---
 reqs.length=0;mode={};T.aiOpen&&0;
 T.aiGo&&0;await T.aiSend('IELTS Writing Task 2 haqida video topib ber');await w(80);
 const m=T.aiS().chat.filter(x=>x.r==='model').slice(-1)[0];
 ok('web-intent question -> chat sent with web:true and a videos request in parallel',reqs.some(r=>r.action==='chat'&&r.web===true)&&reqs.some(r=>r.action==='videos'&&/IELTS Writing Task 2/.test(r.q)&&!/video|topib/i.test(r.q)));
 ok('answer carries source links',m&&m.src&&m.src.length===2);
 const ex=T.aiExtra(m);ok('no YouTube key -> YouTube search link instead of cards; sources shown as chips',ex.includes('youtube.com/results?search_query=IELTS')&&ex.includes('British Council')&&ex.includes('ielts.org'));
 mode={key:1};reqs.length=0;await T.aiSend('Qur‘on tajvid video youtube');await w(80);const m2=T.aiS().chat.filter(x=>x.r==='model').slice(-1)[0];
 const ex2=T.aiExtra(m2);ok('with YouTube key -> real video cards with thumbnail and watch link',ex2.includes('watch?v=abc')&&ex2.includes('IELTS Liz')&&ex2.includes('http://t.jpg'));
 reqs.length=0;await T.aiSend('Salom');await w(60);ok('plain question: normal streaming chat, no search, no videos request',reqs.length===1&&reqs[0].web===false&&reqs[0].stream===true);
 console.log('done');process.exit(0)})();
