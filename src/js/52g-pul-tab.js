// ---- PUL: tablar tartibi. Ixcham: Bosh, Tarix, Hisobot, Reja + "Yana" (Qarzlar, Zakat). "Avvalgidek": 6 ta tab. Prefiks: ptb ----
const ptbOn=()=>{try{return localStorage.getItem('trk_ptb')!=='a'}catch(e){return true}};
function ptbSeg(){
  const b=x=>`<button class="${PV===x[0]?'on':''}" onclick="PV='${x[0]}';render()">${x[1]}</button>`;
  if(!ptbOn())return [['b','🏠 Bosh'],['t','🧾 Tarix'],['q','🤝 Qarzlar'],['h','📈 Hisobot'],['r','🎯 Reja'],['z','🕌 Zakat']].map(b).join('');
  const more=PV==='q'||PV==='z';
  return [['b','🏠 Bosh'],['t','🧾 Tarix'],['h','📈 Hisobot'],['r','🎯 Reja']].map(b).join('')+`<button class="${more?'on':''}" onclick="PV='${PV==='z'?'z':'q'}';render()">⋯ Yana</button>`}
function ptbSub(){
  if(!ptbOn()||!(PV==='q'||PV==='z'))return '';
  return `<div class="seg" style="margin-top:8px"><button class="${PV==='q'?'on':''}" onclick="PV='q';render()">🤝 Qarzlar</button><button class="${PV==='z'?'on':''}" onclick="PV='z';render()">🕌 Zakat</button></div>`}
function ptbJl(){return `<p class="mu" style="margin:12px 0 4px;font-size:12px"><b>💰 Pul tablari</b></p>${jlSeg('trk_ptb','g',[['g','Ixcham (4 + Yana)'],['a','Avvalgidek (6 ta tab)']])}`}
