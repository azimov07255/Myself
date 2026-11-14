# Kunlik tizim: 10/10 ga olib chiqish rejasi

Holat: ✅ bajarildi · 🔜 navbatdagi · ⏳ keyin

## A faza: Ishonchlilik (sotishdan oldin shart)
- ✅ A1. Avtomatik kunlik zaxira (serverda, 10 kun) + ilovadan tiklash (Sozlama → Avtomatik zaxiralar)
- ✅ A2. Xatolarni yig'ish: foydalanuvchi telefonidagi xatolar egasiga ko'rinadi (Sozlama → Xatolar)
- ✅ A3. Xavfsiz sinxron: versiya raqami + uch tomonlama birlashtirish (ikki qurilma bir-birini bosib yubormaydi, o'chirishlar ham hisobga olinadi)
- ✅ A4. Doimiy xotira so'rash + Diagnostika ekrani
- ✅ A5. Avtomatik sinovlar: `bash tests/run_all.sh` (114 tekshiruv + 35 ekran + takroriy nom tekshiruvi)
- ✅ A6. iPhone sinov ro'yxati tayyor (`tests/IPHONE_QA.md`), bajarish egasi telefonida

## B faza: Mahsulot
- ✅ B1. Telegram bot: kod tayyor va sinalgan; ulash qo'llanmasi `server-setup/TELEGRAM_SETUP.md` (egasi ulaydi). Keyingi bosqich: zikr va ro'za tugmalari
- ✅ B2a. To'liq Mushaf (Madina, 15 qator, 604 sahifa): Suralar/Juz' ro'yxati, davom etish, xatcho'p, oyatni uzoq bosib rang va izoh, Izohlar/Zaif ro'yxatlari
- ✅ B2b. Yodlash sinovi (matn yashirilgan): "oyat boshi" va "faqat raqam"; "zaif" oyatlar mavjud Takror tizimiga ulanadi
- ✅ B8. Yo'l (rag'bat tizimi): ochko (XP), daraja, seriya va qalqon, kunlik 3 topshiriq, haftalik chellenj, tanga va mukofotlar do'koni, maqsad mukofoti, yutuqlar
- ✅ D3. Tartib: Qur'on bo'limi 2 guruhga bo'lindi (Qur'on / Ibodat); Bugun ekrani ustuvorlik bo'yicha tartiblandi
- ✅ B9. Rag'bat: Telegram'da "seriya xavfda" (21:00), ertalabki xabar va yakshanba hisoboti; ilova ichida haftalik hisobot
- ✅ B10. Mushaf ↔ yodlash: "Mushafda ochish", oyatni bugungi yodlashga qo'shish, Takrorda "Mushafda sinab ko'r"
- ✅ D1. Kod `src/` da 21 JS + 4 CSS faylga bo'lindi (`tools/build_app.py`, docs/ARCHITECTURE.md)
- ✅ B12. Sabaq · Sabqi · Manzil: yodlangan sahifalar sana bilan qayd etiladi, kunlik sabqi (oxirgi 7 kun) va manzil (30 kunlik aylanish) rejasi, baholash (zaif -> ertaga sabqiga qaytadi), Mushaf bilan bog'langan
- ✅ B13. AI kun rejasi (Top-3 taklifi, foydalanuvchi tasdiqlaydi; maxfiy ma'lumotlar yuborilmaydi)
- ✅ B14. Moslashuvchan kunlik maqsad (oxirgi 2 hafta), haftada 1 yengil kun, qaytish rejimi (+30 tanga)
- ✅ B15. AI kun rejasi (ertalabdan kechgacha): suhbatda "rejamni tuzib ber", bloklarga aniq vazifa, bo'sh oraliqlarga ishlar, Bugun kartasi, ochko, eslatma
- ✅ C5. "Yangi versiya bor, yangilash" xabari (version.json) va egasi uchun yaxshilangan xatolar paneli (guruhlash, yangi/eski belgisi, xulosa)
- ✅ B15. IELTS materiallari: maqola va podkast (subtitr, audio), AI qiyin so'z/chunk tahlili, so'z-ta'rif-misol kartochkalari (gapni to'ldirish, talaffuz), kunlik yangi so'z limiti, IELTS tayyorgarligi + Qur'on hifzi paneli
- ✅ B17. IELTS qayta tartib (4+4 tab, ixcham Bosh), AI Reading mashqi, Xatolar daftari va mashqi, so'z bilan gap tekshirish, podkast diktanti, AI hisoblagich, boyitilgan suhbat konteksti
- ✅ B18. Podkast audiosidan avtomatik transkript (Groq Whisper, so'z vaqtlari), so'zma-so'z yuruvchi subtitr, US/UK talaffuz, gapni o'qib berish
- ✅ B19. B1+ so'zlar, grammar tahlili, daraja filtrlari, hammasini qo'shish/bekor qilish, ✏️ tahrirlash, podkast audiosi bulutda (barcha qurilmalarda), transkript qatorini tuzatish
- ⏳ B16. URL dan maqola olish, so'z o'yinlari, AI provayderni almashtirish (Claude/OpenAI) uchun adapter
- ⏳ B11. Do'st bilan musobaqa (duo), birinchi kirishda 1 daqiqalik sozlash
- ⏳ B2c. AI bilan tilovatni tekshirish: FAQAT "taxminiy yordamchi" sifatida (AI matnni o'zi "to'g'rilab" yuborishi mumkin, shuning uchun ustoz o'rnini bosmaydi)
- ⏳ B3. Oddiy rejim + yangi foydalanuvchi uchun qisqa tanishuv
- ⏳ B4. Rus tili
- ✅ B5. AI kunlik reja (darslar, imtihonlar, namoz vaqtlari asosida, tasdiqlash bilan)
- ⏳ B6. Do'st bilan juftlik (umumiy seriya)
- ⏳ B7. Payme/Click bilan avtomatik obuna

## C faza: Infratuzilma va sotish
- ⏳ C1. Gemini'da to'lov limiti (byudjet bilan) yoqish
- ⏳ C2. Supabase Pro (ma'lumot 1 GB ga yaqinlashsa yoki real mijozlar bo'lsa)
- ⏳ C3. Maxfiylik siyosati va foydalanish shartlari
- ⏳ C4. Egasi statistikasi: faol foydalanuvchilar, AI sarfi, eng ko'p ishlatiladigan bo'limlar

## D faza: Kod sifati
- ✅ D0. Takroriy nom tekshiruvchi (JS va CSS)
- ✅ D1. Kodni modul fayllarga bo'lish + avtomatik yig'ish (bitta index.html chiqadi, sinovlar o'sha-o'sha ishlaydi)
- ✅ D2. CSS sinf nomlari to'qnashmasligi avtomatik tekshiriladi (tests/check_css_collisions.py)

## Ketma-ketlik (30-oktyabr 2026 holatiga; har bosqichdan keyin kamida 1 hafta real ishlatish)
0. 30–31 okt: faqat ishga tayyorlash. "Ishga tayyormi?" tekshiruv ekrani, haftalik zaxira eslatmasi. Qolgani: yuklash va iPhone QA.
1. 1–7 noy: faqat xato tuzatish va kuzatish (funksiya qo'shilmaydi).
2. 8–21 noy: C4 foydalanish statistikasi → Hifz xaritasi → AI haftalik murabbiy → URL dan maqola + so'z o'yinlari → matnni audioga moslash.
3. Dekabr (do'stlarga tayyorlash): B3 oddiy rejim va 1 daqiqalik sozlash → C3 maxfiylik va ma'lumotni o'chirish → B11/B6 do'st musobaqasi → bulut limiti va C1/C2 qarorlari.
4. 2027 (sotish bo'lsa): AI provayder adapteri → Majmuadan Mushaf ruxsati → B7 to'lov → B4 rus tili → B2c tilovat yordamchisi (eng oxirida).

- ✅ 30–31 okt: 5–9 bandlar bajarildi (foydalanish statistikasi, hifz xaritasi, AI haftalik murabbiy, havoladan maqola + so'z o'yinlari, matnni audioga moslash).

- ✅ 31 okt: IELTS bo'limiga 12 ta qo'shimcha: talaffuz tekshiruvi, AI Listening, materialdan savollar, Writing mavzular banki va reja, Task 1 grafik, band 8 variant, parafraza, so'z oilasi va kollokatsiya, Speaking ko'rsatkichlari va namunaviy javob, to'liq mock, imtihon yo'l xaritasi, imtihon kuni to'plami, eksport (Anki/Excel/chop).

- ✅ 31 okt: Pul (kategoriya byudjetlari, oy prognozi, takroriy yozuvlar, tez shablonlar, CSV, tahlil) va Odat (dam kuni, haftalik maqsad, tahrirlash, odat kuchi) yaxshilandi.

- ✅ 31 okt: jadval ustuni kengligi (sudrash va ◀▶), ixcham va keng ko'rinish, Bugun'da dam kuni, zaxira eslatmasi, Ishga tayyormi? ekrani.

- ✅ 1 noy: Hayot paneli + kashfiyotlar, ma'lumotdan so'rash, Maqsad dvigateli (AI reja), fokus sohalari va suzuvchi taymer. Keyingi bosqich: Univer konspekt → AI savollar (4), rasmdan kiritish (5), Telegram bot orqali yozuv (6).

- ✅ 2 noy: kun yakuni qo'shimchalari (odat, kayfiyat, minnatdorlik), haftalik sharh, odat eslatma vaqti va arxivi. Keyingi: rasmdan kiritish (1), Univer konspekt (2), IELTS Speaking suhbati (5), vidjet (9).

- ✅ 2 noy: iPhone vidjeti (Scriptable) va ishonchlilik sinovi (1 yillik ma'lumot). Keyingi: rasmdan kiritish (1), Univer konspekt (2), IELTS Speaking suhbati (5).

- ✅ 2 noy: pul nazorati (hozirgi qoldiq tuzatildi, kunlik chegara, erkin pul, xarajat turi, xohish ro'yxati), haftalik sharh tugmasi tuzatildi, Yangiliklar va qo'llanma, ixcham eslatma kartochkalari.

- ✅ 2 noy: to'liq qo'llanma: video (11 daqiqa, 39 slayd) va rasmli sahifa (ilova ichidan ochiladi).

- ✅ 3 noy: Bugun tuzilishi (tablar tepada, chiplar, Yana), Uyqu bo'limi (grafik, AI), kunlik chegara asosi va qo'lda belgilash, jamg'arma maqsadi (muddat, sur'at, tezlatgich, belgi).

- ✅ 3 noy: Bugun klassik ko'rinishga qaytarildi (standart); Ixcham ixtiyoriy; tablar aylantirganda qotadi; kun yakunida "Yotdim".

- ✅ 3 noy: yangi dizayn (Klassik/Yangi almashtiriladi), 6 rang, matn o'lchami, animatsiyani o'chirish; kontrast avtomatik tekshiriladi.

- ✅ 3 noy: materiallarda hamma so'z ma'nosi va kesh, lug'atdagi so'zlar belgilanishi, internetdan podkast/maqola olish (BBC va RSS), masofadagi audio transkripti.

- ✅ 3 noy: Lug'at qidiruvi (UK/US IPA + ovoz, AI yozuv, kesh). Keyingi: Liquid Glass rejimi, IELTS 8+ yo'l xaritasi (NGSL/NAWL + mavzuli so'zlar), IELTS kursi.

- ✅ 3 noy: avtomatik to'ldirish, Liquid Glass, IELTS 8+ yo'l xaritasi. Keyingi: IELTS kursi (12 haftalik reja, xatolar daftari, savol turlari strategiyasi, to'liq mock).

- ✅ 3 noy: IELTS kursi (reja, strategiyalar, xatolar daftari), ma'lumotlar ilova ichiga. Keyingi: qo'llanma va videolarni yangilash; rasm orqali kiritish; Telegram orqali kiritish.

- ✅ 3 noy: pauzali pleyer, ovoz tanlash, AI ovozi, kurs eslatmalari. Keyingi: Cambridge natijalari kuzatuvi, Speaking yozib baholash, qo'llanma/videolarni yangilash.

- ✅ 3 noy: "Nima yangilandi?" tizimi, AI ovoz limitiga chidamlilik, Speaking pauza tahlili, shadowing rejimi. Keyingi: Cambridge natijalari kuzatuvi, qo'lda yozilgan insho (rasm), qo'llanma/videolarni yangilash.

- ✅ 3 noy: Hafta bossi, muzlatish, til o'yinlari, Pomodoro, kun hikoyasi, kelajakka xat. Keyingi: do'st reytingi va ustoz rejimi (server jadvallari kerak), zaxira, Cambridge natijalari, rasm orqali insho.

- ✅ Ayat o'yini va Aqlli yordamchi. Qolgan: do'st reytingi va ustoz rejimi (server), zaxira, Cambridge natijalari, rasm orqali insho, ovoz bilan yozuv.

- ✅ Hozir nima qilay, brifing, soya poygasi, niyat/muhosaba, bog', natija kartasi, tezlik trenajyori, xotira saroyi.

- ✅ Kunlik nasihatchi; Bugun: kartalarni yig'ish va jilo (ixtiyoriy).

- ✅ Hayot haftalari xaritasi, haftalik stories. Qoldi: insho laboratoriyasi (AI'siz), band bashorati.

- ✅ IELTS kuni, zaif nuqta radari, halol bashorat, CEFR boshlang'ich daraja. Qoldi: insho laboratoriyasi (AI'siz), intervyu mashqi, ariza kuzatuvchisi, ingliz tilida CV.

- ✅ Reja: blok turi va qat'iy/moslashuvchan, kesishish, bo'sh oraliqlar, Kechikdim. Qoldi: 'faqat bugun' tahrir, avto-belgilash, blok statistikasi, reja-haqiqat, avto-jadval, kun buzildi.

- ✅ Xatolar jurnali, iPhone sinov ro'yxati, Cambridge javoblar varag'i. Qoldi: insho laboratoriyasi (AI'siz), ilovani tezlashtirish (lazy-load), reja: avto-jadval/kun buzildi/'faqat bugun', ish yo'li (CV, intervyu, ariza).

- ✅ Nafs bo'limi (shartnoma, tajriba, balans, to'siqlar). Qoldi: avto-jadval, 'kun buzildi', insho laboratoriyasi, tezlashtirish, ish yo'li.

- ✅ Kun tekshiruvi, imtihon yo'li, marosim. Qoldi: avto-jadval, 'kun buzildi', insho laboratoriyasi, tezlashtirish, ish yo'li.

- ✅ Takror 2, Ko'rsatkichlarim, Kashfiyotlar. Qoldi: Adaptiv maqsad, Rekordlar zali, Savol ber, Kashfiyotlarni Bugun'da ko'rsatish, avto-jadval, 'kun buzildi', insho laboratoriyasi, tezlashtirish, ish yo'li.

- ✅ Tezkor reja (＋), maqsad avto-progress, Namozda takror, 604 bet. Endi faqat mavjud funksiyalarni takomillashtirish.

- ✅ Ishonchlilik, jilo va qulaylik (bekor qilish, qidiruv, sana, Bugun kartalari, Quron rejasi, qo'llanma). Qoldi: qo'llanma videolari, haqiqiy iPhone sinovi.

- ✅ Maqsad vaqt hisobi, kuniga bir necha uyqu. Qoldi (ataylab qilinmadi): qulflangan ekran kartasi (Media Session), taymer tugaganda push.

- ✅ Eslatmalar auditi, Bugun bo'limlari, bekor qilish (25 ta), o'zbekcha sanalar, qo'llanma. Qoldi: Safari (WebKit) sinovi, sinxron holati belgisi, eksport.

- ✅ Cambridge so'zlari (shaxsiy fayl + bulut). Qoldi: Reading javoblar varag'i bilan bog'lash (faylda Cambridge test raqami yo'q), so'zlar bo'yicha o'yinlar.

- ✅ 14 noy: Pul (tez yozish, zakot va sadaqa, sof boylik, do'kon foydasi, xarajat = mehnat soati, tablar 4 + Yana), Bugun tepasi ixcham ko'rinish, Sozlamalar guruhlandi (egasi bo'limi, zaxira bir joyda, qisqa yangiliklar). Sinovlar parallel va portativ (`bash tests/run_all.sh` → HAMMASI YAXSHI, ~9 daqiqa).
- ⏸ Lazy-load (tezlik): 14 noy o'lchandi, hozircha SHART EMAS. Birinchi mazmun: 0,3 s (oddiy CPU), 1,2-1,6 s (CPU 4× sekin), 2,4-2,8 s (6× sekin); servis worker keshi bor. Eng katta ma'lumot bloki (`58-data-lugat.js`) hajmning ~7%i; hamma kod bitta global nom maydonida va `onclick` lar global funksiyalarga tayanadi, shuning uchun bo'lish xavfli. Qayta ko'rib chiqish sharti: haqiqiy telefonda ochilish sezilarli sekin bo'lsa (kerak bo'lsa avval `build_app.py --min` va `58-data-lugat.js` ni alohida faylga chiqarish).
- Qoldi: Hisobot sahifasini bo'limlarga bo'lish (Pul), haqiqiy iPhone sinovi, AI provayder adapteri (B16), 1 daqiqalik tanishuv (B3).
