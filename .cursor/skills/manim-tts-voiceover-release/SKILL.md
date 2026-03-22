---
name: manim-tts-voiceover-release
description: Generate and release TTS voiceover for Manim lesson videos with strict venv-only execution, speech-density QA, and safe Cloudflare deployment.
---

# Manim TTS Voiceover Release

## When to use
- User asks to convert VTT/subtitles into narration and embed into lesson MP4.
- User asks to polish narration pacing, density, or reference-voice quality.
- User asks to publish narration updates quickly for student review.

## Hard constraints
- Use repository `./.venv` only.
- Do not use conda unless user explicitly requests it.
- Do not create extra venv directories when `./.venv` exists.

## Pipeline
1. **Prepare source**
   - Read `assets/explain/scene-01.vtt`.
   - Build two narration scripts:
     - full script from cues,
     - concise script for low-density fallback.
2. **Generate voiceover**
   - Use `f5-tts_infer-cli` in `./.venv`.
   - Provide explicit `--ref_text` to avoid unintended ASR text leakage.
   - Prefer concise script first if prior run sounded rushed.
3. **Duration alignment**
   - Probe durations with `ffprobe`.
   - Compute gentle `atempo` factor near 1.0 (avoid aggressive compression).
4. **Mux**
   - `ffmpeg -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -shortest`.
   - Keep candidate outputs as `scene-01.tts-*.mp4` until user approves.
5. **Promote**
   - Replace official `scene-01.mp4` only after approval.
6. **Validate**
   - `python scripts/validate-manim-lesson.py <lesson-dir>` in `./.venv`.
7. **Release**
   - Commit only approved final artifacts.
   - Deploy Pages from clean staging directory excluding caches and model blobs.

## QA checklist
- No unrelated words from reference transcript appear in Chinese narration.
- Speech pace is understandable for students.
- Final MP4 duration matches original scene target.
- Audio stream exists and is decodable.
- Temporary files are not accidentally committed.

## Recommended command snippets
```bash
"./.venv/bin/python" scripts/validate-manim-lesson.py lessons/math/elementary/geometry-area-ratio/pythagorean-dissection-mini
ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "lessons/.../scene-01.mp4"
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of default=nokey=1:noprint_wrappers=1 "lessons/.../scene-01.tts.mp4"
```
