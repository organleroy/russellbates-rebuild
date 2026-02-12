import os, re, json, shutil, sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependency: beautifulsoup4. Install with: python3 -m pip install beautifulsoup4")
    raise

def norm_player_src(src: str) -> str:
    if not src:
        return ""
    if src.startswith("//"):
        return "https:" + src
    return src

def parse_home_tiles(home_html: str):
    soup = BeautifulSoup(home_html, "html.parser")
    tiles = []
    for a in soup.find_all("a", href=re.compile(r"/work/")):
        href = a.get("href", "")
        m = re.search(r"/work/([^/]+)/", href)
        if not m:
            continue
        slug = m.group(1)
        li = a.find_parent("li")
        if not li:
            continue
        style = li.get("style", "")
        thumb = None
        m2 = re.search(r"background-image:\s*url\(([^)]+)\)", style)
        if m2:
            thumb = m2.group(1).strip("'\"")
        h3 = li.find("h3")
        title = h3.get_text(" ", strip=True) if h3 else None
        p = li.find("p")
        subtitle = p.get_text(" ", strip=True) if p else None
        tiles.append({"slug": slug, "thumb": thumb, "title": title, "subtitle": subtitle})
    # De-dupe by slug preserving order
    seen = set()
    out = []
    for t in tiles:
        if t["slug"] in seen:
            continue
        seen.add(t["slug"])
        out.append(t)
    return out

def parse_project_html(project_html: str):
    soup = BeautifulSoup(project_html, "html.parser")
    content = soup.find(id="content-body") or soup
    h1 = content.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else None

    iframe = content.find("iframe", src=re.compile("vimeo"))
    vimeo_src = norm_player_src(iframe.get("src")) if iframe else None
    vimeo_id = None
    if vimeo_src:
        m = re.search(r"video/(\d+)", vimeo_src)
        if m:
            vimeo_id = m.group(1)

    # Blurb: first paragraph inside content-text (if present)
    blurb = None
    ct = content.find("div", class_="content-text")
    if ct:
        first_p = ct.find("p")
        if first_p:
            blurb = first_p.get_text(" ", strip=True)

    # OG image
    og = soup.find("meta", attrs={"property": "og:image"})
    og_image = og.get("content") if og else None

    # Featured work strip on work pages often uses same tile-list; grab first 8 slugs
    featured = []
    for a in soup.find_all("a", href=re.compile(r"/work/")):
        href = a.get("href", "")
        m = re.search(r"/work/([^/]+)/", href)
        if m:
            featured.append(m.group(1))
    # Remove self + de-dupe, keep first 8
    if featured:
        seen = set()
        cleaned = []
        for s in featured:
            if s == "" or s == None:
                continue
            if s in seen:
                continue
            seen.add(s)
            cleaned.append(s)
        featured = [s for s in cleaned if s != ""]
    return {"title": title, "vimeo_id": vimeo_id, "vimeo_src": vimeo_src, "blurb": blurb, "og_image": og_image, "featured_slugs": featured[:8]}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/extract_from_simply_static.py /path/to/simply-static-export")
        sys.exit(1)

    export_root = Path(sys.argv[1]).expanduser().resolve()
    if not export_root.exists():
        print(f"Export folder not found: {export_root}")
        sys.exit(1)

    home_html = (export_root / "index.html").read_text(encoding="utf-8", errors="ignore")
    home_tiles = parse_home_tiles(home_html)
    home_by_slug = {t["slug"]: t for t in home_tiles}

    work_dir = export_root / "work"
    slugs = [p.name for p in work_dir.iterdir() if p.is_dir()]

    projects = []
    for slug in slugs:
        page = work_dir / slug / "index.html"
        if not page.exists():
            continue
        html = page.read_text(encoding="utf-8", errors="ignore")
        if "player.vimeo.com" not in html:
            continue
        p = parse_project_html(html)
        if not p.get("vimeo_id"):
            continue
        p["slug"] = slug

        # Prefer homepage tile title/thumb/subtitle if present
        ht = home_by_slug.get(slug)
        if ht:
            p["featured_home"] = True
            if ht.get("title"):
                p["title"] = ht["title"]
            p["thumb"] = ht.get("thumb") or p.get("og_image")
            p["subtitle"] = ht.get("subtitle")
        else:
            p["featured_home"] = False
            p["thumb"] = p.get("og_image")

        # Normalize image paths to new assets location (we'll copy uploads)
        def rewrite_img(path):
            if not path:
                return None
            # convert /wp-content/uploads/... -> /assets/uploads/...
            return re.sub(r"^/wp-content/uploads/", "/assets/uploads/", path)

        p["thumb"] = rewrite_img(p.get("thumb"))
        p["og_image"] = rewrite_img(p.get("og_image"))

        # Featured slugs keep as-is
        projects.append(p)

    # Sort: homepage featured first in homepage order, then rest alpha
    order = {t["slug"]: i for i, t in enumerate(home_tiles)}
    projects.sort(key=lambda x: (0, order.get(x["slug"], 10**9)) if x.get("featured_home") else (1, x["title"] or x["slug"]))

    # Write JSON into src/content/projects.json
    out_json = Path(__file__).resolve().parent.parent / "src" / "content" / "projects.json"
    out_json.write_text(json.dumps(projects, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(projects)} projects -> {out_json}")

    # Copy uploads to src/assets/uploads
    src_uploads = export_root / "wp-content" / "uploads"
    dst_uploads = Path(__file__).resolve().parent.parent / "src" / "assets" / "uploads"
    if src_uploads.exists():
        if dst_uploads.exists():
            shutil.rmtree(dst_uploads)
        shutil.copytree(src_uploads, dst_uploads)
        print(f"Copied uploads -> {dst_uploads} (this can be large)")
    else:
        print(f"Uploads folder not found at {src_uploads}")

if __name__ == "__main__":
    main()
