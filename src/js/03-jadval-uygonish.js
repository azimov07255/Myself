// ---- Jadval (tahrirlanadigan) ----
const bl=()=>S.bl||BL;
const t2m=s=>{const p=String(s||'0:0').split(':').map(Number);return p[0]*60+p[1]};
function eb(i){BV='j';const b=i>=0?bl()[i]:null;ED=b?{i,t:b.t,n:b.n||'',s:hm(b.s),e:hm(b.e),pt:!!b.pt,d:[...b.d],on:b.on||'',tr:b.tr||0,ty:rjTy(b),fx:rjFx(b)?1:0}:{i:-1,t:'',n:'',s:'09:00',e:'10:00',pt:0,d:[1,2,3,4,5],on:'',tr:0,ty:'boshqa',fx:0};render();scrollTo(0,0)}
function ed(i){const d=ED.d,j=d.indexOf(i);j<0?d.push(i):d.splice(j,1);render()}
function esv(){
  if(!ED.t.trim())return alert('Reja nomini yozing.');
  if(!ED.d.length)return alert('Kamida bitta kunni tanlang.');
  if(!ED.s)return alert('Boshlanish vaqtini kiriting.');
  if(!ED.pt&&!ED.e)return alert('Tugash vaqtini kiriting. Tugash vaqti bo‘lmaydigan reja uchun “Bir lahzalik”ni tanlang.');
  const s=t2m(ED.s);let e;if(ED.pt)e=s+15;else{e=t2m(ED.e);if(e<=s)e+=1440}
  const L=bl().map(b=>({...b})),o={id:ED.i>=0?L[ED.i].id:'n'+Date.now(),t:ED.t.trim(),n:ED.n,s,e,pt:!!ED.pt,d:ED.on?[new Date(ED.on+'T12:00').getDay()]:ED.d,ty:ED.ty||'boshqa',fx:ED.fx?1:0};if(ED.on)o.on=ED.on;if(ED.tr)o.tr=ED.tr;
  if(!rjSaveOk(o))return;
  if(ED.i>=0)L[ED.i]=o;else L.push(o);S.bl=L;ED=null;save()}
function edl(){if(!confirm('Reja o‘chirilsinmi?'))return;const L=bl().map(b=>({...b}));L.splice(ED.i,1);S.bl=L;ED=null;save()}
function edForm(){if(!ED)return ''; const once=!!ED.on,days=[1,2,3,4,5,6,0].map(i=>`<button class="${ED.d.includes(i)?'on':''}" onclick="ed(${i})" aria-pressed="${ED.d.includes(i)}">${DAYS[i].slice(0,2)}</button>`).join(''),
  tin=(l,f,v)=>`<div style="flex:1;min-width:0"><span class="mu" style="font-size:12px">${l}</span><input type="time" style="width:100%" value="${v}" oninput="ED.${f}=this.value" onchange="render()"></div>`,
  dur=ED.pt?'':`<div class="rwch" style="margin:8px 0 0">${[15,30,45,60,90,120,180].map(m=>`<button class="chip ${edDur()===m?'on':''}" style="border:0" onclick="edSetDur(${m})">${({15:'15 daq',30:'30 daq',45:'45 daq',60:'1 soat',90:'1,5 soat',120:'2 soat',180:'3 soat'})[m]}</button>`).join('')}</div>`,
  T0=dk(),T1=rwAdd(T0,1),T2=rwAdd(T0,2),
  when=once?`<div class="rwch" style="margin:0 0 8px">${[[T0,'Bugun'],[T1,'Ertaga'],[T2,'Indinga']].map(([d,l])=>`<button class="chip ${ED.on===d?'on':''}" style="border:0" onclick="edOnSet('${d}')">${l}</button>`).join('')}</div><div class="in"><input type="date" value="${esc(ED.on)}" min="${T0}" onchange="edOnSet(this.value)" aria-label="Sana"></div><p class="mu" style="margin:6px 0 0;font-size:12px">Bu reja faqat shu kunga qo‘shiladi va keyin o‘zi yo‘qoladi: haftalik rejang o‘zgarmaydi.</p>`:`<div class="seg" style="margin-bottom:8px">${days}</div><div class="rwch"><button class="chip" style="border:0" onclick="edPreset('ish')">Ish kunlari</button><button class="chip" style="border:0" onclick="edPreset('dam')">Dam kunlari</button><button class="chip" style="border:0" onclick="edPreset('har')">Har kuni</button></div>`;
  return `<div class="goal edf" style="margin-top:14px"><div class="h"><b>${ED.i>=0?'Rejani tahrirlash':'Yangi reja'}</b><button class="x" onclick="ED=null;render()" aria-label="Yopish">✕</button></div>
   <input class="edt" placeholder="Nomi, masalan: IELTS Writing" value="${esc(ED.t)}" oninput="ED.t=this.value" aria-label="Reja nomi">
   <p class="edl">Qachon?</p><div class="seg"><button class="${once?'':'on'}" onclick="edOnOff()">📅 Har hafta</button><button class="${once?'on':''}" onclick="eb1x()">📍 Faqat bir kun</button></div><div style="margin-top:8px">${when}</div>
   <p class="edl">Vaqt</p><div class="seg" style="margin-bottom:8px"><button class="${ED.pt?'':'on'}" onclick="ED.pt=0;render()">⏱ Vaqt oralig‘i</button><button class="${ED.pt?'on':''}" onclick="ED.pt=1;render()">📍 Bir lahzalik</button></div>
   <div class="in">${tin('Boshlanish','s',ED.s)}${ED.pt?'':tin('Tugash','e',ED.e)}</div>${dur}${ED.pt?'<p class="mu" style="margin:6px 0 0;font-size:13px">Tugash vaqti kerak bo‘lmagan reja uchun, masalan 05:00 da uyg‘onish.</p>':''}${edPv()}
   <div class="in" style="margin-top:8px"><input placeholder="Izoh (ixtiyoriy)" value="${esc(ED.n)}" oninput="ED.n=this.value"></div>${rjEdUi()}
   <div class="in" style="margin-top:12px"><button class="big" style="flex:2;margin:0" onclick="esv()">Saqlash</button><button class="btn s" onclick="ED=null;render()">Bekor</button>${ED.i>=0?'<button class="btn s" onclick="edl()" aria-label="O‘chirish">🗑</button>':''}</div></div>`}
