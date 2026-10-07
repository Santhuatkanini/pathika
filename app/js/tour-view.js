/* Renders an admin-added tour (public.tours) by ?slug=, on the shared tour-view.html
 * shell. Vanilla JS; relies on window.PATHIKA_SB, set by app/js/auth.js which loads
 * first. Public page — no sign-in required to view.
 */
(function () {
    'use strict';

    var CATEGORY_NAMES = {
        'western-ghat-treks': 'Western Ghat Treks',
        'coastal-treks': 'Coastal Treks',
        'day-treks': 'Day Treks',
        'backpacking-tours': 'Backpacking Tours'
    };

    var CATEGORY_PAGES = {
        'western-ghat-treks': 'tours-western-ghat-treks.html',
        'coastal-treks': 'tours-coastal-treks.html',
        'day-treks': 'tours-day-treks.html',
        'backpacking-tours': 'tours-backpacking.html'
    };

    function notFound(body) {
        body.innerHTML = ''; // clearing our own static placeholder, not user input
        var p = document.createElement('p');
        p.className = 'text';
        p.textContent = "We couldn't find that tour. It may have been removed.";
        body.appendChild(p);
    }

    function render(tour) {
        document.title = tour.title + ' | Pathika';
        document.getElementById('tour-view-title').textContent = tour.title;
        document.getElementById('tour-view-breadcrumb').textContent = tour.title;

        var body = document.getElementById('tour-view-body');
        body.innerHTML = ''; // clearing our own static placeholder, not user input

        if (tour.image_path) {
            var hero = document.createElement('img');
            hero.src = tour.image_path;
            hero.alt = tour.title;
            hero.style.width = '100%';
            hero.style.borderRadius = '10px';
            hero.style.marginBottom = '30px';
            body.appendChild(hero);
        }

        var category = document.createElement('p');
        category.className = 'des';
        var categoryLink = document.createElement('a');
        categoryLink.href = CATEGORY_PAGES[tour.category] || 'tours.html';
        categoryLink.textContent = CATEGORY_NAMES[tour.category] || tour.category;
        category.appendChild(categoryLink);
        body.appendChild(category);

        if (tour.summary) {
            var summary = document.createElement('p');
            summary.className = 'text mb-32';
            summary.textContent = tour.summary;
            body.appendChild(summary);
        }

        var facts = [
            tour.price_inr ? '\u20B9' + Number(tour.price_inr).toLocaleString('en-IN') + ' per person' : null,
            tour.duration_days ? tour.duration_days + (tour.duration_days === 1 ? ' day' : ' days') : null,
            tour.max_people ? 'Up to ' + tour.max_people + ' people' : null
        ].filter(Boolean);
        if (facts.length) {
            var list = document.createElement('ul');
            list.className = 'list-term mb-30';
            facts.forEach(function (fact) {
                var li = document.createElement('li');
                var span = document.createElement('span');
                span.textContent = fact;
                li.appendChild(span);
                list.appendChild(li);
            });
            body.appendChild(list);
        }

        if (tour.description) {
            tour.description.split(/\n+/).forEach(function (paragraph) {
                if (!paragraph.trim()) { return; }
                var p = document.createElement('p');
                p.className = 'text mb-25';
                p.textContent = paragraph;
                body.appendChild(p);
            });
        }

        var favourite = document.createElement('button');
        favourite.type = 'button';
        favourite.className = 'btn-submit';
        favourite.style.marginTop = '10px';
        favourite.textContent = '\u2606 Save to favourites';
        favourite.setAttribute('data-favourite-toggle', '');
        favourite.setAttribute('data-tour-slug', tour.slug);
        favourite.setAttribute('data-tour-name', tour.title);
        body.appendChild(favourite);
        if (window.PATHIKA_WIRE_FAVOURITE) { window.PATHIKA_WIRE_FAVOURITE(favourite); }
    }

    function init() {
        var slug = new URLSearchParams(location.search).get('slug');
        var body = document.getElementById('tour-view-body');
        var sb = window.PATHIKA_SB;
        if (!slug || !sb) { notFound(body); return; }

        sb.from('tours').select('*').eq('slug', slug).maybeSingle()
            .then(function (res) {
                if (res.error || !res.data) { notFound(body); return; }
                render(res.data);
            })
            .catch(function () { notFound(body); });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
