// ---- ISHONCHLILIK: ikki qurilma o'rtasida qo'shilganda yo'qolmasligi uchun id'siz massivlarga barqaror id beradi ----
function syIds(s){try{
  if(Array.isArray(s.f5)){const seen={};s.f5.forEach(e=>{if(e&&typeof e==='object'&&e.id===undefined){const k=[e.d,e.t,e.c,e.m].join('|');seen[k]=(seen[k]||0)+1;e.id='f5:'+k+'#'+seen[k]}})}
  if(Array.isArray(s.fl)){const seen={};s.fl.forEach(e=>{if(e&&typeof e==='object'&&e.id===undefined){const k=[e.d,e.a,e.m,e.h].join('|');seen[k]=(seen[k]||0)+1;e.id='fl:'+k+'#'+seen[k]}})}
  const n=s.nf;if(n&&typeof n==='object'){
    if(Array.isArray(n.lg)){const seen={};n.lg.forEach(e=>{if(e&&typeof e==='object'&&e.cid===undefined&&e.id!==undefined&&!String(e.id).startsWith('g')){e.cid=e.id;const k=e.d+'-'+e.cid;seen[k]=(seen[k]||0)+1;e.id='g'+k+(seen[k]>1?'#'+seen[k]:'')}})}
    if(Array.isArray(n.pd)){const seen={};n.pd.forEach(e=>{if(e&&typeof e==='object'&&e.id===undefined){const k=e.d+'|'+e.a;seen[k]=(seen[k]||0)+1;e.id='p:'+k+'#'+seen[k]}})}}
}catch(e){}return s}
const syUid=p=>p+Date.now().toString(36)+Math.floor(Math.random()*1e6).toString(36);
