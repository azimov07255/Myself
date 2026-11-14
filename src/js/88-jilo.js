// ---- JILO: o'zbekcha sanalar, "bekor qilish", kengaytirilgan qidiruv, sozlamalar qidiruvi, takror hisobi qoidasi, surish maslahati, tizim tekshiruvi. Har biri Sozlamalar → 🪄 Jilo va qulaylik da o'chiriladi ----
const dfU=()=>uiG('trk_dfmt')!=='i',udOn=()=>uiG('trk_ud')!=='0',tqRd=()=>uiG('trk_tqrd')==='q';
function dU(k){if(!k||!/^\d{4}-\d\d-\d\d$/.test(String(k)))return String(k||'');if(!dfU())return k;const y=+k.slice(0,4),m=+k.slice(5,7)-1,d=+k.slice(8,10);return d+'-'+MON[m]+(y!==new Date().getFullYear()?' '+y:'')}
// ----- ↩︎ bekor qilish -----
let UDT=0,UDS=null;
function udShow(msg,snap){if(!udOn())return;let e=document.getElementById('udb');if(!e){e=document.createElement('div');e.id='udb';e.className='udb';e.setAttribute('role','status');document.body.appendChild(e)}UDS=snap;e.innerHTML=`<span>${esc(msg)}</span><button onclick="udDo()">↩︎ Bekor qilish</button>`;e.style.display='flex';clearTimeout(UDT);UDT=setTimeout(udHide,8000)}
function udHide(){UDS=null;const e=document.getElementById('udb');if(e)e.style.display='none'}
function udDo(){const sn=UDS;if(!sn)return;try{S=norm(Object.assign(blank(),JSON.parse(sn)))}catch(e){return}udHide();save();toast('↩︎ Qaytarildi')}
function udWrap(name,label){const o=window[name];if(typeof o!=='function'||o.__ud)return;const w=function(){const sn=JSON.stringify(S);const r=o.apply(this,arguments);try{if(JSON.stringify(S)!==sn)udShow(label,sn)}catch(e){}return r};w.__ud=1;window[name]=w}
[['tqDel','Takror yozuvi o‘chirildi'],['nkDel','Shartnoma o‘chirildi'],['nxDel','Tajriba o‘chirildi'],['kmDel','Ko‘rsatkich o‘chirildi'],['edl','Reja o‘chirildi'],['ibDel','Yozuv o‘chirildi'],['ttRem','Vaqt yozuvi o‘chirildi'],['sxDel','Uyqu yozuvi o‘chirildi'],['dm','Yozuv o‘chirildi'],['dDel','Qarz yozuvi o‘chirildi'],['sgDel','Maqsad o‘chirildi'],['dg','Maqsad o‘chirildi'],['rwItemDel','Mukofot o‘chirildi'],['delH','Odat o‘chirildi'],['wDel','Insho o‘chirildi'],['sbDel','Fan o‘chirildi'],['mdDel','Rejim o‘chirildi'],['ktDel','Kitob o‘chirildi'],['exDel','Mashq o‘chirildi'],['apDel','AI reja o‘chirildi'],['ieMatDel','Material o‘chirildi'],['rcDel','Takroriy yozuv o‘chirildi'],['hbArcDel','Odat o‘chirildi'],['klxDel','Xat o‘chirildi'],['slpDel','Uyqu yozuvi o‘chirildi'],['jdApply','Tartib o‘zgardi'],['agApply','Vazifalar joylandi'],['bzApply','Qayta joylandi']].forEach(([n,l])=>udWrap(n,l));
// ----- 🔍 qidiruv endi yangi ma'lumotlarni ham topadi -----
function srExtra(){const out=[];try{const t=tqS();Object.keys(t.d).sort().reverse().slice(0,60).forEach(k=>t.d[k].forEach(e=>out.push({t:e.t,x:dU(k),k:e.w==='n'?'🕌 Namozda takror':'📖 Takror',f:()=>{tab='q';QT='t';TKV='k';TQT=e.w==='n'?'n':'k';TQSEL=k;TQO.t=1;render()}})))}catch(e){}
  try{kmS().forEach(m=>out.push({t:m.t,x:'ko‘rsatkich',k:'🧮 Ko‘rsatkich',f:()=>{tab='m';MQV='n';render()}}))}catch(e){}
  try{const n=S.nf||{};(n.c||[]).forEach(c=>out.push({t:NKM[c.m]?NKM[c.m][1]:'Shartnoma',x:'nafs shartnomasi',k:'🤝 Shartnoma',f:()=>{tab='m';MQV='n';render()}}));(n.x||[]).forEach(x=>out.push({t:x.t,x:x.a+' / '+x.b,k:'🧪 Tajriba',f:()=>{tab='m';MQV='n';render()}}))}catch(e){}
  try{ibL().forEach(x=>out.push({t:x.t,x:dU(x.d),k:'📥 Tezkor yozuv',f:()=>{tab='m';MQV='k';render()}}))}catch(e){}
  try{const r=(S.rt&&S.rt.d)||{};Object.keys(r).sort().reverse().slice(0,30).forEach(k=>Object.keys(r[k]).forEach(id=>{const x=r[k][id];if(x&&x.q)out.push({t:x.q,x:(x.t||'')+' · '+dU(k),k:'🎯 Marosim',f:()=>{tab='h';BV='j';VD=k===dk()?null:k;render()}})}))}catch(e){}
  try{bl().filter(b=>b.on).forEach(b=>out.push({t:b.t,x:'bir kunlik reja · '+dU(b.on),k:'📍 Reja',f:()=>{tab='h';BV='j';VD=b.on===dk()?null:b.on;render()}}))}catch(e){}
  return out}
{const o=window.srAll;if(typeof o==='function'&&!o.__x){const w=function(){return o.apply(this,arguments).concat(srExtra())};w.__x=1;window.srAll=w}}
// ----- ⚙️ sozlamalar ichida qidiruv -----
let SDQ='';
function szQ(v){SDQ=v;render();setTimeout(()=>{const e=document.getElementById('szq');if(e){e.focus();try{e.setSelectionRange(v.length,v.length)}catch(x){}}},0)}
function szAll(open){if(!open)SDO={};render();if(!open)document.querySelectorAll('#app details.sd').forEach(d=>{d.open=false})}
const szBar=()=>`<div class="in" style="margin:10px 0 4px"><input id="szq" type="search" placeholder="🔍 Sozlamalardan qidirish…" value="${esc(SDQ)}" oninput="szQ(this.value)" aria-label="Sozlamalarda qidirish"><button class="btn s" onclick="szAll(false)" aria-label="Hammasini yig‘ish">Yig‘ish</button></div>`;
{const o=window.sozlama;if(typeof o==='function'&&!o.__x){const w=function(){const h=o.apply(this,arguments),m=h.match(/^\s*<div class="top">[\s\S]*?<\/div>/);const q=sn(SDQ).trim();let body=m?h.replace(m[0],m[0]+szBar()):szBar()+h;if(q&&!/<details class="sd"/.test(body))body+='<p class="mu" style="margin:12px 0">Hech narsa topilmadi: boshqa so‘z yozib ko‘ring.</p>';return body};w.__x=1;window.sozlama=w}}
// ----- 🪄 Jilo va qulaylik sozlamalari -----
function jlOpt(k,v){uiS(k,v);render()}
const jlSeg=(k,def,opts)=>`<div class="seg" style="margin-bottom:10px">${opts.map(([v,l])=>`<button class="${(uiG(k)||def)===v?'on':''}" onclick="jlOpt('${k}','${v}')">${l}</button>`).join('')}</div>`;
function jlCard(){return `<p class="mu" style="margin:0 0 8px;font-size:13px">Yangi qulayliklarni xohlasang oldingi holatiga qaytarasan.</p>
  <p class="mu" style="margin:6px 0 4px;font-size:12px"><b>Sana ko‘rinishi</b></p>${jlSeg('trk_dfmt','u',[['u','9-noyabr'],['i','2026-11-09']])}
  <p class="mu" style="margin:6px 0 4px;font-size:12px"><b>Bekor qilish tugmasi</b> (o‘chirilganda 8 soniya chiqadi)</p>${jlSeg('trk_ud','1',[['1','Yoqilgan'],['0','O‘chirilgan']])}
  <p class="mu" style="margin:6px 0 4px;font-size:12px"><b>Sabqi/Manzil va pora takrori</b></p>${jlSeg('trk_tqrd','a',[['a','Alohida sanaladi'],['q','O‘qish hisobiga ham qo‘shilsin (avvalgidek)']])}
  <p class="mu" style="margin:6px 0 4px;font-size:12px"><b>Surish maslahati</b></p><button class="btn s" onclick="uiS('trk_swh','0');toast('Maslahat Bugun jadvalida yana chiqadi');render()">Qayta ko‘rsatish</button>${jlCard2()}${jlCard3()}${jlCard4()}${jlCard5()}${jlCard6()}${jlCard7()}${jlCard8()}${jlCard9()}${jlCard10()}${jlCard11()}${jlCard12()}${jlCard13()}`}
