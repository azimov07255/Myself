#!/bin/bash
# Hamma sinovlarni bir buyruqda ishga tushiradi. Ishlatish:  bash tests/run_all.sh
set -u
APP=/mnt/user-data/outputs/tracker/index.html
echo "== src/ va index.html bir xilmi"; python3 /mnt/user-data/outputs/tools/build_app.py --check || exit 1
T=/mnt/user-data/outputs/tests
python3 - <<PY
import re
h=open("$APP",encoding="utf-8").read()
open("/tmp/t.js","w",encoding="utf-8").write(re.findall(r"<script>(.*?)</script>",h,re.S)[0])
PY
node --check /tmp/t.js || { echo "SINTAKSIS XATO"; exit 1; }
echo "== takroriy nomlar"; python3 $T/lint_dupes.py || { echo "TAKRORIY NOMLAR"; exit 1; }
cp -f $T/shot.py /tmp/shot.py
for f in app_gym_test app_ai_test app_tip_test; do cp -f $T/$f.js /tmp/${f/app_/}.js; done
fail=0
echo "== ilova mantiqi"; for f in gym_test ai_test tip_test; do out=$(node /tmp/$f.js 2>&1); n=$(echo "$out" | grep -c '^PASS'); bad=$(echo "$out" | grep -c -E '^FAIL|Error'); echo "$f: $n o'tdi, $bad xato"; [ "$bad" != "0" ] && { echo "$out" | grep -E '^FAIL|Error' | head -3; fail=1; }; done
echo "== sinxronlash va zaxira"; out=$(node $T/sync_test.js 2>&1); echo "sync_test: $(echo "$out" | grep -c '^PASS') o'tdi, $(echo "$out" | grep -c -E '^FAIL|Error') xato"; echo "$out" | grep -E '^FAIL|Error' | head -3; echo "$out" | grep -q -E '^FAIL|Error' && fail=1
echo "== Telegram (ilova)"; out=$(node $T/tg_client_test.js 2>&1); echo "tg_client_test: $(echo "$out" | grep -c '^PASS') o'tdi, $(echo "$out" | grep -c -E '^FAIL|Error') xato"; echo "$out" | grep -q -E '^FAIL|Error' && fail=1
echo "== supabase papkasi"; python3 $T/check_supabase_folder.py || fail=1
echo "== server"; mkdir -p /tmp/esb; (cd /tmp/esb && [ -d node_modules/esbuild ] || (npm init -y >/dev/null 2>&1; npm i esbuild >/dev/null 2>&1))
for f in server_models_test server_resilience_test server_food_voice_test server_plan_test server_ielts_web_test server_ratelimit_test server_telegram_test server_owner_test widget_server_test server_materials_test server_dict_test server_pack_test server_kurs_test server_tts_test server_hikoya_test server_coach_test server_limit_test server_mnemo_test; do cp -f $T/$f.js /tmp/esb/$f.js; out=$(cd /tmp/esb && node $f.js 2>&1); echo "$f: $(echo "$out" | grep -c '^PASS') o'tdi, $(echo "$out" | grep -c -E '^FAIL|Error') xato"; echo "$out" | grep -q -E '^FAIL|Error' && fail=1; done
echo "== Qur'on matni (6236 oyat mustaqil manba bilan solishtiriladi)"; out=$(python3 $T/verify_quran.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== brauzer (telefon o'lchami)"; python3 $T/smoke_browser.py || fail=1
echo "== Yo'l: ochko, seriya, tanga, topshiriq, do'kon (haqiqiy brauzer)"; out=$(python3 $T/rewards_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Hifz: sabaq-sabqi-manzil (haqiqiy brauzer)"; out=$(python3 $T/hifz_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== AI kun rejasi (klient, haqiqiy brauzer)"; out=$(python3 $T/plan_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== AI kun rejasi: ertalabdan kechgacha (klient, haqiqiy brauzer)"; out=$(python3 $T/dayplan_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== AI suhbat: qayta urinish va xatolar (klient)"; out=$(python3 $T/ai_chat_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== CSS sinf nomlari to'qnashmasligi"; python3 $T/check_css_collisions.py || fail=1
echo "== Yig'ish va paketlar (version.json, zip)"; out=$(python3 $T/check_build.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Sifat: yangi versiya xabari, xatolar paneli (haqiqiy brauzer)"; out=$(python3 $T/quality_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS: materiallar, podkast, lug'at kartochkasi, tayyorgarlik paneli (haqiqiy brauzer)"; out=$(python3 $T/ielts_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS: qayta tartib, AI Reading, xatolar daftari, diktant, AI hisoblagich, kontekst (haqiqiy brauzer)"; out=$(python3 $T/ielts_ai_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS: UK/US talaffuz, o'qib berish, so'zma-so'z subtitr, avtomatik transkript (haqiqiy brauzer)"; out=$(python3 $T/ielts_ovoz_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS: B1 + grammar, darajalar, hammasini qo'shish, bulutdagi audio, tahrirlash (haqiqiy brauzer)"; out=$(python3 $T/ielts_edit_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS o'qish: grammar ko'rinishi, sakramaslik, audio joyi, belgilangan ibora (haqiqiy brauzer)"; out=$(python3 $T/ielts_oqish_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Foydalanish statistikasi va hifz xaritasi (haqiqiy brauzer)"; out=$(python3 $T/yangi_statistika_hifz_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== AI murabbiy va havoladan maqola (haqiqiy brauzer)"; out=$(python3 $T/yangi_murabbiy_url_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== So\'z o\'yinlari va matnni audioga moslash (haqiqiy brauzer)"; out=$(python3 $T/yangi_oyin_moslash_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== AI Listening, materialdan savollar, talaffuz (haqiqiy brauzer)"; out=$(python3 $T/yangi12_a_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Writing yordamchilari, parafraza, so\'z oilasi, eksport (haqiqiy brauzer)"; out=$(python3 $T/yangi12_b_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Speaking ko\'rsatkichlari, mock, yo\'l xaritasi, imtihon kuni (haqiqiy brauzer)"; out=$(python3 $T/yangi12_c_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== AI limit yozuvi: egasi cheksiz, haqiqiy limit (haqiqiy brauzer)"; out=$(python3 $T/ai_limit_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Pul va Odat yaxshilanishlari (haqiqiy brauzer)"; out=$(python3 $T/yangi_pul_odat_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Ustun kengligi, dam kuni, zaxira eslatmasi, Ishga tayyormi (haqiqiy brauzer)"; out=$(python3 $T/yangi_tayyorlik_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Hayot paneli, so'rash, Maqsad dvigateli, fokus (haqiqiy brauzer)"; out=$(python3 $T/yangi_hayot_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Kun yakuni, haftalik sharh, odat eslatmasi va arxivi (haqiqiy brauzer)"; out=$(python3 $T/yangi_kun_hafta_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Vidjet: xulosa, yuborish, Scriptable skripti (haqiqiy brauzer)"; out=$(python3 $T/yangi_vidjet_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Ishonchlilik: 1 yillik katta ma'lumot, tezlik, zaxira (haqiqiy brauzer)"; out=$(python3 $T/stress_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Pul: matn bilan tez yozish (haqiqiy brauzer)"; out=$(python3 $T/yangi_pul_tez_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Pul: zakat, sadaqa, sof boylik, dokon foydasi, mehnat narxi (haqiqiy brauzer)"; out=$(python3 $T/yangi_pul_zakat_boylik_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun tepasi: ixcham ko'rinish (haqiqiy brauzer)"; out=$(python3 $T/yangi_bugun_tepa_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Sozlamalar guruhlari, zaxira bir joyda, egasi bo'limi (haqiqiy brauzer)"; out=$(python3 $T/yangi_sozlama_guruh_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Pul nazorati, haftalik sharh tugmasi, yangiliklar (haqiqiy brauzer)"; out=$(python3 $T/yangi_pul2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Qo'llanma sahifasi (haqiqiy brauzer)"; out=$(python3 $T/qollanma_check.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Uyqu, Bugun tuzilishi, kunlik chegara, jamg'arma maqsadlari (haqiqiy brauzer)"; out=$(python3 $T/yangi_uyqu_bugun_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Dizayn qatlami: hamma qoida html.ui2 ostida"; out=$(python3 $T/ui2_check.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Dizayn almashtirish, ranglar kontrasti, matn o'lchami (haqiqiy brauzer)"; out=$(python3 $T/yangi_dizayn_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Materiallar: hamma so'z ma'nosi, kesh, internetdan olish (haqiqiy brauzer)"; out=$(python3 $T/yangi_lugat_internet_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Lug'at qidiruvi: IPA, ovoz, AI, kesh (haqiqiy brauzer)"; out=$(python3 $T/yangi_qidiruv_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Lug'at qidiruvi: avtomatik to'ldirish (haqiqiy brauzer)"; out=$(python3 $T/yangi_takliflar_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS 8+ yo'l xaritasi (haqiqiy brauzer)"; out=$(python3 $T/yangi_yol_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS kursi: reja, strategiya, xatolar daftari (haqiqiy brauzer)"; out=$(python3 $T/yangi_kurs_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Ovoz: pauzali pleyer, ovoz tanlash, AI ovozi (haqiqiy brauzer)"; out=$(python3 $T/yangi_ovoz_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Kurs eslatmalari (haqiqiy brauzer)"; out=$(python3 $T/yangi_eslatma_kurs_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Nima yangilandi? oynasi va izoh (haqiqiy brauzer)"; out=$(python3 $T/yangi_yangilik_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Speaking pauza tahlili (haqiqiy brauzer)"; out=$(python3 $T/yangi_pauza_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Shadowing, takrorlash, matnni yashirish (haqiqiy brauzer)"; out=$(python3 $T/yangi_shadow_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Hafta bossi va seriyani muzlatish (haqiqiy brauzer)"; out=$(python3 $T/yangi_boss_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Til o\'yinlari (haqiqiy brauzer)"; out=$(python3 $T/yangi_til_oyin_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Pomodoro va fon ovozlari (haqiqiy brauzer)"; out=$(python3 $T/yangi_fokus_xat_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Kun hikoyasi va kelajakka xat (haqiqiy brauzer)"; out=$(python3 $T/yangi_hikoya_xat_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Ayat o\'yini (haqiqiy brauzer)"; out=$(python3 $T/yangi_ayat_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Aqlli yordamchi (haqiqiy brauzer)"; out=$(python3 $T/yangi_aqlli_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== AI holati va sarlavhalar (haqiqiy brauzer)"; out=$(python3 $T/yangi_ai_holat_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Hozir nima qilay, brifing, poyga, niyat, bog (haqiqiy brauzer)"; out=$(python3 $T/yangi_kun_yordam_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Natija kartasi, tezlik, xotira saroyi (haqiqiy brauzer)"; out=$(python3 $T/yangi_karta_tezlik_saroy_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Kunlik nasihatchi (haqiqiy brauzer)"; out=$(python3 $T/yangi_nasihat_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun sozlamalari (haqiqiy brauzer)"; out=$(python3 $T/yangi_bugun_sozlama_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Zaxira holati va tiklash (haqiqiy brauzer)"; out=$(python3 $T/yangi_zaxira_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Tezkor yozuv va ro\za (haqiqiy brauzer)"; out=$(python3 $T/yangi_inbox_roza_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Hayot haftalari va stories (haqiqiy brauzer)"; out=$(python3 $T/yangi_hayot_stories_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== IELTS kuni, radar, bashorat (haqiqiy brauzer)"; out=$(python3 $T/yangi_ielts_kun_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Reja: tur, kesishish, siljitish (haqiqiy brauzer)"; out=$(python3 $T/yangi_reja_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Xatolar jurnali va sinov royxati (haqiqiy brauzer)"; out=$(python3 $T/yangi_xato_jurnal_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Cambridge javoblar varagi (haqiqiy brauzer)"; out=$(python3 $T/yangi_javoblar_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Reja 2: bir kunlik reja, oyna, Hozir kartasi, 5 daqiqa (haqiqiy brauzer)"; out=$(python3 $T/yangi_reja2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Nafs bolimi (haqiqiy brauzer)"; out=$(python3 $T/yangi_nafs_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun 2: tablar, 3 soat, suring, yol, kunni yopish (haqiqiy brauzer)"; out=$(python3 $T/yangi_bugun2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun 3: kun tekshiruvi, imtihon yoli, marosim (haqiqiy brauzer)"; out=$(python3 $T/yangi_bugun3_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Takror 2: maqsad, qoshish, trekker, aylanish (haqiqiy brauzer)"; out=$(python3 $T/yangi_takror2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Korsatkichlar va Kashfiyotlar (haqiqiy brauzer)"; out=$(python3 $T/yangi_kashfiyot_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== 604 bet, maqsad avto-progress, tezkor reja, namozda takror (haqiqiy brauzer)"; out=$(python3 $T/yangi_maqsad_namoz_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Ishonchlilik: qoshish, zaxira, server formati (haqiqiy brauzer)"; out=$(python3 $T/yangi_ishonch_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Jilo: bekor qilish, qidiruv, sana (haqiqiy brauzer)"; out=$(python3 $T/yangi_jilo_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Jilo 2: kartalar, Nafs, Quron rejasi (haqiqiy brauzer)"; out=$(python3 $T/yangi_jilo2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Maqsad vaqt hisobi va uyqu (haqiqiy brauzer)"; out=$(python3 $T/yangi_vaqt_uyqu_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Eslatmalar auditi (server mantigi) (haqiqiy brauzer)"; out=$(python3 $T/yangi_eslatma_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun bolimlari, bekor qilish, sanalar (haqiqiy brauzer)"; out=$(python3 $T/yangi_jilo3_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Cambridge sozlari (haqiqiy brauzer)"; out=$(python3 $T/yangi_cambridge_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun jadvali 4 (haqiqiy brauzer)"; out=$(python3 $T/yangi_jadval_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun jadvali: keyingi reja tunda (haqiqiy brauzer)"; out=$(python3 $T/yangi_jadval2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Mulk, keyingi rejalar royxati, Cambridge matn (haqiqiy brauzer)"; out=$(python3 $T/yangi_mulk_cb2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Testlar bolimi (haqiqiy brauzer)"; out=$(python3 $T/yangi_testlar_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Nafs yordami (haqiqiy brauzer)"; out=$(python3 $T/yangi_sos_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Rejimlar (haqiqiy brauzer)"; out=$(python3 $T/yangi_rejimlar_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Kun tartibi: zanjir, Bomdod, til, 5 ta (haqiqiy brauzer)"; out=$(python3 $T/yangi_zanjir_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Bugun: Jadval va Kun bolimlari (haqiqiy brauzer)"; out=$(python3 $T/yangi_bugun_bolim2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Yorliqlar, sinxronlash holati, avto-zaxira (haqiqiy brauzer)"; out=$(python3 $T/yangi_yorliq_zaxira_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Namoz-markazli kun (haqiqiy brauzer)"; out=$(python3 $T/yangi_namoz_kun_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Testlar kengaytmasi (haqiqiy brauzer)"; out=$(python3 $T/yangi_testlar2_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
echo "== Mushaf (haqiqiy brauzer: 604 sahifa, uzoq bosish, sinov)"; out=$(python3 $T/mushaf_browser.py 2>&1); echo "$out" | grep -E '^FAIL|passed'; echo "$out" | grep -q '^FAIL' && fail=1
[ "$fail" = "0" ] && echo "HAMMASI YAXSHI ✅" || echo "XATOLAR BOR ❌"
exit $fail
