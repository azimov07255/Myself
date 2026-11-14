// ---- AI HOLATI: bepul limit tugaganini ko'rsatish (Gemini limiti yoki ilovaning kunlik limiti) va bugungi sarf; sarlavha belgilarini (##) chiroyli ko'rsatish ----
const aiQKey='trk_aiq';
function aiQuotaMark(msg){const m=String(msg||'');let o=null;if(/Bugungi bepul AI limiti tugadi/.test(m))o={k:'g',t:Date.now()};else if(/Bugungi limit tugadi/.test(m))o={k:'a',d:dk(),t:Date.now()};if(!o)return;try{localStorage.setItem(aiQKey,JSON.stringify(o))}catch(e){}try{aiStatPaint()}catch(e){}}
function aiQuotaClear(){try{if(localStorage.getItem(aiQKey)){localStorage.removeItem(aiQKey);aiStatPaint()}}catch(e){}}
// Google bepul limiti Tinch okean vaqti yarim tunida yangilanadi: 07:00 yoki 08:00 UTC (Toshkentda 12:00-13:00). Ishonch uchun 08:05 UTC gacha kutamiz
function aiQuotaReset(t){const d=new Date(t),at=Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate(),8,5);return d.getTime()<at?at:at+864e5}
function aiQuotaGet(){let o=null;try{o=JSON.parse(localStorage.getItem(aiQKey)||'null')}catch(e){}if(!o)return null;if(o.k==='g'){if(Date.now()>=aiQuotaReset(o.t)){try{localStorage.removeItem(aiQKey)}catch(e){}return null}return o}if(o.k==='a'){if(o.d!==dk()){try{localStorage.removeItem(aiQKey)}catch(e){}return null}return o}return null}
function aiStatIn(){const q=aiQuotaGet();if(q)return `<p class="aistat aibad" role="status">🔴 ${q.k==='g'?'Bepul AI limiti tugagan. Tiklanishi: taxminan 12:00–13:00 (Toshkent vaqti). Shu vaqtgacha AI tugmalari ishlamasligi mumkin; boshqa funksiyalar ishlayveradi.':'Bugungi AI limiting tugadi ('+aiLimit()+' ta so‘rov). Ertaga yangilanadi.'}</p>`;
  const c=aiLimGet();if(!c||c.d!==dk())return '';if(c.o)return '<p class="aistat aiok">🟢 AI: cheksiz (egasi)</p>';const u=aiUsedAll(),l=aiLimit(),r=l?u/l:0;return `<p class="aistat ${r>=.9?'aibad':r>=.6?'aiwarn':'aiok'}">${r>=.9?'🔴':r>=.6?'🟡':'🟢'} AI: ${u}/${l} bugun</p>`}
function aiStat(){try{if(typeof aiLimRefresh==='function')aiLimRefresh()}catch(e){}return `<div data-aistat>${aiStatIn()}</div>`}
function aiStatPaint(){const h=aiStatIn();document.querySelectorAll('[data-aistat]').forEach(e=>{e.innerHTML=h})}
// ---- sarlavhalar: "## Introduction" -> chiroyli sarlavha (o'qib berishda ham belgisiz) ----
function ieHdP(p,m){const h=/^\s*#{1,4}\s+(\S.*)$/.exec(p);return h?`<p class="iep iehd">${ieMark(h[1].trim(),m)}</p>`:`<p class="iep">${ieMark(p,m)}</p>`}
