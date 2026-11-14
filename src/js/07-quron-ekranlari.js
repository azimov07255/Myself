const QGX={q:['u','y','t','h','x','a'],i:['n','z','d','r']};let QGL={q:'y',i:'n'};const qgOf=t=>QGX.i.includes(t)?'i':'q';
function quran(){
  if(QT==='u'&&!mfOn())QT='y';
  const gq=qgOf(QT);QGL[gq]=QT;
  const ALL=[['u','📖 Mushaf'],['y','🧠 Yodlash'],['t','🔁 Takror'],['h','📖 Hatm'],['a','🎧 Tinglash'],['x','🗺 Xarita'],['n','🕌 Namoz'],['z','📿 Zikr'],['d','🤲 Duolar'],['r','🌙 Ramazon']];
  const seg=ALL.filter(x=>QGX[gq].includes(x[0])&&(x[0]!=='u'||mfOn())).map(x=>`<button class="${QT===x[0]?'on':''}" onclick="QT='${x[0]}';render()">${x[1]}</button>`).join('');
  const gs=`<div class="seg" style="margin-top:12px"><button class="${gq==='q'?'on':''}" onclick="QT=QGL.q;render()">📖 Qur‘on</button><button class="${gq==='i'?'on':''}" onclick="QT=QGL.i;render()">🕌 Ibodat</button></div>`;
  return `<div class="top"><p class="d">${gq==='q'?'Qur‘on':'Ibodat'}</p></div>${gs}<div class="seg sc" style="margin-top:8px">${seg}</div>${QT==='u'?mushaf():QT==='y'?yod():QT==='t'?tak():QT==='h'?hatm():QT==='n'?namoz():QT==='r'?ramazon():QT==='d'?duolar():QT==='a'?qaView():QT==='x'?hxView():zikr()}`}
