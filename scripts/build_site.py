#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import re
import shutil
from pathlib import Path
from typing import Any

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BLOG_SRC = ROOT / "blog"
BLOG_DIST = DIST / "blog"
POSTS_SRC = ROOT / "posts"

SITE_NAME = "杨森的学习笔记"
SITE_SUBTITLE = "技术学习笔记和博客"
SITE_YEAR = "2026"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def clean_text(raw: str) -> str:
    # Keep text safe for HTML rendering and remove noisy extra spaces.
    return re.sub(r"\s+", " ", html.unescape(raw)).strip()


def strip_tags(raw_html: str) -> str:
    return clean_text(re.sub(r"<[^>]+>", "", raw_html))


def parse_date(value: str | None, fallback: dt.date) -> dt.date:
    if not value:
        return fallback
    value = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return dt.datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return fallback


def slugify(stem: str) -> str:
    slug = stem.lower().strip()
    slug = re.sub(r"[ _]+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-]+", "", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if slug:
        return slug
    digits = re.sub(r"[^0-9]", "", stem)
    return f"post-{digits or 'item'}"


def get_first_markdown_heading(content: str) -> str | None:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", content)
    return match.group(1).strip() if match else None


def get_markdown_summary(content: str) -> str:
    for line in content.splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith("#") or text.startswith(">") or text.startswith("```"):
            continue
        text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
        text = re.sub(r"[*_`~]", "", text).strip()
        if text:
            return text[:160]
    return "暂无摘要。"


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        return {}, text

    front_matter_text = "\n".join(lines[1:end_index])
    body = "\n".join(lines[end_index + 1 :]).lstrip("\n")
    parsed = yaml.safe_load(front_matter_text) or {}
    return parsed if isinstance(parsed, dict) else {}, body


def article_template(title: str, meta_text: str, body_html: str, tags: list[str]) -> str:
    tags_html = ""
    if tags:
        tag_spans = "\n".join(
            f'                <span class="tag">{html.escape(tag)}</span>' for tag in tags
        )
        tags_html = f"""
            <div class="tags">
{tag_spans}
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - {SITE_NAME}</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <h1>{SITE_NAME}</h1>
        <p class="subtitle">{SITE_SUBTITLE}</p>
    </header>

    <nav>
        <ul>
            <li><a href="../index.html">首页</a></li>
            <li><a href="../archives.html">归档</a></li>
            <li><a href="../about.html">关于</a></li>
        </ul>
    </nav>

    <main class="container container-wide">
        <article class="article-content">
            <div class="post-meta">{html.escape(meta_text)}</div>
            <h1>{html.escape(title)}</h1>

{body_html}{tags_html}
        </article>
    </main>

    <footer>
        <p>&copy; {SITE_YEAR} {SITE_NAME}</p>
    </footer>

    <script src="../js/script.js"></script>
</body>
</html>
"""


def parse_markdown_post(md_path: Path) -> dict[str, Any]:
    raw_text = read_text(md_path)
    fm, body_md = split_front_matter(raw_text)

    title = str(fm.get("title") or get_first_markdown_heading(body_md) or md_path.stem).strip()
    date_value = fm.get("date")
    date_fallback = dt.datetime.fromtimestamp(md_path.stat().st_mtime).date()
    post_date = parse_date(str(date_value) if date_value is not None else None, date_fallback)
    category = str(fm.get("category") or "技术笔记").strip()
    summary = str(fm.get("summary") or get_markdown_summary(body_md)).strip()

    tags_raw = fm.get("tags", [])
    if isinstance(tags_raw, str):
        tags = [x.strip() for x in tags_raw.split(",") if x.strip()]
    elif isinstance(tags_raw, list):
        tags = [str(x).strip() for x in tags_raw if str(x).strip()]
    else:
        tags = []

    custom_slug = str(fm.get("slug") or "").strip()
    slug = slugify(custom_slug or md_path.stem)
    output_filename = f"{slug}.html"
    url = f"blog/{output_filename}"

    body_html = markdown.markdown(
        body_md,
        extensions=[
            "fenced_code",
            "tables",
            "sane_lists",
            "toc",
        ],
    )
    body_html = re.sub(r"(?m)^", "            ", body_html)

    meta_text = f"{post_date.isoformat()} · {category}"
    article_html = article_template(title, meta_text, body_html, tags)
    write_text(BLOG_DIST / output_filename, article_html)

    return {
        "title": title,
        "date": post_date,
        "date_text": post_date.isoformat(),
        "category": category,
        "summary": summary,
        "url": url,
    }


def parse_legacy_html_post(html_path: Path) -> dict[str, Any] | None:
    raw = read_text(html_path)
    article_match = re.search(
        r'<article\s+class="article-content".*?>(.*?)</article>', raw, flags=re.DOTALL | re.IGNORECASE
    )
    if not article_match:
        return None

    article = article_match.group(1)
    title_match = re.search(r"<h1>(.*?)</h1>", article, flags=re.DOTALL | re.IGNORECASE)
    if not title_match:
        return None
    title = strip_tags(title_match.group(1))
    if not title:
        return None

    meta_match = re.search(
        r'<div\s+class="post-meta">(.*?)</div>', article, flags=re.DOTALL | re.IGNORECASE
    )
    meta_text = clean_text(meta_match.group(1)) if meta_match else ""
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", meta_text)
    if date_match:
        post_date = parse_date(date_match.group(1), dt.date.today())
        date_text = date_match.group(1)
    else:
        post_date = dt.date.today()
        date_text = post_date.isoformat()

    category = "技术笔记"
    if "·" in meta_text:
        right = meta_text.split("·", 1)[1].strip()
        category = right or category

    para_match = re.search(r"<p>(.*?)</p>", article, flags=re.DOTALL | re.IGNORECASE)
    summary = strip_tags(para_match.group(1))[:160] if para_match else "暂无摘要。"

    return {
        "title": title,
        "date": post_date,
        "date_text": date_text,
        "category": category,
        "summary": summary,
        "url": f"blog/{html_path.name}",
    }


def generate_index(posts: list[dict[str, Any]]) -> str:
    cards = []
    for post in posts:
        cards.append(
            f"""        <article class="post">
            <div class="post-meta">{post["date_text"]} · {html.escape(post["category"])}</div>
            <h2><a href="{post["url"]}" class="post-link">{html.escape(post["title"])}</a></h2>
            <div class="post-content">
                <p>{html.escape(post["summary"])}</p>
            </div>
            <a href="{post["url"]}" class="read-more">阅读全文</a>
        </article>"""
        )

    cards_html = "\n\n".join(cards) if cards else """        <article class="post">
            <h2>暂无文章</h2>
            <div class="post-content">
                <p>请将 Markdown 文件放到 posts 目录，推送后会自动生成页面。</p>
            </div>
        </article>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SITE_NAME}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>{SITE_NAME}</h1>
        <p class="subtitle">{SITE_SUBTITLE}</p>
    </header>

    <nav>
        <ul>
            <li><a href="index.html">首页</a></li>
            <li><a href="archives.html">归档</a></li>
            <li><a href="about.html">关于</a></li>
        </ul>
    </nav>

    <main class="container">
{cards_html}
    </main>

    <footer>
        <p>&copy; {SITE_YEAR} {SITE_NAME}</p>
    </footer>

    <script src="js/script.js"></script>
</body>
</html>
"""


def month_label(year: int, month: int) -> str:
    return f"{year} 年 {month} 月"


def generate_archives(posts: list[dict[str, Any]]) -> str:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for post in posts:
        ym = (post["date"].year, post["date"].month)
        grouped.setdefault(ym, []).append(post)

    sections = []
    for ym in sorted(grouped.keys(), reverse=True):
        items = "\n".join(
            f"""                <li>
                    <a href="{post["url"]}">
                        <span>{html.escape(post["title"])}</span>
                        <span>{post["date_text"]}</span>
                    </a>
                </li>"""
            for post in grouped[ym]
        )
        sections.append(
            f"""            <h3>{month_label(ym[0], ym[1])}</h3>
            <ul>
{items}
            </ul>"""
        )

    sections_html = "\n\n".join(sections) if sections else """            <h3>暂无文章</h3>
            <ul>
                <li>
                    <span>请将 Markdown 文件放到 posts 目录</span>
                    <span>-</span>
                </li>
            </ul>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>归档 - {SITE_NAME}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>{SITE_NAME}</h1>
        <p class="subtitle">{SITE_SUBTITLE}</p>
    </header>

    <nav>
        <ul>
            <li><a href="index.html">首页</a></li>
            <li><a href="archives.html">归档</a></li>
            <li><a href="about.html">关于</a></li>
        </ul>
    </nav>

    <main class="container">
        <section class="archive">
            <h2>文章归档</h2>

{sections_html}
        </section>
    </main>

    <footer>
        <p>&copy; {SITE_YEAR} {SITE_NAME}</p>
    </footer>

    <script src="js/script.js"></script>
</body>
</html>
"""


def prepare_dist() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)
    BLOG_DIST.mkdir(parents=True, exist_ok=True)


