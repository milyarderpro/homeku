"""Optional bounded 2D statistics. Never labels physical camera motion or edits audit."""
import hashlib
import io
import json
import math
from pathlib import Path
from PIL import Image
from .common import dumps, require, sha256
from .audit_performance import timed,safe_path
from .audit_session import load_session
from .video_cache import atomic
from .render_assets import MAX_PIXELS

MOTION_CACHE_LIMIT = 32 * 1024 * 1024

def dependencies():
    try:
        import cv2
        import numpy
        return cv2, numpy
    except (ImportError, OSError):
        return None

def compose(first, second):
    """Combine two 2×3 affine matrices in temporal order."""
    return [[sum(second[row][k] * first[k][column] for k in range(2)) +
             (second[row][2] if column == 2 else 0)
             for column in range(3)] for row in range(2)]


def transform_metrics(matrix, size):
    """Describe a 2D transform on a shared image coordinate system."""
    width, height = size
    x, y = width / 2, height / 2
    shift_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] - x
    shift_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] - y
    return {"scale_2d": math.hypot(matrix[0][0], matrix[1][0]),
            "rotation_degrees_2d": math.degrees(math.atan2(matrix[1][0], matrix[0][0])),
            "dx_fraction": shift_x / width, "dy_fraction": shift_y / height}


def macro_transform(rows):
    require(rows and all(row["status"] == "ok" for row in rows),
            "A macro transform needs a contiguous sequence of valid intervals")
    matrix = [[1, 0, 0], [0, 1, 0]]
    size = rows[0]["image_size"]
    for row in rows:
        require(row["image_size"] == size, "Transforms must share image coordinates")
        matrix = compose(matrix, row["matrix"])
    return {"matrix": matrix, "image_size": size, **transform_metrics(matrix, size)}


def interval(first, second, dt, *, backend=None):
    require(math.isfinite(dt) and dt>0, "Motion interval needs positive native PTS delta")
    backend=backend or dependencies()
    if backend is None:
        return {"status":"unavailable","reason":"Optional OpenCV/NumPy unavailable; continue visual inspection"}
    cv,np=backend
    a=np.asarray(first.convert("L"));b=np.asarray(second.convert("L"))
    require(a.shape==b.shape and a.size>0,"Motion pictures must share dimensions")
    result={"status":"insufficient","dt_s":dt,"tracked":0,"inliers":0}
    pts=cv.goodFeaturesToTrack(a,maxCorners=250,qualityLevel=.01,minDistance=6)
    if pts is None or len(pts)<8:return result
    following,status,_=cv.calcOpticalFlowPyrLK(a,b,pts,None,winSize=(21,21),maxLevel=3)
    if following is None or status is None:return result
    backwards,backstatus,_=cv.calcOpticalFlowPyrLK(b,a,following,None,winSize=(21,21),maxLevel=3)
    if backwards is None or backstatus is None:return result
    mask=(status.ravel()==1)&(backstatus.ravel()==1)&np.isfinite(following).all(axis=(1,2))
    mask&=np.max(np.abs(pts-backwards),axis=(1,2))<1.5
    p=pts[mask].reshape(-1,2);q=following[mask].reshape(-1,2)
    result["tracked"]=len(p)
    if len(p)<8:return result
    matrix,inliers=cv.estimateAffinePartial2D(p,q,maxIters=300,confidence=.95,refineIters=5)
    if matrix is None or inliers is None or not np.isfinite(matrix).all():return result
    good=inliers.ravel().astype(bool);result["inliers"]=int(good.sum())
    if result["inliers"]<8 or result["inliers"]/len(p)<.4:return result
    h, w = a.shape
    matrix = matrix.tolist()
    metrics = transform_metrics(matrix, (w, h))
    if metrics["scale_2d"] <= 0:
        return result
    flow=(q-p)[good];position=p[good]
    zones={}
    for name,mask in [("lower",position[:,1]>.7*h),("upper",position[:,1]<.3*h)]:
        zones[name]={"count":int(mask.sum()),"dx_fraction":float(np.median(flow[mask,0])/w) if mask.sum()>=3 else None}
    difference=None
    if all(v["dx_fraction"] is not None for v in zones.values()):
        difference=zones["lower"]["dx_fraction"]-zones["upper"]["dx_fraction"]
    result.update(status="ok", matrix=matrix, image_size=[w, h], **metrics,
                  dx_fraction_per_s=metrics["dx_fraction"] / dt,
                  dy_fraction_per_s=metrics["dy_fraction"] / dt,
                  zones=zones, lower_minus_upper_fraction=difference)
    return result

