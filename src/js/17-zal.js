// ================= ZAL: reja, abonement, mashqlar kutubxonasi, ovqat (AI) =================
const ZP=[['gym','🏋️','Zal'],['home','🏠','Uy'],['out','🌳','Ko‘cha'],['rest','😴','Dam']];
const ZMG=['Ko‘krak','Orqa','Yelka','Qo‘l','Oyoq','Press','Kardio','Boshqa'];
let ZV='r',ZGs='Ko‘krak',PLD=new Date().getDay(),ZWK=null,ZRTm=null,FDI='',FDR=null,FDL=false,FDM='Tushlik',FDT='';
const zEx=id=>S.gym.ex.find(x=>x.id===id);
function zal(){
  const seg=[['r','🏋️ Reja'],['a','🎟 Abonement'],['m','📚 Mashqlar'],['o','🍽 Ovqat'],['j','📝 Jurnal']].map(x=>`<button class="${ZV===x[0]?'on':''}" onclick="ZV='${x[0]}';render()">${x[1]}</button>`).join('');
  return `<div class="seg sc" style="margin-top:0">${seg}</div>${ZV==='r'?zReja():ZV==='a'?zPass():ZV==='m'?zLib():ZV==='o'?zFood():zalOld()}`}
const exTh=e=>e.m?`<span class="exw ${e.m.k==='video'?'vd':''}" onclick="exView('${e.id}')">${e.m.th?`<img class="exth" src="${e.m.th}">`:`<span class="exth">${e.m.k==='video'?'🎬':'🖼'}</span>`}</span>`:'';

// ---- Mashqlar kutubxonasi (rasm/video bilan) ----
function exThumb2(f,kind){return new Promise((res,rej)=>{const u=URL.createObjectURL(f);
  const fin=(src,w,h)=>{const s=Math.min(1,160/Math.max(w,h)),c=document.createElement('canvas');c.width=Math.round(w*s);c.height=Math.round(h*s);c.getContext('2d').drawImage(src,0,0,c.width,c.height);URL.revokeObjectURL(u);res(c.toDataURL('image/jpeg',.6))};
  if(kind==='image'){const i=new Image();i.onload=()=>fin(i,i.width,i.height);i.onerror=()=>{URL.revokeObjectURL(u);rej()};i.src=u}
  else{const v=document.createElement('video');v.muted=true;v.playsInline=true;v.preload='metadata';let dn=0;const to=setTimeout(()=>{if(!dn){dn=1;URL.revokeObjectURL(u);rej()}},4000);
    v.onloadeddata=()=>{try{v.currentTime=Math.min(0.5,(v.duration||1)/2)}catch(e){}};v.onseeked=()=>{if(!dn){dn=1;clearTimeout(to);fin(v,v.videoWidth,v.videoHeight)}};v.onerror=()=>{if(!dn){dn=1;URL.revokeObjectURL(u);rej()}};v.src=u}})}
async function exMedia(f,id){const e=zEx(id);if(!e||!f)return;
  if(f.size>50*1024*1024){alert('Fayl 50 MB dan katta. Qisqaroq video tanlang.');return}
  const kind=(f.type||'').startsWith('video')?'video':'image';let th=null;try{th=await exThumb2(f,kind)}catch(x){}
  try{await idbSet('x'+id,{b:await f.arrayBuffer(),t:f.type})}catch(x){alert('Qurilmada saqlab bo‘lmadi.');return}
  e.m={k:kind,t:f.type,th,sz:f.size};save();if(sb&&UID){if(cloudOk(f.size))exUp(e,f);else toast('Bulut limiti to‘ldi: fayl faqat shu telefonda saqlandi')}}
async function exUp(e,f){PUPL['x'+e.id]=1;render();
  try{const r=await sb.storage.from('books').upload(UID+'/x/'+e.id,f,{upsert:true,contentType:f.type||'application/octet-stream'});if(r.error)throw r.error;e.m.cloud=1;save()}catch(x){toast('Bulutga yuklanmadi: '+(x.message||x))}
  delete PUPL['x'+e.id];render()}
function exPick(inp,id){const f=inp.files&&inp.files[0];if(f)exMedia(f,id);inp.value=''}
async function exView(id){const e=zEx(id);if(!e||!e.m)return;let rec=null;try{rec=await idbGet('x'+id)}catch(x){}
  if(!rec&&e.m.cloud&&sb&&UID){toast('Yuklab olinmoqda...');const r=await sb.storage.from('books').download(UID+'/x/'+id);if(!r.error){const b=await r.data.arrayBuffer();rec={b,t:e.m.t};try{await idbSet('x'+id,rec)}catch(x){}}}
  if(!rec){alert('Bu qurilmada fayl topilmadi. Mashq kartasida qayta yuklang.');return}
  exClose();const url=URL.createObjectURL(new Blob([rec.b],{type:rec.t||(e.m.k==='video'?'video/mp4':'image/jpeg')}));
  const d=document.createElement('div');d.id='xv';d.className='rdo';d.style.zIndex=120;
  d.innerHTML=`<div class="rdt"><button class="x" style="font-size:22px" onclick="exClose()">✕</button><b style="flex:1">${esc(e.n)}</b></div><div class="rdc" style="display:flex;align-items:center;justify-content:center;background:#000">${e.m.k==='video'?`<video src="${url}" controls autoplay playsinline loop style="max-width:100%;max-height:100%"></video>`:`<img src="${url}" style="max-width:100%;max-height:100%">`}</div>`;
  d._u=url;document.body.appendChild(d)}
