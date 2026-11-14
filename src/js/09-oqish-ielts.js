// ---- O‘qish: IELTS, Univer, Prava ----
const dl=d=>Math.ceil((new Date(d+'T12:00')-new Date(dk()+'T12:00'))/864e5);
const dlTxt=n=>n<0?'muddat o‘tdi':n===0?'bugun':n+' kun qoldi';
const addD=n=>new Date(Date.now()+n*864e5).toLocaleDateString('sv'),IV=[0,1,3,7,14,30];
const V=id=>{const e=$('#'+id);return e?e.value.trim():''};
function dueCard(){
  const u=S.un,it=[...u.tasks.filter(t=>!t.x&&t.due&&dl(t.due)<=3).map(t=>({t:t.t,n:dl(t.due),k:'Topshiriq'})),...u.exams.filter(e=>dl(e.d)>=0&&dl(e.d)<=7).map(e=>({t:e.s,n:dl(e.d),k:'Imtihon'}))].sort((a,b)=>a.n-b.n);
  (S.debts||[]).filter(d=>d.st!=='closed'&&d.due&&dl(d.due)<=3).forEach(d=>it.push({t:(d.k==='borrow'?d.p+' ga qaytarish ':d.p+' dan olish ')+num(dRem(d)),n:dl(d.due),k:'Qarz'}));const gp=S.gym.pass;if(gp&&dk()>=gp.s&&dk()<=gp.e){const st=psStat();if(gp.v[dk()]==='p')it.push({t:'Zalga borish ('+st.done+'/'+gp.t+')',n:0,k:'Zal'});if(st.rem>0&&dl(gp.e)<=3)it.push({t:'Abonement tugayapti, '+st.rem+' ta kirish qoldi',n:dl(gp.e),k:'Zal'})}it.sort((a,b)=>a.n-b.n);
  if(!it.length)return '';
  return `<div class="goal" style="margin-top:12px;border-left:4px solid var(--bad)"><b style="font:700 18px Fraunces,serif">Yaqin muddatlar</b>${it.map(x=>`<p style="margin:6px 0 0">${x.k}: <b>${esc(x.t)}</b> <span class="mu">${dlTxt(x.n)}</span></p>`).join('')}</div>`}
function oqish(){
  const seg=[['i','🎓 IELTS'],['u','🏫 Univer'],['p','🚗 Prava'],['k','📚 Kitob']].map(x=>`<button class="${EV===x[0]?'on':''}" onclick="EV='${x[0]}';render()">${x[1]}</button>`).join('');
  return `<div class="seg">${seg}</div>${EV==='i'?ielts():EV==='u'?univer():EV==='k'?kitob():prava()}`}
const wDue=()=>{const room=Math.max(0,(S.ie.nl||10)-ieNd());let nw=0;return S.ie.words.filter(w=>w.due<=dk()).sort((a,b)=>(a.t||0)-(b.t||0)).filter(w=>w.t||(nw++<room))};
function iAdd(){const w=V('iw'),m=V('im');if(!w)return;S.ie.words.push({id:Date.now(),w,m,box:0,due:dk(),t:0});save()}
function iBulk(){V('ib').split('\n').forEach((l,i)=>{const p=l.split(/[-–:=]/),w=(p[0]||'').trim();if(w)S.ie.words.push({id:Date.now()+i,w,m:p.slice(1).join('-').trim(),box:0,due:dk(),t:0})});save()}
function iAns(ok){const w=wDue()[0];if(!w)return;if(ok){w.box=Math.min(5,w.box+1);w.due=addD(IV[w.box])}else{w.box=0;w.due=dk();w.fl=(w.fl||0)+1}if(!w.t)S.ie.nd={d:dk(),n:ieNd()+1};w.t=Date.now();IR=0;ISC=null;save()}
function iDel(id){S.ie.words=S.ie.words.filter(w=>w.id!==id);save()}
function iMock(){const b=parseFloat(V('mb'));if(!(b>=0&&b<=9))return;S.ie.mock.push({id:Date.now(),d:dk(),t:V('mt')||'Umumiy',b});save()}
function iWr(){const t=V('wp');if(!t)return;S.ie.wr.push({id:Date.now(),d:dk(),k:V('wk'),t,n:+V('wn')||0});save()}
const lst=(a,k)=>{S[a.split('.')[0]][a.split('.')[1]]=S[a.split('.')[0]][a.split('.')[1]].filter(x=>x.id!==k);save()};

