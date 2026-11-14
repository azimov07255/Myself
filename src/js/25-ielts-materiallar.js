// ---- IELTS: maqola va podkast materiallari. AI qiyin so'z va chunklarni topadi, so'z - ta'rif - misol bo'lib lug'atga tushadi ----
const ieM=()=>S.ie.mat=S.ie.mat||[];
let IMT=null,IMA=null,IMS=null,IMF={follow:1,loop:0,rate:1},IMSEL={},IMFL='a',IMAU=null;
const ieEsc=s=>String(s).replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
// ---- subtitr (SRT, VTT, [mm:ss] qatorlari) ----
function ieTime(s){const m=/^(?:(\d+):)?(\d{1,2}):(\d{2})(?:[.,](\d{1,3}))?$/.exec(String(s).trim());if(!m)return -1;return (+(m[1]||0))*3600+(+m[2])*60+(+m[3])+(m[4]?+('0.'+m[4]):0)}
function ieCues(raw){const txt=String(raw||'').replace(/\r/g,'').replace(/^\uFEFF/,''),L=txt.split('\n'),C=[];
  if(/-->/.test(txt)){for(let i=0;i<L.length;i++){const m=/^\s*([\d:.,]+)\s*-->\s*([\d:.,]+)/.exec(L[i]);if(!m)continue;const s=ieTime(m[1]),e=ieTime(m[2]);if(s<0||e<=s)continue;
      const b=[];let j=i+1;while(j<L.length&&L[j].trim()!==''&&!/-->/.test(L[j])){b.push(L[j].trim());j++}
      const t=b.join(' ').replace(/<[^>]+>/g,'').replace(/\{[^}]*\}/g,'').replace(/\s+/g,' ').trim();if(t&&!(C.length&&C[C.length-1].t===t))C.push({s,e,t});i=j-1}}
  else{const P=[];L.forEach(l=>{const m=/^\s*\[?((?:\d+:)?\d{1,2}:\d{2}(?:[.,]\d{1,3})?)\]?\s*[-–—]?\s*(.+)$/.exec(l);if(m){const s=ieTime(m[1]);if(s>=0&&m[2].trim())P.push({s,t:m[2].trim()})}});
    if(P.length>=3)P.forEach((p,i)=>C.push({s:p.s,e:i+1<P.length?P[i+1].s:p.s+6,t:p.t}))}
  C.sort((a,b)=>a.s-b.s);return C}
const ieText=m=>m.c&&m.c.length?m.c.map(c=>c[2]).join(' '):(m.x||'');
const ieFmt=s=>Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0');
// ---- material qo'shish ----
async function ieMatAdd(){const t=V('mt').trim()||'Nomsiz',k=V('mk')==='p'?'p':'a',raw=V('mx');let cues=k==='p'?ieCues(raw):[],x=cues.length?'':raw.replace(/[ \t]+\n/g,'\n').trim();
  const text=cues.length?cues.map(c=>c.t).join(' '):x;const f0=document.getElementById('mf2')&&document.getElementById('mf2').files&&document.getElementById('mf2').files[0];if(text.length<200&&!(k==='p'&&f0&&text.length<20)){toast('Matn juda qisqa (kamida 200 belgi). Podkastda faqat audio tanlasang, transkript avtomatik qilinadi.');return}
  const lim=k==='p'?15000:12000;let cut=false;if(text.length>lim){cut=true;if(cues.length){let n=0;cues=cues.filter(c=>(n+=c.t.length+1)<=lim)}else x=x.slice(0,lim)}
  const m={id:Date.now(),t:t.slice(0,80),k,x,c:cues.map(c=>[+c.s.toFixed(2),+c.e.toFixed(2),c.t]),au:0,an:null,d:dk()};
  const f=document.getElementById('mf2')&&document.getElementById('mf2').files&&document.getElementById('mf2').files[0];
  if(k==='p'&&f){if(f.size>50*1048576)toast('Audio 50 MB dan katta, saqlanmadi.');else try{await idbSet('ieau'+m.id,f);m.au=1;m.sz=f.size}catch(e){toast('Audio saqlanmadi.')}}
  const A=ieM();A.unshift(m);while(A.filter(x=>!x.cb).length>15){const o=A.splice(A.map(x=>!x.cb).lastIndexOf(true),1)[0];try{idbDel('ieau'+o.id)}catch(e){}ieAudDelCloud(o.id)}
  IMT=m.id;save();if(cut)toast('Matn uzun edi, boshidan '+lim+' belgi olindi.');ieMatOpen(m.id);if(m.au&&f)ieAudUp(m,f)}
function ieMatDel(id){if(!confirm('Material o‘chirilsinmi? (Lug‘atga qo‘shilgan so‘zlar qoladi.)'))return;S.ie.mat=ieM().filter(m=>m.id!==id);try{idbDel('ieau'+id)}catch(e){}ieAudDelCloud(id);save()}
// ---- AI tahlil ----
function iePartsOf(text){const S2=String(text).replace(/\s+/g,' ').trim().match(/[^.!?]+[.!?]*\s*/g)||[text],out=[];let cur='';S2.forEach(s=>{if((cur+s).length>3500&&cur){out.push(cur.trim());cur=s}else cur+=s});if(cur.trim())out.push(cur.trim());
  return out.flatMap(p=>p.length>3500?p.match(/[\s\S]{1,3400}/g):[p]).slice(0,4)}
