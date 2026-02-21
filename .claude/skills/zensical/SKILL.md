---
name: zensical
description: Use when the task involves the project docs — adding or editing pages, configuring mkdocs.yml, changing the theme, or building/serving the docs site with Zensical.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Zensical Skill

Zensical is the static site generator used for this project's docs. It is a drop-in replacement for MkDocs + Material for MkDocs, made by the same team. It reads `mkdocs.yml` natively.

## Commands

```bash
uv run zensical serve   # live preview at http://localhost:8000
uv run zensical build   # build static site to site/
```

## Project layout

```
mkdocs.yml          # site config (theme, nav, etc.)
docs/
  index.md          # Home — installation, usage, Docker, configuration
  architecture.md   # The four composable layers
  dsmr.md           # DSMR protocol, gas sub-meter, output/storage fields
  extending.md      # How to add readers, processors, storage backends
site/               # build output (gitignored)
```

## mkdocs.yml

Current config uses the Material theme with a light/dark palette toggle:

```yaml
theme:
  name: material
  palette:
    - scheme: default      # light
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate        # dark
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
```

`name: material` is the correct theme name for Zensical (same as mkdocs-material).

## Adding a page

1. Create `docs/<page>.md`
2. Add it to `nav:` in `mkdocs.yml`
3. Run `uv run zensical build` to verify

## Notes

- `mkdocs serve` does **not** work — the CLI is `zensical`, not `mkdocs`
- `site/` is the build output directory; it is gitignored
- Zensical replaced `mkdocs-material` as the dev dependency (`pyproject.toml`)
