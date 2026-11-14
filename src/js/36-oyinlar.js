// ---- So'z o'yinlari (lug'atdagi so'zlar bilan): juftlashtirish, imlo, 60 soniyalik tezkor test ----
let GM=null,GMT=0;
const gmMean=w=>w.u||w.m||w.d||'',gmShuf=a=>a.slice().sort(()=>Math.random()-.5);
const GMN={match:'Juftlashtirish',spell:'Imlo',speed:'Tezkor test'};
function gmPool(n){const W=S.ie.words.filter(w=>w.k!=='g'&&gmMean(w)&&String(w.w).length>1);if(W.length<4)return null;return W.map(w=>({w,r:Math.random()+(w.box||0)*0.35})).sort((a,b)=>a.r-b.r).slice(0,n).map(x=>x.w)}
function gmStart(g){const P=gmPool(g==='match'?6:g==='spell'?8:40);if(!P){toast('O‘yin uchun kamida 4 ta ma’noli so‘z kerak. Avval Materiallardan so‘z qo‘sh.');return}clearInterval(GMT);GMT=0;
  if(g==='match')GM={g,items:P,left:gmShuf(P.map(w=>w.id)),right:gmShuf(P.map(w=>w.id)),done:{},sel:null,bad:0,t0:Date.now(),end:0,ms:0,nb:0};
  else if(g==='spell')GM={g,items:P,i:0,sc:0,hint:0,ans:'',res:null,end:0,wrong:[],nb:0};
  else{GM={g,pool:P,i:0,sc:0,bad:0,streak:0,best:0,t0:Date.now(),T:60,end:0,wrong:[],q:null,nb:0};gmSpQ();GMT=setInterval(gmSpTick,250)}
  render()}
function gmExit(){clearInterval(GMT);GMT=0;GM=null;render()}
function gmFinish(){const G=GM;S.ie.gm=S.ie.gm||{};S.ie.gm[dk()]=(S.ie.gm[dk()]||0)+1;const b=S.ie.gb=S.ie.gb||{};
  if(G.g==='match'){if(!b.match||G.ms<b.match){b.match=G.ms;G.nb=1}}else{const v=G.sc;if(!(b[G.g]>=v))b[G.g]=v,G.nb=v>0?1:0}save()}
function gmReview(id){const w=S.ie.words.find(x=>x.id===id);if(!w)return;w.due=dk();toast('“'+w.w+'” bugungi takrorga qo‘shildi');save()}
// --- juftlashtirish ---
function gmPick(side,id){const G=GM;if(!G||G.g!=='match'||G.end||G.done[id])return;if(!G.sel||G.sel.side===side){G.sel={side,id};render();return}const ok=G.sel.id===id;G.sel=null;
  if(ok){G.done[id]=1;if(Object.keys(G.done).length===G.items.length){G.end=1;G.ms=Date.now()-G.t0;gmFinish()}}else G.bad++;render()}
