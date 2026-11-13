# Yik Siu Chan's Personal Website

Source for <https://yiksiu-chan.github.io>, built with [Jekyll](https://jekyllrb.com/)
and the [al-folio](https://github.com/alshedivat/al-folio) theme (forked around v0.13).

You don't need to know Ruby. You edit Markdown/YAML/BibTeX files, preview locally
with one command, and push to `main`. GitHub builds and publishes the site.

---

## 1. Preview locally

Requirements: **Docker** and **make** (both already on the lab server). Nothing else:
Ruby and all gems run inside a container.

```bash
make serve     # preview at http://localhost:4000, rebuilds automatically when you save
```

Stop it with `Ctrl+C`. The first run takes a few minutes (downloads Ruby + gems), later runs take seconds.
If you're connected to the server through VS Code Remote, VS Code forwards port 4000 automatically
(check the "Ports" tab). Otherwise use `ssh -L 4000:localhost:4000 <server>`.

Other commands:

| Command | What it does |
|---|---|
| `make build` | Production build into `_site/`, exactly like GitHub does. |
| `make check` | `make build` + check for broken internal links and missing images. **Run before pushing.** |
| `make clean` | Delete build output/caches (fixes most "weird" stale-build issues). |
| `make update` | Upgrade gem versions (rewrites `Gemfile.lock`). Rarely needed. |
| `make shell` | Open a shell inside the build container (for debugging). |

Local and GitHub use the same Ruby version (`.ruby-version`) and the same gem
versions (`Gemfile.lock`), so if `make build` works locally, it works on GitHub.

---

## 2. What's in this repo

**Your content (what you normally edit):**

| Path | What it is |
|---|---|
| `_pages/` | One Markdown file per page. `about.md` = home page (bio), `publications.md`, `misc.md`, `hiking.md` (hidden from menu), `news.md`, `404.md`. |
| `_news/` | One small file per news item (shown on the home page and at `/news/`). |
| `_bibliography/papers.bib` | Your publications (BibTeX). The publications page is generated from it. |
| `_data/socials.yml` | Email, GitHub, LinkedIn, Google Scholar icons on the home page. |
| `_data/` (others) | `cv.yml` (CV data, empty), `coauthors.yml`/`venues.yml` (optional publication extras), `repositories.yml` (unused demo list). |
| `assets/img/` | Images: `profile_pic.jpeg` and hiking photos. Put new images here. |
| `assets/pdf/` | Put PDFs here (e.g. a CV PDF) if you add any. |
| `_config.yml` | Site-wide settings: name, URL, which features/sections are on. |
| `googled41bb1c82d4ce437.html` | Google Search Console verification. Leave it. |

**Theme and build machinery (normally don't touch):**

| Path | What it is |
|---|---|
| `_layouts/`, `_includes/`, `_sass/` | al-folio's HTML templates and styles. |
| `_plugins/` | Small Ruby plugins the theme uses. |
| `assets/css`, `assets/js`, `assets/fonts`, `assets/webfonts` | Theme styles, scripts, icon fonts. |
| `Gemfile`, `Gemfile.lock` | Ruby dependencies and their exact versions. |
| `.ruby-version` | Ruby version used locally and on GitHub (`3.3` = latest 3.3.x). |
| `.github/workflows/deploy.yml` | GitHub Actions: build + publish the site. |
| `purgecss.config.js` | Used by the deploy workflow to shrink CSS. |
| `Makefile`, `Dockerfile`, `.dockerignore` | Local preview/build setup. |
| `bin/check_site.py` | Broken-link checker used by `make check`. |
| `robots.txt`, `LICENSE` | Search-engine rules; the theme's MIT license. |
| `_site/`, `vendor/`, `.jekyll-cache/` | Generated locally, ignored by git. Safe to delete. |

---

## 3. Common updates

After any change: `make serve` to look at it, then commit and push (section 4).

### Edit the bio / about page
Edit `_pages/about.md`. Text below the second `---` is your bio (Markdown).
The block at the top (between the `---` lines) controls the photo and what is shown:

```yaml
profile:
  image: profile_pic.jpeg   # file in assets/img/
  image_circular: true
news: true                  # news list on the home page
selected_papers: true       # papers with selected={true} in papers.bib
social: true                # social icons
```

### Change the profile photo
Put the new image in `assets/img/` and either name it `profile_pic.jpeg` (replacing the old one)
or change `image:` in `_pages/about.md` to the new file name.

### Add a publication
Add an entry to the top of `_bibliography/papers.bib`, following the existing ones:

```bibtex
@article{chan2027example,
  title={Paper Title},
  author={Yik Siu Chan and Another Author},
  abbr={ICLR 2027},              % badge shown next to the paper
  year={2027},
  journal={International Conference on Learning Representations},
  selected={true},               % true = also shown on the home page
  arxiv={2701.12345},            % adds an arXiv button
  code={https://github.com/...}, % optional buttons: code, website, pdf, slides, poster, video
}
```

Your name is bolded automatically (set by `scholar: last_name/first_name` in `_config.yml`).
`*` after a name (e.g. `Yik Siu Chan*`) is shown as-is for equal contribution.
Use `{...}` around text with special characters; a broken `.bib` entry is a common build error.

### Add a news item
Create `_news/announcement_5.md` (any unique file name):

```markdown
---
layout: post
date: 2027-01-15 12:00:00-0500
inline: true
related_posts: false
---
Our paper [Title](https://arxiv.org/abs/...) was accepted to ICLR 2027!
```

The home page shows the latest 5 (`announcements: limit` in `_config.yml`).

### Add a blog post
The site currently has no blog. To start one:
1. Create `_posts/2027-01-15-my-first-post.md` (the filename must start with the date):
   ```markdown
   ---
   layout: post
   title: My first post
   date: 2027-01-15
   description: A short summary
   tags: research
   ---
   Post text in Markdown.
   ```
2. Create `_pages/blog.md` so it gets a page and a menu entry:
   ```markdown
   ---
   layout: page
   title: blog
   permalink: /blog/
   nav: true
   nav_order: 3
   pagination:
     enabled: true
     collection: posts
     per_page: 5
   ---
   {% for post in paginator.posts %}
   - [{{ post.title }}]({{ post.url | relative_url }}) ({{ post.date | date: "%b %Y" }})
   {% endfor %}
   ```
   (For al-folio's fancier blog list, copy `_pages/blog.md` from the
   [al-folio repo](https://github.com/alshedivat/al-folio/tree/main/_pages).)
3. Optionally set `blog_name` / `blog_description` in `_config.yml` (still "al-folio" defaults).

### Update the CV
Simplest: put your CV PDF at `assets/pdf/cv.pdf` and link it, e.g. in `about.md`:
`[CV](/assets/pdf/cv.pdf)`.
(A full CV page built from `_data/cv.yml` is possible; see al-folio's `_pages/cv.md` and `_data/cv.yml` examples upstream.)

### Show, hide, or reorder pages in the menu
In each page's top block in `_pages/`:
- `nav: true` / `nav: false`: show or hide in the top menu (the page still exists at its URL).
- `nav_order: 1`: position in the menu.
- To remove a page completely, delete its file.

### Enable or disable site features (`_config.yml`)
| Setting | Effect |
|---|---|
| `announcements: enabled` | News on the home page. |
| `latest_posts: enabled` | Latest blog posts on the home page. |
| `enable_darkmode` | Light/dark toggle. |
| `search_enabled` | Search box (Ctrl+K). |
| `enable_math` | LaTeX math via MathJax. |
| `max_author_limit` | How many authors to show before "and N more". |
| `enable_publication_badges` | Altmetric/Dimensions/Scholar badges on papers. |
| `google_analytics` + `enable_google_analytics` | Analytics. |

---

## 4. Deploy

```bash
make check                        # make sure it builds
git add -A && git commit -m "Describe the change"
git push origin main
```

What happens: the **Deploy site** GitHub Action (`.github/workflows/deploy.yml`) builds the site
and pushes the result to the `gh-pages` branch; GitHub Pages serves that branch.
The site updates 1 to 3 minutes after the action finishes.

- Pushing **any other branch** only *builds* (a free check). Nothing is published.
- One-time GitHub settings (already correct, just for reference): **Settings → Pages → Source:
  "Deploy from a branch", Branch: `gh-pages` / `(root)`**; **Settings → Actions → General →
  Workflow permissions: "Read and write"**.

**If a deploy fails:** open the repo on GitHub → **Actions** tab → the red run → click the failed
step to see the error. Reproduce with `make build` locally; it shows the same error.

---

## 5. Troubleshooting

| Symptom | Fix |
|---|---|
| Action fails at **Setup Ruby** with "Unavailable version" | GitHub updated its runners. `.ruby-version` should be a series like `3.3` (not `3.3.5`). If 3.3 itself is retired, change it to a newer series (e.g. `3.4`), run `make update`, `make check`, commit both files. |
| Action fails at **Setup Ruby** / bundle install with exit code 16 | `Gemfile` and `Gemfile.lock` don't match. Run `make install` (or `make build`) locally and commit the updated `Gemfile.lock`. |
| `YAML Exception` / `could not read file ... _config.yml` | Syntax error in a `---` front-matter block or `_config.yml`: check indentation (spaces, not tabs), and quote values containing `:`. The error names the file and line. |
| Publications page empty or build error mentioning BibTeX | A malformed entry in `papers.bib`: missing comma, unbalanced `{}`, duplicate key. |
| Image doesn't show | Check the path/case (`profile_pic.jpeg` ≠ `profile_pic.jpg`); run `make check`. |
| Change doesn't appear locally | Edits to `_config.yml` need a restart of `make serve`. Otherwise `make clean`, then `make serve`. |
| Change doesn't appear online | Check the Actions tab finished green; hard-refresh the browser (Ctrl+Shift+R). |
| `permission denied ... docker.sock` | Your user must be in the `docker` group (ask the server admin). |
| `port is already allocated` | A previous `make serve` is still running: `docker ps`, then `docker stop <id>`; or use `make serve PORT=4001`. |

For theme features not covered here, see al-folio's
[CUSTOMIZE.md](https://github.com/alshedivat/al-folio/blob/main/CUSTOMIZE.md) and
[FAQ.md](https://github.com/alshedivat/al-folio/blob/main/FAQ.md). Note the upstream theme has
moved on to v1.x, so some newer instructions may not apply to this copy.
