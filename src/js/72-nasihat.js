// ---- KUNLIK NASIHATCHI: bugungi kunga mos amallar (Juma, dushanba/payshanba ro'zasi, hijriy maxsus kunlar), nafs mashqi va eslatma. AI kerak emas ----
// Eslatma: bu fatvo emas. Manbalar: Buxoriy, Muslim, Tirmiziy, Abu Dovud, Hokim, Nasoiy (umumiy mashhur sunnatlar). Mazhabga bog'liq tafsilotlar ataylab kiritilmagan.
const NSD=[ // 0 = yakshanba ... 6 = shanba
{n:'Yakshanba',e:'🌅',tag:'Yangi haftani niyat bilan boshla',b:'Haftaning eng muhim 3 ishini tanla va niyat qil',sun:[],tav:['Haftaning eng muhim 3 ishini yoz','Uy va oila ishlariga vaqt ajrat','Kelasi hafta uchun Qur‘on va IELTS rejasini tekshir']},
{n:'Dushanba',e:'🌤',tag:'Rejali va barakali hafta boshlanishi',b:'Ro‘za tutish sunnat; eng qiyin ishni ertalab qil',sun:[{id:'dr',t:'Dushanba kuni nafl ro‘za tut (niyating bo‘lsa)',s:'Muslim'}],tav:['Eng qiyin ishni ertalab boshla','Bugun kimgadir yaxshilik qil: salom, yordam, duo']},
{n:'Seshanba',e:'🔥',tag:'Fokus kuni',b:'Bitta muhim ishga chuqur fokus',sun:[],tav:['2 ta Pomodoro: eng muhim ish uchun','Bugun telefonsiz 1 soat','Kechqurun qisqa muhosaba qil']},
{n:'Chorshanba',e:'⚖️',tag:'Hafta o‘rtasi: tekshir va to‘g‘rila',b:'Haftaning yarmi: nima qoldi, nimani to‘g‘rilash kerak',sun:[],tav:['Hafta rejasini tekshir: nima qoldi?','Qur‘on takrorini kechiktirma','Bitta xatongni tuzat va daftarga yoz']},
{n:'Payshanba',e:'🌙',tag:'Haftani yakunlash va Jumaga tayyorlanish',b:'Ro‘za sunnat; Jumaga kiyim va niyatni tayyorla',sun:[{id:'pr',t:'Payshanba kuni nafl ro‘za tut (niyating bo‘lsa)',s:'Tirmiziy, Nasoiy'},{id:'pk',t:'Kahf surasini payshanba shomidan o‘qishni boshlashing mumkin',s:'Hokim, Nasoiy'}],tav:['Qilinmagan vazifalarni yop','Jumaga toza kiyim va vaqtingni tayyorla','Ko‘proq istig‘for va salovat ayt']},
{n:'Juma',e:'🕌',tag:'Haftaning eng fazilatli kuni, “kichik hayit”',b:'G‘usl, toza kiyim, erta masjid, Kahf surasi, ko‘p salovat, ijobat soatida duo',sun:[
 {id:'j1',t:'G‘usl qil (ta’kidlangan sunnat)',s:'Buxoriy, Muslim'},
 {id:'j2',t:'Toza kiyim kiy, atir ishlat, misvok qil, tirnoq va tozalikka e’tibor ber',s:'Buxoriy, Muslim'},
 {id:'j3',t:'Jumaga erta bor: har qadam savob, avval borganning ajri katta',s:'Buxoriy, Muslim'},
 {id:'j4',t:'Xutbani tinch va diqqat bilan tingla, gapirma, telefonni o‘chir',s:'Buxoriy, Muslim'},
 {id:'j5',t:'Kahf surasini o‘qi (payshanba shomidan juma shomigacha)',s:'Hokim, Nasoiy'},
 {id:'j6',t:'Rasululloh ﷺ ga ko‘p salovat ayt',s:'Abu Dovud'},
 {id:'j7',t:'Ijobat soatida duo qil: ulamolar fikricha xutba–namoz oralig‘i yoki asrdan keyin shomgacha',s:'Buxoriy, Muslim'},
 {id:'j8',t:'Jumadan keyingi sunnat namozlarni o‘qi (mazhabingga ko‘ra)',s:'Muslim'}],
 tav:['Kichik bo‘lsa ham sadaqa qil','Ota-ona va qarindoshlar bilan aloqa qil (sila rahm)','Hafta muhosabasini qil: nima yaxshi ketdi, nima yetishmadi','Do‘stlarga duo va salom yubor']},
{n:'Shanba',e:'🌿',tag:'Dam, tiklanish va tayyorgarlik',b:'Dam ol, oilaga vaqt ajrat, ertangi haftaga tayyorlan',sun:[],tav:['Jismoniy mashq yoki 30 daqiqa yurish','Oila bilan sifatli vaqt','Hafta natijalarini ko‘rib chiq va ertangi kunga niyat qil']}];
const NSALL=[{id:'nm',t:'Besh vaqt namozni vaqtida o‘qi',s:'Buxoriy, Muslim'},{id:'zk',t:'Ertalab va kechqurun zikr: salovat, istig‘for, tasbeh',s:''}];
const NSQ=[
['Nafsini poklagan kishi najot topdi, uni (gunohga) ko‘mgan esa ziyon ko‘rdi.','Qur‘on, 91:9–10'],['Kim Rabbining huzurida turishdan qo‘rqib, nafsini havoyi-havasdan tiysa, jannat uning makonidir.','Qur‘on, 79:40–41'],['Albatta, qiyinchilik bilan birga yengillik bor.','Qur‘on, 94:5–6'],['Bilib qo‘yingki, qalblar faqat Allohni zikr qilish bilan xotirjam bo‘ladi.','Qur‘on, 13:28'],['Alloh hech bir jonga qodir bo‘lganidan ortiq yuk yuklamaydi.','Qur‘on, 2:286'],['Inson uchun faqat o‘zi intilgan narsa bor.','Qur‘on, 53:39'],['Kim Allohga tavakkul qilsa, U unga kifoya qiladi.','Qur‘on, 65:3'],['Sabr qiluvchilarga ajrlari hisobsiz to‘liq beriladi.','Qur‘on, 39:10'],['Alloh bir qavmning holini, ular o‘zlarini o‘zgartirmaguncha o‘zgartirmaydi.','Qur‘on, 13:11'],['Biz yo‘limizda kurashganlarni, albatta, yo‘llarimizga hidoyat qilamiz.','Qur‘on, 29:69'],
['Amallar niyatlarga bog‘liqdir.','Hadis: Buxoriy, Muslim'],['Allohga eng sevimli amal: oz bo‘lsa ham davomli bo‘lgani.','Hadis: Buxoriy, Muslim'],['Kuchli kishi kurashda yengadigan emas, g‘azab paytida o‘zini tuta oladigan kishidir.','Hadis: Buxoriy, Muslim'],['Ikki ne’mat borki, ko‘p odam ularda aldanadi: sog‘liq va bo‘sh vaqt.','Hadis: Buxoriy'],['Kim Allohga va oxirat kuniga iymon keltirsa, yaxshi gapirsin yoki jim tursin.','Hadis: Buxoriy, Muslim'],['Mujohid — Alloh itoatida nafsi bilan kurashgan kishidir.','Hadis: Tirmiziy'],['Kuchli mo‘min zaif mo‘mindan yaxshi va Allohga sevimliroqdir. Foydali narsaga intil, Allohdan yordam so‘ra va bo‘shashma.','Hadis: Muslim'],['Dunyoda g‘arib yoki yo‘lovchi kabi bo‘l.','Hadis: Buxoriy'],
['Nafs chopqir ot kabi: jilovlanmasa, egasini chuqurga olib boradi.','Hikmat'],['Kichik g‘alabalar — katta nafs g‘alabasining g‘ishtlari.','Hikmat'],['Bugun nafsingga “yo‘q” degan har bir daqiqa — ertangi erkinligingning poydevori.','Hikmat'],['Intizom — o‘zingga bergan va’dangni bajarishdir.','Hikmat'],['Boshlashning eng qiyin joyi birinchi 2 daqiqa: taymerni yoq.','Hikmat'],['Dangasalikka qarshi qoida: 5 daqiqa boshla, ketaversa davom et.','Hikmat'],['Telefon — eng arzon vaqt o‘g‘risi.','Hikmat'],['Muvaffaqiyat — har kuni takrorlanadigan kichik odatlar yig‘indisi.','Hikmat'],['O‘zini yengish — eng og‘ir, lekin eng shirin g‘alaba.','Hikmat'],['Muhosaba qilinmagan kun — xaritasiz safar.','Hikmat'],['Bugungi qiyinchiliging — ertangi kuching.','Hikmat']];
const NSM=[
{k:['telefon','instagram','tarmoq','video','skrol'],t:'Bugun 1 soat telefonni boshqa xonaga qo‘y: shu vaqtni o‘qish yoki zikrga ishlat.'},
{k:['uyqu','yot','kech','tur','uyg‘on'],t:'Bugun 30 daqiqa erta yot: 22:00 da telefonni zaryadga qo‘yib, uzoqroqqa qo‘y.'},
{k:['dangasa','keyin','kechik','boshlay','erinch'],t:'5 daqiqa qoidasi: eng yoqmagan ishni faqat 5 daqiqaga boshla. Ketaversa, davom et.'},
{k:['g‘azab','jahl','asab','baqir'],t:'G‘azab kelsa: jim tur, o‘tirib ol, sekin 10 gacha sana, “a’uzu billahi minash-shaytonir-rojim” ayt.'},
{k:['ovqat','shirin','yeb','qand'],t:'Bugun bitta ortiqcha shirinlikdan o‘zingni tiy.'},
{k:['gap','g‘iybat','tortish','befoyda'],t:'Bugun g‘iybat va befoyda gapdan tiyil: yaxshi gapir yoki jim tur.'},
{k:['sadaqa','pul'],t:'Bugun yashirin kichik sadaqa qil: 1000 so‘m bo‘lsa ham.'},
{k:['ota','ona','oila'],t:'Ota-onang bilan 5 daqiqa suhbatlash yoki qo‘ng‘iroq qil.'},
{k:['zikr','namoz'],t:'Bugun 100 marta “Subhanallohi va bihamdihi” yoki istig‘for ayt.'},
{k:['tartib','reja'],t:'Ertalab 3 asosiy ishni yoz va birinchisini tugatmay telefonni ochma.'},
{k:['qiyin','mashaqqat'],t:'Eng qiyin vazifani kunning birinchi ishi qil.'},
{k:['kitob','o‘qish'],t:'Bugun 10 bet foydali kitob o‘qi.'},
{k:['mashq','zal','yurish','charchoq'],t:'Bugun 15 daqiqa yur yoki jismoniy mashq qil.'},
{k:['shukr','nolish'],t:'Bugun 3 ta ne’matga shukr yoz.'},
{k:['kechir','xafa','alam'],t:'Birovni ichingda kechir va unga yaxshilik bilan duo qil.'},
{k:[],t:'Bugun 20 daqiqa ijtimoiy tarmoqsiz o‘tkaz.'}];
const NSHM=['Muharram','Safar','Rabiul avval','Rabiul oxir','Jumadul avval','Jumadul oxir','Rajab','Sha‘bon','Ramazon','Shavvol','Zulqa‘da','Zulhijja'];
let NSF=null;
function nsHijri(d){try{const p=(NSF||(NSF=new Intl.DateTimeFormat('en-u-ca-islamic-umalqura',{day:'numeric',month:'numeric',year:'numeric'}))).formatToParts(d||new Date()),g=t=>+((p.find(x=>x.type===t)||{}).value);const o={d:g('day'),m:g('month'),y:g('year')};return o.y>1300&&o.y<1600&&o.m>=1&&o.m<=12&&o.d>=1?o:null}catch(e){return null}}
function nsSpecial(h){if(!h)return[];const L=[],{d,m}=h;if(m===9)L.push('Ramazon oyi: ro‘za, Qur‘on va ko‘proq ibodat oyi');if(m===10&&d===1)L.push('Ramazon hayiti: bu kuni ro‘za tutilmaydi');if(m===10&&d>=2&&d<=7)L.push('Shavvol: olti kunlik nafl ro‘za fursati');if(m===1&&d===9)L.push('Tosuo (9-muharram): Ashuro bilan birga ro‘za tutish mumkin');if(m===1&&d===10)L.push('Ashuro kuni: ro‘za tutish sunnat');if(m===12&&d===9)L.push('Arafa kuni: haj qilmaganlar uchun ro‘za sunnat');if(m===12&&d===10)L.push('Qurbon hayiti: bu kuni ro‘za tutilmaydi');if(m===12&&d>=11&&d<=13)L.push('Tashriq kunlari (11–13-zulhijja): bu kunlari ro‘za tutilmaydi');if(d>=13&&d<=15&&m!==9&&!(m===12&&d===13))L.push('Oyning “oq kunlari” (13–15): ro‘za tutish tavsiya etiladi');return L}
const nsS=()=>{const a=S.ns=S.ns||{};a.d=a.d||{};return a};
const nsDay=k=>nsS().d[k]||{a:[],m:0,q:0};
function nsItems(k){const w=new Date((k||dk())+'T12:00').getDay(),D=NSD[w];return{D,sun:[...D.sun,...NSALL],tav:D.tav.map((t,i)=>({id:'t'+w+i,t,s:''}))}}
function nsTog(id){const D=nsS().d,k=dk();D[k]=D[k]||{a:[],m:0,q:0};const a=D[k].a,i=a.indexOf(id);if(i>=0)a.splice(i,1);else a.push(id);Object.keys(D).sort().slice(0,-60).forEach(x=>delete D[x]);save()}
function nsMash(){const D=nsS().d,k=dk();D[k]=D[k]||{a:[],m:0,q:0};D[k].m=D[k].m?0:1;save()}
function nsNextQ(){const D=nsS().d,k=dk();D[k]=D[k]||{a:[],m:0,q:0};D[k].q=(D[k].q||0)+1;save()}
function nsWeak(){const W={};for(let i=0;i<7;i++){const d=((S.ny||{}).d||{})[dAgo(i)];if(d&&d.e)(d.e.toLowerCase().match(/[a-zA-Z‘’']+/g)||[]).forEach(w=>{W[w]=1})}return Object.keys(W)}
function nsPickM(k){const wk=nsWeak(),hit=NSM.filter(m=>m.k.length&&m.k.some(x=>wk.some(w=>w.includes(x))));const pool=hit.length?hit:NSM.filter(m=>m.k.length===0||true);const n=[...(k||dk())].reduce((a,c)=>a*31+c.charCodeAt(0),7)>>>0;return{m:pool[n%pool.length],fromWeak:!!hit.length}}
function nsPickQ(k,off){const n=([...(k||dk())].reduce((a,c)=>a*31+c.charCodeAt(0),11)>>>0)+(off||0);return NSQ[n%NSQ.length]}
function nsStreak(){let n=0;for(let i=0;i<60;i++){const d=nsS().d[dAgo(i)];if(d&&(d.a||[]).length>=3)n++;else if(i>0)break}return n}
function nsBrief(){const w=new Date().getDay(),D=NSD[w],h=nsHijri(),sp=nsSpecial(h);return 'Bugun '+D.n.toLowerCase()+'. '+D.b+'.'+(sp.length?' '+sp[0]+'.':'')}
function nsMini(){const k=dk(),{D,sun,tav}=nsItems(k),all=[...sun,...tav],dn=nsDay(k),n=all.filter(x=>dn.a.includes(x.id)).length;return `<button class="row nsm" onclick="MQV='k';go('m')" aria-label="Kunlik nasihatchi"><span style="font-size:26px">${D.e}</span><span class="t"><b>Bugun ${esc(D.n.toLowerCase())}</b> · ${n}/${all.length}<br><small class="mu">${esc(D.b)}</small></span><span class="tm">ochish</span></button>`}
function nsCard(){const k=dk(),{D,sun,tav}=nsItems(k),dn=nsDay(k),h=nsHijri(),sp=nsSpecial(h),all=[...sun,...tav],n=all.filter(x=>dn.a.includes(x.id)).length,pc=all.length?Math.round(n/all.length*100):0,P=nsPickM(k),Q=nsPickQ(k,dn.q),st=nsStreak();
  const row=x=>`<div class="row ${dn.a.includes(x.id)?'done':''}" style="cursor:default;align-items:flex-start"><span class="ck" onclick="nsTog('${x.id}')" role="checkbox" aria-checked="${dn.a.includes(x.id)}" tabindex="0">${dn.a.includes(x.id)?'✓':''}</span><span class="t" onclick="nsTog('${x.id}')">${esc(x.t)}${x.s?`<br><small class="mu">${esc(x.s)}</small>`:''}</span></div>`;
  return `<section class="goal nsc" aria-label="Kunlik nasihatchi"><div class="h"><b>🌿 Kunlik nasihatchi</b>${st>1?`<span class="chip">🔥 ${st} kun</span>`:''}</div>
   <div class="nsh"><span class="nse">${D.e}</span><div><b style="font:700 20px Fraunces,serif">${esc(D.n)}</b>${h?`<br><span class="mu" style="font-size:13px">${h.d} ${NSHM[h.m-1]} ${h.y}-yil (taxminiy)</span>`:''}<br><span style="font-size:14px">${esc(D.tag)}</span></div></div>
   ${sp.map(x=>`<p class="nsp">✨ ${esc(x)}</p>`).join('')}
   <div class="h" style="margin:10px 0 4px"><b style="font-size:14px">Bugungi amallar</b><span class="mu" style="font-size:12px">${n}/${all.length}</span></div><div class="bar" style="margin:0 0 6px"><i style="width:${pc}%"></i></div>
   ${sun.length?`<p class="mu" style="margin:8px 0 2px;font-size:12px">Sunnat va ta’kidlangan amallar</p>${sun.map(row).join('')}`:''}${tav.length?`<p class="mu" style="margin:10px 0 2px;font-size:12px">Bugungi tavsiyalar</p>${tav.map(row).join('')}`:''}
   <div class="nsn"><p style="margin:0 0 4px"><b>🔥 Bugungi nafs mashqi</b>${P.fromWeak?' <span class="chip on" style="font-size:11px">muhosabangdan</span>':''}</p><p style="margin:0 0 8px">${esc(P.m.t)}</p><button class="btn ${dn.m?'on':''}" style="width:100%" onclick="nsMash()">${dn.m?'✅ Bajarildi, barakalloh!':'Bajardim'}</button></div>
   <div class="nsq"><p style="margin:0">“${esc(Q[0])}”</p><p class="mu" style="margin:6px 0 0;font-size:12px">${esc(Q[1])}</p><button class="btn s" style="margin-top:8px" onclick="nsNextQ()">↻ Boshqa eslatma</button></div>
   <p class="mu" style="margin:10px 0 0;font-size:11.5px">Bu fatvo emas: aniq masalalarda mazhabingiz va ishonchli ustozga murojaat qil. Hijriy sana taxminiy (±1 kun).</p></section>`}