// ================= IELTS =================
const LB=[[39,9],[37,8.5],[35,8],[32,7.5],[30,7],[26,6.5],[23,6],[18,5.5],[16,5],[13,4.5],[10,4],[8,3.5],[6,3],[4,2.5]];
const RB=[[39,9],[37,8.5],[35,8],[33,7.5],[30,7],[27,6.5],[23,6],[19,5.5],[15,5],[13,4.5],[10,4],[8,3.5],[6,3],[4,2.5]];
const rawBand=(k,r)=>{for(const[m,b]of(k==='L'?LB:RB))if(r>=m)return b;return 2};
const ieRound=x=>Math.floor(x*2+0.5)/2;
const SK={L:'Listening',R:'Reading',W:'Writing',S:'Speaking'};
function ieSeries(){const o={L:[],R:[],W:[],S:[]};
  S.ie.tests.forEach(t=>{Object.keys(SK).forEach(k=>{if(t.b&&t.b[k]!=null)o[k].push({d:t.d,b:t.b[k]})})});
  S.ie.mock.forEach(m=>{const k={Listening:'L',Reading:'R',Writing:'W',Speaking:'S'}[m.t];if(k)o[k].push({d:m.d,b:m.b})});
  Object.values(o).forEach(a=>a.sort((x,y)=>x.d.localeCompare(y.d)));return o}
const ieCur=a=>a.length?r1(a.slice(-3).reduce((s,x)=>s+x.b,0)/Math.min(3,a.length)):null;
function ieStat(){const s=ieSeries(),c={};let n=0,sum=0;Object.keys(SK).forEach(k=>{c[k]=ieCur(s[k]);if(c[k]!==null){sum+=c[k];n++}});return{s,c,ov:n?ieRound(sum/n):null}}
const IPL=[['v','Lug‘at takrori'],['L','Listening mashqi'],['R','Reading mashqi'],['W','Writing yozish'],['S','Speaking mashqi'],['a','Maqola yoki podkast']];
const ieDp=()=>{S.ie.dp=S.ie.dp||{};return S.ie.dp[dk()]=S.ie.dp[dk()]||{}};
function ieTick(k){const d=ieDp();d[k]=d[k]?0:1;save()}
function ieStreak(){let n=0;for(let i=0;i<120;i++){const d=(S.ie.dp||{})[dAgo(i)]||{},c=Object.values(d).filter(Boolean).length;if(c>=3)n++;else if(i>0)break}return n}
function qsave(){rwReset();S.ts=Date.now();try{localStorage.setItem(KEY(),JSON.stringify(S))}catch(e){}clearTimeout(tm);tm=setTimeout(push,700)}

const IMGS=[['m','Natijalar'],['w','Writing'],['s','Speaking'],['x','AI mashq'],['k','Imtihon']];
function ielts(){const g=IMG.includes(IVW),top=[['b','🏠 Bosh'],['l','🔤 Lug‘at'],['y','🎓 Kurs'],['a','📰 Materiallar'],['m','🎯 Mashq']].map(x=>`<button class="${(x[0]==='m'?g:IVW===x[0])?'on':''}" onclick="IVW='${x[0]==='m'&&g?IVW:x[0]}';render()">${x[1]}</button>`).join(''),sub=g?`<div class="seg ssub" style="margin:8px 0 0">${IMGS.map(x=>`<button class="${IVW===x[0]?'on':''}" onclick="IVW='${x[0]}';render()">${x[1]}</button>`).join('')}</div>`:'';
  return `<div class="seg" style="margin-top:0">${top}</div>${sub}${IVW==='b'?ieBosh():IVW==='l'?(GM?gmView():TG?tgView():ieLug()):IVW==='y'?ksView():IVW==='a'?ieMat():IVW==='m'?ieMashq():IVW==='w'?ieWrite():IVW==='x'?ieAiTab():IVW==='k'?ieImt():ieSpeak()}`}
