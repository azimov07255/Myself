// ---- Foydalanish statistikasi: qaysi bo'lim ochilyapti, qancha vaqt, AI qancha sarflanyapti (faqat o'z hisobingda) ----
const US_QT={u:'Mushaf',y:'Yodlash',t:'Takror',h:'Hatm',a:'Tinglash',x:'Hifz xaritasi'},US_QI={n:'Namoz',z:'Zikr',d:'Duolar',r:'Ramazon'},US_IV={b:'Bosh',l:'Lug‘at',a:'Materiallar',m:'Natijalar',w:'Writing',s:'Speaking',x:'AI mashq',k:'Imtihon'};
const US_ALL=['Bugun','Qur‘on · Mushaf','Qur‘on · Yodlash','Qur‘on · Takror','Qur‘on · Hatm','Qur‘on · Tinglash','Qur‘on · Hifz xaritasi','Ibodat · Namoz','Ibodat · Zikr','Ibodat · Duolar','Ibodat · Ramazon','Odat','Maqsad','IELTS · Bosh','IELTS · Lug‘at','IELTS · Materiallar','IELTS · Natijalar','IELTS · Writing','IELTS · Speaking','IELTS · AI mashq','IELTS · Imtihon','IELTS · O‘qish oynasi','Pul','Sozlama'];
const US_AI={chat:'Suhbat',plan:'Top-3 reja',dayplan:'Kun jadvali',vocab:'Lug‘at tahlili',reading:'Reading mashqi',ielts:'Writing/Speaking',food:'Ovqat',transcribe:'Ovoz',transcript:'Transkript',coach:'Murabbiy',iex:'IELTS mashqlari',videos:'Videolar',boshqa:'Boshqa'};
let USK='',USL=0,UST=0,USP=7;
function usD(){const u=S.us=S.us||{d:{},ai:{}};u.d=u.d||{};u.ai=u.ai||{};return u}
function usKey(){try{if(typeof SO!=='undefined'&&SO)return 'Qidiruv';if(document.getElementById('iem'))return 'IELTS · O‘qish oynasi';if(typeof MFO!=='undefined'&&MFO)return 'Qur‘on · Mushaf';
  if(tab==='h')return 'Bugun';if(tab==='q')return QT in US_QI?'Ibodat · '+US_QI[QT]:'Qur‘on · '+(US_QT[QT]||QT);if(tab==='o')return 'Odat';if(tab==='m')return 'Maqsad';if(tab==='s')return 'Sozlama';
  if(tab==='e')return EV==='i'?'IELTS · '+(US_IV[IVW]||IVW):EV==='u'?'Univer':EV==='p'?'Prava':'Kitob';return 'Pul'}catch(e){return ''}}
function usFlush(){const now=Date.now();if(USK&&USL&&(typeof document==='undefined'||document.visibilityState!=='hidden')){const dt=Math.min(300,Math.round((now-USL)/1000));if(dt>0){const D=usD().d,k=dk(),r=(D[k]=D[k]||{})[USK]=(D[k]||{})[USK]||[0,0];r[1]+=dt}}USL=now}
function usHit(){const key=usKey();if(!key||!(S.ob||S.ts))return;usFlush();if(key!==USK){USK=key;const D=usD().d,k=dk(),r=(D[k]=D[k]||{})[key]=D[k][key]||[0,0];r[0]++;usSaveSoon()}}
function usPrune(){const u=usD(),lo=dAgo(45);Object.keys(u.d).forEach(k=>{if(k<lo)delete u.d[k]});Object.keys(u.ai).forEach(k=>{if(k<lo)delete u.ai[k]})}
function usSaveSoon(){clearTimeout(UST);UST=setTimeout(()=>{usPrune();try{qsave()}catch(e){}},30000)}
function usAi(act){const a=usD().ai,k=dk(),o=a[k]=a[k]||{};o[act||'boshqa']=(o[act||'boshqa']||0)+1;usSaveSoon()}
function usAgg(days){const u=usD(),from=dAgo(days-1),sc={},ai={},daily=[];let active=0;
  Object.keys(u.d).forEach(k=>{if(k<from)return;let any=false;Object.entries(u.d[k]).forEach(([key,v])=>{const e=sc[key]||(sc[key]=[0,0]);e[0]+=v[0];e[1]+=v[1];any=true});if(any)active++});
  for(let i=days-1;i>=0;i--){const k=dAgo(i),a=u.ai[k]||{},n=Object.values(a).reduce((x,y)=>x+y,0);daily.push({d:k,n});Object.entries(a).forEach(([x,v])=>ai[x]=(ai[x]||0)+v)}
  return{screens:sc,active,ai,daily,aiTotal:daily.reduce((a,b)=>a+b.n,0),days}}
const usMin=s=>s<60?s+' s':Math.round(s/60)+' daq';
function usReset(){if(!confirm('Foydalanish statistikasi tozalansinmi?'))return;S.us={d:{},ai:{}};save()}
function usCard(){const A=usAgg(USP),rows=Object.entries(A.screens).sort((a,b)=>b[1][1]-a[1][1]||b[1][0]-a[1][0]),mx=Math.max(1,...rows.map(r=>r[1][1])),unused=US_ALL.filter(k=>!A.screens[k]&&k!=='IELTS · O‘qish oynasi'),mxd=Math.max(40,...A.daily.map(d=>d.n)),
  ais=Object.entries(A.ai).sort((a,b)=>b[1]-a[1]);
  return `<div class="seg" style="margin:0 0 8px"><button class="${USP===7?'on':''}" onclick="USP=7;render()">7 kun</button><button class="${USP===30?'on':''}" onclick="USP=30;render()">30 kun</button></div>
  <p class="mu" style="margin:0 0 8px">Faol kunlar: <b>${A.active}</b> / ${USP} · bu ma’lumot faqat sening hisobingda saqlanadi.</p>
  ${rows.length?rows.slice(0,12).map(([k,v])=>`<div class="usr"><span class="usk">${esc(k)}</span><span class="usb"><i style="width:${Math.round(v[1]/mx*100)}%"></i></span><span class="usv">${usMin(v[1])} · ${v[0]}×</span></div>`).join(''):'<p class="mu">Hali ma’lumot yo‘q: ilovadan foydalan, bu yerda ko‘rinadi.</p>'}
  ${unused.length?`<p class="mu" style="margin:10px 0 4px">Bu davrda ochilmagan bo‘limlar:</p><div class="rwch">${unused.map(k=>`<span class="chip">${esc(k)}</span>`).join('')}</div>`:''}
  <h2 style="margin:14px 0 6px;font-size:16px">AI sarfi</h2><p class="mu" style="margin:0 0 6px">${USP} kunda <b>${A.aiTotal}</b> so‘rov (kuniga limit 40).</p>
  <div class="usd">${A.daily.slice(-14).map(d=>`<div title="${d.d}: ${d.n}"><i style="height:${Math.max(2,Math.round(d.n/mxd*100))}%"></i></div>`).join('')}</div>
  ${ais.map(([k,n])=>`<div class="usr"><span class="usk">${esc(US_AI[k]||k)}</span><span class="usb"><i style="width:${Math.round(n/ais[0][1]*100)}%"></i></span><span class="usv">${n} ta</span></div>`).join('')}
  <button class="btn s" style="margin-top:10px" onclick="usReset()">Statistikani tozalash</button>`}
if(typeof document!=='undefined'){setInterval(()=>{if(document.visibilityState==='visible')usHit()},15000);document.addEventListener('visibilitychange',()=>{usFlush();if(document.visibilityState==='hidden')usSaveSoon()})}
