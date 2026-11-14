// ---- BUGUN KARTALARI BO'LIMLARGA YIG'ILADI (har bo'lim yig'ilib-ochiladi, holati eslab qolinadi). Sozlamalar → 🪄 Jilo da "Alohida (avvalgidek)" ga qaytadi ----
const BKSEC=[['reja','📅 Reja va vaqt',['n3','dc','tt','rit','ap','top','md','zn']],['quron','📖 Qur‘on va ibodat',['qr','tq','ml','sos','zj','zk','rz','ns']],['kuzat','🧮 Kuzatuv',['km','ey','due','uni','ib']],['yakun','🌙 Kun yakuni',['kc','st','wk']],['boshqa','⭐ Boshqa',[]]];
const bkOn=()=>uiG('trk_bsec')!=='a';
let BKX=(()=>{try{return JSON.parse(localStorage.getItem('trk_bso')||'{}')||{}}catch(e){return{}}})();
const bkOpen=id=>BKX[id]===undefined?true:!!BKX[id];
function bkTog(id,v){BKX[id]=v?1:0;try{localStorage.setItem('trk_bso',JSON.stringify(BKX))}catch(e){}}
function bkAll(v){BKSEC.forEach(s=>BKX[s[0]]=v?1:0);try{localStorage.setItem('trk_bso',JSON.stringify(BKX))}catch(e){}render()}
function bkGroup(A,o,ctx){const live=A.filter(x=>x[1]);if(live.length<4)return o.call(ctx,A);const placed=new Set(),G=[];BKSEC.forEach(([id,t,ks])=>{const L=id==='boshqa'?live.filter(x=>!BKSEC.some(s=>s[2].includes(x[0]))):live.filter(x=>ks.includes(x[0]));if(L.length){L.forEach(x=>placed.add(x));G.push({id,t,L,i:Math.min(...L.map(x=>A.indexOf(x)))})}});G.sort((a,b)=>a.i-b.i);
  return `<div class="rwch" style="margin:6px 0"><button class="chip" style="border:0" onclick="bkAll(0)">▾ Hammasini yig‘ish</button><button class="chip" style="border:0" onclick="bkAll(1)">▸ Hammasini ochish</button></div>`+G.map(g=>`<details class="bsec" ${bkOpen(g.id)?'open':''} ontoggle="bkTog('${g.id}',this.open)"><summary>${g.t} <span class="chip">${g.L.length}</span></summary>${o.call(ctx,g.L)}</details>`).join('')}
{const o=window.btCards;if(typeof o==='function'&&!o.__bs){const w=function(L){if(!bkOn()||(typeof btSimple==='function'&&btSimple())||L.length<8)return o.call(this,L);return bkGroup(typeof bcPrep==='function'?bcPrep(L):L,o,this)};w.__bs=1;window.btCards=w}}
