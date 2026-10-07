/* Pathika admin tools — dashboard stats, tours listing, add-tour form.
 * Loaded only on dashboard.html / my-listing.html / add-tour.html by
 * tools/build_auth.py, right after app/js/auth.js (which creates window.PATHIKA_SB).
 * Vanilla JS, no jQuery dependency. Every page here already has data-requires-admin
 * (see initAdminGuard() in auth.js) — RLS is still the real security boundary.
 */
(function () {
    'use strict';

    var sb = window.PATHIKA_SB;
    if (!sb) { return; } // auth.js already shows a "not connected yet" message

    var CATEGORY_NAMES = {
        'western-ghat-treks': 'Western Ghat Treks',
        'coastal-treks': 'Coastal Treks',
        'day-treks': 'Day Treks',
        'backpacking-tours': 'Backpacking Tours'
    };

    function el(id) { return document.getElementById(id); }

    function rupees(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency', currency: 'INR', maximumFractionDigits: 0
        }).format(amount || 0);
    }

    /* ----- dashboard.html ----- */
    function initDashboard() {
        if (!el('stat-revenue')) { return; }

        var now = new Date();
        var monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
            .toISOString().slice(0, 10);
        var today = now.toISOString().slice(0, 10);

        sb.from('bookings')
            .select('tour_name,trek_date,guests,status,amount_inr,created_at')
            .order('created_at', { ascending: false })
            .then(function (res) {
                var bookings = res.data || [];

                var revenue = bookings
                    .filter(function (b) {
                        return ['confirmed', 'paid', 'completed'].indexOf(b.status) !== -1;
                    })
                    .reduce(function (sum, b) { return sum + (Number(b.amount_inr) || 0); }, 0);
                var thisMonth = bookings.filter(function (b) {
                    return b.created_at && b.created_at.slice(0, 10) >= monthStart;
                }).length;
                var upcoming = bookings.filter(function (b) {
                    return b.trek_date && b.trek_date >= today;
                }).length;

                el('stat-revenue').textContent = rupees(revenue);
                el('stat-bookings-month').textContent = String(thisMonth);
                el('stat-upcoming').textContent = String(upcoming);

                var list = el('recent-bookings');
                list.replaceChildren();
                if (!bookings.length) {
                    var empty = document.createElement('li');
                    empty.className = 'comment-by-user';
                    empty.textContent = 'No bookings recorded yet.';
                    list.appendChild(empty);
                    return;
                }
                bookings.slice(0, 8).forEach(function (b) {
                    list.appendChild(recentBookingRow(b));
                });
            });

        sb.from('profiles').select('*', { count: 'exact', head: true }).then(function (res) {
            el('stat-customers').textContent = res.count === null ? '0' : String(res.count);
        });
    }

    function recentBookingRow(booking) {
        var li = document.createElement('li');
        li.className = 'comment-by-user flex-three';

        var content = document.createElement('div');
        content.className = 'content';

        var top = document.createElement('div');
        top.className = 'group-name flex-one';
        var name = document.createElement('div');
        name.className = 'review-name';
        name.textContent = booking.tour_name; // set by the admin, not customer-controlled
        var status = document.createElement('span');
        status.textContent = booking.status.charAt(0).toUpperCase() + booking.status.slice(1);
        top.appendChild(name);
        top.appendChild(status);
        content.appendChild(top);

        var meta = document.createElement('p');
        var guests = booking.guests + (booking.guests === 1 ? ' guest' : ' guests');
        meta.textContent = (booking.trek_date || 'No date set') + ' \u2014 ' + guests;
        content.appendChild(meta);

        li.appendChild(content);
        return li;
    }

    /* ----- my-listing.html: the 14 static tours + any admin-added ones, with real
     * booking counts joined in client-side (small volume, no need for a DB view). */
    function initListing() {
        var grid = el('tours-listing');
        if (!grid) { return; }

        Promise.all([
            fetch('assets/data/tours-manifest.json').then(function (r) { return r.json(); }),
            sb.from('tours').select('*').order('created_at', { ascending: false }),
            sb.from('bookings').select('tour_slug,trek_date')
        ]).then(function (results) {
            var staticTours = results[0];
            var dbTours = (results[1].data || []).map(function (t) {
                return {
                    slug: t.slug,
                    name: t.title,
                    category: t.category,
                    image: t.image_path || 'assets/images/favico.png',
                    page: 'tour-view.html?slug=' + encodeURIComponent(t.slug),
                    static: false
                };
            });

            var stats = {};
            (results[2].data || []).forEach(function (b) {
                var s = stats[b.tour_slug] || { count: 0, last: null };
                s.count += 1;
                if (b.trek_date && (!s.last || b.trek_date > s.last)) { s.last = b.trek_date; }
                stats[b.tour_slug] = s;
            });

            var all = staticTours.concat(dbTours);
            grid.replaceChildren();
            if (!all.length) {
                grid.textContent = 'No tours yet.';
                return;
            }
            all.forEach(function (tour) {
                grid.appendChild(listingCard(tour, stats[tour.slug]));
            });
        }).catch(function () {
            grid.replaceChildren();
            grid.textContent = 'Could not load the tour list right now.';
        });
    }

    function listingCard(tour, stat) {
        var item = document.createElement('div');
        item.className = 'my-listing-item flex-three';

        var imageWrap = document.createElement('div');
        imageWrap.className = 'image relative';
        var img = document.createElement('img');
        img.src = tour.image;
        img.alt = '';
        imageWrap.appendChild(img);
        if (!tour.static) {
            var badge = document.createElement('span');
            badge.className = 'featured';
            badge.textContent = 'Added';
            imageWrap.appendChild(badge);
        }

        var content = document.createElement('div');
        content.className = 'content';

        var top = document.createElement('div');
        top.className = 'flex-two';
        var category = document.createElement('span');
        category.className = 'map';
        category.textContent = CATEGORY_NAMES[tour.category] || tour.category;
        top.appendChild(category);
        content.appendChild(top);

        var title = document.createElement('h6');
        title.className = 'title-listing';
        var link = document.createElement('a');
        link.href = tour.page;
        link.textContent = tour.name;
        title.appendChild(link);
        content.appendChild(title);

        var meta = document.createElement('ul');
        meta.className = 'list-meta flex-three';

        var count = stat ? stat.count : 0;
        var bookingsLi = document.createElement('li');
        var bookingsIcon = document.createElement('i');
        bookingsIcon.className = 'icon-Layer-2';
        var bookingsSpan = document.createElement('span');
        bookingsSpan.textContent = count + (count === 1 ? ' booking' : ' bookings');
        bookingsLi.appendChild(bookingsIcon);
        bookingsLi.appendChild(bookingsSpan);
        meta.appendChild(bookingsLi);

        if (stat && stat.last) {
            var lastLi = document.createElement('li');
            var lastIcon = document.createElement('i');
            lastIcon.className = 'icon-time-left';
            var lastSpan = document.createElement('span');
            lastSpan.textContent = 'Last ' + stat.last;
            lastLi.appendChild(lastIcon);
            lastLi.appendChild(lastSpan);
            meta.appendChild(lastLi);
        }
        content.appendChild(meta);

        item.appendChild(imageWrap);
        item.appendChild(content);
        return item;
    }

    /* ----- add-tour.html ----- */
    function slugify(title) {
        return title.toLowerCase().trim()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    function initAddTour() {
        var form = el('form-add-tour');
        if (!form) { return; }
        var msg = el('add-tour-message');
        var btn = form.querySelector('.btn-submit');
        var idleLabel = btn.innerHTML; // our own static markup, safe to restore verbatim

        function fail(text) {
            btn.disabled = false;
            btn.innerHTML = idleLabel;
            msg.textContent = text;
            msg.hidden = false;
        }

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            msg.hidden = true;
            if (!form.reportValidity()) { return; }

            var title = el('tour-title').value.trim();
            var slug = slugify(title);
            if (!slug) { fail('Please enter a title.'); return; }

            btn.disabled = true;
            btn.textContent = 'Publishing...';

            var photoFile = el('tour-photo').files[0];

            sb.auth.getSession().then(function (res) {
                var session = res.data.session;
                if (!session) { throw new Error('Your session expired. Please sign in again.'); }

                var uploadDone = photoFile
                    ? sb.storage.from('tour-images')
                        .upload(slug + '-' + Date.now() + '.' + photoFile.name.split('.').pop(), photoFile)
                        .then(function (up) {
                            if (up.error) { throw up.error; }
                            return sb.storage.from('tour-images').getPublicUrl(up.data.path).data.publicUrl;
                        })
                    : Promise.resolve(null);

                return uploadDone.then(function (imageUrl) {
                    var price = el('tour-price').value;
                    var duration = el('tour-duration').value;
                    var maxPeople = el('tour-max-people').value;
                    return sb.from('tours').insert({
                        slug: slug,
                        category: el('tour-category').value,
                        title: title,
                        summary: el('tour-summary').value.trim() || null,
                        description: el('tour-description').value.trim(),
                        image_path: imageUrl,
                        price_inr: price ? Number(price) : null,
                        duration_days: duration ? Number(duration) : null,
                        max_people: maxPeople ? Number(maxPeople) : null,
                        created_by: session.user.id
                    });
                });
            }).then(function (res) {
                if (res.error) { throw res.error; }
                location.href = 'my-listing.html';
            }).catch(function (error) {
                fail(error.message || 'Something went wrong. Please try again.');
            });
        });
    }

    function init() {
        initDashboard();
        initListing();
        initAddTour();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
