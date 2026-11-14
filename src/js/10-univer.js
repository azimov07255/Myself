// ---- UNIVER: dars jadvali, fanlar, baho va davomat, topshiriq, imtihon ----
const UPAL=['#46c4b2','#e2b857','#d96f8f','#6f9fd8','#b27ad6','#e8855a','#7fb069','#c9a227'],UKIND=['Ma‘ruza','Amaliy','Laboratoriya','Seminar'];
let UV='b',UD=new Date().getDay();
const uSubj=id=>S.un.subj.find(x=>x.id===id),uCol=n=>{const s=S.un.subj.find(x=>x.n===n);return s?s.col:'var(--ln)'};
function uSub(id){return S.un.subj.length?`<select id="${id}" style="flex:1;min-width:0">${S.un.subj.map(s=>`<option value="${s.id}">${esc(s.n)}</option>`).join('')}</select>`:`<input id="${id}" placeholder="Fan nomi" style="flex:1;min-width:0">`}
const uName=v=>{const s=uSubj(v);return s?s.n:String(v||'').trim()};
function sbAdd(){const n=V('sbn');if(!n)return alert('Fan nomini yozing.');S.un.subj.push({id:'s'+Date.now(),n,cr:+V('sbc')||0,t:V('sbt'),lim:Math.round(+V('sbl'))||0,col:UPAL[S.un.subj.length%UPAL.length]});save()}
function sbDel(id){if(!confirm('Fan va uning darslari, baholari o‘chirilsinmi?'))return;S.un.subj=S.un.subj.filter(x=>x.id!==id);Object.keys(S.un.tt).forEach(d=>{S.un.tt[d]=S.un.tt[d].filter(x=>x.sid!==id)});delete S.un.gr[id];delete S.un.ab[id];save()}
function ttAdd(){const sid=V('tts'),s=V('ttst'),e=V('ttse');if(!uSubj(sid))return alert('Avval Fanlar bo‘limida fan qo‘shing.');if(!s||!e||t2m(e)<=t2m(s))return alert('Boshlanish va tugash vaqtini to‘g‘ri yozing.');
  const L=S.un.tt[UD]=S.un.tt[UD]||[];L.push({id:Date.now(),sid,s,e,r:V('ttr'),k:V('ttk')||UKIND[0]});L.sort((a,b)=>t2m(a.s)-t2m(b.s));save()}
function ttDel(d,id){S.un.tt[d]=(S.un.tt[d]||[]).filter(x=>x.id!==id);save()}
function grAdd(sid){const n=V('grn'+sid),sc=parseFloat(V('grs'+sid)),mx=parseFloat(V('grm'+sid))||100;if(!(sc>=0)||sc>mx)return alert('Ballni to‘g‘ri yozing.');(S.un.gr[sid]=S.un.gr[sid]||[]).push({id:Date.now(),n:n||'Baho',sc,mx});save()}
function grDel(sid,id){S.un.gr[sid]=(S.un.gr[sid]||[]).filter(x=>x.id!==id);save()}
function abAdd(sid,d){S.un.ab[sid]=Math.max(0,(S.un.ab[sid]||0)+d);save()}
function uAdd(){const t=V('ut');if(!t)return;S.un.tasks.push({id:Date.now(),t,s:uName(V('us')),due:V('ud'),x:0,imp:V('up')==='1'?1:0});save()}
function uEx(){const s=uName(V('ue')),d=V('ued');if(!s||!d)return alert('Fan va sanani yozing.');S.un.exams.push({id:Date.now(),s,d,tm:V('uet'),r:V('uer'),p:0});save()}
function uT(id){const t=S.un.tasks.find(x=>x.id===id);t.x=t.x?0:1;save()}
function exPrep(id,v){const e=S.un.exams.find(x=>x.id===id);if(e){e.p=+v||0;qsave()}}
const uAvg=sid=>{const g=S.un.gr[sid]||[],m=g.reduce((a,x)=>a+x.mx,0);return m?Math.round(g.reduce((a,x)=>a+x.sc,0)/m*100):null};
const uLessons=d=>(S.un.tt[d]||[]).slice().sort((a,b)=>t2m(a.s)-t2m(b.s));

