// ================= AI YORDAMCHI =================
const aiUk=()=>'trk_aiu_'+dk();
function aiCount(n,act){try{usAi(act)}catch(e){}try{const k=aiUk();for(let i=localStorage.length-1;i>=0;i--){const x=localStorage.key(i);if(x&&x.startsWith('trk_aiu_')&&x!==k)localStorage.removeItem(x)}localStorage.setItem(k,String((+localStorage.getItem(k)||0)+(n||1)))}catch(e){}}
const aiUsed=()=>{try{return +localStorage.getItem(aiUk())||0}catch(e){return 0}};
let ALM=null,ALB=0;
function aiLimGet(){if(ALM)return ALM;try{ALM=JSON.parse(localStorage.getItem('trk_ailim_'+(UID||''))||'null')}catch(e){}return ALM}
async function aiLimRefresh(force){const c=aiLimGet();if(ALB||typeof aiOk!=='function'||!aiOk())return;if(!force&&c&&c.d===dk()&&Date.now()-c.t<600000)return;ALB=1;
  try{const d=await fnPost({action:'limit'},15000);ALM={o:!!d.owner,l:+d.limit||40,u:+d.used||0,d:dk(),t:Date.now()};try{localStorage.setItem('trk_ailim_'+(UID||''),JSON.stringify(ALM))}catch(e){}const sb2=document.getElementById('aisub');if(sb2)sb2.textContent='Kunlik tizim AI · '+aiUseLabel();try{aiStatPaint()}catch(e){}}catch(e){}ALB=0}
const aiLimit=()=>{const c=aiLimGet();return c&&c.d===dk()&&!c.o?c.l:40},aiIsOwner=()=>{const c=aiLimGet();return !!(c&&c.o)};
const aiUsedAll=()=>{const c=aiLimGet();return Math.max(aiUsed(),c&&c.d===dk()&&!c.o?c.u:0)},aiLeft=()=>aiIsOwner()?Infinity:Math.max(0,aiLimit()-aiUsedAll()),aiUseLabel=()=>{aiLimRefresh();return aiIsOwner()?'AI: cheksiz (egasi)':'AI: '+aiUsedAll()+'/'+aiLimit()+' bugun'};
function aiLimDiag(){const c=aiLimGet();return !c?'hali tekshirilmagan':c.o?'egasi hisobi: cheksiz':'oddiy hisob: kuniga '+c.l+' ta (bugun serverda '+c.u+' ta sarflangan). Egasi bo‘lsang, Supabase Secrets’dagi OWNER_EMAIL kirgan emailing bilan bir xil bo‘lishi kerak.'}
const AIQ=['Bugun nimaga e‘tibor qarataman?','Haftamni tahlil qil','Ertangi kunni rejalashtir','Maqsadlarim bo‘yicha maslahat ber','Odatlarimni qanday yaxshilayman?','Hifz tezligim va takrorimni baholab, maslahat ber','IELTS tayyorgarligimni baholab, haftalik reja tuz','Xatolarim bo‘yicha nimani takrorlay?','IELTS Writing Task 2 bo‘yicha video top','Meni ruhlantir'];
let AIL=false,AIT=null,AITL=false,AIW=null,AIT0=0;
const aiS=()=>{S.ai=S.ai||{};S.ai.chat=S.ai.chat||[];S.ai.sh=S.ai.sh||{core:1,quran:1,study:1,health:1,money:0};S.ai.tip=S.ai.tip||{};return S.ai};
const md=t=>{let s=esc(t).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/(^|\n)[-*•] (.+)/g,'$1<li>$2</li>').replace(/(^|\n)\d+\. (.+)/g,'$1<li>$2</li>');
  s=s.replace(/(<li>.*<\/li>)(\n?<li>.*<\/li>)*/g,m=>'<ul>'+m.replace(/\n/g,'')+'</ul>');return s.replace(/\n/g,'<br>')};
