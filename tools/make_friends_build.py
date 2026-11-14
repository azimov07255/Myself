#!/usr/bin/env python3
"""Do'stlarga beriladigan versiya: Mushaf bo'limi butunlay o'chirilgan, Qur'on matni va shriftlar kiritilmaydi.
Ishlatish: python3 tools/make_friends_build.py   ->  dostlar-versiyasi.zip"""
import os, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); app = os.path.join(root, 'tracker')
src = open(os.path.join(app, 'index.html'), encoding='utf-8').read()
a = "const MUSHAF_MODE='all';"; assert src.count(a) == 1
out = os.path.join(root, 'dostlar-versiyasi.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(os.listdir(app)):
        p = os.path.join(app, f)
        if not os.path.isfile(p) or f.endswith('.sql'): continue   # SQL fayllar saytga kerak emas
        if f == 'index.html': z.writestr(f, src.replace(a, "const MUSHAF_MODE='off';"))
        else: z.write(p, f)
with zipfile.ZipFile(out, 'a', zipfile.ZIP_DEFLATED) as z:
    for f in ('data/words-v1.txt',): z.write(os.path.join(root, f), f)   # kichik lug'at ma'lumotlari (Qur'on matni emas)
print('yozildi:', out, os.path.getsize(out), 'bayt')
with zipfile.ZipFile(out) as z:
    names = z.namelist(); print(names)
    assert not any(n.startswith(('data/', 'fonts/')) and n not in ('data/words-v1.txt', 'data/ielts-lists-v1.json') for n in names)
