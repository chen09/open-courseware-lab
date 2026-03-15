---
name: manim-lesson-polish
description: Polish Manim lesson videos for children-facing math explainers. Use when refining animation pacing, overlap/layout, mapping order, VTT timing, and cross-file consistency across scene python, vtt, index, meta, and manifest.
---

# Manim Lesson Polish

## Goal
Ship a visually clear, logically ordered explainer where animation, formula mapping, and VTT narration are fully aligned.

## Workflow
1. **Baseline scan**
   - Read scene file and VTT.
   - Probe MP4 duration with `ffprobe`.
   - Check `index.html`, `meta.json`, and manifest entry.
2. **Detect common failures**
   - Overlap (title/equation/subtitle safe zones).
   - Mixed mapping language (arrow + ghost for same concept).
   - Wrong narrative order (target appears before source movement).
   - Geometry/labels inconsistency (`a/b/c`, right-angle semantics).
   - VTT describes outdated animation behavior.
3. **Patch with minimal deltas**
   - Prefer small coordinate/timing changes.
   - Keep one visual language per concept segment.
4. **Render and inspect**
   - Render MP4.
   - Extract profile-driven key frames:
     - `python scripts/extract-animation-checkframes.py <lesson-dir> --profile assets/explain/qc-checkpoints.json`
   - Review `assets/explain/qc-report.md`.
   - For token efficiency: send only suspicious/failed frame PNGs to image MCP analysis.
   - Recommended image MCP: `user-minimax-coding-plan / understand_image`.
5. **VTT sync pass**
   - Update wording to match actual motion.
   - Align cue boundaries to motion beats.
   - Extend final cue to >= probed duration if needed.
6. **Cross-file release checks**
   - Video/track paths valid in `index.html`.
   - Fallback text reflects failure mode, not stale setup state.
   - `meta.json` assets/features reflect real files.
   - Manifest contains lesson path.
7. **Run executable validator**
   - Execute:
     - `python scripts/validate-manim-lesson.py <lesson-dir>`
   - Treat validator errors as blockers before handoff.
8. **Execution policy**
   - Agent runs all QA commands after animation edits by default.
   - User should receive results, not command burden, unless local permission/environment blocks execution.

## Non-Negotiables
- Children-facing clarity over visual complexity.
- No unresolved overlap/artifact at handoff.
- No ambiguous sequencing between geometry and equation.
- No release without passing `validate-manim-lesson.py`.
- No release without generating and checking profile keyframes.
