# Qo'llanma video va sahifa yaratuvchi vositalar
Yangi funksiya qo'shilganda qo'llanmani yangilash:
1. `content.py` ga o'zbekcha matnni qo'shing/o'zgartiring (kalit = ekran rasmi nomi).
2. `shoot.py` ga ekranni qo'shing (SHOTS) va ishga tushiring: namuna ma'lumot bilan `/tmp/guide/shots/*.png` yaratadi.
3. `compose.py` (video slaydlari `/tmp/guide/slides`), keyin `ffmpeg` bilan MP4 (`list.txt` + `durs.json`), `build_guide.py` (qollanma.html).
4. `qollanma.html` ni `tracker/` ichiga qo'ying (zip'ga o'zi kiradi).
Skriptlar `/tmp/guide` papkasiga yozadi; kerak bo'lsa yo'llarni o'zgartiring.
