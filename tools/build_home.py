"""Rewrite the Pathika-specific parts of the home page.

Run from the repository root:

    python tools/build_home.py

Patches `pathika/index.html` in place: hero slider, search form options,
about section copy, the featured tour tabs, the counters and the destination
grid. Everything else in the template page is left untouched. Idempotent.
"""

from __future__ import annotations

import re
from pathlib import Path

from tours_data import CATEGORIES, CONTACT, TOURS

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "pathika" / "index.html"

HUB_PAGE = "tours.html"
WHATSAPP_URL = f"https://wa.me/{CONTACT['phone_intl']}"

CATEGORY_BY_SLUG = {c["slug"]: c for c in CATEGORIES}


def rupees(amount: int) -> str:
    return "Rs " + f"{amount:,}"


def headline_price(tour: dict) -> int:
    """The first tier is always the all-inclusive rate."""
    return tour["prices"][0][0]


def tours_in(slug: str):
    return [t for t in TOURS if t["category"] == slug]


def find_section(html: str, opening: str) -> tuple[int, int]:
    """Return the span of a <section ...> ... </section> block, matched by depth."""
    start = html.index(opening)
    i = start
    depth = 0
    while True:
        nxt_open = html.find("<section", i + 1)
        nxt_close = html.find("</section>", i + 1)
        if nxt_close == -1:
            raise ValueError(f"unterminated section: {opening}")
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open
        else:
            if depth == 0:
                return start, nxt_close + len("</section>")
            depth -= 1
            i = nxt_close


def replace_section(html: str, opening: str, new_block: str) -> str:
    start, end = find_section(html, opening)
    return html[:start] + new_block + html[end:]


# --------------------------------------------------------------------------- slider

SLIDES = [
    {
        "image": "slide1.jpg",
        "eyebrow": "Just like that",
        "title": "Treks in the",
        "word": "Western Ghats",
        "des": "Ridge walks, shola forests and misty summits across Chikkamagaluru, "
               "Shivamogga and the Goa border. Leave Bengaluru on Friday night, be back "
               "by Sunday.",
        "cta": "Explore the treks",
        "link": "tours-western-ghat-treks.html",
    },
    {
        "image": "slide2.jpg",
        "eyebrow": "Sea, sand and rapids",
        "title": "Treks along the",
        "word": "Karnataka Coast",
        "des": "Beach-to-beach trails from Belekan to Kudle, scuba diving over the coral "
               "reefs of Netrani Island, and white-water rafting on the Kali river at Dandeli.",
        "cta": "Explore coastal tours",
        "link": "tours-coastal-treks.html",
    },
    {
        "image": "slide3.jpg",
        "eyebrow": "Go further",
        "title": "Backpack across",
        "word": "India",
        "des": "Long-format journeys through the forts and dunes of Rajasthan and the cold "
               "desert of Spiti &mdash; air-conditioned stays, local guides and every "
               "entrance fee covered.",
        "cta": "Explore backpacking tours",
        "link": "tours-backpacking.html",
    },
]


def slider_section() -> str:
    slides = "\n".join(f"""                            <div class="slider-home1 relative overflow-hidden swiper-slide">
                                <div class="silider-image">
                                    <img src="./assets/images/slide/{s['image']}" alt="Image" class="image-slide">
                                    <img src="./assets/images/slide/mask-slide.png" alt="Image" class="mask-slide">
                                    <img src="./assets/images/slide/mask-fly.png" alt="Image" class="mask-flane">
                                    <div class="booking-title tf-anime-rorate">
                                        <p class="booking">Booking</p>
                                        <span></span>
                                    </div>
                                </div>
                                <div class="slider-content">
                                    <div class="tf-container">
                                        <div class="row">
                                            <div class="col-lg-8">
                                                <span class="sub-title text-main font-yes fs-28-46 fadeInDown wow">{s['eyebrow']}</span>
                                                <h1 class="title-slide text-white mb-32 fadeInDown wow">{s['title']}<br>
                                                    <span class="animationtext clip text-main">
                                                        <span class="cd-words-wrapper">
                                                            <span class="item-text is-visible">{s['word']}</span>
                                                            <span class="item-text is-hidden">{s['word']}</span>
                                                        </span>
                                                    </span>
                                                </h1>
                                                <p class="des text-white mb-45 fadeInDown wow">{s['des']}</p>
                                                <div class="btn-group">
                                                    <a href="{s['link']}" class="btn-main fadeInDown wow">
                                                        <p class="btn-main-text">{s['cta']}</p>
                                                        <p class="iconer">
                                                            <i class="icon-arrow-right"></i>
                                                        </p>
                                                    </a>
                                                    <a href="about-us.html" class="btn-w-wa fadeInDown wow">Who we are <i
                                                            class="icon-Group-13"></i></a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>""" for s in SLIDES)

    return f"""<section class="slider relative">
                    <div class="swiper mySwiper">
                        <div class="swiper-wrapper">
{slides}
                        </div>
                        <div class="btn-nex-prev">
                            <div class="swiper-button-next  next-home1"></div>
                            <div class="swiper-button-prev  prev-home1"></div>
                        </div>
                    </div>
                </section>"""


