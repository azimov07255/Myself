// ---- Ramazon ----
const HMN=['Muharram','Safar','Rabiul avval','Rabiul oxir','Jumadil avval','Jumadil oxir','Rajab','Sha‘bon','Ramazon','Shavvol','Zulqa‘da','Zulhijja'];
function hijri(d){try{const p=new Intl.DateTimeFormat('en-u-ca-islamic-umalqura',{day:'numeric',month:'numeric',year:'numeric'}).formatToParts(d),g=t=>+p.find(x=>x.type===t).value;return{d:g('day'),m:g('month'),y:g('year')}}catch(e){return null}}
function rzEst(){const t0=new Date();t0.setHours(12,0,0,0);for(let i=-35;i<420;i++){const d=new Date(t0.getTime()+i*864e5),x=hijri(d);if(!x)break;if(x.m===9&&x.d===1)return d.toLocaleDateString('sv')}return '2027-02-08'}
function rzInfo(){const r=S.rz,est=rzEst(),start=r.start&&dl(r.start)>=-31?r.start:est,n=-dl(start)+1;return{start,est,left:dl(start),on:n>=1&&n<=30,n}}
const rzDay=(st,i)=>{const d=new Date(st+'T12:00');d.setDate(d.getDate()+i);return d.toLocaleDateString('sv')};
function fzT(k){if(k>dk())return;const R=S.rz,c=R.fast[k]||0,nx=(c+1)%3;
  if(c===2){R.debt=Math.max(0,R.debt-1);const i=R.log.findIndex(x=>x.d===k&&x.k==='miss');if(i>=0)R.log.splice(i,1)}
  if(nx===2){R.debt++;R.log.push({id:Date.now(),d:k,k:'miss',n:1})}R.fast[k]=nx;save()}
function tvT(k){if(k>dk())return;const R=S.rz;R.tar[k]=R.tar[k]?0:1;save()}
function rzPay(){const R=S.rz;if(!(R.debt>0))return;R.debt--;R.log.push({id:Date.now(),d:dk(),k:'paid',n:1});save()}
function rzAdd(){const n=parseInt(prompt('Nechta qazo ro‘za qo‘shilsin?'),10);if(!(n>0))return;S.rz.debt+=n;S.rz.log.push({id:Date.now(),d:dk(),k:'add',n});save()}
function rzSet(v){S.rz.start=v||'';save()}
function rzLeftTxt(){const t=ptTimes();if(!t)return '';const d=new Date(),n=d.getHours()*60+d.getMinutes();
  if(n<t.Fajr)return 'Saharlik tugashiga '+fmt(t.Fajr-n).trim()+' qoldi';if(n<t.Maghrib)return 'Iftorgacha '+fmt(t.Maghrib-n).trim()+' qoldi';return 'Iftor vaqti o‘tdi. Qabul bo‘lsin.'}
function rzCard(){
  const I=rzInfo(),k=dk();
  if(!I.on&&!(I.left>0&&I.left<=120))return '';
  if(I.on){const t=ptTimes(),f=S.rz.fast[k]||0;
    return `<section class="hero" style="margin-top:12px"><p class="lab">Ramazon, ${I.n}-kun</p><h1 style="font-size:26px">${rzLeftTxt()||'Ramazon muborak'}</h1>${t?`<p class="mu">Saharlik: ${hm(t.Fajr)} gacha. Iftor: ${hm(t.Maghrib)}.</p>`:''}<button class="big ${f===1?'ok':''}" onclick="fzT('${k}')">${f===1?'Bugun ro‘za tutdim':f===2?'Qazo ro‘za (bekor qilish)':'Bugun ro‘za tutdim'}</button></section>`}
  return `<button class="row" style="margin-top:12px;border-left-color:var(--go)" onclick="QT='r';go('q')"><span class="t"><b>Ramazonga ${I.left} kun qoldi</b><br><span class="mu">Taxminan ${I.start.slice(8)}.${I.start.slice(5,7)}.${I.start.slice(0,4)}</span></span></button>`}
