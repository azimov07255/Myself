#!/usr/bin/env python3
"""Yig'ilgan sayt fayllarini (tracker/) repo ILDIZIGA nusxalaydi: GitHub Pages shu yerdan ishlaydi.
Ishlatish: python3 tools/build_app.py && python3 tools/make_zips.py && python3 tools/deploy_root.py
Faqat o'zgargan fayllarni yozadi va nima o'zgarganini chiqaradi."""
import os, shutil, filecmp
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(root, 'tracker')
names = ['index.html', 'version.json', 'sw.js', 'qollanma.html', 'manifest.webmanifest', 'favicon.svg', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png']
ch = []
for n in names:
    a, b = os.path.join(src, n), os.path.join(root, n)
    if not os.path.exists(a): continue
    if not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
        shutil.copyfile(a, b); ch.append(n)
print('ildizga yozildi:', ', '.join(ch) if ch else 'o\'zgarish yo\'q')
