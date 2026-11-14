// ---- PUL: matn bilan tez kiritish ("taksi 15 ming", "maosh 3 mln karta"). Hammasi telefonning o'zida, AI ham internet ham kerak emas. Prefiks: ptz ----
let PTZ='';
const ptzN=s=>String(s||'').toLowerCase().replace(/[ʻʼ‘’`´]/g,"'").replace(/\s+/g,' ').trim();
// kategoriya kaliti so'zlar (indeks CATS bo'yicha: 0 Ovqat, 1 Transport, 2 O‘qish, 3 Salomatlik, 4 Kiyim, 5 Ko‘ngil ochish, 6 Aloqa, 7 Uy-joy, 8 Sadaqa)
const PTZK=[
 ['ovqat','non','tushlik','kechki','nonushta','osh','lavash','shaurma','burger','kafe','restoran','choy','kofe','coffee','ichimlik','cola','kola','pitsa','pizza','bozor','go\'sht','gosht','sabzavot','meva','sut','tort','shirinlik','mahsulot','market','oziq','fastfud','somsa'],
 ['taksi','taxi','yandex','yo\'lkira','yolkira','yo\'l','benzin','metro','avtobus','marshrutka','poyezd','samolyot','parkovka','mashina'],
 ['kitob','kurs','dars','ielts','daftar','ruchka','repetitor','o\'qish','oqish','universitet','kontrakt','imtihon'],
 ['dori','apteka','shifokor','vrach','tish','analiz','vitamin','klinika','massaj'],
 ['kiyim','krossovka','ko\'ylak','koylak','shim','poyabzal','kurtka','futbolka'],
 ['kino','o\'yin','oyin','game','konsert','teatr','bilyard','playstation','netflix','obuna','park'],
 ['internet','telefon','paket','tarif','mobil','uzmobile','beeline','ucell','mobiuz','sms','aloqa','wifi'],
 ['ijara','kommunal','svet','elektr','gaz','suv','kvartira','remont','mebel'],
 ['sadaqa','zakot','zakat','xayr','ehson','hadya','fitr']];
const PTZIN=/\b(maosh|stipendiya|daromad|kirim|tushum|tushdi|sovg'a|sovga|bonus|premiya|avans|foyda|savdo)\b/,PTZOUT=/\b(chiqim|xarajat|berdim|sotib|to'ladim|toladim)\b/;
const PTZMUL={ming:1e3,min:1e3,k:1e3,mln:1e6,million:1e6,milyon:1e6,mlrd:1e9,milliard:1e9};
function ptzAmt(t){
  t=t.replace(/(\d)[  ](?=\d{3}(?!\d))/g,'$1');
  const re=/(\d+(?:[.,]\d+)?)\s*(milliard|million|milyon|mlrd|mln|ming|min|k)?(?![a-z0-9'])/g;let m,best=null;
  while((m=re.exec(t))){
    let n=m[1],mul=m[2]?PTZMUL[m[2]]:1,v;
    if(!m[2]&&/^\d{1,3}[.,]\d{3}$/.test(n))v=+n.replace(/[.,]/g,'');   // "15.000" = 15000
    else v=parseFloat(n.replace(',','.'))*mul;
    v=Math.round(v);if(!(v>0))continue;
    if(!best||v>best.a)best={a:v,s:m.index,e:m.index+m[0].length}}
  return best}
function ptzCat(t){
  const toks=t.split(/[^a-z0-9'ʻ]+/).filter(Boolean);
  for(const tk of toks)for(let c=0;c<PTZK.length;c++)for(const st of PTZK[c]){
    if(tk===st||(st.length>=4&&tk.startsWith(st))||(st.length<4&&tk.startsWith(st)&&tk.length<=st.length+2))return c}
  return -1}
function ptzParse(raw){
  const t=ptzN(raw);if(!t)return{ok:false};const am=ptzAmt(t);if(!am)return{ok:false};
  let rest=(t.slice(0,am.s)+' '+t.slice(am.e)),ac='cash',d=dk();
  if(/\b(karta|kartadan|kartaga|plastik|click|payme|uzcard|humo)\b/.test(rest)){ac='card';rest=rest.replace(/\b(karta|kartadan|kartaga|plastik|click|payme|uzcard|humo)\b/g,' ')}
  else if(/\b(naqd|naqdda|naqdga|naqdan|cash)\b/.test(rest)){rest=rest.replace(/\b(naqd|naqdda|naqdga|naqdan|cash)\b/g,' ')}
  if(/\bkecha\b/.test(rest)){d=dAgo(1);rest=rest.replace(/\bkecha\b/g,' ')}
  else if(/\bbugun\b/.test(rest))rest=rest.replace(/\bbugun\b/g,' ');
  rest=rest.replace(/\bso'?m\b/g,' ').replace(/\s+/g,' ').trim();
  const isIn=PTZIN.test(rest)&&!PTZOUT.test(rest),k=isIn?'in':'out';let c;
  if(isIn){c=W==='d'?CIN[1]:/\b(sovg'a|sovga)\b/.test(rest)?CIN[2]:/\b(savdo|dokon|do'kon)\b/.test(rest)?CIN[1]:/\b(maosh|stipendiya|bonus|premiya|avans)\b/.test(rest)?CIN[0]:CIN[3]}
  else{const i=ptzCat(rest);c=i>=0?CATS[i]:CATS[9]}
  const n=rest?rest[0].toUpperCase()+rest.slice(1):'';
  return{ok:true,k,a:am.a,c,ac,d,n}}
function ptzTxt(r){const hrs=(typeof mhnTxt==='function'&&r.k==='out')?mhnTxt(r.a):'';return (r.k==='in'?'Kirim':'Chiqim')+' · '+(CI[r.c]||'•')+' '+r.c+' · '+num(r.a)+' so‘m · '+(r.ac==='card'?'💳 Karta':'💵 Naqd')+(r.d!==dk()?' · '+r.d.slice(8)+'-'+MON[+r.d.slice(5,7)-1]:'')+(r.n?' · “'+r.n+'”':'')+(hrs?' · '+hrs:'')}
function ptzPrev(){const e=document.getElementById('ptzi'),p=document.getElementById('ptzp');if(!e||!p)return;PTZ=e.value;
  if(!PTZ.trim()){p.textContent='';p.className='mu';return}
  const r=ptzParse(PTZ);if(r.ok){p.textContent='✓ '+ptzTxt(r);p.className=''}else{p.textContent='Summani topolmadim (masalan: taksi 15 ming)';p.className='mu'}}
function ptzGo(){
  const r=ptzParse(PTZ);if(!r.ok){toast('Summani topolmadim. Masalan: taksi 15 ming');return}
  putM({id:Date.now(),d:r.d,k:r.k,a:r.a,ac:r.ac,n:r.n,w:W,c:r.c});
  try{if(r.k==='out')pBudChk(W,'out',r.c)}catch(e){}
  const tx=ptzTxt(r);PTZ='';toast('✅ '+tx);save()}
function ptzForm(){
  const r=ptzParse(PTZ);if(!r.ok){toast('Summani topolmadim. Masalan: taksi 15 ming');return}
  K=r.k;FACC=r.ac;FA=String(r.a);FN=r.n;FD=r.d===dk()?'':r.d;FT='';EID=0;FC=Math.max(0,(r.k==='out'?CATS:CIN).indexOf(r.c));PTZ='';render();scrollTo(0,0)}
function ptzUi(){
  if(uiG('trk_ptz')==='0')return '';
  return `<div class="goal" style="margin-top:12px"><b>⚡ Tez yozish</b><p class="mu" style="margin:4px 0 8px;font-size:13px">Oddiy gap bilan yoz: “taksi 15 ming”, “tushlik 32000 karta”, “maosh 3 mln”.</p>
  <div class="in"><input id="ptzi" placeholder="Nima va qancha?" value="${esc(PTZ)}" autocomplete="off" oninput="ptzPrev()" onkeydown="if(event.key==='Enter'){event.preventDefault();ptzGo()}"><button class="btn" onclick="ptzGo()">Yozish</button></div>
  <p id="ptzp" class="mu" style="margin:0 0 6px;font-size:13px"></p><button class="btn s" onclick="ptzForm()" style="font-size:13px">Formada tahrirlash</button></div>`}
function ptzJl(){return `<p class="mu" style="margin:12px 0 4px;font-size:12px"><b>💰 Pul: tez yozish oynasi</b></p>${jlSeg('trk_ptz','1',[['1','Ko‘rinsin'],['0','Yashirin (avvalgidek)']])}`}
