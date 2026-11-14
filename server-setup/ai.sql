-- AI yordamchi uchun kunlik foydalanish hisobi (SQL Editor'da ishga tushiring)
create table if not exists ai_usage (
  user_id uuid references auth.users(id) on delete cascade,
  day date not null,
  n int not null default 0,
  primary key (user_id, day)
);
-- Siyosat yo'q: faqat server funksiyasi (service role) yozadi va o'qiydi
alter table ai_usage enable row level security;
