# Haqiqiy brauzerda (Chromium, telefon o'lchami) hamma ekranni ochib, xato va ko'ndalang tasmani tekshiradi
from playwright.sync_api import sync_playwright
seed="""S.ob=1;S.ts=1;const k=d=>{const x=new Date();x.setDate(x.getDate()+d);return x.toLocaleDateString('sv')};
S.un.subj=[{id:'s1',n:'Matematika',cr:5,t:'K',lim:10,col:'#46c4b2'}];S.un.tt={[new Date().getDay()]:[{id:1,sid:'s1',s:'08:30',e:'09:50',r:'204',k:'Amaliy'}]};S.un.tasks=[{id:1,t:'Misol',s:'Matematika',due:k(1),x:0}];S.un.exams=[{id:1,s:'Matematika',d:k(9),tm:'10:00',r:'',p:20}];
S.gym.ex=[{id:'e1',n:'Bench press',g:'Ko‘krak',s:4,r:8,w:60,note:'',m:null}];S.gym.plan[new Date().getDay()]={place:'gym',ex:[{id:'e1',s:4,r:8,w:60}]};S.gym.pass={n:'Fit',s:k(-3),e:k(26),t:12,v:{[k(-3)]:'d'}};S.gym.food.log[dk()]=[{id:1,m:'Tushlik',n:'Osh',kcal:620,p:22,f:28,c:70}];
S.rz.start=k(-5);S.hab=[{id:'h1',t:'Kitob',e:'📚'}];S.ie.words=[{id:1,w:'mitigate',m:'yumshatmoq',box:0,due:dk(),t:0}];"""
screens=[]
for bv in ['j','m','h','t']:screens.append((f"tab='h';BV='{bv}'",f'h/{bv}'))
for q in ['y','t','h','z','n','r','d','a']:screens.append((f"tab='q';QT='{q}'",f'q/{q}'))
for o in ['o','h','w','m','z','i']:screens.append((f"tab='o';OT='{o}'",f'o/{o}'))
for z in ['r','a','m','o','j']:screens.append((f"tab='o';OT='z';ZV='{z}'",f'zal/{z}'))
for e in ['i','u','k','p']:screens.append((f"tab='e';EV='{e}'",f'e/{e}'))
for u in ['b','j','f','t','e']:screens.append((f"tab='e';EV='u';UV='{u}'",f'univer/{u}'))
for t in ['m','p','s']:screens.append((f"tab='{t}'",t))
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);pg=ctx.new_page()
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*',lambda r:r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto('file:///mnt/user-data/outputs/tracker/index.html');pg.wait_for_timeout(400);pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
    pg.evaluate("()=>{"+seed+"}")
    for js,name in screens:
        try:
            pg.evaluate("()=>{"+js+";render();window.scrollTo(0,0)}");pg.wait_for_timeout(50)
            if 'Kechirasan' in pg.evaluate("document.getElementById('app').innerText"):bad.append((name,'crash page'));continue
            r=pg.evaluate("""()=>{const W=document.documentElement.clientWidth;let n=[];document.querySelectorAll('#app *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>W+2&&!e.closest('.seg,.sc,.chips,.rzt,.hg,[style*="overflow-x"]'))n.push((e.className||e.tagName)+':'+Math.round(r.right))});return {sw:document.documentElement.scrollWidth,n:n.slice(0,3)}}""")
            if r['sw']>392 or r['n']:bad.append((name,r))
        except Exception as ex:bad.append((name,str(ex)[:120]))
    print('screens checked:',len(screens),'| problems:',bad or 'none','| JS errors:',errs or 'none')
    b.close()
import sys;sys.exit(1 if (bad or errs) else 0)
