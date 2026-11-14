-- PDF kitoblar uchun shaxsiy bulut ombori (SQL Editor'da ishga tushiring)
insert into storage.buckets (id, name, public, file_size_limit)
values ('books', 'books', false, 52428800)
on conflict (id) do nothing;

drop policy if exists "trk books read" on storage.objects;
drop policy if exists "trk books insert" on storage.objects;
drop policy if exists "trk books update" on storage.objects;
drop policy if exists "trk books delete" on storage.objects;

create policy "trk books read" on storage.objects for select to authenticated
  using (bucket_id = 'books' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "trk books insert" on storage.objects for insert to authenticated
  with check (bucket_id = 'books' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "trk books update" on storage.objects for update to authenticated
  using (bucket_id = 'books' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "trk books delete" on storage.objects for delete to authenticated
  using (bucket_id = 'books' and (storage.foldername(name))[1] = auth.uid()::text);
