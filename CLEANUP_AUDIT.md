# Cleanup audit (2026-11-13)

Audit of every top-level file/folder, made before cleanup on branch `site-revival`.
A backup of the original state is on branch `backup-before-cleanup` (local) and
in `main`. This file can be deleted once you're happy with the cleanup.

Legend: **keep (needed)** = the site/build needs it · **keep (my content)** = your
content · **remove** = unused or redundant (deleted) · **unsure** = kept, your call.

## Your content (untouched)

| Path | Verdict | Reason |
|---|---|---|
| `_pages/` | keep (my content) | Your pages: about (home), publications, misc, hiking, news, 404. |
| `_news/` | keep (my content) | Your news items. |
| `_bibliography/papers.bib` | keep (my content) | Your publications. |
| `_data/socials.yml` | keep (my content) | Your email / GitHub / LinkedIn / Scholar links. |
| `_data/cv.yml`, `coauthors.yml`, `venues.yml` | keep (my content) | Empty, but the publications layout reads `coauthors`/`venues`. |
| `_data/repositories.yml` | **unsure** (kept) | Still the al-folio demo list (torvalds, alshedivat, ...). No page uses it today (there's no "repositories" page), so it's harmless. Edit or delete it if you want. |
| `assets/img/` | keep (my content) | Profile photo + hiking photos (all yours, no demo images). |
| `_config.yml` | keep (my content) | Your settings. Only boilerplate lines were changed (see below). |
| `googled41bb1c82d4ce437.html` | keep (my content) | Google Search Console ownership verification for your site. |
| `README.md` | keep (rewritten) | Now your owner's guide. |

## Theme and build (needed)

| Path | Verdict | Reason |
|---|---|---|
| `_layouts/`, `_includes/`, `_sass/`, `_plugins/` | keep (needed) | al-folio theme internals: page templates, styles, small Ruby plugins. Not modified. |
| `assets/css/`, `assets/js/`, `assets/fonts/`, `assets/webfonts/` | keep (needed) | Theme stylesheets, scripts, icon fonts. |
| `Gemfile`, `Gemfile.lock` | keep (needed) | Ruby gem list and the exact pinned versions (lockfile now committed). |
| `.ruby-version` | keep (needed) | Ruby version (3.3) used by both GitHub Actions and local Docker. |
| `.github/workflows/deploy.yml` | keep (needed) | Builds the site and publishes it to the `gh-pages` branch. |
| `purgecss.config.js` | keep (needed) | Used by the deploy workflow to strip unused CSS. |
| `robots.txt` | keep (needed) | Search engine instructions + sitemap link. |
| `Makefile`, `Dockerfile`, `.dockerignore`, `bin/check_site.py` | keep (needed) | Local preview/build tooling (new or rewritten). |
| `LICENSE` | keep (needed) | al-folio's MIT license, which requires keeping its copyright notice. |
| `.gitignore` | keep (needed) | Keeps build output (`_site`, `vendor`, caches) out of git. |

## Removed

| Path | Verdict | Reason |
|---|---|---|
| `CONTRIBUTING.md`, `CUSTOMIZE.md`, `FAQ.md`, `INSTALL.md` | remove | Upstream al-folio docs for theme contributors; replaced by README.md (which links to upstream docs). |
| `.all-contributorsrc`, `.git-blame-ignore-revs` | remove | Upstream repo-maintenance metadata. |
| `.github/ISSUE_TEMPLATE/`, `.github/release.yml`, `.github/stale.yml` | remove | Upstream issue/release/stale-bot config. |
| `.github/workflows/prettier*.yml` (3) | remove | Upstream code-style check; was failing on every push. |
| `.github/workflows/broken-links*.yml` (2), `.lycheeignore` | remove | Link-check workflows that failed on every push (emails). Replaced by local `make check`. |
| `.github/workflows/axe.yml`, `lighthouse-badger.yml` | remove | Accessibility/performance reports for the upstream demo site. |
| `.github/workflows/deploy-image.yml`, `deploy-docker-tag.yml`, `docker-slim.yml` | remove | Publish al-folio's Docker image to Docker Hub (needs upstream secrets). |
| `.github/workflows/schedule-posts.txt` | remove | Disabled example workflow for scheduled blog posts. |
| `docker-compose.yml`, `docker-compose-slim.yml`, `bin/entry_point.sh` | remove | Old Docker setup using a prebuilt v0.13 image / `ruby:latest` (doesn't match CI). Replaced by `Makefile` + `Dockerfile`. |
| `.devcontainer/` | remove | VS Code dev-container using a different Ruby/Jekyll image than CI. Replaced by `make`. |
| `bin/cibuild`, `bin/deploy` | remove | Legacy manual build/deploy scripts; deployment is done by GitHub Actions. |
| `package.json`, `package-lock.json`, `.prettierrc`, `.prettierignore`, `.pre-commit-config.yaml` | remove | Prettier code-formatter tooling for theme contributors; not needed to build. |
| `lighthouse_results/` | remove | Lighthouse scores of the upstream demo site. |
| `readme_preview/` | remove | Screenshots for upstream's README. |
| `requirements.txt`, `assets/jupyter/` | remove | Jupyter/nbconvert for a demo notebook; it broke local builds (needs Python). |
| `assets/audio/`, `assets/video/`, `assets/pdf/example_pdf.pdf`, `assets/plotly/`, `assets/html/`, `assets/bibliography/`, `assets/json/` | remove | Demo media/data for the theme's sample blog posts (sample posts were already deleted). `assets/json/resume.json` was Albert Einstein's demo CV. Verified unreferenced by your pages. |

## Boilerplate edits in `_config.yml`

- Removed `jekyll-jupyter-notebook` from `plugins`.
- `jekyll_get_json` no longer loads the Einstein demo `resume.json`.
- `exclude:` list updated for the removed files, and now also excludes `Makefile`,
  `Dockerfile` and `CLEANUP_AUDIT.md` so they aren't published.
