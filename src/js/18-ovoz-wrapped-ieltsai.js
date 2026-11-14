// ---- Ovozli kiritish: yozib olinadi, WAV ga o‘tkaziladi, Gemini matnga aylantiradi ----
async function toWav(blob,sr0){
  const AC=window.AudioContext||window.webkitAudioContext,ctx=new AC(),buf=await blob.arrayBuffer();
  const dec=await new Promise((res,rej)=>{const p=ctx.decodeAudioData(buf,res,rej);if(p&&p.catch)p.catch(rej)});try{ctx.close&&ctx.close()}catch(e){}
  const sr=sr0||16000,len=Math.max(1,Math.ceil(dec.duration*sr)),OAC=window.OfflineAudioContext||window.webkitOfflineAudioContext,off=new OAC(1,len,sr),src=off.createBufferSource();src.buffer=dec;src.connect(off.destination);src.start();
  const d=(await off.startRendering()).getChannelData(0),o=new DataView(new ArrayBuffer(44+d.length*2)),w=(p,s)=>{for(let i=0;i<s.length;i++)o.setUint8(p+i,s.charCodeAt(i))};
  w(0,'RIFF');o.setUint32(4,36+d.length*2,true);w(8,'WAVE');w(12,'fmt ');o.setUint32(16,16,true);o.setUint16(20,1,true);o.setUint16(22,1,true);o.setUint32(24,sr,true);o.setUint32(28,sr*2,true);o.setUint16(32,2,true);o.setUint16(34,16,true);w(36,'data');o.setUint32(40,d.length*2,true);
  for(let i=0;i<d.length;i++){const s=Math.max(-1,Math.min(1,d[i]));o.setInt16(44+i*2,s<0?s*0x8000:s*0x7fff,true)}
  return o.buffer}
let REC=null;
async function aiMic(){
  if(REC){REC.stop();return}
  if(!navigator.mediaDevices||!window.MediaRecorder){alert('Bu qurilmada ovoz yozish ishlamaydi. Klaviaturadagi 🎤 (diktovka) tugmasidan foydalaning.');return}
  let st;try{st=await navigator.mediaDevices.getUserMedia({audio:true})}catch(e){alert('Mikrofonga ruxsat berilmadi. Telefon sozlamalarida Kunlik tizim uchun mikrofonga ruxsat bering.');return}
  const ch=[],mr=new MediaRecorder(st),t0=Date.now();REC=mr;let b=document.getElementById('aimic');
  mr.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};
  const tick=setInterval(()=>{const s=Math.floor((Date.now()-t0)/1000),x=document.getElementById('aimic');if(x)x.textContent='⏹ '+s;if(s>=45)mr.stop()},500);
  mr.onstop=async()=>{clearInterval(tick);st.getTracks().forEach(x=>x.stop());REC=null;const x=document.getElementById('aimic');if(x){x.classList.remove('rec');x.textContent='⏳'}
    try{const blob=new Blob(ch,{type:mr.mimeType||'audio/mp4'});if(blob.size<1500)throw new Error('Ovoz juda qisqa, qayta urinib ko‘ring.');
      const d=await fnAI({action:'transcribe',audio:b64(await toWav(blob)),mime:'audio/wav'}),txt=(d.text||'').trim();if(!txt)throw new Error('Gap eshitilmadi.');aiSend(txt)}
    catch(e){alert(e.message||'Ovozni matnga aylantirib bo‘lmadi.')}
    const y=document.getElementById('aimic');if(y){y.classList.remove('rec');y.textContent='🎤'}};
  mr.start();if(b){b.classList.add('rec');b.textContent='⏹ 0'}}

// ---- Yillik hisobot (Wrapped) ----
let RY='m',RYo=0;
function yStats(y){
  const M=[...Array(12)].map((_,m)=>mStats(y,m)).filter(s=>s.days>0);if(!M.length)return null;
  const sum=f=>M.reduce((a,s)=>a+(f(s)||0),0),dz=sum(s=>s.days),hab={};
  M.forEach(s=>s.hab.forEach(x=>{const o=hab[x.t]=hab[x.t]||{t:x.t,e:x.e,n:0,best:0};o.n+=x.n;o.best=Math.max(o.best,x.best)}));
  const hl=Object.values(hab).sort((a,b)=>b.n-a.n),bm=M.slice().sort((a,b)=>b.avg-a.avg)[0];
  return{y,dz,avg:Math.round(sum(s=>s.avg*s.days)/dz),perfect:sum(s=>s.perfect),bm,hl,hatm:sum(s=>s.hatm),takror:r1(sum(s=>s.takror)),ay:sum(s=>s.ay),zikr:sum(s=>s.zikr),fok:sum(s=>s.fok),npc:Math.round(sum(s=>s.npc*s.days)/dz),qz:sum(s=>s.qz),gd:sum(s=>s.gd),kp:sum(s=>s.kp),kb:sum(s=>s.kb),ig:sum(s=>s.ig),pin:sum(s=>s.pin),pout:sum(s=>s.pout),wl:sum(s=>s.wl),M}}
