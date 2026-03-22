---
name: lesson-stage-05-release
description: Execute deterministic release flow with clean artifacts, PR discipline, deployment verification, and rollback-safe reporting.
---

# Lesson Stage 05 - Release

## Goal
Ship only audited lesson outputs to production and verify the final URL behavior.

## Procedure
1. Stage only approved files (exclude caches/temp media/intermediate TTS files).
2. Create branch and commit with clear scope.
3. Push and create PR, then merge per repo policy.
4. Deploy Cloudflare Pages from clean staging directory when needed.
5. Verify production URLs (lesson + root + manifest), including cache-busting checks.
6. Publish final report:
   - PR URL
   - production URL
   - PASS/BLOCKED
   - unresolved risks (if any)

## Non-negotiables
- No deployment when Stage 04 is `BLOCKED`.
- No accidental release of local caches or model artifacts.
- No "release first, verify later" behavior.
