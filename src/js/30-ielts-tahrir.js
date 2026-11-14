// ---- Material tahriri (✏️): nom, matn/subtitr, audio (bulutga ham saqlanadi), transkript qatorlari; tahlil darajasi ----
const ieSb=()=>window.__sb||(typeof sb!=='undefined'?sb:null),ieCloudOn=()=>!!ieSb()&&!!UID,ieAudPath=id=>UID+'/i/'+id;   // ieSb: sinovlar uchun almashtiriladigan nuqta
async function ieAudGet(m){let b=null;try{b=await idbGet('ieau'+m.id)}catch(e){}if(b)return b;
  if(m.cl&&ieCloudOn()){try{toast('Audio bulutdan yuklanmoqda…');const r=await ieSb().storage.from('books').download(ieAudPath(m.id));if(r.error)throw r.error;b=r.data;try{await idbSet('ieau'+m.id,b)}catch(e){}return b}catch(e){toast('Audio yuklanmadi: '+String(e.message||e).slice(0,80))}}return null}
async function ieAudUp(m,blob){if(!ieCloudOn())return false;if(typeof cloudOk==='function'&&!cloudOk(blob.size)){toast('Bulut hajmi to‘lgan: audio faqat shu qurilmada qoladi.');return false}
  try{const r=await ieSb().storage.from('books').upload(ieAudPath(m.id),blob,{upsert:true,contentType:blob.type||'audio/mpeg'});if(r.error)throw r.error;m.cl=1;m.sz=blob.size;save();toast('Audio bulutga yuklandi ☁');return true}catch(e){toast('Audio bulutga yuklanmadi: '+String(e.message||e).slice(0,80));return false}}
function ieAudDelCloud(id){if(ieCloudOn())try{ieSb().storage.from('books').remove([ieAudPath(id)]).catch(()=>{})}catch(e){}}
async function ieAudReload(m){if(IMAU){try{URL.revokeObjectURL(IMAU)}catch(e){}IMAU=null}const o=document.getElementById('ieau');if(o){try{o.pause()}catch(e){}}const pl=document.getElementById('iepl');if(pl)pl.innerHTML='';
  const b=m.au?await ieAudGet(m):null;if(b)IMAU=URL.createObjectURL(b);IMC=-1;ieMatDraw();if(document.getElementById('ied'))ieEdSheet()}
function ieAudPick(id){const inp=document.createElement('input');inp.type='file';inp.accept='audio/*,video/mp4,.mp3,.m4a,.wav,.ogg,.aac';inp.style.display='none';document.body.appendChild(inp);const rm=()=>{try{inp.remove()}catch(e){}};setTimeout(rm,180000);
  inp.onchange=async()=>{const f=inp.files&&inp.files[0];rm();if(!f)return;if(f.size>50*1048576){toast('Audio 50 MB dan katta (bulut chegarasi).');return}const m=ieM().find(x=>x.id===id);if(!m)return;
    try{await idbSet('ieau'+id,f)}catch(e){toast('Audio saqlanmadi.');return}m.au=1;m.cl=0;m.sz=f.size;save();await ieAudReload(m);ieAudUp(m,f).then(()=>{if(document.getElementById('ied'))ieEdSheet()})};inp.click()}
