"""Replace the ViTour placeholder content on contact-us.html with Pathika's details.

Run from the repository root:

    python tools/build_contact.py

Idempotent: every rule matches both the original template markup and its own output.
"""

from __future__ import annotations

import re
from pathlib import Path

from tours_data import CONTACT, PICKUP_POINTS

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "contact-us.html"

WHATSAPP_URL = f"https://wa.me/{CONTACT['phone_intl']}"

BOXES = [
    ("Where we start",
     "Pickups across west Bengaluru &mdash;<br> Vijaynagar, Majestic, Rajajinagar and Goraguntepalya"),
    ("Phone &amp; WhatsApp",
     f'<a href="{WHATSAPP_URL}" target="_blank" rel="noopener">{CONTACT["phone_display"]}</a>'
     f'<br> WhatsApp is the fastest way to reach us'),
    ("Mail &amp; Instagram",
     f'<a href="mailto:{CONTACT["email"]}">{CONTACT["email"]}</a>'
     f'<br> <a href="https://www.instagram.com/{CONTACT["instagram"]}/" target="_blank" '
     f'rel="noopener">@{CONTACT["instagram"]}</a>'),
]

BOX_RE = re.compile(
    r'(<div class="box-contact center">.*?</div>\s*)<span>.*?</span>\s*<p class="des">.*?</p>',
    re.DOTALL,
)

GET_IN_TOUCH_RE = re.compile(
    r'(<div class="inner-header mb-45">\s*<h2 class="title">).*?(</h2>\s*<p class="des">).*?(</p>)',
    re.DOTALL,
)

FORM_HEADER_RE = re.compile(
    r'(<div class="inner-header mb-60">\s*<h2 class="title">).*?(</h2>\s*<p class="des">).*?(</p>)',
    re.DOTALL,
)

# The template's Mapbox box needs an access token we do not ship, so it renders blank.
PICKUP_RE = re.compile(
    r'<div class="map relative">\s*<div id="map"></div>\s*</div>'
    r'|<!-- pathika:pickup -->.*?<!-- /pathika:pickup -->',
    re.DOTALL,
)

BRAND_LOGOS_RE = re.compile(
    r'\s*<section class="brand-logo-widget bg-4">.*?</section>', re.DOTALL)

MAP_SCRIPTS_RE = re.compile(
    r'[ \t]*<script src="app/js/(?:map\.min\.js|map-config\.js|map\.js)"></script>\n?')

CTA_TITLE_RE = re.compile(r'(<h2 class="title-call">).*?(</h2>)', re.DOTALL)
CTA_DES_RE = re.compile(r'(<h2 class="title-call">.*?<p class="des">).*?(</p>)', re.DOTALL)
CTA_LINK_RE = re.compile(r'<a href="[^"]*" class="get-call"[^>]*>.*?</a>', re.DOTALL)

WHATSAPP_SCRIPT_RE = re.compile(
    r'\s*<!-- pathika:contact-form -->.*?<!-- /pathika:contact-form -->', re.DOTALL)


def pickup_block() -> str:
    items = "\n".join(
        f'                                            <li class="flex-three">\n'
        f'                                                <i class="icon-Vector4"></i>\n'
        f'                                                <span>{point}</span>\n'
        f'                                            </li>'
        for point in PICKUP_POINTS
    )
    return f"""<!-- pathika:pickup -->
                                    <div class="pickup-points-wrap">
                                        <ul class="pickup-points">
{items}
                                        </ul>
                                        <p class="des">Choose your pickup point while booking. Timing changes
                                            are shared on WhatsApp 24 hours before the trip starts, and drop-offs
                                            are at the same points.</p>
                                    </div>
                                    <!-- /pathika:pickup -->"""


def whatsapp_script() -> str:
    return f"""
    <!-- pathika:contact-form -->
    <script>
        document.getElementById('form-contact-us').addEventListener('submit', function (event) {{
            event.preventDefault();
            var field = this.querySelectorAll('input, textarea');
            var text = 'Hi Pathika, I am ' + field[0].value.trim()
                + ' (' + field[1].value.trim() + ').\\n\\n' + field[2].value.trim();
            window.open('{WHATSAPP_URL}?text=' + encodeURIComponent(text), '_blank', 'noopener');
        }});
    </script>
    <!-- /pathika:contact-form -->"""


def patch(page: str) -> str:
    boxes = iter(BOXES)

    def swap_box(match: re.Match) -> str:
        label, value = next(boxes)
        return f'{match.group(1)}<span>{label}</span>\n                                    <p class="des">{value}</p>'

    page = BOX_RE.sub(swap_box, page, count=len(BOXES))

    page = GET_IN_TOUCH_RE.sub(
        r"\g<1>Where we pick you up\g<2>Every trip leaves from Bengaluru. These are the four "
        r"pickup points, all on or near the metro.\g<3>", page, count=1)

    page = FORM_HEADER_RE.sub(
        r"\g<1>Tell us what you are planning\g<2>Fill this in and we will open WhatsApp with "
        r"your message ready to send.\g<3>", page, count=1)

    page = PICKUP_RE.sub(pickup_block(), page, count=1)
    page = BRAND_LOGOS_RE.sub("", page, count=1)
    page = MAP_SCRIPTS_RE.sub("", page)

    page = CTA_DES_RE.sub(
        f'\\g<1>Message us on WhatsApp at {CONTACT["phone_display"]} to hold your slot.\\g<2>',
        page, count=1)
    page = CTA_TITLE_RE.sub(r"\g<1>Ready to adventure and enjoy nature?\g<2>", page, count=1)
    page = CTA_LINK_RE.sub(
        f'<a href="{WHATSAPP_URL}" class="get-call" target="_blank" rel="noopener">'
        f"Let's get started</a>", page, count=1)

    page = WHATSAPP_SCRIPT_RE.sub("", page)
    page = page.replace("</body>", whatsapp_script() + "\n\n</body>", 1)

    page = page.replace('placeholder="Enter Your Messege here"',
                        'placeholder="Which trek, which dates, how many people?"')
    page = re.sub(r"<title>.*?</title>", "<title>Contact Pathika | Treks from Bengaluru</title>",
                  page, count=1, flags=re.DOTALL)
    return page


def main() -> None:
    original = PAGE.read_text(encoding="utf-8")
    PAGE.write_text(patch(original), encoding="utf-8")
    print(f"Updated {PAGE.relative_to(ROOT)}")
    print(f"  {len(BOXES)} contact boxes, {len(PICKUP_POINTS)} pickup points, "
          f"form wired to WhatsApp {CONTACT['phone_display']}")


if __name__ == "__main__":
    main()
