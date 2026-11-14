#!/usr/bin/env python3
"""src/  ->  tracker/index.html + tracker/version.json  (ilova hali ham BITTA fayl, sayt shuni talab qiladi).
  python3 tools/build_app.py          yig'adi va yozadi
  python3 tools/build_app.py --check  hech narsa yozmaydi; index.html yoki version.json src/ dan farq qilsa xato bilan chiqadi
version.json: {"v": versiya, "b": yig'ma identifikatori}. Ilova uni tekshirib, "Yangi versiya bor" xabarini ko'rsatadi.
Har safar saytga yuklashda index.html BILAN BIRGA version.json ni ham yuklang."""
import os, sys, re, json, hashlib
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); S = os.path.join(root, 'src')
def cat(d): return ''.join(open(os.path.join(S, d, f), encoding='utf-8', newline='').read() for f in sorted(os.listdir(os.path.join(S, d))))
tpl = open(os.path.join(S, 'index.template.html'), encoding='utf-8', newline='').read()
js_src, css_src = cat('js'), cat('css')
core = tpl.replace('{{CSS}}', css_src).replace('{{JS}}', js_src)
assert core.count('{{BUILD}}') == 1, "src/js/01-yadro.js da {{BUILD}} belgisi aynan bitta bo'lishi kerak"
build = hashlib.sha256(core.encode('utf-8')).hexdigest()[:10]
import shutil, subprocess
def minify(code, loader):
    """Probel va ortiqcha sintaksisni olib tashlaydi (nomlarni O'ZGARTIRMAYDI: onclick="..." lar global nomlarga tayanadi). faqat --min bilan ishlaydi (o'lchov: tezlik farqi sezilmadi, hajm ~2%), o'zgarishsiz qoldiradi."""
    exe = shutil.which('esbuild') or ('/tmp/esb/node_modules/.bin/esbuild' if os.path.exists('/tmp/esb/node_modules/.bin/esbuild') else None)
    if not exe or '--min' not in sys.argv: return code
    r = subprocess.run([exe, '--loader=' + loader, '--minify-whitespace', '--minify-syntax', '--log-level=error'], input=code.encode('utf-8'), capture_output=True)
    if r.returncode != 0: print('OGOHLANTIRISH: siqib bo\'lmadi (%s), oddiy holda yig\'ildi' % loader, r.stderr.decode()[:200]); return code
    return r.stdout.decode('utf-8')
out = tpl.replace('{{CSS}}', minify(css_src, 'css')).replace('{{JS}}', minify(js_src, 'js')).replace('{{BUILD}}', build)
ver = re.search(r"const APP_VER='([^']+)'", core).group(1)
nm = re.search(r"const NEWSV=\[\s*\{v:'([^']+)',t:'([^']*)'", core)
if not nm or nm.group(1) != ver:
    print("XATO: src/js/62-yangiliklar.js dagi NEWSV ro'yxatining BIRINCHI yozuvi APP_VER (%s) bilan bir xil bo'lishi kerak. Yangi versiya uchun yozuv qo'shing." % ver); sys.exit(1)
vj = json.dumps({'v': ver, 'b': build, 'n': nm.group(2)}, separators=(',', ':'), ensure_ascii=False) + '\n'
dst = os.path.join(root, 'tracker', 'index.html'); dv = os.path.join(root, 'tracker', 'version.json')
rd = lambda p: open(p, encoding='utf-8', newline='').read() if os.path.exists(p) else ''
if '--check' in sys.argv:
    if rd(dst) != out or rd(dv) != vj:
        print("XATO: tracker/index.html yoki version.json src/ dan farq qiladi. index.html ni qo'lda tahrirlamang: src/ ni tahrirlab, tools/build_app.py ni ishga tushiring."); sys.exit(1)
    print('src/, tracker/index.html va version.json bir xil (v%s, build %s)' % (ver, build)); sys.exit(0)
open(dst, 'w', encoding='utf-8', newline='').write(out); open(dv, 'w', encoding='utf-8', newline='').write(vj)
print("yig'ildi:", dst, len(out), 'bayt | version.json:', vj.strip())
