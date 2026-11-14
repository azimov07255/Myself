# -*- coding: utf-8 -*-
import sys, os, base64, io, json, html
sys.path.insert(0, '/tmp/guide')
from content import SL
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
W, H = 1280, 720; BG1, BG2 = (14, 59, 48), (24, 84, 68); CREAM = (246, 241, 230); ACC = (232, 126, 70); MUT = (190, 208, 198)
font = lambda p, s: ImageFont.truetype(p, s)
def wrap(d, text, f, mw):
    out, line = [], ''
    for w in text.split(' '):
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=f) <= mw: line = t
        else:
            if line: out.append(line)
            line = w
    if line: out.append(line)
    return out
def bg():
    im = Image.new('RGB', (W, H)); px = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; px.line([(0, y), (W, y)], fill=tuple(int(BG1[i] + (BG2[i] - BG1[i]) * t) for i in range(3)))
    return im
def phone(path, hgt):
    s = Image.open(path).convert('RGB'); w = int(s.width * hgt / s.height); s = s.resize((w, hgt), Image.LANCZOS)
    m = Image.new('L', s.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w, hgt], 26, fill=255)
    out = Image.new('RGBA', (w + 16, hgt + 16), (0, 0, 0, 0)); sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([6, 10, w + 12, hgt + 14], 30, fill=(0, 0, 0, 110)); out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(8)))
    fr = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(fr).rounded_rectangle([4, 4, w + 12, hgt + 12], 30, fill=(235, 232, 222, 255)); out = Image.alpha_composite(out, fr); out.paste(s, (8, 8), m); return out
def layout(d, items, x, y0, mw, sizes, gap):
    # items: list of (kind,text); returns (size, height)
    for sz in sizes:
        f = font(FR, sz); y = y0; 
        for k, t in items:
            n = len(wrap(d, t, f, mw - (50 if k == 'step' else 0))); y += n * int(sz * 1.35) + gap
        if y <= 640: return sz
    return sizes[-1]
def slide(i, S, total):
    k, part, title, where, steps, tip = S
    im = bg(); d = ImageDraw.Draw(im); tx = 80
    if k:
        ph = phone('/tmp/guide/shots/%s.png' % k, 620); im.paste(ph, (64, 50), ph); tx = 64 + ph.width + 56
    mw = W - tx - 60
    d.text((tx, 40), part, font=font(FB, 19), fill=ACC)
    ft = font(FB, 40); tl = wrap(d, title, ft, mw); y = 76
    for l in tl: d.text((tx, y), l, font=ft, fill=CREAM); y += 50
    y += 6
    if where:
        for l in wrap(d, 'Qayerda: ' + where, font(FB, 22), mw): d.text((tx, y), l, font=font(FB, 22), fill=(255, 214, 170)); y += 30
        y += 10
    sz = layout(d, [('step', s) for s in steps], tx, y, mw, [26, 24, 22, 20], 12) if k else layout(d, [('step', s) for s in steps], tx, y, mw, [30, 28, 26, 24, 22], 18)
    f = font(FR, sz)
    for n, s in enumerate(steps, 1):
        d.ellipse([tx, y + 2, tx + 34, y + 36], fill=ACC); nf = font(FB, 20); d.text((tx + 17, y + 19), str(n) if k or True else '', font=nf, fill=(255, 255, 255), anchor='mm')
        ls = wrap(d, s, f, mw - 50)
        for l in ls: d.text((tx + 50, y), l, font=f, fill=CREAM); y += int(sz * 1.35)
        y += 14 if k else 20
    if tip:
        y = max(y + 6, 560) if y < 560 else y + 6
        fb = font(FR, 22); tl2 = wrap(d, tip, fb, mw - 40); bh = len(tl2) * 30 + 44
        y = min(y, H - bh - 40)
        box = Image.new('RGBA', (mw, bh), (0, 0, 0, 0)); ImageDraw.Draw(box).rounded_rectangle([0, 0, mw, bh], 16, fill=(255, 255, 255, 30), outline=(232, 126, 70, 255), width=2); im.paste(box, (tx, y), box)
        d.text((tx + 20, y + 10), 'Maslahat', font=font(FB, 18), fill=ACC)
        for j, l in enumerate(tl2): d.text((tx + 20, y + 34 + j * 30), l, font=fb, fill=CREAM)
    d.text((W - 40, H - 28), 'Kunlik tizim  ·  %d / %d' % (i + 1, total), font=font(FR, 16), fill=MUT, anchor='ra')
    return im
total = len(SL); durs = []
for i, S in enumerate(SL):
    im = slide(i, S, total); im.save('/tmp/guide/slides/%02d.png' % i)
    chars = len(S[2]) + len(S[3] or '') + sum(len(x) for x in S[4]) + len(S[5] or ''); durs.append(max(9, min(20, 5 + chars * 0.045)))
json.dump(durs, open('/tmp/guide/durs.json', 'w'))
print('slides', total, 'total sec', round(sum(durs)), 'min', round(sum(durs) / 60, 1))
# contact sheet of 6 slides
idx = [0, 2, 6, 12, 22, 27]; M = Image.new('RGB', (640 * 3, 360 * 2))
for n, i in enumerate(idx): M.paste(Image.open('/tmp/guide/slides/%02d.png' % i).resize((640, 360)), ((n % 3) * 640, (n // 3) * 360))
M.save('/tmp/guide/sheet.png')
