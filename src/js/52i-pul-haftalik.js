// ---- PUL: haftalik takroriy daromad/xarajat (kunlar bo'yicha) va Daromad rejasi ($ maqsad bilan). Prefiks: drj ----
const DRJD=['Du','Se','Ch','Pa','Ju','Sh','Ya'];
const drjS=()=>{finInit();const f=S.fin;f.wr=f.wr||[];return f};
const drjNext=d=>new Date(new Date(d+'T12:00').getTime()+864e5).toLocaleDateString('sv');
const drjDow=d=>(new Date(d+'T12:00').getDay()+6)%7;
const drjOrd=d=>Math.floor(new Date(d+'T12:00').getTime()/864e5)-18262;
// deterministik id: ikki qurilma bir xil yozuvni yaratsa, birlashtirishda takrorlanmaydi
const drjId=(r,d)=>2e15+r.seq*1e5+drjOrd(d);
function drjRun(){
  const f=S.fin;if(!f||!Array.isArray(f.wr)||!f.wr.length)return;const td=dk();if(f.wrd===td)return;f.wrd=td;let made=0;
  f.wr.forEach(r=>{if(!r.on)return;let d=r.last?drjNext(r.last):r.from,g=0;
    while(d<=td&&g++<400){if(r.days.includes(drjDow(d))){const id=drjId(r,d);if(!S.money.some(m=>m.id===id)){S.money.push({id,d,k:r.k,a:r.a,ac:r.ac||'cash',n:r.n||'',w:r.w||'p',c:r.c||(r.k==='in'?CIN[0]:CATS[0]),wr:r.id});made++}}r.last=d;d=drjNext(d)}});
  if(made)setTimeout(save,50)}
function drjMk(k,a,n,days,c,ac){const f=drjS();f.wrn=(f.wrn||0)+1;f.wr.push({id:Date.now()+f.wrn,seq:f.wrn,k,a,n,days,c,ac:ac||'cash',on:1,w:'p',from:dk(),last:''})}
function drjAdd(){
  const a=sfn(V('drja')),days=[...document.querySelectorAll('#app .drjd:checked')].map(x=>+x.value);
  if(!(a>0)){toast('Summani yozing');return}if(!days.length){toast('Kamida bitta kun tanlang');return}
  const k=V('drjk')||'in',cs=k==='in'?CIN:CATS;drjMk(k,a,V('drjn').slice(0,40),days,cs[+V('drjc')]||cs[0],V('drjac')||'cash');
  S.fin.wrd='';save()}
function drjDel(id){if(!confirm('Takroriy qoida o‘chirilsinmi? (oldin yozilgan yozuvlar qoladi)'))return;const f=drjS();f.wr=f.wr.filter(r=>r.id!==id);save()}
function drjTog(id){const r=drjS().wr.find(x=>x.id===id);if(!r)return;r.on=r.on?0:1;if(r.on){r.from=dk();r.last=''}S.fin.wrd='';save()}
function drjPreset(w){const set=w==='all'?[0,1,2,3,4,5,6]:w==='wd'?[0,1,2,3,4]:[5,6];document.querySelectorAll('#app .drjd').forEach(x=>{x.checked=set.includes(+x.value)})}
function drjSample(){const f=drjS();if(f.wr.length&&!confirm('Mavjud qoidalarga yana 4 ta namuna qo‘shiladi. Davom etasizmi?'))return;
  drjMk('in',75000,'Ishxona (50 000 + tushlik 25 000)',[0,1,2,3,4,5,6],CIN[0]);drjMk('in',70000,'Dadam',[0,1,2,3,4],CIN[3]);
  drjMk('out',37000,'Ovqat',[0,1,2,3,4,5,6],CATS[0]);drjMk('out',27000,'Yo‘lkira',[0,1,2,3,4,5,6],CATS[1]);f.wrd='';save();toast('Namuna qo‘shildi: summalarni o‘zingizga moslab o‘chirib qayta yozing')}
function drjSet(k,v){const f=drjS();f.pl=f.pl||{};f.pl[k]=sfn(v);save()}
function drjPlan(){const f=drjS(),on=f.wr.filter(r=>r.on),wk=k=>on.filter(r=>r.k===k).reduce((s,r)=>s+r.a*r.days.length,0),i=wk('in'),o=wk('out'),pl=f.pl||{},pc=pl.pc>0?pl.pc:30,mi=Math.round(i*30.4/7),sv=Math.round(mi*pc/100),goal=(pl.usd||0)*(pl.rate||0),g=(f.sg||[]).find(x=>x.usd),have=g?g.s:0,rem=Math.max(0,goal-have);
  return{wi:i,wo:o,wn:i-o,mi,mo:Math.round(o*30.4/7),pc,sv,goal,have,rem,eta:(rem>0&&sv>0)?Math.ceil(rem/sv):0,g}}
function drjGoal(){const f=drjS(),pl=f.pl||{};if(!(pl.usd>0)||!(pl.rate>0)){toast('Avval $ summa va kursni yozing');return}
  const a=pl.usd*pl.rate;let g=(f.sg||[]).find(x=>x.usd);if(g){g.a=a;g.t='Maqsad: $'+num(pl.usd);g.usd=pl.usd}else{f.sg.push({id:Date.now(),t:'Maqsad: $'+num(pl.usd),a,s:0,e:'💎',dl:'',h:[],cr:dk(),usd:pl.usd})}toast('Jamg‘arma maqsadi: '+num(a)+' so‘m');save()}
