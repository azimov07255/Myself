// ---- Mushaf: 15 qatorli Madina mushafi (matn: data/quran-mushaf.json, shrift: fonts/) ----
const mfOn=()=>MUSHAF_MODE!=='off'&&!S.nomf;
function mfToggle(){S.nomf=S.nomf?0:1;if(S.nomf){if(QT==='u')QT='y';if(MFO)mfClose()}save()}
function mfSet(){return `<p class="mu" style="margin:0 0 8px">Qur’on bo‘limidagi 📖 Mushaf (matn, rang, izoh, yodlash sinovi). O‘chirsangiz bo‘lim ko‘rinmaydi va hech narsa yuklanmaydi. Belgilaringiz saqlanib qoladi.</p><button class="btn s" onclick="mfToggle()">${S.nomf?'📖 Mushaf’ni yoqish':'Mushaf’ni o‘chirish'}</button>`}
const MFV='1',MFCOL=['#f5d547','#5dbb63','#5aa9e6','#ef7fa8','#f0944d'];
let MF=null,MFP=null,MFPG=1,MFO=false,MV='s',MQ='',MFT=null,MFTM=0,MFSW=null;
const mq=()=>{const q=S.mq=S.mq||{};q.hl=q.hl||{};q.wk=q.wk||{};q.bm=q.bm||[];q.rec=q.rec||[];if(!q.last)q.last=1;return q};
const vkS=k=>Math.floor(k/1000),vkA=k=>k%1000,vkL=k=>SN[vkS(k)-1]+' '+vkS(k)+':'+vkA(k);
const mfIdx=k=>{let s=0;for(let i=0;i<vkS(k)-1;i++)s+=AY[i];return s+vkA(k)-1};
const mfFix=w=>w.replace(/\u06DF/g,'\u06E0');   // faqat ko‘rsatishda: shrift kichik doirani shu kod bilan to‘g‘ri chizadi (saqlangan matn o‘zgarmaydi)
const mfNum=w=>/^[\u0660-\u0669]+$/.test(w);
const mfSurahAt=p=>{let s=1;for(let i=0;i<114;i++)if(SP[i]<=p)s=i+1;return s};
const mfJuz=p=>J.filter((x,i)=>i<30&&x<=p).length||1;
function mfLoad(){if(MF)return Promise.resolve(MF);if(MFP)return MFP;
  MFP=(async()=>{let d=null;try{d=await idbGet('mf'+MFV)}catch(e){}
    if(!d||!d.p){const r=await fetch('data/quran-mushaf.json');if(!r.ok)throw new Error('HTTP '+r.status);d=await r.json();try{await idbSet('mf'+MFV,d)}catch(e){}}
    MF=d;return d})();MFP.catch(()=>{MFP=null});return MFP}
function mfVerse(k){const D=MF,p0=D.vp[mfIdx(k)],out=[];
  for(let p=p0;p<=Math.min(604,p0+1);p++)for(const r of D.p[p].r){if(r[0]!=='x')continue;let i=0;for(const[kk,c]of r[2]){if(kk===k)for(let j=0;j<c;j++){const w=r[1][i+j];if(!mfNum(w))out.push(w)}i+=c}}
  return out}
function mfPageSurah(n){for(const r of MF.p[n].r)if(r[0]==='x')return vkS(r[2][0][0]);return mfSurahAt(n)}
function mfPageHtml(n,st){
  const D=MF,P=D.p[n];let h='',lastK=0,idx=0;const hl=st.hl||{},wk=st.wk||{},T=st.t;
  if(P.t)h+=`<div class="mr mh">${esc(D.hd[P.t-1])}</div>`;
  for(const r of P.r){
    if(r[0]==='h')h+=`<div class="mr mh">${esc(D.hd[r[1]-1])}</div>`;
    else if(r[0]==='b')h+=`<div class="mr ct mb">${D.bsm.map(w=>`<span class="mw">${esc(mfFix(w))}</span>`).join('')}</div>`;
    else if(r[0]==='e')h+='<div class="mr"></div>';
    else{let i=0,sp='';
      for(const[k,c]of r[2]){
        if(k!==lastK){lastK=k;idx=D.vp[mfIdx(k)]<n?99:0}
        for(let j=0;j<c;j++){const w=r[1][i++],num=mfNum(w);let cl='mw';if(num)cl+=' mk';
          const x=hl[k];if(x&&x.c)cl+=' h'+x.c;if(num&&x&&x.n)cl+=' hn';
          const z=wk[k];if(num&&z&&z.s<2)cl+=' wkm';
          if(T&&T.on&&!T.rev[k]&&!num&&(T.mode==='r'||idx>=2))cl+=' xh';
          if(!num)idx++;
          if(/[\u06E3\u06EB]/.test(w))cl+=' qam';sp+=`<span class="${cl}" data-v="${k}">${esc(mfFix(w))}</span>`}}
      h+=`<div class="mr mx">${sp}</div>`}}
  return h}
