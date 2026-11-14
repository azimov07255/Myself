// ---- Talaffuz (US / UK), "o'qib ber", so'zma-so'z yuruvchi subtitr, audiodan avtomatik transkript ----
const ieTts=()=>window.__tts||(typeof speechSynthesis!=='undefined'?speechSynthesis:null);
const ieAcc=()=>S.ie.acc==='uk'?'uk':'us',ieAccLabel=()=>ieAcc()==='uk'?'🗣 UK':'🗣 US';
const IE_VP={us:['Samantha','Ava','Allison','Alex','Google US English','Aria','Jenny','Zira','David'],uk:['Daniel','Serena','Kate','Oliver','Google UK English Female','Google UK English Male','Sonia','Libby','Ryan','Hazel','George']};
function ieVoice(acc,alt){const T=ieTts();if(!T)return null;let V=[];try{V=T.getVoices()||[]}catch(e){}const want=acc==='uk'?'en-gb':'en-us',L=V.filter(v=>String(v.lang||'').replace('_','-').toLowerCase()===want);{const pv=ovPref(L,V,acc,alt);if(pv)return pv}if(!L.length)return null;
  const C=[];for(const p of IE_VP[acc]){const v=L.find(x=>String(x.name).includes(p));if(v&&!C.includes(v))C.push(v)}L.forEach(v=>{if(!C.includes(v)&&v.localService)C.push(v)});L.forEach(v=>{if(!C.includes(v))C.push(v)});return C[alt&&C.length>1?1:0]}
const ieSpk=(s,st)=>`<button class="x" style="font-size:16px;${st||''}" onclick="ieSay(${JSON.stringify(String(s)).replace(/"/g,'&quot;')})" aria-label="Eshitish">🔊</button>`;
const ieAccChip=()=>`<button class="chip accchip" onclick="ieAccToggle()" aria-label="Talaffuz: US yoki UK">${ieAccLabel()}</button>`;
function ieSay(t,o){o=o||{};const T=ieTts();if(!T)return null;try{if(IRA&&!o.rd)ieReadPause();const acc=ieAcc(),u=new SpeechSynthesisUtterance(String(t));u.lang=acc==='uk'?'en-GB':'en-US';const v=ieVoice(acc,o.alt);if(o.pitch)u.pitch=o.pitch;if(v){u.__voice=v;try{u.voice=v}catch(e){}}u.rate=o.rate||(S.ie.slow?0.65:0.92);if(o.onend)u.onend=o.onend;if(o.onstart)u.onstart=o.onstart;if(o.onboundary)u.onboundary=o.onboundary;T.cancel();T.speak(u);return u}catch(e){return null}}
function ieAccToggle(){S.ie.acc=ieAcc()==='us'?'uk':'us';const miss=!ieVoice(ieAcc());try{localStorage.setItem(KEY(),JSON.stringify(S))}catch(e){}
  document.querySelectorAll('.accchip').forEach(x=>x.textContent=ieAccLabel());if(miss)toast(ieAcc()==='uk'?'UK ovozi bu qurilmada topilmadi: standart ovoz ishlatiladi.':'US ovozi bu qurilmada topilmadi: standart ovoz ishlatiladi.');else ieSay(ieAcc()==='uk'?'Hello, this is the British voice.':'Hello, this is the American voice.');clearTimeout(tm);tm=setTimeout(push,700)}
