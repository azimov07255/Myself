// ================= QUR'ON AUDIO PLEYERI =================
let QA={id:null,url:null,a:null,b:null,sl:null,drag:0};
const qaItem=()=>S.qa.list.find(x=>x.id===QA.id);
function qaEl(){let a=document.getElementById('qau');
  if(!a){a=document.createElement('audio');a.id='qau';a.preload='metadata';a.setAttribute('playsinline','');document.body.appendChild(a);
    a.addEventListener('timeupdate',qaTick);a.addEventListener('ended',qaEnd);a.addEventListener('play',qaSync);a.addEventListener('pause',qaSync);a.addEventListener('ratechange',qaPos);a.addEventListener('seeked',qaPos);
    a.addEventListener('loadedmetadata',()=>{const t=qaItem();if(t&&a.duration&&isFinite(a.duration)){t.dur=Math.round(a.duration);qsave()}
      if(QA.resume>2&&a.duration&&QA.resume<a.duration-3)a.currentTime=QA.resume;QA.resume=0;qaSync()})}
  return a}
function qaPos(){try{const a=qaEl();if('mediaSession' in navigator&&navigator.mediaSession.setPositionState&&a.duration&&isFinite(a.duration))navigator.mediaSession.setPositionState({duration:a.duration,playbackRate:a.playbackRate||1,position:Math.min(a.currentTime,a.duration)})}catch(e){}}
function qaSync(){qaPos();try{if('mediaSession' in navigator)navigator.mediaSession.playbackState=qaEl().paused?'paused':'playing'}catch(e){}qaBarUpd();if(tab==='q'&&QT==='a')render()}
function qaTick(){const a=qaEl(),t=qaItem();if(!t)return;
  if(QA.b!=null&&a.currentTime>=QA.b){a.currentTime=QA.a||0;qaPos()}
  if(Date.now()-(QA.pp||0)>1000){QA.pp=Date.now();qaPos()}
  const n=Date.now();if(n-(QA.sv||0)>5000){QA.sv=n;t.pos=Math.floor(a.currentTime);qsave()}
  const e=document.getElementById('qaT');if(e)e.textContent=fmtT(Math.floor(a.currentTime))+' / '+fmtT(Math.floor(a.duration||t.dur||0));
  const r=document.getElementById('qaR');if(r&&!QA.drag){r.max=Math.floor(a.duration||t.dur||0);r.value=Math.floor(a.currentTime)}}
function qaEnd(){const a=qaEl(),t=qaItem();if(!t)return;const m=S.qa.rep;
  if(m==='one'){a.currentTime=0;a.play().catch(()=>{});return}
  t.pos=0;if(m==='all'){qaStep(1,true);return}qsave();qaSync()}
async function qaAdd(inp){const fs=[...(inp.files||[])];inp.value='';
  for(const f of fs){const big=f.size>50*1024*1024;if(big)alert(f.name+': 50 MB dan katta, faqat shu telefonda saqlanadi (bulutga yuklanmaydi).');
    const id='a'+Date.now()+Math.floor(Math.random()*1000);
    try{await idbSet(id,{b:await f.arrayBuffer(),t:f.type||'audio/mpeg'})}catch(e){alert('Saqlab bo‘lmadi: '+f.name);continue}
    S.qa.list.push({id,n:f.name.replace(/\.[a-z0-9]+$/i,''),sz:f.size,t:f.type||'audio/mpeg',pos:0,dur:0,cloud:0});save();
    if(sb&&UID&&!big){if(cloudOk(f.size))qaUp(id,f);else toast('Bulut limiti to‘ldi: fayl faqat shu telefonda saqlandi')}}}
async function qaUp(id,f){const t=S.qa.list.find(x=>x.id===id);if(!t)return;PUPL[id]=1;render();
  try{const r=await sb.storage.from('books').upload(UID+'/a/'+id,f,{upsert:true,contentType:f.type||'audio/mpeg'});if(r.error)throw r.error;t.cloud=1;save()}catch(e){toast('Bulutga yuklanmadi: '+(e.message||e))}
  delete PUPL[id];render()}
