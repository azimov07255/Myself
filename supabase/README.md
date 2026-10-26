# Supabase papkasi
Bu papka repo ildizida (`index.html` yonida) turadi. GitHub integratsiyasi (Working directory = `.`) shu yerdagi
funksiyalarni main ga har yuklashda avtomatik Deploy qiladi.

- `functions/<nom>/index.ts` — funksiya kodi
- `config.toml` — qaysi funksiyalar Deploy qilinadi va JWT tekshiruvi (telegram-bot uchun O'CHIQ)
- Migratsiyalar (`migrations/`) ataylab yo'q: ma'lumotlar bazasi SQL fayllarini qo'lda ishga tushirasan.

Kerakli maxfiy qiymatlar (Supabase → Edge Functions → Secrets): GEMINI_API_KEY, OWNER_EMAIL, VAPID_PUBLIC, VAPID_PRIVATE,
VAPID_SUBJECT, CRON_SECRET, TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET (ixtiyoriy: GEMINI_MODEL, YOUTUBE_API_KEY).

