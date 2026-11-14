// ---- Telegram bot: ulash, eslatmalar va pochta qutisi ----
let TGB='',TGL=null,TGW=false;
async function tgInit(){if(!sb||!UID)return;
  try{const c=await sb.from('app_config').select('value').eq('key','tg_bot').maybeSingle();TGB=(c.data&&c.data.value)||'';
    if(!TGB)return;const l=await sb.from('tg_links').select('chat_id').eq('user_id',UID).maybeSingle();if(l.error)return;
    const was=TGL;TGL=!!l.data;
    if(TGL&&!S.rem.tg){S.rem.tg=true;if(S.rem.nz===undefined)S.rem.nz=true;if(TGW)try{toast('Telegram ulandi ✅')}catch(e){}TGW=false;save();await syncRem(true)}
    else if(!TGL&&S.rem.tg){S.rem.tg=false;save();await syncRem(true)}
  }catch(e){}}
async function tgLink(){if(!TGB){alert('Telegram bot hali sozlanmagan.');return}
  const A='ABCDEFGHJKLMNPQRSTUVWXYZ23456789',rnd=new Uint8Array(8);crypto.getRandomValues(rnd);let code='';rnd.forEach(x=>{code+=A[x%A.length]});
  const r=await sb.from('tg_codes').insert({code,user_id:UID,tz:-new Date().getTimezoneOffset(),expires_at:new Date(Date.now()+20*60000).toISOString()});
  if(r.error){alert('Kod yaratib bo‘lmadi: '+(r.error.message||r.error));return}
  TGW=true;window.open('https://t.me/'+TGB+'?start='+code,'_blank');render()}
async function tgUnlink(){if(!confirm('Telegram uzilsinmi? Eslatmalar botga kelmaydi.'))return;await sb.from('tg_links').delete().eq('user_id',UID);TGL=false;S.rem.tg=false;save();await syncRem(true)}
function rzForce(k,v){const R=S.rz,c=R.fast[k]||0;if(c===v)return;
  if(c===2){R.debt=Math.max(0,R.debt-1);const x=R.log.findIndex(y=>y.d===k&&y.k==='miss');if(x>=0)R.log.splice(x,1)}
  if(v===2){R.debt++;R.log.push({id:Date.now(),d:k,k:'miss',n:1})}R.fast[k]=v}
function nmOne(k,p){const N=S.nm,d=N.d[k]=N.d[k]||{},c=d[p]||0;if(c===1)return;
  if(c===2){N.debt[p]=Math.max(0,(N.debt[p]||0)-1);const i=N.log.findIndex(x=>x.d===k&&x.p===p&&x.k==='miss');if(i>=0)N.log.splice(i,1)}d[p]=1}
// Bot "pochta qutisi"ga yozadi, ilova ochilganda shu yerdan olib o‘z holatiga qo‘llaydi (sinxron bilan to‘qnashmaydi)
async function tgApply(){if(!sb||!UID||!TGL)return;
  try{const r=await sb.from('tg_inbox').select('*').eq('applied',false).order('id',{ascending:true}).limit(100);
    if(r.error||!r.data||!r.data.length)return;
    const done=new Set(S.tgd||[]),ids=[];let ch=false;
    for(const x of r.data){ids.push(x.id);if(done.has(x.id))continue;done.add(x.id);
      const p=x.payload||{},k=/^\d{4}-\d\d-\d\d$/.test(p.d||'')?p.d:dk();if(k>dk())continue;
      if(x.kind==='nm'&&['fajr','dhuhr','asr','maghrib','isha','vitr'].includes(p.p)){nmOne(k,p.p);ch=true}
      else if(x.kind==='blk'&&/^[\w-]{1,40}$/.test(p.id||'')){(S.done[k]=S.done[k]||{})[p.id]=true;ch=true}
      else if(x.kind==='task'&&p.t){(S.tasks[k]=S.tasks[k]||[]).push({t:String(p.t).slice(0,200),x:0});ch=true}
      else if(x.kind==='zk'&&['sb','sh'].includes(p.c)){const D=S.dz.d[k]=S.dz.d[k]||{};dzList(p.c).forEach(d=>{D[d.id+'@'+p.c]=d.k});ch=true}
      else if(x.kind==='rz'&&(p.v===1||p.v===2)){rzForce(k,p.v);ch=true}
      else if(x.kind==='water'){S.water[k]=Math.max(0,Math.min(8,(S.water[k]||0)+(+p.n||1)));ch=true}}
    S.tgd=[...done].slice(-200);
    if(ch){save();try{toast('Telegramdagi belgilar qo‘llandi')}catch(e){}}else lsSet(KEY(),JSON.stringify(S))
    await sb.from('tg_inbox').delete().in('id',ids)
  }catch(e){}}
