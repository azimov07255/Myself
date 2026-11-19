// ---- 3D: Isolation yo'l xaritasi, tanga minorasi, "Hozir" kartasi parallaksi, namoz osmoni. Hammasi CSS perspektiva/SVG, tashqi kutubxonasiz. Sozlamalar → Jilo'dan o'chiriladi. Prefiks: d3 ----
const d3On=()=>uiG('trk_3d')!=='0';
// ---------- 2. yo'l xaritasi (marafon) ----------
function d3Path(I){
  if(!d3On()||I.n>24||I.n<3)return '';
  const n=I.n,cols=4,rows=Math.ceil(n/cols),T=rows>5?46:56,G=12,wd=cols*(T+G),ht=rows*(T+G),H=Math.round(200+rows*30),cw=((document.getElementById('app')||{}).clientWidth)||358,bd=wd*.79+ht*.62,sc=Math.max(.5,Math.min(1,(cw-30)/bd)).toFixed(3);
  const m=I.m,ex=(S.pr&&S.pr.exam)?mrfDiff(m.start,S.pr.exam):-1;let tl='';
  for(let i=0;i<n;i++){
    let c=i%cols;const r=Math.floor(i/cols);if(r%2)c=cols-1-c;
    const k=mrfAt(m.start,i),fu=k>I.td,now=k===I.td,dy=fu?null:mrfDay(k);
    const st=fu?'f':now?'t':dy.full?'d':dy.pc>=60?'p':'m',x=c*(T+G),y=r*(T+G),z=now?22:0;
    const layers=[1,2,3,4,5].map(q=>`<i style="transform:translateZ(${-q*3}px);filter:brightness(${1-q*.07})"></i>`).join('');
    const up=i===ex?'<em class="d3up d3flag">🚗</em>':st==='d'?'<em class="d3up d3coin">✓</em>':now?'<em class="d3up d3pin">📍</em>':i===n-1?'<em class="d3up d3flag">🏁</em>':'';
    tl+=`<div class="d3t ${st}" style="left:${x}px;top:${y}px;width:${T}px;height:${T}px;transform:translateZ(${z}px)">${layers}<b>${i+1}</b>${up}</div>`}
  return `<h2>🧭 Yo‘l xaritasi</h2><div class="d3path" style="height:${H}px" role="img" aria-label="Marafon yo‘li: ${I.dc} / ${n} kun"><div class="d3plane" style="--s:${sc};width:${wd}px;height:${ht}px;left:calc(50% - ${wd/2}px);top:${Math.round((H-ht)/2-8)}px">${tl}</div></div>
   <p class="mu" style="margin:-4px 0 6px;font-size:12px">🟩 to‘liq kun · 🟢 qisman · 🟧 bugun${ex>=0&&ex<n?' · 🚗 Prava imtihoni':''} · 🏁 oxirgi kun</p>`}
// ---------- 3. tanga minorasi ----------
function d3CoinsCard(){
  if(!d3On()||typeof drjPlan!=='function')return '';const P=drjPlan(),g=P.g;if(!g||!(g.a>0))return '';
  const pct=Math.min(1,g.s/g.a),N=24,fi=g.s>0?Math.max(1,Math.round(pct*N)):0;
  const solid=[...Array(fi)].map((_,k)=>[0,1,2,3].map(j=>`<div class="d3co" style="transform:translateZ(${k*6+j*1.5}px);filter:brightness(${.8+j*.07})"></div>`).join('')).join('');
  const ghost=[...Array(N-fi)].map((_,k)=>`<div class="d3co g" style="transform:translateZ(${(fi+k)*6}px)"></div>`).join('');
  return `<h2>🪙 Jamg‘arma minorasi</h2><div class="d3coins" role="img" aria-label="Jamg‘arma: ${Math.round(pct*100)}%"><div class="d3top"><span>${esc(g.t||'Maqsad')}</span><b>${Math.round(pct*100)}%</b></div><div class="d3big"><div class="d3bigc">${g.usd?'$':'₮'}</div></div><div class="d3stack"><div class="d3base"></div>${ghost}${solid}</div><div class="d3bot">${num(g.s)} / ${num(g.a)} so‘m${P.eta?' · ~'+P.eta+' oy':''}</div></div>`}
