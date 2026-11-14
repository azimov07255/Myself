const fs=require('fs'),esbuild=require('esbuild');
let src=fs.readFileSync('/mnt/user-data/outputs/server-setup/ai-assistant.ts','utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n');
const out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code;
let handler=null;const env={GEMINI_API_KEY:'k',SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s'};
globalThis.Deno={env:{get:k=>env[k]},serve:h=>{handler=h}};
let usage={n:0},profile=null,upserts=[];
globalThis.__cc=()=>({auth:{getUser:async t=>t==='good'?{data:{user:{id:'u1',email:'a@x.com'}}}:{data:{user:null}}},from:tb=>({select:()=>({eq:()=>({eq:()=>({maybeSingle:async()=>({data:tb==='ai_usage'?usage:null})}),maybeSingle:async()=>({data:null})})}),upsert:async r=>{upserts.push(r);return{}}})});
new Function(out)();
const mkReq=(body)=>new Request('http://x/ai',{method:'POST',headers:{Authorization:'Bearer good'},body:JSON.stringify(body)});
const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
// Fake Gemini that behaves like the user's real account: 2.5 models are CLOSED (404), 3.8 models are open but reject 'minimal' thinking
const MODELS=['gemini-2.5-flash','gemini-2.5-flash-lite','gemini-3.8-flash','gemini-3.8-flash-lite','gemini-3.7-flash','gemini-3.8-flash-image','gemini-3.8-pro','text-embedding-004'].map(n=>({name:'models/'+n,supportedGenerationMethods:['generateContent']}));
let reqs=[];
globalThis.fetch=async(u,o)=>{
  if(/\/models\?pageSize/.test(u))return new Response(JSON.stringify({models:MODELS}),{status:200});
  const m=/models\/([^:]+):/.exec(u)[1];const body=JSON.parse(o.body);const th=body.generationConfig.thinkingConfig;reqs.push({m,th});
  if(/^gemini-2\.5/.test(m))return new Response(JSON.stringify({error:{message:'This model models/'+m+' is no longer available to new users. Please update your code to use models/gemini-3.8'}}),{status:404});
  if(th&&th.thinkingLevel==='minimal'&&m==='gemini-3.8-flash-lite')return new Response(JSON.stringify({error:{message:'Thinking level minimal is not supported for this model'}}),{status:400});
  const stream=/streamGenerate/.test(u);const payload={candidates:[{content:{parts:[{text:'Salom'}]}}]};
  if(stream){const e=new TextEncoder();return new Response(new ReadableStream({start(c){c.enqueue(e.encode('data: '+JSON.stringify(payload)+'\r\n\r\n'));c.close()}}),{status:200})}
  return new Response(JSON.stringify(payload),{status:200})};
(async()=>{
 const msg=[{r:'user',t:'Salom'}];
 let r=await handler(mkReq({action:'health'}));let j=await r.json();
 console.log('picked models for this account:',JSON.stringify(j.picked));
 ok('auto-picks the newest Flash models, newest version first and lite first: '+j.picked[0],j.picked[0]==='gemini-3.8-flash-lite'&&j.picked.includes('gemini-3.8-flash'));
 ok('skips image/embedding/pro models',!j.picked.some(n=>/image|embed|pro/.test(n)));
 reqs=[];r=await handler(mkReq({action:'chat',messages:msg}));j=await r.json();
 ok('answers using the open model (not the closed 2.5): '+j.model,j.text==='Salom'&&j.model==='gemini-3.8-flash-lite');
 ok('never wastes time on the closed 2.5 models',!reqs.some(x=>/2\.5/.test(x.m)));
 ok('thinking ladder: minimal rejected -> falls to low: '+JSON.stringify(reqs.map(x=>x.th)),JSON.stringify(reqs.map(x=>x.th))==='[{\"thinkingLevel\":\"minimal\"},{\"thinkingLevel\":\"low\"}]');
 reqs=[];r=await handler(mkReq({action:'chat',messages:msg}));j=await r.json();
 ok('2nd request remembers the working setting (1 call only, no probing)',reqs.length===1&&reqs[0].th.thinkingLevel==='low');
 reqs=[];r=await handler(mkReq({action:'chat',stream:true,messages:msg}));const t=await r.text();ok('streaming works on the new model: '+t,t==='Salom'&&/gemini=\d+/.test(r.headers.get('x-timing')));
 env.GEMINI_MODEL='gemini-3.7-flash';globalThis.__x=1;r=await handler(mkReq({action:'chat',messages:msg}));j=await r.json();ok('GEMINI_MODEL secret overrides the choice: '+j.model,j.model==='gemini-3.7-flash');delete env.GEMINI_MODEL;
 r=await handler(mkReq({action:'health',test:true}));j=await r.json();ok('speed test covers picked models: '+JSON.stringify(j.speed.map(s=>s.model+' '+s.ms+'ms status '+s.status)),j.speed.length===3&&j.speed.every(s=>s.status===200));
})();
