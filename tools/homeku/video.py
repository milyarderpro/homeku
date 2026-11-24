"""Native video metadata, integer-PTS selection and real frame extraction."""
from __future__ import annotations
import bisect
import io
import json
import math
import subprocess
from contextvars import ContextVar
from fractions import Fraction
from pathlib import Path
from PIL import Image
from .common import LibraryError, require

ACTIVE = ContextVar("homeku_video_cache", default=None)

def _probe_video_uncached(path: Path):
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


def _frame_times_uncached(source, *, info=None):
    """Presentation timestamps in decoder order, relative to the first video frame."""
    try:
        stream_index = (info if info is not None else probe_video(source))["video_stream_index"]
        result = subprocess.run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-select_streams", str(stream_index),
                                 "-show_frames", "-show_streams", "-show_entries", "frame=best_effort_timestamp:stream=time_base", "-of", "json", str(source)],
                                capture_output=True, text=True, check=True, timeout=120)
        data = json.loads(result.stdout)
        base = Fraction(data["streams"][0]["time_base"])
        raw = [int(f["best_effort_timestamp"]) for f in data["frames"]]
    except (OSError, subprocess.SubprocessError, KeyError, ValueError) as error:
        raise LibraryError(f"Cannot read native frame timestamps: {error}") from error
    require(raw and len(raw) <= 100_000, "Empty video or too many frames for one audit package")
    # ffprobe's *_timestamp_time string is rounded to six decimals; using it
    # can assign the first frame after a cut to the preceding shot at 30 fps.
    times = [round(float((t - raw[0]) * base), 9) for t in raw]
    require(all(a < b for a, b in zip(times, times[1:])), "Duplicate/nonmonotonic PTS needs explicit frame-index contract support")
    return times


def nearest(times, timestamp, start=0.0, end=float("inf")):
    lo, hi = bisect.bisect_left(times, start), bisect.bisect_left(times, end)
    require(lo < hi, "Shot interval has no native video frame")
    pivot = bisect.bisect_left(times, timestamp, lo, hi)
    candidates = [index for index in (pivot - 1, pivot) if lo <= index < hi]
    return min(candidates, key=lambda i: (abs(times[i] - timestamp), i))


def _extract_frame_uncached(source, index, stream_index=None):
    try:
        if stream_index is None:
            stream_index = probe_video(source)["video_stream_index"]
        result = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-protocol_whitelist", "file,pipe",
                                 "-i", str(source), "-map", f"0:{stream_index}", "-vf", f"select=eq(n\\,{index})", "-frames:v", "1", "-f", "image2pipe",
                                 "-vcodec", "mjpeg", "-q:v", "2", "-threads", "1", "-"], capture_output=True, check=True, timeout=120)
        with Image.open(io.BytesIO(result.stdout)) as picture:
            picture.load()
        return result.stdout
    except (OSError, subprocess.SubprocessError) as error:
        raise LibraryError(f"Cannot extract native frame {index}: {error}") from error


def selected_indices(times, start, end, fps=10.0, *, native=False, source_fps=None):
    """PTS-based selection with exact first/last native frames, never interpolation."""
    require(math.isfinite(start) and math.isfinite(end) and 0 <= start < end, "Invalid frame selection interval")
    lo, hi = bisect.bisect_left(times, start), bisect.bisect_left(times, end)
    require(lo < hi, "Shot interval has no native video frame")
    if not native:
        require(math.isfinite(fps) and 0 < fps <= 240, "Sampling fps must be in (0, 240]")
    if native or (source_fps is not None and source_fps <= fps):
        return list(range(lo, hi))
    require((end - start) * fps <= 100_000, "Use bounded sampling intervals")
    chosen = {nearest(times, start + i / fps, start, end) for i in range(math.ceil((end - start) * fps))
              if start + i / fps < end}
    return sorted(chosen | {lo, hi - 1})




def probe_video(path):
    cache=ACTIVE.get()
    return dict(cache.info) if cache is not None and cache.matches(path) else _probe_video_uncached(Path(path))

def frame_times(source, *, info=None):
    cache=ACTIVE.get()
    return list(cache.times) if cache is not None and cache.matches(source) else _frame_times_uncached(source, info=info)

def extract_frame(source,index,stream_index=None):
    cache=ACTIVE.get()
    if cache is not None and cache.matches(source,stream_index):
        return cache.frame(index,stream_index)
    return _extract_frame_uncached(source,index,stream_index)
