"""Find source similarity candidates; never merge, retire or delete references."""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path

from knowledge_library import ROOT, dump, load_release
from sample_temporal_evidence import dhash, extract_frame, video_duration
from verify_source_integrity import sha256_file, verify_sources

MAX_DISTANCE = 6
MIN_MATCHES = 2
MIN_CONTRAST = 12


def matched_frames(left, right, max_distance=MAX_DISTANCE):
    """Greedy one-to-one hash matches; a single shared frame cannot count twice."""
    choices = []
    for a, b in itertools.product(left, right):
        if min(a["contrast"], b["contrast"]) < MIN_CONTRAST:
            continue
        distance = (int(a["dhash"], 16) ^ int(b["dhash"], 16)).bit_count()
        if distance <= max_distance:
            choices.append((distance, a["path"], b["path"], a, b))
    used_a, used_b, result = set(), set(), []
    for distance, pa, pb, a, b in sorted(choices, key=lambda x: x[:3]):
        if pa in used_a or pb in used_b:
            continue
        used_a.add(pa)
        used_b.add(pb)
        result.append({"distance": distance, "left_frame": a, "right_frame": b})
    return result


def collect_samples(root, extract=False):
    root = Path(root)
    verify_sources(root)
    release = load_release(root)
    rows = []
    published = {s["source_path"]: s for s in release["references"]}
    # The scan includes unannotated or not-yet-published videos, without publishing them.
    for video in sorted((root / "video").glob("*.mp4")):
        relative = video.relative_to(root).as_posix()
        source_hash = sha256_file(video)
        source = published.get(relative)
        if source:
            path = root / "knowledge/temporal" / source["reference_id"] / "index.json"
            data = json.loads(path.read_text())
            if data["source"] != source:
                raise ValueError("Stale temporal samples for similarity")
            frames = [f for shot in data["shots"] for f in shot["frames"]]
            ident = source["reference_id"]
            sampling = "three_per_annotated_shot"
        else:
            ident = "archive-" + video.stem
            path = root / "knowledge/similarity/archive-samples" / (video.stem + ".json")
            if not path.exists():
                if not extract:
                    raise ValueError("Missing unannotated samples: run --write")
                duration = video_duration(video)
                frames = []
                for n, ratio in enumerate((0.15, 0.5, 0.85)):
                    timestamp = duration * ratio
                    target = path.parent / f"{video.stem}-{n}.jpg"
                    extract_frame(video, timestamp, target)
                    visual_hash, contrast = dhash(target)
                    frames.append({"label": f"uniform-{n}", "timestamp_s": round(timestamp, 6),
                                   "path": target.relative_to(root).as_posix(),
                                   "sha256": sha256_file(target), "dhash": visual_hash, "contrast": contrast})
                data = {"source_path": relative, "source_sha256": source_hash,
                        "frames": frames, "sampling": "three_uniform_interior_timestamps"}
                path.write_text(dump(data))
            else:
                data = json.loads(path.read_text())
                if data["source_path"] != relative or data["source_sha256"] != source_hash:
                    raise ValueError("Stale archive similarity samples")
            frames = data["frames"]
            sampling = data["sampling"]
        for frame in frames:
            asset = root / frame["path"]
            if sha256_file(asset) != frame["sha256"]:
                raise ValueError("Changed similarity frame: " + frame["path"])
            # Recompute hashes rather than trusting cached perceptual metadata.
            actual_hash, actual_contrast = dhash(asset)
            if actual_hash != frame["dhash"] or actual_contrast != frame["contrast"]:
                raise ValueError("Changed perceptual metadata: " + frame["path"])
        rows.append({"id": ident, "source_path": relative, "source_sha256": source_hash,
                     "sampling": sampling, "frames": frames})
    return rows


def report(root=ROOT, extract=False):
    sources = collect_samples(root, extract)
    candidates = []
    for left, right in itertools.combinations(sources, 2):
        matches = matched_frames(left["frames"], right["frames"])
        if len(matches) >= MIN_MATCHES:
            candidates.append({"id": "similarity." + left["id"] + "." + right["id"],
                               "left": left["id"], "right": right["id"],
                               "left_source_path": left["source_path"], "right_source_path": right["source_path"],
                               "left_source_sha256": left["source_sha256"], "right_source_sha256": right["source_sha256"],
                               "matched_sample_count": len(matches),
                               "left_sample_coverage": round(len(matches) / len(left["frames"]), 4),
                               "right_sample_coverage": round(len(matches) / len(right["frames"]), 4),
                               "matches": matches, "review_state": "candidate_requires_content_review",
                               "action": "retain_both_sources"})
    return {"schema_version": "1.0", "method": "content_crop_dhash64_greedy_unique_matches_v1",
            "release_id": load_release(root)["release_id"],
            "thresholds": {"max_hamming_distance": MAX_DISTANCE, "minimum_unique_matches": MIN_MATCHES,
                           "minimum_grayscale_contrast": MIN_CONTRAST},
            "video_count": len(sources), "sample_count": sum(len(s["frames"]) for s in sources),
            "source_inventory": [{k: v for k, v in s.items() if k != "frames"} for s in sources],
            "compared_video_pairs": len(sources) * (len(sources) - 1) // 2,
            "candidate_count": len(candidates), "candidates": candidates,
            "limitations": [
                "Candidate screen only, not a calibrated duplicate classifier.",
                "Similar compositions may yield false positives; crops, heavy edits and unsampled content may be missed.",
                "Three uniform samples on unannotated videos have lower coverage than annotated videos.",
                "No automatic deletion, merging, count adjustment or claim of independent houses."]}


def render(result):
    lines = ["# Video similarity candidates", "", f"{result['video_count']} videos; {result['sample_count']} samples; "
             f"{result['compared_video_pairs']} video pairs; {result['candidate_count']} candidate pairs.",
             "", "[Full data and matching frames](candidates.json) · [Corpus patterns](../corpus-patterns.md)", "",
             "Method: content-cropped 64-bit difference hashes, Hamming distance ≤6, at least two unique paired samples, "
             "minimum grayscale contrast 12. It can flag a re-encode or shared scene when sampled appearances survive, "
             "but it is not exhaustive and has no calibrated precision/recall.", "",
             "Every result is a review candidate. Both sources remain. Matching styles or layouts alone do not prove a duplicate.", ""]
    for c in result["candidates"]:
        lines += [f"## {c['left']} / {c['right']}", "",
                  f"{c['matched_sample_count']} matching sample pairs; {c['review_state']}.", ""]
        for match in c["matches"][:3]:
            a, b = match["left_frame"], match["right_frame"]
            rel = lambda p: Path("..") / Path(p).relative_to("knowledge")
            lines.append(f"- distance {match['distance']}: [{c['left']} {a['timestamp_s']}s]({rel(a['path']).as_posix()}) / "
                         f"[{c['right']} {b['timestamp_s']}s]({rel(b['path']).as_posix()})")
        lines.append("")
    lines += ["## Limits", ""] + ["- " + x for x in result["limitations"]] + [""]
    return "\n".join(lines)


def run(root=ROOT, write=False):
    root = Path(root)
    value = report(root, extract=write)
    outputs = {"knowledge/similarity/candidates.json": dump(value),
               "knowledge/similarity/README.md": render(value)}
    for relative, content in outputs.items():
        path = root / relative
        if write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        elif not path.is_file() or path.read_text() != content:
            raise ValueError("Stale similarity report: " + relative)
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run(args.root, args.write)
    print(f"{result['video_count']} videos / {result['candidate_count']} candidate pairs; no sources altered")


if __name__ == "__main__":
    main()
