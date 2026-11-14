// ================= PUL =================
const CATS=['Ovqat','Transport','O‘qish','Salomatlik','Kiyim','Ko‘ngil ochish','Aloqa','Uy-joy','Sadaqa','Boshqa'],CIN=['Maosh','Dokon daromadi','Sovg‘a','Boshqa'];
const CI={'Ovqat':'🍽','Transport':'🚕','O‘qish':'📚','Salomatlik':'💊','Kiyim':'👕','Ko‘ngil ochish':'🎮','Aloqa':'📱','Uy-joy':'🏠','Sadaqa':'🤲','Boshqa':'➕','Maosh':'💼','Dokon daromadi':'🏪','Sovg‘a':'🎁'};
const ACN={cash:'Naqd',card:'Karta'};
let PV='b',FACC='cash',FTO='card',FD='',EID=0,PF={mo:0,ac:'all',k:'all',q:''};
function sfn(v){return parseInt(String(v).replace(/[^0-9]/g,''),10)||0}
function finInit(){const f=S.fin;f.open=f.open||{p:{cash:0,card:0},d:{cash:0,card:0}};f.open.p=f.open.p||{cash:0,card:0};f.open.d=f.open.d||{cash:0,card:0};f.sg=f.sg||[];S.debts=S.debts||[];
  if(f.goal&&f.goal.a>0){f.sg.push({id:Date.now(),t:f.goal.t||'Jamg‘arma maqsadi',a:f.goal.a,s:f.goal.s||0});f.goal={t:'',a:0,s:0}}}
const dRem=d=>Math.max(0,d.a-d.pay.reduce((a,x)=>a+x.a,0));
function bal(w){finInit();const o=S.fin.open[w]||{cash:0,card:0},v={cash:o.cash||0,card:o.card||0};
  S.money.filter(m=>m.w===w).forEach(m=>{const ac=m.ac||'cash';if(m.k==='in')v[ac]+=m.a;else if(m.k==='out')v[ac]-=m.a;else if(m.k==='tr'){v[ac]-=m.a;v[m.to||'card']+=m.a}});
  if(w==='p')S.debts.forEach(d=>{if(d.led!==false)v[d.ac||'cash']+=d.k==='borrow'?d.a:-d.a;d.pay.forEach(x=>{v[x.ac||'cash']+=d.k==='borrow'?-x.a:x.a})});
  return{cash:v.cash,card:v.card,tot:v.cash+v.card}}
const mKey=off=>{const d=new Date(new Date().getFullYear(),new Date().getMonth()+off,1);return{k:`${d.getFullYear()}-${pad(d.getMonth()+1)}`,d}};
const mSum=(L,k,ac)=>L.filter(m=>m.k===k&&(!ac||(m.ac||'cash')===ac)).reduce((a,m)=>a+m.a,0);
const mList=(w,k)=>S.money.filter(m=>m.w===w&&m.d.startsWith(k));
function putM(o){const i=S.money.findIndex(x=>x.id===o.id);if(i>=0)S.money[i]=o;else S.money.push(o)}
function addM(){const a=sfn(FA);if(!a)return;const d=FD||dk(),id=EID||Date.now();
  if(K==='tr'){if(FACC===FTO)return;putM({id,d,k:'tr',a,ac:FACC,to:FTO,n:FN.trim(),w:W})}
  else putM({id,d,k:K,a,ac:FACC,n:FN.trim(),w:W,c:(K==='out'?CATS:CIN)[FC]||'Boshqa',t:(K==='out'&&FT)?FT:undefined});
  try{if(K==='out')pBudChk(W,K,CATS[FC]||'Boshqa')}catch(e){}
  EID=0;FA='';FN='';FD='';FT='';save()}
function pCancel(){EID=0;FA='';FN='';FD='';render()}
function pEdit(id){const m=S.money.find(x=>x.id===id);if(!m)return;K=m.k;FACC=m.ac||'cash';FTO=m.to||'card';FA=String(m.a);FN=m.n||'';FD=m.d;FT=m.t||'';EID=id;FC=Math.max(0,(m.k==='out'?CATS:CIN).indexOf(m.c));PV='b';render();scrollTo(0,0)}
function dm(id){if(confirm('Yozuv o‘chirilsinmi?')){S.money=S.money.filter(m=>m.id!==id);if(EID===id)pCancel();else save()}}
function pAcc(a){FACC=a;if(K==='tr'&&FTO===a)FTO=a==='cash'?'card':'cash';render()}
function setOpen(ac,v){finInit();S.fin.open[W][ac]=sfn(v);save()}

