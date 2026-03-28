from datetime import datetime
from pathlib import Path
import re

from flask import Flask, abort, render_template

app = Flask(__name__)

POSTS_DIR = Path(__file__).parent / "posts"
BLOG_ENABLED = False


def parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta_text = parts[1]
    body = parts[2]
    meta = {}
    for line in meta_text.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip()
    return meta, body.lstrip()


def inline_links(text):
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)


def basic_markdown(text):
    lines = text.strip().splitlines()
    html_lines = []
    in_list = False
    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue
        if line.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3>{inline_links(line[4:])}</h3>")
            continue
        if line.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2>{inline_links(line[3:])}</h2>")
            continue
        if line.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h1>{inline_links(line[2:])}</h1>")
            continue
        if line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{inline_links(line[2:])}</li>")
            continue
        if in_list:
            html_lines.append("</ul>")
            in_list = False
        html_lines.append(f"<p>{inline_links(line)}</p>")
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def markdown_to_html(text):
    try:
        import markdown
    except ImportError:
        return basic_markdown(text)
    return markdown.markdown(text, extensions=["extra"])


def parse_date(meta, path):
    date_str = meta.get("date", "")
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            pass
    return datetime.fromtimestamp(path.stat().st_mtime)


def extract_summary(body):
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return ""


def load_posts():
    posts = []
    if not POSTS_DIR.exists():
        return posts
    for path in sorted(POSTS_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(raw)
        date = parse_date(meta, path)
        tags_raw = meta.get("tags", "")
        tags = []
        for tag in [item.strip() for item in tags_raw.split(",") if item.strip()]:
            slug = re.sub(r"[^a-z0-9]+", "-", tag.lower()).strip("-")
            tags.append({"name": tag, "slug": slug})
        posts.append(
            {
                "slug": path.stem,
                "title": meta.get("title", path.stem.replace("-", " ").title()),
                "date": date,
                "date_display": date.strftime("%Y-%m-%d"),
                "summary": meta.get("summary", extract_summary(body)),
                "tags": tags,
                "body": markdown_to_html(body),
            }
        )
    posts.sort(key=lambda item: item["date"], reverse=True)
    return posts


def collect_tags(posts):
    tags = {}
    for post in posts:
        for tag in post["tags"]:
            entry = tags.setdefault(tag["slug"], {"name": tag["name"], "slug": tag["slug"], "count": 0})
            entry["count"] += 1
    return sorted(tags.values(), key=lambda item: item["name"].lower())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/blog")
def blog():
    if not BLOG_ENABLED:
        abort(404)
    posts = load_posts()
    return render_template("blog.html", posts=posts, tags=collect_tags(posts))


@app.route("/blog/<slug>")
def post(slug):
    if not BLOG_ENABLED:
        abort(404)

    posts = load_posts()
    post_data = next((item for item in posts if item["slug"] == slug), None)
    if post_data is None:
        abort(404)
    return render_template("post.html", post=post_data)


@app.route("/tags/<slug>")
def tag(slug):
    if not BLOG_ENABLED:
        abort(404)
    posts = load_posts()
    tagged_posts = [post for post in posts if any(tag["slug"] == slug for tag in post["tags"])]
    if not tagged_posts:
        abort(404)
    tag_name = next(
        (tag["name"] for post in tagged_posts for tag in post["tags"] if tag["slug"] == slug),
        slug,
    )
    return render_template("tag.html", posts=tagged_posts, tag_name=tag_name)


if __name__ == "__main__":
    app.run(debug=True)