function ieBosh(){const st=ieStat(),T=S.ie.target||7,dp=ieDp(),due=wDue().length;
  const skl=Object.keys(SK).map(k=>{const c=st.c[k];return `${ksMini()}<div class="skb"><div class="h"><span>${SK[k]}</span><span class="mu">${c===null?'ma’lumot yo‘q':c+' / maqsad '+T}</span></div><div class="bar" style="margin-top:6px"><i style="width:${c===null?0:c/9*100}%"></i><b style="left:${T/9*100}%"></b></div></div>`}).join('');
  const plan=IPL.map(([k,t])=>`<button class="row ${dp[k]?'done':''}" onclick="ieTick('${k}')"><span class="ck">${dp[k]?'✓':''}</span><span class="t">${t}${k==='v'?` <span class="mu">(${due} ta navbatda)</span>`:''}</span></button>`).join('');
  const mocks=S.ie.tests.filter(t=>t.k==='M').map(t=>({d:t.d,o:ieRound(Object.values(t.b).reduce((a,x)=>a+x,0)/Object.keys(t.b).length)})),n=mocks.length,
    line=n>1?`<svg viewBox="0 0 300 70" width="100%" height="70"><polyline fill="none" stroke="var(--ac)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="${mocks.map((m,i)=>`${i*300/(n-1)},${66-(m.o-4)/5*60}`).join(' ')}"/></svg>`:'';
  return `${dualPanel('i')}<h2>Bugungi reja</h2>${plan}<h2>Ko‘nikmalar</h2>${skl}${line?`<h2>Mock natijalari o‘sishi</h2>${line}`:''}${ieErrBrief()}
  <details class="sd" style="margin-top:14px"><summary>⚙️ Sozlamalar</summary><div class="in" style="margin-top:8px"><span style="align-self:center;min-width:110px">Maqsad ball</span><input type="number" step="0.5" min="4" max="9" value="${T}" onchange="S.ie.target=+this.value||7;save()"></div><div class="in"><span style="align-self:center;min-width:110px">Imtihon sanasi</span><input type="date" value="${S.ie.ex||''}" onchange="S.ie.ex=this.value;save()"></div><div class="in"><span style="align-self:center;min-width:110px">Talaffuz</span>${ieAccChip()}<button class="chip slwchip" onclick="ieSlowToggle()" aria-pressed="${S.ie.slow?'true':'false'}">🐢 ${S.ie.slow?'sekin':'oddiy'}</button></div><div class="in"><span style="align-self:center;min-width:110px">Lug‘at maqsadi</span><input type="number" min="100" step="100" value="${S.ie.vg||1500}" onchange="S.ie.vg=Math.max(100,+this.value||1500);save()"></div></details>`}
function ieQuiz(){const W=S.ie.words.filter(w=>w.m&&w.k!=='g');if(W.length<4){IQ={err:1};render();return}
  const w=W[Math.floor(Math.random()*W.length)],o=W.filter(x=>x.id!==w.id).sort(()=>Math.random()-.5).slice(0,3),opts=[...o,w].sort(()=>Math.random()-.5);
  IQ={w,opts,ans:null,sc:(IQ&&IQ.sc)||0,n:(IQ&&IQ.n)||0};render()}
