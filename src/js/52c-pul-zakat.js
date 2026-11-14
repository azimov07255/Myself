// ---- PUL: zakat va sadaqa hisoblagich. Taxminiy yordamchi: aniq masala uchun imomga murojaat qiling. Prefiks: zkt ----
const ZKT_G=85,ZKT_S=595,ZKT_R=0.025,ZKT_HAWL=354;   // nisob: 85 g oltin yoki 595 g kumush; stavka 2,5%; hijriy yil ≈ 354 kun
const zktS=()=>{finInit();const f=S.fin;f.zk=f.zk||{};const z=f.zk;if(!z.b)z.b='g';if(!Array.isArray(z.p))z.p=[];return z};
function zktSet(k,v){const z=zktS();if(k==='pg'||k==='ps'||k==='x'||k==='sg')z[k]=sfn(v);else if(k==='d')z.d=v?1:0;else z[k]=v;save()}
function zktBasis(b){zktS().b=b;save()}
// qarz hisobi (sof boylik bilan bir xil qoida: faqat balansga ta'sir qiladigan qarzlar)
function zktDebts(){let rec=0,pay=0;(S.debts||[]).forEach(d=>{if(d.led===false||d.st==='closed')return;const r=dRem(d);if(d.k==='lend')rec+=r;else pay+=r});return{rec,pay}}
function zktCalc(){
  const z=zktS(),price=z.b==='s'?z.ps||0:z.pg||0,grams=z.b==='s'?ZKT_S:ZKT_G,nisob=price*grams;
  const cash=bal('p').tot+(z.d?bal('d').tot:0),D=zktDebts(),extra=z.x||0,wealth=cash+D.rec-D.pay+extra;
  const o={z,price,grams,nisob,cash,rec:D.rec,pay:D.pay,extra,wealth,ok:price>0,reached:price>0&&wealth>=nisob};
  o.due=o.reached?Math.round(wealth*ZKT_R):0;
  if(z.h){const end=new Date(new Date(z.h+'T12:00:00').getTime()+ZKT_HAWL*864e5).toLocaleDateString('sv');o.end=end;o.left=dl(end);o.hawl=o.left<=0}
  o.paid=(z.p||[]).filter(x=>!z.h||x.d>=z.h).reduce((a,x)=>a+x.a,0);o.rest=Math.max(0,o.due-o.paid);
  return o}
function zktStart(){const z=zktS();z.h=dk();z.p=z.p||[];save()}
function zktDate(v){const z=zktS();z.h=v||'';save()}
function zktReset(){if(!confirm('Yangi hawl boshlansinmi? Eski hawl sanasi tozalanadi (to‘lovlar tarixi saqlanadi).'))return;const z=zktS();z.h='';save()}
function zktPay(){const a=sfn(V('zktp')),ac=V('zkta')||'cash';if(!a){toast('Summani yozing');return}
  const z=zktS(),d=dk();z.p.push({id:Date.now(),d,a});z.p=z.p.slice(-40);
  putM({id:Date.now()+1,d,k:'out',a,ac,n:'Zakot',w:'p',c:'Sadaqa',z:1});toast('Zakot qayd etildi: '+num(a)+' so‘m 🤲');save()}
function zktPayDel(id){const z=zktS();z.p=z.p.filter(x=>x.id!==id);save()}
// sadaqa statistikasi (zakot yozuvlari alohida: z:1)
function zktSad(){const mk=mKey(0).k,y=String(new Date().getFullYear()),L=S.money.filter(m=>m.w==='p'&&m.k==='out'&&m.c==='Sadaqa'&&!m.z),inc=mSum(mList('p',mk),'in');
  const mo=L.filter(m=>m.d.startsWith(mk)).reduce((a,m)=>a+m.a,0),yr=L.filter(m=>m.d.startsWith(y)).reduce((a,m)=>a+m.a,0),zk=S.money.filter(m=>m.w==='p'&&m.z&&m.d.startsWith(y)).reduce((a,m)=>a+m.a,0);
  return{mo,yr,zk,inc,pc:inc?Math.round(mo/inc*100):null}}