function ieSlowToggle(){S.ie.slow=S.ie.slow?0:1;try{localStorage.setItem(KEY(),JSON.stringify(S))}catch(e){}document.querySelectorAll('.slwchip').forEach(x=>{x.textContent='🐢 '+(S.ie.slow?'sekin':'oddiy');x.setAttribute('aria-pressed',S.ie.slow?'true':'false')});clearTimeout(tm);tm=setTimeout(push,700)}
// ---- o'qib berish: gapma-gap, o'qilayotgan joy ko'rinib turadi, to'xtatib davom ettirsa shu gapdan boshlanadi ----
let IRA=null,IRP=null,IRH=null,IRQ=0;   // IRA: hozirgi holat; IRP: oxirgi to'xtagan joy {id,p,s}; IRH: oxirgi bosilgan joy (shu gapdan o'qish uchun)
function ieUnits(el){const txt=el.textContent,U=[];let c=0;el.querySelectorAll('.iew,mark').forEach(n=>{const w=n.textContent,i=txt.indexOf(w,c);if(i<0)return;U.push({n,s:i,e:i+w.length});c=i+w.length});return U}
function ieSents(txt){const a=[],re=/[^.!?\n]+(?:[.!?]+["”’')\]]*|\n|$)/g;let m;while((m=re.exec(txt))){const lead=m[0].match(/^\s*/)[0].length,tr=m[0].trim();if(tr.length)a.push({a:m.index+lead,b:m.index+lead+tr.length})}return a.length?a:[{a:0,b:txt.length}]}
const ieRdEls=()=>[...document.querySelectorAll('#iemb .iep')];
const ieSentAt=(S,off)=>{let k=S.findIndex(x=>off>=x.a&&off<x.b);if(k<0){k=0;for(let i=0;i<S.length;i++)if(S[i].a<=off)k=i}return k};   // gap boshidagi so'z shu gapga tegishli
function ieRdPos(node){try{const p=node&&node.closest&&node.closest('.iep');if(!p)return null;const r=document.createRange();r.selectNodeContents(p);r.setEnd(node,0);return{p:ieRdEls().indexOf(p),s:ieSentAt(ieSents(p.textContent),r.toString().length)}}catch(e){return null}}
const ieRpGet=m=>IRP&&IRP.id===m.id?IRP:(m.rp?{id:m.id,p:m.rp[0],s:m.rp[1]}:null);
function ieReadHiClear(){document.querySelectorAll('#iemb .ts,#iemb .tts,#iemb .wp').forEach(x=>x.classList.remove('ts','tts','wp'))}
function ieWordHiU(U,pos){let j=-1;for(let q=0;q<U.length;q++){if(U[q].s<=pos)j=q;else break}document.querySelectorAll('#iemb .wp').forEach(x=>x.classList.remove('wp'));if(j>=0)U[j].n.classList.add('wp')}
function ieReadHi(){if(!IRA||!IRA.cur)return;const els=ieRdEls(),el=els[IRA.p];if(!el)return;const txt=el.textContent,S=ieSents(txt),sn=S[IRA.s];if(!sn)return;const U=ieUnits(el),inS=U.filter(u=>u.s>=sn.a&&u.e<=sn.b+1);IRA.cur.el=el;IRA.cur.U=U;IRA.cur.inS=inS;
  document.querySelectorAll('#iemb .ts,#iemb .tts').forEach(x=>x.classList.remove('ts','tts'));(el.closest('.iecu')||el).classList.add('tts');inS.forEach(u=>u.n.classList.add('ts'));if(inS[0])ieScrollView(inS[0].n)}
function ieReadBtn(){const b=document.getElementById('irabtn'),m=ieM().find(x=>x.id===IMT);if(!b)return;const rp=m&&ieRpGet(m);b.textContent=IRA&&!IRA.paused?'⏸ Pauza':rp?'▶ Davom ettirish':'🔊 O‘qib ber';const r=document.getElementById('irarst');if(r)r.style.display=(IRA||rp)?'':'none'}
const ieReadBtnHtml=m=>`<button class="chip" id="irabtn" onclick="ieReadAll()">${IRA&&!IRA.paused?'⏸ Pauza':ieRpGet(m)?'▶ Davom ettirish':'🔊 O‘qib ber'}</button><button class="chip" id="irarst" style="${IRA||ieRpGet(m)?'':'display:none'}" onclick="ieReadFrom(0,0)">⏮ Boshidan</button>`;
const ieHereBtn=()=>IRH&&IRH.p>=0?'<button class="btn s" style="width:100%;margin-top:6px" onclick="ieReadHere()">▶ Shu gapdan o‘qib ber</button>':'';
function ieReadHere(){if(!IRH)return;ieSheetClose();ieReadFrom(IRH.p,IRH.s)}
function ieReadAll(){if(IRA&&!IRA.paused){ieReadPause();return}const m=ieM().find(x=>x.id===IMT),rp=m&&ieRpGet(m);ieReadFrom(rp?rp.p:0,rp?rp.s:0)}
function ieReadFrom(p,s){const els=ieRdEls();if(!els.length)return;if(!ieTts()){toast('Bu qurilmada ovoz chiqarish yo‘q.');return}if(IRA)try{ieTts().cancel()}catch(e){}ieReadHiClear();IRA={p:Math.max(0,Math.min(p||0,els.length-1)),s:s||0,tok:(IRA?IRA.tok:0)+1,paused:0,cps:(IRA&&IRA.cps)||13};ieReadSent()}
function ieReadSave(){if(!IRA)return;const m=ieM().find(x=>x.id===IMT);IRP={id:IMT,p:IRA.p,s:IRA.s};if(m){m.rp=[IRA.p,IRA.s];qsave()}}
function ieReadPause(){if(!IRA||IRA.paused)return;IRA.paused=1;IRA.tok++;try{const T=ieTts();T&&T.cancel()}catch(e){}ieReadSave();ieReadBtn()}
function ieReadDone(){const m=ieM().find(x=>x.id===IMT);IRA=null;IRP=null;if(m&&m.rp){m.rp=null;qsave()}ieReadHiClear();ieReadBtn()}
function ieReadSent(){if(!IRA)return;const els=ieRdEls(),el=els[IRA.p];if(!el){ieReadDone();return}const txt=el.textContent,S=ieSents(txt),sn=S[IRA.s];if(!sn){IRA.p++;IRA.s=0;ieReadSent();return}
  const tok=++IRA.tok,sentence=txt.slice(sn.a,sn.b);IRA.cur={el,sn,U:[],inS:[],t0:0,b:0};document.querySelectorAll('#iemb .wp').forEach(x=>x.classList.remove('wp'));ieReadHi();ieReadSave();
  ieSay(sentence,{rd:1,onstart:()=>{if(IRA&&IRA.tok===tok){IRA.cur.t0=performance.now();ieReadTickStart()}},
    onboundary:e=>{if(!(IRA&&IRA.tok===tok)||(e.name&&e.name!=='word'))return;IRA.cur.b=1;ieWordHiU(IRA.cur.inS,sn.a+(e.charIndex||0))},
    onend:()=>{if(!(IRA&&IRA.tok===tok))return;const dt=IRA.cur.t0?(performance.now()-IRA.cur.t0)/1000:0;if(dt>0.3&&sentence.length>12)IRA.cps=IRA.cps*0.5+(sentence.length/dt)*0.5;IRA.s++;ieReadSent()}});ieReadBtn()}
// boundary hodisasi kelmaydigan ovozlarda (ko'p telefonlarda) so'zlar taxminiy vaqt bo'yicha ajraladi; tezlik har gapdan keyin aniqlashadi
function ieReadTickAt(sec){const c=IRA&&IRA.cur;if(!c||c.b)return;ieWordHiU(c.inS,c.sn.a+Math.min(c.sn.b-c.sn.a,Math.max(0,sec)*IRA.cps))}
function ieReadTickStart(){if(IRQ)return;const loop=()=>{if(IRA&&!IRA.paused&&IRA.cur&&IRA.cur.t0&&!IRA.cur.b)ieReadTickAt((performance.now()-IRA.cur.t0)/1000);IRQ=IRA&&!IRA.paused?requestAnimationFrame(loop):0};IRQ=requestAnimationFrame(loop)}
// ---- so'zma-so'z yuruvchi subtitr (audio chalinayotganda) ----
let IWF=0,IWC=null;
const ieTok=s=>(String(s).match(/[A-Za-z0-9’']+/g)||[]);
function ieWFUnits(m,i){const el=document.getElementById('icu'+i);if(!el)return null;const p=el.querySelector('.iep');if(!p)return null;const U=[...p.querySelectorAll('.iew,mark')],c=m.c[i],ws=c[3],cnt=U.map(n=>Math.max(1,ieTok(n.textContent).length)),st=[];
  if(Array.isArray(ws)&&ws.length){let k=0;U.forEach((n,j)=>{st.push(ws[Math.min(k,ws.length-1)]);k+=cnt[j]})}
  else{const w=U.map(n=>n.textContent.length+1),tw=w.reduce((a,b)=>a+b,0)||1;let acc=0;U.forEach((n,j)=>{st.push(c[0]+(c[1]-c[0])*acc/tw);acc+=w[j]})}
  return{i,U,st,last:-1}}
function ieWFAt(t){const m=ieM().find(x=>x.id===IMT);if(!m||IMC<0||!m.c[IMC])return;if(!IWC||IWC.i!==IMC){document.querySelectorAll('#iemb .wp').forEach(x=>x.classList.remove('wp'));IWC=ieWFUnits(m,IMC);if(!IWC)return}
  let j=-1;for(let q=IWC.st.length-1;q>=0;q--)if(t>=IWC.st[q]-0.02){j=q;break}if(j!==IWC.last){if(IWC.last>=0&&IWC.U[IWC.last])IWC.U[IWC.last].classList.remove('wp');if(j>=0)IWC.U[j].classList.add('wp');IWC.last=j}}
function ieWF(){const a=ieAu();if(a&&!a.paused)ieWFAt(a.currentTime)}
function ieWFStart(){if(IWF)return;const loop=()=>{ieWF();IWF=requestAnimationFrame(loop)};IWF=requestAnimationFrame(loop)}
function ieWFStop(){if(IWF)cancelAnimationFrame(IWF);IWF=0}
function ieWFAttach(a){a.addEventListener('play',ieWFStart);a.addEventListener('pause',ieWFStop);a.addEventListener('ended',ieWFStop);a.addEventListener('seeked',()=>{IWC=null;ieWFAt(a.currentTime)})}
// ---- audiodan avtomatik transkript (server: Groq Whisper, so'z vaqtlari bilan) ----
let ITR=null;
async function fnUpload(fields,blob,name,ms){const s=await aiSession();if(!s)throw new Error('Hisobga qayta kiring.');const fd=new FormData();Object.keys(fields).forEach(k=>fd.append(k,fields[k]));fd.append('file',blob,name||'audio.mp3');
  const ctl=new AbortController(),to=setTimeout(()=>ctl.abort(),ms||130000);let res;
  try{res=await fetch(CFG.url+'/functions/v1/ai-assistant',{method:'POST',signal:ctl.signal,headers:{'Authorization':'Bearer '+s.access_token,'apikey':CFG.key},body:fd})}catch(e){clearTimeout(to);throw new Error(e&&e.name==='AbortError'?'Transkript juda uzoq davom etdi. Qisqaroq audio bilan urinib ko‘ring.':'Serverga ulanib bo‘lmadi. Internetni tekshiring.')}
  clearTimeout(to);let j=null;try{j=JSON.parse(await res.text())}catch(e){}
  if(!res.ok){let m=(j&&(j.error||j.message))||'';if(res.status===404)m='AI funksiyasi topilmadi. Supabase’da “ai-assistant” funksiyasi borligini tekshiring.';else if(res.status===401&&!m)m='Hisobga qayta kiring.';throw new Error(m||('Server xatosi ('+res.status+')'))}
  if(!j)throw new Error('Server javobi tushunarsiz.');aiCount(1,'transcript');return j}
const ieNormW=s=>String(s).toLowerCase().replace(/[’]/g,"'").replace(/[^a-z0-9']/g,'');
function ieAlign(text,w,s,e){const T=ieTok(text),W=(Array.isArray(w)?w:[]).map(x=>({n:ieNormW(x[0]),s:+x[1]})).filter(x=>x.n&&isFinite(x.s)),out=[];let j=0;
  T.forEach(tk=>{const n=ieNormW(tk);let f=-1;for(let k=j;k<Math.min(W.length,j+4);k++)if(W[k].n===n){f=k;break}if(f>=0){out.push(W[f].s);j=f+1}else out.push(null)});
  if(out.length&&out[0]===null)out[0]=s;
  for(let i=0;i<out.length;i++)if(out[i]===null){let a=i-1;while(a>=0&&out[a]===null)a--;let b=i+1;while(b<out.length&&out[b]===null)b++;const t0=a>=0?out[a]:s,t1=b<out.length?out[b]:e,na=a>=0?a:-1,nb=b<out.length?b:out.length;out[i]=t0+(t1-t0)*((i-na)/(nb-na))}
  return out.map(x=>Math.round(Math.max(s,Math.min(e,x))*100)/100)}
const ieAudExt=t=>/mp4|m4a|aac/.test(t)?'.m4a':/wav/.test(t)?'.wav':/ogg|opus/.test(t)?'.ogg':/webm/.test(t)?'.webm':/flac/.test(t)?'.flac':'.mp3';
async function ieTranscribe(id){const m=ieM().find(x=>x.id===id);if(!m||(ITR&&ITR.busy))return;ITR={id,busy:1,err:''};ieMatDraw();
  try{const blob=await ieAudGet(m);let d;if(blob){if(blob.size>24*1048576)throw new Error('Audio 24 MB dan katta (bepul chegara 25 MB).');d=await fnUpload({action:'transcript'},blob,'audio'+ieAudExt(blob.type||''))}else if(m.ar)d=await fnPost({action:'transcript',url:m.ar},130000);else throw new Error('Audio bu qurilmada topilmadi.');if(!Array.isArray(d.cues)||!d.cues.length)throw new Error('Transkript bo‘sh chiqdi.');
    m.c=d.cues.map(c=>{const s=+c.s||0,e=Math.max(s+0.1,+c.e||s+1),t=String(c.t||'').trim();return [Math.round(s*100)/100,Math.round(e*100)/100,t,ieAlign(t,c.w,s,e)]}).filter(c=>c[2]);
    m.x='';m.tr=1;m.an=null;ITR=null;toast('Transkript tayyor: '+m.c.length+' qator');save()}
  catch(e){ITR={id,busy:0,err:String(e.message||e).slice(0,220)}}if(ITR)ITR.busy=0;ieMatDraw()}
function ieTrAgain(id){if(confirm('Hozirgi matn va tahlil o‘chiriladi, audio qayta transkript qilinadi. Davom etilsinmi?')){const m=ieM().find(x=>x.id===id);if(m){m.c=[];m.x='';m.an=null;ieTranscribe(id)}}}
function ieVoiceBar(m){const full=ieText(m).length>0,busy=ITR&&ITR.busy&&ITR.id===m.id,need=m.au&&!(m.c&&m.c.length);
  return `<div class="ieb" style="flex-wrap:wrap">${ieAccChip()}<button class="chip slwchip" onclick="ieSlowToggle()" aria-pressed="${S.ie.slow?'true':'false'}">🐢 ${S.ie.slow?'sekin':'oddiy'}</button>${full?ieReadBtnHtml(m):''}${full?'<button class="chip" onclick="mzOpen()">📝 Savollar</button>':''}${full?glChip(m):''}${full?`<button class="chip" onclick="rvOpen(${m.id})">⚡ Tezlik</button>`:''}${m.au&&m.c&&m.c.length&&m.tr?`<button class="chip" onclick="ieTrAgain(${m.id})">↻ Qayta transkript</button>`:''}</div>
   ${need&&ieAlOk(m)?ieAlCard(m):''}${need&&!ieAlOk(m)?`<div class="goal"><b>🤖 Avtomatik transkript</b><p class="mu" style="margin:6px 0 8px">Audiodan matn va <b>har bir so‘zning vaqti</b> olinadi: chalinayotganda so‘zlar birga ajralib yuradi. 1 ta so‘rov, audio 24 MB gacha (Groq Whisper).</p><button class="big" style="margin-top:0" onclick="ieTranscribe(${m.id})" ${busy?'disabled':''}>${busy?'Transkript qilinmoqda… (1–2 daqiqagacha)':'Transkript qilish'}</button></div>`:''}${ITR&&ITR.id===m.id&&ITR.err?`<p style="color:var(--bad);margin:6px 0">${esc(ITR.err)}</p>`:''}`}
