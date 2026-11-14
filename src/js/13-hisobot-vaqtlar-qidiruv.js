// ---- Oylik hisobot ----
function mStats(y,m){
  const nd=new Date(y,m+1,0).getDate(),T0=dk(),pk=x=>`${y}-${pad(m+1)}-${pad(x)}`,keys=[...Array(nd)].map((_,i)=>pk(i+1)).filter(k=>k<=T0),inM=d=>d.startsWith(`${y}-${pad(m+1)}`);
  const sc=keys.map(k=>scoreOf(k).p),avg=sc.length?Math.round(sc.reduce((a,c)=>a+c,0)/sc.length):0,perfect=sc.filter(v=>v>=100).length,mx=Math.max(0,...sc),bd=sc.length&&mx>0?keys[sc.indexOf(mx)]:null;
  const hab=S.hab.map(x=>{let run=0,best=0,n=0;keys.forEach(k=>{if((S.hb[k]||{})[x.id]){n++;run++;best=Math.max(best,run)}else run=0});return{t:x.t,e:x.e||'',n,best}}).sort((a,b)=>b.n-a.n);
  const q=S.q,sum=f=>keys.reduce((a,k)=>a+(f(k)||0),0);
  let pr=0,qz=0;keys.forEach(k=>PR.slice(0,5).forEach(([p])=>{const s_=((S.nm.d[k]||{})[p])||0;if(s_===1)pr++;if(s_===2)qz++}));
  const gd=new Set(S.gym.log.filter(x=>inM(x.d)).map(x=>x.d)).size,bw=S.gym.body.filter(x=>inM(x.d)),dw=bw.length>1?r1(bw[bw.length-1].w-bw[0].w):null;
  const ml=S.money.filter(x=>x.w==='p'&&inM(x.d)),pin=ml.filter(x=>x.k==='in').reduce((a,x)=>a+x.a,0),pout=ml.filter(x=>x.k==='out').reduce((a,x)=>a+x.a,0),cat={};ml.filter(x=>x.k==='out').forEach(x=>{const c=x.c||'Boshqa';cat[c]=(cat[c]||0)+x.a});
  return{y,m,days:keys.length,sc,avg,perfect,bd,hab,hatm:sum(k=>q.hd[k]),takror:r1(sum(k=>q.rd[k])),ay:sum(k=>((q.ty||{})[k]||[]).filter(e=>e.x).reduce((a,e)=>a+e.b-e.a+1,0)),zikr:sum(k=>Object.values(S.z.c[k]||{}).reduce((a,c)=>a+c,0)),fok:sum(k=>S.fm[k]),
    npc:keys.length?Math.round(pr/(keys.length*5)*100):0,qz,gd,dw,pin,pout,tc:Object.entries(cat).sort((a,b)=>b[1]-a[1])[0],
    kp:S.kt.log.filter(x=>inM(x.d)).reduce((a,x)=>a+x.n,0),kb:S.kt.books.filter(b=>b.st==='t'&&b.fin&&inM(b.fin)).length,ig:keys.filter(k=>(S.rules[k]||{}).ig).length,wl:keys.filter(k=>S.wake[k]).length}}
