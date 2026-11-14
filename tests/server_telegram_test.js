// telegram-bot.ts va send-reminders.ts sinovi: xotiradagi soxta baza + soxta Telegram
const fs=require('fs'),esbuild=require('/tmp/esb/node_modules/esbuild');
const ok=(l,c)=>{console.log((c?'PASS ':'FAIL ')+l);if(!c)process.exitCode=1};
function mkDb(tables){
  const q=(t)=>{const st={f:[],op:'select',row:null};
    const exec=()=>{const T=tables[t]=tables[t]||[];const m=r=>st.f.every(([c,v])=>r[c]===v);
      if(st.op==='insert'){T.push({id:T.length+1,...st.row});return{data:null,error:null}}
      if(st.op==='upsert'){const key=t==='tg_links'?'user_id':'id';const i=T.findIndex(r=>r[key]===st.row[key]);if(i>=0)T[i]={...T[i],...st.row};else T.push({...st.row});return{data:null,error:null}}
      if(st.op==='delete'){tables[t]=T.filter(r=>!m(r));return{data:null,error:null}}
      if(st.op==='update'){T.filter(m).forEach(r=>Object.assign(r,st.row));return{data:null,error:null}}
      return{data:T.filter(m),error:null}};
    const b={select:()=>b,eq:(c,v)=>{st.f.push([c,v]);return b},insert:r=>{st.op='insert';st.row=r;return b},upsert:r=>{st.op='upsert';st.row=r;return b},delete:()=>{st.op='delete';return b},update:r=>{st.op='update';st.row=r;return b},
      maybeSingle:async()=>{const r=exec();return{data:(r.data||[])[0]||null,error:null}},then:(res,rej)=>Promise.resolve(exec()).then(res,rej)};return b};
  return{from:q}}
function load(file,env,extra){
  let src=fs.readFileSync(file,'utf8').replace(/import \{ createClient \} from [^\n]+\n/,'const createClient=globalThis.__cc;\n').replace(/import webpush from [^\n]+\n/,'const webpush=globalThis.__wp;\n');
  const out=esbuild.transformSync(src,{loader:'ts',target:'es2022'}).code;let handler=null;
  globalThis.Deno={env:{get:k=>env[k]},serve:h=>{handler=h}};new Function(out)();return handler}
