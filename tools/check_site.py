"""Check generated static pages, metadata and local navigation."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "index.html", *sorted((ROOT / "writing").glob("**/index.html"))]
SITE = "https://reinaldoleon.github.io/bio/"


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[str] = []
        self.h1 = 0
        self.meta: dict[str, str] = {}
        self.prose_languages: set[str] = set()
        self.title_locales: set[str] = set()
        self.language_buttons: set[str] = set()
        self.images_without_alt = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        if "writing-prose" in classes:
            self.prose_languages.update(classes & {"lang-en", "lang-es"})
        if tag == "title":
            self.title_locales.update(key for key in ("data-title-en", "data-title-es") if values.get(key))
        if tag == "button" and values.get("data-lang-set"):
            self.language_buttons.add(values["data-lang-set"])
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "h1":
            self.h1 += 1
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"])
        if tag in {"img", "script"} and values.get("src"):
            self.links.append(values["src"])
        if tag == "img" and values.get("alt") is None:
            self.images_without_alt += 1
        if tag == "meta":
            name = values.get("name") or values.get("property")
            if name:
                self.meta[name] = values.get("content", "")
        if tag == "link" and values.get("rel") == "canonical":
            self.meta["canonical"] = values.get("href", "")


def resolve_local(page: Path, url: str) -> tuple[Path, str] | None:
    parts = urlsplit(url)
    if parts.scheme or parts.netloc:
        return None
    target = (page.parent / unquote(parts.path)).resolve() if parts.path else page
    if target.is_dir():
        target /= "index.html"
    return target, parts.fragment


def check() -> None:
    parsed: dict[Path, Page] = {}
    errors: list[str] = []
    for path in PAGES:
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        parsed[path.resolve()] = page
        dupes = [value for value, count in Counter(page.ids).items() if count > 1]
        if dupes:
            errors.append(f"{path}: duplicate ids {dupes}")
        if page.h1 != 1:
            errors.append(f"{path}: expected one h1, found {page.h1}")
        if page.images_without_alt:
            errors.append(f"{path}: {page.images_without_alt} image(s) lack alt text")
        for key in ("description", "og:title", "og:description", "og:image", "canonical"):
            if not page.meta.get(key):
                errors.append(f"{path}: missing {key}")
        relative = path.relative_to(ROOT)
        expected = SITE if relative == Path("index.html") else SITE + str(relative.parent).replace("\\", "/") + "/"
        if page.meta.get("canonical") != expected:
            errors.append(f"{path}: canonical mismatch: {page.meta.get('canonical')}")
        if len(relative.parts) > 2 and relative.parts[0] == "writing":
            if page.prose_languages != {"lang-en", "lang-es"}:
                errors.append(f"{path}: missing bilingual article body")
            if page.title_locales != {"data-title-en", "data-title-es"}:
                errors.append(f"{path}: missing localized browser title")
            if page.language_buttons != {"en", "es"}:
                errors.append(f"{path}: missing language controls")
        image = page.meta.get("og:image", "")
        if image.startswith(SITE) and not (ROOT / image.removeprefix(SITE)).exists():
            errors.append(f"{path}: missing social image {image}")
    for path, page in parsed.items():
        for url in page.links:
            local = resolve_local(path, url)
            if local is None:
                continue
            target, fragment = local
            if not target.exists():
                errors.append(f"{path}: broken link {url}")
            elif fragment:
                if target.suffix != ".html":
                    errors.append(f"{path}: fragment on non-HTML file {url}")
                else:
                    other = parsed.get(target.resolve())
                    if other is None:
                        other = Page()
                        other.feed(target.read_text(encoding="utf-8"))
                    if fragment not in other.ids:
                        errors.append(f"{path}: missing fragment {url}")
    try:
        ET.parse(ROOT / "sitemap.xml")
        ET.parse(ROOT / "writing" / "feed.xml")
        for diagram in (ROOT / "assets" / "images" / "flows").glob("*.svg"):
            ET.parse(diagram)
    except ET.ParseError as exc:
        errors.append(f"invalid XML: {exc}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(PAGES)} pages: metadata, headings, IDs and local links OK")


if __name__ == "__main__":
    check()