const mRows=s=>[['O‘rtacha ball',s.avg+'%'],['Mukammal kunlar',s.perfect+' ta'],['Eng uzun odat seriyasi',(s.hab[0]?Math.max(...s.hab.map(x=>x.best)):0)+' kun'],['Qur‘on: hatm / takror',s.hatm+' / '+s.takror+' bet'],['Namozlar',s.npc+'%'+(s.qz?', qazo '+s.qz:'')],['Zal',s.gd+' kun'+(s.dw!==null?', vazn '+(s.dw>0?'+':'')+s.dw+' kg':'')],['Kitob',s.kp+' bet'+(s.kb?', '+s.kb+' ta tugatildi':'')],['Instagramsiz',s.ig+' kun']];
function oy(){return `<div class="seg" style="margin-top:0"><button class="${RY==='m'?'on':''}" onclick="RY='m';render()">Oylik</button><button class="${RY==='y'?'on':''}" onclick="RY='y';render()">Yillik (Wrapped)</button></div>`+(RY==='y'?wrapped():oyM())}
function oyM(){
  const now=new Date(),d0=new Date(now.getFullYear(),now.getMonth()+RM,1),s=mStats(d0.getFullYear(),d0.getMonth()),mn=MON[s.m][0].toUpperCase()+MON[s.m].slice(1);
  const bars=s.sc.map((p,i)=>`<div style="flex:1;min-width:0"><div style="height:60px;display:flex;align-items:flex-end"><div style="width:100%;height:${Math.max(2,p*.6)}px;background:var(--ac);opacity:.8;border-radius:2px"></div></div></div>`).join('');
  const R=(l,v)=>`<div class="row"><span class="t">${l}</span><b>${v}</b></div>`;
  const hr=s.hab.slice(0,6).map(x=>`<div style="margin-bottom:8px"><div style="display:flex;justify-content:space-between"><span>${x.e} ${esc(x.t)}</span><span class="mu">${x.n}/${s.days} kun</span></div><div class="bar"><i style="width:${s.days?x.n/s.days*100:0}%"></i></div></div>`).join('');
  return `<div class="in"><button class="btn s" onclick="RM--;render()">‹</button><button class="btn s" onclick="RM=0;render()">Shu oy</button><button class="btn s" onclick="RM++;render()">›</button></div>
  <section class="hero"><p class="lab">Oylik hisobot</p><h1 style="font-size:36px">${mn} ${s.y}</h1><h1 style="font-size:54px;margin-top:0">${s.avg}%</h1><p class="mu">${s.days} kun hisoblandi. ${s.perfect} ta mukammal kun${s.bd?', eng yaxshi kun '+s.bd.slice(8)+'-sana':''}.</p></section>
  <h2>Kunlar bo‘yicha ball</h2><div style="display:flex;gap:2px">${bars||'<p class="mu">Bu oyda hali ma‘lumot yo‘q.</p>'}</div>
  ${hr?`<h2>Odatlar</h2>${hr}`:''}
  <h2>Raqamlarda</h2>${mRows(s).map(r=>R(r[0],r[1])).join('')}${R('Qur‘on: yodlangan oyat / zikr',s.ay+' / '+s.zikr)}${R('Fokus',s.fok+' daqiqa')}${R('Uyg‘onish yozilgan',s.wl+' kun')}
  <h2>Pul (shaxsiy)</h2>${R('Kirim / chiqim','+'+num(s.pin)+' / −'+num(s.pout))}${R('Balans',num(s.pin-s.pout)+' so‘m')}${s.tc?R('Eng ko‘p sarf',esc(s.tc[0])+', '+num(s.tc[1])):''}
  <h2>Ulashish</h2><button class="row ${RMN?'done':''}" onclick="RMN=!RMN;render()"><span class="ck">${RMN?'✓':''}</span><span class="t">Rasmda pulni ham ko‘rsat</span></button>
  <div class="in" style="margin-top:6px"><button class="btn" style="flex:1" onclick="shareMonth()">Rasm qilib ulashish</button><button class="btn s" style="flex:1" onclick="copyMonth()">Matnni nusxalash</button></div>`}