async function qaPlay(id){const t=S.qa.list.find(x=>x.id===id);if(!t)return;const a=qaEl();
  if(QA.id===id&&a.src){if(a.paused)a.play().catch(()=>{});else a.pause();return}
  let rec=null;try{rec=await idbGet(id)}catch(e){}
  if(!rec&&t.cloud&&sb&&UID){toast('Yuklab olinmoqda...');const r=await sb.storage.from('books').download(UID+'/a/'+id);if(!r.error){const b=await r.data.arrayBuffer();rec={b,t:t.t};try{await idbSet(id,rec)}catch(e){}}}
  if(!rec){alert('Bu qurilmada fayl topilmadi.');return}
  if(QA.url)try{URL.revokeObjectURL(QA.url)}catch(e){}
  QA={id,url:URL.createObjectURL(new Blob([rec.b],{type:rec.t||'audio/mpeg'})),a:null,b:null,sl:QA.sl,drag:0,resume:t.pos||0};
  a.src=QA.url;a.playbackRate=S.qa.rate||1;a.play().catch(()=>{});
  if('mediaSession' in navigator){try{navigator.mediaSession.metadata=new MediaMetadata({title:t.n,artist:'Kunlik tizim'});
    const A=(k,f)=>{try{navigator.mediaSession.setActionHandler(k,f)}catch(e){}};A('play',()=>a.play());A('pause',()=>a.pause());A('seekbackward',e=>qaSeek(-((e&&e.seekOffset)||10)));A('seekforward',e=>qaSeek((e&&e.seekOffset)||10));A('seekto',e=>{if(e&&e.seekTime!=null){if(e.fastSeek&&'fastSeek' in a)a.fastSeek(e.seekTime);else a.currentTime=e.seekTime;qaPos()}});A('previoustrack',()=>qaStep(-1));A('nexttrack',()=>qaStep(1))}catch(e){}}
  render()}
function qaToggle(){const a=qaEl();if(!a.src)return;if(a.paused)a.play().catch(()=>{});else a.pause()}
function qaSeek(d){const a=qaEl();a.currentTime=Math.max(0,Math.min((a.duration||1e9),a.currentTime+d))}
function qaSeekTo(v){qaEl().currentTime=+v||0}
function qaRate(r){S.qa.rate=r;qaEl().playbackRate=r;save()}
function qaRep(m){S.qa.rep=m;save()}
function qaStep(d,auto){const L=S.qa.list;if(!L.length)return;let i=L.findIndex(x=>x.id===QA.id);i=i<0?0:i+d;if(i>=L.length){if(!auto&&d>0)return;i=0}if(i<0)i=0;qaPlay(L[i].id)}
function qaAB(){const a=qaEl();if(QA.a==null){QA.a=a.currentTime;QA.b=null}else if(QA.b==null){if(a.currentTime>QA.a+0.5)QA.b=a.currentTime;else QA.a=a.currentTime}else{QA.a=null;QA.b=null}render()}
function qaSleep(min){if(QA.sl&&QA.sl.tm)clearTimeout(QA.sl.tm);if(!min){QA.sl=null;render();return}QA.sl={end:Date.now()+min*60000,tm:setTimeout(()=>{qaEl().pause();QA.sl=null;render()},min*60000)};render()}
function qaDel(id){if(!confirm('Audio o‘chirilsinmi?'))return;if(QA.id===id){qaEl().pause();qaEl().removeAttribute('src');QA={id:null,url:null,a:null,b:null,sl:null,drag:0};qaBarUpd()}
  S.qa.list=S.qa.list.filter(x=>x.id!==id);idbDel(id).catch(()=>{});if(sb&&UID)sb.storage.from('books').remove([UID+'/a/'+id]).catch(()=>{});save()}
function qaRename(id){const t=S.qa.list.find(x=>x.id===id),n=prompt('Audio nomi:',t.n);if(n&&n.trim()){t.n=n.trim();save()}}
function qaStop(){const a=qaEl();a.pause();a.removeAttribute('src');QA={id:null,url:null,a:null,b:null,sl:QA.sl,drag:0};qaBarUpd();if(tab==='q'&&QT==='a')render()}
let QB=(()=>{try{return JSON.parse(localStorage.getItem('trk_qab')||'null')}catch(e){return null}})()||{x:null,y:null,c:0,s:'r'};
const qbSave=()=>{try{localStorage.setItem('trk_qab',JSON.stringify({x:QB.x,y:QB.y,c:QB.c,s:QB.s}))}catch(e){}};
function qbPlace(b){const W=window.innerWidth||390,H=window.innerHeight||800,w=QB.c?46:Math.min(W-16,300),h=QB.c?46:56;let x=QB.x,y=QB.y;
  if(x==null||y==null){x=(W-w)/2;y=H-h-100}
  if(QB.c){x=QB.s==='l'?-14:W-w+14;y=Math.max(60,Math.min(H-h-90,y))}else{x=Math.max(8,Math.min(W-w-8,x));y=Math.max(50,Math.min(H-h-8,y))}
  b.style.left=x+'px';b.style.top=y+'px';b.style.width=w+'px';b.style.height=h+'px'}