// ----- 💡 surish maslahati (bir marta) -----
const swHint=()=>uiG('trk_swh')==='1'?'':`<div class="row" style="cursor:default;margin:6px 0"><span class="t">💡 <b>Surish:</b> jadval qatorini <b>o‘ngga</b> sursang “bajarildi”, <b>chapga</b> sursang “o‘tkazildi” (sababini so‘raydi).</span><button class="x" onclick="uiS('trk_swh','1');render()" aria-label="Yopish">✕</button></div>`;
// ----- 🧪 tizim tekshiruvi (telefonning o'zida) -----
async function tsRun(){const R=[],add=(n,ok,d)=>R.push({n,ok,d:d||''});
  try{localStorage.setItem('trk_selftest','1');add('Xotira (localStorage) ishlaydi',localStorage.getItem('trk_selftest')==='1');localStorage.removeItem('trk_selftest')}catch(e){add('Xotira (localStorage) ishlaydi',false,String(e&&e.message||e))}
  try{await new Promise((res,rej)=>{const r=indexedDB.open('trk-selftest',1);r.onsuccess=()=>{r.result.close();indexedDB.deleteDatabase('trk-selftest');res()};r.onerror=()=>rej(r.error)});add('Katta xotira (IndexedDB) ishlaydi: zaxira nusxalari uchun',true)}catch(e){add('Katta xotira (IndexedDB) ishlaydi: zaxira nusxalari uchun',false,String(e&&e.message||e))}
  add('Oflayn rejim (service worker) mavjud','serviceWorker' in navigator);
  add('Ulashish (Share) mavjud',typeof navigator.share==='function','bo‘lmasa nusxalash ishlatiladi');
  add('Nusxalash (clipboard) mavjud',!!(navigator.clipboard&&navigator.clipboard.writeText));
  add('Bildirishnoma ruxsati',typeof Notification!=='undefined'&&Notification.permission==='granted',typeof Notification==='undefined'?'brauzerda yo‘q (iPhone’da ilova “Bosh ekran”ga qo‘shilgan bo‘lishi kerak)':'holat: '+Notification.permission);
  let sa=false;try{sa=matchMedia('(display-mode: standalone)').matches||navigator.standalone===true}catch(e){}add('Ilova “Bosh ekran”dan ochilgan (PWA)',sa,sa?'':'brauzer ichida ochilgan');
  add('Surish (pointer events) mavjud',typeof PointerEvent!=='undefined');
  try{const f=new Intl.DateTimeFormat('en-u-ca-islamic-umalqura',{day:'numeric'}).format(new Date());add('Hijriy kalendar ishlaydi (Ro‘za, nasihatchi)',!!f)}catch(e){add('Hijriy kalendar ishlaydi (Ro‘za, nasihatchi)',false)}
  let vo=0;try{vo=speechSynthesis.getVoices().length}catch(e){}add('Ovozli o‘qish (qurilma ovozlari)',vo>0,vo?vo+' ta ovoz':'ovoz topilmadi (ovozli brifing ishlamaydi)');
  let er=0;try{er=window.errLog?errLog.list().length:0}catch(e){}add('Yozilgan xatolar yo‘q',er===0,er?er+' ta xato yozilgan':'');
  let sz=0;try{sz=Math.round(JSON.stringify(S).length/1024)}catch(e){}add('Ma’lumot hajmi me’yorda',sz<2000,sz+' KB');
  let cl=false;try{cl=Math.abs(Date.now()-new Date(dk()+'T12:00').getTime())<36*3600e3}catch(e){}add('Soat va sana to‘g‘ri',cl);
  TS_R=R;render()}
let TS_R=null;
function tsCard(){const R=TS_R;return `<div style="margin-top:12px"><button class="btn" style="width:100%" onclick="tsRun()">🧪 Tizim tekshiruvi (shu telefonda)</button>${R?`<div style="margin-top:8px">${R.map(x=>`<p style="margin:4px 0;font-size:13px">${x.ok?'✅':'⚠️'} ${esc(x.n)}${x.d?' <small class="mu">· '+esc(x.d)+'</small>':''}</p>`).join('')}<p class="mu" style="margin:6px 0 0;font-size:12px">${R.filter(x=>!x.ok).length} ta ogohlantirish. Natija hisobotga ham qo‘shiladi.</p></div>`:''}</div>`}