function mfFit(){const pg=$('#mfpg');if(!pg||!MF)return;const W=pg.clientWidth-20;if(W<=0)return;
  pg.style.fontSize='20px';pg.classList.add('meas');const rows=[...pg.querySelectorAll('.mx')],ws=rows.map(r=>r.getBoundingClientRect().width);pg.classList.remove('meas');
  const m=Math.max(1,...ws),fs=Math.max(11,Math.min(42,20*W/m*0.995));pg.style.fontSize=fs+'px';
  rows.forEach((r,i)=>r.classList.toggle('ct',ws[i]*fs/20<W*0.7));pg.dataset.fs=fs.toFixed(1)}
function mfDraw(keep){const pg=$('#mfpg');if(!pg||!MF)return;const q=mq(),n=MFPG,sc=$('#mfp');const y=keep&&sc?sc.scrollTop:0;
  pg.className='mpg'+(MF.p[n].c?' cc':'');pg.innerHTML=mfPageHtml(n,{hl:q.hl,wk:q.wk,t:MFT});
  const s=mfPageSurah(n);$('#mfn').textContent=MF.hd[s-1];$('#mfj').textContent='Juz’ '+mfJuz(n)+' · '+n+'-bet';
  const i=$('#mfi');if(i)i.value=n;const b=$('#mfb');if(b)b.textContent=q.bm.includes(n)?'★':'☆';
  const st=$('#mfst');if(st){if(MFT&&MFT.on){st.hidden=false;st.innerHTML=`<span>Sinov: ${MFT.mode==='r'?'faqat raqam':'oyat boshi'} · ✅ ${MFT.st[2]} · ➖ ${MFT.st[1]} · ❌ ${MFT.st[0]}</span><button class="x" onclick="mfTestEnd()">Tugatish</button>`}else st.hidden=true}
  mfFit();if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>{if(MFO)mfFit()});if(sc)sc.scrollTop=y}
async function mfShow(n){n=Math.max(1,Math.min(604,Math.round(+n)||1));
  try{await mfLoad()}catch(e){toast('Qur’on fayli yuklanmadi. Internetni tekshiring.');mfClose();return}
  if(!MFO)return;MFPG=n;mfGrBar(0);mfDraw();mfSeen(n)}
function mfSeen(n){const q=mq();q.last=n;q.rec=[{p:n,t:Date.now()}].concat(q.rec.filter(x=>x.p!==n)).slice(0,10);qsave()}
const mfGo=d=>mfShow(MFPG+d),mfJump=v=>mfShow(v);
function mfBm(){const q=mq(),n=MFPG,i=q.bm.indexOf(n);if(i>=0)q.bm.splice(i,1);else{q.bm.push(n);q.bm.sort((a,b)=>a-b)}qsave();const b=$('#mfb');if(b)b.textContent=q.bm.includes(n)?'★':'☆'}
function mfHl(k,c){const q=mq(),x=q.hl[k]||(q.hl[k]={c:0,n:'',t:0});x.c=c;x.t=Date.now();if(!x.c&&!x.n)delete q.hl[k];qsave();mfDraw(1)}
function mfNote(k,t){const q=mq(),x=q.hl[k]||(q.hl[k]={c:0,n:'',t:0});x.n=String(t||'').trim().slice(0,500);x.t=Date.now();if(!x.c&&!x.n)delete q.hl[k];qsave();mfDraw(1)}
function mfLink(k){const i=vkS(k)-1;if(S.q&&S.q.m&&S.q.m[i]>0){const r=rsOf(i);r.weak=true;r.box=0;r.due=dk()}}
function mfWeak(k){const q=mq(),z=q.wk[k];if(z&&z.s<2)delete q.wk[k];else{q.wk[k]={s:0,t:Date.now()};mfLink(k)}qsave();mfDraw(1)}
function mfGrade(k,g){const q=mq();q.wk[k]={s:g,t:Date.now()};if(MFT){MFT.st[g]++;MFT.rev[k]=1}if(g<2)mfLink(k);qsave();mfGrBar(0);mfDraw(1)}
function mfTestStart(m){MFT={on:true,mode:m,rev:{},st:[0,0,0]};mfSheetClose();mfDraw()}
function mfTestEnd(){const t=MFT;MFT=null;mfGrBar(0);mfSheetClose();mfDraw();if(t&&(t.st[0]+t.st[1]+t.st[2]))toast('Sinov: ✅ '+t.st[2]+'  ➖ '+t.st[1]+'  ❌ '+t.st[0])}
function mfTap(k){if(!MFT||!MFT.on)return;if(MFT.rev[k]){delete MFT.rev[k];mfGrBar(0)}else{MFT.rev[k]=1;mfGrBar(k)}mfDraw(1)}
function mfGrBar(k){const g=$('#mfg');if(!g)return;if(!k){g.hidden=true;g.innerHTML='';return}
  g.hidden=false;g.innerHTML=`<span>${esc(vkL(k))}: qanday esladingiz?</span><div class="in"><button class="btn" onclick="mfGrade(${k},2)">✅ Bildim</button><button class="btn s" onclick="mfGrade(${k},1)">➖ Qisman</button><button class="btn s" onclick="mfGrade(${k},0)">❌ Bilmadim</button></div>`}