function exClose(){const d=document.getElementById('xv');if(d){try{URL.revokeObjectURL(d._u)}catch(e){}d.remove()}}
async function exAdd(){const n=V('exn');if(!n)return alert('Mashq nomini yozing.');const f=($('#exf')&&$('#exf').files&&$('#exf').files[0])||null;
  const e={id:'e'+Date.now(),n,g:ZGs,s:Math.round(+V('exs'))||3,r:Math.round(+V('exr'))||10,w:+V('exw')||0,note:V('exo'),m:null};S.gym.ex.push(e);save();if(f)await exMedia(f,e.id)}
function exDel(id){if(!confirm('Mashq kutubxonadan o‘chirilsinmi?'))return;S.gym.ex=S.gym.ex.filter(x=>x.id!==id);Object.values(S.gym.plan).forEach(p=>{p.ex=p.ex.filter(x=>x.id!==id)});idbDel('x'+id).catch(()=>{});if(sb&&UID)sb.storage.from('books').remove([UID+'/x/'+id]).catch(()=>{});save()}
function zLib(){
  const g=ZMG.map(x=>`<button class="${ZGs===x?'on':''}" onclick="ZGs='${x}';render()">${x}</button>`).join('');
  const L=S.gym.ex.slice().sort((a,b)=>a.g>b.g?1:-1).map(e=>`<div class="goal"><div class="h" style="align-items:flex-start"><div style="display:flex;gap:10px;align-items:center">${exTh(e)}<div><b>${esc(e.n)}</b><div class="mu" style="font-size:12px">${esc(e.g)}, ${e.s}×${e.r}${e.w?', '+e.w+' kg':''}</div></div></div><button class="x" onclick="exDel('${e.id}')">×</button></div>${e.note?`<p class="mu" style="margin:6px 0 0;font-size:13px">${esc(e.note)}</p>`:''}
    <div class="mu" style="font-size:12px;margin-top:6px">${PUPL['x'+e.id]?'Bulutga yuklanmoqda…':e.m?(e.m.cloud?'Bulutda saqlangan':'Faqat shu telefonda'):'Rasm yoki video yo‘q'}</div>
    <label class="btn s" style="display:block;text-align:center;margin-top:8px;cursor:pointer;padding:8px">${e.m?'Videoni/rasmni almashtirish':'🎬 Video yoki rasm qo‘shish'}<input type="file" accept="video/*,image/*" style="display:none" onchange="exPick(this,'${e.id}')"></label></div>`).join('');
  return `<p class="mu" style="margin:0 0 8px">Mashqlaringni bir marta yoz, videosini yoki rasmini yukla. Keyin haftalik rejaga qo‘shib, har safar shu yerdan ko‘rib bajarasan.</p>
  <div class="goal"><b>Yangi mashq</b><div class="in" style="margin-top:8px"><input id="exn" placeholder="Nomi, masalan: Bench press"></div><div class="chips">${g}</div>
  <div class="fg3"><label><span class="mu">Set</span><input id="exs" type="number" inputmode="numeric" value="3"></label><label><span class="mu">Takror</span><input id="exr" type="number" inputmode="numeric" value="10"></label><label><span class="mu">Vazn, kg</span><input id="exw" type="number" inputmode="decimal" placeholder="0"></label></div>
  <div class="in"><input id="exo" placeholder="Izoh (texnika, eslatma)"></div>
  <label class="btn s" style="display:block;text-align:center;cursor:pointer;margin-bottom:8px">🎬 Video yoki rasm tanlash (ixtiyoriy)<input id="exf" type="file" accept="video/*,image/*" style="display:none" onchange="toast('Fayl tanlandi')"></label><button class="btn" style="width:100%" onclick="exAdd()">Mashqni saqlash</button></div>
  ${cloudBar()}<h2>Kutubxona (${S.gym.ex.length})</h2>${L||'<p class="mu">Hali mashq yo‘q.</p>'}`}

