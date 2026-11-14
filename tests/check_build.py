# Yig'ish va paketlar: version.json index.html bilan mos, ikkala zipda ham bor, ichidagi versiya bir xil.
import os, re, json, subprocess, sys, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ok = bad = 0
def chk(n, c, x=''):
    global ok, bad
    if c: ok += 1; print('PASS', n)
    else: bad += 1; print('FAIL', n, x)
subprocess.run([sys.executable, os.path.join(root, 'tools', 'make_zips.py')], check=True, stdout=subprocess.DEVNULL)
h = open(os.path.join(root, 'tracker', 'index.html'), encoding='utf-8').read(); vj = json.load(open(os.path.join(root, 'tracker', 'version.json')))
ver = re.search(r"const APP_VER='([^']+)'", h).group(1); bld = re.search(r"const APP_BUILD='([^']+)'", h).group(1)
chk('version.json = APP_VER and APP_BUILD inside index.html, plus the short update note', {k: vj.get(k) for k in ('v', 'b')} == {'v': ver, 'b': bld} and isinstance(vj.get('n'), str) and vj['n'], (vj, ver, bld))
chk('APP_BUILD is a real 10-character identifier (placeholder replaced)', re.fullmatch(r'[0-9a-f]{10}', bld) is not None and '{{BUILD}}' not in h)
chk('version follows YYYY.MM.DD-N', re.fullmatch(r'\d{4}\.\d{2}\.\d{2}-\d+', ver) is not None, ver)
for name in ('mushaf-yuklash.zip', 'dostlar-versiyasi.zip'):
    z = zipfile.ZipFile(os.path.join(root, name)); names = z.namelist()
    chk(name + ' contains index.html AND version.json', 'index.html' in names and 'version.json' in names, names)
    zi = z.read('index.html').decode(); zv = json.loads(z.read('version.json'))
    chk(name + ': version.json matches the index.html inside the same zip', {k: zv.get(k) for k in ('v', 'b')} == {'v': re.search(r"APP_VER='([^']+)'", zi).group(1), 'b': re.search(r"APP_BUILD='([^']+)'", zi).group(1)} and bool(zv.get('n')), zv)
    chk(name + ' has the current version', zv['v'] == ver)
chk('friends build keeps Mushaf off and ships no Quran data or fonts', "const MUSHAF_MODE='off';" in zipfile.ZipFile(os.path.join(root, 'dostlar-versiyasi.zip')).read('index.html').decode() and not any(n.startswith(('data/', 'fonts/')) and n not in ('data/words-v1.txt', 'data/ielts-lists-v1.json') for n in zipfile.ZipFile(os.path.join(root, 'dostlar-versiyasi.zip')).namelist()))
import hashlib
S = os.path.join(root, 'src'); cat = lambda d: ''.join(open(os.path.join(S, d, f), encoding='utf-8', newline='').read() for f in sorted(os.listdir(os.path.join(S, d))))
core = open(os.path.join(S, 'index.template.html'), encoding='utf-8', newline='').read().replace('{{CSS}}', cat('css')).replace('{{JS}}', cat('js'))
chk('the build id is the SHA-256 of the source text (so any source change gives a new id)', hashlib.sha256(core.encode('utf-8')).hexdigest()[:10] == bld and hashlib.sha256((core + ' ').encode('utf-8')).hexdigest()[:10] != bld)
print('\n%d passed, %d failed' % (ok, bad)); sys.exit(1 if bad else 0)