async function tgSync(){await tgInit();await tgApply()}
function tgBlock(){if(!TGB)return '';
  if(TGL)return `<div class="goal" style="padding:12px 14px;border-left:4px solid var(--ac);margin-bottom:8px"><b>✈️ Telegram ulangan ✅</b><p class="mu" style="margin:6px 0 8px">Eslatmalar botga keladi, tugma bosib belgilaysan. Buyruqlar: /bugun, /vazifa, /suv, /yordam.</p><button class="btn s" onclick="tgUnlink()">Uzish</button></div>`;
  return `<div class="goal" style="padding:12px 14px;margin-bottom:8px"><b>✈️ Telegram orqali eslatma</b><p class="mu" style="margin:6px 0 8px">Eslatmalar Telegram’ga keladi va tugma bilan belgilaysan. Bildirishnomadan ishonchliroq.</p><button class="big" style="margin:0" onclick="tgLink()">${TGW?'Telegramda “Start” ni bos, keyin shu yerga qayt':'Telegramga ulash'}</button></div>`}

async function fn(body){const r=await sb.functions.invoke('create-user',{body});
  if(!r.error)return r.data;
  try{return await r.error.context.json()}catch(e){return{error:'Funksiya topilmadi yoki ishlamadi'}}}
let OS='7',OA='',OST=null,PROF=null;
async function loadOw(){const d=await fn({action:'list'});OW=d&&d.users?d.users:false;OST=d&&d.stats||null;render();if(Array.isArray(OW)&&ERRL===null)loadErrs()}
function genP(){const c='abcdefghjkmnpqrstuvwxyz23456789';OP=[...crypto.getRandomValues(new Uint8Array(8))].map(x=>c[x%c.length]).join('');render()}
const ago=t=>{if(!t)return 'hali kirmagan';const m=Math.floor((Date.now()-new Date(t))/60000);return m<2?'hozirgina':m<60?m+' daqiqa oldin':m<1440?Math.floor(m/60)+' soat oldin':Math.floor(m/1440)+' kun oldin'};
async function ownAct(body){const d=await fn(body);OE=d&&d.error?d.error:'';await loadOw();return !OE}
async function mkU(){
  const l=OL.trim().toLowerCase();
  if(!/^[a-z0-9_.]{3,20}$/.test(l)||OP.length<6){OE='Login 3–20 ta lotin harf yoki raqam, parol kamida 6 belgi bo‘lsin.';return render()}
  if(await ownAct({action:'create',login:l,password:OP,name:ON.trim(),plan:+OS})){OC={login:l,pass:OP};OL=OP=ON='';render()}
}
async function ugr(id,days){if(await ownAct({action:'grant',id,days,amount:sfn(OA)}))OA=''}
function ubl(id,b){ownAct({action:'block',id,blocked:b})}
async function upw(id){const p=prompt('Yangi parol (kamida 6 belgi):');if(!p)return;if(p.length<6){alert('Parol kamida 6 belgi.');return}if(await ownAct({action:'setpass',id,password:p}))alert('Parol almashtirildi: '+p)}
function udl(id){if(confirm('Foydalanuvchi va uning hamma ma‘lumoti o‘chirilsinmi?'))ownAct({action:'delete',id})}
function cp(){const t='Kunlik tizim\nLink: '+location.origin+location.pathname+'\nLogin: '+OC.login+'\nParol: '+OC.pass;
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{OC.copied=1;render()}).catch(()=>{prompt('Nusxalang:',t)})}
function stLine(u){const now=Date.now();
  if(u.blocked)return '<span style="color:var(--bad)">Bloklangan</span>';
  if(u.lifetime)return '<span style="color:var(--ac)">∞ Umrbod premium</span>';
  if(!u.expires_at||new Date(u.expires_at)<=now)return '<span style="color:var(--bad)">Obuna tugagan</span>';
  return `<span style="color:var(--ac)">Obuna: ${Math.ceil((new Date(u.expires_at)-now)/864e5)} kun qoldi (${u.expires_at.slice(0,10)})</span>`}