// ---- Univer: tahrirlash ----
let UED='';
const uEdT=k=>{UED=UED===k?'':k;render()};
function sbEd(id,f,v){const s=uSubj(id);if(!s)return;
  if(f==='n'){const nn=String(v).trim();if(!nn)return;S.un.tasks.forEach(t=>{if(t.s===s.n)t.s=nn});S.un.exams.forEach(e=>{if(e.s===s.n)e.s=nn});s.n=nn}
  else if(f==='ab')S.un.ab[id]=Math.max(0,Math.round(+v)||0);
  else if(f==='cr'||f==='lim')s[f]=Math.max(0,Math.round(+v)||0);
  else s[f]=String(v);
  save()}
function ttEd(d,id,f,v){const L=(S.un.tt[d]||[]).find(x=>x.id===id);if(!L)return;const old=L[f];L[f]=v;
  if(!L.s||!L.e||t2m(L.e)<=t2m(L.s)){L[f]=old;alert('Tugash vaqti boshlanishdan keyin bo‘lsin.');render();return}
  S.un.tt[d].sort((a,b)=>t2m(a.s)-t2m(b.s));save()}
function tkEd(id,f,v){const t=S.un.tasks.find(x=>x.id===id);if(!t)return;if(f==='imp')t.imp=+v?1:0;else t[f]=String(v).trim();save()}
function exEd(id,f,v){const e=S.un.exams.find(x=>x.id===id);if(!e)return;if(f==='d'&&!v)return;e[f]=String(v).trim();save()}
const uNameSel=(cur,cb)=>{const names=S.un.subj.map(s=>s.n);if(cur&&!names.includes(cur))names.unshift(cur);return names.length?`<select style="width:100%;margin-top:4px" onchange="${cb}(this.value)">${names.map(n=>`<option ${n===cur?'selected':''}>${esc(n)}</option>`).join('')}</select>`:`<input value="${esc(cur||'')}" onchange="${cb}(this.value)" style="width:100%;margin-top:4px">`};
function uSubEd(s){const ab=S.un.ab[s.id]||0;
  return `<div class="un-ed"><label><span class="mu">Fan nomi</span><input value="${esc(s.n)}" onchange="sbEd('${s.id}','n',this.value)"></label>
  <label><span class="mu">O‘qituvchi</span><input value="${esc(s.t||'')}" onchange="sbEd('${s.id}','t',this.value)"></label>
  <div class="fg"><label><span class="mu">Kredit</span><input type="number" inputmode="numeric" value="${s.cr||''}" onchange="sbEd('${s.id}','cr',this.value)"></label><label><span class="mu">Qoldirish limiti</span><input type="number" inputmode="numeric" value="${s.lim||''}" onchange="sbEd('${s.id}','lim',this.value)"></label></div>
  <label><span class="mu">Qoldirilgan darslar soni</span><input type="number" inputmode="numeric" value="${ab}" onchange="sbEd('${s.id}','ab',this.value)"></label>
  <div class="mu" style="font-size:12px;margin-top:8px">Rang</div><div class="ucs">${UPAL.map(c=>`<button class="ucb" style="background:${c}" onclick="sbEd('${s.id}','col','${c}')">${s.col===c?'✓':''}</button>`).join('')}</div>
  <button class="btn" style="width:100%;margin-top:10px" onclick="UED='';render()">Tayyor</button></div>`}
function uLesEd(d,L){return `<div class="un-ed"><label><span class="mu">Fan</span><select style="width:100%;margin-top:4px" onchange="ttEd(${d},${L.id},'sid',this.value)">${S.un.subj.map(s=>`<option value="${s.id}" ${s.id===L.sid?'selected':''}>${esc(s.n)}</option>`).join('')}</select></label>
  <div class="fg1"><label><span class="mu">Boshlanishi</span><input type="time" value="${L.s}" onchange="ttEd(${d},${L.id},'s',this.value)"></label><label><span class="mu">Tugashi</span><input type="time" value="${L.e}" onchange="ttEd(${d},${L.id},'e',this.value)"></label></div>
  <div class="in"><select style="flex:1;min-width:0" onchange="ttEd(${d},${L.id},'k',this.value)">${UKIND.map(k=>`<option ${k===L.k?'selected':''}>${k}</option>`).join('')}</select><input value="${esc(L.r||'')}" placeholder="Xona" style="flex:1;min-width:0" onchange="ttEd(${d},${L.id},'r',this.value)"></div>
  <button class="btn" style="width:100%" onclick="UED='';render()">Tayyor</button></div>`}