function pForm(){
  const lst=K==='out'?CATS:CIN,chip=(a,fn,sel)=>`<button class="${sel?'on':''}" onclick="${fn}">${a}</button>`;
  const kind=`<div class="seg"><button class="${K==='out'?'on':''}" onclick="K='out';FC=0;render()">Chiqim</button><button class="${K==='in'?'on':''}" onclick="K='in';FC=0;render()">Kirim</button><button class="${K==='tr'?'on':''}" onclick="K='tr';render()">O‘tkazma</button></div>`;
  const acc=K==='tr'?`<div class="acc"><button class="${FACC==='cash'?'on':''}" onclick="FACC='cash';FTO='card';render()">Naqddan kartaga</button><button class="${FACC==='card'?'on':''}" onclick="FACC='card';FTO='cash';render()">Kartadan naqdga</button></div>`:`<div class="acc"><button class="${FACC==='cash'?'on':''}" onclick="pAcc('cash')">💵 Naqd</button><button class="${FACC==='card'?'on':''}" onclick="pAcc('card')">💳 Karta</button></div>`;
  const cats=K==='tr'?'':`<div class="cchips">${lst.map((c,i)=>`<button class="${FC===i?'on':''}" onclick="FC=${i};render()"><span>${CI[c]||'•'}</span>${c}</button>`).join('')}</div>`;
  return `<div class="goal" style="margin-top:12px"><b>${EID?'Yozuvni tahrirlash':'Yangi yozuv'}</b><div style="margin-top:10px">${kind}${acc}</div>
  <div class="in"><input type="text" inputmode="numeric" placeholder="Summa, so‘m" value="${FA?num(+FA):''}" oninput="FA=String(sfn(this.value));this.value=sfn(this.value)?num(sfn(this.value)):''" style="font-size:20px;font-weight:700"></div>${cats}
  <div class="in"><input placeholder="Izoh" value="${esc(FN)}" oninput="FN=this.value"></div><div class="in"><input type="date" value="${FD||dk()}" onchange="FD=this.value"></div>
  <div class="in"><button class="btn" style="flex:1" onclick="addM()">${EID?'Saqlash':'Yozish'}</button>${EID?'<button class="btn s" onclick="pCancel()">Bekor</button>':''}</div></div>`}
function mRow(m){
  const ac=m.ac||'cash',tr=m.k==='tr',ic=tr?'🔁':(CI[m.c]||'•'),ti=tr?`${ACN[ac]} → ${ACN[m.to||'card']}`:(m.n||m.c||(m.k==='in'?'Kirim':'Chiqim'));
  return `<div class="row" onclick="pEdit(${m.id})"><span style="font-size:22px">${ic}</span><span class="t">${esc(ti)}<br><span class="mu">${tr?esc(m.n||''):ACN[ac]+(m.n&&m.c?', '+esc(m.c):'')}</span></span><b class="${tr?'':m.k==='in'?'in-c':'out-c'}">${tr?'':m.k==='in'?'+':'−'}${num(m.a)}</b><button class="x" onclick="event.stopPropagation();dm(${m.id})">×</button></div>`}

