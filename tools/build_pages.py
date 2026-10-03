"""Replace the template's demo content on the alternate home pages.

Run from the repository root:

    python tools/build_pages.py

Rewrites the repeated card components (tour listings, destination tiles,
counters, testimonials) and the leftover placeholder copy on home2-home5 using
the real Pathika tour data. Structure-preserving and idempotent: only the text,
links, images and prices inside existing components are replaced.
"""

from __future__ import annotations

import itertools
import re
from pathlib import Path

from build_home import COUNTERS, TESTIMONIALS, headline_price, rupees
from tours_data import CATEGORIES, CONTACT, TOURS

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "vitour"

HUB_PAGE = "tours.html"
WHATSAPP_URL = f"https://wa.me/{CONTACT['phone_intl']}"

PAGES = {
    "home2.html": (
        "Pathika | Weekend Treks and Backpacking Tours from Bengaluru",
        "Western Ghat treks, coastal tours, day hikes and backpacking trips run by Pathika.",
    ),
    "home3.html": (
        "Pathika | Trekking and Travel Company in Bengaluru",
        "Book a weekend trek in the Western Ghats or a long-format backpacking trip with Pathika.",
    ),
    "home4.html": (
        "Pathika | Treks, Coastal Tours and Adventure Travel",
        "Ridge walks, beach trails, scuba diving and river rafting, run every weekend from Bengaluru.",
    ),
    "home5.html": (
        "Pathika | Adventure Travel and Trekking",
        "Small groups, clean trails and local guides across the Western Ghats and the Indian coast.",
    ),
}


# --------------------------------------------------------------------------- html helpers

def balanced_end(html: str, start: int, tag: str = "div") -> int:
    """Index just past the closing tag matching the one opening at `start`."""
    open_tag, close_tag = f"<{tag}", f"</{tag}>"
    i = start
    depth = 0
    while True:
        nxt_open = html.find(open_tag, i + 1)
        nxt_close = html.find(close_tag, i + 1)
        if nxt_close == -1:
            raise ValueError(f"unterminated {tag}")
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open
        else:
            if depth == 0:
                return nxt_close + len(close_tag)
            depth -= 1
            i = nxt_close


def drop_block(block: str, opening: str) -> str:
    """Remove a nested `<div ...>...</div>` identified by its opening tag."""
    start = block.find(opening)
    if start == -1:
        return block
    return block[:start] + block[balanced_end(block, start):]


def map_blocks(html: str, open_re: re.Pattern, transform, tag: str = "div") -> str:
    """Apply `transform` to every balanced element whose opening tag matches."""
    out = []
    pos = 0
    for match in open_re.finditer(html):
        if match.start() < pos:
            continue
        end = balanced_end(html, match.start(), tag)
        out.append(html[pos:match.start()])
        out.append(transform(html[match.start():end]))
        pos = end
    out.append(html[pos:])
    return "".join(out)


def sub1(block: str, pattern: str, repl: str) -> str:
    return re.sub(pattern, repl, block, count=1, flags=re.DOTALL)


# --------------------------------------------------------------------------- tour cards

TOUR_CARD_RE = re.compile(r'<div class="tour-listing(?=[ "])[^>]*>')