async function ieAudUpLocal(id){const m=ieM().find(x=>x.id===id);if(!m)return;let b=null;try{b=await idbGet('ieau'+id)}catch(e){}if(!b){toast('Audio bu qurilmada yo‘q.');return}toast('Bulutga yuklanmoqda…');await ieAudUp(m,b);ieEdSheet()}
async function ieAudDel(id){const m=ieM().find(x=>x.id===id);if(!m||!confirm('Audio shu qurilmadan va bulutdan o‘chirilsinmi? (Matn qoladi.)'))return;try{await idbDel('ieau'+id)}catch(e){}ieAudDelCloud(id);m.au=0;m.cl=0;m.sz=0;save();await ieAudReload(m)}
// ---- tahrirlash oynasi ----
async function ieEdOpen(id){await ieMatOpen(id);ieEdSheet()}
function ieEdClose(){const e=document.getElementById('ied');if(e)e.remove()}
async function ieEdSheet(){const m=ieM().find(x=>x.id===IMT);if(!m)return;ieSheetClose();ieEdClose();let loc=false;if(m.au){try{loc=!!(await idbGet('ieau'+m.id))}catch(e){}}
  const st=!m.au?'yo‘q':loc&&m.cl?'✓ shu qurilmada va bulutda (boshqa qurilmalarda ham chaladi)':loc?'✓ shu qurilmada, bulutga yuklanmagan':m.cl?'☁ bulutda (ochilganda shu qurilmaga yuklanadi)':'✗ bu qurilmada yo‘q',e=document.createElement('div');e.id='ied';e.className='mfs ied';
  e.innerHTML=`<div class="mfsh"><b>✏️ Tahrirlash</b><button class="x" onclick="ieEdClose()" aria-label="Yopish">✕</button></div><label class="mu">Nomi</label><input id="edt" value="${esc(m.t)}" style="width:100%;margin:2px 0 8px">
   ${m.k==='p'?`<label class="mu">Transkript yoki subtitrni almashtirish (ixtiyoriy)</label><textarea id="edx" rows="4" style="width:100%" placeholder="Yangi SRT, VTT, [01:23] qatorlar yoki oddiy matn. Bo‘sh qoldirsang o‘zgarmaydi. Almashtirsang AI tahlili yangilanadi."></textarea>`:`<label class="mu">Matn</label><textarea id="edx" rows="8" style="width:100%">${esc(m.x||'')}</textarea>`}
   ${m.k==='p'?`<p style="margin:10px 0 4px"><b>🎧 Audio:</b> ${st}</p><div class="in" style="flex-wrap:wrap"><button class="btn" onclick="ieAudPick(${m.id})">${m.au?'Almashtirish':'Audio qo‘shish'}</button>${loc&&!m.cl?`<button class="btn s" onclick="ieAudUpLocal(${m.id})">☁ Bulutga yuklash</button>`:''}${m.au?`<button class="btn s" onclick="ieAudDel(${m.id})">🗑 Audioni o‘chirish</button>`:''}</div>`:''}
   ${m.k==='p'&&m.c&&m.c.length?`<button class="btn s" style="width:100%;margin-top:8px" onclick="ieCeToggle()">${IMF.ce?'✓ Qator tahriri yoqilgan (o‘chirish)':'✏️ Transkript qatorlarini tuzatish'}</button>`:''}
   <div class="in" style="margin-top:10px"><button class="btn" style="flex:1" onclick="ieEdSave()">Saqlash</button><button class="btn s" onclick="ieEdClose()">Bekor</button></div>`;
  document.getElementById('iem').appendChild(e)}
function ieEdSave(){const m=ieM().find(x=>x.id===IMT);if(!m)return;const t=(V('edt')||'').trim().slice(0,80)||m.t,raw=(V('edx')||'').trim();let changed=false;
  if(m.k==='p'){if(raw){const cues=ieCues(raw);if(cues.length){m.c=cues.map(c=>[+c.s.toFixed(2),+c.e.toFixed(2),c.t,null]);m.x='';changed=true}else if(raw.length>=200){m.x=raw.slice(0,15000);m.c=[];changed=true}else{toast('Matn juda qisqa (kamida 200 belgi) yoki subtitr formati tanilmadi.');return}}}
  else if(raw!==(m.x||'').trim()){if(raw.length<200){toast('Matn juda qisqa (kamida 200 belgi).');return}m.x=raw.slice(0,12000);changed=true}
  m.t=t;if(changed){m.an=null;m.tr=0;IMSEL={};IMU=null}save();ieEdClose();ieMatDraw();toast(changed?'Saqlandi. Matn o‘zgargani uchun tahlilni qayta qil.':'Saqlandi')}
// ---- transkript qatorini tuzatish (ismlar, noto'g'ri so'zlar) ----
function ieCeToggle(){IMF.ce=IMF.ce?0:1;ieEdClose();ieMatDraw()}
function ieCueEdit(i){const m=ieM().find(x=>x.id===IMT);if(!m||!m.c[i])return;const v=prompt('Qatorni tahrirla',m.c[i][2]);if(v===null)return;const t=v.replace(/\s+/g,' ').trim();if(!t)return;m.c[i][2]=t;m.c[i][3]=null;save();ieMatDraw()}   // so'z vaqtlari qayta hisoblanadi (proporsional)
// ---- tahlil darajasi ----
const ieMinLv=()=>{const mn=S.ie.minlv||'B1';return `<div class="ieb" style="margin:0 0 6px;gap:6px"><span class="mu" style="font-size:13px">So‘zlar darajasi (shu va undan yuqori):</span>${['B1','B2','C1'].map(v=>`<button class="chip ${mn===v?'on':''}" style="border:0;cursor:pointer;font-weight:600" onclick="ieMinSet('${v}')" aria-label="${v} va undan yuqori">${v}+</button>`).join('')}</div>`};
function ieMinSet(v){S.ie.minlv=v;save();ieMatDraw()}