function aiContext(){
  const A=aiS(),sh=A.sh,k=dk(),d=new Date(),o=[],ln=t=>o.push(t),T=f=>{try{f()}catch(e){}};
  ln('Sana: '+k+', '+DAYS[d.getDay()]+', soat '+pad(d.getHours())+':'+pad(d.getMinutes()));
  if(sh.core)T(()=>{
    if(S.name)ln('Ism: '+S.name);
    const sc=scoreOf(k);ln('Bugungi ball: '+sc.p+'% ('+sc.got+'/'+sc.tot+' belgi bajarilgan)');
    ln('So‘nggi 7 kun ballari (bugundan boshlab): '+[...Array(7)].map((_,i)=>scoreOf(dAgo(i)).p+'%').join(', '));
    const X=xpInfo();ln('Daraja: '+X.L+' ('+X.name+'), ketma-ket faol kunlar: '+X.st);
    const I=nowInfo(),dn=S.done[k]||{};ln('Hozir: '+(I.b?I.b.t:'bo‘sh vaqt'));
    ln('Bugungi jadval: '+bl().filter(b=>rjIn(b,dk(),d.getDay())&&!b.id.startsWith('uyqu')).sort((a,b)=>a.s-b.s).map(b=>hm(b.s)+' '+b.t+(dn[b.id]?' (bajarilgan)':'')).join('; '));
    const top=S.top[k]||[];if(top.length)ln('3 ta asosiy ish: '+top.map(x=>x.t+(x.x?' (bajarilgan)':'')).join('; '));
    if(S.goals.length)ln('Maqsadlar: '+S.goals.map(g=>g.t+' '+gpct(g)+'%'+(g.dl?', muddat '+g.dl:'')).join('; '));
    if(S.hab.length)ln('Odatlar, oxirgi 7 kunda: '+S.hab.map(h=>h.t+' '+[...Array(7)].filter((_,i)=>(S.hb[dAgo(i)]||{})[h.id]).length+'/7').join('; '));
    if(S.wk.start)ln('Uyg‘onish maqsadi: '+hm(tgtFor(k))+(S.wake[k]?', bugun turgan vaqti: '+S.wake[k]:', bugun hali belgilanmagan'));
  });
  if(sh.quran)T(()=>{
    const q=S.q,md_=r1(mdone());ln('Qur‘on yodlash: '+md_+' bet yodlangan (taxminan '+Math.round(TOT-md_)+' bet qolgan), kunlik reja '+q.ppd+' bet, hozirgi sura: '+SN[q.cur]);
    ln('Takror: bugun navbatda '+q.ord.filter(i=>rsOf(i).due<=k).length+' ta sura, zaif suralar '+q.ord.filter(i=>rsOf(i).weak).length+' ta, jami yodlangan sura '+q.ord.length);
    ln('Hatm: '+q.hp+'/604 bet, kunlik maqsad '+q.hg+' bet, tugatilgan hatmlar '+q.hc+', bugun o‘qilgan '+(q.hd[k]||0)+' bet');
    let n=0;for(let i=0;i<7;i++)PR.slice(0,5).forEach(([p])=>{if(((S.nm.d[dAgo(i)]||{})[p])===1)n++});ln('Namoz: oxirgi 7 kunda 35 tadan '+n+' tasi o‘qilgan, jami qazo qarzi '+Object.values(S.nm.debt).reduce((a,c)=>a+c,0)+' ta');
    const R=rzInfo();if(R.left>0&&R.left<=120)ln('Ramazonga '+R.left+' kun qoldi');
  });
  if(sh.quran)T(()=>{const H=hifzStats();ln('Hifz (aniq hisob): yodlangan '+H.done+'/'+H.tot+' bet, '+H.rem+' bet qoldi'+(H.days?', kuniga '+H.ppd+' bet bilan taxminan '+H.days+' kun ('+H.eta+')':'')+', to‘liq juz’lar '+H.juz+'/30, bu hafta '+H.week+' bet, bugungi sabaq '+H.sabaq+'/'+H.ppd+', sabqi va manzil '+H.partsDone+'/'+H.parts+' bajarilgan')});
 if(sh.study)T(()=>{const R=ieReady(),E=ieErrs();ln('IELTS tayyorgarlik: '+R.pc+'% (ko‘nikmalar '+R.skill+'%, lug‘at '+R.vocab+'%, 14 kunlik izchillik '+R.cons+'%, 30 kunlik mock '+R.mock+'%). Yodlangan so‘z '+R.learned+'/'+R.vg+'. Tavsiya: '+R.next);
  if(E.length){const c={};E.forEach(e=>c[e.t]=(c[e.t]||0)+e.n);ln('Writing/Speaking xatolari turlari: '+Object.entries(c).map(([k,n])=>k+' '+n).join(', ')+'. Oxirgi xatolar: '+E.slice(0,4).map(e=>'“'+e.o+'” → “'+e.c+'”').join('; '))}
  ln('IELTS materiallari: '+ieM().length+' ta, ulardan lug‘atga '+S.ie.words.filter(w=>w.src).length+' ta so‘z qo‘shilgan')});
 if(sh.study)T(()=>{
    const st=ieStat(),I=S.ie;if(I.words.length)ln('IELTS lug‘atidagi so‘zlar (takrorlama): '+I.words.slice(-60).map(x=>x.w).join(', '));ln('IELTS: maqsad '+(I.target||7)+', taxminiy umumiy ball '+(st.ov===null?'hali yo‘q':st.ov)+(I.ex?', imtihon '+I.ex+' ('+dl(I.ex)+' kun qoldi)':'')+'. Ko‘nikmalar: '+Object.keys(SK).map(x=>SK[x]+' '+(st.c[x]===null?'yo‘q':st.c[x])).join(', ')+'. Lug‘at: navbatda '+wDue().length+' ta, jami '+I.words.length+' ta. Mashq seriyasi '+ieStreak()+' kun');
    const ut=S.un.tasks.filter(t=>!t.x&&t.due).sort((a,b)=>a.due>b.due?1:-1).slice(0,4);if(ut.length)ln('Univer topshiriqlari: '+ut.map(t=>t.t+' ('+dlTxt(dl(t.due))+')').join('; '));
    const ex=S.un.exams.filter(e=>dl(e.d)>=0).slice(0,3);if(ex.length)ln('Imtihonlar: '+ex.map(e=>e.s+' ('+dlTxt(dl(e.d))+')').join('; '));
    const ts=S.pr.tests.slice(-5);if(ts.length)ln('Prava testlari: o‘rtacha '+Math.round(ts.reduce((a,x)=>a+x.c/x.t,0)/ts.length*100)+'%'+(S.pr.exam?', imtihon '+S.pr.exam:''));
    const rb=S.kt.books.filter(b=>b.st==='o');const kp=S.kt.log.filter(x=>x.d===k).reduce((a,x)=>a+x.n,0);ln('Kitob: o‘qilayotgan '+(rb.map(b=>b.t+' '+b.p+'/'+(b.n||'?')).join('; ')||'yo‘q')+', bugun '+kp+' bet (maqsad '+(S.kt.goal||20)+')');
  });
  if(sh.health)T(()=>{
    const wk=[...Array(7)].map((_,i)=>dAgo(i));ln('Zal: oxirgi 7 kunda '+new Set(S.gym.log.filter(x=>wk.includes(x.d)).map(x=>x.d)).size+' kun mashq qilingan');
    const bd=S.gym.body.slice(-1)[0];if(bd)ln('Oxirgi vazn: '+bd.w+' kg');
    ln('Bugun: suv '+(S.water[k]||0)+'/8 stakan, kayfiyat '+(S.mood[k]?S.mood[k]+'/5':'belgilanmagan')+', fokus '+(S.fm[k]||0)+' daqiqa');
    let st=0;for(let i=0;i<120;i++){if((S.rules[dAgo(i)]||{}).ig)st++;else if(i>0)break}ln('Instagramsiz ketma-ket kunlar: '+st+', bugungi ekran vaqti '+(S.iso.m[k]||0)+' daqiqa (limit '+S.iso.lim+')');
  });
  if(sh.money)T(()=>{const mk=k.slice(0,7),L=S.money.filter(m=>m.w==='p'&&m.d.startsWith(mk)),i=L.filter(m=>m.k==='in').reduce((a,m)=>a+m.a,0),u=L.filter(m=>m.k==='out').reduce((a,m)=>a+m.a,0),c={};L.filter(m=>m.k==='out').forEach(m=>{c[m.c||'Boshqa']=(c[m.c||'Boshqa']||0)+m.a});const tc=Object.entries(c).sort((a,b)=>b[1]-a[1])[0];
    ln('Shaxsiy pul (shu oy): kirim '+num(i)+', chiqim '+num(u)+(tc?', eng ko‘p sarf: '+tc[0]:'')+(S.fin.budget?', oylik limit '+num(S.fin.budget):''))});
  return o.join('\n')}