const ieIn=(text,f)=>{try{return new RegExp('(^|[^A-Za-z])'+ieEsc(f).replace(/\s+/g,'\\s+')+'($|[^A-Za-z])','i').test(text)}catch(e){return false}};
const ieCl=(v,n)=>String(v==null?'':v).replace(/\s+/g,' ').trim().slice(0,n||160);
function ieMerge(res,j,full){if(!j||typeof j!=='object')return;const norm=s=>s.replace(/\s+/g,' ').toLowerCase(),fn=norm(full);res.grammar=res.grammar||[];
  if(!res.lv&&/^(B1|B2|C1|C2)$/.test(j.level||''))res.lv=j.level;if(!res.topic&&j.topic)res.topic=ieCl(j.topic,40);
  const LV=v=>/^(B1|B2|C1|C2)$/.test(v)?v:'',cx=s=>{const c=ieCl(s,240);return c&&fn.includes(norm(c))?c:''},
    seen=new Set(res.words.map(x=>x.w.toLowerCase()).concat(res.chunks.map(x=>x.p.toLowerCase()),res.grammar.map(x=>x.p.toLowerCase())));
  (Array.isArray(j.words)?j.words:[]).forEach(w=>{const lem=ieCl(w&&w.w,40),f=ieCl(w&&(w.f||w.w),40);if(lem.length<3||/\s/.test(lem)||seen.has(lem.toLowerCase())||!ieIn(full,f))return;seen.add(lem.toLowerCase());
    res.words.push({w:lem,f,pos:/^(n|v|adj|adv)$/.test(w.pos)?w.pos:'',lv:LV(w.lv),def:ieCl(w.def),uz:ieCl(w.uz,60),ctx:cx(w.ctx),ex:ieCl(w.ex,200)})});
  (Array.isArray(j.chunks)?j.chunks:[]).forEach(c=>{const p=ieCl(c&&c.p,60),n=p.split(/\s+/).length;if(n<2||n>6||seen.has(p.toLowerCase())||!ieIn(full,p))return;seen.add(p.toLowerCase());
    res.chunks.push({p,k:/^(collocation|phrasal|idiom|phrase)$/.test(c.k)?c.k:'phrase',lv:LV(c.lv),def:ieCl(c.def),uz:ieCl(c.uz,60),ctx:cx(c.ctx),ex:ieCl(c.ex,200)})});
  (Array.isArray(j.grammar)?j.grammar:[]).forEach(g=>{const p=ieCl(g&&g.p,120),n=p.split(/\s+/).length;if(n<3||n>14||seen.has(p.toLowerCase())||!ieIn(full,p))return;seen.add(p.toLowerCase());
    res.grammar.push({p,g:ieCl(g.g,40)||'Grammar',lv:LV(g.lv),def:ieCl(g.def),uz:ieCl(g.uz,100),ctx:cx(g.ctx),ex:ieCl(g.ex,200)})});
  res.words=res.words.slice(0,60);res.chunks=res.chunks.slice(0,30);res.grammar=res.grammar.slice(0,20)}
let IMP=null;   // to'xtab qolgan tahlil: {id,res,next,n} - "Davom ettirish" shu joydan boshlaydi
const ieSlowErr=e=>/sekin|vaqt|ulanib|502|503|504|546/i.test(String(e&&e.message||e));
async function ieAnalyze(id){const m=ieM().find(x=>x.id===id);if(!m||(IMA&&IMA.busy))return;const full=ieText(m),parts=iePartsOf(full),known=S.ie.words.slice(-120).map(w=>w.w);
  const rs=IMP&&IMP.id===id&&IMP.n===parts.length&&IMP.next>0?IMP:null,res=rs?rs.res:{words:[],chunks:[],lv:'',topic:''};let i=rs?rs.next:0,fail=false;IMP=null;
  IMA={id,busy:1,i:i,n:parts.length,err:''};ieMatDraw();
  for(;i<parts.length;i++){IMA.i=i+1;ieMatDraw();let ok=false,last=null;
    for(let at=0;at<2&&!ok;at++){try{const d=await fnAI({action:'vocab',mode:'analyze',text:parts[i],known,min:S.ie.minlv||'B1'}),j=parseJson(d.text);if(!j)throw new Error('AI javobi tushunarsiz.');ieMerge(res,j,full);ok=true}catch(e){last=e;if(!ieSlowErr(e))break}}   // sekin javob bo'lsa bir marta o'zi qayta urinadi
    if(!ok){IMA.err='Qism '+(i+1)+'/'+parts.length+': '+String(last&&last.message||last).slice(0,170);IMP={id,res,next:i,n:parts.length};fail=true;break}}
  res.n=parts.length;res.at=dk();if(res.words.length||res.chunks.length||(res.grammar||[]).length)m.an=res;IMA.busy=0;save();ieMatDraw()}
// ---- lug'atga qo'shish ----
const ieHave=w=>S.ie.words.some(x=>String(x.w).toLowerCase()===String(w).toLowerCase());
let IVC=0,IMU=null;
function ieVocAdd(it,kind,src){const k=kind==='c'?'c':kind==='g'?'g':'w',w=String(k==='w'?it.w:it.p).trim();if(!w||ieHave(w))return false;
  S.ie.words.push({id:Date.now()*1000+(IVC=(IVC+1)%1000),w,m:it.uz||it.def||'',d:it.def||'',u:it.uz||'',e:it.ex||'',c:it.ctx||'',pos:it.pos||'',lv:it.lv||'',pu:it.pu||'',ps:it.ps||'',k,gn:k==='g'?(it.g||''):'',src:src||0,box:0,due:dk(),t:0});return true}