// ---- Haftalik reja ----
const zPl=d=>S.gym.plan[d]||(S.gym.plan[d]={place:'gym',ex:[]});
function plPlace(d,p){zPl(d).place=p;save()}
function plAdd(d){const id=V('pls');const e=zEx(id);if(!e)return alert('Avval Mashqlar bo‘limida mashq yarating.');zPl(d).ex.push({id,s:e.s,r:e.r,w:e.w});save()}
function plRm(d,i){zPl(d).ex.splice(i,1);save()}
function plSet(d,i,f,v){zPl(d).ex[i][f]=+v||0;save()}
function zRest(sec){if(ZRTm&&ZRTm.iv)clearInterval(ZRTm.iv);ZRTm={end:Date.now()+sec*1000};ZRTm.iv=setInterval(()=>{const l=Math.max(0,Math.ceil((ZRTm.end-Date.now())/1000)),e=document.getElementById('zrt');if(e)e.textContent=fmtT(l);if(l<=0){clearInterval(ZRTm.iv);ZRTm=null;if(navigator.vibrate)navigator.vibrate([250,120,250]);render()}},500)}
function zwStart(){const P=S.gym.plan[new Date().getDay()];if(!P||!P.ex.length)return;ZWK={d:dk(),place:P.place,items:P.ex.map(x=>{const e=zEx(x.id)||{n:'Mashq'};return{id:x.id,n:e.n,s:x.s,r:x.r,w:x.w,done:[]}})};render()}
function zwTick(i,j){const it=ZWK.items[i],k=it.done.indexOf(j);if(k<0){it.done.push(j);zRest(90)}else it.done.splice(k,1);render()}
function zwCancel(){if(confirm('Mashg‘ulot bekor qilinsinmi?')){if(ZRTm&&ZRTm.iv)clearInterval(ZRTm.iv);ZRTm=null;ZWK=null;render()}}
function zwEnd(){const Z=ZWK,n=Z.items.filter(it=>it.done.length);if(!n.length){alert('Hech bir set belgilanmadi.');return}
  n.forEach((it,i)=>S.gym.log.push({id:Date.now()+i,d:Z.d,n:it.n,s:it.done.length,r:it.r,w:it.w||0}));
  const P=S.gym.pass;if(P&&Z.d>=P.s&&Z.d<=P.e&&Z.place==='gym')P.v[Z.d]='d';
  if(ZRTm&&ZRTm.iv)clearInterval(ZRTm.iv);ZRTm=null;ZWK=null;toast('Mashg‘ulot saqlandi 💪');confetti();save()}
function zReja(){
  if(ZWK){const Z=ZWK,tl=ZRTm?Math.max(0,Math.ceil((ZRTm.end-Date.now())/1000)):0,total=Z.items.reduce((a,it)=>a+it.s,0),dn=Z.items.reduce((a,it)=>a+it.done.length,0);
    return `<section class="hero"><p class="lab">Mashg‘ulot davom etmoqda</p><h1 style="font-size:34px">${dn} / ${total} set</h1><div class="bar" style="margin:8px 0"><i style="width:${total?dn/total*100:0}%"></i></div>${ZRTm?`<p class="mu" style="margin:0">Dam olish</p><div class="tmr" id="zrt" style="margin:0">${fmtT(tl)}</div>`:'<p class="mu">Set tugagach tugmani bos, dam olish taymeri o‘zi ishga tushadi.</p>'}</section>
    ${Z.items.map((it,i)=>{const e=zEx(it.id);return `<div class="goal"><div class="h"><div class="exr">${e?exTh(e):''}<b>${esc(it.n)}</b></div><span class="mu">${it.r} marta${it.w?', '+it.w+' kg':''}</span></div><div class="in" style="margin:8px 0 0;flex-wrap:wrap">${Array.from({length:it.s},(_,j)=>`<button class="btn ${it.done.includes(j)?'':'s'}" style="min-width:52px" onclick="zwTick(${i},${j})">${it.done.includes(j)?'✓':''} ${j+1}</button>`).join('')}</div></div>`}).join('')}
    <div class="in"><button class="big" style="margin:0" onclick="zwEnd()">Yakunlash va saqlash</button></div><button class="ghost" onclick="zwCancel()">Bekor qilish</button>`}
  const d=PLD,P=zPl(d),T0=new Date().getDay(),wk=[1,2,3,4,5,6,0];
  const strip=wk.map(x=>{const p=S.gym.plan[x],pl=p&&ZP.find(z=>z[0]===p.place);return `<button class="${x===d?'on':''}" onclick="PLD=${x};render()"><span style="display:block;font-size:11px;font-weight:600">${DAYS[x].slice(0,2)}${x===T0?' •':''}</span>${pl?pl[1]:'➕'}</button>`}).join('');
  const n=wk.filter(x=>{const p=S.gym.plan[x];return p&&p.place!=='rest'&&p.ex.length}).length;
  const rows=P.ex.map((x,i)=>{const e=zEx(x.id);if(!e)return '';return `<div class="goal"><div class="h"><div class="exr">${exTh(e)}<b>${esc(e.n)}</b></div><button class="x" onclick="plRm(${d},${i})">×</button></div><div class="in" style="margin:8px 0 0"><input type="number" inputmode="numeric" value="${x.s}" onchange="plSet(${d},${i},'s',this.value)"><span class="mu" style="align-self:center">set ×</span><input type="number" inputmode="numeric" value="${x.r}" onchange="plSet(${d},${i},'r',this.value)"><span class="mu" style="align-self:center">marta</span><input type="number" inputmode="decimal" placeholder="kg" value="${x.w||''}" onchange="plSet(${d},${i},'w',this.value)"></div></div>`}).join('');
  const opts=S.gym.ex.map(e=>`<option value="${e.id}">${esc(e.n)} (${esc(e.g)})</option>`).join('');
  return `<section class="hero"><p class="lab">Haftalik reja</p><h1 style="font-size:30px">Haftada ${n} kun</h1><p class="mu">Qaysi kuni qayerda va qaysi mashqlarni qilishingni belgila.</p></section>
  <div class="wkp" style="margin-top:12px">${strip}</div><h2>${DAYS[d]}${d===T0?' (bugun)':''}</h2>
  <div class="chips">${ZP.map(z=>`<button class="${P.place===z[0]?'on':''}" onclick="plPlace(${d},'${z[0]}')">${z[1]} ${z[2]}</button>`).join('')}</div>
  ${P.place==='rest'?'<p class="mu">Dam olish kuni. Tiklanish ham mashqning bir qismi.</p>':`${rows||'<p class="mu">Bu kunga mashq qo‘shilmagan.</p>'}${S.gym.ex.length?`<div class="in"><select id="pls">${opts}</select><button class="btn" onclick="plAdd(${d})">Qo‘sh</button></div>`:'<p class="mu">Avval 📚 Mashqlar bo‘limida mashqlaringni yarat.</p>'}`}
  ${d===T0&&P.place!=='rest'&&P.ex.length?'<button class="big" onclick="zwStart()">▶ Bugungi mashg‘ulotni boshlash</button>':''}`}

