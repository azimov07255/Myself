# Pul markazi: sog'liq balli, kunlik xulosa, doim ko'rinadigan tanga minorasi, tejash tahlilchisi, chellenj, biznes markazi, yutuqlar. Soat: 2026-11-16 (dushanba) 10:00.
import sys, os
sys.path.insert(0, os.environ.get('KT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tests')
from _pw import Run
with Run('pul_markaz', when=(2026, 11, 16, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-11-16T10:00:00')
    text = lambda: pg.inner_text('#app').replace('\xa0', ' ')
    def base(extra=''):
        ev("""()=>{localStorage.removeItem('trk_3d');localStorage.removeItem('trk_ptb');dzApply();window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);
          S.money=[];S.debts=[];S.fin={open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[],wr:[]};W='p';PV='b';tab='p';PMZB=[];render()}""")
        if extra: ev(extra)
        pg.wait_for_timeout(120)
    # ---------- 1. bo'sh holat: minora doim ko'rinadi ----------
    base()
    chk('Pul Bosh with NO goal still shows the 3D coin tower (empty) plus a goal form', pg.locator('.d3coins').count() == 1 and pg.locator('#pmu').count() == 1 and pg.locator('#pmr').count() == 1)
    chk('the briefing card is on top and the health card asks for data', pg.locator('.pmzbr').count() == 1 and 'Moliyaviy sog' in text())
    chk('no health score with no entries', ev("pmzHealth()") is None)
    pg.fill('#pmu', '1000'); pg.fill('#pmr', '12000'); ev("pmzGoalQuick()"); pg.wait_for_timeout(150)
    g = ev("S.fin.sg.find(x=>x.usd)")
    chk('the quick form creates the dollar goal (1000$ x 12000 = 12 000 000)', g and g['a'] == 12000000 and g['usd'] == 1000, g)
    chk('...and the tower now shows that goal (0%)', pg.locator('.d3coins').count() == 1 and pg.locator('#pmu').count() == 0 and '0%' in pg.inner_text('.d3coins'))
    ev("()=>{S.fin.sg=[];S.fin.pl={};uiS('trk_3d','0');render()}"); pg.wait_for_timeout(100)
    chk('with 3D turned off the empty state is a simple goal card (no tower)', pg.locator('.d3coins').count() == 0 and pg.locator('#pmu').count() == 1)
    # ---------- 2. sog'liq balli ----------
    base("""()=>{S.fin.sg=[{id:1,t:'Maqsad: $500',a:6000000,s:3000000,e:'💎',dl:'',h:[],cr:'2026-11-01',usd:500}];S.fin.pl={usd:500,rate:12000,pc:30};S.fin.dl={p:{m:'m',v:100000}};
      S.money=[{id:11,d:'2026-11-10',k:'in',a:3000000,c:'Maosh',n:'',w:'p',ac:'cash'},{id:12,d:'2026-11-10',k:'out',a:600000,c:'Ovqat',n:'',w:'p',ac:'cash'},{id:13,d:'2026-11-12',k:'out',a:400000,c:'Transport',n:'',w:'p',ac:'cash',t:'k'}];render()}""")
    H = ev("pmzHealth()")
    p = {x['k']: round(x['v'], 1) for x in H['parts']}
    chk('score parts: savings 25, cushion 25, budget 17.1 (12/14 days), no-spend 15, unnecessary 0', p == {'sav': 25, 'cus': 25, 'bud': 17.1, 'nos': 15, 'unn': 0}, p)
    chk('total score is 82 and the label is A‘lo', H['total'] == 82 and H['label'] == 'A‘lo', H['total'])
    chk('weakest part is the unnecessary-spending one', H['weak']['k'] == 'unn')
    t = text()
    chk('Bosh shows "Sog‘liq 82 / 100", tower with 50%, and a daily-limit line', 'Sog‘liq 82' in t and '50%' in t and 'chegara' in t.lower())
    chk('"today can still spend" shows the full limit (100 000) when nothing is spent today', '100 000' in t.replace(' ', ' '), t[:300])
    ev("()=>{S.money.push({id:14,d:'2026-11-16',k:'out',a:130000,c:'Ovqat',n:'',w:'p',ac:'cash'});render()}"); pg.wait_for_timeout(80)
    chk('overspending today is stated ("chegaradan 30 000 oshdi")', 'oshdi' in text() and '30 000' in text().replace(' ', ' '))
    ev("()=>{S.money.pop();S.fin.dl={p:{m:'a'}};render()}")
    chk('without a manual limit nothing crashes and the score still exists', ev("typeof pmzHealth().total")=='number')
    # ---------- 3. yutuqlar ----------
    ev("()=>{S.fin.dl={p:{m:'m',v:100000}};S.fin.mil={};PMZB=[];render()}"); pg.wait_for_timeout(120)
    mil = ev("Object.keys(S.fin.mil).sort()")
    chk('medals earned: first saving, 25%, 50%, 3 no-spend days, health 80+', mil == ['g25', 'g50', 'h80', 'n3', 's1'], mil)
    chk('a congratulation banner with confetti is shown for new medals', pg.locator('.pmzban').count() == 1 and 'Yangi yutuq' in text())
    chk('the medals grid shows 9 medals and "5 / 9"', pg.locator('.pmzm').count() == 9 and '5 / 9' in text())
    pg.evaluate("pmzBannerOk()"); pg.wait_for_timeout(100)
    chk('the banner is dismissed and does not come back on re-render', pg.locator('.pmzban').count() == 0)
    ev("render()"); pg.wait_for_timeout(60)
    chk('...also after another render', pg.locator('.pmzban').count() == 0)
    # ---------- 4. tejash tahlilchisi ----------
    base("""()=>{S.fin.dl={p:{m:'m',v:100000}};const o=[{d:'2026-11-10',a:600000,c:'Ovqat'},{d:'2026-10-01',a:300000,c:'Ovqat'}];for(let i=0;i<10;i++)o.push({d:'2026-11-0'+(i%9+1),a:10000,c:'Boshqa'});
      S.money=o.map((x,i)=>({id:100+i,d:x.d,k:'out',a:x.a,c:x.c,n:'',w:'p',ac:'cash'}));PV='h';render()}""")
    L = ev("pmzLeaks()")
    chk('leaks: Ovqat grew +100%, small spends 10 pcs = 100 000', L and L['cats'][0]['c'] == 'Ovqat' and L['cats'][0]['ch'] == 100 and L['small']['n'] == 10 and L['small']['sum'] == 100000, L and L['small'])
    chk('potential saving = 120 000 (20% of Ovqat) + 50 000 (half of small) = 170 000', L['pot'] == 170000, L['pot'])
    t = text()
    chk('Hisobot shows "Qayerda pul oqyapti?" with tips and the potential saving', 'Qayerda pul oqyapti' in t and '170 000' in t.replace(' ', ' ') and 'Maslahatlar' in t)
    ev("()=>{S.money=S.money.slice(0,3);render()}")
    chk('fewer than 5 spends: a friendly "tahlil chiqadi" message instead of numbers', ev("pmzLeaks()") is None and 'tahlil chiqadi' in text())
    # ---------- 5. chellenj ----------
    chk('before starting: a Start button is shown', pg.locator('button:text-is("Chellenjni boshlash")').count() == 1)
    ev("pmzChStart()"); pg.wait_for_timeout(100)
    I = ev("pmzChInfo()")
    chk('started today: 7 dots, today is "t", the rest future, nothing counted yet', len(I['dots']) == 7 and I['dots'][0]['s'] == 't' and I['dots'][1]['s'] == 'f' and I['ns'] == 0 and not I['done'])
    ev("""()=>{S.fin.ch={start:'2026-11-09',n:7,need:3};S.fin.dl={p:{m:'m',v:100000}};S.money=[{id:1,d:'2026-11-10',k:'out',a:600000,c:'Ovqat',n:'',w:'p',ac:'cash'},{id:2,d:'2026-11-12',k:'out',a:50000,c:'Ovqat',n:'',w:'p',ac:'cash'}];render()}""")
    I = ev("pmzChInfo()")
    chk('a finished week: 11-10 over limit (x), 11-12 within (o), 5 days with no spend → won', [d['s'] for d in I['dots']] == ['n', 'x', 'n', 'o', 'n', 'n', 'n'] and I['ns'] == 5 and I['done'] and I['win'], [d['s'] for d in I['dots']])
    ev("()=>{S.money=[];PV='b';render()}"); pg.wait_for_timeout(80)
    ev("pmzChStop()"); chk('stopping clears the challenge', ev("S.fin.ch") is None)
    # ---------- 6. biznes markazi ----------
    base("""()=>{S.fin.sg=[{id:1,t:'Jamg',a:6000000,s:3000000,e:'💎',dl:'',h:[],cr:'2026-11-01'}];S.money=[{id:11,d:'2026-11-10',k:'out',a:1000000,c:'Ovqat',n:'',w:'p',ac:'cash'}];PV='x';render()}""")
    chk('Biznes tab opens (shows readiness card and a new-trial form)', 'Biznesga tayyorlik' in text() and pg.locator('#bzn').count() == 1)
    chk('the second tab row shows Qarzlar / Zakat / Biznes with Biznes active', pg.locator('.seg button.on:text-is("💼 Biznes")').count() == 1)
    pg.fill('#bzn', 'Onlayn savdo'); pg.fill('#bzc', '1000000'); pg.fill('#bzs', '300000'); ev("pmzBizNew()"); pg.wait_for_timeout(120)
    B = ev("S.fin.bz")
    chk('a trial is created (capital 1 000 000, stop 300 000, started today)', len(B) == 1 and B[0]['cap'] == 1000000 and B[0]['stop'] == 300000 and B[0]['st'] == '2026-11-16', B)
    bid = B[0]['id']
    for k, a in (('c', 1000000), ('o', 200000), ('i', 600000)):
        ev("([k,a,id])=>{document.getElementById('bzk'+id).value=k;document.getElementById('bza'+id).value=a;pmzBizTx(id)}", [k, a, bid]); pg.wait_for_timeout(100)
    S_ = ev("(id)=>pmzBizStat(S.fin.bz.find(x=>x.id===id))", bid)
    chk('stats: spent 1.2M, net −600 000, loss 600 000, profit 400 000, margin 67%, ROI −60%, stop used 200%', S_['spent'] == 1200000 and S_['net'] == -600000 and S_['loss'] == 600000 and S_['profit'] == 400000 and S_['margin'] == 67 and S_['roi'] == -60 and abs(S_['us'] - 2) < 1e-9, S_)
    chk('the stop-loss warning is shown', 'chegarasi oshdi' in text())
    R_ = ev("pmzReady()")
    chk('readiness: cushion ok, capital 1M > 30% of 3M savings fails, stop-loss ok, date ok → 75%', [x['ok'] for x in R_['it']] == [True, False, True, True] and R_['pc'] == 75, R_)
    pg.evaluate("pmzBizChk(0)"); chk('checklist step toggles and persists', ev("S.fin.bzc[0]") == 1)
    ev("()=>{const b=S.fin.bz[0];pmzBizTxDel(b.id,b.tx[0].id)}"); chk('a transaction can be deleted', ev("S.fin.bz[0].tx.length") == 2)
    ev("pmzBizDel(S.fin.bz[0].id)"); chk('a trial can be deleted (confirm)', ev("S.fin.bz.length") == 0)
    chk('empty name/capital is refused with a toast and creates nothing', (ev("()=>{pmzBizNew();return S.fin.bz.length}") == 0))
    # Bosh'dagi karta Biznesga olib boradi
    ev("()=>{PV='b';render()}"); pg.wait_for_timeout(80)
    ev("()=>{[...document.querySelectorAll('#app button.row')].find(b=>/Biznes markazi/.test(b.textContent)).click()}"); pg.wait_for_timeout(100)
    chk('the Bosh "Biznes markazi" card opens the Biznes tab', ev("PV") == 'x')
    # ---------- 7. Yana qatori / eski tuzilish ----------
    ev("()=>{uiS('trk_ptb','a');PV='b';render()}"); pg.wait_for_timeout(80)
    chk('the old 6-tab layout still works (setting "Avvalgidek"), Biznes reachable via the Bosh card', pg.locator('.seg.ptb').count() == 0 and pg.locator('#app button.row:has-text("Biznes markazi")').count() == 1)
    ev("()=>{localStorage.removeItem('trk_ptb');PV='z';render()}"); pg.wait_for_timeout(80)
    chk('in the compact layout the Yana row on Zakat also lists Biznes', pg.locator('.seg button:text-is("💼 Biznes")').count() == 1)
    ev("()=>{uiS('trk_pmz','0');W='p';PV='b';render()}"); pg.wait_for_timeout(80)
    chk('the old look is available: Jilo "Ko‘rinmasin (avvalgidek)" hides briefing, health and medals', pg.locator('.pmzbr').count() == 0 and pg.locator('.pmzm').count() == 0 and 'Moliyaviy sog' not in text())
    ev("()=>{PV='h';render()}"); pg.wait_for_timeout(60)
    chk('...and the leak analyser in Hisobot', 'Qayerda pul oqyapti' not in text())
    ev("()=>{uiS('trk_pmz','1');tab='s';render()}"); pg.wait_for_timeout(100)
    chk('...the setting is listed in Sozlamalar → Jilo', ev("pmzJl().includes('Pul markazi')"))
    ev("()=>{tab='p';PV='b';render()}"); pg.wait_for_timeout(60)
    # ---------- 8. shop hamyoni va toshib ketmaslik ----------
    ev("()=>{W='d';PV='b';render()}"); pg.wait_for_timeout(80)
    chk('the shop wallet does not show the personal Pul markazi (no briefing)', pg.locator('.pmzbr').count() == 0)
    ev("()=>{W='p';PV='b';S.fin.dl={p:{m:'m',v:100000}};render()}"); pg.wait_for_timeout(100)
    chk('no horizontal overflow at phone width (Bosh)', pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    for th, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        for dark in (0, 1):
            ev("([c,d])=>{document.documentElement.className=c+(d?' dk':'');render()}", [th, dark]); pg.wait_for_timeout(60)
            for pv in ('b', 'h', 'x'):
                ev("(v)=>{PV=v;render()}", pv); pg.wait_for_timeout(50)
                chk('%s%s Pul %s: nothing overflows horizontally' % (nm, ' (dark)' if dark else '', pv), pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    # ---------- 9. state: eski ma'lumotga zarar yo'q ----------
    ev("()=>{document.documentElement.className='';S.fin={};S.money=[];PV='b';render()}"); pg.wait_for_timeout(100)
    chk('an old state with an empty S.fin does not crash the Pul home', pg.locator('.pmzbr').count() == 1)
    print('\n%d passed, %d failed' % (R.ok, R.bad))