function mfSheetClose(){const e=$('#mfs');if(e)e.remove()}
function mfSheet(k){mfSheetClose();const q=mq(),x=q.hl[k]||{},z=q.wk[k],w=mfVerse(k);const el=document.createElement('div');el.id='mfs';el.className='mfs';
  el.innerHTML=`<div class="mfsh"><b>${esc(vkL(k))}</b><button class="x" onclick="mfSheetClose()">✕</button></div><p class="mfv" dir="rtl" lang="ar">${esc(w.slice(0,9).map(mfFix).join(' '))}${w.length>9?' …':''}</p>
  <div class="mfdots">${MFCOL.map((c,i)=>`<button class="mfd${x.c===i+1?' on':''}" style="background:${c}" aria-label="Rang ${i+1}" onclick="mfHl(${k},${x.c===i+1?0:i+1});mfSheetClose()"></button>`).join('')}<button class="mfd x0" aria-label="Rangni olib tashlash" onclick="mfHl(${k},0);mfSheetClose()">⌫</button></div>
  <div class="in" style="flex-wrap:wrap"><button class="btn s" onclick="mfNoteEdit(${k})">✎ Izoh${x.n?' (bor)':''}</button><button class="btn s" onclick="mfWeak(${k});mfSheetClose()">${z&&z.s<2?'Zaif belgisini olib tashlash':'⚠ Zaif oyat'}</button><button class="btn s" onclick="mfAddToday(${k});mfSheetClose()">➕ Bugungi yodlashga</button><button class="btn s" onclick="mfCopy(${k})">Nusxalash</button></div>`;
  $('#mf').appendChild(el)}
function mfNoteEdit(k){const e=$('#mfs');if(!e)return;const x=mq().hl[k]||{};
  e.innerHTML=`<div class="mfsh"><b>${esc(vkL(k))} · izoh</b><button class="x" onclick="mfSheetClose()">✕</button></div><textarea id="mfnt" rows="4" maxlength="500" placeholder="Izoh yozing…">${esc(x.n||'')}</textarea><div class="in"><button class="btn" onclick="mfNote(${k},$('#mfnt').value);mfSheetClose()">Saqlash</button>${x.n?`<button class="btn s" onclick="mfNote(${k},'');mfSheetClose()">O‘chirish</button>`:''}</div>`;
  const t=$('#mfnt');if(t)t.focus()}
function mfCopy(k){const t=mfVerse(k).join(' ')+' ﴿'+vkL(k)+'﴾';try{navigator.clipboard.writeText(t).then(()=>toast('Nusxalandi'),()=>toast('Nusxalab bo‘lmadi'))}catch(e){toast('Nusxalab bo‘lmadi')}mfSheetClose()}
function mfTestMenu(){mfSheetClose();const el=document.createElement('div');el.id='mfs';el.className='mfs';
  el.innerHTML=`<div class="mfsh"><b>🧠 Yodlash sinovi</b><button class="x" onclick="mfSheetClose()">✕</button></div><p class="mu">Matn yashiriladi. Oyatga tegib ochasiz va o‘zingizni baholaysiz. Zaif oyatlar takrorga ulanadi.</p>
  <div class="in" style="flex-direction:column"><button class="btn" onclick="mfTestStart('b')">Oyat boshini ko‘rsat, davomini ayt</button><button class="btn s" onclick="mfTestStart('r')">Faqat oyat raqami, o‘zing ayt</button>${MFT&&MFT.on?'<button class="btn s" onclick="mfTestEnd()">Sinovni tugatish</button>':''}</div>`;
  $('#mf').appendChild(el)}