function ieAns(i){if(IQ.ans!==null)return;IQ.ans=i;IQ.n++;if(IQ.opts[i].id===IQ.w.id)IQ.sc++;render()}
function ieLug(){
  const ie=S.ie,due=wDue(),w=due[0],ln=ie.words.filter(x=>x.box>=4).length,nw=ie.words.filter(x=>x.box===0).length;
  const study=ie.words.length?(w?`<section class="hero"><p class="lab">Takror, ${due.length} ta qoldi</p>${ieCard(w)}</section>`:'<section class="hero"><p class="lab">Lug‘at</p><h1 style="font-size:26px">Bugungi takror tugadi</h1><p class="mu">Keyingi so‘zlar o‘z vaqtida chiqadi.</p></section>'):'<p class="mu">Birinchi so‘zlaringni qo‘sh, ilova ularni o‘z vaqtida takrorlatadi.</p>';
  let quiz='';
  if(IQ&&IQ.err)quiz='<p class="mu">Test uchun ma‘nosi yozilgan kamida 4 ta so‘z kerak.</p>';
  else if(IQ&&IQ.w){const q=IQ;quiz=`<div class="goal"><div class="h"><b>Test</b><span class="mu">${q.sc} / ${q.n}</span></div><p style="font:700 24px Fraunces,serif;margin:8px 0">${esc(q.w.w)}</p>${q.opts.map((o,i)=>`<button class="qopt ${q.ans!==null?(o.id===q.w.id?'ok':i===q.ans?'no':''):''}" onclick="ieAns(${i})">${esc(o.m)}</button>`).join('')}${q.ans!==null?'<button class="btn" style="width:100%" onclick="ieQuiz()">Keyingi savol</button>':''}</div>`}
  const list=ieList();
  return `${dqUi()}${ieMode()}${study}${gmCard()}${tgHub()}${mnCard()}${exCard()}<div class="st"><div><b>${ie.words.length}</b>jami</div><div><b>${nw}</b>yangi</div><div><b>${ln}</b>yodlangan</div></div>
  ${ieNlUi()}<h2>Test rejimi</h2><p class="mu" style="margin:0 0 8px">So‘zning to‘g‘ri ma‘nosini 4 ta variantdan top.</p>${quiz||''}<button class="btn s" style="width:100%;margin-bottom:6px" onclick="ieQuiz()">${IQ&&IQ.w?'Yangi savol':'Testni boshlash'}</button>
  <h2>So‘z qo‘shish</h2><div class="in"><input id="iw" placeholder="So‘z"><input id="im" placeholder="Ma‘nosi"><button class="btn" onclick="iAdd()">+</button></div>
  <details><summary class="mu" style="margin-bottom:8px">Ko‘p so‘z qo‘shish (har qatorda: so‘z - ma‘no)</summary><textarea id="ib" placeholder="abundant - mo‘l&#10;mitigate - yumshatmoq"></textarea><button class="btn" style="margin-top:6px" onclick="iBulk()">Qo‘shish</button></details>
  <h2>So‘zlar ro‘yxati</h2><div class="in"><input placeholder="Qidirish" value="${esc(IQS)}" onchange="IQS=this.value;render()"></div>${list||'<p class="mu">Hali so‘z yo‘q.</p>'}`}

function ieAdd(){
  const k=IK,d=V('ied')||dk(),src=V('iesr'),min=+V('iem')||0,b={},raw={};
  if(k==='L'||k==='R'||k==='M'){const lr=k==='M'?[['L','ia'],['R','ib']]:[[k,'ia']];for(const[kk,id]of lr){const r=V(id);if(r===''||+r<0||+r>40)return alert('To‘g‘ri javoblar soni 0 dan 40 gacha bo‘lsin.');raw[kk]=+r;b[kk]=rawBand(kk,+r)}}
  if(k==='W'||k==='M'){const x=parseFloat(V('iw'));if(!(x>=0&&x<=9))return alert('Writing ballini 0–9 oralig‘ida yoz.');b.W=x}
  if(k==='S'||k==='M'){const x=parseFloat(V(k==='M'?'is2':'iw'));if(!(x>=0&&x<=9))return alert('Speaking ballini 0–9 oralig‘ida yoz.');b.S=x}
  S.ie.tests.push({id:Date.now(),d,k,src,min,b,raw});
  if(d===dk())Object.keys(b).forEach(x=>{ieDp()[x]=1});save()}
