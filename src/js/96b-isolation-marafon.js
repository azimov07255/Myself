// ---- ISOLATION MARAFONI: 2 haftalik intensiv (Prava imtihoni + Qur'on yodlash intizomi + pul qo'riqchi + motivatsiya). Mavjud ma'lumotlarga tayanadi, yangisini kam saqlaydi. Prefiks: mrf ----
const mrfS=()=>{S.iso=S.iso||{};S.iso.mr=S.iso.mr||{};return S.iso.mr};
const mrfDiff=(a,b)=>Math.round((new Date(b+'T12:00')-new Date(a+'T12:00'))/864e5);
const mrfAt=(s,i)=>new Date(new Date(s+'T12:00').getTime()+i*864e5).toLocaleDateString('sv');
let MRFO=0;
const MRFQ={
 d:[['Albatta, qiyinchilik bilan birga yengillik bor.','Sharh surasi, 94:6 (ma‘nosi)'],['Kim Allohga tavakkul qilsa, U zot unga kifoya qiladi.','Taloq surasi, 65:3 (ma‘nosi)'],['Rabbim, ilmimni ziyoda qil.','Toha surasi, 20:114 (ma‘nosi)'],['Sabr qiluvchilarga ajrlari hisobsiz to‘liq beriladi.','Zumar surasi, 39:10 (ma‘nosi)'],['Albatta, Alloh sabr qiluvchilar bilandir.','Baqara surasi, 2:153 (ma‘nosi)'],['Alloh hech bir jonga qodir bo‘lganidan ortiq yuk yuklamaydi.','Baqara surasi, 2:286 (ma‘nosi)'],['Ogoh bo‘l, qalblar faqat Allohni zikr qilish bilan xotirjam bo‘ladi.','Ra‘d surasi, 13:28 (ma‘nosi)'],['Biz Qur‘onni eslatma uchun oson qildik, endi o‘git oluvchi bormi?','Qamar surasi, 54:17 (ma‘nosi)'],['Amallar niyatlarga bog‘liqdir.','Hadis, Buxoriy va Muslim (ma‘nosi)'],['Allohga eng suyukli amal, oz bo‘lsa ham davomli bo‘lganidir.','Hadis, Buxoriy va Muslim (ma‘nosi)'],['Sizlarning eng yaxshilaringiz Qur‘onni o‘rganib, o‘rgatganlaringizdir.','Hadis, Buxoriy (ma‘nosi)'],['Kim ilm izlab yo‘lga chiqsa, Alloh unga Jannat yo‘lini yengillashtiradi.','Hadis, Muslim (ma‘nosi)']],
 w:['Intizom, motivatsiya tugagan kunda ham ishlayotgan narsadir.','Bugungi kichik qadam ertangi katta natijaning poydevoridir.','Mukammallik emas, davomiylik natija beradi.','Kechagi o‘zingdan ozgina yaxshi bo‘lish yetarli.','Qiyin kunlarda qilingan ish eng qadrli bo‘ladi.','Ikki hafta o‘tadi, qilgan ishing qoladi.','Boshlash qiyin, davom etish esa odatga aylanadi.','Bugun qilolmagan 1 narsangni ertaga emas, hozir 5 daqiqa qil.','Katta maqsad kichik kunlik g‘alabalardan yig‘iladi.','Kimdir tinch yotganda, sen o‘z yo‘lingda yurayapsan.']};
