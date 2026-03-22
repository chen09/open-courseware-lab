# open-courseware-lab

Open-source interactive K-12 courseware for math, physics, chemistry, and future subjects, with multilingual support and web-first delivery.

## Overview

This repository hosts interactive lesson pages designed for family and classroom learning.

Each lesson can include:

- clear problem statement
- step-by-step solution
- animated visualization
- multilingual text support

## Content structure

Lessons are organized as:

- `lessons/<subject>/<grade>/<topic>/<problem-slug>/`

Current subject taxonomy:

- `math`
- `physics` (planned)
- `chemistry` (planned)

## Current lessons

- Lessons are cataloged in `lessons/manifest.json`.
- Root homepage renders cards from the manifest.
- Example lesson path:
  - `lessons/math/elementary/speed-distance/jiro-taro-catchup-rest/`

## Why this project

- Build reusable lesson templates across subjects
- Support more languages over time
- Share lessons easily via URL (LINE / WeChat / browser)

## Quick start

Run a local static server from repository root:

```bash
python3 -m http.server 8080
```

## Maintain catalog homepage

The root homepage reads `lessons/manifest.json` and renders lesson cards automatically.

When adding or updating lessons, regenerate the manifest before deployment:

```bash
node ./scripts/generate-lessons-manifest.mjs
```

## Modular workflow

- Orchestration prompt:
  - `docs/KICKOFF_AGENT_PROMPT.md`
- Stage skills:
  - `.cursor/skills/lesson-stage-01-intake/SKILL.md`
  - `.cursor/skills/lesson-stage-02-solve-model/SKILL.md`
  - `.cursor/skills/lesson-stage-03-build-lesson/SKILL.md`
  - `.cursor/skills/lesson-stage-04-validate/SKILL.md`
  - `.cursor/skills/lesson-stage-05-release/SKILL.md`
  - `.cursor/skills/lesson-stage-06-retro-governance/SKILL.md`
- Architecture and templates:
  - `docs/workflow-modular-architecture.md`
  - `docs/lesson-retro-template.md`
  - `docs/workflow-cycle-review-template.md`

Run workflow audit before release:

```bash
node ./scripts/qa-workflow-audit.mjs
```
