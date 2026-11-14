// ---- Ko‘rinish va sozlamalar ----
const getTh=()=>{try{return localStorage.getItem('trk_theme')||'auto'}catch(e){return 'auto'}};
function applyTheme(){const t=getTh(),r=document.documentElement;if(t==='auto')r.removeAttribute('data-theme');else r.setAttribute('data-theme',t);
  let dark=t==='dark';if(t==='auto'){try{dark=matchMedia('(prefers-color-scheme:dark)').matches}catch(e){dark=true}}
  const m=document.querySelector('meta[name=theme-color]');if(m)m.content=dark?'#0a1a2c':'#f8f4ea'}
function setTh(t){try{localStorage.setItem('trk_theme',t)}catch(e){}applyTheme();render()}
const grp=(id,title,html)=>{if(!html)return '';const q=typeof SDQ==='string'?sn(SDQ).trim():'';if(q&&!sn(id+' '+title).includes(q))return '';return `<details class="sd" ${(SDO[id]||q)?'open':''} ontoggle="SDO['${id}']=this.open"><summary>${title}</summary>${html.replace(/^\s*<h2>[^<]*<\/h2>/,'')}</details>`};
function sozlama(){const t=getTh();
  const bk=`<p class="mu" style="margin:0 0 8px">Hamma ma‘lumotingni faylga saqlab qo‘y. Keyin istalgan vaqt tiklash mumkin.${(()=>{let b=null;try{b=localStorage.getItem('trk_bk')}catch(e){}return b?' Oxirgi zaxira: '+b+'.':' Hali zaxira olinmagan.'})()}</p><div class="in"><button class="btn s" onclick="bkDl()">Faylga saqlash</button><button class="btn s" onclick="bkCp()">Matnni nusxalash</button></div><div class="in"><label class="btn s" style="cursor:pointer">Fayldan tiklash<input type="file" accept="application/json,.json" style="display:none" onchange="bkLd(this)"></label><button class="btn s" onclick="bkTx()">Matndan tiklash</button></div>`;
  return `<p class="mu" style="margin:0">Sozlamalar</p><h1 class="gr">Ilovani o‘zingga moslash</h1>
  <h2>Ko‘rinish</h2><div class="seg">${[['auto','Tizim'],['light','Yorug‘'],['dark','Qorong‘u']].map(x=>`<button class="${t===x[0]?'on':''}" onclick="setTh('${x[0]}')">${x[1]}</button>`).join('')}</div><p class="mu">Tizim tanlansa, telefonning kunduz va tun rejimiga qarab o‘zi almashadi. Bu tanlov faqat shu qurilmada saqlanadi.</p>
  <h2>Profil</h2><div class="in"><input placeholder="Ismingiz" value="${esc(S.name)}" onchange="S.name=this.value.trim();save()"></div>
  <h2>Hisob</h2><p class="mu" style="margin:0 0 6px">${sb?(UID?'Ma‘lumot hisobingizga saqlanadi va boshqa qurilmada ham ko‘rinadi.':'Kirilmagan.'):'Hozircha faqat shu telefonda saqlanadi.'}</p><p class="mu" style="margin:0 0 6px">${SYNC==='ok'?'Sinxronlash: hamma narsa saqlangan.':SYNC==='wait'?'Sinxronlash: internet kelganda yuboriladi.':'Internet yo‘q. Ma‘lumot shu telefonda saqlanadi va keyin sinxronlanadi.'}</p>${PROF?`<p style="margin:0 0 6px">⭐ ${subLine()}</p>${PROF.lifetime?'':tgBtn('Obunani uzaytirish')}`:''}${sb&&UID?`<button class="ghost" onclick="out()">Chiqish</button>`:''}
  ${grp('ai','✨ AI yordamchi',aiSet())}${grp('rem','🔔 Eslatmalar',remCard())}${grp('us','📊 Foydalanish',usCard())}${grp('mod','🔀 Reja rejimlari',modesCard())}${MUSHAF_MODE!=='off'?grp('mf','📖 Mushaf bo‘limi',mfSet()):''}${grp('ov','🔊 Ovoz',ovCard())}${grp('dz','🎨 Dizayn',dzCard())}${grp('bm','🗂 Bugun ko‘rinishi',bmCard())}${grp('nw','🆕 Yangiliklar va qo‘llanma',newsCard())}${grp('rd','✅ Ishga tayyormi?',rdCard())}${grp('wd','📱 Vidjet (iPhone)',wdCard())}${grp('zh','🛡 Zaxira holati',snCard())}${grp('xj','🩺 Xatolar jurnali'+(XJ().list().length?' ('+XJ().list().length+')':''),xjCard()+tsCard())}${grp('jl','🪄 Jilo va qulaylik',jlCard())}${grp('bk','💾 Zaxira nusxa',bk)}${grp('hs','🕘 Avtomatik zaxiralar',histCard())}${grp('dg','🩺 Diagnostika',diagCard())}${Array.isArray(OW)?grp('er','🐞 Xatolar (egasi uchun)'+errBadge(),errCard()):''}${grp('own','👥 Foydalanuvchilar va obuna',owner())}
  <p class="mu" style="text-align:center;margin-top:28px;letter-spacing:.14em;font-size:12px">KUNLIK TIZIM BY AZIMOV</p>`}