// ---- Abonement (masalan: 1 oyda 12 ta kirish) ----
const nxtDay=k=>{const d=new Date(k+'T12:00');d.setDate(d.getDate()+1);return d.toLocaleDateString('sv')};
function psNew(){const s=V('pss'),e=V('pse'),t=Math.round(+V('pst')),n=V('psn');if(!s||!e||!t)return alert('Boshlanish, tugash sanasi va kirishlar sonini yozing.');if(e<s)return alert('Tugash sanasi boshlanishdan keyin bo‘lsin.');
  if(S.gym.pass)S.gym.past.push(S.gym.pass);S.gym.pass={n,s,e,t,v:{}};save()}
function psV(k){const v=S.gym.pass.v,c=v[k],nx={undefined:'p',p:'d',d:'m',m:undefined}[c];if(nx)v[k]=nx;else delete v[k];save()}
function psAuto(){const P=S.gym.pass,T0=dk();Object.keys(P.v).forEach(k=>{if(P.v[k]==='p'&&k>=T0)delete P.v[k]});
  const done=Object.values(P.v).filter(x=>x==='d').length,rem=P.t-done,days=[];for(let k=T0>P.s?T0:P.s;k<=P.e;k=nxtDay(k))if(!P.v[k])days.push(k);
  if(rem<=0||!days.length){save();return}const n=Math.min(rem,days.length);for(let i=0;i<n;i++)P.v[days[Math.floor((i+0.5)*days.length/n)]]='p';save()}
function psEnd(){if(confirm('Abonement tugatilsinmi? U tarixga o‘tadi.')){S.gym.past.push(S.gym.pass);S.gym.pass=null;save()}}
function psStat(){const P=S.gym.pass;if(!P)return null;const T0=dk(),vs=Object.values(P.v),done=vs.filter(x=>x==='d').length,miss=vs.filter(x=>x==='m').length,
  plan=Object.keys(P.v).filter(k=>P.v[k]==='p'&&k>=T0).length,rem=Math.max(0,P.t-done),over=T0>P.e,from=T0<P.s?P.s:T0,days=over?0:dl(P.e)-dl(from)+1,burn=Math.max(0,rem-days);
  return{done,miss,plan,rem,days,burn,perWeek:days?r1(rem/(days/7)):0,over,total:dl(P.e)-dl(P.s)+1}}
function psToday(){const P=S.gym.pass,k=dk();if(k<P.s||k>P.e){alert('Bugun abonement muddatida emas.');return}
  if(P.v[k]==='d')delete P.v[k];else{P.v[k]='d';const st=psStat();if(st.done>=P.t){confetti();toast('Abonement to‘liq bajarildi! 🎉')}else toast('Barakalla! 💪 Yana '+st.rem+' ta qoldi')}save()}
