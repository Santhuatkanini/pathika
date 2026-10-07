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

-- Lets dashboard.html / my-listing.html count customers and (if ever needed) show
-- names next to bookings, without opening profiles up to every signed-in visitor.
drop policy if exists "profiles: admins read all" on public.profiles;
create policy "profiles: admins read all"
    on public.profiles for select
    using (exists (select 1 from public.admins where user_id = auth.uid()));

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
-- Admin status lives in the separate `admins` table below instead.

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
-- admins — allow-list of user ids who may reach dashboard.html / my-listing.html /
-- add-tour.html (see initAdminGuard() in app/js/auth.js). Rows are added by hand in
-- the Supabase dashboard Table Editor (service role, bypasses RLS) — there is
-- deliberately NO insert/update/delete policy, so a signed-in customer can check
-- whether THEY are an admin but can never grant themselves admin access.
-- ---------------------------------------------------------------------------
create table if not exists public.admins (
    user_id    uuid primary key references auth.users on delete cascade,
    created_at timestamptz not null default now()
);

alter table public.admins enable row level security;

drop policy if exists "admins: read own" on public.admins;
create policy "admins: read own"
    on public.admins for select
    using (auth.uid() = user_id);


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

-- Lets dashboard.html / my-listing.html compute real stats (revenue, bookings this
-- month, per-tour counts) across every customer, not just the admin's own bookings.
drop policy if exists "bookings: admins read all" on public.bookings;
create policy "bookings: admins read all"
    on public.bookings for select
    using (exists (select 1 from public.admins where user_id = auth.uid()));

-- No insert/update/delete policies on purpose: customers must not be able to
-- invent or alter their own bookings.


-- ---------------------------------------------------------------------------
-- tours — admin-added treks, shown alongside the 14 built-in static tour pages.
-- The 14 original tours stay static HTML generated by tools/build_tours.py (fast,
-- SEO-friendly, version-controlled); this table is only for NEW tours an admin adds
-- through add-tour.html after launch, rendered by the client-side tour-view.html.
-- ---------------------------------------------------------------------------
create table if not exists public.tours (
    id            uuid primary key default gen_random_uuid(),
    slug          text not null unique,
    category      text not null
                  check (category in ('western-ghat-treks', 'coastal-treks',
                                       'day-treks', 'backpacking-tours')),
    title         text not null,
    summary       text,
    description   text,
    image_path    text,
    price_inr     numeric(10, 2) check (price_inr >= 0),
    duration_days integer check (duration_days > 0),
    max_people    integer check (max_people > 0),
    created_by    uuid not null references auth.users on delete cascade,
    created_at    timestamptz not null default now()
);

alter table public.tours enable row level security;

-- Tours are public marketing content — anyone can read them, signed in or not.
drop policy if exists "tours: public read" on public.tours;
create policy "tours: public read"
    on public.tours for select
    using (true);

drop policy if exists "tours: admins write" on public.tours;
create policy "tours: admins write"
    on public.tours for insert
    with check (exists (select 1 from public.admins where user_id = auth.uid()));

drop policy if exists "tours: admins update" on public.tours;
create policy "tours: admins update"
    on public.tours for update
    using (exists (select 1 from public.admins where user_id = auth.uid()));

drop policy if exists "tours: admins delete" on public.tours;
create policy "tours: admins delete"
    on public.tours for delete
    using (exists (select 1 from public.admins where user_id = auth.uid()));


-- ---------------------------------------------------------------------------
-- Storage: cover photos for admin-added tours (public bucket, admin-only upload).
-- ---------------------------------------------------------------------------
insert into storage.buckets (id, name, public)
values ('tour-images', 'tour-images', true)
on conflict (id) do nothing;

drop policy if exists "tour-images: public read" on storage.objects;
create policy "tour-images: public read"
    on storage.objects for select
    using (bucket_id = 'tour-images');

drop policy if exists "tour-images: admins upload" on storage.objects;
create policy "tour-images: admins upload"
    on storage.objects for insert
    with check (
        bucket_id = 'tour-images'
        and exists (select 1 from public.admins where user_id = auth.uid())
    );

