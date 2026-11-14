-- Cambridge so'zlari uchun SHAXSIY yopiq xotira (Supabase → SQL Editor → shu faylni bir marta ishga tushiring).
-- Har foydalanuvchi faqat o'z papkasini ( <user_id>/sozlar.json ) o'qiy/yoza oladi; bucket ochiq EMAS.
insert into storage.buckets (id, name, public) values ('cambridge', 'cambridge', false) on conflict (id) do nothing;

drop policy if exists "cambridge_select_own" on storage.objects;
drop policy if exists "cambridge_insert_own" on storage.objects;
drop policy if exists "cambridge_update_own" on storage.objects;
drop policy if exists "cambridge_delete_own" on storage.objects;

create policy "cambridge_select_own" on storage.objects for select to authenticated
  using (bucket_id = 'cambridge' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "cambridge_insert_own" on storage.objects for insert to authenticated
  with check (bucket_id = 'cambridge' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "cambridge_update_own" on storage.objects for update to authenticated
  using (bucket_id = 'cambridge' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'cambridge' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "cambridge_delete_own" on storage.objects for delete to authenticated
  using (bucket_id = 'cambridge' and (storage.foldername(name))[1] = auth.uid()::text);
