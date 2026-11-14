import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# AI holati (limit tugadi / bugungi sarf) va maqola sarlavhalari (##). Soat: 2026-11-05 10:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
TXT = "## Introduction\n\nWhat are your favourite foods? Do you like pizza?\n\n## How Do We Taste Different Flavours?\n\nThese bumps contain receptors.\n\n### Sub heading\n\nUse #hashtag here and ## inside a line.\n\n#notaheading\n\nPlain paragraph."
with Run('aiholat', when=(2026, 11, 5, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(T)=>{window.__t=[];window.toast=m=>window.__t.push(m);window.aiOk=()=>true;window.aiSession=async()=>({access_token:'t'});window.__resp={status:200,body:{text:'{"a":1}'}};window.__calls=[];
      window.fetch=async(u,o)=>{const b=JSON.parse(o.body);__calls.push(b.action);if(b.action==='limit')return new Response(JSON.stringify({owner:false,limit:40,used:12}),{status:200});return new Response(JSON.stringify(__resp.body),{status:__resp.status})};
      localStorage.removeItem('trk_aiq');ALM=null;for(let i=localStorage.length-1;i>=0;i--){const k=localStorage.key(i);if(k&&(k.startsWith('trk_aiu_')||k.startsWith('trk_ailim_')))localStorage.removeItem(k)}
      S.ie.mat=[{id:1,t:'Enhancing the Taste of Our Food',k:'a',x:T,c:[],au:0,d:dk(),an:null}];S.ie.words=[];tab='e';EV='i';IVW='a';render()}""", TXT)
    ev("ieMatOpen(1)"); pg.wait_for_timeout(300)
    # ---- sarlavhalar ----
    chk('"## Introduction" lines become real headings (no # signs): three headings (## ## ###) in this text', ev("document.querySelectorAll('#iem .iehd').length") == 3 and ev("[...document.querySelectorAll('#iem .iehd')].map(e=>e.textContent)") == ['Introduction', 'How Do We Taste Different Flavours?', 'Sub heading'])
    chk('headings are bold and larger than body text, and are still paragraphs that the read-aloud and the word highlighting work on (class iep)', ev("parseInt(getComputedStyle(document.querySelector('#iem .iehd')).fontWeight)") >= 600 and ev("document.querySelector('#iem .iehd').classList.contains('iep')") and ev("ieRdEls().some(e=>e.textContent==='Introduction')"))
    t = ev("[...document.querySelectorAll('#iem .iep:not(.iehd)')].map(e=>e.textContent)")
    chk('normal paragraphs are untouched: a hashtag, a "##" inside a line, a "#notaheading" without a space and plain text keep their characters', 'Use #hashtag here and ## inside a line.' in t and '#notaheading' in t and 'Plain paragraph.' in t and not any(x.startswith('## ') for x in t))
    chk('unit cases: up to 4 hashes + a space make a heading; 5+ hashes, no space, or an empty heading do not', all([ev("ieHdP('# A',{})").count('iehd') == 1, ev("ieHdP('#### D',{})").count('iehd') == 1, ev("ieHdP('##### E',{})").count('iehd') == 0, ev("ieHdP('##X',{})").count('iehd') == 0, ev("ieHdP('## ',{})").count('iehd') == 0, ev("ieHdP('  ## Indented',{})").count('iehd') == 1]))
    # ---- sarf ko'rsatkichi ----
    ev("()=>{ALM={o:false,l:40,u:10,d:dk(),t:Date.now()};ieMatOpen(1)}"); pg.wait_for_timeout(200)
    chk('the material screen shows today\u2019s AI use under the analyse button: green at 10/40', '🟢 AI: 10/40 bugun' in pg.inner_text('#iem') and ev("document.querySelector('#iem .aistat').classList.contains('aiok')"))
    for u, ic, cl in ((25, '🟡', 'aiwarn'), (37, '🔴', 'aibad')):
        ev("(u)=>{ALM={o:false,l:40,u:u,d:dk(),t:Date.now()};aiStatPaint()}", u)
        chk(f'{u}/40 is shown {ic}', f'{ic} AI: {u}/40 bugun' in pg.inner_text('#iem') and ev("document.querySelector('#iem .aistat').classList.contains('%s')" % cl))
    ev("()=>{ALM={o:true,l:40,u:0,d:dk(),t:Date.now()};aiStatPaint()}"); chk('the owner account shows "cheksiz"', 'AI: cheksiz (egasi)' in pg.inner_text('#iem'))
    ev("()=>{ALM=null;localStorage.removeItem('trk_ailim_'+(UID||''));__calls.length=0;aiLimRefresh(true)}"); pg.wait_for_timeout(300)
    chk('the numbers are fetched from the server when unknown and the open screen updates by itself (no re-render needed): 12/40', '🟢 AI: 12/40 bugun' in pg.inner_text('#iem') and 'limit' in ev("__calls"))
    # ---- limit tugadi ----
    ev("()=>{ALM={o:false,l:40,u:10,d:dk(),t:Date.now()};__resp={status:429,body:{error:'AI hozir band (bepul daqiqalik limit). 20 soniyadan keyin qayta urinib ko‘ring.'}}}")
    ev("()=>{fnPost({action:'iex'}).catch(()=>{});return 1}"); pg.wait_for_timeout(200)
    chk('a short per-minute limit message does NOT mark the day as exhausted', ev("localStorage.getItem('trk_aiq')") is None and '🟢' in pg.inner_text('#iem'))
    ev("()=>{__resp={status:429,body:{error:'Bugungi bepul AI limiti tugadi. Limit har kuni taxminan 12:00-13:00 (Toshkent vaqti) da yangilanadi.'}}}")
    ev("()=>{fnPost({action:'iex'}).catch(()=>{});return 1}"); pg.wait_for_timeout(200); t = pg.inner_text('#iem')
    chk('when the server says the free daily limit is used up, the open screen immediately shows the red notice with the reset time (12:00–13:00 Toshkent) instead of the counter', '🔴 Bepul AI limiti tugagan' in t and '12:00–13:00 (Toshkent vaqti)' in t and '🟢' not in t and ev("aiQuotaGet().k") == 'g')
    ev("()=>{window.__t=[];tab='h';BV='t';render()}"); pg.wait_for_timeout(150); chk('the same notice appears in the Tahlil “Aqlli yordamchi” card', '🔴 Bepul AI limiti tugagan' in pg.inner_text('#app'))
    ev("()=>{tab='m';MQV='k';render()}"); pg.wait_for_timeout(150); chk('...and in the “Kun hikoyasi” card on the Goals screen', '🔴 Bepul AI limiti tugagan' in pg.inner_text('#app'))
    q = ev("aiQuotaGet().t"); at = ev("(t=>aiQuotaReset(t))(%d)" % q)
    chk('the reset moment is the next 08:05 UTC after the failure (Google resets at Pacific midnight = 07:00/08:00 UTC)', ev("new Date(%d).getUTCHours()" % at) == 8 and ev("new Date(%d).getUTCMinutes()" % at) == 5 and at > q and at - q <= 86400000)
    pg.clock.set_system_time(ev("new Date(%d-60000).toISOString()" % at)); chk('one minute before the reset the notice is still shown', ev("!!aiQuotaGet()"))
    pg.clock.set_system_time(ev("new Date(%d+60000).toISOString()" % at)); chk('one minute after the reset the notice disappears by itself', ev("aiQuotaGet()") is None and ev("localStorage.getItem('trk_aiq')") is None)
    pg.clock.set_system_time('2026-11-05T10:00:00')
    ev("()=>{__resp={status:429,body:{error:'Bugungi limit tugadi (40 ta so‘rov). Ertaga davom etamiz.'}};fnPost({action:'iex'}).catch(()=>{});return 1}"); pg.wait_for_timeout(200)
    ev("()=>{ieMatOpen(1)}"); pg.wait_for_timeout(200)
    chk('the app\u2019s own daily limit (40) is a different message: “Bugungi AI limiting tugadi (40 ta so‘rov). Ertaga yangilanadi.”', ev("aiQuotaGet().k") == 'a' and 'Bugungi AI limiting tugadi (40 ta so‘rov)' in pg.inner_text('#iem'))
    pg.clock.set_system_time('2026-11-06T10:00:00'); chk('the app-limit notice is for that day only (gone the next day)', ev("aiQuotaGet()") is None); pg.clock.set_system_time('2026-11-05T10:00:00')
    ev("()=>{localStorage.setItem('trk_aiq',JSON.stringify({k:'g',t:Date.now()}));aiStatPaint();__resp={status:200,body:{text:'{\"a\":1}'}}}"); ev("()=>{fnAI({action:'iex',kind:'x'}).catch(()=>{});return 1}"); pg.wait_for_timeout(300)
    chk('after ANY successful AI answer the notice is cleared at once (the limit evidently works again)', ev("localStorage.getItem('trk_aiq')") is None and '🔴 Bepul AI limiti tugagan' not in pg.inner_text('#iem'))
    bad = []
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];localStorage.setItem('trk_aiq',JSON.stringify({k:'g',t:Date.now()}));ieMatOpen(1)}", [ui, th]); pg.wait_for_timeout(150)
            if not ev("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(ui + th)
    chk('the notice and the headings fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{localStorage.removeItem('trk_aiq');uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