async function aiSession(){try{return (await sb.auth.getSession()).data.session}catch(e){return null}}
async function fnPost(body,ms){
  let s=await aiSession();
  if(!s)throw new Error('Hisobga qayta kiring.');
  const ctl=new AbortController(),to=setTimeout(()=>ctl.abort(),ms||60000);let res;
  try{res=await fetch(CFG.url+'/functions/v1/ai-assistant',{method:'POST',signal:ctl.signal,headers:{'Content-Type':'application/json','Authorization':'Bearer '+s.access_token,'apikey':CFG.key},body:JSON.stringify(body)})}
  catch(e){clearTimeout(to);throw new Error(e&&e.name==='AbortError'?'AI juda sekin javob berdi. Qayta urinib ko‘ring.':'Serverga ulanib bo‘lmadi. Internetni tekshiring.')}
  clearTimeout(to);let j=null;try{j=JSON.parse(await res.text())}catch(e){}
  if(!res.ok){let m=(j&&(j.error||j.message))||'';
    if(res.status===404)m='AI funksiyasi topilmadi. Supabase’da nomi aynan “ai-assistant” bo‘lgan funksiya borligini tekshiring.';
    else if(res.status===401&&!m)m='Hisobga qayta kiring.';
    else if(/Savol topilmadi/.test(m)&&body.action&&body.action!=='chat')m='Server eski versiyada. Supabase’da ai-assistant funksiyasini yangi kod bilan qayta Deploy qiling.';
    try{aiQuotaMark(m)}catch(e){}throw new Error((m||'Server xatosi ('+res.status+').')+(res.status===429&&j&&j.detail?' ['+j.detail+']':''))}
  if(!j)throw new Error('Serverdan tushunarsiz javob keldi.');
  if(j.error)throw new Error(j.error);return j}
