// ---- Takror: o‘zim tanlagan suralar va pora ----
const crRange=s=>[SP[s],s<113?Math.max(SP[s],SP[s+1]):604];
function crAdd(){const q=S.q,s=CRS<0?q.cur:CRS,[lo,hi]=crRange(s);let a=Math.round(+V('cra')||lo),b=Math.round(+V('crb')||a);a=Math.max(lo,Math.min(hi,a));b=Math.max(a,Math.min(hi,b));q.cr=q.cr||{};(q.cr[dk()]=q.cr[dk()]||[]).push({s,a,b,x:0});save()}
function crT(j){const q=S.q,k=dk(),e=q.cr[k][j],n=e.b-e.a+1;e.x=e.x?0:1;q.rd[k]=Math.max(0,r1((q.rd[k]||0)+(e.x?n:-n)));save()}
function crD(j){const q=S.q,k=dk(),e=q.cr[k][j];if(e.x)q.rd[k]=Math.max(0,r1((q.rd[k]||0)-(e.b-e.a+1)));q.cr[k].splice(j,1);save()}
function crCard(){
  const q=S.q,s=CRS<0?q.cur:CRS,[lo,hi]=crRange(s),L=(q.cr||{})[dk()]||[];
  const opts=SN.map((n,i)=>`<option value="${i}" ${i===s?'selected':''}>${i+1}. ${n}</option>`).join('');
  const rows=L.map((e,j)=>`<div class="row ${e.x?'done':''}"><span class="ck" onclick="crT(${j})">${e.x?'✓':''}</span><span class="t" onclick="crT(${j})">${SN[e.s]}, ${e.a===e.b?e.a+'-bet':e.a+'–'+e.b+'-betlar'}</span><button class="x" onclick="crD(${j})">×</button></div>`).join('');
  return `<h2>O‘zim tanlagan takror</h2><p class="mu" style="margin:0 0 8px">Xohlagan sura va betlaringni tanlab, bugungi takrorga qo‘sh.</p>${rows}<div class="in"><select onchange="CRS=+this.value;render()">${opts}</select></div><div class="in"><input id="cra" type="number" inputmode="numeric" placeholder="Betdan" value="${lo}"><input id="crb" type="number" inputmode="numeric" placeholder="Betgacha" value="${hi}"><button class="btn" onclick="crAdd()">Qo‘sh</button></div><p class="mu" style="margin:0">${SN[s]}: ${lo===hi?lo+'-bet':lo+'–'+hi+'-betlar'}.</p>`}
const jzo=()=>S.q.jz=S.q.jz||{sel:[],per:1,ptr:0};
function jzS(j){const z=jzo(),i=z.sel.indexOf(j);i<0?z.sel.push(j):z.sel.splice(i,1);if(z.ptr>=z.sel.length)z.ptr=0;save()}
function jzP(d){const z=jzo();z.per=Math.max(1,Math.min(10,z.per+d));save()}
function jzDone(){const q=S.q,z=jzo(),k=dk(),n=z.sel.length;if(!n)return;const s=z.sel.slice().sort((a,b)=>a-b),per=Math.min(z.per,n);let pg=0;for(let i=0;i<per;i++){const j=s[(z.ptr+i)%n];pg+=J[j]-J[j-1]}z.ptr=(z.ptr+per)%n;q.jd=q.jd||{};q.jd[k]=(q.jd[k]||0)+1;if(tqRd())q.rd[k]=r1((q.rd[k]||0)+pg);try{for(let i=0;i<per;i++){const j=s[((z.ptr-per+i)%n+n)%n];tqLog({m:'p',j,pa:J[j-1],pb:J[j]-1,pg:J[j]-J[j-1],t:j+'-pora',src:'jz'})}}catch(e){}save()}
function jzCard(){
  const q=S.q,z=jzo(),k=dk(),s=z.sel.slice().sort((a,b)=>a-b),n=s.length,per=Math.min(z.per,n||1),done=(q.jd||{})[k]||0;
  const chips=[...Array(30)].map((_,x)=>`<button class="${z.sel.includes(x+1)?'on':''}" onclick="jzS(${x+1})">${x+1}</button>`).join('');
  const today=n?[...Array(per)].map((_,i)=>s[(z.ptr+i)%n]):[];
  return `<h2>Pora takrori</h2><p class="mu" style="margin:0 0 8px">Takror qilmoqchi bo‘lgan poralaringni tanla, ilova ularni kunma-kun aylantiradi.</p><div class="chips">${chips}</div>
  <p class="mu" style="margin:8px 0 0">Kuniga ${z.per} pora${n?`. ${n} pora ${Math.ceil(n/per)} kunda aylanib chiqadi.`:''}</p><div class="in" style="margin-top:6px"><button class="btn s" onclick="jzP(-1)">−</button><button class="btn s" onclick="jzP(1)">+</button></div>
  ${n?`<div class="goal"><b style="font:700 17px Fraunces,serif">Bugun: ${today.map(j=>j+'-pora').join(', ')}</b>${today.map(j=>`<p class="mu" style="margin:4px 0 0">${j}-pora, ${J[j-1]}–${J[j]-1}-betlar</p>`).join('')}<button class="big ${done?'ok':''}" style="margin-top:10px" onclick="jzDone()">${done?'Bajarildi, yana bir marta':'Takror qildim'}</button></div>`:''}`}

