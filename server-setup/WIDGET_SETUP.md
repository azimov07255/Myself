# iPhone vidjeti (Scriptable) — sozlash (bir marta, ~5 daqiqa)

Vidjet ilovadan serverga yozilgan kichik xulosani (odat, namoz, hifz, keyingi reja, IELTS kunlari) o'qiydi. Pul va salomatlik ma'lumoti yuborilmaydi.

1. **Jadval:** Supabase → SQL Editor → `widget.sql` faylidagi kodni qo'yib **Run** bosing.
2. **Funksiya:** `supabase/functions/widget/index.ts` ni GitHub'ga yuklang (boshqa funksiyalar kabi, auto-deploy). Nomi aynan `widget`. "Verify JWT" yoqiq qolsa ham bo'ladi (skript ochiq anon kalitni yuboradi).
3. **Ilova:** Sozlama → 📱 Vidjet → **Vidjetni yoqish**.
4. **iPhone:** App Store'dan **Scriptable** (bepul) → **+** → "Skriptni nusxalash" bilan nusxalangan kodni yopishtiring → nomi: *Kunlik tizim*.
5. Bosh ekranni uzoq bosing → **+** → Scriptable → o'lcham (kichik / o'rta / katta) → vidjetni bosing → *Script* ni tanlang: *Kunlik tizim*.

Eslatmalar:
- iOS vidjetni o'zi belgilagan oraliqda yangilaydi (taxminan 15–60 daqiqa), real vaqt emas.
- Skriptdagi `t=` kaliti sirli. Yo'qolsa: Sozlama → Vidjet → "Kalitni almashtirish" (eski kalit ishlamay qoladi, skriptni qayta nusxalab qo'ying).
- Ilova ochiq bo'lganda xulosa har 2 daqiqada, yopilganda ham yangilanadi.
