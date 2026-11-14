import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# AI kun rejasi (klient): kontekst, taklif, qo'shish, xatolar. fnAI soxta javob bilan almashtiriladi. Soat qotirilgan: 2026-10-31 (shanba).
import sys, datetime, json
from playwright.sync_api import sync_playwright
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a');if(localStorage.getItem('trk_pl')===null)localStorage.setItem('trk_pl','0')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto(('file://' + ROOT + '/tracker/index.html')); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    ev = pg.evaluate
    ev("""()=>{S.ob=1;S.ts=1;S.top={};S.tasks={};S.un.tasks=[{id:1,t:'Misol',s:'Matematika',due:dAgo(-1),x:0}];S.un.exams=[{id:1,s:'Fizika',d:dAgo(-5)}];
      S.goals=[{t:'Hofiz bo‘lish',ms:[{t:'Juz Amma',x:1},{t:'5 pora',x:0}],dl:dAgo(-100),rw:'SIR-MUKOFOT'}];S.main=0;S.q.ppd=3;S.q.cur=1;S.q.m={1:20};S.q.ord=[1];S.q.lg=[{id:1,d:dAgo(2),i:1,a:3,b:6,t:'n'}];
      S.money=[{id:1,d:dk(),w:'p',k:'out',a:777777,c:'MAXFIY-XARAJAT'}];S.note={[dk()]:'MAXFIY-IZOH'};rwReset();window.aiOk=()=>true}""")
    c = ev("aiPlanCtx()"); s = json.dumps(c, ensure_ascii=False)
    chk('context has date, weekday, today\u2019s plan blocks', c['sana'] == '2026-10-31' and c['hafta_kuni'] == 'Shanba' and len(c['reja']) >= 3 and all(' ' in x for x in c['reja']), c['reja'][:2])
    chk('context has the deadlines (task due tomorrow, exam in 5 days)', any('Misol' in x and '1 kun' in x for x in c['muddatlar']) and any('Fizika' in x for x in c['muddatlar']), c['muddatlar'])
    chk('context has the main goal with progress, next step and days left', c['maqsad']['nom'] == 'Hofiz bo‘lish' and c['maqsad']['foiz'] == 50 and c['maqsad']['keyingi_bosqich'] == '5 pora' and c['maqsad']['kun_qoldi'] == 100, c['maqsad'])
    chk('context has the hifz plan (3 pages/day, sabqi 3 pages, manzil from the old part)', c['hifz']['kunlik_bet'] == 3 and c['hifz']['sabqi_bet'] == 3 and c['hifz']['manzil_bet'] >= 1, c['hifz'])
    chk('context carries today\u2019s goal, streak and light-day flag', c['kun_maqsadi_xp'] == 100 and c['seriya'] == 0 and c['yengil_kun'] is False and 'kecha_xp' in c)
    chk('PRIVACY: money entries, notes and the reward text are NOT sent to the AI', 'MAXFIY' not in s and '777777' not in s and 'SIR-MUKOFOT' not in s, s[:200])
    chk('context is compact (< 3000 characters)', len(s) < 3000, len(s))
    # ---------- success path ----------
    ev("""()=>{window.__calls=[];window.fnAI=async(body)=>{window.__calls.push(body);return {text:'```json\\n{"top3":[{"t":"Misol topshirig‘ini tugat"},{"t":"   3 bet sabaq yodla   "},{"t":"Sabqini takrorla"},{"t":"To‘rtinchi ish"}],"tip":"Bugun yengil boshla, barakalla"}\\n```'}};tab='h';BV='j';VD=null;render()}""")
    pg.wait_for_timeout(150)
    chk('Bugun: with fewer than 3 items the "AI bilan rejala" button is shown in the Top-3 card', 'AI bilan rejala' in pg.inner_text('#app'))
    pg.click('#app >> text=AI bilan rejala'); pg.wait_for_timeout(300)
    chk('it calls the plan action once, with the context as a JSON string', ev("__calls.length") == 1 and ev("__calls[0].action") == 'plan' and json.loads(ev("__calls[0].ctx"))['sana'] == '2026-10-31')
    pl = ev("PLN"); chk('the answer is parsed (fenced JSON ok), trimmed and limited to 3 items', pl['top3'] == ['Misol topshirig‘ini tugat', '3 bet sabaq yodla', 'Sabqini takrorla'] and 'barakalla' in pl['tip'], pl)
    t = pg.inner_text('#app'); chk('the suggestion card shows the items, the tip and both buttons', 'AI taklifi' in t and 'Sabqini takrorla' in t and 'Top-3 ga qo‘sh' in t and 'Rad etish' in t)
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());document.querySelector('.aipl').scrollIntoView({block:'center'})"); pg.wait_for_timeout(120); pg.screenshot(path='/tmp/ai_plan.png')
    pg.click('#app >> text=Top-3 ga qo‘sh'); pg.wait_for_timeout(250)
    chk('accepting adds them to today\u2019s Top-3 (3 items, not done)', ev("S.top[dk()].map(x=>x.t)") == ['Misol topshirig‘ini tugat', '3 bet sabaq yodla', 'Sabqini takrorla'] and ev("S.top[dk()].every(x=>x.x===0)") and ev("PLN") is None)
    chk('with a full Top-3 the AI button is gone', 'AI bilan rejala' not in pg.inner_text('#app'))
    # existing items -> only free slots are filled
    ev("""()=>{S.top[dk()]=[{t:'Mening ishim',x:0}];PLN=null;render()}"""); pg.wait_for_timeout(100)
    pg.click('#app >> text=AI bilan rejala'); pg.wait_for_timeout(300); chk('the suggestion button says it fills the free places', 'Bo‘sh joyga qo‘sh' in pg.inner_text('#app'))
    pg.click('#app >> text=Bo‘sh joyga qo‘sh'); pg.wait_for_timeout(200)
    chk('with 1 item already there only 2 are added (max 3), existing one is kept', ev("S.top[dk()].length") == 3 and ev("S.top[dk()][0].t") == 'Mening ishim')
    ev("""()=>{S.top[dk()]=[];PLN={top3:['A','B'],tip:''};render()}"""); pg.wait_for_timeout(100)
    pg.click('#app >> text=Rad etish'); pg.wait_for_timeout(100); chk('"Rad etish" discards the suggestion and adds nothing', ev("PLN") is None and ev("S.top[dk()].length") == 0)
    # ---------- failure paths ----------
    ev("""()=>{window.fnAI=async()=>{throw new Error('Bugungi limit tugadi (40 ta so‘rov). Ertaga davom etamiz.')};PLN=null;render()}"""); pg.wait_for_timeout(100)
    pg.click('#app >> text=AI bilan rejala'); pg.wait_for_timeout(300)
    chk('server error is shown in plain words with a retry button, nothing is added', 'Bugungi limit tugadi' in pg.inner_text('#app') and 'Qayta urinish' in pg.inner_text('#app') and ev("S.top[dk()].length") == 0)
    ev("""()=>{window.fnAI=async()=>({text:'bu JSON emas'});PLN=null;render()}"""); pg.wait_for_timeout(100)
    pg.click('#app >> text=AI bilan rejala'); pg.wait_for_timeout(300); chk('unparseable AI answer -> friendly error', 'tushunarli reja bermadi' in pg.inner_text('#app'))
    ev("""()=>{window.fnAI=async()=>({text:'{"top3":[],"tip":"x"}'});PLN=null;render()}"""); pg.wait_for_timeout(100)
    pg.click('#app >> text=AI bilan rejala'); pg.wait_for_timeout(300); chk('empty suggestion list -> friendly error', 'tushunarli reja bermadi' in pg.inner_text('#app'))
    ev("""()=>{let n=0;window.fnAI=async()=>{n++;window.__n=n;await new Promise(r=>setTimeout(r,200));return {text:'{"top3":[{"t":"X"}],"tip":""}'}};PLN=null;render();aiPlan();aiPlan();aiPlan()}"""); pg.wait_for_timeout(500)
    chk('pressing the button repeatedly sends only one request', ev("window.__n") == 1)
    # ---------- visibility ----------
    ev("""()=>{PLN=null;VD=dAgo(1);render()}"""); pg.wait_for_timeout(100); chk('not offered when looking at another day', 'AI bilan rejala' not in pg.inner_text('#app'))
    ev("""()=>{VD=null;window.aiOk=()=>false;render()}"""); pg.wait_for_timeout(100); chk('not offered to signed-out users (the server needs a login)', 'AI bilan rejala' not in pg.inner_text('#app'))
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
