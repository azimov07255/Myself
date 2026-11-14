import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Pul nazorati: hozirgi qoldiq, kunlik chegara, erkin pul, xarajat turi, xohish ro'yxati; haftalik sharh tugmasi; yangiliklar. Soat: 2026-10-10 (shanba) 10:00.
import sys, json, re
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
digits = lambda s: int(re.sub(r'[^\d-]', '', s) or 0)
def M(i, d, k, a, c='Ovqat', n='', w='p', ac='cash', t=None):
    x = {'id': i, 'd': d, 'k': k, 'a': a, 'c': c, 'n': n, 'w': w, 'ac': ac}
    if t: x['t'] = t
    return x
with Run('pul2') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-10-10T10:00:00')
    ev("""(L)=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);S.money=L;S.debts=[];S.fin={open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[]};W='p';PV='r';PF={mo:0,ac:'all',k:'all',q:''};tab='p';render()}""",
       [M(1, '2026-10-05', 'in', 1000000, 'Maosh'), M(2, '2026-10-06', 'out', 200000)])
    chk('baseline: opening 0 + income 1 000 000 − expense 200 000 = 800 000 cash', ev("bal('p').cash") == 800000 and ev("bal('p').card") == 0)
    ev("setCur('cash','1 500 000')"); b = ev("bal('p')")
    chk('typing the CURRENT cash 1 500 000 makes the main balance exactly 1 500 000 (it is not added on top)', b['cash'] == 1500000 and ev("S.fin.open.p.cash") == 700000 and len(ev("S.money")) == 2, b)
    ev("setCur('card','250000')"); chk('the card is separate: 250 000; total 1 750 000', ev("bal('p').card") == 250000 and ev("bal('p').tot") == 1750000)
    ev("setCur('cash','1500000')"); chk('typing the same number again changes nothing', ev("S.fin.open.p.cash") == 700000 and ev("bal('p').cash") == 1500000)
    ev("S.money.push({id:9,d:'2026-10-09',k:'out',a:100000,c:'Ovqat',n:'',w:'p',ac:'cash'})"); chk('a later expense lowers the balance by its amount (1 400 000)', ev("bal('p').cash") == 1400000)
    ev("setCur('cash','-50000')"); chk('a negative balance (overdraft) can be entered', ev("bal('p').cash") == -50000)
    ev("setCur('cash','1400000')"); ev("S.debts.push({id:1,k:'borrow',a:300000,ac:'cash',pay:[],st:'open',t:'Qarz',d:'2026-10-01'})"); ev("setCur('cash','2000000')"); chk('with a debt in the ledger the balance still equals the typed number', ev("bal('p').cash") == 2000000); ev("S.debts=[]"); ev("setCur('cash','1400000')")
    ev("()=>{W='d';setCur('cash','77777')}"); chk('the shop wallet has its own balance; the personal one is untouched', ev("bal('d').cash") == 77777 and ev("bal('p').cash") == 1400000 and ev("S.fin.open.d.cash") == 77777); ev("W='p'")
    ev("()=>{S.fin.sg=[{id:1,t:'Noutbuk',a:1000000,s:400000}];PV='r';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('Reja shows "Hozirgi qoldiq" prefilled with the real balances, a note that it matches the home screen, and that savings goals are NOT taken from the balance', 'Hozirgi qoldiq (shaxsiy)' in t and 'Boshlang‘ich qoldiq' not in t and 'ustiga qo‘shilmaydi' in t and 'balansdan ayrilmaydi' in t and ev("document.querySelectorAll('#app input[onchange^=\"setCur\"]')[0].value") == '1400000' and ev("document.querySelectorAll('#app input[onchange^=\"setCur\"]')[1].value") == '250000')
    ev("sgPut(1)") if False else None; b0 = ev("bal('p').tot"); ev("()=>{S.fin.sg[0].s+=100000;save()}"); chk('adding money to a savings goal does not change the main balance', ev("bal('p').tot") == b0)
    pg.fill('#app input[onchange^="setCur"] >> nth=0', '3 000 000'); pg.press('#app input[onchange^="setCur"] >> nth=0', 'Tab'); pg.wait_for_timeout(100)
    ev("()=>{PV='b';render()}"); pg.wait_for_timeout(100); hero = digits(pg.inner_text('#app .hero h1')); chk('after typing it in Reja, the "Umumiy balans" on the Pul home is cash 3 000 000 + card 250 000 = 3 250 000', hero == 3250000 and ev("bal('p').cash") == 3000000, hero)
    # ---------- kunlik chegara ----------
    ev("""(L)=>{S.money=L;S.fin.budget=3100000;S.fin.sg=[{id:1,t:'X',a:1000000,s:1200000}];S.fin.open.p={cash:0,card:0};PV='b';render()}""", [M(1, '2026-10-03', 'in', 5000000, 'Maosh'), M(2, '2026-10-03', 'out', 300000), M(3, '2026-10-10', 'out', 50000), M(4, '2026-09-12', 'out', 3000000)])
    D = ev("pDaily()"); chk('on the 10th with a 3 100 000 budget: spent 350 000 → left 2 750 000 over 22 days = 125 000 a day; today 50 000 → 75 000 more', D['lim'] == 125000 and D['sp'] == 50000 and D['left'] == 75000 and 'byudjet' in D['src'], D)
    t = pg.inner_text('#app'); chk('the Pul home shows the card: "Bugun yana 75 000 so‘m sarflasang bo‘ladi" with a progress bar', 'Bugungi xarajat chegarasi' in t and '75000' in t.replace('\xa0', '').replace(' ', '') and 'sarflasang bo‘ladi' in t and ev("document.querySelectorAll('#app .goal .usb i').length") >= 1)
    chk('free money = balance − savings goals (4 650 000 + ... ) is shown and never negative', ev("pDaily().free") == max(0, ev("bal('p').tot") - 1200000) and 'Erkin pul' in t)
    ev("S.money.push({id:5,d:'2026-10-10',k:'out',a:200000,c:'Ovqat',n:'',w:'p',ac:'cash'});render()"); D = ev("pDaily()"); chk('when today\u2019s spending passes the limit the card says by how much', D['left'] == -125000 + 0 or D['left'] < 0, D); chk('...and warns in words', 'oshdi' in pg.inner_text('#app') and 'boshqa xarajat qilmaslikka' in pg.inner_text('#app'))
    ev("()=>{S.fin.budget=0;S.money=S.money.filter(m=>m.id!==5);render()}"); D = ev("pDaily()"); chk('without a budget it uses last month\u2019s average (3 000 000 / 30 = 100 000 a day)', D['lim'] == 100000 and 'o‘tgan oy' in D['src'])
    ev("()=>{S.money=[];render()}"); chk('with no data at all it explains how to get a limit', 'Chegara hisoblanmadi' in pg.inner_text('#app'))
    ev("()=>{W='d';render()}"); chk('the shop wallet has no free-money line', 'Erkin pul' not in pg.inner_text('#app')); ev("()=>{W='p';render()}")
    # ---------- xarajat turi ----------
    ev("()=>{S.money=[];K='out';FT='';FA='';FN='';render()}"); chk('the expense form has the type chips (not set, zarur, xohish, keraksiz) above it', ev("[...document.querySelectorAll('#app .chips button')].map(b=>b.textContent.trim()).filter(x=>/Zarur|Xohish|Keraksiz|Belgilanmagan/.test(x))") == ['Belgilanmagan', '🟢 Zarur', '🟡 Xohish', '🔴 Keraksiz'])
    pg.click('#app .chips button >> text=Keraksiz'); chk('choosing a type highlights it', ev("FT") == 'k' and ev("document.querySelector('#app .chips button.on').textContent").endswith('Keraksiz'))
    ev("()=>{FA='45 000';FN='Chips va cola';FC=0;FACC='cash';FD='';EID=0;addM()}"); e = ev("S.money[S.money.length-1]"); chk('the expense is saved with its type; the type resets for the next entry', e['t'] == 'k' and e['a'] == 45000 and ev("FT") == '' and e['n'] == 'Chips va cola')
    ev("()=>{K='out';FA='20000';FN='Non';FC=0;FACC='cash';FT='z';addM();FA='30000';FN='Kino';FT='x';addM();FA='';FT='';FN=''}"); ev("()=>{K='in';FA='500000';FN='Stipendiya';FC=0;FT='k';addM();K='out'}"); inc = ev("S.money.filter(m=>m.k==='in').slice(-1)[0]"); chk('income never gets a type, even if one was selected', 't' not in inc or inc['t'] is None)
    ev("pEdit(S.money[0].id)"); chk('editing an entry loads its type back into the chips', ev("FT") == 'k'); ev("pCancel()")
    ev("()=>{S.money.push({id:77,d:dk(),k:'out',a:10000,c:'Ovqat',n:'Eski',w:'p',ac:'cash'});PV='h';PF.mo=0;render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); tr = t.replace('\xa0', '').replace(' ', '')
    chk('the report splits the month by type: keraksiz 45 000, zarur 20 000, xohish 30 000, unmarked 10 000 (shares of the marked ones: 47%, 21%, 32%)', 'Xarajat turlari' in t and '45000·47%' in tr and '20000·21%' in tr and '30000·32%' in tr and 'Belgilanmagan:10000' in tr, tr[:400])
    chk('and says how much was wasted with the biggest items', 'Keraksiz xarajat: 45' in t.replace('\xa0', ' ').replace('  ', ' ') or '45000' in tr and 'Shuncha pul jamg‘armaga' in t and 'Chips va cola' in t)
    ev("()=>{S.money=[M0];render()}".replace('M0', json.dumps(M(1, '2026-10-02', 'out', 5000)))); chk('with no marked expenses it explains how to use the types', 'belgilasang' in pg.inner_text('#app'))
    ev("()=>{S.money=[{id:1,d:'2026-10-02',k:'out',a:5000,c:'Ovqat',n:'Tushlik, \"katta\"',w:'p',ac:'cash',t:'k'}]}"); csv = ev("pCsvText(1)"); chk('the CSV has an "Xarajat turi" column (Keraksiz / Xohish / Zarur)', '"Xarajat turi"' in csv.split('\r\n')[0] and csv.split('\r\n')[1].endswith('"Keraksiz"'))
    # ---------- xohish ro'yxati ----------
    ev("()=>{S.fin.wl=[];S.fin.wlSaved=0;S.money=[];PV='b';render()}"); ev("__t=[]"); ev("wlAdd()"); chk('an item without a name or price is refused', len(ev("S.fin.wl")) == 0 and any('Nomi va narxini' in x for x in ev("__t")))
    ev("document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('Xohish ro‘yxati'))d.open=true})"); pg.fill('#wlt', 'Yangi quloqchin'); pg.fill('#wla', '450000'); pg.click('#app details button >> text="+"'); pg.wait_for_timeout(100)
    chk('an item is added with the time and shows a 24-hour countdown; "Olaman" is disabled while waiting', len(ev("S.fin.wl")) == 1 and ev("S.fin.wl[0].a") == 450000 and '⏳ 24 soat' in pg.inner_text('#app') and ev("[...document.querySelectorAll('#app button')].find(b=>b.textContent==='Olaman').disabled"))
    ev("__t=[]"); ev("wlBuy(S.fin.wl[0].id)"); chk('buying early is refused with the time left and the item stays', len(ev("S.fin.wl")) == 1 and any('kut' in x for x in ev("__t")))
    pg.clock.set_system_time('2026-10-11T11:00:00'); ev("render()"); pg.wait_for_timeout(100); chk('after 24 hours it asks "hali ham kerakmi?" and "Olaman" is enabled', '24 soat o‘tdi' in pg.inner_text('#app') and not ev("[...document.querySelectorAll('#app button')].find(b=>b.textContent==='Olaman').disabled"))
    ev("wlNo(S.fin.wl[0].id)"); chk('"Kerak emas" removes it, adds its price to "tejading" and congratulates', len(ev("S.fin.wl")) == 0 and ev("S.fin.wlSaved") == 450000 and any('Tejading' in x for x in ev("__t"))); ev("render()"); chk('the saved total is shown', '450' in pg.inner_text('#app').replace('\xa0', '').replace(' ', '') and 'tejaldi' in pg.inner_text('#app').lower())
    ev("()=>{S.fin.wl=[{id:5,t:'Soat',a:300000,at:Date.now()-90000000}];K='in';FA='';FN='';FT='';wlBuy(5)}"); chk('"Olaman" fills the expense form (type xohish, the name and price) for confirmation and removes the item', ev("K") == 'out' and ev("FA") == '300000' and ev("FN") == 'Soat' and ev("FT") == 'x' and len(ev("S.fin.wl")) == 0)
    ev("()=>{W='d';render()}"); chk('the wishlist is only for the personal wallet', 'Xohish ro‘yxati' not in pg.inner_text('#app')); ev("W='p'")
    # ---------- haftalik sharh tugmasi ----------
    pg.clock.set_system_time('2026-11-02T10:00:00'); ev("()=>{window.__sc=0;Element.prototype.scrollIntoView=function(){window.__sc++;window.__scid=this.id};S.wrd='';S.hab=[];tab='h';BV='j';render()}"); pg.wait_for_timeout(100)
    chk('Monday: the "Haftalik sharh tayyor" banner is on the Bugun screen', 'Haftalik sharh tayyor' in pg.inner_text('#app'))
    pg.click('#app >> text=Ko‘rish'); pg.wait_for_timeout(300); chk('"Ko‘rish" switches to Tahlil AND scrolls to the review card (before, nothing seemed to happen because the card was far below)', ev("BV") == 't' and ev("!!document.getElementById('wrc')") and ev("__sc") >= 1 and ev("__scid") == 'wrc')
    # ---------- yangiliklar ----------
    ev("()=>{tab='s';render()}"); ev("document.querySelectorAll('#app details').forEach(d=>{if(d.textContent.includes('Yangiliklar'))d.open=true})"); pg.wait_for_timeout(60); t = pg.inner_text('#app')
    chk('Sozlama has "Yangiliklar va qo‘llanma" listing the new features by section with where to find each', 'Yangiliklar va qo‘llanma' in t and all(s in t for s in ['Pul nazorati', 'Odatlar', 'Bugun', 'Maqsad', 'IELTS', 'Tizim', 'Hozirgi qoldiq', 'Xohish ro‘yxati', 'Haftalik sharh', 'Vidjet', 'Hayot paneli']) and ev("NEWS.reduce((a,g)=>a+g[1].length,0)") >= 20)
