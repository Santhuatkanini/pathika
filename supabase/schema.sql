-- Pathika — Supabase schema.
-- Run once in the Supabase dashboard: SQL Editor -> New query -> paste -> Run.
-- Safe to re-run.
--
-- Security model: the browser only ever holds the publishable ("anon") key, which is
-- public by design. Every table below has Row Level Security ON, so Postgres itself
-- refuses to return another user's rows regardless of what the client asks for.


-- ---------------------------------------------------------------------------
-- profiles — one row per account, created automatically on sign-up.
-- ---------------------------------------------------------------------------
create table if not exists public.profiles (
    id         uuid primary key references auth.users on delete cascade,
    full_name  text,
    phone      text,
    created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

drop policy if exists "profiles: read own" on public.profiles;
create policy "profiles: read own"
    on public.profiles for select
    using (auth.uid() = id);

drop policy if exists "profiles: update own" on public.profiles;
create policy "profiles: update own"
    on public.profiles for update
    using (auth.uid() = id)
    with check (auth.uid() = id);

-- No INSERT policy: rows are created by the trigger below, which runs as the
-- definer and therefore bypasses RLS. Clients must not be able to forge profiles.
--
-- Deliberately NO is_admin column here. A user can update their own profile row,
-- so an is_admin flag on this table would let anyone grant themselves admin.
-- Admin work happens in the Supabase dashboard, which uses the service role.

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
    insert into public.profiles (id, full_name, phone)
    values (
        new.id,
        new.raw_user_meta_data ->> 'full_name',
        new.raw_user_meta_data ->> 'phone'
    )
    on conflict (id) do nothing;
    return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_user();


-- ---------------------------------------------------------------------------
-- favourites — saved treks. tour_slug matches the static page, e.g. 'kodachadri'
-- for tour-kodachadri.html. Tours stay as generated HTML; only the saves live here.
-- ---------------------------------------------------------------------------
create table if not exists public.favourites (
    user_id    uuid not null references auth.users on delete cascade,
    tour_slug  text not null,
    created_at timestamptz not null default now(),
    primary key (user_id, tour_slug)
);

alter table public.favourites enable row level security;

drop policy if exists "favourites: read own" on public.favourites;
create policy "favourites: read own"
    on public.favourites for select
    using (auth.uid() = user_id);

drop policy if exists "favourites: add own" on public.favourites;
create policy "favourites: add own"
    on public.favourites for insert
    with check (auth.uid() = user_id);

drop policy if exists "favourites: remove own" on public.favourites;
create policy "favourites: remove own"
    on public.favourites for delete
    using (auth.uid() = user_id);


-- ---------------------------------------------------------------------------
-- bookings — read-only for customers. You create these in the Supabase dashboard
-- after a WhatsApp enquiry; the dashboard uses the service role, which bypasses RLS.
-- ---------------------------------------------------------------------------
create table if not exists public.bookings (
    id         uuid primary key default gen_random_uuid(),
    user_id    uuid not null references auth.users on delete cascade,
    tour_slug  text not null,
    tour_name  text not null,
    trek_date  date,
    guests     integer not null default 1 check (guests > 0),
    amount_inr numeric(10, 2) check (amount_inr >= 0),
    status     text not null default 'enquiry'
               check (status in ('enquiry', 'confirmed', 'paid', 'completed', 'cancelled')),
    notes      text,
    created_at timestamptz not null default now()
);

create index if not exists bookings_user_id_idx on public.bookings (user_id, trek_date desc);

alter table public.bookings enable row level security;

drop policy if exists "bookings: read own" on public.bookings;
create policy "bookings: read own"
    on public.bookings for select
    using (auth.uid() = user_id);

-- No insert/update/delete policies on purpose: customers must not be able to
-- invent or alter their own bookings.