function fzSet(k,v){if(k>dk())return;const R=S.rz,c=R.fast[k]||0;if(c===v)v=0;
  if(c===2){R.debt=Math.max(0,R.debt-1);const x=R.log.findIndex(y=>y.d===k&&y.k==='miss');if(x>=0)R.log.splice(x,1)}
  if(v===2){R.debt++;R.log.push({id:Date.now(),d:k,k:'miss',n:1})}
  if(v)R.fast[k]=v;else delete R.fast[k];save()}
function ramazon(){
  const I=rzInfo(),R=S.rz,T0=dk(),hj=hijri(new Date()),t=ptTimes();
  const done=Object.values(R.fast).filter(v=>v===1).length,qaz=Object.values(R.fast).filter(v=>v===2).length,tv=Object.keys(R.tar).filter(k=>R.tar[k]).length;
  const C=2*Math.PI*40,pct=Math.min(1,done/30),f0=R.fast[T0]||0;
  const title=I.on?`Ramazon, ${I.n}-kun`:I.left>0?`${I.left} kun qoldi`:'Ramazon tugadi';
  const sub=I.on?(rzLeftTxt()||'Ramazon muborak'):I.left>0?`Taxminan ${I.start.slice(8)}.${I.start.slice(5,7)}.${I.start.slice(0,4)} kuni boshlanadi`:'Qabul bo‘lsin';
  const hero=`<div class="rzh"><div class="rzh-top"><div style="min-width:0"><p class="lab">🌙 ${hj?hj.d+' '+HMN[hj.m-1]+' '+hj.y:'Ramazon'}</p><h2 class="rzh-n">${title}</h2><p class="mu">${sub}</p></div>
    <div class="rzr"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,.16)" stroke-width="9"/><circle cx="50" cy="50" r="40" fill="none" stroke="#e2b857" stroke-width="9" stroke-linecap="round" stroke-dasharray="${(C*pct).toFixed(1)} ${C.toFixed(1)}"/></svg><b><span>${done}<small>/30</small></span></b></div></div>
    ${t?`<div class="rzt"><div><span>Saharlik tugashi</span><b>${hm(t.Fajr)}</b></div><div><span>Iftor</span><b>${hm(t.Maghrib)}</b></div></div>`:''}</div>`;
  const cta=I.on&&T0>=I.start?`<div class="in" style="margin-top:12px"><button class="big ${f0===1?'ok':''}" style="margin:0;flex:1;padding:14px 8px" onclick="fzSet('${T0}',1)">${f0===1?'✓ Ro‘za tutildi':'✅ Ro‘za tutdim'}</button><button class="btn ${f0===2?'':'s'}" style="flex:1;padding:14px 8px" onclick="fzSet('${T0}',2)">${f0===2?'Qazo bo‘ldi ✓':'Tutolmadim (qazo)'}</button></div>`:'';
  const last10=I.on&&I.n>=21?`<div class="bn wr">🌙 Oxirgi 10 kecha. Qadr kechasini toq kechalardan (21, 23, 25, 27, 29) izla.</div>`:`<div class="bn ok" style="margin-top:12px">✨ Qadr kechasini izla: oxirgi 10 kunning toq kechalari (21, 23, 25, 27, 29) ✦ bilan belgilangan.</div>`;
  const off=(new Date(I.start+'T12:00').getDay()+6)%7;
  const grid=(m,cls,fill)=>`<div class="cal rm">${['Du','Se','Ch','Pa','Ju','Sh','Ya'].map(x=>`<span class="w">${x}</span>`).join('')}${Array(off).fill('<i></i>').join('')}${[...Array(30)].map((_,i)=>{const k=rzDay(I.start,i),s=m(k),fu=k>T0,dd=k.slice(8)+'.'+k.slice(5,7),ten=i>=20;
    return `<div class="c ${s===1?fill:s===2?'m':''} ${k===T0?'t':''} ${fu?'fu':''} ${ten?'ld':''}" ${fu?'':`onclick="${cls}('${k}')"`}>${ten&&i%2===0?'<em>✦</em>':''}${s===1?'<sup>✓</sup>':s===2?'<sup>✗</sup>':''}${i+1}<small>${dd}</small></div>`}).join('')}</div>`;
  const lbl={miss:['🔴','Qazo bo‘ldi'],paid:['🟢','Qazo ro‘za tutildi'],add:['🟡','Eski qazo qo‘shildi']},paid=R.log.filter(x=>x.k==='paid').length;
  const log=R.log.slice().reverse().slice(0,8).map(x=>`<div class="rtl"><span class="tdot">${lbl[x.k][0]}</span><div><b>${lbl[x.k][1]}${x.k==='add'?' (+'+x.n+')':''}</b><br><span class="mu" style="font-size:12px">${dShort(x.d)}</span></div></div>`).join('');
  return `${hero}${cta}
  <div class="st"><div><b>${done}</b>ro‘za tutildi</div><div><b>${qaz}</b>qazo</div><div><b>${tv}</b>taroveh</div></div>${last10}
  <h2>Ro‘za jurnali</h2><div class="goal" style="padding:12px 10px">${grid(k=>R.fast[k]||0,'fzT','d')}
    <div class="lg" style="justify-content:center"><span style="--c:var(--ac)">tutdim</span><span style="--c:var(--bad)">qazo</span><span style="--c:var(--go)">oxirgi 10 kun</span></div><p class="mu" style="margin:6px 0 0;text-align:center;font-size:12px">Kunni bossang: tutdim, yana bossang: qazo, yana: bekor.</p></div>
  <h2>Taroveh</h2><div class="goal" style="padding:12px 10px">${grid(k=>R.tar[k]?1:0,'tvT','g')}<p class="mu" style="margin:8px 0 0;text-align:center;font-size:12px">${tv} / 30 kun o‘qildi</p></div>
  <h2>Hatm rejasi</h2><div class="goal"><div style="display:flex;align-items:center;gap:14px"><div style="font:800 34px Fraunces,serif;color:var(--ac)">~21</div><div><b>bet kuniga</b><div class="mu" style="font-size:13px">Ramazonda 30 kunda hatm. Tugma Hatm bo‘limidagi rejani yoqadi.</div></div></div><button class="btn s" style="width:100%;margin-top:10px" onclick="hPlan(30);QT='h';render()">30 kunlik hatm rejasini yoqish</button></div>
  <h2>Ramazon kun tartibi</h2><div class="goal"><div class="mu" style="font-size:13px">Saharlik, taroveh va iftorga mos kun jadvali. Reja rejimlariga qo‘shiladi, keyin o‘zgartirsang bo‘ladi.</div><button class="btn s" style="width:100%;margin-top:10px" onclick="mdNew('ramazon')">Ramazon rejimini qo‘shish</button></div>
  <h2>Qazo ro‘zalar</h2><div class="goal" style="text-align:center;padding:16px"><div style="font:800 46px Fraunces,serif;line-height:1;color:${R.debt>0?'var(--bad)':'var(--ac)'}">${R.debt}</div><div class="mu">${R.debt>0?'ta qazo ro‘za qoldi':'qazo ro‘za qolmadi'}${paid?' · '+paid+' tasi tutildi':''}</div>
    <div class="in" style="margin:12px 0 0"><button class="btn" style="flex:1" onclick="rzPay()">Qazoni tutdim (−1)</button><button class="btn s" style="flex:1" onclick="rzAdd()">+ Qo‘shish</button></div></div>
  ${log?`<div class="goal" style="padding:6px 14px">${log}</div>`:''}
  <details class="goal" style="margin-top:8px"><summary style="font-weight:600">Boshlanish sanasi</summary><p class="mu" style="margin:8px 0">Sana hisob bo‘yicha taxminiy. Rasman e‘lon qilingach, shu yerga yoz.</p><div class="in"><input type="date" value="${R.start||I.start}" onchange="rzSet(this.value)"><button class="btn s" onclick="rzSet('')">Hisobga qaytish</button></div></details>`}
