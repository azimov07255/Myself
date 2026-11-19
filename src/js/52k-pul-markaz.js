// ---- PUL MARKAZI: moliyaviy sog'liq balli, kunlik xulosa (3D minora bilan), tejash tahlilchisi va chellenj, biznes markazi, pul yutuqlari. Hammasi mavjud yozuvlardan hisoblanadi. Prefiks: pmz ----
const pmzCl=(v,a,b)=>Math.max(a,Math.min(b,v));
const pmzSum=L=>L.reduce((a,m)=>a+m.a,0);
const pmzRange=(f,k0,k1)=>S.money.filter(m=>m.w==='p'&&m.k===f&&m.d>=k0&&m.d<=k1);
const pmzOutD=k=>pmzSum(S.money.filter(m=>m.w==='p'&&m.k==='out'&&m.d===k));
const pmzSav=()=>((S.fin&&S.fin.sg)||[]).reduce((a,g)=>a+(g.s||0),0);
const pmzDow=['dushanba','seshanba','chorshanba','payshanba','juma','shanba','yakshanba'];
let PMZB=[];
function pmzLim(){const w=W;W='p';let l=0;try{l=pDaily().lim||0}catch(e){}W=w;return l}
function pmzExp(){const o=pmzSum(pmzRange('out',dAgo(29),dk()));let pl=0;try{pl=drjPlan().mo||0}catch(e){}return Math.max(o,pl)}
// ---------- moliyaviy sog'liq ----------
function pmzHealth(){
  const td=dk(),d30=dAgo(29),in30=pmzSum(pmzRange('in',d30,td)),out30=pmzSum(pmzRange('out',d30,td));
  if(!in30&&!out30)return null;
  const sav=in30>0?(in30-out30)/in30:0,p1=pmzCl(sav/.3,0,1)*25,sv=pmzSav(),me=pmzExp(),mo=me>0?sv/me:0,p2=pmzCl(mo/3,0,1)*25,lim=pmzLim();
  let ok=0,ns=0;for(let i=1;i<=14;i++){const sp=pmzOutD(dAgo(i));if(sp===0)ns++;if(!lim||sp<=lim)ok++}
  const p3=lim?ok/14*20:10,p4=pmzCl(ns/4,0,1)*15,typed=pmzRange('out',d30,td).filter(m=>m.t),kr=pmzSum(typed.filter(m=>m.t==='k')),sh=out30?kr/out30:0,p5=typed.length?(1-pmzCl(sh/.2,0,1))*15:7.5;
  const parts=[
   {k:'sav',e:'💎',t:'Jamg‘arish darajasi',v:p1,mx:25,tip:`Daromadning 30% ini jamg‘arsang +${Math.round(25-p1)} ball (hozir ${Math.round(sav*100)}%).`},
   {k:'cus',e:'🛡',t:'Xavfsizlik yostig‘i',v:p2,mx:25,tip:`Jamg‘arma ${mo.toFixed(1)} oylik xarajatni qoplaydi; maqsad 3 oy (+${Math.round(25-p2)} ball).`},
   {k:'bud',e:'🎯',t:'Kunlik chegarada',v:p3,mx:20,tip:lim?`Oxirgi 14 kundan ${ok} tasida chegara saqlandi (+${Math.round(20-p3)} ball).`:'Kunlik chegara qo‘y: Pul → Reja (ball aniqlashadi).'},
   {k:'nos',e:'🌱',t:'Sarfsiz kunlar',v:p4,mx:15,tip:`Oxirgi 14 kunda ${ns} sarfsiz kun; 4 tasi maqsad (+${Math.round(15-p4)} ball).`},
   {k:'unn',e:'🧹',t:'Keraksiz xarajat',v:p5,mx:15,tip:typed.length?`Keraksiz xarajat ulushi ${Math.round(sh*100)}%; 20% dan past bo‘lsin.`:'Xarajat kiritganda turini belgila: zarur / xohish / keraksiz.'}];
  const total=Math.round(parts.reduce((a,p)=>a+p.v,0)),weak=parts.slice().sort((a,b)=>(a.v/a.mx)-(b.v/b.mx))[0];
  return{total,parts,weak,label:total>=80?'A‘lo':total>=60?'Yaxshi':total>=40?'O‘rtacha':'Boshlang‘ich',sav,mo,ns,ok,lim}}
