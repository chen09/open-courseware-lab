#!/usr/bin/env python3
"""
Validate a Manim-backed lesson package for publish readiness.

Usage:
  python scripts/validate-manim-lesson.py lessons/math/.../pythagorean-dissection-mini
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> Any:
    return json.loads(_read_text(path))


def _parse_vtt_time(value: str) -> float:
    # WEBVTT supports hh:mm:ss.mmm (or mm:ss.mmm). We normalize both.
    parts = value.strip().split(":")
    if len(parts) == 2:
        hours = 0
        minutes = int(parts[0])
        seconds = float(parts[1])
    elif len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
    else:
        raise ValueError(f"Invalid VTT time: {value}")
    return hours * 3600 + minutes * 60 + seconds


def _last_vtt_end_seconds(vtt_path: Path) -> float | None:
    text = _read_text(vtt_path)
    matches = re.findall(r"(\d{1,2}:\d{2}(?::\d{2})?\.\d{3})\s*-->\s*(\d{1,2}:\d{2}(?::\d{2})?\.\d{3})", text)
    if not matches:
        return None
    return _parse_vtt_time(matches[-1][1])


def _ffprobe_duration_seconds(mp4_path: Path) -> float:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(mp4_path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def _fail(errors: list[str], message: str) -> None:
    errors.append(message)


def _warn(warnings: list[str], message: str) -> None:
    warnings.append(message)


def validate(lesson_dir: Path, repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    index_path = lesson_dir / "index.html"
    meta_path = lesson_dir / "meta.json"
    assets_dir = lesson_dir / "assets" / "explain"
    mp4_path = assets_dir / "scene-01.mp4"
    vtt_path = assets_dir / "scene-01.vtt"
    poster_path = assets_dir / "scene-01.poster.webp"
    manifest_path = repo_root / "lessons" / "manifest.json"

    for required in (index_path, meta_path, mp4_path, vtt_path, poster_path, manifest_path):
        if not required.exists():
            _fail(errors, f"Missing required file: {required}")

    if errors:
        return errors, warnings

    index_text = _read_text(index_path)
    if "./assets/explain/scene-01.mp4" not in index_text:
        _fail(errors, "index.html missing expected MP4 source path './assets/explain/scene-01.mp4'")
    if "./assets/explain/scene-01.vtt" not in index_text:
        _fail(errors, "index.html missing expected VTT track path './assets/explain/scene-01.vtt'")
    if index_text.count("<video") < 1:
        _fail(errors, "index.html contains no <video> element")

    meta = _load_json(meta_path)
    assets = meta.get("assets", [])
    for expected in ("assets/explain/scene-01.mp4", "assets/explain/scene-01.poster.webp", "assets/explain/scene-01.vtt"):
        if expected not in assets:
            _fail(errors, f"meta.json assets missing: {expected}")

    features = meta.get("features", [])
    if "manim-explainer-slot" not in features:
        _warn(warnings, "meta.json features does not include 'manim-explainer-slot'")

    manifest_data = _load_json(manifest_path)
    if isinstance(manifest_data, dict):
        manifest = manifest_data.get("lessons", [])
    elif isinstance(manifest_data, list):
        manifest = manifest_data
    else:
        _fail(errors, "manifest.json has unexpected top-level shape")
        return errors, warnings
    lesson_id = meta.get("id")
    lesson_slug = meta.get("slug")
    lesson_path = "./" + str(lesson_dir.relative_to(repo_root)).replace("\\", "/") + "/"

    found_id = any(isinstance(entry, dict) and entry.get("id") == lesson_id for entry in manifest)
    found_path = any(isinstance(entry, dict) and entry.get("path") == lesson_path for entry in manifest)
    if not found_id:
        _fail(errors, f"manifest missing lesson id: {lesson_id}")
    if not found_path:
        _fail(errors, f"manifest missing lesson path: {lesson_path}")
    if lesson_slug and not any(isinstance(entry, dict) and entry.get("slug") == lesson_slug for entry in manifest):
        _fail(errors, f"manifest missing lesson slug: {lesson_slug}")

    try:
        video_duration = _ffprobe_duration_seconds(mp4_path)
    except Exception as exc:  # pylint: disable=broad-except
        _fail(errors, f"ffprobe failed for MP4 duration: {exc}")
        return errors, warnings

    vtt_end = _last_vtt_end_seconds(vtt_path)
    if vtt_end is None:
        _fail(errors, "VTT has no cue timing blocks")
        return errors, warnings

    # Allow tiny drift due to player precision/trimming.
    if vtt_end + 0.05 < video_duration:
        _fail(
            errors,
            f"VTT ends too early: {vtt_end:.3f}s < video {video_duration:.3f}s; extend final cue",
        )
    if vtt_end > video_duration + 1.5:
        _warn(
            warnings,
            f"VTT ends much later than video: {vtt_end:.3f}s vs {video_duration:.3f}s",
        )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Manim lesson assets and metadata consistency")
    parser.add_argument("lesson_dir", help="Path to lesson directory (e.g., lessons/math/.../pythagorean-dissection-mini)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    lesson_dir = Path(args.lesson_dir)
    if not lesson_dir.is_absolute():
        lesson_dir = (repo_root / lesson_dir).resolve()

    errors, warnings = validate(lesson_dir=lesson_dir, repo_root=repo_root)

    print(f"Lesson: {lesson_dir}")
    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("\nOK: validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
