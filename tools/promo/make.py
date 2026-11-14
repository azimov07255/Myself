# -*- coding: utf-8 -*-
import os, sys, math, wave, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1280, 720, 24
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
_fc = {}
def F(sz, b=False):
    k = (sz, b)
    if k not in _fc: _fc[k] = ImageFont.truetype(FB if b else FR, sz)
    return _fc[k]
CREAM, ACC, GRN, YEL, RED, MUT = (246, 241, 230), (232, 126, 70), (79, 191, 139), (231, 190, 80), (226, 85, 85), (176, 200, 188)
ease = lambda t: 1 - (1 - max(0, min(1, t))) ** 3
def back(t):
    t = max(0, min(1, t)); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
prog = lambda lt, a, b: max(0, min(1, (lt - a) / (b - a)))
SC = [
 dict(k='TANISHUV', head='Kunlik tizim', shot='bugun_kunlik', w='title', text='Kunlik tizim. Butun kuningni bitta ilovada boshqar.'),
 dict(k='BUGUN', head='Kun jadvali va asosiy ishlar', shot='bugun_jadval', w='bugun', text='Bugun ekranida kun jadvali, uchta asosiy ish va odatlaring bir joyda turadi.'),
 dict(k='ODATLAR', head='Odatlar va seriya', shot='odatlar', w='odat', text='Odatlarni belgilab bor. Kasal bo‘lsang dam kuni qo‘y, seriyang uzilmaydi.'),
 dict(k='QUR‘ON', head='Hifz, takror va namoz', shot='takror', w='quron', text='Qur‘on yodlash uchun sabaq, sabqi va manzil tartibi, hifz xaritasi va namoz vaqtlari bor.'),
 dict(k='IELTS', head='IELTS tayyorgarligi', shot='ielts_ai', w='ielts', text='IELTS tayyorgarligi: lug‘at, maqolalar, yozish va gapirish mashqlari. Sun‘iy intellekt tekshiradi, mock va imtihon rejasi ham tayyor.'),
 dict(k='PUL', head='Pulni nazorat qil', shot='pul_bosh', w='pul', text='Pulni nazorat qil: balans, kunlik xarajat chegarasi va byudjet. Keraksiz xarajatni belgilaysan, xohish ro‘yxati esa tejashga yordam beradi.'),
 dict(k='MAQSAD', head='Maqsad dvigateli', shot='maqsad_dvigatel', w='maqsad', text='Maqsad dvigateli maqsadingni haftalik rejaga aylantiradi.'),
 dict(k='TAHLIL', head='Haftalik sharh va hayot paneli', shot='hayot', w='hayot', text='Haftalik sharh va hayot paneli kuchli va zaif tomonlaringni ko‘rsatadi.'),
 dict(k='TIZIM', head='Hamma qurilmada, xavfsiz', shot='sozlama_vidjet', w='tizim', text='Telefon va kompyuterda ishlaydi. Eslatmalar, iPhone vidjeti va zaxira nusxa ham bor.'),
 dict(k='SINAB KO‘R', head='Kunni boshqar, maqsadga yet', shot='bugun_kunlik', w='outro', text='Kunlik tizim. Kunni boshqar, maqsadga yet. Sinab ko‘r!'),
]
# ---------------- ovoz ----------------
def synth(i, text):
    p = '/tmp/promo/v%02d.wav' % i; subprocess.run(['espeak-ng', '-v', 'uz', '-s', '158', '-p', '48', '-g', '4', '-w', p, text], check=True)
    w = wave.open(p); n = w.getnframes(); a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768; sr = w.getframerate(); w.close()
    return a, sr
