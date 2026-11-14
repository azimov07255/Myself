# Kunlik tizim — loyiha qo'llanmasi (Claude Code uchun)

## Kim bilan ishlayapsan
- Foydalanuvchi: **Abdulaziz** (18 yosh, O'zbekiston, universitet 1-kurs va ishlaydi). **Har doim o'zbek tilida (lotin) javob ber.** Qisqa, aniq, "mukammal" natija va soddalikni yoqtiradi.
- Ilova: shaxsiy "Kunlik tizim" PWA (Qur'on hifz, IELTS, odat, pul, maqsad, AI yordamchi, Telegram, vidjet). Windows'da desktop oynasi, iPhone'da PWA sifatida ishlaydi.
- **Halollik qoidasi:** nimani sinab ko'rganingni va nimani sinab ko'ra olmaganingni aniq ayt (haqiqiy iPhone, Groq/Gemini, haqiqiy internet). Taxminni haqiqat deb ko'rsatma.

## Arxitektura (eng muhimi)
- **Haqiqat manbai: `src/`** (`src/js/00…95-*.js`, `src/css/10-asos…92-jilo.css`, `src/index.template.html`). `tracker/index.html` — shundan yig'iladigan **natija**, qo'lda tahrir qilinmaydi.
- Yig'ish: `python3 tools/build_app.py` (`--check` src bilan index.html mosligini tekshiradi). `APP_VER` — `src/js/01-yadro.js` (har chiqarishda oshir).
- Paketlash: `python3 tools/make_zips.py` → `mushaf-yuklash.zip`, `dostlar-versiyasi.zip`.
- Hamma JS bitta global nom maydonida: **funksiya/`let`/`const` nomlari to'qnashmasligi shart.** Tekshirish: `node --check` (yig'ilgan skriptda), `python3 tests/lint_dupes.py`, `python3 tests/check_css_collisions.py`. Yangi nomga prefiks ber (masalan `ks…` kurs, `xd…` xatolar, `yx…` so'z yo'li, `vp/ov…` ovoz, `dq…` lug'at qidiruvi, `dz…` dizayn).
- Holat: bitta JSON `S` (localStorage + Supabase sinxron). Noma'lum kalitlar saqlanadi. IELTS ma'lumotlari `S.ie.*`; `S.ie.ed` boshqa funksiyaga band.
- Server: `server-setup/*.ts` (ai-assistant, create-user, send-reminders, telegram-bot, widget) → `bash tests/sync_supabase_folder.sh` ularni `supabase/functions/<nom>/index.ts` ga nusxalaydi. `supabase/config.toml` har funksiyani e'lon qilishi shart (`tests/check_supabase_folder.py` tekshiradi). GitHub→Supabase avtomatik deploy yoqilgan.
- **Sirlar (kalitlar, tokenlar) hech qachon repoga tushmasin.** `server-setup/` da faqat kod va SQL shablonlari bor (kalit yo'q), shuning uchun repoda turishi mumkin. Kalitlar faqat Supabase → Edge Functions → Secrets da (`GEMINI_API_KEY`, `GROQ_API_KEY`, `OWNER_EMAIL`, `AI_DAILY_LIMIT`, `TTS_MODEL` va h.k.).
- Ma'lumot: `data/` (Qur'on matni `quran-mushaf.json`, ixtiyoriy `words-v1.txt`), `fonts/`. Lug'at va NGSL/NAWL ro'yxatlari ilova ichida: `src/js/58-data-lugat.js` (`python3 tools/make_data_js.py` bilan yaratiladi).

## Dizayn qoidalari
- Uch uslub almashtiriladi: **Klassik (standart, o'zgarmaydi)**, Yangi (`html.ui2`), Liquid Glass (`html.ui2.glass`). Yangi qoidalar faqat `src/css/90-ui2.css` va `91-glass.css` da, **hammasi `html.ui2` ostida** (`tests/ui2_check.py` tekshiradi). Klassik ko'rinishni buzma.
- Ranglarni qattiq yozma: CSS o'zgaruvchilaridan ol (`--bg --c1 --ac --go …`). Kontrast avtomatik tekshiriladi (`tests/yangi_dizayn_browser.py`).
- Bugun ekrani standart klassik; Ixcham ko'rinish ixtiyoriy.

## Sinovlar
- Hammasi: `bash tests/run_all.sh` (~10 daqiqa, oxirida "HAMMASI YAXSHI ✅" chiqishi kerak). Brauzer sinovlari Playwright (Chromium), `tests/_pw.py` yordamchi (soxta soat: `Run(..., when=(y,m,d,h,mi,s))`).
- Yangi funksiya = yangi sinov (haqiqiy brauzerda, telefon o'lchamida) va `tests/run_all.sh` ga qo'shish. Dizayn o'zgarsa uchala uslubda (yorug'/qorong'i) gorizontal toshib ketmasligini tekshir.
- Ma'lum tuzoqlar: Playwright `text=` katta-kichik harfga e'tiborsiz va qism qidiradi (aniq matn uchun qo'shtirnoq yoki `:text-is`); `sb` const (sinovda `wdDb()` orqali); formada yozilgan matn bor joyda tanlov bosilganda butun `render()` qilma; global `let/const` to'qnashuvi (`node --check` ushlaydi).

## Chiqarish (deploy)
Repo ildizi = GitHub Pages sayti (`azimov07255/Myself`, `main`). Manba (`src/`, `tools/`, `tests/`, `docs/`, `server-setup/`) ham shu repoda, lekin `tracker/` (yig'ish natijasi) git'ga kirmaydi.
1. `APP_VER` ni oshir (`src/js/01-yadro.js`) va **`src/js/62-yangiliklar.js` dagi `NEWSV` ro'yxatining BOSHIGA shu versiya uchun yozuv qo'sh** (o'zbekcha: nima yangilandi va qayerdan topiladi; `v` = APP_VER, `t` = qisqa xulosa, apostrofsiz; usiz `build_app.py` to'xtaydi), keyin: `python3 tools/build_app.py && bash tests/sync_supabase_folder.sh && python3 tools/make_zips.py`.
2. `bash tests/run_all.sh` yashil bo'lsin ("HAMMASI YAXSHI ✅"). Brauzer sinovlari ishlamasa (Playwright o'rnatilmagan), buni foydalanuvchiga aniq ayt: sinalmagan deb belgila.
3. `python3 tools/deploy_root.py` yig'ilgan fayllarni ildizga nusxalaydi (`index.html`, `version.json`, `sw.js`, `qollanma.html`, ikonlar).
4. Commit qil (qisqa o'zbekcha xabar) va push qil; bulut sessiyada shox + Pull Request ochilsa, foydalanuvchi aytsa `main` ga qo'sh. Pages ~1 daqiqada yangilanadi; Supabase funksiyalari (`supabase/functions/`, `config.toml`) GitHub'dan o'zi deploy bo'ladi.
5. Yangi Supabase secret kerak bo'lsa foydalanuvchiga ayt (o'zing qo'sha olmaysan). Kalitlarni hech qachon faylga yozma.

## Birinchi vazifa (Claude Code'da ilk marta, Windows)
Skriptlarda (`tools/`, `tests/`, `tests/run_all.sh`) `/mnt/user-data/outputs` (loyiha ildizi) va `/tmp` mutlaq yo'llari qattiq yozilgan: Windows'da ular ishlamaydi. Birinchi ish shu:
1. Loyiha ildizini bitta joydan olinadigan qil (masalan Python'da `ROOT = Path(__file__).resolve().parent.parent`, `.sh` da `ROOT=$(cd "$(dirname "$0")/.." && pwd)`), vaqtinchalik fayllar uchun `tempfile`/`$TMPDIR` ishlat. Hamma `/mnt/user-data/outputs` va `/tmp/...` o'rniga shularni qo'y (≈110 fayl: `grep -rl "/mnt/user-data/outputs" tools tests`).
2. Kerakli dasturlar: Python 3.11+, Node.js 20+, `pip install playwright pdfplumber` va `playwright install chromium`. `.sh` skriptlar Git Bash orqali (`bash tests/run_all.sh`).
3. Tekshir: `python tools/build_app.py --check`, so'ng bitta brauzer sinovi (`python tests/yangi_jadval_browser.py`), so'ng hammasi (`bash tests/run_all.sh`, ~15 daqiqa, oxirida "HAMMASI YAXSHI ✅"). Natijani foydalanuvchiga halol ayt.
4. Shundan keyin oddiy ishga o'tish.

## Ish uslubi
- Katta o'zgarishdan oldin qisqa reja ayt, so'ng qil. Har bir o'zgarishdan keyin tegishli sinovni ishga tushir.
- Foydalanuvchi o'zgarishni yoqtirmasa, **eskisini qaytarish va rejim sifatida saqlash** usulini afzal ko'radi (Klassik/Yangi/Glass shu sabab).
- Mualliflik huquqi: Cambridge/Oxford kabi litsenziyali kontentni avtomatik yuklab olma yoki ilovaga ko'chirma; faqat havola, foydalanuvchining o'z natijalari yoki ochiq manbalar (NGSL/NAWL CC BY-SA, Wiktionary).
- Reja: `ROADMAP.md`; arxitektura: `docs/ARCHITECTURE.md`; telefonda sinash ro'yxati: `tests/IPHONE_QA.md`.

## Xavfsizlik qoidalari (buzmaslik uchun)
- **`main` ga to'g'ridan-to'g'ri push qilma.** Avval shox + Pull Request och. Sayt (GitHub Pages) faqat `main` o'zgarganda yangilanadi.
- **Doimiy ruxsat (foydalanuvchidan, 2026-11-14):** har o'zgarishni sinab ko'rgach, Pull Request ochib **o'zing `main` ga qo'sha olasan** (alohida so'ramasdan). Shartlar: har o'zgarish alohida commit/PR; `build_app.py --check` va mumkin bo'lgan sinovlar o'tgan bo'lsin; sinalmagan narsani (iPhone, Playwright yo'q bo'lsa brauzer sinovi) foydalanuvchiga aniq ayt; saqlash/sinxron/zaxira kodiga tegsang alohida ehtiyot bo'l. Foydalanuvchi "qaytar" desa, `Revert` PR och.
- Foydalanuvchining ma'lumoti (Supabase, telefon xotirasi) kodga bog'liq emas: hech qachon ma'lumotni o'chiradigan/qayta yozadigan migratsiya yoki skript ishga tushirma. Zaxira va sinxron kodiga (`src/js/` dagi `syncRem`, `save`, backup) o'zgartirish kiritsang, tegishli sinovni ishga tushir.
- `supabase/config.toml` ishlayotgan holatda; faqat yangi funksiya qo'shilganda o'zgartir va `python3 tests/check_supabase_folder.py` bilan tekshir. Mavjud funksiya nomlarini o'zgartirma.
- Mavjud sayt fayllarini (`index.html`, `sw.js`, `version.json`, `data/`, `fonts/`) faqat `tools/deploy_root.py` orqali yangila, qo'lda tahrir qilma.
- Hech narsa sinalmagan bo'lsa, buni aniq yoz. Xato chiqsa, taxmin bilan ketma-ket "tuzatma"; to'xtab sababini top.
- Orqaga qaytarish: har o'zgarish alohida commit bo'lsin (GitHub'da `Revert` bilan qaytariladi).

## Hozirgi holat va doimiy qoidalar (2026-dekabr)
- **Doimiy qoida (foydalanuvchidan): har yangi yoki o'zgargan xatti-harakatning eskisi Sozlamalar → 🪄 Jilo va qulaylik da tanlanadigan bo'lib qolsin ("har doimgidek").** Yangi sozlamalar `jlSeg('trk_...', standart, [[qiymat, nom], ...])` bilan `jlCardN()` larga qo'shiladi (`88-jilo.js` → `jlCard2/3/4`). Sozlamalar qurilmada (`uiG/uiS`, localStorage `trk_*`).
- **Modul tartibi (`src/js/`)**: `00` xatolar jurnali; `01` yadro (Bugun `hozir()`, `APP_VER`); `07` Qur'on; `08` eslatmalar; `62` yangiliklar (`NEWSV`); `77–79` IELTS kun/reja/javoblar; `80–89` takror, Nafs, Bugun2/3, kashfiyot, ishonch, jilo; `90` vaqt hisobi (`tt*`); `91` ko'p uyqu (`sx*`); `92` eslatma istisnolari (`rmBlk`); `93` Bugun bo'limlari (`bk*`); `94` Cambridge so'zlari (`cb*`); `95` Bugun jadvali 4 (`jd*`, `ag*`, `bz*`). Yangi kod uchun **band bo'lmagan prefiks** tanla (`python3 tests/lint_dupes.py`): `00-xato-jurnal.js` va `docs/ARCHITECTURE.md` ro'yxatiga qarab.
- **Versiya qoidasi:** `build_app.py` faqat `src/js/62-yangiliklar.js` dagi `NEWSV` ning BIRINCHI yozuvi `APP_VER` ga teng bo'lsa yig'adi. `NEWSV` matnida **apostrof (') bo'lmasin** (‘ ’ ishlat). Yangilik oynasida tugma matni ("Hammasi") yozuvlar matnida qaytarilmasin (sinov `text=` qism bo'yicha topadi).
- **Bekor qilish:** o'chirish/o'zgartirish funksiyalari `88-jilo.js` dagi `udWrap` ro'yxatiga qo'shiladi (↩︎ Bekor qilish paneli). Qaytarib bo'lmaydigan narsalar (audio/PDF fayllar, hisob ma'lumoti) qo'shilmaydi.
- **Bir kunlik o'zgarishlar** (`S.ov` — surilgan/qayta tartiblangan, `S.ex` — ko'chirilgan blok) eslatma qatorlariga ta'sir qiladi (`92-eslatma.js`); server qoidasi: sana bilan cheklangan eslatma `kind` i `<asos>@YYYY-MM-DD` ko'rinishida (`tests/yangi_eslatma_browser.py` serverning haqiqiy mantig'ini sinaydi).
- **📚 Cambridge so'zlari:** `cambridge-sozlar.json` (uchinchi shaxs mehnati) **repoga, saytga, do'stlar versiyasiga tushmaydi**; foydalanuvchi uni ilovada import qiladi (qurilma IndexedDB + shaxsiy yopiq Supabase bucket, SQL: `server-setup/cambridge-storage.sql`). Uni yaratuvchi: `tools/build_cambridge.py <pdf> <chiqish.json>`. Ilova kodiga so'zlar ro'yxatini kiritma (`tests/yangi_cambridge_browser.py` buni tekshiradi).
- **Sinov ishga tushirish tuzoqlari:** `run_all.sh` ni ishga tushirgach ishlayotgan paytda `build_app.py` ni qayta ishga tushirma; tugamay to'xtab qolsa (hukm chiqmasa) qayta ishga tushir. Bir vaqtda bir nechta brauzer sinovini ishga tushirish mumkin. Playwright'da `text=` qism bo'yicha topadi; yangi kartalar `.goal` ichida bo'lsa eski sinovlardagi "birinchi `.goal b`" tekshiruvlariga ta'sir qiladi.
- **Foydalanuvchining haqiqiy qurilmasi (iPhone PWA, Windows oyna) bu yerda yo'q:** sinov faqat Chromium'da. "iPhone'da sinalmagan" deb ayt; `tests/IPHONE_QA.md` va ilovadagi "Xatolar jurnali → iPhone sinov ro'yxati" bor.