// ---- Uyg‘onish tizimi ----
const dAgo=i=>new Date(Date.now()-i*864e5).toLocaleDateString('sv');
function tgtFor(k){const w=S.wk;const n=Math.floor((new Date(k)-new Date(w.start))/864e5/3);return Math.max(300,w.base-15*Math.max(0,n))}
function wkStart(){S.wk={base:t2m($('#wb').value||'07:00'),start:dk()};save()}
function wakeC(){
  const k=dk(),w=S.wk;
  if(!w.start)return `<div class="goal" style="margin-top:12px"><b>Uyg‘onish tizimi</b><p class="mu" style="margin:6px 0 10px">Hozir odatda soat nechada turasan? Maqsad 05:00 gacha har 3 kunda 15 daqiqadan suriladi.</p><div class="in"><input type="time" id="wb" value="07:00"><button class="btn" onclick="wkStart()">Boshlash</button></div></div>`;
  const tg_=tgtFor(k),got=S.wake[k],tom=tgtFor(dAgo(-1));
  let st=0;for(let i=0;i<90;i++){const v=S.wake[dAgo(i)];if(!v){if(i===0)continue;break}if(t2m(v)<=tgtFor(dAgo(i)))st++;else break}
  const msg=got?(t2m(got)<=tg_?`Turding ${got}. Maqsadga erishding.`:`Turding ${got}, ${t2m(got)-tg_} daqiqa kech.`):'';
  return `<div class="goal" style="margin-top:12px"><div class="h"><b>Uyg‘onish</b><span class="mu">${st} kun ketma-ket</span></div><p style="margin:6px 0 0;font:800 30px Fraunces,system-ui">${hm(tg_)}</p><p class="mu" style="margin:2px 0 8px">Bugungi maqsad. Ertaga: ${hm(tom)}</p>${got?`<p class="mu" style="margin:0">${msg}</p>`:`<button class="big" style="margin-top:6px" onclick="wk()">Turdim</button>`}<button class="x" style="font-size:13px;margin-top:8px" onclick="if(confirm('Qayta boshlansinmi?')){S.wk={base:0,start:null};save()}">Qayta boshlash</button></div>`}

