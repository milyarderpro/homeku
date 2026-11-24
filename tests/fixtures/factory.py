"""Synthetic inputs and packages for integration tests in disposable roots."""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path
from homeku.audit_session import add_frames, mark_viewed
from homeku.authoring import complete, prepare
from homeku.common import dumps, read_json
from homeku.derivations import referenced_frames
from homeku.exporter import draft, export, review

ROOT = Path(__file__).resolve().parents[2]


def isolated_root(path):
    (path / "data").mkdir(parents=True)
    shutil.copyfile(ROOT / "data/taxonomy.json", path / "data/taxonomy.json")
    for name in ("incoming", "video", "references"):
        (path / name).mkdir()
    (path / ".homeku-fixture-root").write_text("Synthetic fixture only.\n")
    return path


def make_source(path, *, rate=10, duration=1.2, stamp=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-f", "lavfi", "-i", f"testsrc2=size=96x160:rate={rate}",
                    "-t", str(duration), "-c:v", "mpeg4", "-q:v", "5", "-threads", "1",
                    "-metadata", f"comment={stamp or path.stem}", str(path)],
                   check=True, capture_output=True, timeout=30)
    return path


def make_inputs(work, source, *, multi=False, revision=1, edit=None):
    result = prepare(source, [], work)
    name = "multi" if multi else "normal"
    audit = read_json(ROOT / "audit/examples" / name / "audit.json")
    audit.update(id=source.stem, revision=revision)
    if edit:
        edit(audit)
    audit_path, info_path = Path(result["audit"]), Path(result["audit_info"])
    audit_path.write_text(dumps(audit))
    info_path.write_text(dumps({"method": "Fixture", "limitations": "Synthetic fixture",
                                "ai": {"provider": "fixture", "model": "fixture", "model_build": None}}))
    available = {i for row in result["passes"] for i in row["record"]["selected_frame_indices"]}
    extra = sorted(set(referenced_frames(audit)) - available)
    if extra:
        add_frames(result["session"], extra, reason="Bukti tambahan fixture.")
    mark_viewed(result["session"], all_frames=True, all_passes=True)
    complete(audit_path, session_path=result["session"])
    return audit_path, read_json(info_path)


def make_package(work, root, rid, *, revision=1, supersedes=None, multi=False, edit=None,
                 purpose="fixture", out=None):
    source = root / "video" / (rid + ".mp4")
    if not source.is_file():
        make_source(source)
    audit, info = make_inputs(work / "authoring", source, multi=multi, revision=revision, edit=edit)
    result = draft(source, audit, info, work / "candidates", supersedes=supersedes, purpose=purpose)
    folder = Path(result["candidate"])
    cards = review(folder, work / "review.md")
    return Path(export(folder, out or root / "incoming", cards["receipt"])["package"])
