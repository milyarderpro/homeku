"""Local helper timings, never part of a reference snapshot."""
import json
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from .common import require

def safe_path(path):
    path = Path(path).absolute()
    require(not any(p.is_symlink() for p in (path, *path.parents)), "Symlink workspace/cache path rejected")
    return path

def event(path, stage, **values):
    if path is None:
        return
    path = safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"at": datetime.now(timezone.utc).isoformat(), "stage": stage, **values}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")

@contextmanager
def timed(path, stage, **values):
    started = time.perf_counter()
    event(path, stage, state="started", **values)
    try:
        yield
    except Exception as exc:
        event(path, stage, state="failed", seconds=round(time.perf_counter()-started, 6), error=str(exc), **values)
        raise
    else:
        event(path, stage, state="complete", seconds=round(time.perf_counter()-started, 6), **values)