# --------------------------------------------------------------------------- search form

def select_options(current: str, values) -> str:
    opts = [f'                                                            <li data-value class="option selected">{current}</li>']
    for v in values:
        slug = re.sub(r"[^a-z0-9]+", "-", v.lower()).strip("-")
        opts.append(f'                                                            <li data-value="{slug}" class="option">{v}</li>')
    return f"""<div class="nice-select" tabindex="0">
                                                        <span class="current">{current}</span>
                                                        <ul class="list">
{chr(10).join(opts)}
                                                        </ul>
                                                    </div>"""


def patch_search_form(html: str) -> str:
    """Swap the demo Destination / Type dropdown options for the real ones."""
    for label, current, values in [
        ("Destination", "All destinations", [t["heading"] for t in TOURS]),
        ("Type", "All tour types", [c["name"] for c in CATEGORIES]),
    ]:
        pattern = re.compile(
            r'(<label>' + label + r'</label>\s*\n\s*)<div class="nice-select" tabindex="0">.*?</div>\s*\n',
            re.DOTALL,
        )
        html, n = pattern.subn(
            lambda m: m.group(1) + select_options(current, values) + "\n", html, count=1
        )
        if not n:
            raise ValueError(f"search form {label} dropdown not found")
    return html


# --------------------------------------------------------------------------- about

ABOUT_REPLACEMENTS = [
    (r'(<p class="client fadeInUp wow">).*?(</p>)',
     r'\g<1>Over 7 years of hosting solo travellers, groups of friends and families on '
     r'clean, safe trails\g<2>'),
    (r'(<span class="sub-title-heading text-main mb-15 fadeInUp wow">).*?(</span>)',
     r'\g<1>Why Pathika\g<2>'),
    (r'(<h2 class="title-heading mb-18 fadeInUp wow">).*?(</h2>)',
     r'\g<1>Just like that, we are on our way to <span class="text-gray font-yes">'
     r'everywhere</span>\g<2>'),
    (r'(<p class="des-heading fadeInUp wow">).*?(</p>)',
     r'\g<1>We enliven, enrich and inspire your adventure &mdash; and we give travellers '
     r'their space, because you are not sheep and we are not shepherds. Safety and clean '
     r'trails are our top priorities.\g<2>'),
    (r'(<h6 class="title mb-10"><a href=")#(">)Trusted travel guide(</a></h6>\s*\n\s*'
     r'<p class="des">).*?(</p>)',
     r'\g<1>about-us.html\g<2>Local guides on every trail\g<3>Forest permits, jeep '
     r'transfers and a trip captain who knows the route, the weather and the rules.\g<4>'),
    (r'(<h6 class="title mb-10"><a href=")#(">)Pesonalized Trips(</a></h6>\s*\n\s*'
     r'<p class="des">).*?(</p>)',
     r'\g<1>about-us.html\g<2>Small, inclusive groups\g<3>Solo travellers, groups of '
     r'friends or a family travelling together &mdash; with Pathika you are part of the '
     r'family.\g<4>'),
    (r'(<a href=")#(" class="btn-main">\s*\n\s*<p class="btn-main-text">)More about us(</p>)',
     r'\g<1>about-us.html\g<2>More about us\g<3>'),
    (r'(<span class="text-main">)Checkout Beautiful Places Arround the World\.(</span>)',
     r'\g<1>Your trash comes back from the trail with you.\g<2>'),
]


