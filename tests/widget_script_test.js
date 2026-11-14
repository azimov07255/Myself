// Scriptable skriptini Node'da soxta Scriptable API bilan ishga tushiradi (haqiqiy iPhone'da sinab bo'lmaydi).
const fs=require('fs'),code=fs.readFileSync(process.argv[2],'utf8'),AF=Object.getPrototypeOf(async function(){}).constructor;
const ok=(l,c)=>console.log((c?'PASS ':'FAIL ')+l);
async function run(o){const texts=[],rec={reqs:[],set:0,present:0,done:0};
  class Stack{addText(t){texts.push(t);return{}}addSpacer(){}centerAlignContent(){}}
  class ListWidget{addText(t){texts.push(t);return{}}addStack(){return new Stack()}addSpacer(){}setPadding(){}async presentMedium(){rec.present++}}
  class Color{constructor(h){this.h=h}}const Font={systemFont:n=>n,boldSystemFont:n=>n};
  class Request{constructor(u){this.url=u;rec.reqs.push(this)}async loadJSON(){if(o.fail)throw new Error(o.fail);this.response={statusCode:o.status||200};return o.json}}
  const config={runsInWidget:o.inWidget!==false,widgetFamily:o.fam},Script={setWidget:w=>{rec.set++;rec.w=w},complete:()=>{rec.done++}};
  await new AF('Request','ListWidget','Color','Font','config','Script',code)(Request,ListWidget,Color,Font,config,Script);return{texts,...rec}}
const SNAP={snap:{v:1,d:'2026-11-02',dow:'Dushanba',dd:'2 noyabr',hab:[3,8],nm:[5,5],hf:[1,3],fm:45,top:[{t:'Misol',x:1},{t:'Hifz',x:0},{t:'Zal',x:0}],nx:{t:'Zal',at:'22:00'},ie:12,gl:{t:'IELTS',p:40}},updated_at:'2026-11-02T10:05:00'};
(async()=>{
 let r=await run({json:SNAP,fam:'medium'});const T=r.texts.join(' | ');
 ok('medium: title with the weekday and date, habits bar 3/8 (▰▰▰▱▱▱▱▱), prayers 5/5, next block, hifz and focus (5 rows)',/Kunlik tizim · Dushanba 2 noyabr/.test(T)&&T.includes('Odatlar ▰▰▰▱▱▱▱▱')&&T.includes('3/8')&&T.includes('Namoz ▰▰▰▰▰▰▰▰')&&T.includes('5/5')&&T.includes('22:00 Zal')&&T.includes('1/3 bet')&&T.includes('45 daq')&&!T.includes('Top-3'));
 ok('in a widget the script hands it to iOS (setWidget) and does not open a preview; it completes',r.set===1&&r.present===0&&r.done===1);
 ok('the update time is shown',/Yangilandi \d\d:05/.test(T));
 r=await run({json:SNAP,fam:'small'});ok('small: only 3 rows (habits, prayers, next)',r.texts.some(t=>t.includes('Odatlar'))&&r.texts.some(t=>t.includes('Namoz'))&&r.texts.some(t=>t==='22:00 Zal')&&!r.texts.some(t=>t.includes('Hifz')));
 r=await run({json:SNAP,fam:'large'});const L=r.texts.join(' | ');ok('large: all 8 rows plus today\u2019s top tasks with ✓ / ○',L.includes('Top-3')&&L.includes('1/3')&&L.includes('12 kun')&&L.includes('40%')&&L.includes('✓ Misol')&&L.includes('○ Hifz'));
 r=await run({json:SNAP,fam:'medium',inWidget:false});ok('run inside the Scriptable app: shows a preview instead',r.present===1&&r.set===0);
 r=await run({json:SNAP});ok('the request goes to the widget URL with the token and sends the key headers',r.reqs.length===1&&/\/functions\/v1\/widget\?t=[a-f0-9]{32}/.test(r.reqs[0].url)&&(r.reqs[0].headers||{}).Authorization===('Bearer '+(r.reqs[0].headers||{}).apikey));
 r=await run({json:{error:'Vidjet topilmadi. Ilovada vidjetni qayta yoqing.'}});ok('a server error message is shown on the widget instead of crashing',r.texts.join(' ').includes('Vidjet topilmadi')&&r.set===1);
 r=await run({fail:'Network request failed'});ok('no internet: the widget shows "Malumot olinmadi" with the reason and still finishes',r.texts.join(' ').includes('Malumot olinmadi: Network request failed')&&r.set===1&&r.done===1);
 r=await run({json:{snap:{v:1,hab:[0,0],nm:[0,5]},updated_at:null},fam:'medium'});ok('an empty day (no habits, nothing done, no time) does not break it',r.texts.join(' ').includes('Odatlar ▱▱▱▱▱▱▱▱')&&r.set===1);
 r=await run({json:{snap:{v:1,hab:[8,8],nm:[5,5],ie:3},updated_at:'2026-11-02T10:05:00'},fam:'large'});ok('everything done fills the bars (▰×8); an exam within 14 days is highlighted',r.texts.join(' ').includes('▰▰▰▰▰▰▰▰')&&r.texts.join(' ').includes('3 kun'));
 r=await run({json:{code:401,message:'Invalid JWT'},status:401});ok('a Supabase gateway error (not from our function) shows its own message and the status code',r.texts.join(' ').includes('Invalid JWT (401)')&&r.set===1);
 r=await run({json:{code:'NOT_FOUND',message:'Requested function was not found'},status:404});ok('a function that is not deployed is shown clearly (message and 404)',r.texts.join(' ').includes('Requested function was not found (404)'));
})();
