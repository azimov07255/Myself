# Pul: matn bilan tez kiritish ("taksi 15 ming"). Soat: 2026-10-10 (shanba) 10:00.
import sys
sys.path.insert(0, '/mnt/user-data/outputs/tests')
from _pw import Run
with Run('pul_tez') as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-10-10T10:00:00')
    ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);S.money=[];S.debts=[];S.fin={open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[]};W='p';PV='b';K='out';tab='p';PTZ='';render()}""")
    P = lambda s: ev("(s)=>ptzParse(s)", s)
    # ---------- summa ----------
    chk('"taksi 15 ming" = 15 000', P('taksi 15 ming')['a'] == 15000)
    chk('"15k" and "15 k" = 15 000', P('taksi 15k')['a'] == 15000 and P('taksi 15 k')['a'] == 15000)
    chk('"tushlik 32000" = 32 000 and "32 000" with a space is also 32 000', P('tushlik 32000')['a'] == 32000 and P('tushlik 32 000')['a'] == 32000)
    chk('"1 500 000" with two spaces = 1 500 000', P('kiyim 1 500 000')['a'] == 1500000)
    chk('"maosh 3 mln" = 3 000 000 and "1.5 mln" = 1 500 000 and "2 million" = 2 000 000', P('maosh 3 mln')['a'] == 3000000 and P('maosh 1.5 mln')['a'] == 1500000 and P('maosh 2 million')['a'] == 2000000)
    chk('"15.000" is fifteen thousand (a thousands dot), not 15', P('non 15.000')['a'] == 15000)
    chk('"2 ta non 5000": the amount is the larger number (5000), "2 ta non" stays in the note', P('2 ta non 5000')['a'] == 5000 and '2 ta non' in P('2 ta non 5000')['n'].lower())
    chk('text without any number is not understood', P('taksi')['ok'] is False and P('')['ok'] is False)
    chk('"5kg guruch" is not an amount (no number is left)', P('guruch kg')['ok'] is False)
    # ---------- kategoriya ----------
    cat = lambda s: P(s)['c']
    chk('taksi / yandex / benzin → Transport', all(cat(x) == 'Transport' for x in ['taksi 15 ming', 'yandex 12000', 'benzin 200 ming']))
    chk('tushlik / lavash / non / choy → Ovqat', all(cat(x) == 'Ovqat' for x in ['tushlik 30000', 'lavash 25 ming', 'non 5000', 'choy 8000']))
    chk('Uzbek endings work: "taksiga 15 ming", "ovqatga 40000", "nonga 5000"', cat('taksiga 15 ming') == 'Transport' and cat('ovqatga 40000') == 'Ovqat' and cat('nonga 5000') == 'Ovqat')
    chk('apostrophe variants: "go‘sht 90 ming" and "go\'sht 90 ming" → Ovqat', cat('go‘sht 90 ming') == 'Ovqat' and cat("go'sht 90 ming") == 'Ovqat')
    chk('kitob/kurs → O‘qish; dori → Salomatlik; kino → Ko‘ngil ochish; internet → Aloqa; ijara → Uy-joy; sadaqa → Sadaqa',
        [cat('kitob 80 ming'), cat('dori 40000'), cat('kino 50 ming'), cat('internet 100 ming'), cat('ijara 1 mln'), cat('sadaqa 20 ming')] == ['O‘qish', 'Salomatlik', 'Ko‘ngil ochish', 'Aloqa', 'Uy-joy', 'Sadaqa'])
    chk('"uyqu" is NOT matched as a housing word; an unknown word is "Boshqa"', cat('uyqu dori 1000') == 'Salomatlik' and cat('qwerty 1000') == 'Boshqa' and cat('uyqu 1000') == 'Boshqa')
    # ---------- hisob, sana, kirim ----------
    chk('"karta" / "kartadan" → card; nothing or "naqd" → cash; the account word is not left in the note', P('tushlik 32000 karta')['ac'] == 'card' and P('kartadan taksi 10 ming')['ac'] == 'card' and P('tushlik 32000')['ac'] == 'cash' and P('tushlik 32000 naqd')['ac'] == 'cash' and 'karta' not in P('tushlik 32000 karta')['n'].lower())
    chk('"kecha" = yesterday (2026-10-09); without it today (2026-10-10)', P('kecha kitob 80 ming')['d'] == '2026-10-09' and P('kitob 80 ming')['d'] == '2026-10-10')
    r = P('maosh 3 mln karta')
    chk('"maosh 3 mln karta" = income, Maosh, card, 3 000 000', r['k'] == 'in' and r['c'] == 'Maosh' and r['ac'] == 'card' and r['a'] == 3000000, r)
    chk('"sovg‘a 200 ming" = income, Sovg‘a; "xarajat" keeps it an expense', P('sovg‘a 200 ming')['k'] == 'in' and P('sovg‘a 200 ming')['c'] == 'Sovg‘a' and P('sovga uchun xarajat 200 ming')['k'] == 'out')
    chk('"berdim" makes it an expense even with "sovga"', P('sovga berdim 100 ming')['k'] == 'out')
    chk('in the shop wallet income goes to "Dokon daromadi"', ev("()=>{W='d';const r=ptzParse('savdo 1 mln');W='p';return r.c}") == 'Dokon daromadi')
    # ---------- ekran ----------
    ev("()=>{PV='b';render()}"); pg.wait_for_timeout(100)
    chk('the Pul home shows the "Tez yozish" card with an input and the Yozish button', pg.locator('#ptzi').count() == 1 and 'Tez yozish' in pg.inner_text('#app'))
    y_in = pg.evaluate("document.getElementById('ptzi').getBoundingClientRect().top"); y_form = pg.evaluate("[...document.querySelectorAll('#app b')].find(b=>/Yangi yozuv/.test(b.textContent)).getBoundingClientRect().top")
    chk('the quick box is ABOVE the long form', y_in < y_form, (y_in, y_form))
    pg.fill('#ptzi', 'taksi 15 ming'); pg.wait_for_timeout(50)
    pv = pg.inner_text('#ptzp')
    chk('typing shows a live preview of what was understood (expense, Transport, 15 000, cash)', 'Chiqim' in pv and 'Transport' in pv and '15' in pv and 'Naqd' in pv, pv)
    chk('typing does NOT re-render the page (the input keeps focus and text)', pg.evaluate("document.activeElement&&document.activeElement.id")=='ptzi' and pg.input_value('#ptzi') == 'taksi 15 ming')
    pg.fill('#ptzi', 'salom'); pg.wait_for_timeout(50)
    chk('an unclear text says it could not find the amount', 'topolmadim' in pg.inner_text('#ptzp'))
    pg.click('#app button >> text="Yozish"'); pg.wait_for_timeout(100)
    chk('saving unclear text writes nothing and tells why', ev("S.money.length") == 0 and any('topolmadim' in t for t in ev("window.__t")))
    pg.fill('#ptzi', 'taksi 15 ming'); pg.press('#ptzi', 'Enter'); pg.wait_for_timeout(150)
    m = ev("S.money")
    chk('Enter saves the entry: out, 15 000, Transport, cash, today, personal', len(m) == 1 and m[0]['k'] == 'out' and m[0]['a'] == 15000 and m[0]['c'] == 'Transport' and m[0]['ac'] == 'cash' and m[0]['d'] == '2026-10-10' and m[0]['w'] == 'p', m)
    chk('the box is cleared after saving and the balance dropped by 15 000', pg.input_value('#ptzi') == '' and ev("bal('p').tot") == -15000)
    pg.fill('#ptzi', 'maosh 3 mln karta'); pg.click('#app button >> text="Yozish"'); pg.wait_for_timeout(150)
    chk('income saved to the card: balance 2 985 000 (card 3 000 000, cash −15 000)', ev("bal('p').card") == 3000000 and ev("bal('p').cash") == -15000 and ev("S.money.filter(m=>m.k==='in').length") == 1)
    pg.fill('#ptzi', 'kecha kitob 80 ming karta'); pg.click('#app button >> text="Yozish"'); pg.wait_for_timeout(150)
    e = ev("S.money.find(m=>m.c==='O‘qish')"); chk('"kecha kitob 80 ming karta" is dated yesterday, O‘qish, card', e and e['d'] == '2026-10-09' and e['ac'] == 'card' and e['a'] == 80000, e)
    # budjet ogohlantirishi ishlaydi
    ev("()=>{S.fin.cb={p:{'Ovqat':50000}};PTZ='';render()}"); pg.fill('#ptzi', 'tushlik 60000'); pg.press('#ptzi', 'Enter'); pg.wait_for_timeout(150)
    chk('a category budget (50 000) is still checked when saving by text (a warning toast)', any(('byudjet' in t.lower() or 'limit' in t.lower() or 'oshdi' in t.lower()) for t in ev("window.__t")), ev("window.__t"))
    # formaga o'tkazish
    ev("()=>{PTZ='';render()}"); pg.fill('#ptzi', 'sadaqa 25 ming karta'); pg.click('#app button >> text="Formada tahrirlash"'); pg.wait_for_timeout(150)
    chk('"Formada tahrirlash" opens the normal form filled in (amount, card, Sadaqa) and saves nothing yet', ev("FA") == '25000' and ev("FACC") == 'card' and ev("CATS[FC]") == 'Sadaqa' and ev("S.money.filter(m=>m.c==='Sadaqa').length") == 0, (ev("FA"), ev("FACC")))
    ev("()=>{FA='';FN='';FD='';EID=0;render()}")
    # jilo sozlamasi
    ev("()=>{uiS('trk_ptz','0');render()}"); chk('the old look is available: Sozlamalar → Jilo can hide the quick box', pg.locator('#ptzi').count() == 0)
    ev("()=>{uiS('trk_ptz','1');tab='s';render()}"); pg.wait_for_timeout(100)
    chk('...and the setting is listed in Sozlamalar → 🪄 Jilo va qulaylik', 'tez yozish oynasi' in pg.inner_text('#app').lower() or ev("jlCard&&ptzJl().includes('tez yozish')"))
    # shop wallet
    ev("()=>{tab='p';PV='b';W='d';render()}"); pg.wait_for_timeout(100)
    pg.fill('#ptzi', 'savdo 2 mln'); pg.press('#ptzi', 'Enter'); pg.wait_for_timeout(150)
    s = ev("S.money.find(m=>m.w==='d')"); chk('in the shop wallet the entry belongs to the shop', s and s['w'] == 'd' and s['c'] == 'Dokon daromadi' and s['a'] == 2000000, s)
    # 390 px da toshib ketmaydi
    ev("()=>{W='p';render()}"); pg.wait_for_timeout(100)
    chk('no horizontal overflow at phone width', pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    for th, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        ev("(c)=>{document.documentElement.className=c;render()}", th); pg.wait_for_timeout(80)
        chk(nm + ' style: quick box is visible and fits the screen', pg.evaluate("(()=>{const e=document.getElementById('ptzi');if(!e)return false;const r=e.getBoundingClientRect();return r.width>100&&r.right<=window.innerWidth})()"))
    print('\n%d passed, %d failed' % (R.ok, R.bad))