function uTaskEd(t){return `<div class="un-ed"><label><span class="mu">Topshiriq</span><input value="${esc(t.t)}" onchange="tkEd(${t.id},'t',this.value)"></label><label><span class="mu">Fan</span>${uNameSel(t.s,"tkEd.bind(null,"+t.id+",'s')")}</label>
  <div class="fg1"><label><span class="mu">Muddati</span><input type="date" value="${t.due||''}" onchange="tkEd(${t.id},'due',this.value)"></label><label><span class="mu">Muhimligi</span><select style="width:100%;margin-top:4px" onchange="tkEd(${t.id},'imp',this.value)"><option value="0">Oddiy</option><option value="1" ${t.imp?'selected':''}>⭐ Muhim</option></select></label></div>
  <button class="btn" style="width:100%" onclick="UED='';render()">Tayyor</button></div>`}
function uExEd(e){return `<div class="un-ed"><label><span class="mu">Fan</span>${uNameSel(e.s,"exEd.bind(null,"+e.id+",'s')")}</label>
  <div class="fg1"><label><span class="mu">Sana</span><input type="date" value="${e.d}" onchange="exEd(${e.id},'d',this.value)"></label><label><span class="mu">Vaqt</span><input type="time" value="${e.tm||''}" onchange="exEd(${e.id},'tm',this.value)"></label></div>
  <label><span class="mu">Xona</span><input value="${esc(e.r||'')}" onchange="exEd(${e.id},'r',this.value)"></label><button class="btn" style="width:100%;margin-top:8px" onclick="UED='';render()">Tayyor</button></div>`}
function uLRow(L,del){const s=uSubj(L.sid)||{n:'Fan',col:'var(--ln)'};
  return `<div class="un-l" style="--c:${s.col}"><div class="un-t"><b>${L.s}</b><span class="mu">${L.e}</span></div><div class="un-b"><b>${esc(s.n)}</b><div class="mu" style="font-size:12px">${esc(L.k||'')}${L.r?' · '+esc(L.r):''}</div></div>${del!==undefined?`<button class="x" style="font-size:15px" onclick="uEdT('les:${L.id}')">✎</button><button class="x" onclick="ttDel(${del},${L.id})">×</button>`:''}</div>${del!==undefined&&UED==='les:'+L.id?uLesEd(del,L):''}`}
function uniCard(){const L=uLessons(new Date().getDay());if(!L.length)return '';const n=new Date(),m=n.getHours()*60+n.getMinutes();
  const cur=L.find(x=>m>=t2m(x.s)&&m<t2m(x.e)),nxt=L.find(x=>t2m(x.s)>m);
  const msg=cur?`Hozir: ${esc(uName(cur.sid))} (${cur.e} gacha)`:nxt?`Keyingi: ${esc(uName(nxt.sid))}, ${nxt.s} da`:'Bugungi darslar tugadi';
  return `<button class="row" style="margin-top:12px;border-left-color:var(--ac)" onclick="EV='u';UV='b';go('e')"><span class="t"><b>🎓 Bugun ${L.length} ta dars</b><br><span class="mu">${msg}</span></span></button>`}