const hasPrem=u=>u.lifetime||(u.expires_at&&new Date(u.expires_at)>Date.now());
const revokeBtn=u=>hasPrem(u)&&!u.blocked?`<button class="ghost" style="margin-top:6px;color:var(--bad);border-color:var(--bad)" onclick="urv('${u.id}',${u.lifetime?1:0})">↩ ${u.lifetime?'Umrbod premiumni':'Premiumni'} qaytarib olish</button>`:'';
function urv(id,life){const d=prompt((life?'Umrbod premium qaytarib olinadi.':'Premium muddati qisqartiriladi.')+' Necha kun qolsin? (0 yozsang, darhol tugaydi)','0');if(d===null)return;
  const n=Math.max(0,parseInt(d,10)||0);if(!confirm(n?`Premium ${n} kundan keyin tugaydi. Davom etilsinmi?`:'Premium DARHOL tugaydi va foydalanuvchi kira olmaydi. Davom etilsinmi?'))return;
  ownAct({action:'revoke',id,days:n,amount:sfn(OA)}).then(r=>{if(r){OA='';render()}})}
function owner(){
  if(!Array.isArray(OW))return '';
  const s=OST||{month:0,prev:0,total:0},us=OW.map(u=>{const lg=(u.email||'').replace('@trk.app','');
    return `<div class="goal"><b>${esc(u.name||lg)}${u.me?' (siz)':''}</b><p class="mu" style="margin:2px 0">${esc(lg)}, oxirgi faollik: ${ago(u.last)}</p><p style="margin:0 0 ${u.me?0:8}px">${stLine(u)}</p>
    ${u.me?'':`<div class="ug"><button class="btn s" onclick="ugr('${u.id}',1)">+1</button><button class="btn s" onclick="ugr('${u.id}',7)">+7</button><button class="btn s" onclick="ugr('${u.id}',30)">+30</button><button class="btn s" onclick="ugr('${u.id}',-1)">∞</button><button class="btn s" onclick="ubl('${u.id}',${!u.blocked})">${u.blocked?'Ochish':'Blok'}</button></div><div class="in" style="margin:6px 0 0"><button class="btn s" style="flex:1" onclick="upw('${u.id}')">Parol</button><button class="btn s" style="flex:1" onclick="udl('${u.id}')">O‘chirish</button></div>${revokeBtn(u)}`}</div>`}).join('');
  const card=OC?`<div class="goal" style="border:1px solid var(--go)"><b>Tayyor. Yuborish uchun nusxala</b><p class="mu" style="margin:6px 0 10px">Login: ${esc(OC.login)}<br>Parol: ${esc(OC.pass)}</p><button class="btn" onclick="cp()">${OC.copied?'Nusxalandi':'Nusxalash'}</button></div>`:'';
  return `<h2>Foydalanuvchilar</h2><div class="st"><div><b style="font-size:15px">${num(s.month)}</b>bu oy, so‘m</div><div><b style="font-size:15px">${num(s.prev)}</b>o‘tgan oy</div><div><b style="font-size:15px">${num(s.total)}</b>jami</div></div>
  ${card}<div class="goal" style="margin-top:12px"><b>Yangi foydalanuvchi</b><div class="in" style="margin-top:10px"><input placeholder="Login (masalan: aziz01)" value="${esc(OL)}" oninput="OL=this.value" autocapitalize="none"></div><div class="in"><input placeholder="Parol (kamida 6 belgi)" value="${esc(OP)}" oninput="OP=this.value" autocapitalize="none"></div><button class="ghost" style="margin:0 0 8px" onclick="genP()">Parol yaratish</button><div class="in"><input placeholder="Ism (ixtiyoriy)" value="${esc(ON)}" oninput="ON=this.value"></div><div class="in"><select onchange="OS=this.value">${[['3','Sinov: 3 kun'],['7','Sinov: 7 kun'],['30','30 kun'],['-1','Umrbod premium']].map(x=>`<option value="${x[0]}" ${OS===x[0]?'selected':''}>${x[1]}</option>`).join('')}</select></div><p class="err">${esc(OE)}</p><button class="big" style="margin:0" onclick="mkU()">Foydalanuvchi qo‘shish</button></div>
  <h2>Obuna berish</h2><div class="in"><input type="text" inputmode="numeric" placeholder="To‘lov summasi, so‘m (sovg‘a bo‘lsa bo‘sh qoldir)" value="${esc(OA)}" oninput="OA=this.value"></div><p class="mu" style="margin:0 0 8px">Pastdagi +1, +7, +30 yoki ∞ tugmasini bossang, shu summa to‘lov sifatida yoziladi. Premiumni qaytarib olayotganda summa yozilgan bo‘lsa, u qaytarilgan pul sifatida hisobdan ayriladi.</p>${us}`;
}