function psEd(f,v){const P=S.gym.pass;if(f==='n')P.n=String(v).trim();else if(f==='t'){const n=Math.round(+v);if(n>0)P.t=n}else if(f==='e'){if(v&&v>=P.s)P.e=v;else alert('Tugash sanasi boshlanishdan keyin bo‘lsin.')}save()}
function psSet(id,v){const e=$('#'+id);if(e)e.value=v}
function psPre(m){const s=V('pss')||dk(),d=new Date(s+'T12:00');d.setMonth(d.getMonth()+m);d.setDate(d.getDate()-1);psSet('pse',d.toLocaleDateString('sv'))}
const dShort=k=>+k.slice(8)+' '+MON[+k.slice(5,7)-1].slice(0,3);
function psForm(first){
  return `<div class="goal" style="padding:16px"><b style="font:700 18px Fraunces,serif">${first?'Abonementni kiriting':'Yangi abonement'}</b>
  <div class="in" style="margin-top:10px"><input id="psn" placeholder="Zal nomi (ixtiyoriy)"></div>
  <div class="fg1"><label><span class="mu">Boshlanish</span><input id="pss" type="date" value="${dk()}"></label><label><span class="mu">Tugash</span><input id="pse" type="date"></label></div>
  <div class="chips" style="margin-top:8px"><button onclick="psPre(1)">+1 oy</button><button onclick="psPre(2)">+2 oy</button><button onclick="psPre(3)">+3 oy</button></div>
  <label style="display:block"><span class="mu">Jami kirishlar soni</span><input id="pst" type="number" inputmode="numeric" placeholder="masalan, 12" style="width:100%;margin-top:4px"></label>
  <div class="chips" style="margin-top:8px">${[8,12,16,20,30].map(n=>`<button onclick="psSet('pst',${n})">${n} ta</button>`).join('')}</div>
  <button class="big" style="margin:8px 0 0" onclick="psNew()">Abonementni boshlash</button></div>`}
