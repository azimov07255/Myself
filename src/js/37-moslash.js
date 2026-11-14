// ---- Matnni audioga moslash: o'zing qo'ygan matn Whisper vaqtlari bilan moslanadi (matn o'zgarmaydi, so'zma-so'z sinxron) ----
let IAL=null;
const ieAlOk=m=>!!(m.au&&!(m.c&&m.c.length)&&(m.x||'').length>=200);
function ieAlignTx(text,cues,dur){const U=[],re=/[A-Za-z0-9’']+/g;let x;while((x=re.exec(text)))U.push({n:ieNormW(x[0]),a:x.index,b:x.index+x[0].length});
  const W=[];(cues||[]).forEach(c=>(c.w||[]).forEach(w=>{const n=ieNormW(w[0]);if(n&&isFinite(+w[1]))W.push({n,s:+w[1],e:+w[2]})}));if(U.length<20||W.length<20)return{err:'Matn yoki audio juda qisqa.'};
  const n=U.length,m=W.length,M=m+1,eq=(a,b)=>a===b||(a.length>=5&&b.length>=5&&a[0]===b[0]&&Math.abs(a.length-b.length)<=1&&ieLev(a,b)<=1),D=new Uint16Array((n+1)*M);
  for(let i=n-1;i>=0;i--)for(let j=m-1;j>=0;j--)D[i*M+j]=eq(U[i].n,W[j].n)?D[(i+1)*M+j+1]+1:Math.max(D[(i+1)*M+j],D[i*M+j+1]);
  const ts=new Array(n).fill(null),te=new Array(n).fill(null);let i=0,j=0,hit=0;
  while(i<n&&j<m){if(eq(U[i].n,W[j].n)){ts[i]=W[j].s;te[i]=W[j].e;hit++;i++;j++}else if(D[(i+1)*M+j]>=D[i*M+j+1])i++;else j++}
  const ratio=hit/n,end=Math.max(+dur||0,W[m-1].e);
  for(let k=0;k<n;k++)if(ts[k]===null){let a=k-1;while(a>=0&&ts[a]===null)a--;let b=k+1;while(b<n&&ts[b]===null)b++;const t0=a>=0?ts[a]:0,t1=b<n?ts[b]:end,na=a>=0?a:-1,nb=b<n?b:n;ts[k]=t0+(t1-t0)*((k-na)/(nb-na))}
  for(let k=1;k<n;k++)if(ts[k]<ts[k-1])ts[k]=ts[k-1];
  // jumlalar -> qatorlar (qisqalar birlashadi, uzunlar bo'linadi)
  const S2=ieSents(text);let ti=0,P=[];S2.forEach(sn=>{const a=ti;while(ti<n&&U[ti].a<sn.b)ti++;if(ti>a)P.push([a,ti-1])});
  const Q=[];P.forEach(p=>{if(Q.length&&Q[Q.length-1][2]){Q[Q.length-1][1]=p[1];Q[Q.length-1][2]=(Q[Q.length-1][1]-Q[Q.length-1][0]+1)<4;return}Q.push([p[0],p[1],(p[1]-p[0]+1)<4])});
  const R=[];Q.forEach(q=>{const len=q[1]-q[0]+1;if(len>26){const k=Math.ceil(len/18),sz=Math.ceil(len/k);for(let a=q[0];a<=q[1];a+=sz)R.push([a,Math.min(q[1],a+sz-1)])}else R.push([q[0],q[1]])});
  const cu=R.map((r,ix)=>{const a=r[0],b=r[1],nx=R[ix+1],s=ts[a],e0=te[b]!==null?te[b]:ts[b]+0.5,e=Math.max(s+0.3,Math.min(e0,nx?ts[nx[0]]:end+0.5)),mt=/^[^\sA-Za-z0-9’']*/.exec(text.slice(U[b].b))[0];
    return [Math.round(s*100)/100,Math.round(e*100)/100,text.slice(U[a].a,U[b].b+mt.length).replace(/\s+/g,' ').trim(),ts.slice(a,b+1).map(v=>Math.round(v*100)/100)]});
  return{cues:cu,ratio,hit,n}}
async function ieAlignGo(id){const m=ieM().find(x=>x.id===id);if(!m||(IAL&&IAL.busy)||!ieAlOk(m))return;IAL={id,busy:1,err:''};ieMatDraw();
  try{const blob=await ieAudGet(m);if(!blob)throw new Error('Audio bu qurilmada topilmadi.');if(blob.size>24*1048576)throw new Error('Audio 24 MB dan katta (bepul chegara 25 MB).');
    const d=await fnUpload({action:'transcript'},blob,'audio'+ieAudExt(blob.type||'')),r=ieAlignTx(m.x,d.cues,d.dur);if(r.err)throw new Error(r.err);
    if(r.ratio<0.45)throw new Error('Matn audio bilan mos kelmadi (so‘zlarning atigi '+Math.round(r.ratio*100)+'% i mos). To‘g‘ri audio va matn ekanini tekshir.');
    m.c=r.cues;m.x='';m.al=1;m.tr=0;IAL=null;toast('Moslandi: '+Math.round(r.ratio*100)+'% so‘z mos keldi · '+r.cues.length+' qator'+(r.ratio<0.8?'. Ba’zi joylar noaniq bo‘lishi mumkin.':''));save()}
  catch(e){IAL={id,busy:0,err:String(e.message||e).slice(0,220)}}if(IAL)IAL.busy=0;ieMatDraw()}
function ieAlCard(m){const busy=IAL&&IAL.busy&&IAL.id===m.id;return `<div class="goal"><b>🎯 Matnni audioga moslash</b><p class="mu" style="margin:6px 0 8px">O‘zing qo‘ygan matn audio bilan vaqt bo‘yicha moslanadi: chalinganda har bir <b>so‘z</b> birga ajralib yuradi. Matning o‘zgarmaydi. 1 ta so‘rov, audio 24 MB gacha.</p><button class="big" style="margin-top:0" onclick="ieAlignGo(${m.id})" ${busy?'disabled':''}>${busy?'Moslanmoqda… (1–2 daqiqagacha)':'Moslash'}</button><button class="chip" style="margin-top:8px;border:0" onclick="ieTranscribe(${m.id})">yoki audiodan yangi transkript</button>${IAL&&IAL.id===m.id&&IAL.err?`<p style="color:var(--bad);margin:8px 0 0">${esc(IAL.err)}</p>`:''}</div>`}
