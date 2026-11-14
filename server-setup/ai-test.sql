-- AI ni Supabase'ning o'zida tekshirish (SQL Editor). Avval ai-assistant funksiyasini yangi kod bilan qayta Deploy qiling.
-- 1-qadam: funksiyaga so'rov yuborish (anon kalit ochiq kalit, uni ulashish xavfsiz)
select net.http_post(
  url := 'https://dsfwagfsehpugjkervqc.supabase.co/functions/v1/ai-assistant',
  headers := jsonb_build_object(
    'Content-Type', 'application/json',
    'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRzZndhZ2ZzZWhwdWdqa2VydnFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3MjcwNTksImV4cCI6MjEwODMwMzA1OX0.-fUlJz-VU3Y3_PkpfHsbFkCFsRTCBeJJ5qXs-ZiAMq8'
  ),
  body := '{"action":"health"}'::jsonb
) as request_id;

-- 2-qadam: 3-5 soniyadan keyin natijani ko'rish (shuni alohida ishga tushiring)
-- Eslatma funksiyasining har daqiqalik javoblari ({"sent":0}) ro'yxatni to'ldirib turadi, shuning uchun ularni chiqarib tashlaymiz:
select id, status_code, left(content, 700) as content
from net._http_response
where content not like '{"sent":%'
order by id desc
limit 3;

-- Natijani o'qish:
-- status_code 404                -> funksiya yo'q yoki nomi boshqa (aynan: ai-assistant)
-- ok:false, step:"secret"        -> GEMINI_API_KEY secret qo'shilmagan
-- ok:false, step:"gemini"        -> kalit noto'g'ri yoki bekor qilingan (error maydoniga qarang)
-- ok:true va models ro'yxati     -> hammasi tayyor, ro'yxatdagi nomlardan bittasini GEMINI_MODEL qilib qo'yish mumkin
