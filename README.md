# 10-Is-Mana.github.io

This repository is a plain static GitHub Pages site.

## Structure

- `index.html` - homepage
- `cv/index.html` - CV page
- `static/` - CSS, JavaScript, PDF, images, favicon

## Maintenance

Edit the deployed files directly:

```bash
open index.html
open cv/index.html
```

GitHub Pages serves this repository as static files. No Python app, build step, or template rendering is required.

## Publishing

Commit and push changes to the default branch. GitHub Pages will publish the updated static files.

## Notes

- Root-relative links like `/cv` and `/static/...` work because this repository is the user site `10-Is-Mana.github.io`.
- If you later add a blog, use either hand-written static HTML pages or introduce a small static site generator only when the repetition becomes worth automating.