function zktUi(){
  const o=zktCalc(),z=o.z,S2=zktSad(),sg=z.sg||0,sp=sg?Math.min(100,Math.round(S2.mo/sg*100)):0,bs=z.b==='s',
    pr=bs?'Kumush narxi (1 gramm), so‘m':'Oltin narxi (1 gramm), so‘m';
  const row=(t,v,c)=>`<div class="usr"><span class="usk" style="flex:1">${t}</span><span class="usv ${c||''}" style="min-width:110px;text-align:right">${v}</span></div>`;
  let res='';
  if(!o.ok)res=`<p class="mu" style="margin:8px 0 0">Nisobni hisoblash uchun ${bs?'kumush':'oltin'} narxini yoz (1 gramm, bugungi kurs).</p>`;
  else if(!o.reached)res=`<p style="margin:10px 0 4px"><b>Nisobga yetmagan.</b> Kerak: ${num(o.nisob)} so‘m, sende: ${num(Math.max(0,o.wealth))} (${Math.max(0,Math.round(o.wealth/o.nisob*100))}%). Hozircha zakot farz emas.</p><div class="bar"><i style="width:${Math.max(0,Math.min(100,o.wealth/o.nisob*100))}%"></i></div>`;
  else res=`<p style="margin:10px 0 4px"><b>Nisobga yetgan.</b> Taxminiy zakot: <b style="font:700 20px Fraunces,serif">${num(o.due)} so‘m</b> <span class="mu">(${num(o.wealth)} × 2,5%)</span></p>
   ${z.h?`<p class="mu" style="margin:0 0 6px">Hawl boshi: ${esc(dU(z.h))}. ${o.hawl?'<b style="color:var(--ac)">Hawl to‘ldi, zakot berish vaqti.</b>':'Hawl to‘lishiga <b>'+o.left+' kun</b> qoldi ('+esc(dU(o.end))+').'}</p>
   <p style="margin:0 0 8px">Berilgan: <b>${num(o.paid)}</b> · Qolgan: <b>${num(o.rest)}</b> so‘m</p>
   <div class="in"><input id="zktp" type="text" inputmode="numeric" placeholder="Zakot berdim, so‘m"><select id="zkta" style="flex:0 0 96px"><option value="cash">Naqd</option><option value="card">Karta</option></select><button class="btn" onclick="zktPay()">+</button></div>
   ${(z.p||[]).length?`<p class="mu" style="margin:6px 0 0;font-size:12px">To‘lovlar: ${z.p.slice(-6).map(x=>x.d.slice(8)+'.'+x.d.slice(5,7)+' '+num(x.a)+' <button class="x" style="display:inline;padding:0 4px" onclick="zktPayDel(${x.id})">×</button>').join(', ')}</p>`:''}
   <div class="in" style="margin-top:8px"><button class="btn s" onclick="zktReset()" style="font-size:13px">Yangi hawl boshlash</button></div>`
   :`<p class="mu" style="margin:0 0 8px">Zakot nisobga yetgan pul ustidan to‘liq bir qamariy yil (≈354 kun) o‘tgandan keyin beriladi. Pul nisobga qachon yetganini belgila, ilova hawlni sanaydi.</p><div class="in"><button class="btn" style="flex:1" onclick="zktStart()">Hawl bugundan boshlansin</button></div><div class="in"><input type="date" onchange="zktDate(this.value)"><span class="mu" style="align-self:center;white-space:nowrap">yoki sanani tanla</span></div>`}`;
  return `<h2>🕌 Zakot hisobi</h2><div class="goal"><p class="mu" style="margin:0 0 8px;font-size:13px">Taxminiy hisob: nisob ${ZKT_G} g oltin yoki ${ZKT_S} g kumush qiymati, stavka 2,5%. Mazhab va mahalliy idoraga qarab farq qilishi mumkin; aniq masala uchun imomga murojaat qiling.</p>
   <div class="seg" style="margin-bottom:8px"><button class="${bs?'':'on'}" onclick="zktBasis('g')">Oltin (${ZKT_G} g)</button><button class="${bs?'on':''}" onclick="zktBasis('s')">Kumush (${ZKT_S} g)</button></div>
   <div class="in"><input type="text" inputmode="numeric" placeholder="${pr}" value="${(bs?z.ps:z.pg)||''}" onchange="zktSet('${bs?'ps':'pg'}',this.value)"></div>
   <div class="in"><input type="text" inputmode="numeric" placeholder="Ilovada yo‘q boylik (oltin, dollar...), so‘m" value="${z.x||''}" onchange="zktSet('x',this.value)"></div>
   <label class="mu" style="display:flex;gap:8px;align-items:center;margin:4px 0 8px;font-size:13px"><input type="checkbox" ${z.d?'checked':''} onchange="zktSet('d',this.checked)"> Do‘kon hamyonini ham hisobga ol</label>
   ${o.ok?`<div style="margin:6px 0">${row('Naqd va karta',num(o.cash))}${o.extra?row('Ilovada yo‘q boylik','+'+num(o.extra)):''}${o.rec?row('Menga qarzdor','+'+num(o.rec)):''}${o.pay?row('Men qarzdorman','−'+num(o.pay)):''}${row('<b>Jami</b>','<b>'+num(o.wealth)+'</b>')}${row('Nisob ('+o.grams+' g)',num(o.nisob))}</div>`:''}${res}</div>
  <h2>🤲 Sadaqa</h2><div class="sum"><div><span class="mu">Shu oy</span><b>${num(S2.mo)}</b><span class="mu" style="font-size:12px">${S2.pc!==null?'daromadning '+S2.pc+'%i':'daromad yozilmagan'}</span></div><div><span class="mu">Shu yil</span><b>${num(S2.yr)}</b><span class="mu" style="font-size:12px">zakot: ${num(S2.zk)}</span></div></div>
   <div class="goal"><b>Oylik sadaqa maqsadi</b><div class="in" style="margin-top:8px"><input type="text" inputmode="numeric" placeholder="Oyiga, so‘m" value="${sg||''}" onchange="zktSet('sg',this.value)"></div>${sg?`<div class="usr"><span class="usb"><i style="width:${sp}%"></i></span><span class="usv">${num(S2.mo)} / ${num(sg)}</span></div>`:'<p class="mu" style="margin:0;font-size:13px">Maqsad qo‘ysang, shu oy qancha berganing ko‘rinadi.</p>'}</div>`}