const TGSEND=[];let tgStatus=200;
globalThis.fetch=async(u,o)=>{if(/api\.telegram\.org/.test(u)){const m=/bot[^/]+\/(\w+)/.exec(u)[1];TGSEND.push({m,b:JSON.parse(o.body)});return{ok:tgStatus<300,status:tgStatus,json:async()=>({ok:tgStatus<300})}}return{ok:true,status:200,json:async()=>({})}};
(async()=>{
 // ================= telegram-bot =================
 const tables={tg_codes:[],tg_links:[],tg_inbox:[],app_state:[{user_id:'u1',data:{}}]};
 globalThis.__cc=()=>mkDb(tables);
 const env={TELEGRAM_BOT_TOKEN:'tok',TELEGRAM_WEBHOOK_SECRET:'sec',SUPABASE_URL:'u',SUPABASE_SERVICE_ROLE_KEY:'s'};
 const H=load('/mnt/user-data/outputs/server-setup/telegram-bot.ts',env);
 const call=async(body,secret='sec')=>{TGSEND.length=0;const r=await H(new Request('http://x',{method:'POST',headers:secret?{'x-telegram-bot-api-secret-token':secret}:{},body:JSON.stringify(body)}));return r};
 const msg=(text,chat=111,type='private')=>({message:{text,chat:{id:chat,type},from:{username:'aziz'},message_id:5}});
 const last=()=>TGSEND.filter(x=>x.m==='sendMessage').slice(-1)[0];
 const tzDate=tz=>new Date(Date.now()+tz*60000).toISOString().slice(0,10);
 let r=await call(msg('/start'),'wrong');ok('wrong webhook secret -> 403 (nobody else can call the bot)',r.status===403);
 r=await call(msg('/start'),'');ok('missing secret -> 403',r.status===403);
 r=await call(msg('/start'));ok('/start without code (not linked) explains how to link',r.status===200&&/Telegramga ulash/.test(last().b.text));
 tables.tg_codes.push({code:'ABCD2345',user_id:'u1',tz:300,expires_at:new Date(Date.now()+600000).toISOString()});
 r=await call(msg('/start abcd2345'));
 ok('/start CODE (case-insensitive) links the chat to the user with the app\'s timezone',tables.tg_links.length===1&&tables.tg_links[0].user_id==='u1'&&tables.tg_links[0].chat_id===111&&tables.tg_links[0].tz===300&&tables.tg_links[0].username==='aziz');
 ok('code is consumed and a welcome with help is sent',tables.tg_codes.length===0&&/Ulandi/.test(last().b.text)&&/\/bugun/.test(last().b.text)&&last().b.parse_mode==='HTML');
 tables.tg_codes.push({code:'OLDOLD22',user_id:'u2',tz:300,expires_at:new Date(Date.now()-1000).toISOString()});
 await call(msg('/start OLDOLD22',222));ok('expired code refused, nothing linked',!tables.tg_links.some(l=>l.chat_id===222)&&/eskirgan/.test(last().b.text));
 tables.tg_codes.push({code:'MOVE5555',user_id:'u3',tz:360,expires_at:new Date(Date.now()+600000).toISOString()});
 await call(msg('/start MOVE5555',111));ok('a chat linked to another account is re-linked to the new one (old link removed)',tables.tg_links.length===1&&tables.tg_links[0].user_id==='u3'&&tables.tg_links[0].tz===360);
 // back to u1 for the following checks
 tables.tg_links=[{user_id:'u1',chat_id:111,username:'aziz',tz:300}];
 await call(msg('/vazifa Kitob o‘qish'));const inb=tables.tg_inbox.slice(-1)[0];
 ok('/vazifa adds a task to the inbox with today\'s date in the user\'s timezone',inb&&inb.kind==='task'&&inb.payload.t==='Kitob o‘qish'&&inb.payload.d===tzDate(300)&&inb.user_id==='u1');
 await call(msg('/vazifa <b>x</b> & y'));ok('user text is HTML-escaped in the reply (no formatting injection)',/&lt;b&gt;x&lt;\/b&gt; &amp; y/.test(last().b.text));
 await call(msg('/vazifa'));ok('/vazifa without text shows the usage',/\/vazifa/.test(last().b.text));
 const n0=tables.tg_inbox.length;await call(msg('/vazifa '+'x'.repeat(500)));ok('long task text is cut to 200 chars',tables.tg_inbox.length===n0+1&&tables.tg_inbox.slice(-1)[0].payload.t.length===200);
 await call(msg('/suv'));ok('/suv adds one glass to the inbox',tables.tg_inbox.slice(-1)[0].kind==='water'&&tables.tg_inbox.slice(-1)[0].payload.n===1);
 // /bugun reads the synced state
 const d=tzDate(300);tables.app_state[0].data={top:{[d]:[{t:'Dars tayyorlash',x:1},{t:'Zal',x:0}]},tasks:{[d]:[{t:'Referat',x:0}]},nm:{d:{[d]:{fajr:1,dhuhr:2}}},water:{[d]:3}};
 await call(msg('/bugun'));const bt=last().b.text;
 ok('/bugun shows top tasks, tasks, prayers (✅/❌/⬜) and water',/✅ Dars tayyorlash/.test(bt)&&/⬜ Zal/.test(bt)&&/⬜ Referat/.test(bt)&&/✅ Bomdod/.test(bt)&&/❌ Peshin/.test(bt)&&/⬜ Asr/.test(bt)&&/Suv: 3\/8/.test(bt));
 // callbacks
 const cb=data=>({callback_query:{id:'cq1',data,message:{message_id:9,text:'🔔 Bomdod namozi\nVaqti kirdi',chat:{id:111,type:'private'}}}});
 await call(cb('nm:fajr'));ok('button "O‘qidim" -> inbox row nm/fajr with the date',tables.tg_inbox.slice(-1)[0].kind==='nm'&&tables.tg_inbox.slice(-1)[0].payload.p==='fajr'&&tables.tg_inbox.slice(-1)[0].payload.d===d);
 ok('button press answers the tap and replaces the buttons with ✅ Belgilandi',TGSEND.some(x=>x.m==='answerCallbackQuery'&&x.b.callback_query_id==='cq1')&&TGSEND.some(x=>x.m==='editMessageText'&&/Belgilandi/.test(x.b.text)&&x.b.reply_markup.inline_keyboard.length===0));
 await call(cb('blk:dars-1'));ok('block button -> inbox row blk with the block id',tables.tg_inbox.slice(-1)[0].kind==='blk'&&tables.tg_inbox.slice(-1)[0].payload.id==='dars-1');
 const n1=tables.tg_inbox.length;await call(cb('nm:../../x'));await call(cb('blk:a b;drop'));await call(cb('evil'));ok('malformed/unknown button data is rejected (nothing inserted)',tables.tg_inbox.length===n1);
 const bad={callback_query:{id:'c9',data:'nm:fajr',message:{message_id:1,text:'x',chat:{id:999,type:'private'}}}};await call(bad);ok('button from an unlinked chat does nothing',tables.tg_inbox.length===n1&&TGSEND.some(x=>x.m==='answerCallbackQuery'&&/ulang/i.test(x.b.text)));
 await call(msg('/bugun',999));ok('commands from an unlinked chat ask to link first',/Avval ulang/.test(last().b.text));
 await call(msg('/vazifa x',333,'group'));ok('group chat messages are ignored',TGSEND.length===0);
 await call(msg('salom'));ok('unknown text -> hint to /yordam',/yordam/.test(last().b.text));
 await call(msg('/stop'));ok('/stop removes the link',tables.tg_links.length===0&&/uzildi/.test(last().b.text));
 const H2=load('/mnt/user-data/outputs/server-setup/telegram-bot.ts',env);globalThis.__cc=()=>({from:()=>{throw new Error('db down')}});
 const r5=await H2(new Request('http://x',{method:'POST',headers:{'x-telegram-bot-api-secret-token':'sec'},body:JSON.stringify(msg('/bugun'))}));ok('database failure still answers 200 (Telegram must not retry forever)',r5.status===200);
 // ================= send-reminders =================
 const loc=new Date(Date.now()+300*60000),hhmm=String(loc.getUTCHours()).padStart(2,'0')+':'+String(loc.getUTCMinutes()).padStart(2,'0'),dow=loc.getUTCDay();
 const mkRem=(over)=>({id:over.id,user_id:'u1',hhmm,days:[dow],title:over.title,body:over.body||'',tz:300,last_sent:null,kind:over.kind||''});
 const t2={reminders:[mkRem({id:1,title:'Bomdod namozi',body:'Vaqti kirdi',kind:'nm:fajr'}),mkRem({id:2,title:'Dars',kind:'blk:dars-1'}),mkRem({id:3,title:'Kunni yopish vaqti'})],push_subs:[],tg_links:[{user_id:'u1',chat_id:111}]};
 globalThis.__cc=()=>mkDb(t2);globalThis.__wp={setVapidDetails(){},sendNotification:async()=>{}};
 const env2={...env,CRON_SECRET:'cs',VAPID_SUBJECT:'mailto:a@b.c',VAPID_PUBLIC:'p',VAPID_PRIVATE:'q'};
 const SR=load('/mnt/user-data/outputs/server-setup/send-reminders.ts',env2);TGSEND.length=0;
 const rr=await SR(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));const sm=TGSEND.filter(x=>x.m==='sendMessage');
 ok('due reminders are delivered to Telegram (3 messages): '+sm.map(x=>x.b.text.split('\n')[0]).join(' | '),sm.length===3&&sm.every(x=>x.b.chat_id===111));
 ok('prayer reminder carries the "O‘qidim" button with callback nm:fajr',sm[0].b.reply_markup&&sm[0].b.reply_markup.inline_keyboard[0][0].callback_data==='nm:fajr'&&/O‘qidim/.test(sm[0].b.reply_markup.inline_keyboard[0][0].text));
 ok('schedule-block reminder carries "Bajardim" (blk:dars-1); plain reminder has no buttons',sm[1].b.reply_markup.inline_keyboard[0][0].callback_data==='blk:dars-1'&&!sm[2].b.reply_markup);
 ok('reminders are marked as sent (no duplicates next minute)',t2.reminders.every(x=>x.last_sent));
 TGSEND.length=0;await SR(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));ok('second run in the same minute sends nothing again',TGSEND.length===0);
 t2.reminders.forEach(x=>x.last_sent=null);tgStatus=403;TGSEND.length=0;await SR(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));ok('user blocked the bot (403) -> link removed automatically',t2.tg_links.length===0);tgStatus=200;
 t2.tg_links=[{user_id:'u1',chat_id:111}];t2.reminders.forEach(x=>x.last_sent=null);const SR2=load('/mnt/user-data/outputs/server-setup/send-reminders.ts',{...env2,TELEGRAM_BOT_TOKEN:''});TGSEND.length=0;await SR2(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));ok('without a bot token nothing is sent to Telegram (push-only setups keep working)',TGSEND.length===0);
 const rf=await SR(new Request('http://x',{headers:{'x-cron-secret':'bad'}}));ok('reminder function still requires the cron secret',rf.status===403);

 // ================= setup problems must be visible, not silent =================
 const errs=[];const realErr=console.error;console.error=(...a)=>errs.push(a.join(' '));
 const mkDbErr=msg=>({from:()=>{const b={select:()=>b,eq:()=>b,insert:()=>b,upsert:()=>b,delete:()=>b,maybeSingle:async()=>({data:null,error:{message:msg}}),then:(res)=>res({data:null,error:{message:msg}})};return b}});
 globalThis.__cc=()=>mkDbErr('relation "public.tg_links" does not exist');
 const H3=load('/mnt/user-data/outputs/server-setup/telegram-bot.ts',env);TGSEND.length=0;
 const r3=await H3(new Request('http://x',{method:'POST',headers:{'x-telegram-bot-api-secret-token':'sec'},body:JSON.stringify(msg('/start'))}));
 ok('tables missing (telegram.sql not run): still 200, and the chat says what to do instead of staying silent',r3.status===200&&TGSEND.some(x=>x.m==='sendMessage'&&/telegram\.sql/.test(x.b.text))&&errs.some(e=>/telegram-bot error/.test(e)));
 globalThis.__cc=()=>mkDbErr('connection reset');TGSEND.length=0;const H3b=load('/mnt/user-data/outputs/server-setup/telegram-bot.ts',env);
 await H3b(new Request('http://x',{method:'POST',headers:{'x-telegram-bot-api-secret-token':'sec'},body:JSON.stringify(msg('/bugun'))}));
 ok('other errors give a generic message (internal details are not shown to users)',TGSEND.some(x=>x.m==='sendMessage'&&/Vaqtincha/.test(x.b.text)&&!/connection reset/.test(x.b.text)));
 globalThis.__cc=()=>mkDb({tg_links:[],tg_codes:[],tg_inbox:[]});
 const H4=load('/mnt/user-data/outputs/server-setup/telegram-bot.ts',{...env,TELEGRAM_BOT_TOKEN:' "bot123456:AAH-x_y" ',TELEGRAM_WEBHOOK_SECRET:' sec \n'});
 const urls=[];const f0=globalThis.fetch;globalThis.fetch=async(u,o)=>{urls.push(u);return f0(u,o)};
 const r4=await H4(new Request('http://x',{method:'POST',headers:{'x-telegram-bot-api-secret-token':'sec'},body:JSON.stringify(msg('/start'))}));
 ok('badly copied secrets (quotes, spaces, "bot" prefix, trailing newline) are cleaned: token used = 123456:AAH-x_y',r4.status===200&&urls.some(u=>u==='https://api.telegram.org/bot123456:AAH-x_y/sendMessage'));
 globalThis.fetch=f0;errs.length=0;tgStatus=401;await H3(new Request('http://x',{method:'POST',headers:{'x-telegram-bot-api-secret-token':'sec'},body:JSON.stringify(msg('/start'))}));
 globalThis.__cc=()=>mkDb({tg_links:[],tg_codes:[],tg_inbox:[]});const H5=load('/mnt/user-data/outputs/server-setup/telegram-bot.ts',env);errs.length=0;
 await H5(new Request('http://x',{method:'POST',headers:{'x-telegram-bot-api-secret-token':'sec'},body:JSON.stringify(msg('/start'))}));
 ok('when Telegram rejects the token (401) the cause is written to Logs ("telegram api sendMessage 401")',errs.some(e=>/telegram api sendMessage 401/.test(e)));
 tgStatus=200;console.error=realErr;
 // reminders: same cleaning
 const t5={reminders:[mkRem({id:1,title:'Test'})],push_subs:[],tg_links:[{user_id:'u1',chat_id:111}]};globalThis.__cc=()=>mkDb(t5);
 const SR3=load('/mnt/user-data/outputs/server-setup/send-reminders.ts',{...env2,TELEGRAM_BOT_TOKEN:' bot555:ZZ '});const u2=[];globalThis.fetch=async(u,o)=>{u2.push(u);return f0(u,o)};
 await SR3(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));ok('reminder sender also cleans the token',u2.some(u=>u==='https://api.telegram.org/bot555:ZZ/sendMessage'));globalThis.fetch=f0;

 // ================= zikr and fasting buttons =================
 {
 const tb={tg_codes:[],tg_links:[{user_id:'u1',chat_id:111,tz:300}],tg_inbox:[],app_state:[]};globalThis.__cc=()=>mkDb(tb);
 const HZ=load('/mnt/user-data/outputs/server-setup/telegram-bot.ts',env);
 const cz=async data=>{TGSEND.length=0;return HZ(new Request('http://x',{method:'POST',headers:{'x-telegram-bot-api-secret-token':'sec'},body:JSON.stringify({callback_query:{id:'q',data,message:{message_id:3,text:'🔔 x',chat:{id:111,type:'private'}}}})}))};
 const dz=tzDate(300);
 await cz('zk:sb');ok('zikr button (morning) -> inbox zk with category sb',tb.tg_inbox.slice(-1)[0].kind==='zk'&&tb.tg_inbox.slice(-1)[0].payload.c==='sb'&&tb.tg_inbox.slice(-1)[0].payload.d===dz);
 await cz('zk:sh');ok('zikr button (evening) -> category sh',tb.tg_inbox.slice(-1)[0].payload.c==='sh');
 await cz('rz:1');ok('fasting "Tutdim" -> inbox rz with v=1 (number)',tb.tg_inbox.slice(-1)[0].kind==='rz'&&tb.tg_inbox.slice(-1)[0].payload.v===1);
 await cz('rz:2');ok('fasting "Tutolmadim" -> v=2',tb.tg_inbox.slice(-1)[0].payload.v===2);
 const n=tb.tg_inbox.length;await cz('zk:nm');await cz('rz:3');await cz('rz:');await cz('zk:sb;x');ok('other zikr/fasting values are rejected',tb.tg_inbox.length===n);
 // reminder buttons
 const loc2=new Date(Date.now()+300*60000),hh=String(loc2.getUTCHours()).padStart(2,'0')+':'+String(loc2.getUTCMinutes()).padStart(2,'0'),dw=loc2.getUTCDay();
 const mk2=(id,title,kind)=>({id,user_id:'u1',hhmm:hh,days:[dw],title,body:'',tz:300,last_sent:null,kind});
 const t6={reminders:[mk2(1,'Ertalabki zikr','zk:sb'),mk2(2,'Kechki zikr','zk:sh'),mk2(3,'Ro‘za: bugun tutdingmi?','rz')],push_subs:[],tg_links:[{user_id:'u1',chat_id:111}]};globalThis.__cc=()=>mkDb(t6);
 const SR6=load('/mnt/user-data/outputs/server-setup/send-reminders.ts',env2);TGSEND.length=0;await SR6(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));
 const m6=TGSEND.filter(x=>x.m==='sendMessage');
 ok('zikr reminders carry one "O‘qidim" button (zk:sb / zk:sh)',m6[0].b.reply_markup.inline_keyboard[0][0].callback_data==='zk:sb'&&m6[1].b.reply_markup.inline_keyboard[0][0].callback_data==='zk:sh'&&m6[0].b.reply_markup.inline_keyboard[0].length===1);
 const rzb=m6[2].b.reply_markup.inline_keyboard[0];ok('fasting reminder carries two buttons: ✅ Tutdim (rz:1) and ❌ Tutolmadim (rz:2) in one row',rzb.length===2&&rzb[0].callback_data==='rz:1'&&rzb[1].callback_data==='rz:2'&&/Tutdim/.test(rzb[0].text)&&/Tutolmadim/.test(rzb[1].text));
 }

 // ================= date-limited reminders (st@date / wk@date) and plain 'ym' =================
 {
 const loc=new Date(Date.now()+300*60000),hh=String(loc.getUTCHours()).padStart(2,'0')+':'+String(loc.getUTCMinutes()).padStart(2,'0'),dw=loc.getUTCDay();
 const day=x=>new Date(loc.getTime()+x*864e5).toISOString().slice(0,10),today=day(0);
 const mk=(id,title,kind)=>({id,user_id:'u1',hhmm:hh,days:[dw],title,body:'x',tz:300,last_sent:null,kind});
 const t7={reminders:[mk(1,'BUGUNGI','st@'+today),mk(2,'ESKI','st@'+day(-1)),mk(3,'KELAJAK','st@'+day(1)),mk(4,'ODDIY','ym'),mk(5,'HAFTA','wk@'+today)],push_subs:[],tg_links:[{user_id:'u1',chat_id:111}]};globalThis.__cc=()=>mkDb(t7);
 const SR7=load('/mnt/user-data/outputs/server-setup/send-reminders.ts',env2);TGSEND.length=0;await SR7(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));
 const ms=TGSEND.filter(x=>x.m==='sendMessage'),tx=ms.map(x=>x.b.text).join('|');
 ok('a reminder dated today (st@date) is sent',tx.includes('BUGUNGI'));
 ok('a reminder dated yesterday is NOT sent and is deleted',!tx.includes('ESKI')&&!t7.reminders.some(r=>r.id===2));
 ok('a reminder dated tomorrow is neither sent nor deleted',!tx.includes('KELAJAK')&&t7.reminders.some(r=>r.id===3));
 ok('plain kind "ym" (morning) is sent without buttons',tx.includes('ODDIY')&&ms.find(x=>x.b.text.includes('ODDIY')).b.reply_markup===undefined);
 ok('weekly report kind (wk@date) is sent on its date',tx.includes('HAFTA'));
 const t8={reminders:[mk(9,'BLOK','blk:qur@'+today)],push_subs:[],tg_links:[{user_id:'u1',chat_id:111}]};globalThis.__cc=()=>mkDb(t8);
 const SR8=load('/mnt/user-data/outputs/server-setup/send-reminders.ts',env2);TGSEND.length=0;await SR8(new Request('http://x',{headers:{'x-cron-secret':'cs'}}));
 const m8=TGSEND.filter(x=>x.m==='sendMessage');
 ok('a dated block reminder (blk:qur@date) still gets its "Bajardim" button with the clean callback blk:qur',m8.length===1&&m8[0].b.reply_markup.inline_keyboard[0][0].callback_data==='blk:qur');
 }
})();