function ieDel(id){S.ie.tests=S.ie.tests.filter(t=>t.id!==id);save()}
function ieMashq(){
  const kb=[['L','Listening'],['R','Reading'],['W','Writing'],['S','Speaking'],['M','To‘liq mock']].map(x=>`<button class="${IK===x[0]?'on':''}" onclick="IK='${x[0]}';render()">${x[1]}</button>`).join('');
  const n=(id,ph,st)=>`<input id="${id}" type="number" inputmode="decimal" ${st?`step="${st}"`:''} placeholder="${ph}">`;
  const inputs=IK==='L'||IK==='R'?`<div class="in">${n('ia','To‘g‘ri javoblar, 40 dan')}</div><p class="mu" style="margin:0 0 8px;font-size:12px">Ball Academic jadvali bo‘yicha taxminiy hisoblanadi.</p>`
   :IK==='M'?`<div class="in">${n('ia','Listening, 40 dan')}${n('ib','Reading, 40 dan')}</div><div class="in">${n('iw','Writing ball','0.5')}${n('is2','Speaking ball','0.5')}</div>`
   :`<div class="in">${n('iw',SK[IK]+' ball (0–9)','0.5')}</div>`;
  const L=S.ie.tests.slice().reverse().slice(0,12).map(t=>{const ks=Object.keys(t.b),ov=t.k==='M'?ieRound(Object.values(t.b).reduce((a,x)=>a+x,0)/ks.length):null;
    return `<div class="row"><span class="t">${t.k==='M'?'Mock, umumiy '+ov:SK[t.k]+' '+t.b[t.k]}<br><span class="mu">${t.d.slice(8)}.${t.d.slice(5,7)}${t.src?', '+esc(t.src):''}${t.raw&&t.raw[t.k]!==undefined?', '+t.raw[t.k]+'/40':''}${t.k==='M'?', '+ks.map(k=>k+' '+t.b[k]).join(' '):''}${t.min?', '+t.min+' daq':''}</span></span><button class="x" onclick="ieDel(${t.id})">×</button></div>`}).join('');
  return `<p class="mu" style="margin:0 0 8px">Har mashq yoki mock natijasini yoz, ilova o‘sishingni hisoblab boradi.</p><div class="seg sc">${kb}</div>${inputs}
  <div class="in"><input id="iesr" placeholder="Manba, masalan: Cambridge 17, Test 2"></div><div class="in"><input id="ied" type="date" value="${dk()}"><input id="iem" type="number" inputmode="numeric" placeholder="Daqiqa" style="max-width:100px"></div><button class="big" style="margin:0 0 12px" onclick="ieAdd()">Yozish</button>
  <h2>So‘nggi natijalar</h2>${L||'<p class="mu">Hali natija yo‘q.</p>'}`}

const WP2=['Some people believe that studying abroad is the best way to get a high-quality education, while others think local universities are just as good. Discuss both views and give your opinion.','In many countries, young people spend more time on social media than with their families. What are the causes of this, and is it a positive or negative development?','Some argue that governments should spend money on public transport rather than building new roads. To what extent do you agree or disagree?','Many people now work from home instead of going to an office. What are the advantages and disadvantages of this trend?','Some people think children should learn practical skills at school, such as cooking and money management, rather than only academic subjects. Do you agree or disagree?','Environmental problems are too big for individuals to solve, so only governments and large companies can make a difference. To what extent do you agree?','Fast food is becoming more popular around the world, and this is causing health problems. What can be done to solve this?','Some people believe that technology has made our lives more complicated, not easier. Discuss both views and give your opinion.','Older people have a lot of experience, so they should be given more responsibility in the workplace. Do you agree or disagree?','In some countries, a growing number of people choose to live alone. Why is this happening, and is it a positive or negative trend?','Some people say that international tourism brings more problems than benefits to local communities. Discuss both views and give your opinion.','Reading books for pleasure is becoming less common among young people. Why do you think this is happening, and what can be done to encourage reading?'];
const WP1=['Describe a line graph showing how the percentage of households with internet access changed in three countries over twenty years.','Summarise a bar chart comparing the average weekly hours that men and women in four countries spend on housework.','Describe a process diagram showing how plastic bottles are collected and recycled.','Describe two maps of a town centre before and after a major redevelopment.','Compare two pie charts showing the sources of electricity in one country in 1990 and in 2020.','Summarise a table comparing the monthly spending of students in four cities on housing, food and transport.'];
function wK(k){if(WE.run)return;WE.k=k;WE.p='';WE.ch=null;render()}
function wPick(){const L=WE.k===2?WP2:WP1;WE.p=L[Math.floor(Math.random()*L.length)];render()}
function wTimer(){if(WE.run){clearInterval(WE.iv);WE.run=false;render();return}
  WE.end=Date.now()+(WE.k===2?40:20)*60000;WE.run=true;
  WE.iv=setInterval(()=>{const e=document.getElementById('wtm'),l=Math.max(0,Math.ceil((WE.end-Date.now())/1000));if(e)e.textContent=fmtT(l);if(l<=0){clearInterval(WE.iv);WE.run=false;if(navigator.vibrate)navigator.vibrate([300,100,300]);render()}},500);render()}
