---
name: lesson-stage-02-solve-model
description: Solve with at least two independent methods, run unit and boundary checks, and produce a verified solution contract.
---

# Lesson Stage 02 - Solve and Model

## Goal
Produce mathematically verified outputs that can be used directly by lesson UI and animation.

## Mandatory outputs
- Method A and Method B derivations
- final numeric answers with units
- consistency checks (substitution, boundary, dimensional sanity)
- a short "common mistakes" teaching note

## Procedure
1. Define symbols from Stage 01 contract.
2. Solve by two independent methods (for example equation + ratio/geometry).
3. Cross-check final values and units.
4. Run explicit conversion checks (`km/h`, `m/s`, `min`, `s`) when relevant.
5. Emit a solved model contract for Stage 03:
   - key values
   - timeline/event points
   - labels shown in UI/animation

## Non-negotiables
- No single-method release decisions.
- No inferred units without explicit check.
- If checks disagree, stop and return `BLOCKED`.
