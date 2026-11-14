// ---- AI kun rejasi (ertalabdan kechgacha): qat'iy bloklar joyida qoladi, AI ularning ichiga aniq vazifa yozadi va bo'sh oraliqlarga qo'shimcha ish qo'yadi ----
function aiPlanIntent(t){return /(ertangi\s+kun|bugungi\s+kun|kunimni|kunni|ertalabdan|kechgacha|rejamni|kun\s+(tartib|reja|jadval)|jadval(imni)?|ertaga\s+uchun)/i.test(t)&&/(tuz|rejala|rejalashtir|chiz|yoz)/i.test(t)}
function dpDate(t){return /ertaga|ertalab|ertangi|erta\b/i.test(t)?dAgo(-1):/bugun/i.test(t)?dk():new Date().getHours()>=20?dAgo(-1):dk()}
function dpWord(d){return d===dk()?'Bugun':d===dAgo(-1)?'Ertaga':d.slice(8)+'.'+d.slice(5,7)}
function dpBlocks(date){const dow=new Date(date+'T12:00').getDay();return bl().filter(b=>rjIn(b,date,dow)&&!b.id.startsWith('uyqu')).sort((a,b)=>a.s-b.s)}
function dpCtx(date,wish,alt){const dow=new Date(date+'T12:00').getDay(),u=S.un||{tasks:[],exams:[]},mg=S.goals[S.main],mn=mg&&(mg.ms||[]).find(m=>!m.x),P=ssParts(),pz=a=>r1((P.find(p=>p.k===a)||{p:0}).p),pt=ptTimes(),sl=bl().find(b=>b.id.startsWith('uyqu')&&b.d.includes(dow));
  return{sana:date,hafta_kuni:DAYS[dow],bugun:date===dk(),istak:String(wish||'').slice(0,400),boshqacha:!!alt,turish:hm(S.wk&&S.wk.start?tgtFor(date):300),uxlash:sl?hm(sl.s):'23:00',
    qat_bloklar:dpBlocks(date).map(b=>({id:b.id,s:hm(b.s),e:hm(b.e),t:b.t})),
    namoz_vaqtlari:pt?Object.fromEntries(PNAMES.map(([k,n])=>[n,hm(pt[k])])):null,
    muddatlar:[...(u.tasks||[]).filter(t=>!t.x&&t.due&&dl(t.due)<=10).map(t=>'Topshiriq: '+t.t+' (muddat '+t.due+')'),...(u.exams||[]).filter(e=>dl(e.d)>=0&&dl(e.d)<=21).map(e=>'Imtihon: '+e.s+' ('+e.d+')')].slice(0,8),
    maqsad:mg?{nom:mg.t,foiz:gpct(mg),keyingi_bosqich:mn?mn.t:''}:null,
    hifz:{kunlik_bet:S.q.ppd,sabqi_bet:pz('q'),manzil_bet:pz('m')},zal:(S.gym.plan[dow]&&S.gym.plan[dow].place)||'',zaif_soha:rwRep(rwMon(dk())).weak||'',
    yengil_kun:!!rw().lt[date],mavjud_top3:(S.top[date]||[]).map(x=>x.t)}}
// AI javobini tekshirib, jadvalga aylantiradi: bloklar o'z vaqtida, qo'shimcha ishlar bloklar bilan va o'zaro kesishmaydi
function dpBuild(date,j){const B=dpBlocks(date),notes={},dow=new Date(date+'T12:00').getDay(),sl=bl().find(b=>b.id.startsWith('uyqu')&&b.d.includes(dow)),lo=S.wk&&S.wk.start?tgtFor(date):300,hi=sl?Math.min(sl.s,1439):1380;
  (Array.isArray(j&&j.blocks)?j.blocks:[]).forEach(x=>{if(x&&x.id)notes[String(x.id)]=String(x.n||'').trim().slice(0,110)});
  const fx=B.map(b=>({id:b.id,s:b.s,e:b.e,t:b.t,n:notes[b.id]||'',fx:1})),tm=v=>{const m=/^(\d{1,2}):(\d{2})$/.exec(String(v||'').trim());if(!m)return NaN;const h=+m[1],n=+m[2];return h>23||n>59?NaN:h*60+n};
  const ex=[];(Array.isArray(j&&j.extra)?j.extra:[]).forEach((x,i)=>{if(!x)return;const s=tm(x.s),e=tm(x.e),t=String(x.t||'').trim().slice(0,60);if(isNaN(s)||isNaN(e)||!t||e<=s)return;ex.push({id:'x'+date.slice(5).replace('-','')+i,s,e,t,n:'',x:0})});
  ex.sort((a,b)=>a.s-b.s);const keep=[];
  for(const x of ex){if(x.s<lo||x.e>hi)continue;if(fx.some(b=>x.s<b.e&&x.e>b.s))continue;const pv=keep[keep.length-1];if(pv&&x.s<pv.e)x.s=pv.e;if(x.e-x.s<15)continue;keep.push(x);if(keep.length>=6)break}
  return{it:fx.concat(keep).sort((a,b)=>a.s-b.s||a.e-b.e)}}