// ---- Namoz va qazo jurnali ----
const PR=[['fajr','Bomdod'],['dhuhr','Peshin'],['asr','Asr'],['maghrib','Shom'],['isha','Xufton'],['vitr','Vitr']];
function nmS(k,p){if(k>dk())return;const N=S.nm,d=N.d[k]=N.d[k]||{},c=d[p]||0,nx=(c+1)%3;
  if(c===2){N.debt[p]=Math.max(0,(N.debt[p]||0)-1);const i=N.log.findIndex(x=>x.d===k&&x.p===p&&x.k==='miss');if(i>=0)N.log.splice(i,1)}
  if(nx===2){N.debt[p]=(N.debt[p]||0)+1;N.log.push({id:Date.now(),d:k,p,k:'miss',n:1})}
  d[p]=nx;save()}
function qzPay(p){const N=S.nm;if(!(N.debt[p]>0))return;N.debt[p]--;N.log.push({id:Date.now(),d:dk(),p,k:'paid',n:1});save()}
function qzAdd(p){const n=parseInt(prompt('Nechta qazo namoz qo‘shilsin? (eski qazolar uchun)'),10);if(!(n>0))return;S.nm.debt[p]=(S.nm.debt[p]||0)+n;S.nm.log.push({id:Date.now(),d:dk(),p,k:'add',n});save()}
function nmQ(n){const N=S.nm,k=dk();N.qb=N.qb||{};const v=Math.max(0,(N.qb[k]||0)+n);if(v===(N.qb[k]||0))return;N.qb[k]=v;hd(n)}
function namoz(){
  const T0=dk(),now=new Date(),N=S.nm,d0=new Date(now.getFullYear(),now.getMonth()+NMo,1),y=d0.getFullYear(),m=d0.getMonth(),nd=new Date(y,m+1,0).getDate(),key=x=>`${y}-${pad(m+1)}-${pad(x)}`;
  let tot=0,got=0,qz=0;
  const today=PR.map(([p,t])=>{const s_=((N.d[T0]||{})[p])||0;return `<button class="${s_===1?'on':s_===2?'bad':''}" onclick="nmS('${T0}','${p}')">${s_===1?'✓ ':s_===2?'✗ ':''}${t}${ptT(PK[p])?`<small>${ptT(PK[p])}</small>`:''}</button>`}).join('');
  const head=gHead(y,m,nd,T0,1),NL2=PR.map(([p,t])=>`<div class="mr" style="display:flex;align-items:center">${t}</div>`);
  const body=PR.map(([p,t])=>`<tr style="height:48px">${[...Array(nd)].map((_,i)=>{const kk=key(i+1),s_=((N.d[kk]||{})[p])||0,fu=kk>T0;if(!fu&&p!=='vitr'){tot++;if(s_===1)got++;if(s_===2)qz++}return `<td class="${gCls(y,m,i+1,T0)}"><button class="cell ${s_===1?'on':s_===2?'qz':''}" ${fu?'disabled':''} onclick="nmS('${kk}','${p}')"></button></td>`}).join('')}</tr>`).join('');
  const debt=PR.reduce((a,[p])=>a+(N.debt[p]||0),0),qb=(N.qb||{})[T0]||0;
  const rows=PR.map(([p,t])=>`<div class="row"><span class="t">${t}<br><span class="mu">${N.debt[p]||0} ta qazo</span></span><button class="btn s" style="padding:8px 12px" onclick="qzPay('${p}')">O‘qidim</button><button class="btn s" style="padding:8px 12px" onclick="qzAdd('${p}')">+</button></div>`).join('');
  const lbl={miss:'qazo qilindi',paid:'qazo o‘qildi',add:'eski qazo qo‘shildi'},nmz=Object.fromEntries(PR);
  const log=N.log.slice().reverse().slice(0,12).map(x=>`<div class="row"><span class="t">${nmz[x.p]}<br><span class="mu">${x.d.slice(8)}.${x.d.slice(5,7)}, ${lbl[x.k]}${x.k==='add'?' ('+x.n+' ta)':''}</span></span></div>`).join('');
  return `${ptCard()}<section class="hero" style="margin-top:12px"><p class="lab">Bugungi namozlar</p><div class="np" style="margin-top:8px">${today}</div><p class="mu" style="margin-top:8px">Bir bosish: o‘qildi, ikki: qazo, uch: bekor qilish.</p></section>
  <h2>Namozda o‘qilgan Qur‘on</h2><p class="mu" style="margin:0 0 8px">Namozlarda o‘qigan betlaring odatiy hatm hisobiga qo‘shiladi.</p><div class="in"><button class="btn s" onclick="nmQ(-1)">−1</button><div class="row" style="flex:1;justify-content:center;margin:0"><b>Bugun ${qb} bet</b></div><button class="btn" onclick="nmQ(1)">+1 bet</button></div>
  ${nhCard()}
  <h2>${MON[m][0].toUpperCase()+MON[m].slice(1)} ${y}</h2><div class="in"><button class="btn s" onclick="NMo--;render()">‹</button><button class="btn s" onclick="NMo=0;render()">Shu oy</button><button class="btn s" onclick="NMo++;render()">›</button></div>
  <div class="sum"><div><span class="mu">O‘qilgan namozlar</span><b>${tot?Math.round(got/tot*100):0}%</b></div><div><span class="mu">Shu oy qazo</span><b>${qz}</b></div></div>${mgrid(NL2,head,body,'n',48)}<p class="mu" style="margin:6px 0 0">Yashil: o‘qildi. Qizil: qazo. Katakni bossang, holat almashadi.</p>
  <h2>Qazo namozlar jurnali</h2><div class="sum"><div class="w"><span class="mu">Jami qazo qarzi</span><b>${debt} ta</b></div></div>${rows}${log?`<p class="mu" style="margin:12px 0 6px">So‘nggi yozuvlar</p>${log}`:''}`}