async function aiCall(msgs,ctx){const d=await fnPost({action:'chat',messages:msgs,context:ctx},60000);if(!d.text)throw new Error('AI javob bermadi.');return d}
function aiBuild(){const old=document.getElementById('ai');if(old)old.remove();const d=document.createElement('div');d.id='ai';d.className='ai';
  d.innerHTML=`<div class="aih"><button class="x" style="font-size:22px" onclick="aiClose()">✕</button><div style="flex:1"><b>✨ Yordamchi</b><div class="mu" style="font-size:12px" id="aisub">Kunlik tizim AI</div></div><button class="btn s" style="padding:7px 12px" onclick="aiNew()">Yangi suhbat</button></div><div id="aic" class="aic"></div><div id="aiq" class="aiq">${AIQ.map((q,i)=>`<button onclick="aiGo(${i})">${q}</button>`).join('')}</div><div class="aif"><button class="mic" id="aimic" onclick="aiMic()" aria-label="Ovozli kiritish">🎤</button><textarea id="aii" rows="1" placeholder="Savol yoz..." oninput="aiGrow(this)" onfocus="setTimeout(()=>{const c=document.getElementById('aic');if(c)c.scrollTop=c.scrollHeight},350)"></textarea><button class="send" onclick="aiGo()">➤</button></div>`;
  document.body.appendChild(d)}
function aiGrow(el){el.style.height='auto';el.style.height=Math.min(120,el.scrollHeight)+'px'}
function aiRender(){const sb2=document.getElementById('aisub');if(sb2)sb2.textContent='Kunlik tizim AI · '+aiUseLabel();const c=document.getElementById('aic');if(!c)return;const A=aiS(),ch=A.chat;
  const hi=`<div class="bb a">Assalomu alaykum${S.name?', '+esc(S.name):''}! Men sening shaxsiy yordamchingman. Kuning, odatlaring, Qur‘on, IELTS va maqsadlaring haqida ma‘lumotlaringni ko‘raman, shunga qarab maslahat beraman. Pastdagi savollardan birini tanla yoki o‘zing yoz.</div>`;
  c.innerHTML=hi+ch.map((m,i)=>{const t=(AIT&&i===ch.length-1&&m.r==='model')?m.t.slice(0,AIT.n):m.t;return `<div class="bb ${m.r==='user'?'u':m.r==='err'?'e':'a'}">${m.r==='plan'?dpCard(m,i):m.r==='user'?esc(t).replace(/\n/g,'<br>'):m.r==='err'?'⚠️ '+esc(t)+(i===ch.length-1&&ch[i-1]&&ch[i-1].r==='user'&&!AIL?'<br><button class="btn s" style="margin-top:8px" onclick="aiRetry()">↻ Qayta yuborish</button>':''):md(m.r==='model'?aiActs(t).clean:t)+(m.r==='model'&&!AIT?aiCards(m,i)+aiExtra(m):'')+(m.ms&&!AIT?`<div class="mu" style="font-size:11px;margin-top:6px">⏱ ${esc(m.ms)}</div>`:'')}</div>`}).join('')+(AIL?`<div class="bb a"><span class="dots"><span></span><span></span><span></span></span> <span class="mu" style="font-size:12px">${Math.floor((Date.now()-AIT0)/1000)} s${AIRT?' · qayta urinyapman':''}</span></div>`:'');
  c.scrollTop=c.scrollHeight}
// Oyna ochiq paytda orqadagi sahifa qotiriladi, oyna esa klaviatura ustidagi ko‘rinadigan maydonga moslanadi (iOS)
let OVL=null;
function ovLock(el){ovUnlock();const y=window.scrollY||window.pageYOffset||0,v=window.visualViewport;
  const fit=()=>{const w=window.visualViewport;if(!w||!el.isConnected)return;el.style.height=w.height+'px';el.style.top=w.offsetTop+'px';el.style.bottom='auto';
    const c=el.querySelector('.aic');if(c&&document.activeElement&&document.activeElement.tagName==='TEXTAREA')c.scrollTop=c.scrollHeight};
  const tm=e=>{if(!(e.target.closest&&e.target.closest('.aic,.aiq,.mfp,.mfs,textarea')))e.preventDefault()};
  OVL={el,y,v,fit,tm};document.documentElement.classList.add('ovl');document.body.style.top=(-y)+'px';
  if(v){v.addEventListener('resize',fit);v.addEventListener('scroll',fit)}el.addEventListener('touchmove',tm,{passive:false});fit()}
function ovUnlock(){if(!OVL)return;const o=OVL;OVL=null;if(o.v){o.v.removeEventListener('resize',o.fit);o.v.removeEventListener('scroll',o.fit)}
  try{o.el.removeEventListener('touchmove',o.tm)}catch(e){}document.documentElement.classList.remove('ovl');document.body.style.top='';window.scrollTo(0,o.y)}