function uView(){
  const u=S.un,T0=dk(),now=new Date(),m=now.getHours()*60+now.getMinutes();
  if(UV==='b'){
    const L=uLessons(now.getDay()),cur=L.find(x=>m>=t2m(x.s)&&m<t2m(x.e)),nxt=L.find(x=>t2m(x.s)>m);
    const open=u.tasks.filter(t=>!t.x),soon=open.filter(t=>t.due&&dl(t.due)<=2).sort((a,b)=>a.due>b.due?1:-1),ex=u.exams.filter(e=>dl(e.d)>=0).sort((a,b)=>a.d>b.d?1:-1)[0];
    const lines=L.map(x=>{const s=uSubj(x.sid)||{n:'Fan',col:'var(--ln)'},on=cur&&cur.id===x.id,past=m>=t2m(x.e);return `<div class="un-l ${on?'now':''}" style="--c:${s.col};${past?'opacity:.5':''}"><div class="un-t"><b>${x.s}</b><span class="mu">${x.e}</span></div><div class="un-b"><b>${esc(s.n)}</b><div class="mu" style="font-size:12px">${esc(x.k||'')}${x.r?' · '+esc(x.r):''}</div></div>${on?'<span class="chip-on">hozir</span>':nxt&&nxt.id===x.id?`<span class="mu" style="font-size:12px">${fmt(t2m(x.s)-m).trim()} dan keyin</span>`:''}</div>`}).join('');
    return `<section class="hero"><p class="lab">${DAYS[now.getDay()]}</p><h1 style="font-size:30px">${L.length?L.length+' ta dars':'Bugun dars yo‘q'}</h1><p class="mu">${cur?'Hozir: '+esc(uName(cur.sid)):nxt?'Keyingi: '+esc(uName(nxt.sid))+', '+nxt.s:L.length?'Bugungi darslar tugadi':'Dam olish yoki mustaqil tayyorgarlik kuni.'}</p></section>
    <div class="st"><div><b>${open.length}</b>topshiriq</div><div><b>${soon.length}</b>tez orada</div><div><b>${ex?dl(ex.d):'—'}</b>${ex?'kun: imtihon':'imtihon yo‘q'}</div></div>
    ${lines?`<h2>Bugungi darslar</h2>${lines}`:''}
    ${soon.length?`<h2>Muddati yaqin</h2>${soon.map(t=>`<div class="row"><span class="ck" onclick="uT(${t.id})"></span><span class="t" onclick="uT(${t.id})">${esc(t.t)}<br><span class="mu" style="color:var(--bad)">${t.s?esc(t.s)+', ':''}${dlTxt(dl(t.due))}</span></span></div>`).join('')}`:''}
    ${!u.subj.length?'<div class="bn wr">Boshlash uchun <b>Fanlar</b> bo‘limida fanlaringni qo‘sh, keyin <b>Jadval</b>da darslarni yoz.</div>':''}`}
  if(UV==='j'){
    const strip=[1,2,3,4,5,6,0].map(d=>`<button class="${UD===d?'on':''}" onclick="UD=${d};render()"><span style="display:block;font-size:11px;font-weight:600">${DAYS[d].slice(0,2)}${d===now.getDay()?' •':''}</span><b style="font-size:16px">${uLessons(d).length||'·'}</b></button>`).join('');
    const L=uLessons(UD);
    return `<div class="wkp">${strip}</div><h2>${DAYS[UD]}</h2>${L.map(x=>uLRow(x,UD)).join('')||'<p class="mu">Bu kunga dars qo‘yilmagan.</p>'}
    <details class="goal" style="margin-top:10px"${L.length?'':' open'}><summary style="font-weight:600">+ Dars qo‘shish</summary><div style="margin-top:10px"><div class="in">${uSub('tts')}</div>
    <div class="fg1"><label><span class="mu">Boshlanishi</span><input id="ttst" type="time" value="09:00"></label><label><span class="mu">Tugashi</span><input id="ttse" type="time" value="10:20"></label></div>
    <div class="in"><select id="ttk" style="flex:1;min-width:0">${UKIND.map(k=>`<option>${k}</option>`).join('')}</select><input id="ttr" placeholder="Xona" style="flex:1;min-width:0"></div><button class="big" style="margin:4px 0 0" onclick="ttAdd()">Darsni qo‘shish</button></div></details>`}
  if(UV==='f'){
    const cards=u.subj.map(s=>{const a=uAvg(s.id),ab=u.ab[s.id]||0,lim=s.lim||0,pc=lim?Math.min(100,ab/lim*100):0,bad=lim&&ab>=lim*0.8,g=(u.gr[s.id]||[]);
      return `<div class="goal" style="border-left:5px solid ${s.col}"><div class="h" style="align-items:flex-start"><div style="min-width:0"><b style="font-size:17px">${esc(s.n)}</b><div class="mu" style="font-size:12px">${s.t?esc(s.t):'o‘qituvchi yozilmagan'}${s.cr?' · '+s.cr+' kredit':''}</div></div><span><button class="x" style="font-size:16px" onclick="uEdT('sub:${s.id}')">✎</button><button class="x" onclick="sbDel('${s.id}')">×</button></span></div>${UED==='sub:'+s.id?uSubEd(s):''}
      <div class="un-m"><div><span class="mu">O‘rtacha ball</span><b>${a===null?'—':a+'%'}</b></div><div><span class="mu">Qoldirilgan dars</span><b style="${bad?'color:var(--bad)':''}">${ab}${lim?' / '+lim:''}</b></div></div>
      ${a!==null?`<div class="bar"><i style="width:${a}%;background:${s.col}"></i></div>`:''}
      <div class="in" style="margin:10px 0 0;align-items:center"><span class="mu" style="flex:1">Davomat${lim?'':' (limit qo‘yilmagan)'}</span><button class="btn s" style="padding:6px 14px" onclick="abAdd('${s.id}',-1)">−</button><button class="btn" style="padding:6px 14px" onclick="abAdd('${s.id}',1)">+ qoldirdim</button></div>
      ${lim?`<div class="bar" style="margin-top:6px"><i style="width:${pc}%;background:${bad?'var(--bad)':'var(--ac)'}"></i></div>${bad?`<p style="color:var(--bad);margin:6px 0 0;font-size:13px">⚠️ Limitga yaqinlashding: ${lim-ab>0?(lim-ab)+' ta qoldi':'limit tugadi'}.</p>`:''}`:''}
      ${g.length?`<div class="chips" style="margin-top:10px">${g.map(x=>`<button onclick="grDel('${s.id}',${x.id})" title="O‘chirish">${esc(x.n)}: ${x.sc}/${x.mx} ×</button>`).join('')}</div>`:''}
      <details style="margin-top:8px"><summary class="mu">+ Baho qo‘shish</summary><div class="in" style="margin-top:8px"><input id="grn${s.id}" placeholder="Nomi (Nazorat 1)" style="flex:2;min-width:0"><input id="grs${s.id}" type="number" inputmode="decimal" placeholder="Ball" style="flex:1;min-width:0"><input id="grm${s.id}" type="number" inputmode="decimal" placeholder="100" style="flex:1;min-width:0"></div><button class="btn" style="width:100%" onclick="grAdd('${s.id}')">Qo‘shish</button></details></div>`}).join('');
    return `${cards||'<p class="mu">Hali fan yo‘q. Quyida qo‘sh.</p>'}
    <details class="goal"${u.subj.length?'':' open'}><summary style="font-weight:600">+ Fan qo‘shish</summary><div style="margin-top:10px"><div class="in"><input id="sbn" placeholder="Fan nomi, masalan: Matematika"></div><div class="in"><input id="sbt" placeholder="O‘qituvchi (ixtiyoriy)"></div>
    <div class="fg"><label><span class="mu">Kredit</span><input id="sbc" type="number" inputmode="numeric" placeholder="4"></label><label><span class="mu">Dars qoldirish limiti</span><input id="sbl" type="number" inputmode="numeric" placeholder="10"></label></div><button class="big" style="margin:4px 0 0" onclick="sbAdd()">Fanni qo‘shish</button></div></details>`}
  if(UV==='t'){
    const T=u.tasks.slice().sort((a,b)=>(a.x-b.x)||((a.due||'9')>(b.due||'9')?1:-1)),row=t=>{const n=t.due?dl(t.due):null,hot=!t.x&&n!==null&&n<=1;return `<div class="row ${t.x?'done':''}" style="border-left:4px solid ${uCol(t.s)}"><span class="ck" onclick="uT(${t.id})">${t.x?'✓':''}</span><span class="t" onclick="uT(${t.id})">${t.imp?'⭐ ':''}${esc(t.t)}<br><span class="mu" style="${hot?'color:var(--bad)':''}">${t.s?esc(t.s)+', ':''}${n===null?'muddatsiz':dlTxt(n)}</span></span><span><button class="x" style="font-size:15px" onclick="uEdT('tsk:${t.id}')">✎</button><button class="x" onclick="lst('un.tasks',${t.id})">×</button></span></div>${UED==='tsk:'+t.id?uTaskEd(t):''}`};
    const od=T.filter(t=>!t.x&&t.due&&dl(t.due)<0),td=T.filter(t=>!t.x&&t.due&&dl(t.due)>=0&&dl(t.due)<=7),lt=T.filter(t=>!t.x&&(!t.due||dl(t.due)>7)),dn=T.filter(t=>t.x);
    const grp=(t,L)=>L.length?`<h2>${t} (${L.length})</h2>${L.map(row).join('')}`:'';
    return `<div class="goal"><div class="in" style="margin:0 0 8px">${uSub('us')}</div><div class="in"><input id="ut" placeholder="Topshiriq" style="flex:1;min-width:0"></div><div class="fg1"><label><span class="mu">Muddati</span><input id="ud" type="date"></label><label><span class="mu">Muhimligi</span><select id="up" style="width:100%;margin-top:4px"><option value="0">Oddiy</option><option value="1">⭐ Muhim</option></select></label></div><button class="big" style="margin:4px 0 0" onclick="uAdd()">Topshiriqni qo‘shish</button></div>
    ${grp('Muddati o‘tgan',od)}${grp('Shu hafta',td)}${grp('Keyinroq',lt)}${grp('Bajarilgan',dn)}${T.length?'':'<p class="mu">Topshiriq yo‘q.</p>'}`}
  const E=u.exams.slice().sort((a,b)=>a.d>b.d?1:-1),up=E.filter(e=>dl(e.d)>=0),pa=E.filter(e=>dl(e.d)<0);
  const card=e=>{const n=dl(e.d),pst=n<0;return `<div class="goal un-ex" style="border-left:5px solid ${uCol(e.s)};${pst?'opacity:.55':''}"><div class="un-cd"><b>${pst?'✓':n}</b><span>${pst?'o‘tdi':n===0?'bugun':'kun'}</span></div><div class="un-b"><b>${esc(e.s)}</b><div class="mu" style="font-size:12px">${e.d.slice(8)}.${e.d.slice(5,7)}${e.tm?', '+e.tm:''}${e.r?' · '+esc(e.r):''}</div>${pst?'':`<div style="display:flex;align-items:center;gap:8px;margin-top:6px"><input type="range" min="0" max="100" step="5" value="${e.p||0}" oninput="this.nextElementSibling.textContent=this.value+'%';exPrep(${e.id},this.value)" style="flex:1;accent-color:var(--ac)"><span class="mu" style="min-width:38px;text-align:right">${e.p||0}%</span></div><div class="mu" style="font-size:11px">tayyorgarlik</div>`}</div><span><button class="x" style="font-size:15px" onclick="uEdT('exm:${e.id}')">✎</button><button class="x" onclick="lst('un.exams',${e.id})">×</button></span></div>${UED==='exm:'+e.id?uExEd(e):''}`};
  return `<div class="goal"><div class="in" style="margin:0 0 8px">${uSub('ue')}</div><div class="fg1"><label><span class="mu">Sana</span><input id="ued" type="date"></label><label><span class="mu">Vaqt</span><input id="uet" type="time"></label></div><div class="in"><input id="uer" placeholder="Xona (ixtiyoriy)"></div><button class="big" style="margin:4px 0 0" onclick="uEx()">Imtihonni qo‘shish</button></div>
  ${up.length?`<h2>Kelayotgan imtihonlar</h2>${up.map(card).join('')}`:'<p class="mu">Kelayotgan imtihon yo‘q.</p>'}${pa.length?`<h2>O‘tgan</h2>${pa.map(card).join('')}`:''}`}