def copy_static_assets() -> None:
    for folder in ("css", "js"):
        src = ROOT / folder
        if src.exists():
            shutil.copytree(src, DIST / folder, dirs_exist_ok=True)

    for filename in ("about.html", "CNAME"):
        src = ROOT / filename
        if src.exists():
            shutil.copy2(src, DIST / filename)


def build() -> None:
    prepare_dist()
    copy_static_assets()

    generated_urls: set[str] = set()
    posts: list[dict[str, Any]] = []

    if POSTS_SRC.exists():
        for md_path in sorted(POSTS_SRC.rglob("*.md")):
            if md_path.name.lower() == "readme.md" or md_path.name.startswith("_"):
                continue
            post = parse_markdown_post(md_path)
            posts.append(post)
            generated_urls.add(post["url"])

    if BLOG_SRC.exists():
        for html_path in sorted(BLOG_SRC.glob("*.html")):
            url = f"blog/{html_path.name}"
            # If a markdown post generated the same output file, keep the markdown result.
            if url in generated_urls:
                continue
            shutil.copy2(html_path, BLOG_DIST / html_path.name)
            parsed = parse_legacy_html_post(html_path)
            if parsed and parsed["url"] not in generated_urls:
                posts.append(parsed)

    posts.sort(key=lambda p: p["date"], reverse=True)

    write_text(DIST / "index.html", generate_index(posts))
    write_text(DIST / "archives.html", generate_archives(posts))

    print(f"Built {len(posts)} posts into {DIST}")


if __name__ == "__main__":
    build()
