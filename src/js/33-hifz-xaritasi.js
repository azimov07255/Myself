// ---- Hifz xaritasi: 604 sahifa, 30 juz' qatorida. Rang = holat (yodlanmagan, yangi, mustahkam, takror kerak, zaif) ----
let HXP=0;
const hxJ=p=>{for(let j=0;j<30;j++)if(p>=J[j]&&p<J[j+1])return j;return 29};
const HXS={n:'Yodlanmagan',x:'Yangi (sabqi)',m:'Yodlangan',s:'Mustahkam',d:'Takror kerak',w:'Zaif'};
function hxSurahsOn(p){const a=[];for(let i=0;i<114;i++)if((SP[i]<=p&&(i>=113||SP[i+1]>p))||SP[i]===p)a.push(i);return a}
function hxInfo(){const mem=ssMem(),win=ssWin().inc,t=dk(),rs=S.q.rs||{},res=[],tp=new Set(),cov=(p,I)=>Math.max(0,Math.min(1,1-ivLen(ivSub([[p,p+1]],I))));
  ssParts().forEach(P=>(P.r||[]).forEach(r=>{for(let p=Math.floor(r[0]+1e-6);p<r[1]-1e-6;p++)tp.add(p)}));
  for(let p=1;p<=604;p++){const c=cov(p,mem);let st='n',si=-1;
    if(c>=0.02){const sl=hxSurahsOn(p).filter(i=>(S.q.m[i]||0)>0);si=sl.length?sl[0]:ssSurahAt(p);const r=rs[si],weak=!!(r&&r.weak),nw=cov(p,win)>=0.5*c,due=!!(r&&r.due<=t),strong=!!(r&&r.box>=4);st=weak?'w':nw?'x':due?'d':strong?'s':'m'}
    res.push({p,c,st,si,td:tp.has(p)})}
  return res}
function hxCount(I){const c={n:0,x:0,m:0,s:0,d:0,w:0};I.forEach(x=>c[x.st]++);return c}
function hxTap(p){HXP=HXP===p?0:p;render()}
function hxWeak(i){const r=rsOf(i);r.weak=!r.weak;if(r.weak){r.box=0;r.due=dk()}save()}
function hxDue(i){rsOf(i).due=dk();save()}
function hxDetail(I){if(!HXP)return '';const x=I[HXP-1],sl=hxSurahsOn(HXP),si=x.si>=0?x.si:sl[0],r=x.si>=0?rsOf(x.si):null,j=hxJ(HXP)+1;
  return `<div class="goal"><div class="h"><b>${HXP}-bet · ${j}-juz’</b><button class="x" onclick="HXP=0;render()" aria-label="Yopish">✕</button></div>
   <p style="margin:0 0 4px">${sl.map(i=>esc(SN[i])).join(', ')}</p><p style="margin:0 0 6px"><span class="erb ${x.st==='w'?'new':'old'}">${HXS[x.st]}</span>${x.c>0&&x.c<0.98?` <span class="mu">yarmi yodlangan (${Math.round(x.c*100)}%)</span>`:''}${x.td?' <span class="mu">· bugungi rejada</span>':''}</p>
   ${r&&x.st!=='n'?`<p class="mu" style="margin:0 0 6px;font-size:13px">So‘nggi takror: ${r.last?esc(r.last):'yo‘q'} · navbatdagi: ${esc(r.due||'—')} · quti ${r.box||0}</p>`:''}
   <div class="in" style="flex-wrap:wrap">${typeof mfOn==='function'&&mfOn()?`<button class="btn" onclick="HXP=0;mfOpen(${HXP})">📖 Mushafda ochish</button>`:''}${r&&x.st!=='n'?`<button class="btn s" onclick="hxWeak(${x.si})">${r.weak?'✓ Zaifni olib tashla':'⚠ Zaif deb belgila'}</button><button class="btn s" onclick="hxDue(${x.si})">🔁 Bugun takrorla</button>`:''}</div></div>`}
function hxView(){const I=hxInfo(),c=hxCount(I),mem=I.length-c.n,pc=Math.round(mem/604*100),rows=[];
  for(let j=0;j<30;j++){let cells='';for(let p=J[j];p<J[j+1];p++){const x=I[p-1];cells+=`<button class="hxp${x.td?' hxt':''}${HXP===p?' hxs':''}" data-s="${x.st}" data-p="${p}"${x.c>0&&x.c<0.98?' data-c="p"':''} onclick="hxTap(${p})" aria-label="${p}-bet, ${HXS[x.st]}"></button>`}rows.push(`<div class="hxr"><span class="hxj">${j+1}</span><div class="hxc">${cells}</div></div>`)}
  const old=S.q.ord.filter(i=>(S.q.m[i]||0)>0&&rsOf(i).last).sort((a,b)=>rsOf(a).last>rsOf(b).last?1:-1).slice(0,3);
  return `<div class="top"><p class="d">Hifz xaritasi</p></div><section class="hero"><p class="lab">Yodlangan</p><h1 style="font-size:30px">${mem} / 604 bet · ${pc}%</h1><p class="mu">Har katak bitta sahifa, har qator bitta juz’. Katakni bossang tafsilot ochiladi.</p></section>
  ${hxDetail(I)}<div class="hxg">${rows.join('')}</div>
  <div class="hxl">${['n','x','m','s','d','w'].map(k=>`<span><i data-s="${k}"></i>${HXS[k]} <b>${c[k]}</b></span>`).join('')}<span><i class="hxt2"></i>Bugungi reja</span></div>
  ${old.length?`<h2>Eng uzoq takrorlanmagan</h2>${old.map(i=>`<div class="row"><span class="t">${esc(SN[i])}<br><small class="mu">so‘nggi takror: ${esc(rsOf(i).last)}</small></span><button class="btn s" onclick="hxDue(${i})">🔁 Bugun</button></div>`).join('')}`:''}
  <button class="big" onclick="QT='t';TKV='s';render()">🔁 Takrorni ochish</button>`}
