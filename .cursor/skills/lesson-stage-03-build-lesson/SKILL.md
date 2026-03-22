---
name: lesson-stage-03-build-lesson
description: Implement lesson files from the solved model contract, including multilingual text, LaTeX formulas, teacher mode, animation semantics, and metadata.
---

# Lesson Stage 03 - Build Lesson

## Goal
Implement a learner-facing lesson package consistent with the solved model and project conventions.

## Mandatory files
- `lessons/<subject>/<grade>/<topic>/<slug>/index.html`
- `lessons/<subject>/<grade>/<topic>/<slug>/meta.json`
- lesson assets under `assets/`

## Procedure
1. Create or update lesson directory using repository taxonomy.
2. Implement `index.html` tabs: problem, solution, animation.
3. Ensure formulas are LaTeX-rendered (KaTeX/MathJax as applicable).
4. Add teacher mode notes and multilingual content (`ja`, `zh`, `en`).
5. Keep animation states aligned with solved model event points.
6. Update manifest via:
   - `node ./scripts/generate-lessons-manifest.mjs`

## Non-negotiables
- No plain-text final equations in learner-facing math sections.
- No mismatch between displayed values and solved model contract.
- No missing lesson metadata fields required by manifest generation.