const J=[1,22,42,62,82,102,121,142,162,182,201,222,242,262,282,302,322,342,362,382,402,422,442,462,482,502,522,542,562,582,605];
const AY=[7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6];
function juzMem(j){let s=0;SN.forEach((_,i)=>{const d=Math.min(S.q.m[i]||0,SL(i));if(d>0){const a=SPF(i);s+=Math.max(0,Math.min(a+d,J[j+1])-Math.max(a,J[j]))}});return s}
function ya(){const q=S.q,n=AY[YS<0?q.cur:YS],s=YS<0?q.cur:YS,a=Math.max(1,Math.min(n,+YA||1)),b=Math.max(a,Math.min(n,+YB||a));q.ty=q.ty||{};(q.ty[dk()]=q.ty[dk()]||[]).push({s,a,b,x:0});save()}
function yx(j){const q=S.q,e=q.ty[dk()][j],p=(e.b-e.a+1)/AY[e.s]*SL(e.s);e.x=e.x?0:1;setM(e.s,(q.m[e.s]||0)+(e.x?p:-p))}
function yd(j){const q=S.q,L=q.ty[dk()],e=L[j];if(e.x){const p=(e.b-e.a+1)/AY[e.s]*SL(e.s);L.splice(j,1);setM(e.s,(q.m[e.s]||0)-p)}else{L.splice(j,1);save()}}
function yod(){
  const q=S.q,cs=q.cur,md=r1(mdone()),rem=TOT-md,days=Math.ceil(rem/q.ppd),fin=new Date(Date.now()+days*864e5);
  const st=SP[cs]+Math.floor(q.m[cs]||0),en=Math.min(st+q.ppd-1,cs<113?SP[cs+1]:604);
  const plan=SL(cs)<=1?`${SN[cs]} surasi`:`${SN[cs]}, ${st}–${en}-betlar`;
  const rows=SN.map((n,i)=>{const d=r1(q.m[i]||0),l=SL(i),f=d>=l;return `<div class="row ${f?'done':''} ${i===cs?'now':''}"><span class="ck" onclick="sf(${i})">${f?'✓':''}</span><span class="t" onclick="sc(${i})">${i+1}. ${n}<br><span class="mu">${SP[i]}-bet, ${AY[i]} oyat, ${d}/${l} bet</span></span><button class="x" onclick="sp(${i},-1)">−</button><button class="x" onclick="sp(${i},1)">+</button></div>`}).join('');
  const ty=(q.ty||{})[dk()]||[],ys=YS<0?cs:YS;
  const picks=ty.map((e,j)=>`<div class="row ${e.x?'done':''}"><span class="ck" onclick="yx(${j})">${e.x?'✓':''}</span><span class="t" onclick="yx(${j})">${SN[e.s]}, ${e.a}–${e.b}-oyatlar</span>${mfOn()?`<button class="x" onclick="mfOpenV(${(e.s+1)*1000+e.a})" aria-label="Mushafda ochish">📖</button>`:''}<button class="x" onclick="yd(${j})">×</button></div>`).join('');
  const opts=SN.map((n,i)=>`<option value="${i}" ${i===ys?'selected':''}>${i+1}. ${n} (${AY[i]} oyat)</option>`).join('');
  const jz=J.slice(0,30).map((s,j)=>{const l=J[j+1]-s,p=Math.min(100,Math.round(juzMem(j)/l*100));return `<div class="row"><span class="t">${j+1}-pora<br><span class="mu">${s}–${J[j+1]-1}-betlar</span><div class="bar" style="margin-top:4px"><i style="width:${p}%"></i></div></span><span class="mu" style="min-width:44px;text-align:right">${p}%</span></div>`}).join('');
  return `<section class="hero"><p class="lab">Bugungi yodlash</p><h1 style="font-size:28px">${plan}</h1><div class="bar" style="margin:10px 0"><i style="width:${md/TOT*100}%"></i></div><p class="mu">Yodlangan ${md} bet, qolgan taxminan ${Math.round(rem)} bet. Kuniga ${q.ppd} bet bilan ${days} kunda (${fin.getDate()} ${MON[fin.getMonth()]} ${fin.getFullYear()}) tugaydi.</p><p class="mu" style="margin-top:8px">Kunlik reja: ${q.ppd} bet</p>${stp('ppd',1)}<button class="big" style="margin-top:6px" onclick="addP(${q.ppd})">Bugun ${q.ppd} bet yodladim</button>${mfOn()?`<button class="btn s" style="margin-top:8px;width:100%" onclick="mfOpen(${st})">📖 Mushafda ochish (${st}-bet)</button>`:''}</section>
  <h2>Bugun yodlayotganlarim</h2><p class="mu" style="margin:0 0 8px">Sura va oyatlarni o‘zing tanla. Belgilasang, oyat ulushi sahifa hisobiga qo‘shiladi.</p>${picks}
  <div class="in"><select onchange="YS=+this.value;YA=1;YB=Math.min(AY[YS],3);render()">${opts}</select></div><div class="in"><input type="number" inputmode="numeric" placeholder="Oyatdan" value="${YA}" oninput="YA=this.value"><input type="number" inputmode="numeric" placeholder="Oyatgacha" value="${YB}" oninput="YB=this.value"><button class="btn" onclick="ya()">Qo‘sh</button></div>
  <h2>Suralar</h2><p class="mu" style="margin:0 0 8px">Nomini bossang, hozirgi sura bo‘ladi. Belgi bossang, to‘liq yodlangan bo‘ladi.</p><details ${LO?'open':''} ontoggle="LO=this.open"><summary class="mu" style="margin-bottom:8px">Barcha 114 sura</summary>${rows}</details>
  <h2>30 pora</h2><details ${LJ?'open':''} ontoggle="LJ=this.open"><summary class="mu" style="margin-bottom:8px">Pora bo‘yicha yodlash</summary>${jz}</details>`}
const BX=[1,2,4,7,14,30];
function initRs(i){(S.q.rs=S.q.rs||{})[i]={box:0,due:addD(1),weak:false,last:''}}
function rsOf(i){const q=S.q;q.rs=q.rs||{};return q.rs[i]||(q.rs[i]={box:1,due:dk(),weak:false,last:''})}
function rate(i,lv){
  const q=S.q,r=rsOf(i),k=dk();
  if(tqRd())q.rd[k]=r1((q.rd[k]||0)+Math.min(q.m[i]||0,SL(i)));
  try{const pgx=Math.min(q.m[i]||0,SL(i));tqLog({m:'r',s:i,pa:SP[i],pb:Math.max(SP[i],SP[i]+Math.ceil(pgx)-1),pg:r1(pgx),t:SN[i],src:'rate'})}catch(e){}
  r.last=k;
  if(lv===0){r.weak=true;r.box=0;r.due=addD(1)}
  else if(lv===1){r.due=addD(r.weak?2:BX[r.box])}
  else{r.weak=false;r.box=Math.min(5,r.box+1);r.due=addD(BX[r.box])}
  save()}
