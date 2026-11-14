-- Vidjet (iPhone, Scriptable) uchun: SQL Editor'da BIR MARTA ishga tushiring
create table if not exists widget_snap (
  user_id uuid primary key references auth.users(id) on delete cascade,
  token text unique not null,
  snap jsonb not null default '{}'::jsonb,
  updated_at timestamptz default now()
);
alter table widget_snap enable row level security;
drop policy if exists "own widget" on widget_snap;
create policy "own widget" on widget_snap for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
