// ---- Vidjet (iPhone, Scriptable): kichik xulosa serverga yoziladi, vidjet uni maxfiy kalit bilan o'qiydi. Pul va salomatlik YUBORILMAYDI ----
let WDG={busy:0,err:'',ok:''},WDQ={sig:'',t:0};
function wdDb(){return sb}
const wdMask=t=>t?t.slice(0,4)+'…'+t.slice(-4):'';
function wdTok(){const a=new Uint8Array(16);try{crypto.getRandomValues(a)}catch(e){for(let i=0;i<16;i++)a[i]=Math.floor(Math.random()*256)}return[...a].map(b=>b.toString(16).padStart(2,'0')).join('')}
function wdNext(){const n=new Date(),dow=n.getDay(),m=n.getHours()*60+n.getMinutes(),b=bl().filter(x=>x.d&&rjIn(x,dk(),dow)&&x.s>m&&!String(x.id).startsWith('uyqu')).sort((p,q)=>p.s-q.s)[0];return b?{t:String(b.t).slice(0,40),at:hm(b.s)}:null}
function wdSnap(){const k=dk(),n=new Date(),hb=S.hb[k]||{},act=S.hab.filter(x=>!hkOn(k,x.id)),nd=(S.nm&&S.nm.d&&S.nm.d[k])||{},g=S.goals.find(x=>gpct(x)<100)||S.goals[0];
  return{v:1,d:k,dow:DAYS[n.getDay()],dd:n.getDate()+' '+MON[n.getMonth()],hab:[act.filter(x=>hb[x.id]).length,act.length],nm:[['fajr','dhuhr','asr','maghrib','isha'].filter(p=>nd[p]===1).length,5],hf:[((S.q&&S.q.ny)||{})[k]||0,(S.q&&S.q.ppd)||0],fm:(S.fm||{})[k]||0,top:(S.top[k]||[]).slice(0,3).map(x=>({t:String(x.t).slice(0,40),x:x.x?1:0})),nx:wdNext(),ie:S.ie&&S.ie.ex?dl(S.ie.ex):null,gl:g?{t:String(g.t).slice(0,40),p:gpct(g)}:null}}
async function wdPush(force){const w=S.wd,db=wdDb();if(!w||!w.on||!w.t||!db||!UID||WDG.busy)return;const snap=wdSnap(),sig=JSON.stringify(snap);if(!force&&sig===WDQ.sig&&Date.now()-WDQ.t<600000)return;WDG.busy=1;
  try{const r=await db.from('widget_snap').upsert({user_id:UID,token:w.t,snap,updated_at:new Date().toISOString()});if(r&&r.error)throw r.error;WDQ={sig,t:Date.now()};WDG.err='';WDG.ok=new Date().toLocaleTimeString('sv').slice(0,5)}
  catch(e){const m=String((e&&e.message)||e);WDG.err=/widget_snap|relation|does not exist|schema cache/i.test(m)?'Baza jadvali yo‘q: server-setup/widget.sql ni Supabase SQL Editor’da ishga tushiring.':m.slice(0,120)}WDG.busy=0;if(tab==='s')render()}