function pBosh(){
  const B=bal(W),mk=mKey(0).k,L=mList(W,mk),inn=mSum(L,'in'),ou=mSum(L,'out'),dB=S.debts.filter(d=>d.st!=='closed');
  const owe=dB.filter(d=>d.k==='borrow').reduce((a,d)=>a+dRem(d),0),lent=dB.filter(d=>d.k==='lend').reduce((a,d)=>a+dRem(d),0);
  const recent=S.money.filter(m=>m.w===W).slice().sort((a,b)=>b.d.localeCompare(a.d)||b.id-a.id).slice(0,6).map(mRow).join('');
  return `<section class="hero"><p class="lab">Umumiy balans</p><h1 style="font-size:36px;word-break:break-all">${num(B.tot)} so‘m</h1><div class="pbal"><div><span>💵 Naqd</span><b>${num(B.cash)}</b></div><div><span>💳 Karta</span><b>${num(B.card)}</b></div></div></section>
  <h2>${MON[new Date().getMonth()][0].toUpperCase()+MON[new Date().getMonth()].slice(1)} oyi</h2>
  <div class="sum"><div><span class="mu">Kirim</span><b class="in-c">${num(inn)}</b><span class="mu" style="font-size:12px">naqd ${num(mSum(L,'in','cash'))}, karta ${num(mSum(L,'in','card'))}</span></div><div><span class="mu">Chiqim</span><b class="out-c">${num(ou)}</b><span class="mu" style="font-size:12px">naqd ${num(mSum(L,'out','cash'))}, karta ${num(mSum(L,'out','card'))}</span></div><div class="w"><span class="mu">Oy balansi</span><b>${num(inn-ou)} so‘m</b></div></div>
  ${W==='p'&&(owe||lent)?`<button class="row" onclick="PV='q';render()"><span class="t">Qarzlar<br><span class="mu">Men qarzdorman: ${num(owe)}. Menga qarzdor: ${num(lent)}</span></span></button>`:''}
  ${pDailyUi()}${pForecastUi()}${pQuickUi()}${pTypeUi()}${pForm()}${pWlUi()}<h2>So‘nggi yozuvlar</h2>${recent||'<p class="mu">Hali yozuv yo‘q.</p>'}`}

function pTarix(){
  const mk=mKey(PF.mo),mn=MON[mk.d.getMonth()];let L=mList(W,mk.k);
  if(PF.ac!=='all')L=L.filter(m=>(m.ac||'cash')===PF.ac||(m.k==='tr'&&m.to===PF.ac));
  if(PF.k!=='all')L=L.filter(m=>m.k===PF.k);
  if(PF.q)L=L.filter(m=>sn((m.n||'')+' '+(m.c||'')).includes(sn(PF.q)));
  L=L.slice().sort((a,b)=>b.d.localeCompare(a.d)||b.id-a.id);const g={};L.forEach(m=>(g[m.d]=g[m.d]||[]).push(m));
  const chips=(arr,key)=>`<div class="chips">${arr.map(([v,t])=>`<button class="${PF[key]===v?'on':''}" onclick="PF.${key}='${v}';render()">${t}</button>`).join('')}</div>`;
  const days=Object.keys(g).sort().reverse().map(d=>{const dn=mSum(g[d],'in')-mSum(g[d],'out');return `<p class="mu" style="margin:14px 0 6px;display:flex;justify-content:space-between"><span>${+d.slice(8)}-${MON[+d.slice(5,7)-1]}</span><span>${dn>=0?'+':'−'}${num(Math.abs(dn))}</span></p>${g[d].map(mRow).join('')}`}).join('');
  return `<div class="in"><button class="btn s" onclick="PF.mo--;render()">‹</button><button class="btn s" onclick="PF.mo=0;render()">${mn[0].toUpperCase()+mn.slice(1)} ${mk.d.getFullYear()}</button><button class="btn s" onclick="PF.mo++;render()">›</button></div>
  ${chips([['all','Hammasi'],['cash','Naqd'],['card','Karta']],'ac')}${chips([['all','Barchasi'],['in','Kirim'],['out','Chiqim'],['tr','O‘tkazma']],'k')}
  <div class="in"><input placeholder="Izoh yoki kategoriya bo‘yicha qidirish" value="${esc(PF.q)}" onchange="PF.q=this.value;render()"></div>
  <p class="mu" style="margin:0">Kirim ${num(mSum(L,'in'))}, chiqim ${num(mSum(L,'out'))}. Yozuvni bossang, tahrirlanadi.</p>${days||'<p class="mu">Bu oyda yozuv yo‘q.</p>'}`}