applyTheme();try{matchMedia('(prefers-color-scheme:dark)').addEventListener('change',()=>{if(getTh()==='auto')applyTheme()})}catch(e){}

// ---- Bugungi 3 ta asosiy ish va kunni yopish ----
function addTopTo(id,k){const e=$('#'+id),v=e&&e.value.trim();if(!v)return;const L=S.top[k]=S.top[k]||[];if(L.length>=3)return;L.push({t:v,x:0});save()}
function tpT(k,i){const t=S.top[k][i];t.x=t.x?0:1;save()}
function tpD(k,i){S.top[k].splice(i,1);save()}
function setRate(k,v){(S.close[k]=S.close[k]||{}).r=v;save()}
function togPh(k){const c=S.close[k]=S.close[k]||{};c.p=!c.p;save()}
function closeDay(k,v){(S.close[k]=S.close[k]||{}).d=v;save()}
function topCard(k,fu){
  const L=S.top[k]||[],a=fu?'':'1';
  const rows=L.map((x,i)=>`<div class="row ${x.x?'done':''}"><span class="ck" onclick="${a?`tpT('${k}',${i})`:''}">${x.x?'✓':''}</span><span class="t" onclick="${a?`tpT('${k}',${i})`:''}">${esc(x.t)}</span><button class="x" onclick="tpD('${k}',${i})">×</button></div>`).join('');
  return `<div class="goal" style="margin-top:12px;border-left:4px solid var(--go)"><div class="h"><b style="font:700 19px Fraunces,serif">3 ta asosiy ish</b><span class="mu">${L.filter(x=>x.x).length}/${L.length||3}</span></div>${L.length?'':'<p class="mu" style="margin:6px 0 8px">Eng muhim 3 ta ishni yoz. Qolgan hamma narsa shulardan keyin.</p>'}<div style="margin-top:8px">${rows}</div>${L.length<3?`<div class="in"><input id="tpa" placeholder="${L.length+1}-asosiy ish" onkeydown="if(event.key==='Enter')addTopTo('tpa','${k}')"><button class="btn" onclick="addTopTo('tpa','${k}')">+</button></div>`:''}${aiPlanUi(k,fu,L)}</div>`}
function ritual(k,sc){
  const cl=S.close[k]||{},tom=dAgo(-1),tt=S.top[tom]||[];
  if(cl.d)return `<section class="hero" style="margin-top:12px"><p class="lab">Kun yopildi</p><h1 style="font-size:28px">Xayrli tun</h1><p class="mu">Bugungi ball ${sc}%${cl.r?', baho '+'★'.repeat(cl.r):''}. Ertaga uchun ${tt.length} ta asosiy ish tayyor.</p><button class="ghost" style="color:var(--htx)" onclick="closeDay('${k}',false)">Qayta ochish</button></section>`;
  const list=tt.map((x,i)=>`<div class="row"><span class="t">${esc(x.t)}</span><button class="x" onclick="tpD('${tom}',${i})">×</button></div>`).join('');
  return `<section class="hero" style="margin-top:12px"><p class="lab">Kunni yopish</p><h1 style="font-size:26px">Bugunni xotirjam yakunla</h1>
  <p class="mu" style="margin-top:10px">1. Kunni bahola (bugungi ball ${sc}%)</p><div class="stars">${[1,2,3,4,5].map(n=>`<button class="${(cl.r||0)>=n?'on':''}" onclick="setRate('${k}',${n})">★</button>`).join('')}</div>
  <p class="mu">2. Ertangi 3 ta asosiy ish (${tt.length}/3)</p>${list}${tt.length<3?`<div class="in"><input id="tpb" placeholder="Ertangi ish" onkeydown="if(event.key==='Enter')addTopTo('tpb','${tom}')"><button class="btn" onclick="addTopTo('tpb','${tom}')">+</button></div>`:''}
  <p class="mu">3. Telefon</p><button class="row ${cl.p?'done':''}" onclick="togPh('${k}')"><span class="ck">${cl.p?'✓':''}</span><span class="t">Telefonni chetga qo‘ydim</span></button>
  ${eodExtra(k)}<button class="big" onclick="closeDay('${k}',true)">Kunni yopish</button></section>`}

