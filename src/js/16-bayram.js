// ---- Bayram: konfetti va yutuqlar ----
function confetti(){
  try{if(matchMedia('(prefers-reduced-motion:reduce)').matches)return}catch(e){}
  const W=window.innerWidth||360,H=window.innerHeight||640,c=document.createElement('canvas');c.style.cssText='position:fixed;left:0;top:0;width:100%;height:100%;pointer-events:none;z-index:300';c.width=W;c.height=H;document.body.appendChild(c);
  const x=c.getContext('2d'),cols=['#e2b857','#46c4b2','#d96f8f','#6f9fd8','#b27ad6','#ffffff'];
  const P=[...Array(130)].map(()=>({x:W/2+(Math.random()-.5)*80,y:H*.55,vx:(Math.random()-.5)*14,vy:-(Math.random()*13+6),g:.32+Math.random()*.15,s:5+Math.random()*6,r:Math.random()*6,vr:(Math.random()-.5)*.4,c:cols[Math.floor(Math.random()*cols.length)]}));
  let t=0;(function f(){t++;x.clearRect(0,0,W,H);P.forEach(p=>{p.vy+=p.g;p.x+=p.vx;p.y+=p.vy;p.vx*=.99;p.r+=p.vr;x.save();x.translate(p.x,p.y);x.rotate(p.r);x.fillStyle=p.c;x.globalAlpha=Math.max(0,1-t/110);x.fillRect(-p.s/2,-p.s/2,p.s,p.s*.6);x.restore()});if(t<110)requestAnimationFrame(f);else c.remove()})();
  try{if(navigator.vibrate)navigator.vibrate([40,40,60])}catch(e){}}
const MIL=[7,14,30,60,100,365];
let CELB=0;
function celeb(){
  const k=dk();S.cel=S.cel||{};const C=S.cel;let msg='';
  const sc=scoreOf(k).p,L=xpInfo(),ms=h=>MIL.filter(m=>hst(h.id)>=m).pop()||0,bk=S.kt.books.filter(b=>b.st==='t').length;
  if(!C.init){C.init=1;C.d={};C.d[k]=sc>=100?1:0;C.lv=L.L;C.hs={};S.hab.forEach(h=>{C.hs[h.id]=ms(h)});C.hc=S.q.hc;C.bk=bk;qsave();return}
  C.d=C.d||{};C.hs=C.hs||{};
  if(sc>=100&&!C.d[k]){C.d[k]=1;msg='Kun mukammal, 100%! 🎉'}
  if(!C.v2){C.v2=1;C.lv=L.L}if(L.L>(C.lv||0)){C.lv=L.L;msg='Yangi daraja: '+L.L+' · '+L.name+' 🚀'}
  S.hab.forEach(h=>{const m=ms(h);if(m>(C.hs[h.id]||0)){C.hs[h.id]=m;msg=(h.e||'🔥')+' '+h.t+': '+m+' kunlik seriya!'}});
  if(S.q.hc>(C.hc||0)){C.hc=S.q.hc;msg='Hatm tugadi, Alhamdulillah! 🤲'}
  if(bk>(C.bk||0)){C.bk=bk;msg='Kitob tugatildi! 📚'}
  {const dp=dayPts(k).t,st=rwStreak();C.xg=C.xg||{};if(dp>=rwGoal(k)&&dp>=DAYMIN&&!C.xg[k]){C.xg[k]=1;if(!msg)msg='Kun maqsadi bajarildi: '+dp+' XP ⚡'}if(MIL.includes(st)&&C.sm!==st+'@'+k){C.sm=st+'@'+k;msg='🔥 '+st+' kunlik seriya!'}}if(msg){confetti();toast(msg);qsave()}}
function badgeHtml(){
  const q=S.q,xp=xpInfo(),fin=S.kt.books.filter(b=>b.st==='t').length,md_=mdone(),words=S.ie.words.length;
  let perfect=0,bestDay=0;for(let i=0;i<120;i++){if(scoreOf(dAgo(i)).p>=100)perfect++;bestDay=Math.max(bestDay,dayPts(dAgo(i)).t)}
  const mocks=S.ie.tests.filter(t=>t.k==='M').map(t=>ieRound(Object.values(t.b).reduce((a,x)=>a+x,0)/Object.keys(t.b).length)),best=mocks.length?Math.max(...mocks):0;
  const gym=new Set(S.gym.log.map(x=>x.d)).size,hs=S.hab.length?Math.max(...S.hab.map(h=>hst(h.id))):0;
  const B=[['🔥','7 kunlik seriya',xp.st,7],['🔥','30 kunlik seriya',xp.st,30],['💎','100 kunlik seriya',xp.st,100],['⭐','10 mukammal kun',perfect,10],['✅','Odatda 14 kun',hs,14],
    ['📖','Birinchi hatm',q.hc,1],['🧠','100 bet yodlandi',Math.floor(md_),100],['🕌','300 bet yodlandi',Math.floor(md_),300],['🔤','100 ta so‘z',words,100],['🎓','IELTS mock 7.0',best,7],['📚','Birinchi kitob',fin,1],['💪','20 ta zal kuni',gym,20],['🏅','5-daraja',xp.L,5],['🥇','10-daraja',xp.L,10],['💎','20-daraja',xp.L,20],['🎁','Birinchi mukofot olindi',rw().buy.filter(b=>b.k!=='sh').length,1],['⚡','Bir kunda 200 XP',bestDay,200],['🛡','Qalqon seriyani saqladi',rw().su.length,1],['🏆','Haftalik chellenj',Object.keys(rw().wk).length,1]];
  const got=B.filter(b=>b[2]>=b[3]).length;
  return `<h2>🏆 Yutuqlar (${got}/${B.length})</h2><div class="bdg">${B.map(b=>`<div class="bd ${b[2]>=b[3]?'on':''}"><i>${b[0]}</i>${b[1]}<small>${Math.min(b[2],b[3])}/${b[3]}</small></div>`).join('')}</div>`}

