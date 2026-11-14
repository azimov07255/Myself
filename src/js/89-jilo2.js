// ---- JILO 2: Bugun kartalari (vaqtga qarab tartib va ko'rinish), Nafs bo'limi ikkiga bo'lingan, 📖 Bugungi Qur'on rejasi, keng ekran avto. Hammasi Sozlamalar → 🪄 Jilo va qulaylik da avvalgidek qilib qo'yiladi ----
const BCL=[['n3','⏭ Keyingi 3 soat'],['dc','🩺 Kun tekshiruvi'],['qr','📖 Bugungi Qur‘on rejasi'],['rw','🏅 Daraja va XP'],['co','↩︎ Qaytish'],['md','⚙️ Rejim'],['ns','🌿 Kun nasihati'],['ib','📥 Tezkor yozuvlar'],['kc','🌙 Kunni yopish'],['ey','🛤 Imtihon yo‘li'],['tq','📖 Takror qatori'],['km','🧮 Ko‘rsatkichlar'],['tt','⏱ Vaqt hisobi'],['cb','📚 Cambridge takror'],['ml','🌙 Mulk surasi'],['sos','🛡 Nafs himoyasi'],['zn','🧭 Rejimlar'],['zj','🧭 Kun tartibi'],['st','📊 Haftalik xulosa'],['rit','⏰ Uyg‘onish tizimi'],['ap','🗓 AI kun rejasi'],['wk','📝 Haftalik sharh'],['rz','🌙 Ramazon'],['top','🎯 3 ta asosiy ish'],['due','⏳ Muddatlar'],['uni','🎓 Univer'],['zk','🤲 Zikr'],['mg','⭐ Asosiy maqsad'],['ai','✨ AI maslahat']];
const bcMode=()=>uiG('trk_bco')!=='a',bcHidden=()=>new Set(String(uiG('trk_bch')||'').split(',').filter(Boolean));
const BCF={m:['tq','qr','ns','ib','km','md'],e:['kc','st','km','ib','ml','sos','zn','zj']},BCB={m:['kc','st','ey'],e:['tq','qr','ns','ey']};
function bcPrep(L){const H=bcHidden();let A=L.filter(x=>!H.has(x[0]));if(!bcMode()||A.length<8)return A;const h=new Date().getHours(),p=h<12?'m':h>=18?'e':'';if(!p)return A;const F=BCF[p],B=BCB[p],byK=k=>A.find(x=>x[0]===k);return F.map(byK).filter(Boolean).concat(A.filter(x=>!F.includes(x[0])&&!B.includes(x[0]))).concat(B.filter(k=>!F.includes(k)).map(byK).filter(Boolean))}
function bcToggle(k){const H=bcHidden();H.has(k)?H.delete(k):H.add(k);uiS('trk_bch',[...H].join(','));render()}
function bcAll(){uiS('trk_bch','');render()}
{const o=window.btCards;if(typeof o==='function'&&!o.__x){const w=function(L){return o.call(this,bcPrep(L))};w.__x=1;window.btCards=w}}
// ----- 🧭 Nafs ikkiga bo'lingan -----
let NVS='k';
const nfvSplit=()=>uiG('trk_nfv')!=='a';
function nvsGo(v){NVS=v;render()}
{const o=window.nafsTab;if(typeof o==='function'&&!o.__x){const w=function(){if(!nfvSplit())return o.apply(this,arguments);try{nkEval()}catch(e){}return `<div class="seg" style="margin-bottom:10px"><button class="${NVS==='k'?'on':''}" onclick="nvsGo('k')">🧮 Kuzatuv</button><button class="${NVS==='o'?'on':''}" onclick="nvsGo('o')">🤝 Odat va nafs</button></div>`+(NVS==='o'?rtStatCard()+nkCard()+nkBarCard()+nxCard():nkF5Card()+kmCard()+kfCard()+nkBalCard())};w.__x=1;window.nafsTab=w}}
// ----- 📖 Bugungi Qur'on rejasi -----
const qrOn=()=>uiG('trk_qr')!=='0';
function qrRows(){const q=ssC(),k=dk(),R=[];const ny=(q.ny||{})[k]||0,ppd=q.ppd||0;if(ppd>0)R.push({i:'🌱',n:'Sabaq',v:r1(ny)+' / '+ppd+' bet',ok:ny>=ppd,go:"tab='q';QT='t';TKV='s';render()"});
  try{ssParts().forEach(P=>R.push({i:P.k==='q'?'🔁':'📚',n:P.n,v:r1(P.p)+' bet',ok:!!P.done,go:"tab='q';QT='t';TKV='s';render()"}))}catch(e){}
  const tg=tqGoalPg('k'),p=tqPages(k,'k');if(tg>0||p>0)R.push({i:'📖',n:'Takror',v:tqF(p)+(tg?' / '+tqF(tg):'')+' bet',ok:tg>0?p>=tg:p>0,go:"tqGo()"});
  const tn=tqGoalPg('n'),pn=tqPages(k,'n');if(tn>0||pn>0)R.push({i:'🕌',n:'Namozda',v:tqF(pn)+(tn?' / '+tqF(tn):'')+' bet',ok:tn>0?pn>=tn:pn>0,go:"tqGo();TQT='n';render()"});
  [['k',tqCyO('k')],['n',tqCyO('n')]].forEach(([tr,c])=>{if(c&&c.on){const P=tqCy(tr);R.push({i:'🔄',n:tr==='n'?'Namozda aylanish':'Aylanish',v:P.done?'bajarildi':'≈ '+tqF(P.items.reduce((a,e)=>a+e.pg,0))+' bet',ok:P.done,go:"tqGo();TQT='"+tr+"';render()"})}});
  return R}
