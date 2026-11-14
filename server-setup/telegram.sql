-- =====================================================================
-- TELEGRAM BOT: ulash kodlari, bog'langan chatlar, "pochta qutisi", eslatma turi
-- Supabase -> SQL Editor da BIR MARTA ishga tushiring (takror ishga tushirsa ham xavfsiz).
-- =====================================================================

-- 0) Ilova sozlamalari (botning username'ini shu yerdan o'qiydi, index.html ni qayta yuklash shart emas)
create table if not exists public.app_config (key text primary key, value text not null);
alter table public.app_config enable row level security;
drop policy if exists "config read" on public.app_config;
create policy "config read" on public.app_config for select to authenticated using (true);

-- 1) Bog'langan Telegram chatlar (faqat bot yozadi; foydalanuvchi o'qiy va uza oladi)
create table if not exists public.tg_links (
  user_id uuid primary key references auth.users(id) on delete cascade,
  chat_id bigint not null unique,
  username text,
  tz integer not null default 300,
  linked_at timestamptz not null default now()
);
alter table public.tg_links enable row level security;
drop policy if exists "own link read" on public.tg_links;
create policy "own link read" on public.tg_links for select using (auth.uid() = user_id);
drop policy if exists "own link delete" on public.tg_links;
create policy "own link delete" on public.tg_links for delete using (auth.uid() = user_id);

-- 2) Bir martalik ulash kodlari (ilova yaratadi, 20 daqiqa amal qiladi, bot ishlatadi)
create table if not exists public.tg_codes (
  code text primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  tz integer not null default 300,
  expires_at timestamptz not null
);
alter table public.tg_codes enable row level security;
drop policy if exists "own code insert" on public.tg_codes;
create policy "own code insert" on public.tg_codes for insert to authenticated
  with check (user_id = auth.uid() and expires_at <= now() + interval '30 minutes');
drop policy if exists "own code read" on public.tg_codes;
create policy "own code read" on public.tg_codes for select using (auth.uid() = user_id);
drop policy if exists "own code delete" on public.tg_codes;
create policy "own code delete" on public.tg_codes for delete using (auth.uid() = user_id);

-- 3) Pochta qutisi: bot shu yerga yozadi ("namozni o'qidim", "vazifa qo'sh", "suv"), ilova ochilganda qo'llaydi
create table if not exists public.tg_inbox (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  kind text not null,
  payload jsonb not null default '{}',
  created_at timestamptz not null default now(),
  applied boolean not null default false
);
create index if not exists tg_inbox_pending on public.tg_inbox (user_id) where not applied;
alter table public.tg_inbox enable row level security;
drop policy if exists "own inbox read" on public.tg_inbox;
create policy "own inbox read" on public.tg_inbox for select using (auth.uid() = user_id);
drop policy if exists "own inbox delete" on public.tg_inbox;
create policy "own inbox delete" on public.tg_inbox for delete using (auth.uid() = user_id);

-- 4) Eslatma turi (namoz / reja bloki): botdagi "✅ O'qidim" tugmasi uchun
alter table public.reminders add column if not exists kind text not null default '';

-- 5) MUHIM: bot username'ini yozing (@ belgisiz). Quyidagi qatorda BOT_USERNAME ni almashtiring:
-- insert into public.app_config(key, value) values ('tg_bot', 'BOT_USERNAME')
--   on conflict (key) do update set value = excluded.value;

select
  (select count(*) from information_schema.tables where table_name in ('tg_links','tg_codes','tg_inbox','app_config')) as jadvallar_4,
  (select count(*) from information_schema.columns where table_name='reminders' and column_name='kind') as kind_ustun;