const ieAnL=(an,k)=>k==='c'?an.chunks:k==='g'?(an.grammar||[]):an.words,ieKT=(k,it)=>k==='w'?it.w:it.p;
function ieAddOne(kind,i){const m=ieM().find(x=>x.id===IMT);if(!m||!m.an)return;const it=ieAnL(m.an,kind)[i];if(it&&ieVocAdd(it,kind,m.id)){toast('Lug‘atga qo‘shildi: '+ieKT(kind,it));save();ieMatDraw();ieSheetClose()}}
function ieAddSel(){const m=ieM().find(x=>x.id===IMT);if(!m||!m.an)return;let n=0;const ids=[];Object.keys(IMSEL).filter(k=>k!=='_o'&&IMSEL[k]).forEach(k=>{const[kind,i]=k.split(':'),it=ieAnL(m.an,kind)[+i];if(it&&ieVocAdd(it,kind,m.id)){n++;ids.push(S.ie.words[S.ie.words.length-1].id)}});IMSEL={};if(n)IMU={ids,mat:m.id,n};toast(n+' ta qo‘shildi');save();ieMatDraw()}
function ieSelAll(on){const m=ieM().find(x=>x.id===IMT);if(!m||!m.an)return;ieRows(m).forEach(r=>{if(!ieHave(r[2]))IMSEL[r[0]+':'+r[1]]=!!on});IMSEL._o=1;ieMatDraw()}
function ieAddAll(){const m=ieM().find(x=>x.id===IMT);if(!m||!m.an)return;const ids=[];ieRows(m).forEach(r=>{const it=ieAnL(m.an,r[0])[r[1]];if(it&&!ieHave(r[2])&&ieVocAdd(it,r[0],m.id))ids.push(S.ie.words[S.ie.words.length-1].id)});
  if(!ids.length){toast('Qo‘shiladigan yangi element yo‘q');return}IMU={ids,mat:m.id,n:ids.length};IMSEL={_o:1};toast(ids.length+' ta qo‘shildi. Xato bo‘lsa "Bekor qilish" tugmasi bor.');save();ieMatDraw()}