// ---------- qayerda pul oqyapti ----------
function pmzLeaks(){
  const td=dk(),cur=pmzRange('out',dAgo(29),td),prev=pmzRange('out',dAgo(59),dAgo(30));if(cur.length<5)return null;
  const by=L=>{const o={};L.forEach(m=>{const c=m.c||'Boshqa';o[c]=(o[c]||0)+m.a});return o},C=by(cur),P=by(prev),cats=Object.keys(C).map(c=>({c,a:C[c],p:P[c]||0,ch:P[c]?Math.round((C[c]-P[c])/P[c]*100):null})).sort((a,b)=>b.a-a.a);
  const small=cur.filter(m=>m.a<30000),ss=pmzSum(small),dw=[0,0,0,0,0,0,0];cur.forEach(m=>{dw[drjDow(m.d)]+=m.a});const tot=pmzSum(cur),mxI=dw.indexOf(Math.max(...dw));
  const tips=[];let pot=0;
  const gr=cats.find(x=>x.p>0&&x.a>=100000&&x.a/x.p>=1.25);if(gr){const sv=Math.round(gr.a*.2);pot+=sv;tips.push(`${CI[gr.c]||''} ${gr.c}: oldingi 30 kundan +${gr.ch}% oshdi (${num(gr.p)} → ${num(gr.a)}). 20% kamaytirsang oyiga ~${num(sv)} so‘m tejaysan.`)}
  if(small.length>=8){const sv=Math.round(ss/2);pot+=sv;tips.push(`🪙 Kichik xarajatlar (30 000 dan kam): ${small.length} ta, jami ${num(ss)} so‘m. Yarmini tejasang oyiga ~${num(sv)} so‘m.`)}
  if(tot>0&&dw[mxI]>=tot/7*1.5)tips.push(`📅 Eng ko‘p sarf: ${pmzDow[mxI]} (${num(dw[mxI])} so‘m, haftaning ${Math.round(dw[mxI]/tot*100)}%). O‘sha kuni oldindan chegara qo‘y.`);
  return{cats,small:{n:small.length,sum:ss},topDow:mxI,tips,pot,tot}}
const pmzChS=()=>{finInit();return S.fin.ch||null};
function pmzChStart(){finInit();S.fin.ch={start:dk(),n:7,need:3};save()}
function pmzChStop(){finInit();S.fin.ch=null;save()}
function pmzChInfo(){const c=pmzChS();if(!c)return null;const lim=pmzLim(),td=dk(),dots=[];let ns=0,ok=0;
  for(let i=0;i<c.n;i++){const k=drjAddD(c.start,i);if(k>td){dots.push({k,s:'f'});continue}const sp=pmzOutD(k);if(k===td){dots.push({k,s:'t',sp});continue}const s=sp===0?'n':(lim&&sp<=lim)?'o':'x';if(s==='n')ns++;if(s!=='x')ok++;dots.push({k,s,sp})}
  const done=drjAddD(c.start,c.n-1)<td;return{c,dots,ns,ok,done,win:done&&ns>=c.need}}
// ---------- yutuqlar ----------
function pmzMedals(H){
  const f=drjS(),sv=pmzSav(),g=(f.sg||[]).find(x=>x.usd)||(f.sg||[])[0],gp=g&&g.a>0?g.s/g.a:0,st=(()=>{try{return drjJz().streak}catch(e){return 0}})(),lim=pmzLim();
  let ns7=0,in7=0;for(let i=1;i<=7;i++){const sp=pmzOutD(dAgo(i));if(sp===0)ns7++;if(lim&&sp<=lim)in7++}
  return[{k:'s1',e:'💎',t:'Birinchi jamg‘arma',ok:sv>0,c:'g',h:'Jamg‘arma maqsadiga pul qo‘sh'},{k:'g25',e:'🥉',t:'Maqsadning 25%i',ok:gp>=.25,c:'b',h:'Maqsadning choragiga yet'},{k:'g50',e:'🥈',t:'Maqsadning yarmi',ok:gp>=.5,c:'s',h:'Maqsadning 50%i'},{k:'g100',e:'🏆',t:'Maqsadga yetding',ok:gp>=1,c:'g',h:'Maqsadning 100%i'},
   {k:'w2',e:'🔥',t:'2 hafta ketma-ket jamg‘arma',ok:st>=2,c:'g',h:'Har juma jamg‘arma qil'},{k:'n3',e:'🛡',t:'7 kunda 3 sarfsiz kun',ok:ns7>=3,c:'s',h:'Bir haftada 3 kun hech narsa sotib olma'},{k:'b7',e:'🎯',t:'7 kun chegarada',ok:!!lim&&in7===7,c:'g',h:'7 kun ketma-ket chegaradan oshma'},
   {k:'bz',e:'💼',t:'Biznes sinovi boshlandi',ok:(f.bz||[]).length>0,c:'b',h:'Biznes markazida sinov yarat'},{k:'h80',e:'⭐',t:'Moliyaviy sog‘liq 80+',ok:!!H&&H.total>=80,c:'g',h:'Sog‘liq ballini 80 dan oshir'}]}
