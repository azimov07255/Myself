# Isolation marafoni: kun sanagichi, 5 ta kunlik ish (avto), Prava rejasi, Hifz, pul, motivatsiya, muhosaba. Soat: 2026-11-16 (dushanba) 10:00.
import sys, os
sys.path.insert(0, os.environ.get('KT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tests')
from _pw import Run
with Run('isolation', when=(2026, 11, 16, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-11-16T10:00:00')
    def fresh():
        ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);S.iso={lim:60,m:{},log:[]};S.nm.d={};S.rules={};S.money=[];S.pr.tests=[];S.pr.er={};S.pr.exam='';S.q.lg=[];S.q.ppd=0;S.fin={open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[]};W='p';tab='o';OT='i';render()}"""); pg.wait_for_timeout(100)
    text = lambda: pg.inner_text('#app').replace('\xa0', ' ')
    fresh()
    chk('before starting: the Isolation tab offers "Marafonni boshlash" (start date, days, tests a day, exam date, why)', 'Marafonni boshlash' in text() and pg.locator('#mrs').count() == 1 and pg.locator('#mrn').count() == 1 and pg.locator('#mrw').count() == 1)
    chk('...and the old Isolation tools are still below (screen time, distraction log)', 'Chalg‘ishlar nazorati' in text() and 'Bugungi ekran vaqti' in text())
    pg.fill('#mre', '2026-11-29'); pg.fill('#mrw', 'Prava olib, Qur‘onni davom ettiraman'); pg.click('#app button >> text="Marafonni boshlash"'); pg.wait_for_timeout(150)
    m = ev("S.iso.mr")
    chk('started: on, start today, 14 days, 2 tests a day, the reason saved, exam date saved to Prava', m['on'] == 1 and m['start'] == '2026-11-16' and m['n'] == 14 and m['pt'] == 2 and 'Prava olib' in m['why'] and ev("S.pr.exam") == '2026-11-29', m)
    t = text(); chk('day 1: the hero shows "1 / 14 kun", "13 kun qoldi" and the reason in quotes', '1 / 14 kun' in t and '13 kun qoldi' in t and 'Prava olib, Qur‘onni davom ettiraman' in t)
    chk('the 14-dot road is drawn (14 dots, today highlighted)', pg.locator('#app .mrfdot').count() == 14 and pg.locator('#app .mrfdot.now').count() == 1)
    I = ev("mrfInfo()"); chk('day 3 (18 Nov): dc = 3, 11 days left', (pg.clock.set_system_time('2026-11-18T10:00:00') or True) and ev("mrfInfo().dc") == 3 and ev("mrfInfo().left") == 11)
    pg.clock.set_system_time('2026-11-16T10:00:00')
    # kunlik 5 ta ish
    D = ev("mrfDay('2026-11-16')"); chk('five daily items, none done yet: namoz 0 / 5, tests 0 / 2, 0 of 5', len(D['it']) == 5 and D['dn'] == 0 and D['it'][0]['v'] == '0 / 5' and D['it'][2]['v'] == '0 / 2', D)
    ev("()=>{S.nm.d['2026-11-16']={fajr:1,dhuhr:1,asr:1,maghrib:1,isha:1};render()}"); chk('five prayers marked in Bugun → the prayer item is done automatically', ev("mrfDay('2026-11-16').it[0].ok") is True and ev("mrfDay('2026-11-16').it[0].v") == '5 / 5')
    ev("()=>{S.nm.d['2026-11-16']={fajr:1,dhuhr:2,asr:1,maghrib:1,isha:1};render()}"); chk('a missed prayer (✗) does not count: 4 / 5 is not done', ev("mrfDay('2026-11-16').it[0].ok") is False and ev("mrfDay('2026-11-16').it[0].v") == '4 / 5')
    ev("()=>{S.nm.d['2026-11-16']={fajr:1,dhuhr:1,asr:1,maghrib:1,isha:1}}")
    ev("()=>{S.q.ppd=3;S.q.lg=[{id:1,d:'2026-11-16',i:1,a:0,b:2,t:'n'},{id:2,d:'2026-11-16',i:2,a:0,b:1,t:'n'},{id:3,d:'2026-11-16',i:1,a:2,b:5,t:'r'}];render()}"); chk('Qur‘on: 3 new pages (2 + 1) reach the daily goal of 3; review entries (r) are NOT counted', ev("mrfPages('2026-11-16')") == 3 and ev("mrfDay('2026-11-16').it[1].ok") is True)
    ev("()=>{S.pr.tests=[{id:1,d:'2026-11-16',c:18,t:20},{id:2,d:'2026-11-15',c:10,t:20}];render()}"); chk('Prava: only today\'s tests count (1 of 2): not done yet', ev("mrfDay('2026-11-16').it[2].ok") is False and ev("mrfDay('2026-11-16').it[2].v") == '1 / 2')
    ev("()=>{S.pr.tests.push({id:3,d:'2026-11-16',c:19,t:20});render()}"); chk('the second test today completes the Prava item', ev("mrfDay('2026-11-16').it[2].ok") is True)
    ev("()=>{S.rules['2026-11-16']={ig:true};render()}"); chk('the "Instagramsiz kun" rule completes the phone item', ev("mrfDay('2026-11-16').it[3].ok") is True)
    chk('4 of 5 done, not a full day until the evening review is written', ev("mrfDay('2026-11-16').dn") == 4 and ev("mrfDay('2026-11-16').full") is False)
    ev("()=>{document.getElementById('mrg').value='Hamma test yechildi';document.getElementById('mri').value='Telefonga kamroq qarayman';document.getElementById('mrx').value='Chorrahalar mavzusi';mrfRef()}"); pg.wait_for_timeout(120)
    chk('the evening review is saved and shown; now 5 of 5 = a full day', ev("S.iso.mr.ref['2026-11-16'].g") == 'Hamma test yechildi' and ev("mrfDay('2026-11-16').full") is True and 'Chorrahalar mavzusi' in text())
    chk('the screen congratulates ("Bugun to‘liq bajarding") and the day-1 dot shows a check', 'to‘liq bajarding' in text() and 'Barakalla' in text() and ev("document.querySelector('#app .mrfdot').textContent") == '✓')
    # qo'lda belgilash
    ev("()=>{S.iso.mr.man={};S.rules={};render();mrfTog('ph')}"); chk('manual toggle: the phone item can be ticked by hand', ev("mrfDay('2026-11-16').it[3].ok") is True)
    ev("mrfTog('ph')"); chk('...and unticked again', ev("mrfDay('2026-11-16').it[3].ok") is False)
    ev("mrfTog('nm')"); chk('an auto-completed item (prayers 5 / 5) cannot be toggled by hand (it tells why)', ev("mrfDay('2026-11-16').it[0].ok") is True and any('avtomatik' in x for x in ev("window.__t")))
    # seriya
    ev("()=>{S.rules={};S.iso.mr.man={};S.iso.mr.ref={'2026-11-16':{g:'a'},'2026-11-17':{g:'b'}};['2026-11-16','2026-11-17'].forEach(k=>{S.nm.d[k]={fajr:1,dhuhr:1,asr:1,maghrib:1,isha:1};S.rules[k]={ig:true};S.q.lg.push({id:k.slice(-2)*1000,d:k,i:1,a:0,b:3,t:'n'});S.pr.tests.push({id:k.slice(-2)*77,d:k,c:18,t:20},{id:k.slice(-2)*99,d:k,c:19,t:20})})}")
    pg.clock.set_system_time('2026-11-18T10:00:00'); ev("()=>{render()}"); I = ev("mrfInfo()")
    chk('two full days in a row (16, 17) then today (18, not yet complete) → streak 2', ev("mrfStreak(mrfInfo())") == 2, I)
    chk('the hero shows "🔥 2 kun ketma-ket" and "3 / 14 kun", "11 kun qoldi"', '2 kun ketma-ket' in text() and '3 / 14 kun' in text() and '11 kun qoldi' in text())
    # Prava reja
    tp = lambda d, n=14: ev("(a)=>mrfTopic(a[0],a[1])", [d, n])
    chk('Prava plan: day 1 = Yo‘l belgilari, day 3 = Tezlik, day 9 = Huquq va javobgarlik (9 topics in order)', tp(1)['t'] == 'Yo‘l belgilari' and tp(3)['t'] == 'Tezlik' and tp(9)['t'] == 'Huquq va javobgarlik' and tp(1)['k'] == 'mavzu')
    chk('days 10-13 = weak topics and full tests; the last day = rest before the exam', tp(10)['k'] == 'zaif' and tp(13)['k'] == 'zaif' and tp(14)['k'] == 'dam' and 'Imtihon oldi' in tp(14)['t'])
    chk('a 7-day marafon compresses it: 5 topic days, then weak topics, then the exam eve', tp(1, 7)['k'] == 'mavzu' and tp(5, 7)['k'] == 'mavzu' and tp(6, 7)['k'] == 'zaif' and tp(7, 7)['k'] == 'dam')
    ev("()=>{S.pr.er={'Chorrahalar':5,'Tezlik':3,'Yo‘l belgilari':1,'Boshqa':0};S.pr.pm=18;S.pr.exam='2026-11-29';render()}"); t = text()
    chk('the Prava block: today\'s topic (day 3 = Tezlik), tests 0 / 2 today, exam in 11 days, average of the last tests, weak topics', 'Tezlik' in t and '0 / 2' in t and 'Imtihongacha 11 kun' in t and 'Chorrahalar (5)' in t and 'Oxirgi 5 test o‘rtachasi' in t)
    # Hifz
    chk('Hifz block: marafon target 3 pages x 14 days = 42 bet, with the 3 + 3 + 3 pages done so far', '42 bet' in t and '/ 3 bet' in t)
    # pul
    ev("()=>{S.fin.budget=3100000;S.money=[{id:1,d:'2026-11-17',k:'out',a:30000,c:'Ovqat',n:'',w:'p',ac:'cash'},{id:2,d:'2026-11-18',k:'out',a:20000,c:'Ovqat',n:'',w:'p',ac:'cash'},{id:3,d:'2026-11-17',k:'out',a:15000,c:'Kino',n:'',w:'p',ac:'cash',t:'k'}];render()}"); MN = ev("(()=>{const m=mrfMoney(mrfInfo());return {ns:m.ns,kr:m.kr,lim:m.D&&m.D.lim}})()")
    chk('money guard: of the 2 finished days only 16 Nov had no spending → 1 no-spend day; 15 000 marked "keraksiz"; a daily limit exists', MN['ns'] == 1 and MN['kr'] == 15000 and MN['lim'] > 0, MN)
    t = text(); chk('the money block shows the daily limit, the no-spend days and the 24h wishlist advice', 'Pulni asrash' in t and 'Sarfsiz kunlar: 1' in t and '24 soatlik xohish ro‘yxati' in t)
    ev("()=>{S.money.push({id:9,d:'2026-11-18',k:'out',a:900000,c:'Boshqa',n:'',w:'p',ac:'cash'});render()}"); chk('spending far over the limit shows a warning', 'oshdi' in text())
    # g'alabalar, motivatsiya
    w = ev("mrfWins(mrfInfo())"); chk('wins: full days (2), the streak and no-spend days are listed (nothing is done yet today)', any('To‘liq bajarilgan kunlar: 2' in x for x in w) and any('2 kun ketma-ket' in x for x in w), w)
    q1 = ev("(()=>{const I=mrfInfo();return MRFQ.d[(I.dc+MRFO)%MRFQ.d.length][0]})()"); ev("mrfOther()"); q2 = ev("(()=>{const I=mrfInfo();return MRFQ.d[(I.dc+MRFO)%MRFQ.d.length][0]})()")
    chk('motivation: a religious and a worldly line every day; "Boshqasini ko‘rsat" gives another one', q1 != q2 and 'Diniy' in text() and 'Hayotiy' in text() and 'ishonchli manbaga' in text(), (q1, q2))
    chk('every religious line names its source and says it is the meaning (ma‘nosi)', ev("MRFQ.d.every(x=>x[1].includes('ma‘nosi')&&x[1].length>10)") and ev("MRFQ.d.length") >= 10 and ev("MRFQ.w.length") >= 8)
    chk('the daily schedule highlights the current block (10:00 → Prava: bugungi mavzu)', pg.evaluate("(()=>{const r=[...document.querySelectorAll('#app .row')].find(r=>r.textContent.includes('hozir')&&r.textContent.includes('09:00'));return !!r})()"))
    # Bugun mini karta
    ev("()=>{tab='h';BV='j';render()}"); pg.wait_for_timeout(120); chk('Bugun → Jadval shows the small card "Isolation: 3 / 14 kun"', 'Isolation: 3 / 14 kun' in text())
    ev("()=>{BV='m';render()}"); chk('the small card is only on the Jadval tab', 'Isolation: 3 / 14 kun' not in text())
    # tugash va to'xtatish
    pg.clock.set_system_time('2026-12-05T10:00:00'); ev("()=>{tab='o';OT='i';render()}"); chk('after the 14 days the screen says the marafon is finished', 'Marafon tugadi' in text() and ev("mrfInfo().over") is True)
    ev("()=>{tab='h';BV='j';render()}"); chk('...and the Bugun card disappears', 'Isolation:' not in text())
    pg.clock.set_system_time('2026-11-18T10:00:00'); ev("()=>{tab='o';OT='i';render()}"); ev("mrfStop()"); chk('"Marafonni to‘xtatish" turns it off but keeps the data', ev("S.iso.mr.on") == 0 and ev("Object.keys(S.iso.mr.ref).length") >= 2)
    chk('after stopping, the start form is offered again', pg.locator('#mrs').count() == 1)
    # boshlanishidan oldin
    ev("()=>{S.iso.mr={on:1,start:'2026-11-20',n:14,pt:2,man:{},ref:{}};render()}"); chk('a marafon starting in the future shows the countdown ("2 kundan keyin")', '2 kundan keyin' in text())
    # uslublar
    ev("()=>{S.iso.mr={on:1,start:'2026-11-16',n:14,pt:2,why:'Niyat',man:{},ref:{}};render()}")
    for cls, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        ev("(c)=>{document.documentElement.className=c;render()}", cls); pg.wait_for_timeout(80)
        chk('%s style: no horizontal overflow on the Isolation screen' % nm, pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    print('\n%d passed, %d failed' % (R.ok, R.bad))