VO = [synth(i, s['text']) for i, s in enumerate(SC)]
DUR = [max(6.5, len(a) / sr + 1.5) for a, sr in VO]; DUR[0] = max(DUR[0], 7.0); DUR[-1] += 1.2
START = [sum(DUR[:i]) for i in range(len(SC))]; TOTAL = sum(DUR); NF = int(TOTAL * FPS)
VSTART = [START[i] + 0.55 for i in range(len(SC))]
SR = 44100
def build_audio(with_voice):
    n = int((TOTAL + 0.5) * SR); mix = np.zeros(n, dtype=np.float32)
    # musiqa: Am - F - C - G, yumshoq pad va arpeggio
    bpm = 84; beat = 60 / bpm; chords = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]; mf = lambda m: 440 * 2 ** ((m - 69) / 12)
    tt = np.arange(n) / SR
    for ci in range(int(TOTAL / (4 * beat)) + 2):
        t0 = ci * 4 * beat; ch = chords[ci % 4]; i0 = int(t0 * SR); L = int(4 * beat * SR)
        if i0 >= n: break
        seg = np.arange(min(L, n - i0)) / SR; env = np.minimum(seg / 0.6, 1) * np.minimum((4 * beat - seg) / 0.8, 1).clip(0, 1)
        pad = sum(np.sin(2 * np.pi * mf(m - 12) * seg) + 0.35 * np.sin(2 * np.pi * mf(m) * seg) for m in ch) * env * 0.045
        mix[i0:i0 + len(seg)] += pad.astype(np.float32)
        for k in range(8):
            ti = t0 + k * beat / 2; j0 = int(ti * SR)
            if j0 >= n: break
            m = ch[[0, 1, 2, 1, 2, 1, 0, 1][k]] + 12; s2 = np.arange(min(int(0.5 * SR), n - j0)) / SR
            mix[j0:j0 + len(s2)] += (np.sin(2 * np.pi * mf(m) * s2) * np.exp(-s2 * 7) * 0.05).astype(np.float32)
    fade = np.minimum(1, np.minimum(tt / 1.5, (TOTAL + 0.3 - tt) / 2.0).clip(0, 1)); mix *= fade.astype(np.float32)
    if with_voice:
        for i, (a, sr) in enumerate(VO):
            a2 = np.interp(np.arange(int(len(a) * SR / sr)) / SR * sr, np.arange(len(a)), a).astype(np.float32); a2 /= max(1e-3, np.abs(a2).max()); j0 = int(VSTART[i] * SR)
            mix[j0:j0 + len(a2)] *= 0.55; mix[j0:j0 + len(a2)] += a2[:len(mix) - j0] * 0.85
    mix = mix / max(1.0, np.abs(mix).max() * 1.05); p = '/tmp/promo/audio_%s.wav' % ('voice' if with_voice else 'music')
    w = wave.open(p, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close(); return p
# ---------------- tasvir ----------------
def mk_bg():
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * y / H) for a, b in zip((12, 52, 42), (26, 92, 74))))
    return im
BG = mk_bg().convert('RGBA'); PH = {}
def phone(k):
    if k in PH: return PH[k]
    s = Image.open('/tmp/guide/shots/%s.png' % k).convert('RGB'); h = 600; w = int(s.width * h / s.height); s = s.resize((w, h), Image.LANCZOS)
    m = Image.new('L', s.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w, h], 26, fill=255)
    out = Image.new('RGBA', (w + 24, h + 24), (0, 0, 0, 0)); sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([8, 14, w + 16, h + 20], 32, fill=(0, 0, 0, 120)); out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(9)))
    fr = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(fr).rounded_rectangle([6, 6, w + 18, h + 18], 32, fill=(238, 235, 226, 255)); out = Image.alpha_composite(out, fr); out.paste(s, (12, 12), m); PH[k] = out; return out
def deco(img, t):
    o = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    for k, (cx, cy, r, sp) in enumerate([(200, 130, 190, .7), (1060, 560, 240, .5), (640, 700, 160, .9), (1120, 90, 120, 1.1)]):
        x = cx + 40 * math.sin(t * sp + k); y = cy + 30 * math.cos(t * sp * .8 + k); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 10))
    img.alpha_composite(o)
