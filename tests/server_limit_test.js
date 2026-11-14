const fs=require('fs'),esbuild=require('esbuild');
let src=fs.readFileSync('/mnt/user-data/outputs/server-setup/ai-assistant.ts','utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n');
const out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code;
let handler=null;const env={GEMINI_API_KEY:'k',SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s'};
globalThis.Deno={env:{get:k=>env[k]},serve:h=>{handler=h}};
let usage={n:0},ups=[];
globalThis.__cc=()=>({auth:{getUser:async t=>t==='good'?{data:{user:{id:'u1',email:'a@x.com'}}}:{data:{user:null}}},from:tb=>({select:()=>({eq:()=>({eq:()=>({maybeSingle:async()=>({data:tb==='ai_usage'?usage:null})}),maybeSingle:async()=>({data:null})})}),upsert:async r=>{ups.push(r);return{}}})});
new Function(out)();
const rq=b=>new Request('http://x',{method:'POST',headers:{Authorization:'Bearer good'},body:JSON.stringify(b)});
const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);

const MODELS=['gemini-3.8-flash','gemini-2.5-flash-lite','gemini-2.5-flash','gemini-2.0-flash','gemini-1.9-flash','gemini-1.8-flash','gemini-1.7-flash','gemini-1.6-flash'].map(n=>({name:'models/'+n,supportedGenerationMethods:['generateContent']}));
let calls=[],script={};
const okBody=t=>({candidates:[{content:{parts:[{text:t}]}}]});
globalThis.fetch=async(u,o)=>{u=String(u);
 if(/\/models\?pageSize/.test(u))return new Response(JSON.stringify({models:MODELS}),{status:200});
 const m=/models\/([^:/?]+):/.exec(u);if(!m)return new Response('{}',{status:200});const name=m[1];calls.push(name);
 const q=script[name];const s=q&&q.length?q.shift():{status:200,body:okBody('{"ok":1}')};
 return new Response(JSON.stringify(s.body),{status:s.status});};
const perDay={error:{code:429,message:'Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: x',details:[{violations:[{quotaId:'GenerateRequestsPerDayPerProjectPerModel-FreeTier'}]}]}};
const reset=()=>{calls=[];script={}};
(async()=>{
 reset();let r=await handler(rq({action:'iex',kind:'model',question:'Describe a place you like to visit in your city.',part:2,band:7}));
 ok('heavy task (speaking model answer): the NEWEST model is tried first (the usual order)',r.status===200&&calls[0]==='gemini-3.8-flash',calls);
 reset();r=await handler(rq({action:'iex',kind:'daystory',stats:{sana:'2026-11-05',xp:50}}));
 ok('light task (day story): the lite model is tried FIRST, so the main models keep their quota for heavy work',r.status===200&&calls[0]==='gemini-2.5-flash-lite'&&JSON.parse(r.body?await r.clone().text():'{}').model==='gemini-2.5-flash-lite',calls);
 reset();r=await handler(rq({action:'iex',kind:'coach',mode:'q',stats:{sana:'2026-11-05',xp:50}}));ok('light task (coach questions) also goes to the lite model first',calls[0]==='gemini-2.5-flash-lite');
 reset();r=await handler(rq({action:'iex',kind:'dict',word:'support'}));ok('light task (dictionary AI entry) goes to the lite model first',calls[0]==='gemini-2.5-flash-lite');
 reset();r=await handler(rq({action:'plan',ctx:'{"kun":"2026-11-05","bloklar":["a","b","c"]}'}));ok('the short day-plan helper is light too',calls[0]==='gemini-2.5-flash-lite',calls);
 reset();r=await handler(rq({action:'iex',kind:'material',text:'x'.repeat(400)}));ok('article analysis (material) is heavy: newest model first',calls[0]==='gemini-3.8-flash',calls);
 // JSON tekshiruvi (faqat yengil vazifa)
 reset();script['gemini-2.5-flash-lite']=[{status:200,body:okBody('bu JSON emas {')}];r=await handler(rq({action:'iex',kind:'daystory',stats:{sana:'2026-11-05',xp:50}}));let j=await r.json();
 ok('a light task whose lite model returns broken JSON is retried on the NEXT model and the valid answer is returned',r.status===200&&calls.length>=2&&calls[0]==='gemini-2.5-flash-lite'&&j.text==='{"ok":1}'&&j.model!=='gemini-2.5-flash-lite',[calls,j]);
 reset();const bad=()=>({status:200,body:okBody('hali ham JSON emas')});for(const mm of MODELS.map(x=>x.name.slice(7)))script[mm]=[bad(),bad(),bad()];r=await handler(rq({action:'iex',kind:'daystory',stats:{sana:'2026-11-05',xp:50}}));j=await r.json();
 ok('if EVERY model returns broken JSON the first answer is still returned (the app shows its own message as before), not a server error',r.status===200&&j.text==='hali ham JSON emas',[r.status,j]);
 reset();script['gemini-3.8-flash']=[{status:200,body:okBody('uzilgan {"a":')}];r=await handler(rq({action:'iex',kind:'material',text:'x'.repeat(400)}));j=await r.json();
 ok('a HEAVY task is never retried for JSON shape (a long answer may be legitimately cut): exactly one call, text returned as is',calls.length===1&&j.text==='uzilgan {"a":',calls);
 // PerDay
 reset();script['gemini-3.8-flash']=[{status:429,body:perDay}];r=await handler(rq({action:'iex',kind:'material',text:'x'.repeat(400)}));j=await r.json();
 ok('a model whose DAILY free limit is used up is skipped within the same request: the next model answers',r.status===200&&calls[0]==='gemini-3.8-flash'&&calls[1]!=='gemini-3.8-flash'&&!!j.text,calls);
 reset();r=await handler(rq({action:'iex',kind:'material',text:'x'.repeat(400)}));
 ok('...and the next requests do not waste time on it (it is moved to the end until the limit resets)',calls[0]!=='gemini-3.8-flash'&&r.status===200,calls);
 reset();for(const mm of MODELS.map(x=>x.name.slice(7)))script[mm]=[{status:429,body:perDay},{status:429,body:perDay}];r=await handler(rq({action:'iex',kind:'material',text:'x'.repeat(400)}));j=await r.json();
 ok('when EVERY model is out of daily quota the user gets the clear message with the reset time (429), after trying at most 6 models once each',r.status===429&&/Bugungi bepul AI limiti tugadi/.test(j.error)&&/12:00-13:00/.test(j.error)&&calls.length<=6,[r.status,calls.length,j.error]);
 reset();r=await handler(rq({action:'iex',kind:'daystory',stats:{sana:'2026-11-05',xp:50}}));ok('after that the dead models are still retried (at the end of the list) in case the limit has reset: a call is made, not an instant refusal',calls.length>=1,calls);
 reset();script={};usage={n:40};r=await handler(rq({action:'limit'}));j=await r.json();ok('the limit endpoint still reports the app-level counter (used 40 of 40)',j.used===40&&j.limit===40&&j.owner===false,j);
})();