const mName=m=>MON[m][0].toUpperCase()+MON[m].slice(1);
const yRows=s=>[['Eng yaxshi oy',mName(s.bm.m)+', '+s.bm.avg+'%'],['Mukammal kunlar',s.perfect+' ta'],['Eng barqaror odat',s.hl[0]?(s.hl[0].e+' '+s.hl[0].t+', '+s.hl[0].n+' kun').trim():'—'],['Qur‘on: yodlangan / takror',s.hatm+' / '+s.takror+' bet'],['Namozlar',s.npc+'%'],['Zal',s.gd+' kun'],['Kitob',s.kp+' bet'+(s.kb?', '+s.kb+' ta tugadi':'')],['Instagramsiz',s.ig+' kun'],['Fokus',Math.round(s.fok/60)+' soat'],['Zikr',num(s.zikr)+' marta']];
function wrapped(){
  const y=new Date().getFullYear()+RYo,s=yStats(y);
  const nav=`<div class="in"><button class="btn s" onclick="RYo--;render()">‹</button><button class="btn s" onclick="RYo=0;render()">Shu yil</button><button class="btn s" onclick="RYo++;render()">›</button></div>`;
  if(!s)return nav+`<p class="mu">${y} yil uchun hali ma‘lumot yo‘q.</p>`;
  const bars=s.M.map(m=>`<div style="flex:1;text-align:center"><div style="height:70px;display:flex;align-items:flex-end"><div style="width:100%;height:${Math.max(3,m.avg*.7)}px;background:var(--ac);opacity:.85;border-radius:3px"></div></div><span class="mu" style="font-size:10px">${MON[m.m].slice(0,3)}</span></div>`).join('');
  const hr=s.hl.slice(0,5).map(x=>`<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between"><span>${x.e} ${esc(x.t)}</span><span class="mu">${x.n} kun</span></div><div class="bar"><i style="width:${s.dz?Math.min(100,x.n/s.dz*100):0}%"></i></div></div>`).join('');
  return `${nav}<section class="hero"><p class="lab">${y} YILIM${S.name?', '+esc(S.name.toUpperCase()):''}</p><h1 style="font-size:64px;margin:4px 0">${s.avg}%</h1><p class="mu">o‘rtacha ball, ${s.dz} kun hisoblandi. Eng yaxshi oying: <b style="color:var(--tx)">${mName(s.bm.m)}</b> (${s.bm.avg}%).</p></section>
  <h2>Oylar bo‘yicha</h2><div style="display:flex;gap:3px">${bars}</div>
  ${hr?`<h2>Eng barqaror odatlar</h2>${hr}`:''}
  <h2>Yil raqamlarda</h2>${yRows(s).map(r=>`<div class="row"><span class="t">${r[0]}</span><b>${r[1]}</b></div>`).join('')}
  <h2>Ulashish</h2><button class="row ${RMN?'done':''}" onclick="RMN=!RMN;render()"><span class="ck">${RMN?'✓':''}</span><span class="t">Rasmda pulni ham ko‘rsat</span></button>
  <div class="in" style="margin-top:6px"><button class="btn" style="flex:1" onclick="shareYear()">Rasm qilib ulashish</button></div>`}
