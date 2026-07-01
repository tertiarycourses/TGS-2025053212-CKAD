---
name: tertiary-course-slides
description: Generate a highly professional, all-white-theme WSQ course slide deck (python-pptx) for Tertiary Infotech Academy. Produces a cover page with course title + n8n & Tertiary logos + UEN, admin slides (digital attendance/TRAQOM, About the Trainer, Ground Rules, Lesson Plan, Learning Outcomes, Assessment), n8n key-concept slides, per-activity overview + workflow screenshot + step-by-step slides, and lunch/tea-break dividers. Use when creating or updating course/training slides for a Tertiary Infotech WSQ course.
---

# WSQ Course Slides

Generate a professional 3-day course deck with `python-pptx`. Template: `make_slides.py`.

## How to use
1. Edit `make_slides.py`: set `REPO` and the activity/concept content.
2. Run `python3 make_slides.py` → writes `courseware/n8n-slides.pptx` (150–200 slides for a 3-day course).
3. Embed real n8n **workflow screenshots** (see the `verify`/Playwright flow) or rendered diagrams from `labs/<activity>/*.png`.

## Design rules (must follow)
- **White theme only — NO dark/black slide backgrounds.** Use white slides with blue/teal accents.
- **16:9** (13.333 × 7.5 in). **Font: Arial** for every run.
- **Cover slide**: course title, the **n8n course logo** (top-right) and **Tertiary Infotech Academy logo** (top-left), `WSQ Course Code: TGS-XXXX`, `Conducted by Tertiary Infotech Academy Pte Ltd`, `UEN 201200696W`.
- **Section dividers**: white background, big faint number, blue kicker + ink title (never a full dark fill).
- **Admin front matter**: Digital Attendance (Mandatory / TRAQOM — SSG QR), About the Trainer, Let's Know Each Other, Ground Rules, LMS/TMS, Lesson Plan, Learning Outcomes, Assessment (Written SAQ 1h + Practical PP 1h, open book), Briefing for Assessment.
- **n8n key concepts**: What is n8n, nodes, triggers & actions, execution modes, data/JSON/expressions, pin data, code/edit-fields, IF/Switch, split out, merge, sub-workflows; AI agents (LLM/memory/tools/system prompt); RAG (embeddings/vector store); API & HTTP request; webhooks & auth; security/guardrails.
- **Per activity**: an overview slide (tag + description + "You'll build" + key nodes), a **workflow screenshot** slide, then **one step per slide** (big numbered badge), then a green "Test it" slide.
- **Breaks**: white slides reading "Lunch Break / 1 hour" and "Tea Break / 15 minutes".
- **Footer on every content slide**: course title · TGS code (left), `© 2026 Tertiary Infotech Academy Pte Ltd` (center), slide number (right).

## House format — Tertiary Infotech Academy Pte Ltd (WSQ)

Every generated document/deck MUST include:

- **Cover page** with: the **Course Title**; the **n8n course logo** and the **Tertiary Infotech Academy Pte Ltd logo**; `WSQ Course Code: TGS-XXXX`; `Conducted by Tertiary Infotech Academy Pte Ltd`; `UEN: 201200696W`; and a **Version** number. (Logos live in `courseware/assets/`: `tertiary-infotech-logo.png`, `n8n-course-logo.png`.)
- **Document Version Control Record** table — columns: Version Number | Effective Date of Release | Summary of Included Changes | Author.
- **Table of Contents** — a Word TOC field that auto-updates (headings use the built-in Heading 1/2 styles; `updateFields` is enabled so Word refreshes it on open).
- **Footer on every page** — the copyright line `© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.` and **Page X of Y** numbering. The footer URL is **www.tertiarycourses.com.sg**.
- **Font: Arial**, **11 pt** body; headings in Arial bold.
- **Brand colours**: blue `#1F6FEB`, teal `#10B981`, ink `#161B26`, grey `#5B6372`.

The reusable helper `prodoc.py` implements the cover page, version-control table, TOC field, page numbering and copyright footer — import it and call `add_cover_page`, `add_version_control`, `add_toc`, `add_page_numbers`, `enable_update_fields`, `style_headings`.
