# Lesson TTS Release Checklist

This checklist captures stable workflow decisions learned from recent Manim + TTS release iterations.

## 0) When to use this checklist
- Use this checklist when the lesson includes generated narration audio and/or narrated explainer video.
- Mandatory for 3Blue1Brown-style video output (when enabled by learning objective).
- Optional for web-only lessons without TTS/video assets.
- In modular workflow, apply this checklist during:
  - Stage 04 (`lesson-stage-04-validate`)
  - Stage 05 (`lesson-stage-05-release`)

## 0.1) Trigger for 3Blue1Brown-style mode (strict)
- Enable only when visual intuition requires continuous transformation that static text/web animation cannot explain clearly.
- Before generation, search and review similar high-quality references (at least 2) for math narrative structure and visual sequencing.
- Do not imitate style blindly; preserve problem-specific correctness as highest priority.

## 1) Environment discipline
- Run all Python commands in `./.venv`.
- Do not use host Python package installs.
- Do not switch to conda unless explicitly requested.

## 2) Narration authoring
- Start from `scene-01.vtt`, then create a concise narration script for classroom pacing.
- Prefer reducing information density over heavy speed-up.
- Keep formula mentions notation-consistent with on-screen equations.

## 3) Voice cloning safety
- Provide explicit reference transcript text (`--ref_text`) when calling TTS.
- If lexical leakage appears (e.g. unrelated words from sample text), regenerate with a neutral reference transcript.
- Use short reference audio only if quality remains stable; otherwise use longer reference with neutral text.

## 4) Timing and mux
- Probe durations:
  - source video duration
  - generated narration duration
- Apply small `atempo` correction near 1.0 when possible.
- Mux with video copy + AAC audio:
  - keep video stream unchanged,
  - map narration as primary audio stream.

## 5) Validation
- Run:
  - `python scripts/validate-manim-lesson.py <lesson-dir>`
- Verify final output:
  - duration equals target scene duration,
  - audio stream exists (`codec`, sample rate, channels),
  - no obvious pacing/comprehension issues in manual listen-through.
- For 3Blue1Brown-style output, add frame-level checks:
  - key timestamps map to expected math states,
  - on-screen equations and narration remain notation-consistent,
  - no visual shortcut introduces mathematical ambiguity.

## 6) Release hygiene
- Promote approved candidate to official `scene-01.mp4` only after user confirmation.
- Commit only final approved files, avoid temporary TTS artifacts.
- If local deploy fails because of oversized caches/model blobs, deploy from clean staging directory excluding:
  - `.cache/`
  - venv directories
  - temporary generated audio/video files
- Block release immediately if any math/audiovisual contradiction remains unresolved.
