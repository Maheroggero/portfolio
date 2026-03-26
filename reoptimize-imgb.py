from PIL import Image
from pathlib import Path

ROOT = Path("d:/AI/Websites/Project_clone")
MAX_W = 1200
QUALITY = 72

targets = [
    # Already done
    (ROOT / "TamRender/Mockup1.png",            ROOT / "TamRender/Mockup1.webp"),
    (ROOT / "BoldRender/mockupsite.jpg",         ROOT / "BoldRender/mockupsite.webp"),
    (ROOT / "03_RENDER/frame2Color.jpg",         ROOT / "03_RENDER/frame2Color.webp"),
    # New batch
    (ROOT / "TokyoRender/Logo2.png",             ROOT / "TokyoRender/Logo2.webp"),
    (ROOT / "prada/Mockup_city.jpg",             ROOT / "prada/Mockup_city.webp"),
    (ROOT / "NikeRender/billboard.png",          ROOT / "NikeRender/billboard.webp"),
    (ROOT / "Oakley/Frame.Still001.jpg",         ROOT / "Oakley/Frame.Still001.webp"),
    (ROOT / "restaurantRender/updated.jpg",      ROOT / "restaurantRender/updated.webp"),
]

for src, dest in targets:
    before = dest.stat().st_size // 1024 if dest.exists() else 0
    with Image.open(src) as img:
        w, h = img.size
        if w > MAX_W:
            img = img.resize((MAX_W, int(h * MAX_W / w)), Image.LANCZOS)
        img.convert("RGB").save(dest, "WEBP", quality=QUALITY, method=6)
    after = dest.stat().st_size // 1024
    print(f"{src.name:30s}  {before}KB -> {after}KB")
