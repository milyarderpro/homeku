"""Stage-1 runtime probe, not the production splitter.

Requires Pillow. Inputs must have two equal side-by-side panels whose layout
has already been inspected. This probe does not infer architecture or detect
panel boundaries. It never resizes or generates replacement pixels.
"""
from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path

from PIL import Image
import PIL

WORKSPACE = Path(__file__).resolve().parents[1]
RUNS = WORKSPACE / "runs"


def panel_regions(size, inset=False):
    width, height = size
    if width % 2 or width < 18 or height < 16:
        raise ValueError("Expected an even-width canvas with two equal panels.")
    panel_width = width // 2
    frame_width, frame_height = panel_width, height
    if frame_width * 16 != frame_height * 9:
        if not inset:
            raise ValueError("Panels are not exactly 9:16; inspect them before allowing an inset crop.")
        unit = min(panel_width // 9, height // 16)
        frame_width, frame_height = 9 * unit, 16 * unit
    left = (panel_width - frame_width) // 2
    top = (height - frame_height) // 2
    return [(offset + left, top, offset + left + frame_width, top + frame_height)
            for offset in (0, panel_width)]


def split_probe(source, output, inset=False):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not output.is_relative_to(RUNS.resolve()):
        raise ValueError("Probe output must stay under bekerja/plugin/runs/.")
    names = ("shot-01-start.png", "shot-01-end.png", "probe.json")
    if any((output / name).exists() for name in names):
        raise FileExistsError("Existing probe output will not be overwritten.")
    raw = source.read_bytes()
    with Image.open(BytesIO(raw)) as image:
        image.load()
        if image.mode not in ("RGB", "RGBA"):
            raise ValueError("This pilot accepts RGB/RGBA images without color conversion.")
        regions = panel_regions(image.size, inset)
        output.mkdir(parents=True, exist_ok=True)
        records = []
        for role, box, name in zip(("start", "end"), regions, names[:2]):
            crop = image.crop(box)
            path = output / name
            crop.save(path, format="PNG")
            with Image.open(path) as saved:
                saved.load()
                preserved = saved.mode == crop.mode and saved.size == crop.size and saved.tobytes() == crop.tobytes()
            if not preserved:
                raise ValueError("Saved crop does not preserve source pixels.")
            records.append({
                "role": role, "file": name, "box_xyxy": list(box),
                "size": list(crop.size), "aspect_ratio": "9:16",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "source_pixels_preserved": preserved,
                "retained_panel_fraction": crop.width * crop.height / ((image.width // 2) * image.height),
            })
        report = {
            "scope": "stage1_workspace_capability_probe_not_production_component",
            "source": str(source.relative_to(WORKSPACE)) if source.is_relative_to(WORKSPACE) else str(source),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "source_size": list(image.size),
            "pillow_version": PIL.__version__,
            "layout_assumption": "visually_inspected_equal_side_by_side_panels",
            "inset_crop_explicitly_enabled": inset,
            "resized": False, "files": records,
        }
    (output / "probe.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def self_check(output):
    output = Path(output).resolve()
    if not output.is_relative_to(RUNS.resolve()):
        raise ValueError("Self-check output must stay under bekerja/plugin/runs/.")
    output.mkdir(parents=True, exist_ok=True)
    source = output / "synthetic-collage.png"
    if source.exists():
        raise FileExistsError("Existing synthetic source will not be overwritten.")
    data = bytes(channel for y in range(640) for x in range(720)
                 for channel in (x % 256, y % 256, 32 if x < 360 else 224))
    image = Image.frombytes("RGB", (720, 640), data)
    image.save(source)
    report = split_probe(source, output / "frames")
    assert [r["box_xyxy"] for r in report["files"]] == [[0, 0, 360, 640], [360, 0, 720, 640]]
    assert all(r["source_pixels_preserved"] for r in report["files"])
    checks = ["ordered_exact_crops_and_decoded_pixel_equality"]
    for label, size in (("odd_width_rejected", (721, 640)), ("wrong_aspect_rejected", (730, 640))):
        try:
            panel_regions(size)
        except ValueError:
            checks.append(label)
        else:
            raise AssertionError(label)
    assert panel_regions((1330, 1182), True) == [(4, 7, 661, 1175), (669, 7, 1326, 1175)]
    checks.append("explicit_inset_retains_exact_9_16_without_resize")
    try:
        split_probe(source, output / "frames")
    except FileExistsError:
        checks.append("existing_outputs_not_overwritten")
    else:
        raise AssertionError("Overwrite protection failed")
    return {"scope": "synthetic_checks_not_visual_consistency", "checks_passed": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--source", type=Path)
    mode.add_argument("--self-check", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--inset-to-9x16", action="store_true",
                        help="Explicitly crop a centered 9:16 rectangle inside each inspected panel.")
    args = parser.parse_args()
    if args.self_check and args.inset_to_9x16:
        parser.error("--inset-to-9x16 is only for --source")
    try:
        result = self_check(args.output) if args.self_check else split_probe(args.source, args.output, args.inset_to_9x16)
    except (ValueError, FileExistsError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