// ---- Qarzlar ----
function dAdd(){const p=V('dpn'),a=sfn(V('dpa')),k=V('dpk')||'borrow';if(!p||!a)return;S.debts.push({id:Date.now(),p,k,a,d:dk(),due:V('dpd'),n:V('dpt'),ac:V('dpc')||'cash',led:V('dpl')!=='0',pay:[],st:'open'});save()}
function dPay(id){const d=S.debts.find(x=>x.id===id),a=Math.min(sfn(V('dq'+id)),dRem(d));if(!a)return;d.pay.push({id:Date.now(),d:dk(),a,ac:V('dc'+id)||'cash'});if(dRem(d)<=0)d.st='closed';save()}
function dClose(id){const d=S.debts.find(x=>x.id===id);d.st=d.st==='closed'?'open':'closed';save()}
function dDel(id){if(confirm('Qarz yozuvi o‘chirilsinmi? Balansga ta‘siri ham bekor bo‘ladi.')){S.debts=S.debts.filter(x=>x.id!==id);save()}}
function pQarz(){
  if(W==='d')return `<p class="mu">Qarzlar shaxsiy hisobda yuritiladi.</p><button class="btn" onclick="W='p';render()">Shaxsiyga o‘tish</button>`;
  const acs=`<option value="cash">Naqd</option><option value="card">Karta</option>`;
  const card=d=>{const rem=dRem(d),paid=d.a-rem,n=d.due?dl(d.due):null,late=d.st!=='closed'&&n!==null&&n<0,bor=d.k==='borrow';
    return `<div class="dbt ${bor?'':'lend'} ${late?'late':''}" style="${d.st==='closed'?'opacity:.6':''}"><div style="display:flex;justify-content:space-between;gap:8px"><b style="font:700 18px Fraunces,serif">${esc(d.p)}</b><button class="x" onclick="dDel(${d.id})">×</button></div>
    <p class="mu" style="margin:2px 0 6px">${bor?'Men qarzdorman':'Menga qarzdor'}${d.n?', '+esc(d.n):''}</p><div class="bar"><i style="width:${d.a?paid/d.a*100:0}%"></i></div>
    <p style="margin:6px 0 0"><b>${num(rem)}</b> <span class="mu">qoldi, jami ${num(d.a)}</span></p><p class="mu" style="margin:2px 0 8px;${late?'color:var(--bad)':''}">${d.st==='closed'?'Yopilgan':d.due?'Muddat: '+d.due.slice(8)+'.'+d.due.slice(5,7)+'.'+d.due.slice(0,4)+', '+dlTxt(n):'Muddat belgilanmagan'}</p>
    ${d.st!=='closed'?`<div class="in"><input id="dq${d.id}" type="text" inputmode="numeric" placeholder="${bor?'Qaytardim':'Qaytarib berdi'}, so‘m"><select id="dc${d.id}" style="flex:0 0 96px">${acs}</select><button class="btn" onclick="dPay(${d.id})">+</button></div>`:''}
    <div class="in" style="margin:0"><button class="btn s" style="flex:1" onclick="dClose(${d.id})">${d.st==='closed'?'Qayta ochish':'Yopish'}</button></div>${d.pay.length?`<p class="mu" style="margin:8px 0 0;font-size:12px">To‘lovlar: ${d.pay.map(x=>x.d.slice(8)+'.'+x.d.slice(5,7)+' '+num(x.a)).join(', ')}</p>`:''}</div>`};
  const open=S.debts.filter(d=>d.st!=='closed').sort((a,b)=>(a.due||'9')>(b.due||'9')?1:-1),shut=S.debts.filter(d=>d.st==='closed');
  const owe=open.filter(d=>d.k==='borrow'),lent=open.filter(d=>d.k==='lend'),sm=a=>a.reduce((s,d)=>s+dRem(d),0);
  return `<div class="sum"><div><span class="mu">Men qarzdorman</span><b class="out-c">${num(sm(owe))}</b></div><div><span class="mu">Menga qarzdor</span><b class="in-c">${num(sm(lent))}</b></div></div>
  <div class="goal"><b>Yangi qarz</b><div class="in" style="margin-top:10px"><select id="dpk"><option value="borrow">Men qarz oldim</option><option value="lend">Men qarz berdim</option></select></div>
  <div class="in"><input id="dpn" placeholder="Kim bilan (ism)"></div><div class="in"><input id="dpa" type="text" inputmode="numeric" placeholder="Summa, so‘m"><select id="dpc" style="flex:0 0 96px">${acs}</select></div>
  <div class="in"><input id="dpd" type="date"><span class="mu" style="align-self:center;white-space:nowrap">muddat</span></div><div class="in"><input id="dpt" placeholder="Izoh (ixtiyoriy)"></div>
  <div class="in"><select id="dpl"><option value="1">Balansga ta‘sir qilsin</option><option value="0">Faqat yozib qo‘yish</option></select></div><button class="btn" onclick="dAdd()">Qo‘shish</button></div>
  ${owe.length?`<h2>Men qarzdorman</h2>${owe.map(card).join('')}`:''}${lent.length?`<h2>Menga qarzdor</h2>${lent.map(card).join('')}`:''}${shut.length?`<h2>Yopilgan</h2>${shut.map(card).join('')}`:''}${!S.debts.length?'<p class="mu">Qarz yozuvi yo‘q.</p>':''}`}

