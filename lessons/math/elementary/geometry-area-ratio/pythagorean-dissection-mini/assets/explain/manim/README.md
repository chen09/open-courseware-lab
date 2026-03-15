# Manim Render Guide (venv-only)

This lesson uses a 3Blue1Brown-style Manim scene as the primary animation.

## 0) System prerequisites for MathTex (macOS)

`scene_01_pythagorean.py` uses `MathTex`, so `latex` must exist in PATH.

Recommended (Homebrew):

```bash
brew install --cask mactex-no-gui
```

Then ensure command is available:

```bash
which latex
latex --version
```

## 1) Create isolated environment

```bash
cd /Volumes/WDC2T/Project/open-courseware-lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-manim.txt
```

## 2) Render scene

```bash
cd lessons/math/elementary/geometry-area-ratio/pythagorean-dissection-mini/assets/explain/manim
manim -pqh scene_01_pythagorean.py Scene01PythagoreanDissection
```

## 3) Copy output to lesson asset path

The lesson page expects:

- `assets/explain/scene-01.mp4`
- `assets/explain/scene-01.poster.webp`
- `assets/explain/scene-01.vtt`

Copy the rendered mp4 to:

```bash
cp "<rendered_mp4_path>" ../scene-01.mp4
```

Optional:

- export one frame as `scene-01.poster.webp`
- add captions as `scene-01.vtt`

## 4) Run release validation (required)

From repo root:

```bash
python scripts/extract-animation-checkframes.py lessons/math/elementary/geometry-area-ratio/pythagorean-dissection-mini --profile assets/explain/qc-checkpoints.json
python scripts/validate-manim-lesson.py lessons/math/elementary/geometry-area-ratio/pythagorean-dissection-mini
```

Only treat the lesson as ready when the validator prints `OK: validation passed`.
