"""Generate the Pathika tour category and tour detail pages.

Run from the repository root:

    python tools/build_tours.py

Writes static HTML into `pathika/` using the existing Pathika markup and CSS,
and refreshes the "Tours" dropdown in the shared navigation of every page.
"""

from __future__ import annotations

import re
from pathlib import Path

from tours_data import (
    BACKPACKING_CANCELLATION_NOTE,
    CATEGORIES,
    CONTACT,
    FOREST_FEE_NOTE,
    PICKUP_NOTES,
    PICKUP_POINTS,
    TERMS,
    TOURS,
    TREK_CANCELLATION_NOTE,
    TREK_CANCELLATION_POLICY,
    TREK_EXCLUSIONS,
    TREK_PAYMENT_POLICY,
    TREK_THINGS_TO_CARRY,
    WHY_PATHIKA,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT

HUB_PAGE = "tours.html"
WHATSAPP_URL = f"https://wa.me/{CONTACT['phone_intl']}"
MAIL_URL = f"mailto:{CONTACT['email']}"

COPYRIGHT_HTML = (
    '<p class="copy-right">Copyright &copy; Pathika. All Rights Reserved '
    '&nbsp;|&nbsp; <a href="privacy-policy.html">Privacy Policy</a> '
    '&nbsp;|&nbsp; <a href="terms-condition.html">Terms &amp; Condition</a></p>'
)

CATEGORY_BY_SLUG = {c["slug"]: c for c in CATEGORIES}


# --------------------------------------------------------------------------- helpers

def rupees(amount: int) -> str:
    return "Rs " + f"{amount:,}"


def headline_price(tour: dict) -> int:
    """The first tier is always the all-inclusive rate."""
    return tour["prices"][0][0]


def indent(block: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in block.split("\n"))


def li_plain(items) -> str:
    return "\n".join(f"<li>\n    <p>{item}</p>\n</li>" for item in items)


def li_check(items) -> str:
    return "\n".join(
        f'<li class="flex-three">\n    <i class="icon-Vector-7"></i>\n    <p>{item}</p>\n</li>'
        for item in items
    )


def li_dot(items) -> str:
    return "\n".join(
        f'<li class="flex-three">\n    <i class="icon-10"></i>\n    <p>{item}</p>\n</li>'
        for item in items
    )


def split_two(items):
    half = (len(items) + 1) // 2
    return items[:half], items[half:]


# --------------------------------------------------------------------------- chrome

def nav(active: str) -> str:
    """`active` is "tours" or "" and controls the highlighted top-level item."""
    tours_class = "dropdown2 current" if active == "tours" else "dropdown2"
    return f"""<ul class="navigation clearfix">
    <li><a href="index.html">Home</a></li>
    <li class="{tours_class}">
        <a href="{HUB_PAGE}">Tours</a>
        {TOURS_SUBMENU}
    </li>
    <li><a href="blog.html">News</a></li>
    <li><a href="contact-us.html">Contact</a></li>
    <li class="dropdown2"><a href="#">More</a>
        <ul>
            <li><a href="about-us.html">About Us</a></li>
            <li><a href="team.html">Team member</a></li>
            <li><a href="gallery.html">Gallery</a></li>
            <li><a href="terms-condition.html">Terms &amp; Condition</a></li>
            <li><a href="help-center.html">Help center</a></li>
        </ul>
    </li>
</ul>"""


def _tours_submenu() -> str:
    lines = [f'    <li><a href="{HUB_PAGE}">All Tours</a></li>']
    for cat in CATEGORIES:
        lines.append(f'    <li><a href="{cat["page"]}">{cat["name"]}</a></li>')
    return "<ul>\n" + "\n".join(lines) + "\n</ul>"


TOURS_SUBMENU = _tours_submenu()


def head(title: str, description: str) -> str:
    return f"""<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">

<head>
    <meta charset="utf-8">
    <title>{title}</title>

    <meta name="description" content="{description}">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

    <link rel="stylesheet" href="app/css/app.css">
    <link rel="stylesheet" href="app/css/map.min.css">
    <link rel="stylesheet" href="app/css/jquery.fancybox.min.css">

    <!-- Favicon and Touch Icons  -->
    <link rel="shortcut icon" href="assets/images/favico.png">
    <link rel="apple-touch-icon-precomposed" href="assets/images/favico.png">

</head>

<body class="body header-fixed ">

    <div class="preload preload-container">
        <svg class="pl" width="240" height="240" viewBox="0 0 240 240">
            <circle class="pl__ring pl__ring--a" cx="120" cy="120" r="105" fill="none" stroke="#000" stroke-width="20" stroke-dasharray="0 660" stroke-dashoffset="-330" stroke-linecap="round"></circle>
            <circle class="pl__ring pl__ring--b" cx="120" cy="120" r="35" fill="none" stroke="#000" stroke-width="20" stroke-dasharray="0 220" stroke-dashoffset="-110" stroke-linecap="round"></circle>
            <circle class="pl__ring pl__ring--c" cx="85" cy="120" r="70" fill="none" stroke="#000" stroke-width="20" stroke-dasharray="0 440" stroke-linecap="round"></circle>
            <circle class="pl__ring pl__ring--d" cx="155" cy="120" r="70" fill="none" stroke="#000" stroke-width="20" stroke-dasharray="0 440" stroke-linecap="round"></circle>
        </svg>
    </div>

    <!-- /preload -->

    <div id="wrapper">
        <div id="pagee" class="clearfix">
"""


def header_html() -> str:
    return f"""
            <!-- Main Header -->
            <header class="main-header flex">
                <div id="header">
                    <div class="header-top">
                        <div class="header-top-wrap flex-two">
                            <div class="header-top-right">
                                <ul class=" flex-three">
                                    <li class="flex-three">
                                        <i class="icon-mail"></i>
                                        <span>{CONTACT['email']}</span>
                                    </li>
                                    <li class="flex-three">
                                        <i class="icon-phone"></i>
                                        <span>{CONTACT['phone_display']}</span>
                                    </li>
                                </ul>
                            </div>
                            <div class="header-top-left flex-two">
                                <a href="{WHATSAPP_URL}" class="booking" target="_blank" rel="noopener">
                                    <i class="icon-19"></i>
                                    <span>Booking Now</span>
                                </a>
                                <div class="follow-social flex-two">
                                    <span>Follow Us :</span>
                                    <ul class="flex-two">
                                        <li><a href="#"><i class="icon-icon-2"></i></a></li>
                                        <li><a href="#"><i class="icon-icon_03"></i></a></li>
                                        <li><a href="#"><i class="icon-x"></i></a></li>
                                        <li><a href="#"><i class="icon-icon"></i></a></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="header-lower">
                        <div class="tf-container full">
                            <div class="row">
                                <div class="col-lg-12">
                                    <div class="inner-container flex justify-space align-center">
                                        <div class="mobile-nav-toggler mobie-mt mobile-button">
                                            <i class="icon-Vector3"></i>
                                        </div>
                                        <div class="logo-box">
                                            <div class="logo">
                                                <a href="index.html">
                                                    <img src="assets/images/logo2.png" alt="Pathika">
                                                </a>
                                            </div>
                                        </div>
                                        <div class="nav-outer flex align-center">
                                            <nav class="main-menu show navbar-expand-md">
                                                <div class="navbar-collapse collapse clearfix" id="navbarSupportedContent">
{indent(nav('tours'), 36)}
                                                </div>
                                            </nav>
                                        </div>
                                        <div class="header-account flex align-center">
                                            <div class="register">
                                                <ul class="flex align-center">
                                                    <li class="">
                                                        <a href="{WHATSAPP_URL}" target="_blank" rel="noopener"><i class="icon-user-1-1"></i>
                                                            <span>Enquire</span>
                                                        </a>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <a href="#" class="header-sidebar flex-three" data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">
                    <i class="icon-Bars"></i>
                </a>

                <!-- Mobile Menu  -->
                <div class="close-btn"><span class="icon flaticon-cancel-1"></span></div>
                <div class="mobile-menu">
                    <div class="menu-backdrop"></div>
                    <nav class="menu-box">
                        <div class="nav-logo"><a href="index.html">
                                <img src="assets/images/logo2.png" alt=""></a></div>
                        <div class="bottom-canvas">
                            <div class="menu-outer">
                            </div>
                        </div>
                    </nav>
                </div>
                <!-- End Mobile Menu -->

            </header>
            <!-- End Main Header -->
"""


def breadcrumb(title: str, trail, banner: str = None) -> str:
    items = "".join(
        f'\n                                    <li><a href="{href}">{label}</a></li>'
        if href else
        f'\n                                    <li><span>{label}</span></li>'
        for label, href in trail
    )
    style = f' style="background-image: url({banner});"' if banner else ""
    return f"""
                <section class="breadcumb-section"{style}>
                    <div class="tf-container">
                        <div class="row">
                            <div class="col-lg-12 center z-index1">
                                <h1 class="title">{title}</h1>
                                <ul class="breadcumb-list flex-five">{items}
                                </ul>
                                <img class="bcrumb-ab" src="./assets/images/page/mask-bcrumb.png" alt="">
                            </div>
                        </div>
                    </div>
                </section>
"""


def cta_section() -> str:
    return f"""
                <section class="mb--93">
                    <div class="tf-container">
                        <div class="callt-to-action flex-two z-index3 relative">
                            <div class="callt-to-action-content flex-three">
                                <div class="image">
                                    <img src="./assets/images/page/ready.png" alt="Image">
                                </div>
                                <div class="content">
                                    <h2 class="title-call">Ready to adventure and enjoy nature?</h2>
                                    <p class="des">Message us on WhatsApp at {CONTACT['phone_display']} to hold your slot.</p>
                                </div>
                            </div>
                            <img src="./assets/images/page/vector4.png" alt="" class="shape-ab">
                            <div class="callt-to-action-button">
                                <a href="{WHATSAPP_URL}" class="get-call" target="_blank" rel="noopener">Let's get started</a>
                            </div>
                        </div>
                    </div>
                </section>
"""


def footer_html() -> str:
    cat_links = "\n".join(
        f'                                <li>\n'
        f'                                    <a href="{c["page"]}">{c["name"]}</a>\n'
        f'                                </li>'
        for c in CATEGORIES
    )
    gallery = "\n".join(
        f'                                <a href="./assets/images/gallery/gl{i}.jpg" data-fancybox="gallery">\n'
        f'                                    <img src="./assets/images/gallery/gl{i}.jpg" alt="image gallery">\n'
        f'                                </a>'
        for i in range(1, 7)
    )
    return f"""
            <footer class="footer footer-style1">
                <div class="tf-container">
                    <div class="footer-main">
                        <div class="footer-logo">
                            <div class="logo-footer">
                                <img src="./assets/images/logo2.png" alt="">
                            </div>
                            <p class="des-footer">Just like that, we are on our way to everywhere
                                to enliven, enrich and inspire your adventure.
                            </p>
                            <ul class="footer-info">
                                <li class="flex-three">
                                    <i class="icon-noun-mail-5780740-1"></i>
                                    <p>{CONTACT['email']}</p>
                                </li>
                                <li class="flex-three">
                                    <i class="icon-Group-9"></i>
                                    <p>{CONTACT['phone_display']}</p>
                                </li>
                                <li class="flex-three">
                                    <i class="icon-Layer-19"></i>
                                    <p>Bengaluru, Karnataka, India</p>
                                </li>
                            </ul>
                        </div>
                        <div class="footer-service">
                            <h5 class="title">Our Tours</h5>
                            <ul class="footer-menu">
{cat_links}
                                <li>
                                    <a href="contact-us.html">Contact</a>
                                </li>
                            </ul>
                        </div>
                        <div class="footer-gallery">
                            <h5 class="title">Gallery</h5>
                            <div class="gallery-img">
{gallery}
                            </div>
                        </div>
                        <div class="footer-newsletter">
                            <h5 class="title">Newsletter</h5>
                            <form action="/" id="footer-form">
                                <div class="input-wrap flex-three">
                                    <input type="email" placeholder="Enter Email Adress">
                                    <button type="submit"><i class="icon-paper-plane"></i></button>
                                </div>
                                <div class="check-form flex-three">
                                    <i class="icon-Vector-121"></i>
                                    <p>I agree to all your terms and policies</p>
                                </div>
                            </form>
                            <ul class="social-ft flex-three">
                                <li><a href="#"><i class="icon-icon-2"></i></a></li>
                                <li><a href="#"><i class="icon-x"></i></a></li>
                                <li><a href="#"><i class="icon-8"></i></a></li>
                                <li><a href="#"><i class="icon-2"></i></a></li>
                            </ul>
                        </div>
                    </div>

                    <div class="row footer-bottom">
                        <div class="col-md-6">
                            {COPYRIGHT_HTML}
                        </div>
                        <div class="col-md-6">
                            <ul class="social flex-six">
                                <li><a href="#"><i class="icon-icon-2"></i></a></li>
                                <li><a href="#"><i class="icon-x"></i></a></li>
                                <li><a href="#"><i class="icon-8"></i></a></li>
                                <li><a href="#"><i class="icon-6"></i></a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </footer>
"""


def page_tail() -> str:
    return f"""
        </div>
        <!-- /#page -->
    </div>

    <a id="scroll-top" class="button-go"></a>

    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight">
        <div class="offcanvas-header">
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <div class="logo-canvas">
                <img src="./assets/images/logo.png" alt="image">
            </div>
            <p class="des">Just like that, we are on our way to everywhere
                to enliven, enrich and inspire your adventure.
            </p>
            <ul class="canvas-info">
                <li class="flex-three">
                    <i class="icon-noun-mail-5780740-1"></i>
                    <p>{CONTACT['email']}</p>
                </li>
                <li class="flex-three">
                    <i class="icon-Group-9"></i>
                    <p>{CONTACT['phone_display']}</p>
                </li>
                <li class="flex-three">
                    <i class="icon-Layer-19"></i>
                    <p>Bengaluru, Karnataka, India</p>
                </li>
            </ul>
            <ul class="social flex-three">
                <li><a href="#"><i class="icon-icon-2"></i></a></li>
                <li><a href="#"><i class="icon-x"></i></a></li>
                <li><a href="#"><i class="icon-8"></i></a></li>
                <li><a href="#"><i class="icon-6"></i></a></li>
            </ul>
        </div>
    </div>

    <!-- Javascript -->
    <script src="app/js/jquery.min.js"></script>
    <script src="app/js/jquery.nice-select.min.js"></script>
    <script src="app/js/bootstrap.min.js"></script>
    <script src="app/js/swiper-bundle.min.js"></script>
    <script src="app/js/swiper.js"></script>
    <script src="app/js/plugin.js"></script>
    <script src="app/js/jquery.fancybox.js"></script>
    <script src="app/js/map.min.js"></script>
    <script src="app/js/map-config.js"></script>
    <script src="app/js/map.js"></script>
    <script src="app/js/shortcodes.js"></script>
    <script src="app/js/main.js"></script>

</body>

</html>
"""


# --------------------------------------------------------------------------- cards

def tour_card(tour: dict) -> str:
    cat = CATEGORY_BY_SLUG[tour["category"]]
    page = detail_page(tour)
    return f"""<div class="col-sm-6 col-xl-3 mb-32">
    <div class="tour-listing box-sd">
        <a href="{page}" class="tour-listing-image">
            <div class="badge-top flex-two">
                <span class="feature">{cat['name']}</span>
            </div>
            <img src="{tour['image']}" alt="{tour['name']}">
        </a>
        <div class="tour-listing-content">
            <span class="map"><i class="icon-Vector4"></i>{tour['location']}</span>
            <h3 class="title-tour-list"><a href="{page}">{tour['heading']}</a></h3>
            <div class="icon-box flex-three">
                <div class="icons flex-three">
                    <i class="icon-time-left"></i>
                    <span>{tour['duration']}</span>
                </div>
                <div class="icons flex-three">
                    <i class="icon-hiking-1-1"></i>
                    <span>{tour['difficulty']}</span>
                </div>
            </div>
            <div class="flex-two">
                <div class="price-box flex-three">
                    <p><span class="price-sale">{rupees(headline_price(tour))}</span> per head</p>
                </div>
                <a href="{page}" class="icon-bookmark"><i class="icon-Vector-151"></i></a>
            </div>
        </div>
    </div>
</div>"""


def category_card(cat: dict, count: int) -> str:
    return f"""<div class="col-sm-6 col-xl-3 mb-32">
    <div class="tour-listing box-sd">
        <a href="{cat['page']}" class="tour-listing-image">
            <div class="badge-top flex-two">
                <span class="feature">{count} {'Tour' if count == 1 else 'Tours'}</span>
            </div>
            <img src="{cat['image']}" alt="{cat['name']}">
        </a>
        <div class="tour-listing-content">
            <span class="map"><i class="icon-Vector4"></i>{cat['tagline']}</span>
            <h3 class="title-tour-list"><a href="{cat['page']}">{cat['name']}</a></h3>
            <p class="des">{cat['blurb']}</p>
            <div class="flex-two">
                <div class="price-box flex-three">
                    <p><a href="{cat['page']}" class="text-main">View all {count} &rarr;</a></p>
                </div>
            </div>
        </div>
    </div>
</div>"""


# --------------------------------------------------------------------------- detail page

def detail_page(tour: dict) -> str:
    return f"tour-{tour['slug']}.html"


def price_widget(tour: dict) -> str:
    rows = "\n".join(
        f"""                                                            <div class="flex-two mb-15">
                                                                <p>{label}</p>
                                                                <span class="total text-main">{rupees(amount)}</span>
                                                            </div>"""
        for amount, label in tour["prices"]
    )
    note = ""
    if tour.get("price_note"):
        note = f"""
                                                        <p class="des mb-30">{tour['price_note']}</p>"""
    return f"""                                                    <div class="sidebar-widget">
                                                        <h6 class="block-heading">Package Cost</h6>
                                                        <div class="input-wrap-sellect mb-30">
                                                            <span class="label">Per head:</span>
{rows}
                                                        </div>{note}
                                                        <a href="{WHATSAPP_URL}" class="get-call" target="_blank" rel="noopener">Book on WhatsApp</a>
                                                    </div>"""


def facts_widget(tour: dict) -> str:
    rows = "\n".join(
        f"""                                                            <li class="flex-three">
                                                                <i class="icon-Vector-7"></i>
                                                                <span>{label}</span>
                                                            </li>"""
        for label in [
            f"Duration: {tour['duration']}",
            f"Difficulty: {tour['difficulty']}",
            f"Trail: {tour['distance']}",
            f"Region: {tour['location']}",
        ]
    )
    return f"""                                                    <div class="sidebar-widget">
                                                        <h6 class="block-heading">At a Glance</h6>
                                                        <ul class="category-confidence">
{rows}
                                                        </ul>
                                                    </div>"""


def contact_widget() -> str:
    return f"""                                                    <div class="sidebar-widget">
                                                        <h6 class="block-heading">Talk to Us</h6>
                                                        <ul class="category-confidence">
                                                            <li class="flex-three">
                                                                <i class="icon-customer-service-1"></i>
                                                                <span><a href="{WHATSAPP_URL}" target="_blank" rel="noopener">WhatsApp {CONTACT['phone_display']}</a></span>
                                                            </li>
                                                            <li class="flex-three">
                                                                <i class="icon-noun-mail-5780740-1"></i>
                                                                <span><a href="{MAIL_URL}">{CONTACT['email']}</a></span>
                                                            </li>
                                                            <li class="flex-three">
                                                                <i class="icon-Vector-6"></i>
                                                                <span>Instagram: {CONTACT['instagram']}</span>
                                                            </li>
                                                            <li class="flex-three">
                                                                <i class="icon-price-tag-1-1"></i>
                                                                <span>Over 7 years of hosting travellers</span>
                                                            </li>
                                                        </ul>
                                                    </div>"""


def related_widget(tour: dict) -> str:
    siblings = [t for t in TOURS if t["category"] == tour["category"] and t["slug"] != tour["slug"]][:3]
    if not siblings:
        return ""
    cat = CATEGORY_BY_SLUG[tour["category"]]
    rows = "\n".join(
        f"""                                                            <div class="list-recent flex-three">
                                                                <a href="{detail_page(s)}" class="recent-image">
                                                                    <img src="{s['image']}" alt="{s['name']}">
                                                                </a>
                                                                <div class="recent-info">
                                                                    <h4 class="title">
                                                                        <a href="{detail_page(s)}">{s['heading']}</a>
                                                                    </h4>
                                                                    <p>From <span class="text-main">{rupees(headline_price(s))}</span></p>
                                                                </div>
                                                            </div>"""
        for s in siblings
    )
    return f"""                                                    <div class="sidebar-widget">
                                                        <h4 class="block-heading">More {cat['name']}</h4>
                                                        <div class="recent-post-list">
{rows}
                                                        </div>
                                                    </div>"""


def sidebar(tour: dict) -> str:
    parts = [price_widget(tour), facts_widget(tour), contact_widget(), related_widget(tour)]
    return """                            <div class="col-lg-4">
                                <div class="side-bar-right">
""" + "\n".join(p for p in parts if p) + """
                                </div>
                            </div>"""


def overview_tab(tour: dict) -> str:
    cat = CATEGORY_BY_SLUG[tour["category"]]

    intro = "\n".join(
        f'                                                        <p class="des mb-18">{p}</p>'
        for p in tour["intro"]
    )

    facts = "\n".join(
        f"""                                                        <div class="expect flex-three">
                                                            <span>{label}</span>
                                                            <p>{value}</p>
                                                        </div>"""
        for label, value in tour["facts"]
    )

    inc_a, inc_b = split_two(tour["inclusions"])
    exclusions = tour.get("exclusions") or TREK_EXCLUSIONS

    hotels_block = ""
    if tour.get("hotels"):
        rows = "\n".join(
            f"""                                                        <div class="expect flex-three">
                                                            <span>{city}</span>
                                                            <p>{hotel}</p>
                                                        </div>"""
            for city, hotel in tour["hotels"]
        )
        hotels_block = f"""
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-18">Proposed Stays</h4>
{rows}
                                                    </div>"""

    carry = tour.get("things_to_carry", TREK_THINGS_TO_CARRY)
    carry_block = ""
    if carry:
        carry_a, carry_b = split_two(carry)
        carry_block = f"""
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-40">Things to Carry</h4>
                                                        <p class="des mb-18">Your trash comes back from the trail with you.</p>
                                                        <div class="row">
                                                            <div class="col-md-6">
                                                                <ul class="listing-icon">
{indent(li_dot(carry_a), 68)}
                                                                </ul>
                                                            </div>
                                                            <div class="col-md-6">
                                                                <ul class="listing-icon">
{indent(li_dot(carry_b), 68)}
                                                                </ul>
                                                            </div>
                                                        </div>
                                                    </div>"""

    return f"""                                    <div class="tab-pane fade show active" id="pills-overview" role="tabpanel"
                                        aria-labelledby="pills-overview-tab" tabindex="0">
                                        <div class="row mb-50">
                                            <div class="col-lg-12">
                                                <div class="inner-heading-wrap flex-two">
                                                    <div class="inner-heading">
                                                        <span class="feature">{cat['name']}</span>
                                                        <h2 class="title">{tour['heading']}</h2>
                                                        <ul class="flex-three list-wrap-heading">
                                                            <li class="flex-three">
                                                                <i class="icon-time-left"></i>
                                                                <span>{tour['duration']}</span>
                                                            </li>
                                                            <li class="flex-three">
                                                                <i class="icon-hiking-1-1"></i>
                                                                <span>{tour['difficulty']}</span>
                                                            </li>
                                                            <li class="flex-three">
                                                                <i class="icon-18"></i>
                                                                <span>{tour['location']}</span>
                                                            </li>
                                                        </ul>
                                                    </div>
                                                    <div class="inner-price">
                                                        <p class="price-sale text-main">{rupees(headline_price(tour))} <span class="price">per head</span></p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row mb-40 image-gallery-single">
                                            <div class="col-12 col-sm-6">
                                                <img src="{tour['gallery'][0]}" alt="{tour['name']}">
                                            </div>
                                            <div class="col-6 col-sm-3">
                                                <img src="{tour['gallery'][1]}" alt="{tour['name']}">
                                            </div>
                                            <div class="col-6 col-sm-3">
                                                <img src="{tour['gallery'][2]}" alt="{tour['name']}">
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-lg-8">
                                                <div class="information-content-tour">
                                                    <div class="description-wrap mb-40">
                                                        <span class="description">About {tour['name']}</span>
{intro}
                                                    </div>
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-18">Trek Facts</h4>
{facts}
                                                    </div>
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-40">Included</h4>
                                                        <div class="row">
                                                            <div class="col-md-6">
                                                                <ul class="listing-clude">
{indent(li_check(inc_a), 68)}
                                                                </ul>
                                                            </div>
                                                            <div class="col-md-6">
                                                                <ul class="listing-clude">
{indent(li_check(inc_b), 68)}
                                                                </ul>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-40">Not Included</h4>
                                                        <ul class="listing-des">
{indent(li_plain(exclusions), 60)}
                                                        </ul>
                                                    </div>{hotels_block}{carry_block}
                                                </div>
                                            </div>
{sidebar(tour)}
                                        </div>
                                    </div>"""


def itinerary_tab(tour: dict) -> str:
    blocks = []
    for i, (day, label, bullets) in enumerate(tour["itinerary"], start=1):
        blocks.append(f"""                                                    <div class="tour-planing-section flex">
                                                        <div class="number-box flex-five">{i:02d}</div>
                                                        <div class="content-box">
                                                            <h5 class="title">{day}: {label}</h5>
                                                            <ul class="listing-des">
{indent(li_plain(bullets), 64)}
                                                            </ul>
                                                        </div>
                                                    </div>""")
    return f"""                                    <div class="tab-pane fade" id="pills-itinerary" role="tabpanel"
                                        aria-labelledby="pills-itinerary-tab" tabindex="0">
                                        <div class="row">
                                            <div class="col-lg-8">
                                                <div class="planing-content-tour">
                                                    <h3 class="title-plan">Day by Day Plan</h3>
                                                    <p class="des mb-25">Timings are indicative. Departure dates are
                                                        announced per batch &mdash; message us for the current schedule.</p>
{chr(10).join(blocks)}
                                                </div>
                                            </div>
{sidebar(tour)}
                                        </div>
                                    </div>"""


def location_tab(tour: dict) -> str:
    lat, lng = tour["coords"]

    if tour.get("pickup", True):
        points = "\n".join(
            f'                                                            <li>\n'
            f'                                                                <p>{p}</p>\n'
            f'                                                            </li>'
            for p in PICKUP_POINTS
        )
        notes = "\n".join(
            f'                                                        <p class="des mb-18">{n}</p>'
            for n in PICKUP_NOTES
        )
        reach = f"""{notes}
                                                    <p class="des mb-18">Pickup points from Bengaluru:</p>
                                                    <ul class="listing-des mb-25">
{points}
                                                    </ul>
                                                    <p class="des">{tour['own_transport']}</p>"""
    else:
        reach = "\n".join(
            f'                                                    <p class="des mb-18">{n}</p>'
            for n in tour["arrival"]
        )

    return f"""                                    <div class="tab-pane fade" id="pills-location" role="tabpanel"
                                        aria-labelledby="pills-location-tab" tabindex="0">
                                        <div class="row">
                                            <div class="col-lg-8">
                                                <div class="localtion-content-tour">
                                                    <div class="map2 relative mb-32">
                                                        <div id="map2" data-lat="{lat}" data-lng="{lng}" data-zoom="9"></div>
                                                    </div>
                                                    <div class="flex-three map-list mb-50">
                                                        <i class="icon-18"></i>
                                                        <p>{tour['location']} &mdash; {tour['coords_label']}</p>
                                                    </div>
                                                    <h3 class="title-location">How to Reach</h3>
{reach}
                                                </div>
                                            </div>
{sidebar(tour)}
                                        </div>
                                    </div>"""


def policies_tab(tour: dict) -> str:
    payment = tour.get("payment_policy", TREK_PAYMENT_POLICY)
    cancellation = tour.get("cancellation_policy", TREK_CANCELLATION_POLICY)
    cancel_note = tour.get("cancellation_note", TREK_CANCELLATION_NOTE)
    forest = ""
    if tour.get("forest_fee"):
        forest = f"""
                                                        <p class="des mb-18">{FOREST_FEE_NOTE}</p>"""
    why = "\n".join(
        f'                                                        <p class="des mb-18">{p}</p>' for p in WHY_PATHIKA
    )
    return f"""                                    <div class="tab-pane fade" id="pills-policies" role="tabpanel"
                                        aria-labelledby="pills-policies-tab" tabindex="0">
                                        <div class="row">
                                            <div class="col-lg-8">
                                                <div class="information-content-tour">
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-40">Payment Policy</h4>
                                                        <ul class="listing-des">
{indent(li_plain(payment), 60)}
                                                        </ul>
                                                    </div>
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-40">Cancellation &amp; Refund Policy</h4>
                                                        <ul class="listing-des mb-25">
{indent(li_plain(cancellation), 60)}
                                                        </ul>{forest}
                                                        <p class="des">{cancel_note}</p>
                                                    </div>
                                                    <div class="expect-wrap mb-70">
                                                        <h4 class="title mb-40">Terms &amp; Conditions</h4>
                                                        <ul class="listing-des">
{indent(li_plain(TERMS), 60)}
                                                        </ul>
                                                    </div>
                                                    <div class="description-wrap mb-40">
                                                        <span class="description">Why Pathika?</span>
{why}
                                                    </div>
                                                </div>
                                            </div>
{sidebar(tour)}
                                        </div>
                                    </div>"""


def gallery_tab(tour: dict) -> str:
    blocks = "\n\n".join(
        f"""                                                    <div class="image-gallery{i} image">
                                                        <img src="{src}" alt="{tour['name']}" class="item{1 if i % 2 else 2}">
                                                    </div>"""
        for i, src in enumerate(tour["gallery_tab"], start=1)
    )
    return f"""                                    <div class="tab-pane fade" id="pills-gallery" role="tabpanel"
                                        aria-labelledby="pills-gallery-tab" tabindex="0">
                                        <div class="row">
                                            <div class="col-lg-8">
                                                <div class="gallery-content-tour">
{blocks}
                                                </div>
                                            </div>
{sidebar(tour)}
                                        </div>
                                    </div>"""


TABS = [
    ("overview", "Overview", "icon-Vector-51"),
    ("itinerary", "Itinerary", "icon-destination-2-1"),
    ("location", "Location", "icon-map-1"),
    ("policies", "Policies", "icon-favourite-1"),
    ("gallery", "Gallery", "icon-image-gallery-1"),
]


def tab_nav() -> str:
    items = []
    for i, (key, label, icon) in enumerate(TABS):
        active = " active" if i == 0 else ""
        selected = "true" if i == 0 else "false"
        items.append(f"""                                    <li class="nav-item" role="presentation">
                                        <button class="nav-link{active}" id="pills-{key}-tab" data-bs-toggle="pill"
                                            data-bs-target="#pills-{key}" type="button" role="tab"
                                            aria-controls="pills-{key}" aria-selected="{selected}"><i
                                                class="{icon}"></i> {label}</button>
                                    </li>""")
    return "\n".join(items)


def render_detail(tour: dict) -> str:
    cat = CATEGORY_BY_SLUG[tour["category"]]
    title = f"{tour['heading']} with Pathika | {cat['name']}"
    desc = (f"{tour['heading']} &mdash; {tour['duration']}, {tour['difficulty']}. "
            f"Itinerary, inclusions, package cost and booking details from Pathika.")
    desc = re.sub(r"&[a-z]+;", "-", desc)

    body = "\n".join([
        overview_tab(tour),
        itinerary_tab(tour),
        location_tab(tour),
        policies_tab(tour),
        gallery_tab(tour),
    ])

    return (
        head(title, desc)
        + header_html()
        + "            <main id=\"main\">\n"
        + breadcrumb(tour["heading"], [
            ("Home", "index.html"),
            ("Tours", HUB_PAGE),
            (cat["name"], cat["page"]),
            (tour["name"], None),
        ], tour["banner"])
        + f"""
                <section class="tour-single pd-main">
                    <div class="tf-container">
                        <div class="row">
                            <div class="col-lg-12">
                                <ul class="nav justify-content-between tab-tour-single" id="pills-tab" role="tablist">
{tab_nav()}
                                </ul>
                            </div>
                        </div>
                        <div class="row pd-main">
                            <div class="col-lg-12">
                                <div class="tab-content" id="pills-tabContent">
{body}
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
"""
        + cta_section()
        + "\n            </main>\n"
        + footer_html()
        + page_tail()
    )


# --------------------------------------------------------------------------- listing pages

def render_category(cat: dict) -> str:
    tours = [t for t in TOURS if t["category"] == cat["slug"]]
    cards = "\n".join(indent(tour_card(t), 28) for t in tours)
    title = f"{cat['name']} | Pathika"
    return (
        head(title, re.sub(r"&[a-z]+;", "-", cat["blurb"]))
        + header_html()
        + "            <main id=\"main\">\n"
        + breadcrumb(cat["name"], [
            ("Home", "index.html"),
            ("Tours", HUB_PAGE),
            (cat["name"], None),
        ], cat["banner"])
        + f"""
                <section class="archieve-tour pd-main">
                    <div class="tf-container">
                        <div class="row mb-40">
                            <div class="col-lg-8">
                                <h2 class="title">{cat['tagline']}</h2>
                                <p class="des">{cat['blurb']}</p>
                            </div>
                        </div>
                        <div class="row">
{cards}
                        </div>
                    </div>
                </section>
"""
        + cta_section()
        + "\n            </main>\n"
        + footer_html()
        + page_tail()
    )


def render_hub() -> str:
    counts = {c["slug"]: len([t for t in TOURS if t["category"] == c["slug"]]) for c in CATEGORIES}
    cat_cards = "\n".join(indent(category_card(c, counts[c["slug"]]), 28) for c in CATEGORIES)

    sections = []
    for cat in CATEGORIES:
        tours = [t for t in TOURS if t["category"] == cat["slug"]]
        cards = "\n".join(indent(tour_card(t), 28) for t in tours)
        sections.append(f"""
                <section class="archieve-tour pd-main">
                    <div class="tf-container">
                        <div class="row mb-40">
                            <div class="col-lg-8">
                                <h2 class="title">{cat['name']}</h2>
                                <p class="des">{cat['blurb']}</p>
                            </div>
                        </div>
                        <div class="row">
{cards}
                        </div>
                    </div>
                </section>
""")

    return (
        head("Tours | Pathika",
             "All Pathika tours: Western Ghat treks, coastal treks, day treks and backpacking tours.")
        + header_html()
        + "            <main id=\"main\">\n"
        + breadcrumb("Our Tours", [("Home", "index.html"), ("Tours", None)])
        + f"""
                <section class="archieve-tour pd-main">
                    <div class="tf-container">
                        <div class="row mb-40">
                            <div class="col-lg-8">
                                <h2 class="title">Pick your kind of weekend</h2>
                                <p class="des">Every Pathika trip falls into one of four categories. Weekend
                                    treks in the Western Ghats, coastal trails and water sports, single-day
                                    hikes around Bengaluru, and long-format backpacking journeys across India.</p>
                            </div>
                        </div>
                        <div class="row">
{cat_cards}
                        </div>
                    </div>
                </section>
"""
        + "".join(sections)
        + cta_section()
        + "\n            </main>\n"
        + footer_html()
        + page_tail()
    )


# --------------------------------------------------------------------------- nav patch

TOUR_DROPDOWN_RE = re.compile(
    r'<li class="(dropdown2[^"]*)">\s*\n?\s*<a href="[^"]*">Tours?</a>\s*\n?\s*<ul>.*?</ul>',
    re.DOTALL,
)


def patch_existing_nav() -> int:
    """Point the shared "Tour" dropdown at the Pathika tour pages."""
    generated = {detail_page(t) for t in TOURS} | {c["page"] for c in CATEGORIES} | {HUB_PAGE}
    patched = 0
    for path in sorted(OUT_DIR.glob("*.html")):
        if path.name in generated:
            continue
        original = path.read_text(encoding="utf-8")
        updated, n = TOUR_DROPDOWN_RE.subn(
            lambda m: (f'<li class="{m.group(1)}">\n'
                       f'    <a href="{HUB_PAGE}">Tours</a>\n'
                       f'    {TOURS_SUBMENU}'),
            original,
        )
        if n and updated != original:
            path.write_text(updated, encoding="utf-8")
            patched += 1
    return patched


# --------------------------------------------------------------------------- contact details

CONTACT_SWAPS = [
    ("Info@webmail.com", CONTACT["email"]),
    ("Mail Us: Info@Webmail.Com", f"Mail Us: {CONTACT['email']}"),
    ("Info@Webmail.Com", CONTACT["email"]),
    ("support@example.com", CONTACT["email"]),
    ("684 555-0102 490", CONTACT["phone_display"]),
    ("6391 Elgin St. Celina, NYC 10299", "Bengaluru, Karnataka, India"),
    ("Thursday, Mar 26, 2021", "Trekking every weekend"),
    ("Services Req", "Our Tours"),
]

CONTACT_RE_SWAPS = [
    (re.compile(r"The world[\u2019']s first and largest digital market\s*\n?\s*"
                r"for crypto collectibles and non-fungible", re.DOTALL),
     "Just like that, we are on our way to everywhere\n"
     "                                to enliven, enrich and inspire your adventure."),
    (re.compile(r'<p class="copy-right">.*?</p>', re.DOTALL), COPYRIGHT_HTML),
]


def patch_contact_details() -> int:
    """Replace the template's placeholder contact details site-wide."""
    generated = {detail_page(t) for t in TOURS} | {c["page"] for c in CATEGORIES} | {HUB_PAGE}
    patched = 0
    for path in sorted(OUT_DIR.glob("*.html")):
        if path.name in generated:
            continue
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in CONTACT_SWAPS:
            updated = updated.replace(old, new)
        for pattern, new in CONTACT_RE_SWAPS:
            updated = pattern.sub(new, updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            patched += 1
    return patched


# --------------------------------------------------------------------------- shared nav fixes

DESTINATION_NAV_RE = re.compile(
    r'\s*<li class="dropdown2[^"]*">\s*<a href="[^"]*">Destination</a>\s*<ul>.*?</ul>\s*</li>',
    re.DOTALL,
)

# Account pages: now reached from the header-account dropdown (auth.js), which
# already shows the right items for a customer vs. an admin. This public, always-
# visible copy leaked Dashboard/My Listing/Add Tour to every visitor, signed in or not.
DASHBOARD_NAV_RE = re.compile(
    r'\s*<li class="dropdown2[^"]*">\s*<a href="#">Dashboard</a>\s*<ul>.*?</ul>\s*</li>',
    re.DOTALL,
)

BLOG_NAV_RE = re.compile(
    r'<li class="dropdown2([^"]*)">\s*<a href="[^"]*">Blog</a>\s*<ul>.*?</ul>\s*</li>',
    re.DOTALL,
)


def _news_item(match: re.Match) -> str:
    current = ' class="current"' if "current" in match.group(1) else ""
    return f'<li{current}><a href="blog.html">News</a></li>'


PAGES_NAV_RE = re.compile(
    r'[ \t]*<li class="dropdown2([^"]*)">\s*<a href="[^"]*">Pages</a>\s*(<ul>.*?</ul>)\s*</li>\n?',
    re.DOTALL,
)

CONTACT_NAV_RE = re.compile(r'([ \t]*)(<li[^>]*><a href="contact-us\.html">Contact</a></li>)')

# Fake language/currency switchers the generated pages never had.
HEADER_SELECT_RE = re.compile(
    r'[ \t]*<div class="(?:language|currency)">\s*<div class="nice-select".*?</div>\s*</div>[ \t]*\n?',
    re.DOTALL,
)

# The header search box never searched anything: <form action="/"> with a type="button" submit.
HEADER_SEARCH_RE = re.compile(
    r'[ \t]*<div class="search-mobie[^"]*">\s*<div class="dropdown">.*?</div>\s*</div>[ \t]*\n?',
    re.DOTALL,
)

# Six repeats of the same placeholder logo, presented as partners.
BRAND_LOGOS_RE = re.compile(
    r'\s*<section class="brand-logo-widget[^"]*">.*?</section>', re.DOTALL)

# The header is brand green now, so it needs the transparent white/yellow mark. The
# off-canvas panel stays light and keeps logo.png, hence matching on the exact tag.
HEADER_LOGO_OLD = '<img src="assets/images/logo.png" alt="Logo">'
HEADER_LOGO_NEW = '<img src="assets/images/logo2.png" alt="Pathika">'

# A stock airliner on a white background, wrong for a trekking brand and a white
# rectangle now that the header is green.
FLY_AB_RE = re.compile(r'\n[ \t]*<img src="[^"]*fl1\.png"[^>]*class="fly-ab">')

CTA_RE = re.compile(
    r'(<h2 class="title-call">).*?(</h2>\s*<p class="des">).*?(</p>)', re.DOTALL)
CTA_LINK_RE = re.compile(r'<a href="[^"]*" class="get-call"[^>]*>.*?</a>', re.DOTALL)


def fix_cta(page: str) -> str:
    page = CTA_RE.sub(
        f'\\g<1>Ready to adventure and enjoy nature?\\g<2>Message us on WhatsApp at '
        f'{CONTACT["phone_display"]} to hold your slot.\\g<3>', page)
    return CTA_LINK_RE.sub(
        f'<a href="https://wa.me/{CONTACT["phone_intl"]}" class="get-call" target="_blank" '
        f'rel="noopener">Let\'s get started</a>', page)


def move_pages_to_end(page: str) -> str:
    """Pull the Pages dropdown out of the middle of the nav and re-add it last as More."""
    found = PAGES_NAV_RE.search(page)
    if not found:
        return page
    classes, submenu = found.group(1), found.group(2)
    page = page[:found.start()] + page[found.end():]

    contact = CONTACT_NAV_RE.search(page)
    if not contact:
        return page
    indent = contact.group(1)
    more = (f'\n{indent}<li class="dropdown2{classes}"><a href="#">More</a>\n'
            f'{indent}    {submenu}\n'
            f'{indent}</li>')
    return page[:contact.end()] + more + page[contact.end():]


def patch_static_pages() -> int:
    """Keep the pages we do not regenerate in step with nav() and header_html()."""
    generated = {detail_page(t) for t in TOURS} | {c["page"] for c in CATEGORIES} | {HUB_PAGE}
    patched = 0
    for path in sorted(OUT_DIR.glob("*.html")):
        if path.name in generated:
            continue
        original = path.read_text(encoding="utf-8")
        updated = DESTINATION_NAV_RE.sub("", original)
        updated = DASHBOARD_NAV_RE.sub("", updated)
        updated = BLOG_NAV_RE.sub(_news_item, updated)
        updated = HEADER_SELECT_RE.sub("", updated)
        updated = HEADER_SEARCH_RE.sub("", updated)
        updated = BRAND_LOGOS_RE.sub("", updated)
        updated = updated.replace(HEADER_LOGO_OLD, HEADER_LOGO_NEW)
        updated = FLY_AB_RE.sub("", updated)
        updated = fix_cta(updated)
        updated = move_pages_to_end(updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            patched += 1
    return patched


# --------------------------------------------------------------------------- about page

TOP_WEEK_RE = re.compile(
    r'\n[ \t]*<!-- Widget Top this Week -->.*?<!-- Widget Top this Week -->', re.DOTALL)

# The page shipped two identical call-to-action bands; keep only the closing one.
DUPLICATE_CTA_RE = re.compile(r'\n[ \t]*<section class="mt--82\s*">.*?</section>\n', re.DOTALL)


def patch_about_page() -> bool:
    """Drop the template's "Our top this week" slider of invented Moscow tours."""
    path = OUT_DIR / "about-us.html"
    if not path.is_file():
        return False
    original = path.read_text(encoding="utf-8")

    updated = TOP_WEEK_RE.sub("", original, count=1)
    updated = DUPLICATE_CTA_RE.sub("\n", updated, count=1)
    # That -14em pulled the (now deleted) slider up over the video; it left the CTA floating.
    updated = updated.replace("video-h4-widget relative overflow-hidden mb--14em",
                              "video-h4-widget relative overflow-hidden")

    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


# --------------------------------------------------------------------------- gallery page

GALLERY_TILE_RE = re.compile(
    r'(<div class="tf-gallery">\s*<img src=")[^"]+("[^>]*>\s*<a href=")[^"]+'
    r'("[^>]*>.*?<h4 class="gallery-title text-white mb-10">)[^<]+'
    r'(</h4>\s*<p class="sub-title">)[^<]+',
    re.DOTALL,
)

GALLERY_PAGE_TOURS = ["kodachadri", "gokarna", "dudhsagar", "kudremukha", "netrani", "spiti"]


def patch_gallery_page() -> bool:
    """Show real trips on gallery.html instead of the template's 'Discovery Island' tiles."""
    path = OUT_DIR / "gallery.html"
    if not path.is_file():
        return False

    picks = [t for slug in GALLERY_PAGE_TOURS for t in TOURS if t["slug"] == slug]
    tiles = iter(picks)

    def swap(match: re.Match) -> str:
        tour = next(tiles, None)
        if tour is None:
            return match.group(0)
        cat = CATEGORY_BY_SLUG[tour["category"]]
        return (f'{match.group(1)}{tour["image"]}{match.group(2)}{tour["image"]}'
                f'{match.group(3)}{tour["heading"]}{match.group(4)}{cat["name"]}')

    original = path.read_text(encoding="utf-8")
    updated = GALLERY_TILE_RE.sub(swap, original)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


# --------------------------------------------------------------------------- main

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = []

    (OUT_DIR / HUB_PAGE).write_text(render_hub(), encoding="utf-8")
    written.append(HUB_PAGE)

    for cat in CATEGORIES:
        (OUT_DIR / cat["page"]).write_text(render_category(cat), encoding="utf-8")
        written.append(cat["page"])

    for tour in TOURS:
        name = detail_page(tour)
        (OUT_DIR / name).write_text(render_detail(tour), encoding="utf-8")
        written.append(name)

    patched = patch_existing_nav()
    contacts = patch_contact_details()
    navs = patch_static_pages()
    gallery = patch_gallery_page()
    about = patch_about_page()

    print(f"Wrote {len(written)} pages into {OUT_DIR}:")
    for name in written:
        print(f"  {name}")
    print(f"Patched the Tours dropdown in {patched} existing pages.")
    print(f"Patched contact details in {contacts} existing pages.")
    print(f"Patched the shared nav in {navs} existing pages.")
    print(f"Patched gallery.html: {gallery}")
    print(f"Patched about-us.html: {about}")


if __name__ == "__main__":
    main()