function wkT(i){const r=rsOf(i);r.weak=!r.weak;if(r.weak){r.box=0;r.due=dk()}else r.due=addD(BX[r.box]);save()}
const ago2=d=>{if(!d)return 'hali takror qilinmagan';const n=-dl(d);return n<=0?'bugun takror qilindi':n+' kun oldin takror qilindi'};
// ---- Sabaq · Sabqi · Manzil: yodlangan sahifalarni sana bilan qayd etish va kunlik takror rejasi ----
// Sabaq = bugungi yangi bet. Sabqi = oxirgi N kun ichida yodlanganlar (har kuni). Manzil = eskilari, M kunda bir marta aylanib chiqiladi.
const ssC=()=>{const q=S.q;q.lg=q.lg||[];q.sqd=q.sqd||{};q.mzd=q.mzd||{};if(!q.sd)q.sd=7;if(!q.mc)q.mc=30;if(q.mz===undefined)q.mz=0;return q};
function qLog(i,a,b,t,nm){const q=ssC(),k=dk();if(!(b>a+1e-9))return 0;t=t||'n';const L=q.lg[q.lg.length-1];
  if(!nm&&L&&L.d===k&&L.i===i&&L.t===t&&Math.abs(L.b-a)<1e-6){L.b=b;return L.id}
  const id=Date.now()*1000+q.lg.length%1000;q.lg.push({id,d:k,i,a,b,t});
  if(q.lg.length>300)q.lg=q.lg.filter(e=>e.d>=dAgo(45)).slice(-300);return id}
function qTrim(i,v){const q=ssC();q.lg=q.lg.map(e=>e.i!==i||e.t!=='n'?e:(e.a>=v-1e-9?null:{...e,b:Math.min(e.b,v)})).filter(Boolean)}
const ivMerge=a=>{const s=a.filter(x=>x[1]-x[0]>1e-6).sort((x,y)=>x[0]-y[0]),o=[];for(const x of s){const l=o[o.length-1];if(l&&x[0]<=l[1]+1e-6)l[1]=Math.max(l[1],x[1]);else o.push([x[0],x[1]])}return o};
const ivSub=(A,B)=>{let out=[];for(const[a,b]of A){let cur=[[a,b]];for(const[c,d]of B){const nx=[];for(const[x,y]of cur){if(d<=x||c>=y)nx.push([x,y]);else{if(c>x)nx.push([x,c]);if(d<y)nx.push([d,y])}}cur=nx}out=out.concat(cur)}return ivMerge(out)};
const ivLen=a=>a.reduce((s,x)=>s+(x[1]-x[0]),0);
const ssMem=()=>ivMerge(S.q.ord.map(i=>[SPF(i),SPF(i)+Math.min(S.q.m[i]||0,SL(i))]));
function ssWin(){const q=ssC(),T=dk(),lo=dAgo(q.sd),f=e=>[SPF(e.i)+e.a,SPF(e.i)+Math.min(e.b,Math.min(q.m[e.i]||0,SL(e.i)))];
  return{sab:ivMerge(q.lg.filter(e=>e.d>=lo&&e.d<T).map(f)),inc:ivMerge(q.lg.filter(e=>e.d>=lo&&e.d<=T).map(f))}}
function ssInfo(){const q=ssC(),old=ivSub(ssMem(),ssWin().inc),tot=ivLen(old);return{old,tot,Q:tot<1e-6?0:Math.min(tot,Math.max(1,Math.ceil(tot/q.mc)))}}
function ssManzil(){const q=ssC(),k=dk(),sig=JSON.stringify([ssMem(),ssWin().inc,q.mc,q.mz]);if(q.mzp&&q.mzp.d===k&&q.mzp.sig===sig)return q.mzp;
  const{old,tot,Q}=ssInfo(),res={d:k,sig,r:[],p:0,tot,Q,end:q.mz};if(Q<=0){q.mzp=res;return res}
  let idx=old.findIndex(x=>x[1]>q.mz+1e-6),from=idx<0?old[0][0]:Math.max(q.mz,old[idx][0]);if(idx<0)idx=0;let need=Q,g=0;
  while(need>1e-6&&g++<500){const x=old[idx],a=Math.max(from,x[0]),take=Math.min(need,x[1]-a);if(take>1e-6){res.r.push([a,a+take]);need-=take}
    if(a+take>=x[1]-1e-6){idx=(idx+1)%old.length;from=old[idx][0]}else break}
  res.p=ivLen(res.r);res.end=res.r.length?res.r[res.r.length-1][1]:q.mz;q.mzp=res;return res}
function ssParts(){const q=ssC(),k=dk(),w=ssWin(),P=[],dq=q.sqd[k],dm=q.mzd[k];
  if(w.sab.length||dq)P.push({k:'q',n:'Sabqi',r:dq?dq.r:w.sab,p:dq?dq.p:ivLen(w.sab),done:dq});
  if(dm)P.push({k:'m',n:'Manzil',r:dm.r,p:dm.p,done:dm});else{const m=ssManzil();if(m.r.length)P.push({k:'m',n:'Manzil',r:m.r,p:m.p,done:null})}
  return P}
