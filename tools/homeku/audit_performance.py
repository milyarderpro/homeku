"""Local helper timings, never part of a reference snapshot."""
import fcntl
import json
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .common import LibraryError, require

PHASES = ("shot-mapping", "camera", "design-media", "validation-export", "drive-delivery")
TRACKED_COMMANDS = frozenset({"check-camera", "complete", "check-input", "draft", "review", "export"})


def safe_path(path):
    path = Path(path).absolute()
    require(not any(p.is_symlink() for p in (path, *path.parents)), "Symlink workspace/cache path rejected")
    return path


def _timestamp():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def _open_log(path, mode):
    path = safe_path(path)
    if mode != "r":
        path.parent.mkdir(parents=True, exist_ok=True)
    with path.open(mode, encoding="utf-8") as stream:
        fcntl.flock(stream, fcntl.LOCK_SH if mode == "r" else fcntl.LOCK_EX)
        yield stream


def _append(stream, stage, *, at=None, **values):
    row = {"at": at or _timestamp(), "stage": stage, **values}
    stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
    stream.flush()
    return row


def _read_rows(stream):
    for i, line in enumerate(stream, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            raise LibraryError(f"Invalid performance event on line {i}") from error
        require(isinstance(row, dict) and isinstance(row.get("stage"), str), f"Invalid performance event on line {i}")
        yield row


def event(path, stage, **values):
    if path is not None:
        with _open_log(path, "a") as stream:
            return _append(stream, stage, **values)


@contextmanager
def timed(path, stage, **values):
    started = time.perf_counter()
    attempt_id = uuid4().hex
    event(path, stage, state="started", attempt_id=attempt_id, **values)
    outcome = {"state": "complete"}

    def finish():
        event(path, stage, **{**values, **outcome},
              attempt_id=attempt_id, seconds=round(time.perf_counter() - started, 6))

    try:
        yield outcome
    except Exception as exc:
        outcome.update(state="failed", error=str(exc))
        finish()
        raise
    else:
        finish()


def mark_phase(path, phase, action):
    require(phase in PHASES and action in {"start", "finish"}, "Invalid audit phase or action")
    with _open_log(path, "a+") as stream:
        stream.seek(0)
        latest = None
        for row in _read_rows(stream):
            if row["stage"] == "phase" and row.get("phase") == phase:
                latest = row
        active = latest is not None and latest["state"] == "started"
        if action == "start":
            require(not active, f"Phase already started: {phase}")
            return _append(stream, "phase", phase=phase, state="started", phase_id=uuid4().hex)
        require(active, f"No open phase to finish: {phase}")
        ended = _timestamp()
        seconds = (datetime.fromisoformat(ended) - datetime.fromisoformat(latest["at"])).total_seconds()
        require(seconds >= 0, f"Clock changed during audit phase: {phase}")
        return _append(stream, "phase", at=ended, phase=phase, state="complete", phase_id=latest["phase_id"],
                       seconds=round(seconds, 6))


def summarize(path):
    path = safe_path(path)
    phases = {phase: {} for phase in PHASES}
    attempts = {}
    untracked = 0
    if path.is_file():
        with _open_log(path, "r") as stream:
            for row in _read_rows(stream):
                stage = row["stage"]
                if stage == "phase":
                    entries, key = phases[row["phase"]], row["phase_id"]
                elif stage in TRACKED_COMMANDS and "attempt_id" in row:
                    entries, key = attempts.setdefault(stage, {}), row["attempt_id"]
                else:
                    untracked += 1
                    continue
                record = entries.setdefault(key, {})
                if row["state"] == "started":
                    record.update(started_at=row["at"], state="incomplete")
                else:
                    record.update(ended_at=row["at"], state=row["state"], seconds=row["seconds"])
                record.update({name: row[name] for name in ("shot", "snapshot_sha256", "error") if name in row})
    return {
        "phases": {phase: [{"phase_id": key, **row} for key, row in entries.items()]
                   for phase, entries in phases.items()},
        "commands": {stage: {"attempts": len(entries),
                             "runs": [{"attempt_id": key, **row} for key, row in entries.items()]}
                     for stage, entries in attempts.items()},
        "untracked_events": untracked,
    }
