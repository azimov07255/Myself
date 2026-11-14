// ---- Lug'at qidiruvida yozayotganda harflarga mos so'zlar ketma-ket chiqadi (avtomatik to'ldirish). Ro'yxat: data/words-v1.txt (≈26 ming so'z, chastota tartibida) ----
let DQW=null,DQWP=null,DQSL=[],DQSI=-1;
function dqWords(){if(!DQW){try{DQW=DATA_WORDS.split('\n').filter(Boolean)}catch(e){DQW=[]}if(!DQWP)DQWP=fetch('data/words-v1.txt').then(r=>r.ok?r.text():Promise.reject()).then(x=>{const a=x.split('\n').filter(Boolean);if(a.length>DQW.length)DQW=a}).catch(()=>{})}return Promise.resolve(DQW)}
function dqSugg(p){p=String(p||'').toLowerCase().replace(/^\s+/,'');if(!/^[a-z][a-z' -]{0,40}$/.test(p.trimEnd())&&p.trim())return[];p=p.trimEnd();if(!p)return[];const out=[],seen=new Set(),add=(w,m)=>{if(w&&!seen.has(w)&&out.length<8){seen.add(w);out.push({w,m})}};
  (S.ie.words||[]).filter(x=>x.k!=='g'&&x.w&&String(x.w).toLowerCase().startsWith(p)&&String(x.w).toLowerCase()!==p).slice(0,3).forEach(x=>add(String(x.w).toLowerCase(),'mine'));
  dqHistG().filter(x=>x.startsWith(p)&&x!==p).slice(0,2).forEach(x=>add(x,'hist'));
  if(DQW&&!/ /.test(p)){for(let i=0;i<DQW.length&&out.length<8;i++){const w=DQW[i];if(w.length>p.length&&w.startsWith(p))add(w,'')}if(out.length<6&&p.length>=3){for(let i=0;i<DQW.length&&out.length<8;i++){const w=DQW[i];if(w.includes(p)&&!w.startsWith(p))add(w,'in')}}}
  return out}
function dqSgDraw(){const el=document.getElementById('dqsg');if(!el)return;const p=(document.getElementById('dqi')||{}).value||'',q=p.trim().toLowerCase();
  el.innerHTML=DQSL.map((s,i)=>{const w=s.w,k=s.m==='in'?w.indexOf(q):0,pre=s.m==='in'?esc(w.slice(0,k))+'<b>'+esc(w.slice(k,k+q.length))+'</b>'+esc(w.slice(k+q.length)):'<b>'+esc(w.slice(0,q.length))+'</b>'+esc(w.slice(q.length));return `<button role="option" class="${i===DQSI?'on':''}" onmousedown="event.preventDefault()" onclick="dqPick(${i})"><span>${pre}</span>${s.m==='mine'?'<small>📚 lug‘atingda</small>':s.m==='hist'?'<small>🕘 oldingi</small>':''}</button>`}).join('')}
async function dqType(v){DQSI=-1;const q=String(v||'').trim();if(!q){DQSL=[];dqSgDraw();return}if(!DQW)await dqWords();if(String((document.getElementById('dqi')||{}).value||'').trim()!==q)return;DQSL=dqSugg(v);dqSgDraw()}
function dqPick(i){const s=DQSL[i];if(!s)return;DQSL=[];DQSI=-1;dqGo(s.w)}
function dqKey(e){const k=e.key;if(k==='ArrowDown'||k==='ArrowUp'){if(!DQSL.length)return;e.preventDefault();DQSI=k==='ArrowDown'?Math.min(DQSL.length-1,DQSI+1):Math.max(-1,DQSI-1);dqSgDraw();return}
  if(k==='Escape'){DQSL=[];DQSI=-1;dqSgDraw();return}if(k==='Enter'){e.preventDefault();if(DQSI>=0&&DQSL[DQSI]){dqPick(DQSI)}else{DQSL=[];dqGo()}}}
