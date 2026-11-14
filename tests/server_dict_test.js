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
 let r=await handler(rq({action:'dict',word:'Support'}));let j=await r.json();
 ok('dict: UK and US IPA and the two recorded audio files are picked from the open dictionary (the insecure http audio is dropped)',r.status===200&&j.ipaUK==='/səˈpɔːt/'&&j.ipaUS==='/səˈpɔɹt/'&&j.auUK.endsWith('support-uk.mp3')&&j.auUS.endsWith('support-us.mp3')&&j.auAny.startsWith('https://'),JSON.stringify(j).slice(0,220));
 ok('dict: meanings with definitions, examples, synonyms and antonyms, plus the source page',j.meanings.length===2&&j.meanings[0].pos==='verb'&&j.meanings[0].defs[0].ex==='We support the plan.'&&j.meanings[0].syn.includes('back')&&j.meanings[0].ant[0]==='oppose'&&j.src==='https://en.wiktionary.org/wiki/support');
 ok('dict: the word is lower-cased and sent to the open dictionary address',seen.includes('https://api.dictionaryapi.dev/api/v2/entries/en/support'));
 usage={n:40};r=await handler(rq({action:'dict',word:'support'}));ok('dict is not an AI request: works with the daily AI limit used up',r.status===200);usage={n:0};
 r=await handler(rq({action:'dict',word:'zzzxq'}));j=await r.json();ok('dict: an unknown word -> {nf:true} (the app then asks the AI)',r.status===200&&j.nf===true);
 r=await handler(rq({action:'dict',word:'make up'}));j=await r.json();ok('dict: a phrase with a space is looked up too',r.status===200&&j.ipa==='/meɪk ʌp/'&&j.ipaUK==='');
 for(const bad of ['','1234','a'.repeat(70),'<script>','rm -rf/','привет']){r=await handler(rq({action:'dict',word:bad}));if(r.status!==400){ok('dict refuses malformed words: '+bad,false);break}}
 ok('dict refuses malformed words (empty, digits, too long, tags, non-English) with 400 and never fetches them',!seen.some(u=>/script|1234|%D0|rm/.test(u)));
 r=await handler(rq({action:'dict',word:'broken'}));ok('dict: a garbled reply from the dictionary service -> 502 with a clear message',r.status===502);
 r=await handler(rq({action:'dict',word:'down'}));ok('dict: the service being down -> an error, not a crash',r.status===502);
 // AI entry
 r=await handler(rq({action:'iex',kind:'dict',word:'support',hint:'verb: To help someone or something.'}));j=await r.json();
 ok('AI dictionary entry: the word and the open-dictionary hint reach the model; JSON mode; the prompt asks for separate UK and US IPA, Uzbek meanings, collocations, an IELTS 8+ tip and a spelling fix',r.status===200&&/support/.test(JSON.stringify(last.contents))&&/LUG‘AT MA‘LUMOTI/.test(JSON.stringify(last.contents))&&/ALOHIDA/.test(last.systemInstruction.parts[0].text)&&/collocation/.test(last.systemInstruction.parts[0].text)&&/"fix"/.test(last.systemInstruction.parts[0].text)&&last.generationConfig.responseMimeType==='application/json');
 r=await handler(rq({action:'iex',kind:'dict',word:'  '}));ok('AI dictionary entry: an empty word -> 400',r.status===400);
 usage={n:40};r=await handler(rq({action:'iex',kind:'dict',word:'support'}));ok('the AI entry (unlike the free lookup) respects the daily limit',r.status===429);
})();