const ssSurahAt=x=>{let s=0;for(let i=0;i<114;i++)if(SPF(i)<=x+1e-6)s=i;return s};
const ssPg=x=>Math.max(1,Math.floor(x+1e-6));
function ssLbl(r){const p1=ssPg(r[0]),p2=Math.max(p1,Math.ceil(r[1]-1e-6)-1);return SN[ssSurahAt(r[0])]+', '+(p1===p2?p1+'-bet':p1+'–'+p2+'-betlar')}
function ssSet(pk,ql){const q=ssC(),k=dk(),M=pk==='q'?q.sqd:q.mzd;if(M[k])ssUndo(pk,true);
  const P=ssParts().find(x=>x.k===pk);if(!P||P.done)return;const rec={q:ql,p:r1(P.p),r:P.r.map(x=>[x[0],x[1]]),ids:[]};
  rec.rd=tqRd()?1:0;if(rec.rd)q.rd[k]=r1((q.rd[k]||0)+P.p);try{P.r.forEach(r=>{const pa=ssPg(r[0]),pb=Math.max(pa,Math.ceil(r[1]-1e-6)-1);rec.tq=rec.tq||[];const e={id:syUid('ssm:'),m:'r',s:ssSurahAt(r[0]),pa,pb,pg:r1(r[1]-r[0]),t:ssLbl(r),src:'ssm'};tqLog(e);rec.tq.push(e.id)})}catch(e){} if(pk==='m'){rec.pv=q.mz;if(q.mzp&&q.mzp.d===k)q.mz=q.mzp.end}
  if(ql==='w')P.r.forEach(x=>{for(let i=0;i<114;i++){const m=Math.min(q.m[i]||0,SL(i));if(m<=0)continue;const a=Math.max(x[0],SPF(i))-SPF(i),b=Math.min(x[1],SPF(i)+m)-SPF(i);if(b>a+1e-6){rec.ids.push(qLog(i,a,b,'r',true));mfLink((i+1)*1000+1)}}});
  M[k]=rec;save();toast(ql==='w'?'Zaif belgilandi: ertaga sabqiga qaytadi':'+'+r1(P.p)+' bet takror')}
