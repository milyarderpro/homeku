"""Read-only by default: verify the Design Intelligence catalog against reference YAML.

--write regenerates only knowledge/reference-catalog.md using existing YAML.
It does not modify references, production artifacts or source analysis files.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
CATALOG = ROOT / "knowledge" / "reference-catalog.md"
ROW_RE = re.compile(
    r"^\| \[(?P<id>[A-Za-z0-9_.-]+)\]\(\.\./references/(?P=id)/analysis\.yaml\)\s*\|"
)


def read_references() -> dict[str, dict]:
    result = {}
    for file in sorted(REFERENCES.glob("*/analysis.yaml")):
        data = yaml.safe_load(file.read_text(encoding="utf-8"))
        ident = file.parent.name
        if data["video"]["id"] != ident:
            raise ValueError(f"Reference identifier mismatch: {ident}")
        shots = data["shots"]
        if data["video"]["shot_count"] != len(shots):
            raise ValueError(f"Shot count mismatch: {ident}")
        result[ident] = data
    if not result:
        raise ValueError("No source analysis files")
    return result


def markdown_rows(text: str) -> dict[str, list[str]]:
    rows = {}
    for line in text.splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        ident = match.group("id")
        if ident in rows:
            raise ValueError(f"Duplicate catalog ID: {ident}")
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            raise ValueError(f"Expected seven catalog columns: {ident}")
        rows[ident] = cells
    return rows


def verify_catalog() -> tuple[int, int]:
    data = read_references()
    rows = markdown_rows(CATALOG.read_text(encoding="utf-8"))
    if set(rows) != set(data):
        raise ValueError(
            f"Catalog sources differ; missing={sorted(set(data)-set(rows))}, "
            f"obsolete={sorted(set(rows)-set(data))}"
        )
    shots = 0
    for ident, item in data.items():
        cells = rows[ident]
        style = str(item["architecture"]["primary_style"])
        total = int(item["video"]["shot_count"])
        duration = float(item["video"]["duration_s"])
        opening = float(item["shots"][0]["end_s"]) - float(item["shots"][0]["start_s"])
        recorded_opening = cells[4].replace("*", "").strip()
        if cells[1] != style or int(cells[3]) != total:
            raise ValueError(f"Source style/shot mismatch in catalog: {ident}")
        if abs(float(cells[2]) - duration) > 0.02:
            raise ValueError(f"Duration mismatch in catalog: {ident}")
        if abs(float(recorded_opening) - opening) > 0.03:
            raise ValueError(f"Opening shot mismatch in catalog: {ident}")
        shots += total
    return len(data), shots


def render_catalog() -> str:
    refs = read_references()
    lines = [
        "# HOMEKU — Reference catalog (generated from source YAML)",
        "",
        "A source-data index, not an AI design-generation or video-production rule. "
        "Descriptions and durations are recorded annotations, not independently verified measurements. "
        "Regenerate explicitly with `python scripts/refresh_design_catalog.py --write` and review the diff.",
        "",
        "| Reference | Recorded style | Length (s) | Shots | Opening shot (s) | Annotated scenes | First-shot camera labels |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for ident, item in sorted(refs.items()):
        shots = item["shots"]
        video = item["video"]
        style = item["architecture"]["primary_style"]
        scene = ", ".join(str(x) for x in item["video_structure"]["scene_sequence"])
        camera = " + ".join(shots[0]["camera"]["movements"]) or "not_recorded"
        first = float(shots[0]["end_s"]) - float(shots[0]["start_s"])
        fields = [
            f"[{ident}](../references/{ident}/analysis.yaml)",
            str(style),
            f"{float(video['duration_s']):.3f}",
            str(len(shots)),
            f"{first:.3f}",
            scene,
            camera,
        ]
        if any("|" in cell or "\n" in cell for cell in fields):
            raise ValueError(f"Unsafe catalog text for {ident}")
        lines.append("| " + " | ".join(fields) + " |")
    lines.extend(
        ["", "Use each linked YAML, its analysis report and visual frames to inspect individual claims. "
         "A scene label or camera tag cannot establish a measured floorplan or physical camera rig.", ""]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Validate catalog against reference YAML (default)")
    mode.add_argument("--write", action="store_true", help="Regenerate catalog from current YAML")
    args = parser.parse_args()
    if args.write:
        CATALOG.write_text(render_catalog(), encoding="utf-8")
    count, shots = verify_catalog()
    print(f"Design catalog verified: {count} references / {shots} shots")


if __name__ == "__main__":
    main()
