// ---- PUL: sof boylik (net worth) va oyma-oy trend. Hamma narsa mavjud yozuvlardan hisoblanadi (yangi ma'lumot saqlanmaydi). Prefiks: sbl ----
const sblWs=()=>(S.fin&&S.fin.nwd)?['p','d']:['p'];
function sblNwd(v){finInit();S.fin.nwd=v?1:0;save()}
// D sanasidagi holat. bal() bilan bir xil qoida: qarz boshlang'ich yozuvi faqat balansga ta'sir qilsa, to'lovlar har doim
function sblAt(D,ws){
  finInit();let cash=0,rec=0,pay=0;
  ws.forEach(w=>{const o=(S.fin.open&&S.fin.open[w])||{};cash+=(o.cash||0)+(o.card||0);
    S.money.forEach(m=>{if(m.w!==w||m.d>D)return;if(m.k==='in')cash+=m.a;else if(m.k==='out')cash-=m.a})});
  if(ws.includes('p'))(S.debts||[]).forEach(d=>{
    const bor=d.k==='borrow',paid=(d.pay||[]).filter(x=>x.d<=D).reduce((a,x)=>a+x.a,0),on=d.led!==false&&(d.d||'')<=D;
    if(on)cash+=bor?d.a:-d.a;
    cash+=bor?-paid:paid;
    if(on&&d.st!=='closed'){const r=Math.max(0,d.a-paid);if(bor)pay+=r;else rec+=r}});
  return{cash,rec,pay,nw:cash+rec-pay}}
function sblSeries(n){const ws=sblWs(),out=[],now=new Date();
  for(let i=n-1;i>=0;i--){const d=new Date(now.getFullYear(),now.getMonth()-i+1,0),D=i===0?dk():d.toLocaleDateString('sv');out.push(Object.assign({D,l:MON[d.getMonth()].slice(0,3)},sblAt(D,ws)))}
  return out}
function sblChart(s){
  const W0=300,H0=96,vals=s.map(x=>x.nw),mn=Math.min(...vals,0),mx=Math.max(...vals,0),rg=Math.max(1,mx-mn),px=i=>8+i*(W0-16)/Math.max(1,s.length-1),py=v=>6+(mx-v)/rg*(H0-12);
  const pts=s.map((x,i)=>px(i).toFixed(1)+','+py(x.nw).toFixed(1)).join(' ');
  return `<svg viewBox="0 0 ${W0} ${H0}" width="100%" role="img" aria-label="Sof boylik: so‘nggi 12 oy" style="display:block;margin:8px 0 2px;overflow:visible">${mn<0?`<line x1="8" x2="${W0-8}" y1="${py(0).toFixed(1)}" y2="${py(0).toFixed(1)}" stroke="var(--mu,#999)" stroke-dasharray="3 3" stroke-width="1" opacity=".6"/>`:''}<polyline points="${pts}" fill="none" stroke="var(--ac)" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>${s.map((x,i)=>`<circle cx="${px(i).toFixed(1)}" cy="${py(x.nw).toFixed(1)}" r="${i===s.length-1?4:2.4}" fill="var(--ac)"/>`).join('')}</svg>
   <div style="display:flex">${s.map(x=>`<span class="mu" style="flex:1;text-align:center;font-size:10px">${x.l}</span>`).join('')}</div>`}
const sblSgn=v=>(v>0?'+':v<0?'−':'')+num(Math.abs(v));
function sblUi(){
  const s=sblSeries(12),c=s[s.length-1],p=s[s.length-2],h=s[Math.max(0,s.length-7)],hasData=S.money.length||(S.debts||[]).length||sblWs().some(w=>{const o=(S.fin.open||{})[w]||{};return o.cash||o.card});
  const dm=c.nw-p.nw,d6=c.nw-h.nw,row=(t,v,cl)=>`<div class="usr"><span class="usk" style="flex:1">${t}</span><span class="usv ${cl||''}" style="min-width:120px;text-align:right">${v}</span></div>`;
  return `<h2>💎 Sof boylik</h2><div class="goal">${hasData?`<p style="margin:0"><b style="font:700 26px Fraunces,serif;word-break:break-all">${c.nw<0?'−':''}${num(Math.abs(c.nw))} so‘m</b></p>
   <p class="mu" style="margin:4px 0 0">O‘tgan oy oxiriga nisbatan <b class="${dm>=0?'in-c':'out-c'}">${sblSgn(dm)}</b>${s.length>=7?` · 6 oy oldinga nisbatan <b class="${d6>=0?'in-c':'out-c'}">${sblSgn(d6)}</b>`:''}</p>${sblChart(s)}
   <div style="margin:8px 0 4px">${row('Naqd va karta',num(c.cash))}${c.rec?row('Menga qarzdor','+'+num(c.rec),'in-c'):''}${c.pay?row('Men qarzdorman','−'+num(c.pay),'out-c'):''}${row('<b>Sof boylik</b>','<b>'+(c.nw<0?'−':'')+num(Math.abs(c.nw))+'</b>')}</div>
   <p class="mu" style="margin:4px 0 6px;font-size:12px">Sof boylik = naqd + karta + senga qarzdorlar − sen qarzdorlar. Jamg‘arma maqsadlaridagi pul ham shu summaga kiradi. Tarix yozuvlar sanasi bo‘yicha qayta hisoblanadi (hozirgi qoldiqni o‘zgartirsang, butun grafik shuncha siljiydi).</p>`
   :'<p class="mu" style="margin:0">Kirim-chiqim yoz: sof boylik va uning oyma-oy o‘zgarishi shu yerda chiqadi.</p>'}
   <label class="mu" style="display:flex;gap:8px;align-items:center;margin:4px 0 0;font-size:13px"><input type="checkbox" ${S.fin.nwd?'checked':''} onchange="sblNwd(this.checked)"> Do‘kon hamyonini ham qo‘sh</label></div>`}
