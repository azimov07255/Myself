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
  ${drjEnvUi()}<div class="goal"><b>🎯 Dollar maqsadi</b><div class="in" style="margin-top:8px"><input type="text" inputmode="numeric" placeholder="Maqsad, $" value="${pl.usd||''}" onchange="drjSet('usd',this.value)"><input type="text" inputmode="numeric" placeholder="Kurs: 1$ = so‘m" value="${pl.rate||''}" onchange="drjSet('rate',this.value)"></div>
   <p class="mu" style="margin:0 0 4px;font-size:12px">Kursni o‘zing yoz (Markaziy bank kursi); ilova uni tekshirmaydi.</p>
   <p class="mu" style="margin:8px 0 4px;font-size:13px">Daromaddan necha foizni jamg‘arasan?</p><div class="seg">${pcs}</div>
   ${P.goal?`<p style="margin:8px 0 0">Maqsad: <b>${num(P.goal)}</b> so‘m. Oyiga ${P.pc}% = <b>${num(P.sv)}</b> so‘m jamg‘arsang, ${P.eta?`<b>~${P.eta} oyda</b> yetasan.`:P.rem<=0?'maqsadga yetgansan! 🎉':'daromad rejasini kiriting.'}</p><button class="btn" style="margin-top:8px;width:100%" onclick="drjGoal()">${P.g?'Jamg‘arma maqsadini yangilash':'Jamg‘arma maqsadi qilib qo‘shish'}</button>`:'<p class="mu" style="margin:8px 0 0">$ va kursni yozsang, necha oyda yetishing hisoblanadi.</p>'}</div>${drjQUi()}`}

// ---- haftalik konvertlar, "agar tejasam?" kalkulyatori, juma jamg'arma marosimi ----
const drjAddD=(d,n)=>new Date(new Date(d+'T12:00').getTime()+n*864e5).toLocaleDateString('sv');
const drjWk=(d)=>{const x=new Date((d||dk())+'T12:00');x.setDate(x.getDate()-drjDow(d||dk()));return x.toLocaleDateString('sv')};
function drjEnv(){const f=drjS(),e=f.env||{},wk=drjWk(),we=drjAddD(wk,6),sp={};
  S.money.forEach(m=>{if(m.w==='p'&&m.k==='out'&&m.d>=wk&&m.d<=we){const c=m.c||'Boshqa';sp[c]=(sp[c]||0)+m.a}});
  const left=7-drjDow(dk());
  return Object.keys(e).map(c=>({c,lim:e[c],sp:sp[c]||0,pc:e[c]?Math.round((sp[c]||0)/e[c]*100):0,left:e[c]-(sp[c]||0),perDay:Math.floor((e[c]-(sp[c]||0))/left),dl:left}))}
function drjEnvPlan(){const f=drjS();f.env={};f.wr.filter(r=>r.on&&r.k==='out').forEach(r=>{f.env[r.c]=(f.env[r.c]||0)+r.a*r.days.length});if(!Object.keys(f.env).length){toast('Avval xarajat qoidalarini qo‘shing');return}save()}
function drjEnvSet(){const a=sfn(V('drje')),c=CATS[+V('drjec')];if(!(a>0)){toast('Summani yozing');return}const f=drjS();f.env=f.env||{};f.env[c]=a;save()}
function drjEnvDel(c){const f=drjS();if(f.env)delete f.env[c];save()}
function drjEnvUi(){const L=drjEnv();
  const bar=x=>{const col=x.pc>=100?'var(--bad)':x.pc>=80?'#d9a441':'var(--ac)';return `<div style="margin-bottom:10px"><div style="display:flex;justify-content:space-between"><span>${CI[x.c]||''} ${esc(x.c)}</span><span class="mu">${num(x.sp)} / ${num(x.lim)}</span></div><div class="bar" style="margin:4px 0"><i style="width:${Math.min(100,x.pc)}%;background:${col}"></i></div><span class="mu" style="font-size:12px">${x.left>=0?'Qoldi '+num(x.left)+(x.dl>0?', kuniga ~'+num(Math.max(0,x.perDay)):''):'<b style="color:var(--bad)">Chegaradan '+num(-x.left)+' oshdi</b>'}</span><button class="x" style="float:right" onclick="drjEnvDel('${x.c}')" aria-label="O‘chirish">×</button></div>`};
  return `<h2>🧾 Haftalik konvertlar</h2><div class="goal"><p class="mu" style="margin:0 0 8px;font-size:13px">Har kategoriya uchun haftalik chegara (dushanbadan yakshanbagacha). Daromading haftalik kelgani uchun oylikdan qulayroq.</p>${L.length?L.map(bar).join(''):'<p class="mu" style="margin:0 0 8px">Hali konvert yo‘q.</p>'}
   <button class="btn s" onclick="drjEnvPlan()">Xarajat qoidalaridan to‘ldirish</button>
   <div class="in" style="margin-top:8px"><select id="drjec">${CATS.map((c,i)=>`<option value="${i}">${c}</option>`).join('')}</select><input id="drje" type="text" inputmode="numeric" placeholder="Haftalik, so‘m"><button class="btn" onclick="drjEnvSet()">+</button></div></div>`}
// agar tejasam?
function drjWhatIf(q){const P=drjPlan();if(!P.goal||P.rem<=0||P.sv<=0)return null;const extra=Math.round(q*30.4),sv2=P.sv+extra,mo=Math.ceil(P.rem/sv2);return{extra,sv2,mo,saved:Math.max(0,P.eta-mo)}}
function drjQ(v){const e=document.getElementById('drjqo'),l=document.getElementById('drjql');if(!e)return;const q=+v||0;if(l)l.textContent=num(q);const w=drjWhatIf(q);e.textContent=w?(q?'Oyiga +'+num(w.extra)+' so‘m. Maqsadga ~'+w.mo+' oyda yetasan'+(w.saved?' (':'')+(w.saved?w.saved+' oy erta)':''):'Hozirgi sur‘at bilan ~'+drjPlan().eta+' oy'):'Avval $ maqsad va kursni yozing.'}
function drjQUi(){const P=drjPlan();if(!P.goal)return '';return `<div class="goal"><b>💡 Agar tejasam?</b><p class="mu" style="margin:6px 0 8px;font-size:13px">Kuniga qancha tejasang (yo‘lkira, ovqat…), maqsadga necha oy erta yetasan?</p><div style="display:flex;justify-content:space-between"><span>Kuniga tejayman</span><b><span id="drjql">0</span> so‘m</b></div><input type="range" min="0" max="30000" step="1000" value="0" style="width:100%" oninput="drjQ(this.value)" aria-label="Kuniga tejash"><p id="drjqo" style="margin:6px 0 0">${P.eta?'Hozirgi sur‘at bilan ~'+P.eta+' oy':P.rem<=0?'Maqsadga yetgansan! 🎉':''}</p></div>`}
// juma jamg'arma marosimi
function drjJz(){const f=drjS(),P=drjPlan();f.jz=f.jz||{};const wk=drjWk(),weekly=Math.round(P.sv*7/30.4);
  let st=0,w=f.jz[wk]?wk:drjAddD(wk,-7);while(f.jz[w]&&st<520){st++;w=drjAddD(w,-7)}
  return{wk,weekly,done:f.jz[wk]||0,streak:st,dow:drjDow(dk()),P}}
function drjSaveWeek(){const f=drjS(),J=drjJz(),g=J.P.g;if(!g){toast('Avval jamg‘arma maqsadini qo‘shing');return}if(J.done)return;
  const a=sfn(V('drjws'))||J.weekly;if(!(a>0)){toast('Summani yozing');return}g.s+=a;(g.h=g.h||[]).push({d:dk(),a});g.h=g.h.slice(-60);f.jz[J.wk]=a;toast('💎 Jamg‘arma: +'+num(a)+' so‘m');save()}
function drjUnsave(){const f=drjS(),J=drjJz(),g=J.P.g;if(!J.done||!g)return;g.s=Math.max(0,g.s-J.done);g.h=(g.h||[]).filter((x,i,a)=>!(i===a.length-1&&x.a===J.done));delete f.jz[J.wk];save()}
function drjJzUi(){const J=drjJz();if(!J.P.g||!(J.weekly>0))return '';
  const fri=J.dow>=4,day=['dushanba','seshanba','chorshanba','payshanba','juma','shanba','yakshanba'];
  return `<div class="goal" style="border-left:4px solid var(--go)"><div class="h"><b>💎 Haftalik jamg‘arma</b>${J.streak?`<span class="chip">🔥 ${J.streak} hafta ketma-ket</span>`:''}</div>
   ${J.done?`<p style="margin:6px 0">Bu hafta <b>${num(J.done)}</b> so‘m jamg‘arding. Barakalla! 👏</p><button class="btn s" onclick="drjUnsave()">Bekor qilish</button>`
   :`<p style="margin:6px 0 8px">${fri?'<b>Bugun jamg‘arma kuni.</b> ':'Jamg‘arma kuni: juma ('+(4-J.dow)+' kun qoldi). '}Bu hafta rejadagi summa: <b>${num(J.weekly)}</b> so‘m.</p><div class="in"><input id="drjws" type="text" inputmode="numeric" value="${J.weekly}"><button class="btn" onclick="drjSaveWeek()">Jamg‘armaga o‘tkazdim</button></div>`}</div>`}
function drjHome(){if(W!=='p')return '';const f=drjS();let h=drjJzUi();const E=drjEnv();if(E.length)h+=`<div class="goal"><b>🧾 Bu hafta konvertlari</b>${E.map(x=>{const col=x.pc>=100?'var(--bad)':x.pc>=80?'#d9a441':'var(--ac)';return `<div class="usr" style="margin-top:8px"><span class="usk" style="flex-basis:96px">${CI[x.c]||''} ${esc(x.c)}</span><span class="usb"><i style="width:${Math.min(100,x.pc)}%;background:${col}"></i></span><span class="usv">${x.left>=0?num(x.left):'−'+num(-x.left)}</span></div>`}).join('')}<p class="mu" style="margin:6px 0 0;font-size:12px">Qolgan summa shu hafta uchun.</p></div>`;return h}