async function shareMonth(){
  const d0=new Date(new Date().getFullYear(),new Date().getMonth()+RM,1),s=mStats(d0.getFullYear(),d0.getMonth()),mn=MON[s.m][0].toUpperCase()+MON[s.m].slice(1);
  const c=document.createElement('canvas');c.width=1080;c.height=1350;const x=c.getContext('2d'),g=x.createLinearGradient(0,0,0,1350);g.addColorStop(0,'#0a1a2c');g.addColorStop(1,'#143a5c');x.fillStyle=g;x.fillRect(0,0,1080,1350);
  x.fillStyle='rgba(226,184,87,.08)';for(let i=0;i<8;i++){x.beginPath();x.arc(980,120+i*0,200+i*40,0,7);x.fill()}
  x.textBaseline='alphabetic';x.fillStyle='#e2b857';x.font='600 34px Georgia,serif';x.fillText('OYLIK HISOBOT'+(S.name?'  '+S.name.toUpperCase():''),80,120);
  x.fillStyle='#e9eef2';x.font='700 92px Georgia,serif';x.fillText(mn+' '+s.y,80,230);
  const cx=840,cy=420,R=130;x.lineWidth=26;x.strokeStyle='rgba(255,255,255,.12)';x.beginPath();x.arc(cx,cy,R,0,7);x.stroke();x.strokeStyle='#46c4b2';x.lineCap='round';x.beginPath();x.arc(cx,cy,R,-Math.PI/2,-Math.PI/2+Math.PI*2*s.avg/100);x.stroke();
  x.fillStyle='#e9eef2';x.textAlign='center';x.font='700 84px Georgia,serif';x.fillText(s.avg+'%',cx,cy+28);x.font='500 28px sans-serif';x.fillStyle='#8fa6ba';x.fillText('o‘rtacha ball',cx,cy+78);x.textAlign='left';
  const rows=mRows(s).slice(1);if(RMN)rows.push(['Pul balansi',num(s.pin-s.pout)+' so‘m']);
  rows.forEach((r,i)=>{const y=620+i*84;x.fillStyle='rgba(255,255,255,.06)';x.fillRect(80,y-52,920,70);x.fillStyle='#8fa6ba';x.font='500 30px sans-serif';x.fillText(r[0],104,y-6);x.fillStyle='#e9eef2';x.font='700 32px sans-serif';x.textAlign='right';x.fillText(r[1],976,y-6);x.textAlign='left'});
  x.fillStyle='#e2b857';x.font='600 30px Georgia,serif';x.textAlign='center';x.fillText('KUNLIK TIZIM BY AZIMOV',540,1290);
  const blob=await new Promise(r=>c.toBlob(r,'image/png')),f=new File([blob],'oylik-hisobot-'+s.y+'-'+pad(s.m+1)+'.png',{type:'image/png'});
  try{if(navigator.canShare&&navigator.canShare({files:[f]})){await navigator.share({files:[f],title:'Oylik hisobot'});return}}catch(e){if(e&&e.name==='AbortError')return}
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=f.name;document.body.appendChild(a);a.click();a.remove()}
function copyMonth(){const d0=new Date(new Date().getFullYear(),new Date().getMonth()+RM,1),s=mStats(d0.getFullYear(),d0.getMonth());
  const t=MON[s.m]+' '+s.y+' hisoboti\n'+mRows(s).map(r=>r[0]+': '+r[1]).join('\n')+(RMN?'\nPul balansi: '+num(s.pin-s.pout)+' so‘m':'')+'\nKunlik tizim by AZIMOV';
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>alert('Nusxalandi.')).catch(()=>prompt('Nusxalang:',t))}