function drjUi(){
  if(W!=='p')return '';const f=drjS(),P=drjPlan(),pl=f.pl||{},esc2=esc;
  const rows=k=>f.wr.filter(r=>r.k===k).map(r=>`<div class="row" style="${r.on?'':'opacity:.5'}"><span style="font-size:20px">${k==='in'?'⬆️':'⬇️'}</span><span class="t"><b>${num(r.a)}</b> · ${esc2(r.n||(r.c||''))}<br><span class="mu" style="font-size:12px">${r.days.length===7?'Har kuni':r.days.length===5&&r.days.every(d=>d<5)?'Du–Ju':r.days.map(d=>DRJD[d]).join(', ')} · ${r.ac==='card'?'💳':'💵'}</span></span><button class="x" onclick="drjTog(${r.id})" aria-label="To‘xtatish">${r.on?'⏸':'▶'}</button><button class="x" onclick="drjDel(${r.id})">×</button></div>`).join('')||'<p class="mu" style="margin:4px 0;font-size:13px">Hali yo‘q.</p>';
  const pcs=[20,25,30,40].map(p=>`<button class="${P.pc===p?'on':''}" onclick="drjSet('pc','${p}')">${p}%</button>`).join('');
  return `<h2>📅 Daromad rejasi</h2><div class="goal"><p class="mu" style="margin:0 0 8px;font-size:13px">Har kuni yoki hafta kunlari bo‘yicha keladigan daromad va xarajatingni bir marta yoz: ilova o‘zi shu kunlarda yozuv qo‘shib boradi.</p>
   <b>Daromad</b>${rows('in')}<b style="display:block;margin-top:10px">Xarajat</b>${rows('out')}
   <details class="sd" ${f.wr.length?'':'open'}><summary>＋ Yangi takroriy qoida</summary><div class="in" style="margin-top:8px"><select id="drjk" onchange="document.getElementById('drjc').innerHTML=(this.value==='in'?CIN:CATS).map((c,i)=>'<option value=\\''+i+'\\'>'+c+'</option>').join('')"><option value="in">Daromad</option><option value="out">Xarajat</option></select><input id="drja" type="text" inputmode="numeric" placeholder="Summa, so‘m"></div>
   <div class="in"><select id="drjc">${CIN.map((c,i)=>`<option value="${i}">${c}</option>`).join('')}</select><select id="drjac" style="flex:0 0 96px"><option value="cash">Naqd</option><option value="card">Karta</option></select></div><div class="in"><input id="drjn" placeholder="Izoh (masalan: Dadam)"></div>
   <div class="rwch" style="margin:6px 0">${DRJD.map((n,i)=>`<label class="chip" style="border:0;cursor:pointer"><input type="checkbox" class="drjd" value="${i}" ${i<5?'checked':''} style="margin-right:4px">${n}</label>`).join('')}</div>
   <div class="in"><button class="btn s" onclick="drjPreset('all')">Har kuni</button><button class="btn s" onclick="drjPreset('wd')">Du–Ju</button><button class="btn s" onclick="drjPreset('we')">Dam olish</button></div><button class="btn" style="width:100%" onclick="drjAdd()">Qo‘shish</button></details>
   <button class="btn s" style="margin-top:8px" onclick="drjSample()">Namuna qoidalarni qo‘shish</button><p class="mu" style="margin:6px 0 0;font-size:12px">Ishxona 75 000 (har kuni), dadam 70 000 (Du–Ju), ovqat 37 000, yo‘lkira 27 000. Keyin o‘zingizga moslab o‘zgartirasiz.</p></div>
  ${f.wr.length?`<div class="sum"><div><span class="mu">Haftalik daromad</span><b class="in-c">${num(P.wi)}</b></div><div><span class="mu">Haftalik xarajat</span><b class="out-c">${num(P.wo)}</b></div><div><span class="mu">Oylik daromad (≈)</span><b>${num(P.mi)}</b></div><div><span class="mu">Oylik xarajat (≈)</span><b>${num(P.mo)}</b></div><div class="w"><span class="mu">Qoladigan pul (haftasiga)</span><b class="${P.wn>=0?'in-c':'out-c'}">${P.wn<0?'−':''}${num(Math.abs(P.wn))} so‘m</b></div></div>`:''}
  <div class="goal"><b>🎯 Dollar maqsadi</b><div class="in" style="margin-top:8px"><input type="text" inputmode="numeric" placeholder="Maqsad, $" value="${pl.usd||''}" onchange="drjSet('usd',this.value)"><input type="text" inputmode="numeric" placeholder="Kurs: 1$ = so‘m" value="${pl.rate||''}" onchange="drjSet('rate',this.value)"></div>
   <p class="mu" style="margin:0 0 4px;font-size:12px">Kursni o‘zing yoz (Markaziy bank kursi); ilova uni tekshirmaydi.</p>
   <p class="mu" style="margin:8px 0 4px;font-size:13px">Daromaddan necha foizni jamg‘arasan?</p><div class="seg">${pcs}</div>
   ${P.goal?`<p style="margin:8px 0 0">Maqsad: <b>${num(P.goal)}</b> so‘m. Oyiga ${P.pc}% = <b>${num(P.sv)}</b> so‘m jamg‘arsang, ${P.eta?`<b>~${P.eta} oyda</b> yetasan.`:P.rem<=0?'maqsadga yetgansan! 🎉':'daromad rejasini kiriting.'}</p><button class="btn" style="margin-top:8px;width:100%" onclick="drjGoal()">${P.g?'Jamg‘arma maqsadini yangilash':'Jamg‘arma maqsadi qilib qo‘shish'}</button>`:'<p class="mu" style="margin:8px 0 0">$ va kursni yozsang, necha oyda yetishing hisoblanadi.</p>'}</div>`}