function univer(){
  const seg=[['b','📅 Bugun'],['j','🗓 Jadval'],['f','📘 Fanlar'],['t','✍️ Topshiriq'],['e','🎯 Imtihon']].map(x=>`<button class="${UV===x[0]?'on':''}" onclick="UV='${x[0]}';render()">${x[1]}</button>`).join('');
  return `<p class="mu" style="margin:0">Univer</p><h1 class="gr">Universitet</h1><div class="seg sc" style="margin-top:8px">${seg}</div>${uView()}`}

const PTOP=['Yo‘l belgilari','Chorrahalar','Tezlik','Quvib o‘tish','To‘xtash va to‘xtab turish','Svetofor va ishoralar','Yo‘l chiziqlari','Birinchi yordam','Huquq va javobgarlik','Boshqa'];
function pAdd(){const c=+V('pc'),t=+V('pt');if(!t||c<0||c>t)return;S.pr.tests.push({id:Date.now(),d:dk(),c,t});S.pr.er=S.pr.er||{};PSel.forEach(x=>{S.pr.er[x]=(S.pr.er[x]||0)+1});PSel=[];save()}
function pS(i){S.pr.st[i].x=S.pr.st[i].x?0:1;save()}
function pTop(i){const t=PTOP[i],j=PSel.indexOf(t);j<0?PSel.push(t):PSel.splice(j,1);render()}
function psSim(){if(PSim&&PSim.run){clearInterval(PSim.iv);PSim=null;render();return}
  PSim={run:1,end:Date.now()+25*60000};PSim.iv=setInterval(()=>{const l=Math.max(0,Math.ceil((PSim.end-Date.now())/1000)),e=document.getElementById('ptm');if(e)e.textContent=fmtT(l);if(l<=0){clearInterval(PSim.iv);PSim=null;if(navigator.vibrate)navigator.vibrate([300,100,300]);render()}},500);render()}
