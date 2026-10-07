/* Pathika accounts — Supabase email/password + Google sign-in.
 * Loaded on every page by tools/build_auth.py. Vanilla JS, no jQuery dependency.
 */
(function () {
    'use strict';

    var PLACEHOLDER = /YOUR-(PROJECT|PUBLISHABLE)/i;
    var ACCOUNT_HOME = 'my-booking.html';
    var LOGIN_PAGE = 'login.html';
    var HOME_PAGE = 'index.html';

    var cfg = window.PATHIKA_SUPABASE || {};
    var configured = !!(cfg.url && cfg.anonKey &&
        !PLACEHOLDER.test(cfg.url) && !PLACEHOLDER.test(cfg.anonKey));

    // window.supabase is the UMD library; sb is our configured client.
    var sb = (configured && window.supabase)
        ? window.supabase.createClient(cfg.url, cfg.anonKey)
        : null;

    var NOT_SET_UP = 'Accounts are not connected yet. Add your Supabase project ' +
        'details to app/js/supabase-config.js.';

    function el(id) { return document.getElementById(id); }

    function absolute(page) { return new URL(page, location.href).href; }

    /* Only ever redirect to a page on this site — a raw ?next= would be an open redirect. */
    function nextPage() {
        var next = new URLSearchParams(location.search).get('next') || '';
        return /^[\w-]+\.html$/.test(next) ? next : ACCOUNT_HOME;
    }

    function message(node, text, kind) {
        if (!node) { return; }
        node.textContent = text || '';
        node.classList.toggle('is-success', kind === 'success');
        node.hidden = !text;
    }

    function busy(form, on, label) {
        var btn = form.querySelector('.btn-submit');
        if (!btn) { return; }
        btn.disabled = on;
        if (on) {
            btn.dataset.idleLabel = btn.textContent;
            btn.textContent = label;
        } else if (btn.dataset.idleLabel) {
            btn.textContent = btn.dataset.idleLabel;
        }
    }

    function ready(node) {
        if (sb) { return true; }
        message(node, NOT_SET_UP);
        return false;
    }

    function firstName(user) {
        var name = (user.user_metadata && user.user_metadata.full_name) || '';
        return name.trim().split(/\s+/)[0] || user.email;
    }

    function signOut() {
        if (!sb) { return; }
        sb.auth.signOut().then(function () { location.href = HOME_PAGE; });
    }

    /* ----- is this user allow-listed in the admins table? (see supabase/schema.sql) ----- */
    function isAdmin(userId) {
        return sb.from('admins').select('user_id').eq('user_id', userId)
            .maybeSingle()
            .then(function (res) { return !res.error && !!res.data; })
            .catch(function () { return false; });
    }

    /* ----- sign up ----- */
    function initSignUp() {
        var form = el('sign-up');
        if (!form) { return; }
        var msg = el('signup-message');

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            message(msg, '');
            if (!form.reportValidity() || !ready(msg)) { return; }

            busy(form, true, 'Creating account...');
            sb.auth.signUp({
                email: el('signup-email').value.trim(),
                password: el('signup-password').value,
                options: {
                    data: {
                        full_name: el('signup-name').value.trim(),
                        phone: el('signup-phone').value.trim()
                    },
                    emailRedirectTo: absolute(LOGIN_PAGE)
                }
            }).then(function (res) {
                busy(form, false);
                if (res.error) { message(msg, res.error.message); return; }
                if (res.data.session) { location.href = nextPage(); return; }
                form.reset();
                message(msg, 'Almost there — check your inbox for a link to confirm ' +
                    'your email address.', 'success');
            });
        });
    }

    /* ----- sign in ----- */
    function initSignIn() {
        var form = el('login');
        if (!form) { return; }
        var msg = el('login-message');

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            message(msg, '');
            if (!form.reportValidity() || !ready(msg)) { return; }

            busy(form, true, 'Signing in...');
            sb.auth.signInWithPassword({
                email: el('login-email').value.trim(),
                password: el('login-password').value
            }).then(function (res) {
                busy(form, false);
                if (res.error) { message(msg, res.error.message); return; }
                location.href = nextPage();
            });
        });

        var forgot = el('forgot-password');
        if (forgot) {
            forgot.addEventListener('click', function (event) {
                event.preventDefault();
                message(msg, '');
                if (!ready(msg)) { return; }

                var email = el('login-email').value.trim();
                if (!email) {
                    message(msg, 'Enter your email address above, then click ' +
                        'Forgot Password again.');
                    el('login-email').focus();
                    return;
                }
                sb.auth.resetPasswordForEmail(email, {
                    redirectTo: absolute('reset-password.html')
                }).then(function (res) {
                    if (res.error) { message(msg, res.error.message); return; }
                    message(msg, 'If that address has an account, a password reset ' +
                        'link is on its way.', 'success');
                });
            });
        }
    }

    /* ----- choose a new password after following the emailed link ----- */
    function initResetPassword() {
        var form = el('reset-password');
        if (!form) { return; }
        var msg = el('reset-message');

        if (!sb) { message(msg, NOT_SET_UP); return; }

        // The client reads the recovery token out of the URL fragment on load.
        sb.auth.onAuthStateChange(function (event) {
            if (event === 'PASSWORD_RECOVERY') { message(msg, ''); }
        });

        form.addEventListener('submit', function (event) {
            event.preventDefault();
            message(msg, '');
            if (!form.reportValidity()) { return; }

            if (el('reset-password-field').value !== el('reset-password-confirm').value) {
                message(msg, 'Those two passwords do not match.');
                return;
            }

            busy(form, true, 'Saving...');
            sb.auth.getSession().then(function (res) {
                if (!res.data.session) {
                    busy(form, false);
                    message(msg, 'This reset link has expired. Request a new one from ' +
                        'the sign-in page.');
                    return;
                }
                return sb.auth.updateUser({
                    password: el('reset-password-field').value
                }).then(function (update) {
                    busy(form, false);
                    if (update.error) { message(msg, update.error.message); return; }
                    message(msg, 'Password updated. Taking you to your bookings...',
                        'success');
                    setTimeout(function () { location.href = ACCOUNT_HOME; }, 1500);
                });
            });
        });
    }

    /* ----- Google ----- */
    function initGoogle() {
        var btn = el('google-signin');
        if (!btn) { return; }
        var msg = el('login-message') || el('signup-message');

        // signInWithOAuth redirects immediately, so there is no chance to catch an
        // error: a disabled provider would strand the visitor on Supabase's raw JSON.
        // Only show the button once the project confirms Google is actually enabled.
        var block = btn.closest('.col-lg-12') || btn.closest('.input-wrap-social');
        if (block) { block.style.display = 'none'; }

        if (!sb) { return; }

        fetch(cfg.url + '/auth/v1/settings', { headers: { apikey: cfg.anonKey } })
            .then(function (res) { return res.json(); })
            .then(function (settings) {
                if (block && settings.external && settings.external.google === true) {
                    block.style.display = '';
                }
            })
            .catch(function () { /* leave it hidden; email sign-in still works */ });

        btn.addEventListener('click', function () {
            if (!ready(msg)) { return; }
            sb.auth.signInWithOAuth({
                provider: 'google',
                options: { redirectTo: absolute(nextPage()) }
            }).then(function (res) {
                if (res.error) { message(msg, res.error.message); }
            });
        });
    }

    /* ----- header: swap "Sign in" for the account menu ----- */
    function initHeader() {
        document.querySelectorAll('[data-signout]').forEach(function (node) {
            node.addEventListener('click', function (event) {
                event.preventDefault();
                signOut();
            });
        });

        var list = document.querySelector('.header-account .register ul');
        if (!list || !sb) { return; }

        // Tour pages put the "Enquire" WhatsApp button here instead of a sign-in link.
        // Replace a sign-in link, but keep anything else — Enquire is the main CTA.
        var signInLink = list.querySelector('a[href="login.html"]');
        var signInItem = signInLink ? signInLink.closest('li') : null;

        function paint(session) {
            if (!session || list.querySelector('[data-account-menu]')) { return; }

            var account = document.createElement('li');
            account.className = 'account-dropdown';
            account.setAttribute('data-account-menu', '');

            var link = document.createElement('a');
            link.href = ACCOUNT_HOME;
            link.className = 'account-trigger';
            var icon = document.createElement('i');
            icon.className = 'icon-user-1-1';
            var label = document.createElement('span');
            label.textContent = firstName(session.user); // user-supplied: never innerHTML
            link.appendChild(icon);
            link.appendChild(label);

            var submenu = document.createElement('ul');
            submenu.className = 'account-submenu';

            function addItem(href, text, onClick) {
                var li = document.createElement('li');
                var a = document.createElement('a');
                a.href = href;
                a.textContent = text;
                if (onClick) {
                    a.addEventListener('click', function (event) {
                        event.preventDefault();
                        onClick();
                    });
                }
                li.appendChild(a);
                submenu.appendChild(li);
                return li;
            }

            addItem('my-booking.html', 'My Booking');
            addItem('my-profile.html', 'My Profile');
            addItem('#', 'Log out', signOut);

            account.appendChild(link);
            account.appendChild(submenu);

            if (signInItem) { signInItem.remove(); }
            list.appendChild(account);

            // Admins get a quick link to the dashboard too, ahead of Log out.
            isAdmin(session.user.id).then(function (admin) {
                if (!admin) { return; }
                var dashboardItem = addItem('dashboard.html', 'Dashboard');
                submenu.insertBefore(dashboardItem, submenu.lastElementChild);
            });
        }

        sb.auth.getSession().then(function (res) { paint(res.data.session); });
        sb.auth.onAuthStateChange(function (_event, session) { paint(session); });
    }

    /* ----- keep signed-out visitors off the account pages ----- */
    function initGuard() {
        if (!document.body.hasAttribute('data-requires-auth') || !sb) { return; }

        sb.auth.getSession().then(function (res) {
            if (res.data.session) { return; }
            var here = location.pathname.split('/').pop() || ACCOUNT_HOME;
            location.replace(LOGIN_PAGE + '?next=' + encodeURIComponent(here));
        });
    }

    /* ----- keep non-admins off the dashboard/listing/add-tour pages -----
     * A signed-out visitor is sent to login (like initGuard); a signed-in customer
     * who just isn't an admin is bounced to their bookings instead, not login — they
     * don't need to sign in again, they just don't have access to this page.
     */
    function initAdminGuard() {
        if (!document.body.hasAttribute('data-requires-admin') || !sb) { return; }

        sb.auth.getSession().then(function (res) {
            var session = res.data.session;
            if (!session) {
                var here = location.pathname.split('/').pop() || ACCOUNT_HOME;
                location.replace(LOGIN_PAGE + '?next=' + encodeURIComponent(here));
                return;
            }
            isAdmin(session.user.id).then(function (admin) {
                if (!admin) { location.replace(ACCOUNT_HOME); }
            });
        });
    }

    /* ----- my-booking.html: real bookings, or an honest empty state -----
     * bookings only has a SELECT policy (see supabase/schema.sql) — rows are created
     * by hand in the Supabase dashboard, so most new accounts will see none yet.
     */
    function formatDate(value) {
        if (!value) { return 'To be scheduled'; }
        return new Date(value + 'T00:00:00').toLocaleDateString('en-IN', {
            day: '2-digit', month: 'short', year: 'numeric'
        });
    }

    function formatPrice(amount) {
        if (amount === null || amount === undefined) { return ''; }
        return new Intl.NumberFormat('en-IN', {
            style: 'currency', currency: 'INR', maximumFractionDigits: 0
        }).format(amount);
    }

    function bookingRow(booking) {
        var li = document.createElement('li');
        li.className = 'flex-three';

        var main = document.createElement('div');
        main.className = 'booking-list flex-three';
        var image = document.createElement('div');
        image.className = 'image';
        var img = document.createElement('img');
        img.src = 'assets/images/favico.png';
        img.alt = '';
        image.appendChild(img);
        var content = document.createElement('div');
        content.className = 'content';
        var title = document.createElement('h6');
        title.className = 'title-booking';
        title.textContent = booking.tour_name; // from the dashboard, never user-supplied
        content.appendChild(title);
        var price = formatPrice(booking.amount_inr);
        if (price) {
            var priceEl = document.createElement('p');
            priceEl.className = 'price';
            priceEl.textContent = price;
            content.appendChild(priceEl);
        }
        main.appendChild(image);
        main.appendChild(content);

        var status = document.createElement('div');
        status.className = 'booking-list-table';
        var statusText = document.createElement('p');
        statusText.className = 'status';
        statusText.textContent = booking.status.charAt(0).toUpperCase() + booking.status.slice(1);
        status.appendChild(statusText);

        var date = document.createElement('div');
        date.className = 'booking-list-table';
        var dateText = document.createElement('p');
        dateText.className = 'date-gues';
        dateText.textContent = formatDate(booking.trek_date);
        date.appendChild(dateText);

        var guests = document.createElement('div');
        guests.className = 'booking-list-table';
        var guestsText = document.createElement('p');
        guestsText.className = 'date-gues';
        guestsText.textContent = booking.guests + (booking.guests === 1 ? ' Guest' : ' Guests');
        guests.appendChild(guestsText);

        li.appendChild(main);
        li.appendChild(status);
        li.appendChild(date);
        li.appendChild(guests);
        return li;
    }

    function emptyBookingsRow(text) {
        var li = document.createElement('li');
        li.className = 'flex-three';
        var p = document.createElement('p');
        p.textContent = text;
        li.appendChild(p);
        return li;
    }

    function initBookings() {
        var list = el('booking-table-content');
        if (!list || !sb) { return; }

        sb.auth.getSession().then(function (res) {
            var session = res.data.session;
            if (!session) { return; }
            return sb.from('bookings')
                .select('tour_name,trek_date,guests,status,amount_inr')
                .eq('user_id', session.user.id)
                .order('trek_date', { ascending: false });
        }).then(function (result) {
            if (!result) { return; }
            list.replaceChildren();
            if (result.error) {
                list.appendChild(emptyBookingsRow('Could not load your bookings right now.'));
                return;
            }
            if (!result.data.length) {
                list.appendChild(emptyBookingsRow(
                    'No bookings yet — message us on WhatsApp to plan your first trek.'));
                return;
            }
            result.data.forEach(function (booking) { list.appendChild(bookingRow(booking)); });
        });
    }

    /* ----- never show a sign-in form to someone who is already signed in -----
     * Confirmation and OAuth links land back on login.html carrying a session in the
     * URL fragment, which would otherwise leave the visitor staring at a login form.
     */
    function initSignedInRedirect() {
        if (!sb || (!el('login') && !el('sign-up'))) { return; }

        function leave(session) {
            if (session) { location.replace(nextPage()); }
        }
        sb.auth.getSession().then(function (res) { leave(res.data.session); });
        sb.auth.onAuthStateChange(function (_event, session) { leave(session); });
    }

    function init() {
        if (configured && !window.supabase) {
            console.error('Pathika: app/js/supabase.min.js failed to load.');
        }
        initSignUp();
        initSignIn();
        initResetPassword();
        initGoogle();
        initHeader();
        initGuard();
        initAdminGuard();
        initBookings();
        initSignedInRedirect();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