def T(d, xy, s, sz, col=CREAM, b=False, a='la'): d.text(xy, s, font=F(sz, b), fill=col, anchor=a)
def wrap(s, f, mw, d):
    out, line = [], ''
    for w in s.split(' '):
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=f) <= mw: line = t
        else: out.append(line); line = w
    if line: out.append(line)
    return out
def chip(d, x, y, s, col, sc=1.0, sz=44):
    if sc <= 0.02: return 0
    f = F(max(8, int(sz * sc)), True); tw = d.textlength(s, font=f); h = int(sz * 1.55 * sc); w = int(tw + 44 * sc)
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=col + (255,)); d.text((x + w / 2, y + h / 2), s, font=f, fill=(255, 255, 255), anchor='mm'); return w
def ring(d, cx, cy, r, p, col, label, sub=''):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 50), width=22)
    if p > 0.005: d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * p, fill=col + (255,), width=22)
    T(d, (cx, cy - 6), label, 76, CREAM, True, 'mm')
    if sub: T(d, (cx, cy + 56), sub, 30, MUT, False, 'mm')
def bar(d, x, y, wd, p, col, h=30):
    d.rounded_rectangle([x, y, x + wd, y + h], h // 2, fill=(255, 255, 255, 45))
    if p > 0.01: d.rounded_rectangle([x, y, x + max(h, wd * p), y + h], h // 2, fill=col + (255,))
def check(d, cx, cy, r, col=GRN):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,)); d.line([(cx - r * .42, cy), (cx - r * .1, cy + r * .35), (cx + r * .45, cy - r * .3)], fill=(255, 255, 255), width=int(r * .28))
fmt = lambda n: '{:,}'.format(int(n)).replace(',', ' ')
# ---------------- vidjetlar (2x tuval: 1400x840) ----------------
def w_title(d, lt):
    for k, s in enumerate(['Hifz', 'IELTS', 'Odat', 'Pul', 'Maqsad', 'AI']):
        x = 0 + (k % 3) * 330; y = 560 + (k // 3) * 110; chip(d, x, y, s, [GRN, ACC, (70, 150, 220), (200, 150, 40), (150, 100, 210), (60, 170, 170)][k], back(prog(lt, 1.6 + k * .18, 2.2 + k * .18)))
    pp = back(prog(lt, .3, 1.0)); T(d, (0, 30), 'Kunlik tizim', max(1, int(150 * min(1, pp))), CREAM, True)
    T(d, (0, 300), 'Butun kuning', 64, CREAM, True); T(d, (0, 390), 'bitta ilovada', 64, ACC, True)
def w_bugun(d, lt):
    for k, (s, c) in enumerate([('Kun jadvali', GRN), ('3 ta asosiy ish', ACC), ('Odatlar', (70, 150, 220))]): chip(d, 0, 40 + k * 120, s, c, back(prog(lt, .9 + k * .8, 1.5 + k * .8)))
    p = ease(prog(lt, 1.5, 4.5)); ring(d, 1010, 270, 190, 0.72 * p, GRN, str(int(72 * p)) + '%', 'bugungi kun'); 
def w_odat(d, lt):
    n = 8
    for k in range(n):
        cx = 60 + k * 118; cy = 130; on = lt > 1.0 + k * .45
        d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=(255, 255, 255, 110), width=6)
        if on: pp = back(prog(lt, 1.0 + k * .45, 1.3 + k * .45)); check(d, cx, cy, int(44 * pp))
    d.ellipse([60 + 6 * 118 - 44, 130 - 44, 60 + 6 * 118 + 44, 130 + 44], fill=(255, 255, 255, 45)) if lt > 5 else None
    done = min(n, max(0, int((lt - 1.0) / .45) + 1)); T(d, (0, 270), 'Bugun: %d / %d' % (done, n), 72, CREAM, True)
    T(d, (0, 380), 'Seriya', 40, MUT); T(d, (330, 360), str(int(12 * ease(prog(lt, 1.5, 4)))) + ' kun', 72, ACC, True)
    chip(d, 0, 520, 'Dam kuni: seriya uzilmaydi', (70, 150, 220), back(prog(lt, 4.8, 5.5)), 40)