// ---- Zaxira nusxa ----
const bkMark=()=>{try{localStorage.setItem('trk_bk',dk())}catch(e){}};
function bkApply(t){try{const d=JSON.parse(t);if(!d||typeof d!=='object'||!d.goals)throw 0}catch(e){alert('Zaxira noto‘g‘ri.');return}snPreview(t,'Fayl yoki matn')}
function bkDl(){const b=new Blob([JSON.stringify(S)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='tizim-zaxira-'+dk()+'.json';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),4000);bkMark();render()}
function bkCp(){const t=JSON.stringify(S);(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{bkMark();alert('Nusxalandi. Uni Telegram’dagi “Saqlangan xabarlar”ga yopishtirib qo‘ying.');render()}).catch(()=>prompt('Nusxalang:',t))}
function bkLd(inp){const f=inp.files[0];if(!f)return;const r=new FileReader();r.onload=()=>bkApply(r.result);r.readAsText(f)}
function bkTx(){const t=prompt('Zaxira matnini shu yerga qo‘ying:');if(t)bkApply(t)}

// ---- Eslatmalar (push bildirishnoma) ----
const VAPID='BHSPty1nCc5qXZ7PE3kydFGguHvZ9s9t07YHGGnUh0tOSgro81f841YP9k3ksADS5Gs60dzOq6SH30vGFKXBX0Y';
let RT=null;
const u8=b=>{const s=(b+'='.repeat((4-b.length%4)%4)).replace(/-/g,'+').replace(/_/g,'/'),r=atob(s);return Uint8Array.from([...r].map(c=>c.charCodeAt(0)))};
function remRows(){
  const r=S.rem,rows=[],tz=-new Date().getTimezoneOffset(),A=[0,1,2,3,4,5,6];
  if(!r.on&&!r.tg)return rows;
  if(r.blk)bl().forEach(b=>{if(b.s-r.off<0||b.s>=1440)return;if(b.on){if(b.on<dk()||b.on>rwAdd(dk(),7))return;rows.push({hhmm:hm(b.s-r.off),days:[new Date(b.on+'T12:00').getDay()],title:b.t,body:r.off?r.off+' daqiqadan keyin boshlanadi':'Boshlanish vaqti keldi',tz,kind:'blk:'+b.id+'@'+b.on});if(b.tr&&b.s-b.tr>=0)rows.push({hhmm:hm(b.s-b.tr),days:[new Date(b.on+'T12:00').getDay()],title:'🚶 Yo‘lga chiqish: '+b.t,body:b.tr+' daqiqada yetib borasan',tz,kind:'tr:'+b.id+'@'+b.on});return}rmBlk(rows,b,r,tz)});
  if(r.close)rows.push({hhmm:r.ct,days:A,title:'Kunni yopish vaqti',body:'Bugunni baholang va ertangi 3 ta asosiy ishni yozing.',tz});
  if(r.wake&&S.wk.start){const t=tgtFor(new Date().getHours()>=12?dAgo(-1):dk());rows.push({hhmm:hm(t),days:A,title:'Turish vaqti',body:'Bugungi maqsad: '+hm(t)+'. Tur va namozga tayyorlan.',tz})}
  if(r.nz){const tt=ptTimes(),no=r.noff!==undefined?r.noff:10;if(tt)[['Fajr','Bomdod'],['Dhuhr','Peshin'],['Asr','Asr'],['Maghrib','Shom'],['Isha','Xufton']].forEach(([k,n])=>{if(tt[k]!==undefined)rows.push({hhmm:hm(tt[k]-no+1440),days:A,title:n+' namozi',body:no?no+' daqiqadan keyin vaqti kiradi':'Vaqti kirdi',tz,kind:'nm:'+k.toLowerCase()})})}
  if(r.zk){rows.push({hhmm:r.zam||'06:30',days:A,title:'Ertalabki zikr',body:'Ertalabki zikr va duolarni o‘qish vaqti.',tz,kind:'zk:sb'});rows.push({hhmm:r.zpm||'18:30',days:A,title:'Kechki zikr',body:'Kechki zikr va duolarni o‘qish vaqti.',tz,kind:'zk:sh'})}
  if(r.blk){const T=dk(),nw=new Date().getHours()*60+new Date().getMinutes();[T,dAgo(-1)].forEach(d=>{const P=(S.ap||{})[d];if(!P)return;const dw=new Date(d+'T12:00').getDay();P.it.filter(x=>!x.fx).forEach(x=>{const s=x.s-r.off;if(s<0||(d===T&&s<=nw))return;rows.push({hhmm:hm(s),days:[dw],title:x.t,body:(r.off?r.off+' daqiqadan keyin boshlanadi':'Boshlanish vaqti keldi')+' · AI reja',tz,kind:'ap@'+d})})})}
  if(r.yo){const k=dk(),t=dayPts(k).t,st=rwStreak(),X=xpInfo(),dow=new Date().getDay(),sun=rwAdd(rwMon(k),6);
    if(st>0&&t<DAYMIN)rows.push({hhmm:'21:00',days:[dow],title:'🔥 Seriyang xavfda',body:st+' kunlik seriya. Saqlash uchun yana '+(DAYMIN-t)+' XP kerak: 10 daqiqada ham ulgurasan!',tz,kind:'st@'+k});
    rows.push({hhmm:'07:00',days:A,title:'🌅 Yangi kun',body:X.L+'-daraja'+(st>0?' · 🔥 '+st+' kunlik seriya':'')+'. Bugungi 3 topshiriq Yo‘l ekranida kutmoqda.',tz,kind:'ym'});
    rows.push({hhmm:'20:30',days:[0],title:'📊 Haftalik hisobot',body:rwRepShort(),tz,kind:'wk@'+sun})}
  if(r.rz&&rzInfo().on)rows.push({hhmm:'21:30',days:A,title:'Ro‘za: bugun tutdingmi?',body:'Belgilab qo‘y: ro‘za tutdingmi yoki qazo bo‘ldimi.',tz,kind:'rz'});
  r.custom.forEach(c=>rows.push({hhmm:c.time,days:A,title:c.t,body:'',tz}));
  S.hab.forEach(x=>{if(x.rt&&/^\d\d:\d\d$/.test(x.rt))rows.push({hhmm:x.rt,days:A,title:'🔔 '+(x.e?x.e+' ':'')+x.t,body:'Odatni belgilashni unutma.',tz,kind:'hb:'+x.id})});
  try{ksRows(rows,tz,A)}catch(e){}
  try{klxRows(rows,tz,A)}catch(e){}
  return rows}
