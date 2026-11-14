const fs=require('fs'),esbuild=require('esbuild');
let src=fs.readFileSync('/mnt/user-data/outputs/server-setup/widget.ts','utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n');
const out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code;
let handler=null;const env={SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s'};
globalThis.Deno={env:{get:k=>env[k]},serve:h=>{handler=h}};
const TOK='a'.repeat(32),ROWS={[TOK]:{snap:{v:1,d:'2026-11-02',hab:[3,8]},updated_at:'2026-11-02T10:00:00Z',user_id:'SECRET-USER'}};let asked=[],fail=false;
globalThis.__cc=()=>({from:tb=>({select:cols=>({eq:(c,v)=>({maybeSingle:async()=>{asked.push([tb,cols,c,v]);if(fail)return{data:null,error:{message:'x'}};const r=ROWS[v];return{data:r?{snap:r.snap,updated_at:r.updated_at}:null,error:null}}})})})});
new Function(out)();
const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
(async()=>{
 let r=await handler(new Request('http://x/?t='+TOK));let j=await r.json();
 ok('a valid token returns the snapshot and its update time',r.status===200&&j.snap.hab[1]===8&&j.updated_at==='2026-11-02T10:00:00Z');
 ok('only snap and updated_at are selected: nothing else (user id, token) can leak',asked[0][1]==='snap,updated_at'&&asked[0][0]==='widget_snap'&&asked[0][2]==='token'&&!JSON.stringify(j).includes('SECRET'));
 ok('responses are never cached and allow any origin',r.headers.get('Cache-Control')==='no-store'&&r.headers.get('Access-Control-Allow-Origin')==='*');
 r=await handler(new Request('http://x/',{method:'POST',body:JSON.stringify({t:TOK})}));ok('the token can also come in a POST body',r.status===200);
 r=await handler(new Request('http://x/'));ok('no token -> 400',r.status===400);
 for(const bad of ['abc','Z'.repeat(32),'a'.repeat(31),'a'.repeat(65),"a'; drop table",'../etc']){r=await handler(new Request('http://x/?t='+encodeURIComponent(bad)));if(r.status!==400){ok('a malformed token is refused before touching the database: '+bad,false);break}}
 ok('malformed tokens (too short, too long, uppercase, symbols) are refused with 400 without any database query',asked.length===2);
 r=await handler(new Request('http://x/?t='+'b'.repeat(32)));ok('an unknown token -> 404 with a helpful message',r.status===404&&(await r.json()).error.includes('qayta yoqing'));
 fail=true;r=await handler(new Request('http://x/?t='+TOK));ok('a database error -> 500 without details',r.status===500&&!(await r.text()).includes('message'));fail=false;
 r=await handler(new Request('http://x/',{method:'OPTIONS'}));ok('browser preflight is answered',r.status===200&&/authorization/.test(r.headers.get('Access-Control-Allow-Headers')));
 ok('the function and SQL contain no Cyrillic characters',!/[\u0400-\u04FF]/.test(fs.readFileSync('/mnt/user-data/outputs/server-setup/widget.ts','utf8')+fs.readFileSync('/mnt/user-data/outputs/server-setup/widget.sql','utf8')));
 ok('the SQL protects the table: row level security and an own-row policy',/enable row level security/.test(fs.readFileSync('/mnt/user-data/outputs/server-setup/widget.sql','utf8'))&&/auth\.uid\(\) = user_id/.test(fs.readFileSync('/mnt/user-data/outputs/server-setup/widget.sql','utf8')));
})();
