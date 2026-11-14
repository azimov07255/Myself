-- 4-qadam: har daqiqada funksiyani chaqirish (SQL Editor'da ishga tushiring)
create extension if not exists pg_cron;
create extension if not exists pg_net;

select cron.schedule('send-reminders', '* * * * *', $$
  select net.http_post(
    url := 'https://dsfwagfsehpugjkervqc.supabase.co/functions/v1/send-reminders',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRzZndhZ2ZzZWhwdWdqa2VydnFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3MjcwNTksImV4cCI6MjEwODMwMzA1OX0.-fUlJz-VU3Y3_PkpfHsbFkCFsRTCBeJJ5qXs-ZiAMq8',
      'x-cron-secret', '<CRON_SECRET: Supabase Secrets dagi CRON_SECRET qiymati>'
    ),
    body := '{}'::jsonb
  );
$$);
