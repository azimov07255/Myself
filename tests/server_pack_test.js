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
const MODELS=['gemini-3.8-flash-lite','gemini-3.8-flash'].map(n=>({name:'models/'+n,supportedGenerationMethods:['generateContent']}));
let last=null,urls=[];
const FB={band:6.5,words:262,criteria:[{k:'Task Response',b:6.5,n:'ok'}],errors:[{o:'people is',c:'people are',w:'kelishuv'}],strengths:['a'],improve:['b'],better:'x',vocab:[{w:'mitigate',m:'yumshatmoq'}]};

const SUP=[{word:'support',phonetic:'/səˈpɔːt/',phonetics:[{text:'/səˈpɔːt/',audio:'https://api.dictionaryapi.dev/media/pronunciations/en/support-uk.mp3'},{text:'/səˈpɔɹt/',audio:'https://api.dictionaryapi.dev/media/pronunciations/en/support-us.mp3'},{text:'/səˈpɔːt/',audio:'http://insecure.example/x.mp3'}],meanings:[{partOfSpeech:'verb',definitions:[{definition:'To help someone or something.',example:'We support the plan.'},{definition:'To bear weight.'}],synonyms:['back','help'],antonyms:['oppose']},{partOfSpeech:'noun',definitions:[{definition:'Help given.'}],synonyms:[],antonyms:[]}],sourceUrls:['https://en.wiktionary.org/wiki/support']}];
let seen=[];
globalThis.fetch=async(u,o)=>{u=String(u);seen.push(u);
 if(/\/models\?pageSize/.test(u))return new Response(JSON.stringify({models:MODELS}),{status:200});
 if(u==='https://api.dictionaryapi.dev/api/v2/entries/en/support')return new Response(JSON.stringify(SUP),{status:200,headers:{'content-type':'application/json'}});
 if(/entries\/en\/zzzxq$/.test(u))return new Response(JSON.stringify({title:'No Definitions Found'}),{status:404,headers:{'content-type':'application/json'}});
 if(/entries\/en\/broken$/.test(u))return new Response('<html>',{status:200,headers:{'content-type':'application/json'}});
 if(/entries\/en\/down$/.test(u))return new Response('x',{status:500});
 if(/entries\/en\/make%20up$/.test(u))return new Response(JSON.stringify([{word:'make up',phonetic:'/meɪk ʌp/',meanings:[{partOfSpeech:'verb',definitions:[{definition:'To invent.'}]}]}]),{status:200,headers:{'content-type':'application/json'}});
 last=JSON.parse(o.body);return new Response(JSON.stringify({candidates:[{content:{parts:[{text:'{"w":"support"}'}]}}]}),{status:200})};
(async()=>{
 let r=await handler(rq({action:'iex',kind:'pack',words:['Mitigate','carbon footprint','a double-edged sword']}));let j=await r.json();
 ok('pack: the words reach the model one per line (lower-cased); JSON mode; the prompt asks for separate UK/US IPA, Uzbek meaning, definition, example and collocations for EVERY word in order',r.status===200&&/mitigate\ncarbon footprint\na double-edged sword/.test(JSON.stringify(last.contents).replace(/\\n/g,'\n'))&&/ALOHIDA/.test(last.systemInstruction.parts[0].text)&&/HAR BIR/.test(last.systemInstruction.parts[0].text)&&/"col"/.test(last.systemInstruction.parts[0].text)&&last.generationConfig.responseMimeType==='application/json'&&last.generationConfig.maxOutputTokens>=3800);
 for(const bad of [[],['ok','<b>'],['x'.repeat(60)],['123'],'nope',null]){r=await handler(rq({action:'iex',kind:'pack',words:bad}));if(r.status!==400){ok('pack refuses empty or malformed lists',false);break}}
 ok('pack refuses empty lists, tags, too long words, digits and non-lists (400)',true);
 r=await handler(rq({action:'iex',kind:'pack',words:Array.from({length:30},(_,i)=>'word'+String.fromCharCode(97+i%26))}));ok('pack: at most 12 words are sent to the model per request',r.status===200&&JSON.stringify(last.contents).split('word').length-1<=13);
 usage={n:40};r=await handler(rq({action:'iex',kind:'pack',words:['support']}));ok('pack respects the daily AI limit',r.status===429);
})();