// ---------- 5. "Hozir" kartasi: barmoq bilan egiladi ----------
function d3Tilt(e){const el=e.target&&e.target.closest&&e.target.closest('.hero.d3c');if(!el||!d3On())return;const r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;el.style.animation='none';el.style.transform=`perspective(900px) rotateX(${(-y*16).toFixed(1)}deg) rotateY(${(x*20).toFixed(1)}deg)`}
function d3TiltEnd(){document.querySelectorAll('.hero.d3c').forEach(e=>{e.style.animation='';e.style.transform=''})}
try{document.addEventListener('pointermove',d3Tilt,{passive:true});['pointerup','pointercancel','touchend'].forEach(t=>document.addEventListener(t,d3TiltEnd,{passive:true}))}catch(e){}
// ---------- 6. namoz osmoni ----------
function d3Sky(){
  if(!d3On()||typeof ptTimes!=='function')return '';let t=null;try{t=ptTimes()}catch(e){}if(!t||!(t.Isha>t.Fajr))return '';
  const now=new Date(),nm=now.getHours()*60+now.getMinutes(),F=t.Fajr,I2=t.Isha,sp=I2-F,tp=v=>Math.min(1,Math.max(0,(v-F)/sp)),pos=u=>{const a=Math.PI*(1-u);return[195+150*Math.cos(a),215-150*Math.sin(a)]};
  const night=nm<F||nm>I2,[sx,sy]=pos(tp(nm)),nx=ptNext();
  const marks=PNAMES.map(([k,nn])=>{const u=tp(t[k]),[x,y]=pos(u),sd=u<.25?'r':u>.7?'l':'m',ax=sd==='r'?x+13:sd==='l'?x-13:x,an=sd==='r'?'start':sd==='l'?'end':'middle',ny=sd==='m'?y-15:y+3,ty=sd==='m'?y+25:y+16;return `<g><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="7" fill="#fff" stroke="#2b6a55" stroke-width="3"/><text x="${ax.toFixed(1)}" y="${ny.toFixed(1)}" text-anchor="${an}" font-size="11" font-weight="700" fill="#fff">${nn}</text><text x="${ax.toFixed(1)}" y="${ty.toFixed(1)}" text-anchor="${an}" font-size="10" fill="#cfe9de">${hm(t[k])}</text></g>`}).join('');
  const body=night?`<circle cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="20" fill="#e8ecf5"/><circle cx="${(sx+8).toFixed(1)}" cy="${(sy-4).toFixed(1)}" r="18" fill="#10244a"/>`:`<circle class="d3gl" cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="58" fill="url(#d3gl)"/><circle cx="${sx.toFixed(1)}" cy="${sy.toFixed(1)}" r="22" fill="url(#d3sn)"/>`;
  return `<div class="d3sky ${night?'n':''}" role="img" aria-label="Namoz vaqtlari: quyosh yoyi"><div class="d3skyt">${nx?'Keyingi: <b>'+nx.n+' '+hm(nx.t)+'</b> · '+fmt(nx.left).trim()+' qoldi':'<b>Bugungi namozlar tugadi</b>'}</div>
   <svg viewBox="0 0 390 250" width="100%" aria-hidden="true"><defs><radialGradient id="d3sn" cx="35%" cy="30%"><stop offset="0" stop-color="#fff7c2"/><stop offset=".5" stop-color="#ffc247"/><stop offset="1" stop-color="#e07a1a"/></radialGradient><radialGradient id="d3gl"><stop offset="0" stop-color="#ffd36b" stop-opacity=".75"/><stop offset="1" stop-color="#ffd36b" stop-opacity="0"/></radialGradient></defs>
   <path d="M45 215 A150 150 0 0 1 345 215" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="2.5" stroke-dasharray="5 7"/><path d="M45 215 A150 150 0 0 1 ${sx.toFixed(1)} ${sy.toFixed(1)}" fill="none" stroke="#ffd36b" stroke-width="4" stroke-linecap="round"/>
   <polygon points="0,215 390,215 440,250 -50,250" fill="rgba(0,0,0,.25)"/>${[-60,10,80,150,220,290,360,430].map(x=>`<line x1="${x}" y1="215" x2="${(x-195)*1.9+195}" y2="250" stroke="rgba(255,255,255,.12)"/>`).join('')}${body}${marks}</svg></div>`}
function d3Jl(){const o=d3On();return `<p class="mu" style="margin:12px 0 4px;font-size:12px"><b>🧊 3D animatsiyalar</b> <span style="font-size:11px">(Isolation yo‘li, tanga minorasi, Hozir kartasi, namoz osmoni)</span></p><div class="seg" style="margin-bottom:10px"><button class="${o?'on':''}" onclick="bmOpt('3d','1')">Yoqilgan</button><button class="${o?'':'on'}" onclick="bmOpt('3d','0')">O‘chirilgan (avvalgidek)</button></div>`}