PRE.ramazon=['Ramazon kuni',[mkb('sah','Saharlik',M(4,30),M(5,15),'Sahar va niyat.'),mkb('qur','Bomdod va Qur‘on',M(5,30),M(7)),mkb('ish','Ish yoki dars',M(9),M(15)),mkb('hat','Qur‘on hatmi',M(15),M(16,30)),mkb('dam','Dam olish',M(16,30),M(17,30)),mkb('ift','Iftor',M(17,30),M(18,30),'Iftor va ovqat.'),mkb('tar','Taroveh',M(20),M(21,30)),mkb('uyqu1','Uxlash',M(22,30),M(28,30),'Saharlikka turish.')]];

// ---- PDF kitoblar (qurilmada saqlanadi) ----
const IDBO=()=>new Promise((res,rej)=>{const r=indexedDB.open('trk-files',1);r.onupgradeneeded=()=>r.result.createObjectStore('pdf');r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)});
async function idbSet(k,v){const d=await IDBO();return new Promise((res,rej)=>{const t=d.transaction('pdf','readwrite');t.objectStore('pdf').put(v,k);t.oncomplete=()=>res();t.onerror=()=>rej(t.error)})}
async function idbGet(k){const d=await IDBO();return new Promise((res,rej)=>{const q=d.transaction('pdf').objectStore('pdf').get(k);q.onsuccess=()=>res(q.result);q.onerror=()=>rej(q.error)})}
async function idbDel(k){const d=await IDBO();return new Promise((res,rej)=>{const t=d.transaction('pdf','readwrite');t.objectStore('pdf').delete(k);t.oncomplete=()=>res();t.onerror=()=>rej(t.error)})}

