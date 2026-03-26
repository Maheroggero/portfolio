from PIL import Image
from pathlib import Path

ROOT = Path("d:/AI/Websites/Project_clone")
MAX_W = 2400
QUALITY = 80

targets = [
    (ROOT / "TamRender/Mockup1.png",          ROOT / "TamRender/Mockup1-full.webp"),
    (ROOT / "BoldRender/mockupsite.jpg",       ROOT / "BoldRender/mockupsite-full.webp"),
    (ROOT / "03_RENDER/frame2Color.jpg",       ROOT / "03_RENDER/frame2Color-full.webp"),
    (ROOT / "TokyoRender/Logo2.png",           ROOT / "TokyoRender/Logo2-full.webp"),
    (ROOT / "prada/Mockup_city.jpg",           ROOT / "prada/Mockup_city-full.webp"),
    (ROOT / "NikeRender/billboard.png",        ROOT / "NikeRender/billboard-full.webp"),
    (ROOT / "Oakley/Frame.Still001.jpg",       ROOT / "Oakley/Frame.Still001-full.webp"),
    (ROOT / "restaurantRender/updated.jpg",    ROOT / "restaurantRender/updated-full.webp"),
]

for src, dest in targets:
    with Image.open(src) as img:
        w, h = img.size
        if w > MAX_W:
            img = img.resize((MAX_W, int(h * MAX_W / w)), Image.LANCZOS)
        img.convert("RGB").save(dest, "WEBP", quality=QUALITY, method=6)
    print(f"{src.name:30s} -> {dest.name:35s}  {dest.stat().st_size // 1024}KB")
