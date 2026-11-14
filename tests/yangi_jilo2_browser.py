import os as _os; ROOT = _os.environ.get('KT_ROOT') or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
# Jilo 2: Bugun kartalari tartibi/ko'rinishi, Nafs bo'limi ikkiga bo'lingan, Bugungi Qur'on rejasi, keng ekran, sinov ro'yxati. Soat: 2026-11-09 08:00.
import sys
sys.path.insert(0, ROOT + '/tests')
from _pw import Run
BL = "[{id:'uyqu1',t:'Uxlash',s:1380,e:1800,d:[0,1,2,3,4,5,6]},{id:'k1',t:'Dokon',s:540,e:1020,d:[0,1,2,3,4,5,6]},{id:'z1',t:'Zal',s:1050,e:1110,d:[0,1,2,3,4,5,6]}]"
LIST = "[['rw','A'],['co','B'],['md','C'],['ns','D'],['ib','E'],['kc','F'],['ey','G'],['tq','H'],['km','I'],['st','J'],['rit','K'],['ap','L'],['wk','M']]"
with Run('j2', when=(2026, 11, 9, 8, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    ev("""(B)=>{window.__t=[];window.toast=m=>window.__t.push(m);window.confirm=()=>true;for(const k of ['trk_bco','trk_bch','trk_nfv','trk_qr','trk_wide','trk_swh','trk_dfmt'])localStorage.removeItem(k);localStorage.setItem('trk_swh','1');
      const q=S.q;q.tk=undefined;q.cr={};q.rd={};for(let i=0;i<114;i++)q.m[i]=0;q.m[0]=1;q.m[1]=10;q.ppd=3;q.ny={};q.sqd={};q.mzd={};S.nf=undefined;S.km=[];S.kv={};S.ib=[];S.bl=eval(B);S.done={};S.rt=undefined;S.kc={};NVS='k';SDQ='';SDO={};tab='h';BV='j';VD=null;render()}""", BL)
    pg.wait_for_timeout(120)
    keys = lambda L: [x[0] for x in L]
    pr = lambda: keys(ev("bcPrep(%s)" % LIST))
    base = ['rw', 'co', 'md', 'ns', 'ib', 'kc', 'ey', 'tq', 'km', 'st', 'rit', 'ap', 'wk']
    m = pr(); chk('morning (08:00): Takror, Nasihat, Tezkor yozuvlar, Ko‘rsatkichlar, Rejim come first; Kunni yopish, Haftalik xulosa and Imtihon yo‘li move to the end; the rest keep their order', m[:5] == ['tq', 'ns', 'ib', 'km', 'md'] and m[-3:] == ['kc', 'st', 'ey'] and [x for x in m[5:-3]] == [x for x in base if x not in ('tq', 'ns', 'ib', 'km', 'md', 'kc', 'st', 'ey')], m)
    pg.clock.set_system_time('2026-11-09T19:00:00'); m = pr(); chk('evening (19:00): Kunni yopish, Haftalik xulosa, Ko‘rsatkichlar, Tezkor yozuvlar first; Takror, Nasihat and Imtihon yo‘li go to the end', m[:4] == ['kc', 'st', 'km', 'ib'] and set(m[-3:]) == {'tq', 'ns', 'ey'}, m)
    pg.clock.set_system_time('2026-11-09T14:00:00'); chk('afternoon: the original order is kept', pr() == base, pr())
    ev("uiS('trk_bco','a')"); pg.clock.set_system_time('2026-11-09T08:00:00'); chk('“Avvalgidek” (Settings) always keeps the original order, even in the morning', pr() == base); ev("uiS('trk_bco','v')")
    ev("uiS('trk_bch','tq,ib')"); chk('hidden cards are removed from the list (Takror and Tezkor yozuvlar here)', 'tq' not in pr() and 'ib' not in pr() and len(pr()) == 11); ev("uiS('trk_bch','')")
    chk('short lists (like the first group: Hozir, ritual, 3 hours, audit) are never reordered', keys(ev("bcPrep([['hero','a'],['rt','b'],['n3','c'],['dc','d'],['qr','e']])")) == ['hero', 'rt', 'n3', 'dc', 'qr'])
    # DOM: ertalab va kechqurun
    ev("""()=>{tqGoal('bet',5);tqLog({m:'b',pa:1,pb:1,pg:2,t:'x'});S.ib=[{id:5,t:'Kitob olish',d:dk(),x:0}];kmPre(0);render()}"""); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('on the Bugun screen in the morning the Takror row comes before the quick-notes row', t.find('Takror: 2 / 5 bet') != -1 and t.find('saralanmagan yozuv') != -1 and t.find('Takror: 2 / 5 bet') < t.find('saralanmagan yozuv'), (t.find('Takror: 2 / 5'), t.find('saralanmagan yozuv')))
    pg.clock.set_system_time('2026-11-09T19:00:00'); ev("render()"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('in the evening the Kunni yopish row comes first and Takror drops below the quick notes', t.find('Kunni yopish') != -1 and t.find('Kunni yopish') < t.find('saralanmagan yozuv') < t.find('Takror: 2 / 5 bet'), (t.find('Kunni yopish'), t.find('saralanmagan yozuv'), t.find('Takror: 2 / 5')))
    pg.clock.set_system_time('2026-11-09T08:00:00')
    ev("uiS('trk_bch','tq')"); ev("render()"); pg.wait_for_timeout(80); chk('a hidden card really disappears from Bugun', 'Takror: 2 / 5 bet' not in pg.inner_text('#app')); ev("uiS('trk_bch','')")
    # sozlamalar
    ev("()=>{SDO={jl:1};tab='s';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app'); chk('Settings → Jilo has: card order (Vaqtga qarab / Avvalgidek), one chip per card to hide it, Nafs view, daily Qur‘on card and the wide-screen choice', all(x in t for x in ['Bugun kartalari tartibi', 'Vaqtga qarab', 'Avvalgidek', 'Bugun’da ko‘rinadigan kartalar', 'Nafs bo‘limi', 'Ikkiga bo‘lingan', 'Hammasi birga', 'Bugungi Qur‘on rejasi kartasi', 'Keng ekran', 'Avto']) and ev("document.querySelectorAll('#app [aria-pressed]').length") >= 20)
    ev("bcToggle('tq')"); chk('tapping a card chip hides it (remembered) and shows “Hammasini ko‘rsat”', ev("uiG('trk_bch')") == 'tq' and ev("bcHidden().has('tq')")); pg.wait_for_timeout(60); chk('…the button restores all', 'Hammasini ko‘rsat' in pg.inner_text('#app')); ev("bcAll()"); chk('…', ev("uiG('trk_bch')") == '')
    # Nafs
    ev("()=>{tab='m';MQV='n';NVS='k';render()}"); pg.wait_for_timeout(100); t = pg.inner_text('#app')
    chk('Nafs is split in two (default): 🧮 Kuzatuv (5 daqiqa, ko‘rsatkichlar, kashfiyotlar, vaqt balansi) and 🤝 Odat va nafs; the first shows only its cards', '🧮 Kuzatuv' in t and '🤝 Odat va nafs' in t and 'Mening ko‘rsatkichlarim' in t and 'Kashfiyotlar' in t and 'Vaqt balansi' in t and 'Faqat 5 daqiqa' in t and 'Nafs shartnomasi' not in t and 'Men o‘zimni sinayman' not in t)
    ev("nvsGo('o')"); pg.wait_for_timeout(80); t = pg.inner_text('#app'); chk('the second part: shartnoma, to‘siqlar, tajriba and the ritual statistics', 'Nafs shartnomasi' in t and 'To‘siqlar xaritasi' in t and 'Men o‘zimni sinayman' in t and 'Blok boshlanish marosimi' in t and 'Mening ko‘rsatkichlarim' not in t)
    ev("uiS('trk_nfv','a')"); ev("render()"); pg.wait_for_timeout(80); t = pg.inner_text('#app'); chk('“Hammasi birga (avvalgidek)” brings back the single long page without the switch', 'Nafs shartnomasi' in t and 'Mening ko‘rsatkichlarim' in t and '🧮 Kuzatuv' not in t); ev("uiS('trk_nfv','s')")
    # Qur'on rejasi
    ev("""()=>{const q=S.q,k=dk();q.ny={[k]:3};q.ppd=3;window.ssParts=()=>[{k:'q',n:'Sabqi',r:[[2,4]],p:2,done:{q:'g',p:2,r:[[2,4]],ids:[]}},{k:'m',n:'Manzil',r:[[6,9]],p:3,done:null}];S.q.tk=undefined;tqGoal('bet',5);tqLog({m:'b',pa:1,pb:1,pg:2,t:'x'});TQT='n';tqGoal('bet',3);tqLog({m:'b',pa:1,pb:1,pg:3,t:'y',w:'n'});TQT='k';tqCyStart(10);tab='q';QT='t';TKV='k';render()}""")
    pg.wait_for_timeout(100); R_ = ev("qrRows()")
    chk('the daily Qur‘on plan collects everything in one list: Sabaq (3/3 ✅), Sabqi (done ✅), Manzil (3 bet, not done), Takror (2/5), Namozda (3/3 ✅), Aylanish (today’s share)', [x['n'] for x in R_] == ['Sabaq', 'Sabqi', 'Manzil', 'Takror', 'Namozda', 'Aylanish'] and [x['ok'] for x in R_] == [True, True, False, False, True, False], [(x['n'], x['ok'], x['v']) for x in R_])
    t = pg.inner_text('#app'); chk('the card is at the top of the Takror view with a 3/6 chip and each row showing its numbers', '📖 Bugungi Qur‘on rejasi' in t and '3/6' in t and '3 / 3 bet' in t and '2 / 5 bet' in t)
    ev("()=>{document.querySelector('#app section[aria-label=\"Bugungi Qur‘on rejasi\"] button[aria-label=\"Manzil\"]').click()}"); pg.wait_for_timeout(80); chk('tapping Manzil opens the Sabqi · Manzil screen', ev("tab") == 'q' and ev("TKV") == 's')
    ev("()=>{tab='h';BV='j';render()}"); pg.wait_for_timeout(100); chk('the same card is on Bugun right after the Hozir card/3 hours/audit', '📖 Bugungi Qur‘on rejasi' in pg.inner_text('#app'))
    ev("uiS('trk_qr','0')"); ev("render()"); pg.wait_for_timeout(60); chk('it can be switched off in Settings', '📖 Bugungi Qur‘on rejasi' not in pg.inner_text('#app')); ev("uiS('trk_qr','1')")
    ev("()=>{for(const i in S.q.m)S.q.m[i]=0;S.q.tk=undefined;window.ssParts=()=>[];S.q.ppd=0;render()}"); chk('with nothing to do (no memorised parts, no goals) the card is not shown at all', ev("qrCard()") == '')
    # keng ekran
    chk('phone width: the wide layout is off by default', ev("wideOn()") is False and ev("document.documentElement.classList.contains('wide')") is False)
    pg.set_viewport_size({'width': 1280, 'height': 800}); pg.wait_for_timeout(150); chk('a computer window (≥ 1000 px) switches the wide layout on automatically (“Avto”)', ev("wideOn()") is True and ev("document.documentElement.classList.contains('wide')") is True)
    ev("wideSet('0')"); chk('“O‘chirilgan” keeps the narrow column even on a big window', ev("wideOn()") is False and ev("document.documentElement.classList.contains('wide')") is False)
    pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(100); ev("wideSet('1')"); chk('“Yoqilgan” forces it on a phone too', ev("document.documentElement.classList.contains('wide')") is True); ev("wideSet('a')"); chk('back to “Avto”', ev("document.documentElement.classList.contains('wide')") is False)
    # sinov ro'yxati
    ev("()=>{localStorage.removeItem('trk_qa');tab='s';SDO={xj:1};render();document.querySelectorAll('#app details').forEach(d=>d.open=true)}"); pg.wait_for_timeout(80); chk('the iPhone checklist now covers the new features (22 items) and the report includes the self-check warnings', ev("XJQ.length") == 22 and '0 ✅ · 0 ❌ / 22' in pg.inner_text('#app').replace('\n', ' '))
    ev("()=>{TS_R=[{n:'Bildirishnoma ruxsati',ok:false,d:'holat: default'},{n:'Xotira',ok:true,d:''}]}"); chk('…', 'Tizim tekshiruvi: 1 ta ogohlantirish' in ev("xjReport()") and '⚠️ Bildirishnoma ruxsati: holat: default' in ev("xjReport()"))
    bad = []
    ev("()=>{S.q.m[1]=10;S.q.m[0]=1;S.q.ppd=3;window.ssParts=()=>[{k:'m',n:'Manzil',r:[[6,9]],p:3,done:null}];S.q.tk=undefined;tqGoal('bet',5);tqLog({m:'b',pa:1,pb:1,pg:2,t:'x'});kmPre(0);S.ib=[{id:5,t:'Uzun yozuv '.repeat(6),d:dk(),x:0}]}")
    for ui in ('1', '2', '3'):
        for th in ('light', 'dark'):
            ev("(a)=>{uiS('trk_ui',a[0]);dzApply();document.documentElement.dataset.theme=a[1];SDO={jl:1};tab='s';render()}", [ui, th]); pg.wait_for_timeout(70); ok1 = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            ev("()=>{tab='m';MQV='n';NVS='o';render()}"); pg.wait_for_timeout(50); ok2 = ev("document.documentElement.scrollWidth<=window.innerWidth+1"); ev("()=>{NVS='k';tab='h';BV='j';render()}"); pg.wait_for_timeout(50); ok3 = ev("document.documentElement.scrollWidth<=window.innerWidth+1")
            if not (ok1 and ok2 and ok3): bad.append(ui + th)
    chk('Settings with all the new choices, both Nafs halves and Bugun with the Qur‘on plan fit the phone in all three styles, light and dark', not bad, bad)
    ev("()=>{uiS('trk_ui','1');dzApply();document.documentElement.dataset.theme='light'}")
