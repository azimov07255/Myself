import sys,json
from playwright.sync_api import sync_playwright
def shoot(seed_js,out,full=True,w=390,h=844,theme=None,scroll=0,clip_h=None):
    with sync_playwright() as p:
        b=p.chromium.launch()
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=ctx.new_page()
        pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a')}catch(e){}")
        errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.route('**/*',lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
        pg.goto('file:///mnt/user-data/outputs/tracker/index.html')
        pg.wait_for_timeout(400)
        pg.evaluate("""()=>{document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())}""")
        if theme: pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
        pg.evaluate(seed_js)
        pg.wait_for_timeout(300)
        # overflow check: anything wider than viewport?
        ov=pg.evaluate("""()=>{const W=document.documentElement.clientWidth,bad=[];document.querySelectorAll('#app *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&(r.right>W+1||r.left<-1))bad.push((e.className||e.tagName)+':'+Math.round(r.left)+'-'+Math.round(r.right))});return {W,sw:document.documentElement.scrollWidth,bad:bad.slice(0,8)}}""")
        pg.screenshot(path=out,full_page=full)
        b.close()
        return errs,ov
if __name__=='__main__':
    print(shoot(sys.argv[1],sys.argv[2]))