def w_quron(d, lt):
    for k, (s, c) in enumerate([('Sabaq', GRN), ('Sabqi', (70, 150, 220)), ('Manzil', ACC)]): chip(d, k * 320, 30, s, c, back(prog(lt, .8 + k * .7, 1.4 + k * .7)))
    p = ease(prog(lt, 1.5, 5)); ring(d, 340, 400, 170, 0.23 * p, GRN, str(int(23 * p)) + '%', 'hifz xaritasi')
    T(d, (720, 330), 'Namoz vaqtlari', 40, MUT); 
    for k, (n, tm) in enumerate([('Peshin', '12:07'), ('Asr', '15:35'), ('Shom', '17:22')]):
        a = ease(prog(lt, 3.5 + k * .5, 4.2 + k * .5)); T(d, (720, 400 + k * 80), n, 44, tuple(int(c * a) for c in CREAM)); T(d, (1100, 400 + k * 80), tm, 44, tuple(int(c * a) for c in ACC), True)
def w_ielts(d, lt):
    items = [('Listening', 7.0), ('Reading', 6.5), ('Writing', 6.0), ('Speaking', 6.5)]
    for k, (n, v) in enumerate(items):
        y = 60 + k * 120; p = ease(prog(lt, 1.0 + k * .6, 2.4 + k * .6)); T(d, (0, y), n, 40, CREAM); bar(d, 280, y + 6, 700, p * v / 9, [GRN, (70, 150, 220), ACC, (150, 100, 210)][k], 36); T(d, (1010, y), '%.1f' % (v * p), 44, CREAM, True)
    x = 280 + 700 * 7 / 9; d.line([(x, 30), (x, 520)], fill=ACC + (255,), width=5); T(d, (x, 535), 'maqsad 7.0', 34, ACC, True, 'ma')
    for k, s in enumerate(['Lug‘at', 'Yozish', 'Gapirish', 'Mock']): chip(d, k * 270, 640, s, [GRN, ACC, (70, 150, 220), (150, 100, 210)][k], back(prog(lt, 4.2 + k * .5, 4.8 + k * .5)), 36)
def w_pul(d, lt):
    p = ease(prog(lt, .8, 3)); T(d, (0, 20), 'Balans', 40, MUT); T(d, (0, 80), fmt(5365000 * p) + ' so‘m', 82, CREAM, True)
    T(d, (0, 250), 'Bugungi chegara', 40, MUT); q = ease(prog(lt, 2.6, 5)); bar(d, 0, 320, 900, 0.62 * q, YEL, 44); T(d, (930, 318), str(int(62 * q)) + '%', 46, CREAM, True)
    for k, (s, c) in enumerate([('Zarur', GRN), ('Xohish', YEL), ('Keraksiz', RED)]): chip(d, k * 330, 470, s, c, back(prog(lt, 5.2 + k * .5, 5.8 + k * .5)), 44)
    chip(d, 0, 640, 'Xohish ro‘yxati: 24 soat kut', (70, 150, 220), back(prog(lt, 7.0, 7.7)), 38)
def w_maqsad(d, lt):
    st = ['1-hafta: Diagnostika', '2-hafta: Reading', '3-hafta: Writing', '4-hafta: Speaking']
    for k, s in enumerate(st):
        a = back(prog(lt, .8 + k * .9, 1.4 + k * .9)); y = 60 + k * 130; d.rounded_rectangle([0, y, 980, y + 100], 24, fill=(255, 255, 255, int(40 * min(1, a))))
        if a > 0.05: T(d, (110, y + 50), s, 46, CREAM, False, 'lm')
        if lt > 1.6 + k * .9: check(d, 55, y + 50, int(30 * back(prog(lt, 1.6 + k * .9, 2.0 + k * .9))))
    q = ease(prog(lt, 1.5, 5.5)); T(d, (0, 620), 'Maqsad: %d%%' % int(75 * q), 56, ACC, True); bar(d, 400, 635, 580, .75 * q, ACC, 36)
