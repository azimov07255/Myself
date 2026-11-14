// ---- Matnda belgilangan 1-8 so'zli ibora: ma'nosi (AI), eshitish, lug'atga qo'shish ----
let ISEL=null,ISELT=0;
function ieSelRead(){try{const s=window.getSelection&&window.getSelection();if(!s||!s.rangeCount||s.isCollapsed)return null;const t=s.toString().replace(/\s+/g,' ').trim();if(t.length<2||t.length>80)return null;const n=ieTok(t).length;if(n<1||n>8)return null;
  const r=s.getRangeAt(0),pe=x=>{const el=x.nodeType===1?x:x.parentElement;return el&&el.closest?el.closest('.ietx .iep'):null},a=pe(r.startContainer),b=pe(r.endContainer);if(!a||a!==b)return null;
  const pre=document.createRange();pre.selectNodeContents(a);pre.setEnd(r.startContainer,r.startOffset);const off=pre.toString().length,S=ieSents(a.textContent),sn=S[ieSentAt(S,off)]||S[0],ctx=a.textContent.slice(sn.a,sn.b).trim().slice(0,300);
  return{t,n,ctx,pos:ieRdPos(r.startContainer.nodeType===1?r.startContainer:r.startContainer.parentElement)}}catch(e){return null}}
function ieSelUpdate(){const x=document.getElementById('iem')?ieSelRead():null;ISEL=x;let bar=document.getElementById('iesel');if(!x){if(bar)bar.remove();return}
  if(!bar){bar=document.createElement('div');bar.id='iesel';bar.className='iesel';document.getElementById('iem').appendChild(bar)}
  const pl=document.getElementById('iepl');bar.style.bottom=((pl?pl.offsetHeight:0)+10)+'px';
  bar.innerHTML=`<span class="t">“${esc(x.t.length>40?x.t.slice(0,38)+'…':x.t)}”</span><button class="btn" onclick="ieSelGo()">✨ Ma’nosi</button><button class="btn s" onclick="ieSelSay()" aria-label="Eshitish">🔊</button><button class="btn s" onclick="ieSelAdd()" aria-label="Lug‘atga qo‘shish">➕</button>`}
function ieSelHide(){const b=document.getElementById('iesel');if(b)b.remove();ISEL=null}
function ieSelClear(){try{window.getSelection().removeAllRanges()}catch(e){}}
function ieSelGo(){const x=ISEL;if(!x)return;IRH=x.pos;ieSheetClose();IMS={word:x.t,ctx:x.ctx,def:null,busy:0,err:''};ieGlSeedSel(IMS,x.t);const el=document.createElement('div');el.id='iesh';el.className='mfs';document.getElementById('iem').appendChild(el);ieSelHide();ieSelClear();ieSheetWord();ieDefine()}
function ieSelSay(){if(ISEL)ieSay(ISEL.t)}
function ieSelAdd(){const x=ISEL;if(!x)return;const m=ieM().find(y=>y.id===IMT),ok=x.n>1?ieVocAdd({p:x.t,ctx:x.ctx},'c',m?m.id:0):ieVocAdd({w:x.t,ctx:x.ctx},'w',m?m.id:0);ieSelHide();ieSelClear();if(ok){toast('Qo‘shildi: '+x.t+'. Ma’nosini bilish uchun “Ma’nosi” ni bos.');save();ieMatDraw()}else toast('Bu lug‘atda bor')}
document.addEventListener('selectionchange',()=>{clearTimeout(ISELT);ISELT=setTimeout(ieSelUpdate,220)});
