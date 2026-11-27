"""Measure image scale between two positions of an auditor-selected anchor."""
import hashlib
import io
import math

from PIL import Image, ImageDraw

from .audit_session import load_session, workspace
from .common import dumps, require
from .motion_analysis import require_backend, track_points
from .video_cache import atomic

MAX_TRACK_FRAMES = 64


def anchor_points(coordinates, size):
    width, height = size
    require(len(coordinates) == 4 and all(math.isfinite(value) for value in coordinates),
            "Provide two finite native pixel points as X1 Y1 X2 Y2")
    a = tuple(coordinates[:2])
    b = tuple(coordinates[2:])
    require(all(0 <= x < width and 0 <= y < height for x, y in (a, b)),
            "Anchor point outside native frame")
    require(a != b, "Anchor points must have positive length")
    return a, b


def propose_points(cache, first, last, points, native_size):
    if last - first + 1 > MAX_TRACK_FRAMES:
        return None, "Tracking spans up to 64 consecutive native frames. Supply manual end points or shorten the interval."

    cv, np = backend = require_backend()
    frames = cache.extract_many(range(first, last + 1))
    previous = None
    tracked = None
    width, height = native_size
    scale = min(1, 640 / max(width, height))
    size = max(1, round(width * scale)), max(1, round(height * scale))
    factors = np.array((size[0] / width, size[1] / height), dtype=np.float32)
    points = np.asarray(points, dtype=np.float32).reshape(2, 1, 2) * factors
    for index in range(first, last + 1):
        with Image.open(io.BytesIO(frames[index])) as image:
            require(image.size == native_size, "Native frame dimensions changed in the tracking interval")
            with image.convert("L").resize(size) as reduced:
                current = np.asarray(reduced)
        if previous is not None:
            try:
                tracked = track_points(previous, current, points, backend, max_level=1)
            except cv.error:
                tracked = None
            if tracked is None or not tracked[1].all() or (tracked[0] < 0).any() or (tracked[0] >= size).any():
                return None, f"Tracking could not verify both points at F{index} ({cache.times[index]:.3f}s). Supply manual end points."
            points = tracked[0]
        previous = current
    return tuple(float(value) for value in (points / factors).ravel()), None


def anchor_preview(image, points, path):
    with image.convert("RGB") as view:
        width, height = view.size
        view.thumbnail((1000, 1000))
        if points is not None:
            mapped = [(x * view.width / width, y * view.height / height) for x, y in points]
            draw = ImageDraw.Draw(view)
            draw.line(mapped, fill="#00ffff", width=3)
            for x, y in mapped:
                draw.ellipse((x - 5, y - 5, x + 5, y + 5), outline="white", fill="#006b73", width=2)
        with io.BytesIO() as buffer:
            view.save(buffer, format="JPEG", quality=90)
            atomic(path, buffer.getvalue())


def measure_anchor(session_path, shot_id, frames, start_points, end_points, output):
    _, session, cache = load_session(session_path)
    first, last = frames
    shot = next((item for item in session["shots"] if item["shot"] == shot_id), None)
    require(shot is not None, "Unknown session shot")
    require(shot["first"] <= first < last <= shot["last"],
            "Use two chronological native frames in the same shot")
    manual = end_points is not None
    with (Image.open(io.BytesIO(cache.frame(first))) as initial_image,
          Image.open(io.BytesIO(cache.frame(last))) as final_image):
        initial = anchor_points(start_points, initial_image.size)
        reason = None
        if not manual:
            end_points, reason = propose_points(cache, first, last, initial, initial_image.size)
        final = anchor_points(end_points, final_image.size) if end_points is not None else None
        identity = {"source_sha256": cache.source_hash, "runtime_signature": cache.signature,
                    "shot": shot_id, "frames": frames, "start_points": initial, "end_points": final,
                    "manual": manual, "reason": reason}
        key = hashlib.sha256(dumps(identity).encode()).hexdigest()[:24]
        report = workspace(output / f"{shot_id}-{first:06d}-{last:06d}-{key}.json")
        result = {"shot": shot_id, "source_sha256": cache.source_hash, "frames": [], "measurement": str(report)}
        cache.ensure_source()
        for label, index, image, points in (("start", first, initial_image, initial), ("end", last, final_image, final)):
            path = report.with_name(f"{report.stem}-{label}.jpg")
            anchor_preview(image, points, path)
            result["frames"].append({"frame_index": index, "pts_s": cache.times[index], "points_px": points,
                                     "length_px": math.dist(*points) if points else None, "preview": str(path)})
    if manual:
        before, after = (row["length_px"] for row in result["frames"])
        ratio = max(before, after) / min(before, after)
        direction = "enlarging" if after > before else "shrinking" if after < before else "unchanged"
        result.update(status="measured", direction=direction, ratio=ratio, estimate=f"~{ratio:.3g}×")
    elif reason is not None:
        result.update(status="insufficient", reason=reason)
    else:
        result.update(status="proposed", next="Inspect both previews and confirm or correct --end-points.")
    atomic(report, dumps(result).encode())
    return result
