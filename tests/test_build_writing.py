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
            output = root / "writing"
            article = source / "example-article.md"
            article.write_text(ARTICLE)
            with patch.object(build_writing, "ROOT", root), patch.object(build_writing, "SOURCE", source), patch.object(build_writing, "OUTPUT", output):
                build_writing.build()
                self.assertTrue((output / "example-article" / "index.html").exists())
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


if __name__ == "__main__":
    unittest.main()
