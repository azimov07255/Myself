// ---- Isolation ----
function isoM(){S.iso.m[dk()]=+V('im2')||0;save()}
function isoAdd(win){const t=V('it');if(!t)return;S.iso.log.push({id:Date.now(),d:dk(),t,w:win});save()}
function iso(){
  const I=S.iso,k=dk(),m=I.m[k]||0;let best=0,run=0;
  for(let i=119;i>=0;i--){if((S.rules[dAgo(i)]||{}).ig){run++;best=Math.max(best,run)}else run=0}
  let cur=0;for(let i=0;i<120;i++){if((S.rules[dAgo(i)]||{}).ig)cur++;else if(i>0)break}
  const bars=[...Array(14)].map((_,i)=>{const kk=dAgo(13-i),v=I.m[kk]||0;return `<div style="flex:1;text-align:center"><div style="height:70px;display:flex;align-items:flex-end"><div style="width:100%;height:${Math.max(3,Math.min(70,v/Math.max(I.lim*2,1)*70))}px;background:${v>I.lim?'var(--bad)':'var(--ac)'};opacity:.85;border-radius:4px"></div></div><span class="mu" style="font-size:11px">${kk.slice(8)}</span></div>`}).join('');
  const lg=I.log.slice().reverse().slice(0,8).map(x=>`<div class="row"><span class="t">${esc(x.t)}<br><span class="mu">${x.d.slice(8)}.${x.d.slice(5,7)}, ${x.w?'yengdim':'yutqazdim'}</span></span><button class="x" onclick="lst('iso.log',${x.id})">×</button></div>`).join('');
  const wins=I.log.filter(x=>x.w).length;
  return `<section class="hero"><p class="lab">Isolation</p><h1 style="font-size:40px">${cur} kun</h1><p class="mu">Ketma-ket Instagramsiz kunlar. Eng uzun seriya: ${Math.max(best,cur)} kun. Chalg‘ishni yengganlar: ${wins} marta.</p><p class="mu" style="margin-top:6px">Kunni belgilash uchun Bugun ekranidagi “Instagramsiz kun” qoidasidan foydalan.</p></section>
  <h2>Bugungi ekran vaqti</h2><div class="bar"><i style="width:${Math.min(100,m/Math.max(I.lim,1)*100)}%;${m>I.lim?'background:var(--bad)':''}"></i></div><p class="mu">${m} / ${I.lim} daqiqa${m>I.lim?'. Limitdan oshdi.':''}</p>
  <div class="in"><input id="im2" type="number" placeholder="Bugun necha daqiqa?" value="${m||''}"><button class="btn" onclick="isoM()">Yoz</button></div><div class="in"><input type="number" value="${I.lim}" onchange="S.iso.lim=+this.value||60;save()"><span class="mu" style="align-self:center">kunlik limit, daqiqa</span></div>
  <h2>So‘nggi 14 kun</h2><p class="mu" style="margin:0 0 8px">7 kunlik o‘rtacha: ${Math.round([...Array(7)].reduce((a,_,i)=>a+(I.m[dAgo(i)]||0),0)/7)} daqiqa</p><div style="display:flex;gap:3px">${bars}</div>
  ${urgeCard()}<h2>Chalg‘ish jurnali</h2><p class="mu" style="margin:0 0 8px">Kirgingiz kelganda sababini yoz va natijani belgila.</p><div class="in"><input id="it" placeholder="Nega kirgim keldi?"></div><div class="in"><button class="btn" style="flex:1" onclick="isoAdd(1)">Yengdim</button><button class="btn s" style="flex:1" onclick="isoAdd(0)">Yutqazdim</button></div>${lg}`}

// ---- Brend, Telegram, tanishuv, rejimlar ----
const OWNER_TG='';   // Telegram username, @ belgisiz (masalan: azimov_uz). Bo‘sh qolsa, tugma chiqmaydi.
const brand=()=>'<p class="mu" style="margin:0 0 10px;letter-spacing:.2em;font-size:12px">BY AZIMOV</p>';
function tgBtn(label){if(!OWNER_TG)return '';let em='';try{em=(localStorage.getItem('trk_em')||'').replace('@trk.app','')}catch(e){}
  return `<a class="big" style="display:block;text-align:center;text-decoration:none;margin-top:12px" href="https://t.me/${OWNER_TG}?text=${encodeURIComponent('Assalomu alaykum! Kunlik tizim obunasini olmoqchiman. Login: '+em)}">${label}</a>`}

