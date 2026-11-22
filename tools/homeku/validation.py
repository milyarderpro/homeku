"""Untrusted ZIP validation, source binding, and MD/media consistency."""

from __future__ import annotations

import json
import re
import stat
import subprocess
import warnings
import zipfile
from datetime import datetime
from fractions import Fraction
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from PIL import Image

from .common import LibraryError, content_hash, read_json, require, safe_relative, sha256
from .markdown import parse

CODE_ROOT = Path(__file__).resolve().parents[2]
SCHEMA = CODE_ROOT / "docs/contracts/manifest-v1.schema.json"
MAX_FILES = 2000
MAX_FILE = 95 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_PIXELS = 60_000_000
Image.MAX_IMAGE_PIXELS = MAX_PIXELS


def extract_package(package: Path, destination: Path) -> Path:
    require(package.is_file() and not package.is_symlink(), f"Package is not a regular file: {package}")
    require(package.stat().st_size <= MAX_TOTAL, "ZIP exceeds 256 MiB")
    require(not destination.exists(), "Extraction destination must be new")
    try:
        with zipfile.ZipFile(package) as archive:
            infos = archive.infolist()
            require(0 < len(infos) <= MAX_FILES, "ZIP has too many files or is empty")
            seen, roots, total = set(), set(), 0
            files = []
            for info in infos:
                name = info.filename[:-1] if info.is_dir() else info.filename
                safe_relative(name)
                require(name.casefold() not in seen, f"Duplicate/case-colliding ZIP path: {name}")
                seen.add(name.casefold())
                roots.add(name.split("/")[0])
                mode = info.external_attr >> 16
                kind = stat.S_IFMT(mode)
                require(kind in (0, stat.S_IFREG, stat.S_IFDIR), f"Special file/symlink in ZIP: {name}")
                require(info.is_dir() or not mode & 0o111, f"Executable ZIP member: {name}")
                require(not info.flag_bits & 1, f"Encrypted ZIP member: {name}")
                require(info.file_size <= MAX_FILE, f"ZIP member exceeds 95 MiB: {name}")
                total += info.file_size
                require(total <= MAX_TOTAL, "Uncompressed ZIP exceeds 256 MiB")
                if not info.is_dir():
                    files.append((info, name))
            require(len(roots) == 1, "ZIP must contain exactly one reference folder")
            reference_id = next(iter(roots))
            require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", reference_id), "Invalid ZIP root ID")
            require(re.fullmatch(re.escape(reference_id) + r"-r[0-9]{4}\.zip", package.name), "Expected <id>-r0001.zip")
            for info in infos:
                if info.is_dir():
                    directory = info.filename.rstrip("/")
                    require(directory == reference_id or re.fullmatch(re.escape(reference_id) + r"/media(?:/shot-[0-9]{2,})?", directory),
                            f"Unsupported directory in ZIP: {directory}")
            for info, name in files:
                relative = name[len(reference_id) + 1:]
                require(relative in {"analysis.md", "manifest.json", "source.mp4"} or
                        re.fullmatch(r"media/(?:storyboard\.jpg|shot-[0-9]{2,}/(?:area-overview|start|middle|end|reveal-[0-9]{2,}|detail-[0-9]{2,})\.jpg)", relative),
                        f"Unsupported file in package: {name}")
                if relative in {"analysis.md", "manifest.json"}:
                    require(info.file_size <= 2 * 1024 * 1024, f"Text file exceeds 2 MiB: {name}")
            destination.mkdir(parents=True)
            for info, name in files:
                target = destination / name
                target.parent.mkdir(parents=True, exist_ok=True)
                # Read through ZipExtFile for CRC checking, never extractall untrusted paths.
                with archive.open(info) as source, target.open("xb") as output:
                    while block := source.read(1024 * 1024):
                        output.write(block)
            return destination / reference_id
    except (zipfile.BadZipFile, RuntimeError, OSError) as error:
        raise LibraryError(f"{package.name}: cannot extract ZIP: {error}") from error


