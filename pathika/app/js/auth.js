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
            account.setAttribute('data-account-menu', '');
            var link = document.createElement('a');
            link.href = ACCOUNT_HOME;
            var icon = document.createElement('i');
            icon.className = 'icon-user-1-1';
            var label = document.createElement('span');
            label.textContent = firstName(session.user); // user-supplied: never innerHTML
            link.appendChild(icon);
            link.appendChild(label);
            account.appendChild(link);

            var out = document.createElement('li');
            out.setAttribute('data-account-menu', '');
            var outLink = document.createElement('a');
            outLink.href = '#';
            outLink.textContent = 'Log out';
            outLink.addEventListener('click', function (event) {
                event.preventDefault();
                signOut();
            });
            out.appendChild(outLink);

            if (signInItem) { signInItem.remove(); }
            list.appendChild(account);
            list.appendChild(out);
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
        initSignedInRedirect();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