function ssUndo(pk,quiet){const q=ssC(),k=dk(),M=pk==='q'?q.sqd:q.mzd,rec=M[k];if(!rec)return;if(rec.rd!==0)q.rd[k]=Math.max(0,r1((q.rd[k]||0)-rec.p));try{if(rec.tq&&q.tk&&q.tk.d&&q.tk.d[k]){q.tk.d[k]=q.tk.d[k].filter(e=>!rec.tq.includes(e.id));if(!q.tk.d[k].length)delete q.tk.d[k]}}catch(e){}if(pk==='m'&&rec.pv!==undefined)q.mz=rec.pv;q.lg=q.lg.filter(e=>!rec.ids.includes(e.id));delete M[k];if(!quiet)save()}
function ssStep(f,d,lo,hi){const q=ssC();q[f]=Math.max(lo,Math.min(hi,q[f]+d));if(f==='mc'||f==='sd')q.mzp=null;save()}
function ssTest(p){if(!mfOn())return;MFT={on:true,mode:'b',rev:{},st:[0,0,0]};mfOpen(p)}
let TKV='k';
function ssmView(){const q=ssC(),k=dk(),P=ssParts(),ppd=q.ppd,cs=q.cur,ny=(q.ny||{})[k]||0,st=SP[cs]+Math.floor(q.m[cs]||0),I=ssInfo(),QL={g:'yaxshi',m:'o‘rtacha',w:'zaif'};
  const sab=`<div class="ssc ${ny>=ppd&&ppd>0?'ok':''}"><div class="ssh"><b>① Sabaq · yangi</b><span class="mu">${r1(ny)}/${ppd} bet</span></div><p class="ssr">${esc(SL(cs)<=1?SN[cs]+' surasi':SN[cs]+', '+st+'-bet')}dan boshlab ${ppd} bet</p><div class="in" style="flex-wrap:wrap">${mfOn()?`<button class="btn s" onclick="mfOpen(${st})">📖 Mushafda</button>`:''}<button class="btn" onclick="addP(${ppd})">Bugun ${ppd} bet yodladim</button></div></div>`;
  const card=(p,n)=>{const d=p.done,o=ssPg(p.r[0][0]);return `<div class="ssc ${d?'ok':''}"><div class="ssh"><b>${n} ${p.n} · ${p.k==='q'?'oxirgi '+q.sd+' kun':'eskilari'}</b><span class="mu">${r1(p.p)} bet</span></div><p class="ssr">${p.r.map(x=>esc(ssLbl(x))).join('<br>')}</p>${d?`<p class="mu" style="margin:6px 0 0">✓ Bajarildi (${QL[d.q]}) <button class="x" onclick="ssUndo('${p.k}')" aria-label="Bekor qilish">↩</button></p>`:`${mfOn()?`<div class="in" style="flex-wrap:wrap"><button class="btn s" onclick="mfOpen(${o})">📖 Mushafda</button><button class="btn s" onclick="ssTest(${o})">🧠 Sinash</button></div>`:''}<div class="in"><button class="btn" style="flex:1" onclick="ssSet('${p.k}','g')">✅ Yaxshi</button><button class="btn s" style="flex:1" onclick="ssSet('${p.k}','m')">➖ O‘rtacha</button><button class="btn s" style="flex:1" onclick="ssSet('${p.k}','w')">⚠ Zaif</button></div>`}</div>`};
  const pq=P.find(x=>x.k==='q'),pm=P.find(x=>x.k==='m'),done=P.filter(x=>x.done).length;
  const empty=!P.length?`<div class="ssc"><p class="mu" style="margin:0">${q.ord.length?'Bugun takror uchun hech narsa yo‘q: sabqi (oxirgi '+q.sd+' kun) va manzil (eskilari) bo‘sh. Yangi bet yodlasang, ertadan sabqi boshlanadi.':'Hali yodlangan sahifa yo‘q. Avval sabaq: bugun yangi bet yodlab, “yodladim” bos.'}</p></div>`:'';
  const hist=[...Array(7)].map((_,i)=>{const d=dAgo(6-i),a=q.sqd[d],b=q.mzd[d],n=(a?1:0)+(b?1:0);return `<div title="${d}"><i class="ssd ${n===2?'g':n===1?'m':''}"></i><small>${DAYS[new Date(d+'T12:00').getDay()].slice(0,2)}</small></div>`}).join('');
  return `<section class="hero"><p class="lab">Bugungi hifz tartibi</p><h1 style="font-size:26px">${P.length?done+'/'+P.length+' takror bajarildi':'Sabaq → sabqi → manzil'}</h1><p class="mu">Sabaq: yangi bet. Sabqi: oxirgi ${q.sd} kunda yodlaganlaring. Manzil: eskilari, ${q.mc} kunda bir marta aylanib chiqiladi.</p></section>${sab}${pq?card(pq,'②'):''}${pm?card(pm,pq?'③':'②'):''}${empty}
  <h2>Oxirgi 7 kun</h2><div class="ssdr">${hist}</div><p class="mu" style="margin:4px 0 0">To‘liq nuqta: sabqi va manzil ikkalasi bajarilgan.</p>
  <h2>Sozlama</h2><div class="goal"><div class="ssst"><span>Sabqi muddati</span><div><button class="btn s" onclick="ssStep('sd',-1,3,10)">−</button><b>${q.sd} kun</b><button class="btn s" onclick="ssStep('sd',1,3,10)">+</button></div></div><div class="ssst"><span>Manzil aylanishi</span><div><button class="btn s" onclick="ssStep('mc',-5,7,90)">−</button><b>${q.mc} kun</b><button class="btn s" onclick="ssStep('mc',5,7,90)">+</button></div></div><p class="mu" style="margin:8px 0 0">${I.tot>0?'Eski yodlaganing '+r1(I.tot)+' bet: kuniga ~'+I.Q+' bet manzil, hammasi '+q.mc+' kunda aylanadi.':'Eski yodlagan sahifa hali yo‘q (yangilari avval sabqida takrorlanadi).'}</p></div>`}
function tak(){const seg=`<div class="seg" style="margin-bottom:10px"><button class="${TKV==='k'?'on':''}" onclick="TKV='k';render()">📖 Bugun</button><button class="${TKV==='s'?'on':''}" onclick="TKV='s';render()">Sabqi · Manzil</button><button class="${TKV==='b'?'on':''}" onclick="TKV='b';render()">Sura qutilari</button></div>`;if(QG)return qgView();return qgHub()+seg+(TKV==='k'?tqHome():TKV==='s'?ssmView():takBoxes())}

