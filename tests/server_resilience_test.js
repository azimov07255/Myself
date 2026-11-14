const fs=require('fs'),esbuild=require('esbuild');
let src=fs.readFileSync('/mnt/user-data/outputs/server-setup/ai-assistant.ts','utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n');
const out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code;
let handler=null;const env={GEMINI_API_KEY:'k',SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s',GEMINI_TIMEOUT_MS:'150'};
globalThis.Deno={env:{get:k=>env[k]},serve:h=>{handler=h}};
let usage={n:0};
globalThis.__cc=()=>({auth:{getUser:async t=>t==='good'?{data:{user:{id:'u1',email:'a@x.com'}}}:{data:{user:null}}},from:tb=>({select:()=>({eq:()=>({eq:()=>({maybeSingle:async()=>({data:tb==='ai_usage'?usage:null})}),maybeSingle:async()=>({data:null})})}),upsert:async()=>({})})});
const load=()=>{new Function(out)()};
const rq=b=>new Request('http://x',{method:'POST',headers:{Authorization:'Bearer good'},body:JSON.stringify(b)});
const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
const MODELS=['gemini-3.8-flash-lite','gemini-3.8-flash'].map(n=>({name:'models/'+n,supportedGenerationMethods:['generateContent']}));
let calls=[],beh={};
globalThis.fetch=async(u,o)=>{
  if(/\/models\?pageSize/.test(u))return new Response(JSON.stringify({models:MODELS}),{status:200});
  const m=/models\/([^:]+):/.exec(u)[1];calls.push(m);const b=beh[m]||'ok';
  if(b==='hang')return new Promise((_,rej)=>o.signal.addEventListener('abort',()=>rej(new DOMException('aborted','AbortError'))));
  if(b==='503')return new Response(JSON.stringify({error:{message:'overloaded'}}),{status:503});
  const payload={candidates:[{content:{parts:[{text:'Salom '+m}]}}]};
  if(/streamGenerate/.test(u)){const e=new TextEncoder();return new Response(new ReadableStream({start(c){c.enqueue(e.encode('data: '+JSON.stringify(payload)+'\r\n\r\n'));c.close()}}),{status:200})}
  return new Response(JSON.stringify(payload),{status:200})};
const chat=(extra={})=>handler(rq({action:'chat',stream:true,messages:[{r:'user',t:'Salom'}],...extra}));
(async()=>{
 load();
 // 1. the newest model hangs: we fall back quickly and say so in the timing header
 beh={'gemini-3.8-flash-lite':'hang'};calls=[];let t0=Date.now();let r=await chat();let txt=await r.text();let el=Date.now()-t0;
 const tm=r.headers.get('x-timing')||'';
 ok('a hanging model is abandoned after the timeout and the next model answers ('+txt.trim()+', '+el+' ms)',r.status===200&&/flash$/.test(txt.trim())&&el<1500&&calls.join()==='gemini-3.8-flash-lite,gemini-3.8-flash');
 ok('the timing header lists ALL attempts (the wasted time is visible)',/att=3\.8-flash-lite:timeout\d+\|3\.8-flash:ok\d+/.test(tm),tm);
 // 2. next request: the working model goes first, the slow one is not even tried
 calls=[];r=await chat();txt=await r.text();
 ok('next request starts with the model that worked, the slow one is skipped',calls.join()==='gemini-3.8-flash'&&/att=3\.8-flash:ok/.test(r.headers.get('x-timing')||''),calls.join());
 // 3. the good model starts failing: the slow one is still used as a fallback
 beh={'gemini-3.8-flash':'503'};calls=[];r=await chat();txt=await r.text();
 ok('if the good model fails (503) the demoted model is still used as a fallback',r.status===200&&calls.join()==='gemini-3.8-flash,gemini-3.8-flash-lite'&&/flash-lite$/.test(txt.trim()),calls.join()+' | '+txt);
 // 4. everything fails: the error explains every attempt
 beh={'gemini-3.8-flash':'503','gemini-3.8-flash-lite':'503'};calls=[];r=await chat();let j=await r.json();
 ok('all models failing -> 502 JSON with a readable message that lists the attempts',r.status===502&&/AI javob bera olmadi/.test(j.error)&&/http503/.test(j.error)&&j.error.includes(';'),JSON.stringify(j));
 // 5. streaming first-byte limit (TTFB) is shorter than the overall limit
 load();env.GEMINI_TIMEOUT_MS='20000';env.GEMINI_TTFB_MS='150';beh={'gemini-3.8-flash-lite':'hang'};calls=[];t0=Date.now();r=await chat();txt=await r.text();el=Date.now()-t0;
 ok('streaming: a model that sends nothing for 150 ms (TTFB limit) is dropped, not waited for 20 s ('+el+' ms)',r.status===200&&el<2000&&calls.length===2,calls.join());
 // 6. non-stream calls keep the longer limit
 load();env.GEMINI_TIMEOUT_MS='400';env.GEMINI_TTFB_MS='50';beh={};calls=[];r=await handler(rq({action:'chat',messages:[{r:'user',t:'Salom'}]}));j=await r.json();
 ok('non-streaming answers are not cut by the (shorter) streaming limit',r.status===200&&/Salom/.test(j.text)&&/att=/.test(j.timing||''));
 // 7. an owner-pinned GEMINI_MODEL stays first even if another model worked last time
 load();delete env.GEMINI_MODEL;env.GEMINI_TIMEOUT_MS='150';delete env.GEMINI_TTFB_MS;beh={};calls=[];await chat().then(x=>x.text());
 env.GEMINI_MODEL='gemini-3.8-flash';calls=[];r=await chat();await r.text();
 ok('the GEMINI_MODEL secret is tried first even when another model was the last that worked',calls[0]==='gemini-3.8-flash',calls.join());
 delete env.GEMINI_MODEL;
 // 8. daily limit still enforced, error stays JSON
 usage={n:40};r=await chat();ok('daily limit still applies (429 JSON)',r.status===429&&!!(await r.json()).error);
})();
