const fs=require('fs'),esbuild=require('esbuild');
let src=fs.readFileSync(((process.env.KT_ROOT||require('path').join(__dirname,'..'))+'/server-setup/ai-assistant.ts'),'utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n');
let out;try{out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code}catch(e){console.log('BUILD FAIL',e.message.slice(0,300));process.exit(1)}
let handler=null;const env={GEMINI_API_KEY:'k',SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s'};
globalThis.Deno={env:{get:k=>env[k]},serve:h=>{handler=h}};
// make the waits instant for the test
const realST=setTimeout;globalThis.setTimeout=(f,ms,...a)=>realST(f,ms>1000?5:ms,...a);
let usage={n:0},ups=[];
globalThis.__cc=()=>({auth:{getUser:async t=>t==='good'?{data:{user:{id:'u1',email:'a@x.com'}}}:{data:{user:null}}},from:tb=>({select:()=>({eq:()=>({eq:()=>({maybeSingle:async()=>({data:tb==='ai_usage'?usage:null})}),maybeSingle:async()=>({data:null})})}),upsert:async r=>{ups.push(r);return{}}})});
new Function(out)();
const rq=b=>new Request('http://x',{method:'POST',headers:{Authorization:'Bearer good'},body:JSON.stringify(b)});
const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
const MODELS=['gemini-3.8-flash-lite','gemini-3.8-flash'].map(n=>({name:'models/'+n,supportedGenerationMethods:['generateContent']}));
const E429=(extra)=>new Response(JSON.stringify({error:{code:429,message:extra.msg||'Quota exceeded',details:[{'@type':'type.googleapis.com/google.rpc.QuotaFailure',violations:[{quotaId:extra.id||'GenerateRequestsPerMinutePerProjectPerModel-FreeTier',quotaDimensions:{model:extra.model||'gemini-3.8-flash-lite'}}]},...(extra.retry?[{'@type':'type.googleapis.com/google.rpc.RetryInfo',retryDelay:extra.retry}]:[])]}}),{status:429});
const OK=()=>new Response(JSON.stringify({candidates:[{content:{parts:[{text:'Salom!'}]}}]}),{status:200});
let calls=0,plan=[];
globalThis.fetch=async(u,o)=>{if(/\/models\?pageSize/.test(u))return new Response(JSON.stringify({models:MODELS}),{status:200});calls++;return plan.shift()?.()||OK()};
(async()=>{
 const msg=[{r:'user',t:'Salom'}];
 // short per-minute limit on every model -> waits and retries once, then succeeds
 calls=0;plan=[()=>E429({retry:'12s'}),()=>E429({retry:'12s',model:'gemini-3.8-flash'}),()=>OK()];
 let r=await handler(rq({action:'chat',messages:msg}));let j=await r.json();
 ok('short per-minute limit: server waits and retries once, then the answer arrives ('+calls+' upstream calls)',r.status===200&&j.text==='Salom!');
 // limit persists -> clear message with seconds + technical detail
 plan=[()=>E429({retry:'12s'}),()=>E429({retry:'12s'}),()=>E429({retry:'12s'}),()=>E429({retry:'12s'})];
 r=await handler(rq({action:'chat',messages:msg}));j=await r.json();
 ok('still limited after the retry -> 429 with seconds and quota detail: '+j.error+' ['+j.detail+']',r.status===429&&/12 soniyadan/.test(j.error)&&/PerMinute/.test(j.detail)&&/gemini-3.8/.test(j.detail));
 // daily limit -> no pointless waiting, tells when it resets
 calls=0;plan=[()=>E429({id:'GenerateRequestsPerDayPerProjectPerModel-FreeTier'}),()=>E429({id:'GenerateRequestsPerDayPerProjectPerModel-FreeTier'})];
 r=await handler(rq({action:'chat',messages:msg}));j=await r.json();
 ok('daily limit: no retry (2 upstream calls only), explains the reset time',calls===2&&r.status===429&&/12:00-13:00/.test(j.error)&&/PerDay/.test(j.detail));
 // limit: 0 on first model (not in free tier) -> silently moves on to the next model
 calls=0;plan=[()=>E429({msg:'Quota exceeded for metric ... limit: 0, model: gemini-3.8-flash-lite',id:'X'}),()=>OK()];
 r=await handler(rq({action:'chat',messages:msg}));j=await r.json();ok('model with "limit: 0" is skipped, next model answers',r.status===200&&calls===2);
 // all models limit:0 -> specific message
 plan=[()=>E429({msg:'limit: 0'}),()=>E429({msg:'limit: 0'})];r=await handler(rq({action:'chat',messages:msg}));j=await r.json();ok('every model limit:0 -> says the key has no free quota: '+j.error,r.status===429&&/kvotasi yo‘q/.test(j.error));
 // one-shot actions (food, ielts) get the same retry
 calls=0;plan=[()=>E429({retry:'10s'}),()=>E429({retry:'10s'}),()=>OK()];
 r=await handler(rq({action:'food',text:'osh'}));j=await r.json();ok('food request also retries once on a short limit',r.status===200&&calls===3);
 // token-per-minute
 plan=[()=>E429({id:'GenerateContentInputTokensPerModelPerMinute-FreeTier'}),()=>E429({id:'GenerateContentInputTokensPerModelPerMinute-FreeTier'}),()=>E429({id:'GenerateContentInputTokensPerModelPerMinute-FreeTier'}),()=>E429({id:'GenerateContentInputTokensPerModelPerMinute-FreeTier'})];
 r=await handler(rq({action:'chat',messages:msg}));j=await r.json();ok('token limit named correctly',/token/.test(j.error));
})();
