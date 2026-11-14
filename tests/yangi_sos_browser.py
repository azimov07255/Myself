import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Nafs: 🆘 yo'l, 🕊 tavba va qaytish, 🛡 xavfli soatlar, 📱 Screen Time. Soat: chorshanba 2026-11-11 22:30.
import sys, json, re
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
with Run('sos', when=(2026, 11, 11, 22, 30, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_sos','trk_sosb','trk_sosm','trk_sosp','trk_sosc','trk_sosd','trk_sosr','trk_swh','trk_bsec'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');localStorage.setItem('trk_bsec','a');S.sos=undefined;SOSO=false;SOSV='h';SOSG={tg:{},msg:''};S.rem=undefined;S.bl=[{id:'uyqu1',t:'Uxlash',s:0,e:300,d:[0,1,2,3,4,5,6]}];tab='h';render()}""")
    pg.wait_for_timeout(100)
    h = ev("sosCard()"); chk('Bugun has a calm “🛡 Himoya” card with a big “🆘 Hozir qiynalyapman” button and a 📵 Telefon button', all(x in h for x in ['🛡 Himoya', '🆘 Hozir qiynalyapman', '📵 Telefon']))
    chk('the card also sits in the Nafs tab (Maqsad → Nafs) as “🆘 Nafs yordami” with Qaytish and Himoya buttons', all(x in ev("sosCard2()") for x in ['🆘 Nafs yordami', '🕊 Qaytish', '🛡']))
    ev("sosOpen('h')"); pg.wait_for_timeout(80); t = pg.inner_text('#sosv'); chk('the SOS screen opens with “Bu to‘lqin o‘tadi.”, a “▶ 10 daqiqalik kutishni boshlash” button, the five steps, zikr counters, optional triggers, “✅ Tinchlandim”, “😔 Yiqildim” and a button to message a trusted person', all(x in t for x in ['Bu to‘lqin o‘tadi', '10 daqiqalik kutishni boshlash', 'Hozir turgan joyingni o‘zgartir', 'Telefonni boshqa xonaga', 'Abdest ol', '2 rakat', 'Astag‘firulloh', 'Hasbunallohu', 'Nima kuchaytirdi', '✅ Tinchlandim', '😔 Yiqildim', 'Ishongan odamga yozish']))
    ev("sosStart()"); pg.wait_for_timeout(80); chk('the 10-minute wait starts at 10:00 and counts down by the clock', ev("document.getElementById('sost').textContent") == '10:00'); pg.clock.run_for(61000); pg.wait_for_timeout(60); chk('…after a minute it shows 8:59–9:00', ev("document.getElementById('sost').textContent") in ('8:59', '9:00'))
    ev("sosCk(0)"); ev("sosCk(2)"); chk('steps can be ticked (✅)', pg.inner_text('#sosv').count('✅') >= 2)
    pg.reload(); pg.wait_for_timeout(800); pg.clock.run_for(1500); ev("()=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true}"); ev("sosOpen('h')"); pg.wait_for_timeout(100); chk('after closing and reopening the app the wait is still running with the right time (it is kept by timestamp)', ev("sosRun()") is not None and ev("document.getElementById('sost').textContent") in ('8:50', '8:51', '8:52', '8:53', '8:54', '8:55', '8:56', '8:57', '8:58', '8:59', '9:00'), ev("document.getElementById('sost')&&document.getElementById('sost').textContent"))
    pg.clock.run_for(545000); pg.wait_for_timeout(1500); chk('when 10 minutes pass it says so once (“10 daqiqa o‘tdi”)', '10 daqiqa o‘tdi' in ev("document.getElementById('sost').textContent") and sum('10 daqiqa o‘tdi' in m for m in ev("__t")) == 1, (ev("document.getElementById('sost').textContent"), ev("__t"), ev("SOSG")))
    ev("sosTg('t')"); ev("sosTg('n')"); p0 = ev("dayPts(dk()).t"); ev("sosWin()"); l = ev("sosD().l"); chk('“✅ Tinchlandim” records a win with the chosen triggers (Telefon, Tun) — only time and tags, no text — and gives +8 points', len(l) == 1 and l[0]['r'] == 'g' and l[0]['tg'] == ['t', 'n'] and set(l[0].keys()) == {'id', 'd', 'm', 'r', 'tg', 'tv'} and ev("dayPts(dk()).t") == p0 + 8 and ev("sosRun()") is None)
    for _ in range(4): ev("sosWin()")
    chk('wins give points up to 3 a day (24), not more', ev("dayPts(dk()).t") == p0 + 24)
    chk('PRIVACY: by default the records live only on this phone — nothing about them is in the synced app data (S) and the local store holds them', 'sos' not in ev("Object.keys(S)") and len(json.loads(ev("localStorage.getItem('trk_sosd')"))['l']) == 5)
    # tavba
    ev("sosOpen('t')"); t = pg.inner_text('#sosv'); chk('the 🕊 Qaytish tab is gentle: “Qaytish eshigi doim ochiq”, the verse meaning (Zumar 53), the four conditions of tavba, “ustozingdan so‘ra”, and the buttons “Yiqilganimni belgilayman” / “Tavba qildim”', all(x in t for x in ['Qaytish eshigi doim ochiq', 'Zumar surasi, 53-oyat', '1. Qilganingdan pushaymon bo‘l', '4. Birovning haqi bo‘lsa', 'ustozingdan so‘ra', '😔 Yiqilganimni belgilayman', '🕊 Tavba qildim']))
    ev("sosFall1()"); ev("sosFall1()"); ys = [x for x in ev("sosD().l") if x['r'] == 'y']; chk('marking a slip records it once (a second tap within 6 hours does not duplicate it)', len(ys) == 1)
    pg.clock.run_for(10800000); ev("sosTawba()"); ys = [x for x in ev("sosD().l") if x['r'] == 'y']; chk('“Tavba qildim” stamps the return time on that slip (about 3 hours later) and gives +5 points', ys[0]['tv'] > 0 and 2.9 <= (ys[0]['tv'] - ys[0]['id']) / 3600e3 <= 3.1 and ['Tavba va qaytish', 5] in ev("dayPts(dk()).p"))
    ev("sosTawba()"); chk('tavba with no recent slip is still recorded (as a plain “return”), never refused', any(x['r'] == 'v' for x in ev("sosD().l")))
    pg.clock.set_system_time('2026-11-11T22:30:00')
    ev("()=>{const d=sosD();d.l=[{id:Date.now()-3*864e5,d:dAgo(3),m:1390,r:'y',tg:['t','n'],tv:Date.now()-3*864e5+5*3600e3},{id:Date.now()-2*864e5,d:dAgo(2),m:1400,r:'g',tg:['n'],tv:0},{id:Date.now()-864e5,d:dAgo(1),m:1395,r:'g',tg:['t','n'],tv:0}];sosW(d)}")
    s = ev("sosStats()"); chk('the return statistics are shown without blame: days since the last slip = 3, 1 return within 24 hours, 2 calm moments, average return time 5 hours', s['clean'] == 3 and s['ret'] == 1 and s['win'] == 2 and s['avg'] == 5 and ev("sosTawbaV()").count('3 kun') >= 1, s)
    chk('the hardest hour (23:00–24:00, 3 records) and the most common triggers (Tun, Telefon) are found', s['H']['23'] == 3 and s['TG']['n'] == 3 and s['TG']['t'] == 2)
    # himoya
    R_ = ev("sosRisk()"); chk('the shield proposes the risky hour found from the records (23:00–24:00, 3 times)', len(R_) == 1 and R_[0]['s'] == 1380 and R_[0]['n'] == 3 and R_[0]['a'] == 1, R_)
    ev("sosAddWin(1380,300)"); R_ = ev("sosRisk()"); chk('a manual window “Tun 23:00–05:00” can be added; it replaces the automatic one inside it', len(R_) == 1 and R_[0]['a'] == 0 and R_[0]['s'] == 1380 and R_[0]['e'] == 300)
    ev("sosTab('p')"); t = pg.inner_text('#sosv'); chk('the 🛡 Himoya tab lists the window, the protection plan (phone out of bed, Mulk, schedule block, reminder) and the hourly bar chart', '23:00–05:00' in t and 'karavotdan tashqarida' in t and 'Mulk surasi' in t and 'Qiyinlashgan soatlar' in t)
    chk('the middle of the night counts as inside the window (also across midnight): 23:30 and 02:00 are inside, 12:00 is not', ev("sosIn({s:1380,e:300},1410)") and ev("sosIn({s:1380,e:300},120)") and not ev("sosIn({s:1380,e:300},720)"))
    nx = ev("sosNext()"); chk('at 22:30 the next risky window starts in 30 minutes', nx['dd'] == 30 and nx['w']['s'] == 1380, nx)
    h = ev("sosCard()"); chk('close to the window the Bugun card says so (“Xavfli vaqt 30 daqiqadan keyin boshlanadi (23:00)”)', 'Xavfli vaqt 30 daqiqadan keyin boshlanadi (23:00)' in h)
    n0 = len(ev("S.bl")); ev("sosBlk(0)"); chk('a window that crosses midnight is not forced into the one-day schedule: the app explains and adds nothing', len(ev("S.bl")) == n0 and any('00:00 gacha qisqartir' in m for m in ev("__t")))
    ev("sosAddWin(1320,1380)"); idx = ev("sosD().mr.findIndex(w=>w.s===1320)"); ev("(i)=>sosBlk(i)", idx); b = ev("S.bl[S.bl.length-1]"); chk('a normal window (22:00–23:00) becomes a daily “📵 Telefonsiz vaqt” block in the schedule', b['t'] == '📵 Telefonsiz vaqt' and b['s'] == 1320 and b['e'] == 1380 and b['d'] == [0, 1, 2, 3, 4, 5, 6])
    p0 = ev("dayPts(dk()).t"); ev("sosPhone()"); chk('the 📵 phone ritual gives +5 points and the card shows “📵 telefon qo‘yildi”; tapping again undoes it', ev("dayPts(dk()).t") == p0 + 5 and '📵 telefon qo‘yildi' in ev("sosCard()")); ev("sosPhone()"); chk('…', ev("dayPts(dk()).t") == p0)
    # eslatma
    ev("()=>{S.rem=Object.assign({},S.rem,{on:true,tg:false,blk:false,close:false,wake:false,nz:false,zk:false,yo:false,rz:false,custom:[]})}"); rs = [x for x in ev("remRows()") if x.get('kind') == 'sh']
    chk('with reminders on, each window gets a “🛡 Xavfli vaqt yaqinlashyapti” reminder 20 minutes before it starts (22:40 and 21:40), every day', sorted(x['hhmm'] for x in rs) == ['21:40', '22:40'] and all(x['days'] == [0, 1, 2, 3, 4, 5, 6] and re.fullmatch(r'[a-z]{1,3}(:[\w-]+)?(@\d{4}-\d\d-\d\d)?', x['kind']) for x in rs), rs)
    ev("uiS('trk_sosm','0')"); chk('the reminder can be switched off', not [x for x in ev("remRows()") if x.get('kind') == 'sh']); ev("uiS('trk_sosm','1')"); ev("()=>{S.rem.on=false}"); chk('and there is none when all reminders are off', not [x for x in ev("remRows()") if x.get('kind') == 'sh'])
    # screen time
    ev("sosTab('m')"); t = pg.inner_text('#sosv'); chk('📱 Screen Time guide: the 7 steps (turn on, passcode, Downtime, App Limits, Limit Adult Websites, Allowed Apps, Passcode Changes), honest note that the app cannot block other apps, and the link for a separate 🆘 home-screen shortcut ending in #sos', all(x in t for x in ['Use Screen Time Passcode', 'Downtime', 'App Limits', 'Limit Adult Websites', 'Allowed Apps & Features', 'Passcode Changes', 'to‘sa olmaydi', '#sos']) and '0/7' in t)
    ev("sosCk2('st',0)"); ev("sosCk2('st',4)"); chk('steps can be ticked and the progress counter follows (2/7), saved on this phone', '2/7' in pg.inner_text('#sosv') and len(json.loads(ev("localStorage.getItem('trk_sosd')"))['ck']['st']) == 2)
    # sozlamalar
    ev("sosTab('g')"); ev("(()=>{const e=document.getElementById('sosw');e.value='Allohga yaqin bo‘lish';sosAddW()})()"); ev("(()=>{const e=document.getElementById('sosw');e.value='Madrasaga kirish';sosAddW()})()"); chk('your own reasons (“Nima uchun?”) can be added (up to 6) and show on the SOS screen', ev("sosD().w") == ['Allohga yaqin bo‘lish', 'Madrasaga kirish']); ev("sosTab('h')"); chk('…', 'Madrasaga kirish' in pg.inner_text('#sosv'))
    ev("sosTab('g')"); t = pg.inner_text('#sosv'); chk('the ⚙️ tab explains privacy (“matn yo‘q”, “faqat shu qurilmada”), offers “Bulutga ham”, and can erase all records', all(x in t for x in ['matn yo‘q', 'faqat shu qurilmada', 'Bulutga ham', 'Hamma qaydlarni o‘chirish']))
    ev("uiS('trk_sosc','1')"); ev("sosLog('g',{})"); chk('if you choose “Bulutga ham”, the records move into the synced data (S.sos); otherwise never', 'sos' in ev("Object.keys(S)") and len(ev("S.sos.l")) >= 1); ev("uiS('trk_sosc','0')")
    ev("sosClr()"); d = ev("sosD()"); chk('erasing removes everything (records, windows, reasons)', d['l'] == [] and d['mr'] == [] and d['w'] == [])
    # kartochka rejimlari
    ev("uiS('trk_sosb','r')"); chk('“Faqat xavfli vaqt oldidan” hides the card outside risky times', ev("sosCard()") == ''); ev("sosAddWin(1380,300)"); chk('…and shows it 30 minutes before one', '🛡 Himoya' in ev("sosCard()")); ev("uiS('trk_sosb','o')"); chk('“Ko‘rsatilmasin” hides it completely', ev("sosCard()") == ''); ev("uiS('trk_sosb','a')")
    ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings → Jilo has the switches: Nafs bo‘limi, Himoya kartasi, xavfli oyna eslatmasi, ball berish, qaydlarni saqlash joyi', all(x in t for x in ['Nafs bo‘limi', 'Himoya kartasi', 'Xavfli oyna eslatmasi', 'Ball berish', 'Qaydlarni saqlash joyi']))
    ev("uiS('trk_sos','0')"); ev("sosClose()"); chk('switched off: no card, nothing opens, no points', ev("sosCard()") == '' and ev("sosCard2()") == '' and ev("(()=>{sosOpen('h');return !!document.getElementById('sosv')})()") is False); ev("uiS('trk_sos','1')")
    # yorliq
    pg.evaluate("location.hash='#sos'"); pg.reload(); pg.wait_for_timeout(900); pg.clock.run_for(1500); pg.wait_for_timeout(300); chk('opening the app with “#sos” (the home-screen shortcut) goes straight to the 🆘 screen', ev("!!document.getElementById('sosv')") and 'Bu to‘lqin o‘tadi' in pg.inner_text('#sosv')); pg.evaluate("history.replaceState(null,'',location.pathname)")
    bad = []
    ev("()=>{window.toast=()=>{};window.confirm=()=>true;sosClose()}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];tab='h';render()}", [ui, th]); pg.wait_for_timeout(60); ok = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            for v in ('h', 't', 'p', 'm', 'g'):
                ev("(v)=>{SOSO=true;SOSV=v;sosDraw()}", v); ok = ok and ev("document.querySelector('#sosv .asc').scrollWidth<=document.querySelector('#sosv .asc').clientWidth+1")
            ev("sosClose()")
            if not ok: bad.append(ui + th)
    chk('the Himoya card and all five tabs fit the phone in Klassik, Yangi and Liquid Glass, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