function zPass(){
  const P=S.gym.pass;
  if(!P)return `<div class="tk" style="text-align:center"><div style="font-size:54px">🎟</div><h2 class="tk-n" style="margin:6px 0">Abonementni kuzatib bor</h2><p class="mu" style="margin:0 auto;max-width:300px">Boshlanish va tugash sanasini hamda kirishlar sonini yoz. Ilova yetib borishingni kuzatadi va kuyib ketmasligi uchun eslatadi.</p></div><div style="margin-top:12px">${psForm(true)}</div>${psPast()}`;
  const st=psStat(),T0=dk(),pct=P.t?Math.min(1,st.done/P.t):0,C=2*Math.PI*42;
  const plans=Object.keys(P.v).filter(k=>P.v[k]==='p'&&k>=T0).sort(),nxt=plans[0];
  const inPass=T0>=P.s&&T0<=P.e,td=P.v[T0];
  // holat banneri
  const need=st.days?st.rem/st.days:0;
  const bn=st.rem===0?['ok','🎉 Hammasi bajarildi. Barakalla!']
    :st.over?['bd','Muddat tugadi: '+st.rem+' ta kirish ishlatilmay kuyib ketdi.']
    :st.burn>0?['bd','⚠️ '+st.rem+' ta kirish qoldi, lekin atigi '+st.days+' kun bor. Har kuni borsang ham '+st.burn+' tasi kuyadi.']
    :need>0.6?['wr','Tezroq kerak: haftasiga taxminan '+st.perWeek+' marta borish lozim.']
    :['ok','Tempdasan. Haftasiga taxminan '+st.perWeek+' marta borsang yetadi.'];
  // muhr kartasi
  const cols=P.t<=12?6:P.t<=24?8:10;
  const stamps=Array.from({length:P.t},(_,i)=>{const c=i<st.done?'d':(st.burn>0&&i>=P.t-st.burn)?'b':(i-st.done<st.plan)?'p':'';return `<div class="${c}">${c==='d'?'✓':c==='b'?'🔥':i+1}</div>`}).join('');
  // kalendar (dushanbadan boshlab)
  const first=(new Date(P.s+'T12:00').getDay()+6)%7,cells=[];for(let k=P.s,n=0;k<=P.e&&n<120;k=nxtDay(k),n++)cells.push(k);
  const cal=['Du','Se','Ch','Pa','Ju','Sh','Ya'].map(x=>`<span class="w">${x}</span>`).join('')+Array(first).fill('<i></i>').join('')+cells.map(k=>{const s=P.v[k],mTag=(+k.slice(8)===1||k===P.s)?`<em>${MON[+k.slice(5,7)-1].slice(0,3)}</em>`:'';
    return `<div class="c ${s||''} ${k<T0&&!s?'past':''} ${k===T0?'t':''} ${mTag?'mm':''}" onclick="psV('${k}')">${mTag}${+k.slice(8)}${s==='d'?'<small>✓</small>':s==='m'?'<small>✗</small>':s==='p'?'<small>•</small>':''}</div>`}).join('');
  return `<div class="tk"><div class="tk-h"><div style="min-width:0"><p class="lab">🎟 ABONEMENT</p><h2 class="tk-n">${esc(P.n||'Zal abonementi')}</h2><p class="mu">${dShort(P.s)} → ${dShort(P.e)}, ${st.total} kun</p></div>
    <div class="tk-r"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,.16)" stroke-width="9"/><circle cx="50" cy="50" r="42" fill="none" stroke="${st.burn>0?'#f0a090':'#e2b857'}" stroke-width="9" stroke-linecap="round" stroke-dasharray="${(C*pct).toFixed(1)} ${C.toFixed(1)}"/></svg><b><span>${st.done}<small>/ ${P.t}</small></span></b></div></div>
    <div class="tk-cut"></div>
    <div class="tk-s"><div><b>${st.rem}</b><span>qolgan kirish</span></div><div><b>${st.over?0:st.days}</b><span>qolgan kun</span></div><div><b>${st.rem?st.perWeek:'0'}</b><span>haftasiga</span></div></div></div>
  <div class="bn ${bn[0]}">${bn[1]}</div>
  ${inPass?(td==='d'?`<button class="btn s" style="width:100%;margin-top:10px;padding:14px" onclick="psToday()">✓ Bugun bordim, bekor qilish</button>`:`<button class="big" style="margin:10px 0 0" onclick="psToday()">✅ Bugun bordim</button>`):''}
  ${nxt?`<p class="mu" style="margin:10px 2px 0">Keyingi reja: <b style="color:var(--tx)">${DAYS[new Date(nxt+'T12:00').getDay()]}, ${dShort(nxt)}</b>${plans.length>1?' (yana '+(plans.length-1)+' ta)':''}</p>`:''}
  <h2>Muhr kartasi</h2><div class="stp" style="grid-template-columns:repeat(${cols},minmax(0,1fr))">${stamps}</div>
  <div class="lg"><span style="--c:var(--ac)">bordim</span><span style="--c:var(--go)">rejalashtirilgan</span>${st.burn>0?'<span style="--c:var(--bad)">kuyadi</span>':''}<span style="--c:var(--ln)">qolgan</span></div>
  <h2>Kalendar</h2><div class="goal" style="padding:12px 10px"><div class="cal">${cal}</div>
  <div class="lg" style="justify-content:center"><span style="--c:var(--go)">kunni bossang: rejalashtirish</span><span style="--c:var(--ac)">bordim</span><span style="--c:var(--bad)">bormadim</span></div></div>
  <div class="in" style="margin-top:10px"><button class="btn" style="flex:1" onclick="psAuto()">✨ Mos kunlarni rejalashtir</button></div>
  <details class="goal" style="margin-top:6px"><summary style="font-weight:600">Sozlamalar</summary>
    <div style="margin-top:8px"><label style="display:block"><span class="mu">Zal nomi</span><input type="text" style="width:100%;margin-top:4px" value="${esc(P.n||'')}" onchange="psEd('n',this.value)"></label>
    <div class="fg1"><label><span class="mu">Tugash sanasi</span><input type="date" value="${P.e}" onchange="psEd('e',this.value)"></label><label><span class="mu">Jami kirishlar</span><input type="number" inputmode="numeric" value="${P.t}" onchange="psEd('t',this.value)"></label></div>
    <button class="btn s" style="width:100%;margin-top:4px" onclick="psEnd()">Abonementni tugatish (tarixga o‘tadi)</button></div></details>
  <details class="goal" style="margin-top:6px"><summary style="font-weight:600">Yangi abonement boshlash</summary><div style="margin-top:10px">${psForm(false)}</div></details>${psPast()}`}
function psPast(){const A=S.gym.past||[];if(!A.length)return '';
  return `<h2>Oldingi abonementlar</h2>${A.slice().reverse().map(x=>{const d=Object.values(x.v||{}).filter(v=>v==='d').length,l=Math.max(0,x.t-d);return `<div class="row" style="align-items:flex-start"><span class="t"><b>${esc(x.n||'Abonement')}</b><br><span class="mu">${dShort(x.s)} → ${dShort(x.e)}</span></span><span style="text-align:right"><b>${d} / ${x.t}</b><br><span class="mu" style="font-size:12px">${l?l+' ta kuygan':'to‘liq ✓'}</span></span></div>`}).join('')}`}

