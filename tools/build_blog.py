"""Rebuild blog.html from Google News headlines about Karnataka trekking.

Run from the repository root:

    python tools/build_blog.py

Google News RSS is a link-out aggregator: we store the headline, source, date and
URL only, and every card links back to the publisher. No article text is copied.

The script is idempotent and refuses to touch blog.html if the fetch fails, so a
network blip leaves the last good build in place instead of emptying the page.
"""

from __future__ import annotations

import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

from tours_data import CONTACT, TOURS

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog.html"
PHOTO_DIR = ROOT / "assets" / "images" / "tours"

FEEDS = [
    ("Karnataka treks", "Karnataka trek OR trekking"),
    ("Western Ghats", '"Western Ghats" trekking OR monsoon trails Karnataka'),
    ("Forests & wildlife", "Karnataka forest department trekking OR wildlife sanctuary permit"),
]

FEED_URL = ("https://news.google.com/rss/search?q={query}"
            "&hl=en-IN&gl=IN&ceid=IN:en")
USER_AGENT = "Mozilla/5.0 (compatible; PathikaSiteBuilder/1.0)"

MAIN_CARDS = 9
SIDEBAR_CARDS = 4


# --------------------------------------------------------------------------- fetch

def tidy(title: str) -> str:
    """Google News clips long headlines at ~105 chars, mid-word and with no marker."""
    title = title.strip()
    if len(title) >= 100 and title[-1].isalnum():
        title = title.rsplit(" ", 1)[0].rstrip(",;:-") + "\u2026"
    return title


def fetch(topic: str, query: str) -> list[dict]:
    url = FEED_URL.format(query=urllib.parse.quote(query))
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        root = ET.fromstring(response.read())

    stories = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue

        source = item.findtext("{*}source") or item.findtext("source") or ""
        source = source.strip()
        # Google News appends " - Publisher" to every headline.
        if not source and " - " in title:
            title, _, source = title.rpartition(" - ")
        elif title.endswith(f" - {source}"):
            title = title[: -len(f" - {source}")]

        try:
            published = parsedate_to_datetime(item.findtext("pubDate"))
        except (TypeError, ValueError):
            published = datetime.now(timezone.utc)
        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)

        stories.append({
            "title": tidy(title),
            "link": link,
            "source": source or "Google News",
            "published": published,
            "topic": topic,
        })
    return stories


def collect() -> list[dict]:
    seen, stories = set(), []
    for topic, query in FEEDS:
        for story in fetch(topic, query):
            key = re.sub(r"\W+", "", story["title"].lower())[:80]
            if key in seen:
                continue
            seen.add(key)
            stories.append(story)
    stories.sort(key=lambda s: s["published"], reverse=True)
    return stories


# --------------------------------------------------------------------------- render

# The stories are all Karnataka / Western Ghats, so Himalayan and desert trips are
# excluded from the illustrative photo pool.
PHOTO_SKIP = {"backpacking-tours", "rajasthan", "spiti"}


def photos() -> list[str]:
    names = sorted(p.name for p in PHOTO_DIR.glob("*.jpg")
                   if not p.stem.rsplit("-", 1)[-1].isdigit()
                   and not p.stem.startswith("stand-")
                   and p.stem not in PHOTO_SKIP)
    return [f"./assets/images/tours/{n}" for n in names]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def article_card(story: dict, image: str) -> str:
    return f"""                                <article class="side-blog mb-56px">
                                    <div class="blog-image">
                                        <div class="list-categories">
                                            <a href="{esc(story['link'])}" target="_blank" rel="noopener noreferrer nofollow" class="new">{story['published']:%d %b}</a>
                                        </div>
                                        <a class="post-thumbnail" href="{esc(story['link'])}" target="_blank" rel="noopener noreferrer nofollow">
                                            <img src="{image}" alt="" loading="lazy">
                                        </a>
                                    </div>
                                    <div class="blog-content">
                                        <div class="top-detail-info">
                                            <ul class="flex-three">
                                                <li>
                                                    <i class="icon-user"></i>
                                                    <span class="date">{esc(story['source'])}</span>
                                                </li>
                                                <li>
                                                    <i class="icon-4"></i>
                                                    <span class="date">{story['published']:%b %d, %Y}</span>
                                                </li>
                                                <li>
                                                    <i class="icon-24"></i>
                                                    <span class="date">{esc(story['topic'])}</span>
                                                </li>
                                            </ul>
                                        </div>
                                        <h3 class="entry-title">
                                            <a href="{esc(story['link'])}" target="_blank" rel="noopener noreferrer nofollow">{esc(story['title'])}</a>
                                        </h3>
                                        <div class="button-main">
                                            <a href="{esc(story['link'])}" target="_blank" rel="noopener noreferrer nofollow" class="button-link">Read on {esc(story['source'])} <i
                                                    class="icon-Arrow-11"></i></a>
                                        </div>
                                    </div>
                                </article>"""


def main_column(stories: list[dict], built: datetime) -> str:
    art = photos()
    cards = "\n".join(article_card(s, art[i % len(art)] if art else "./assets/images/blog/blog.jpg")
                      for i, s in enumerate(stories[:MAIN_CARDS]))
    # The trailing </div> closes col-lg-8; without it the sidebar nests inside this column.
    return f"""
                                <div class="mb-40">
                                    <h2 class="title">Trail news</h2>
                                    <p class="des">Permit rules, trail closures and Western Ghats reporting,
                                        pulled from the Indian press. Headlines link straight to the publisher.
                                        Photographs are from our own trails, not from the linked article.
                                        Last updated {built:%d %B %Y}.</p>
                                </div>
{cards}
                            </div>
                            """