function takBoxes(){
  const q=S.q,t=dk();
  const due=q.ord.filter(i=>rsOf(i).due<=t).sort((a,b)=>(rsOf(b).weak-rsOf(a).weak)||(rsOf(a).due>rsOf(b).due?1:-1));
  const plan=[];let acc=0;for(const i of due){if(plan.length&&acc>=q.rg)break;plan.push(i);acc+=Math.min(q.m[i]||0,SL(i))}
  const rest=due.length-plan.length,weakN=q.ord.filter(i=>rsOf(i).weak).length,strong=q.ord.filter(i=>rsOf(i).box>=4&&!rsOf(i).weak).length;
  const cards=plan.map(i=>{const r=rsOf(i);return `<div class="goal" style="${r.weak?'border-left:4px solid var(--bad)':''}"><div class="h"><b style="font:700 18px Fraunces,serif">${SN[i]}</b><span class="mu">${r1(Math.min(q.m[i]||0,SL(i)))} bet</span></div><p class="mu" style="margin:2px 0 8px">${r.weak?'Zaif sura. ':''}${ago2(r.last)}</p>${mfOn()?`<div class="in" style="margin:0 0 8px"><button class="btn s" style="flex:1" onclick="mfTestSura(${i})">🧠 Mushafda sinab ko‘r</button></div>`:''}<div class="in" style="margin:0"><button class="btn s" style="flex:1" onclick="rate(${i},0)">Zaif</button><button class="btn s" style="flex:1" onclick="rate(${i},1)">O‘rtacha</button><button class="btn" style="flex:1" onclick="rate(${i},2)">Yaxshi</button></div></div>`}).join('');
  const days=[...Array(7)].map((_,n)=>{const d=addD(n),c=q.ord.filter(i=>n===0?rsOf(i).due<=d:rsOf(i).due===d).length;return{n,c,l:n===0?'Bugun':DAYS[new Date(d+'T12:00').getDay()].slice(0,2)}}),mx=Math.max(1,...days.map(x=>x.c));
  const fc=days.map(x=>`<div style="flex:1;text-align:center"><div style="height:60px;display:flex;align-items:flex-end"><div style="width:100%;height:${Math.max(3,x.c/mx*60)}px;background:${x.n===0?'var(--go)':'var(--ac)'};opacity:.85;border-radius:4px"></div></div><span class="mu" style="font-size:11px">${x.l}</span><br><span style="font-size:12px">${x.c}</span></div>`).join('');
  const list=q.ord.slice().sort((a,b)=>(rsOf(b).weak-rsOf(a).weak)||(rsOf(a).due>rsOf(b).due?1:-1)).map(i=>{const r=rsOf(i),n=dl(r.due);return `<div class="row ${plan.includes(i)?'now':''}"><span class="t">${SN[i]}<br><span class="mu">${r.weak?'zaif, ':''}keyingi takror: ${n<=0?'bugun':n===1?'ertaga':n+' kundan keyin'}</span></span><button class="x" style="font-size:16px;${r.weak?'color:var(--bad)':''}" onclick="wkT(${i})">${r.weak?'⚑':'⚐'}</button></div>`}).join('');
  return `<section class="hero"><p class="lab">Bugungi takror</p>${plan.length?`<h1 style="font-size:30px">${plan.length} ta sura</h1><p class="mu">Taxminan ${r1(acc)} bet. Har birini baholasang, ilova keyingi takror vaqtini o‘zi belgilaydi: zaiflar tez-tez, mustahkamlar kamroq chiqadi.${rest>0?` Navbatda yana ${rest} ta sura bor.`:''}</p>`:`<h1 style="font-size:28px">${q.ord.length?'Bugungi takror tugadi':'Hali takror yo‘q'}</h1><p class="mu">${q.ord.length?'Keyingi suralar o‘z vaqtida chiqadi.':'Yodlashda sura belgilasang, takror shu yerda chiqadi.'}</p>`}<p class="mu" style="margin-top:8px">Bugun takror qilingan: ${r1(q.rd[t]||0)} bet. Kunlik maqsad: ${q.rg} bet</p>${stp('rg',1)}</section>
  ${cards}${crCard()}${jzCard()}${q.ord.length?`<div style="margin-top:10px"><span class="chip bad">${weakN} zaif</span><span class="chip" style="color:var(--ac)">${strong} mustahkam</span><span class="chip">${q.ord.length} yodlangan sura</span></div><h2>Keyingi 7 kun yuki</h2><div style="display:flex;gap:4px">${fc}</div><h2>Yodlangan suralar</h2><p class="mu" style="margin:0 0 8px">Bayroqchani bossang, sura zaif deb belgilanadi va tez-tez takrorlanadi.</p>${list}`:''}`}
