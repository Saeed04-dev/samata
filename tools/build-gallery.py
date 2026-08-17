#!/usr/bin/env python3
"""Build the Instagram gallery assets for the Samata site.

Reads the curated shortlist from uploads/samatabrewing/ (originals, untracked)
and writes two WebP renditions into assets/gallery/:

  thumb/<id>.webp  800x1000 (4:5, centre-cropped)  -> grid
  full/<id>.webp   longest edge 1600px             -> lightbox

Originals are never modified. Re-run after changing SELECTED:

    python3 tools/build-gallery.py
"""

import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "uploads" / "samatabrewing"
OUT = ROOT / "assets" / "gallery"

THUMB_SIZE = (800, 1000)  # 4:5 — every original is cropped to this
FULL_MAX = 1600
THUMB_QUALITY = 72
FULL_QUALITY = 80

# Curated from all 102 originals. Posters/text cards, low-quality phone shots
# and the 17 images already used elsewhere on the page are excluded.
SELECTED = [
    "004", "005", "006", "008", "012", "017", "018", "020", "021", "022",
    "024", "026", "028", "029", "030", "033", "034", "037", "040", "043",
    "049", "052", "053", "056", "058", "060", "063", "064", "067", "068",
    "069", "070", "072", "082", "083", "084", "087", "089", "091", "092",
]


def find_source(prefix):
    """Originals are named <prefix>_<instagram-id>.<ext>.

    A prefix must identify exactly one original — picking the first of several
    would silently publish the wrong photo.
    """
    matches = sorted(SRC.glob(f"{prefix}_*"))
    if len(matches) > 1:
        names = ", ".join(m.name for m in matches)
        sys.exit(f"error: prefix {prefix} matches more than one original: {names}")
    return matches[0] if matches else None


def prune(kept):
    """Drop renditions whose id is no longer in SELECTED."""
    removed = []
    for sub in ("thumb", "full"):
        for path in (OUT / sub).glob("*.webp"):
            if path.stem not in kept:
                path.unlink()
                removed.append(f"{sub}/{path.name}")
    return removed


def main():
    if not SRC.is_dir():
        sys.exit(f"error: source directory not found: {SRC}")

    (OUT / "thumb").mkdir(parents=True, exist_ok=True)
    (OUT / "full").mkdir(parents=True, exist_ok=True)

    missing = []
    total = 0

    for prefix in SELECTED:
        src = find_source(prefix)
        if src is None:
            missing.append(prefix)
            continue

        with Image.open(src) as im:
            # Honour EXIF orientation, then drop alpha — WebP here is opaque.
            im = ImageOps.exif_transpose(im).convert("RGB")

            thumb = ImageOps.fit(im, THUMB_SIZE, Image.LANCZOS, centering=(0.5, 0.5))
            thumb_path = OUT / "thumb" / f"{prefix}.webp"
            thumb.save(thumb_path, "WEBP", quality=THUMB_QUALITY, method=6)

            full = im.copy()
            full.thumbnail((FULL_MAX, FULL_MAX), Image.LANCZOS)
            full_path = OUT / "full" / f"{prefix}.webp"
            full.save(full_path, "WEBP", quality=FULL_QUALITY, method=6)

        total += thumb_path.stat().st_size + full_path.stat().st_size
        print(f"{prefix}  {src.name}  ->  thumb {thumb_path.stat().st_size // 1024}KB"
              f"  full {full_path.stat().st_size // 1024}KB")

    for name in prune(set(SELECTED)):
        print(f"removed stale {name}")

    print(f"\n{len(SELECTED) - len(missing)} images  ·  {total / 1_048_576:.1f} MB total")

    if missing:
        sys.exit(f"error: no source found for: {', '.join(missing)}")


if __name__ == "__main__":
    main()
