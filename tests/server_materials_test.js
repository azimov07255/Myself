const fs=require('fs'),esbuild=require('esbuild');
let src=fs.readFileSync(((process.env.KT_ROOT||require('path').join(__dirname,'..'))+'/server-setup/ai-assistant.ts'),'utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n');
const out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code;
let handler=null;const env={GEMINI_API_KEY:'k',SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s'};
globalThis.Deno={env:{get:k=>env[k]},serve:h=>{handler=h}};
let usage={n:0},ups=[];
globalThis.__cc=()=>({auth:{getUser:async t=>t==='good'?{data:{user:{id:'u1',email:'a@x.com'}}}:{data:{user:null}}},from:tb=>({select:()=>({eq:()=>({eq:()=>({maybeSingle:async()=>({data:tb==='ai_usage'?usage:null})}),maybeSingle:async()=>({data:null})})}),upsert:async r=>{ups.push(r);return{}}})});
new Function(out)();
const rq=b=>new Request('http://x',{method:'POST',headers:{Authorization:'Bearer good'},body:JSON.stringify(b)});
const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
const MODELS=['gemini-3.8-flash-lite','gemini-3.8-flash'].map(n=>({name:'models/'+n,supportedGenerationMethods:['generateContent']}));
let last=null,urls=[];
const FB={band:6.5,words:262,criteria:[{k:'Task Response',b:6.5,n:'ok'}],errors:[{o:'people is',c:'people are',w:'kelishuv'}],strengths:['a'],improve:['b'],better:'x',vocab:[{w:'mitigate',m:'yumshatmoq'}]};

const RSS='<?xml version="1.0"?><rss xmlns:itunes="x"><channel><title>6 Minute English</title><item><title><![CDATA[Why we sleep]]></title><pubDate>Thu, 30 Oct 2026 05:00:00 +0000</pubDate><description><![CDATA[<p>Learn about <b>sleep</b> &amp; dreams.</p>]]></description><link>https://www.bbc.co.uk/ep1</link><enclosure url="https://cdn.example.org/a1.mp3" length="5000000" type="audio/mpeg"/><itunes:duration>00:06:12</itunes:duration></item><item><title>Second</title><enclosure url="https://cdn.example.org/a2.mp3" type="audio/mpeg"/></item></channel></rss>';
const AUD=new Uint8Array(3000).fill(7);let seen=[];
globalThis.fetch=async(u,o)=>{u=String(u);seen.push(u);
 if(/\/models\?pageSize/.test(u))return new Response(JSON.stringify({models:MODELS}),{status:200});
 if(u==='https://feeds.example.org/rss')return new Response(RSS,{status:200,headers:{'content-type':'application/rss+xml'}});
 if(u==='https://feeds.example.org/html')return new Response('<html></html>',{status:200,headers:{'content-type':'image/png'}});
 if(u==='https://feeds.example.org/empty')return new Response('<rss><channel></channel></rss>',{status:200,headers:{'content-type':'text/xml'}});
 if(u==='https://feeds.example.org/go')return new Response(null,{status:302,headers:{location:'https://cdn.example.org/a1.mp3'}});
 if(u==='https://cdn.example.org/a1.mp3')return new Response(AUD,{status:200,headers:{'content-type':'audio/mpeg','content-length':String(AUD.length)}});
 if(u==='https://cdn.example.org/big.mp3')return new Response(AUD,{status:200,headers:{'content-type':'audio/mpeg','content-length':String(30*1048576)}});
 if(u==='https://cdn.example.org/missing.mp3')return new Response('nope',{status:404});
 if(/api\.groq\.com/.test(u)){const fd=o.body;window_last=fd;return new Response(JSON.stringify({text:'Hello world.',duration:3,segments:[{start:0,end:3,text:' Hello world.'}],words:[{word:'Hello',start:0,end:1},{word:'world',start:1.1,end:2}]}),{status:200})}
 last=JSON.parse(o.body);return new Response(JSON.stringify({candidates:[{content:{parts:[{text:'{"words":{"cities":"shaharlar"}}'}]}}]}),{status:200})};
let window_last=null;
(async()=>{
 let r=await handler(rq({action:'feed',url:'https://feeds.example.org/rss'}));let j=await r.json();
 ok('feed: the RSS is parsed into the channel title and items with title, date, a clean description (HTML and CDATA removed), page link, audio URL and duration',r.status===200&&j.title==='6 Minute English'&&j.items.length===2&&j.items[0].t==='Why we sleep'&&j.items[0].desc==='Learn about sleep & dreams.'&&j.items[0].au==='https://cdn.example.org/a1.mp3'&&j.items[0].dur==='00:06:12'&&j.items[0].link==='https://www.bbc.co.uk/ep1'&&j.items[1].au.endsWith('a2.mp3'),JSON.stringify(j).slice(0,200));
 usage={n:40};r=await handler(rq({action:'feed',url:'https://feeds.example.org/rss'}));ok('feed is not an AI request: it works even when the daily AI limit is used up',r.status===200);usage={n:0};
 r=await handler(rq({action:'feed',url:'nonsense'}));ok('feed: a malformed address -> 400',r.status===400);
 for(const bad of ['http://localhost/rss','http://127.0.0.1/rss','http://192.168.1.5/rss','http://10.0.0.1/x','http://x/rss','ftp://feeds.example.org/rss']){r=await handler(rq({action:'feed',url:bad}));if(r.status!==400){ok('feed refuses private and local addresses: '+bad,false);break}}
 ok('feed refuses private, local and non-http addresses (SSRF protection) without fetching them',!seen.some(u=>/localhost|127\.0|192\.168|10\.0\.0|ftp:/.test(u)));
 r=await handler(rq({action:'feed',url:'https://feeds.example.org/html'}));ok('feed: a non-text file (image) is refused (415)',r.status===415);
 r=await handler(rq({action:'feed',url:'https://feeds.example.org/empty'}));ok('feed: a page without items -> 422 with a clear message',r.status===422);
 // transcript by URL
 r=await handler(rq({action:'transcript',url:'https://cdn.example.org/a1.mp3'}));j=await r.json();env.GROQ_API_KEY='gk';
 ok('transcript by URL without a Groq key -> the usual "nokey" message',r.status===501&&j.code==='nokey');
 r=await handler(rq({action:'transcript',url:'https://cdn.example.org/a1.mp3'}));j=await r.json();
 ok('transcript by URL: the server downloads the audio itself and returns timed sentences and words',r.status===200&&j.cues&&j.cues[0].t==='Hello world.'&&j.cues[0].w.length===2,JSON.stringify(j).slice(0,160));
 ok('the audio was fetched from the given address and sent to Groq as a file',seen.includes('https://cdn.example.org/a1.mp3')&&window_last&&window_last.get('file')&&window_last.get('file').size===3000&&window_last.get('model')==='whisper-large-v3-turbo');
 r=await handler(rq({action:'transcript',url:'https://feeds.example.org/go'}));ok('the audio address may redirect (up to a few hops) and still works',r.status===200);
 r=await handler(rq({action:'transcript',url:'https://cdn.example.org/big.mp3'}));ok('audio larger than 24 MB is refused before downloading it all (413)',r.status===413);
 r=await handler(rq({action:'transcript',url:'https://cdn.example.org/missing.mp3'}));ok('a missing audio file gives a clear error (404 → 502)',r.status===502);
 r=await handler(rq({action:'transcript',url:'http://localhost/a.mp3'}));ok('transcript by URL refuses local addresses',r.status===400);
 r=await handler(rq({action:'transcript'}));ok('transcript without a file or a URL -> 400',r.status===400);
 // gloss
 usage={n:0};ups.length=0;r=await handler(rq({action:'iex',kind:'gloss',text:'short'}));ok('gloss: a too short text -> 400',r.status===400);
 r=await handler(rq({action:'iex',kind:'gloss',text:'Cities around the world are investing in public transport to reduce traffic congestion. Experts argue that electric buses can cut pollution.'}));j=await r.json();
 ok('gloss: JSON mode with a large token budget; the text reaches the model; the prompt lists every unique word, excludes articles, prepositions and names, and caps at 260',r.status===200&&last.generationConfig.maxOutputTokens>=4500&&/Cities around the world/.test(JSON.stringify(last.contents))&&/260/.test(last.systemInstruction.parts[0].text)&&/KIRITMA/.test(last.systemInstruction.parts[0].text)&&/"words"/.test(last.systemInstruction.parts[0].text));
})();