function qbTuck(){const W=window.innerWidth||390,b=document.getElementById('qab');const cx=b?b.offsetLeft+b.offsetWidth/2:W;QB.s=cx<W/2?'l':'r';QB.c=1;qbSave();qaBarUpd(true)}
function qbInit(b){if(b._i)return;b._i=1;let d=null;
  b.addEventListener('pointerdown',e=>{if(e.target.closest('[data-nodrag]'))return;d={x:e.clientX,y:e.clientY,l:b.offsetLeft,t:b.offsetTop,m:0};try{b.setPointerCapture(e.pointerId)}catch(x){}});
  b.addEventListener('pointermove',e=>{if(!d)return;const dx=e.clientX-d.x,dy=e.clientY-d.y;if(!d.m&&Math.hypot(dx,dy)<6)return;d.m=1;
    const W=window.innerWidth,H=window.innerHeight;QB.x=Math.max(-20,Math.min(W-26,d.l+dx));QB.y=Math.max(40,Math.min(H-60,d.t+dy));b.style.left=QB.x+'px';b.style.top=QB.y+'px'});
  const end=e=>{if(!d)return;const moved=d.m;d=null;try{b.releasePointerCapture(e.pointerId)}catch(x){}
    const W=window.innerWidth,w2=Math.min(W-16,300);
    if(moved){const px=e.clientX;
      if(px<44||px>W-44){QB.c=1;QB.s=px<W/2?'l':'r';QB.y=b.offsetTop}   // barmoq chetga yetganda yig‘iladi
      else{QB.c=0;QB.x=Math.max(8,Math.min(W-w2-8,px-w2/2));QB.y=b.offsetTop}   // aks holda shu joyda ochiladi
      qbSave();qaBarUpd(true)}
    else if(QB.c){QB.c=0;QB.x=QB.s==='l'?8:W-w2-8;qbSave();qaBarUpd(true)}   // bosilsa, qaytadan ochiladi
    else if(e.target.closest('.qa-t')){QT='a';go('q')}};
  b.addEventListener('pointerup',end);b.addEventListener('pointercancel',end)}
function qaBarUpd(force){let b=document.getElementById('qab');const a=document.getElementById('qau'),t=QA.id&&a&&a.src?qaItem():null,show=t&&!(tab==='q'&&QT==='a'&&!document.getElementById('ai'));
  if(!show){if(b)b.remove();return}
  if(!b){b=document.createElement('div');b.id='qab';document.body.appendChild(b);qbInit(b)}
  const cls='qab'+(QB.c?' qbc':''),html=QB.c?`<button class="qa-bub" aria-label="Pleyerni ochish">${a.paused?'🎧':'⏸'}</button>`:`<span class="qa-g" aria-hidden="true">⠿</span><span class="qa-t">🎧 ${esc(t.n)}</span><button data-nodrag onclick="qaToggle()" aria-label="Ijro">${a.paused?'▶':'⏸'}</button><button data-nodrag onclick="qbTuck()" aria-label="Chetga yig‘ish">⇥</button><button data-nodrag onclick="qaStop()" aria-label="Yopish">✕</button>`;
  if(b.className!==cls)b.className=cls;if(b._h!==html||force){b._h=html;b.innerHTML=html}qbPlace(b)}
