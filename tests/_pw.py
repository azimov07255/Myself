# Haqiqiy brauzer sinovlari uchun umumiy yordamchi: HTTP server, soxta soat, ilovani ochish, chk() hisoblagichi.
import os, shutil, struct, base64, http.server, threading, socketserver, functools, datetime, sys
from playwright.sync_api import sync_playwright
import tempfile
OUT = os.environ.get('KT_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def wav(sec=8, sr=8000):
    n = sr * sec
    return b'RIFF' + struct.pack('<I', 36 + n) + b'WAVEfmt ' + struct.pack('<IHHIIHH', 16, 1, 1, sr, sr, 1, 8) + b'data' + struct.pack('<I', n) + bytes([128]) * n
class Run:
    def __init__(self, name, when=(2026, 10, 31, 10, 0, 0), width=390, bg='o'):
        self.name, self.when, self.width, self.ok, self.bad, self.bg = name, when, width, 0, 0, bg
    def __enter__(self):
        site = os.path.join(tempfile.gettempdir(), 'site_' + self.name); shutil.rmtree(site, ignore_errors=True); os.makedirs(site)
        [shutil.copy(os.path.join(OUT, 'tracker', f), site) for f in os.listdir(OUT + '/tracker') if os.path.isfile(os.path.join(OUT, 'tracker', f))]
        class H(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a): pass
            def handle(self):
                try: super().handle()
                except (BrokenPipeError, ConnectionResetError): pass
        self.srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(H, directory=site)); self.port = self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.pw = sync_playwright().start(); self.b = self.pw.chromium.launch()
        ctx = self.b.new_context(viewport={'width': self.width, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        self.pg = ctx.new_page(); self.errs = []; self.pg.on('pageerror', lambda e: self.errs.append(str(e)))
        self.pg.clock.install(time=datetime.datetime(*self.when))
        if self.bg == 'o': self.pg.add_init_script("try{if(localStorage.getItem('trk_bg')===null)localStorage.setItem('trk_bg','o');if(localStorage.getItem('trk_sgr')===null)localStorage.setItem('trk_sgr','a');if(localStorage.getItem('trk_ptb')===null)localStorage.setItem('trk_ptb','a');if(localStorage.getItem('trk_pl')===null)localStorage.setItem('trk_pl','0')}catch(e){}")  # eski sinovlar eski (hammasi bir ekranda) tuzilishni tekshiradi
        self.pg.route('**/*', lambda r: r.continue_() if r.request.url.startswith(('http://127.0.0.1', 'data:', 'blob:')) else r.abort())
        self.pg.goto(f'http://127.0.0.1:{self.port}/index.html'); self.pg.wait_for_timeout(600)
        self.pg.evaluate("document.querySelectorAll('#spl,.splash,#splash').forEach(e=>e.remove())")
        self.ev = self.pg.evaluate; self.ev("()=>{S.ob=1;S.ts=1;window.__fnAI0=fnAI}")
        return self
    def at(self, *when): self.pg.clock.set_system_time(datetime.datetime(*when))
    def put_audio(self, key, data):
        self.pg.evaluate("""async(a)=>{const u=Uint8Array.from(atob(a[1]),c=>c.charCodeAt(0));await idbSet(a[0],new Blob([u],{type:'audio/wav'}))}""", [key, base64.b64encode(data).decode()])
    def chk(self, name, cond, extra=''):
        if cond: self.ok += 1; print('PASS', name)
        else: self.bad += 1; print('FAIL', name, extra)
    def __exit__(self, *a):
        try:
            self.chk('no JavaScript errors during the whole run', not self.errs, self.errs[:3])
            self.b.close(); self.pw.stop()
        finally:
            print('\n%d passed, %d failed' % (self.ok, self.bad))
        if a[0] is None: sys.exit(1 if self.bad else 0)
