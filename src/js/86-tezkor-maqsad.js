// ---- ＋ TEZKOR REJA (tepada, sozlamalar yonida) va 📊 MAQSADGA AVTOMATIK PROGRESS (Qur'on hifzi / IELTS paneli maqsad kartasi ichida) ----
let QP=null;
const QPD=[15,30,45,60,90,120];
function qpOpen(){const now=rjMin(),s=Math.min(1425,Math.ceil((now+5)/15)*15);QP={t:'',d:dk(),s,m:30,ty:'boshqa'};qpDraw();setTimeout(()=>{const e=document.getElementById('qpt');if(e)e.focus()},60)}
function qpClose(){QP=null;const e=document.getElementById('qpv');if(e)e.remove()}
function qpSet(k,v){if(!QP)return;QP[k]=v;qpDraw()}
function qpTime(v){if(!QP||!/^\d\d:\d\d$/.test(v||''))return;QP.s=t2m(v);qpDraw()}
function qpDate(v){if(!QP||!/^\d{4}-\d\d-\d\d$/.test(v||'')||v<dk())return;QP.d=v;qpDraw()}
function qpBlock(){const A=QP,dw=new Date(A.d+'T12:00').getDay(),e=Math.min(1440,A.s+A.m);return{id:'qp'+Date.now()+Math.floor(Math.random()*999),t:String(A.t).trim().slice(0,60),s:A.s,e,d:[dw],on:A.d,ty:A.ty,fx:0}}
function qpAdd(){if(!QP)return;if(!String(QP.t).trim()){toast('Rejaning nomini yozing');return}if(QP.d<dk()){toast('O‘tgan kunga qo‘shib bo‘lmaydi');return}const b=qpBlock();if(b.e<=b.s){toast('Vaqt kunning oxiriga sig‘mayapti');return}
  const C=rjConfOf(rjDay(QP.d).concat([b])).filter(c=>c.a.id===b.id||c.b.id===b.id);if(C.length&&!confirm('⚠️ Bu reja boshqa reja bilan kesishadi:\n'+C.map(c=>'• '+(c.a.id===b.id?c.b.t:c.a.t)+' ('+hm(c.s)+'–'+hm(c.e)+')').join('\n')+'\n\nBaribir qo‘shilsinmi?'))return;
  S.bl=bl().concat([b]);const T=dk();qpClose();toast('✅ Qo‘shildi: '+b.t+' · '+hm(b.s)+'–'+hm(b.e)+(b.on===T?' (bugun)':b.on===rwAdd(T,1)?' (ertaga)':' ('+dU(b.on)+')'));save()}
function qpFull(){if(!QP)return;const A=QP;qpClose();eb(-1);ED.t=A.t;ED.s=hm(A.s);ED.e=hm(Math.min(1439,A.s+A.m));ED.on=A.d;ED.d=[new Date(A.d+'T12:00').getDay()];ED.ty=A.ty;ED.fx=0;go('h');render()}
function qpDraw(){let e=document.getElementById('qpv');if(!QP){if(e)e.remove();return}const A=QP,T=dk(),T1=rwAdd(T,1),first=!e;
  if(!e){e=document.createElement('div');e.id='qpv';e.className='nwo';e.setAttribute('role','dialog');e.setAttribute('aria-modal','true');e.setAttribute('aria-label','Tezkor reja qo‘shish');document.body.appendChild(e)}
  const kp=document.getElementById('qpt');
  e.innerHTML=`<div class="nwb" onclick="qpClose()"></div><div class="nws"><div class="h"><b>＋ Tezkor reja</b><button class="x" onclick="qpClose()" aria-label="Yopish">✕</button></div>
   <input id="qpt" placeholder="Nima qilasan? Masalan: Listening 1 soat" maxlength="60" value="${esc(A.t)}" style="width:100%;font-size:17px;margin:6px 0 8px" oninput="QP.t=this.value" onkeydown="if(event.key==='Enter')qpAdd()" aria-label="Reja nomi">
   <div class="rwch" style="margin-bottom:6px"><button class="chip ${A.d===T?'on':''}" style="border:0" onclick="qpSet('d','${T}')">Bugun</button><button class="chip ${A.d===T1?'on':''}" style="border:0" onclick="qpSet('d','${T1}')">Ertaga</button><input type="date" min="${T}" value="${esc(A.d)}" onchange="qpDate(this.value)" aria-label="Sana" style="flex:1;min-width:0"></div>
   <div class="in" style="margin:0 0 6px"><label class="mu" style="font-size:12px;flex:1">Boshlanish<input type="time" value="${hm(A.s)}" onchange="qpTime(this.value)" style="width:100%" aria-label="Boshlanish vaqti"></label></div>
   <div class="rwch" style="margin-bottom:6px">${QPD.map(m=>`<button class="chip ${A.m===m?'on':''}" style="border:0" onclick="qpSet('m',${m})">${m<60?m+' daq':m===60?'1 soat':m===90?'1,5 soat':(m/60)+' soat'}</button>`).join('')}</div>
   <div class="rwch" style="margin-bottom:8px">${Object.entries(RJT).map(([k,v])=>`<button class="chip ${A.ty===k?'on':''}" style="border:0" onclick="qpSet('ty','${k}')" aria-label="${v[1]}">${v[0]}</button>`).join('')}</div>
   <p class="edpv" style="margin:0 0 10px">${hm(A.s)}–${hm(Math.min(1440,A.s+A.m))} · ${A.d===T?'bugun':A.d===T1?'ertaga':esc(dU(A.d))} · faqat shu kunga</p>
   <div class="in"><button class="big" style="flex:2;margin:0" onclick="qpAdd()">Qo‘shish</button><button class="btn s" onclick="qpFull()">To‘liq oyna</button></div></div>`;
  if(!first&&kp){const n=document.getElementById('qpt');if(n&&document.activeElement===document.body){}}}
// ----- 📊 maqsad kartasiga avtomatik progress -----
const GLK=[['','✋ Qo‘lda (bosqichlar)'],['hifz','📖 Qur‘on hifzi'],['ielts','🎓 IELTS tayyorgarligi']];
function glkAuto(){(S.goals||[]).forEach(g=>{if(g.lk===undefined){g.lk=/hofiz|hifz|yodla/i.test(String(g.t))?'hifz':/ielts/i.test(String(g.t))?'ielts':''}})}
function glk(i,v){const g=(S.goals||[])[i];if(!g)return;g.lk=v;save()}
function glkUi(x,i){glkAuto();return `<p class="mu" style="margin:0 0 4px;font-size:12px">📊 Progress manbai</p><div class="rwch" style="margin-bottom:8px">${GLK.map(([k,l])=>`<button class="chip ${(x.lk||'')===k?'on':''}" style="border:0" onclick="glk(${i},'${k}')">${l}</button>`).join('')}</div>${x.lk?lkPanel(x.lk):''}`}
