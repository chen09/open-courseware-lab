# Workflow Modular Architecture

This project now uses a staged execution model:

1. Intake (`lesson-stage-01-intake`)
2. Solve/Model (`lesson-stage-02-solve-model`)
3. Build Lesson (`lesson-stage-03-build-lesson`)
4. Validate (`lesson-stage-04-validate`)
5. Release (`lesson-stage-05-release`)
6. Retrospective/Governance (`lesson-stage-06-retro-governance`)

## Why
- Reduce prompt drift from one monolithic workflow file.
- Keep each stage independently updatable.
- Make recurring failures actionable through periodic governance.

## Contract between stages
- Stage 01 -> 02: normalized problem contract.
- Stage 02 -> 03: solved model contract (values, units, event points).
- Stage 03 -> 04: implemented lesson package.
- Stage 04 -> 05: PASS/BLOCKED decision plus evidence.
- Stage 05 -> 06: release outcome and incident summary.

## Evidence artifacts
- Validation evidence: browser checkpoints + numeric assertions.
- Audit evidence: `reports/workflow-audit/latest.json`.
- Retro evidence: `docs/lesson-retro-template.md` records.

## Cycle governance
- Trigger a full cycle review every 10-15 lessons using:
  - `docs/workflow-cycle-review-template.md`
- Convert frequent errors into rule/skill/script updates.