function pmzMilCheck(M){const f=drjS();f.mil=f.mil||{};let nw=[];M.forEach(m=>{if(m.ok&&!f.mil[m.k]){f.mil[m.k]=dk();nw.push(m)}});if(nw.length){PMZB=PMZB.concat(nw);setTimeout(pmzQuiet,60)}}
// save() ekranni qayta chizadi (ochiq bo'limlar yopilib qoladi); yutuq belgisini ekranga tegmasdan saqlaymiz
function pmzQuiet(){S.ts=Date.now();try{localStorage.setItem(KEY(),JSON.stringify(S))}catch(e){}clearTimeout(tm);tm=setTimeout(push,700)}
function pmzBannerOk(){PMZB=[];render()}
// ---------- Bosh ekran ----------
function pmzGoalQuick(){const u=sfn(V('pmu')),r=sfn(V('pmr'));if(!(u>0)||!(r>0)){toast('$ summa va kursni yozing');return}drjSet('usd',String(u));drjSet('rate',String(r));drjGoal()}
function pmzTower(){
  const P=drjPlan();if(P.g&&P.g.a>0)return d3CoinsCard();
  const form=`<div class="in" style="margin-top:8px"><input id="pmu" type="text" inputmode="numeric" placeholder="Maqsad, $ (masalan 1000)"><input id="pmr" type="text" inputmode="numeric" placeholder="Kurs: 1$ = so‘m"></div><button class="btn" style="width:100%" onclick="pmzGoalQuick()">Maqsad qo‘yish va minorani boshlash</button>`;
  if(!d3On())return `<h2>🪙 Jamg‘arma maqsadi</h2><div class="goal"><p class="mu" style="margin:0">Dollar maqsad qo‘y: ilova necha oyda yetishingni hisoblaydi.</p>${form}</div>`;
  const gh=[...Array(24)].map((_,k)=>`<div class="d3co g" style="transform:translateZ(${k*6}px)"></div>`).join('');
  return `<h2>🪙 Jamg‘arma minorasi</h2><div class="d3coins" role="img" aria-label="Jamg‘arma minorasi: maqsad qo‘yilmagan"><div class="d3top"><span>Maqsad qo‘yilmagan</span><b>0%</b></div><div class="d3big"><div class="d3bigc">$</div></div><div class="d3stack"><div class="d3base"></div>${gh}</div><div class="d3bot">Maqsad qo‘y: tanga minorasi o‘sishni boshlaydi</div></div><div class="goal">${form}</div>`}