def patch_about(html: str) -> str:
    start, end = find_section(html, '<section class="about-us pb-150">')
    block = html[start:end]
    if "Why Pathika" in block:
        return html
    for pattern, repl in ABOUT_REPLACEMENTS:
        block, n = re.subn(pattern, repl, block, count=1, flags=re.DOTALL)
        if not n:
            raise ValueError(f"about-us pattern not matched: {pattern[:60]}")
    return html[:start] + block + html[end:]


# --------------------------------------------------------------------------- tour tabs

def home_card(tour: dict, delay: float) -> str:
    cat = CATEGORY_BY_SLUG[tour["category"]]
    page = f"tour-{tour['slug']}.html"
    return f"""                                                <div class="col-sm-6 col-lg-3">
                                                    <div class="tour-listing wow fadeInUp animated" data-wow-delay="{delay:.1f}s">
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


def tour_package_section() -> str:
    tabs, panes = [], []
    for i, cat in enumerate(CATEGORIES):
        active = " active" if i == 0 else ""
        selected = "true" if i == 0 else "false"
        tabs.append(f"""                                        <li class="nav-item" role="presentation">
                                            <button class="nav-link{active}" id="{cat['slug']}-tab" data-bs-toggle="tab"
                                                data-bs-target="#{cat['slug']}-tab-pane" type="button" role="tab"
                                                aria-controls="{cat['slug']}-tab-pane" aria-selected="{selected}">{cat['name']}</button>
                                        </li>""")

        cards = "\n".join(home_card(t, 0.1 * ((n % 4) + 1))
                          for n, t in enumerate(tours_in(cat["slug"])))
        show = " show active" if i == 0 else ""
        panes.append(f"""                                        <div class="tab-pane fade{show}" id="{cat['slug']}-tab-pane" role="tabpanel"
                                            aria-labelledby="{cat['slug']}-tab" tabindex="0">
                                            <div class="row">
{cards}
                                            </div>
                                            <div class="row">
                                                <div class="col-lg-12 center mt-20">
                                                    <a href="{cat['page']}" class="btn-main">
                                                        <p class="btn-main-text">View all {cat['name']}</p>
                                                        <p class="iconer">
                                                            <i class="icon-arrow-right"></i>
                                                        </p>
                                                    </a>
                                                </div>
                                            </div>
                                        </div>""")

    return f"""<section class="tour-package pd-main">
                    <div class="tf-container w-1456">
                        <div class="row">
                            <div class="col-lg-12">
                                <div class="center m0-auto w-text-heading">
                                    <span class="sub-title-heading text-main mb-15 fadeInUp wow">Our tours</span>
                                    <h2 class="title-heading mb-40 fadeInUp wow">Pick your kind of <span
                                            class="text-gray font-yes">weekend</span></h2>
                                </div>
                                <div class="tab-tour-list">
                                    <ul class="nav justify-content-center tab-list mb-37" id="myTab" role="tablist">
{chr(10).join(tabs)}
                                    </ul>
                                    <div class="tab-content" id="myTabContent">
{chr(10).join(panes)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>"""


# --------------------------------------------------------------------------- counters

COUNTERS = [
    ("14", "Tours &amp;<br>Treks"),
    ("100", "Leave No Trace<br>Trails"),
    ("7", "Years of<br>Hosting"),
    ("4", "Trip<br>Categories"),
]


def patch_counters(html: str) -> str:
    start, end = find_section(html, '<section class="widget-counter relative">')
    block = html[start:end]

    block = re.sub(
        r'(<h2 class="title-call text-white mb-18 fadeInUp wow">).*?(</h2>)',
        r'\g<1>Ready to adventure and enjoy nature?\g<2>',
        block, count=1, flags=re.DOTALL)
    block = re.sub(
        r'(<p class="des text-white fadeInUp wow">).*?(</p>)',
        f'\\g<1>Seven years of clean trails, small groups and no sheep-herding.\\g<2>',
        block, count=1, flags=re.DOTALL)
    block = re.sub(
        r'<a href="#" class="get-call">.*?</a>',
        f'<a href="{WHATSAPP_URL}" class="get-call" target="_blank" rel="noopener">Talk to us</a>',
        block, count=1, flags=re.DOTALL)

    values = iter(COUNTERS)
    block, n = re.subn(
        r'data-to="[\d.]+"',
        lambda m: f'data-to="{next(values)[0]}"',
        block,
    )
    if n != len(COUNTERS):
        raise ValueError(f"expected {len(COUNTERS)} counters, found {n}")

    numbers = iter(COUNTERS)
    block = re.sub(
        r'(data-waypoint-active="yes">)[^<]*(</div>)',
        lambda m: m.group(1) + next(numbers)[0] + m.group(2),
        block,
    )

    labels = iter(COUNTERS)
    block = re.sub(
        r'(<p class="title-counter">).*?(</p>)',
        lambda m: m.group(1) + next(labels)[1] + m.group(2),
        block,
        flags=re.DOTALL,
    )
    return html[:start] + block + html[end:]


# --------------------------------------------------------------------------- destinations

DESTINATION_IMAGES = [
    "./assets/images/destination/list.jpg",
    "./assets/images/destination/list1.jpg",
    "./assets/images/destination/list2.jpg",
    "./assets/images/destination/list3.jpg",
]


def destination_section() -> str:
    cards = []
    for i, cat in enumerate(CATEGORIES):
        count = len(tours_in(cat["slug"]))
        cards.append(f"""                            <div class="tf-widget-destination wow fadeInUp animated" data-wow-delay="0.{i + 1}s">
                                <a href="{cat['page']}" class="destination-imgae">
                                    <span class="tour">{count} {'tour' if count == 1 else 'tours'}</span>
                                    <img src="{DESTINATION_IMAGES[i % len(DESTINATION_IMAGES)]}" alt="{cat['name']}">
                                </a>
                                <div class="destination-content">
                                    <span class="nation">{cat['name']}</span>
                                    <div class="flex-two btn-destination">
                                        <h6 class="title"><a href="{cat['page']}">View all tours</a></h6>
                                        <a href="{cat['page']}" class="flex-five btn-view">
                                            <i class="icon-Vector-32"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>""")

    return f"""<section class="widget-destination">
                    <div class="tf-container">
                        <div class="row">
                            <div class="col-lg-12">
                                <div class="center m0-auto w-text-heading mb-40">
                                    <span class="sub-title-heading text-main mb-15 fadeInUp wow">Where we go</span>
                                    <h2 class="title-heading fadeInUp wow">Four ways to travel with Pathika</h2>
                                </div>
                            </div>
                        </div>
                        <div class="grid-three-destination">
{chr(10).join(cards)}
                        </div>
                    </div>
                </section>"""


# --------------------------------------------------------------------------- offer package

FEATURED = ["kodachadri", "kudremukha", "gokarna", "bandajje", "netrani",
            "dandeli", "spiti", "rajasthan"]


def offer_package_section() -> str:
    by_slug = {t["slug"]: t for t in TOURS}
    slides = []
    for slug in FEATURED:
        tour = by_slug[slug]
        cat = CATEGORY_BY_SLUG[tour["category"]]
        page = f"tour-{tour['slug']}.html"
        slides.append(f"""                                            <div class="swiper-slide">
                                                <div class="tour-listing">
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
                                            </div>""")

    return f"""<section class="offer-package pd-main bg-1 relative">
                    <img src="./assets/images/page/feature.jpg" alt="image" class="feature-ofer">
                    <div class="tf-container">
                        <div class="row align-center z-index3 relative">
                            <div class="col-lg-5">
                                <div class="content">
                                    <div class="mb-50">
                                        <span class="sub-title-heading text-main mb-15 fadeInUp wow">Group &amp; repeater discount</span>
                                        <h2 class="title-heading mb-32 fadeInUp wow">Bring your <span
                                                class="text-gray font-yes">people</span> along</h2>
                                        <p class="des-heading fadeInUp wow">Trekked with us before, or booking for five
                                            or more? Every head gets Rs 100 off the package cost, on every trek we run.</p>
                                    </div>
                                    <div class="inner-content flex-three">
                                        <div class="offer fadeInUp wow">
                                            <span class="number">100 <span>Rs off</span></span>
                                        </div>
                                        <p class="font-italic fadeInUp wow">Per head, for <span
                                                class="text-main">repeaters</span> and groups of 5 or more</p>
                                    </div>
                                    <div class="btn-wap fadeInUp wow mt-30">
                                        <a href="{HUB_PAGE}" class="btn-main">
                                            <p class="btn-main-text">Explore all tours</p>
                                            <p class="iconer">
                                                <i class="icon-arrow-right"></i>
                                            </p>
                                        </a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-lg-7">
                                <div class="relative on-week-swipper-wrap">
                                    <div class="swiper offer-package-swipper overflow-hidden relative">
                                        <div class="swiper-wrapper">
{chr(10).join(slides)}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>"""


# --------------------------------------------------------------------------- adventure

def adventure_section() -> str:
    icons = ["icon-Group1", "icon-river-1", "icon-adventure-1", "icon-deer-1"]
    tabs, panes = [], []

    for i, cat in enumerate(CATEGORIES):
        active = " active" if i == 0 else ""
        selected = "true" if i == 0 else "false"
        tabs.append(f"""                                            <li class="nav-link flex-three{active}" id="nav-{cat['slug']}-tab"
                                                data-bs-toggle="tab" data-bs-target="#nav-{cat['slug']}" role="tab"
                                                aria-controls="nav-{cat['slug']}" aria-selected="{selected}">
                                                <i class="{icons[i % len(icons)]}"></i>
                                                <span>{cat['name']}</span>
                                            </li>""")

        cards = []
        for tour in tours_in(cat["slug"]):
            page = f"tour-{tour['slug']}.html"
            cards.append(f"""                                                <div class="col-6 col-sm-6 col-lg-3">
                                                    <div class="tf-adventure flex-three mb-43">
                                                        <a href="{page}" class="adventure-image">
                                                            <img src="{tour['image']}" alt="{tour['name']}">
                                                        </a>
                                                        <div class="adventure-image">
                                                            <span class="tour-ad">({tour['duration']})</span>
                                                            <h6 class="title-ad"><a href="{page}">{tour['heading']}</a></h6>
                                                            <p class="price-ad text-main">{rupees(headline_price(tour))}</p>
                                                        </div>
                                                    </div>
                                                </div>""")

        show = " show active" if i == 0 else ""
        panes.append(f"""                                        <div class="tab-pane fade{show}" id="nav-{cat['slug']}" role="tabpanel"
                                            tabindex="0">
                                            <div class="row">
{chr(10).join(cards)}
                                            </div>
                                        </div>""")

    return f"""<section class="widget-adventure">
                    <div class="tf-container">
                        <div class="row">
                            <div class="col-lg-12">
                                <div class="mb-40">
                                    <span class="sub-title-heading text-main mb-15 fadeInUp wow">Every trail we run</span>
                                    <h2 class="title-heading fadeInUp wow">Adventures for everyone</h2>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-lg-12">
                                <div class="adventure-content">
                                    <nav class="mb-40 adventure-scroll">
                                        <div class="nav nav-justified nav-tabs-adventure" id="nav-tab" role="tablist">
{chr(10).join(tabs)}
                                        </div>
                                    </nav>
                                    <div class="tab-content" id="nav-tabContent">
{chr(10).join(panes)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>"""


# --------------------------------------------------------------------------- what we stand for

VALUES = [
    {
        "slug": "pace",
        "tab": "Your own pace",
        "icon": "icon-Group-4",
        "image": "./assets/images/page/feature.jpg",
        "eyebrow": "Why Pathika",
        "title": "You are not sheep, and we are not shepherds",
        "points": [("icon-Page-1", "Room to roam"),
                   ("icon-rubber-ring-1", "No forced marching")],
    },
    {
        "slug": "everyone",
        "tab": "Everyone is welcome",
        "icon": "icon-Group-22",
        "image": "./assets/images/page/stand-for.jpg",
        "eyebrow": "Seven years in",
        "title": "Solo, with friends, or the whole family",
        "points": [("icon-Page-1", "Inclusive by default"),
                   ("icon-rubber-ring-1", "Small groups")],
    },
    {
        "slug": "safety",
        "tab": "Safety first",
        "icon": "icon-Group-31",
        "image": "./assets/images/page/feature.jpg",
        "eyebrow": "Our top priority",
        "title": "A trip captain who knows the route and the weather",
        "points": [("icon-Page-1", "Basic first aid on every trip"),
                   ("icon-rubber-ring-1", "Permits and ID checks handled")],
    },
    {
        "slug": "trace",
        "tab": "Leave no trace",
        "icon": "icon-deer-1",
        "image": "./assets/images/page/stand-for.jpg",
        "eyebrow": "Clean trails",
        "title": "Your trash comes back from the trail",
        "points": [("icon-Page-1", "No plastic packaging"),
                   ("icon-rubber-ring-1", "Respect the ecosystem")],
    },
    {
        "slug": "family",
        "tab": "Part of the family",
        "icon": "icon-adventure-1",
        "image": "./assets/images/page/feature.jpg",
        "eyebrow": "With Pathika as your host",
        "title": "You are not just a traveller",
        "points": [("icon-Page-1", "Campfire, games, travel diaries"),
                   ("icon-rubber-ring-1", "Rs 100 off for repeaters")],
    },
]


def stand_for_section() -> str:
    tabs, panes = [], []
    for i, value in enumerate(VALUES):
        first = i == 0
        tabs.append(f"""                                    <li class="nav-item" role="presentation">
                                        <button class="nav-link{" active" if first else ""}" id="stand-{value['slug']}-tab"
                                            data-bs-toggle="tab" data-bs-target="#stand-{value['slug']}-pane" type="button"
                                            role="tab" aria-controls="stand-{value['slug']}-pane"
                                            aria-selected="{"true" if first else "false"}">
                                            <span class="icon flex-five">
                                                <i class="{value['icon']}"></i>
                                            </span>
                                            <span>{value['tab']}</span>
                                        </button>
                                    </li>""")

        points = "\n".join(f"""                                                    <li class="flex-three text-white icon-list-wrap">
                                                        <span class="icon">
                                                            <i class="{icon}"></i>
                                                        </span>
                                                        <span class="icon-lists">{label}</span>
                                                    </li>""" for icon, label in value["points"])

        panes.append(f"""                                    <div class="tab-pane fade{" show active" if first else ""}" id="stand-{value['slug']}-pane"
                                        role="tabpanel" aria-labelledby="stand-{value['slug']}-tab" tabindex="0">
                                        <div class="tabs-activities-content">
                                            <div class="activities-image">
                                                <img src="{value['image']}" alt="{value['tab']}" loading="lazy">
                                            </div>
                                            <div class="activities-content relative">
                                                <span class="sub-title text-white">{value['eyebrow']}</span>
                                                <h3 class="title-activitis text-white">{value['title']}</h3>
                                                <ul class="activities-points">
{points}
                                                </ul>
                                                <div class="flex-three btn-wrap-activitis">
                                                    <a href="{HUB_PAGE}" class="icon-activitis flex-five">
                                                        <i class="icon-Vector-21"></i>
                                                    </a>
                                                    <a href="about-us.html" class="text-white get-start">See how we travel</a>
                                                </div>
                                                <img src="./assets/images/page/mask-tap.png" alt="" class="mask-tab">
                                            </div>
                                        </div>
                                    </div>""")

    return f"""<section class="relative tf-widget-activities pd-main overflow-hidden">
                    <img src="./assets/images/page/mask-activiti.png" alt="image" class="mask-top">
                    <img src="./assets/images/page/mask-print-2.png" alt="image" class="mask-bottom">
                    <div class="tf-container">
                        <div class="row z-index3 relative">
                            <div class="col-lg-12 mb-60">
                                <div class="clip-text">What we stand for</div>
                            </div>
                            <div class="col-lg-12">
                                <ul class="nav nav-tabs-activities justify-content-center" id="standForTabs"
                                    role="tablist">
{chr(10).join(tabs)}
                                </ul>
                                <div class="tab-content mt-44" id="standForContent">
{chr(10).join(panes)}
                                </div>
                            </div>
                        </div>
                    </div>
                </section>"""


# --------------------------------------------------------------------------- closing copy

def patch_banner_contact(html: str) -> str:
    start, end = find_section(html, '<section class="widget-banner-contact relative">')
    block = html[start:end]
    block = re.sub(
        r'(<span\s+class="sub-title-heading text-main mb-15 font-yes fs-28-46 wow fadeInUp animated">).*?(</span>)',
        r'\g<1>Clean trails, safe groups\g<2>', block, count=1, flags=re.DOTALL)
    block = re.sub(
        r'(<h2 class="title-heading text-white wow fadeInUp animated">).*?(</h2>)',
        r'\g<1>Ready to swap the city for a ridge this weekend?\g<2>',
        block, count=1, flags=re.DOTALL)
    block = re.sub(
        r"<address class=\"wow fadeInUp animated\">.*?</address>",
        f'<address class="wow fadeInUp animated">\n'
        f'                                        Contact us at <a href="mailto:{CONTACT["email"]}">'
        f'{CONTACT["email"]}</a><br>\n'
        f'                                        WhatsApp <a href="{WHATSAPP_URL}" target="_blank" '
        f'rel="noopener">{CONTACT["phone_display"]}</a>\n'
        f'                                    </address>',
        block, count=1, flags=re.DOTALL)
    return html[:start] + block + html[end:]


def patch_cta(html: str) -> str:
    start, end = find_section(html, '<section class="mb--93">')
    block = html[start:end]
    block = re.sub(r'(<h2 class="title-call">).*?(</h2>)',
                   r'\g<1>Ready to adventure and enjoy nature?\g<2>',
                   block, count=1, flags=re.DOTALL)
    block = re.sub(r'(<p class="des">).*?(</p>)',
                   f'\\g<1>Message us on WhatsApp at {CONTACT["phone_display"]} to hold your slot.\\g<2>',
                   block, count=1, flags=re.DOTALL)
    block = re.sub(r'<a href="#" class="get-call">.*?</a>',
                   f'<a href="{WHATSAPP_URL}" class="get-call" target="_blank" '
                   f'rel="noopener">Let\'s get started</a>',
                   block, count=1, flags=re.DOTALL)
    return html[:start] + block + html[end:]


# The template ships three identical stock testimonials; swap in Pathika's own words
# rather than inventing customer quotes.
TESTIMONIALS = [
    ("Pathika", "Our promise",
     "Just like that, we are on our way to everywhere to enliven, enrich and inspire "
     "your adventure."),
    ("Pathika", "How we travel",
     "We allow travellers their space, since you are all not sheep, and we are not "
     "shepherds."),
    ("Pathika", "On the trail",
     "Safety and clean trails are our top priorities. With Pathika as your host you are "
     "not just a traveller, you are part of the family."),
]


def patch_testimonials(html: str) -> str:
    start, end = find_section(html, '<section class="widget-testimonial-style01">')
    block = html[start:end]

    names = iter(TESTIMONIALS)
    block, n = re.subn(
        r'<h3 class="name">.*?</h3>\s*\n\s*<span class="job">.*?</span>',
        lambda m: (lambda t: f'<h3 class="name">{t[0]}</h3>\n'
                             f'                                                        '
                             f'<span class="job">{t[1]}</span>')(next(names)),
        block, flags=re.DOTALL)
    if n != len(TESTIMONIALS):
        raise ValueError(f"expected {len(TESTIMONIALS)} testimonials, found {n}")

    quotes = iter(TESTIMONIALS)
    block = re.sub(r'(<p class="tes">).*?(</p>)',
                   lambda m: m.group(1) + next(quotes)[2] + m.group(2),
                   block, flags=re.DOTALL)
    return html[:start] + block + html[end:]


# --------------------------------------------------------------------------- head

def patch_head(html: str) -> str:
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Pathika | Treks, Coastal Tours and Backpacking Trips from Bengaluru</title>",
        html,
        count=1,
        flags=re.DOTALL,
    )
    description = ('Pathika runs weekend treks in the Western Ghats, coastal tours on the '
                   'Karnataka coast, day hikes around Bengaluru and backpacking trips across India.')
    if 'name="description"' in html:
        html = re.sub(r'<meta name="description" content="[^"]*">',
                      f'<meta name="description" content="{description}">', html, count=1)
    else:
        html = html.replace(
            '<meta name="author" content="themesflat.com">',
            f'<meta name="description" content="{description}">',
            1,
        )
    return html


# --------------------------------------------------------------------------- main

def main() -> None:
    html = INDEX.read_text(encoding="utf-8")

    html = patch_head(html)
    html = replace_section(html, '<section class="slider relative">', slider_section())
    html = patch_search_form(html)
    html = patch_about(html)
    html = replace_section(html, '<section class="tour-package pd-main">', tour_package_section())
    html = replace_section(
        html, '<section class="relative tf-widget-activities pd-main overflow-hidden">',
        stand_for_section())
    html = replace_section(html, '<section class="offer-package pd-main bg-1 relative">',
                           offer_package_section())
    html = patch_counters(html)
    html = replace_section(html, '<section class="widget-adventure">', adventure_section())
    html = patch_testimonials(html)
    html = patch_banner_contact(html)
    html = patch_cta(html)

    INDEX.write_text(html, encoding="utf-8")
    print(f"Updated {INDEX.relative_to(ROOT)}")
    print(f"  {len(SLIDES)} hero slides, {len(CATEGORIES)} tour tabs covering {len(TOURS)} tours")


if __name__ == "__main__":
    main()