def w_hayot(d, lt):
    L = ['Din', 'Odatlar', 'Ta‘lim', 'Fokus', 'Salomatlik', 'Moliya']; sc = [57, 69, 80, 45, 71, 90]; cx, cy, R = 700, 400, 270; p = ease(prog(lt, .8, 3.5))
    pt = lambda i, r: (cx + r * math.cos(-math.pi / 2 + i * math.pi / 3), cy + r * math.sin(-math.pi / 2 + i * math.pi / 3))
    for f in (1, .5): d.polygon([pt(i, R * f) for i in range(6)], outline=(255, 255, 255, 70))
    for i in range(6): d.line([(cx, cy), pt(i, R)], fill=(255, 255, 255, 50), width=2)
    d.polygon([pt(i, R * sc[i] / 100 * p) for i in range(6)], fill=(79, 191, 139, 110), outline=GRN + (255,))
    for i, l in enumerate(L):
        x, y = pt(i, R + 52); T(d, (x, y), l, 36, CREAM, True, 'mm')
def w_tizim(d, lt):
    items = [('Telefon', 'phone'), ('Kompyuter', 'pc'), ('Eslatma', 'bell'), ('Vidjet', 'wid'), ('Zaxira', 'shield')]
    for k, (n, g) in enumerate(items):
        a = back(prog(lt, .8 + k * .6, 1.4 + k * .6)); cx = 90 + k * 270; cy = 250
        if a < .05: continue
        r = int(100 * a); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 40)); s = a
        if g == 'phone': d.rounded_rectangle([cx - 28 * s, cy - 50 * s, cx + 28 * s, cy + 50 * s], 10, outline=CREAM + (255,), width=6)
        elif g == 'pc': d.rectangle([cx - 56 * s, cy - 38 * s, cx + 56 * s, cy + 24 * s], outline=CREAM + (255,), width=6); d.line([(cx - 30 * s, cy + 44 * s), (cx + 30 * s, cy + 44 * s)], fill=CREAM + (255,), width=6)
        elif g == 'bell': d.arc([cx - 40 * s, cy - 50 * s, cx + 40 * s, cy + 30 * s], 180, 360, fill=CREAM + (255,), width=6); d.line([(cx - 40 * s, cy - 10 * s), (cx - 52 * s, cy + 34 * s), (cx + 52 * s, cy + 34 * s), (cx + 40 * s, cy - 10 * s)], fill=CREAM + (255,), width=6)
        elif g == 'wid': d.rounded_rectangle([cx - 52 * s, cy - 40 * s, cx + 52 * s, cy + 40 * s], 14, outline=CREAM + (255,), width=6); d.line([(cx - 34 * s, cy - 10 * s), (cx + 34 * s, cy - 10 * s)], fill=ACC + (255,), width=8); d.line([(cx - 34 * s, cy + 14 * s), (cx + 10 * s, cy + 14 * s)], fill=GRN + (255,), width=8)
        else: d.polygon([(cx, cy - 56 * s), (cx + 46 * s, cy - 32 * s), (cx + 40 * s, cy + 24 * s), (cx, cy + 58 * s), (cx - 40 * s, cy + 24 * s), (cx - 46 * s, cy - 32 * s)], outline=CREAM + (255,)); check(d, cx, cy, int(22 * s))
        T(d, (cx, cy + 150), n, 36, CREAM, True, 'mm')
    chip(d, 130, 520, 'Ma‘lumot o‘zingda: shaxsiy hisob', GRN, back(prog(lt, 4.5, 5.2)), 40)