function hSet(){const v=Math.round(+V('hpg'));if(!(v>=0&&v<=604))return;S.q.hp=v;if(!S.q.hs)S.q.hs=dk();save()}
function hJz(j){if(confirm(j+'-poradan boshlanadi. Davom etilsinmi?')){S.q.hp=J[j-1]-1;if(!S.q.hs)S.q.hs=dk();save()}}
function hPlan(d){const q=S.q;q.ht=d;q.hs=dk();q.h0=q.hp;q.hg=Math.max(1,Math.ceil((604-q.hp)/d));save()}
function hatm(){
  const q=S.q,k=dk(),left=604-q.hp,days=Math.ceil(left/q.hg);let jn=1;for(let j=0;j<30;j++)if(q.hp+1>=J[j])jn=j+1;
  let cur=0,best=0,run=0;for(let i=119;i>=0;i--){if((q.hd[dAgo(i)]||0)>0){run++;best=Math.max(best,run)}else run=0}for(let i=0;i<120;i++){if((q.hd[dAgo(i)]||0)>0)cur++;else if(i>0)break}
  let w7=0;for(let i=0;i<7;i++)w7+=q.hd[dAgo(i)]||0;const avg=w7/7,fin=avg>0?new Date(Date.now()+Math.ceil(left/avg)*864e5):null;
  const exp=q.ht&&q.hs?Math.min(604,Math.round((q.h0||0)+(604-(q.h0||0))*Math.min(1,(-dl(q.hs)+1)/q.ht))):null;
  const cells=[...Array(30)].map((_,x)=>{const j=x+1,s=J[x],e=J[x+1]-1;return `<button class="${q.hp>=e?'rd':q.hp>=s-1?'cu':''}" onclick="hJz(${j})">${j}</button>`}).join('');
  const bars=[...Array(14)].map((_,i)=>{const v=q.hd[dAgo(13-i)]||0;return `<div style="flex:1;text-align:center"><div style="height:60px;display:flex;align-items:flex-end"><div style="width:100%;height:${Math.max(3,Math.min(60,v*3))}px;background:${i===13?'var(--go)':'var(--ac)'};opacity:.85;border-radius:4px"></div></div><span class="mu" style="font-size:10px">${v}</span></div>`}).join('');
  const hist=(q.hh||[]).slice().reverse().map(x=>`<div class="row"><span class="t">${dU(x.d)}</span><span class="tm">${x.days} kunda</span></div>`).join('');
  return `<section class="hero"><p class="lab">Hatm</p><h1 style="font-size:30px">${q.hp} / 604 bet</h1><div class="bar" style="margin:10px 0"><i style="width:${q.hp/6.04}%"></i></div><p class="mu">Hozirgi pora: ${jn}-pora. Tugatilgan hatmlar: ${q.hc}. Kuniga ${q.hg} bet bilan hatmga ${days} kun qoldi. Bugun o‘qilgan: ${q.hd[k]||0} bet.</p><p class="mu" style="margin-top:8px">Kunlik maqsad: ${q.hg} bet</p>${stp('hg',1)}<button class="big" style="margin-top:6px" onclick="hd(${q.hg})">Bugun ${q.hg} bet o‘qidim</button><div class="in" style="margin-top:8px">${[[1,'+1'],[5,'+5'],[10,'+10'],[20,'+1 pora']].map(x=>`<button class="btn s" style="flex:1;padding:10px 0" onclick="hd(${x[0]})">${x[1]}</button>`).join('')}<button class="btn s" style="flex:1;padding:10px 0" onclick="hd(-1)">−1</button></div></section>
  <div class="st"><div><b>${cur} kun</b>ketma-ket o‘qish</div><div><b>${best} kun</b>eng uzun seriya</div><div><b>${r1(avg)}</b>bet/kun (7 kun)</div></div>
  ${fin?`<p class="mu" style="margin:10px 0 0">Shu tezlikda hatm taxminan ${fin.getDate()} ${MON[fin.getMonth()]} kuni tugaydi.</p>`:'<p class="mu" style="margin:10px 0 0">Bir necha kun o‘qisang, tugash sanasi hisoblanadi.</p>'}
  <h2>Hatm rejasi</h2><p class="mu" style="margin:0 0 8px">Necha kunda tugatmoqchisan? Kunlik maqsad o‘zi hisoblanadi.</p><div class="chips">${[7,15,30,60,90].map(d=>`<button class="${q.ht===d?'on':''}" onclick="hPlan(${d})">${d} kun</button>`).join('')}</div>
  ${exp!==null?`<p style="margin:8px 0 0">Reja bo‘yicha bugun <b>${exp}-bet</b>ga yetish kerak. Sen ${q.hp}-betdasan: ${q.hp>=exp?`${q.hp-exp} bet oldindasan`:`${exp-q.hp} bet ortdasan`}.</p>`:''}
  <h2>Pora xaritasi</h2><div class="jm">${cells}</div><p class="mu" style="margin:6px 0 0">Yashil: o‘qilgan, sariq: hozirgi. Poraga bossang, o‘sha poradan boshlanadi.</p>
  <h2>Joyni belgilash</h2><div class="in"><input id="hpg" type="number" inputmode="numeric" placeholder="Hozir nechanchi betdasan?" value="${q.hp||''}"><button class="btn" onclick="hSet()">Saqla</button></div>
  <h2>So‘nggi 14 kun, bet</h2><div style="display:flex;gap:3px">${bars}</div>
  ${hist?`<h2>Tugatilgan hatmlar</h2>${hist}`:''}`}
