#!/usr/bin/env python3
"""Yuklash paketlarini yig'adi:  mushaf-yuklash.zip (o'zing uchun, hammasi)  va  dostlar-versiyasi.zip (Mushaf o'chirilgan).
Ikkalasida ham index.html BILAN BIRGA version.json bor: usiz ilova "yangi versiya bor" deb bilolmaydi."""
import os, subprocess, sys, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, os.path.join(root, 'tools', 'build_app.py'), '--check'], check=True)
files = ['tracker/index.html', 'tracker/version.json', 'tracker/sw.js', 'tracker/qollanma.html', 'data/quran-mushaf.json', 'data/words-v1.txt', 'fonts/UthmanicHafs1Ver18.ttf',
         'fonts/AmiriQuran-arabic.woff2', 'fonts/AmiriQuran-OFL.txt', 'fonts/FONTS-NOTICE.txt']
dest = lambda f: f.split('/', 1)[1] if f.startswith('tracker/') else f
out = os.path.join(root, 'mushaf-yuklash.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files: z.write(os.path.join(root, f), dest(f))
print('yozildi:', out, os.path.getsize(out), 'bayt')
subprocess.run([sys.executable, os.path.join(root, 'tools', 'make_friends_build.py')], check=True)
