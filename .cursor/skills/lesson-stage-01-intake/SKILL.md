---
name: lesson-stage-01-intake
description: Intake and normalize one new problem into a release-ready lesson spec with explicit givens, targets, units, and ambiguity blockers.
---

# Lesson Stage 01 - Intake

## Goal
Convert raw input (image/text/optional solution) into a normalized problem contract before solving or coding.

## Mandatory outputs
- `subject`, `gradeBand`, `topic`, `slug` candidate
- extracted givens, unknowns, units, and constraints
- ambiguity/conflict list (if any)
- release decision: `GO` or `BLOCKED`

## Procedure
1. Parse the problem source and optional answer source independently.
2. Build a canonical statement with variables and units.
3. Compare problem vs optional answer for contradiction.
4. If contradiction exists, mark `BLOCKED` and stop release flow.
5. Emit a concise intake summary for downstream stages.

## Non-negotiables
- Never skip unit normalization.
- Never continue if core conditions are contradictory.
- Keep decisions deterministic (same input -> same contract).