function qrCard(){if(!qrOn())return '';const R=qrRows();if(!R.length)return '';const d=R.filter(x=>x.ok).length,pc=Math.round(d/R.length*100);return `<section class="goal" aria-label="Bugungi Qur‘on rejasi"><div class="h"><b>📖 Bugungi Qur‘on rejasi</b><span class="chip ${d===R.length?'on':''}">${d}/${R.length}</span></div><div class="bar" style="margin:8px 0 6px"><i style="width:${pc}%"></i></div>${R.map(x=>`<button class="row ${x.ok?'done':''}" onclick="${x.go}" aria-label="${esc(x.n)}"><span style="font-size:20px">${x.i}</span><span class="t"><b>${esc(x.n)}</b></span><span class="mu" style="font-size:13px">${esc(x.v)} ${x.ok?'✅':'›'}</span></button>`).join('')}</section>`}
// ----- 🖥 keng ekran: avto (≥1000px), yoqilgan, o'chirilgan -----
const wideOn=()=>{const v=uiG('trk_wide');return v==='1'||((!v||v==='a')&&innerWidth>=1000)};
function wideSet(v){uiS('trk_wide',v);document.documentElement.classList.toggle('wide',wideOn());render()}
try{document.documentElement.classList.toggle('wide',wideOn());addEventListener('resize',()=>document.documentElement.classList.toggle('wide',wideOn()))}catch(e){}
// ----- 🪄 sozlamalar (kengaytma) -----
function jlCard2(){const H=bcHidden();return `<p class="mu" style="margin:12px 0 4px;font-size:12px"><b>Bugun kartalari tartibi</b></p>${jlSeg('trk_bco','v',[['v','Vaqtga qarab'],['a','Avvalgidek']])}
  <p class="mu" style="margin:6px 0 4px;font-size:12px"><b>Bugun’da ko‘rinadigan kartalar</b> (bosib yashir/ko‘rsat)</p><div class="rwch" style="margin-bottom:8px">${BCL.map(([k,l])=>`<button class="chip ${H.has(k)?'':'on'}" style="border:0" onclick="bcToggle('${k}')" aria-pressed="${!H.has(k)}">${l}</button>`).join('')}</div>${H.size?'<button class="btn s" onclick="bcAll()">Hammasini ko‘rsat</button>':''}
  <p class="mu" style="margin:12px 0 4px;font-size:12px"><b>Bugun kartalari</b></p>${jlSeg('trk_bsec','g',[['g','Bo‘limlarga yig‘ilgan'],['a','Alohida (avvalgidek)']])}<p class="mu" style="margin:12px 0 4px;font-size:12px"><b>Nafs bo‘limi</b></p>${jlSeg('trk_nfv','s',[['s','Ikkiga bo‘lingan'],['a','Hammasi birga (avvalgidek)']])}
  <p class="mu" style="margin:6px 0 4px;font-size:12px"><b>Bugungi Qur‘on rejasi kartasi</b></p>${jlSeg('trk_qr','1',[['1','Yoqilgan'],['0','O‘chirilgan']])}
  <p class="mu" style="margin:6px 0 4px;font-size:12px"><b>Keng ekran (kompyuter)</b></p><div class="seg" style="margin-bottom:10px">${[['a','Avto'],['1','Yoqilgan'],['0','O‘chirilgan']].map(([v,l])=>`<button class="${(uiG('trk_wide')||'a')===v?'on':''}" onclick="wideSet('${v}')">${l}</button>`).join('')}</div>`}
