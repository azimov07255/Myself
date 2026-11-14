-- AI tezlik sinovi: Gemini'ning o'zi qancha vaqt ketkazayotganini o'lchaydi.
-- Avval ai-assistant funksiyasini YANGI kod bilan qayta Deploy qiling.

-- 1-qadam: so'rov yuborish (timeout 90 soniya, sinov sekin bo'lishi mumkin)
select net.http_post(
  url := 'https://dsfwagfsehpugjkervqc.supabase.co/functions/v1/ai-assistant',
  headers := jsonb_build_object(
    'Content-Type', 'application/json',
    'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRzZndhZ2ZzZWhwdWdqa2VydnFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3MjcwNTksImV4cCI6MjEwODMwMzA1OX0.-fUlJz-VU3Y3_PkpfHsbFkCFsRTCBeJJ5qXs-ZiAMq8'
  ),
  body := '{"action":"health","test":true}'::jsonb,
  timeout_milliseconds := 90000
) as request_id;

-- 2-qadam: 10-60 soniyadan keyin (shuni alohida ishga tushiring). Eslatma javoblarini chiqarib tashlaymiz:
select id, status_code, left(content, 1500) as content
from net._http_response
where content like '%"picked"%'
order by id desc
limit 1;

-- Natijani o'qish: "picked" - funksiya sizning kalitingiz uchun tanlagan modellar (birinchisi ishlatiladi).
-- "speed" ro'yxatida har modelning "ms" (millisekund) qiymati bor.
--   1000-5000 ms   -> Gemini tez ishlayapti, sekinlik boshqa joyda (ilovaga yuborib, "⏱" yozuvini ayting)
--   10000+ ms yoki "err" -> Gemini'ning o'zi sekin/band: natijani yuboring, boshqa modelni sinaymiz