def rewrite_tour_card(block: str, tour: dict) -> str:
    page = f"tour-{tour['slug']}.html"
    cat = next(c for c in CATEGORIES if c["slug"] == tour["category"])

    block = re.sub(r'href="(?:tour-single|tour-[a-z-]+)\.html"', f'href="{page}"', block)
    block = drop_block(block, '<div class="badge-media flex-five">')
    block = drop_block(block, '<div class="review">')
    block = re.sub(r'<span class="tag-listing">[^<]*</span>\s*', "", block)

    block = sub1(block, r'<img\s+src="\./assets/images/[^"]+"\s*\n?\s*alt="[^"]*">',
                 f'<img src="{tour["image"]}" alt="{tour["name"]}">')
    block = sub1(block, r'(<span class="feature[^"]*">)[^<]*(</span>)',
                 rf'\g<1>{cat["name"]}\g<2>')
    block = sub1(block, r'(<span class="map"><i class="icon-Vector4"></i>).*?(</span>)',
                 rf'\g<1>{tour["location"]}\g<2>')
    block = sub1(block, r'<h3 class="title-tour-list">.*?</h3>',
                 f'<h3 class="title-tour-list"><a href="{page}">{tour["heading"]}</a></h3>')

    meta = iter([tour["duration"], tour["difficulty"]])

    def icons(inner: str) -> str:
        value = next(meta, None)
        if value is None:
            return inner
        return sub1(inner, r'(<span>)[^<]*(</span>)', rf'\g<1>{value}\g<2>')

    block = map_blocks(block, re.compile(r'<div class="icons flex-three">'), icons)

    block = sub1(block, r'<p>From <span class="price-sale">[^<]*</span></p>',
                 '<p><span class="price-sale">PRICE</span> per head</p>')
    block = sub1(block, r'(<span class="price-sale">)[^<]*(</span>)',
                 rf'\g<1>{rupees(headline_price(tour))}\g<2>')
    block = re.sub(r'<span class="price">[^<]*</span>\s*', "", block)
    return block


# --------------------------------------------------------------------------- destination tiles

DESTINATION_TOUR_RE = re.compile(r'<div class="destination-tour(?=[ "])[^>]*>')
WIDGET_DESTINATION_RE = re.compile(r'<div class="tf-widget-destination(?=[ "])[^>]*>')


def category_count(cat: dict) -> int:
    return len([t for t in TOURS if t["category"] == cat["slug"]])


def rewrite_destination_tour(block: str, cat: dict) -> str:
    count = category_count(cat)
    block = re.sub(r'href="[^"]*\.html"', f'href="{cat["page"]}"', block)
    block = sub1(block, r'<img\s+src="\./assets/images/[^"]+"\s*\n?\s*alt="[^"]*">',
                 f'<img src="{cat["image"]}" alt="{cat["name"]}">')
    block = sub1(block, r'(<span class="tour text-white">)[^<]*(</span>)',
                 rf'\g<1>{count} {"Tour" if count == 1 else "Tours"}\g<2>')
    block = sub1(block, r'(<div class="title-tour">\s*<a href="[^"]*">).*?(</a>)',
                 rf'\g<1>{cat["name"]}\g<2>')
    return block


def rewrite_widget_destination(block: str, cat: dict) -> str:
    count = category_count(cat)
    block = re.sub(r'href="[^"]*\.html"', f'href="{cat["page"]}"', block)
    block = sub1(block, r'<img\s+src="\./assets/images/[^"]+"\s*\n?\s*alt="[^"]*">',
                 f'<img src="{cat["image"]}" alt="{cat["name"]}">')
    block = sub1(block, r'(<span class="tour">)[^<]*(</span>)',
                 rf'\g<1>{count} {"tour" if count == 1 else "tours"}\g<2>')
    block = sub1(block, r'(<span class="nation">).*?(</span>)', rf'\g<1>{cat["name"]}\g<2>')
    return block


DESTINATION_STYLE_RE = re.compile(r'<a href="[^"]*" class="destination-style relative">')


def rewrite_destination_style(block: str, cat: dict) -> str:
    count = category_count(cat)
    block = re.sub(r'href="[^"]*\.html"', f'href="{cat["page"]}"', block)
    block = sub1(block, r'<img\s+src="\./assets/images/[^"]+"\s*\n?\s*alt="[^"]*">',
                 f'<img src="{cat["image"]}" alt="{cat["name"]}">')
    block = sub1(block, r'(<span class="tour">)[^<]*(</span>)',
                 rf'\g<1>{count} {"tour" if count == 1 else "tours"}\g<2>')
    block = sub1(block, r'(<p class="text-white">).*?(</p>)', rf'\g<1>{cat["name"]}\g<2>')
    return block