function mfAddToday(k){const q=S.q,s=vkS(k)-1,a=vkA(k),T=(q.ty=q.ty||{})[dk()]=q.ty[dk()]||[];
  if(T.some(e=>e.s===s&&a>=e.a&&a<=e.b)){toast('Bu oyat bugungi yodlashda bor');return}
  const L=T[T.length-1];if(L&&L.s===s&&!L.x&&L.b+1===a)L.b=a;else T.push({s,a,b:a,x:0});save();toast('Bugungi yodlashga qo‘shildi: '+vkL(k))}
function mfTestSura(i){if(!mfOn())return;MFT={on:true,mode:'b',rev:{},st:[0,0,0]};mfOpen(SP[i])}
function mfBind(){const pg=$('#mfp');if(!pg)return;let t=null,sx=0,sy=0,fired=false,mv=false,tgt=null;
  const pt=e=>e.touches&&e.touches[0]?e.touches[0]:(e.changedTouches&&e.changedTouches[0]?e.changedTouches[0]:e);
  const ig=e=>!e.touches&&Date.now()-MFTM<900;
  const start=e=>{if(ig(e))return;if(e.touches)MFTM=Date.now();const p=pt(e);sx=p.clientX;sy=p.clientY;fired=false;mv=false;tgt=e.target.closest?e.target.closest('.mw'):null;clearTimeout(t);
    if(tgt&&tgt.dataset.v&&!(MFT&&MFT.on))t=setTimeout(()=>{fired=true;if(navigator.vibrate)navigator.vibrate(15);mfSheet(+tgt.dataset.v)},480)};
  const move=e=>{if(ig(e))return;const p=pt(e);if(Math.abs(p.clientX-sx)>10||Math.abs(p.clientY-sy)>10){mv=true;clearTimeout(t)}};
  const end=e=>{if(ig(e))return;clearTimeout(t);if(e.touches)MFTM=Date.now();const p=pt(e),dx=p.clientX-sx,dy=p.clientY-sy;
    if(fired)return;
    if(Math.abs(dx)>70&&Math.abs(dx)>1.6*Math.abs(dy)){mfGo(dx>0?1:-1);return}
    if(!mv&&tgt&&tgt.dataset.v&&MFT&&MFT.on)mfTap(+tgt.dataset.v)};
  pg.addEventListener('touchstart',start,{passive:true});pg.addEventListener('touchmove',move,{passive:true});pg.addEventListener('touchend',end);
  pg.addEventListener('mousedown',start);pg.addEventListener('mousemove',move);pg.addEventListener('mouseup',end);pg.addEventListener('contextmenu',e=>e.preventDefault())}
function mfKey(e){if(!MFO)return;if(e.key==='ArrowLeft')mfGo(1);else if(e.key==='ArrowRight')mfGo(-1);else if(e.key==='Escape'){if($('#mfs'))mfSheetClose();else mfClose()}}
function mfOpen(n){if(MFO||!mfOn())return;MFO=true;const el=document.createElement('div');el.id='mf';el.className='mfo';
  el.innerHTML=`<div class="mft"><button class="x" onclick="mfClose()" aria-label="Yopish">✕</button><div class="mfti"><b id="mfn"></b><small id="mfj"></small></div><button class="x" id="mfb" onclick="mfBm()" aria-label="Xatcho‘p">☆</button><button class="x" onclick="mfTestMenu()" aria-label="Yodlash sinovi">🧠</button></div><div id="mfst" class="mfst" hidden></div><div class="mfp" id="mfp"><div class="mpg" id="mfpg"></div></div><div id="mfg" class="mfg" hidden></div><div class="mfnv"><button class="btn s" onclick="mfGo(1)">‹ Keyingi</button><input id="mfi" type="number" inputmode="numeric" min="1" max="604" aria-label="Sahifa raqami" onchange="mfJump(this.value)"><span class="mu">/ 604</span><button class="btn s" onclick="mfGo(-1)">Oldingi ›</button></div>`;
  document.body.appendChild(el);ovLock(el);mfBind();document.addEventListener('keydown',mfKey);mfShow(n||mq().last||1)}