def summarize(rows, start, end):
    """Report tracking coverage within the PTS interval, preserving gaps."""
    first_pts, last_pts = rows[0]["start_s"], rows[-1]["end_s"]
    require(start <= first_pts < last_pts <= end, "Motion rows outside requested PTS")
    gaps, runs, current = [], [], []
    if first_pts > start:
        gaps.append({"start_s": start, "end_s": first_pts, "reason": "No sampled interval"})
    for row in rows:
        if row["status"] == "ok":
            current.append(row)
            continue
        if current:
            runs.append(current)
            current = []
        gaps.append({"start_s": row["start_s"], "end_s": row["end_s"],
                     "reason": row.get("reason", "Insufficient tracking")})
    if current:
        runs.append(current)
    if last_pts < end:
        gaps.append({"start_s": last_pts, "end_s": end, "reason": "No sampled interval"})

    ranges = []
    for run in runs:
        transform = macro_transform(run)
        ranges.append({"start_s": run[0]["start_s"], "end_s": run[-1]["end_s"],
                       **{k: v for k, v in transform.items() if k not in {"matrix", "image_size"}}})
    valid = [row for row in rows if row["status"] == "ok"]
    valid_s = sum(row["end_s"] - row["start_s"] for row in valid)
    span = last_pts - first_pts
    trends = []
    for i, label in enumerate(("early", "middle", "late")):
        left, right = first_pts + i * span / 3, first_pts + (i + 1) * span / 3
        duration = translation = scale = rotation = 0.0
        for row in valid:
            overlap = min(row["end_s"], right) - max(row["start_s"], left)
            if overlap <= 0:
                continue
            weight = overlap / (row["end_s"] - row["start_s"])
            metrics = transform_metrics(row["matrix"], row["image_size"])
            duration += overlap
            translation += weight * math.hypot(metrics["dx_fraction"], metrics["dy_fraction"])
            scale += weight * math.log(metrics["scale_2d"])
            rotation += weight * metrics["rotation_degrees_2d"]
        trends.append({"segment": label, "start_s": left, "end_s": right,
                       "covered_fraction": duration / (right - left),
                       "translation_fraction_per_s": translation / duration if duration else None,
                       "scale_log_change_per_s": scale / duration if duration else None,
                       "rotation_degrees_2d_per_s": rotation / duration if duration else None})
    total = ranges[0] if len(valid) == len(rows) else None
    return {"requested": {"start_s": start, "end_s": end},
            "sampled": {"start_s": first_pts, "end_s": last_pts},
            "coverage": {"valid_duration_s": valid_s, "fraction_sampled": valid_s / span,
                         "fraction_requested": valid_s / (end - start),
                         "valid_intervals": len(valid), "sampled_intervals": len(rows)},
            "gaps": gaps, "ranges": ranges, "total": total, "trends": trends}


def motion_hints(session_path,shot_id,*,start=None,end=None,max_frames=32,width=320,details=False):
    require(type(max_frames) is int and 2<=max_frames<=64 and type(width) is int and 80<=width<=640,
            "Use 2–64 frames and analysis width 80–640")
    path,session,cache=load_session(session_path)
    shot=next((s for s in session["shots"] if s["shot"]==shot_id),None)
    require(shot is not None,"Unknown motion shot")
    start=shot["start_s"] if start is None else start;end=shot["end_s"] if end is None else end
    require(shot["start_s"]<=start<end<=shot["end_s"],"Motion interval outside shot")
    backend=dependencies()
    if backend is None:
        return {"status":"unavailable","reason":"Optional OpenCV/NumPy unavailable; continue visual inspection","reused":False}
    cv,np=backend
    ids=sorted({i for p in session["passes"] if p["record"]["shot_id"]==shot_id
                for i in p["record"]["selected_frame_indices"] if start<=cache.times[i]<end})
    require(len(ids)>=2,"Prepare at least two frames in this interval")
    if len(ids)>max_frames:
        ids=[ids[round(n*(len(ids)-1)/(max_frames-1))] for n in range(max_frames)]
    signature={"source":cache.source_hash,"cache":cache.signature,"helper":sha256(Path(__file__)),
               "indices":ids,"pts":[cache.times[i] for i in ids],"width":width, "bounds":[start,end],
               "backend":[cv.__version__,np.__version__]}
    key=hashlib.sha256(dumps(signature).encode()).hexdigest()
    target=safe_path(path.parent/".cache"/"motion"/(key+".json"))
    digest_path=safe_path(target.with_suffix(".sha256"))
    def present(saved):
        rows = saved["intervals"]
        result = dict(saved)
        result["problem_intervals"] = [
            {key: row[key] for key in ("first", "last", "start_s", "end_s", "status", "reason")
             if key in row} for row in rows if row["status"] != "ok"]
        if not details:
            result.pop("intervals")
        return result

    if (target.is_file() and target.stat().st_size <= MOTION_CACHE_LIMIT and digest_path.is_file()
            and digest_path.stat().st_size == 64 and sha256(target) == digest_path.read_text()):
        saved = json.loads(target.read_text())
        saved["reused"] = True
        return present(saved)
    with timed(path.parent/"performance.jsonl","motion-hints",shot=shot_id):
        data=cache.extract_many(ids);previous=None;rows=[]
        for i in ids:
            with Image.open(io.BytesIO(data[i])) as raw:
                require(raw.width * raw.height <= MAX_PIXELS, "Source frame exceeds helper pixel budget")
                im=raw.convert("RGB");im.thumbnail((width,width*4))
            if previous:
                j,first=previous
                try:row=interval(first,im,cache.times[i]-cache.times[j],backend=backend)
                except cv.error:
                    row={"status":"insufficient","reason":"Tracking failed; inspect interval visually"}
                rows.append({"first":j,"last":i,"start_s":cache.times[j],"end_s":cache.times[i],**row})
                first.close()
            previous=(i,im)
        previous[1].close()
        result={"status":"ok" if any(r["status"]=="ok" for r in rows) else "insufficient",
                "source_sha256":cache.source_hash,"shot":shot_id,"indices":ids,"intervals":rows,
                "summary": summarize(rows, start, end),
                "backend":signature["backend"],"reused":False,
                "limitations":"2D hints only; upper/lower are image zones, not inferred depth. No movement verdict."}
        payload=dumps(result).encode()
        used=sum(safe_path(p).stat().st_size for p in target.parent.rglob("*") if p.is_file()) if target.parent.exists() else 0
        if used + len(payload) + 64 > MOTION_CACHE_LIMIT:
            result["cache_note"]="Motion cache quota reached; result returned without storing"
        else:
            atomic(target,payload);atomic(digest_path,sha256(target).encode())
    return present(result)
