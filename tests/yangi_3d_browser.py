# 3D: Isolation yo'l xaritasi, tanga minorasi, Hozir kartasi parallaksi, namoz osmoni; o'chirish sozlamasi. Soat: 2026-11-18 (chorshanba) 10:00.
import sys, os
sys.path.insert(0, os.environ.get('KT_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/tests')
from _pw import Run
with Run('d3', when=(2026, 11, 18, 10, 0, 0)) as R:
    ev, chk, pg = R.ev, R.chk, R.pg
    pg.clock.set_system_time('2026-11-18T10:00:00')
    def setup(d3=None):
        ev("""(a)=>{localStorage.removeItem('trk_3d');if(a)uiS('trk_3d',a);dzApply();window.confirm=()=>true;window.__t=[];window.toast=m=>window.__t.push(m);
          S.iso={lim:60,m:{},log:[],mr:{on:1,start:'2026-11-14',n:14,pt:2,man:{},ref:{}}};S.nm.d={};S.rules={};S.money=[];S.pr.tests=[];S.pr.er={};S.pr.exam='2026-11-25';S.q.lg=[];S.q.ppd=0;
          const full=k=>{S.iso.mr.man[k]={nm:1,hf:1,pr:1,ph:1};S.iso.mr.ref[k]={g:'a'}};full('2026-11-14');full('2026-11-17');S.iso.mr.man['2026-11-15']={nm:1,hf:1,pr:1};
          S.pt={lat:41.31,lon:69.28,loc:'tash',tune:{}};
          S.fin={open:{p:{cash:1000000,card:0},d:{cash:0,card:0}},budget:0,sg:[],cb:{},rc:[],wl:[]};W='p';tab='o';OT='i';render()}""", d3); pg.wait_for_timeout(150)
    text = lambda: pg.inner_text('#app').replace('\xa0', ' ')
    cls = lambda: ev("[...document.querySelectorAll('#app .d3t')].map(t=>t.className.replace('d3t ',''))")
    # ---------- 2. yo'l xaritasi ----------
    setup(); chk('default is ON: html has the "d3" class and the Isolation screen shows "Yo‘l xaritasi"', ev("document.documentElement.classList.contains('d3')") and 'Yo‘l xaritasi' in text())
    c = cls(); chk('14 tiles: full days 14 and 17 = d, the 60% day 15 = p, the empty day 16 = m, today (18) = t, the rest future = f', len(c) == 14 and c[0] == 'd' and c[1] == 'p' and c[2] == 'm' and c[3] == 'd' and c[4] == 't' and all(x == 'f' for x in c[5:]), c)
    chk('tiles are real 3D (the plane has preserve-3d + rotateX; each tile has 5 depth layers)', ev("getComputedStyle(document.querySelector('#app .d3plane')).transformStyle") == 'preserve-3d' and ev("document.querySelectorAll('#app .d3t')[0].querySelectorAll('i').length") == 5)
    chk('markers: ✓ coin on full days, 📍 pin on today, 🚗 on the Prava exam day (25 Nov = 12th tile), 🏁 on the last tile', ev("document.querySelectorAll('#app .d3coin').length") == 2 and ev("document.querySelectorAll('#app .d3pin').length") == 1 and ev("document.querySelectorAll('#app .d3t')[11].textContent.includes('🚗')") and ev("document.querySelectorAll('#app .d3t')[13].textContent.includes('🏁')"))
    chk('the map fits inside the card without sideways overflow', pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1") and ev("(()=>{const p=document.querySelector('#app .d3path').getBoundingClientRect(),q=[...document.querySelectorAll('#app .d3t')].map(t=>t.getBoundingClientRect());return q.every(r=>r.left>=p.left-2&&r.right<=p.right+2)})()"))
    ev("()=>{S.iso.mr.n=30;render()}"); chk('a 30-day marafon is too long for the map: it is not drawn (the dots remain)', pg.locator('#app .d3path').count() == 0 and pg.locator('#app .mrfdot').count() == 30); ev("()=>{S.iso.mr.n=14;render()}")
    ev("()=>{S.iso.mr.n=7;S.iso.mr.start='2026-11-16';render()}"); chk('a 7-day marafon gets a 7-tile map', len(cls()) == 7); ev("()=>{S.iso.mr.n=14;S.iso.mr.start='2026-11-14';render()}")
    # ---------- 3. tanga minorasi ----------
    ev("()=>{tab='p';PV='b';drjSet('usd','1000');drjSet('rate','12500');drjGoal();S.fin.sg[0].s=3000000;render()}"); pg.wait_for_timeout(120); t = text()
    chk('Pul → Bosh shows "Jamg‘arma minorasi" with 24%', 'Jamg‘arma minorasi' in t and '24%' in t and '3 000 000 / 12 500 000' in t)
    chk('24% of 24 slots = 6 gold coins (4 depth layers each = 24) and 18 dashed ghost slots', ev("document.querySelectorAll('#app .d3co:not(.g)').length") == 24 and ev("document.querySelectorAll('#app .d3co.g').length") == 18)
    chk('a big spinning "$" coin sits on top (CSS rotateY animation)', ev("getComputedStyle(document.querySelector('#app .d3bigc')).animationName") == 'd3spin' and '$' in ev("document.querySelector('#app .d3bigc').textContent"))
    ev("()=>{S.fin.sg[0].s=0;render()}"); chk('nothing saved yet: 0 solid coins, 24 ghost slots', ev("document.querySelectorAll('#app .d3co:not(.g)').length") == 0 and ev("document.querySelectorAll('#app .d3co.g').length") == 24)
    ev("()=>{S.fin.sg[0].s=500000;render()}"); chk('even a small saving shows at least one coin', ev("document.querySelectorAll('#app .d3co:not(.g)').length") == 4)
    ev("()=>{S.fin.sg[0].s=13000000;render()}"); chk('goal reached: the tower is full (24 coins = 96 layers, no ghosts) and says 100%', ev("document.querySelectorAll('#app .d3co:not(.g)').length") == 96 and ev("document.querySelectorAll('#app .d3co.g').length") == 0 and '100%' in text())
    ev("()=>{S.fin.sg=[];drjSet('usd','');render()}"); chk('without a goal the tower is EMPTY (no solid coins) and a goal form invites the user to start', pg.locator('#app .d3coins').count() == 1 and ev("document.querySelectorAll('#app .d3co:not(.g)').length") == 0 and pg.locator('#pmu').count() == 1)
    # ---------- 5. Hozir kartasi ----------
    ev("()=>{tab='h';BV='j';render()}"); pg.wait_for_timeout(150)
    chk('Bugun → Jadval: the "Hozir" card has the 3D class and a floating animation', pg.locator('#app .hero.d3c').count() == 1 and ev("getComputedStyle(document.querySelector('#app .hero.d3c')).animationName") == 'd3fl')
    chk('the title, ring and button sit at different depths (translateZ), so the card looks layered', ev("getComputedStyle(document.querySelector('#app .hero.d3c h1')).transform") != 'none' and ev("getComputedStyle(document.querySelector('#app .hero.d3c')).transformStyle") == 'preserve-3d')
    ev("()=>{const h=document.querySelector('#app .hero.d3c');const r=h.getBoundingClientRect();h.dispatchEvent(new PointerEvent('pointermove',{bubbles:true,clientX:r.left+r.width*.9,clientY:r.top+r.height*.2}))}")
    chk('touching/moving over the card tilts it (inline perspective + rotateX/rotateY, animation paused)', 'rotateY' in ev("document.querySelector('#app .hero.d3c').style.transform") and ev("document.querySelector('#app .hero.d3c').style.animation") != '')
    ev("()=>{document.dispatchEvent(new Event('pointerup'))}"); chk('letting go returns it to the floating animation (inline styles cleared)', ev("document.querySelector('#app .hero.d3c').style.transform") == '')
    chk('buttons inside the 3D card still work: "Bajardim" can be pressed', ev("(()=>{const b=[...document.querySelectorAll('#app .hero.d3c button')].find(x=>/Bajardim/.test(x.textContent));return !!b&&b.getBoundingClientRect().width>40})()"))
    # ---------- 6. namoz osmoni ----------
    ev("()=>{BV='m';render()}"); pg.wait_for_timeout(150)
    chk('Bugun → Kunlik shows the prayer sky with 6 markers (Bomdod, Quyosh, Peshin, Asr, Shom, Xufton) and the next prayer', pg.locator('#app .d3sky').count() == 1 and ev("document.querySelectorAll('#app .d3sky svg circle[r=\"7\"]').length") == 6 and 'Keyingi:' in text())
    xs = ev("[...document.querySelectorAll('#app .d3sky svg circle[r=\"7\"]')].map(c=>+c.getAttribute('cx'))"); chk('markers are ordered left to right along the arc in prayer order', xs == sorted(xs) and xs[0] < 80 and xs[-1] > 310, xs)
    chk('daytime (10:00): the sun is drawn (gradient circle), the sky is not in night mode', pg.locator('#app .d3sky.n').count() == 0 and ev("document.querySelectorAll('#app .d3sky svg circle[fill=\"url(#d3sn)\"]').length") == 1)
    pg.clock.set_system_time('2026-11-18T23:30:00'); ev("()=>{render()}"); pg.wait_for_timeout(120)
    chk('late evening (23:30): night mode with the moon instead of the sun, still naming the next prayer', pg.locator('#app .d3sky.n').count() == 1 and ev("document.querySelectorAll('#app .d3sky svg circle[fill=\"url(#d3sn)\"]').length") == 0 and 'Keyingi:' in text())
    pg.clock.set_system_time('2026-11-18T10:00:00')
    ev("()=>{S.pt=null;render()}"); chk('no prayer times set: no sky (nothing breaks)', pg.locator('#app .d3sky').count() == 0)
    # ---------- o'chirish ----------
    setup('0'); chk('3D OFF: no class, no path, no 3D hero class animation', not ev("document.documentElement.classList.contains('d3')") and pg.locator('#app .d3path').count() == 0 and 'Yo‘l xaritasi' not in text())
    ev("()=>{tab='p';PV='b';drjSet('usd','1000');drjSet('rate','12500');drjGoal();S.fin.sg[0].s=3000000;render()}"); chk('3D OFF: no coin tower', pg.locator('#app .d3coins').count() == 0)
    ev("()=>{tab='h';BV='m';render()}"); chk('3D OFF: no prayer sky', pg.locator('#app .d3sky').count() == 0 and 'Namozlar' in text())
    ev("()=>{SDO={w_v:1,jl:1};tab='s';render()}"); chk('Jilo has "3D animatsiyalar" with Yoqilgan / O‘chirilgan', 'd3Jl' and ev("d3Jl().includes('O‘chirilgan')"))
    ev("bmOpt('3d','1')"); chk('Jilo → Yoqilgan turns it back on and saves the choice', ev("uiG('trk_3d')") == '1' and ev("document.documentElement.classList.contains('d3')"))
    # ---------- harakatni kamaytirish ----------
    setup(); pg.emulate_media(reduced_motion='reduce'); ev("()=>{tab='o';OT='i';render()}"); pg.wait_for_timeout(120)
    chk('"Reduce motion": the map, the spinning coin and the floating card stop animating', ev("getComputedStyle(document.querySelector('#app .d3plane')).animationName") == 'none'); pg.emulate_media(reduced_motion='no-preference')
    # ---------- uslublar ----------
    for cls_, nm in (('', 'Klassik'), ('ui2', 'Yangi'), ('ui2 glass', 'Glass')):
        bad = []
        for tb in ('o', 'p', 'h'):
            ev("(a)=>{document.documentElement.className=a[0];localStorage.removeItem('trk_3d');dzApply();S.pt={lat:41.31,lon:69.28,loc:'tash',tune:{}};S.fin.sg=[{id:1,t:'M',a:12500000,s:3000000,usd:1000}];drjSet('usd','1000');drjSet('rate','12500');tab=a[1];OT='i';PV='b';BV=a[1]==='h'?'m':'j';render()}", [cls_, tb]); pg.wait_for_timeout(100)
            if not pg.evaluate("document.documentElement.scrollWidth<=window.innerWidth+1"): bad.append(tb)
        chk('%s style: Isolation, Pul and Bugun screens with 3D do not overflow sideways' % nm, not bad, bad)
    print('\n%d passed, %d failed' % (R.ok, R.bad))