const wcount=t=>(t.trim().match(/\S+/g)||[]).length;
function wInput(el){S.ie.dr=el.value;qsave();const n=wcount(el.value),c=document.getElementById('wcn'),min=WE.k===2?250:150;if(c){c.textContent=n+' so‘z (kamida '+min+')';c.style.color=n>=min?'var(--ac)':'var(--bad)'}}
function wSave(){const text=(S.ie.dr||'').trim(),n=wcount(text);if(n<20){alert('Avval matn yoz.');return}
  const r=['wta','wcc','wlr','wgr'].map(id=>parseFloat(V(id))||0),have=r.filter(x=>x>0),sc=have.length?ieRound(have.reduce((a,x)=>a+x,0)/have.length):0,mins=WE.run?Math.round((WE.k===2?40:20)-(WE.end-Date.now())/60000):0;
  if(WE.run){clearInterval(WE.iv);WE.run=false}
  const aiB=WFB?(+WFB.band||0):0,use=sc||aiB;S.ie.wr.push({id:Date.now(),d:dk(),k:WE.k,t:WE.p||'Mavzusiz',x:text,n,sc:use,min:mins,fb:WFB||undefined,ch:WE.ch||undefined});
  if(use){S.ie.tests.push({id:Date.now()+1,d:dk(),k:'W',src:'Essay (Task '+WE.k+')'+(sc?'':' (AI)'),min:mins,b:{W:use},raw:{}})}
  ieDp().W=1;try{mkRec('W',use)}catch(e){}S.ie.dr='';WE.p='';WE.ch=null;WFB=null;save()}
