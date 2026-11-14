// ---- Yangi versiya xabari: version.json ni tekshiradi, "Yangilash" bosilganda ma'lumotni saqlab, keshni tozalab qayta yuklaydi ----
const SWC='trk-v2'; // sw.js dagi kesh nomi bilan bir xil
const verCmp=(a,b)=>{const p=x=>String(x||'').split(/[.\-]/).map(n=>parseInt(n,10)||0),A=p(a),B=p(b);for(let i=0;i<Math.max(A.length,B.length);i++){const d=(A[i]||0)-(B[i]||0);if(d)return d<0?-1:1}return 0};
const skGet=k=>{try{return sessionStorage.getItem(k)}catch(e){return null}},skSet=(k,v)=>{try{v===null?sessionStorage.removeItem(k):sessionStorage.setItem(k,v)}catch(e){}};
let UPD=null,UPDT=0,UPDMSG='',UPDX=skGet('trk_updx')||'';
async function updCheck(manual){
  if(typeof location==='undefined'||!/^https?:/.test(location.protocol)){if(manual){UPDMSG='Bu yerda tekshirib bo‘lmaydi (ilova sayt orqali ochilishi kerak).';render()}return}
  UPDT=Date.now();let j=null;
  try{const r=await fetch('version.json?t='+Date.now(),{cache:'no-store'});if(r.ok)j=await r.json()}catch(e){}
  if(!j||!j.v){if(manual){UPDMSG='Tekshirib bo‘lmadi (internet yoki server).';render()}return}
  const c=verCmp(j.v,APP_VER),newer=c>0||(c===0&&!!j.b&&j.b!==APP_BUILD);   // eski versiya ko'rsatilsa (tarqalish kechikishi yoki orqaga qaytarish) e'tibor bermaymiz
  if(newer){UPD={v:j.v,b:j.b||'',n:String(j.n||'').slice(0,140)};if(manual)UPDMSG='Yangi versiya bor: v'+j.v+'. Yuqoridagi “Yangilash” tugmasini bosing.'}
  else{UPD=null;skSet('trk_updtry',null);if(manual)UPDMSG='Eng so‘nggi versiya o‘rnatilgan (v'+APP_VER+').'}
  updShow();if(manual)render()}
function updShow(){let b=document.getElementById('updb');const tok=UPD?UPD.v+'|'+UPD.b:'';
  if(!UPD||tok===UPDX){if(b)b.remove();return}
  if(!b){b=document.createElement('div');b.id='updb';b.className='updb';b.setAttribute('role','status');document.body.appendChild(b)}
  b.innerHTML=`<span>🔄 Yangi versiya tayyor (v${esc(UPD.v)})${UPD.n?`<small>${esc(UPD.n)}</small>`:''}</span><button class="btn" onclick="updGo()">Yangilash</button><button class="x" onclick="updLater()" aria-label="Keyinroq">✕</button>`}
function updLater(){if(UPD){UPDX=UPD.v+'|'+UPD.b;skSet('trk_updx',UPDX)}updShow()}
function updReload(){location.reload()}
async function updGo(){
  const last=+skGet('trk_updtry')||0;
  if(Date.now()-last<120000){toast('Yangilanish hali tarqalmagan bo‘lishi mumkin. 1–2 daqiqadan keyin yana bosing.');return}   // qayta-qayta yuklanib qolmaslik uchun
  const b=document.querySelector('#updb .btn');if(b){b.disabled=true;b.textContent='Saqlanmoqda…'}
  try{await Promise.race([push(),new Promise(r=>setTimeout(r,3500))])}catch(e){}          // avval hamma ma'lumot serverga ketsin (mahalliy nusxa baribir saqlangan)
  skSet('trk_updtry',String(Date.now()));
  try{if(window.caches){const c=await caches.open(SWC),ks=await c.keys();await Promise.all(ks.filter(r=>!/\/(fonts|data)\//.test(new URL(r.url).pathname)).map(r=>c.delete(r)))}}catch(e){}   // ilova fayllari yangilanadi, katta Qur'on fayllari qoladi
  try{const reg=navigator.serviceWorker&&await navigator.serviceWorker.getRegistration();if(reg)await reg.update()}catch(e){}
  updReload()}
function updCard(){return `<div class="in"><button class="btn s" style="flex:1" onclick="updCheck(true)">🔄 Yangilanishni tekshirish</button></div>${UPDMSG?`<p class="mu" style="margin:8px 0 0">${esc(UPDMSG)}</p>`:''}`}
if(typeof window!=='undefined'&&typeof location!=='undefined'&&/^https?:/.test(location.protocol)){
  setTimeout(()=>updCheck(),4000);
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'&&Date.now()-UPDT>30*60*1000)updCheck()});
  window.addEventListener('online',()=>{if(Date.now()-UPDT>5*60*1000)updCheck()})}