function toast(t){let e=document.getElementById('toast');if(!e){e=document.createElement('div');e.id='toast';e.style.cssText='pointer-events:none;position:fixed;left:50%;transform:translateX(-50%);bottom:calc(env(safe-area-inset-bottom,0px) + 140px);background:#222;color:#fff;padding:10px 16px;border-radius:14px;z-index:200;font-size:14px;max-width:86%;text-align:center';document.body.appendChild(e)}e.textContent=t;e.style.display='block';clearTimeout(e._t);e._t=setTimeout(()=>{e.style.display='none'},3500)}
async function cloudUp(b,buf){if(!sb||!UID)return;if(!cloudOk(buf.byteLength)){toast('Bulut limiti to‘ldi: PDF faqat shu telefonda qoladi');return}b.sz=buf.byteLength;PUPL[b.id]=1;render();
  try{const r=await sb.storage.from('books').upload(UID+'/'+b.id+'.pdf',new Blob([buf],{type:'application/pdf'}),{upsert:true,contentType:'application/pdf'});if(r.error)throw r.error;b.cloud=1;save();toast('PDF bulutga saqlandi')}
  catch(e){toast('Bulutga yuklanmadi: '+(e.message||e)+'. PDF faqat shu telefonda qoldi.')}
  delete PUPL[b.id];render()}
function cloudDel(id){if(sb&&UID)sb.storage.from('books').remove([UID+'/'+id+'.pdf']).catch(()=>{})}
let PDFL=null;
function loadPdfjs(){return PDFL||(PDFL=new Promise((res,rej)=>{const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.min.js';s.onload=()=>{window.pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js';res(window.pdfjsLib)};s.onerror=()=>{PDFL=null;rej(new Error('pdf.js yuklanmadi'))};document.head.appendChild(s)}))}
async function ktPdf(inp,id){
  const f=inp.files&&inp.files[0];if(!f)return;
  try{const buf=await f.arrayBuffer(),lib=await loadPdfjs(),doc=await lib.getDocument({data:buf.slice(0)}).promise,n=doc.numPages;doc.destroy();
    let b=id?ktB(id):null;
    if(!b){b={id:Date.now(),t:f.name.replace(/\.pdf$/i,''),a:'',n,p:0,st:'o',fin:'',r:0,sum:'',pdf:1,cur:1};S.kt.books.push(b)}
    else{b.n=n;b.pdf=1;b.cur=b.cur||Math.max(1,b.p)}
    await idbSet(b.id,buf);try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist()}catch(x){}save();cloudUp(b,buf);
  }catch(e){alert('PDF ochilmadi: '+(e.message||e))}
  inp.value=''}
