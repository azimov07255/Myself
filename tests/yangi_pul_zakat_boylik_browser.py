# Pul: zakat va sadaqa, sof boylik, do'kon foydasi, xarajat = necha soatlik ish. Soat: 2026-10-10 (shanba) 10:00.
import sys, re
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
digits = lambda s: int(re.sub(r'[^\d-]', '', s.replace('−', '-')) or 0)
def M(i, d, k, a, c='Ovqat', n='', w='p', ac='cash', t=None):
    x = {'id': i, 'd': d, 'k': k, 'a': a, 'c': c, 'n': n, 'w': w, 'ac': ac}
    if t: x['t'] = t
    return x
with Run('pul_zbd') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-10-10T10:00:00')
    def setup(money=None, debts=None, fin=None, w='p', pv='b'):
        ev("""(a)=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);S.money=a[0];S.debts=a[1];S.fin=Object.assign({open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[]},a[2]);W=a[3];PV=a[4];PF={mo:0,ac:'all',k:'all',q:''};K='out';FA='';FN='';FT='';EID=0;PTZ='';tab='p';render()}""", [money or [], debts or [], fin or {}, w, pv])
        pg.wait_for_timeout(80)
    text = lambda: pg.inner_text('#app').replace('\xa0', ' ')
    nows = lambda: pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1")

    # ================= ZAKAT =================
    setup(pv='z')
    chk('the Pul tabs include "🕌 Zakat" and opening it shows the zakat card', 'Zakot hisobi' in text() and ev("[...document.querySelectorAll('#app .seg button')].some(b=>/Zakat/.test(b.textContent))"))
    chk('without a gold price it asks for the price (no zakat is invented)', 'narxini yoz' in text() and ev("zktCalc().ok") is False)
    setup(money=[M(1, '2026-10-01', 'in', 50000000, 'Maosh')], fin={'zk': {'b': 'g', 'pg': 1000000}}, pv='z')
    o = ev("zktCalc()")
    chk('gold 1 000 000/g × 85 g = nisob 85 000 000; wealth 50 000 000 → not reached', o['nisob'] == 85000000 and o['wealth'] == 50000000 and not o['reached'] and o['due'] == 0, o)
    chk('the screen says "Nisobga yetmagan", 59% and shows no zakot amount', 'Nisobga yetmagan' in text() and '59%' in text() and 'Taxminiy zakot' not in text())
    setup(money=[M(1, '2026-10-01', 'in', 100000000, 'Maosh')], debts=[{'id': 1, 'k': 'lend', 'a': 10000000, 'pay': [], 'st': 'open', 'd': '2026-10-02', 'ac': 'cash', 'p': 'Ali'}, {'id': 2, 'k': 'borrow', 'a': 5000000, 'pay': [], 'st': 'open', 'd': '2026-10-02', 'ac': 'cash', 'p': 'Vali'}],
          fin={'zk': {'b': 'g', 'pg': 1000000, 'x': 5000000}}, pv='z')
    o = ev("zktCalc()")
    # naqd: 100M −10M(berilgan qarz) +5M(olingan qarz) = 95M; + qarzdorlar 10M − qarzim 5M + ilovada yo'q 5M = 105M
    chk('wealth = cash/card 95 000 000 + owed to me 10 000 000 − I owe 5 000 000 + outside assets 5 000 000 = 105 000 000', o['cash'] == 95000000 and o['rec'] == 10000000 and o['pay'] == 5000000 and o['wealth'] == 105000000, o)
    chk('reached; zakat = 2.5% of 105 000 000 = 2 625 000', o['reached'] and o['due'] == 2625000, o)
    t = text(); chk('the screen shows "Nisobga yetgan", the amount and the breakdown (Jami, Nisob)', 'Nisobga yetgan' in t and '2 625 000' in t and 'Jami' in t and 'Nisob (85 g)' in t)
    chk('without a hawl date it explains hawl and offers to start it (no zakat is called "due now")', 'Hawl bugundan boshlansin' in t)
    ev("zktStart()"); pg.wait_for_timeout(80); o = ev("zktCalc()")
    chk('starting the hawl today: 354 days left; not yet due', o['z']['h'] == '2026-10-10' and o['left'] == 354 and o['hawl'] is False, o)
    ev("zktDate('2026-06-22')"); o = ev("zktCalc()"); chk('hawl begun 2026-06-22 (110 days ago) → 244 days left', o['left'] == 244, o)
    ev("zktDate('2025-09-01')"); o = ev("zktCalc()"); chk('hawl begun a year+ ago → completed (zakat time) and the screen says so', o['hawl'] is True and 'Hawl to‘ldi' in text(), o)
    pg.fill('#zktp', '1 000 000'); pg.click('#app button >> text="+"'); pg.wait_for_timeout(120)
    o = ev("zktCalc()"); m = ev("S.money.filter(m=>m.z)")
    chk('"Zakot berdim 1 000 000" is recorded: paid 1 000 000, rest 1 625 000', o['paid'] == 1000000 and o['rest'] == 1625000, o)
    chk('...and it also creates an expense (category Sadaqa, note Zakot) so the balance drops by 1 000 000', len(m) == 1 and m[0]['c'] == 'Sadaqa' and m[0]['n'] == 'Zakot' and m[0]['k'] == 'out' and m[0]['a'] == 1000000 and ev("bal('p').tot") == 94000000, m)
    ev("zktPayDel(S.fin.zk.p[0].id)"); chk('a wrongly entered payment can be removed from the list', ev("zktCalc().paid") == 0)
    ev("S.money=S.money.filter(m=>!m.z);S.fin.zk.p=[];S.fin.zk.h=''")
    ev("zktBasis('s')"); o = ev("zktCalc()"); chk('silver basis: needs its own price (none yet) so no nisob', o['grams'] == 595 and o['ok'] is False)
    ev("zktSet('ps','100000')"); o = ev("zktCalc()"); chk('silver 100 000/g × 595 g = 59 500 000', o['nisob'] == 59500000 and o['reached'] is True, o)
    ev("zktBasis('g')"); ev("zktSet('d',true)"); ev("S.money.push({id:77,d:'2026-10-02',k:'in',a:20000000,c:'Dokon daromadi',n:'',w:'d',ac:'cash'})")
    chk('"Do‘kon hamyonini ham hisobga ol" adds the shop balance (20 000 000) to the wealth', ev("zktCalc().cash") == 115000000, ev("zktCalc()"))
    ev("zktSet('d',false)")
    # sadaqa
    setup(money=[M(1, '2026-10-02', 'in', 1000000, 'Maosh'), M(2, '2026-10-03', 'out', 20000, 'Sadaqa'), M(3, '2026-10-04', 'out', 30000, 'Sadaqa'), M(4, '2026-02-01', 'out', 100000, 'Sadaqa'), {**M(5, '2026-10-05', 'out', 400000, 'Sadaqa'), 'z': 1}], fin={'zk': {'b': 'g', 'sg': 100000}}, pv='z')
    s = ev("zktSad()")
    chk('sadaqa this month = 50 000 (zakot is NOT counted as sadaqa), this year 150 000, zakot this year 400 000, 5% of income', s['mo'] == 50000 and s['yr'] == 150000 and s['zk'] == 400000 and s['pc'] == 5, s)
    chk('a monthly sadaqa goal of 100 000 shows 50 000 / 100 000', '50 000 / 100 000' in text())
    chk('the page has no horizontal overflow', nows())

    # ================= SOF BOYLIK =================
    D = [{'id': 1, 'k': 'borrow', 'a': 2000000, 'pay': [{'id': 11, 'd': '2026-10-05', 'a': 500000, 'ac': 'cash'}], 'st': 'open', 'd': '2026-09-20', 'ac': 'cash', 'p': 'Vali'},
         {'id': 2, 'k': 'lend', 'a': 300000, 'pay': [], 'st': 'open', 'd': '2026-10-01', 'ac': 'cash', 'p': 'Ali'}]
    setup(money=[M(1, '2026-08-15', 'in', 5000000, 'Maosh'), M(2, '2026-09-10', 'out', 1000000), M(3, '2026-10-03', 'out', 0 + 100, 'Ovqat')][:2], debts=D, fin={'open': {'p': {'cash': 1000000, 'card': 0}, 'd': {'cash': 0, 'card': 0}}}, pv='h')
    s = ev("sblSeries(12)")
    chk('today: cash 1 000 000 + 5 000 000 − 1 000 000 + borrowed 2 000 000 − repaid 500 000 − lent 300 000 = 6 200 000, equal to the main balance', s[-1]['cash'] == 6200000 and ev("bal('p').tot") == 6200000, s[-1])
    chk('net worth today = cash 6 200 000 + owed to me 300 000 − I owe 1 500 000 = 5 000 000', s[-1]['rec'] == 300000 and s[-1]['pay'] == 1500000 and s[-1]['nw'] == 5000000, s[-1])
    chk('end of September = 5 000 000 (borrowing does not change net worth) and end of August = 6 000 000', s[-2]['nw'] == 5000000 and s[-3]['nw'] == 6000000, (s[-2], s[-3]))
    chk('the series has 12 points, the last one is today and the first one is a year back', len(s) == 12 and s[-1]['D'] == '2026-10-10' and s[0]['D'] == '2025-11-30', (s[0]['D'], s[-1]['D']))
    t = text(); chk('Hisobot shows "Sof boylik" with 5 000 000, the change vs last month and a chart', 'Sof boylik' in t and '5 000 000' in t and pg.locator('#app svg polyline').count() == 1)
    chk('the change since last month is 0 (shown as a number, not hidden)', 'O‘tgan oy oxiriga nisbatan' in t)
    ev("S.debts[1].led=false;render()"); s2 = ev("sblAt(dk(),['p'])")
    chk('a debt marked "faqat yozib qo‘yish" does not change the balance or net worth: cash 6 500 000, no receivable', s2['cash'] == 6500000 and s2['rec'] == 0 and s2['nw'] == 5000000, s2)
    ev("S.debts[1].led=true")
    ev("S.money.push({id:90,d:'2026-10-02',k:'in',a:3000000,c:'Dokon daromadi',n:'',w:'d',ac:'cash'});render()")
    chk('shop wallet is NOT included by default', ev("sblAt(dk(),sblWs()).nw") == 5000000)
    ev("sblNwd(true)"); chk('with the checkbox the shop is included: 8 000 000', ev("sblAt(dk(),sblWs()).nw") == 8000000)
    ev("sblNwd(false)")
    setup(pv='h'); chk('with no data it says so and shows no chart', 'sof boylik va uning oyma-oy' in text() and pg.locator('#app svg polyline').count() == 0)
    setup(money=[M(1, '2026-10-01', 'out', 400000)], fin={'open': {'p': {'cash': 100000, 'card': 0}, 'd': {'cash': 0, 'card': 0}}}, pv='h')
    chk('a negative net worth is shown with a minus and the chart does not break', '−300 000' in text() and pg.locator('#app svg polyline').count() == 1)
    chk('no horizontal overflow in Hisobot', nows())

    # ================= DOKON FOYDASI =================
    shop = [M(1, '2026-10-02', 'in', 1000000, 'Dokon daromadi', w='d'), M(2, '2026-10-03', 'in', 2000000, 'Dokon daromadi', w='d'), M(3, '2026-10-05', 'in', 500000, 'Dokon daromadi', w='d'),
            M(4, '2026-10-02', 'out', 400000, 'Boshqa', w='d'), M(5, '2026-10-06', 'out', 700000, 'Boshqa', w='d'), M(6, '2026-09-10', 'in', 2000000, 'Dokon daromadi', w='d'), M(7, '2026-09-11', 'out', 1500000, 'Boshqa', w='d'),
            M(8, '2026-10-04', 'in', 9999999, 'Maosh', w='p')]
    setup(money=shop, w='d', pv='h')
    c = ev("dfyCalc(0)")
    chk('revenue 3 500 000, cost 1 100 000, profit 2 400 000, margin 69% (the personal 9 999 999 is NOT counted)', c['A']['rev'] == 3500000 and c['A']['cost'] == 1100000 and c['A']['profit'] == 2400000 and c['margin'] == 69, c)
    chk('versus last month (2 000 000 / 1 500 000 / 500 000): revenue +75%, profit +380%', c['dRev'] == 75 and c['dProfit'] == 380, c)
    chk('3 sale days out of 10 elapsed, 7 days without a sale, average per sale day 1 166 667', c['sale'] == 3 and c['el'] == 10 and c['noSale'] == 7 and c['avgSale'] == 1166667, c)
    chk('best day 3 Oct (2 000 000), weakest sale day 5 Oct (500 000), 1 day with more cost than revenue', c['best'][0] == '2026-10-03' and c['best'][1]['i'] == 2000000 and c['worst'][0] == '2026-10-05' and c['lossDays'] == 1, c)
    chk('projection to month end = 3 500 000 / 10 × 31 = 10 850 000', c['proj'] == 10850000, c)
    chk('the strongest weekday is Saturday (avg 1 000 000: 3 and 10 Oct)', c['bestW'] == 5 and c['avg'][5] == 1000000, c['avg'])
    t = text(); chk('the screen shows the card with profit, margin, best day, "savdosiz kun" and the weekday bars', 'Do‘kon foydasi' in t and '2 400 000' in t and '69%' in t and 'Eng yaxshi kun' in t and '3-oktyabr' in t and 'savdosiz kun: 7' in t and 'Shanba' in t, t[:300])
    ev("(()=>{PF.mo=-1;render()})()"); pg.wait_for_timeout(60); c9 = ev("dfyCalc(-1)")
    chk('last month (September) works too: revenue 2 000 000, cost 1 500 000, profit 500 000; no projection for a past month', c9['A']['rev'] == 2000000 and c9['A']['profit'] == 500000 and c9['proj'] is None and '500 000' in text(), c9)
    ev("(()=>{PF.mo=0;render()})()")
    chk('it also shows the profit sign correctly for a loss month', ev("(()=>{S.money=[{id:1,d:'2026-10-02',k:'in',a:100000,c:'Dokon daromadi',n:'',w:'d',ac:'cash'},{id:2,d:'2026-10-03',k:'out',a:300000,c:'Boshqa',n:'',w:'d',ac:'cash'}];render();return 1})()") == 1 and '−200 000' in text())
    ev("(()=>{S.money=[];PF.mo=0;render()})()"); chk('an empty month shows a short hint instead of zeros', 'do‘kon yozuvi yo‘q' in text())
    chk('in the shop wallet the personal net worth and hours cards are NOT shown (they would mislead)', 'Sof boylik' not in text() and 'Xarajat = mehnat' not in text())
    ev("(()=>{W='p';render()})()"); chk('the personal wallet does not show the shop card', 'Do‘kon foydasi' not in text())
    setup(money=shop, w='d', pv='h'); chk('no horizontal overflow in the shop report', nows())

    # ================= XARAJAT = MEHNAT =================
    setup(pv='b'); chk('with nothing set there is no hours hint anywhere', ev("mhnTxt(25000)") == '' and pg.locator('#mhnf').count() == 0)
    ev("mhnSet('inc','1 600 000')"); pg.wait_for_timeout(60)
    chk('income 1 600 000 / default 160 hours = 10 000 so‘m an hour', ev("mhnRate()") == 10000)
    chk('25 000 = 2 soat 30 daqiqa; 5 000 = 30 daqiqa; 10 000 = 1 soat; 50 = under a minute', ev("mhnTxt(25000)") == '⏱ ≈ 2 soat 30 daqiqa ish' and ev("mhnTxt(5000)") == '⏱ ≈ 30 daqiqa ish' and ev("mhnTxt(10000)") == '⏱ ≈ 1 soat ish' and 'kam' in ev("mhnTxt(50)"))
    chk('80 000 = 8 hours = 1 ish kuni; 120 000 = 1,5 ish kuni; with a 6-hour day 120 000 = 2 ish kuni (6 soat)', ev("mhnTxt(80000)") == '⏱ ≈ 1 ish kuni (8 soat) ish' and '1,5 ish kuni' in ev("mhnTxt(120000)") and (ev("(()=>{mhnSet('dh','6');const r=mhnTxt(120000);mhnSet('dh','');return r})()") == '⏱ ≈ 2 ish kuni (6 soat) ish'))
    ev("()=>{PV='b';K='out';render()}"); pg.wait_for_timeout(80)
    chk('the expense form shows a live line under the amount (empty until a number is typed)', pg.locator('#mhnf').count() == 1 and pg.inner_text('#mhnf').strip() == '')
    pg.fill('#app input[placeholder="Summa, so‘m"]', '25 000'); pg.wait_for_timeout(60)
    chk('typing 25 000 updates it to "≈ 2 soat 30 daqiqa ish" without re-rendering the page', '2 soat 30 daqiqa' in pg.inner_text('#mhnf') and pg.evaluate("document.activeElement&&document.activeElement.placeholder")=='Summa, so‘m')
    ev("()=>{K='in';render()}"); chk('for income (Kirim) the line is not shown', pg.locator('#mhnf').count() == 0); ev("()=>{K='out';FA='';render()}")
    pg.fill('#ptzi', 'kino 50 ming'); pg.wait_for_timeout(60)
    chk('the quick-entry preview also says "≈ 5 soat ish"', '5 soat' in pg.inner_text('#ptzp'), pg.inner_text('#ptzp'))
    ev("()=>{PV='r';render()}"); pg.wait_for_timeout(80); t = text()
    chk('Reja has the "Mehnat narxi" card with the hourly rate and examples', 'Mehnat narxi' in t and '10 000' in t and '1 soat mehnating' in t)
    ev("()=>{S.fin.mh={};S.money=[];render()}"); ev("mhnAuto()"); chk('"Kirimimdan" with no income only warns', ev("S.fin.mh.inc||0") == 0 and any('kirim' in x.lower() for x in ev("window.__t")))
    setup(money=[M(1, '2026-10-01', 'in', 3200000, 'Maosh'), M(2, '2026-10-02', 'out', 100000, 'Kino', t='k'), M(3, '2026-10-03', 'out', 50000, 'Ovqat', t='x'), M(4, '2026-10-04', 'out', 200000, 'Ovqat', t='z')], pv='r')
    ev("mhnAuto()"); chk('"Kirimimdan" fills the monthly income with the income estimate (3 200 000) → 20 000/hour', ev("S.fin.mh.inc") == 3200000 and ev("mhnRate()") == 20000)
    ev("()=>{PV='h';render()}"); pg.wait_for_timeout(80); t = text()
    chk('Hisobot: spending 350 000 ≈ 17 soat 30 daqiqa → "2,2 ish kuni"; keraksiz 100 000 ≈ 5 soat; xohish 50 000 ≈ 2 soat 30 daqiqa', 'Xarajat = mehnat' in t and '350 000' in t and 'Keraksiz: 100 000 so‘m ≈ 5 soat' in t and 'Xohish: 50 000 so‘m ≈ 2 soat 30 daqiqa' in t, t[-600:])
    ev("uiS('trk_mhn','0');render()"); chk('the old look: switching it off in Jilo hides the form line, the preview and the report', 'Xarajat = mehnat' not in text() and ev("mhnTxt(25000)") == '' and ev("mhnLine()") == '')
    ev("uiS('trk_mhn','1');tab='s';render()"); pg.wait_for_timeout(100)
    chk('the setting is listed in Sozlamalar → 🪄 Jilo va qulaylik', ev("mhnJl().includes('necha soatlik ish')"))

    # ================= 3 uslub, telefon kengligi =================
    for th, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        for pv, w in (('z', 'p'), ('h', 'p'), ('h', 'd'), ('r', 'p')):
            ev("(a)=>{document.documentElement.className=a[0];tab='p';PV=a[1];W=a[2];render()}", [th, pv, w]); pg.wait_for_timeout(60)
            chk('%s style, tab %s, wallet %s: no horizontal overflow' % (nm, pv, w), nows())
    print('\n%d passed, %d failed' % (R.ok, R.bad))