const MRFB=[['05:00','Bomdod, Qur‘on sabaq (yangi bet)','🧠'],['09:00','Prava: bugungi mavzu (nazariya)','🚗'],['12:30','Peshin namozi va dam','🕌'],['14:00','Prava: testlar','📝'],['16:30','Yurish yoki yengil sport','🚶'],['17:30','Asr, Qur‘on sabqi va manzil','🔁'],['19:30','Prava: xatolar ustida ishlash','🔎'],['21:00','Kechki muhosaba','🌙'],['22:30','Uxlash','😴']];
function mrfInfo(){const m=mrfS();if(!m.on||!m.start)return null;const n=m.n||14,td=dk(),d=mrfDiff(m.start,td)+1;return{m,n,td,d,dc:Math.min(Math.max(d,1),n),before:d<1,over:d>n,left:Math.max(0,n-Math.max(d,1))}}
const mrfPages=k=>((S.q&&S.q.lg)||[]).filter(x=>x.d===k&&x.t==='n').reduce((a,x)=>a+Math.max(0,(x.b-x.a)),0);
const mrfTests=k=>((S.pr&&S.pr.tests)||[]).filter(x=>x.d===k);
function mrfTopic(d,n){const T=PTOP.slice(0,PTOP.length-1),nt=Math.max(1,Math.round(n*.65));if(d>=n)return{t:'Imtihon oldi: yengil takror, hujjatlar va dam',k:'dam'};if(d>nt)return{t:'Zaif mavzular va to‘liq test',k:'zaif'};return{t:T[(d-1)%T.length],k:'mavzu'}}
function mrfDay(k){
  const m=mrfS(),man=(m.man||{})[k]||{},pt=m.pt||2,ppd=(S.q&&S.q.ppd)||0,nm=PR.slice(0,5).filter(([p])=>((S.nm.d[k]||{})[p])===1).length,pg=mrfPages(k),ts=mrfTests(k).length,ig=!!((S.rules[k]||{}).ig);
  const it=[{id:'nm',e:'🕌',t:'5 vaqt namoz',v:nm+' / 5',ok:nm>=5||!!man.nm,au:nm>=5},
   {id:'hf',e:'🧠',t:ppd>0?'Qur‘on: '+ppd+' bet yodlash':'Qur‘on yodlash',v:ppd>0?(Math.round(pg*10)/10)+' / '+ppd+' bet':(man.hf?'belgilandi':'belgila'),ok:(ppd>0&&pg>=ppd)||!!man.hf,au:ppd>0&&pg>=ppd},
   {id:'pr',e:'🚗',t:'Prava: '+pt+' ta test',v:ts+' / '+pt,ok:ts>=pt||!!man.pr,au:ts>=pt},
   {id:'ph',e:'📵',t:'Telefonsiz, tinch kun',v:ig?'Instagramsiz':(man.ph?'belgilandi':'belgila'),ok:ig||!!man.ph,au:ig},
   {id:'rf',e:'🌙',t:'Kechki muhosaba',v:(m.ref||{})[k]?'yozildi':'yoz',ok:!!(m.ref||{})[k],au:true}];
  const dn=it.filter(x=>x.ok).length;return{it,dn,tot:it.length,full:dn===it.length,pc:Math.round(dn/it.length*100)}}
function mrfTog(id){const m=mrfS(),k=dk();m.man=m.man||{};const o=m.man[k]=m.man[k]||{};const D=mrfDay(k).it.find(x=>x.id===id);if(!D||D.au&&D.ok&&!o[id]){toast('Bu avtomatik belgilangan');return}o[id]=o[id]?0:1;save()}
function mrfStreak(I){let st=0;for(let i=Math.min(I.d,I.n)-1;i>=0;i--){const k=mrfAt(I.m.start,i);if(k>I.td)continue;if(mrfDay(k).full)st++;else if(k===I.td)continue;else break}return st}
function mrfStart(){const m=mrfS(),sd=V('mrs')||dk(),n=Math.min(60,Math.max(3,+V('mrn')||14)),pt=Math.min(10,Math.max(1,+V('mrt')||2)),ex=V('mre');
  Object.assign(m,{on:1,start:sd,n,pt,why:(V('mrw')||'').slice(0,200),man:m.man||{},ref:m.ref||{}});if(ex){S.pr=S.pr||{};S.pr.exam=ex}save()}
