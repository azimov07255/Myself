// ---- Jadval ustuni kengligi, ixcham va keng ko'rinish, Bugun'da dam kuni, zaxira eslatmasi, "Ishga tayyormi?" ----
const uiG=k=>{try{return localStorage.getItem(k)}catch(e){return null}},uiS=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
const NWMIN=90,NWMAX=260,NWDEF=138,hbNwGet=()=>{const v=+uiG('trk_nw');return v>=NWMIN&&v<=NWMAX?v:NWDEF};
function hbNwSet(px){px=Math.max(NWMIN,Math.min(NWMAX,Math.round(px)));document.documentElement.style.setProperty('--nw',px+'px');uiS('trk_nw',px);return px}
function hbNw(d){hbNwSet(hbNwGet()+d);render()}
function hbNwReset(){uiS('trk_nw','');document.documentElement.style.removeProperty('--nw');render()}
function hbCompact(){const on=uiG('trk_hbc')!=='1';uiS('trk_hbc',on?'1':'0');document.documentElement.classList.toggle('hbc',on);render()}
function wideToggle(){const on=!wideOn();uiS('trk_wide',on?'1':'0');document.documentElement.classList.toggle('wide',on);render()}
function uiInit(){const d=document.documentElement;if(+uiG('trk_nw'))d.style.setProperty('--nw',hbNwGet()+'px');else d.style.removeProperty('--nw');d.classList.toggle('hbc',uiG('trk_hbc')==='1');d.classList.toggle('wide',typeof wideOn==='function'?wideOn():uiG('trk_wide')==='1')}
try{uiInit()}catch(e){}
try{(function(){let dr=null;
  document.addEventListener('pointerdown',e=>{const n=e.target.closest&&e.target.closest('.mn');if(!n)return;const r=n.getBoundingClientRect();if(e.clientX<r.right-8)return;dr={x:e.clientX,w:r.width,mv:0}});
  document.addEventListener('pointermove',e=>{if(!dr)return;if(!dr.mv&&Math.abs(e.clientX-dr.x)<4)return;dr.mv=1;hbNwSet(dr.w+e.clientX-dr.x)});
  const up=()=>{dr=null};document.addEventListener('pointerup',up);document.addEventListener('pointercancel',up)})()}catch(e){}
function hbCtl(){const c=uiG('trk_hbc')==='1',w=wideOn();return `<div class="in" style="flex-wrap:wrap;margin:8px 0"><span class="mu hbcol" style="align-self:center;font-size:13px">Ustun:</span><button class="btn s hbcol" onclick="hbNw(-20)" aria-label="Torroq">◀ Tor</button><button class="btn s hbcol" onclick="hbNw(20)" aria-label="Kengroq">Keng ▶</button><button class="btn s" onclick="hbCompact()">${c?'Batafsil':'Ixcham'}</button><button class="btn s hbwide" onclick="wideToggle()">${w?'Tor ekran':'↔ Keng ekran'}</button></div>`}
// ---- Bugun'da dam kuni ----
function hbS(id,k){k=k||dk();S.hb[k]=S.hb[k]||{};S.hk=S.hk||{};const hk=S.hk[k]=S.hk[k]||{};if(hk[id]){delete hk[id];if(!Object.keys(hk).length)delete S.hk[k]}else{hk[id]=1;S.hb[k][id]=false}save()}
function hbRest(k){if(!S.hab.length)return '';const rs=x=>hkOn(k,x.id)&&!(S.hb[k]||{})[x.id],n=S.hab.filter(rs).length;
  return `<details class="sd"${n?' open':''}><summary>🛌 Dam kuni belgilash${n?' ('+n+')':''}</summary><div class="rwch" style="margin-top:6px">${S.hab.map(x=>`<button class="chip ${rs(x)?'on':''}" style="border:0" onclick="hbS('${x.id}','${k}')">${x.e?x.e+' ':''}${esc(x.t)}</button>`).join('')}</div><p class="mu" style="font-size:12px;margin:6px 0 0">Kasal yoki safarda: odat bajarilmagan hisoblanmaydi va seriya uzilmaydi.</p></details>`}
// ---- zaxira eslatmasi ----
function bkAge(){const b=uiG('trk_bk'),m=b&&String(b).match(/\d{4}-\d{2}-\d{2}/);return m?Math.floor((new Date(dk()+'T12:00')-new Date(m[0]+'T12:00'))/864e5):null}
const bkUsed=()=>Object.keys(S.hb||{}).filter(k=>Object.values(S.hb[k]||{}).some(Boolean)).length>=3||(S.money||[]).length>=10||((S.ie&&S.ie.words)||[]).length>=20;
function bkBar(){const age=bkAge();if(!bkUsed()||(age!==null&&age<7)||(uiG('trk_bksn')||'')>dk())return '';
  return `<div class="goal" style="padding:10px 14px"><b>💾 Zaxira nusxa</b><p class="mu" style="margin:4px 0 6px;font-size:13px">${age===null?'Hali zaxira olinmagan.':age+' kun oldin zaxira olgansan.'} Ma‘lumot serverda saqlanadi, lekin faylga ham saqlab qo‘yish xavfsizroq.</p><div class="in"><button class="btn" style="flex:1" onclick="bkDl()">Faylga saqlash</button><button class="btn s" onclick="bkShare()" aria-label="Telegram yoki Fayllarga yuborish">📲</button><button class="btn s" onclick="bkSn()">Keyinroq</button></div></div>`}