# --------------------------------------------------------------------------- place cards

PLACE_CARD_RE = re.compile(r'<div class="tf-widget-place(?=[ "])[^>]*>')


def rewrite_place_card(block: str, tour: dict) -> str:
    page = f"tour-{tour['slug']}.html"
    cat = next(c for c in CATEGORIES if c["slug"] == tour["category"])

    block = re.sub(r'href="#"', f'href="{page}"', block)
    block = sub1(block, r'<img\s+src="\./assets/images/[^"]+"\s*\n?\s*alt="[^"]*">',
                 f'<img src="{tour["image"]}" alt="{tour["name"]}">')
    block = sub1(block, r'(<span class="feature[^"]*">)[^<]*(</span>)',
                 rf'\g<1>{cat["name"]}\g<2>')
    block = sub1(block, r'<p class="price-place">.*?</p>',
                 f'<p class="price-place"><span class="price">'
                 f'{rupees(headline_price(tour))}</span> per head</p>')
    block = sub1(block, r'(<span class="map"><i class="icon-Vector-15"></i>).*?(</span>)',
                 rf'\g<1>{tour["location"]}\g<2>')
    block = sub1(block, r'<h4 class="title-place">.*?</h4>',
                 f'<h4 class="title-place"><a href="{page}">{tour["heading"]}</a></h4>')

    meta = iter([tour["duration"], tour["difficulty"]])

    def meta_item(inner: str) -> str:
        value = next(meta, None)
        if value is None:
            return inner
        return sub1(inner, r'(<span>)[^<]*(</span>)', rf'\g<1>{value}\g<2>')

    return map_blocks(block, re.compile(r'<li class="flex-three">'), meta_item, tag="li")


# --------------------------------------------------------------------------- tab groups

DESTINATION_STYLE1_RE = re.compile(r'<div class="destination-style1(?=[ "])[^>]*>')


def rewrite_destination_style1(block: str, tour: dict) -> str:
    page = f"tour-{tour['slug']}.html"
    block = re.sub(r'href="(?:single-destination|tour-[a-z-]+)\.html"', f'href="{page}"', block)
    block = sub1(block, r'<img\s+src="\./assets/images/[^"]+"\s*\n?\s*alt="[^"]*">',
                 f'<img src="{tour["image"]}" alt="{tour["name"]}">')
    block = sub1(block, r'(<h6 class="tittle center"><a href="[^"]*">).*?(</a>)',
                 rf'\g<1>{tour["heading"]}\g<2>')
    return block


ITEM_KINDS = {
    "tour": (TOUR_CARD_RE, rewrite_tour_card),
    "destination": (DESTINATION_STYLE1_RE, rewrite_destination_style1),
}

# Demo city / activity tabs that should be grouped by Pathika category instead.
TAB_GROUPS = {
    "home2.html": [("myTab", "myTabContent", "tour")],
    "home3.html": [("pills-tab", "pills-tabContent", "destination")],
    "home5.html": [("myTab", "myTabContent", "tour")],
}


def set_attr(tag: str, name: str, value: str) -> str:
    return re.sub(rf'{name}="[^"]*"', f'{name}="{value}"', tag, count=1)


def item_spans(pane: str, item_re: re.Pattern):
    """Spans of the column/grid wrappers that contain a matching item."""
    spans = []
    for m in re.finditer(r'<div class="(?:col-|destination-style1)[^>]*>', pane):
        if spans and m.start() < spans[-1][1]:
            continue
        end = balanced_end(pane, m.start())
        if item_re.search(pane[m.start():end]):
            spans.append((m.start(), end))
    return spans


