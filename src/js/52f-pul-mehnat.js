// ---- PUL: "bu necha soatlik ish?" xarajatni mehnat soatiga aylantirib ko'rsatadi. Hamma narsa qurilmada. Prefiks: mhn ----
const mhnS=()=>{finInit();return S.fin.mh=S.fin.mh||{}};
const mhnOn=()=>uiG('trk_mhn')!=='0';
function mhnRate(){const m=(S.fin&&S.fin.mh)||{};return(m.inc>0&&(m.hrs||160)>0)?m.inc/(m.hrs||160):0}
const mhnDay=()=>{const m=(S.fin&&S.fin.mh)||{};return m.dh>0?m.dh:8};
function mhnFmt(h){
  const mins=Math.round(h*60);if(mins<1)return '1 daqiqadan kam';if(mins<60)return mins+' daqiqa';
  const dh=mhnDay();if(h<dh){const hh=Math.floor(mins/60),mm=mins%60;return hh+' soat'+(mm?' '+mm+' daqiqa':'')}
  const d=Math.round(h/dh*10)/10;return String(d).replace('.',',')+' ish kuni ('+dh+' soat)'}
// a so'm necha soatlik mehnat; sozlanmagan yoki o'chirilgan bo'lsa bo'sh matn
function mhnTxt(a){if(!mhnOn()||!(a>0))return '';const r=mhnRate();return r?'⏱ ≈ '+mhnFmt(a/r)+' ish':''}
function mhnForm(){const e=document.getElementById('mhnf');if(!e)return;e.textContent=K==='out'?mhnTxt(+FA||0):''}
function mhnLine(){if(K!=='out'||!mhnOn()||!mhnRate())return '';return `<p id="mhnf" class="mu" style="margin:-2px 0 6px;font-size:13px">${esc(mhnTxt(+FA||0))}</p>`}
function mhnSet(k,v){const m=mhnS();m[k]=sfn(v);if(!(m[k]>0))delete m[k];save()}
function mhnAuto(){const e=pIncomeEst();if(!(e>0)){toast('Avval kirim yozuvlarini qo‘sh');return}mhnS().inc=e;save()}
function mhnCard(){
  if(W!=='p')return '';const m=mhnS(),r=mhnRate(),ex=[10000,50000,200000];
  return `<h2>⏱ Mehnat narxi</h2><div class="goal"><p class="mu" style="margin:0 0 8px;font-size:13px">Oylik daromading va ish soatingni yoz: xarajat kiritganingda “bu necha soatlik ish?” deb ko‘rsatiladi. Impuls xaridlarni kamaytiradi.</p>
   <div class="in"><input type="text" inputmode="numeric" placeholder="Oylik daromad, so‘m" value="${m.inc||''}" onchange="mhnSet('inc',this.value)"><button class="btn s" onclick="mhnAuto()" style="flex:0 0 auto;font-size:12px">Kirimimdan</button></div>
   <div class="in"><input type="text" inputmode="numeric" placeholder="Oyiga ish soati (standart 160)" value="${m.hrs||''}" onchange="mhnSet('hrs',this.value)"><input type="text" inputmode="numeric" placeholder="Ish kuni soati (8)" value="${m.dh||''}" onchange="mhnSet('dh',this.value)"></div>
   ${r?`<p style="margin:0 0 4px">1 soat mehnating ≈ <b>${num(Math.round(r))}</b> so‘m.</p><p class="mu" style="margin:0;font-size:13px">${ex.map(a=>num(a)+' so‘m = '+mhnFmt(a/r)).join(' · ')}</p>`:'<p class="mu" style="margin:0;font-size:13px">Daromad yozilmaguncha ko‘rsatma chiqmaydi.</p>'}</div>`}
function mhnRep(){
  const r=mhnRate();if(!r||!mhnOn())return '';
  const L=mList(W,mKey(PF.mo).k).filter(m=>m.k==='out'),tot=L.reduce((a,m)=>a+m.a,0),t={z:0,x:0,k:0};L.forEach(m=>{if(t[m.t]!==undefined)t[m.t]+=m.a});
  if(!tot)return '';
  return `<h2>⏱ Xarajat = mehnat</h2><div class="goal"><p style="margin:0 0 6px">Shu oy sarflaganing <b>${num(tot)}</b> so‘m ≈ <b>${mhnFmt(tot/r)}</b> ish.</p>
   ${t.k||t.x?`<p class="mu" style="margin:0;font-size:13px">${t.k?'🔴 Keraksiz: '+num(t.k)+' so‘m ≈ '+mhnFmt(t.k/r)+'. ':''}${t.x?'🟡 Xohish: '+num(t.x)+' so‘m ≈ '+mhnFmt(t.x/r)+'.':''}</p>`:''}</div>`}
function mhnJl(){return `<p class="mu" style="margin:12px 0 4px;font-size:12px"><b>⏱ Pul: xarajat necha soatlik ish ekani</b></p>${jlSeg('trk_mhn','1',[['1','Ko‘rinsin (daromad kiritilsa)'],['0','Ko‘rinmasin (avvalgidek)']])}`}