function bkSn(){const d=new Date(dk()+'T12:00');d.setDate(d.getDate()+3);uiS('trk_bksn',d.toLocaleDateString('sv'));render()}
// ---- Ishga tayyormi? ----
let RDY={run:0,res:null};
async function rdRun(){if(RDY.run)return;RDY.run=1;RDY.res=null;render();const R=[],add=(ok,t,h)=>R.push({ok,t,h});
  try{const d=await fnPost({action:'limit'},15000);add(true,'Server va AI ishlayapti',d.owner?'Egasi hisobi: AI cheksiz.':'AI limiti: kuniga '+d.limit+' ta (bugun '+d.used+' ta).')}catch(e){add(false,'Server javob bermayapti',String(e.message||e).slice(0,110)+' Internetni va Supabase funksiyasini tekshir.')}
  add(SYNC==='ok'||SYNC==='wait','Sinxronlash',SYNC==='ok'?'Ma‘lumot serverga saqlangan.':SYNC==='wait'?'Kutilmoqda, birozdan keyin saqlanadi.':'Oflayn: internet yo‘q yoki server javob bermayapti.');
  const a=bkAge();add(a!==null&&a<=7,'Zaxira nusxa',a===null?'Hali olinmagan: Sozlama → Zaxira nusxa → Faylga saqlash.':a>7?a+' kun oldin. Yangisini ol.':'Oxirgi zaxira '+a+' kun oldin.');
  const r=S.rem||{},tg=!!(r.tg||r.tgOn||r.telegram),np=typeof Notification!=='undefined'?Notification.permission:'yo‘q';add(!!(r.on||tg),'Eslatmalar',r.on||tg?'Yoqilgan'+(r.on?' (bildirishnoma)':'')+(tg?' (Telegram)':'')+'.':'Yoqilmagan: Sozlama → Eslatmalar.');
  const sa=!!(navigator.standalone||(window.matchMedia&&matchMedia('(display-mode: standalone)').matches));add(sa,'Ilova sifatida o‘rnatilgan',sa?'Ha.':'Yo‘q: iPhone’da Safari → Ulashish → Bosh ekranga qo‘shish (bildirishnoma uchun shart).');
  if(np!=='yo‘q')add(np==='granted'||tg,'Bildirishnoma ruxsati',np==='granted'?'Berilgan.':tg?'Berilmagan, lekin Telegram yoqilgan.':'Berilmagan: Sozlama → Eslatmalar → Bildirishnomani yoqish.');
  add(S.hab.length>0,'Odatlar',S.hab.length?S.hab.length+' ta odat.':'Odat bo‘limida o‘z odatlaringni yoz.');
  add((S.goals||[]).length>0,'Maqsadlar',(S.goals||[]).length?(S.goals||[]).length+' ta maqsad.':'Maqsad bo‘limida kamida bitta maqsad yoz.');
  add(!!(S.ie&&S.ie.ex),'IELTS imtihon sanasi',S.ie&&S.ie.ex?S.ie.ex+'.':'IELTS → Bosh’da sanani qo‘y (yo‘l xaritasi shundan tuziladi).');
  add(!!(S.ie&&S.ie.target),'IELTS maqsad bali',S.ie&&S.ie.target?String(S.ie.target):'IELTS → Bosh’da maqsad ballni tanla.');
  add(!!(S.q&&S.q.ppd>0),'Hifz: kuniga bet',S.q&&S.q.ppd>0?S.q.ppd+' bet.':'Qur‘on bo‘limida kuniga necha bet yodlashni sozla.');
  let sz=0;try{sz=JSON.stringify(S).length}catch(e){}add(sz<3.5*1048576,'Saqlash hajmi',(sz/1048576).toFixed(1)+' MB (brauzer chegarasi ~5 MB).'+(sz<3.5*1048576?'':' Zaxira olib, eski yozuvlarni tozala.'));
  RDY.res=R;RDY.run=0;render()}
function rdCard(){const R=RDY.res,n=R?R.filter(x=>x.ok).length:0;
  return `<p class="mu" style="margin:0 0 8px">Ilovani real ishlatishdan oldin hamma muhim narsa joyidami, tekshirib beradi.</p><button class="btn" onclick="rdRun()" ${RDY.run?'disabled':''}>${RDY.run?'Tekshirilmoqda…':R?'Qayta tekshirish':'Tekshirish'}</button>${R?`<p style="margin:10px 0 6px"><b>${n} / ${R.length}</b> tayyor</p>${R.map(x=>`<div class="row" style="cursor:default"><span class="ck" style="${x.ok?'':'background:var(--bad);border-color:var(--bad);color:#fff'}">${x.ok?'✓':'!'}</span><span class="t">${esc(x.t)}<br><span class="mu" style="font-size:13px">${esc(x.h)}</span></span></div>`).join('')}`:''}`}
