// ---- IELTS: AI mashq (Reading yaratish), Xatolar daftari va mashqi, so'z bilan gap tuzishni tekshirish ----
const IMG=['m','w','s','x','k'];
let IRD={topic:'',useW:1,busy:0,err:'',d:null,ans:{},done:0,sc:0},ISC=null,IED=null;
const IRT=['Environment','Technology','Education','Health','Cities','Science','Society','History'];
const ieNorm=s=>String(s||'').toLowerCase().replace(/[’‘]/g,"'").replace(/[^a-z0-9' ]+/g,' ').replace(/\s+/g,' ').trim();
function ieLev(a,b){const m=a.length,n=b.length;if(!m)return n;if(!n)return m;let p=[...Array(n+1).keys()];for(let i=1;i<=m;i++){const c=[i];for(let j=1;j<=n;j++)c[j]=Math.min(p[j]+1,c[j-1]+1,p[j-1]+(a[i-1]===b[j-1]?0:1));p=c}return p[n]}
const ieNear=(a,b)=>{const x=ieNorm(a),y=ieNorm(b);return !!x&&(x===y||(y.length>=6&&ieLev(x,y)<=1))};
// ---- Reading mashqi ----
const ieRdPick=()=>S.ie.words.filter(w=>w.k!=='c'&&String(w.w).length>3&&!/\s/.test(w.w)).sort((a,b)=>(a.box-b.box)||((a.t||0)-(b.t||0))).slice(0,6).map(w=>w.w);
function ieRdValid(j,words){if(!j||typeof j.passage!=='string')throw new Error('AI matn bermadi. Qayta urinib ko‘ring.');
  const passage=j.passage.replace(/\r/g,'').trim(),wc=passage.split(/\s+/).length;if(wc<120)throw new Error('AI yaratgan matn juda qisqa. Qayta urinib ko‘ring.');
  const low=passage.toLowerCase(),Q=[];
  (Array.isArray(j.questions)?j.questions:[]).forEach(q=>{if(!q||!q.q)return;const a=String(q.a||'').trim(),qq=ieCl(q.q,300),why=ieCl(q.why,260);
    if(q.t==='tfng'&&['TRUE','FALSE','NOT GIVEN'].includes(a.toUpperCase()))Q.push({t:'tfng',q:qq,a:a.toUpperCase(),why});
    else if(q.t==='mcq'&&Array.isArray(q.o)&&q.o.length===4&&/^[ABCD]$/i.test(a))Q.push({t:'mcq',q:qq,o:q.o.map(x=>ieCl(x,200)),a:a.toUpperCase(),why});
    else if(q.t==='gap'&&a&&a.split(/\s+/).length<=2&&/_{2,}/.test(qq)&&ieIn(low,a.toLowerCase()))Q.push({t:'gap',q:qq,a:a.toLowerCase(),why})});   // gap javobi matnda aynan bo'lishi shart
  if(Q.length<5)throw new Error('AI savollari ishonchli chiqmadi (javoblarni matndan tekshirib bo‘lmadi). Qayta urinib ko‘ring.');
  return{title:ieCl(j.title,80)||'Reading mashqi',passage,wc,q:Q.slice(0,10),words,used:words.filter(w=>new RegExp('\\b'+ieEsc(w.slice(0,Math.max(4,w.length-2)))+'\\w*','i').test(passage))}}
async function ieRdGen(){if(IRD.busy)return;const topic=(IRD.topic||'').trim().slice(0,80),words=IRD.useW?ieRdPick():[];IRD.busy=1;IRD.err='';render();
  try{const d=await fnAI({action:'reading',topic,band:S.ie.target||7,words}),j=parseJson(d.text);IRD.d=ieRdValid(j,words);IRD.ans={};IRD.done=0;IRD.sc=0}
  catch(e){IRD.err=String(e.message||e).slice(0,200)}IRD.busy=0;render()}
function ieRdSet(i,v){if(IRD.done)return;IRD.ans[i]=v;render()}
function ieRdCheck(){const D=IRD.d;if(!D||IRD.done)return;const un=D.q.filter((_,i)=>!String(IRD.ans[i]||'').trim()).length;if(un&&!confirm(un+' ta savolga javob berilmadi. Baribir tekshiraymi?'))return;
  let sc=0;D.q.forEach((q,i)=>{const a=String(IRD.ans[i]||'').trim();q.ok=q.t==='gap'?ieNear(a,q.a):a.toUpperCase()===q.a;if(q.ok)sc++});IRD.sc=sc;IRD.done=1;
  (S.ie.pr=S.ie.pr||[]).push({id:Date.now(),d:dk(),k:'R',s:sc,n:D.q.length,topic:(IRD.topic||D.title).slice(0,60),wc:D.wc});S.ie.pr=S.ie.pr.slice(-60);ieDp().R=1;try{mkRec('R',Math.round(sc/D.q.length*40))}catch(e){}save()}
const ieRdNew=()=>{IRD.d=null;IRD.ans={};IRD.done=0;render()};
function ieRdToMat(){const D=IRD.d;if(!D)return;ieM().unshift({id:Date.now(),t:D.title,k:'a',x:D.passage,c:[],au:0,an:null,d:dk()});while(ieM().length>15)ieM().pop();toast('Materiallarga qo‘shildi: tahlil qilib so‘z olishing mumkin');save()}
function ieHlWords(text,words){const stems=words.map(w=>w.toLowerCase().slice(0,Math.max(4,w.length-2)));return String(text).replace(/([A-Za-z][A-Za-z'’-]*)|([^A-Za-z]+)/g,(m,w,o)=>w?(stems.some(s=>w.toLowerCase().startsWith(s))?'<mark class="mw2">'+esc(w)+'</mark>':esc(w)):esc(o))}
function ieRdUi(){const D=IRD.d;
  if(!D){const nw=ieRdPick().length;return `<div class="goal"><div class="h"><b>📖 AI Reading mashqi</b><span class="mu">1 so‘rov</span></div><p class="mu" style="margin:0 0 8px">AI sen uchun yangi matn yozadi (band ${S.ie.target||7} darajasida) va 8 ta IELTS savol beradi: True/False/Not Given, test, gapni to‘ldirish. Javoblar matndan tekshiriladi.</p>
    <input id="rdt" placeholder="Mavzu (ixtiyoriy), masalan: urban planning" value="${esc(IRD.topic)}" oninput="IRD.topic=this.value" style="width:100%;margin-bottom:6px"><div class="seg sc" style="margin:0 0 8px">${IRT.map(t=>`<button onclick="IRD.topic='${t}';render()">${t}</button>`).join('')}</div>
    <label class="mu" style="display:flex;gap:8px;align-items:center;margin-bottom:8px"><input type="checkbox" ${IRD.useW&&nw>=3?'checked':''} ${nw<3?'disabled':''} onchange="IRD.useW=this.checked?1:0"> Lug‘atimdagi zaif so‘zlarni matnga kirit (${nw>=3?nw+' ta':'kamida 3 ta so‘z kerak'})</label>
    ${IRD.err?`<p style="color:var(--bad);margin:0 0 8px">${esc(IRD.err)}</p>`:''}<button class="big" onclick="ieRdGen()" ${IRD.busy?'disabled':''}>${IRD.busy?'AI matn yozmoqda… (20–40 soniya)':'✨ Mashq yaratish'}</button></div>`}
  const ps=D.passage.split(/\n{2,}|\n/).filter(x=>x.trim()).map(p=>`<p class="iep">${ieHlWords(p,D.used)}</p>`).join('');
  const qs=D.q.map((q,i)=>{const a=IRD.ans[i],mark=IRD.done?(q.ok?'<span class="chip" style="color:var(--ac)">✓</span>':'<span class="chip" style="color:var(--bad)">✗</span>'):'';
    let inp='';if(q.t==='tfng')inp=`<div class="tfo">${['TRUE','FALSE','NOT GIVEN'].map(v=>`<button class="${a===v?'on':''}${IRD.done&&q.a===v?' ok':''}" onclick="ieRdSet(${i},'${v}')">${v}</button>`).join('')}</div>`;
    else if(q.t==='mcq')inp=q.o.map((o,k)=>{const L='ABCD'[k];return `<button class="qopt ${a===L?'on':''} ${IRD.done&&q.a===L?'ok':IRD.done&&a===L?'no':''}" onclick="ieRdSet(${i},'${L}')">${L}. ${esc(o.replace(/^[A-D][.)]\s*/,''))}</button>`}).join('');
    else inp=`<input class="rdg" value="${esc(a||'')}" placeholder="1–2 so‘z" ${IRD.done?'disabled':''} oninput="IRD.ans[${i}]=this.value">`;
    return `<div class="rdq"><div class="h"><b>${i+1}. ${esc(q.q)}</b>${mark}</div>${inp}${IRD.done?`<p class="mu" style="margin:6px 0 0;font-size:13px">To‘g‘ri javob: <b>${esc(q.a)}</b>. ${esc(q.why)}</p>`:''}</div>`}).join('');
  const hist=(S.ie.pr||[]).slice(-5);
  return `<div class="goal"><div class="h"><b>📖 ${esc(D.title)}</b><span class="mu">${D.wc} so‘z</span></div>${D.used.length?`<p class="mu" style="margin:0 0 6px;font-size:12px">Sariq belgilangan so‘zlar sening lug‘atingdan: ${esc(D.used.join(', '))}</p>`:''}<div class="ietx">${ps}</div></div>
    <h2>Savollar</h2>${qs}${IRD.done?`<div class="goal"><div class="h"><b>Natija</b><span style="font:700 22px Fraunces,serif">${IRD.sc} / ${D.q.length}</span></div><div class="in" style="flex-wrap:wrap"><button class="btn" onclick="ieRdNew()">Yangi mashq</button><button class="btn s" onclick="ieRdToMat()">📰 Materiallarga qo‘sh</button></div></div>`:'<button class="big" onclick="ieRdCheck()">✅ Tekshirish</button><button class="btn s" style="width:100%;margin-top:8px" onclick="ieRdNew()">Bekor qilish</button>'}
    ${hist.length?`<p class="mu" style="margin-top:10px">Oxirgi mashqlar: ${hist.map(h=>h.s+'/'+h.n).join(' · ')}</p>`:''}`}
// ---- so'z bilan gap tuzish (productive vocabulary) ----
function ieSck(id){ISC=ISC&&ISC.id===id?null:{id,txt:'',busy:0,res:null,err:''};render()}
async function ieSckGo(){const q=ISC;if(!q||q.busy)return;const w=S.ie.words.find(x=>x.id===q.id),s=String(q.txt||'').trim();if(!w)return;if(s.length<8){q.err='Gap juda qisqa: to‘liq gap yoz.';render();return}
  q.busy=1;q.err='';render();try{const d=await fnAI({action:'vocab',mode:'check',word:w.w,sentence:s}),j=parseJson(d.text);if(!j||typeof j.ok!=='boolean')throw new Error('AI javobi tushunarsiz.');q.res={ok:j.ok,fix:ieCl(j.fix,300),better:ieCl(j.better,300),note:ieCl(j.note,300)};w.pu=(w.pu||0)+1;if(j.ok)w.po=(w.po||0)+1;save()}catch(e){q.err=String(e.message||e).slice(0,160)}q.busy=0;if(ISC===q)render()}
function ieSckUi(w){if(!ISC||ISC.id!==w.id)return `<div class="in" style="margin-top:8px"><button class="btn s" style="flex:1" onclick="ieSck(${w.id})">✍ Gap tuz va AI tekshirsin</button></div>`;const q=ISC,r=q.res;
  return `<div style="margin-top:10px;background:rgba(255,255,255,.12);border-radius:12px;padding:10px"><p style="margin:0 0 6px;font-size:13px">“${esc(w.w)}” so‘zi bilan o‘z gapingni yoz:</p><textarea rows="2" style="width:100%" placeholder="Masalan: The government mitigated…" oninput="ISC.txt=this.value">${esc(q.txt)}</textarea>${q.err?`<p style="color:#ffb4a8;margin:6px 0">${esc(q.err)}</p>`:''}
   <div class="in" style="margin-top:6px"><button class="btn" onclick="ieSckGo()" ${q.busy?'disabled':''}>${q.busy?'Tekshirilmoqda…':'Tekshirish'}</button><button class="btn s" onclick="ieSck(${w.id})">Yopish</button></div>
   ${r?`<div style="margin-top:8px"><p style="margin:0;font-weight:700">${r.ok?'✅ To‘g‘ri va tabiiy':'⚠ Tuzatish kerak'}</p>${r.fix?`<p style="margin:4px 0 0">Tuzatilgani: <i>${esc(r.fix)}</i></p>`:''}${r.better?`<p style="margin:4px 0 0">Yaxshiroq (band 7+): <i>${esc(r.better)}</i></p>`:''}${r.note?`<p style="margin:4px 0 0;opacity:.9;font-size:13px">${esc(r.note)}</p>`:''}</div>`:''}</div>`}
// ---- Xatolar daftari ----
const IET={grammar:'Grammatika',vocab:'So‘z tanlash',collocation:'Kollokatsiya',spelling:'Imlo',other:'Boshqa'};
const ieErrT=x=>{const v=String(x&&x.t||'').toLowerCase();return IET[v]&&v!=='other'?v:'other'};
function ieErrs(){const M={};(S.ie.tests||[]).concat(S.ie.wr||[]).forEach(t=>{const e=t.fb&&Array.isArray(t.fb.errors)?t.fb.errors:[];e.forEach(x=>{if(!x||!x.o||!x.c)return;const o=ieCl(x.o,200),c=ieCl(x.c,200);if(ieNorm(o)===ieNorm(c))return;const k=ieNorm(o)+'|'+ieNorm(c),r=M[k]||(M[k]={o,c,w:ieCl(x.w,240),t:ieErrT(x),d:t.d||'',n:0});r.n++;if((t.d||'')>r.d)r.d=t.d})});
  return Object.values(M).sort((a,b)=>b.n-a.n||(b.d>a.d?1:-1))}
const ieErrKey=e=>ieNorm(e.o)+'|'+ieNorm(e.c);
const ieErrOpen=()=>ieErrs().filter(e=>((S.ie.ed||{})[ieErrKey(e)]||{ok:0}).ok<3);
function ieErrCard(){const E=ieErrs(),open=ieErrOpen(),cnt={};E.forEach(e=>cnt[e.t]=(cnt[e.t]||0)+e.n);const tot=E.reduce((a,e)=>a+e.n,0),rep=E.filter(e=>e.n>=2).slice(0,4);
  if(!E.length)return `<div class="goal"><div class="h"><b>📒 Xatolar daftari</b></div><p class="mu" style="margin:0">Writing yoki Speaking javobingni AI bilan tekshirtirsang, xatolaring shu yerda yig‘iladi va o‘zingga mos mashq tuziladi.</p></div>`;
  return `<div class="goal"><div class="h"><b>📒 Xatolar daftari</b><span class="mu">${E.length} xil · ${tot} marta</span></div>${Object.keys(IET).filter(k=>cnt[k]).map(k=>`<div style="margin-bottom:5px"><div style="display:flex;justify-content:space-between;font-size:12px"><span>${IET[k]}</span><b>${cnt[k]}</b></div><div class="dpb"><i style="width:${Math.round(cnt[k]/tot*100)}%"></i></div></div>`).join('')}
    ${rep.length?`<p class="mu" style="margin:10px 0 4px">Qayta-qayta takrorlanayotgan xatolar:</p>${rep.map(e=>`<p style="margin:0 0 6px;font-size:14px"><span class="mu">×${e.n}</span> <s>${esc(e.o)}</s> → <b>${esc(e.c)}</b></p>`).join('')}`:''}
    <p class="mu" style="margin:10px 0 4px">Oxirgilari:</p>${E.slice().sort((a,b)=>b.d>a.d?1:-1).slice(0,3).map(e=>`<p style="margin:0 0 6px;font-size:14px"><s>${esc(e.o)}</s> → <b>${esc(e.c)}</b>${e.w?`<br><small class="mu">${esc(e.w)}</small>`:''}</p>`).join('')}
    ${open.length>=3?`<button class="big" style="margin-top:8px" onclick="ieDrillStart()">🎯 Xatolarim bo‘yicha mashq (${Math.min(5,open.length)} savol)</button>`:`<p class="mu" style="margin:8px 0 0">${open.length?'Mashq uchun kamida 3 ta ochiq xato kerak.':'Hamma xato o‘zlashtirilgan, barakalla!'}</p>`}</div>`}
function ieErrBrief(){const E=ieErrs();if(!E.length)return '';const top=Object.entries(E.reduce((c,e)=>(c[e.t]=(c[e.t]||0)+e.n,c),{})).sort((a,b)=>b[1]-a[1])[0];return `<button class="row" style="margin:10px 0" onclick="IVW='x';render()"><span class="t">📒 Xatolar daftari: ${E.length} xil xato<br><small class="mu">Ko‘pi bilan: ${IET[top[0]]} (${top[1]})</small></span><span class="tm">mashq</span></button>`}
function ieDrillStart(){const open=ieErrOpen();if(open.length<3)return;const pick=open.slice().sort((a,b)=>b.n-a.n||Math.random()-.5).slice(0,5).sort(()=>Math.random()-.5);IED={q:pick,i:0,sc:0,ans:'',res:null,end:0};render()}
function ieDrillCheck(){const D=IED;if(!D||D.res)return;const q=D.q[D.i],ok=ieNear(D.ans,q.c);D.res=ok?'ok':'no';if(ok)D.sc++;S.ie.ed=S.ie.ed||{};const r=S.ie.ed[ieErrKey(q)]=S.ie.ed[ieErrKey(q)]||{ok:0,bad:0};ok?r.ok++:r.bad++;save()}
function ieDrillNext(){const D=IED;if(!D)return;if(D.i+1>=D.q.length)D.end=1;else{D.i++;D.ans='';D.res=null}render()}
const ieDrillClose=()=>{IED=null;render()};
function ieDrillUi(){const D=IED;if(!D)return '';
  if(D.end)return `<div class="goal"><div class="h"><b>🎯 Mashq tugadi</b><span style="font:700 22px Fraunces,serif">${D.sc} / ${D.q.length}</span></div><p class="mu">${D.sc===D.q.length?'Zo‘r! Bu xatolarni endi qilmaysan.':'To‘g‘ri yozgan xatolaring 3 martadan keyin daftardan chiqadi. Qolganini yana mashq qil.'}</p><button class="btn" onclick="ieDrillClose()">Yopish</button></div>`;
  const q=D.q[D.i];return `<div class="goal"><div class="h"><b>🎯 Xatoni tuzat ${D.i+1}/${D.q.length}</b><span class="chip">${IET[q.t]}</span></div><p style="font:500 20px Georgia,serif;margin:6px 0 10px"><s>${esc(q.o)}</s></p><input value="${esc(D.ans)}" placeholder="To‘g‘ri variantni yoz" ${D.res?'disabled':''} oninput="IED.ans=this.value" style="width:100%">
    ${D.res?`<p style="margin:8px 0 0;font-weight:700;color:${D.res==='ok'?'var(--ac)':'var(--bad)'}">${D.res==='ok'?'✅ To‘g‘ri':'✗ To‘g‘ri variant:'} <b>${esc(q.c)}</b></p>${q.w?`<p class="mu" style="margin:4px 0 0;font-size:13px">${esc(q.w)}</p>`:''}<button class="btn" style="margin-top:8px" onclick="ieDrillNext()">${D.i+1>=D.q.length?'Natija':'Keyingisi'}</button>`:'<div class="in" style="margin-top:8px"><button class="btn" onclick="ieDrillCheck()">Tekshirish</button><button class="btn s" onclick="ieDrillClose()">Chiqish</button></div>'}</div>`}
// ---- AI mashq tabi ----
function ieAiTab(){return `<section class="hero"><p class="lab">AI mashq</p><h1 style="font-size:26px">Sening xatolaring, sening so‘zlaring</h1><p class="mu">${aiUseLabel()}. Har AI mashq 1 ta so‘rov sarflaydi.</p></section>${IED?ieDrillUi():ieErrCard()}${ieRdUi()}${axSections()}<div class="goal"><b>Yana nima bor</b><p class="mu" style="margin:6px 0 0">✍ <b>Gap tuzish:</b> Lug‘at kartochkasida “Gap tuz” tugmasi. 🎧 <b>Diktant:</b> Materiallar ichidagi podkast qatorlari yonidagi ✍ tugmasi. 🔤 <b>So‘z olish:</b> Materiallar bo‘limida maqola yoki podkastni AI bilan tahlil qil.</p></div>`}
