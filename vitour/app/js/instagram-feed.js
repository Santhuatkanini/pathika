/*
 * Keeps ".instagram-post-grid" in sync with the latest @_pathika_ posts.
 *
 * Instagram has no public endpoint a static site can read directly, so this
 * reads a Behold JSON feed (https://behold.so/docs/json-feeds) which refreshes
 * itself whenever the account posts. Nothing secret is exposed: the feed URL is
 * a read-only, domain-whitelistable endpoint.
 *
 * Configure the feed URL in app/js/instagram-config.js. With no URL set the
 * grid keeps the static images that are already in the markup.
 */
(function () {
    'use strict';

    var CACHE_KEY = 'pathika:instagram-feed';
    var CACHE_TTL = 15 * 60 * 1000;
    var PROFILE_FALLBACK = 'https://www.instagram.com/_pathika_/';

    function profileUrl() {
        return window.INSTAGRAM_PROFILE_URL || PROFILE_FALLBACK;
    }

    function readCache() {
        try {
            var raw = window.sessionStorage.getItem(CACHE_KEY);
            if (!raw) return null;
            var entry = JSON.parse(raw);
            if (!entry || Date.now() - entry.time > CACHE_TTL) return null;
            return entry.posts;
        } catch (err) {
            return null;
        }
    }

    function writeCache(posts) {
        try {
            window.sessionStorage.setItem(CACHE_KEY, JSON.stringify({ time: Date.now(), posts: posts }));
        } catch (err) {
            /* storage unavailable or full - caching is optional */
        }
    }

    function imageFor(post) {
        var sizes = post.sizes || {};
        var size = sizes.medium || sizes.large || sizes.small || sizes.full;
        return (size && size.mediaUrl) || post.thumbnailUrl || post.mediaUrl || '';
    }

    function captionFor(post) {
        var text = post.altText || post.prunedCaption || post.caption || '';
        return text.length > 120 ? text.slice(0, 117).trim() + '...' : text;
    }

    function render(grid, template, posts) {
        var fragment = document.createDocumentFragment();

        posts.forEach(function (post) {
            var src = imageFor(post);
            if (!src) return;

            var card = template.cloneNode(true);
            var img = card.querySelector('img');
            card.setAttribute('href', post.permalink || profileUrl());
            card.setAttribute('target', '_blank');
            card.setAttribute('rel', 'noopener');
            if (img) {
                img.setAttribute('src', src);
                img.setAttribute('alt', captionFor(post) || 'Instagram post by Pathika');
                img.setAttribute('loading', 'lazy');
            }
            fragment.appendChild(card);
        });

        if (!fragment.childNodes.length) return;
        grid.innerHTML = '';
        grid.appendChild(fragment);
    }

    function init() {
        var grid = document.querySelector('.instagram-post-grid');
        if (!grid) return;

        var tiles = grid.querySelectorAll('.tf-instagram');
        if (!tiles.length) return;

        // The static tiles double as the template and the offline fallback.
        var template = tiles[0].cloneNode(true);
        var limit = tiles.length;
        Array.prototype.forEach.call(tiles, function (tile) {
            if (tile.getAttribute('href') === '#') {
                tile.setAttribute('href', profileUrl());
                tile.setAttribute('target', '_blank');
                tile.setAttribute('rel', 'noopener');
            }
        });

        var feedUrl = window.INSTAGRAM_FEED_URL;
        if (!feedUrl || typeof window.fetch !== 'function') return;

        var cached = readCache();
        if (cached) render(grid, template, cached.slice(0, limit));

        window.fetch(feedUrl, { cache: 'no-cache' })
            .then(function (response) {
                if (!response.ok) throw new Error('Instagram feed responded ' + response.status);
                return response.json();
            })
            .then(function (feed) {
                var posts = (feed && feed.posts) || [];
                if (!posts.length) return;
                writeCache(posts);
                render(grid, template, posts.slice(0, limit));
            })
            .catch(function (err) {
                if (window.console) console.warn('Instagram feed unavailable:', err.message);
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
