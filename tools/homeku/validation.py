"""Validate and bind an audit package before publishing its bytes."""
from __future__ import annotations
import re
import stat
import warnings
import zipfile
from pathlib import Path
from PIL import Image
from . import FORMAT_VERSION
from .audit_quality import validate_audit_logs
from .common import LibraryError, read_json, require, safe_relative, sha256, snapshot_hash
from .media import expected_media
from .models import ROOT as CODE_ROOT, _clean, from_json, schema_check, validate_audit
from .package_manifest import validate_frame_map
from .render_assets import MAX_BYTES, MAX_PIXELS, verify_renderer
from .reporting import render_report
from .video import frame_times, probe_video

MAX_FILES = 2000
MAX_FILE = MAX_BYTES
MAX_TOTAL = 256 * 1024 * 1024
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
                require(info.orig_filename == info.filename, "NUL in ZIP member name")
                name = info.filename[:-1] if info.is_dir() else info.filename
                safe_relative(name)
                require(name.casefold() not in seen, f"Duplicate/case-colliding ZIP path: {name}")
                seen.add(name.casefold())
                roots.add(name.split("/")[0])
                mode = info.external_attr >> 16
                kind = stat.S_IFMT(mode)
                require(kind in (0, stat.S_IFREG, stat.S_IFDIR), f"Special file/symlink in ZIP: {name}")
                require(kind in (0, stat.S_IFDIR if info.is_dir() else stat.S_IFREG),
                        f"Inconsistent file type in ZIP: {name}")
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
                    require(directory in {reference_id, reference_id + "/media"},
                            f"Unsupported directory in ZIP: {directory}")
            for info, name in files:
                require(name.startswith(reference_id + "/"), "ZIP requires a reference folder")
                relative = name[len(reference_id) + 1:]
                require(relative in {"analysis.md", "audit.json", "manifest.json"} or
                        re.fullmatch(r"media/(?:shot-[0-9]{2,}|overview|storyboard)\.jpg", relative),
                        f"Unsupported file in package: {name}. Create a final ZIP with the current HOMEKU kit.")
                if relative in {"analysis.md", "audit.json", "manifest.json"}:
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


def package_files(folder, audit):
    files = {"audit.json", "analysis.md", "manifest.json", "media/overview.jpg", "media/storyboard.jpg"}
    files.update(f"media/{shot['shot']}.jpg" for shot in audit["shots"])
    actual = set()
    total = 0
    for path in folder.rglob("*"):
        relative = path.relative_to(folder).as_posix()
        require(not path.is_symlink(), f"Symlink in candidate: {relative}")
        if path.is_dir():
            require(relative == "media", f"Unmanaged directory in candidate: {relative}")
            continue
        require(path.is_file() and relative in files, f"Unmanaged file in candidate: {relative}")
        size = path.stat().st_size
        require(size <= (MAX_FILE if relative.startswith("media/") else 2 * 1024 * 1024),
                f"File size exceeds package limit: {relative}")
        total += size
        actual.add(relative)
    require(len(actual) <= MAX_FILES and total <= MAX_TOTAL, "Candidate exceeds package limits")
    require(files == actual, f"Missing candidate files: {sorted(files - actual)}")
    return sorted(files)


def validate_folder(folder: Path, root: Path, package_name=None, source_overrides=None, *,
                    require_source=True, context=None, plan=None, report=None):
    folder = Path(folder)
    require(folder.is_dir() and not folder.is_symlink(), "Invalid candidate folder")
    def require_document(name):
        path = folder / name
        require(path.is_file() and not path.is_symlink() and path.stat().st_size <= 2 * 1024 * 1024,
                f"Missing or invalid candidate file: {name}")
        return path

    manifest = read_json(require_document("manifest.json"))
    require(isinstance(manifest, dict) and manifest.get("contract_version") == FORMAT_VERSION,
            "Unsupported package format; audit again with the current HOMEKU kit")
    require_document("analysis.md")
    audit_path = require_document("audit.json")
    schema_check(manifest, "manifest.schema.json")
    audit = read_json(audit_path)
    require(isinstance(audit, dict) and audit.get("schema_version") == FORMAT_VERSION,
            "Unsupported audit format; audit again with the current HOMEKU kit")
    require(sha256(audit_path) == manifest["audit_sha256"], "Audit SHA-256 mismatch")
    rid, revision = manifest["id"], manifest["revision"]
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", rid) and folder.name == rid and
            audit.get("id") == rid and audit.get("revision") == revision, "Audit/manifest/folder identity mismatch")
    if package_name is not None:
        require(package_name == f"{rid}-r{revision:04d}.zip", "ZIP revision differs from manifest")
    supersedes = manifest["supersedes"]
    require((revision == 1 and supersedes is None) or
            (revision > 1 and supersedes is not None and supersedes["revision"] == revision - 1),
            "Invalid supersedes for revision")
    info = manifest["source"]
    require(info["path"] == f"video/{rid}.mp4", "Source must be video/<id>.mp4")
    source = None
    times = None
    if require_source:
        canonical = root / info["path"]
        if canonical.parent.exists():
            require(not any(p.name.casefold() == canonical.name.casefold() and p.name != canonical.name
                            for p in canonical.parent.iterdir()), "Source filename case collision")
        source = Path((source_overrides or {}).get(rid, canonical))
        require(source.is_file() and not source.is_symlink() and source.name == f"{rid}.mp4",
                f"Source unavailable: {info['path']}")
        if context is None:
            digest = sha256(source)
            require(digest == info["sha256"], "Source SHA-256 mismatch")
            actual = probe_video(source)
            times = frame_times(source, info=actual)
        else:
            digest, actual, times = context["sha256"], context["info"], context["times"]
        require(digest == info["sha256"], "Source SHA-256 mismatch")
        require(all(actual[key] == info[key] for key in actual), "Source metadata differs from native stream")
        if canonical.exists() and canonical.resolve() != source.resolve():
            require(not canonical.is_symlink() and sha256(canonical) == digest,
                    "Canonical source must retain the same bytes")
    validate_audit(audit, info["duration_s"], times)
    package_files(folder, audit)
    validate_frame_map(manifest, audit, times)
    _clean(manifest["audit"])
    if require_source:
        validate_audit_logs(manifest["audit"], audit, source, info, times=times)
    verify_renderer(manifest["render"])
    frames = manifest["frames"]
    try:
        text = (folder / "analysis.md").read_bytes().decode("utf-8")
    except UnicodeError as error:
        raise LibraryError("analysis.md must be UTF-8") from error
    expected_report = report if report is not None else render_report(audit, frames)
    require(text == expected_report, "analysis.md differs from the rendered report")
    if plan is None:
        plan = list(expected_media(audit, info, manifest["render"], frames))
    require(len(plan) == len(manifest["media"]), "Manifest media inventory does not match source")
    for (expected, _, _), media in zip(plan, manifest["media"]):
        require(expected == {key: value for key, value in media.items() if key != "sha256"},
                f"Manifest media geometry/inventory mismatch: {expected['path']}")
        path = folder / media["path"]
        require(sha256(path) == media["sha256"], f"Media SHA-256 mismatch: {media['path']}")
        require(jpeg_size(path) == (media["width"], media["height"]), f"JPEG dimensions mismatch: {media['path']}")
    model = from_json(audit, manifest)
    model["content_sha256"] = snapshot_hash(folder)
    return manifest, model, source