const HC=['var(--ac)','var(--go)','#6f9fd8','#b27ad6','#d96f8f','#c9a227'];
function gHead(y,m,nd,T0,nn){return `<tr>${nn?'':'<th class="sk" style="background:var(--c1)"></th>'}${[...Array(nd)].map((_,i)=>{const d=i+1,kk=`${y}-${pad(m+1)}-${pad(d)}`,wd=new Date(y,m,d).getDay();return `<th class="${kk===T0?'td tdy':''}${wd===0||wd===6?' we':''}"><span style="font-size:11px">${DAYS[wd].slice(0,2)}</span><br><b style="font-size:15px">${d}</b></th>`}).join('')}</tr>`}
function mgrid(names,head,body,k,rh){return `<div class="mg" style="--rh:${rh}px"><div class="mn"><div class="mh"></div>${names.join('')}</div><div class="hg" data-k="${k}"><table>${head}${body}</table></div></div>`}
function gCls(y,m,d,T0){const kk=`${y}-${pad(m+1)}-${pad(d)}`,wd=new Date(y,m,d).getDay();return (kk===T0?'tdy':'')+(wd===0||wd===6?' we':'')}
function fixSeg(ss){if(!document.querySelectorAll)return;[...document.querySelectorAll('.seg.sc')].forEach((e,i)=>{const hint=()=>{e.classList.toggle('mr-r',e.scrollLeft+e.clientWidth<e.scrollWidth-4);e.classList.toggle('mr-l',e.scrollLeft>4)};if(!e._h){e._h=1;e.addEventListener('scroll',hint,{passive:true})}const o=ss[i];if(o&&o.s===e.textContent.slice(0,30))e.scrollLeft=o.l;const b=e.querySelector('button.on');if(b){const l=b.offsetLeft,r=l+b.offsetWidth;if(l<e.scrollLeft||r>e.scrollLeft+e.clientWidth)e.scrollLeft=Math.max(0,l-(e.clientWidth-b.offsetWidth)/2)}hint()})}
function fixGrid(hs){if(!document.querySelectorAll)return;document.querySelectorAll('.hg').forEach(e=>{const k=e.dataset.k;if(hs[k]!==undefined)e.scrollLeft=hs[k];else{const t=e.querySelector('th.td');if(t)e.scrollLeft=Math.max(0,t.offsetLeft-e.clientWidth/2+t.offsetWidth/2)}})}

