"""Wire Supabase accounts into the static pages.

Idempotent — re-run after adding pages. What it does:
  * injects the three auth <script> tags before </body> on every page
  * marks customer pages with data-requires-auth and admin pages with
    data-requires-admin (see supabase/schema.sql for the admins allow-list)
  * turns the dead "Logout" links (href="login.html") into real sign-out buttons
  * regenerates reset-password.html from login.html

Usage:  python tools/build_auth.py

Run this LAST. build_tours.py regenerates the 19 tour pages from scratch and will
drop the script tags, so the order is build_tours -> build_home -> build_blog ->
build_contact -> build_auth.
"""

import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent

# Pages any signed-in customer should reach.
PROTECTED = [
    "my-booking.html",
    "my-favorite.html",
    "my-profile.html",
]

# Pages only an allow-listed admin should reach (customers get bounced to
# my-booking.html — see initAdminGuard() in app/js/auth.js).
ADMIN_PROTECTED = [
    "add-tour.html",
    "dashboard.html",
    "my-listing.html",
]

SCRIPTS = """    <!-- pathika:auth -->
    <script src="app/js/supabase.min.js"></script>
    <script src="app/js/supabase-config.js"></script>
    <script src="app/js/auth.js"></script>
    <!-- /pathika:auth -->
"""

SCRIPTS_RE = re.compile(
    r"[ \t]*<!-- pathika:auth -->.*?<!-- /pathika:auth -->\n", re.DOTALL
)

# Both shapes of dead logout link on the account pages.
LOGOUT_LINK_RE = re.compile(r'<a(\s+)href="login\.html">(\s*)(<i class="icon-turn-off-1">)')
LOGOUT_ITEM_RE = re.compile(r'<a(\s+)href="login\.html">Logout</a>')

# The sidebar on every account page (sidebar-dashboard .db-menu) lists all six pages
# regardless of role; the three admin-only links don't belong on customer pages.
SIDEBAR_ADMIN_ITEM_RE = re.compile(
    r'[ \t]*<li>\s*<a href="(?:dashboard|my-listing|add-tour)\.html">\s*'
    r'<i[^>]*></i>\s*<span>[^<]*</span>\s*</a>\s*</li>\n?'
)

# The template's sidebar "My Profile" item links to my-favorite.html by mistake.
MY_PROFILE_HREF_RE = re.compile(
    r'(<a href=")my-favorite(\.html">\s*<i class="icon-profile-user-1"></i>'
    r'\s*<span>My Profile</span>)'
)


def trim_customer_sidebar(html: str) -> str:
    return SIDEBAR_ADMIN_ITEM_RE.sub("", html)


def fix_my_profile_link(html: str) -> str:
    return MY_PROFILE_HREF_RE.sub(r"\1my-profile\2", html)


def inject_scripts(html: str) -> str:
    # Replace in place when already present, so surrounding whitespace is preserved
    # and re-running cannot drift the file.
    if SCRIPTS_RE.search(html):
        return SCRIPTS_RE.sub(SCRIPTS, html)
    return html.replace("</body>", SCRIPTS + "\n</body>", 1)


BODY_TAG_RE = re.compile(r"<body([^>]*)>")


def mark_body(html: str, attr: str) -> str:
    """Set exactly one data-requires-* marker, replacing any stale one from a
    previous run (a page can move between PROTECTED and ADMIN_PROTECTED)."""
    def repl(match: re.Match) -> str:
        attrs = re.sub(r"\s*data-requires-(?:auth|admin)\b", "", match.group(1))
        return f"<body {attr}{attrs}>"
    return BODY_TAG_RE.sub(repl, html, count=1)


def wire_logout(html: str) -> str:
    html = LOGOUT_LINK_RE.sub(r'<a\1href="#" data-signout>\2\3', html)
    return LOGOUT_ITEM_RE.sub(r'<a\1href="#" data-signout>Logout</a>', html)


RESET_FORM = """<div class="inner-header-login">
                                            <h3 class="title">Choose a new password</h3>
                                            <div class="flex-three">
                                                <p>Pick something you have not used on another site.</p>
                                            </div>
                                        </div>
                                        <form action="#" method="post" id="reset-password" class="login-user" novalidate>
                                            <div class="row">
                                                <div class="col-lg-12">
                                                    <div class="input-wrap">
                                                        <label for="reset-password-field">New password</label>
                                                        <input type="password" id="reset-password-field" name="password"
                                                            placeholder="At least 8 characters*"
                                                            autocomplete="new-password" minlength="8" required>
                                                    </div>
                                                </div>
                                                <div class="col-lg-12">
                                                    <div class="input-wrap">
                                                        <label for="reset-password-confirm">Confirm new password</label>
                                                        <input type="password" id="reset-password-confirm"
                                                            name="password_confirm" placeholder="Repeat your password*"
                                                            autocomplete="new-password" minlength="8" required>
                                                    </div>
                                                </div>
                                                <div class="col-lg-12">
                                                    <p class="auth-message" id="reset-message" role="alert"
                                                        aria-live="polite" hidden></p>
                                                </div>
                                                <div class="col-lg-12 mb-30">
                                                    <button type="submit" class="btn-submit">Save password</button>
                                                </div>
                                                <div class="col-md-12">
                                                    <div class="flex-three">
                                                        <span class="account">Remembered it after all?</span>
                                                        <a href="login.html" class="link-login">Back to sign in</a>
                                                    </div>
                                                </div>
                                            </div>

                                        </form>"""

LOGIN_FORM_RE = re.compile(
    r'<div class="inner-header-login">.*?</form>', re.DOTALL
)


def build_reset_page() -> None:
    """reset-password.html is login.html with the form swapped out."""
    html = (SITE / "login.html").read_text(encoding="utf-8")

    html = html.replace("<title>Login | Pathika</title>",
                        "<title>Reset password | Pathika</title>", 1)
    html = html.replace("<h1 class=\"title\">User Login</h1>",
                        "<h1 class=\"title\">Reset password</h1>", 1)
    html = html.replace("<li><span>User Login</span></li>",
                        "<li><span>Reset password</span></li>", 1)

    html, count = LOGIN_FORM_RE.subn(RESET_FORM, html, count=1)
    if count != 1:
        raise SystemExit("build_auth: could not find the login form in login.html")

    (SITE / "reset-password.html").write_text(html, encoding="utf-8")
    print("  wrote reset-password.html")


def main() -> None:
    build_reset_page()

    for page in sorted(SITE.glob("*.html")):
        original = page.read_text(encoding="utf-8")
        html = inject_scripts(original)
        html = fix_my_profile_link(html)
        if page.name in PROTECTED:
            html = mark_body(html, "data-requires-auth")
            html = wire_logout(html)
            html = trim_customer_sidebar(html)
        elif page.name in ADMIN_PROTECTED:
            html = mark_body(html, "data-requires-admin")
            html = wire_logout(html)
        if html != original:
            page.write_text(html, encoding="utf-8")
            print(f"  patched {page.name}")

    print("build_auth: done")


if __name__ == "__main__":
    main()