function mrfStop(){if(!confirm('Marafon to‘xtatilsinmi? Natijalaring saqlanadi.'))return;mrfS().on=0;save()}
function mrfRef(){const m=mrfS(),k=dk(),g=V('mrg'),i=V('mri'),t=V('mrx');if(!g&&!i&&!t){toast('Kamida bitta qatorni yoz');return}m.ref=m.ref||{};m.ref[k]={g:g.slice(0,200),i:i.slice(0,200),t:t.slice(0,200),m:+(window.MRFM||0)||0};save()}
function mrfMood(v){window.MRFM=v;document.querySelectorAll('#app .mrfmo button').forEach(b=>b.classList.toggle('on',+b.dataset.v===v))}
function mrfOther(){MRFO++;render()}
function mrfMoney(I){const w=W;W='p';let D=null;try{D=pDaily()}catch(e){}W=w;let ns=0,kr=0;
  for(let i=0;i<I.dc;i++){const k=mrfAt(I.m.start,i);if(k>=I.td)break;if(!S.money.some(x=>x.w==='p'&&x.k==='out'&&x.d===k))ns++}
  S.money.forEach(x=>{if(x.w==='p'&&x.k==='out'&&x.t==='k'&&x.d>=I.m.start&&x.d<=I.td)kr+=x.a});return{D,ns,kr}}
function mrfWins(I){const k=I.td,w=[],pg=mrfPages(k),T=mrfTests(k),m=mrfMoney(I);
  if(pg>0)w.push('📖 Bugun '+(Math.round(pg*10)/10)+' bet yodlading');T.forEach(x=>w.push('🚗 Prava testi: '+x.c+' / '+x.t+' ('+Math.round(x.c/x.t*100)+'%)'));
  if(mrfDay(k).it[0].ok)w.push('🕌 Bugun hamma namozlar o‘z vaqtida');if((S.rules[k]||{}).ig)w.push('📵 Instagramsiz kun');
  const full=[...Array(Math.max(0,Math.min(I.d,I.n)))].filter((_,i)=>mrfDay(mrfAt(I.m.start,i)).full).length;if(full)w.push('🏆 To‘liq bajarilgan kunlar: '+full);
  const st=mrfStreak(I);if(st>=2)w.push('🔥 '+st+' kun ketma-ket to‘liq');if(m.ns)w.push('💰 Sarfsiz kunlar: '+m.ns);
  const yw=((S.iso&&S.iso.log)||[]).filter(x=>x.w&&x.d>=I.m.start).length;if(yw)w.push('💪 Chalg‘ishni yengding: '+yw+' marta');return w}
function mrfPravaUi(I){
  const p=S.pr||{},ts=(p.tests||[]),last5=ts.slice(-5),avg=last5.length?Math.round(last5.reduce((a,x)=>a+x.c/x.t,0)/last5.length*100):0,pm=p.pm||18,top=mrfTopic(I.dc,I.n),pt=I.m.pt||2,today=mrfTests(I.td).length,
   weak=Object.entries(p.er||{}).sort((a,b)=>b[1]-a[1]).slice(0,3),ex=p.exam,ed=ex?dl(ex):null;
  return `<h2>🚗 Prava imtihoniga tayyorgarlik</h2><div class="goal mrfc"><p class="mu" style="margin:0 0 4px;font-size:13px">Bugungi mavzu (${I.dc}-kun)</p><b style="font:700 20px Fraunces,serif">${esc(top.t)}</b>
   <div class="usr" style="margin-top:10px"><span class="usk" style="flex-basis:110px">Bugungi testlar</span><span class="usb"><i style="width:${Math.min(100,today/pt*100)}%"></i></span><span class="usv">${today} / ${pt}</span></div>
   <p style="margin:8px 0 0">${ex?(ed>=0?'Imtihongacha <b>'+ed+' kun</b> ('+esc(dU(ex))+').':'Imtihon sanasi o‘tib ketdi.'):'Imtihon sanasi qo‘yilmagan: Prava bo‘limida belgila.'}</p>
   <p class="mu" style="margin:6px 0 0;font-size:13px">${last5.length?'Oxirgi '+last5.length+' test o‘rtachasi: <b>'+avg+'%</b>. O‘tish chegarasi: '+pm+' / 20 (90%).':'Hali test natijasi yo‘q. Test ilovasidan yechib, natijani Prava bo‘limiga yoz.'}</p>
   ${weak.length?'<p style="margin:8px 0 0"><b>Zaif mavzular:</b> '+weak.map(x=>esc(x[0])+' ('+x[1]+')').join(', ')+'</p>':''}
   <p class="mu" style="margin:8px 0 0;font-size:12px">Savollarni o‘zing ishlatadigan test ilovasidan yech: bu yerda natija va rejani kuzatamiz.</p>
   <div class="in" style="margin-top:8px"><button class="btn" style="flex:1" onclick="tab='e';EV='p';render()">Prava bo‘limini ochish</button></div></div>`}
