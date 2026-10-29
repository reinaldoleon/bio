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
PILLAR_ES = {
    "AI Platform Engineering": "Ingeniería de plataformas de IA",
    "Agentic Systems": "Sistemas agénticos",
    "AI Reliability & Evaluation": "Fiabilidad y evaluación de IA",
    "AI Governance": "Gobierno de IA",
    "AI Enablement": "Habilitación de IA",
    "Platform Engineering / SRE / FinOps": "Ingeniería de plataforma / SRE / FinOps",
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
    if data.get("slug_es") and not SLUG.fullmatch(str(data["slug_es"])):
        raise ValueError(f"{path}: invalid Spanish slug")
    if data.get("localized_routes") and not data.get("slug_es"):
        raise ValueError(f"{path}: localized routes require slug_es")
    published = data["date"]
    if isinstance(published, str):
        published = date.fromisoformat(published)
    if not isinstance(published, date):
        raise ValueError(f"{path}: date must be YYYY-MM-DD")
    data["date"] = published
    if data.get("updated"):
        updated = data["updated"]
        if isinstance(updated, str):
            updated = date.fromisoformat(updated)
        if not isinstance(updated, date) or updated < published:
            raise ValueError(f"{path}: updated must be on or after date")
        data["updated"] = updated
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


def parse_translation(path: Path) -> dict:
    source = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", source, re.S)
    if not match:
        raise ValueError(f"{path}: expected YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict) or not all(data.get(key) for key in ("title", "description")):
        raise ValueError(f"{path}: translation needs title and description")
    if not match.group(2).strip():
        raise ValueError(f"{path}: translation body is empty")
    data["body"] = MARKDOWN.render(match.group(2))
    return data


def head(title: str, description: str, canonical: str, prefix: str, page_type: str, published: date | None = None, title_es: str | None = None, description_es: str | None = None, *, locale: str | None = None, alternates: dict[str, str] | None = None, image: str | None = None, updated: date | None = None) -> str:
    image = image or f"{SITE}/assets/images/social-card.png"
    meta = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f'<title' + (f' data-title-en="{esc(title)}" data-title-es="{esc(title_es)}"' if title_es else "") + f'>{esc(title)}</title>',
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
        f'<script src="{prefix}assets/js/lang-init.js"></script>',
        f'<link rel="stylesheet" href="{prefix}assets/css/style.css">',
    ]
    if locale:
        meta.append(f'<meta property="og:image:alt" content="{esc(title)}">')
        meta.append(f'<meta name="twitter:image:alt" content="{esc(title)}">')
        meta.append(f'<meta property="og:locale" content="{locale}_{"US" if locale == "en" else "ES"}">')
        meta.append(f'<meta property="og:locale:alternate" content="{"es_ES" if locale == "en" else "en_US"}">')
    if alternates:
        for language, url in alternates.items():
            meta.append(f'<link rel="alternate" hreflang="{language}" href="{esc(url)}">')
        meta.append(f'<link rel="alternate" hreflang="x-default" href="{esc(alternates["en"])}">')
    if published:
        meta.append(f'<meta property="article:published_time" content="{published.isoformat()}">')
    if updated:
        meta.append(f'<meta property="article:modified_time" content="{updated.isoformat()}">')
    return "\n  ".join(meta)


def shell(title: str, description: str, canonical: str, prefix: str, main: str, page_type: str = "website", published: date | None = None, structured: str = "", bilingual_ui: bool = False, title_es: str | None = None, description_es: str | None = None, *, locale: str | None = None, alternates: dict[str, str] | None = None, image: str | None = None, updated: date | None = None) -> str:
    labels = [
        bilingual("About", "Sobre mí") if bilingual_ui else "About",
        bilingual("Experience", "Experiencia") if bilingual_ui else "Experience",
        bilingual("Projects", "Proyectos") if bilingual_ui else "Projects",
        bilingual("Writing", "Artículos") if bilingual_ui else "Writing",
        bilingual("Contact", "Contacto") if bilingual_ui else "Contact",
    ]
    language_switch = '''<li><div class="lang-selector"><button class="lang-btn active" data-lang-set="en" aria-label="Set language to English">EN</button><span class="lang-divider">|</span><button class="lang-btn" data-lang-set="es" aria-label="Establecer idioma en Español">ES</button></div></li>''' if bilingual_ui else ""
    if alternates:
        language_switch = f'''<li><div class="lang-selector"><a class="lang-route{' active' if locale == 'en' else ''}" data-lang-route="en" href="{esc(alternates['en'])}" hreflang="en" aria-label="Read in English"{' aria-current="page"' if locale == 'en' else ''}>EN</a><span class="lang-divider">|</span><a class="lang-route{' active' if locale == 'es' else ''}" data-lang-route="es" href="{esc(alternates['es'])}" hreflang="es" aria-label="Leer en español"{' aria-current="page"' if locale == 'es' else ''}>ES</a></div></li>'''
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
<html lang="{locale or 'en'}" data-theme="dark" data-lang="{locale or 'en'}"{' data-route-lang="' + locale + '"' if locale else ''}>
<head>
  {head(title, description, canonical, prefix, page_type, published, title_es, description_es, locale=locale, alternates=alternates, image=image, updated=updated)}
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
    if article.get("localized_routes"):
        en_url = f"{prefix}en/writing/{article['slug']}/"
        es_url = f"{prefix}es/writing/{article['slug_es']}/"
        heading = f'<span class="lang-en"><a href="{en_url}" hreflang="en">{esc(article["title"])}</a></span><span class="lang-es"><a href="{es_url}" hreflang="es">{esc(article["title_es"])}</a></span>'
        read_link = f'<a class="project-link lang-en" href="{en_url}" hreflang="en">Read article →</a><a class="project-link lang-es" href="{es_url}" hreflang="es">Leer artículo →</a>'
    else:
        heading = f'<a href="{url}">{bilingual(article["title"], article["title_es"])}</a>'
        read_link = f'<a class="project-link" href="{url}">{bilingual("Read article →", "Leer artículo →")}</a>'
    return f'''<article class="glass-card writing-card">
      <p class="writing-meta"><time datetime="{article['date'].isoformat()}">{article['date'].isoformat()}</time> · {bilingual(article['pillar'], PILLAR_ES[article['pillar']])}</p>
      <h2>{heading}</h2>
      <p>{bilingual(article['description'], article['description_es'])}</p>
      <div class="project-tags">{tags}</div>
      {read_link}
    </article>'''


def with_diagram(body: str, figure: str) -> str:
    if not figure:
        return body
    position = body.find("<h2>")
    if position < 0:
        first_paragraph_end = body.find("</p>")
        position = first_paragraph_end + len("</p>") if first_paragraph_end >= 0 else len(body)
    return body[:position].rstrip() + "\n" + figure + "\n" + body[position:].lstrip()


def render_inline_diagrams(body: str, entries: list[dict], lang: str, prefix: str, diagram_prefix: str) -> str:
    expected = set()
    for entry in entries:
        if not isinstance(entry, dict) or not SLUG.fullmatch(str(entry.get("id", ""))):
            raise ValueError(f"invalid {lang} diagram ID")
        diagram_id = entry["id"]
        if diagram_id in expected or not entry.get("alt") or not entry.get("caption"):
            raise ValueError(f"incomplete or duplicate {lang} diagram: {diagram_id}")
        expected.add(diagram_id)
        token = f"<p>{{{{diagram:{diagram_id}}}}}</p>"
        if body.count(token) != 1:
            raise ValueError(f"expected one {lang} diagram placeholder: {diagram_id}")
        filename = f"{diagram_prefix}-{diagram_id}-{lang}.svg"
        if not (ROOT / "assets" / "images" / "flows" / filename).exists():
            raise ValueError(f"missing diagram asset: {filename}")
        url = f"{prefix}assets/images/flows/{filename}"
        figure = f'''<figure class="writing-flow writing-flow-article">
          <a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{esc('Open diagram at full size' if lang == 'en' else 'Abrir diagrama a tamaño completo')}"><img src="{url}" alt="{esc(entry['alt'])}" width="480" height="800" loading="lazy"></a>
          <figcaption>{esc(entry['caption'])}</figcaption>
        </figure>'''
        body = body.replace(token, figure)
    if re.search(r"\{\{diagram:[^}]+\}\}", body):
        raise ValueError(f"unresolved {lang} diagram placeholder")
    return body


def localized_url(article: dict, lang: str) -> str:
    slug = article["slug"] if lang == "en" else article["slug_es"]
    return f"{SITE}/{lang}/writing/{slug}/"


def build_localized_article(article: dict) -> None:
    alternates = {lang: localized_url(article, lang) for lang in ("en", "es")}
    for lang in ("en", "es"):
        translated = lang == "es"
        title = article["title_es"] if translated else article["title"]
        description = article["description_es"] if translated else article["description"]
        subtitle = article["subtitle_es"] if translated else article["subtitle"]
        body = article["body_es"] if translated else article["body"]
        body = render_inline_diagrams(body, article[f"diagrams_{lang}"], lang, "../../../", article["diagram_prefix"])
        tags = "".join(f'<span class="project-tag">{esc(tag)}</span>' for tag in article["tags"][:6])
        modified = article.get("updated", article["date"])
        updated_label = f' · {"Actualizado" if translated else "Updated"} <time datetime="{modified.isoformat()}">{modified.isoformat()}</time>' if modified != article["date"] else ""
        main = f'''<article class="writing-article writing-longform">
          <p class="writing-back"><a href="../../../writing/">{"← Todos los artículos" if translated else "← All writing"}</a></p>
          <p class="writing-meta"><time datetime="{article['date'].isoformat()}">{article['date'].isoformat()}</time>{updated_label} · {esc(PILLAR_ES[article['pillar']] if translated else article['pillar'])}</p>
          <h1>{esc(title)}</h1>
          <p class="writing-deck">{esc(subtitle)}</p>
          <p class="writing-author">{esc(article.get('author', 'Reinaldo León'))} <span aria-hidden="true">·</span> Principal Platform Engineer | AI Platform &amp; Enablement</p>
          <div class="project-tags">{tags}</div>
          <div class="writing-prose" lang="{lang}">{body}</div>
        </article>'''
        url = alternates[lang]
        image = f"{SITE}/assets/images/writing/{article['slug']}-{lang}.png"
        schema = {
            "@context": "https://schema.org", "@type": "BlogPosting", "headline": title,
            "description": description, "datePublished": article["date"].isoformat(),
            "dateModified": modified.isoformat(), "inLanguage": lang,
            "author": {"@type": "Person", "name": article.get("author", "Reinaldo León"), "url": f"{SITE}/"},
            "mainEntityOfPage": url, "image": image,
        }
        structured = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c") + "</script>"
        slug = article["slug"] if lang == "en" else article["slug_es"]
        target = ROOT / lang / "writing" / slug
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(shell(f"{title} | Reinaldo León", description, url, "../../../", main, "article", article["date"], structured, bilingual_ui=True, locale=lang, alternates=alternates, image=image, updated=modified), encoding="utf-8")


def build() -> None:
    articles = [parse_article(path) for path in sorted(SOURCE.glob("*.md")) if not path.name.startswith("_")]
    slugs = [article["slug"] for article in articles]
    if len(slugs) != len(set(slugs)):
        raise ValueError("duplicate article slug")
    for article in articles:
        translation_path = SOURCE / "es" / f"{article['slug']}.md"
        if not translation_path.exists():
            raise ValueError(f"missing Spanish translation: {translation_path}")
        translated = parse_translation(translation_path)
        for key in ("title", "description", "body"):
            article[f"{key}_es"] = translated[key]
        if article.get("localized_routes"):
            if not SLUG.fullmatch(str(article.get("diagram_prefix", ""))):
                raise ValueError(f"{article['slug']}: localized article requires diagram_prefix")
            if not article.get("subtitle") or not translated.get("subtitle"):
                raise ValueError(f"{article['slug']}: localized article requires both subtitles")
            article["subtitle_es"] = translated["subtitle"]
            en_diagrams = article.get("diagrams")
            es_diagrams = translated.get("diagrams")
            if not isinstance(en_diagrams, list) or not isinstance(es_diagrams, list) or [d.get("id") for d in en_diagrams] != [d.get("id") for d in es_diagrams]:
                raise ValueError(f"{article['slug']}: bilingual diagrams must have matching IDs")
            article["diagrams_en"] = en_diagrams
            article["diagrams_es"] = es_diagrams
            for lang in ("en", "es"):
                render_inline_diagrams(article["body" if lang == "en" else "body_es"], article[f"diagrams_{lang}"], lang, "../../../", article["diagram_prefix"])
                social_image = ROOT / "assets" / "images" / "writing" / f"{article['slug']}-{lang}.png"
                if not social_image.exists():
                    raise ValueError(f"missing localized social image: {social_image}")
        if article.get("illustration_en") or article.get("illustration_es"):
            if article.get("diagram"):
                raise ValueError(f"{article['slug']}: use either a diagram or an illustration")
            for lang in ("en", "es"):
                filename = article.get(f"illustration_{lang}")
                if not isinstance(filename, str) or Path(filename).name != filename or Path(filename).suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".svg"}:
                    raise ValueError(f"{article['slug']}: invalid illustration_{lang}")
                illustration = ROOT / "assets" / "images" / "writing" / filename
                if not illustration.exists():
                    raise ValueError(f"missing article illustration: {illustration}")
            for key in ("illustration_alt", "illustration_caption"):
                if not article.get(key) or not translated.get(key):
                    raise ValueError(f"{article['slug']}: missing bilingual {key}")
                article[f"{key}_es"] = translated[key]
        if article.get("diagram"):
            if not SLUG.fullmatch(str(article["diagram"])):
                raise ValueError(f"{article['slug']}: invalid diagram name")
            for lang in ("en", "es"):
                diagram = ROOT / "assets" / "images" / "flows" / f"{article['diagram']}-{lang}.svg"
                if not diagram.exists():
                    raise ValueError(f"missing flow diagram: {diagram}")
            for key in ("diagram_alt", "diagram_caption"):
                if not article.get(key) or not translated.get(key):
                    raise ValueError(f"{article['slug']}: missing bilingual {key}")
                article[f"{key}_es"] = translated[key]
    articles = [article for article in articles if not article.get("draft", False)]
    articles.sort(key=lambda article: (article.get("featured", False), article["date"], article["slug"]), reverse=True)
    OUTPUT.mkdir(exist_ok=True)
    localized_manifest = OUTPUT / ".generated-localized-routes"
    previous_localized = set(localized_manifest.read_text(encoding="utf-8").splitlines()) if localized_manifest.exists() else set()
    current_localized = {
        f"{lang}/writing/{article['slug'] if lang == 'en' else article['slug_es']}"
        for article in articles if article.get("localized_routes") for lang in ("en", "es")
    }
    for route in previous_localized - current_localized:
        if not re.fullmatch(r"(?:en|es)/writing/[a-z0-9]+(?:-[a-z0-9]+)*", route):
            raise ValueError(f"invalid localized route in manifest: {route}")
        stale = ROOT / route / "index.html"
        if stale.exists():
            if set(stale.parent.iterdir()) != {stale}:
                raise ValueError(f"refusing to remove generated directory with extra files: {stale.parent}")
            stale.unlink()
            stale.parent.rmdir()
    manifest = OUTPUT / ".generated-slugs"
    previous = set(manifest.read_text(encoding="utf-8").splitlines()) if manifest.exists() else set()
    current = {article["slug"] for article in articles if not article.get("localized_routes")}
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
      <h1>{bilingual("Writing", "Artículos")}</h1>
      <p class="section-intro">{bilingual("Long-form notes on AI Platform Engineering, agentic systems, reliability, governance and the platform foundations behind them. Projects are evidence within these themes.", "Artículos sobre AI Platform Engineering, sistemas agénticos, fiabilidad, gobierno y los fundamentos de plataforma que los sostienen. Los proyectos aportan evidencia dentro de estos temas.")}</p>
      <p class="writing-follow">{bilingual("This site is the canonical home for articles in English and Spanish. LinkedIn is where shorter versions and conversations happen.", "Esta web es la fuente canónica de los artículos en español e inglés. LinkedIn acoge versiones breves y conversaciones.")}</p>
      <div class="writing-list">{cards}</div>
    </section>'''
    (OUTPUT / "index.html").write_text(shell("Writing | Reinaldo León", "Technical writing on AI Platform Engineering, AI Enablement, agentic systems, reliability and governance.", f"{SITE}/writing/", "../", index_main, bilingual_ui=True, title_es="Artículos | Reinaldo León", description_es="Artículos técnicos sobre AI Platform Engineering, AI Enablement, sistemas agénticos, fiabilidad y gobierno."), encoding="utf-8")

    for article in articles:
        if article.get("localized_routes"):
            build_localized_article(article)
            continue
        url = f"{SITE}/writing/{article['slug']}/"
        project = article.get("project")
        related = f'<p class="related-project">{bilingual("Related project:", "Proyecto relacionado:")} <a href="../../index.html#project-{project}">{esc(PROJECTS[project])}</a></p>' if project else ""
        linkedin = f'<p class="writing-linkedin"><a href="{esc(article["linkedin_url"])}" rel="noopener noreferrer" target="_blank">{bilingual("Discuss on LinkedIn ↗", "Conversar en LinkedIn ↗")}</a></p>' if article.get("linkedin_url") else ""
        tags = "".join(f'<span class="project-tag">{esc(tag)}</span>' for tag in article["tags"])
        diagrams = {"en": "", "es": ""}
        if article.get("diagram"):
            for lang in ("en", "es"):
                alt = article["diagram_alt"] if lang == "en" else article["diagram_alt_es"]
                caption = article["diagram_caption"] if lang == "en" else article["diagram_caption_es"]
                diagrams[lang] = f'''<figure class="writing-flow">
            <img src="../../assets/images/flows/{esc(article['diagram'])}-{lang}.svg" alt="{esc(alt)}" width="480" height="680" loading="lazy">
            <figcaption>{esc(caption)}</figcaption>
          </figure>'''
        elif article.get("illustration_en"):
            for lang in ("en", "es"):
                alt = article["illustration_alt"] if lang == "en" else article["illustration_alt_es"]
                caption = article["illustration_caption"] if lang == "en" else article["illustration_caption_es"]
                image_url = f"../../assets/images/writing/{esc(article[f'illustration_{lang}'])}"
                diagrams[lang] = f'''<figure class="writing-flow writing-illustration">
            <a href="{image_url}" target="_blank" rel="noopener noreferrer" aria-label="{esc('Open full-size illustration' if lang == 'en' else 'Abrir ilustración a tamaño completo')}"><img src="{image_url}" alt="{esc(alt)}" width="1254" height="1254" loading="lazy"></a>
            <figcaption>{esc(caption)}</figcaption>
          </figure>'''
        main = f'''<article class="writing-article">
          <p class="writing-back"><a href="../../writing/">{bilingual("← All writing", "← Todos los artículos")}</a></p>
          <p class="writing-meta"><time datetime="{article['date'].isoformat()}">{article['date'].isoformat()}</time> · {bilingual(article['pillar'], PILLAR_ES[article['pillar']])}</p>
          <h1>{bilingual(article['title'], article['title_es'])}</h1>
          <p class="writing-deck">{bilingual(article['description'], article['description_es'])}</p>
          <div class="project-tags">{tags}</div>
          <div class="writing-prose lang-en" lang="en">{with_diagram(article['body'], diagrams['en'])}</div>
          <div class="writing-prose lang-es" lang="es">{with_diagram(article['body_es'], diagrams['es'])}</div>
          {related}{linkedin}
        </article>'''
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": article["title"],
            "description": article["description"],
            "datePublished": article["date"].isoformat(),
            "inLanguage": ["en", "es"],
            "author": {"@type": "Person", "name": "Reinaldo León", "url": f"{SITE}/"},
            "mainEntityOfPage": url,
            "image": f"{SITE}/assets/images/social-card.png",
        }
        structured = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c") + "</script>"
        target = OUTPUT / article["slug"]
        target.mkdir(exist_ok=True)
        (target / "index.html").write_text(shell(f"{article['title']} | Reinaldo León", article["description"], url, "../../", main, "article", article["date"], structured, bilingual_ui=True, title_es=f"{article['title_es']} | Reinaldo León", description_es=article["description_es"]), encoding="utf-8")

    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    sitemap = ET.Element("{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
    for url in [f"{SITE}/", f"{SITE}/writing/"]:
        ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = url
    ET.register_namespace("xhtml", "http://www.w3.org/1999/xhtml")
    for article in articles:
        urls = [localized_url(article, lang) for lang in ("en", "es")] if article.get("localized_routes") else [f"{SITE}/writing/{article['slug']}/"]
        for url in urls:
            item = ET.SubElement(sitemap, "url")
            ET.SubElement(item, "loc").text = url
            if article.get("localized_routes"):
                ET.SubElement(item, "lastmod").text = article.get("updated", article["date"]).isoformat()
                for lang in ("en", "es"):
                    ET.SubElement(item, "{http://www.w3.org/1999/xhtml}link", {"rel": "alternate", "hreflang": lang, "href": localized_url(article, lang)})
    (ROOT / "sitemap.xml").write_bytes(ET.tostring(sitemap, encoding="utf-8", xml_declaration=True))

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for tag, value in (("title", "Reinaldo León — Writing"), ("link", f"{SITE}/writing/"), ("description", "Technical writing on AI Platform Engineering and reliable AI systems."), ("language", "en")):
        ET.SubElement(channel, tag).text = value
    for article in articles:
        item = ET.SubElement(channel, "item")
        link = localized_url(article, "en") if article.get("localized_routes") else f"{SITE}/writing/{article['slug']}/"
        for tag, value in (("title", article["title"]), ("link", link), ("guid", link), ("description", article["description"]), ("pubDate", article["date"].strftime("%a, %d %b %Y 00:00:00 GMT"))):
            ET.SubElement(item, tag).text = value
    (OUTPUT / "feed.xml").write_bytes(ET.tostring(rss, encoding="utf-8", xml_declaration=True))
    manifest.write_text("".join(f"{slug}\n" for slug in sorted(current)), encoding="utf-8")
    localized_manifest.write_text("".join(f"{route}\n" for route in sorted(current_localized)), encoding="utf-8")
    print(f"Built {len(articles)} article(s), Writing index, sitemap and RSS")


if __name__ == "__main__":
    build()
