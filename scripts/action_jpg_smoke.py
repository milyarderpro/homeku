"""Generate and verify four test JPG keyframes and a storyboard from an MP4.

POC only: timestamps deliberately fixed to dreamsHouse002.mp4 shot ranges.
Never used to publish or overwrite production references/VID-XXX.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

TIMESTAMPS_S = [3.10, 9.20, 13.70, 18.10]


def run(video: Path, output: Path) -> dict:
    if not video.is_file():
        raise ValueError(f"MP4 source missing: {video}")
    if video.suffix.lower() != ".mp4":
        raise ValueError("Trial only accepts MP4 files")
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not installed")
    if output.exists():
        raise ValueError(f"Output already exists (no overwrites): {output}")
    output.mkdir(parents=True)
    files = []
    for index, timestamp in enumerate(TIMESTAMPS_S, 1):
        jpg = output / f"shot-{index:02d}.jpg"
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
            "-ss", f"{timestamp:.2f}", "-i", str(video),
            "-frames:v", "1", "-q:v", "2", str(jpg),
        ], check=True)
        if not jpg.is_file() or jpg.stat().st_size == 0:
            raise RuntimeError(f"FFmpeg did not produce {jpg.name}")
        with Image.open(jpg) as img:
            if img.format != "JPEG":
                raise RuntimeError(f"Invalid JPEG format: {jpg.name}")
            img.verify()
        files.append(jpg)
    width, height = 340, 340
    board = Image.new("RGB", (width * 2, height * 2), "white")
    draw = ImageDraw.Draw(board)
    for i, jpg in enumerate(files):
        with Image.open(jpg) as image:
            thumb = ImageOps.contain(image.convert("RGB"), (width, height - 26))
        x = (i % 2) * width + (width - thumb.width) // 2
        y = (i // 2) * height + (height - 26 - thumb.height) // 2
        board.paste(thumb, (x, y))
        draw.text(((i % 2) * width + 10, (i // 2) * height + height - 22), f"Shot {i + 1:02d} - {TIMESTAMPS_S[i]:.2f}s", fill="black")
    storyboard = output / "storyboard.jpg"
    board.save(storyboard, "JPEG", quality=90)
    files.append(storyboard)
    report = []
    for jpg in files:
        raw = jpg.read_bytes()
        with Image.open(jpg) as image:
            dimensions = image.size
            image.verify()
        report.append({
            "name": jpg.name, "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "dimensions": f"{dimensions[0]}x{dimensions[1]}",
        })
    return {"video": video.name, "output_dir": str(output), "files": report}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(run(args.video, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
