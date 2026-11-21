"""Read-only verification or deterministic rendering of the published catalog."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
CATALOG = ROOT / "knowledge/reference-catalog.md"
ROW_RE = re.compile(r"^\| \[(?P<id>[A-Za-z0-9_.-]+)\]\(\.\./references/(?P=id)/analysis\.yaml\)\s*\|")


def read_references(root=ROOT, *, published=False):
    if published:
        from knowledge_library import published_references
        return published_references(root)
    result = {}
    for file in sorted((Path(root) / "references").glob("*/analysis.yaml")):
        data = yaml.safe_load(file.read_text(encoding="utf-8"))
        ident = file.parent.name
        if data["video"]["id"] != ident or data["video"]["shot_count"] != len(data["shots"]):
            raise ValueError(f"Reference identity/shot count mismatch: {ident}")
        result[ident] = data
    if not result:
        raise ValueError("No source analysis files")
    return result


def markdown_rows(text):
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


def render_catalog(refs=None, *, release_id=None, root=ROOT):
    if refs is None:
        from knowledge_library import load_release, published_references
        release_id = load_release(root)["release_id"]
        refs = published_references(root)
    lines = ["# HOMEKU — Published reference catalog", "",
             f"Knowledge release: {release_id}. Source labels and timings remain recorded annotations.",
             "New archives do not enter this table until an explicit knowledge publication.",
             "", "[Reference profiles](reference-profiles/README.md) · [Core knowledge](ai-knowledge.md) · [Release](release.json)",
             "", "| Reference | Recorded style | Length (s) | Shots | Opening shot (s) | Annotated scenes | First-shot camera labels |",
             "| --- | --- | ---: | ---: | ---: | --- | --- |"]
    for ident, doc in sorted(refs.items()):
        shots, video = doc["shots"], doc["video"]
        fields = [f"[{ident}](../references/{ident}/analysis.yaml)",
                  str(doc["architecture"]["primary_style"]), f"{float(video['duration_s']):.3f}",
                  str(len(shots)), f"{float(shots[0]['end_s']) - float(shots[0]['start_s']):.3f}",
                  ", ".join(str(x) for x in doc["video_structure"].get("scene_sequence", [])),
                  " + ".join(shots[0]["camera"]["movements"]) or "not_recorded"]
        if any("|" in cell or "\n" in cell for cell in fields):
            raise ValueError(f"Unsafe catalog text for {ident}")
        lines.append("| " + " | ".join(fields) + " |")
    return "\n".join(lines + ["", "Inspect source YAML, frames and original video for evidence; this table does not establish a floorplan or physical camera rig.", ""])


def verify_catalog(root=ROOT):
    root = Path(root)
    refs = read_references(root, published=True)
    content = (root / "knowledge/reference-catalog.md").read_text(encoding="utf-8")
    if set(markdown_rows(content)) != set(refs) or content != render_catalog(root=root):
        raise ValueError("Published catalog differs from its release; rebuild the current snapshot")
    return len(refs), sum(len(d["shots"]) for d in refs.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        (args.root / "knowledge/reference-catalog.md").write_text(render_catalog(root=args.root), encoding="utf-8")
    count, shots = verify_catalog(args.root)
    print(f"Published catalog verified: {count} references / {shots} shots")


if __name__ == "__main__":
    main()