function mfClose(){MFO=false;MFT=null;document.removeEventListener('keydown',mfKey);ovUnlock();const e=$('#mf');if(e)e.remove();render()}
async function mfOpenV(k){try{await mfLoad()}catch(e){toast('Qur’on fayli yuklanmadi. Internetni tekshiring.');return}mfOpen(MF.vp[mfIdx(k)])}
function mfSurahRows(){const f=MQ.trim().toLowerCase();return SN.map((nm,i)=>({nm,i})).filter(x=>!f||x.nm.toLowerCase().includes(f)||String(x.i+1)===f).map(x=>`<button class="row" onclick="mfOpen(${SP[x.i]})"><b style="min-width:26px">${x.i+1}</b><span class="t">${esc(x.nm)}<br><small class="mu">${AY[x.i]} oyat</small></span><span class="tm">${SP[x.i]}-bet</span></button>`).join('')||'<p class="mu">Topilmadi.</p>'}
function mfListUpd(v){MQ=v;const e=$('#mfl');if(e)e.innerHTML=mfSurahRows()}
function mushaf(){const q=mq(),last=q.last||1;
  const seg=[['s','Suralar'],['j','Juz’'],['n','Izohlar'],['b','Xatcho‘p'],['w','Zaif']].map(x=>`<button class="${MV===x[0]?'on':''}" onclick="MV='${x[0]}';render()">${x[1]}</button>`).join('');
  const rec=q.rec.filter(x=>x.p!==last).slice(0,8).map(x=>`<button class="mfch" onclick="mfOpen(${x.p})">${x.p}<small>${esc(SN[mfSurahAt(x.p)-1])}</small></button>`).join('');
  let body='';
  if(MV==='s')body=`<input class="mfq" placeholder="Sura qidirish" value="${esc(MQ)}" oninput="mfListUpd(this.value)"><div id="mfl">${mfSurahRows()}</div>`;
  else if(MV==='j')body=J.slice(0,30).map((p,i)=>`<button class="row" onclick="mfOpen(${p})"><b style="min-width:26px">${i+1}</b><span class="t">${i+1}-juz<br><small class="mu">${esc(SN[mfSurahAt(p)-1])}dan</small></span><span class="tm">${p}-bet</span></button>`).join('');
  else if(MV==='n'){const a=Object.entries(q.hl).sort((x,y)=>(y[1].t||0)-(x[1].t||0));body=a.length?a.map(([k,x])=>`<button class="row" onclick="mfOpenV(${k})"><i class="mfdot" style="background:${x.c?MFCOL[x.c-1]:'var(--ln)'}"></i><span class="t">${esc(vkL(+k))}${x.n?`<br><small class="mu">${esc(x.n)}</small>`:''}</span><span class="tm">${mfJuz(MF?MF.vp[mfIdx(+k)]:SP[vkS(+k)-1])}-juz</span></button>`).join(''):'<p class="mu">Hali belgilangan oyat yo‘q. Mushafda oyatni uzoq bosib, rang tanlang yoki izoh yozing.</p>'}
  else if(MV==='b')body=q.bm.length?q.bm.map(p=>`<div class="row"><button class="x" style="flex:1;text-align:left;color:var(--tx);font:inherit" onclick="mfOpen(${p})">★ ${p}-bet <small class="mu">${esc(SN[mfSurahAt(p)-1])}</small></button><button class="x" onclick="mfBmDel(${p})">✕</button></div>`).join(''):'<p class="mu">Xatcho‘p yo‘q. Mushafda tepadagi ☆ ni bosing.</p>';
  else{const a=Object.entries(q.wk).filter(([k,z])=>z.s<2).sort((x,y)=>(y[1].t||0)-(x[1].t||0));body=(a.length?`<p class="mu" style="margin:0 0 8px">${a.length} ta zaif oyat. Ularning surasi “Takror” ga qo‘shilgan (agar sura yodlash ro‘yxatida bo‘lsa).</p>`+a.map(([k,z])=>`<button class="row" onclick="mfOpenV(${k})"><span class="t">${esc(vkL(+k))}<br><small class="mu">${z.s===0?'Bilmadim':'Qisman'} · ${new Date(z.t).toLocaleDateString('sv')}</small></span><span class="tm">ochish</span></button>`).join(''):'<p class="mu">Zaif oyat yo‘q. Mushafda 🧠 bilan sinab ko‘ring.</p>')}
  return `<section class="goal"><p class="mu" style="margin:0">DAVOM ETISH</p><h2 style="margin:4px 0 0">${esc(SN[mfSurahAt(last)-1])} · ${last}-bet</h2><button class="big" style="margin-top:10px" onclick="mfOpen(${last})">📖 Mushafni ochish</button>${rec?`<div class="mfrc">${rec}</div>`:''}</section><div class="seg sc">${seg}</div>${body}<p class="mu" style="font-size:11px;margin-top:14px">Matn va shrift: Madina mushafi, Qur’on bosmaxonasi majmuasi (KFGQPC). Shaxsiy foydalanish uchun. Tafsilot: fonts/FONTS-NOTICE.txt</p>`}
function mfBmDel(p){const q=mq();q.bm=q.bm.filter(x=>x!==p);save()}