// ---- Namoz vaqtlari ----
const PK={fajr:'Fajr',dhuhr:'Dhuhr',asr:'Asr',maghrib:'Maghrib',isha:'Isha'};
const PCITY=[['Toshkent',41.2995,69.2401],['Samarqand',39.6542,66.9597],['Buxoro',39.7748,64.4286],['Andijon',40.7821,72.3442],['Farg‘ona',40.3842,71.7843],['Namangan',41.0011,71.6726],['Qo‘qon',40.5286,70.9425],['Qarshi',38.8606,65.7891],['Navoiy',40.0844,65.3792],['Jizzax',40.1158,67.8422],['Guliston',40.4897,68.7842],['Termiz',37.2242,67.2783],['Urganch',41.5506,60.6314],['Xiva',41.3783,60.3639],['Nukus',42.4531,59.6103]];
const PNAMES=[['Fajr','Bomdod'],['Sunrise','Quyosh'],['Dhuhr','Peshin'],['Asr','Asr'],['Maghrib','Shom'],['Isha','Xufton']];
const ptTz=()=>S.pt.loc==='gps'?-new Date().getTimezoneOffset()/60:5;
// O‘zbekiston Musulmonlar idorasi uslubi (islom.uz Toshkent jadvaliga moslab sozlangan)
function ptCalc(y,m,d,lat,lon,tz){
  const D=Math.PI/180;
  const jd=h=>{let Y=y,M=m;if(M<=2){Y--;M+=12}const A=Math.floor(Y/100),B=2-A+Math.floor(A/4);return Math.floor(365.25*(Y+4716))+Math.floor(30.6001*(M+1))+d+B-1524.5+h/24};
  const sun=j=>{const T=(j-2451545)/36525,L0=(280.46646+T*(36000.76983+T*0.0003032))%360,M2=357.52911+T*(35999.05029-0.0001537*T),e=0.016708634-T*(0.000042037+0.0000001267*T),
    C=Math.sin(M2*D)*(1.914602-T*(0.004817+0.000014*T))+Math.sin(2*M2*D)*(0.019993-0.000101*T)+Math.sin(3*M2*D)*0.000289,om=125.04-1934.136*T,lam=L0+C-0.00569-0.00478*Math.sin(om*D),
    e0=23+(26+(21.448-T*(46.815+T*(0.00059-T*0.001813)))/60)/60,eps=e0+0.00256*Math.cos(om*D),dec=Math.asin(Math.sin(eps*D)*Math.sin(lam*D))/D,y2=Math.tan(eps*D/2)**2,
    eot=4*(y2*Math.sin(2*L0*D)-2*e*Math.sin(M2*D)+4*e*y2*Math.sin(M2*D)*Math.cos(2*L0*D)-0.5*y2*y2*Math.sin(4*L0*D)-1.25*e*e*Math.sin(2*M2*D))/D;return[dec,eot]};
  const j0=jd(0),ha=(al,dc)=>{const c=(Math.sin(al*D)-Math.sin(lat*D)*Math.sin(dc*D))/(Math.cos(lat*D)*Math.cos(dc*D));return Math.acos(Math.max(-1,Math.min(1,c)))/D};
  const at=(t0,sg,fn)=>{let t=t0;for(let i=0;i<3;i++){const[dc,eo]=sun(j0+(t-tz*60)/1440);t=720-4*lon-eo+tz*60+sg*4*fn(dc)}return t};
  const[d0,e0]=sun(j0+(720-tz*60)/1440),n=720-4*lon-e0+tz*60,R=x=>Math.floor(x+0.5);
  const asr=dc=>ha(Math.atan(1/(2+Math.tan(Math.abs(lat-dc)*D)))/D,dc);
  return{Fajr:R(at(n-300,-1,dc=>ha(-15.55,dc))),Sunrise:R(at(n-300,-1,dc=>ha(-0.833,dc))),Dhuhr:R(n),Asr:Math.ceil(at(n+200,1,asr)),Maghrib:R(at(n+300,1,dc=>ha(-0.833,dc))+5.8),Isha:Math.ceil(at(n+400,1,dc=>ha(-15.1,dc)))}}
function ptRaw(date){const P=S.pt,dt=date||new Date();return ptCalc(dt.getFullYear(),dt.getMonth()+1,dt.getDate(),P.lat,P.lon,ptTz())}
function ptTimes(){const P=S.pt;if(!P)return null;const r=ptRaw(),o={};PNAMES.forEach(([k])=>{o[k]=(r[k]+((P.tune||{})[k]||0)+1440)%1440});return o}
const ptT=k=>{const t=ptTimes();return t&&k&&t[k]!==undefined?hm(t[k]):''};
function ptNext(){const t=ptTimes();if(!t)return null;const d=new Date(),n=d.getHours()*60+d.getMinutes();
  for(const [k,nm] of PNAMES){if(k==='Sunrise')continue;if(t[k]>n)return{n:nm,t:t[k],left:t[k]-n}}
  return{n:'Bomdod',t:t.Fajr,left:t.Fajr+1440-n}}