def regroup_tab_group(html: str, nav_id: str, content_id: str, kind: str) -> str:
    item_re, rewrite_item = ITEM_KINDS[kind]

    nav_open = re.search(rf'<ul[^>]*id="{nav_id}"[^>]*>', html)
    content_open = re.search(rf'<div class="tab-content" id="{content_id}">', html)
    if not nav_open or not content_open:
        raise ValueError(f"tab group {nav_id}/{content_id} not found")

    nav_start = nav_open.start()
    nav_end = balanced_end(html, nav_start, "ul")
    nav_block = html[nav_start:nav_end]

    li_spans = []
    cursor = 0
    while True:
        p = nav_block.find("<li", cursor)
        if p == -1:
            break
        e = balanced_end(nav_block, p, "li")
        li_spans.append((p, e))
        cursor = e
    if not li_spans:
        raise ValueError(f"no tab items in {nav_id}")
    li_template = nav_block[li_spans[0][0]:li_spans[0][1]]

    content_start = content_open.start()
    content_end = balanced_end(html, content_start, "div")
    content_block = html[content_start:content_end]

    pane_spans = []
    cursor = 0
    while True:
        p = content_block.find('<div class="tab-pane', cursor)
        if p == -1:
            break
        e = balanced_end(content_block, p, "div")
        pane_spans.append((p, e))
        cursor = e
    if not pane_spans:
        raise ValueError(f"no panes in {content_id}")
    pane_template = content_block[pane_spans[0][0]:pane_spans[0][1]]

    spans = item_spans(pane_template, item_re)
    if not spans:
        raise ValueError(f"no {kind} items in the first pane of {content_id}")
    prefix = pane_template[:spans[0][0]]
    item_template = pane_template[spans[0][0]:spans[0][1]]
    suffix = pane_template[spans[-1][1]:]

    tabs, panes = [], []
    for i, cat in enumerate(CATEGORIES):
        first = i == 0

        tab = li_template
        tab = re.sub(r'class="nav-link[^"]*"',
                     f'class="nav-link{" active" if first else ""}"', tab, count=1)
        tab = set_attr(tab, "id", f"{cat['slug']}-tab")
        tab = set_attr(tab, "data-bs-target", f"#{cat['slug']}-pane")
        tab = set_attr(tab, "aria-controls", f"{cat['slug']}-pane")
        tab = set_attr(tab, "aria-selected", "true" if first else "false")
        tab = re.sub(r"[^<>]*(</button>)", rf"{cat['name']}\1", tab, count=1)
        tabs.append(tab)

        items = [rewrite_item(item_template, t)
                 for t in TOURS if t["category"] == cat["slug"]]
        pane = re.sub(r'class="tab-pane[^"]*"',
                      f'class="tab-pane fade{" show active" if first else ""}"',
                      prefix, count=1)
        pane = set_attr(pane, "id", f"{cat['slug']}-pane")
        pane = set_attr(pane, "aria-labelledby", f"{cat['slug']}-tab")
        panes.append(pane + "\n".join(items) + suffix)

    new_nav = (nav_block[:li_spans[0][0]] + "\n".join(tabs)
               + nav_block[li_spans[-1][1]:])
    new_content = (content_block[:pane_spans[0][0]] + "\n".join(panes)
                   + content_block[pane_spans[-1][1]:])

    return (html[:nav_start] + new_nav + html[nav_end:content_start]
            + new_content + html[content_end:])


# --------------------------------------------------------------------------- counters

def rewrite_counters(html: str) -> str:
    if "number-counter" not in html:
        return html

    values = itertools.cycle(COUNTERS)
    html = re.sub(r'data-to="[\d.]+"', lambda m: f'data-to="{next(values)[0]}"', html)

    numbers = itertools.cycle(COUNTERS)
    html = re.sub(r'(data-waypoint-active="yes">)[^<]*(</div>)',
                  lambda m: m.group(1) + next(numbers)[0] + m.group(2), html)

    labels = itertools.cycle(COUNTERS)
    html = re.sub(r'(<p class="title-counter[^"]*">).*?(</p>)',
                  lambda m: m.group(1) + next(labels)[1] + m.group(2), html, flags=re.DOTALL)

    # home4 puts the label in a leading <span> instead of a .title-counter paragraph
    plain = itertools.cycle([lbl.replace("<br>", " ") for _, lbl in COUNTERS])

    def counter_item(block: str) -> str:
        return sub1(block, r'(<span>)[^<]*(</span>)', rf'\g<1>{next(plain)}\g<2>')

    return map_blocks(html, re.compile(r'<div class="counter-item(?=[ "])[^>]*>'), counter_item)


