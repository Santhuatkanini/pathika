"""Generate the site logo files from the Pathika brand artwork.

Run from the repository root:

    python tools/build_logos.py

Sources live in `pathika/assets/images/brand/`. The header and off-canvas sit on light
backgrounds so they use the green-block version; the footer and mobile menu sit on dark
backgrounds so they use the transparent white/yellow version.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "assets" / "images" / "brand"
IMAGES = ROOT / "assets" / "images"

LOGO_WIDTH = 420  # rendered at 128px, so this stays crisp on 3x screens
FAVICON = 180

# A contour-only patch of the round logo. The wordmark reaches row 2135 and the disc
# edge curves in below row 3000, so this box is the clean area between the two.
CONTOUR_BOX = (1000, 2200, 3136, 3000)
HEADER_WIDTH = 2000


def resized(source: Path, width: int) -> Image.Image:
    image = Image.open(source).convert("RGBA")
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.LANCZOS)


def header_background(source: Path, width: int) -> Image.Image:
    """Mirror-tile the contour patch so it repeats seamlessly across a wide header."""
    patch = Image.open(source).convert("RGB").crop(CONTOUR_BOX)
    strip = Image.new("RGB", (patch.width * 2, patch.height))
    strip.paste(patch, (0, 0))
    strip.paste(patch.transpose(Image.FLIP_LEFT_RIGHT), (patch.width, 0))
    return strip.resize((width, round(strip.height * width / strip.width)), Image.LANCZOS)


def circle_crop(source: Path, size: int) -> Image.Image:
    """The round artwork sits on a white square; keep the disc and drop the corners."""
    image = Image.open(source).convert("RGBA")
    side = min(image.size)
    left = (image.width - side) // 2
    top = (image.height - side) // 2
    image = image.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    image.putalpha(mask)
    return image


def main() -> None:
    jobs = [
        ("PATHIKA RECTANGLE WYG.png", IMAGES / "logo.png", LOGO_WIDTH),
        ("PATHIKA LOGO WY.png", IMAGES / "logo2.png", LOGO_WIDTH),
    ]
    for name, target, width in jobs:
        resized(BRAND / name, width).save(target, "PNG", optimize=True)
        image = Image.open(target)
        print(f"  {target.name:<12} {image.size[0]}x{image.size[1]}  "
              f"{target.stat().st_size // 1024} KB  <- {name}")

    favicon = IMAGES / "favico.png"
    circle_crop(BRAND / "PATHIKA ROUND LOGO WYG.png", FAVICON).save(favicon, "PNG", optimize=True)
    print(f"  {favicon.name:<12} {FAVICON}x{FAVICON}  {favicon.stat().st_size // 1024} KB  "
          f"<- PATHIKA ROUND LOGO WYG.png (circle cropped)")

    header = IMAGES / "page" / "header-contour.jpg"
    strip = header_background(BRAND / "PATHIKA ROUND LOGO WYG.png", HEADER_WIDTH)
    strip.save(header, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  {header.name:<12} {strip.size[0]}x{strip.size[1]}  "
          f"{header.stat().st_size // 1024} KB  <- PATHIKA ROUND LOGO WYG.png (contour patch)")


if __name__ == "__main__":
    main()
