# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Website for the **Second Workshop on Foundation Models for Structured Data (FMSD)** at ICML 2026, Seoul. The first edition was held at ICML 2025 in Vancouver. Built with Jekyll using the [al-folio](https://github.com/alshedivat/al-folio) academic theme. Deployed to GitHub Pages via GitHub Actions on push to `main`. **Important:** GitHub Pages must be configured to deploy via "GitHub Actions" (not "Deploy from a branch"), because the site uses `jekyll-scholar` which is not supported by the default GitHub Pages Jekyll build.

## Build & Development Commands

### Local development with Docker (recommended)
```bash
docker compose up
```
Serves at `http://localhost:8080` with live reload. Auto-restarts Jekyll when `_config.yml` changes.

### Local development without Docker
```bash
bundle install
bundle exec jekyll serve --port=8080 --livereload
```
Requires Ruby, ImageMagick, and `nbconvert` (Python).

### Production build
```bash
JEKYLL_ENV=production bundle exec jekyll build
```
Output goes to `_site/`.

### Formatting
```bash
npx prettier --check .       # check formatting
npx prettier --write .       # fix formatting
```
Uses Prettier with `@shopify/prettier-plugin-liquid`. Config: `.prettierrc` (printWidth: 150). All submitted code must pass the Prettier check (enforced by CI).

### Pre-commit hooks
```bash
pre-commit install           # set up hooks
pre-commit run --all-files   # run manually
```
Checks: trailing whitespace, end-of-file fixer, YAML validation, large file detection.

## Architecture

### Multi-year structure

The site supports multiple workshop editions. The current year (2026) lives at the top level, while past editions are archived under `_pages/<year>/`.

- **Current edition (2026):** `_pages/about.md` (landing page at `/`), `_pages/cfp.md`, `_pages/accepted.md`, `_pages/speakers.md`, `_pages/profiles.md` (organizers)
- **Archived editions:** `_pages/2025/` contains the full ICML 2025 workshop site served under `/2025/`, using archive-specific layouts
- **Past Editions nav:** `_pages/past-editions.md` provides a dropdown menu linking to archived years

### Content pages (`_pages/`)
- `about.md` — Landing page (serves as `/`), contains workshop intro, schedule, and sponsors for 2026
- `cfp.md` — Call for papers, submission instructions, scope and topics
- `accepted.md` — Accepted papers list (currently TBA for 2026)
- `speakers.md` — Keynote speakers and industry spotlights, uses the `profiles` layout
- `profiles.md` — Organizers page, uses the `profiles` layout
- `past-editions.md` — Dropdown nav linking to archived workshop years (currently ICML 2025)

### Key content files
- `_bibliography/papers.bib` — BibTeX entries for current year's accepted papers, rendered by `jekyll-scholar`. Entries require `---\n---` YAML front matter delimiter at the top of the file.
- `_bibliography/papers-2025.bib` — Archived BibTeX entries from the ICML 2025 edition.
- `_config.yml` — Central configuration: site metadata, Jekyll plugins, theme settings, third-party library versions. Many pages from the upstream al-folio template are excluded from the build (blog, teaching, publications, etc.). `CLAUDE.md` is also excluded to prevent Liquid parsing errors.
- `_pages/speakers/*.md` and `_pages/organizers/*.md` — Individual bio content files for the current year. Files prefixed with `2025_` (e.g., `2025_andrew.md`) are stubs that include the corresponding 2025 archive bio.
- `_pages/2025/speakers/*.md` and `_pages/2025/organizers/*.md` — Archived bio content files for the 2025 edition.

### Layouts
- `profiles.liquid` — Standard profiles layout for current-year speaker and organizer pages.
- `archive-default.liquid`, `archive-page.liquid`, `archive-profiles.liquid` — Layouts for archived edition pages, with `archive-header.liquid` include for navigation banners.

### Excluded upstream al-folio pages
The `_config.yml` exclude list disables several al-folio default pages (`blog.md`, `projects.md`, `teaching.md`, `publications.md`, `about_einstein.md`) plus `_posts`, `_news`, and `_projects` collections. The active site pages are: About (`/`), Call for Papers, Accepted Papers, Speakers, Organizers, and Past Editions.

### Deployment
The `deploy.yml` GitHub Actions workflow builds with Ruby 3.3.5 + Python 3.13, runs `jekyll build`, purges unused CSS with `purgecss`, and deploys to GitHub Pages using `JamesIves/github-pages-deploy-action`. Triggered on push/PR to `main`/`master` for content file changes.

## Adding/Editing Content

### Adding a new accepted paper
Add a BibTeX `@inproceedings` entry to `_bibliography/papers.bib`. The entry will automatically appear on the Accepted Papers page.

### Adding a new speaker or organizer
1. Add a headshot image to `assets/img/speakers/` or `assets/img/organizers/` (use `placeholder.svg` if no photo is available yet)
2. Create a markdown bio file in `_pages/speakers/` or `_pages/organizers/`
3. Add a profile entry in `_pages/speakers.md` or `_pages/profiles.md` referencing the image and content file

### Archiving a year
When a new edition begins, the previous year's content is moved to `_pages/<year>/` with archive layouts. Speaker/organizer bios in the current `_pages/speakers/` and `_pages/organizers/` directories get `<year>_` prefixed stub files that include the archived content. The bibliography is renamed to `papers-<year>.bib`. A new entry is added to `_pages/past-editions.md`.