async function ktPdfDel(id){if(!confirm('PDF fayl o‘chirilsinmi? Kitob va o‘qilgan betlar qoladi.'))return;try{await idbDel(id)}catch(e){}const b=ktB(id);cloudDel(id);if(b){b.pdf=0;b.cloud=0}save()}
// o‘qilgan betni hisoblash: ketma-ket (3 betgacha) o‘tish o‘qilgan deb yoziladi, katta sakrash faqat joyni eslab qoladi
function pgTrack(b,p){b.cur=p;if(p>b.p){const d=p-b.p;if(d<=3)ktLog(b,d);b.p=p;if(b.n&&b.p>=b.n&&b.st==='o'){b.st='t';b.fin=dk()}}}
let RD=null;
async function rdOpen(id){
  const b=ktB(id);if(!b)return;
  try{let buf=await idbGet(id);
    if(!buf&&b.cloud&&sb&&UID){toast('PDF bulutdan yuklab olinmoqda...');const r=await sb.storage.from('books').download(UID+'/'+id+'.pdf');if(r.error)throw r.error;buf=await r.data.arrayBuffer();await idbSet(id,buf)}
    if(!buf){alert('Bu qurilmada PDF topilmadi. Qayta yuklash uchun “PDF o‘chirish” va keyin “PDF qo‘shish” ni bos.');return}
    const lib=await loadPdfjs(),doc=await lib.getDocument({data:buf.slice(0)}).promise;
    rdClose(true);RD={id,doc,n:doc.numPages,page:1,zoom:1,tok:0};rdBuild(b);await rdShow(b.cur||1)
  }catch(e){alert('PDF ochilmadi: '+(e.message||e))}}
function rdBuild(b){const old=document.getElementById('rd');if(old)old.remove();const d=document.createElement('div');d.id='rd';d.className='rdo';
  d.innerHTML=`<div class="rdt"><button class="x" style="font-size:22px" onclick="rdClose()">✕</button><b style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(b.t)}</b><span id="rdn" class="mu"></span></div><div id="rdc" class="rdc"><canvas id="rdv"></canvas></div><div class="rdb"><button class="btn s" onclick="rdGo(-1)">‹</button><input id="rdp" type="number" inputmode="numeric" onchange="rdSet(this.value)"><button class="btn s" onclick="rdGo(1)">›</button><button class="btn s" onclick="rdZ(-0.25)">−</button><button class="btn s" onclick="rdZ(0.25)">+</button></div>`;
  document.body.appendChild(d);let x0=null;const c=d.querySelector('#rdc');
  c.addEventListener('touchstart',e=>{x0=e.touches.length===1?e.touches[0].clientX:null},{passive:true});
  c.addEventListener('touchend',e=>{if(x0===null||RD.zoom>1)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>70)rdGo(dx<0?1:-1);x0=null},{passive:true})}
async function rdShow(p){
  const R=RD;if(!R)return;p=Math.max(1,Math.min(R.n,Math.round(p)||1));R.page=p;const t=++R.tok;
  const pg=await R.doc.getPage(p),box=document.getElementById('rdc'),cv=document.getElementById('rdv');if(!box||!cv||t!==R.tok)return;
  const v0=pg.getViewport({scale:1}),dpr=window.devicePixelRatio||1,sc=box.clientWidth/v0.width*R.zoom,vp=pg.getViewport({scale:sc*dpr});
  cv.width=vp.width;cv.height=vp.height;cv.style.width=vp.width/dpr+'px';cv.style.height=vp.height/dpr+'px';
  await pg.render({canvasContext:cv.getContext('2d'),viewport:vp}).promise;if(t!==R.tok)return;
  box.scrollTop=0;document.getElementById('rdp').value=p;document.getElementById('rdn').textContent=p+' / '+R.n;
  const b=ktB(R.id);if(b){pgTrack(b,p);save()}}
function rdGo(d){if(RD)rdShow(RD.page+d)}
function rdSet(v){if(RD)rdShow(+v)}
function rdZ(d){if(RD){RD.zoom=Math.max(0.75,Math.min(3,RD.zoom+d));rdShow(RD.page)}}
function rdClose(silent){const e=document.getElementById('rd');if(e)e.remove();if(RD&&RD.doc){try{RD.doc.destroy()}catch(x){}}RD=null;if(!silent)render()}