async function aiDayPlan(text,date,alt){const A=aiS();AIL=true;AIT0=Date.now();clearInterval(AIW);AIW=setInterval(()=>{if(AIL)aiRender();else{clearInterval(AIW);AIW=null}},1000);aiRender();
  try{const d=await fnAI({action:'dayplan',ctx:JSON.stringify(dpCtx(date,text,alt))}),j=parseJson(d.text);if(!j)throw new Error('AI tushunarli reja bermadi. Qayta urinib ko‘ring.');
    const P=dpBuild(date,j);if(!P.it.length)throw new Error('AI reja tuza olmadi. Qayta urinib ko‘ring.');
    AIL=false;A.chat.push({r:'plan',date,it:P.it,tip:String(j.tip||'').slice(0,160),text});aiRender()}
  catch(e){AIL=false;A.chat.push({r:'err',t:e.message});aiRender()}
  qsave()}
function dpCard(m,i){const rows=m.it.map(x=>`<div class="dpr${x.fx?' fx':''}"><span class="dpt">${hm(x.s)}–${hm(x.e)}</span><div><b>${esc(x.t)}</b>${x.n?`<div class="mu">${esc(x.n)}</div>`:''}</div></div>`).join(''),had=(S.ap||{})[m.date];
  return `<div class="dpc"><b>📅 ${dpWord(m.date)} uchun reja · ${DAYS[new Date(m.date+'T12:00').getDay()]}</b>${rows}${m.tip?`<p class="mu" style="margin:8px 0 0">${esc(m.tip)}</p>`:''}${m.saved?'<p class="mu" style="margin:8px 0 0">✓ Rejaga qo‘shildi. Bugun ekranida ko‘rinadi.</p>':`<div class="in" style="margin-top:8px"><button class="btn" onclick="dpSave(${i})">✅ Rejaga qo‘sh</button><button class="btn s" onclick="dpAgain(${i})">↻ Boshqacha tuz</button></div>${had?'<p class="mu" style="margin:6px 0 0;font-size:12px">Bu kunda reja bor: almashtiriladi.</p>':''}`}</div>`}
function dpSave(i){const m=aiS().chat[i];if(!m||m.r!=='plan')return;S.ap=S.ap||{};S.ap[m.date]={it:m.it.map(x=>({...x})),tip:m.tip||'',at:Date.now()};
  Object.keys(S.ap).forEach(d=>{if(d<dAgo(14))delete S.ap[d]});m.saved=1;save();toast('Reja saqlandi');aiRender()}
function dpAgain(i){const ch=aiS().chat,m=ch[i];if(!m||m.r!=='plan'||AIL)return;ch.splice(i,1);aiDayPlan(m.text,m.date,true)}
function apT(k,id){const P=(S.ap||{})[k];if(!P||k>dk())return;const x=P.it.find(y=>y.id===id);if(!x)return;if(x.fx){const D=S.done[k]=S.done[k]||{};D[id]=!D[id]}else x.x=!x.x;save()}
function apDel(k){if(!confirm('Shu kunning AI rejasi o‘chirilsinmi? (Doimiy jadvaling o‘zgarmaydi.)'))return;delete S.ap[k];save()}
function apCard(k,fu){const P=(S.ap||{})[k];
  if(!P){if(k===dk()&&aiOk()&&new Date().getHours()>=19&&!(S.ap||{})[dAgo(-1)])return `<div class="goal" style="margin-top:12px;border-left:4px solid var(--ac)"><b style="font:700 17px Fraunces,serif">📅 Ertangi kunni rejala</b><p class="mu" style="margin:6px 0 8px">AI doimiy jadvaling va muddatlaringga qarab ertangi kun uchun aniq reja tuzadi.</p><button class="btn" onclick="aiOpen('Ertangi kunni rejalashtir')">✨ Reja tuzish</button></div>`;return ''}
  const now=new Date(),cur=now.getHours()*60+now.getMinutes(),D=S.done[k]||{},isT=k===dk();
  const rows=P.it.map(x=>{const dn=x.fx?!!D[x.id]:!!x.x,on=isT&&cur>=x.s&&cur<x.e&&!dn;return `<div class="apr${dn?' done':''}${on?' now':''}"><button class="ck" ${fu?'disabled':''} onclick="apT('${k}','${x.id}')" aria-label="Belgilash">${dn?'✓':''}</button><span class="dpt">${hm(x.s)}–${hm(x.e)}</span><div><b>${esc(x.t)}</b>${x.n?`<div class="mu">${esc(x.n)}</div>`:''}</div></div>`}).join('');
  const done=P.it.filter(x=>x.fx?!!D[x.id]:!!x.x).length;
  return `<div class="goal apc" style="margin-top:12px;border-left:4px solid var(--ac)"><div class="h"><b style="font:700 18px Fraunces,serif">📅 ${dpWord(k)} rejasi</b><span class="mu">${done}/${P.it.length}</span></div>${rows}${P.tip?`<p class="mu" style="margin:8px 0 0">${esc(P.tip)}</p>`:''}<div class="in" style="margin-top:8px">${aiOk()?`<button class="btn s" onclick="aiOpen('${k===dk()?'Bugungi':'Ertangi'} kunni qayta rejalashtir')">↻ Qayta tuz</button>`:''}<button class="btn s" onclick="apDel('${k}')">O‘chirish</button></div></div>`}