function prava(){
  const p=S.pr;p.er=p.er||{};p.pm=p.pm||18;const dn=p.st.filter(x=>x.x).length,ts=p.tests.slice(-10),avg=ts.length?Math.round(ts.reduce((a,x)=>a+x.c/x.t,0)/ts.length*100):0;
  const passN=ts.filter(x=>x.t>=20&&x.c>=p.pm).length,last=p.tests[p.tests.length-1];
  const sp=ts.length>1?`<svg viewBox="0 0 300 60" width="100%" height="60"><polyline fill="none" stroke="var(--ac)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" points="${ts.map((x,i)=>`${i*300/(ts.length-1)},${58-x.c/x.t*54}`).join(' ')}"/></svg>`:'';
  const er=Object.entries(p.er).sort((a,b)=>b[1]-a[1]),mx=Math.max(1,...er.map(x=>x[1]));
  const tl=PSim?Math.max(0,Math.ceil((PSim.end-Date.now())/1000)):1500;
  return `<section class="hero"><p class="lab">Prava</p><h1 style="font-size:34px">${dn} / ${p.st.length} bosqich</h1><div class="bar" style="margin:8px 0"><i style="width:${dn/p.st.length*100}%"></i></div><p class="mu">${p.exam?'Imtihongacha: '+dlTxt(dl(p.exam))+'.':'Imtihon sanasini quyida belgila.'}</p></section>
  <div class="st"><div><b>${avg}%</b>o‘rtacha natija</div><div><b>${passN}/${ts.length}</b>o‘tish balidan yuqori</div><div><b>${p.tests.length}</b>jami test</div></div>
  <h2>Imtihon simulyatori</h2><p class="mu" style="margin:0 0 8px">25 daqiqa ichida testni tugat. Savollarni o‘zing ishlatayotgan test ilovasidan ishla, bu yerda esa vaqt hisobini yurit.</p><div class="tmr" id="ptm">${fmtT(tl)}</div><button class="big ${PSim?'ok':''}" style="margin:0 0 8px" onclick="psSim()">${PSim?'To‘xtatish':'Simulyatorni boshlash'}</button>
  <h2>Natija yozish</h2><div class="in"><input id="pc" type="number" inputmode="numeric" placeholder="To‘g‘ri javob"><input id="pt" type="number" inputmode="numeric" placeholder="Jami savol" value="20"><button class="btn" onclick="pAdd()">Yoz</button></div>
  <p class="mu" style="margin:0 0 6px">Xato qilgan mavzularingni belgila (zaif joylar hisoblanadi):</p><div class="chips">${PTOP.map((t,i)=>`<button class="${PSel.includes(t)?'on':''}" onclick="pTop(${i})">${t}</button>`).join('')}</div>
  <div class="in"><span style="align-self:center;min-width:120px">O‘tish bali</span><input type="number" value="${p.pm}" onchange="S.pr.pm=+this.value||18;save()"></div>
  ${last?`<p class="mu">Oxirgi natija: ${last.c} / ${last.t} (${Math.round(last.c/last.t*100)}%).</p>`:''}${sp}
  ${er.length?`<h2>Zaif mavzular</h2>${er.map(([t,n])=>`<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between"><span>${esc(t)}</span><span class="mu">${n} marta</span></div><div class="bar"><i style="width:${n/mx*100}%;background:var(--bad)"></i></div></div>`).join('')}`:''}
  <h2>Bosqichlar</h2>${p.st.map((x,i)=>`<button class="row ${x.x?'done':''}" onclick="pS(${i})"><span class="ck">${x.x?'✓':''}</span><span class="t">${esc(x.t)}</span></button>`).join('')}
  <div class="in"><input type="date" value="${p.exam}" onchange="S.pr.exam=this.value;save()"><span class="mu" style="align-self:center;white-space:nowrap">imtihon sanasi</span></div>
  <h2>So‘nggi natijalar</h2>${p.tests.slice().reverse().slice(0,8).map(x=>`<div class="row"><span class="t">${x.c} / ${x.t}<br><span class="mu">${x.d.slice(8)}.${x.d.slice(5,7)}</span></span><b>${Math.round(x.c/x.t*100)}%</b><button class="x" onclick="lst('pr.tests',${x.id})">×</button></div>`).join('')}`}