function aiOpen(msg){if(!sb||!UID){alert('AI yordamchi uchun hisobga kirgan bo‘lish kerak.');return}aiBuild();ovLock(document.getElementById('ai'));aiRender();if(msg)aiSend(msg)}
function aiClose(){ovUnlock();const e=document.getElementById('ai');if(e)e.remove()}
function aiNew(){if(AIT&&AIT.iv)clearInterval(AIT.iv);AIT=null;AIL=false;aiS().chat=[];qsave();aiRender()}
function aiClear(){if(confirm('Suhbat tarixi o‘chirilsinmi?')){aiS().chat=[];save()}}
function aiGo(i){if(AIL)return;let t;if(typeof i==='number')t=AIQ[i];else{const e=document.getElementById('aii');t=e?e.value.trim():'';if(e){e.value='';aiGrow(e)}}if(t)aiSend(t)}
async function aiStream(msgs,ctx,onText,onMeta,opt){let got=false;const wrap=x=>{got=true;onText(x)};
  try{const r=await aiStream1(msgs,ctx,wrap,onMeta,opt);aiCount(1,'chat');return r}
  catch(e){if(got||!e.gw)throw e;if(opt&&opt.onRetry)opt.onRetry();await new Promise(r=>setTimeout(r,1500));const r2=await aiStream1(msgs,ctx,onText,onMeta,opt);aiCount(1,'chat');return r2}}
async function aiStream1(msgs,ctx,onText,onMeta,opt){
  let s=await aiSession();
  if(!s)throw new Error('Hisobga qayta kiring.');
  let res;const ctl=new AbortController(),to=setTimeout(()=>ctl.abort(),45000);
  try{res=await fetch(CFG.url+'/functions/v1/ai-assistant',{method:'POST',signal:ctl.signal,headers:{'Content-Type':'application/json','Authorization':'Bearer '+s.access_token,'apikey':CFG.key},body:JSON.stringify({action:'chat',stream:true,web:!!(opt&&opt.web),messages:msgs,context:ctx})})}
  catch(e){clearTimeout(to);if(e&&e.name==='AbortError')throw new Error('AI 45 soniyada javob bermadi. Birozdan keyin urinib ko‘ring.');const r=await aiCall(msgs,ctx);onText(r.text);return r.text}
  clearTimeout(to);try{const tm=res.headers&&res.headers.get&&res.headers.get('x-timing');if(tm&&onMeta)onMeta(tm)}catch(e){}
  if(!res.ok){let m='',raw='';try{raw=await res.text();const j=JSON.parse(raw);m=(j.error||j.message||'')+(res.status===429&&j.detail?' ['+j.detail+']':'')}catch(e){}
    if(res.status===404)m='AI funksiyasi topilmadi. Supabase’da nomi aynan “ai-assistant” bo‘lgan funksiya yaratilganini tekshiring.';
    if(!m&&[502,503,504,546].includes(res.status)){const er=new Error('AI serveri vaqtincha javob bermadi ('+res.status+').'+(raw?' '+raw.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim().slice(0,100):''));er.gw=1;throw er}throw new Error(m||('Server xatosi ('+res.status+').'))}
  const ct=(res.headers&&res.headers.get&&res.headers.get('content-type'))||'';
  if(ct.includes('application/json')){const j=await res.json();if(j&&j.text){onText(j.text);if(opt&&opt.onSrc)opt.onSrc(j.sources||[]);return j.text}throw new Error((j&&j.error)||'AI javob bermadi.')}
  if(!res.body||!res.body.getReader){const t=await res.text();onText(t);return t}
  const rd=res.body.getReader(),dec=new TextDecoder();let full='';
  while(true){const{done,value}=await rd.read();if(done)break;full+=dec.decode(value,{stream:true});onText(full)}
  full+=dec.decode();onText(full);return full}
function aiTimingLine(meta,tf,tot){meta=meta||'';const g=/gemini=(\d+)/.exec(meta),sv=/auth=(\d+),db=(\d+)/.exec(meta),th=/think=(\w+)/.exec(meta),at=/att=([^,]*)/.exec(meta),sg=(g?+g[1]:0)+(sv?+sv[1]+ +sv[2]:0);
  return (tot/1000).toFixed(1)+' s ('+(tf?'birinchi so‘z '+(tf/1000).toFixed(1)+' s':'')+(g?', Gemini '+(g[1]/1000).toFixed(1)+' s':'')+(sv?', server '+((+sv[1]+ +sv[2])/1000).toFixed(1)+' s':'')+(th?', o‘ylash: '+th[1]:'')+(at&&at[1].includes('|')?', urinishlar: '+at[1].split('|').map(x=>x.replace(/^gemini-/,'')).join(' → '):'')+(tf&&tf-sg>4000?', tarmoq/kutish: '+((tf-sg)/1000).toFixed(1)+' s':'')+')'}