def probe_video(path: Path):
    try:
        completed = subprocess.run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe",
                                    "-show_streams", "-show_format", "-of", "json", str(path)],
                                   check=True, capture_output=True, text=True, timeout=30)
        data = json.loads(completed.stdout)
        videos = [s for s in data["streams"] if s.get("codec_type") == "video" and not s.get("disposition", {}).get("attached_pic")]
        require(videos, f"No video stream: {path.name}")
        video = videos[0]
        duration = float(video.get("duration", data.get("format", {}).get("duration", 0)))
        fps = Fraction(video["avg_frame_rate"])
        require(duration > 0 and 0 < fps <= 240, "Invalid source duration/frame rate")
        width, height = video["width"], video["height"]
        rotations = [v.get("rotation", 0) for v in video.get("side_data_list", [])]
        rotation = rotations[0] if rotations else float(video.get("tags", {}).get("rotate", 0))
        if abs(rotation) % 180 == 90:
            width, height = height, width
        return {"duration_s": duration, "width": width, "height": height,
                "fps": {"numerator": fps.numerator, "denominator": fps.denominator},
                "video_stream_index": video["index"]}
    except (OSError, subprocess.SubprocessError, KeyError, ValueError, ZeroDivisionError) as error:
        raise LibraryError(f"ffprobe cannot read {path.name}: {error}") from error


def jpeg_size(path: Path):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(path) as picture:
                require(picture.format == "JPEG", f"Not a JPEG: {path.name}")
                picture.load()
                return picture.size
    except (OSError, ValueError, Image.DecompressionBombWarning, Image.DecompressionBombError) as error:
        raise LibraryError(f"Invalid JPEG {path.name}: {error}") from error