function zikr(){
  const z=S.z,c=z.c[dk()]||{},x=ZK[z.sel],t=z.tg||x[2],v=c[z.sel]||0,rem=v%t,tot=Object.values(c).reduce((a,b)=>a+b,0);
  const chips=ZK.map((y,i)=>`<button class="${z.sel===i?'on':''}" onclick="S.z.sel=${i};render()">${y[0]}</button>`).join('');
  return `<div class="chips" style="margin-top:12px">${chips}</div><div class="seg" style="margin-top:10px">${[[0,'Standart'],[33,'33'],[99,'99'],[100,'100']].map(y=>`<button class="${(z.tg||0)===y[0]?'on':''}" onclick="ztg(${y[0]})">${y[1]}</button>`).join('')}</div><p dir="rtl" lang="ar" style="font-size:28px;text-align:center;margin:14px 0 0">${x[1]}</p>
  <button class="tsb" style="background:conic-gradient(var(--ac) ${rem/t*360}deg,var(--c2) 0)" onclick="zt()"><span>${rem}</span></button>
  <p class="mu" style="text-align:center;margin:0">Maqsad: ${t}. To‘liq aylanish: ${Math.floor(v/t)}. Jami bugun: ${tot}</p><button class="ghost" onclick="zr()">Nolga tushirish</button>`}


function go(t){tab=t;SO=false;render();scrollTo(0,0);const a=$('#app');a.classList.remove('anim');void a.offsetWidth;a.classList.add('anim');setTimeout(()=>a.classList.remove('anim'),1000)}
function hbT(id,k){k=k||dk();(S.hb[k]=S.hb[k]||{})[id]=!S.hb[k][id];if(S.hb[k][id]&&S.hk&&S.hk[k]){delete S.hk[k][id];if(!Object.keys(S.hk[k]).length)delete S.hk[k]}save()}
function addH(){const v=$('#nh').value.trim();if(!v)return;const e=($('#ne')&&$('#ne').value.trim())||'';S.hab.push({id:'h'+Date.now(),t:v,e});save()}
function delH(i){if(confirm('Odat o‘chirilsinmi?')){S.hab.splice(i,1);save()}}
function hst(id){let n=0;for(let i=0;i<400;i++){const k=dAgo(i);if((S.hb[k]||{})[id])n++;else if(hkOn(k,id))continue;else if(i>0)break}return n}
const gpct=g=>g.lk==='hifz'?hifzStats().pc:g.lk==='ielts'?ieReady().pc:g.ms&&g.ms.length?Math.round(g.ms.filter(m=>m.x).length/g.ms.length*100):(g.p||0);
function gm(i,j){const g=S.goals[i],m=g.ms[j];m.x=!m.x;m.xd=m.x?dk():'';if(m.x){confetti();toast(g.ms.every(x=>x.x)?'🏆 Maqsadga erishding! '+(g.rw?'Mukofot: '+g.rw:'Alhamdulillah!'):'Bosqich bajarildi! +'+RWP.ms+' XP')}save()}
function gmd(i,j){S.goals[i].ms.splice(j,1);save()}
function gma(i){const e=$('#gm'+i),v=e.value.trim();if(!v)return;const g=S.goals[i];(g.ms=g.ms||[]).push({t:v,x:0});save()}
function gdl(i,v){S.goals[i].dl=v;save()}
function wt(n){S.water[cd()]=Math.max(0,Math.min(8,n));save()}
const fmtT=s=>pad(Math.floor(s/60))+':'+pad(s%60);
function ftick(){FS=Math.max(0,Math.ceil((FE-Date.now())/1000));const e=$('#ft');if(e)e.textContent=fmtT(FS);fkBar();if(FS<=0){clearInterval(FR);FR=null;S.fm[dk()]=(S.fm[dk()]||0)+FL;fkLog(FL);FS=FL*60;fkBar();toast('⏱ Fokus tugadi: +'+FL+' daqiqa');if(navigator.vibrate)navigator.vibrate([200,100,200]);save()}}
function fgo(){if(FR){clearInterval(FR);FR=null;fkBar();render();return}FE=Date.now()+FS*1000;FR=setInterval(ftick,500);fkBar();render()}
function fset(m){if(FR)return;FL=m;FS=m*60;render()}
function frs(){clearInterval(FR);FR=null;FS=FL*60;fkBar();render()}