// ---- Ovqat: AI bilan kaloriya va makrolar ----
const FDMS=['Nonushta','Tushlik','Kechki ovqat','Snack'];
function b64(buf){const u=new Uint8Array(buf);let s='';for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));return btoa(s)}
async function fnAI(body){const d=await fnPost(body,({ielts:95000,vocab:105000,reading:105000,iex:105000})[body.action]||60000);if(!d.text)throw new Error('AI javob bermadi.');aiCount(1,body.action);try{aiQuotaClear()}catch(e){}return d}
function parseJson(t){let s=String(t||'').replace(/```json|```/g,'').trim();const a=s.indexOf('{'),b=s.lastIndexOf('}');if(a<0||b<a)return null;try{return JSON.parse(s.slice(a,b+1))}catch(e){return null}}
function shrink(f,max){return new Promise((res,rej)=>{const img=new Image(),u=URL.createObjectURL(f);img.onload=()=>{const s=Math.min(1,max/Math.max(img.width,img.height)),c=document.createElement('canvas');c.width=Math.round(img.width*s);c.height=Math.round(img.height*s);c.getContext('2d').drawImage(img,0,0,c.width,c.height);URL.revokeObjectURL(u);res(c.toDataURL('image/jpeg',.8).split(',')[1])};img.onerror=()=>{URL.revokeObjectURL(u);rej(new Error('Rasm ochilmadi'))};img.src=u})}
async function fdPic(inp){const f=inp.files&&inp.files[0];inp.value='';if(!f)return;try{FDI=await shrink(f,900);render()}catch(e){alert(e.message)}}
async function fdAI(){const t=V('fdt');if(!t&&!FDI)return alert('Ovqat nomini yozing yoki rasm yuboring.');if(!sb||!UID)return alert('AI uchun hisobga kirgan bo‘lish kerak.');
  FDL=true;FDR=null;render();
  try{const d=await fnAI({action:'food',text:t,image:FDI||undefined,mime:'image/jpeg'}),j=parseJson(d.text);
    if(!j||!Array.isArray(j.items)||!j.items.length)throw new Error((j&&j.note)||'Ovqatni aniqlab bo‘lmadi. Aniqroq yozing yoki boshqa rasm yuboring.');
    FDR={items:j.items.map(x=>({name:String(x.name||'Ovqat'),g:Math.round(+x.grams||0),kcal:Math.round(+x.kcal||0),p:Math.round(+x.p||0),f:Math.round(+x.f||0),c:Math.round(+x.c||0)})),note:String(j.note||''),mul:1};FDI=''}
  catch(e){FDR=null;alert(e.message)}
  FDL=false;render()}
const fdSum=(L,f)=>L.reduce((a,x)=>a+(x[f]||0),0);
function fdAdd(){if(!FDR)return;const k=FDT||dk(),m=FDR.mul,L=S.gym.food.log[k]=S.gym.food.log[k]||[];
  FDR.items.forEach((x,i)=>L.push({id:Date.now()+i,m:FDM,n:x.name,kcal:Math.round(x.kcal*m),p:Math.round(x.p*m),f:Math.round(x.f*m),c:Math.round(x.c*m)}));FDR=null;save()}
