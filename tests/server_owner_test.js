// Egasi emaili endi Secrets'dan o'qiladi (OWNER_EMAIL): to'g'ri ishlashi va xavfsiz bo'lishi
const fs=require('fs'),esbuild=require('/tmp/esb/node_modules/esbuild');
const ok=(l,c)=>{console.log((c?'PASS ':'FAIL ')+l);if(!c)process.exitCode=1};
function load(file,env){let src=fs.readFileSync(file,'utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n');
  const out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code;let h=null;globalThis.Deno={env:{get:k=>env[k]},serve:x=>{h=x}};new Function(out)();return h}
const MODELS=['gemini-3.8-flash-lite'].map(n=>({name:'models/'+n,supportedGenerationMethods:['generateContent']}));
globalThis.fetch=async(u)=>/\/models\?/.test(u)?new Response(JSON.stringify({models:MODELS}),{status:200}):new Response(JSON.stringify({candidates:[{content:{parts:[{text:'ok'}]}}]}),{status:200});
const users={own:{id:'o1',email:'Boss@Example.com'},usr:{id:'u2',email:'a@b.c'}};
globalThis.__cc=()=>({auth:{getUser:async t=>({data:{user:users[t]||null}}),admin:{listUsers:async()=>({data:{users:[]}})}},from:tb=>{const b={select:()=>b,eq:()=>b,maybeSingle:async()=>({data:tb==='ai_usage'?{n:40}:null}),upsert:async()=>({}),insert:async()=>({}),then:r=>r({data:[],error:null})};return b}});
(async()=>{
 const base={GEMINI_API_KEY:'k',SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s'};
 const rq=(tok,body)=>new Request('http://x',{method:'POST',headers:{Authorization:'Bearer '+tok},body:JSON.stringify(body)});
 const msg=[{r:'user',t:'Salom'}];
 let H=load('/mnt/user-data/outputs/server-setup/ai-assistant.ts',{...base,OWNER_EMAIL:' boss@example.com '});
 let r=await H(rq('own',{action:'chat',messages:msg}));ok('OWNER_EMAIL secret set (any case/spaces): the owner is not limited by the daily cap',r.status===200);
 r=await H(rq('usr',{action:'chat',messages:msg}));ok('a normal user at the cap is still limited (429)',r.status===429);
 H=load('/mnt/user-data/outputs/server-setup/ai-assistant.ts',base);
 r=await H(rq('own',{action:'chat',messages:msg}));ok('OWNER_EMAIL not set: nobody is treated as owner (fails closed, limit applies)',r.status===429);
 const C=load('/mnt/user-data/outputs/server-setup/create-user.ts',{...base,OWNER_EMAIL:'boss@example.com'});
 r=await C(rq('own',{action:'list'}));ok('create-user: owner may use the owner API',r.status!==403);
 r=await C(rq('usr',{action:'list'}));ok('create-user: a normal user gets 403',r.status===403);
 const C2=load('/mnt/user-data/outputs/server-setup/create-user.ts',base);
 r=await C2(rq('own',{action:'list'}));ok('create-user without OWNER_EMAIL: nobody is admitted (403)',r.status===403);
})();