// ---- Hisobot ----
function pHisob(){
  const mk=mKey(PF.mo),pk=mKey(PF.mo-1),L=mList(W,mk.k),P=mList(W,pk.k),inn=mSum(L,'in'),ou=mSum(L,'out'),pou=mSum(P,'out'),nd=new Date(mk.d.getFullYear(),mk.d.getMonth()+1,0).getDate(),el=PF.mo===0?new Date().getDate():nd,mn=MON[mk.d.getMonth()];
  const cat={};L.filter(m=>m.k==='out').forEach(m=>{const c=m.c||'Boshqa';cat[c]=(cat[c]||0)+m.a});const cs=Object.entries(cat).sort((a,b)=>b[1]-a[1]);
  const day=[...Array(nd)].map((_,i)=>L.filter(m=>m.k==='out'&&m.d.endsWith('-'+pad(i+1))).reduce((a,m)=>a+m.a,0)),mx=Math.max(1,...day);
  const top=L.filter(m=>m.k==='out').sort((a,b)=>b.a-a.a).slice(0,5).map(mRow).join('');
  const tr=[5,4,3,2,1,0].map(o=>{const k=mKey(PF.mo-o).k,l=mList(W,k);return{l:MON[+k.slice(5)-1].slice(0,3),i:mSum(l,'in'),o:mSum(l,'out')}}),tm=Math.max(1,...tr.flatMap(x=>[x.i,x.o]));
  const diff=pou?Math.round((ou-pou)/pou*100):null;
  return `<div class="in"><button class="btn s" onclick="PF.mo--;render()">‹</button><button class="btn s" onclick="PF.mo=0;render()">${mn[0].toUpperCase()+mn.slice(1)} ${mk.d.getFullYear()}</button><button class="btn s" onclick="PF.mo++;render()">›</button></div>
  <section class="hero"><p class="lab">Oylik xulosa</p><h1 style="font-size:32px">${inn-ou>=0?'+':'−'}${num(Math.abs(inn-ou))} so‘m</h1><p class="mu">Kirim ${num(inn)}, chiqim ${num(ou)}.${inn?` Jamg‘arish ulushi ${Math.round((inn-ou)/inn*100)}%.`:''}</p><div class="pbal"><div><span>💵 Naqd chiqim</span><b>${num(mSum(L,'out','cash'))}</b></div><div><span>💳 Karta chiqim</span><b>${num(mSum(L,'out','card'))}</b></div></div></section>
  <div class="sum"><div><span class="mu">Kunlik o‘rtacha chiqim</span><b>${num(Math.round(ou/Math.max(1,el)))}</b></div><div><span class="mu">O‘tgan oyga nisbatan</span><b class="${diff>0?'out-c':'in-c'}">${diff===null?'—':(diff>0?'+':'')+diff+'%'}</b></div></div>
  <h2>Chiqim kategoriyalari</h2>${cs.map(([c,v])=>`<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between"><span>${CI[c]||''} ${esc(c)}</span><span class="mu">${num(v)}, ${Math.round(v/Math.max(1,ou)*100)}%</span></div><div class="bar"><i style="width:${v/Math.max(1,ou)*100}%"></i></div></div>`).join('')||'<p class="mu">Bu oyda chiqim yo‘q.</p>'}
  <h2>Kunlar bo‘yicha chiqim</h2><div class="bars2">${day.map(v=>`<i style="height:${Math.max(2,v/mx*80)}px"></i>`).join('')}</div>
  <h2>Eng katta chiqimlar</h2>${top||'<p class="mu">Yo‘q.</p>'}
  <h2>So‘nggi 6 oy</h2><div class="bars2" style="height:90px;gap:6px">${tr.map(x=>`<div style="flex:1;display:flex;gap:2px;align-items:flex-end;height:90px"><i style="height:${Math.max(2,x.i/tm*90)}px;background:var(--ac)"></i><i style="height:${Math.max(2,x.o/tm*90)}px;background:var(--bad)"></i></div>`).join('')}</div><div style="display:flex;gap:6px">${tr.map(x=>`<span class="mu" style="flex:1;text-align:center;font-size:11px">${x.l}</span>`).join('')}</div><p class="mu" style="margin:6px 0 0;font-size:12px">Yashil: kirim, qizil: chiqim.</p>`}

// ---- Reja: byudjet, jamg'arma, boshlang'ich qoldiq ----


function sgDel(id){if(confirm('Maqsad o‘chirilsinmi?')){S.fin.sg=S.fin.sg.filter(x=>x.id!==id);save()}}
function pReja(){
  finInit();const o=S.fin.open[W],mk=mKey(0).k,po=mSum(mList('p',mk),'out'),bud=S.fin.budget||0,n0=new Date(),dl2=new Date(n0.getFullYear(),n0.getMonth()+1,0).getDate()-n0.getDate()+1;
  const goals=S.fin.sg.map(g=>{const p=Math.min(100,g.s/g.a*100);return `<div class="goal"><div class="h"><b>${esc(g.t)}</b><button class="x" onclick="sgDel(${g.id})">×</button></div><div class="bar" style="margin:8px 0"><i style="width:${p}%"></i></div><p class="mu" style="margin:0 0 8px">${num(g.s)} / ${num(g.a)} (${Math.round(p)}%). Qoldi ${num(Math.max(0,g.a-g.s))}.</p><div class="in" style="margin:0"><input id="sgp${g.id}" type="text" inputmode="numeric" placeholder="Qo‘shilgan summa"><button class="btn" onclick="sgPut(${g.id})">+</button></div></div>`}).join('');
  return `${pCurUi()}<h2>Oylik byudjet (shaxsiy chiqim)</h2><div class="in"><input type="text" inputmode="numeric" placeholder="Oylik limit, so‘m" value="${bud||''}" onchange="S.fin.budget=sfn(this.value);save()"></div>${bud?`<div class="bar"><i style="width:${Math.min(100,po/bud*100)}%;${po>bud?'background:var(--bad)':''}"></i></div><p class="mu">Sarflandi ${num(po)} / ${num(bud)}. ${po>bud?'Limitdan '+num(po-bud)+' oshdi.':'Qoldi '+num(bud-po)+', kuniga taxminan '+num(Math.floor((bud-po)/dl2))+' so‘m.'}</p>`:'<p class="mu">Limit qo‘ysang, ilova qolgan summani va kunlik me‘yorni ko‘rsatadi.</p>'}
  ${pSgUi()}`}

function pul(){
  finInit();
  const seg=[['b','🏠 Bosh'],['t','🧾 Tarix'],['q','🤝 Qarzlar'],['h','📈 Hisobot'],['r','🎯 Reja']].map(x=>`<button class="${PV===x[0]?'on':''}" onclick="PV='${x[0]}';render()">${x[1]}</button>`).join('');
  return `<div class="top"><p class="d">Pul</p></div><div class="seg" style="margin-top:12px"><button class="${W==='p'?'on':''}" onclick="W='p';render()">👤 Shaxsiy</button><button class="${W==='d'?'on':''}" onclick="W='d';render()">🏪 Dokon</button></div><div class="seg sc">${seg}</div>${PV==='b'?pBosh():PV==='t'?pTarix():PV==='q'?pQarz():PV==='h'?pHisob()+pTypeRep()+pInsUi():pReja()+pCatBudUi()+pRcUi()}`}

function authView(msg){
  return `<div class="auth"><img src="favicon.svg" width="64" height="64" alt="" style="border-radius:16px;margin-bottom:16px"><h1>Kunlik tizim</h1>${brand()}<p class="mu">Kirish uchun login va parol kiriting.</p><div style="margin-top:20px"><div class="in"><input id="lg" placeholder="Login yoki email" autocapitalize="none" autocomplete="username"></div><div class="in"><input id="pw" type="password" placeholder="Parol (kamida 6 belgi)" autocomplete="current-password"></div></div><p class="err" id="er">${msg||''}</p><button class="big" style="margin-top:0" onclick="auth(false)">Kirish</button></div>`;
}

const topbar=()=>`<div class="tbar"><button class="tbb" onclick="qpOpen()" aria-label="Tezkor reja qo‘shish">＋</button><button class="tbb" onclick="srOpen()" aria-label="Qidiruv">🔍</button><button class="tbb" onclick="nwOpen()" aria-label="Hozir nima qilay">🎯</button><button class="tbb ${tab==='s'?'on':''} ${XJ().unseen()?'edot':''}" onclick="go('s')" aria-label="Sozlamalar">⚙️</button></div>`;
function navOff(){const n=document.getElementById('navc');if(n&&n.dataset.s){n.innerHTML='';n.dataset.s=''}}
function drawNav(){
  let n=document.getElementById('navc');if(!n){n=document.createElement('div');n.id='navc';document.body.appendChild(n)}
  const ai=!!(sb&&UID),sig=tab+'|'+SO+'|'+(ai?1:0);if(n.dataset.s===sig)return;n.dataset.s=sig;
  const T=[['h','☀️','Bugun'],['q','📖','Qur‘on'],['o','✅','Odat'],['m','🎯','Maqsad'],['e','📚','O‘qish'],['p','💰','Pul']];
  const b=x=>`<button class="${tab===x[0]?'on':''}" onclick="go('${x[0]}')"><span class="ni">${x[1]}</span><span>${x[2]}</span></button>`;
  const mid=ai?`<button class="navai" onclick="aiOpen()" aria-label="Yordamchi (AI)">✨</button>`:'';
  n.innerHTML=`<nav><div>${T.slice(0,3).map(b).join('')}${mid}${T.slice(3).map(b).join('')}</div></nav>`}
function render(){try{renderCore()}catch(e){try{reportErr('render: '+e.message,e.stack)}catch(x){}const a=$('#app');if(a)a.innerHTML=errView(e)}}
function renderCore(){try{rcRun()}catch(e){}
  const a=$('#app');
  if(sb&&!UID){navOff();if(!$('#lg'))a.innerHTML=authView();return}
  if(sb&&UID&&lockMsg()){navOff();a.innerHTML=lockView();return}
  if(!S.ob&&!S.ts){navOff();a.innerHTML=PULLED?obView():`<div class="auth"><h1>Yuklanmoqda</h1><p class="mu">Ma‘lumotlaringiz yuklanmadi. Internetni tekshirib, qayta urinib ko‘ring.</p><button class="big" onclick="start(UID)">Qayta urinish</button></div>`;return}
  if(tab==='s'&&sb&&UID&&OW===null){OW=0;loadOw()}
  const v=SO?srView():tab==='h'?hozir():tab==='q'?quran():tab==='o'?odatTab():tab==='e'?oqish():tab==='m'?maqsad()+meCard():tab==='s'?sozlama():pul();
  const ss=document.querySelectorAll?[...document.querySelectorAll('.seg.sc')].map(e=>({s:e.textContent.slice(0,30),l:e.scrollLeft})):[];
  const hs={};if(document.querySelectorAll)document.querySelectorAll('.hg').forEach(e=>{hs[e.dataset.k]=e.scrollLeft});
  const sy=window.scrollY||0;
  a.innerHTML=stick((SO?'':topbar())+v);
  drawNav();fixGrid(hs);fixSeg(ss);if(RWO)rwDraw();try{usHit()}catch(e){}
  if(sy>0)window.scrollTo(0,sy);
}

const cd=()=>VD||dk();
const tgl=(o,id)=>{const k=cd();(o[k]=o[k]||{})[id]=!o[k][id]};
function tg(id){tgl(S.done,id);save()}
function rl(id){tgl(S.rules,id);save()}
function wk(){const d=new Date();S.wake[dk()]=pad(d.getHours())+':'+pad(d.getMinutes());slpFin();save()}
function addT(){const v=$('#nt').value.trim();if(!v)return;const k=cd();(S.tasks[k]=S.tasks[k]||[]).push({t:v,x:0});save()}
function tk(i){const t=S.tasks[cd()][i];t.x=t.x?0:1;save()}
function dt(i){S.tasks[cd()].splice(i,1);save()}
function gp(i,v){S.goals[i].p=+v;save()}
function addG(){const v=$('#ng').value.trim();if(!v)return;S.goals.push({t:v,why:$('#nw').value.trim(),dl:'',ms:[],p:0});save()}
function dg(i){if(confirm('Maqsad o‘chirilsinmi?')){S.goals.splice(i,1);save()}}

