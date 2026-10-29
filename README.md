# Reinaldo León — professional bio

Static GitHub Pages site. The homepage is hand-authored in `index.html`; styling and interactions live in `assets/css/style.css` and `assets/js/main.js`. The `.nojekyll` file means GitHub Pages serves committed files directly.

## Writing

Long-form articles live in `content/writing/*.md` with YAML frontmatter. `tools/build_writing.py` generates the public `writing/` pages, `writing/feed.xml` and `sitemap.xml`. Generated files are committed alongside their Markdown sources. No client-side Markdown rendering is needed, so articles remain indexable without JavaScript.

Run:

```sh
uv sync
uv run python tools/build_writing.py
```

Then preview the repository root with a static server, for example `python3 -m http.server 8000`, and open `http://localhost:8000/`.

Copy `content/writing/_template.md` to a filename matching its `slug`. Required frontmatter: `title`, `slug`, `date` (YYYY-MM-DD), `description`, `tags` (list) and `pillar`. Optional: `description_es`, `project`, `draft`, `featured`, `linkedin_text`, `linkedin_url`, `linkedin_published_at`. `description_es` localizes the Writing index summary; article bodies are currently English. Drafts are omitted from the generated index, feed and sitemap. `project` accepts `growthmesh`, `causio`, `ecos-inmersivos` or `ai-conversacional-lab` and links to the related homepage card. Add a new project to `PROJECTS` in the build script when it is added to the homepage.

Pillars:

- AI Platform Engineering
- Agentic Systems
- AI Reliability & Evaluation
- AI Governance
- AI Enablement
- Platform Engineering / SRE / FinOps

The bio is the canonical home for long-form articles. `linkedin_text` can hold a short distribution version, and `linkedin_url` can be added after publication. A short LinkedIn-only post does not require a website article.

## Review before publishing

Run the builder, check `git diff --check`, review the generated HTML and verify public claims and Cobee confidentiality. Pushing the `gh-pages` branch publishes the committed static files; this repository does not run an automatic build.