def validate_folder(folder: Path, root: Path, package_name=None, source_overrides=None):
    manifest_path = folder / "manifest.json"
    require(manifest_path.is_file(), "manifest.json is missing")
    manifest = read_json(manifest_path)
    validator = Draft202012Validator(read_json(SCHEMA), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda e: str(list(e.path)))
    if errors:
        error = errors[0]
        raise LibraryError(f"manifest/{'/'.join(map(str, error.path))}: {error.message}")
    reference_id = manifest["id"]
    require(folder.name == reference_id, "Manifest ID differs from package folder")
    if package_name:
        require(package_name == f"{reference_id}-r{manifest['revision']:04d}.zip", "ZIP revision differs from manifest")
    source_info = manifest["source"]
    require(source_info["path"] == f"video/{reference_id}.mp4", "Source must be video/<id>.mp4")
    video_dir = root / "video"
    if video_dir.exists():
        for video in (p for p in video_dir.iterdir() if p.suffix.casefold() == ".mp4"):
            require(video.name.casefold() != f"{reference_id}.mp4".casefold() or video.name == f"{reference_id}.mp4",
                    f"Source filename case collision: {video.name}")
    source = folder / "source.mp4"
    if not source.exists():
        source = (source_overrides or {}).get(reference_id, root / source_info["path"])
    require(source.is_file() and not source.is_symlink(), f"Source unavailable: {source_info['path']}")
    require(sha256(source) == source_info["sha256"], "Source SHA-256 mismatch")
    canonical = root / source_info["path"]
    if manifest["revision"] == 1 and canonical.exists():
        require(sha256(canonical) == source_info["sha256"], "First revision cannot overwrite different canonical source bytes")
    actual = probe_video(source)
    require(abs(actual["duration_s"] - source_info["duration_s"]) <= 0.001, "Source duration does not match video stream")
    for key in ("width", "height", "fps", "video_stream_index"):
        require(actual[key] == source_info[key], f"Source {key} differs from ffprobe")
    duration = source_info["duration_s"]
    try:
        created = datetime.fromisoformat(manifest["audit"]["created_at"].replace("Z", "+00:00"))
        require(created.utcoffset() is not None, "Audit created_at needs a timezone")
    except ValueError as error:
        raise LibraryError("Audit created_at must be an ISO timestamp with timezone") from error
    ranges = sorted(manifest["audit"]["reviewed_ranges"], key=lambda r: r["start_s"])
    covered = 0.0
    for interval in ranges:
        require(0 <= interval["start_s"] < interval["end_s"] <= duration + 0.001, "Invalid reviewed range")
        require(interval["start_s"] <= covered + 0.001, "Audit coverage has a gap")
        covered = max(covered, interval["end_s"])
    require(abs(covered - duration) <= 0.001, "Audit must describe coverage of the whole duration")
    analysis = folder / "analysis.md"
    require(analysis.is_file(), "analysis.md is missing")
    try:
        model = parse(analysis.read_text(encoding="utf-8"))
    except UnicodeError as error:
        raise LibraryError("analysis.md is not UTF-8") from error
    require(model["format_version"] == manifest["contract_version"], "MD format version differs from manifest")
    require(model["id"] == reference_id and model["revision"] == manifest["revision"], "MD identity/revision differs from manifest")
    for field in ("method", "limitations"):
        require(model["coverage"][field] == manifest["audit"][field], f"MD coverage {field} differs from manifest")
    shots = model["shots"]
    require(abs(shots[0]["start_s"]) <= 0.001 and abs(shots[-1]["end_s"] - duration) <= 0.001, "Timeline must cover source duration")
    for previous, current in zip(shots, shots[1:]):
        require(abs(previous["end_s"] - current["start_s"]) <= 0.001, "Timeline has a gap/overlap; use segments inside a continuous shot")
    by_shot = {s["shot"]: s for s in shots}
    if manifest["contract_version"] == "1.1":
        native_times = validate_frame_reviews(manifest["audit"]["frame_reviews"], shots, source, source_info)
        for interval in ranges:
            if interval["mode"] == "frame-by-frame":
                intervals = sorted((r["start_s"], r["end_s"]) for r in manifest["audit"]["frame_reviews"] if r["mode"] == "frame-by-frame")
                cursor = interval["start_s"]
                for left, right in intervals:
                    if left <= cursor + 0.000001:
                        cursor = max(cursor, right)
                require(cursor >= interval["end_s"] - 0.000001, "Frame-by-frame coverage claim lacks native review records")
    media, folded = {}, set()
    for item in manifest["media"]:
        name = safe_relative(item["path"])
        require(name.casefold() not in folded, f"Duplicate media path: {name}")
        folded.add(name.casefold())
        media[name] = item
        target = folder / name
        require(target.is_file() and not target.is_symlink(), f"Missing media: {name}")
        require(sha256(target) == item["sha256"], f"Media hash mismatch: {name}")
        require(jpeg_size(target) == (item["width"], item["height"]), f"Media dimensions mismatch: {name}")
        if item["kind"] == "storyboard":
            require(name == "media/storyboard.jpg" and item["shot_id"] is None and item["timestamp_s"] is None and item["crop"] is None,
                    "Invalid storyboard metadata")
            continue
        sid = item["shot_id"]
        require(sid in by_shot, f"Unknown media shot: {sid}")
        pattern = item["kind"] + (r"-[0-9]{2,}" if item["kind"] in {"reveal", "detail"} else "")
        require(re.fullmatch(r"media/" + re.escape(sid) + "/" + pattern + r"\.jpg", name), f"Media path/kind mismatch: {name}")
        shot = by_shot[sid]
        timestamp = item["timestamp_s"]
        require(timestamp is not None and shot["start_s"] <= timestamp < shot["end_s"], f"Timestamp outside shot: {name}")
        require(not item["derived_from"], f"Only storyboard uses derived_from: {name}")
        crop = item["crop"]
        if crop is not None:
            x, y, width, height = crop
            require(item["kind"] == "detail" and width > 0 and height > 0 and x + width <= actual["width"] and y + height <= actual["height"],
                    f"Invalid crop coordinates: {name}")
            require((item["width"], item["height"]) == (width, height), f"Crop dimensions differ: {name}")
        else:
            require((item["width"], item["height"]) == (actual["width"], actual["height"]), f"Keep source frame dimensions: {name}")
    require("media/storyboard.jpg" in media, "Missing storyboard")
    require(media["media/storyboard.jpg"]["derived_from"] == [f"media/{s['shot']}/area-overview.jpg" for s in shots],
            "Storyboard must derive from every area-overview in shot order")
    step = source_info["fps"]["denominator"] / source_info["fps"]["numerator"]
    for shot in shots:
        sid = shot["shot"]
        required = {kind: media.get(f"media/{sid}/{kind}.jpg") for kind in ("area-overview", "start", "middle", "end")}
        require(all(required.values()), f"{sid}: missing required area/start/middle/end media")
        t0, tm, t1 = [required[k]["timestamp_s"] for k in ("start", "middle", "end")]
        if manifest["contract_version"] == "1.1":
            import bisect
            first = bisect.bisect_left(native_times, shot["start_s"])
            last = bisect.bisect_left(native_times, shot["end_s"]) - 1
            require(abs(t0 - native_times[first]) <= 0.000001 and abs(t1 - native_times[last]) <= 0.000001,
                    f"{sid}: start/end must be exact first/last native shot frames")
            for item in media.values():
                if item["shot_id"] == sid:
                    pos = bisect.bisect_left(native_times, item["timestamp_s"])
                    require(any(abs(native_times[j] - item["timestamp_s"]) <= 0.000001 for j in (pos - 1, pos) if 0 <= j < len(native_times)),
                            f"{sid}: media timestamp must match native PTS")
        require(t0 <= tm <= t1, f"{sid}: start/middle/end timestamps not ordered")
        require(t0 - shot["start_s"] <= step + 0.002 and shot["end_s"] - t1 <= step * 2 + 0.002,
                f"{sid}: boundary frames too far from shot boundaries")
        require(abs(tm - (shot["start_s"] + shot["end_s"]) / 2) <= step + 0.002, f"{sid}: middle frame not near midpoint")
        comp = shot["composition"]
        overview = required["area-overview"]["timestamp_s"]
        require(abs(overview - comp["overview_timestamp_s"]) <= 0.000001, f"{sid}: overview timestamp differs from MD")
        fraction = (overview - shot["start_s"]) / (shot["end_s"] - shot["start_s"])
        require({"start": fraction <= 1 / 3, "middle": 1 / 3 <= fraction <= 2 / 3, "end": fraction >= 2 / 3}[comp["overview_role"]],
                f"{sid}: overview_role contradicts timestamp (use first/middle/last third)")
        for claim in shot["facts"] + shot["phases"]:
            for link in claim["evidence"]:
                require(link in media and media[link]["shot_id"] == sid, f"{sid}: evidence must belong to this shot: {link}")
    for claim in model.get("profile", []):
        require(all(name in media and media[name]["kind"] != "storyboard" for name in claim["evidence"]), "DNA evidence must link original shot media")
    for relation in model["relations"]:
        require(all(link in media for link in relation["evidence"]), "Unknown relation evidence")
    for link in model["links"]:
        require(link in media or link == f"../../video/{reference_id}.mp4" or link in {f"#{s['shot']}" for s in shots}, f"Unknown/unsupported MD link: {link}")
    require("media/storyboard.jpg" in model["links"], "MD must display/link storyboard")
    for shot in shots:
        require(f"media/{shot['shot']}/area-overview.jpg" in model["links"], f"{shot['shot']}: MD must display/link area-overview")
    actual_files = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}
    allowed = set(media) | {"analysis.md", "manifest.json"}
    if (folder / "source.mp4").exists():
        allowed.add("source.mp4")
    require(actual_files == allowed, f"Unexpected/unlisted files: {sorted(actual_files ^ allowed)}")
    model.update({"source": source_info, "media": manifest["media"], "audit": manifest["audit"],
                  "content_sha256": content_hash(folder)})
    return manifest, model, source


