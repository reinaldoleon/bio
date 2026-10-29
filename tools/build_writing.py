"""Build versioned Markdown writing into static pages for GitHub Pages."""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml
from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "writing"
OUTPUT = ROOT / "writing"
SITE = "https://reinaldoleon.github.io/bio"
PILLARS = {
    "AI Platform Engineering",
    "Agentic Systems",
    "AI Reliability & Evaluation",
    "AI Governance",
    "AI Enablement",
    "Platform Engineering / SRE / FinOps",
}
PROJECTS = {
    "growthmesh": "GrowthMesh",
    "causio": "CAUSIO",
    "ecos-inmersivos": "Ecos Inmersivos",
    "ai-conversacional-lab": "AI Conversacional Lab",
}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN = MarkdownIt("commonmark", {"html": False, "linkify": False})


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def bilingual(en: str, es: str) -> str:
    return f'<span class="lang-en">{esc(en)}</span><span class="lang-es">{esc(es)}</span>'


def parse_article(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", source, re.S)
    if not match:
        raise ValueError(f"{path}: expected YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    required = ("title", "slug", "date", "description", "tags", "pillar")
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise ValueError(f"{path}: missing {', '.join(missing)}")
    if not SLUG.fullmatch(str(data["slug"])) or path.stem != data["slug"]:
        raise ValueError(f"{path}: slug must match the filename and use lowercase hyphens")
    if data["pillar"] not in PILLARS:
        raise ValueError(f"{path}: unknown pillar {data['pillar']}")
    if not isinstance(data["tags"], list) or not all(isinstance(tag, str) for tag in data["tags"]):
        raise ValueError(f"{path}: tags must be a list of strings")
    if data.get("project") and data["project"] not in PROJECTS:
        raise ValueError(f"{path}: unknown project {data['project']}")
    if type(data.get("draft", False)) is not bool or type(data.get("featured", False)) is not bool:
        raise ValueError(f"{path}: draft and featured must be booleans")
    published = data["date"]
    if isinstance(published, str):
        published = date.fromisoformat(published)
    if not isinstance(published, date):
        raise ValueError(f"{path}: date must be YYYY-MM-DD")
    data["date"] = published
    if data.get("linkedin_published_at"):
        linked_date = data["linkedin_published_at"]
        if isinstance(linked_date, str):
            date.fromisoformat(linked_date)
        elif not isinstance(linked_date, date):
            raise ValueError(f"{path}: invalid linkedin_published_at")
    if data.get("linkedin_url") and not str(data["linkedin_url"]).startswith("https://www.linkedin.com/"):
        raise ValueError(f"{path}: linkedin_url must be a LinkedIn HTTPS URL")
    data["body"] = MARKDOWN.render(match.group(2))
    return data


def head(title: str, description: str, canonical: str, prefix: str, page_type: str, published: date | None = None, description_es: str | None = None) -> str:
    image = f"{SITE}/assets/images/social-card.png"
    meta = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{esc(description)}"' + (f' data-description-en="{esc(description)}" data-description-es="{esc(description_es)}"' if description_es else "") + '>',
        f'<link rel="canonical" href="{esc(canonical)}">',
        '<meta name="author" content="Reinaldo León">',
        f'<meta property="og:type" content="{page_type}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:url" content="{esc(canonical)}">',
        f'<meta property="og:image" content="{image}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(description)}">',
        f'<meta name="twitter:image" content="{image}">',
        f'<link rel="alternate" type="application/rss+xml" title="Reinaldo León — Writing" href="{SITE}/writing/feed.xml">',
        f'<link rel="icon" type="image/png" href="{prefix}assets/images/avatar.png">',
        f'<link rel="stylesheet" href="{prefix}assets/css/style.css">',
    ]
    if published:
        meta.append(f'<meta property="article:published_time" content="{published.isoformat()}">')
    return "\n  ".join(meta)


def shell(title: str, description: str, canonical: str, prefix: str, main: str, page_type: str = "website", published: date | None = None, structured: str = "", bilingual_ui: bool = False, description_es: str | None = None) -> str:
    labels = [
        bilingual("About", "Sobre mí") if bilingual_ui else "About",
        bilingual("Experience", "Experiencia") if bilingual_ui else "Experience",
        bilingual("Projects", "Proyectos") if bilingual_ui else "Projects",
        bilingual("Writing", "Artículos") if bilingual_ui else "Writing",
        bilingual("Contact", "Contacto") if bilingual_ui else "Contact",
    ]
    language_switch = '''<li><div class="lang-selector"><button class="lang-btn active" data-lang-set="en" aria-label="Set language to English">EN</button><span class="lang-divider">|</span><button class="lang-btn" data-lang-set="es" aria-label="Establecer idioma en Español">ES</button></div></li>''' if bilingual_ui else ""
    header = f'''<header><div class="container nav-wrapper">
      <a class="logo" href="{prefix}index.html">Reinaldo León</a>
      <button class="mobile-nav-toggle" id="mobile-toggle" aria-controls="nav-links" aria-expanded="false" aria-label="Toggle navigation">☰</button>
      <nav><ul class="nav-links" id="nav-links">
        <li><a href="{prefix}index.html#about">{labels[0]}</a></li>
        <li><a href="{prefix}index.html#experience">{labels[1]}</a></li>
        <li><a href="{prefix}index.html#projects">{labels[2]}</a></li>
        <li><a href="{prefix}writing/" aria-current="page">{labels[3]}</a></li>
        <li><a href="{prefix}index.html#contact">{labels[4]}</a></li>
        <li><button class="theme-toggle-btn" id="theme-toggle" aria-label="Toggle theme"><svg class="moon-icon" viewBox="0 0 20 20" fill="currentColor"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/></svg><svg class="sun-icon" viewBox="0 0 20 20" fill="currentColor"><circle cx="10" cy="10" r="4"/></svg></button></li>
        {language_switch}
      </ul></nav></div></header>'''
    page = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark" data-lang="en">
<head>
  {head(title, description, canonical, prefix, page_type, published, description_es)}
  {structured}
</head>
<body>
  {header}
  <main class="container writing-main">{main}</main>
  <footer><div class="container footer-content"><p class="footer-text">© Reinaldo León · <a href="{prefix}index.html">{bilingual("Professional bio", "Bio profesional") if bilingual_ui else "Professional bio"}</a> · <a href="{prefix}writing/feed.xml">RSS</a></p></div></footer>
  <script src="{prefix}assets/js/main.js"></script>
</body>
</html>
'''
    return "\n".join(line.rstrip() for line in page.splitlines()) + "\n"


def article_card(article: dict, prefix: str) -> str:
    url = f"{prefix}writing/{article['slug']}/"
    tags = "".join(f'<span class="project-tag">{esc(tag)}</span>' for tag in article["tags"])
    return f'''<article class="glass-card writing-card">
      <p class="writing-meta"><time datetime="{article['date'].isoformat()}">{article['date'].isoformat()}</time> · {esc(article['pillar'])}</p>
      <h2><a href="{url}">{esc(article['title'])}</a></h2>
      <p>{bilingual(article['description'], article.get('description_es', article['description']))}</p>
      <div class="project-tags">{tags}</div>
      <a class="project-link" href="{url}">{bilingual("Read article (English) →", "Leer artículo (en inglés) →")}</a>
    </article>'''


def build() -> None:
    articles = [parse_article(path) for path in sorted(SOURCE.glob("*.md")) if not path.name.startswith("_")]
    slugs = [article["slug"] for article in articles]
    if len(slugs) != len(set(slugs)):
        raise ValueError("duplicate article slug")
    articles = [article for article in articles if not article.get("draft", False)]
    articles.sort(key=lambda article: (article.get("featured", False), article["date"], article["slug"]), reverse=True)
    OUTPUT.mkdir(exist_ok=True)
    manifest = OUTPUT / ".generated-slugs"
    previous = set(manifest.read_text(encoding="utf-8").splitlines()) if manifest.exists() else set()
    current = {article["slug"] for article in articles}
    for slug in previous - current:
        if not SLUG.fullmatch(slug):
            raise ValueError(f"invalid generated slug in manifest: {slug}")
        stale = OUTPUT / slug / "index.html"
        if stale.exists():
            if set(stale.parent.iterdir()) != {stale}:
                raise ValueError(f"refusing to remove generated directory with extra files: {stale.parent}")
            stale.unlink()
            stale.parent.rmdir()
    cards = "\n".join(article_card(article, "../") for article in articles)
    if not cards:
        cards = '<p class="glass-card">' + bilingual("Articles are being prepared. Follow the RSS feed for updates.", "Estamos preparando nuevos artículos. Sigue el RSS para recibir novedades.") + '</p>'
    index_main = f'''<section class="writing-landing">
      <p class="section-pretitle">{bilingual("Field notes", "Notas técnicas")}</p>
      <h1>Writing</h1>
      <p class="section-intro">{bilingual("Long-form notes on AI Platform Engineering, agentic systems, reliability, governance and the platform foundations behind them. Projects are evidence within these themes.", "Artículos sobre AI Platform Engineering, sistemas agénticos, fiabilidad, gobierno y los fundamentos de plataforma que los sostienen. Los proyectos aportan evidencia dentro de estos temas.")}</p>
      <p class="writing-follow">{bilingual("This site is the canonical home for articles. LinkedIn is where shorter versions and conversations happen. Articles are currently written in English.", "Esta web es la fuente canónica de los artículos. LinkedIn acoge versiones breves y conversaciones. Por ahora, los artículos están escritos en inglés.")}</p>
      <div class="writing-list">{cards}</div>
    </section>'''
    (OUTPUT / "index.html").write_text(shell("Writing | Reinaldo León", "Technical writing on AI Platform Engineering, AI Enablement, agentic systems, reliability and governance.", f"{SITE}/writing/", "../", index_main, bilingual_ui=True, description_es="Artículos técnicos sobre AI Platform Engineering, AI Enablement, sistemas agénticos, fiabilidad y gobierno."), encoding="utf-8")

    for article in articles:
        url = f"{SITE}/writing/{article['slug']}/"
        project = article.get("project")
        related = f'<p class="related-project">Related project: <a href="../../index.html#project-{project}">{esc(PROJECTS[project])}</a></p>' if project else ""
        linkedin = f'<p class="writing-linkedin"><a href="{esc(article["linkedin_url"])}" rel="noopener noreferrer" target="_blank">Discuss on LinkedIn ↗</a></p>' if article.get("linkedin_url") else ""
        tags = "".join(f'<span class="project-tag">{esc(tag)}</span>' for tag in article["tags"])
        main = f'''<article class="writing-article">
          <p class="writing-back"><a href="../../writing/">← All writing</a></p>
          <p class="writing-language">Article in English</p>
          <p class="writing-meta"><time datetime="{article['date'].isoformat()}">{article['date'].isoformat()}</time> · {esc(article['pillar'])}</p>
          <h1>{esc(article['title'])}</h1>
          <p class="writing-deck">{esc(article['description'])}</p>
          <div class="project-tags">{tags}</div>
          <div class="writing-prose">{article['body']}</div>
          {related}{linkedin}
        </article>'''
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": article["title"],
            "description": article["description"],
            "datePublished": article["date"].isoformat(),
            "author": {"@type": "Person", "name": "Reinaldo León", "url": f"{SITE}/"},
            "mainEntityOfPage": url,
            "image": f"{SITE}/assets/images/social-card.png",
        }
        structured = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c") + "</script>"
        target = OUTPUT / article["slug"]
        target.mkdir(exist_ok=True)
        (target / "index.html").write_text(shell(f"{article['title']} | Reinaldo León", article["description"], url, "../../", main, "article", article["date"], structured), encoding="utf-8")

    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    sitemap = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
    for url in [f"{SITE}/", f"{SITE}/writing/"] + [f"{SITE}/writing/{a['slug']}/" for a in articles]:
        ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = url
    (ROOT / "sitemap.xml").write_bytes(ET.tostring(sitemap, encoding="utf-8", xml_declaration=True))

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for tag, value in (("title", "Reinaldo León — Writing"), ("link", f"{SITE}/writing/"), ("description", "Technical writing on AI Platform Engineering and reliable AI systems."), ("language", "en")):
        ET.SubElement(channel, tag).text = value
    for article in articles:
        item = ET.SubElement(channel, "item")
        link = f"{SITE}/writing/{article['slug']}/"
        for tag, value in (("title", article["title"]), ("link", link), ("guid", link), ("description", article["description"]), ("pubDate", article["date"].strftime("%a, %d %b %Y 00:00:00 GMT"))):
            ET.SubElement(item, tag).text = value
    (OUTPUT / "feed.xml").write_bytes(ET.tostring(rss, encoding="utf-8", xml_declaration=True))
    manifest.write_text("".join(f"{slug}\n" for slug in sorted(current)), encoding="utf-8")
    print(f"Built {len(articles)} article(s), Writing index, sitemap and RSS")


if __name__ == "__main__":
    build()
