---
name: lesson-stage-04-validate
description: Run deterministic QA gates across math correctness, page behavior, animation semantics, and metadata consistency before release.
---

# Lesson Stage 04 - Validate

## Goal
Fail fast on correctness or consistency issues before release.

## Required checks
- numeric assertion checks (including unit conversions)
- local preview self-check (`file exists` + `HTTP 200`)
- browser checkpoints (`start`, `mid`, `end`) with evidence
- manifest and metadata consistency
- Manim/TTS checks when explainers exist

## Procedure
1. Run project validation scripts from `./.venv` for Python tools.
2. Run local HTTP probe for lesson URL and root index.
3. Capture browser evidence at key timeline checkpoints.
4. Run workflow audit script and review warnings/errors.
5. Mark status:
   - `PASS` if all mandatory checks pass
   - `BLOCKED` otherwise

## Non-negotiables
- No visual-only PASS claims without measurable checks.
- No release on unresolved warnings that affect correctness.
- Treat `BLOCKED` as release stop.