async function syncRem(force){
  if(!sb||!UID)return;const rows=remRows(),sig=JSON.stringify(rows);let last=null;try{last=localStorage.getItem('trk_remsig')}catch(e){}
  if(!force&&sig===last)return;
  try{const d=await sb.from('reminders').delete().eq('user_id',UID);if(d.error)throw d.error;
    if(rows.length){let i=await sb.from('reminders').insert(rows.map(x=>({user_id:UID,...x})));if(i.error&&/kind/.test(i.error.message||'')){i=await sb.from('reminders').insert(rows.map(x=>{const y={user_id:UID,...x};delete y.kind;return y}))}if(i.error)throw i.error}
    try{localStorage.setItem('trk_remsig',sig)}catch(e){}}catch(e){}}
function remSoon(){clearTimeout(RT);RT=setTimeout(()=>syncRem(),2000)}
async function pushOn(){
  if(!sb||!UID){alert('Avval hisobga kiring.');return}
  if(!('serviceWorker' in navigator)||!('PushManager' in window)||typeof Notification==='undefined'){alert('Bu yerda bildirishnoma ishlamaydi. iPhone’da ilovani “Bosh ekranga qo‘shish” orqali o‘rnatib, bosh ekrandagi ikonkadan oching.');return}
  const p=await Notification.requestPermission();if(p!=='granted'){alert('Ruxsat berilmadi. Telefon sozlamalaridan ilova uchun bildirishnomaga ruxsat bering.');return}
  try{const reg=await navigator.serviceWorker.ready;let sub=await reg.pushManager.getSubscription();if(!sub)sub=await reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:u8(VAPID)});
    const j=sub.toJSON(),r=await sb.from('push_subs').upsert({user_id:UID,endpoint:j.endpoint,p256dh:j.keys.p256dh,auth:j.keys.auth},{onConflict:'endpoint'});if(r.error)throw r.error;
    S.rem.on=true;save();await syncRem(true)}catch(e){alert('Yoqib bo‘lmadi: '+(e.message||e))}}
