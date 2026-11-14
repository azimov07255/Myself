const fs=require('fs');
const old={ob:1,ts:5,name:'Aziz',goals:[],ie:{words:[],mock:[],wr:[],tests:[],target:7},pr:{st:[],tests:[],exam:''},q:{ppd:3,cur:0,m:{},ord:[],rv:0,rg:5,rd:{},hp:0,hg:20,hc:0,hd:{}},fin:{budget:0,goal:{t:'',a:0,s:0}},money:[],hab:[],iso:{lim:60,m:{},log:[]},gym:{log:[],body:[]}};
const store={trk_local:JSON.stringify(old)};global.localStorage={getItem:k=>store[k]||null,setItem:(k,v)=>{store[k]=v},removeItem:k=>{delete store[k]}};
const fakeSb={createClient:()=>({from:()=>({select:()=>({eq:()=>({maybeSingle:async()=>({data:null})})}),upsert:async()=>({}),delete:()=>({eq:async()=>({})}),insert:async()=>({})}),auth:{getSession:async()=>({data:{session:{access_token:'tok'}}}),signOut:async()=>{}},storage:{from:()=>({})}})};
global.supabase=fakeSb;global.window={addEventListener(){},supabase:fakeSb,scrollY:0,innerWidth:390,innerHeight:800,scrollTo(){}};global.scrollTo=()=>{};global.confirm=()=>true;global.alert=()=>{};
const app={_h:'',classList:{add(){},remove(){}},set innerHTML(v){this._h=v},get innerHTML(){return this._h}};global.matchMedia=()=>({matches:false,addEventListener(){}});
const nodes={};const mk=()=>({id:'',style:{},dataset:{},classList:{add(){},remove(){}},_h:'',set innerHTML(v){this._h=v},get innerHTML(){return this._h},remove(){},addEventListener(){},querySelector:()=>null});
global.document={addEventListener(){},documentElement:{setAttribute(){},removeAttribute(){},classList:{add(){},remove(){}}},body:{appendChild:e=>{if(e.id)nodes[e.id]=e},style:{}},querySelector:s=>s==='#app'?app:({value:'',content:'',innerHTML:''}),querySelectorAll:()=>[],activeElement:null,getElementById:id=>nodes[id]||null,createElement:()=>mk(),head:{appendChild(){}}};
global.navigator={onLine:true,vibrate(){}};global.requestAnimationFrame=()=>0;global.setInterval=()=>1;global.clearInterval=()=>{};const realST=global.setTimeout;global.setTimeout=()=>0;
let mode='limit';
global.fetch=async(u,o)=>{const R=(st,obj)=>({ok:st<400,status:st,text:async()=>JSON.stringify(obj),json:async()=>obj,headers:{get:()=>'application/json'}});
 if(mode==='limit')return R(429,{error:'AI hozir band (bepul daqiqalik limit). 12 soniyadan keyin qayta urinib ko‘ring.',retry:12,detail:'gemini-3.8-flash-lite · GenerateRequestsPerMinutePerProjectPerModel-FreeTier'});
 return R(200,{text:'1) Qur’on 2) IELTS 3) Zal'})};
eval(fs.readFileSync('/tmp/t.js','utf8')+`;S=load();S.ob=1;S.ts=1;UID='u1';globalThis.T={get S(){return S},aiTip,aiCard,aiS,get AITERR(){return AITERR}}`);
const T=globalThis.T,ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
(async()=>{
 await T.aiTip();let h=T.aiCard();
 ok('limit error is NOT saved as today\'s tip',!T.aiS().tip[new Date().toLocaleDateString('sv')]);
 ok('error is shown under the button with seconds and quota detail',h.includes('12 soniyadan')&&h.includes('GenerateRequestsPerMinute')&&h.includes('Bugungi maslahatni olish'));
 // old build stored errors as the tip: they must be ignored now
 T.aiS().tip[new Date().toLocaleDateString('sv')]='⚠️ AI hozir band (bepul daqiqalik limit). Biroz keyin qayta urinib ko‘ring.';
 h=T.aiCard();ok('a previously saved error text no longer blocks the card (button is back)',h.includes('Bugungi maslahatni olish')&&!h.includes('Yangilash'));
 mode='ok';await T.aiTip();h=T.aiCard();ok('after the limit passes, pressing the button saves the real tip',h.includes('Qur’on')&&h.includes('Yangilash'));
 console.log('done');process.exit(0)})();