async function shareYear(){
  const y=new Date().getFullYear()+RYo,s=yStats(y);if(!s)return;
  const c=document.createElement('canvas');c.width=1080;c.height=1920;const x=c.getContext('2d'),g=x.createLinearGradient(0,0,0,1920);g.addColorStop(0,'#0a1a2c');g.addColorStop(1,'#16466e');x.fillStyle=g;x.fillRect(0,0,1080,1920);
  x.fillStyle='rgba(226,184,87,.08)';for(let i=0;i<8;i++){x.beginPath();x.arc(940,160,160+i*50,0,7);x.fill()}
  x.textBaseline='alphabetic';x.fillStyle='#e2b857';x.font='600 38px Georgia,serif';x.fillText('YILLIK HISOBOT'+(S.name?'  '+S.name.toUpperCase():''),80,130);
  x.fillStyle='#e9eef2';x.font='700 150px Georgia,serif';x.fillText(String(y),80,300);
  const cx=540,cy=560,R=170;x.lineWidth=34;x.strokeStyle='rgba(255,255,255,.12)';x.beginPath();x.arc(cx,cy,R,0,7);x.stroke();x.strokeStyle='#46c4b2';x.lineCap='round';x.beginPath();x.arc(cx,cy,R,-Math.PI/2,-Math.PI/2+Math.PI*2*s.avg/100);x.stroke();
  x.fillStyle='#e9eef2';x.textAlign='center';x.font='700 110px Georgia,serif';x.fillText(s.avg+'%',cx,cy+36);x.font='500 32px sans-serif';x.fillStyle='#8fa6ba';x.fillText('o‘rtacha ball',cx,cy+96);x.textAlign='left';
  const rows=yRows(s);if(RMN)rows.push(['Pul balansi',num(s.pin-s.pout)+' so‘m']);
  rows.forEach((r,i)=>{const yy=860+i*88;x.fillStyle='rgba(255,255,255,.06)';x.fillRect(80,yy-54,920,72);x.fillStyle='#8fa6ba';x.font='500 30px sans-serif';x.fillText(r[0],104,yy-6);x.fillStyle='#e9eef2';x.font='700 32px sans-serif';x.textAlign='right';x.fillText(r[1],976,yy-6);x.textAlign='left'});
  x.fillStyle='#e2b857';x.font='600 32px Georgia,serif';x.textAlign='center';x.fillText('KUNLIK TIZIM BY AZIMOV',540,1850);
  const blob=await new Promise(r=>c.toBlob(r,'image/png')),f=new File([blob],'yillik-hisobot-'+y+'.png',{type:'image/png'});
  try{if(navigator.canShare&&navigator.canShare({files:[f]})){await navigator.share({files:[f],title:'Yillik hisobot'});return}}catch(e){if(e&&e.name==='AbortError')return}
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=f.name;document.body.appendChild(a);a.click();a.remove()}

// ---- IELTS: AI tekshiruvi (Writing va Speaking) ----
let WFB=null,WBUSY=false,SFB=null,SBUSY=false,SREC=null,SOP=0;
function fbGet(src){return src==='w'?WFB:src==='s'?SFB:((S.ie.wr.find(x=>String(x.id)===String(src))||{}).fb||(S.ie.tests.find(x=>String(x.id)===String(src))||{}).fb)||null}
function fbWord(src,i){const f=fbGet(src),v=f&&f.vocab&&f.vocab[i];if(!v||!v.w)return;
  if(S.ie.words.some(x=>sn(x.w)===sn(v.w))){toast('Bu so‘z lug‘atda bor');return}
  S.ie.words.push({id:Date.now()+i,w:String(v.w).trim(),m:String(v.m||'').trim(),box:0,due:dk(),t:0});toast('Lug‘atga qo‘shildi ✓');save()}
