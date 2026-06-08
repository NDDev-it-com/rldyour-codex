---
name: visual-diff-review
description: "Surgical visual QA для Figma, screenshots и reference images. Используй для: pixel-perfect, сравни с Figma, сравни с фото, diff, deviation report. EN triggers: visual diff, pixel-perfect, compare with Figma, compare with reference image."
---

# Visual Diff Review

Use this workflow for pixel-perfect checks, Figma parity, screenshot comparisons, or photo/reference-image comparisons.

Required evidence:

- Reference source: Figma frame export, photo, screenshot, or accepted product reference.
- actual screenshot captured with Playwright CLI under `browser/`.
- Diff image or measured deviation report.
- Responsive viewport evidence when layout is responsive.
- Chrome DevTools MCP diagnosis for computed styles, layout, network, runtime, performance, or memory when deviations require debugging.

Use Webwright only for multi-page or reusable visual workflows.