function wdOn(){if(!wdDb()||!UID){toast('Avval hisobga kiring');return}S.wd={on:1,t:wdTok()};WDQ={sig:'',t:0};save();wdPush(true)}
function wdNew(){if(!confirm('Yangi maxfiy kalit yaratilsinmi? Eski vidjet ishlamay qoladi, skriptni qayta nusxalab qo‘yasan.'))return;S.wd={on:1,t:wdTok()};WDQ={sig:'',t:0};save();wdPush(true)}
async function wdOff(){if(!confirm('Vidjet o‘chirilsinmi? Serverdagi xulosa ham o‘chadi.'))return;try{const db=wdDb();if(db&&UID)await db.from('widget_snap').delete().eq('user_id',UID)}catch(e){}S.wd={on:0,t:''};WDQ={sig:'',t:0};WDG.err='';save()}
const WDT=`// Kunlik tizim vidjeti (Scriptable). Skriptni o'zgartirma: ilova yaratgan.
const URL_ = "__URL__";
const KEY_ = "__KEY__";
const C = { bg: "#0f1b2d", tx: "#f2efe6", mu: "#9fb0c8", ac: "#4fbf8b", wr: "#e0a458" };
function bar(a, b) { const n = 8, f = b > 0 ? Math.round(Math.min(1, a / b) * n) : 0; return "▰".repeat(f) + "▱".repeat(n - f); }
async function getData() {
  const r = new Request(URL_);
  if (KEY_) r.headers = { Authorization: "Bearer " + KEY_, apikey: KEY_ };
  const j = await r.loadJSON();
  const sc = r.response && r.response.statusCode;
  if (!j || !j.snap) throw new Error(((j && (j.error || j.message || j.msg)) || "Malumot yoq") + (sc ? " (" + sc + ")" : ""));
  return j;
}
function row(w, label, val, color) {
  const s = w.addStack(); s.centerAlignContent();
  const a = s.addText(label); a.font = Font.systemFont(12); a.textColor = new Color(C.mu);
  s.addSpacer();
  const b = s.addText(val); b.font = Font.boldSystemFont(13); b.textColor = new Color(color || C.tx);
  w.addSpacer(3);
}
async function build() {
  const w = new ListWidget();
  w.backgroundColor = new Color(C.bg);
  w.setPadding(12, 14, 12, 14);
  let j;
  try { j = await getData(); } catch (e) {
    const t = w.addText("Kunlik tizim"); t.font = Font.boldSystemFont(14); t.textColor = new Color(C.tx);
    const m = w.addText("Malumot olinmadi: " + String(e.message || e).slice(0, 80)); m.font = Font.systemFont(11); m.textColor = new Color(C.wr);
    return w;
  }
  const d = j.snap, fam = config.widgetFamily || "medium";
  const h = w.addText("Kunlik tizim · " + (d.dow || "") + " " + (d.dd || "")); h.font = Font.boldSystemFont(13); h.textColor = new Color(C.tx);
  w.addSpacer(6);
  const R = [];
  if (d.hab) R.push(["Odatlar " + bar(d.hab[0], d.hab[1]), d.hab[0] + "/" + d.hab[1], d.hab[1] && d.hab[0] >= d.hab[1] ? C.ac : C.tx]);
  if (d.nm) R.push(["Namoz " + bar(d.nm[0], d.nm[1]), d.nm[0] + "/" + d.nm[1], d.nm[0] >= d.nm[1] ? C.ac : C.tx]);
  if (d.nx) R.push(["Keyingi", d.nx.at + " " + d.nx.t, C.tx]);
  if (d.hf && d.hf[1]) R.push(["Hifz", d.hf[0] + "/" + d.hf[1] + " bet", d.hf[0] >= d.hf[1] ? C.ac : C.tx]);
  if (d.fm !== undefined) R.push(["Fokus", d.fm + " daq", C.tx]);
  if (d.top && d.top.length) R.push(["Top-3", d.top.filter(function (x) { return x.x; }).length + "/" + d.top.length, C.tx]);
  if (d.ie !== null && d.ie !== undefined) R.push(["IELTS imtihon", d.ie + " kun", d.ie <= 14 ? C.wr : C.tx]);
  if (d.gl) R.push(["Maqsad", d.gl.p + "%", C.tx]);
  const cap = fam === "small" ? 3 : fam === "medium" ? 5 : 8;
  R.slice(0, cap).forEach(function (r) { row(w, r[0], r[1], r[2]); });
  if (fam === "large" && d.top) d.top.forEach(function (x) { const t = w.addText((x.x ? "✓ " : "○ ") + x.t); t.font = Font.systemFont(11); t.textColor = new Color(x.x ? C.ac : C.mu); });
  w.addSpacer();
  const u = j.updated_at ? new Date(j.updated_at) : null;
  const f = w.addText(u ? "Yangilandi " + ("0" + u.getHours()).slice(-2) + ":" + ("0" + u.getMinutes()).slice(-2) : "");
  f.font = Font.systemFont(9); f.textColor = new Color(C.mu);
  w.refreshAfterDate = new Date(Date.now() + 15 * 60 * 1000);
  return w;
}
const widget = await build();
if (config.runsInWidget) { Script.setWidget(widget); } else { await widget.presentMedium(); }
Script.complete();
`;
function wdScript(){const k=/^eyJ/.test(CFG.key||'')?CFG.key:'';return WDT.replace('__URL__',CFG.url+'/functions/v1/widget?t='+((S.wd&&S.wd.t)||'')).replace('__KEY__',k)}
function wdCopy(){const t=wdScript();if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(t).then(()=>toast('Skript nusxalandi')).catch(()=>prompt('Nusxalang:',t));else prompt('Nusxalang:',t)}
function wdCard(){const w=S.wd||{};if(!wdDb()||!UID)return '<p class="mu" style="margin:0">Vidjet uchun avval hisobga kirish kerak.</p>';
  if(!w.on)return `<p class="mu" style="margin:0 0 8px">iPhone bosh ekraniga kichik panel: odat, namoz, hifz, keyingi reja, IELTS imtihonigacha kun. Pul va salomatlik ma‘lumoti yuborilmaydi. Bepul Scriptable ilovasi kerak.</p><button class="btn" onclick="wdOn()">Vidjetni yoqish</button>`;
  return `<p style="margin:0 0 6px"><b>Yoqilgan.</b> Maxfiy kalit: <code>${esc(wdMask(w.t))}</code>${WDG.ok?`<br><span class="mu" style="font-size:13px">Oxirgi yangilash: ${esc(WDG.ok)}</span>`:''}</p>${WDG.err?`<p style="color:var(--bad);margin:0 0 8px">${esc(WDG.err)}</p>`:''}
   <div class="in" style="flex-wrap:wrap"><button class="btn" onclick="wdCopy()">📋 Skriptni nusxalash</button><button class="btn s" onclick="wdPush(true)" ${WDG.busy?'disabled':''}>${WDG.busy?'…':'Hozir yangila'}</button></div><div class="in" style="flex-wrap:wrap;margin-top:6px"><button class="btn s" onclick="wdNew()">Kalitni almashtirish</button><button class="btn s" onclick="wdOff()">O‘chirish</button></div>
   <ol class="mu" style="font-size:13px;padding-left:18px;margin:10px 0 0;line-height:1.5"><li>App Store’dan <b>Scriptable</b> (bepul) o‘rnat.</li><li>Supabase’da bir marta: <code>widget.sql</code> ni SQL Editor’da ishga tushir va <code>widget</code> funksiyasini yukla.</li><li>“Skriptni nusxalash” → Scriptable → <b>+</b> → yopishtir → nomi: Kunlik tizim.</li><li>Bosh ekranda ekranni uzoq bos → <b>+</b> → Scriptable → o‘lcham → vidjetni bos → Script: Kunlik tizim.</li></ol><p class="mu" style="font-size:12px;margin:8px 0 0">iOS vidjetni o‘zi belgilagan oraliqda (taxminan 15–60 daqiqa) yangilaydi. Skriptdagi kalit sirli: boshqalarga ko‘rsatma. Yo‘qolsa “Kalitni almashtirish”.</p>`}
try{setInterval(()=>{try{wdPush()}catch(e){}},120000);document.addEventListener('visibilitychange',()=>{if(document.hidden){try{wdPush()}catch(e){}}})}catch(e){}