function fdRm(i){FDR.items.splice(i,1);if(!FDR.items.length)FDR=null;render()}
function fdDel(id){const k=FDT||dk();S.gym.food.log[k]=(S.gym.food.log[k]||[]).filter(x=>x.id!==id);save()}
function fdMan(){const n=V('fmn'),kc=Math.round(+V('fmk'));if(!n||!kc)return alert('Nomi va kkal kerak.');const k=FDT||dk();(S.gym.food.log[k]=S.gym.food.log[k]||[]).push({id:Date.now(),m:FDM,n,kcal:kc,p:Math.round(+V('fmp'))||0,f:Math.round(+V('fmf'))||0,c:Math.round(+V('fmc'))||0});save()}
function fdGoal(f,v){S.gym.food.goal[f]=Math.max(0,Math.round(+v)||0);save()}
function fdMul(x){FDR.mul=x;render()}
function zFood(){
  const F=S.gym.food,k=FDT||dk(),L=F.log[k]||[],G=F.goal,T={kcal:fdSum(L,'kcal'),p:fdSum(L,'p'),f:fdSum(L,'f'),c:fdSum(L,'c')};
  const bar=(l,v,g,u,col)=>`<div class="skb"><div class="h"><span>${l}</span><span class="mu">${v} / ${g} ${u}</span></div><div class="bar" style="margin-top:6px"><i style="width:${Math.min(100,g?v/g*100:0)}%;background:${v>g?'var(--bad)':col}"></i></div></div>`;
  const meals=FDMS.map(mm=>{const A=L.filter(x=>x.m===mm);return A.length?`<p class="mu" style="margin:12px 0 6px">${mm}, ${fdSum(A,'kcal')} kkal</p>`+A.map(x=>`<div class="row"><span class="t">${esc(x.n)}<br><span class="mu">${x.kcal} kkal, oqsil ${x.p}, yog‘ ${x.f}, uglevod ${x.c}</span></span><button class="x" onclick="fdDel(${x.id})">×</button></div>`).join(''):''}).join('');
  const R=FDR,mul=R?R.mul:1,rt={kcal:R?Math.round(fdSum(R.items,'kcal')*mul):0,p:R?Math.round(fdSum(R.items,'p')*mul):0,f:R?Math.round(fdSum(R.items,'f')*mul):0,c:R?Math.round(fdSum(R.items,'c')*mul):0};
  const res=R?`<div class="goal" style="border:1px solid var(--go)"><b>AI natijasi (taxminiy)</b>${R.items.map((x,i)=>`<div class="row" style="margin-top:6px"><span class="t">${esc(x.name)}${x.g?', '+x.g+' g':''}<br><span class="mu">${x.kcal} kkal, oqsil ${x.p}, yog‘ ${x.f}, uglevod ${x.c}</span></span><button class="x" onclick="fdRm(${i})">×</button></div>`).join('')}
    ${R.note?`<p class="mu" style="margin:8px 0 0;font-size:13px">${esc(R.note)}</p>`:''}<p class="mu" style="margin:10px 0 4px">Porsiya:</p><div class="chips">${[0.5,0.75,1,1.5,2].map(x=>`<button class="${mul===x?'on':''}" onclick="fdMul(${x})">×${x}</button>`).join('')}</div>
    <button class="big" style="margin:8px 0 0" onclick="fdAdd()">Qo‘shish: ${rt.kcal} kkal (${rt.p}/${rt.f}/${rt.c})</button></div>`:'';
  return `<section class="hero"><p class="lab">${k===dk()?'Bugun':k.slice(8)+'.'+k.slice(5,7)}</p><h1 style="font-size:46px">${T.kcal}<span style="font-size:20px;font-weight:600;opacity:.75"> / ${G.kcal} kkal</span></h1><div class="bar" style="margin:8px 0"><i style="width:${Math.min(100,G.kcal?T.kcal/G.kcal*100:0)}%"></i></div><p class="mu">${T.kcal<=G.kcal?(G.kcal-T.kcal)+' kkal qoldi':(T.kcal-G.kcal)+' kkal oshdi'}</p></section>
  <div style="margin-top:10px">${bar('Oqsil',T.p,G.p,'g','var(--ac)')}${bar('Yog‘',T.f,G.f,'g','var(--go)')}${bar('Uglevod',T.c,G.c,'g','#6f9fd8')}</div>
  <div class="in"><input type="date" value="${k}" onchange="FDT=this.value;render()"></div>
  <h2>🍽 AI bilan hisoblash</h2><div class="chips">${FDMS.map(x=>`<button class="${FDM===x?'on':''}" onclick="FDM='${x}';render()">${x}</button>`).join('')}</div>
  <div class="in"><input id="fdt" placeholder="Ovqat nomi, masalan: 300 g osh va non"></div>
  <div class="in"><label class="btn s" style="flex:1;text-align:center;cursor:pointer">📷 Rasm${FDI?' ✓':''}<input type="file" accept="image/*" style="display:none" onchange="fdPic(this)"></label><button class="btn" style="flex:2" onclick="fdAI()">${FDL?'Hisoblanmoqda…':'AI hisoblasin'}</button></div>
  ${FDI?`<img src="data:image/jpeg;base64,${FDI}" style="width:100%;max-height:220px;object-fit:cover;border-radius:14px;margin-bottom:8px">`:''}<p class="mu" style="margin:0 0 8px;font-size:12px">Rasm Google Gemini'ga yuboriladi va saqlanmaydi. Natija taxminiy, aniqlik uchun porsiyani sozla.</p>${res}
  <details style="margin:8px 0"><summary class="mu">Qo‘lda qo‘shish</summary><div class="in" style="margin-top:8px"><input id="fmn" placeholder="Nomi"><input id="fmk" type="number" inputmode="numeric" placeholder="kkal" style="max-width:90px"></div><div class="in"><input id="fmp" type="number" placeholder="Oqsil g"><input id="fmf" type="number" placeholder="Yog‘ g"><input id="fmc" type="number" placeholder="Uglevod g"></div><button class="btn" style="width:100%" onclick="fdMan()">Qo‘shish</button></details>
  <h2>Kunlik ovqatlar</h2>${meals||'<p class="mu">Bu kunga ovqat yozilmagan.</p>'}
  <details style="margin-top:12px"><summary class="mu">Kunlik maqsadlar</summary><div class="in" style="margin-top:8px">${[['kcal','kkal'],['p','oqsil g'],['f','yog‘ g'],['c','uglevod g']].map(([f,l])=>`<div style="flex:1;min-width:0"><span class="mu" style="font-size:11px">${l}</span><input type="number" inputmode="numeric" style="width:100%" value="${G[f]}" onchange="fdGoal('${f}',this.value)"></div>`).join('')}</div></details>`}