function ieFb(f,src){
  if(!f)return '';
  const crit=(f.criteria||[]).map(c=>`<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between;gap:8px"><b>${esc(c.k)}</b><b>${esc(String(c.b))}</b></div><div class="bar" style="margin:4px 0"><i style="width:${Math.min(100,(+c.b||0)/9*100)}%"></i></div><span class="mu" style="font-size:13px">${esc(c.n||'')}</span></div>`).join('');
  const errs=(f.errors||[]).map(e=>`<div class="fbe"><div class="fbo">${esc(e.o||'')}</div><div class="fbc">${esc(e.c||'')}</div><div class="mu" style="font-size:13px">${esc(e.w||'')}</div></div>`).join('');
  const ul=a=>(a&&a.length)?`<ul style="margin:6px 0 0;padding-left:20px;line-height:1.5">${a.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:'';
  const vocab=(f.vocab||[]).map((v,i)=>`<div class="row"><span class="t"><b>${esc(v.w||'')}</b><br><span class="mu">${esc(v.m||'')}</span></span><button class="btn s" style="padding:6px 10px" onclick="fbWord('${src}',${i})">+ Lug‘at</button></div>`).join('');
  return `<section class="hero" style="margin-top:12px"><p class="lab">🤖 AI bahosi (taxminiy)</p><h1 style="font-size:56px;margin:2px 0">${esc(String(f.band))}</h1><p class="mu">Rasmiy imtihonda ball farq qilishi mumkin. Bu mashq uchun yo‘l ko‘rsatkich.</p></section>
  ${ieSpM(f)}${f.transcript?`<details class="goal" style="margin-top:8px"><summary style="font-weight:600">Sen aytganing (transkript)</summary><p style="margin:8px 0 0;white-space:pre-wrap;line-height:1.5">${esc(f.transcript)}</p></details>`:''}
  <h2>Mezonlar bo‘yicha</h2><div class="goal">${crit}</div>
  ${errs?`<h2>Xatolar va tuzatishlar</h2>${errs}`:''}
  ${(f.strengths&&f.strengths.length)?`<h2>Yaxshi tomonlar</h2><div class="goal">${ul(f.strengths)}</div>`:''}
  ${(f.improve&&f.improve.length)?`<h2>Nimani yaxshilash kerak</h2><div class="goal">${ul(f.improve)}</div>`:''}
  ${f.better?`<h2>Yaxshilangan variant</h2><div class="goal" style="white-space:pre-wrap;line-height:1.55">${esc(f.better)}</div>`:''}
  ${vocab?`<h2>Foydali so‘zlar</h2>${vocab}`:''}`}
async function wAI(){const text=(S.ie.dr||'').trim(),n=wcount(text);
  if(n<40){alert('Avval inshoni yozing (kamida 40 so‘z).');return}if(!sb||!UID){alert('AI uchun hisobga kirgan bo‘lish kerak.');return}
  WBUSY=true;WFB=null;render();
  try{const d=await fnAI({action:'ielts',kind:'writing',task:WE.k,prompt:WE.p||'',text}),f=parseJson(d.text);if(!f||!f.band)throw new Error('AI javobini tushunib bo‘lmadi. Qayta urinib ko‘ring.');WFB=f}
  catch(e){alert(e.message)}
  WBUSY=false;render()}
function spMax(){return SPQ?(SPQ.part===2?120:SPQ.part===3?90:60):60}
async function spRec(){
  if(SREC){SREC.mr.stop();return}
  if(!SPQ)return;if(!aiOk()){alert('AI uchun hisobga kirgan bo‘lish kerak.');return}
  if(!navigator.mediaDevices||!window.MediaRecorder){alert('Bu qurilmada ovoz yozish ishlamaydi.');return}
  let st;try{st=await navigator.mediaDevices.getUserMedia({audio:true})}catch(e){alert('Mikrofonga ruxsat berilmadi. Telefon sozlamalarida ruxsat bering.');return}
  const ch=[],mr=new MediaRecorder(st),t0=Date.now(),part=SPQ.part,question=SPQ.q;SFB=null;
  mr.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};
  const iv=setInterval(()=>{const s=Math.floor((Date.now()-t0)/1000),b=document.getElementById('sprb');if(b)b.textContent='⏹ Tugatish ('+s+' s)';if(s>=spMax())mr.stop()},500);
  mr.onstop=async()=>{clearInterval(iv);SDUR=Math.round((Date.now()-t0)/1000);st.getTracks().forEach(x=>x.stop());SREC=null;SBUSY=true;render();
    try{const blob=new Blob(ch,{type:mr.mimeType||'audio/mp4'});if(blob.size<4000)throw new Error('Ovoz juda qisqa, qayta urinib ko‘ring.');
      const wv=await toWav(blob,12000);let pa=null;try{pa=spPauses(wv)}catch(e2){}
      const d=await fnAI({action:'ielts',kind:'speaking',part,question,audio:b64(wv),mime:'audio/wav'}),f=parseJson(d.text);
      if(!f||!f.band)throw new Error('AI javobini tushunib bo‘lmadi. Qayta urinib ko‘ring.');SFB=f;SFB.pa=pa}
    catch(e){alert(e.message||'Tekshirib bo‘lmadi.')}
    SBUSY=false;render()};
  SREC={mr,t0};mr.start();render()}
function spSaveAI(){if(!SFB||!SPQ)return;const b=+SFB.band||0;S.ie.tests.push({id:Date.now(),d:dk(),k:'S',src:'Speaking, Part '+SPQ.part+' (AI)',b:{S:b},raw:{},fb:Object.assign(SFB,{dur:SDUR,q:SPQ.q})});ieDp().S=1;try{mkRec('S',b)}catch(e){}SPQ=null;SFB=null;if(IT)clearInterval(IT.iv);IT=null;save()}