# --------------------------------------------------------------------------- testimonials

def rewrite_testimonials(html: str) -> str:
    names = itertools.cycle(TESTIMONIALS)
    html = re.sub(r'(<h3 class="name">).*?(</h3>)',
                  lambda m: m.group(1) + next(names)[0] + m.group(2), html, flags=re.DOTALL)
    jobs = itertools.cycle(TESTIMONIALS)
    html = re.sub(r'(<h3 class="name">[^<]*</h3>\s*\n?\s*<span class="job">).*?(</span>)',
                  lambda m: m.group(1) + next(jobs)[1] + m.group(2), html, flags=re.DOTALL)
    quotes = itertools.cycle(TESTIMONIALS)
    html = re.sub(r'(<p class="tes">).*?(</p>)',
                  lambda m: m.group(1) + next(quotes)[2] + m.group(2), html, flags=re.DOTALL)

    # home2 / home4 / home5 styles
    def card(block: str) -> str:
        name, job, quote = next(style_cycle)
        block = sub1(block, r'(<p class="des">).*?(</p>)', rf'\g<1>{quote}\g<2>')
        block = sub1(block, r'(<h\d class="(?:title|name)">).*?(</h\d>)', rf'\g<1>{name}\g<2>')
        block = sub1(block, r'(<span class="job">).*?(</span>)', rf'\g<1>{job}\g<2>')
        return block

    style_cycle = itertools.cycle(TESTIMONIALS)
    return map_blocks(html, re.compile(r'<div class="widget-testimonial-style[245](?=[ "])[^>]*>'),
                      card)


# --------------------------------------------------------------------------- copy

PRINT128_RE = re.compile(r"Welcome to our Print 128\b.*?(?=</p>|</span>)", re.DOTALL)

COPY_RE_SWAPS = [
    (PRINT128_RE,
     "Weekend treks, coastal tours and backpacking trips, run from Bengaluru with "
     "small groups and local guides."),
    (re.compile(r"Explore\s*\n?\s*the\s*\n?\s*world", re.IGNORECASE),
     "Explore with Pathika"),
    (re.compile(r"Lorem ipsum dolor sit amet,\s*\n?\s*consectetur\s*\n?\s*notted\s*\n?\s*adipisicin",
                re.DOTALL),
     f"Message us on WhatsApp at {CONTACT['phone_display']} to hold your slot."),
    (re.compile(r"Denouncing\s*(<span class=\"text-main\">pleasure</span>)?.*?"
                r"(?=</p>)", re.DOTALL),
     TESTIMONIALS[0][2]),
    (re.compile(r"<span\s*\n?\s*class=\"text-main\">2,500</span> people booked\s*\n?\s*"
                r"Tommorow land Event in last 24 hours", re.DOTALL),
     "Over <span class=\"text-main\">7 years</span> of clean trails and small groups"),
    (re.compile(r"2,500 people booked Tommorow land Event in last 24\s*\n?\s*hours", re.DOTALL),
     "Over 7 years of hosting solo travellers, groups of friends and families on clean, "
     "safe trails"),
    (re.compile(r"Our Clients Amazing\s*<span\s*\n?\s*class=\"font-yes text-gray\">Feedback"
                r"</span>\s*\n?\s*Here", re.DOTALL),
     'Why travellers <span class="font-yes text-gray">come back</span>'),
    (re.compile(r"Our Cilent(?:\u2019|â€™|')s Feedback"),
     "What we stand for"),
    (re.compile(r"<p>\+88 1900 6789 56</p>"),
     f"<p>{CONTACT['phone_display']}</p>"),
]

