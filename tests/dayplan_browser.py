import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# AI kun rejasi (ertalabdan kechgacha): niyat, kontekst, AI javobini tozalash, suhbat oqimi, saqlash, Bugun kartasi, ochko, eslatma.
# Soat qotirilgan: 2026-10-31 (shanba) 10:00. Ertaga = yakshanba 2026-11-01.
import sys, datetime, json
from playwright.sync_api import sync_playwright
ok = bad = 0
def chk(name, cond, extra=''):
    global ok, bad
    if cond: ok += 1; print('PASS', name)
    else: bad += 1; print('FAIL', name, extra)
SETUP = """()=>{S.ob=1;S.ts=1;S.ap={};S.done={};S.top={};S.tasks={};S.hb={};S.rules={};S.nm.d={};S.gym.log=[];S.close={};S.water={};S.money=[];S.note={[dk()]:'MAXFIY-IZOH'};S.goals=[];S.hab=[];
  S.bl=[{id:'uyg',t:'Uyg‘onish',s:300,e:330,d:[0,1,2,3,4,5,6]},{id:'qur',t:'Qur‘on',s:360,e:540,d:[0,1,2,3,4,5,6]},{id:'dok',t:'Dokon',s:540,e:1020,d:[1,2,3,4,5]},{id:'iel',t:'IELTS',s:1275,e:1335,d:[0,1,2,3,4,5,6]},{id:'uyqu1',t:'Uxlash',s:1375,e:1740,d:[0,1,2,3,4,5,6]}];
  S.rem={...S.rem,on:true,blk:true,off:5};rwReset();window.aiOk=()=>true}"""