function pmzBrief(H){
  const hr=new Date().getHours(),gr=hr<12?'Xayrli tong':hr<18?'Xayrli kun':'Xayrli kech',P=drjPlan(),lim=pmzLim(),sp=pmzOutD(dk()),L=pmzLeaks(),ns7=H?H.ns:0,
   tip=(H&&H.weak?H.weak.tip:'')||'Birinchi yozuvlarni kirit: ilova sog‘liq ballingni hisoblaydi.';
  const R=2*Math.PI*30,pc=H?H.total:0;
  return `<section class="hero pmzbr"><p class="lab">${gr}${S.name?', '+esc(S.name):''}! Pul markazing</p>
   <div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><div><h1 style="font-size:30px">${H?'Sog‘liq '+H.total+' / 100':'Boshlaymiz'}</h1><p class="mu" style="margin:0">${H?H.label+' daraja':'Yozuv kiriting'}</p></div>
   <svg width="74" height="74" viewBox="0 0 74 74" aria-label="Moliyaviy sog‘liq"><circle cx="37" cy="37" r="30" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="8"/><circle cx="37" cy="37" r="30" fill="none" stroke="var(--go)" stroke-width="8" stroke-linecap="round" stroke-dasharray="${R*pc/100} ${R}" transform="rotate(-90 37 37)"/><text x="37" y="43" text-anchor="middle" font-size="17" font-weight="800" fill="currentColor">${pc}</text></svg></div>
   <p style="margin:10px 0 2px">${lim?(sp<=lim?'Bugun yana <b>'+num(lim-sp)+'</b> so‘m sarflasa bo‘ladi.':'<b>Bugun chegaradan '+num(sp-lim)+' so‘m oshdi.</b>'):'Kunlik chegara qo‘yilmagan (Pul → Reja).'}</p>
   ${P.goal>0?`<p style="margin:0 0 2px">Maqsadga: <b>${P.goal>0?Math.min(100,Math.round(P.have/P.goal*100)):0}%</b>${P.eta?', ~'+P.eta+' oy qoldi':''}.</p>`:''}
   <p class="mu" style="margin:8px 0 0;font-size:13px">💡 ${esc(tip)}${L&&L.pot?' Tejash imkoniyati: ~'+num(L.pot)+' so‘m/oy (Hisobot).':''}</p></section>`}
function pmzHealthUi(H){if(!H)return `<h2>❤️ Moliyaviy sog‘liq</h2><div class="goal"><p class="mu" style="margin:0">Kamida bir necha kirim-chiqim yozilgach, ball chiqadi (jamg‘arish, yostiq, chegara, sarfsiz kunlar, keraksiz xarajat).</p></div>`;
  return `<h2>❤️ Moliyaviy sog‘liq: ${H.total} / 100</h2><div class="goal pmzc">${H.parts.map(p=>`<div class="usr" style="margin-bottom:6px"><span class="usk" style="flex-basis:150px">${p.e} ${p.t}</span><span class="usb"><i style="width:${Math.round(p.v/p.mx*100)}%"></i></span><span class="usv">${Math.round(p.v)}/${p.mx}</span></div>`).join('')}<p class="mu" style="margin:8px 0 0;font-size:13px">Eng ko‘p ball beradigan joy: <b>${H.weak.e} ${H.weak.t}</b>. ${esc(H.weak.tip)}</p></div>`}
function pmzMedalsUi(M){const e=M.filter(x=>x.ok).length;
  return `<h2>🏅 Pul yutuqlari <span class="mu" style="font-size:14px;font-family:Figtree,system-ui">${e} / ${M.length}</span></h2><div class="pmzmd">${M.map((m,i)=>`<div class="pmzm ${m.ok?'on '+m.c:''}" style="animation-delay:${-i*.6}s" title="${esc(m.ok?m.t:m.h)}"><div class="pmzc2">${m.ok?m.e:'🔒'}</div><b>${esc(m.t)}</b></div>`).join('')}</div>`}
function pmzBanner(){if(!PMZB.length)return '';const cf=[...Array(16)].map((_,i)=>`<i style="left:${(i*37)%100}%;animation-delay:${(i%6)*.25}s">${['🎉','✨','🪙','⭐'][i%4]}</i>`).join('');
  return `<div class="goal pmzban"><div class="pmzcf" aria-hidden="true">${cf}</div><b style="font:700 19px Fraunces,serif">🎉 Yangi yutuq!</b>${PMZB.map(m=>`<p style="margin:6px 0 0">${m.e} <b>${esc(m.t)}</b></p>`).join('')}<button class="btn" style="margin-top:10px" onclick="pmzBannerOk()">Ajoyib!</button></div>`}
function pmzChUi(){const I=pmzChInfo();
  if(!I)return `<h2>🎯 Tejash chellenji</h2><div class="goal pmzc"><p style="margin:0 0 8px">7 kun ichida kamida <b>3 kun hech narsa sotib olmasdan</b> yurib ko‘r. Kunlar ketma-ket bo‘lishi shart emas.</p><button class="btn" style="width:100%" onclick="pmzChStart()">Chellenjni boshlash</button></div>`;
  return `<h2>🎯 Tejash chellenji</h2><div class="goal pmzc"><div class="mrfdots pmzdots">${I.dots.map((d,i)=>`<span class="pmzdt ${d.s}" title="${d.k}">${d.s==='n'?'🌱':d.s==='o'?'✓':d.s==='x'?'✗':d.s==='t'?'•':i+1}</span>`).join('')}</div>
   <p style="margin:10px 0 0">Sarfsiz kunlar: <b>${I.ns} / ${I.c.need}</b>${I.win?' 🎉 Chellenj yutildi!':I.done?'. Bu safar bo‘lmadi, yana urinib ko‘r.':''}</p><p class="mu" style="margin:4px 0 8px;font-size:12px">🌱 sarfsiz · ✓ chegarada · ✗ oshgan · • bugun (kun oxirida hisoblanadi)</p><button class="btn s" onclick="pmzChStop()">${I.done?'Yangidan boshlash':'To‘xtatish'}</button></div>`}
