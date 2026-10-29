import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from tools import build_writing


ARTICLE = """---
title: Example article
slug: example-article
date: 2026-10-29
description: A test article.
tags:
  - AI Reliability
pillar: AI Reliability & Evaluation
draft: false
featured: true
---

## Evidence

The article body.
"""

SPANISH = """---
title: Artículo de ejemplo
description: Un artículo de prueba.
---

## Evidencia

El cuerpo del artículo.
"""


class WritingBuildTests(unittest.TestCase):
    def test_frontmatter_and_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "example-article.md"
            source.write_text(ARTICLE)
            article = build_writing.parse_article(source)
            self.assertEqual(article["date"], date(2026, 10, 29))
            self.assertIn("<h2>Evidence</h2>", article["body"])

    def test_drafts_omitted_and_removed_from_generated_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "content" / "writing"
            source.mkdir(parents=True)
            spanish = source / "es"
            spanish.mkdir()
            output = root / "writing"
            article = source / "example-article.md"
            article.write_text(ARTICLE)
            (spanish / "example-article.md").write_text(SPANISH)
            with patch.object(build_writing, "ROOT", root), patch.object(build_writing, "SOURCE", source), patch.object(build_writing, "OUTPUT", output):
                build_writing.build()
                self.assertTrue((output / "example-article" / "index.html").exists())
                rendered = (output / "example-article" / "index.html").read_text()
                self.assertIn("Artículo de ejemplo", rendered)
                self.assertIn("El cuerpo del artículo", rendered)
                self.assertIn('data-lang-set="es"', rendered)
                self.assertIn("example-article", (root / "sitemap.xml").read_text())
                article.write_text(ARTICLE.replace("draft: false", "draft: true"))
                build_writing.build()
                self.assertFalse((output / "example-article").exists())
                self.assertNotIn("example-article", (root / "sitemap.xml").read_text())
                self.assertNotIn("example-article", (output / "feed.xml").read_text())

    def test_rejects_slug_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "wrong-name.md"
            source.write_text(ARTICLE)
            with self.assertRaisesRegex(ValueError, "slug must match"):
                build_writing.parse_article(source)

    def test_raw_html_is_escaped(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "example-article.md"
            source.write_text(ARTICLE + "\n<script>alert(1)</script>\n")
            article = build_writing.parse_article(source)
            self.assertNotIn("<script>", article["body"])

    def test_missing_translation_blocks_build(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "content" / "writing"
            source.mkdir(parents=True)
            (source / "example-article.md").write_text(ARTICLE)
            with patch.object(build_writing, "ROOT", root), patch.object(build_writing, "SOURCE", source), patch.object(build_writing, "OUTPUT", root / "writing"):
                with self.assertRaisesRegex(ValueError, "missing Spanish translation"):
                    build_writing.build()

    def test_diagram_sits_after_introduction(self):
        body = "<p>Introduction.</p>\n<h2>First section</h2>\n<p>Detail.</p>"
        result = build_writing.with_diagram(body, "<figure>Flow</figure>")
        self.assertLess(result.index("Introduction."), result.index("<figure>"))
        self.assertLess(result.index("<figure>"), result.index("<h2>"))

    def test_bilingual_illustration_is_rendered(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "content" / "writing"
            spanish = source / "es"
            spanish.mkdir(parents=True)
            images = root / "assets" / "images" / "writing"
            images.mkdir(parents=True)
            (images / "review-en.jpg").write_bytes(b"image")
            (images / "review-es.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            extra = "illustration_en: review-en.jpg\nillustration_es: review-es.svg\nillustration_alt: English visual\nillustration_caption: English caption\n"
            (source / "example-article.md").write_text(ARTICLE.replace("draft: false", extra + "draft: false"))
            (spanish / "example-article.md").write_text(SPANISH.replace("---\n\n## Evidencia", "illustration_alt: Imagen española\nillustration_caption: Leyenda española\n---\n\n## Evidencia"))
            output = root / "writing"
            with patch.object(build_writing, "ROOT", root), patch.object(build_writing, "SOURCE", source), patch.object(build_writing, "OUTPUT", output):
                build_writing.build()
            rendered = (output / "example-article" / "index.html").read_text()
            self.assertIn("review-en.jpg", rendered)
            self.assertIn("review-es.svg", rendered)
            self.assertIn("Imagen española", rendered)

    def test_localized_routes_have_reciprocal_metadata_and_diagrams(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "content" / "writing"
            spanish = source / "es"
            spanish.mkdir(parents=True)
            flows = root / "assets" / "images" / "flows"
            flows.mkdir(parents=True)
            images = root / "assets" / "images" / "writing"
            images.mkdir(parents=True)
            for lang in ("en", "es"):
                (flows / f"example-article-flow-{lang}.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
                (images / f"example-article-{lang}.png").write_bytes(b"image")
            english_extra = "slug_es: articulo-ejemplo\nlocalized_routes: true\ndiagram_prefix: example-article\nsubtitle: A useful subtitle.\ndiagrams:\n  - id: flow\n    alt: English diagram\n    caption: English caption\n"
            spanish_extra = "subtitle: Un subtítulo útil.\ndiagrams:\n  - id: flow\n    alt: Diagrama español\n    caption: Leyenda española\n"
            (source / "example-article.md").write_text(ARTICLE.replace("draft: false", english_extra + "draft: false").replace("The article body.", "The article body.\n\n{{diagram:flow}}"))
            (spanish / "example-article.md").write_text(SPANISH.replace("---\n\n## Evidencia", spanish_extra + "---\n\n## Evidencia").replace("El cuerpo del artículo.", "El cuerpo del artículo.\n\n{{diagram:flow}}"))
            with patch.object(build_writing, "ROOT", root), patch.object(build_writing, "SOURCE", source), patch.object(build_writing, "OUTPUT", root / "writing"):
                build_writing.build()
            en = (root / "en" / "writing" / "example-article" / "index.html").read_text()
            es = (root / "es" / "writing" / "articulo-ejemplo" / "index.html").read_text()
            self.assertIn('lang="en" data-theme', en)
            self.assertIn('lang="es" data-theme', es)
            self.assertIn('hreflang="es" href="https://reinaldoleon.github.io/bio/es/writing/articulo-ejemplo/"', en)
            self.assertIn('hreflang="en" href="https://reinaldoleon.github.io/bio/en/writing/example-article/"', es)
            self.assertIn("Diagrama español", es)
            self.assertNotIn("English diagram", es)
            self.assertIn("example-article-flow-en.svg", en)
            self.assertIn("example-article-flow-es.svg", es)
            self.assertIn("/es/writing/articulo-ejemplo/", (root / "sitemap.xml").read_text())
            self.assertIn("/en/writing/example-article/", (root / "writing" / "feed.xml").read_text())
            (source / "example-article.md").write_text((source / "example-article.md").read_text().replace("draft: false", "draft: true"))
            with patch.object(build_writing, "ROOT", root), patch.object(build_writing, "SOURCE", source), patch.object(build_writing, "OUTPUT", root / "writing"):
                build_writing.build()
            self.assertFalse((root / "en" / "writing" / "example-article" / "index.html").exists())
            self.assertFalse((root / "es" / "writing" / "articulo-ejemplo" / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