let AIRT=false;
function aiRetry(){if(AIL)return;const ch=aiS().chat,l=ch[ch.length-1];if(!l||l.r!=='err')return;ch.pop();const u=ch[ch.length-1];if(!u||u.r!=='user')return;ch.pop();aiSend(u.t)}
async function aiSend(text){AIRT=false;
  const A=aiS();A.chat.push({r:'user',t:text});if(A.chat.length>40)A.chat.splice(0,A.chat.length-40);AIL=true;AIT0=Date.now();clearInterval(AIW);AIW=setInterval(()=>{if(AIL)aiRender();else{clearInterval(AIW);AIW=null}},1000);aiRender();qsave();if(aiOk()&&aiPlanIntent(text)){await aiDayPlan(text,dpDate(text));return}
  const hist=A.chat.filter(m=>m.r==='user'||m.r==='model').slice(-10).map(m=>({r:m.r,t:m.t})),ctx=aiContext();
  try{
    const m={r:'model',t:''};let started=false,last=0,meta='',tf=0;
    const web=/video|youtube|yutub|havola|link|qidir|internet|saytdan|manba|izla|yangilik|news/i.test(text),vid=/video|youtube|yutub/i.test(text),vq=text.replace(/video(lar)?|youtube|yutub|havola(si)?|link(ini)?|topib|top\b|ber\b|qidir|izla|menga|iltimos|tashla|bo‘yicha|haqida/gi,' ').replace(/\s+/g,' ').trim()||text;
    let vidData=null,mref=null;const setVid=()=>{if(mref&&vidData){mref.vid=vidData;aiRender()}};
    if(vid){fnPost({action:'videos',q:vq.slice(0,100)},25000).then(d=>{vidData=d;setVid()}).catch(()=>{vidData={videos:[]};setVid()})}
    const full=await aiStream(hist,ctx,t=>{if(!started){started=true;tf=Date.now()-AIT0;A.chat.push(m);AIL=false;mref=m;if(vid){m.vq=vq;setVid()}}m.t=t;const n=Date.now();if(n-last>50){last=n;aiRender()}},h=>{meta=h},{web,onRetry:()=>{AIRT=true;aiRender()},onSrc:s=>{if(mref&&s.length)mref.src=s;else m.src=s}});
    AIL=false;if(!started)A.chat.push(m);m.t=full;
    const g=/gemini=(\d+)/.exec(meta),sv=/auth=(\d+),db=(\d+)/.exec(meta),th=/think=(\w+)/.exec(meta);m.ms=aiTimingLine(meta,tf,Date.now()-AIT0);
    if(!String(full).trim()){A.chat.pop();throw new Error('Bo‘sh javob keldi.')}
    aiRender()}
  catch(e){AIL=false;A.chat.push({r:'err',t:e.message});aiRender()}
  qsave()}
let AITERR='';
async function aiTip(){if(AITL)return;AITL=true;AITERR='';render();
  try{const r=await aiCall([{r:'user',t:'Bugun uchun menga 3 ta eng muhim, aniq va qisqa maslahat ber. Ma‘lumotlarimga qarab yoz. Oxirida bitta ruhlantiruvchi gap qo‘sh.'}],aiContext());aiS().tip[dk()]=r.text}
  catch(e){AITERR=e.message}AITL=false;save()}
function aiCard(){if(!sb||!UID)return '';const t0=aiS().tip[dk()],t=t0&&!/^⚠️/.test(t0)?t0:'';
  return `<div class="goal" style="margin-top:12px;border-left:4px solid var(--ac)"><div class="h"><b style="font:700 18px Fraunces,serif">✨ Yordamchi</b><button class="x" style="font-size:14px" onclick="aiOpen()">Suhbat</button></div>${AITL?'<p class="mu" style="margin:8px 0 0">Maslahat tayyorlanmoqda…</p>':t?`<div style="margin:8px 0;font-size:14.5px;line-height:1.5">${md(t)}</div><button class="btn s" style="padding:6px 12px" onclick="aiTip()">Yangilash</button>`:`<p class="mu" style="margin:4px 0 10px">Ma‘lumotlaringga qarab bugungi eng muhim maslahatlarni oladi.</p><button class="btn" style="width:100%" onclick="aiTip()">Bugungi maslahatni olish</button>${AITERR?`<p style="color:var(--bad);margin:8px 0 0;font-size:13px">⚠️ ${esc(AITERR)}</p>`:''}`}</div>`}
function aiSh(k){const sh=aiS().sh;sh[k]=sh[k]?0:1;save()}
async function aiModels(){try{const r=await sb.functions.invoke('ai-assistant',{body:{action:'models'}});if(r.error)throw new Error('Funksiya javob bermadi');const m=(r.data&&r.data.models)||[];alert('Mavjud modellar ('+m.length+'):\n'+m.filter(x=>/flash|pro/i.test(x)).slice(0,25).join('\n')+'\n\nBittasini Supabase secret GEMINI_MODEL sifatida yozishing mumkin.')}catch(e){alert('Modellarni olib bo‘lmadi: '+e.message)}}
function aiSet(){const sh=aiS().sh,row=(k,t)=>`<button class="row ${sh[k]?'done':''}" onclick="aiSh('${k}')"><span class="ck">${sh[k]?'✓':''}</span><span class="t">${t}</span></button>`;
  return `<p class="mu" style="margin:0 0 8px">Yordamchi javob berish uchun tanlangan bo‘limlarning <b>umumiy raqamlarini</b> Google Gemini'ga yuboradi. Shaxsiy yozuvlar (kun xulosasi, izohlar, qarzlar) yuborilmaydi. Chatga o‘zing yozgan matn esa yuboriladi.</p>${row('core','Kun, odat va maqsadlar')}${row('quran','Qur‘on va namoz')}${row('study','IELTS, Univer, Prava, kitob')}${row('health','Zal, kayfiyat, Isolation')}${row('money','Pul (oylik umumiy kirim va chiqim)')}<button class="ghost" onclick="aiClear()">Suhbat tarixini tozalash</button>${Array.isArray(OW)?'<button class="ghost" onclick="aiModels()">Mavjud modellarni ko‘rish</button>':''}`}