AI_JSON = json.dumps({"blocks": [{"id": "qur", "n": "3 bet sabaq, sabqi 5 bet, manzil 2 bet"}, {"id": "iel", "n": "Listening Part 2 va 20 so‘z"}, {"id": "yoq", "n": "yo‘q blok"}, {"id": "uyg", "n": "x" * 300}],
  "extra": [{"s": "09:15", "e": "10:00", "t": "Misol topshirig‘ini yoz"}, {"s": "8:00", "e": "9:30", "t": "Qur‘on bilan kesishadi"}, {"s": "10:00", "e": "09:00", "t": "Teskari vaqt"}, {"s": "bad", "e": "11:00", "t": "Noto‘g‘ri vaqt"},
            {"s": "03:00", "e": "04:00", "t": "Turishdan oldin"}, {"s": "23:00", "e": "23:30", "t": "Uxlashdan keyin"}, {"s": "12:00", "e": "13:30", "t": "Zalga bor"}, {"s": "13:00", "e": "14:00", "t": "Ovqat va dam " + "y" * 80}, {"s": "15:00", "e": "15:10", "t": "Juda qisqa"},
            {"s": "16:00", "e": "17:00", "t": ""}], "tip": "Ertalab yengil boshla, barakalla"}, ensure_ascii=False)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a');if(localStorage.getItem('trk_pl')===null)localStorage.setItem('trk_pl','0');localStorage.setItem('trk_fqd','0')}catch(e){}"); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.clock.install(time=datetime.datetime(2026, 10, 31, 10, 0, 0))
    pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto(('file://' + ROOT + '/tracker/index.html')); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    ev = pg.evaluate; ev(SETUP)
    # ---------- 1. intent ----------
    pos = ["rejamni tuzib ber", "Qara men ilovani zo‘r qilib yasadim, bugun uyga borib uxlayman va ertalabdan to kechgacha bo‘lgan rejamni tuzib ber", "Ertangi kunni rejalashtir", "kunimni rejala", "bugungi kunni qayta rejalashtir", "ertaga uchun jadval tuz"]
    neg = ["IELTS uchun reja tuz", "Haftamni tahlil qil", "Bugun nimaga e‘tibor qarataman?", "Qur‘on yodlash va takror bo‘yicha maslahat ber", "Meni ruhlantir", "Rejamni tushuntirib ber"]
    chk('plan intent recognised in %d real phrasings (including the user\u2019s own message)' % len(pos), all(ev("aiPlanIntent(%s)" % json.dumps(t)) for t in pos), [t for t in pos if not ev("aiPlanIntent(%s)" % json.dumps(t))])
    chk('and NOT in ordinary questions (including the "IELTS uchun reja tuz" quick prompt)', not any(ev("aiPlanIntent(%s)" % json.dumps(t)) for t in neg), [t for t in neg if ev("aiPlanIntent(%s)" % json.dumps(t))])
    d1 = lambda t: ev("dpDate(%s)" % json.dumps(t))
    chk('date: "ertalabdan..." -> tomorrow, "bugun..." -> today, plain request at 10:00 -> today', d1('ertalabdan kechgacha rejamni tuzib ber') == '2026-11-01' and d1('bugun rejamni tuzib ber') == '2026-10-31' and d1('rejamni tuzib ber') == '2026-10-31' and d1('Ertangi kunni rejalashtir') == '2026-11-01')
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 21, 0, 0))
    chk('date: plain request after 20:00 -> tomorrow, but "bugun" stays today', d1('rejamni tuzib ber') == '2026-11-01' and d1('bugungi kunni qayta rejalashtir') == '2026-10-31')
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 10, 0, 0))
    # ---------- 2. context ----------
    c = ev("dpCtx('2026-11-01','ertalab dam olaman',false)"); s = json.dumps(c, ensure_ascii=False)
    chk('context = tomorrow (Sunday), the wish, wake/sleep times', c['sana'] == '2026-11-01' and c['hafta_kuni'] == 'Yakshanba' and c['istak'] == 'ertalab dam olaman' and c['turish'] == '05:00' and c['uxlash'] == '22:55' and c['bugun'] is False, c)
    chk('fixed blocks of THAT weekday only (Sunday: no Dokon), without sleep, with ids and HH:MM times', [x['id'] for x in c['qat_bloklar']] == ['uyg', 'qur', 'iel'] and c['qat_bloklar'][1] == {'id': 'qur', 's': '06:00', 'e': '09:00', 't': 'Qur‘on'}, c['qat_bloklar'])
    chk('weekday: Monday has the shop block too', 'dok' in [x['id'] for x in ev("dpCtx('2026-11-02','',false).qat_bloklar")])
    chk('context carries hifz amounts and the "different" flag; it is compact', c['hifz']['kunlik_bet'] >= 0 and ev("dpCtx('2026-11-01','',true).boshqacha") is True and len(s) < 3500, len(s))
    chk('PRIVACY: private notes and money are not sent', 'MAXFIY' not in s and 'pul' not in s.lower().replace('muddat', ''), s[:200])
    # ---------- 3. cleaning the AI answer ----------
    P = ev("dpBuild('2026-11-01',%s)" % AI_JSON); it = P['it']; by = {x['id']: x for x in it}
    chk('fixed blocks are all there with their ORIGINAL times and names, flagged fx', [(x['id'], x['s'], x['e'], x['t']) for x in it if x.get('fx')] == [('uyg', 300, 330, 'Uyg‘onish'), ('qur', 360, 540, 'Qur‘on'), ('iel', 1275, 1335, 'IELTS')])
    chk('AI notes are attached to blocks by id; unknown ids ignored; very long notes cut to 110', by['qur']['n'] == '3 bet sabaq, sabqi 5 bet, manzil 2 bet' and by['iel']['n'].startswith('Listening') and len(by['uyg']['n']) == 110 and 'yoq' not in by)
    ex = [x for x in it if not x.get('fx')]
    chk('extras: overlapping a block, reversed, malformed, before wake-up, after bedtime, <15 min and untitled ones are dropped', [x['t'][:12] for x in ex] == ['Misol topshi', 'Zalga bor', 'Ovqat va dam'], [x['t'] for x in ex])
    chk('two overlapping extras: the later one is trimmed to start when the first ends (13:30-14:00)', [(x['s'], x['e']) for x in ex] == [(555, 600), (720, 810), (810, 840)], [(x['s'], x['e']) for x in ex])
    chk('titles are cut to 60 characters and extras start undone', all(len(x['t']) <= 60 for x in ex) and all(x['x'] == 0 for x in ex))
    chk('the final timeline is sorted and has no overlaps at all', all(it[i]['e'] <= it[i + 1]['s'] for i in range(len(it) - 1)) and len({x['id'] for x in it}) == len(it), [(x['id'], x['s'], x['e']) for x in it])
    chk('garbage input (null, wrong types) gives just the fixed blocks, no crash', len(ev("dpBuild('2026-11-01',null).it")) == 3 and len(ev("dpBuild('2026-11-01',{blocks:5,extra:'x'}).it")) == 3)
    many = json.dumps({"extra": [{"s": "%02d:00" % (10 + i), "e": "%02d:30" % (10 + i), "t": "Ish %d" % i} for i in range(9)]})
    chk('at most 6 extras are kept', len([x for x in ev("dpBuild('2026-11-01',%s).it" % many) if not x.get('fx')]) == 6)
    # ---------- 4. chat flow ----------
    ev("""()=>{window.__f=[];window.__fetch=0;window.fnPost=async()=>({owner:false,limit:40,used:0});window.fnAI=async(body)=>{window.__f.push(body);return {text:'```json\\n'+window.__ans+'\\n```'}};window.fetch=async()=>{window.__fetch++;return new Response('Salom',{status:200})};window.__ans=%s;aiS().chat=[];aiBuild();aiRender();window.aiSession=async()=>({access_token:'t'})}""" % json.dumps(AI_JSON))
    ev("aiSend('Qara men ilovani yasadim, bugun uyga borib uxlayman va ertalabdan to kechgacha bo‘lgan rejamni tuzib ber')"); pg.wait_for_timeout(500)
    chk('the request goes to the dayplan action (not the ordinary chat), once, with tomorrow\u2019s date and the user\u2019s own words', ev("__f.length") == 1 and ev("__f[0].action") == 'dayplan' and ev("__fetch") == 0 and json.loads(ev("__f[0].ctx"))['sana'] == '2026-11-01' and 'uyga borib uxlayman' in json.loads(ev("__f[0].ctx"))['istak'])
    txt = pg.inner_text('#aic')
    chk('the chat shows the timeline card: header, block times with AI notes, extras and the tip', 'Ertaga uchun reja' in txt and '06:00–09:00' in txt and '3 bet sabaq' in txt and 'Zalga bor' in txt and 'Ertalab yengil boshla' in txt and 'Rejaga qo‘sh' in txt and 'Boshqacha tuz' in txt, txt[-500:])
    pg.evaluate("document.getElementById('aic').scrollTop=0"); pg.wait_for_timeout(100); pg.screenshot(path='/tmp/dp_chat.png')
    chk('the history sent to the model for ordinary chat will not contain plan cards', ev("aiS().chat.filter(m=>m.r==='user'||m.r==='model').length") == 1)
    pg.click('#aic >> text=Boshqacha tuz'); pg.wait_for_timeout(500)
    chk('"Boshqacha tuz" asks again with the flag, replaces the card, keeps a single user message', ev("__f.length") == 2 and json.loads(ev("__f[1].ctx"))['boshqacha'] is True and ev("aiS().chat.map(m=>m.r)") == ['user', 'plan'])
    pg.click('#aic >> text=Rejaga qo‘sh'); pg.wait_for_timeout(300)
    chk('"Rejaga qo\u2018sh" saves the plan under tomorrow\u2019s date (3 blocks + 3 extras) and the card confirms', ev("(S.ap['2026-11-01']||{it:[]}).it.length") == 6 and 'Rejaga qo‘shildi' in pg.inner_text('#aic') and ev("S.ap['2026-11-01'].tip") != '')
    chk('saved items are independent copies', ev("(()=>{const m=aiS().chat[1];m.it[0].t='O‘ZGARDI';return S.ap['2026-11-01'].it[0].t!=='O‘ZGARDI'})()"))
    # ordinary question is NOT a plan
    ev("window.__fetch=0;aiSend('Haftamni tahlil qil')"); pg.wait_for_timeout(800)
    chk('an ordinary question still uses the normal chat stream (no dayplan call)', ev("__f.length") == 2 and ev("__fetch") >= 1)
    # failure + retry
    ev("""()=>{window.fnAI=async()=>{throw new Error('Bugungi limit tugadi (40 ta so‘rov).')};aiS().chat=[];aiRender();aiSend('rejamni tuzib ber')}"""); pg.wait_for_timeout(400)
    chk('a failing plan request shows the message with a retry button', 'Bugungi limit tugadi' in pg.inner_text('#aic') and 'Qayta yuborish' in pg.inner_text('#aic'))
    ev("""()=>{window.fnAI=async(b)=>{window.__f.push(b);return {text:window.__ans}}}"""); pg.click('#aic >> text=Qayta yuborish'); pg.wait_for_timeout(500)
    chk('retry works: one user message and the plan card, no error left', ev("aiS().chat.map(m=>m.r)") == ['user', 'plan'])
    ev("aiS().chat=[];aiRender();window.fnAI=async()=>({text:'bu JSON emas'});aiSend('rejamni tuzib ber')"); pg.wait_for_timeout(400)
    chk('unparseable AI answer -> friendly error', 'tushunarli reja bermadi' in pg.inner_text('#aic'))
    ev("aiS().chat=[];aiRender();window.fnAI=async()=>({text:'{\"blocks\":[],\"extra\":[]}'});aiSend('rejamni tuzib ber')"); pg.wait_for_timeout(400)
    chk('an answer with no usable items still shows the fixed blocks (not an error)', 'Qur‘on' in pg.inner_text('#aic') and 'Rejaga qo‘sh' in pg.inner_text('#aic'))
    ev("()=>{aiS().chat=[];aiClose()}")
    # ---------- 5. Bugun card ----------
    ev("""()=>{S.ap={};const T=dk(),dow=new Date().getDay();S.ap[T]={tip:'Bugun ham barakali',it:[{id:'uyg',s:300,e:330,t:'Uyg‘onish',n:'',fx:1},{id:'qur',s:360,e:540,t:'Qur‘on',n:'3 bet sabaq',fx:1},{id:'x1',s:600,e:660,t:'Misol topshirig‘ini yoz',n:'',x:0},{id:'x2',s:720,e:780,t:'Zalga bor',n:'',x:0},{id:'iel',s:1275,e:1335,t:'IELTS',n:'Listening',fx:1}]};rwReset();tab='h';BV='j';VD=null;render()}"""); pg.wait_for_timeout(200)
    card = pg.inner_text('.apc'); chk('Bugun shows today\u2019s plan card with times, notes and progress 0/5', 'Bugun rejasi' in card and '06:00–09:00' in card and '3 bet sabaq' in card and '0/5' in card, card[:200])
    chk('the item that is happening now (10:00-11:00) is highlighted', pg.evaluate("document.querySelector('.apr.now b').textContent") == 'Misol topshirig‘ini yoz')
    pg.evaluate("document.querySelectorAll('canvas').forEach(c=>c.remove());document.querySelector('.apc').scrollIntoView({block:'center'})"); pg.wait_for_timeout(150); pg.screenshot(path='/tmp/dp_bugun.png')
    xp0 = ev("dayPts(dk()).t"); ev("apT(dk(),'x1')"); xp1 = ev("dayPts(dk()).t")
    chk('ticking an extra item: saved, +5 XP', ev("S.ap[dk()].it.find(x=>x.id==='x1').x") is True and xp1 - xp0 == 5 and 'AI reja' in json.dumps(ev("dayPts(dk()).p"), ensure_ascii=False), (xp0, xp1))
    xp0 = ev("dayPts(dk()).t"); ev("apT(dk(),'qur')"); xp1 = ev("dayPts(dk()).t")
    chk('ticking a fixed block uses the normal schedule record (S.done) and gives the normal block XP (+4), not the AI-plan XP', ev("S.done[dk()].qur") is True and xp1 - xp0 == 4, (xp0, xp1))
    ev("apT(dk(),'x1')"); chk('un-ticking works and removes the XP', ev("S.ap[dk()].it.find(x=>x.id==='x1').x") is False)
    ev("""()=>{S.ap[dk()].it=Array.from({length:12},(_,i)=>({id:'e'+i,s:600+i,e:601+i,t:'a',n:'',x:1}));rwReset()}"""); chk('XP from extras is capped at 8 items (40 XP)', ev("dayPts(dk()).p.find(x=>x[0]==='AI reja')[1]") == 40)
    ev("""()=>{S.ap={'2026-11-01':{tip:'',it:[{id:'qur',s:360,e:540,t:'Qur‘on',n:'',fx:1}]}};rwReset();VD='2026-11-01';render()}"""); pg.wait_for_timeout(150)
    chk('looking at tomorrow shows its plan, with the tick boxes disabled', 'Ertaga rejasi' in pg.inner_text('.apc') and pg.evaluate("[...document.querySelectorAll('.apc .ck')].every(b=>b.disabled)"))
    ev("apT('2026-11-01','qur')"); chk('a future day cannot be ticked', not ev("!!(S.done['2026-11-01']||{}).qur"))
    ev("VD=null;render()"); chk('today has no card when only tomorrow has a plan (10:00)', not ev("!!document.querySelector('.apc')") and 'Ertangi kunni rejala' not in pg.inner_text('#app'))
    # ---------- 6. evening nudge ----------
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 20, 0, 0)); ev("S.ap={};rwReset();render()"); pg.wait_for_timeout(100)
    chk('at 20:00 with no plan for tomorrow the Bugun screen offers "Ertangi kunni rejala"', 'Ertangi kunni rejala' in pg.inner_text('#app'))
    ev("S.ap={'2026-11-01':{tip:'',it:[{id:'qur',s:360,e:540,t:'Qur‘on',n:'',fx:1}]}};render()"); pg.wait_for_timeout(100)
    chk('...and not when tomorrow already has a plan', 'Ertangi kunni rejala' not in pg.inner_text('#app'))
    pg.clock.set_system_time(datetime.datetime(2026, 10, 31, 10, 0, 0)); ev("S.ap={};rwReset();render()"); pg.wait_for_timeout(100)
    chk('...and not in the morning', 'Ertangi kunni rejala' not in pg.inner_text('#app'))
    # ---------- 7. reminders ----------
    ev("""()=>{S.ap={'2026-11-01':{tip:'',it:[{id:'qur',s:360,e:540,t:'Qur‘on',n:'',fx:1},{id:'x1',s:555,e:600,t:'Misol topshirig‘ini yoz',n:'',x:0},{id:'x2',s:720,e:810,t:'Zalga bor',n:'',x:0}]},[dk()]:{tip:'',it:[{id:'x9',s:540,e:560,t:'O‘tgan ish',n:'',x:0},{id:'x8',s:780,e:840,t:'Bugungi ish',n:'',x:0}]}};rwReset()}""")
    ap = [r for r in ev("remRows()") if (r.get('kind') or '').startswith('ap@')]
    chk('reminders: only the EXTRA items (fixed blocks already have weekly reminders), 5 min before, for the right weekday and date', sorted((r['kind'], r['hhmm'], tuple(r['days'])) for r in ap if r['kind'] == 'ap@2026-11-01') == [('ap@2026-11-01', '09:10', (0,)), ('ap@2026-11-01', '11:55', (0,))], [(r['kind'], r['hhmm']) for r in ap])
    chk('items of today that are already in the past are not scheduled', [r['hhmm'] for r in ap if r['kind'] == 'ap@2026-10-31'] == ['12:55'], [(r['kind'], r['hhmm']) for r in ap])
    ev("S.rem.blk=false"); chk('with block reminders switched off there are none', not any((r.get('kind') or '').startswith('ap@') for r in ev("remRows()"))); ev("S.rem.blk=true")
    # ---------- 8. housekeeping ----------
    ev("""()=>{S.ap={'2026-09-01':{it:[],tip:''},'2026-10-30':{it:[],tip:''}};aiS().chat=[{r:'plan',date:'2026-11-01',it:[{id:'qur',s:360,e:540,t:'Qur‘on',n:'',fx:1}],tip:''}];dpSave(0)}""")
    chk('plans older than 14 days are pruned when saving (recent ones stay)', not ev("'2026-09-01' in S.ap") and ev("'2026-10-30' in S.ap") and ev("'2026-11-01' in S.ap"))
    ev("S.ap={'2026-11-01':{tip:'',it:[{id:'qur',s:360,e:540,t:'Qur‘on',n:'',fx:1}]}};window.confirm=()=>true;apDel('2026-11-01')"); chk('a plan can be deleted (the weekly schedule stays untouched)', not ev("'2026-11-01' in S.ap") and ev("bl().length") == 5)
    chk('no JavaScript errors during the whole run', not errs, errs[:3])
    b.close()
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
