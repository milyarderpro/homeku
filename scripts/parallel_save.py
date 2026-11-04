"""Homeku v1.4: one immutable filename-based request per independent Actions run.

ChatGPT is the only AI: this runner validates approved prose and produces files.
Run from a git checkout pinned to the triggering commit.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import yaml

from save_analysis_action import markdown
from storyboard import generate_storyboard
from validate_analysis import validate, validate_narratives

STEM = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z")
VIDEO_PATH = re.compile(r"video/([A-Za-z0-9][A-Za-z0-9_.-]{0,63})\.mp4\Z")
REQUEST_PATH = re.compile(r"requests/pending/([A-Za-z0-9][A-Za-z0-9_.-]{0,63})\.json\Z")
REQUEST_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{7,79}\Z")


class SaveConflict(ValueError):
    """Refuse ambiguous, conflicting, or partially published state."""


def require(ok, reason):
    if not ok:
        raise SaveConflict(reason)


def git(*args, cwd=None):
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.PIPE
    ).strip()


def git_bytes(*args, cwd=None):
    return subprocess.check_output(["git", *args], cwd=cwd, stderr=subprocess.PIPE)


def filename_id(path):
    match = VIDEO_PATH.fullmatch(path) if isinstance(path, str) else None
    require(match is not None, "Invalid video path (expected video/<stem>.mp4)")
    name = match.group(1)
    require(name.upper() != "PENDING" and not name.startswith("VID-"),
            "Reserved filename ID")
    return name


def request_id_from_path(path):
    match = REQUEST_PATH.fullmatch(path) if isinstance(path, str) else None
    require(match is not None, "Invalid pending request path")
    name = match.group(1)
    require(name.upper() != "PENDING" and not name.startswith("VID-"),
            "Reserved request ID stem")
    return name


def request_path_for_video(video_path):
    return f"requests/pending/{filename_id(video_path)}.json"


def check_case_collisions(root, stem):
    """Names are case-sensitive but portable across case-insensitive filesystems."""
    for parent, suffix in (
        (root / "video", ".mp4"),
        (root / "requests/pending", ".json"),
        (root / "requests/results", ".json"),
        (root / "references", ""),
    ):
        if not parent.exists():
            continue
        for item in parent.iterdir():
            actual = item.name[:-len(suffix)] if suffix and item.name.casefold().endswith(suffix) else (
                item.name if not suffix and item.is_dir() else None
            )
            if actual is not None and actual.casefold() == stem.casefold():
                require(actual == stem, f"Case collision: {actual} vs {stem}")


def find_archive(root, video_filename):
    """Return archive directory name; fail closed on malformed existing YAML."""
    ref_dir = root / "references"
    if not ref_dir.exists():
        return None
    matches = []
    for folder in sorted(ref_dir.iterdir()):
        if not folder.is_dir():
            continue
        source = folder / "analysis.yaml"
        require(source.is_file(), f"Unparseable existing archive: {folder.name}")
        try:
            data = yaml.safe_load(source.read_text(encoding="utf-8"))
            existing_filename = data["video"]["filename"]
            require(isinstance(existing_filename, str), "Invalid archive filename")
        except (KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
            raise SaveConflict(f"Invalid existing archive: {folder.name}") from exc
        if existing_filename.casefold() == video_filename.casefold():
            matches.append(folder.name)
    require(len(matches) <= 1, f"Duplicate archive records: {matches}")
    return matches[0] if matches else None


def load_request(root, request_path, *, require_narratives=True):
    vid = request_id_from_path(request_path)
    path = root / request_path
    require(path.is_file(), f"Pending request not found: {request_path}")
    req = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(req, dict) and req.get("schema_version") == "1.0"
            and req.get("status") == "approved", "Invalid request schema/status")
    rid = req.get("request_id")
    require(isinstance(rid, str) and REQUEST_ID.fullmatch(rid), "Invalid request_id")
    source = req.get("video")
    require(isinstance(source, dict), "Missing video")
    video_path = source.get("path")
    require(filename_id(video_path) == vid, "Request ID differs from video filename")
    sha = source.get("blob_sha")
    require(isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{40}", sha),
            "Invalid source Git blob SHA")
    check_case_collisions(root, vid)
    require(git("rev-parse", f"HEAD:{video_path}", cwd=root) == sha,
            "Video Git blob SHA mismatch")
    video = root / video_path
    require(video.is_file() and video.stat().st_size > 0, "MP4 missing")
    raw = req.get("analysis_yaml")
    require(isinstance(raw, str) and len(raw) > 100, "Missing analysis_yaml")
    data = yaml.safe_load(raw)
    require(isinstance(data, dict) and str(data.get("schema_version")) == "2.1",
            "Invalid YAML schema")
    v = data.get("video")
    shots = data.get("shots")
    require(isinstance(v, dict) and v.get("filename") == video.name,
            "YAML filename mismatch")
    require(v.get("id") in ("PENDING", vid), "YAML draft ID mismatches request")
    require(isinstance(shots, list) and 1 <= len(shots) <= 99
            and v.get("shot_count") == len(shots), "Invalid shot count")
    times = req.get("keyframe_times_s")
    require(isinstance(times, list) and len(times) == len(shots),
            "Invalid keyframe count")
    for index, (shot, t) in enumerate(zip(shots, times), 1):
        require(isinstance(shot, dict) and shot.get("id") == f"shot-{index:02d}",
                "Invalid shot order")
        require(type(t) in (int, float) and math.isfinite(t)
                and float(shot["start_s"]) <= t < float(shot["end_s"]),
                "Keyframe outside shot")
    narratives = req.get("shot_narratives")
    if require_narratives:
        require("shot_narratives" in req, "v1.4 request requires shot_narratives")
    validate_narratives(data, narratives)
    return vid, req, data, narratives, times


def render(root, request_path):
    """Generate a temporary new-format archive and result; no git writes."""
    vid, req, data, narratives, times = load_request(root, request_path)
    already = find_archive(root, data["video"]["filename"])
    if already is not None:
        return {"status": "already_saved", "video_id": already,
                "request_id": req["request_id"]}
    dest = root / "references" / vid
    result_path = root / "requests/results" / (vid + ".json")
    require(not dest.exists() and not result_path.exists(),
            "Partial/conflicting local archive or result")
    source = root / req["video"]["path"]
    data["video"]["id"] = vid
    dest.mkdir(parents=True)
    try:
        frames = []
        for i, (shot, t) in enumerate(zip(data["shots"], times), 1):
            shot["keyframe"] = f"references/{vid}/shot-{i:02d}.jpg"
            jpg = dest / f"shot-{i:02d}.jpg"
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                 "-ss", f"{t:.3f}", "-i", str(source), "-frames:v", "1",
                 "-q:v", "2", str(jpg)], check=True
            )
            require(jpg.is_file() and jpg.stat().st_size > 0, "FFmpeg JPEG missing")
            frames.append(jpg)
        generate_storyboard(frames, dest / "storyboard.jpg",
                            video=data["video"], architecture=data["architecture"],
                            shots=data["shots"])
        (dest / "analysis.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        (dest / "analysis.md").write_text(
            markdown(data, req["request_id"], narratives), encoding="utf-8"
        )
        info = validate(dest, vid, narratives)
        result = {"status": "saved", "request_id": req["request_id"], "video_id": vid,
                  "video_path": req["video"]["path"], "source_blob_sha": req["video"]["blob_sha"],
                  "shot_count": len(data["shots"]), "file_count": len(info["files"]),
                  "run_id": os.getenv("GITHUB_RUN_ID")}
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
        return result
    except BaseException:
        shutil.rmtree(dest, ignore_errors=True)
        result_path.unlink(missing_ok=True)
        raise


def event_request_path(root, event, event_name, trigger_sha):
    """Require exactly one new request on push; dispatch chooses one existing path."""
    if event_name == "workflow_dispatch":
        require(event.get("ref") == "refs/heads/main",
                "Manual recovery is only permitted on main")
        inputs = event.get("inputs") or {}
        path = inputs.get("request_path")
        request_id_from_path(path)
        require((root / path).is_file(), "Dispatch request missing in snapshot")
        return path
    require(event_name == "push" and event.get("ref") == "refs/heads/main",
            "Unsupported workflow event")
    before = event.get("before")
    require(isinstance(before, str) and re.fullmatch(r"[0-9a-f]{40}", before)
            and before != "0" * 40, "Invalid push before SHA")
    names = git("diff", "--name-status", before, trigger_sha, "--",
                "requests/pending", cwd=root).splitlines()
    added = []
    changes = []
    for line in names:
        status, _, path = line.partition("\t")
        if REQUEST_PATH.fullmatch(path) and status == "A":
            added.append(path)
        elif path.startswith("requests/pending/"):
            changes.append(line)
    require(len(added) == 1 and not changes,
            f"Expected exactly one added request (dispatch other paths manually): "
            f"added={added}, other_changes={changes}")
    return added[0]


def remote_files(root, ref, folder):
    """Extract the exact remote archive into an isolated temp directory for validation."""
    prefix = f"references/{folder}/"
    names = [p for p in git("ls-tree", "-r", "--name-only", ref, "--",
                           f"references/{folder}", cwd=root).splitlines() if p.startswith(prefix)]
    return names


def check_remote_case_collisions(root, ref, stem):
    """Recheck casefold aliases against moving main before each publication."""
    paths = git("ls-tree", "-r", "--name-only", ref, "--", "video", "requests",
                "references", cwd=root).splitlines()
    for path in paths:
        name = None
        if path.startswith("video/") and path.count("/") == 1 and path.casefold().endswith(".mp4"):
            name = path.split("/")[-1][:-4]
        elif path.startswith(("requests/pending/", "requests/results/")) and path.casefold().endswith(".json"):
            name = path.split("/")[-1][:-5]
        elif path.startswith("references/") and path.count("/") == 2:
            name = path.split("/")[1]
        if name is not None and name.casefold() == stem.casefold():
            require(name == stem, f"Remote case collision: {name} vs {stem}")


def remote_archive(root, ref, video_filename):
    """Check every YAML archive, including legacy, at the current remote HEAD."""
    names = [p for p in git("ls-tree", "-r", "--name-only", ref, "--", "references",
                           cwd=root).splitlines() if p.endswith("/analysis.yaml")]
    matches = []
    for path in names:
        try:
            value = yaml.safe_load(git_bytes("show", f"{ref}:{path}", cwd=root))
            name = value["video"]["filename"]
            require(isinstance(name, str), "Bad archive filename")
        except (KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
            raise SaveConflict(f"Bad remote archive: {path}") from exc
        if name.casefold() == video_filename.casefold():
            matches.append(path.split("/")[1])
    require(len(matches) <= 1, f"Duplicate remote archives: {matches}")
    return matches[0] if matches else None


def read_remote_result(root, ref, vid):
    path = f"requests/results/{vid}.json"
    try:
        raw = git_bytes("show", f"{ref}:{path}", cwd=root)
    except subprocess.CalledProcessError:
        return None
    try:
        result = json.loads(raw)
        require(isinstance(result, dict), "Bad result JSON")
        return result
    except (ValueError, UnicodeDecodeError) as exc:
        raise SaveConflict("Corrupt remote result") from exc


def verify_remote_package(root, ref, vid, req, result):
    """Do not claim already_saved/saved before reading and validating remote bytes."""
    require(result.get("status") == "saved" and result.get("request_id") == req["request_id"]
            and result.get("video_id") == vid and result.get("video_path") == req["video"]["path"]
            and result.get("source_blob_sha") == req["video"]["blob_sha"],
            "Remote result does not match approved request")
    paths = remote_files(root, ref, vid)
    require(paths, "Remote result exists without archive")
    with tempfile.TemporaryDirectory(prefix="homeku-remote-verify-") as temp:
        folder = Path(temp) / vid
        folder.mkdir()
        for item in paths:
            target = folder / Path(item).name
            target.write_bytes(git_bytes("show", f"{ref}:{item}", cwd=root))
        info = validate(folder, vid, req.get("shot_narratives"))
        require(info["shot_count"] == result["shot_count"]
                and len(info["files"]) == result["file_count"],
                "Remote result file/shot counts differ from archive")
        md = (folder / "analysis.md").read_text(encoding="utf-8")
        require(f"<!-- homeku_request_id: {req['request_id']} -->" in md,
                "Wrong request marker in remote Markdown")
    return True


def inspect_remote(root, ref, vid, req):
    """Return existing status only for a *complete* matching published package."""
    result = read_remote_result(root, ref, vid)
    paths = remote_files(root, ref, vid)
    if result is not None or paths:
        require(result is not None and bool(paths), "Partial remote archive/result")
        verify_remote_package(root, ref, vid, req, result)
        return {"status": "already_saved", "request_id": req["request_id"],
                "video_id": vid}
    archive = remote_archive(root, ref, req["video"]["path"].split("/")[-1])
    if archive is not None:
        return {"status": "already_saved", "request_id": req["request_id"],
                "video_id": archive, "archive_id": archive}
    return None


def check_remote_source_sha(root, ref, req):
    """Reject when video in moving main changed after approved snapshot."""
    path = req["video"]["path"]
    try:
        actual = git("rev-parse", f"{ref}:{path}", cwd=root)
    except subprocess.CalledProcessError as exc:
        raise SaveConflict("Approved video was removed from remote main") from exc
    require(actual == req["video"]["blob_sha"],
            "Video source Git blob SHA changed in remote main")


def check_remote_request_id_unique(root, ref, request_path, req):
    """Do not reuse a reviewed approval ID for a different video."""
    rid = req["request_id"]
    names = git("ls-tree", "-r", "--name-only", ref, "--",
                "requests/pending", "requests/results", "references", cwd=root).splitlines()
    for path in names:
        if path == request_path:
            continue
        if path.startswith(("requests/pending/", "requests/results/")) and path.endswith(".json"):
            try:
                obj = json.loads(git_bytes("show", f"{ref}:{path}", cwd=root))
            except (ValueError, UnicodeDecodeError):
                # An unrelated invalid pending request must not block other videos.
                continue
            if isinstance(obj, dict) and obj.get("request_id") == rid:
                raise SaveConflict(f"request_id reused by another video: {path}")
        elif path.startswith("references/") and path.endswith("/analysis.md"):
            # Legacy marker remains the permanent history of a saved request.
            if path.split("/")[1] == request_id_from_path(request_path):
                continue
            md = git_bytes("show", f"{ref}:{path}", cwd=root)
            if f"<!-- homeku_request_id: {rid} -->".encode() in md:
                raise SaveConflict(f"request_id already saved for another video: {path}")


def remote_request_sha(root, ref, path):
    try:
        return git("rev-parse", f"{ref}:{path}", cwd=root)
    except subprocess.CalledProcessError as exc:
        raise SaveConflict("Pending request removed from remote") from exc


def publish(root, request_path, trigger_sha, *, max_attempts=5):
    """Optimistic FFmpeg parallelism with serialized fast-forward Git publication."""
    vid = request_id_from_path(request_path)
    require(git("rev-parse", "HEAD", cwd=root) == trigger_sha,
            "Checkout must be pinned to event SHA")
    request_blob = git("rev-parse", f"{trigger_sha}:{request_path}", cwd=root)
    _, req, _, _, _ = load_request(root, request_path)
    git("fetch", "origin", "main", cwd=root)
    check_remote_case_collisions(root, "origin/main", vid)
    check_remote_source_sha(root, "origin/main", req)
    require(remote_request_sha(root, "origin/main", request_path) == request_blob,
            "Pending request changed since trigger")
    check_remote_request_id_unique(root, "origin/main", request_path, req)
    found = inspect_remote(root, "origin/main", vid, req)
    if found:
        return found
    out = render(root, request_path)
    if out["status"] == "already_saved":
        return out
    files = sorted((root / "references" / vid).iterdir())
    expected = {f.name for f in files}
    require(expected == ({"analysis.yaml", "analysis.md", "storyboard.jpg"} |
                        {f"shot-{i:02d}.jpg" for i in range(1, out["shot_count"] + 1)}),
            "Unexpected local package files")
    paths = [str(f.relative_to(root)) for f in files]
    paths.append(f"requests/results/{vid}.json")
    git("add", "--", *paths, cwd=root)
    require(set(git("diff", "--cached", "--name-only", cwd=root).splitlines()) == set(paths),
            "Staged files include unrelated changes")
    git("config", "user.name", "github-actions[bot]", cwd=root)
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com",
        cwd=root)
    git("commit", "-m", f"analysis: save {vid} from filename request", cwd=root)
    for attempt in range(1, max_attempts + 1):
        git("fetch", "origin", "main", cwd=root)
        check_remote_case_collisions(root, "origin/main", vid)
        check_remote_source_sha(root, "origin/main", req)
        require(remote_request_sha(root, "origin/main", request_path) == request_blob,
                "Remote request changed during processing")
        check_remote_request_id_unique(root, "origin/main", request_path, req)
        found = inspect_remote(root, "origin/main", vid, req)
        if found:
            return found
        try:
            git("rebase", "origin/main", cwd=root)
        except subprocess.CalledProcessError as exc:
            subprocess.run(["git", "rebase", "--abort"], cwd=root, check=False)
            raise SaveConflict("Rebase conflict; no overwrite attempted") from exc
        pushed = subprocess.run(["git", "push", "origin", "HEAD:main"],
                                cwd=root, text=True, capture_output=True)
        if pushed.returncode == 0:
            git("fetch", "origin", "main", cwd=root)
            verify_remote_package(root, "origin/main", vid, req,
                                  read_remote_result(root, "origin/main", vid))
            return out
        if attempt < max_attempts:
            time.sleep(min(attempt, 3))
    raise SaveConflict("Push failed after five safe retries; request remains pending")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--event-name", required=True, choices=("push", "workflow_dispatch"))
    parser.add_argument("--trigger-sha", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    event = json.loads(args.event.read_text(encoding="utf-8"))
    path = event_request_path(root, event, args.event_name, args.trigger_sha)
    request_id_from_path(path)
    if args.dry_run:
        print(json.dumps({"status": "preflight", "request_path": path}))
    else:
        print(json.dumps(publish(root, path, args.trigger_sha), indent=2,
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
