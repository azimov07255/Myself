-- =====================================================================
-- ISHONCHLILIK: 1) versiya bilan xavfsiz saqlash  2) avtomatik kunlik zaxira
--               3) xatolar jadvali.   Supabase -> SQL Editor da BIR MARTA ishga tushiring.
-- Bu fayl takror ishga tushirilsa ham xavfsiz (hech narsani o'chirmaydi).
-- =====================================================================

-- 1) Versiya raqami: ikki qurilma bir-birining o'zgarishini bosib yubormasligi uchun
alter table public.app_state add column if not exists rev integer not null default 0;

create or replace function public.save_state(p_data jsonb, p_base integer)
returns jsonb
language plpgsql security definer set search_path = public as $$
declare cur integer; cur_data jsonb;
begin
  if auth.uid() is null then raise exception 'not authenticated'; end if;
  if not public.is_active() then raise exception 'inactive'; end if;
  select rev, data into cur, cur_data from public.app_state where user_id = auth.uid() for update;
  if not found then
    insert into public.app_state(user_id, data, rev, updated_at) values (auth.uid(), p_data, 1, now());
    return jsonb_build_object('ok', true, 'rev', 1);
  end if;
  if p_base is not null and p_base = cur then
    update public.app_state set data = p_data, rev = cur + 1, updated_at = now() where user_id = auth.uid();
    return jsonb_build_object('ok', true, 'rev', cur + 1);
  end if;
  -- boshqa qurilma oraliqda saqlagan: serverdagi nusxani qaytaramiz, ilova ikkalasini birlashtiradi
  return jsonb_build_object('ok', false, 'rev', cur, 'data', cur_data);
end $$;
revoke all on function public.save_state(jsonb, integer) from public;
grant execute on function public.save_state(jsonb, integer) to authenticated;

-- 2) Avtomatik zaxira: har kuni birinchi o'zgarishdan oldingi holat saqlanadi (oxirgi 10 kun).
--    Ma'lumot keskin kichrayib ketsa (buzilish alomati), alohida "shrink" nusxa ham olinadi.
create table if not exists public.app_state_history (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  day date not null,
  kind text not null default 'daily',
  data jsonb not null,
  created_at timestamptz not null default now(),
  unique (user_id, day, kind)
);
alter table public.app_state_history enable row level security;
drop policy if exists "own history read" on public.app_state_history;
create policy "own history read" on public.app_state_history for select using (auth.uid() = user_id);

create or replace function public.snapshot_state() returns trigger
language plpgsql security definer set search_path = public as $$
declare d date := (now() at time zone 'Asia/Tashkent')::date;
begin
  if pg_column_size(old.data) > 300 then
    if not exists (select 1 from public.app_state_history where user_id = old.user_id and day = d and kind = 'daily') then
      insert into public.app_state_history(user_id, day, kind, data) values (old.user_id, d, 'daily', old.data);
      delete from public.app_state_history where user_id = old.user_id and day < d - 10;
    end if;
    if pg_column_size(old.data) > 4000 and pg_column_size(new.data) < pg_column_size(old.data) * 0.6 then
      insert into public.app_state_history(user_id, day, kind, data) values (old.user_id, d, 'shrink', old.data)
      on conflict (user_id, day, kind) do update set data = excluded.data, created_at = now();
    end if;
  end if;
  return new;
end $$;
drop trigger if exists trg_snapshot_state on public.app_state;
create trigger trg_snapshot_state before update on public.app_state
  for each row execute function public.snapshot_state();

-- 3) Xatolar jadvali: foydalanuvchilar telefonida chiqqan xatolar egasiga ko'rinadi
create table if not exists public.client_errors (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  ver text, tab text, msg text, stack text, ua text, standalone boolean
);
alter table public.client_errors enable row level security;
drop policy if exists "errors insert own" on public.client_errors;
create policy "errors insert own" on public.client_errors for insert to authenticated with check (user_id = auth.uid());
-- DIQQAT: pastdagi email egasining emaili (create-user.ts dagi OWNER bilan bir xil bo'lsin)
drop policy if exists "errors owner read" on public.client_errors;
create policy "errors owner read" on public.client_errors for select to authenticated
  using ((auth.jwt() ->> 'email') = 'brodyagayou1999@gmail.com');
drop policy if exists "errors owner delete" on public.client_errors;
create policy "errors owner delete" on public.client_errors for delete to authenticated
  using ((auth.jwt() ->> 'email') = 'brodyagayou1999@gmail.com');

-- Tekshiruv: bu so'rov 3 ta qator qaytarsa (rev, trigger, jadval) hammasi tayyor
select
  (select count(*) from information_schema.columns where table_name='app_state' and column_name='rev') as rev_ustun,
  (select count(*) from pg_trigger where tgname='trg_snapshot_state') as zaxira_trigger,
  (select count(*) from information_schema.tables where table_name='client_errors') as xatolar_jadvali;