function ieUndoAdd(){if(!IMU)return;const set=new Set(IMU.ids);let k=0;S.ie.words=S.ie.words.filter(w=>{if(set.has(w.id)&&!w.t&&w.box===0){k++;return false}return true});IMU=null;IMSEL={_o:1};toast(k+' ta bekor qilindi');save();ieMatDraw()}
function ieDone(){const m=ieM().find(x=>x.id===IMT);if(!m)return;S.ie.mr=S.ie.mr||{};S.ie.mr[dk()]=1;ieDp().a=1;m.dn=dk();toast('Zo‘r! Bugungi mashqqa belgilandi (+15 XP)');save();ieMatDraw()}
// ---- matnni belgilash (chunk va so'zlar) ----
function ieMark(text,m){const an=m.an,R=[],G=[];
  const add=(s,kind,i)=>{if(!s)return;const re=new RegExp('(^|[^A-Za-z])('+ieEsc(s).replace(/\s+/g,'\\s+')+')(?=$|[^A-Za-z])','gi');let x;while((x=re.exec(text))){const a=x.index+x[1].length,b=a+x[2].length;if(!R.some(r=>a<r.b&&b>r.a))R.push({a,b,kind,i})}};
  if(an){an.chunks.forEach((c,i)=>add(c.p,'c',i));an.words.forEach((w,i)=>{add(w.f,'w',i);if(w.w.toLowerCase()!==w.f.toLowerCase())add(w.w,'w',i)});
    (an.grammar||[]).forEach((g,i)=>{const re=new RegExp('(^|[^A-Za-z])('+ieEsc(g.p).replace(/\s+/g,'\\s+')+')(?=$|[^A-Za-z])','i'),x=re.exec(text);if(x){const a=x.index+x[1].length;G.push({a,b:a+x[2].length,i})}})}
  {const lt=text.toLowerCase();(S.ie.words||[]).forEach((w,vi)=>{if(w.k==='g'||!w.w)return;if(lt.includes(String(w.w).toLowerCase()))add(w.w,'v',vi)})}if(typeof cbRanges==='function')cbRanges(text,m,R);R.sort((a,b)=>a.a-b.a);const gi=a=>{const g=G.find(r=>a>=r.a&&a<r.b);return g?g.i:-1};
  const plain=(s,base)=>{let h='',x;const re=/([A-Za-z][A-Za-z'’-]*)|([^A-Za-z]+)/g;while((x=re.exec(s))){if(x[1]){const g=gi(base+x.index);h+='<span class="iew'+(g>=0?' gtx" data-g="'+g:'')+'">'+esc(x[1])+'</span>'}else h+=esc(x[2])}return h};
  let h='',p=0;R.forEach(r=>{if(r.a<p)return;h+=plain(text.slice(p,r.a),p);const vv=r.kind==='v',bb=r.kind==='b',it=bb?{}:vv?S.ie.words[r.i]:(r.kind==='c'?an.chunks:an.words)[r.i],have=bb?cbHasI(r.i):(vv||ieHave(r.kind==='c'?it.p:it.w)),g=gi(r.a);
    h+=`<mark class="${bb?'mcb':vv?'mv':r.kind==='c'?'mc':'mw2'}${it.lv?' lv'+it.lv:''}${have?' hv':''}${g>=0?' gtx':''}" data-k="${r.kind}" data-i="${r.i}">${esc(text.slice(r.a,r.b))}</mark>`;p=r.b});
  return h+plain(text.slice(p),p)}
// ---- o'qish oynasi ----
async function ieMatOpen(id){const m=ieM().find(x=>x.id===id);if(!m)return;if(document.getElementById('iem'))ieMatClose(true);IMT=id;
  const el=document.createElement('div');el.id='iem';el.className='mfo iemo';
  el.innerHTML='<div class="mft"><button class="x" onclick="ieMatClose()" aria-label="Yopish">✕</button><div class="mfti"><b id="iemt" style="font:700 17px Fraunces,serif"></b><small id="iems"></small></div><button class="x" onclick="ieEdSheet()" aria-label="Tahrirlash" style="width:38px">✏️</button></div><div class="mfp" id="iemb"></div><div id="iepl"></div>';
  document.body.appendChild(el);ovLock(el);el.addEventListener('click',ieTap);IMAU=null;
  if(m.au){try{const b=await ieAudGet(m);if(b){IMAU=URL.createObjectURL(b)}}catch(e){}}if(!IMAU&&m.ar)IMAU=m.ar;
  ieMatDraw()}
function ieMatClose(quiet){ieReadPause();IRA=null;ieSelHide();ieWFStop();IWC=null;{const a0=document.getElementById('ieau'),m0=ieM().find(x=>x.id===IMT);if(a0&&m0&&a0.currentTime>1&&!a0.ended){m0.pos=Math.floor(a0.currentTime);qsave()}}const a=document.getElementById('ieau');if(a){try{a.pause()}catch(e){}}if(IMAU){try{URL.revokeObjectURL(IMAU)}catch(e){}IMAU=null}ovUnlock();const e=document.getElementById('iem');if(e)e.remove();IMT=null;IMS=null;if(!quiet)render()}
function ieMatDraw(){const b=document.getElementById('iemb'),m=ieM().find(x=>x.id===IMT);if(!b||!m)return;const an=m.an,sc=b.scrollTop,st=an?`${an.words.length} so‘z · ${an.chunks.length} chunk · ${(an.grammar||[]).length} grammar${an.lv?' · '+an.lv:''}${an.topic?' · '+an.topic:''}`:'tahlil qilinmagan';
  document.getElementById('iemt').textContent=m.t;document.getElementById('iems').textContent=(m.k==='p'?'🎧 Podkast':'📰 Maqola')+' · '+st;
  const busy=IMA&&IMA.busy&&IMA.id===m.id,full=ieText(m),np=iePartsOf(full).length;
  const bar=ieVoiceBar(m)+(full.length?ieMinLv()+`<div class="ieb">${busy?`<div class="mu" style="margin-bottom:6px">🔍 AI tahlil qilmoqda… ${IMA.i}/${IMA.n}</div>`:`<button class="btn" style="flex:1" onclick="ieAnalyze(${m.id})">${IMP&&IMP.id===m.id&&IMP.n===np&&IMP.next>0?`↻ Davom ettirish (qism ${IMP.next+1}/${np}, oldingilari saqlangan)`:`🔍 ${an?'Qayta tahlil':'AI bilan tahlil'} (${np} so‘rov)`}</button>`}${m.dn===dk()?'<span class="chip">✓ bugun</span>':`<button class="btn s" onclick="ieDone()">✓ Tugatdim</button>`}</div>${aiStat()}${IMA&&IMA.id===m.id&&IMA.err?`<p style="color:var(--bad);margin:6px 0">${esc(IMA.err)}</p>`:''}`:'');
  const res=an?ieResults(m):'';
  let body;
  if(m.c&&m.c.length)body=m.c.map((c,i)=>`<div class="iecu" data-i="${i}" id="icu${i}"><button class="iet" onclick="ieCueGo(${i})" aria-label="${ieFmt(c[0])} ga o‘tish">${ieFmt(c[0])}</button>${m.au&&IMAU?`<button class="iet" onclick="ieDictOpen(${i})" aria-label="Diktant">✍</button>`:''}${IMF.ce?`<button class="iet" onclick="ieCueEdit(${i})" aria-label="Qatorni tahrirla">✏️</button>`:''}<span class="iep">${ieMark(c[2],m)}</span></div>`).join('');
  else body=full.split(/\n{2,}|\n/).filter(p=>p.trim()).map(p=>ieHdP(p,m)).join('')||`<p class="iep">${ieMark(full,m)}</p>`;
  b.innerHTML=bar+(an?`<details class="iesum" ${IMSEL._o?'open':''}><summary>📋 Tahlil natijalari: tanlab qo‘shish</summary>${res}</details>`:'')+`<div class="ietx" style="font-size:${17}px">${body}</div><p class="mu" style="font-size:12px;margin-top:12px">Ajratilgan so‘z yoki iborani bos. Boshqa so‘zni bossang, AI dan so‘rashing mumkin. O‘zbekcha ma’nolarni AI yozadi: ishonchsiz bo‘lsa tekshirib ol.</p>`;
  b.scrollTop=sc;iePlayer(m);IMC=-1;if(ieAu())ieTU();if(IRA)ieReadHi()}
function ieRows(m){const an=m.an,f=IMFL,rows=[],lvF=/^(B1|B2|C1|C2)$/.test(f),ok=x=>!lvF||x.lv===f;
  if(f==='a'||lvF)an.words.forEach((w,i)=>{if(ok(w))rows.push(['w',i,w.w,w.lv,w.uz||w.def,'so‘z'])});
  if(f==='a'||lvF||f==='c')an.chunks.forEach((c,i)=>{if(ok(c))rows.push(['c',i,c.p,c.lv,c.uz||c.def,'chunk'])});
  if(f==='a'||lvF||f==='g')(an.grammar||[]).forEach((g,i)=>{if(ok(g))rows.push(['g',i,g.p,g.lv,(g.g?g.g+' · ':'')+(g.uz||g.def||''),'grammar'])});return rows}
function ieResults(m){const rows=ieRows(m),n=Object.keys(IMSEL).filter(k=>k!=='_o'&&IMSEL[k]).length,fresh=rows.filter(r=>!ieHave(r[2])).length,
  fl=[['a','Hammasi'],['B1','B1'],['B2','B2'],['C1','C1'],['C2','C2'],['c','Chunklar'],['g','Grammar']].map(x=>`<button class="${IMFL===x[0]?'on':''}" onclick="IMFL='${x[0]}';IMSEL._o=1;ieMatDraw()">${x[1]}</button>`).join('');
  return `<div class="seg sc" style="margin:8px 0">${fl}</div><p class="mu" style="font-size:12px;margin:2px 0 6px"><span class="lgd lvB1">B1</span> <span class="lgd lvB2">B2</span> <span class="lgd lvC1">C1</span> <span class="lgd lvC2">C2</span> so‘z matnda shu rangda chiziladi; binafsha fon: grammatika</p>
  <div class="in" style="flex-wrap:wrap;margin-bottom:6px"><button class="btn s" onclick="ieSelAll(1)">☑ Hammasini belgilash</button><button class="btn s" onclick="ieSelAll(0)">☐ Tozalash</button><span class="mu" style="align-self:center">${fresh} ta yangi</span></div>
  ${rows.map(r=>{const have=ieHave(r[2]);return `<label class="ierow ${have?'hv':''}"><input type="checkbox" ${have?'checked disabled':IMSEL[r[0]+':'+r[1]]?'checked':''} onchange="IMSEL['${r[0]}:${r[1]}']=this.checked;IMSEL._o=1;ieMatDraw()"><span class="t"><b>${esc(r[2])}</b> ${r[3]?`<span class="erb new">${esc(r[3])}</span>`:''}${r[5]!=='so‘z'?`<span class="erb old">${r[5]}</span>`:''}<br><small class="mu">${esc(r[4]||'')}</small></span><button class="x" onclick="ieSheet('${r[0]}',${r[1]})" aria-label="Batafsil">ⓘ</button></label>`}).join('')||'<p class="mu">Hech narsa topilmadi.</p>'}
  <button class="big" style="margin-top:8px" onclick="ieAddSel()" ${n?'':'disabled'}>➕ Tanlanganlarni qo‘shish (${n})</button><button class="big" style="margin-top:8px;background:var(--ac);color:#fff" onclick="ieAddAll()" ${fresh?'':'disabled'}>⚡ Ko‘ringanlarning hammasini qo‘shish (${fresh})</button>${IMU&&IMU.mat===m.id?`<button class="btn s" style="width:100%;margin-top:8px" onclick="ieUndoAdd()">↩ Oxirgi ${IMU.n} ta qo‘shilganni bekor qilish</button>`:''}`}
// ---- so'z kartochkasi (bottom sheet) ----
function ieSheetClose(){IMS=null;const e=document.getElementById('iesh');if(e)e.remove()}
function ieSheetHtml(it,kind,have,idx){const w=kind==='c'?it.p:it.w,hl=s=>esc(s).replace(new RegExp('('+ieEsc(esc(kind==='c'?it.p:(it.f||it.w)))+')','ig'),'<b>$1</b>');
  return `<div class="mfsh"><b style="font:700 22px Fraunces,serif">${esc(w)}</b><span>${ieAccChip()}<button class="x" onclick="ieSay(${JSON.stringify(w).replace(/"/g,'&quot;')})" aria-label="Talaffuz">🔊</button><button class="x" onclick="ieSheetClose()" aria-label="Yopish">✕</button></span></div>
   <div style="margin-bottom:6px">${it.pos?`<span class="erb old">${esc(it.pos)}</span>`:''}${it.lv?`<span class="erb new">${esc(it.lv)}</span>`:''}${kind==='c'?`<span class="erb old">${esc(it.k||'chunk')}</span>`:''}</div>
   ${it.uz?`<p style="margin:0 0 4px;font-size:18px"><b>${esc(it.uz)}</b></p>`:''}${it.def?`<p style="margin:0 0 6px">${esc(it.def)}</p>`:''}${it.ctx?`<p class="mu" style="margin:0 0 6px">“${hl(it.ctx)}” ${ieSpk(it.ctx)}</p>`:''}${it.ex?`<p style="margin:0 0 8px"><i>${esc(it.ex)}</i> ${ieSpk(it.ex)}</p>`:''}
   ${have?'<button class="btn s" disabled>✓ Lug‘atda bor</button>':`<button class="btn" style="width:100%" onclick="${idx!==undefined?`ieAddOne('${kind}',${idx})`:'ieAddDef()'}">➕ Lug‘atga qo‘shish</button>`}${ieHereBtn()}`}
function ieGramHtml(it,have,idx,word){return `<div class="mfsh"><b style="font:700 19px Fraunces,serif">${esc(it.g||'Grammar')}</b><span>${ieAccChip()}${ieSpk(it.p)}<button class="x" onclick="ieSheetClose()" aria-label="Yopish">✕</button></span></div>
   <div style="margin-bottom:6px"><span class="erb new">grammar</span>${it.lv?`<span class="erb new">${esc(it.lv)}</span>`:''}</div><p style="margin:0 0 6px;font-size:17px"><b>“${esc(it.p)}”</b></p>${it.def?`<p style="margin:0 0 4px"><code>${esc(it.def)}</code></p>`:''}${it.uz?`<p style="margin:0 0 6px">${esc(it.uz)}</p>`:''}
   ${it.ctx&&it.ctx!==it.p?`<p class="mu" style="margin:0 0 6px">“${esc(it.ctx)}” ${ieSpk(it.ctx)}</p>`:''}${it.ex?`<p style="margin:0 0 8px"><i>${esc(it.ex)}</i> ${ieSpk(it.ex)}</p>`:''}
   ${have?'<button class="btn s" disabled>✓ Lug‘atda bor</button>':`<button class="btn" style="width:100%" onclick="ieAddOne('g',${idx})">➕ Lug‘atga qo‘shish</button>`}${ieHereBtn()}${word?`<button class="btn s" style="width:100%;margin-top:6px" onclick="ieGramWord(${JSON.stringify(word).replace(/"/g,'&quot;')},${idx})">“${esc(word)}” so‘zini izohlash</button>`:''}`}
function ieSheet(kind,i,word){const m=ieM().find(x=>x.id===IMT);if(!m||!m.an)return;const it=ieAnL(m.an,kind)[i];if(!it)return;ieSheetClose();IMS={kind,i};const e=document.createElement('div');e.id='iesh';e.className='mfs';
  e.innerHTML=kind==='g'?ieGramHtml(it,ieHave(it.p),i,word):ieSheetHtml(it,kind,ieHave(kind==='c'?it.p:it.w),i);document.getElementById('iem').appendChild(e)}
function ieGramWord(word,gi){const m=ieM().find(x=>x.id===IMT),g=m&&m.an&&(m.an.grammar||[])[gi];ieSheetClose();IMS={word,ctx:(g&&(g.ctx||g.p))||'',def:null,busy:0,err:''};const el=document.createElement('div');el.id='iesh';el.className='mfs';document.getElementById('iem').appendChild(el);ieSheetWord()}
function ieSentence(node){const p=node.closest('.iep');if(!p)return '';const t=p.textContent||'',w=node.textContent||'',i=t.indexOf(w),S3=t.match(/[^.!?]+[.!?]*\s*/g)||[t];let pos=0;for(const s of S3){if(i>=pos&&i<pos+s.length)return s.trim().slice(0,300);pos+=s.length}return t.slice(0,300)}
function ieTap(e){{const sl=window.getSelection&&window.getSelection();if(sl&&!sl.isCollapsed&&sl.toString().trim().length>1&&e.target.closest&&e.target.closest('.ietx'))return}IRH=ieRdPos(e.target);const mk=e.target.closest&&e.target.closest('mark[data-k]');if(mk){if(mk.dataset.k==='b'){cbSheet(+mk.dataset.i);return}if(mk.dataset.k==='v'){ieSheetVocab(+mk.dataset.i);return}ieSheet(mk.dataset.k,+mk.dataset.i);return}
  const w=e.target.closest&&e.target.closest('.iew');if(w){if(w.dataset.g!==undefined){ieSheet('g',+w.dataset.g,w.textContent);return}const word=w.textContent.replace(/[’']s?$/,''),ctx=ieSentence(w);ieSheetClose();IMS={word,ctx,def:null,busy:0,err:''};ieGlSeed(IMS,word);const el=document.createElement('div');el.id='iesh';el.className='mfs';document.getElementById('iem').appendChild(el);ieSheetWord()}}
function ieSheetWord(){const el=document.getElementById('iesh');if(!el||!IMS||!IMS.word)return;const q=IMS;
  if(q.def){el.innerHTML=ieSheetHtml(q.def,'w',ieHave(q.def.w||q.word))+(q.glw&&q.glw.length?`<p class="mu" style="margin:8px 0 0;font-size:13px">So‘zma-so‘z: ${q.glw.map(a=>esc(a[0])+' = '+esc(a[1])).join(' · ')}</p>`:'');return}
  el.innerHTML=`<div class="mfsh"><b style="font:700 22px Fraunces,serif">${esc(q.word)}</b><span>${ieAccChip()}<button class="x" onclick="ieSay(${JSON.stringify(q.word).replace(/"/g,'&quot;')})" aria-label="Talaffuz">🔊</button><button class="x" onclick="ieSheetClose()" aria-label="Yopish">✕</button></span></div>${q.ctx?`<p class="mu" style="margin:0 0 8px">“${esc(q.ctx)}” ${ieSpk(q.ctx)}</p>`:''}${q.gl?`<p style="margin:0 0 8px;font-size:20px"><b>${esc(q.gl)}</b></p>`:''}${!q.gl&&!ieAnyGl()?'<button class="btn s" style="width:100%;margin-bottom:8px" onclick="ieSheetClose();glRun()">📖 Hamma so‘z ma‘nosini olish (bir marta)</button>':''}${q.glw&&q.glw.length?`<p class="mu" style="margin:0 0 8px">${q.glw.map(a=>esc(a[0])+' = '+esc(a[1])).join(' · ')}</p>`:''}${q.err?`<p style="color:var(--bad);margin:0 0 8px">${esc(q.err)}</p>`:''}${q.busy?'<p class="mu">AI izohlamoqda…</p>':`<div class="in" style="flex-wrap:wrap"><button class="btn" onclick="ieDefine()">✨ ${q.gl?'To‘liq izoh (AI)':'AI dan ma’nosini so‘rash'}</button><button class="btn s" onclick="ieQuickAdd()">➕ Faqat so‘zni qo‘sh</button></div>`}${ieHereBtn()}`}
async function ieDefine(){const q=IMS;if(!q||q.busy)return;{const c=ieCacheGet(ieM().find(x=>x.id===IMT),q.word);if(c&&c.full){q.def=c.full;ieSheetWord();return}}q.busy=1;q.err='';ieSheetWord();
  try{const d=await fnAI({action:'vocab',mode:'define',word:q.word,ctx:q.ctx}),j=parseJson(d.text);if(!j||!j.def&&!j.uz)throw new Error('AI javobi tushunarsiz.');
    q.def={w:ieTok(q.word).length>1?ieCl(q.word,80):ieCl(j.w||q.word,40),pos:/^(n|v|adj|adv)$/.test(j.pos)?j.pos:'',lv:/^(B1|B2|C1|C2)$/.test(j.lv)?j.lv:'',def:ieCl(j.def),uz:ieCl(j.uz,60),ctx:q.ctx,ex:ieCl(j.ex,200)};try{ieCachePut(ieM().find(x=>x.id===IMT),q.word,{u:q.def.uz,full:q.def})}catch(e2){}}
  catch(e){q.err=String(e.message||e).slice(0,160)}q.busy=0;if(IMS===q)ieSheetWord()}
function ieAddDef(){const q=IMS;if(!q||!q.def)return;const m=ieM().find(x=>x.id===IMT),multi=ieTok(q.word).length>1;if(ieVocAdd(multi?{...q.def,p:q.def.w}:q.def,multi?'c':'w',m?m.id:0)){toast('Lug‘atga qo‘shildi: '+q.def.w);save();ieMatDraw();ieSheetClose()}}
function ieQuickAdd(){const q=IMS;if(!q)return;const m=ieM().find(x=>x.id===IMT);if(ieTok(q.word).length>1?ieVocAdd({p:q.word,ctx:q.ctx},'c',m?m.id:0):ieVocAdd({w:q.word,ctx:q.ctx,uz:q.gl||''},'w',m?m.id:0)){toast('Qo‘shildi. Ma’nosini keyin yozib qo‘y.');save();ieMatDraw()}else toast('Bu so‘z lug‘atda bor');ieSheetClose()}
// ---- podkast pleyeri (subtitr bilan) ----
function iePlayer(m){const pl=document.getElementById('iepl');if(!pl)return;if(!(m.c&&m.c.length)&&!m.au){pl.innerHTML='';return}
  if(!IMAU){pl.innerHTML=`<div class="iepb"><span class="mu" style="flex:1">${m.au?(m.cl?'Audio yuklanmadi (internetni tekshir).':'Audio bu qurilmada yo‘q.'):'Audio qo‘shilmagan: matnni subtitr kabi o‘qiysiz.'}</span><button class="btn s" onclick="ieAudPick(${m.id})">🎧 Audio qo‘shish</button></div>`;return}
  if(document.getElementById('ieau'))return;
  pl.innerHTML=`<div class="iepb"><audio id="ieau" src="${IMAU}" preload="metadata"></audio><button class="x" id="iepp" onclick="iePlay()" aria-label="Boshlash">▶</button><button class="x" onclick="ieSkip(-5)" aria-label="5 soniya orqaga">⟲5</button><button class="x" onclick="ieSkip(5)" aria-label="5 soniya oldinga">5⟳</button><input id="iesk" type="range" min="0" max="1000" value="0" oninput="ieSeekR(this.value)" aria-label="Joylashuv"><button class="btn s" id="ierate" onclick="ieRate()">${IMF.rate}×</button><button class="btn s ${IMF.loop?'on':''}" id="ieloop" onclick="ieLoop()">⟲ gap</button></div>`;
  const a=document.getElementById('ieau');a.playbackRate=IMF.rate;ieWFAttach(a);if(m.pos>1)a.addEventListener('loadedmetadata',()=>{if(m.pos<(a.duration||0)-2){a.currentTime=m.pos;IMC=-1;ieTU(true);toast('Davom ettirildi: '+ieFmt(m.pos))}},{once:true});a.addEventListener('pause',()=>{if(a.ended)return;m.pos=Math.floor(a.currentTime);qsave()});a.addEventListener('ended',()=>{m.pos=0;qsave()});a.addEventListener('timeupdate',()=>ieTU());a.addEventListener('play',()=>{const b=document.getElementById('iepp');if(b)b.textContent='⏸'});a.addEventListener('pause',()=>{const b=document.getElementById('iepp');if(b)b.textContent='▶'})}
const ieAu=()=>document.getElementById('ieau');
const ieP=a=>{try{const p=a.play();if(p&&p.catch)p.catch(()=>{})}catch(e){}};
function iePlay(){const a=ieAu();if(!a)return;a.paused?ieP(a):a.pause()}
function ieSkip(d){const a=ieAu();if(a)a.currentTime=Math.max(0,Math.min(a.duration||1e9,a.currentTime+d))}
function ieSeekR(v){const a=ieAu();if(a&&a.duration)a.currentTime=a.duration*v/1000}
function ieRate(){const R=[.75,1,1.25,1.5],a=ieAu();IMF.rate=R[(R.indexOf(IMF.rate)+1)%R.length];if(a)a.playbackRate=IMF.rate;const b=document.getElementById('ierate');if(b)b.textContent=IMF.rate+'×'}
function ieLoop(){IMF.loop=IMF.loop?0:1;const b=document.getElementById('ieloop');if(b)b.classList.toggle('on',!!IMF.loop)}
function ieCueIdx(m,t){const C=m.c||[];for(let i=C.length-1;i>=0;i--)if(t>=C[i][0]-0.05)return t<=C[i][1]+0.6||i===C.length-1?i:i;return -1}
let IMC=-1;
function ieScrollView(n){try{const r=n.getBoundingClientRect(),h=window.innerHeight;if(r.top<110||r.bottom>h-150)n.scrollIntoView({block:'center',behavior:'smooth'})}catch(e){}}
function ieTU(force){const a=ieAu(),m=ieM().find(x=>x.id===IMT);if(!a||!m)return;const t=a.currentTime,i=ieCueIdx(m,t),sk=document.getElementById('iesk');if(typeof IDK!=='undefined'&&IDK&&IDK.stop&&t>=IDK.stop){a.pause();IDK.stop=0;a.playbackRate=IMF.rate}if(sk&&a.duration)sk.value=Math.round(t/a.duration*1000);
  if(IMF.loop&&IMC>=0&&m.c[IMC]&&t>=m.c[IMC][1]){a.currentTime=m.c[IMC][0];return}
  if(i!==IMC){document.querySelectorAll('#iemb .iecu.on').forEach(x=>x.classList.remove('on'));IMC=i;const n=document.getElementById('icu'+i);if(n){n.classList.add('on');if(IMF.follow&&(force===true||!a.paused))ieScrollView(n)}}}
function ieCueGo(i){const a=ieAu(),m=ieM().find(x=>x.id===IMT);if(!m||!m.c[i])return;if(!a){toast('Audio yo‘q: faqat matn.');return}a.currentTime=m.c[i][0];IMC=-1;ieTU(true);ieP(a)}
// ---- material ro'yxati va qo'shish formasi ----
function ieMat(){const A=ieM(),adding=IMF.add,list=A.map(m=>{const an=m.an,hv=an?an.words.concat(an.chunks,an.grammar||[]).filter(x=>ieHave(x.w||x.p)).length:0;
    return `<div class="row iemr"><button class="x" style="flex:1;text-align:left;color:var(--tx);font:inherit" onclick="ieMatOpen(${m.id})"><b>${m.k==='p'?'🎧':'📰'} ${esc(m.t)}</b><br><small class="mu">${esc(m.d)} · ${ieText(m).length} belgi${m.au?(m.cl?' · audio ☁':' · audio'):''}${m.c&&m.c.length?' · subtitr':''}${an?` · ${an.words.length} so‘z, ${an.chunks.length} chunk, ${(an.grammar||[]).length} grammar (${hv} qo‘shilgan)`:' · tahlil qilinmagan'}</small></button><button class="x" onclick="ieEdOpen(${m.id})" aria-label="Tahrirlash">✏️</button><button class="x" onclick="ieMatDel(${m.id})" aria-label="O‘chirish">✕</button></div>`}).join('');
  const form=adding?`<div class="goal"><b>Yangi material</b><div class="seg" style="margin:8px 0"><button class="${IMF.mk!=='p'?'on':''}" onclick="IMF.mk='a';render()">📰 Maqola</button><button class="${IMF.mk==='p'?'on':''}" onclick="IMF.mk='p';render()">🎧 Podkast</button></div><input type="hidden" id="mk" value="${IMF.mk==='p'?'p':'a'}"><input id="mt" placeholder="Nomi" style="width:100%;margin-bottom:6px"><div class="in" style="margin-bottom:4px"><input id="mu" placeholder="Havola (https://…): maqola yoki transkript sahifasi" style="flex:1;min-width:0"><button class="btn s" onclick="ieUrlGet()">🔗 Olish</button></div><p id="mus" class="mu" style="margin:0 0 6px;font-size:12px"></p><textarea id="mx" rows="7" placeholder="${IMF.mk==='p'?'Transkript yoki subtitr (SRT, VTT yoki [01:23] qatorlar) shu yerga qo‘yiladi. Vaqtlari bo‘lsa audio bilan birga yuradi.':'Maqola matnini shu yerga qo‘y (BBC, Guardian, Cambridge, TED transkript…)'}" style="width:100%"></textarea>${IMF.mk==='p'?'<div class="mu" style="margin:6px 0 4px">Audio (ixtiyoriy). Bulutga ham yuklanadi, telefon va kompyuterda chalinadi:</div><input type="file" id="mf2" accept="audio/*,video/mp4">':''}<div class="in" style="margin-top:8px"><button class="btn" onclick="ieMatAdd()">Saqlash va ochish</button><button class="btn s" onclick="IMF.add=0;render()">Bekor</button></div></div>`:`<button class="big" onclick="IMF.add=1;IMF.mk=IMF.mk||'a';render()">➕ Maqola yoki podkast qo‘shish</button>`;
  return `<section class="hero"><p class="lab">Materiallar</p><h1 style="font-size:26px">O‘qi, eshit, so‘zni ol</h1><p class="mu">Maqola yoki podkast transkriptini qo‘y. AI qiyin so‘z va iboralarni topib, <b>so‘z · ta’rif · misol</b> ko‘rinishida lug‘atga qo‘shadi. Kuniga bitta material ham yetarli.</p></section>${form}${nfUi()}<h2>Kutubxona</h2>${list||'<p class="mu">Hali material yo‘q. Birinchisini qo‘sh: masalan BBC 6 Minute English transkripti.</p>'}`}