function wOpen(id){WE.open=WE.open===id?0:id;render()}
function wDel(id){if(confirm('Insho o‘chirilsinmi?')){S.ie.wr=S.ie.wr.filter(x=>x.id!==id);save()}}
function ieWrite(){
  const min=WE.k===2?250:150,n=wcount(S.ie.dr||''),tl=Math.max(0,WE.run?Math.ceil((WE.end-Date.now())/1000):(WE.k===2?2400:1200));
  const sel=id=>`<select id="${id}" style="flex:1"><option value="">${id==='wta'?'Task':id==='wcc'?'Coherence':id==='wlr'?'Lexical':'Grammar'}</option>${[9,8.5,8,7.5,7,6.5,6,5.5,5,4.5,4].map(x=>`<option>${x}</option>`).join('')}</select>`;
  const old=S.ie.wr.slice().reverse().slice(0,8).map(e=>`<div class="goal"><div class="h"><b>Task ${e.k}${e.sc?', taxminiy '+e.sc:''}${e.fb?' 🤖':''}</b><span><button class="x" style="font-size:14px" onclick="wOpen(${e.id})">${WE.open===e.id?'yopish':'ochish'}</button><button class="x" onclick="wDel(${e.id})">×</button></span></div><p class="mu" style="margin:2px 0">${e.d.slice(8)}.${e.d.slice(5,7)}, ${e.n} so‘z${e.min?', '+e.min+' daq':''}</p><p style="margin:4px 0;font-size:14px">${esc(e.t||'').slice(0,110)}${(e.t||'').length>110?'…':''}</p>${WE.open===e.id&&e.x?`<p style="white-space:pre-wrap;font-size:15px;line-height:1.5;margin:8px 0 0">${esc(e.x)}</p>${e.fb?ieFb(e.fb,String(e.id)):''}`:''}</div>`).join('');
  return `<div class="seg"><button class="${WE.k===2?'on':''}" onclick="wK(2)">Task 2 (40 daq)</button><button class="${WE.k===1?'on':''}" onclick="wK(1)">Task 1 (20 daq)</button></div>${wxBar()}
  <div class="goal"><div class="h"><b>Mavzu</b><button class="btn s" style="padding:6px 12px" onclick="wPick()">${WE.p?'Boshqa mavzu':'Mavzu tanlash'}</button></div><p style="margin:8px 0 0;line-height:1.45">${WE.p?esc(WE.p):'<span class="mu">“Mavzu tanlash” ni bos yoki o‘z mavzungda yoz.</span>'}</p></div>
  <div class="tmr" id="wtm">${fmtT(tl)}</div><button class="big ${WE.run?'ok':''}" style="margin:0 0 10px" onclick="wTimer()">${WE.run?'Taymerni to‘xtatish':'Taymerni boshlash'}</button>
  <textarea class="wta" placeholder="Inshoni shu yerga yoz..." oninput="wInput(this)">${esc(S.ie.dr||'')}</textarea><p id="wcn" class="mu" style="margin:6px 0 10px;color:${n>=min?'var(--ac)':'var(--bad)'}">${n} so‘z (kamida ${min})</p>
  <button class="big" style="margin:0 0 6px" onclick="wAI()">${WBUSY?'AI tekshirmoqda… (30-60 soniya)':'🤖 AI tekshirsin va tushuntirsin'}</button>${WFB?ieFb(WFB,'w'):''}
  <p class="mu" style="margin:0 0 6px">O‘zingni bahola (ixtiyoriy):</p><div class="in">${sel('wta')}${sel('wcc')}</div><div class="in">${sel('wlr')}${sel('wgr')}</div><button class="btn" style="width:100%" onclick="wSave()">Inshoni saqlash</button>
  <h2>Yozilgan inshoalar</h2>${old||'<p class="mu">Hali insho yo‘q.</p>'}`}

const SP1=['Do you work or are you a student?','What do you like most about your hometown?','How often do you use public transport?','What kind of food do you enjoy cooking or eating?','Do you prefer mornings or evenings? Why?','How do you usually spend your weekends?','What are your hobbies?','Do you like reading books?','How important is music in your life?','What kind of weather do you like?','What do you use your phone for?','Tell me about your family.','Do you enjoy shopping?','What do you do to stay healthy?','Do you like travelling? Why?','What did you do yesterday?','Is there a festival you enjoy in your country?','Do you prefer to study alone or with others?','How do you keep in touch with friends?','What would you like to learn in the future?'];
const SP2=['Describe a person who has influenced you. You should say: who the person is, how you know them, what they did, and explain why they influenced you.','Describe a book you enjoyed reading. You should say: what it was, why you read it, what it was about, and explain why you liked it.','Describe a place you visited that you would like to visit again. You should say: where it is, when you went, what you did there, and explain why you want to go back.','Describe a skill you learned that was useful. You should say: what the skill is, how you learned it, how long it took, and explain why it was useful.','Describe a memorable meal you had. You should say: where you had it, who was with you, what you ate, and explain why it was memorable.','Describe a time when you helped someone. You should say: who you helped, how you helped, why they needed help, and explain how you felt.','Describe a goal you want to achieve in the future. You should say: what the goal is, when you want to achieve it, how you plan to do it, and explain why it is important to you.','Describe a teacher you remember well. You should say: who the teacher was, what they taught, what they were like, and explain why you remember them.'];
const SP3=['Why do some people find it hard to learn new skills?','How has technology changed the way people read?','Do you think teachers are more important than parents in a child‘s development?','What makes a place worth visiting for tourists?','Should governments invest more in public libraries?','Why do people set goals, and why do many fail to achieve them?','How do role models affect young people?','What are the advantages of learning from experience rather than from books?'];
function spPick(part){SMD=null;SME='';if(IT)clearInterval(IT.iv);IT=null;const L=part===1?SP1:part===2?SP2:SP3;SPQ={part,q:L[Math.floor(Math.random()*L.length)],ph:0};render()}
function spTimer(sec,label,next){if(IT)clearInterval(IT.iv);IT={end:Date.now()+sec*1000,label};
  IT.iv=setInterval(()=>{const l=Math.max(0,Math.ceil((IT.end-Date.now())/1000)),e=document.getElementById('itm');if(e)e.textContent=fmtT(l);if(l<=0){clearInterval(IT.iv);if(navigator.vibrate)navigator.vibrate([250,120,250]);IT=null;if(next){SPQ.ph=2;spTimer(120,'Gapiring')}else render()}},500);render()}
