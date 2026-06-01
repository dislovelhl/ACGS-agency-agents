---
id: impeccable
name: Impeccable
description: Frontend design skill and CLI for AI harnesses, with design vocabulary, visual design commands, deterministic anti-pattern detection, and guidance for typography, color, motion, spatial design, interaction, responsive design, and UX writing.
source_url: https://github.com/pbakaus/impeccable
install: npx impeccable skills install
commands:
  - npx impeccable skills install
  - npx impeccable detect src/
  - npx impeccable detect --fast --json .
  - /impeccable audit
  - /impeccable polish
  - /impeccable critique
python_api: []
capabilities:
  - design-audit
  - frontend-design
  - ui-polish
  - visual-critique
  - anti-pattern-detection
  - ux-writing
  - responsive-design
formats:
  - html
  - css
  - javascript
  - typescript
  - url
  - screenshot
keywords:
  - design
  - frontend
  - ui
  - ux
  - audit
  - polish
  - critique
  - anti-pattern
  - anti-patterns
  - visual
  - hierarchy
  - typography
  - color
  - motion
  - responsive
  - layout
  - impeccable
security_notes:
  - Review any installer or downloaded skill bundle before running it in sensitive repositories.
  - URL scanning uses browser automation; treat remote pages as untrusted and avoid authenticated or private sessions unless explicitly required.
  - Do not let design automation override product, accessibility, privacy, or brand constraints without human review.
use_when:
  - An agent needs frontend design critique, anti-pattern detection, or final visual polish.
  - An agent needs shared `/impeccable` commands such as audit, polish, critique, harden, animate, colorize, typeset, layout, or adapt.
  - An agent needs deterministic detection of common AI-generated frontend design smells.
avoid_when:
  - The task is backend-only, data-only, or has no user interface.
  - The environment cannot run Node/npx or browser-based URL scanning safely.
---

# Impeccable

Use Impeccable when an agent needs a design skill, visual quality vocabulary, or CLI anti-pattern detection for frontend work.