function qaView(){
  const L=S.qa.list,a=document.getElementById('qau'),cur=QA.id?qaItem():null,playing=!!(cur&&a&&a.src&&!a.paused),mb=n=>(n/1048576).toFixed(1)+' MB';
  const sl=QA.sl?Math.max(0,Math.ceil((QA.sl.end-Date.now())/60000)):0;
  const player=cur?`<div class="qa-p"><p class="lab" style="margin:0;color:var(--hlab)">${playing?'IJRO ETILMOQDA':'PAUZA'}</p><h2 class="qa-n">${esc(cur.n)}</h2>
    <input id="qaR" type="range" min="0" max="${Math.floor(cur.dur||0)}" value="${Math.floor((a&&a.currentTime)||cur.pos||0)}" oninput="QA.drag=1" onchange="qaSeekTo(this.value);QA.drag=0" style="width:100%;accent-color:#e2b857">
    <div style="display:flex;justify-content:space-between;font-size:12px;opacity:.8"><span id="qaT">${fmtT(Math.floor((a&&a.currentTime)||0))} / ${fmtT(Math.floor(cur.dur||0))}</span>${QA.a!=null?`<span>🔁 ${fmtT(Math.floor(QA.a))}${QA.b!=null?' – '+fmtT(Math.floor(QA.b)):' – …'}</span>`:''}</div>
    <div class="qa-c"><button onclick="qaStep(-1)" aria-label="Oldingi">⏮</button><button onclick="qaSeek(-15)">−15</button><button class="qa-pp" onclick="qaToggle()">${playing?'⏸':'▶'}</button><button onclick="qaSeek(15)">+15</button><button onclick="qaStep(1)" aria-label="Keyingi">⏭</button></div>
    <div class="qa-r"><span>Tezlik</span>${[0.75,1,1.25,1.5].map(r=>`<button class="${S.qa.rate===r?'on':''}" onclick="qaRate(${r})">${r}×</button>`).join('')}</div>
    <div class="qa-r"><span>Takror</span>${[['off','Yo‘q'],['one','Bitta'],['all','Hammasi']].map(x=>`<button class="${S.qa.rep===x[0]?'on':''}" onclick="qaRep('${x[0]}')">${x[1]}</button>`).join('')}</div>
    <div class="qa-r"><span>Yodlash</span><button class="${QA.a!=null?'on':''}" onclick="qaAB()">${QA.a==null?'A nuqta':QA.b==null?'B nuqta':'Bekor qilish'}</button><small style="opacity:.75">oraliqni takrorlab eshitish</small></div>
    <div class="qa-r"><span>Uyqu taymeri</span>${[15,30,60].map(m=>`<button onclick="qaSleep(${m})">${m} daq</button>`).join('')}${sl?`<button class="on" onclick="qaSleep(0)">${sl} daq ✕</button>`:''}</div></div>`:'';
  const rows=L.map(x=>{const on=QA.id===x.id,pc=x.dur?Math.min(100,(x.pos||0)/x.dur*100):0;
    return `<div class="goal qa-i ${on?'on':''}"><button class="qa-pl" onclick="qaPlay('${x.id}')">${on&&playing?'⏸':'▶'}</button><div style="flex:1;min-width:0"><b style="overflow-wrap:anywhere">${esc(x.n)}</b><div class="mu" style="font-size:12px">${x.dur?fmtT(x.dur)+' · ':''}${mb(x.sz||0)} · ${PUPL[x.id]?'bulutga yuklanmoqda…':x.cloud?'bulutda':'faqat shu telefonda'}</div>${pc>1?`<div class="bar" style="margin-top:6px"><i style="width:${pc}%"></i></div>`:''}</div><button class="x" style="font-size:15px" onclick="qaRename('${x.id}')">✎</button><button class="x" onclick="qaDel('${x.id}')">×</button></div>`}).join('');
  return `<p class="mu" style="margin:0 0 8px">Qur’on tilovati va darslarni yuklab, istalgan paytda eshit. Pozitsiyang eslab qolinadi, ekran qulflansa ham eshitish davom etadi.</p>
  <label class="big" style="display:block;text-align:center;margin:0 0 10px;cursor:pointer">＋ Audio qo‘shish<input type="file" accept="audio/*,.mp3,.m4a,.aac,.wav,.ogg" multiple style="display:none" onchange="qaAdd(this)"></label>
  ${player}${cloudBar()}${rows?`<h2>Audiolarim (${L.length})</h2>${rows}`:'<div class="bn wr">Hali audio yo‘q. Yuqoridagi tugma bilan mp3 yoki m4a fayllarni tanla (har biri 50 MB gacha bulutga ham saqlanadi).</div>'}`}
setInterval(qaBarUpd,800);

