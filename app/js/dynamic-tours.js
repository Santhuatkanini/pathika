/* Appends admin-added tours (public.tours) into the existing static tour-card grids
 * on tours.html and the 4 category pages. No-ops everywhere else (detail pages have
 * no [data-category] row). Relies on window.PATHIKA_SB from app/js/auth.js, which
 * runs first — but wait for DOMContentLoaded regardless, so load order never matters.
 */
(function () {
    'use strict';

    var CATEGORY_NAMES = {
        'western-ghat-treks': 'Western Ghat Treks',
        'coastal-treks': 'Coastal Treks',
        'day-treks': 'Day Treks',
        'backpacking-tours': 'Backpacking Tours'
    };

    function rupees(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency', currency: 'INR', maximumFractionDigits: 0
        }).format(amount);
    }

    function tourCard(tour) {
        var col = document.createElement('div');
        col.className = 'col-sm-6 col-xl-3 mb-32';

        var card = document.createElement('div');
        card.className = 'tour-listing box-sd';

        var page = 'tour-view.html?slug=' + encodeURIComponent(tour.slug);

        var imageLink = document.createElement('a');
        imageLink.href = page;
        imageLink.className = 'tour-listing-image';
        var badgeWrap = document.createElement('div');
        badgeWrap.className = 'badge-top flex-two';
        var badge = document.createElement('span');
        badge.className = 'feature';
        badge.textContent = CATEGORY_NAMES[tour.category] || tour.category;
        badgeWrap.appendChild(badge);
        var img = document.createElement('img');
        img.src = tour.image_path || 'assets/images/favico.png';
        img.alt = tour.title;
        imageLink.appendChild(badgeWrap);
        imageLink.appendChild(img);

        var content = document.createElement('div');
        content.className = 'tour-listing-content';

        var titleEl = document.createElement('h3');
        titleEl.className = 'title-tour-list';
        var titleLink = document.createElement('a');
        titleLink.href = page;
        titleLink.textContent = tour.title;
        titleEl.appendChild(titleLink);

        var iconBox = document.createElement('div');
        iconBox.className = 'icon-box flex-three';
        if (tour.duration_days) {
            var durationWrap = document.createElement('div');
            durationWrap.className = 'icons flex-three';
            var durationIcon = document.createElement('i');
            durationIcon.className = 'icon-time-left';
            var durationSpan = document.createElement('span');
            durationSpan.textContent = tour.duration_days +
                (tour.duration_days === 1 ? ' Day' : ' Days');
            durationWrap.appendChild(durationIcon);
            durationWrap.appendChild(durationSpan);
            iconBox.appendChild(durationWrap);
        }

        var bottom = document.createElement('div');
        bottom.className = 'flex-two';
        var priceBox = document.createElement('div');
        priceBox.className = 'price-box flex-three';
        if (tour.price_inr) {
            var priceP = document.createElement('p');
            var priceSpan = document.createElement('span');
            priceSpan.className = 'price-sale';
            priceSpan.textContent = rupees(tour.price_inr);
            priceP.appendChild(priceSpan);
            priceP.appendChild(document.createTextNode(' per head'));
            priceBox.appendChild(priceP);
        }
        var bookmark = document.createElement('a');
        bookmark.href = page;
        bookmark.className = 'icon-bookmark';
        var bookmarkIcon = document.createElement('i');
        bookmarkIcon.className = 'icon-Vector-151';
        bookmark.appendChild(bookmarkIcon);
        bottom.appendChild(priceBox);
        bottom.appendChild(bookmark);

        content.appendChild(titleEl);
        content.appendChild(iconBox);
        content.appendChild(bottom);

        card.appendChild(imageLink);
        card.appendChild(content);
        col.appendChild(card);
        return col;
    }

    function init() {
        var rows = document.querySelectorAll('.row[data-category]');
        var sb = window.PATHIKA_SB;
        if (!rows.length || !sb) { return; }

        var categories = {};
        rows.forEach(function (row) { categories[row.dataset.category] = row; });

        sb.from('tours').select('*')
            .in('category', Object.keys(categories))
            .order('created_at', { ascending: false })
            .then(function (res) {
                (res.data || []).forEach(function (tour) {
                    var row = categories[tour.category];
                    if (row) { row.appendChild(tourCard(tour)); }
                });
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