// ---- Maqsadlarga mos odatlar ----
const HB={
 'Hofizi Qur‘on bo‘lish':[['📖','Har kuni 3 bet Qur‘on yodlash'],['🔁','Kuniga 5 bet takror'],['🎧','15 daqiqa Qur‘on tinglash']],
 'IELTS 8–9 ball':[['🎓','20 ta yangi so‘z yodlash'],['🎧','30 daqiqa Listening yoki Reading'],['🗣','10 daqiqa Speaking mashqi']],
 'O‘qituvchi bo‘lib ishlash':[['🧑‍🏫','30 daqiqa kasbiy tayyorgarlik'],['📝','Bitta dars rejasi ustida ishlash']],
 'Prava olish':[['🚗','20 ta test savoli yechish'],['🛣','Yo‘l qoidalaridan 1 mavzu takror']],
 'Zalda yaxshi tana qurish':[['💪','Mashq (zal yoki uy)'],['💧','2 litr suv ichish'],['🥗','Oqsilga boy ovqat']],
 'Pul jamg‘arish':[['💰','Kunlik xarajatni yozib borish']],
 'Kitob o‘qish':[['📚','20 bet kitob o‘qish']],
 'Universitetni a‘lo tugatish':[['🏫','30 daqiqa dars tayyorgarligi'],['📓','Konspektni takrorlash']]
};
const HGEN=[['🤲','Tong va kech zikri'],['🌅','Maqsad vaqtida turish'],['📵','Uyqudan oldin telefonsiz 30 daqiqa']];
const hnorm=t=>t.toLowerCase().replace(/[‘’'`ʻ]/g,'').replace(/[^a-z0-9]/g,'');
function suggList(){const have=new Set(S.hab.map(x=>hnorm(x.t))),out=[];
  S.goals.forEach(g=>(HB[g.t]||[]).forEach(([e,t])=>{if(!have.has(hnorm(t))&&!out.some(o=>o[1]===t))out.push([e,t,g.t])}));
  HGEN.forEach(([e,t])=>{if(!have.has(hnorm(t))&&!out.some(o=>o[1]===t))out.push([e,t,'Umumiy'])});return out}
function sgAdd(i){const o=suggList()[i];if(!o)return;S.hab.push({id:'h'+Date.now()+i,t:o[1],e:o[0]});save()}
function sgAll(){suggList().forEach(([e,t],i)=>S.hab.push({id:'h'+Date.now()+i,t,e}));save()}
function sgMig(){if(S.sg)return;S.sg=1;const have=new Set(S.hab.map(x=>hnorm(x.t)));let n=0;
  S.goals.forEach(g=>(HB[g.t]||[]).slice(0,2).forEach(([e,t])=>{if(!have.has(hnorm(t))){have.add(hnorm(t));S.hab.push({id:'h'+Date.now()+(n++),t,e})}}));
  HGEN.slice(0,1).forEach(([e,t])=>{if(!have.has(hnorm(t)))S.hab.push({id:'h'+Date.now()+(n++),t,e})});save()}
function suggCard(){const L=suggList();if(!L.length)return '';
  return `<h2>Maqsadlarga mos odatlar</h2><p class="mu" style="margin:0 0 8px">Maqsadlaringga yordam beradigan odatlar. Bosib qo‘shasan.</p><div class="chips">${L.map(([e,t],i)=>`<button onclick="sgAdd(${i})">${e} ${esc(t)}</button>`).join('')}</div><button class="ghost" onclick="sgAll()">Hammasini qo‘sh (${L.length})</button>`}

// ---- Kitob o‘qish ----
function ktAdd(st){const t=V('kt'),a=V('ka'),n=Math.round(+V('kn'))||0;if(!t)return;S.kt.books.push({id:Date.now(),t,a,n,p:0,st,fin:'',r:0,sum:''});save()}
const ktB=id=>S.kt.books.find(x=>x.id===id),ktLog=(b,d)=>{if(d>0)S.kt.log.push({id:Date.now()+Math.random(),d:dk(),b:b.id,n:d})};
function ktPg(id){const b=ktB(id),v=Math.round(+V('kp'+id));if(!(v>=0))return;const nv=b.n?Math.min(v,b.n):v;ktLog(b,nv-b.p);b.p=nv;if(b.n&&b.p>=b.n){b.st='t';b.fin=dk()}save()}
function ktQ(id,n){const b=ktB(id),a=b.n?Math.min(n,b.n-b.p):n;b.p+=a;ktLog(b,a);if(b.n&&b.p>=b.n){b.st='t';b.fin=dk()}save()}
function ktFin(id){const b=ktB(id);if(b.n){ktLog(b,b.n-b.p);b.p=b.n}b.st='t';b.fin=dk();save()}
function ktSt(id,st){const b=ktB(id);b.st=st;if(st==='o')b.fin='';save()}
function ktSum(id,v){ktB(id).sum=v;save()}
function ktR(id,v){ktB(id).r=v;save()}
function ktDel(id){if(confirm('Kitob o‘chirilsinmi?')){S.kt.books=S.kt.books.filter(x=>x.id!==id);idbDel(id).catch(()=>{});cloudDel(id);rdClose();save()}}
function ktGoal(v){S.kt.goal=Math.max(1,+v||20);save()}
function kitob(){
  const K=S.kt,k=dk(),tp=K.log.filter(x=>x.d===k).reduce((a,x)=>a+x.n,0),goal=K.goal||20,mo=k.slice(0,7),mp=K.log.filter(x=>x.d.startsWith(mo)).reduce((a,x)=>a+x.n,0);
  let st=0;for(let i=0;i<120;i++){if(K.log.some(x=>x.d===dAgo(i)))st++;else if(i>0)break}
  const fin=K.books.filter(b=>b.st==='t'),yr=fin.filter(b=>b.fin&&b.fin.startsWith(k.slice(0,4))).length;
  const area=(b)=>`<textarea placeholder="Xulosa: asosiy fikrlar va o‘rganganlarim" onchange="ktSum(${b.id},this.value)">${esc(b.sum||'')}</textarea>`;
  const reading=K.books.filter(b=>b.st==='o').map(b=>`<div class="goal"><div class="h"><b style="font:700 18px Fraunces,serif">${esc(b.t)}</b><button class="x" onclick="ktDel(${b.id})">×</button></div>${b.a?`<p class="mu" style="margin:0">${esc(b.a)}</p>`:''}<div class="bar" style="margin:8px 0"><i style="width:${b.n?Math.min(100,b.p/b.n*100):0}%"></i></div><p class="mu" style="margin:0 0 8px">${b.p}${b.n?' / '+b.n:''} bet</p>
    <div class="in"><input id="kp${b.id}" type="number" inputmode="numeric" placeholder="Hozirgi bet" value="${b.p||''}"><button class="btn" onclick="ktPg(${b.id})">Saqla</button></div>
    <div class="in">${[5,10,20].map(n=>`<button class="btn s" style="flex:1;padding:10px 0" onclick="ktQ(${b.id},${n})">+${n}</button>`).join('')}<button class="btn" style="flex:1;padding:10px 0" onclick="ktFin(${b.id})">Tugatdim</button></div>${b.pdf?`<p class="mu" style="margin:4px 0;font-size:12px">${PUPL[b.id]?'Bulutga yuklanmoqda…':b.cloud?'Bulutda saqlangan: boshqa qurilmada ham ochiladi.':'Faqat shu telefonda saqlangan.'}</p>`:''}${b.pdf?`<div class="in"><button class="btn" style="flex:1" onclick="rdOpen(${b.id})">PDF o‘qish (${b.cur||1}-bet)</button><button class="btn s" onclick="ktPdfDel(${b.id})">PDF o‘chirish</button></div>`:`<label class="btn s" style="display:block;text-align:center;margin:6px 0;cursor:pointer">PDF qo‘shish<input type="file" accept="application/pdf" style="display:none" onchange="ktPdf(this,${b.id})"></label>`}${area(b)}</div>`).join('');
  const planned=K.books.filter(b=>b.st==='r').map(b=>`<div class="row"><span class="t">${esc(b.t)}<br><span class="mu">${esc(b.a||'')}${b.n?' '+b.n+' bet':''}</span></span><button class="btn s" style="padding:8px 12px" onclick="ktSt(${b.id},'o')">Boshlash</button><button class="x" onclick="ktDel(${b.id})">×</button></div>`).join('');
  const done=fin.slice().reverse().map(b=>`<div class="goal"><div class="h"><b style="font:700 17px Fraunces,serif">${esc(b.t)}</b><button class="x" onclick="ktDel(${b.id})">×</button></div><p class="mu" style="margin:0">${esc(b.a||'')} Tugatilgan: ${b.fin||''}</p><div class="stars" style="margin:6px 0 4px">${[1,2,3,4,5].map(n=>`<button class="${(b.r||0)>=n?'on':''}" style="color:var(--mu)" onclick="ktR(${b.id},${n})">★</button>`).join('')}</div>${area(b)}<button class="ghost" style="margin-top:6px" onclick="ktSt(${b.id},'o')">Qayta o‘qish</button></div>`).join('');
  return `<section class="hero"><p class="lab">Kitob o‘qish</p><h1 style="font-size:34px">${tp} / ${goal} bet</h1><div class="bar" style="margin:8px 0"><i style="width:${Math.min(100,tp/goal*100)}%"></i></div><p class="mu">Bugungi maqsad. ${st} kun ketma-ket o‘qigansan. Shu oy ${mp} bet, bu yil ${yr} ta kitob tugatilgan.</p></section>
  <div class="in" style="margin-top:8px"><input type="number" value="${goal}" onchange="ktGoal(this.value)"><span class="mu" style="align-self:center;white-space:nowrap">kunlik maqsad, bet</span></div>
  ${reading||'<p class="mu">Hozir o‘qilayotgan kitob yo‘q. Pastdan birinchi kitobingni qo‘sh.</p>'}
  <h2>Kitob qo‘shish</h2><div class="in"><input id="kt" placeholder="Kitob nomi"></div><div class="in"><input id="ka" placeholder="Muallif"><input id="kn" type="number" placeholder="Betlar" style="max-width:90px"></div><div class="in"><button class="btn" style="flex:1" onclick="ktAdd('o')">O‘qishni boshlash</button><button class="btn s" style="flex:1" onclick="ktAdd('r')">Rejaga qo‘shish</button></div><label class="btn s" style="display:block;text-align:center;cursor:pointer">PDF yuklab o‘qishni boshlash<input type="file" accept="application/pdf" style="display:none" onchange="ktPdf(this)"></label><p class="mu" style="margin:6px 0 0;font-size:12px">PDF telefonda saqlanadi va hisobga kirgan bo‘lsang, bulutga ham yuklanadi (har fayl 50 MB gacha). Zaxira nusxaga PDF kirmaydi.</p>
  ${planned?`<h2>O‘qish rejasi</h2>${planned}`:''}${done?`<h2>Tugatilgan kitoblar</h2>${done}`:''}`}