// --- imlo ---
function gmSpellCheck(){const G=GM,w=G.items[G.i];if(G.res)return;const ok=ieNorm(G.ans)===ieNorm(w.w);G.res=ok?'ok':'no';if(ok)G.sc++;else G.wrong.push(w.id);render()}
function gmSpellNext(){const G=GM;if(G.i+1>=G.items.length){G.end=1;gmFinish()}else{G.i++;G.ans='';G.res=null;G.hint=0}render()}
// --- tezkor test ---
function gmSpQ(){const G=GM,w=G.pool[G.i%G.pool.length],o=gmShuf(G.pool.filter(x=>x.id!==w.id)).slice(0,3);G.q={w,opts:gmShuf([w,...o]),ans:null}}
function gmSpAns(i){const G=GM;if(!G||G.end||!G.q||G.q.ans!==null)return;G.q.ans=i;const ok=G.q.opts[i].id===G.q.w.id;if(ok){G.sc++;G.streak++;G.best=Math.max(G.best,G.streak)}else{G.bad++;G.streak=0;G.wrong.push(G.q.w.id)}render();setTimeout(gmSpNext,ok?350:900)}
function gmSpNext(){const G=GM;if(!G||G.g!=='speed'||G.end)return;G.i++;gmSpQ();render()}
function gmSpTick(){const G=GM;if(!G||G.g!=='speed'||G.end)return;const left=Math.max(0,G.T-Math.floor((Date.now()-G.t0)/1000)),el=document.getElementById('gmt');if(el)el.textContent=left+' s';if(left<=0)gmEnd()}
function gmEnd(){const G=GM;if(!G||G.end)return;G.end=1;clearInterval(GMT);GMT=0;gmFinish();render()}
// --- ekranlar ---
const gmBest=()=>{const b=S.ie.gb||{};return {match:b.match?(b.match/1000).toFixed(1)+' s':'—',spell:b.spell!=null?b.spell+' / 8':'—',speed:b.speed!=null?b.speed+' ta':'—'}};
function gmCard(){const B=gmBest(),ok=S.ie.words.filter(w=>w.k!=='g'&&gmMean(w)).length>=4;return `<h2>🎮 So‘z o‘yinlari</h2><div class="gmg"><button class="gmb" onclick="gmStart('match')"><b>🔗 Juftlashtirish</b><small>6 so‘z ↔ ma’no · eng yaxshi: ${B.match}</small></button><button class="gmb" onclick="gmStart('spell')"><b>⌨️ Imlo</b><small>eshit va yoz · eng yaxshi: ${B.spell}</small></button><button class="gmb" onclick="gmStart('speed')"><b>⚡ Tezkor test</b><small>60 soniya · eng yaxshi: ${B.speed}</small></button></div>${ok?'':'<p class="mu">O‘yin uchun lug‘atda kamida 4 ta ma’noli so‘z bo‘lishi kerak.</p>'}`}
const gmWrongList=G=>G.wrong&&G.wrong.length?`<p class="mu" style="margin:10px 0 4px">Xato qilingan so‘zlar:</p>${[...new Set(G.wrong)].map(id=>{const w=S.ie.words.find(x=>x.id===id);return w?`<div class="row"><span class="t"><b>${esc(w.w)}</b><br><small class="mu">${esc(gmMean(w))}</small></span><button class="btn s" onclick="gmReview(${id})">🔁 Takrorga</button></div>`:''}).join('')}`:'';
function gmView(){const G=GM,head=`<div class="in" style="align-items:center"><button class="btn s" onclick="gmExit()">← Lug‘at</button><b style="flex:1;text-align:center">${GMN[G.g]}</b><span></span></div>`;
  if(G.g==='match'){if(G.end)return `${head}<section class="hero"><p class="lab">Tayyor!</p><h1>${(G.ms/1000).toFixed(1)} soniya</h1><p>${G.bad} ta xato${G.nb?' · 🏆 yangi rekord':''}</p></section><button class="big" onclick="gmStart('match')">Yana</button>`;
    const w=id=>S.ie.words.find(x=>x.id===id);
    return `${head}<p class="mu" style="margin:8px 0">So‘zni bos, keyin uning ma’nosini bos. Xatolar: <b>${G.bad}</b></p><div class="gmc"><div>${G.left.map(id=>`<button class="gmb ${G.done[id]?'ok':G.sel&&G.sel.side==='l'&&G.sel.id===id?'on':''}" ${G.done[id]?'disabled':''} onclick="gmPick('l',${id})">${esc(w(id).w)}</button>`).join('')}</div><div>${G.right.map(id=>`<button class="gmb ${G.done[id]?'ok':G.sel&&G.sel.side==='r'&&G.sel.id===id?'on':''}" ${G.done[id]?'disabled':''} onclick="gmPick('r',${id})">${esc(gmMean(w(id)))}</button>`).join('')}</div></div>`}
  if(G.g==='spell'){if(G.end)return `${head}<section class="hero"><p class="lab">Natija</p><h1>${G.sc} / ${G.items.length}</h1><p>${G.nb?'🏆 yangi rekord':''}</p></section>${gmWrongList(G)}<button class="big" onclick="gmStart('spell')">Yana</button>`;
    const w=G.items[G.i];return `${head}<p class="mu" style="margin:8px 0">${G.i+1} / ${G.items.length}</p><section class="hero"><p class="lab">Ma’nosi</p><h1 style="font-size:24px">${esc(gmMean(w))}</h1><button class="btn s" onclick="ieSay(${JSON.stringify(w.w).replace(/"/g,'&quot;')})">🔊 Eshit</button> ${G.hint?`<p style="margin:8px 0 0">${esc(w.w[0])}${'_ '.repeat(Math.max(0,w.w.length-1))} (${w.w.length} harf)</p>`:`<button class="btn s" onclick="GM.hint=1;render()">💡 Ishora</button>`}</section>
      <input id="gmi" value="${esc(G.ans)}" placeholder="Inglizcha yoz" ${G.res?'disabled':''} oninput="GM.ans=this.value" autocapitalize="off" autocomplete="off" spellcheck="false" style="width:100%;margin:10px 0">${G.res?`<p style="font-weight:700;color:${G.res==='ok'?'var(--ac)':'var(--bad)'}">${G.res==='ok'?'✅ To‘g‘ri':'✗ To‘g‘ri imlo:'} <b>${esc(w.w)}</b></p><button class="btn" onclick="gmSpellNext()">${G.i+1>=G.items.length?'Natija':'Keyingisi'}</button>`:'<button class="btn" onclick="gmSpellCheck()">Tekshirish</button>'}`}
  if(G.end)return `${head}<section class="hero"><p class="lab">Vaqt tugadi</p><h1>${G.sc} ta to‘g‘ri</h1><p>Eng uzun ketma-ketlik: ${G.best}${G.nb?' · 🏆 yangi rekord':''}</p></section>${gmWrongList(G)}<button class="big" onclick="gmStart('speed')">Yana</button>`;
  const q=G.q;return `${head}<div class="in" style="justify-content:space-between;margin-top:8px"><span>✅ <b>${G.sc}</b> · 🔥 ${G.streak}</span><b id="gmt">${Math.max(0,G.T-Math.floor((Date.now()-G.t0)/1000))} s</b></div><section class="hero"><p class="lab">Qaysi so‘z?</p><h1 style="font-size:22px">${esc(gmMean(q.w))}</h1></section><div class="gmc1">${q.opts.map((o,i)=>`<button class="gmb ${q.ans===null?'':o.id===q.w.id?'ok':q.ans===i?'gmw':''}" onclick="gmSpAns(${i})">${esc(o.w)}</button>`).join('')}</div>`}
