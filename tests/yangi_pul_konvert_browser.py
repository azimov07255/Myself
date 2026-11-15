# Pul: haftalik konvertlar, "agar tejasam?", juma jamg'arma marosimi. Soat: 2026-11-09 (dushanba) 10:00.
import sys, os
sys.path.insert(0, os.environ.get('KT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tests')
from _pw import Run
def M(i, d, a, c): return {'id': i, 'd': d, 'k': 'out', 'a': a, 'c': c, 'n': '', 'w': 'p', 'ac': 'cash'}
with Run('pul_konvert', when=(2026, 11, 9, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-11-09T10:00:00')
    ev("""()=>{window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);S.money=[];S.debts=[];S.fin={open:{p:{cash:0,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[]};W='p';PV='r';tab='p';render();drjSample();drjSet('usd','1000');drjSet('rate','12500');drjGoal();render()}"""); pg.wait_for_timeout(150)
    text = lambda: pg.inner_text('#app').replace('\xa0', ' ')
    # ---------- konvertlar ----------
    chk('no envelopes at first; the card offers to fill them from the expense rules', ev("drjEnv().length") == 0 and 'Haftalik konvertlar' in text())
    ev("drjEnvPlan()"); e = ev("drjEnv()")
    chk('"Xarajat qoidalaridan to‘ldirish": Ovqat 37 000×7 = 259 000 and Transport 27 000×7 = 189 000 a week', sorted((x['c'], x['lim']) for x in e) == [('Ovqat', 259000), ('Transport', 189000)], e)
    ev("()=>{S.money=[{id:1,d:'2026-11-09',k:'out',a:100000,c:'Ovqat',n:'',w:'p',ac:'cash'},{id:2,d:'2026-11-08',k:'out',a:999999,c:'Ovqat',n:'',w:'p',ac:'cash'},{id:3,d:'2026-11-09',k:'out',a:50000,c:'Transport',n:'',w:'p',ac:'cash'},{id:4,d:'2026-11-09',k:'out',a:80000,c:'Ovqat',n:'',w:'d',ac:'cash'}];render()}")
    d = {x['c']: x for x in ev("drjEnv()")}
    chk('spent counts only THIS week (Mon 9 – Sun 15 Nov) and only the personal wallet: Ovqat 100 000 (last week\'s 999 999 and the shop\'s 80 000 are ignored)', d['Ovqat']['sp'] == 100000 and d['Transport']['sp'] == 50000, d)
    chk('Ovqat 39%, left 159 000 over 7 days = 22 714 a day; Transport 26%, left 139 000', d['Ovqat']['pc'] == 39 and d['Ovqat']['left'] == 159000 and d['Ovqat']['perDay'] == 22714 and d['Transport']['pc'] == 26 and d['Transport']['left'] == 139000, d)
    ev("()=>{S.money.push({id:5,d:'2026-11-10',k:'out',a:200000,c:'Ovqat',n:'',w:'p',ac:'cash'});render()}"); o = {x['c']: x for x in ev("drjEnv()")}['Ovqat']
    chk('over the limit: Ovqat 300 000 of 259 000 → left −41 000 and the screen says it was exceeded', o['left'] == -41000 and 'oshdi' in text(), o)
    ev("()=>{PV='b';render()}"); pg.wait_for_timeout(100); t = text()
    chk('the Pul home shows "Bu hafta konvertlari" with the remaining amounts', 'Bu hafta konvertlari' in t and 'Ovqat' in t and 'Transport' in t)
    ev("drjEnvDel('Transport')"); chk('an envelope can be removed', [x['c'] for x in ev("drjEnv()")] == ['Ovqat'])
    ev("()=>{PV='r';render();document.getElementById('drjec').value='4';document.getElementById('drje').value='100 000';drjEnvSet()}"); chk('a manual envelope (Kiyim 100 000) is added', {x['c']: x['lim'] for x in ev("drjEnv()")}.get('Kiyim') == 100000)
    ev("()=>{W='d';PV='b';render()}"); chk('the shop wallet shows none of it', 'konvertlari' not in text() and 'Haftalik jamg' not in text()); ev("()=>{W='p';render()}")
    # ---------- agar tejasam ----------
    ev("()=>{S.money=[];PV='r';render()}"); P = ev("drjPlan()")
    chk('baseline: goal 12 500 000, monthly saving 1 140 000 → 11 months', P['eta'] == 11 and P['sv'] == 1140000, P)
    w = ev("drjWhatIf(8000)"); chk('saving 8 000 a day (≈ 243 200 a month) → 1 383 200 a month → 10 months (1 month earlier)', w['extra'] == 243200 and w['sv2'] == 1383200 and w['mo'] == 10 and w['saved'] == 1, w)
    w = ev("drjWhatIf(18000)"); chk('saving 18 000 a day → 8 months (3 months earlier)', w['mo'] == 8 and w['saved'] == 3, w)
    chk('0 per day = no change (the slider text says the current pace)', ev("drjWhatIf(0).saved") == 0)
    pg.evaluate("document.querySelector('#app input[type=range]').scrollIntoView()"); pg.evaluate("()=>{const r=document.querySelector('#app input[type=range]');r.value=8000;r.dispatchEvent(new Event('input',{bubbles:true}))}"); pg.wait_for_timeout(80)
    chk('moving the slider updates the sentence live (8 000 → "~10 oyda … 1 oy erta") WITHOUT re-rendering the page', '~10 oyda' in pg.inner_text('#drjqo') and '1 oy erta' in pg.inner_text('#drjqo') and pg.inner_text('#drjql').replace('\xa0', ' ') == '8 000')
    ev("()=>{drjSet('usd','');render()}"); chk('without a goal the slider card is not shown', pg.locator('#drjqo').count() == 0)
    ev("()=>{drjSet('usd','1000');render()}")
    # ---------- juma marosimi ----------
    J = ev("drjJz()"); chk('weekly saving target = 1 140 000 × 7 / 30.4 = 262 500; Monday → 4 days until Friday', J['weekly'] == 262500 and J['dow'] == 0 and J['done'] == 0 and J['streak'] == 0, J)
    ev("()=>{PV='b';render()}"); pg.wait_for_timeout(100); t = text()
    chk('Pul home shows the card: "Jamg‘arma kuni: juma (4 kun qoldi)" and the 262 500 amount', 'Haftalik jamg‘arma' in t and '4 kun qoldi' in t and '262 500' in ev("document.querySelector('#drjws').value+' '+document.getElementById('app').innerText").replace('\xa0', ' '))
    ev("[...document.querySelectorAll('#app button')].find(b=>b.textContent.includes('o‘tkazdim')).click()"); pg.wait_for_timeout(120)
    g = ev("S.fin.sg[0]"); chk('tapping it adds 262 500 to the dollar goal and logs it', g['s'] == 262500 and g['h'][-1]['a'] == 262500, g)
    chk('the card now congratulates and shows the 1-week streak; it cannot be done twice', 'Barakalla' in text() and '1 hafta ketma-ket' in text() and (ev("drjSaveWeek()") or True) and ev("S.fin.sg[0].s") == 262500)
    ev("drjUnsave()"); chk('"Bekor qilish" returns the goal to 0 and removes this week\'s mark', ev("S.fin.sg[0].s") == 0 and ev("drjJz().done") == 0)
    ev("drjSaveWeek()"); pg.clock.set_system_time('2026-11-16T10:00:00'); ev("()=>{render()}"); J = ev("drjJz()")
    chk('next week (16 Nov): the card is open again, but the streak of 1 is kept (last week was done)', J['done'] == 0 and J['streak'] == 1, J)
    ev("drjSaveWeek()"); chk('doing the 2nd week → streak 2, goal 525 000', ev("drjJz().streak") == 2 and ev("S.fin.sg[0].s") == 525000)
    pg.clock.set_system_time('2026-11-30T10:00:00'); ev("()=>{render()}"); chk('skipping a week (23 Nov) breaks the streak: on 30 Nov the streak shows 0', ev("drjJz().streak") == 0)
    pg.clock.set_system_time('2026-11-13T10:00:00'); ev("()=>{S.fin.jz={};render()}"); pg.wait_for_timeout(80); chk('on Friday the card says "Bugun jamg‘arma kuni"', 'Bugun jamg‘arma kuni' in text() or ev("PV") != 'b')
    # tekis raqamlar
    ev("()=>{uiS('trk_pl','1');dzApply();render()}"); chk('polish on: amounts use tabular numerals (font-variant-numeric: tabular-nums)', 'tabular-nums' in ev("getComputedStyle(document.getElementById('app')).fontVariantNumeric"))
    for cls, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        for pv in ('b', 'r'):
            ev("(a)=>{document.documentElement.className=a[0];W='p';PV=a[1];render()}", [cls, pv]); pg.wait_for_timeout(80)
            chk('%s style, Pul %s: no horizontal overflow' % (nm, pv), pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"))
    print('\n%d passed, %d failed' % (R.ok, R.bad))