function ptEnsure(){const P=S.pt;if(P&&P.v!==2){P.v=2;P.tune={};P.cache=null;save()}}
function ptLoc(v){const P=S.pt;
  if(v==='gps'){if(!navigator.geolocation){alert('Joylashuv aniqlanmadi.');return}
    navigator.geolocation.getCurrentPosition(p=>{P.loc='gps';P.lat=p.coords.latitude;P.lon=p.coords.longitude;save()},()=>alert('Joylashuvga ruxsat berilmadi. Shaharni ro‘yxatdan tanla.'),{timeout:10000});return}
  const c=PCITY.find(x=>x[0]===v);if(!c)return;P.loc=c[0];P.lat=c[1];P.lon=c[2];save()}
function ptCal(){const P=S.pt,r=ptRaw();P.tune=P.tune||{};PNAMES.forEach(([k])=>{const v=V('pc_'+k);if(v)P.tune[k]=t2m(v)-r[k]});save()}
function ptRst(){S.pt.tune={};save()}
function ptCard(){
  const P=S.pt,t=ptTimes(),nx=ptNext(),nm=PNAMES.map(([k,n])=>`<div class="pc ${nx&&t&&t[k]===nx.t&&n===nx.n?'nx':''}"><span>${n}</span><b>${t&&t[k]!==undefined?hm(t[k]):'--:--'}</b></div>`).join('');
  const opts=`<option value="gps" ${P.loc==='gps'?'selected':''}>Joylashuvim (GPS)</option>`+PCITY.map(c=>`<option value="${c[0]}" ${P.loc===c[0]?'selected':''}>${c[0]}</option>`).join('');
  const cal=PNAMES.map(([k,n])=>`<div class="in" style="margin-bottom:6px"><span style="align-self:center;min-width:64px">${n}</span><input id="pc_${k}" type="time" value="${t&&t[k]!==undefined?hm(t[k]):''}"></div>`).join('');
  return `<section class="hero"><p class="lab">Namoz vaqtlari, ${P.loc==='gps'?'joylashuvim':P.loc}</p>${nx?`<h1 style="font-size:30px">${nx.n} ${hm(nx.t)}</h1><p class="mu">${fmt(nx.left).trim()} qoldi</p>`:`<h1 style="font-size:26px">Vaqt hisoblanmadi</h1>`}
  <div class="np" style="grid-template-columns:repeat(3,1fr);margin:10px 0">${nm}</div>
  <div class="in"><select onchange="ptLoc(this.value)">${opts}</select></div>
  <details><summary class="mu" style="margin-bottom:8px">Daqiqalarni qo‘lda to‘g‘rilash</summary><p class="mu" style="margin:0 0 8px">Joyingdagi masjid yoki islom.uz bilan farq bo‘lsa, kerakli vaqtni yoz. Ilova farqni eslab, keyingi kunlarda ham qo‘llaydi.</p>${cal}<div class="in"><button class="btn" style="flex:1" onclick="ptCal()">Moslash</button><button class="btn s" style="flex:1" onclick="ptRst()">Asliga qaytarish</button></div></details>
  <p class="mu" style="margin:6px 0 0;font-size:12px">O‘zbekiston Musulmonlar idorasi uslubida, Hanafiy mazhab. Toshkent uchun islom.uz jadvaliga solishtirib sozlangan.</p></section>${ptMonth()}`}

// ---- Namozda yodlaganlarim hatmi ----
const nhList=()=>{const q=S.q,o=[];SN.forEach((n,i)=>{const d=Math.min(q.m[i]||0,SL(i));if(d>0)o.push({i,pg:d})});return o};
function nhPos(p){let c=0;for(const x of nhList()){if(p<c+x.pg-1e-9)return{i:x.i,left:c+x.pg-p,off:p-c,pg:x.pg};c+=x.pg}return null}
function nhAdd(n,sura){const N=S.nh,T=nhList().reduce((a,x)=>a+x.pg,0);if(!T)return;let a=n;if(sura){const pos=nhPos(N.p);if(!pos)return;a=pos.left}
  N.log.push({id:Date.now(),d:dk(),pr:N.pr,n:a});N.p+=a;while(N.p>=T-1e-9){N.c++;N.hist.push({d:dk()});N.p=Math.max(0,N.p-T)}save()}
