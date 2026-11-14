import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Kun hikoyasi (AI) va kelajakka xat. Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('hikoya', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.__cf=0;window.__conf=0;window.confirm=m=>{window.__conf++;window.__cm=m;return window.__yes!==0};window.__req=[];window.__fail='';window.__ret=null;
      window.fnAI=async b=>{__req.push(b);if(window.__fail)throw new Error(window.__fail);if(window.__ret!==null)return {text:window.__ret};return {text:JSON.stringify({t:'Sokin va unumli kun',s:'Bugun odatlaringni bajarding va fokusda ishlading. Seriyang davom etyapti. Ertaga ertalab birinchi ishni 10 daqiqadan boshla.',e:'🌤'})}};
      window.__clip='';Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>{window.__clip=t}},configurable:true});
      S.hs=undefined;S.hab=[{id:'h1',t:'Kitob o‘qish'},{id:'h2',t:'Suv ichish'},{id:'h3',t:'Zal'}];S.hb={};S.hb[dk()]={h1:true,h2:true};S.fl=[{d:dk(),a:'IELTS',m:40},{d:dk(),a:'Hifz',m:25}];S.pm={};S.pm[dk()]=2;S.ie.gm={};S.ie.gm[dk()]=3;S.ie.rmd={};S.ie.rmd[dk()]=12;S.ie.xdr={};S.ie.tests=[{id:1,d:dk(),k:'R',b:{R:6}}];S.klx=[];S.rem=Object.assign(S.rem||{},{on:true});tab='m';MQV='k';render()}""")
    st = ev("hsStats()")
    chk('the day statistics sent to the AI are only numbers and a few habit names: date, XP, streak, habits done today (names, up to 6), focus minutes by area, pomodoros, IELTS tests, new words, game rounds, mistake reviews, sleep', set(st.keys()) == {'sana', 'xp', 'seriya', 'odat', 'odat_soni', 'fokus_daq', 'fokus', 'pomodoro', 'ielts_test', 'yangi_soz', 'oyin_raund', 'xato_takror', 'uyqu_soat'} and st['odat'] == ['Kitob o‘qish', 'Suv ichish'] and st['fokus_daq'] == 65 and st['fokus'] == {'IELTS': 40, 'Hifz': 25} and st['pomodoro'] == 2 and st['ielts_test'] == 1 and st['yangi_soz'] == 12 and st['oyin_raund'] == 3, st)
    ev("()=>{S.hab=Array.from({length:10},(_,i)=>({id:'x'+i,t:'N'.repeat(50)+i}));S.hb[dk()]=Object.fromEntries(S.hab.map(h=>[h.id,true]))}"); o = ev("hsStats().odat"); chk('at most 6 habit names are sent and each is cut to 30 characters', len(o) == 6 and all(len(x) <= 30 for x in o), o)
    ev("()=>{S.hab=[{id:'h1',t:'Kitob o‘qish'},{id:'h2',t:'Suv ichish'}];S.hb[dk()]={h1:true,h2:true};render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('the card "📖 Kun hikoyasi" explains what is sent and offers the button', '📖 Kun hikoyasi' in t and 'Faqat qisqa sonlar yuboriladi' in t and 'Bugungi kun hikoyasini yoz (1 AI)' in t)
    ev("window.__yes=0"); pg.click('#app >> text=Bugungi kun hikoyasini yoz'); pg.wait_for_timeout(150)
    chk('the first time the user is asked for permission (with what is sent); saying no sends nothing', ev("__conf") == 1 and 'odat nomlari' in ev("__cm") and len(ev("__req")) == 0 and not ev("S.hs&&S.hs.ok"))
    ev("window.__yes=1"); pg.click('#app >> text=Bugungi kun hikoyasini yoz'); pg.wait_for_timeout(300); rq = ev("__req")
    chk('after permission ONE request (iex daystory) with the statistics is sent; the story is saved for today and shown with its emoji, title and three sentences', len(rq) == 1 and rq[0]['kind'] == 'daystory' and rq[0]['stats']['xp'] is not None and ev("S.hs.ok") == 1 and ev("S.hs.d[dk()].t") == 'Sokin va unumli kun' and 'Sokin va unumli kun' in pg.inner_text('#app') and '🌤' in pg.inner_text('#app'))
    pg.click('#app >> text=Nusxalash'); pg.wait_for_timeout(80); chk('"📋 Nusxalash" copies emoji + title + story', ev("__clip").startswith('🌤 Sokin va unumli kun\nBugun odatlaringni'))
    ev("__conf=0"); pg.click('#app >> text=Qayta yozish'); pg.wait_for_timeout(300); chk('"↻ Qayta yozish" asks the AI again but never asks for permission twice', ev("__conf") == 0 and len(ev("__req")) == 2)
    ev("()=>{window.__ret='nope';S.hs.d={}}"); ev("hsGo()"); pg.wait_for_timeout(200); chk('an unusable AI answer shows a clear error and keeps the app working', 'AI hikoya yozmadi' in ev("S.hs.err") or 'tushunarsiz' in ev("S.hs.err")); ev("window.__ret=null")
    ev("()=>{window.__fail='Bugungi limit tugadi (40 ta so‘rov).'}"); ev("hsGo()"); pg.wait_for_timeout(200); chk('the AI failing (limit) shows the reason on the card', 'Bugungi limit tugadi' in pg.inner_text('#app')); ev("window.__fail=''")
    ev("window.aiOk=()=>false"); ev("__t=[]"); ev("hsGo()"); chk('not signed in: a clear message, no request', any('hisobga kirish' in x for x in ev("__t"))); ev("window.aiOk=()=>true")
    ev("()=>{S.hs.d={};for(let i=1;i<=45;i++){const d=new Date('2026-09-20T12:00');d.setDate(d.getDate()+i);S.hs.d[d.toLocaleDateString('sv')]={t:'Kun '+i,s:'Matn',e:'📖'}}hsGo();return 1}"); pg.wait_for_timeout(300)
    chk('only the last 40 stories are kept; older days appear under "Oldingi kunlar" (5 shown)', len(ev("Object.keys(S.hs.d)")) <= 40 and ev("[...document.querySelectorAll('#app details summary')].some(s=>s.textContent.startsWith('Oldingi kunlar (5)'))"))
    ev("()=>{S.hs.d={};S.hs.d[dk()]={t:'<b>x</b>',s:'<img src=x onerror=alert(1)>',e:'🔥'};render()}"); pg.wait_for_timeout(80); chk('story text is shown as plain text (no HTML from the AI is ever executed)', ev("document.querySelectorAll('.hst img,.hst b b').length") == 0)
    # ---------- xat ----------
    ev("()=>{S.klx=[];KLX={open:1,date:'',read:0};render()}"); pg.wait_for_timeout(100)
    chk('the "✉️ Kelajakka xat" card has the writing form (text, presets 1 oy / 3 oy / 6 oy / 1 yil, date, "🔒 Muhrlash")', all(x in pg.inner_text('#app') for x in ['✉️ Kelajakka xat', '1 oy', '3 oy', '6 oy', '1 yil', 'Muhrlash']) and ev("!!document.getElementById('klxt')") and ev("!!document.getElementById('klxd')"))
    pg.fill('#klxt', 'short'); ev("klxSeal()"); chk('a too short letter is refused', ev("S.klx.length") == 0 and any('20 belgi' in x for x in ev("__t")))
    TX = 'Salom, kelajakdagi men! Umid qilamanki IELTS 8 olgansan va maqsadlaring sari yurgansan.'; pg.fill('#klxt', TX); ev("klxSeal()"); chk('without a date it is refused', ev("S.klx.length") == 0 and any('sanasini tanla' in x for x in ev("__t")))
    ev("()=>{KLX.date=dk();render()}"); pg.fill('#klxt', TX); ev("klxSeal()"); chk('a date of today (or earlier) is refused: it must be tomorrow or later', ev("S.klx.length") == 0)
    ev("()=>{KLX.date='2032-01-01';render()}"); pg.fill('#klxt', TX); ev("klxSeal()"); chk('more than 5 years ahead is refused', ev("S.klx.length") == 0 and any('5 yil' in x for x in ev("__t")))
    pg.click('#app .chip >> text=3 oy'); pg.wait_for_timeout(60); d3 = ev("KLX.date"); chk('the "3 oy" preset sets the date three months ahead and lights up', d3 == '2027-02-05' and ev("document.getElementById('klxd').value") == '2027-02-05')
    pg.fill('#klxt', TX); pg.click('#app >> text=Muhrlash'); pg.wait_for_timeout(100); x = ev("S.klx[0]")
    chk('sealing stores the letter (created today, opens on the chosen date, unread) and the form is cleared', x['c'] == '2026-11-05' and x['o'] == '2027-02-05' and x['t'] == TX and x['r'] == 0 and ev("KLX.date") == '' and any('muhrlandi' in m for m in ev("__t")))
    t = pg.inner_text('#app'); chk('the list shows the letter as sealed with the opening date and the days left (92), with a lock', '✉️ Muhrlangan' in t and 'ochiladi: 2027-02-05 (92 kun)' in t and ev("document.querySelectorAll('[aria-label=Muhrlangan]').length") == 1)
    ev("klxOpen(%d)" % x['id']); chk('a sealed letter cannot be opened early', ev("S.klx[0].r") == 0 and ev("KLX.read") == 0)
    pg.clock.set_system_time('2027-02-05T08:00:00'); ev("render()"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('on the opening day the card says "💌 Ochishga tayyor!" and counts it in the chip', '💌 Ochishga tayyor!' in t and '💌 1 ochishga tayyor' in t)
    pg.click('#app .row button:text-is("Ochish")'); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('opening shows the letter text and when it was written, and marks it read', TX in t and '2026-11-05 kuni yozilgan' in t and ev("S.klx[0].r") == 1)
    ev("KLX.read=0;render()"); pg.wait_for_timeout(60); chk('afterwards it is listed as "Ochilgan" and can be read again', '📭 Ochilgan' in pg.inner_text('#app') and 'O‘qish' in pg.inner_text('#app'))
    # eslatma va toast
    ev("()=>{S.klx=[{id:1,c:'2026-11-01',o:'2027-02-08',t:'x'.repeat(30),r:0},{id:2,c:'2026-11-01',o:'2027-02-09',t:'y'.repeat(30),r:0},{id:3,c:'2026-11-01',o:'2027-03-30',t:'z'.repeat(30),r:0},{id:4,c:'2026-11-01',o:'2027-02-06',t:'w'.repeat(30),r:1},{id:5,c:'2026-11-01',o:'2027-02-08',t:'v'.repeat(30),r:0}]}")
    rows = ev("remRows().filter(r=>String(r.kind).startsWith('klx@')).map(r=>[r.kind,r.hhmm,r.days,r.title])")
    chk('reminder rows only for UNREAD letters opening within the next 7 days: one per date (two letters on Feb 8 give one row), at 09:00, on that weekday; far-future and already-read letters give none', sorted(r[0] for r in rows) == ['klx@2027-02-08', 'klx@2027-02-09'] and all(r[1] == '09:00' and len(r[2]) == 1 for r in rows) and rows[0][2] == [1] and '✉️' in rows[0][3], rows)
    ev("()=>{window.__klxForce=1;localStorage.removeItem('trk_klxt');S.klx=[{id:1,c:'2026-11-01',o:'2027-02-05',t:'x'.repeat(30),r:0}];__t=[];klxCheck()}"); chk('when an unread letter is ready the app announces it once a day', any('xating ochildi' in m for m in ev("__t")))
    ev("__t=[];klxCheck()"); chk('...and does not repeat the announcement on the same day', ev("__t.length") == 0)
    ev("()=>{localStorage.removeItem('trk_klxt');S.klx[0].r=1;__t=[];klxCheck()}"); chk('a letter already read does not trigger the announcement', ev("__t.length") == 0)
    ev("()=>{S.klx=Array.from({length:20},(_,i)=>({id:i+1,c:'2027-02-05',o:'2027-12-31',t:'a'.repeat(30),r:0}));KLX={open:1,date:'2027-12-31',read:0};render()}"); pg.wait_for_timeout(80); pg.fill('#klxt', TX); ev("klxSeal()"); chk('at most 20 letters are kept', ev("S.klx.length") == 20 and any('20 tadan' in m for m in ev("__t")))
    ev("()=>{S.klx=[{id:7,c:'2026-11-01',o:'2027-02-01',t:'<img src=x onerror=alert(1)>Matn',r:0}];KLX={open:0,date:'',read:7};render()}"); pg.wait_for_timeout(80); chk('letter text is shown as plain text (no HTML is executed)', ev("document.querySelectorAll('.klxr img').length") == 0 and 'Matn' in ev("document.querySelector('.klxr').textContent"))
    ev("()=>{window.__conf=0;window.__yes=1}"); ev("klxDel(7)"); chk('deleting a letter asks first and removes it', ev("__conf") == 1 and ev("S.klx.length") == 0)
    # ko'rinish
    ev("()=>{S.hs={ok:1,d:{[dk()]:{t:'Sarlavha',s:'Uch gapli uzun hikoya matni shu yerda turadi va satrdan oshib ketishi mumkin.',e:'🌤'}}};S.klx=[{id:1,c:'2027-02-01',o:'2027-02-05',t:'Matn '.repeat(40),r:0},{id:2,c:'2027-02-01',o:'2027-12-31',t:'Matn',r:0}];KLX={open:1,date:'',read:1}}")
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='m';MQV='k';render()}", [ui, th]); pg.wait_for_timeout(50)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the story and letter cards fit the phone screen in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