const mkb=(id,t,s,e,n)=>({id,t,s,e,n:n||'',d:[0,1,2,3,4,5,6]});
const PRE={
 talaba:['Talaba kuni',[mkb('uyg','Uyg‘onish',M(5,30),M(6),'Tur, tahorat, namoz.'),mkb('qur','Qur‘on',M(6),M(7),'Yodlash yoki takror.'),mkb('yol','Yo‘l',M(7,30),M(8,30)),mkb('dars','Dars',M(8,30),M(14)),mkb('ovq','Ovqat va dam',M(14),M(15)),mkb('oq','O‘qish va til o‘rganish',M(15),M(17)),mkb('spo','Sport',M(17,30),M(19)),mkb('tak','Takror va uy vazifasi',M(19,30),M(21)),mkb('uyqu1','Uxlash',M(22,30),M(29,30),'Telefon chetga.')]],
 ish:['Ish kuni',[mkb('uyg','Uyg‘onish',M(5),M(6),'Tur, tahorat, namoz.'),mkb('qur','Qur‘on',M(6),M(7)),mkb('ish','Ish',M(9),M(17)),mkb('yol','Yo‘l va ovqat',M(17),M(18)),mkb('oq','O‘qish va til o‘rganish',M(19),M(20,30)),mkb('spo','Sport',M(20,30),M(21,30)),mkb('uyqu1','Uxlash',M(23),M(29),'Telefon chetga.')]],
 imtihon:['Imtihon haftasi',[mkb('uyg','Uyg‘onish',M(5),M(6)),mkb('qur','Qur‘on',M(6),M(7)),mkb('t1','Tayyorgarlik 1',M(8),M(12),'Eng qiyin mavzu.'),mkb('ovq','Ovqat va dam',M(12),M(13)),mkb('t2','Tayyorgarlik 2',M(13),M(17)),mkb('spo','Yengil sport',M(17),M(18,30)),mkb('tak','Takror va test',M(19),M(21,30)),mkb('uyqu1','Uxlash',M(22),M(29),'To‘liq uxla.')]],
 dam:['Dam olish kuni',[mkb('uyg','Uyg‘onish',M(6),M(7)),mkb('qur','Qur‘on',M(7),M(8,30)),mkb('spo','Sport',M(9),M(10,30)),mkb('oila','Oila va do‘stlar',M(11),M(15)),mkb('kit','Kitob o‘qish',M(16),M(17,30)),mkb('hft','Haftani rejalash',M(20),M(20,30)),mkb('uyqu1','Uxlash',M(23),M(30))]],
 erkin:['Erkin kun',[mkb('uyg','Uyg‘onish',M(6),M(7)),mkb('qur','Qur‘on',M(7),M(8)),mkb('ish','Asosiy ish',M(9),M(13)),mkb('dam','Ovqat va dam',M(13),M(14)),mkb('rv','Rivojlanish',M(15),M(17)),mkb('spo','Sport',M(18),M(19)),mkb('uyqu1','Uxlash',M(23),M(30))]]
};
const OBG_ALL=['Hofizi Qur‘on bo‘lish','IELTS 8–9 ball','O‘qituvchi bo‘lib ishlash','Prava olish','Zalda yaxshi tana qurish','Pul jamg‘arish','Kitob o‘qish','Universitetni a‘lo tugatish'];
function obGo(n){OB=n;render()}
function obG(i){const t=OBG_ALL[i],j=OBG.indexOf(t);j<0?OBG.push(t):OBG.splice(j,1);render()}
function obAdd(){const c=OBC.trim();if(c&&!OBG.includes(c))OBG.push(c);OBC='';render()}
function obFin(){S.name=OBN.trim();S.goals=OBG.map(t=>({t,why:'',dl:'',ms:[],p:0}));S.bl=PRE[OBP][1].map(b=>({...b}));S.md={cur:PRE[OBP][0],sets:{}};S.ob=1;S.sg=0;save();sgMig()}
function obView(){
  const head=`<div class="auth" style="margin-top:6vh"><img src="favicon.svg" width="56" height="56" alt="" style="border-radius:14px;margin-bottom:12px"><h1 style="font-size:30px">Xush kelibsiz</h1>${brand()}<p class="mu">${OB} / 3 qadam</p>`;
  if(OB===1)return head+`<h2 style="margin-top:6px">Ismingiz nima?</h2><div class="in"><input placeholder="Ism" value="${esc(OBN)}" oninput="OBN=this.value"></div><button class="big" onclick="obGo(2)">Davom etish</button></div>`;
  if(OB===2)return head+`<h2 style="margin-top:6px">Maqsadlaringizni tanlang</h2><p class="mu">Bir nechtasini tanlang, keyin o‘zgartirish mumkin.</p><div class="chips">${OBG_ALL.map((t,i)=>`<button class="${OBG.includes(t)?'on':''}" onclick="obG(${i})">${t}</button>`).join('')}${OBG.filter(t=>!OBG_ALL.includes(t)).map(t=>`<button class="on" onclick="OBG.splice(OBG.indexOf('${esc(t).replace(/'/g,'')}'),1);render()">${esc(t)}</button>`).join('')}</div><div class="in" style="margin-top:8px"><input placeholder="O‘zingning maqsading" value="${esc(OBC)}" oninput="OBC=this.value"><button class="btn" onclick="obAdd()">+</button></div><div class="in"><button class="btn s" onclick="obGo(1)">Orqaga</button><button class="btn" style="flex:1" onclick="obGo(3)">Davom etish</button></div></div>`;
  return head+`<h2 style="margin-top:6px">Kun jadvalingiz qanday?</h2><p class="mu">Tayyor jadvalni tanlang. Keyin istalgancha o‘zgartira olasiz.</p>${Object.keys(PRE).filter(k=>k!=='ramazon').map(k=>`<button class="row ${OBP===k?'done':''}" onclick="OBP='${k}';render()"><span class="ck">${OBP===k?'✓':''}</span><span class="t">${PRE[k][0]}<br><span class="mu">${PRE[k][1].filter(b=>!b.id.startsWith('uyqu')).length} ta reja</span></span></button>`).join('')}<div class="in" style="margin-top:10px"><button class="btn s" onclick="obGo(2)">Orqaga</button><button class="btn" style="flex:1" onclick="obFin()">Boshlash</button></div></div>`;
}

