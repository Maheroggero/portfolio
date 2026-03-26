"""
Portfolio Image Optimizer
Converts JPG/PNG images to WebP format for faster web loading.
- /images/ folder: quality 80 (thumbnails)
- Project render folders: quality 82 (project pages, seen by recruiters)

Run: python optimize-images.py
"""

import os
from pathlib import Path
from PIL import Image

# Project root
ROOT = Path(__file__).parent

# Thumbnail folder (All Projects grid + hero)
THUMBNAIL_DIR = ROOT / "images"
THUMBNAIL_QUALITY = 80

# Project render folders
RENDER_DIRS = [
    "BoldRender",
    "NikeRender",
    "Prada",
    "prada",
    "Oakley",
    "03_RENDER",
    "RestaurantRender",
    "restaurantRender",
    "TamRender",
    "TokyoRender",
]
RENDER_QUALITY = 82

# Formats to process
SUPPORTED = {".jpg", ".jpeg", ".png"}


def format_size(bytes_val):
    if bytes_val >= 1024 * 1024:
        return f"{bytes_val / (1024*1024):.1f}MB"
    return f"{bytes_val / 1024:.0f}KB"


def convert_to_webp(src, quality):
    """Convert image to WebP. Returns (original_size, webp_size) or None if skipped."""
    src = Path(src)
    dest = src.with_suffix(".webp")

    if dest.exists():
        return None  # Already converted, skip

    try:
        original_size = src.stat().st_size
        with Image.open(src) as img:
            if img.mode in ("RGBA", "LA"):
                img.save(dest, "WEBP", quality=quality, method=6)
            else:
                img.convert("RGB").save(dest, "WEBP", quality=quality, method=6)
        webp_size = dest.stat().st_size
        return original_size, webp_size
    except Exception as e:
        print(f"  ERROR: {src.name} -> {e}")
        return None


def process_folder(folder, quality, label):
    folder = Path(folder)
    if not folder.exists():
        return None

    files = [f for f in folder.iterdir() if f.suffix.lower() in SUPPORTED]
    if not files:
        return None

    total_original = 0
    total_webp = 0
    converted = 0
    skipped = 0

    for f in sorted(files):
        result = convert_to_webp(f, quality)
        if result is None:
            skipped += 1
            continue
        orig, webp = result
        total_original += orig
        total_webp += webp
        converted += 1
        saving_pct = (1 - webp / orig) * 100 if orig > 0 else 0
        safe_name = f.name.encode('ascii', errors='replace').decode('ascii')
        print(f"  OK {safe_name:40s} {format_size(orig):>8} -> {format_size(webp):>8}  (-{saving_pct:.0f}%)")

    if converted > 0:
        total_saving_pct = (1 - total_webp / total_original) * 100 if total_original > 0 else 0
        print(f"  --- {label}: {converted} files | {format_size(total_original)} -> {format_size(total_webp)} (-{total_saving_pct:.0f}%)")
        if skipped:
            print(f"  --- {skipped} file(s) already converted, skipped")
        return total_original, total_webp, converted
    else:
        print(f"  --- All files already converted ({skipped} skipped)")
        return None


def main():
    print("=" * 65)
    print("  Portfolio Image Optimizer - WebP Conversion")
    print("=" * 65)

    grand_orig = 0
    grand_webp = 0
    grand_count = 0

    # Thumbnails
    print(f"\n[images/]  (quality {THUMBNAIL_QUALITY}%)")
    result = process_folder(THUMBNAIL_DIR, THUMBNAIL_QUALITY, "Thumbnails")
    if result:
        grand_orig += result[0]
        grand_webp += result[1]
        grand_count += result[2]

    # Render folders (deduplicated by resolved path)
    seen_paths = set()
    for dirname in RENDER_DIRS:
        folder = ROOT / dirname
        resolved = folder.resolve() if folder.exists() else None
        if resolved and resolved in seen_paths:
            continue
        if resolved:
            seen_paths.add(resolved)
        print(f"\n[{dirname}/]  (quality {RENDER_QUALITY}%)")
        result = process_folder(folder, RENDER_QUALITY, dirname)
        if result:
            grand_orig += result[0]
            grand_webp += result[1]
            grand_count += result[2]

    # Summary
    print("\n" + "=" * 65)
    if grand_count > 0:
        total_saving_pct = (1 - grand_webp / grand_orig) * 100 if grand_orig > 0 else 0
        print(f"  TOTAL : {grand_count} images converted")
        print(f"  Before: {format_size(grand_orig)}")
        print(f"  After : {format_size(grand_webp)}")
        print(f"  Saved : {format_size(grand_orig - grand_webp)} (-{total_saving_pct:.0f}%)")
    else:
        print("  No new images to convert.")
    print("=" * 65)


if __name__ == "__main__":
    main()