COPY_SWAPS = [
    ("Let,s get started", "Talk to us"),
]


def rewrite_copy(html: str) -> str:
    for pattern, new in COPY_RE_SWAPS:
        html = pattern.sub(new, html)
    for old, new in COPY_SWAPS:
        html = html.replace(old, new)
    return html


def rewrite_links(html: str) -> str:
    """Any remaining demo tour links point at the tours hub."""
    return html.replace('href="tour-single.html"', f'href="{HUB_PAGE}"')


def rewrite_cta(html: str) -> str:
    html = re.sub(r'(<h2 class="title-call[^"]*">).*?(</h2>)',
                  r'\g<1>Ready to adventure and enjoy nature?\g<2>', html, flags=re.DOTALL)
    html = re.sub(r'<a href="#" class="get-call">.*?</a>',
                  f'<a href="{WHATSAPP_URL}" class="get-call" target="_blank" '
                  f'rel="noopener">Talk to us</a>', html, flags=re.DOTALL)
    return html


def rewrite_head(html: str, title: str, description: str) -> str:
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html,
                  count=1, flags=re.DOTALL)
    if 'name="description"' in html:
        html = re.sub(r'<meta name="description" content="[^"]*">',
                      f'<meta name="description" content="{description}">', html, count=1)
    else:
        html = html.replace('<meta name="author" content="themesflat.com">',
                            f'<meta name="description" content="{description}">', 1)
    return html


# --------------------------------------------------------------------------- main

def rewrite_page(html: str, name: str, title: str, description: str) -> tuple[str, dict]:
    stats = {}

    tours = itertools.cycle(TOURS)
    cats = itertools.cycle(CATEGORIES)

    stats["tour cards"] = len(TOUR_CARD_RE.findall(html))
    html = map_blocks(html, TOUR_CARD_RE, lambda b: rewrite_tour_card(b, next(tours)))

    stats["place cards"] = len(PLACE_CARD_RE.findall(html))
    html = map_blocks(html, PLACE_CARD_RE, lambda b: rewrite_place_card(b, next(tours)))

    stats["destination tiles"] = (len(DESTINATION_TOUR_RE.findall(html))
                                  + len(WIDGET_DESTINATION_RE.findall(html))
                                  + len(DESTINATION_STYLE_RE.findall(html)))
    html = map_blocks(html, DESTINATION_TOUR_RE,
                      lambda b: rewrite_destination_tour(b, next(cats)))
    html = map_blocks(html, WIDGET_DESTINATION_RE,
                      lambda b: rewrite_widget_destination(b, next(cats)))
    html = map_blocks(html, DESTINATION_STYLE_RE,
                      lambda b: rewrite_destination_style(b, next(cats)), tag="a")

    for nav_id, content_id, kind in TAB_GROUPS.get(name, []):
        html = regroup_tab_group(html, nav_id, content_id, kind)
        stats["category tab groups"] = stats.get("category tab groups", 0) + 1

    html = rewrite_counters(html)
    html = rewrite_testimonials(html)
    html = rewrite_copy(html)
    html = rewrite_cta(html)
    html = rewrite_links(html)
    html = rewrite_head(html, title, description)
    return html, stats


def main() -> None:
    for name, (title, description) in PAGES.items():
        path = OUT_DIR / name
        html, stats = rewrite_page(path.read_text(encoding="utf-8"), name, title, description)
        path.write_text(html, encoding="utf-8")
        summary = ", ".join(f"{v} {k}" for k, v in stats.items() if v)
        print(f"Updated {name}" + (f" ({summary})" if summary else ""))


if __name__ == "__main__":
    main()