def sidebar_item(story: dict, image: str) -> str:
    return f"""                                            <div class="list-recent flex-three">
                                                <a href="{esc(story['link'])}" target="_blank" rel="noopener noreferrer nofollow" class="recent-image">
                                                    <img src="{image}" alt="" loading="lazy">
                                                </a>
                                                <div class="recent-info">
                                                    <div class="date">
                                                        <i class="icon-4"></i>
                                                        <span>{story['published']:%b %d, %Y}</span>
                                                    </div>
                                                    <h4 class="title">
                                                        <a href="{esc(story['link'])}" target="_blank" rel="noopener noreferrer nofollow">{esc(story['title'])}</a>
                                                    </h4>
                                                </div>
                                            </div>"""


def topic_links() -> str:
    rows = []
    for topic, query in FEEDS:
        url = "https://news.google.com/search?q=" + urllib.parse.quote(query) + "&hl=en-IN&gl=IN&ceid=IN:en"
        rows.append(f"""                                            <li>
                                                <a href="{esc(url)}" target="_blank" rel="noopener noreferrer nofollow" class="flex-two">
                                                    <span>{esc(topic)}</span>
                                                    <span><i class="icon-Arrow-11"></i></span>
                                                </a>
                                            </li>""")
    return "\n".join(rows)


def tour_tags() -> str:
    picks = ["kodachadri", "kudremukha", "gokarna", "dudhsagar", "netrani",
             "dandeli", "spiti", "rajasthan"]
    by_slug = {t["slug"]: t for t in TOURS}
    rows = []
    for slug in picks:
        tour = by_slug.get(slug)
        if tour:
            rows.append(f"""                                            <li>
                                                <a href="tour-{slug}.html">{esc(tour['name'])}</a>
                                            </li>""")
    return "\n".join(rows)


# --------------------------------------------------------------------------- patch

def replace_between(html_text: str, opening: str, closing: str, block: str) -> str:
    start = html_text.index(opening) + len(opening)
    end = html_text.index(closing, start)
    return html_text[:start] + block + html_text[end:]


def patch(html_text: str, stories: list[dict], built: datetime) -> str:
    art = photos()

    html_text = replace_between(
        html_text,
        '<div class="col-lg-8 col-12">',
        '<div class="col-lg-4 col-12">',
        main_column(stories, built),
    )

    recent = "\n".join(
        sidebar_item(s, art[(MAIN_CARDS + i) % len(art)] if art else "./assets/images/blog/re-blog1.jpg")
        for i, s in enumerate(stories[MAIN_CARDS:MAIN_CARDS + SIDEBAR_CARDS])
    )
    html_text = replace_between(
        html_text,
        '<div class="recent-post-list">',
        '</div>\n                                    </div>\n                                    <div class="sidebar-widget">',
        "\n" + recent + "\n                                        ",
    )

    html_text = re.sub(
        r'(<div class="profile-widget center">).*?(</div>\s*</div>\s*<div class="sidebar-widget">)',
        lambda m: m.group(1) + f"""
                                            <div class="name">Trail news</div>
                                            <span class="job">Karnataka treks &amp; Western Ghats</span>
                                            <p class="des">What is changing on the trails we walk &mdash; permits,
                                                closures, new rules and weather. Every headline links to the
                                                publisher who reported it.</p>
                                            <ul class="social">
                                                <li>
                                                    <a href="https://www.instagram.com/{CONTACT['instagram']}/" target="_blank" rel="noopener noreferrer">
                                                        <i class="icon-icon_03"></i>
                                                    </a>
                                                </li>
                                                <li>
                                                    <a href="https://wa.me/{CONTACT['phone_intl']}" target="_blank" rel="noopener noreferrer">
                                                        <i class="icon-2"></i>
                                                    </a>
                                                </li>
                                            </ul>
                                        """ + m.group(2),
        html_text, count=1, flags=re.DOTALL,
    )

    html_text = re.sub(r'(<ul class="category-blog">).*?(</ul>)',
                       lambda m: m.group(1) + "\n" + topic_links() + "\n                                        " + m.group(2),
                       html_text, count=1, flags=re.DOTALL)

    html_text = re.sub(r'(<ul class="tag">).*?(</ul>)',
                       lambda m: m.group(1) + "\n" + tour_tags() + "\n                                        " + m.group(2),
                       html_text, count=1, flags=re.DOTALL)

    html_text = re.sub(r"<title>.*?</title>",
                       "<title>Trail news | Pathika</title>", html_text, count=1, flags=re.DOTALL)
    html_text = re.sub(r'(<h1 class="title">)[^<]*(</h1>)', r"\1Trail news\2", html_text, count=1)
    html_text = re.sub(r'(<li><span>)Blog Page(</span></li>)', r"\1Trail news\2", html_text, count=1)

    return html_text


def main() -> None:
    try:
        stories = collect()
    except (urllib.error.URLError, ET.ParseError, TimeoutError) as exc:
        sys.exit(f"Could not fetch Google News ({exc}). blog.html left unchanged.")

    if len(stories) < MAIN_CARDS:
        sys.exit(f"Only {len(stories)} stories returned, expected at least {MAIN_CARDS}. "
                 "blog.html left unchanged.")

    built = datetime.now()
    BLOG.write_text(patch(BLOG.read_text(encoding="utf-8"), stories, built), encoding="utf-8")

    print(f"Updated {BLOG.relative_to(ROOT)}")
    print(f"  {len(stories)} unique stories, showing {MAIN_CARDS} + {SIDEBAR_CARDS} in the sidebar")
    for story in stories[:MAIN_CARDS]:
        print(f"  {story['published']:%Y-%m-%d}  {story['source'][:22]:<22} {story['title'][:70]}")


if __name__ == "__main__":
    main()