function nhPr(p){S.nh.pr=p;save()}
function nhDel(id){const N=S.nh,x=N.log.find(y=>y.id===id);if(!x)return;N.log=N.log.filter(y=>y.id!==id);N.p=Math.max(0,N.p-x.n);save()}
function nhCard(){
  const N=S.nh,L=nhList(),T=L.reduce((a,x)=>a+x.pg,0),k=dk();
  if(!T)return `<h2>Namozda yodlaganlarim hatmi</h2><p class="mu">Avval Qur‘on → Yodlash bo‘limida suralarni belgila. Keyin namozda ovoz chiqarib o‘qiganlaringni shu yerda hatm qilasan.</p>`;
  const pos=nhPos(N.p),PL=[['fajr','Bomdod'],['dhuhr','Peshin'],['asr','Asr'],['maghrib','Shom'],['isha','Xufton'],['nafl','Nafl']],nmz=Object.fromEntries(PL);
  const td=N.log.filter(x=>x.d===k),tp=td.reduce((a,x)=>a+x.n,0);
  const rows=td.slice().reverse().map(x=>`<div class="row"><span class="t">${nmz[x.pr]||''}<br><span class="mu">${r1(x.n)} bet</span></span><button class="x" onclick="nhDel(${x.id})">×</button></div>`).join('');
  return `<h2>Namozda yodlaganlarim hatmi</h2><p class="mu" style="margin:0 0 8px">Yodlagan suralaringni namozda ovoz chiqarib o‘qib, aylanib hatm qilasan. Tartib mushaf bo‘yicha.</p>
  <div class="goal"><div class="h"><b style="font:700 19px Fraunces,serif">${r1(N.p)} / ${r1(T)} bet</b><span class="mu">${N.c} ta hatm</span></div><div class="bar" style="margin:8px 0"><i style="width:${Math.min(100,N.p/T*100)}%"></i></div>
  ${pos?`<p style="margin:0 0 8px">Navbatdagi sura: <b>${SN[pos.i]}</b> <span class="mu">(shu suradan ${r1(pos.left)} bet qoldi)</span></p>`:''}
  <div class="chips">${PL.map(([p,t])=>`<button class="${N.pr===p?'on':''}" onclick="nhPr('${p}')">${t}</button>`).join('')}</div>
  <div class="in">${[0.5,1,2,3].map(n=>`<button class="btn s" style="flex:1;padding:10px 0" onclick="nhAdd(${n})">+${n}</button>`).join('')}</div><button class="btn" style="width:100%" onclick="nhAdd(0,1)">Navbatdagi surani to‘liq o‘qidim</button>
  <p class="mu" style="margin:8px 0 0">Bugun namozda: ${r1(tp)} bet</p>${rows}${N.hist.length?`<p class="mu" style="margin:10px 0 0">Tugatilgan hatmlar: ${N.hist.map(x=>x.d).join(', ')}</p>`:''}</div>`}

let PM=0,PMO=false,PUPL={},HV='w',HW=0,LT=0;
let SO=false,SQ='',SRL=[];
function ptMonth(){
  const P=S.pt,now=new Date(),d0=new Date(now.getFullYear(),now.getMonth()+PM,1),y=d0.getFullYear(),m=d0.getMonth(),nd=new Date(y,m+1,0).getDate();
  let rows='';if(PMO)for(let d=1;d<=nd;d++){const r=ptCalc(y,m+1,d,P.lat,P.lon,ptTz()),td=PM===0&&d===now.getDate();
    rows+=`<tr class="${td?'tdr':''}"><td>${d}</td>${PNAMES.map(([k])=>`<td>${hm((r[k]+((P.tune||{})[k]||0)+1440)%1440)}</td>`).join('')}</tr>`}
  return `<details ${PMO?'open':''} ontoggle="PMO=this.open" style="margin-top:12px"><summary class="mu" style="margin-bottom:8px">Oylik jadval (${P.loc==='gps'?'joylashuvim':P.loc})</summary>${PMO?`<div class="in"><button class="btn s" onclick="PM--;render()">‹</button><button class="btn s" onclick="PM=0;render()">Shu oy</button><button class="btn s" onclick="PM++;render()">›</button></div><p class="mu" style="margin:0 0 6px">${MON[m][0].toUpperCase()+MON[m].slice(1)} ${y}</p><div class="hg" data-k="pm"><table class="mt"><tr><th>Kun</th>${PNAMES.map(([,n])=>`<th>${n}</th>`).join('')}</tr>${rows}</table></div>`:''}</details>`}