// ---- Reja rejimlari ----
const mdNames=()=>[...new Set([S.md.cur,...Object.keys(S.md.sets)])];
function mdSave(){S.md.sets[S.md.cur]=bl().map(b=>({...b}))}
function mdSw(n){const m=S.md;if(!m.sets[n]||n===m.cur)return;mdSave();S.bl=m.sets[n].map(b=>({...b}));m.cur=n;save()}
function mdNew(base){const n=(prompt('Rejim nomi (masalan: Dam olish kuni):',base?PRE[base][0]:'')||'').trim().replace(/['"\\<>]/g,'');if(!n)return;const m=S.md;mdSave();m.sets[n]=(base?PRE[base][1]:bl()).map(b=>({...b}));S.bl=m.sets[n].map(b=>({...b}));m.cur=n;save()}
function mdDel(n){const m=S.md;if(n===m.cur||mdNames().length<2)return;if(confirm('“'+n+'” rejimi o‘chirilsinmi?')){delete m.sets[n];save()}}
function mdBar(){const n=mdNames();return n.length>1?`<div class="chips" style="margin-top:8px">${n.map(x=>`<button class="${x===S.md.cur?'on':''}" onclick="mdSw('${x}')">${esc(x)}</button>`).join('')}</div>`:''}
function modesCard(){
  const n=mdNames();
  return `<h2>Reja rejimlari</h2><p class="mu">Kuning turiga qarab jadvalni almashtir. Hozirgi rejim: <b style="color:var(--tx)">${esc(S.md.cur)}</b>. Bugun ekranida rejim tugmalari chiqadi.</p>
  ${n.map(x=>`<div class="row ${x===S.md.cur?'now':''}"><span class="t">${esc(x)}</span>${x===S.md.cur?'<span class="tm">faol</span>':`<button class="btn s" style="padding:6px 10px" onclick="mdSw('${x}')">Almashtir</button><button class="x" onclick="mdDel('${x}')">×</button>`}</div>`).join('')}
  <p class="mu" style="margin:10px 0 6px">Yangi rejim qo‘shish:</p><div class="chips">${Object.keys(PRE).map(k=>`<button onclick="mdNew('${k}')">${PRE[k][0]}</button>`).join('')}<button onclick="mdNew()">Hozirgidan nusxa</button></div>`}

