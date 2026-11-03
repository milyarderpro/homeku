"""Validate a Homeku analysis package; never writes to GitHub."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml
from PIL import Image

ID_RE = re.compile(r"(?:VID-\d{3,}|PENDING)\Z")
SHOT_RE = re.compile(r"shot-(\d{2,})\Z")
COMMON_REGIONS = frozenset({"north_america", "south_america", "europe", "asia", "africa", "oceania"})


class InvalidPackage(ValueError):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidPackage(message)


def validate(package: Path, expected_id: str | None = None) -> dict[str, Any]:
    package = package.resolve(strict=True)
    check(package.is_dir(), "Package must be a directory")
    yaml_path, md_path = package / "analysis.yaml", package / "analysis.md"
    check(yaml_path.is_file() and md_path.is_file(), "analysis.yaml and analysis.md are required")
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    check(isinstance(data, dict), "YAML must be a mapping")
    check(str(data.get("schema_version")) == "2.1", "Unsupported schema_version")
    video = data.get("video") or {}
    vid = video.get("id")
    check(isinstance(vid, str) and bool(ID_RE.fullmatch(vid)), "Invalid video.id")
    check(expected_id is None or vid == expected_id, "video.id does not match expected ID")
    check(package.name == vid, "Package folder and video.id differ")
    shots = data.get("shots")
    check(isinstance(shots, list) and bool(shots), "shots must be non-empty")
    check(video.get("shot_count") == len(shots), "video.shot_count differs from shots length")
    duration = video.get("duration_s")
    check(isinstance(duration, (float, int)) and not isinstance(duration, bool) and duration > 0, "Invalid video duration")
    architecture = data.get("architecture") or {}
    scale = architecture.get("building_scale") or {}
    check(all(k in scale for k in ("perceived_size", "building_form", "vertical_scale", "footprint", "estimated_floor_area_m2", "confidence")), "Missing architecture.building_scale fields")
    area = scale["estimated_floor_area_m2"]
    check(isinstance(area, dict) and "min" in area and "max" in area, "Missing area range")
    lo, hi = area["min"], area["max"]
    check((lo is None and hi is None) or (isinstance(lo, (int, float)) and not isinstance(lo, bool) and isinstance(hi, (int, float)) and not isinstance(hi, bool) and 0 < lo <= hi), "Invalid estimated area range")
    check(scale["confidence"] in ("low", "medium", "high"), "Invalid area confidence")
    if "common_regions" in architecture:
        regions = architecture["common_regions"]
        check(isinstance(regions, list), "architecture.common_regions must be a list")
        check(all(isinstance(region, str) and region in COMMON_REGIONS for region in regions),
              "Invalid architecture.common_regions value")
        check(len(regions) == len(set(regions)), "Duplicate architecture.common_regions value")
    markdown = md_path.read_text(encoding="utf-8")
    if "common_regions" in architecture:
        region_text = ", ".join(region.replace("_", " ") for region in regions) if regions else "Tidak diketahui"
        check(f"| Wilayah terkait gaya desain | {region_text} |" in markdown,
              "architecture.common_regions differs from Markdown")
    if "<!-- homeku_detail_narratives: chat-reviewed -->" in markdown:
        for label in ("Arsitektur", "Furnitur dan properti", "Lingkungan"):
            check(markdown.count("\n**" + label + "**\n") == len(shots),
                  f"Incomplete narrative category in Markdown: {label}")
    check(vid in markdown, "Video ID missing from Markdown")
    check(re.search(r"!\[[^\]]*\]\(storyboard\.jpg\)", markdown) is not None, "Storyboard must appear inline")
    expected_files = {"analysis.yaml", "analysis.md", "storyboard.jpg"}
    previous_end = 0.0
    for i, shot in enumerate(shots, 1):
        sid = f"shot-{i:02d}"
        name = f"{sid}.jpg"
        check(shot.get("id") == sid, f"Unexpected shot ID at index {i}")
        start, end = shot.get("start_s"), shot.get("end_s")
        check(all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (start, end)), f"Invalid timestamp {sid}")
        check(start >= 0 and end > start and abs(start - previous_end) <= 0.35, f"Shot timeline gap or overlap: {sid}")
        previous_end = end
        check(shot.get("keyframe") == f"references/{vid}/{name}", f"Incorrect keyframe path: {sid}")
        check(re.search(rf'<img\s+[^>]*src=[\"\']{name}[\"\']', markdown) is not None, f"Missing inline image {name}")
        check(f"Shot {i:02d}" in markdown, f"Missing Shot {i:02d} label")
        expected_files.add(name)
    check(abs(previous_end - duration) <= 0.35, "Shots do not cover video duration")
    present = {p.name for p in package.iterdir() if p.is_file()}
    check(present == expected_files, f"Unexpected/missing files: missing={sorted(expected_files-present)}, extra={sorted(present-expected_files)}")
    for name in sorted(expected_files):
        if name.endswith(".jpg"):
            p = package / name
            with Image.open(p) as image:
                check(image.format == "JPEG", f"Not a JPEG file: {name}")
                image.verify()
    quality = data.get("analysis_quality") or {}
    check(quality.get("status") in ("draft", "reviewed") and isinstance(quality.get("human_verified"), bool), "Invalid analysis quality status")
    return {"video_id": vid, "shot_count": len(shots), "files": sorted(expected_files), "duration_s": duration}



NARRATIVE_CATEGORIES = ("architectural", "furniture_and_props", "environment")
MAX_NARRATIVE_CHARS = 4000


def validate_narratives(data: dict[str, Any], narratives: Any) -> None:
    """Validate ChatGPT-reviewed presentation text against YAML item coverage.

    This proves structural coverage, NOT semantic equivalence. ChatGPT must
    review fidelity to the visible evidence and YAML before 'save now'.
    """
    shots = data.get("shots")
    check(isinstance(shots, list) and bool(shots), "Missing shots for narratives")
    check(isinstance(narratives, dict), "shot_narratives must be an object")
    shot_ids = [s.get("id") for s in shots]
    check(set(narratives) == set(shot_ids) and len(shot_ids) == len(set(shot_ids)),
          "shot_narratives shot IDs must match YAML shots exactly")
    for shot in shots:
        sid = shot["id"]
        details = shot.get("visible_details")
        check(isinstance(details, dict), f"Missing visible_details: {sid}")
        entry = narratives[sid]
        check(isinstance(entry, dict) and set(entry) == set(NARRATIVE_CATEGORIES),
              f"Missing/extra narrative categories: {sid}")
        for category in NARRATIVE_CATEGORIES:
            source = details.get(category)
            check(isinstance(source, list) and all(isinstance(x, str) for x in source),
                  f"Invalid YAML source details: {sid}.{category}")
            cell = entry[category]
            check(isinstance(cell, dict) and set(cell) == {"text", "covered_indices"},
                  f"Invalid narrative cell keys: {sid}.{category}")
            indices = cell["covered_indices"]
            check(isinstance(indices, list) and
                  all(type(i) is int for i in indices) and
                  len(indices) == len(source) and
                  set(indices) == set(range(len(source))),
                  f"Invalid covered_indices: {sid}.{category}")
            value = cell["text"]
            if not source:
                check(value is None, f"Empty YAML category must have null text: {sid}.{category}")
            else:
                check(isinstance(value, str) and bool(value.strip()) and
                      len(value) <= MAX_NARRATIVE_CHARS and
                      all(ord(char) >= 32 or char in "\t\n\r" for char in value),
                      f"Invalid narrative text: {sid}.{category}")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="references/PENDING or references/VID-XXX")
    parser.add_argument("--id", help="Expected video ID")
    args = parser.parse_args()
    import json
    print(json.dumps(validate(args.package, args.id), indent=2))


if __name__ == "__main__":
    main()