function mrfHifzUi(I){
  const q=S.q||{},ppd=q.ppd||0,tg=ppd*I.n;let tot=0;for(let i=0;i<Math.min(I.d,I.n);i++)tot+=mrfPages(mrfAt(I.m.start,i));tot=Math.round(tot*10)/10;const pc=tg?Math.min(100,Math.round(tot/tg*100)):0,td=mrfPages(I.td);
  return `<h2>🧠 Qur‘on yodlash intizomi</h2><div class="goal mrfc">${ppd>0?`<div class="usr"><span class="usk" style="flex-basis:110px">Bugun</span><span class="usb"><i style="width:${Math.min(100,td/ppd*100)}%"></i></span><span class="usv">${Math.round(td*10)/10} / ${ppd} bet</span></div>
   <div class="usr" style="margin-top:8px"><span class="usk" style="flex-basis:110px">Marafon</span><span class="usb"><i style="width:${pc}%"></i></span><span class="usv">${tot} / ${tg} bet</span></div>
   <p class="mu" style="margin:8px 0 0;font-size:13px">${I.n} kunda ${tg} bet maqsad. Yangi bet + sabqi + manzil tartibi Qur‘on bo‘limida.</p>`:`<p style="margin:0 0 8px">Kunlik yodlash rejasi belgilanmagan. Marafon uchun real son tanla (masalan 1-3 bet).</p>`}
   <div class="in"><button class="btn" style="flex:1" onclick="tab='q';render()">Yodlashni ochish</button></div></div>`}