function habNav(){
  const seg=`<div class="seg"><button class="${HV==='w'?'on':''}" onclick="HV='w';render()">Haftalik jadval</button><button class="${HV==='m'?'on':''}" onclick="HV='m';render()">Oylik jadval</button></div>`;
  return seg+(HV==='w'?`<div class="in"><button class="btn s" onclick="HW--;render()">‹</button><button class="btn s" onclick="HW=0;render()">Shu hafta</button><button class="btn s" onclick="HW++;render()">›</button></div>`:`<div class="in"><button class="btn s" onclick="HMo--;render()">‹</button><button class="btn s" onclick="HMo=0;render()">Shu oy</button><button class="btn s" onclick="HMo++;render()">›</button></div>`)}
function habWeek(today){
  const b=new Date();b.setDate(b.getDate()+HW*7);const w0=(b.getDay()+6)%7;
  const days=[...Array(7)].map((_,i)=>{const x=new Date(b.getFullYear(),b.getMonth(),b.getDate()-w0+i);return{k:x.toLocaleDateString('sv'),wd:x.getDay(),d:x.getDate()}});
  const cl=d=>(d.k===today?'tdy':'')+(d.wd===0||d.wd===6?' we':'');
  const head=`<div class="hw hwh">${days.map(d=>`<div class="${cl(d)}${d.k===today?' td':''}"><span style="font-size:11px">${DAYS[d.wd].slice(0,2)}</span><b style="font-size:15px">${d.d}</b></div>`).join('')}</div>`;
  const rows=S.hab.map((x,hi)=>{const st=hst(x.id),col=HC[hi%HC.length],n=days.filter(d=>(S.hb[d.k]||{})[x.id]).length;
    return `<div class="hcard"><div style="display:flex;align-items:center;gap:8px"><span style="flex:1;font-weight:600">${x.e?x.e+' ':`<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${col};margin-right:6px"></span>`}${esc(x.t)}</span><button class="x" onclick="delH(${hi})">×</button></div><p class="mu" style="margin:2px 0 6px;font-size:12px">🔥 ${st}&nbsp; haftada ${n} kun</p><div class="hw">${days.map(d=>{const on=(S.hb[d.k]||{})[x.id],fu=d.k>today;return `<div class="${cl(d)}"><button class="cell ${on?'on':hkOn(d.k,x.id)?'hsk':''}" style="--hc:${col}" ${fu?'disabled':''} onclick="hbC('${x.id}','${d.k}')"></button></div>`}).join('')}</div></div>`}).join('');
  return head+rows}

function spHide(){const s=document.getElementById('splash');if(!s||s._h)return;s._h=1;s.classList.add('out');setTimeout(()=>{if(s.remove)s.remove()},900)}
try{const rm=matchMedia('(prefers-reduced-motion:reduce)').matches;setTimeout(spHide,rm?900:3700)}catch(e){setTimeout(spHide,3700)}

function urgeStart(){URG={end:Date.now()+5*60000};URG.iv=setInterval(()=>{const l=Math.max(0,Math.ceil((URG.end-Date.now())/1000)),e=document.getElementById('utm');if(e)e.textContent=fmtT(l);if(l<=0){clearInterval(URG.iv);URG.done=1;if(navigator.vibrate)navigator.vibrate([250,120,250]);render()}},500);render()}
function urgeEnd(win){if(URG)clearInterval(URG.iv);if(win!==null)S.iso.log.push({id:Date.now(),d:dk(),t:'5 daqiqa kutish usuli',w:win});URG=null;save()}
const UTIPS=['Chuqur nafas ol: 4 soniya nafas ol, 6 soniya chiqar.','Bir stakan suv ich.','Telefonni boshqa xonaga qo‘y.','Bir oz yur yoki cho‘zil.','O‘zingdan so‘ra: zerikdingmi, charchadingmi yoki yolg‘izmisan?'];
function urgeCard(){
  if(!URG)return `<div class="goal" style="border-left:4px solid var(--go)"><b>Kirgging keldimi?</b><p class="mu" style="margin:4px 0 10px">Chalg‘ish istagi odatda 5–10 daqiqada pasayadi. Shu vaqtni kutib ko‘r.</p><button class="btn" style="width:100%" onclick="urgeStart()">5 daqiqa kutaman</button></div>`;
  if(URG.done)return `<div class="goal" style="border-left:4px solid var(--ac)"><b>5 daqiqa o‘tdi</b><p class="mu" style="margin:4px 0 10px">Hali ham kirging kelyaptimi? Natijani yoz.</p><div class="in" style="margin:0"><button class="btn" style="flex:1" onclick="urgeEnd(1)">Yengdim</button><button class="btn s" style="flex:1" onclick="urgeEnd(0)">Yutqazdim</button></div></div>`;
  const l=Math.max(0,Math.ceil((URG.end-Date.now())/1000)),tip=UTIPS[Math.min(4,Math.floor((300-l)/60))];
  return `<div class="goal" style="border-left:4px solid var(--ac);text-align:center"><b>Kuting va nafas oling</b><div class="breath"></div><div class="tmr" id="utm">${fmtT(l)}</div><p style="margin:0 0 10px">${tip}</p><button class="btn s" style="width:100%" onclick="urgeEnd(null)">Bekor qilish</button></div>`}

const STK={'Kun yo‘li':'🛣','Kun jadvali':'📅','Barcha rejalar':'📅','Namozlar':'🕌','Odatlar':'✅','Kun qoidalari':'📜','Qo‘shimcha vazifalar':'📝','Kayfiyat':'😊','Suv':'💧','Kun xulosasi':'📓','So‘nggi 14 kun':'📊',
'Suralar':'📜','Pora takrori':'🔁','O‘zim tanlagan takror':'🎯','Bugun yodlayotganlarim':'🧠','Takror navbati':'🔁','Yodlangan suralar':'📜','Keyingi 7 kun yuki':'📆','Hatm rejasi':'🗓','Pora xaritasi':'🗺','Joyni belgilash':'📍','Tugatilgan hatmlar':'🏁','Namozda o‘qilgan Qur‘on':'📖','Namozda yodlaganlarim hatmi':'🕌','Qazo namozlar jurnali':'📒','Taroveh':'🌙','Ro‘za jurnali':'🌙','Boshlanish sanasi':'📅','Ramazon jadvali':'🗓','Qazo ro‘zalar jurnali':'📒','30 pora':'📖',
'Maqsadlarga mos odatlar':'💡','Kunlar bo‘yicha':'📊','Hafta raqamlarda':'🔢','Odat va qoidalar':'✅','Xulosa':'📝','Mashq yozish':'💪','Vazn va o‘lchamlar':'⚖️','Raqamlarda':'🔢','Ulashish':'📤','Pul (shaxsiy)':'💰',
'Test rejimi':'🧪','So‘z qo‘shish':'➕','So‘zlar ro‘yxati':'🔤','Ko‘nikmalar':'🎚','Bugungi reja':'📋','Mock natijalari o‘sishi':'📈','Yozilgan inshoalar':'📄','So‘nggi baholar':'⭐','So‘nggi natijalar':'🧾','Imtihonlar':'🗓','Imtihon simulyatori':'⏱','Natija yozish':'✍️','Zaif mavzular':'⚠️','Bosqichlar':'🪜','Tugatilgan kitoblar':'🏁','Kitob qo‘shish':'➕','O‘qish rejasi':'🗒','Chalg‘ish jurnali':'📓',
'So‘nggi yozuvlar':'🧾','Men qarzdorman':'📤','Menga qarzdor':'📥','Yopilgan':'✔️','Chiqim kategoriyalari':'🗂','Kunlar bo‘yicha chiqim':'📊','Eng katta chiqimlar':'🔝','So‘nggi 6 oy':'📈','Boshlang‘ich qoldiq':'🏦','Oylik byudjet':'📏','Jamg‘arma maqsadlari':'💎','Obuna berish':'🎁','Sozlamalar':'⚙️',
'Ko‘rinish':'🎨','Profil':'👤','Hisob':'🔐','Obuna':'⭐','Sinxronlash':'🔄','Eslatmalar':'🔔','Zaxira nusxa':'💾','Reja rejimlari':'🔀','Foydalanuvchilar':'👥'};
const STKK=Object.keys(STK).sort((a,b)=>b.length-a.length);
const stick=html=>html.replace(/<h2([^>]*)>([^<]+)/g,(m,a,t)=>{const k=STKK.find(x=>t.startsWith(x));return k?`<h2${a}>${STK[k]} ${t}`:m});

