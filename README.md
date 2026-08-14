# Samata Beer — Website

Static marketing site for **Samata Beer**, a nano brewery in Bangkok, Thailand
brewing award-winning Thai fruited sours.

Built as a 1:1 port of the `Samata Beer website design` prototype into plain,
dependency-free HTML + CSS.

## Structure

```
index.html      Whole site (single page, anchor-nav sections)
styles.css      All styling — design tokens, layout, responsive rules
assets/         Logo files
uploads/        Product, award, taproom and collaboration photography
.nojekyll       Tells GitHub Pages to serve files as-is
```

`Samata Beer website design/` is the original design source, kept for reference.

## Sections

Hero → marquee → The Beers (core, limited & seasonal, collaborations) → Awards →
Brand story → World stage banner → Taproom → Stockists → Contact footer.

## Design tokens

| Token | Value | Use |
| --- | --- | --- |
| `--ink` | `#141414` | Text, borders, hard shadows |
| `--paper` | `#FAF8F1` | Page background |
| `--lime` | `#CCD936` | Hero background, accents |
| `--pink` | `#F5BFCD` | Taproom, founder card |
| `--slate` | `#35424E` | Awards section |
| `--gold` | `#F2C230` | Award years, eyebrow |

Type: **Anton** (display), **Space Grotesk** (body), **IBM Plex Sans Thai** (Thai).

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Deployment

Published with GitHub Pages from the `main` branch root.

## Notes

- `assets/logo-mark.png` is a transparent-background version of `logo.png`,
  generated because the original ships an opaque white background that rendered
  as a black box on the dark footer.
- Taproom address and hours are still placeholders in the design source and
  remain so here.