// ---- Obuna va bloklash ----
async function loadProf(){
  if(!sb||!UID)return;
  try{const r=await sb.from('profiles').select('*').eq('user_id',UID).maybeSingle();if(!r.error){PROF=r.data||null;try{localStorage.setItem('trk_prof',JSON.stringify(PROF))}catch(e){}}}catch(e){}
  if(!PROF){try{PROF=JSON.parse(localStorage.getItem('trk_prof')||'null')}catch(e){}}}
const lockMsg=()=>{const p=PROF;if(!p)return '';if(p.blocked)return 'Hisobingiz bloklangan. Egasi bilan bog‘laning.';if(!p.lifetime&&(!p.expires_at||new Date(p.expires_at)<=new Date()))return 'Obuna muddati tugagan. Davom etish uchun egasi bilan bog‘laning.';return ''};
const subDays=()=>PROF&&!PROF.lifetime&&PROF.expires_at?Math.ceil((new Date(PROF.expires_at)-Date.now())/864e5):null;
const subLine=()=>!PROF?'':PROF.lifetime?'∞ Umrbod premium':'Obuna: '+subDays()+' kun qoldi ('+PROF.expires_at.slice(0,10)+')';
const subChip=()=>{const d=subDays();return d!==null&&d<=3&&d>0?` <span class="chip bad">obuna ${d} kun qoldi</span>`:''};
async function recheck(){await loadProf();if(!lockMsg())await pull();render()}
function lockView(){return `<div class="auth"><img src="favicon.svg" width="64" height="64" alt="" style="border-radius:16px;margin-bottom:16px"><h1>Kirish cheklangan</h1>${brand()}<p class="mu">${lockMsg()}</p>${tgBtn('Obuna olish: Telegram’da yozish')}<button class="ghost" onclick="recheck()">Qayta tekshirish</button><button class="ghost" onclick="out()">Chiqish</button></div>`}
async function out(){try{await sb.auth.signOut()}catch(e){}try{localStorage.removeItem('trk_uid')}catch(e){}UID=null;OW=null;OC=null;PROF=null;S=blank();render()}
function err(t){const e=$('#er');if(e)e.textContent=t}
async function auth(up){
  const l=$('#lg').value.trim().toLowerCase(),p=$('#pw').value;
  if(!l.includes('@')&&!/^[a-z0-9_.]{3,20}$/.test(l))return err('Login 3–20 ta lotin harf yoki raqamdan iborat bo‘lsin.');
  if(p.length<6)return err('Parol kamida 6 belgidan iborat bo‘lsin.');
  const c={email:l.includes('@')?l:l+'@trk.app',password:p};
  const r=up?await sb.auth.signUp(c):await sb.auth.signInWithPassword(c);
  if(r.error)return err(/invalid/i.test(r.error.message)?'Login yoki parol noto‘g‘ri.':r.error.message);
    await start(r.data.session.user.id,r.data.session.user.email);
}
async function start(id,em){UID=id;REV=(()=>{const v=lsGet('trk_rev_'+id);return v==null?null:+v})();ensurePersist();try{localStorage.setItem('trk_uid',id);if(em)localStorage.setItem('trk_em',em)}catch(e){}S=load();await loadProf();if(!lockMsg()){await pull();if(S.ts&&!S.sg)sgMig();await tgSync();try{if(localStorage.getItem('trk_dirty'))push()}catch(e){}}render()}
(async()=>{
  await Promise.resolve();
  if(!sb){S=load();render();ptEnsure()}
  else{
    let ok=false;
    try{const r=await sb.auth.getSession();if(r.data&&r.data.session){ok=true;await start(r.data.session.user.id,r.data.session.user.email);ptEnsure()}}catch(e){}
    if(!ok){let u=null;try{u=localStorage.getItem('trk_uid')}catch(e){}if(u&&navigator.onLine===false)await start(u);else render()}
  }
  ['touchstart','touchmove','scroll'].forEach(ev=>window.addEventListener(ev,()=>{LT=Date.now()},{passive:true}));
  setInterval(()=>{ptEnsure();if(Date.now()-LT<3000)return;if(tab!=='h'&&tab!=='q')return;const a=document.activeElement;if(!a||!/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))render()},30000);
  window.addEventListener('online',()=>{SYNC='ok';let d=null;try{d=localStorage.getItem('trk_dirty')}catch(e){}if(d)push();else pull().then(c=>{if(c)render()});tgSync();render()});
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'&&sb&&UID&&Date.now()-LPL>20000){LPL=Date.now();pull().then(c=>{if(c)render();tgSync()})}});
  window.addEventListener('offline',()=>{SYNC='off';render()});
  if('serviceWorker' in navigator&&/^https?:/.test(location.protocol))navigator.serviceWorker.register('sw.js').catch(()=>{});
})();
