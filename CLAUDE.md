# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Website for the **First Workshop on Foundation Models for Structured Data (FMSD)** at ICML 2025, Vancouver. Built with Jekyll using the [al-folio](https://github.com/alshedivat/al-folio) academic theme. Deployed to GitHub Pages via GitHub Actions on push to `main`.

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

### Content pages (`_pages/`)
- `about.md` — Landing page (serves as `/`), contains workshop intro, schedule, and sponsors
- `cfp.md` — Call for papers, submission instructions, reviewer guidelines
- `accepted.md` — Accepted papers list, rendered from `_bibliography/papers.bib` via `{% bibliography %}`
- `speakers.md` and `profiles.md` — Use the `profiles` layout with per-person markdown files in `_pages/speakers/` and `_pages/organizers/`

### Key content files
- `_bibliography/papers.bib` — BibTeX entries for accepted papers, rendered by `jekyll-scholar`. Entries require `---\n---` YAML front matter delimiter at the top of the file.
- `_config.yml` — Central configuration: site metadata, Jekyll plugins, theme settings, third-party library versions. Many pages from the upstream al-folio template are excluded from the build (blog, teaching, publications, etc.).
- `_pages/speakers/*.md` and `_pages/organizers/*.md` — Individual bio content files referenced by the profiles layout.

### Excluded upstream al-folio pages
The `_config.yml` exclude list disables several al-folio default pages (`blog.md`, `projects.md`, `teaching.md`, `publications.md`, `about_einstein.md`) plus `_posts`, `_news`, and `_projects` collections. This workshop site only uses: About (`/`), Call for Papers, Accepted Papers, Speakers, and Organizers.

### Deployment
The `deploy.yml` GitHub Actions workflow builds with Ruby 3.3.5 + Python 3.13, runs `jekyll build`, purges unused CSS with `purgecss`, and deploys to GitHub Pages using `JamesIves/github-pages-deploy-action`. Triggered on push/PR to `main`/`master` for content file changes.

## Adding/Editing Content

### Adding a new accepted paper
Add a BibTeX `@inproceedings` entry to `_bibliography/papers.bib`. The entry will automatically appear on the Accepted Papers page.

### Adding a new speaker or organizer
1. Add a headshot image to `assets/img/speakers/` or `assets/img/organizers/`
2. Create a markdown bio file in `_pages/speakers/` or `_pages/organizers/`
3. Add a profile entry in `_pages/speakers.md` or `_pages/profiles.md` referencing the image and content file
