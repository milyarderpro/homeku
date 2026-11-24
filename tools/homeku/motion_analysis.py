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

def dependencies():
    try:
        import cv2
        import numpy
        return cv2, numpy
    except (ImportError, OSError):
        return None

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
    h,w=a.shape;center=np.array([w/2,h/2,1]);delta=matrix@center-center[:2]
    flow=(q-p)[good];position=p[good]
    zones={}
    for name,mask in [("lower",position[:,1]>.7*h),("upper",position[:,1]<.3*h)]:
        zones[name]={"count":int(mask.sum()),"dx_fraction":float(np.median(flow[mask,0])/w) if mask.sum()>=3 else None}
    difference=None
    if all(v["dx_fraction"] is not None for v in zones.values()):
        difference=zones["lower"]["dx_fraction"]-zones["upper"]["dx_fraction"]
    result.update(status="ok",scale_2d=float(math.hypot(matrix[0,0],matrix[1,0])),
                  dx_fraction=float(delta[0]/w),dy_fraction=float(delta[1]/h),
                  dx_fraction_per_s=float(delta[0]/w/dt),dy_fraction_per_s=float(delta[1]/h/dt),
                  zones=zones,lower_minus_upper_fraction=difference)
    return result

def motion_hints(session_path,shot_id,*,start=None,end=None,max_frames=32,width=320):
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
               "indices":ids,"pts":[cache.times[i] for i in ids],"width":width,
               "backend":[cv.__version__,np.__version__]}
    key=hashlib.sha256(dumps(signature).encode()).hexdigest()
    target=safe_path(path.parent/".cache"/"motion"/(key+".json"))
    digest_path=safe_path(target.with_suffix(".sha256"))
    if target.is_file() and digest_path.is_file() and sha256(target)==digest_path.read_text():
        saved=json.loads(target.read_text());saved["reused"]=True;return saved
    with timed(path.parent/"performance.jsonl","motion-hints",shot=shot_id):
        data=cache.extract_many(ids);previous=None;rows=[]
        for i in ids:
            with Image.open(io.BytesIO(data[i])) as raw:
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
                "backend":signature["backend"],"reused":False,
                "limitations":"2D hints only; upper/lower are image zones, not inferred depth. No movement verdict."}
        payload=dumps(result).encode()
        used=sum(safe_path(p).stat().st_size for p in target.parent.rglob("*") if p.is_file()) if target.parent.exists() else 0
        if used+len(payload)>32*1024*1024:
            result["cache_note"]="Motion cache quota reached; result returned without storing"
        else:
            atomic(target,payload);atomic(digest_path,sha256(target).encode())
    return result
