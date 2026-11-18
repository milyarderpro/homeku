"""Crop an inspected two-panel collage into start/end PNGs without resizing.

Dependencies: requirements.txt. Equal left/right panels are assumed, never
detected. Inspect the image first. Non-exact canvases require explicit crop boxes, not an automatic
inset. This tool records pixel/file checks; it does not approve house continuity.
"""
from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import re

from PIL import Image
import yaml

SKILL_ROOT = Path(__file__).resolve().parents[1]
FRAME_RULES = yaml.safe_load(
    (SKILL_ROOT / "references/production-rules.yaml").read_text()
)["frames"]
RATIO_X, RATIO_Y = FRAME_RULES["aspect_ratio"]


def panel_boxes(size, start_box=None, end_box=None):
    """Validate integer XYXY crops, right/bottom exclusive, inside each half."""
    width, height = size
    if (start_box is None) != (end_box is None):
        raise ValueError("Supply both --start-box and --end-box.")
    if start_box is None:
        if width % 2 or (width // 2) * RATIO_Y != height * RATIO_X:
            raise ValueError("Canvas halves are not exactly 9:16; inspect and supply both crop boxes.")
        boxes = ((0, 0, width // 2, height), (width // 2, 0, width, height))
    else:
        boxes = (tuple(start_box), tuple(end_box))
    sizes = []
    for box in boxes:
        if len(box) != 4 or any(type(value) is not int for value in box):
            raise ValueError("Crop boxes must contain four integers.")
        left, top, right, bottom = box
        if not (0 <= left < right <= width and 0 <= top < bottom <= height):
            raise ValueError("Crop box is empty or outside the source canvas.")
        frame_size = (right - left, bottom - top)
        if frame_size[0] * RATIO_Y != frame_size[1] * RATIO_X:
            raise ValueError("Every crop must be exactly 9:16 without resizing.")
        sizes.append(frame_size)
    if sizes[0] != sizes[1]:
        raise ValueError("Both frames must have the same dimensions.")
    if boxes[0][2] > width // 2 or boxes[1][0] < (width + 1) // 2:
        raise ValueError("Start must stay in the left half and end in the right half; do not mix panels.")
    return boxes


def split_frames(source, output, shot_id, start_box=None, end_box=None, min_frame_width=None):
    """Write two new PNGs and a crop report; never overwrite existing results."""
    if not re.fullmatch(r"shot-[0-9]{2,}", shot_id):
        raise ValueError("shot_id must use the shot-01 naming pattern.")
    if min_frame_width is not None and (type(min_frame_width) is not int or min_frame_width <= 0):
        raise ValueError("min_frame_width must be a positive integer.")
    source, output = Path(source).resolve(), Path(output).resolve()
    raw = source.read_bytes()
    payloads, records = {}, []
    with Image.open(BytesIO(raw)) as image:
        if getattr(image, "is_animated", False) or getattr(image, "n_frames", 1) != 1:
            raise ValueError("Use one still collage, not an animated or multi-frame image.")
        if image.getexif().get(274, 1) != 1:
            raise ValueError("Source has an orientation transform; prepare an upright source before cropping.")
        image.load()
        if image.mode not in ("RGB", "RGBA"):
            raise ValueError("Use an RGB/RGBA source; this tool does not convert colors or pixels.")
        boxes = panel_boxes(image.size, start_box, end_box)
        source_size, mode = image.size, image.mode
        for role, box in zip(FRAME_RULES["roles"], boxes):
            crop = image.crop(box)
            buffer = BytesIO()
            crop.save(buffer, format=FRAME_RULES["format"], icc_profile=image.info.get("icc_profile"))
            encoded = buffer.getvalue()
            with Image.open(BytesIO(encoded)) as saved:
                saved.load()
                if (saved.format != FRAME_RULES["format"] or saved.mode != crop.mode
                        or saved.size != crop.size or saved.tobytes() != crop.tobytes()):
                    raise ValueError("PNG encoding failed to preserve the crop pixels.")
            filename = f"{shot_id}-{role}.png"
            payloads[filename] = encoded
            records.append({
                "role": role, "file": filename, "box_xyxy": list(box),
                "width": crop.width, "height": crop.height, "mode": crop.mode,
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "source_pixels_preserved": True,
                "retained_half_fraction": crop.width * crop.height / ((image.width / 2) * image.height),
            })
    target_met = None if min_frame_width is None else records[0]["width"] >= min_frame_width
    report = {
        "report_version": "1.0", "shot_id": shot_id,
        "source": {
            "path": os.path.relpath(source, output),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "width": source_size[0], "height": source_size[1], "mode": mode,
        },
        "layout_assumption": "inspected_equal_panels_left_start_right_end",
        "aspect_ratio": FRAME_RULES["aspect_ratio"],
        "explicit_boxes": start_box is not None,
        "resized": False, "regenerated": False,
        "visual_review_performed": False,
        "minimum_frame_width": min_frame_width,
        "resolution_target_met": target_met,
        "warnings": [] if target_met is not False else [
            "Frame width is below the requested minimum. Cropping does not add detail."
        ],
        "files": records,
    }
    report_name = f"{shot_id}-split.json"
    payloads[report_name] = (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if any((output / name).exists() or (output / name).is_symlink() for name in payloads):
        raise FileExistsError("Existing frame/report will not be overwritten; use a new revision directory.")
    output.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for name, data in payloads.items():
            path = output / name
            with path.open("xb") as handle:
                created.append(path)
                handle.write(data)
            if path.read_bytes() != data:
                raise OSError("Written file does not match the prepared output.")
    except (OSError, ValueError):
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shot-id", required=True)
    parser.add_argument("--start-box", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--end-box", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--min-frame-width", type=int,
                        help="Optional production width target; smaller output is reported, never upscaled.")
    args = parser.parse_args()
    try:
        result = split_frames(args.source, args.output, args.shot_id,
                              args.start_box, args.end_box, args.min_frame_width)
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
