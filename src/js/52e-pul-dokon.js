// ---- PUL: do'kon foyda hisoboti (Hisobot bo'limida, faqat 🏪 Dokon hamyonida). Hamma narsa yozuvlardan hisoblanadi. Prefiks: dfy ----
const DFYW=['Dushanba','Seshanba','Chorshanba','Payshanba','Juma','Shanba','Yakshanba'];
function dfyData(mk){
  const L=mList('d',mk),days={};
  L.forEach(m=>{if(m.k==='tr')return;const x=days[m.d]=days[m.d]||{i:0,o:0};if(m.k==='in')x.i+=m.a;else x.o+=m.a});
  const rev=mSum(L,'in'),cost=mSum(L,'out');return{days,rev,cost,profit:rev-cost}}
const dfyPct=(a,b)=>b?Math.round((a-b)/Math.abs(b)*100):null;
const dfyDay=d=>+d.slice(8)+'-'+MON[+d.slice(5,7)-1];
function dfyCalc(mo){
  const mk=mKey(mo),pk=mKey(mo-1),A=dfyData(mk.k),B=dfyData(pk.k),y=mk.d.getFullYear(),m=mk.d.getMonth(),nd=pDim(y,m),el=mo===0?new Date().getDate():(mo<0?nd:0);
  const ent=Object.entries(A.days),sale=ent.filter(([,x])=>x.i>0),byI=sale.slice().sort((a,b)=>b[1].i-a[1].i);
  const wd=[0,0,0,0,0,0,0],wc=[0,0,0,0,0,0,0];
  for(let d=1;d<=el;d++){const k=y+'-'+pad(m+1)+'-'+pad(d),w=(new Date(y,m,d).getDay()+6)%7;wc[w]++;wd[w]+=(A.days[k]||{i:0}).i}
  const avg=wd.map((v,i)=>wc[i]?Math.round(v/wc[i]):0),bestW=avg.some(v=>v>0)?avg.indexOf(Math.max(...avg)):-1;
  return{A,B,nd,el,sale:sale.length,noSale:Math.max(0,el-sale.length),avgSale:sale.length?Math.round(A.rev/sale.length):0,
    proj:mo===0&&el>0&&A.rev>0?Math.round(A.rev/el*nd):null,best:byI[0]||null,worst:byI.length>1?byI[byI.length-1]:null,
    lossDays:ent.filter(([,x])=>x.o>x.i).length,avg,bestW,margin:A.rev?Math.round(A.profit/A.rev*100):null,
    dRev:dfyPct(A.rev,B.rev),dProfit:B.profit?dfyPct(A.profit,B.profit):null}}
function dfyUi(){
  if(W!=='d')return '';
  const c=dfyCalc(PF.mo),A=c.A,B=c.B,mx=Math.max(1,...c.avg),sg=v=>(v>0?'+':v<0?'−':'')+num(Math.abs(v)),pc=v=>v===null?'—':(v>0?'+':'')+v+'%';
  if(!A.rev&&!A.cost)return `<h2>🏪 Do‘kon foydasi</h2><div class="goal"><p class="mu" style="margin:0">Bu oyda do‘kon yozuvi yo‘q. Daromad va chiqim yozilsa, foyda va marja shu yerda chiqadi.</p></div>`;
  return `<h2>🏪 Do‘kon foydasi</h2><div class="goal">
   <p class="mu" style="margin:0">Sof foyda (daromad − chiqim)</p><p style="margin:2px 0 8px"><b class="${A.profit>=0?'in-c':'out-c'}" style="font:700 26px Fraunces,serif">${sg(A.profit)} so‘m</b></p>
   <div class="sum"><div><span class="mu">Daromad</span><b class="in-c">${num(A.rev)}</b><span class="mu" style="font-size:12px">o‘tgan oyga ${pc(c.dRev)}</span></div><div><span class="mu">Chiqim</span><b class="out-c">${num(A.cost)}</b><span class="mu" style="font-size:12px">o‘tgan oy ${num(B.cost)}</span></div></div>
   <div class="sum" style="margin-top:8px"><div><span class="mu">Marja (foyda ulushi)</span><b>${c.margin===null?'—':c.margin+'%'}</b><span class="mu" style="font-size:12px">o‘tgan oy foydasi ${sg(B.profit)}</span></div><div><span class="mu">Foyda o‘zgarishi</span><b class="${c.dProfit>0?'in-c':c.dProfit<0?'out-c':''}">${pc(c.dProfit)}</b><span class="mu" style="font-size:12px">o‘tgan oyga nisbatan</span></div></div>
   <p style="margin:10px 0 4px">Savdo bo‘lgan kunlar: <b>${c.sale}</b>${c.el?` / ${c.el}`:''}${c.noSale?` · savdosiz kun: <b>${c.noSale}</b>`:''}. Savdo kunidagi o‘rtacha daromad: <b>${num(c.avgSale)}</b> so‘m.</p>
   ${c.proj?`<p class="mu" style="margin:0 0 4px">Shu sur‘atda oy oxirigacha daromad ≈ <b>${num(c.proj)}</b> so‘m.</p>`:''}
   ${c.best?`<p style="margin:0 0 2px">🔝 Eng yaxshi kun: <b>${dfyDay(c.best[0])}</b>, daromad ${num(c.best[1].i)}.</p>`:''}${c.worst?`<p style="margin:0 0 2px">📉 Eng past savdo kuni: <b>${dfyDay(c.worst[0])}</b>, daromad ${num(c.worst[1].i)}.</p>`:''}
   ${c.lossDays?`<p class="mu" style="margin:0 0 2px">Chiqimi daromaddan ko‘p bo‘lgan kunlar: ${c.lossDays} ta.</p>`:''}
   ${c.bestW>=0?`<p style="margin:8px 0 4px">Hafta kunlari bo‘yicha o‘rtacha daromad (eng kuchli: <b>${DFYW[c.bestW]}</b>)</p><div class="bars2" style="height:70px;gap:6px">${c.avg.map((v,i)=>`<i style="height:${Math.max(2,v/mx*64)}px;${i===c.bestW?'':'opacity:.55'}"></i>`).join('')}</div><div style="display:flex;gap:6px">${DFYW.map(n=>`<span class="mu" style="flex:1;text-align:center;font-size:10px">${n.slice(0,2)}</span>`).join('')}</div>`:''}
   </div>`}
