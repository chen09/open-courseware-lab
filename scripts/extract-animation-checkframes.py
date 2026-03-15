#!/usr/bin/env python3
"""
Extract keyframes for animation QA from a checkpoint profile.

Profile format (JSON):
{
  "video": "assets/explain/scene-01.mp4",
  "checkpoints": [
    {
      "id": "top-overlap",
      "time": "00:00:03.800",
      "description": "No overlap at top area",
      "mcp_prompt": "Analyze overlap..."
    }
  ]
}

Usage:
  python scripts/extract-animation-checkframes.py \
    lessons/.../pythagorean-dissection-mini \
    --profile assets/explain/qc-checkpoints.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def _ffprobe_duration(video_path: Path) -> float:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def _extract_frame(video_path: Path, time_code: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        time_code,
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        str(output_path),
    ]
    _run(command)


def _write_markdown_report(
    report_path: Path,
    lesson_dir: Path,
    video_path: Path,
    duration: float,
    checkpoints: list[dict[str, Any]],
    frames_dir: Path,
) -> None:
    lines: list[str] = []
    lines.append("# Animation QA Report")
    lines.append("")
    lines.append(f"- lesson: `{lesson_dir}`")
    lines.append(f"- video: `{video_path}`")
    lines.append(f"- duration: `{duration:.3f}s`")
    lines.append("")
    lines.append("## Checkpoints")
    lines.append("")

    for item in checkpoints:
        cid = item["id"]
        desc = item.get("description", "")
        time_code = item["time"]
        frame_path = frames_dir / f"{cid}.png"
        lines.append(f"- [ ] `{cid}` @ `{time_code}`")
        if desc:
            lines.append(f"  - check: {desc}")
        lines.append(f"  - frame: `{frame_path}`")
        prompt = item.get("mcp_prompt")
        if prompt:
            lines.append(f"  - minimax prompt: `{prompt}`")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Use local frame extraction to save tokens.")
    lines.append("- Send only failed/suspicious frames to image MCP (e.g. understand_image).")
    lines.append("")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract animation keyframes for QA")
    parser.add_argument("lesson_dir", help="Lesson directory path")
    parser.add_argument(
        "--profile",
        default="assets/explain/qc-checkpoints.json",
        help="Checkpoint profile path relative to lesson_dir",
    )
    parser.add_argument(
        "--output-dir",
        default="assets/explain/qc-frames",
        help="Output frame directory relative to lesson_dir",
    )
    parser.add_argument(
        "--report",
        default="assets/explain/qc-report.md",
        help="Output report path relative to lesson_dir",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    lesson_dir = Path(args.lesson_dir)
    if not lesson_dir.is_absolute():
        lesson_dir = (repo_root / lesson_dir).resolve()

    profile_path = (lesson_dir / args.profile).resolve()
    if not profile_path.exists():
        print(f"Profile not found: {profile_path}", file=sys.stderr)
        return 1

    profile = _read_json(profile_path)
    video_rel = profile.get("video", "assets/explain/scene-01.mp4")
    checkpoints = profile.get("checkpoints", [])
    if not isinstance(checkpoints, list) or not checkpoints:
        print("Profile checkpoints are empty", file=sys.stderr)
        return 1

    video_path = (lesson_dir / video_rel).resolve()
    if not video_path.exists():
        print(f"Video not found: {video_path}", file=sys.stderr)
        return 1

    frames_dir = (lesson_dir / args.output_dir).resolve()
    report_path = (lesson_dir / args.report).resolve()
    duration = _ffprobe_duration(video_path)

    for item in checkpoints:
        cid = item.get("id")
        time_code = item.get("time")
        if not cid or not time_code:
            print(f"Invalid checkpoint item: {item}", file=sys.stderr)
            return 1
        output_path = frames_dir / f"{cid}.png"
        _extract_frame(video_path=video_path, time_code=time_code, output_path=output_path)

    _write_markdown_report(
        report_path=report_path,
        lesson_dir=lesson_dir,
        video_path=video_path,
        duration=duration,
        checkpoints=checkpoints,
        frames_dir=frames_dir,
    )

    print(f"Extracted {len(checkpoints)} frames to: {frames_dir}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