function mrfUi(){
  const I=mrfInfo();
  if(!I)return `<section class="hero"><p class="lab">Isolation marafoni</p><h1 style="font-size:30px">2 haftalik intensiv</h1><p class="mu">Telefonni chetga qo‘yib, bitta maqsadga: Prava imtihoni, Qur‘on yodlash intizomi, pulni yo‘qotmaslik. Har kun nima qolganini va nima qilganingni ko‘rasan.</p></section>
   <div class="goal"><b>Marafonni boshlash</b><div class="in" style="margin-top:8px"><input type="date" id="mrs" value="${dk()}"><span class="mu" style="align-self:center">boshlanish</span></div>
   <div class="in"><input type="number" id="mrn" value="14" min="3" max="60"><span class="mu" style="align-self:center;white-space:nowrap">kun</span><input type="number" id="mrt" value="2" min="1" max="10"><span class="mu" style="align-self:center;white-space:nowrap">test/kun</span></div>
   <div class="in"><input type="date" id="mre" value="${(S.pr&&S.pr.exam)||''}"><span class="mu" style="align-self:center;white-space:nowrap">Prava imtihoni</span></div>
   <div class="in"><input id="mrw" placeholder="Nega boshlayapman? (o‘z so‘zing bilan)"></div><button class="btn" style="width:100%" onclick="mrfStart()">Marafonni boshlash</button></div>`;
  const m=I.m,k=I.td,D=mrfDay(k),st=mrfStreak(I),pct=Math.round(I.dc/I.n*100),R=2*Math.PI*44,ref=(m.ref||{})[k]||{};
  const dots=[...Array(I.n)].map((_,i)=>{const dk_=mrfAt(m.start,i),fu=dk_>I.td,t=dk_===I.td,dy=fu?null:mrfDay(dk_),cl=fu?'':dy.full?'f':dy.pc>=60?'p':t?'t':'m';return `<span class="mrfdot ${cl} ${t?'now':''}" title="${i+1}-kun">${dy&&dy.full?'✓':i+1}</span>`}).join('');
  const dq=MRFQ.d[(I.dc+MRFO)%MRFQ.d.length],wq=MRFQ.w[(I.dc*3+MRFO)%MRFQ.w.length],nowH=new Date().getHours()*60+new Date().getMinutes(),bi=MRFB.map(x=>+x[0].slice(0,2)*60+(+x[0].slice(3))).filter(t=>t<=nowH).length-1;
  const MN=mrfMoney(I),Dd=MN.D,wins=mrfWins(I);
  const head=I.before?`<h1 style="font-size:40px">${-I.d+1} kundan keyin</h1><p class="mu">Marafon ${esc(dU(m.start))} da boshlanadi.</p>`:I.over?`<h1 style="font-size:36px">Marafon tugadi 🎉</h1><p class="mu">${I.n} kunni yakunlading. Barakalla!</p>`:`<h1 style="font-size:46px">${I.dc}<span style="font-size:22px;opacity:.7"> / ${I.n} kun</span></h1><p class="mu" style="font-size:15px">${I.left>0?'<b>'+I.left+' kun qoldi</b>':'<b>Bugun oxirgi kun!</b>'} · bugungi natija ${D.pc}%${st>1?' · 🔥 '+st+' kun ketma-ket':''}</p>`;
  return `<section class="hero mrfh"><p class="lab">Isolation marafoni</p><div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><div>${head}</div>
   <svg width="104" height="104" viewBox="0 0 104 104" aria-label="Marafon: ${pct}%"><circle cx="52" cy="52" r="44" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="9"/><circle cx="52" cy="52" r="44" fill="none" stroke="var(--go)" stroke-width="9" stroke-linecap="round" stroke-dasharray="${R*pct/100} ${R}" transform="rotate(-90 52 52)"/><text x="52" y="58" text-anchor="middle" font-size="20" font-weight="800" fill="currentColor">${pct}%</text></svg></div>
   <div class="mrfdots">${dots}</div>${m.why?`<p style="margin:12px 0 0;font-style:italic">“${esc(m.why)}”</p><p class="mu" style="margin:2px 0 0;font-size:12px">Sening niyating</p>`:''}</section>
  <h2>Bugungi ${D.tot} ta asosiy ish <span class="mu" style="font-size:14px;font-family:Figtree,system-ui">${D.dn} / ${D.tot}</span></h2><div class="bar" style="margin-bottom:8px"><i style="width:${D.pc}%"></i></div>
  ${D.it.map(x=>`<button class="row ${x.ok?'done':''}" onclick="mrfTog('${x.id}')"><span class="ck">${x.ok?'✓':''}</span><span class="t">${x.e} ${esc(x.t)}<br><span class="mu">${esc(x.v)}</span></span></button>`).join('')}
  ${D.full?'<div class="goal mrfc"><b>🏆 Bugun to‘liq bajarding! Barakalla.</b></div>':''}
  <h2>💡 Bugungi ruh</h2><div class="goal mrfc"><p style="margin:0 0 4px;font-size:12px" class="mu">🌙 Diniy</p><p style="margin:0;font:600 17px Fraunces,serif">“${esc(dq[0])}”</p><p class="mu" style="margin:2px 0 10px;font-size:12px">${esc(dq[1])}</p><p style="margin:0 0 4px;font-size:12px" class="mu">☀️ Hayotiy</p><p style="margin:0;font:600 17px Fraunces,serif">“${esc(wq)}”</p>
   <p class="mu" style="margin:10px 0 6px;font-size:11px">Oyat va hadislar ma‘nosi; aniq matn va izoh uchun ishonchli manbaga qara.</p><button class="btn s" onclick="mrfOther()">Boshqasini ko‘rsat</button></div>
  <h2>🗓 Bugungi tartib</h2><div class="goal">${MRFB.map((x,i)=>`<div class="row" style="${i===bi?'border-left:4px solid var(--go);font-weight:700':'opacity:.8'}"><span style="font-size:20px">${x[2]}</span><span class="t">${x[0]} · ${esc(x[1])}</span>${i===bi?'<span class="chip">hozir</span>':''}</div>`).join('')}</div>
  ${mrfPravaUi(I)}${mrfHifzUi(I)}
  <h2>💰 Pulni asrash</h2><div class="goal mrfc">${Dd&&Dd.lim?`<div class="usr"><span class="usk" style="flex-basis:110px">Bugun</span><span class="usb"><i style="width:${Math.min(100,Dd.sp/Dd.lim*100)}%;${Dd.sp>Dd.lim?'background:var(--bad)':''}"></i></span><span class="usv">${num(Dd.sp)} / ${num(Dd.lim)}</span></div><p style="margin:8px 0 0">${Dd.left>=0?'Bugun yana <b>'+num(Dd.left)+'</b> so‘m sarflasa bo‘ladi.':'<b style="color:var(--bad)">Chegaradan '+num(-Dd.left)+' so‘m oshdi.</b> To‘xta va o‘yla: bu kerakmi?'}</p>`:'<p style="margin:0">Kunlik chegara yo‘q. Pul → Reja’da byudjet yoki jamg‘arma maqsadi qo‘y.</p>'}
   <p class="mu" style="margin:8px 0 0;font-size:13px">Sarfsiz kunlar: <b>${MN.ns}</b>${MN.kr?' · “keraksiz” deb belgilangan: '+num(MN.kr)+' so‘m':''}. Izolyatsiyada pul kerak emas: xohish chiqsa, Pul → Bosh’dagi 24 soatlik xohish ro‘yxatiga yoz.</p><div class="in" style="margin-top:8px"><button class="btn s" style="flex:1" onclick="tab='p';PV='b';render()">Pulni ochish</button></div></div>
  <h2>🏆 Kichik g‘alabalaring</h2><div class="goal mrfc">${wins.length?wins.map(x=>`<p style="margin:0 0 6px">${esc(x)}</p>`).join(''):'<p class="mu" style="margin:0">Birinchi g‘alaba: bitta test yoki bitta bet. Boshla!</p>'}</div>
  <h2>🌙 Kechki muhosaba</h2><div class="goal mrfc">${ref.g||ref.i||ref.t?`<p style="margin:0 0 6px"><b>Yaxshi ketdi:</b> ${esc(ref.g||'—')}</p><p style="margin:0 0 6px"><b>Yaxshilayman:</b> ${esc(ref.i||'—')}</p><p style="margin:0"><b>Ertangi bitta ish:</b> ${esc(ref.t||'—')}</p>`:`<div class="in"><input id="mrg" placeholder="Bugun nima yaxshi ketdi?"></div><div class="in"><input id="mri" placeholder="Nimani yaxshilayman?"></div><div class="in"><input id="mrx" placeholder="Ertangi eng muhim bitta ish"></div><button class="btn" style="width:100%" onclick="mrfRef()">Saqlash</button>`}</div>
  <div class="in" style="margin-top:14px"><button class="btn s" onclick="mrfStop()">Marafonni to‘xtatish</button></div>`}
function mrfMini(){const I=mrfInfo();if(!I||I.over||I.before)return '';const D=mrfDay(I.td);return `<button class="row" style="margin-top:10px;border-left-color:var(--go)" onclick="tab='o';OT='i';render()"><span style="font-size:22px">🧘</span><span class="t"><b>Isolation: ${I.dc} / ${I.n} kun</b><br><span class="mu">${I.left>0?I.left+' kun qoldi':'oxirgi kun'} · bugun ${D.dn} / ${D.tot} bajarildi</span></span></button>`}
