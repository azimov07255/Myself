# Telegram botni ulash (taxminan 10 daqiqa)

## 1. Botni yaratish
1. Telegram'da **@BotFather** ni oching → `/newbot`
2. Nom: masalan `Kunlik tizim`; username: oxiri `bot` bilan tugasin, masalan `KunlikTizimBot`
3. BotFather sizga **token** beradi (uzun matn). Uni hech kimga ko'rsatmang.
4. (Ixtiyoriy, chiroyli menyu uchun) BotFather'da `/setcommands` → botni tanlang → quyidagini yuboring:
```
bugun - Bugungi holat
vazifa - Vazifa qo'shish
suv - Bir stakan suv
yordam - Yordam
stop - Botni uzish
```

## 2. Supabase: maxfiy kalitlar (Edge Functions → Secrets)
- `TELEGRAM_BOT_TOKEN` = BotFather bergan token
- `TELEGRAM_WEBHOOK_SECRET` = o'zingiz o'ylab topgan uzun tasodifiy matn (harf, raqam, `_`, `-`; masalan `kt_9fA2xQ7mLp4Zr8Vb1Nc`)

## 3. Ma'lumotlar bazasi
SQL Editor'da `telegram.sql` ni ishga tushiring (oxirgi qatordagi natija: `4` va `1`).
Keyin **alohida so'rov** sifatida (BOT_USERNAME o'rniga o'z botingiz username'ini, @ belgisiz):
```sql
insert into public.app_config(key, value) values ('tg_bot', 'KunlikTizimBot')
  on conflict (key) do update set value = excluded.value;
```

## 4. Funksiyalar
- **Yangi funksiya:** nomi aynan `telegram-bot`, kodi `telegram-bot.ts`. Funksiya sozlamasida **Verify JWT** ni **O'CHIRING** (Telegram o'zi chaqiradi, himoya maxfiy kalit bilan).
- **Mavjud `send-reminders`:** kodini yangi `send-reminders.ts` bilan almashtirib Deploy qiling.

## 5. Webhook'ni yoqish (brauzerda bir marta oching)
Quyidagi manzilda `TOKEN` va `SECRET` ni o'zingiznikiga almashtiring:
```
https://api.telegram.org/botTOKEN/setWebhook?url=https://dsfwagfsehpugjkervqc.supabase.co/functions/v1/telegram-bot&secret_token=SECRET
```
Javob `{"ok":true,"result":true,...}` bo'lishi kerak. (Bu manzilda token bor, hech kimga yubormang.)

## 6. Ilova
`index.html` ni GitHub'ga yuklang → ilovada **Sozlama → Eslatmalar → Telegramga ulash** → Telegram ochiladi → **Start** ni bosing → ilovaga qayting: "Telegram ulandi ✅".

## Tekshirish
- Botga `/bugun` yozing: bugungi holat keladi.
- `/vazifa Kitob o'qish` yozing, ilovani oching: vazifa ro'yxatda paydo bo'ladi.
- Namoz vaqti kelganda botga eslatma keladi, **✅ O'qidim** ni bossangiz, ilovada belgilanadi.

## Muammo bo'lsa
- Bot javob bermasa: webhook javobini (5-qadam) va Edge Functions → telegram-bot → Logs ni tekshiring; Verify JWT o'chiq ekaniga ishonch hosil qiling.
- "Kod eskirgan": ilovada "Telegramga ulash" ni qayta bosing (kod 20 daqiqa amal qiladi).
- Eslatma kelmasa: Sozlama → Eslatmalar'da kerakli turlar (namoz, reja) yoqilganini tekshiring.