def validate_frame_reviews(reviews, shots, source, info):
    """Check declarations against native PTS; cannot prove an AI actually looked."""
    from .exporter import frame_times, selected_indices
    times = frame_times(source)
    source_fps = info["fps"]["numerator"] / info["fps"]["denominator"]
    by_shot = {s["shot"]: s for s in shots}
    coverage = {sid: [] for sid in by_shot}
    for review in reviews:
        sid = review["shot_id"]
        require(sid in by_shot, "Frame review has unknown shot")
        shot = by_shot[sid]
        start, end = review["start_s"], review["end_s"]
        require(shot["start_s"] <= start < end <= shot["end_s"], "Frame review outside shot")
        native = review["mode"] == "frame-by-frame"
        fps = review["sampling_fps"]
        require((native and fps is None) or (not native and fps is not None), "Native review uses null FPS; sampling declares FPS")
        expected = selected_indices(times, start, end, fps or 10, native=native, source_fps=source_fps)
        require(review["selected_frame_indices"] == expected, "Selected frame indices differ from native PTS selection")
        require(sorted(review["viewed_frame_indices"]) == expected, "Frame review incomplete: declare only frames actually viewed; finish the pass before export")
        coverage[sid].append((start, end))
    for sid, shot in by_shot.items():
        cursor = shot["start_s"]
        for start, end in sorted(coverage[sid]):
            require(start <= cursor + 0.000001, f"Every shot requires a complete 10 FPS (or native) viewed baseline; gap in {sid}")
            cursor = max(cursor, end)
        require(abs(cursor - shot["end_s"]) <= 0.000001,
                f"Every shot requires a complete 10 FPS (or native) viewed baseline including boundary frames: {sid}")
    return times
