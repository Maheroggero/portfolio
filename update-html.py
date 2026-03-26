"""
HTML update script for WebP migration.
- Wraps local <img> tags in <picture> with WebP <source>
- Adds loading="lazy" to non-hero images
- Adds picture { display: contents } CSS rule to each file
Run: python update-html.py
"""

import re
from pathlib import Path

ROOT = Path(r"d:\AI\Websites\Project_clone")

def is_external(src):
    return src.startswith('http://') or src.startswith('https://')

def webp_src(src):
    """Return WebP path (same path, .webp extension)."""
    return str(Path(src).with_suffix('.webp')).replace('\\', '/')

def picture_wrap(img_html, webp, lazy=True):
    """Wrap an <img ...> string in <picture> with WebP source."""
    # Inject loading="lazy" before the closing >
    if lazy:
        img_html = re.sub(r'\s*/?>$', ' loading="lazy">', img_html.strip())
    # Detect indentation of the img tag
    stripped = img_html.lstrip()
    indent = img_html[: len(img_html) - len(stripped)]
    inner_indent = indent + '  '
    return (
        f'{indent}<picture>\n'
        f'{inner_indent}<source srcset="{webp}" type="image/webp">\n'
        f'{inner_indent}{stripped}\n'
        f'{indent}</picture>'
    )

def process_img_tag(m, lazy=True):
    """Regex match callback: decide whether to wrap or not."""
    full = m.group(0)
    src_m = re.search(r'src=["\']([^"\']+)["\']', full)
    if not src_m:
        return full
    src = src_m.group(1)
    if is_external(src):
        # External URL: just add loading=lazy, no picture wrapper
        if lazy and 'loading=' not in full:
            full = re.sub(r'\s*/?>$', ' loading="lazy">', full.rstrip())
        return full
    return picture_wrap(full, webp_src(src), lazy)

# ─── projects.html ───────────────────────────────────────────────────────────

def update_projects():
    path = ROOT / 'projects.html'
    html = path.read_text(encoding='utf-8')

    # 1. CSS: add picture rule after ".project-img img" block
    css_insert = '\n    .project-img picture { display: contents; }'
    html = html.replace(
        '.project-img img {\n      width: 100%;\n      height: 100%;\n      object-fit: cover;\n      display: block;\n    }',
        '.project-img img {\n      width: 100%;\n      height: 100%;\n      object-fit: cover;\n      display: block;\n    }' + css_insert
    )

    # 2. HTML: wrap every local <img> inside .projects-grid in <picture>
    # All images are below the fold → all get loading="lazy"
    def replace_img(m):
        return process_img_tag(m, lazy=True)

    # Only replace img tags inside the projects-grid div
    grid_start = html.index('<div class="projects-grid">')
    grid_end   = html.index('</div>\n  </div>\n\n  <script>', grid_start)
    grid_html  = html[grid_start:grid_end]

    img_pattern = re.compile(r'[ \t]*<img\b[^>]*>', re.DOTALL)
    new_grid_html = img_pattern.sub(replace_img, grid_html)

    html = html[:grid_start] + new_grid_html + html[grid_end:]
    path.write_text(html, encoding='utf-8')
    print('OK projects.html updated')


# ─── index.html ──────────────────────────────────────────────────────────────

def update_index():
    path = ROOT / 'index.html'
    html = path.read_text(encoding='utf-8')

    # 1. CSS: add picture rule for carousel
    css_insert = '\n    .carousel-track picture { display: contents; }'
    html = html.replace(
        '.carousel-track img {\n      height: 100%;\n      width: auto;\n      object-fit: cover;\n      display: block;\n      flex-shrink: 0;\n      user-select: none;\n      -webkit-user-drag: none;\n    }',
        '.carousel-track img {\n      height: 100%;\n      width: auto;\n      object-fit: cover;\n      display: block;\n      flex-shrink: 0;\n      user-select: none;\n      -webkit-user-drag: none;\n    }' + css_insert
    )

    # 2. HTML: wrap carousel images in <picture>, NO loading=lazy (all visible)
    track_start = html.index('<div class="carousel-track"')
    track_end   = html.index('</div>\n    </div>\n\n  </div>', track_start)
    track_html  = html[track_start:track_end]

    img_pattern = re.compile(r'[ \t]*<img\b[^>]*>', re.DOTALL)
    new_track_html = img_pattern.sub(lambda m: process_img_tag(m, lazy=False), track_html)

    html = html[:track_start] + new_track_html + html[track_end:]
    path.write_text(html, encoding='utf-8')
    print('OK index.html updated')


# ─── Project pages ────────────────────────────────────────────────────────────

PROJECT_PAGES = [
    'prada.html',
    'tokyo.html',
    'nike.html',
    'oakley.html',
    'morocco.html',
    'bold-agency.html',
    'tam.html',
    'vecchia.html',
    'photography.html',
]

# CSS insertion target (same in every project page)
IMG_WRAP_CSS = '.img-wrap img { width: 100%; height: auto; display: block; }'
IMG_WRAP_CSS_ALT = '.img-wrap img { width: 100%; height: 100%; object-fit: cover; display: block; }'  # photography.html

def update_project_page(filename):
    path = ROOT / filename
    html = path.read_text(encoding='utf-8')

    # 1. CSS: add picture display rule
    css_rule = '\n    .img-wrap picture { display: contents; }'
    if IMG_WRAP_CSS in html:
        html = html.replace(IMG_WRAP_CSS, IMG_WRAP_CSS + css_rule, 1)
    elif IMG_WRAP_CSS_ALT in html:
        html = html.replace(IMG_WRAP_CSS_ALT, IMG_WRAP_CSS_ALT + css_rule, 1)

    # 2. HTML: wrap images in <picture>
    # First, find the project-images div
    try:
        images_start = html.index('<div class="project-images">')
        images_end   = html.index('</div>\n  </div>\n\n  <script>', images_start)
    except ValueError:
        try:
            images_end = html.index('</div>\n  </div>\n\n</body>', images_start)
        except ValueError:
            print(f'  WARNING: Could not find end of project-images in {filename}')
            path.write_text(html, encoding='utf-8')
            return

    images_html = html[images_start:images_end]

    # Track whether we've seen the first real <img> (for hero detection)
    first_img_done = [False]

    def replace_img(m):
        full = m.group(0)
        # Check if this img is in a hero row
        # We detect "hero" by checking if the match is inside an img-row hero div
        # Simple heuristic: the first <img> tag in the images block is the hero
        # (if it's local). After that, all are lazy.
        is_hero = not first_img_done[0]

        src_m = re.search(r'src=["\']([^"\']+)["\']', full)
        if src_m and is_external(src_m.group(1)):
            # External image: just add loading=lazy, no picture
            first_img_done[0] = True  # external doesn't count as the hero check trigger
            if 'loading=' not in full:
                full = re.sub(r'\s*/?>$', ' loading="lazy">', full.rstrip())
            return full

        # Local image
        first_img_done[0] = True
        lazy = not is_hero
        if src_m:
            return picture_wrap(full, webp_src(src_m.group(1)), lazy)
        return full

    img_pattern = re.compile(r'[ \t]*<img\b[^>]*>', re.DOTALL)
    new_images_html = img_pattern.sub(replace_img, images_html)

    html = html[:images_start] + new_images_html + html[images_end:]
    path.write_text(html, encoding='utf-8')
    print(f'OK {filename} updated')


# ─── Run all ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    update_projects()
    update_index()
    for page in PROJECT_PAGES:
        update_project_page(page)
    print('\nAll HTML files updated.'  )