function spStop(){if(IT)clearInterval(IT.iv);IT=null;render()}
function spRate(b){S.ie.tests.push({id:Date.now(),d:dk(),k:'S',src:'Speaking, Part '+SPQ.part,b:{S:b},raw:{}});ieDp().S=1;SPQ=null;if(IT)clearInterval(IT.iv);IT=null;save()}
function ieSpeak(){
  const q=SPQ,tl=IT?Math.max(0,Math.ceil((IT.end-Date.now())/1000)):0;
  const pick=`<div class="seg"><button onclick="spPick(1)">Part 1</button><button onclick="spPick(2)">Part 2</button><button onclick="spPick(3)">Part 3</button></div>`;
  let card='<p class="mu">Qismni tanla, tasodifiy savol chiqadi. Javobni ovoz chiqarib ayt va oxirida o‘zingni baho.</p>';
  if(q){card=`<div class="goal"><b>Part ${q.part}</b><p style="margin:8px 0;font-size:17px;line-height:1.45">${esc(q.q)}</p>${spModelUi()}
   ${IT?`<div class="tmr" id="itm">${fmtT(tl)}</div><p class="mu" style="text-align:center;margin:0 0 8px">${IT.label}</p><button class="btn s" style="width:100%" onclick="spStop()">To‘xtatish</button>`
   :q.part===2?`<button class="btn" style="width:100%;margin-bottom:6px" onclick="SPQ.ph=1;spTimer(60,'Tayyorlanish: 1 daqiqa',1)">1 daqiqa tayyorlanish, keyin 2 daqiqa gapirish</button>`
   :`<button class="btn" style="width:100%;margin-bottom:6px" onclick="spTimer(${q.part===1?30:60},'Gapiring')">${q.part===1?'30':'60'} soniya javob berish</button>`}
   <button class="btn ${SREC?'':'s'}" id="sprb" style="width:100%;margin:8px 0 0" onclick="spRec()">${SBUSY?'AI tinglamoqda… (30-60 soniya)':SREC?'⏹ Tugatish (0 s)':'🎙 Javobni yozib, AI ga tekshirtirish'}</button>
    <p class="mu" style="margin:8px 0 6px">O‘zingni bahola (ball):</p><div class="chips">${[5,5.5,6,6.5,7,7.5,8].map(b=>`<button onclick="spRate(${b})">${b}</button>`).join('')}</div></div>`}
  const hist=S.ie.tests.filter(t=>t.k==='S').slice(-6).reverse().map(t=>`<div class="row"><span class="t">${t.b.S}<br><span class="mu">${t.d.slice(8)}.${t.d.slice(5,7)}, ${esc(t.src||'')}</span></span>${t.fb?`<button class="x" style="font-size:14px" onclick="SOP=SOP===${t.id}?0:${t.id};render()">${SOP===t.id?'yopish':'AI izohi'}</button>`:''}</div>${SOP===t.id&&t.fb?ieFb(t.fb,String(t.id)):''}`).join('');
  return `${pick}${card}${SFB?ieFb(SFB,'s')+`<button class="big" style="margin:8px 0 0" onclick="spSaveAI()">Natijani saqlash (${esc(String(SFB.band))})</button>`:''}<h2>So‘nggi baholar</h2>${hist||'<p class="mu">Hali yozuv yo‘q.</p>'}`}

