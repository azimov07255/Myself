-- Obuna va to'lovlar tizimi (SQL Editor'da ishga tushiring)
create table if not exists profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  name text default '',
  lifetime boolean not null default false,
  expires_at timestamptz,
  blocked boolean not null default false,
  created_at timestamptz default now()
);
create table if not exists payments (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete set null,
  amount bigint not null default 0,
  days int not null default 0,
  created_at timestamptz default now()
);
alter table profiles enable row level security;
alter table payments enable row level security;
drop policy if exists "own profile" on profiles;
create policy "own profile" on profiles for select using (auth.uid() = user_id);

-- Hozirgi hamma foydalanuvchilar (shu jumladan siz) umrbod premium bo'ladi
insert into profiles (user_id, lifetime)
select id, true from auth.users
on conflict (user_id) do nothing;

-- Bloklangan yoki obunasi tugagan foydalanuvchi ma'lumotga kira olmaydi
create or replace function public.is_active() returns boolean
language sql security definer stable set search_path = public as $$
  select not exists (
    select 1 from public.profiles p
    where p.user_id = auth.uid()
      and (p.blocked or (not p.lifetime and (p.expires_at is null or p.expires_at <= now())))
  )
$$;

drop policy if exists "own row" on app_state;
drop policy if exists "own row active" on app_state;
create policy "own row active" on app_state for all
  using (auth.uid() = user_id and public.is_active())
  with check (auth.uid() = user_id and public.is_active());