def w_outro(d, lt):
    p = back(prog(lt, .4, 1.1)); T(d, (0, 70), 'Kunlik tizim', int(110 * min(1, p)) or 1, CREAM, True); T(d, (0, 230), 'Kunni boshqar,', 66, MUT, True); T(d, (0, 320), 'maqsadga yet.', 66, ACC, True)
    pulse = 1 + 0.05 * math.sin(lt * 5); chip(d, 0, 520, 'Sinab ko‘r', ACC, back(prog(lt, 1.6, 2.3)) * pulse, 56)
WID = dict(title=w_title, bugun=w_bugun, odat=w_odat, quron=w_quron, ielts=w_ielts, pul=w_pul, maqsad=w_maqsad, hayot=w_hayot, tizim=w_tizim, outro=w_outro)
def scene_layer(i, lt, d_):
    S = SC[i]; L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    a = ease(prog(lt, 0.1, 0.6)); T(d, (70, 52 - int(10 * (1 - a))), S['k'], 20, tuple(int(c) for c in ACC), True)
    if i not in (0, 9): T(d, (70, 86 - int(12 * (1 - a))), S['head'], 38, CREAM, True)
    ph = phone(S['shot']); sl = ease(prog(lt, 0.15, 0.9)); px = 880 + int(300 * (1 - sl)); py = 50 + int(5 * math.sin(lt * 1.6)); L.alpha_composite(ph, (px, py))
    w2 = Image.new('RGBA', (1400, 840), (0, 0, 0, 0)); dw = ImageDraw.Draw(w2); WID[S['w']](dw, lt); w2 = w2.resize((700, 420), Image.LANCZOS); L.alpha_composite(w2, (70, 150))
    cap = S['text']; f = F(26); ca = ease(prog(lt, 0.7, 1.2)) * (1 - ease(prog(lt, d_ - .5, d_ - .15)))
    if ca > 0.02:
        lines = wrap(cap, f, 700, d); bh = len(lines) * 36 + 28; y0 = H - bh - 28; box = Image.new('RGBA', (740, bh), (0, 0, 0, 0)); bd = ImageDraw.Draw(box); bd.rounded_rectangle([0, 0, 740, bh], 18, fill=(0, 0, 0, int(135 * ca)))
        for j, l in enumerate(lines): bd.text((20, 14 + j * 36), l, font=f, fill=tuple(int(c) for c in CREAM) + (int(255 * ca),))
        L.alpha_composite(box, (50, y0))
    return L
def frame(t):
    i = max(k for k in range(len(SC)) if START[k] <= t + 1e-6); lt = t - START[i]; d_ = DUR[i]
    base = BG.copy(); deco(base, t); L = scene_layer(i, lt, d_); a = min(ease(prog(lt, 0, 0.35)), 1 - ease(prog(lt, d_ - .35, d_)))
    if a < 1: L.putalpha(L.getchannel('A').point(lambda v: int(v * a)))
    base.alpha_composite(L); return base.convert('RGB')
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        pts = [3.0, START[2] + 4, START[4] + 3.5, START[5] + 6, START[7] + 3, START[9] + 3]; M = Image.new('RGB', (640 * 3, 360 * 2))
        for n, t in enumerate(pts): M.paste(frame(t).resize((640, 360)), ((n % 3) * 640, (n // 3) * 360))
        M.save('/tmp/promo/preview.png'); print('durs', [round(x, 1) for x in DUR], 'total', round(TOTAL, 1)); sys.exit()
    json.dump(dict(START=START, DUR=DUR, VSTART=VSTART, VOD=[len(a) / sr for a, sr in VO], TEXT=[s['text'] for s in SC], TOTAL=TOTAL), open('/tmp/promo/meta.json', 'w'))
    build_audio(True); build_audio(False)
    pr = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '/tmp/promo/video_only.mp4'], stdin=subprocess.PIPE)
    for f in range(NF):
        pr.stdin.write(frame(f / FPS).tobytes())
        if f % 240 == 0: print('frame', f, '/', NF, flush=True)
    pr.stdin.close(); pr.wait(); print('DONE')
