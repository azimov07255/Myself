-- 1-qadam: jadvallar (SQL Editor'da ishga tushiring)
create table if not exists push_subs (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  endpoint text unique not null,
  p256dh text not null,
  auth text not null,
  created_at timestamptz default now()
);
create table if not exists reminders (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users(id) on delete cascade,
  hhmm text not null,
  days int[] not null,
  title text not null,
  body text default '',
  tz int default 300,
  last_sent text
);
alter table push_subs enable row level security;
alter table reminders enable row level security;
create policy "own subs" on push_subs for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own rems" on reminders for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