function aiExtra(m){let o='';
  if(m.vid&&m.vid.videos&&m.vid.videos.length)o+=`<div class="vcs">${m.vid.videos.map(v=>`<a class="vc" href="https://www.youtube.com/watch?v=${esc(v.id)}" target="_blank" rel="noopener">${v.th?`<img src="${esc(v.th)}" alt="">`:''}<span><b style="font-size:13px;line-height:1.3;display:block">${esc(v.t||'Video')}</b><span class="mu" style="font-size:12px">${esc(v.ch||'')}</span></span></a>`).join('')}</div>`;
  else if(m.vq)o+=`<div class="srcs"><a href="https://www.youtube.com/results?search_query=${encodeURIComponent(m.vq)}" target="_blank" rel="noopener">▶ YouTube’da qidirish: ${esc(m.vq.slice(0,40))}</a></div>`;
  if(m.src&&m.src.length)o+=`<div class="srcs">${m.src.map(s=>{let t=s.t;if(!t){try{t=new URL(s.u).hostname}catch(e){t='manba'}}return `<a href="${esc(s.u)}" target="_blank" rel="noopener">🔗 ${esc(t.slice(0,32))}</a>`}).join('')}</div>`;
  return o}
// ---- AI amallari: AI taklif qiladi, foydalanuvchi tasdiqlaydi ----
function aiActs(text){const acts=[];let clean=String(text).replace(/\[\[ACTION\s*([\s\S]*?)\]\]/g,(m,j)=>{try{const o=JSON.parse(j.trim());if(o&&o.type)acts.push(o)}catch(e){}return ''});
  clean=clean.replace(/\[\[ACTION[\s\S]*$/,'').replace(/\n{3,}/g,'\n\n').trim();return{clean,acts}}
const aiDesc=a=>a.type==='add_words'?`➕ ${(a.items||[]).length} ta so‘z IELTS lug‘atiga`:a.type==='add_task'&&a.t?`📝 Vazifa: ${a.t}${a.date?' ('+a.date+')':''}`:a.type==='add_top3'&&a.t?`⭐ Asosiy ish: ${a.t}`:a.type==='add_habit'&&a.t?`✅ Odat: ${(a.e||'')+' '+a.t}`:a.type==='add_plan'&&a.t&&a.s?`📅 Reja: ${a.t}, ${a.s}${a.e?'–'+a.e:' (bir lahzalik)'}`:a.type==='add_milestone'&&a.t&&a.goal?`🎯 Bosqich: ${a.t} (${a.goal})`:'';
const aiList=m=>aiActs(m.t).acts.filter(a=>aiDesc(a));
function aiCards(m,i){return aiList(m).map((a,j)=>`<div class="act"><span>${esc(aiDesc(a))}</span>${m.dn&&m.dn[j]?'<b style="color:var(--ac)">✓ Qo‘shildi</b>':`<button class="btn" style="padding:6px 12px" onclick="aiApply(${i},${j})">Qo‘shish</button>`}</div>`).join('')}
function aiApply(i,j){
  const m=aiS().chat[i];if(!m)return;const a=aiList(m)[j];if(!a||(m.dn&&m.dn[j]))return;let ok=false;
  try{switch(a.type){
    case 'add_words':{let n=0;const have=new Set(S.ie.words.map(x=>sn(x.w)));(a.items||[]).slice(0,30).forEach((x,k)=>{const w=String(x&&x.w||'').trim();if(w&&!have.has(sn(w))){have.add(sn(w));S.ie.words.push({id:Date.now()+k,w,m:String(x.m||'').trim(),box:0,due:dk(),t:0});n++}});ok=n>0;if(!ok)alert('Bu so‘zlar lug‘atda allaqachon bor.');break}
    case 'add_task':{const k=/^\d{4}-\d\d-\d\d$/.test(a.date||'')?a.date:dk();(S.tasks[k]=S.tasks[k]||[]).push({t:String(a.t).trim(),x:0});ok=true;break}
    case 'add_top3':{const k=dk(),L=S.top[k]=S.top[k]||[];if(L.length>=3){alert('Bugun 3 ta asosiy ish allaqachon bor.');break}L.push({t:String(a.t).trim(),x:0});ok=true;break}
    case 'add_habit':{if(S.hab.some(h=>hnorm(h.t)===hnorm(a.t))){alert('Bunday odat allaqachon bor.');break}S.hab.push({id:'h'+Date.now(),t:String(a.t).trim(),e:a.e||''});ok=true;break}
    case 'add_plan':{if(!/^\d{1,2}:\d\d$/.test(a.s||'')){alert('Reja vaqti noto‘g‘ri.');break}const s=t2m(a.s),pt=!a.e,e=pt?s+15:(t2m(a.e)<=s?t2m(a.e)+1440:t2m(a.e));S.bl=bl().map(b=>({...b}));S.bl.push({id:'n'+Date.now(),t:String(a.t).trim(),n:a.n||'',s,e,pt,d:[0,1,2,3,4,5,6]});ok=true;break}
    case 'add_milestone':{const g=S.goals.find(x=>sn(x.t).includes(sn(a.goal))||sn(a.goal).includes(sn(x.t)));if(!g){alert('Bunday maqsad topilmadi.');break}(g.ms=g.ms||[]).push({t:String(a.t).trim(),x:0});ok=true;break}
  }}catch(e){alert('Qo‘shib bo‘lmadi.')}
  if(ok){(m.dn=m.dn||{})[j]=1;save();aiRender()}}

// ---- AI kun rejasi: AI taklif qiladi, foydalanuvchi tasdiqlaydi ----
let PLN=null;
function aiPlanCtx(){const k=dk(),d=new Date(),day=d.getDay(),u=S.un||{tasks:[],exams:[]},mg=S.goals[S.main],mn=mg&&(mg.ms||[]).find(m=>!m.x),P=ssParts(),pz=a=>r1((P.find(p=>p.k===a)||{p:0}).p);
  return{sana:k,hafta_kuni:DAYS[day],soat:d.getHours(),
    reja:bl().filter(b=>rjIn(b,dk(),day)&&!b.id.startsWith('uyqu')).map(b=>hm(b.s)+'-'+hm(b.e)+' '+b.t).slice(0,14),
    muddatlar:[...(u.tasks||[]).filter(t=>!t.x&&t.due&&dl(t.due)<=7).map(t=>'Topshiriq: '+t.t+' ('+dlTxt(dl(t.due))+')'),...(u.exams||[]).filter(e=>dl(e.d)>=0&&dl(e.d)<=14).map(e=>'Imtihon: '+e.s+' ('+dlTxt(dl(e.d))+')')].slice(0,8),
    maqsad:mg?{nom:mg.t,foiz:gpct(mg),keyingi_bosqich:mn?mn.t:'',kun_qoldi:mg.dl?dl(mg.dl):null}:null,
    mavjud_top3:(S.top[k]||[]).map(x=>x.t),hifz:{kunlik_bet:S.q.ppd,sabqi_bet:pz('q'),manzil_bet:pz('m')},zaif_soha:rwRep(rwMon(k)).weak||'',
    kecha_xp:dayPts(dAgo(1)).t,kun_maqsadi_xp:rwGoal(k),seriya:rwStreak(),yengil_kun:!!rw().lt[k]}}
async function aiPlan(){if(PLN&&PLN.busy)return;PLN={busy:true};render();
  try{const d=await fnAI({action:'plan',ctx:JSON.stringify(aiPlanCtx())}),j=parseJson(d.text),T=j&&Array.isArray(j.top3)?j.top3.map(x=>String((x&&x.t)||'').trim().slice(0,70)).filter(Boolean).slice(0,3):[];
    if(!T.length)throw new Error('AI tushunarli reja bermadi. Qayta urinib ko‘ring.');PLN={top3:T,tip:String(j.tip||'').slice(0,160)}}
  catch(e){PLN={err:String(e.message||e).slice(0,200)}}render()}
function aiPlanAdd(){const k=dk(),L=S.top[k]=S.top[k]||[],free=3-L.length;if(!PLN||!PLN.top3)return;if(free<=0){toast('Top-3 to‘la');return}
  const A=PLN.top3.slice(0,free);A.forEach(t=>L.push({t,x:0}));PLN=null;save();toast(A.length+' ta ish qo‘shildi')}
const aiPlanNo=()=>{PLN=null;render()};
function aiOk(){return !!(sb&&UID)}
function aiPlanUi(k,fu,L){if(!aiOk()||fu||k!==dk())return '';
  if(PLN&&PLN.busy)return '<p class="mu" style="margin:8px 0 0">✨ AI reja tuzmoqda…</p>';
  if(PLN&&PLN.err)return `<p style="margin:8px 0;color:var(--bad)">${esc(PLN.err)}</p><button class="btn s" onclick="aiPlan()">Qayta urinish</button> <button class="x" onclick="aiPlanNo()">✕</button>`;
  if(PLN&&PLN.top3)return `<div class="aipl"><b>✨ AI taklifi</b><ol>${PLN.top3.map(t=>`<li>${esc(t)}</li>`).join('')}</ol>${PLN.tip?`<p class="mu" style="margin:6px 0">${esc(PLN.tip)}</p>`:''}<div class="in"><button class="btn" onclick="aiPlanAdd()">${L.length?'Bo‘sh joyga qo‘sh':'Top-3 ga qo‘sh'}</button><button class="btn s" onclick="aiPlanNo()">Rad etish</button></div></div>`;
  return L.length<3?'<button class="btn s" style="margin-top:8px" onclick="aiPlan()">✨ AI bilan rejala</button>':''}
