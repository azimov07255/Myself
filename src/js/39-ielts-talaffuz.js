// ---- Talaffuz va shadowing: gapni o'qiysan, ovozing yoziladi, transkript bilan so'zma-so'z solishtiriladi ----
let PT={ref:'',busy:0,rec:null,res:null,heard:'',err:''};
function ptSources(){const out=[];S.ie.words.forEach(w=>[w.c,w.e].forEach(s=>{const n=s?ieTok(s).length:0;if(n>=5&&n<=25)out.push(String(s).trim())}));
  ieM().forEach(m=>{const t=ieText(m);(t.match(/[^.!?\n]+[.!?]/g)||[]).forEach(s=>{const n=ieTok(s).length;if(n>=6&&n<=22)out.push(s.trim())})});return out}
function ptNew(){const L=ptSources();if(!L.length){PT.err='Gap manbasi yo‘q: lug‘atga misolli so‘z qo‘sh, material qo‘sh yoki o‘z gapingni yoz.';PT.ref='';render();return}PT.ref=L[Math.floor(Math.random()*L.length)];PT.res=null;PT.heard='';PT.err='';render()}
function ptOwn(){const v=(V('ptr')||'').trim();if(ieTok(v).length<3){toast('Kamida 3 so‘zli gap yoz.');return}PT.ref=v.slice(0,300);PT.res=null;PT.heard='';PT.err='';render()}
async function ptRec(){if(PT.rec){PT.rec.mr.stop();return}if(!PT.ref)return;if(!aiOk()){toast('Tekshirish uchun hisobga kirish kerak.');return}if(!navigator.mediaDevices||!window.MediaRecorder){toast('Bu qurilmada ovoz yozish ishlamaydi.');return}
  let st;try{st=await navigator.mediaDevices.getUserMedia({audio:true})}catch(e){toast('Mikrofonga ruxsat berilmadi. Telefon sozlamalarida ruxsat bering.');return}
  const ch=[],mr=new MediaRecorder(st);mr.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};PT.rec={mr};PT.err='';PT.res=null;
  mr.onstop=async()=>{st.getTracks().forEach(x=>x.stop());PT.rec=null;await ptCheck(new Blob(ch,{type:mr.mimeType||'audio/mp4'}))};mr.start();render()}
async function ptCheck(blob){PT.busy=1;PT.err='';render();
  try{if(blob.size<1500)throw new Error('Ovoz juda qisqa. Qayta urinib ko‘ring.');const d=await fnUpload({action:'transcript'},blob,'say'+ieAudExt(blob.type||'')),heard=(d.cues||[]).map(c=>c.t).join(' ');if(!heard.trim())throw new Error('Gap eshitilmadi.');PT.heard=heard;PT.res=ieDiff(PT.ref,heard);(S.ie.pt=S.ie.pt||[]).push({d:dk(),p:PT.res.pct,n:PT.res.n});S.ie.pt=S.ie.pt.slice(-60);ieDp().S=1;save()}
  catch(e){PT.err=String(e.message||e).slice(0,200)}PT.busy=0;render()}
function ptUi(){const r=PT.res,hist=(S.ie.pt||[]).slice(-5),avg=hist.length?Math.round(hist.reduce((a,x)=>a+x.p,0)/hist.length):null;
  return `<p class="mu" style="margin:8px 0">Gapni eshit, o‘zing o‘qi (ovozing yoziladi), ilova qaysi so‘zlar aniq chiqmaganini ko‘rsatadi. 1 ta AI so‘rovi (Groq kaliti kerak).</p>
   <div class="in" style="flex-wrap:wrap"><button class="btn s" onclick="ptNew()">🎲 Lug‘at yoki materialdan gap</button></div><div class="in" style="margin-top:6px"><input id="ptr" placeholder="yoki o‘z gapingni yoz" style="flex:1;min-width:0"><button class="btn s" onclick="ptOwn()">Olish</button></div>
   ${PT.err?`<p style="color:var(--bad);margin:8px 0">${esc(PT.err)}</p>`:''}
   ${PT.ref?`<div class="goal"><p style="font:500 19px/1.5 Georgia,serif;margin:0 0 8px">${esc(PT.ref)}</p><div class="in" style="flex-wrap:wrap">${ieAccChip()}<button class="btn s" onclick="ieSay(PT.ref)">🔊 Namuna</button><button class="btn s" onclick="ieSay(PT.ref,{rate:0.6})">🐢 Sekin</button></div>
     <button class="big" style="margin-top:10px" onclick="ptRec()" ${PT.busy?'disabled':''}>${PT.busy?'Tekshirilmoqda…':PT.rec?'⏹ Tugatish':'🎙 O‘qishni boshlash'}</button></div>`:''}
   ${r?`<div class="goal"><div class="h"><b>Natija</b><span style="font:700 22px Fraunces,serif">${r.pct}%</span></div><p class="ietx" style="margin:0 0 8px">${r.parts.map(p=>p.p?esc(p.t):`<span class="${p.ok?'dok':'dno'}">${esc(p.t)}</span>`).join('')}</p><p class="mu" style="margin:0 0 6px">${r.pct>=90?'Ajoyib!':r.pct>=70?'Yaxshi, qizil so‘zlarni mashq qil.':'Yana bir marta urinib ko‘r.'}</p>
     ${r.missed.length?`<div class="rwch">${[...new Set(r.missed.map(x=>x.toLowerCase()))].map(w=>`<button class="chip" style="border:0" onclick="ieSay('${esc(w).replace(/'/g,"\\'")}')">🔊 ${esc(w)}</button>`).join('')}</div>`:''}<details class="sd" style="margin-top:8px"><summary>Ilova nimani eshitdi</summary><p style="margin:6px 0 0">${esc(PT.heard)}</p></details></div>`:''}
   ${avg!==null?`<p class="mu">Oxirgi ${hist.length} urinish o‘rtachasi: <b>${avg}%</b></p>`:''}`}