function pmzLeakUi(){
  if(W!=='p'||!pmzOn())return '';const L=pmzLeaks();
  if(!L)return `<h2>🔎 Qayerda pul oqyapti?</h2><div class="goal"><p class="mu" style="margin:0">Kamida 5 ta xarajat yozilgach, tahlil chiqadi.</p></div>${pmzChUi()}`;
  const mx=Math.max(1,...L.cats.map(x=>x.a));
  return `<h2>🔎 Qayerda pul oqyapti?</h2><div class="goal pmzc"><p class="mu" style="margin:0 0 8px;font-size:13px">Oxirgi 30 kun, oldingi 30 kun bilan taqqoslangan.</p>${L.cats.slice(0,5).map(x=>`<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between"><span>${CI[x.c]||''} ${esc(x.c)}</span><span class="mu">${num(x.a)}${x.ch!==null?' · '+(x.ch>0?'+':'')+x.ch+'%':''}</span></div><div class="bar"><i style="width:${x.a/mx*100}%;${x.ch!==null&&x.ch>=25?'background:var(--bad)':''}"></i></div></div>`).join('')}
   ${L.tips.length?'<p style="margin:10px 0 4px"><b>Maslahatlar</b></p>'+L.tips.map(t=>`<p style="margin:0 0 6px;font-size:14px">${esc(t)}</p>`).join(''):'<p class="mu" style="margin:6px 0 0">Hozircha keskin ko‘tarilish yo‘q. Davom et.</p>'}${L.pot?`<p style="margin:8px 0 0">💡 Taxminiy tejash imkoniyati: <b>${num(L.pot)}</b> so‘m/oy</p>`:''}</div>${pmzChUi()}`}
// ---------- biznes markazi ----------
const pmzBz=()=>{finInit();S.fin.bz=S.fin.bz||[];return S.fin.bz};
function pmzBizNew(){const t=V('bzn').trim().slice(0,40),cap=sfn(V('bzc')),stop=sfn(V('bzs'));if(!t||!(cap>0)){toast('Nomi va kapitalni yozing');return}pmzBz().push({id:Date.now(),t,cap,stop:stop>0?stop:Math.round(cap*.3),st:V('bzd')||dk(),tx:[]});save()}
function pmzBizTx(id){const b=pmzBz().find(x=>x.id===id),k=V('bzk'+id)||'i',a=sfn(V('bza'+id));if(!b||!(a>0)){toast('Summani yozing');return}b.tx.push({id:Date.now(),d:dk(),k,a,n:V('bzt'+id).slice(0,40)});save()}
function pmzBizDel(id){if(!confirm('Biznes sinovi o‘chirilsinmi?'))return;S.fin.bz=pmzBz().filter(x=>x.id!==id);save()}
function pmzBizTxDel(id,tid){const b=pmzBz().find(x=>x.id===id);if(b){b.tx=b.tx.filter(x=>x.id!==tid);save()}}
function pmzBizChk(i){finInit();S.fin.bzc=S.fin.bzc||{};S.fin.bzc[i]=S.fin.bzc[i]?0:1;save()}
function pmzBizStat(b){let c=0,o=0,i=0;b.tx.forEach(x=>{if(x.k==='c')c+=x.a;else if(x.k==='o')o+=x.a;else i+=x.a});const spent=c+o,net=i-spent,loss=Math.max(0,-net),profit=i-o;return{c,o,i,spent,net,loss,us:b.stop>0?loss/b.stop:0,profit,margin:i>0?Math.round(profit/i*100):null,roi:c>0?Math.round((i-o-c)/c*100):null}}
function pmzReady(){const B=pmzBz(),sv=pmzSav(),me=pmzExp(),capT=B.reduce((a,b)=>a+b.cap,0);
  const it=[{t:'Xavfsizlik yostig‘i: jamg‘arma kamida 1 oylik xarajatga teng',ok:me>0&&sv>=me,h:me>0?`Jamg‘arma ${num(sv)} / oylik xarajat ${num(me)}`:'Xarajatlarni yozing'},
   {t:'Biznes kapitali jamg‘armaning 30% idan oshmaydi',ok:B.length?capT<=sv*.3:null,h:B.length?`Kapital ${num(capT)} / ruxsat ${num(Math.round(sv*.3))}`:'Sinov yaratilganda tekshiriladi'},
   {t:'Yo‘qotish chegarasi (stop-loss) kapitalning 30% idan oshmaydi',ok:B.length?B.every(b=>b.stop>0&&b.stop<=b.cap*.3):null,h:B.length?'Har sinov uchun':'Sinov yaratilganda tekshiriladi'},
   {t:'Sinov muddati belgilangan (30 kun)',ok:B.length?B.every(b=>!!b.st):null,h:B.length?'Boshlanish sanasi bor':'Sinov yaratilganda tekshiriladi'}];
  const pass=it.filter(x=>x.ok===true).length;return{it,pc:Math.round(pass/it.length*100)}}
const PMZBS=['Kamida 10 ta potentsial mijoz bilan gaplashdim','Eng kichik sinov variantini sotdim yoki ko‘rsatdim','Narxni 2 xil sinadim','Har bir xarajatni yozib bordim','30 kundan keyin davom yoki to‘xtash qarorini yozdim'];
function pmzBizUi(){
  if(W!=='p')return '<p class="mu">Biznes markazi shaxsiy hamyonda.</p><button class="btn" onclick="W=\'p\';render()">Shaxsiyga o‘tish</button>';
  const B=pmzBz(),R=pmzReady(),ck=(S.fin.bzc||{});
  const card=b=>{const s=pmzBizStat(b),col=s.us>=1?'var(--bad)':s.us>=.8?'#d9a441':'var(--ac)',days=b.st?Math.max(0,-dl(b.st)):0;
    return `<div class="goal pmzc"><div class="h"><b>💼 ${esc(b.t)}</b><button class="x" onclick="pmzBizDel(${b.id})">×</button></div>
     <p class="mu" style="margin:4px 0 8px;font-size:12px">${esc(dU(b.st))} dan · ${days} kun · rejalangan kapital ${num(b.cap)}</p>
     <div class="sum"><div><span class="mu">Kapital qo‘yildi</span><b>${num(s.c)}</b></div><div><span class="mu">Xarajat</span><b class="out-c">${num(s.o)}</b></div><div><span class="mu">Savdo</span><b class="in-c">${num(s.i)}</b></div><div><span class="mu">Foyda (savdo − xarajat)</span><b class="${s.profit>=0?'in-c':'out-c'}">${s.profit<0?'−':''}${num(Math.abs(s.profit))}</b></div></div>
     <div class="usr" style="margin:6px 0"><span class="usk" style="flex-basis:120px">Yo‘qotish chegarasi</span><span class="usb"><i style="width:${Math.min(100,s.us*100)}%;background:${col}"></i></span><span class="usv">${num(s.loss)} / ${num(b.stop)}</span></div>
     <p style="margin:6px 0 0">${s.net>=0?'✅ Kiritilgan pul qaytgan (+'+num(s.net)+').':'Hali qaytmagan: <b>'+num(s.loss)+'</b> so‘m.'} ${s.margin!==null?'Marja '+s.margin+'%.':''} ${s.roi!==null?'ROI '+s.roi+'%.':''}</p>
     ${s.us>=1?'<p style="margin:6px 0 0;color:var(--bad)"><b>⚠️ Yo‘qotish chegarasi oshdi. To‘xta va qaror qil: davom etish yoki yopish.</b></p>':s.us>=.8?'<p style="margin:6px 0 0;color:#b9800f"><b>Chegaraga yaqinlashding (80%+).</b></p>':''}
     <div class="in" style="margin-top:8px"><select id="bzk${b.id}" style="flex:0 0 110px"><option value="i">Savdo</option><option value="o">Xarajat</option><option value="c">Kapital</option></select><input id="bza${b.id}" type="text" inputmode="numeric" placeholder="Summa"><button class="btn" onclick="pmzBizTx(${b.id})">+</button></div><div class="in"><input id="bzt${b.id}" placeholder="Izoh (ixtiyoriy)"></div>
     ${b.tx.slice(-5).reverse().map(x=>`<div class="row"><span class="t">${x.k==='i'?'⬆️ Savdo':x.k==='o'?'⬇️ Xarajat':'🏦 Kapital'} ${num(x.a)}<br><span class="mu">${x.d.slice(8)}.${x.d.slice(5,7)}${x.n?' · '+esc(x.n):''}</span></span><button class="x" onclick="pmzBizTxDel(${b.id},${x.id})">×</button></div>`).join('')}</div>`};
  return `<h2>💼 Biznesga tayyorlik: ${R.pc}%</h2><div class="goal pmzc">${R.it.map(x=>`<div class="row" style="padding:8px 4px"><span style="font-size:20px">${x.ok===true?'✅':x.ok===false?'⬜':'⏳'}</span><span class="t">${esc(x.t)}<br><span class="mu" style="font-size:12px">${esc(x.h)}</span></span></div>`).join('')}<p class="mu" style="margin:8px 0 0;font-size:12px">Qoida: avval yostiq, keyin kichik sinov. Qarz olib biznes boshlama. Kapital va yo‘qotish chegarasini oldindan belgila.</p></div>
  <h2>Sinovlaring</h2>${B.length?B.map(card).join(''):'<p class="mu" style="margin:0 0 8px">Hali sinov yo‘q. G‘oyani katta pul tikmasdan, kichik kapital va aniq yo‘qotish chegarasi bilan sina.</p>'}
  <details class="sd" ${B.length?'':'open'}><summary>＋ Yangi biznes sinovi</summary><div class="in" style="margin-top:8px"><input id="bzn" placeholder="Nomi (masalan: Onlayn savdo)"></div><div class="in"><input id="bzc" type="text" inputmode="numeric" placeholder="Kapital, so‘m"><input id="bzs" type="text" inputmode="numeric" placeholder="Yo‘qotish chegarasi (bo‘sh=30%)"></div><div class="in"><input id="bzd" type="date" value="${dk()}"><span class="mu" style="align-self:center;white-space:nowrap">boshlanish</span></div><button class="btn" style="width:100%" onclick="pmzBizNew()">Sinovni boshlash</button></details>
  <h2>🧪 G‘oyani sinash: 5 qadam</h2><div class="goal">${PMZBS.map((t,i)=>`<button class="row ${ck[i]?'done':''}" onclick="pmzBizChk(${i})"><span class="ck">${ck[i]?'✓':''}</span><span class="t">${esc(t)}</span></button>`).join('')}</div>`}
// ---------- Bosh ekranga yig'ish ----------
const pmzOn=()=>uiG('trk_pmz')!=='0';
function pmzJl(){return `<p class="mu" style="margin:12px 0 4px;font-size:12px"><b>💰 Pul markazi</b> <span style="font-size:11px">(kunlik xulosa, sog‘liq balli, yutuqlar, doim ko‘rinadigan minora)</span></p>${jlSeg('trk_pmz','1',[['1','Ko‘rinsin'],['0','Ko‘rinmasin (avvalgidek)']])}`}
function pmzBosh(){
  if(W!=='p')return '';
  if(!pmzOn())return d3CoinsCard();const H=pmzHealth(),M=pmzMedals(H);pmzMilCheck(M);
  const ch=pmzChInfo(),bz=pmzReady();
  return `${pmzBanner()}${pmzBrief(H)}${pmzTower()}${pmzHealthUi(H)}${ch&&!ch.done?`<button class="row" style="border-left-color:var(--go)" onclick="PV='h';render()"><span style="font-size:22px">🎯</span><span class="t"><b>Tejash chellenji: ${ch.ns} / ${ch.c.need} sarfsiz kun</b><br><span class="mu">Hisobot’da batafsil</span></span></button>`:''}${pmzMedalsUi(M)}
  <button class="row" style="border-left-color:var(--go)" onclick="PV='x';render()"><span style="font-size:22px">💼</span><span class="t"><b>Biznes markazi: tayyorlik ${bz.pc}%</b><br><span class="mu">Kapital, yo‘qotish chegarasi, sinov hisobi</span></span></button>`}