async function pushOff(){try{const reg=await navigator.serviceWorker.ready,sub=await reg.pushManager.getSubscription();if(sub){await sb.from('push_subs').delete().eq('endpoint',sub.endpoint);await sub.unsubscribe()}}catch(e){}S.rem.on=false;save();await syncRem(true)}
function testN(){navigator.serviceWorker.ready.then(r=>r.showNotification('Kunlik tizim',{body:'Sinov: bildirishnoma ishlayapti.',icon:'icon-192.png'})).catch(()=>alert('Yuborib bo‘lmadi.'))}
function remT(f){S.rem[f]=!S.rem[f];save()}
function remOff(v){S.rem.off=+v;save()}
function remNo(v){S.rem.noff=+v;save()}
function remCt(v){if(v){S.rem.ct=v;save()}}
function addRem(){const t=$('#rt').value,x=$('#rx').value.trim();if(!t||!x)return;S.rem.custom.push({id:Date.now(),time:t,t:x});save()}
function delRem(i){S.rem.custom.splice(i,1);save()}
function remCard(){
  const r=S.rem,np=typeof Notification!=='undefined'?Notification.permission:'yo‘q',chk=(on,f,t)=>`<button class="row ${on?'done':''}" onclick="remT('${f}')"><span class="ck">${on?'✓':''}</span><span class="t">${t}</span></button>`;
  if(!sb||!UID)return `<h2>Eslatmalar</h2><p class="mu">Eslatmalar uchun hisobga kirgan bo‘lishing kerak.</p>`;
  if(!r.on&&!r.tg)return `<h2>Eslatmalar</h2><p class="mu">Reja vaqti kelganda telefoningga bildirishnoma keladi, ilova yopiq bo‘lsa ham. iPhone’da avval ilovani “Bosh ekranga qo‘shish” orqali o‘rnat va bosh ekrandagi ikonkadan och.</p><button class="big" style="margin:0" onclick="pushOn()">Bildirishnomani yoqish</button>${tgBlock()}`;
  return `<h2>Eslatmalar</h2>${tgBlock()}<p class="mu">${r.on?`Bildirishnoma yoqilgan (ruxsat: ${np==='granted'?'berilgan':np}).`:'Faqat Telegram yoqilgan.'}</p>${r.on?'':'<button class="btn s" style="margin-bottom:8px" onclick="pushOn()">Bildirishnomani ham yoqish</button>'}
  ${chk(r.blk,'blk','Har bir reja boshlanganda')}<div class="in"><select onchange="remOff(this.value)">${[0,5,10,15].map(m=>`<option value="${m}" ${r.off===m?'selected':''}>${m?m+' daqiqa oldin':'Aynan boshlanganda'}</option>`).join('')}</select></div>
  ${chk(r.wake,'wake','Turish vaqti (uyg‘onish maqsadi)')}${chk(r.close,'close','Kunni yopish')}<div class="in"><input type="time" value="${r.ct}" onchange="remCt(this.value)"></div>
  ${chk(r.yo,'yo','Yo‘l: seriya xavfi (21:00), ertalabki xabar, yakshanba hisoboti')}${chk(r.zk,'zk','Ertalabki va kechki zikr (06:30 va 18:30)')}${chk(r.rz,'rz','Ramazon: kechqurun ro‘za belgilash (21:30)')}
  ${chk(r.nz,'nz','Namoz vaqtlari')}<div class="in"><select onchange="remNo(this.value)">${[0,5,10,15,20].map(m=>`<option value="${m}" ${(r.noff!==undefined?r.noff:10)===m?'selected':''}>${m?m+' daqiqa oldin':'Aynan vaqti kirganda'}</option>`).join('')}</select></div>
  <p class="mu" style="margin:8px 0">O‘zingning eslatmang:</p>${r.custom.map((c,i)=>`<div class="row"><span class="t">${esc(c.t)}</span><span class="tm">${c.time}</span><button class="x" onclick="delRem(${i})">×</button></div>`).join('')}
  <div class="in"><input type="time" id="rt" value="08:00" style="flex:0 0 120px"><input id="rx" placeholder="Masalan: 33 ta zikr" onkeydown="if(event.key==='Enter')addRem()"><button class="btn" onclick="addRem()">+</button></div>
  <div class="in"><button class="btn s" onclick="testN()">Sinab ko‘rish</button><button class="btn s" onclick="pushOff()">O‘chirish</button></div>`}

