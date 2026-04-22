# Markdown Posts

Put your blog source files in this directory.

Supported file extension: `*.md`

Recommended front matter:

```md
---
title: My New Post
date: 2026-04-22
category: 技术笔记
summary: One-sentence summary shown on index page.
tags:
  - markdown
  - notes
slug: my-new-post
---

# My New Post

Write your content here.
```

Notes:
- `title` is used for article title and index link.
- `date` format should be `YYYY-MM-DD`.
- `slug` controls generated file name under `blog/`.
- If front matter is omitted, the builder will infer values from file name and content.