// ---- Qidiruv ----
const sn=t=>String(t||'').toLowerCase().replace(/[‘’'`ʻ]/g,'');
function srAll(){const o=[],add=(k,t,x,f)=>o.push({k,t,x:x||'',f});
  S.hab.forEach(x=>add('Odat',x.t,'',()=>{OT='j';go('o')}));
  S.goals.forEach(g=>{add('Maqsad',g.t,g.why||'',()=>go('m'));(g.ms||[]).forEach(m=>add('Bosqich',m.t,g.t,()=>go('m')))});
  Object.keys(S.tasks).forEach(k=>S.tasks[k].forEach(t=>add('Vazifa',t.t,k,()=>{vd(k);go('h')})));
  Object.keys(S.top).forEach(k=>(S.top[k]||[]).forEach(t=>add('Asosiy ish',t.t,k,()=>{vd(k);go('h')})));
  Object.keys(S.note).forEach(k=>S.note[k]&&add('Kun xulosasi',S.note[k].slice(0,80),k,()=>{vd(k);go('h')}));
  S.kt.books.forEach(b=>add('Kitob',b.t,(b.a||'')+' '+(b.sum||'').slice(0,60),()=>{EV='k';go('e')}));
  S.ie.words.forEach(w=>add('Lug‘at',w.w,w.m,()=>{EV='i';go('e')}));
  S.un.tasks.forEach(t=>add('Univer',t.t,t.s||'',()=>{EV='u';go('e')}));S.un.exams.forEach(e=>add('Imtihon',e.s,e.d,()=>{EV='u';go('e')}));
  SN.forEach((n,i)=>add('Sura',n,(i+1)+'-sura',()=>{QT='y';go('q')}));
  S.money.forEach(m=>{if(m.n)add('Pul',m.n,m.d+', '+num(m.a),()=>go('p'))});
  S.gym.log.forEach(g=>add('Zal',g.n,g.d,()=>{OT='z';go('o')}));
  bl().forEach(b=>add('Reja',b.t,hm(b.s),()=>go('h')));
  S.iso.log.forEach(x=>add('Isolation',x.t,x.d,()=>{OT='i';go('o')}));
  (S.debts||[]).forEach(x=>add('Qarz',x.p,num(x.a),()=>{PV='q';go('p')}));
  return o}
function srRes(){const q=sn(SQ).trim();if(q.length<2){SRL=[];return '<p class="mu">Kamida 2 ta harf yoz.</p>'}
  SRL=srAll().filter(r=>sn(r.t+' '+r.x).includes(q)).slice(0,40);
  return SRL.length?SRL.map((r,i)=>`<button class="row" onclick="srGo(${i})"><span class="t">${esc(r.t)}<br><span class="mu">${r.k}${r.x?', '+esc(r.x):''}</span></span></button>`).join(''):'<p class="mu">Hech narsa topilmadi.</p>'}
function srGo(i){const r=SRL[i];if(!r)return;SO=false;SQ='';r.f()}
function srQ(v){SQ=v;const e=$('#srr');if(e)e.innerHTML=srRes()}
function srOpen(){SO=true;render();setTimeout(()=>{const e=$('#srq');if(e)e.focus()},60)}
function srView(){return `<div class="top"><p class="d">Qidiruv</p><button class="x" style="font-size:28px" onclick="SO=false;SQ='';render()">×</button></div><div class="in" style="margin-top:12px"><input id="srq" placeholder="Odat, kitob, so‘z, sura, vazifa..." value="${esc(SQ)}" oninput="srQ(this.value)"></div><div id="srr">${srRes()}</div>`}

