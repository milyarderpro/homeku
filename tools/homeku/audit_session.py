"""Source-bound sampling passes. Extraction never declares a frame viewed."""
import bisect
import hashlib
import io
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .common import dumps, read_json, require
from . import FORMAT_VERSION
from .video import selected_indices, nearest
from .video_cache import FrameCache, atomic
from .audit_performance import safe_path, timed, event

def workspace(path):
    path=safe_path(path)
    code=Path(__file__).resolve().parents[2]
    for name in ("references","video","data","catalogs","knowledge","archive"):
        require(not path.resolve().is_relative_to((code/name).resolve()),"Use a separate audit workspace")
    require(not (path.parent/"manifest.json").exists(),"Do not edit a rendered candidate; use its source working files")
    return path

def load_session(path):
    path=workspace(path)
    value=read_json(path)
    require(isinstance(value,dict) and value.get("format_version")==FORMAT_VERSION
            and not {"contract_version", "version"}.intersection(value),
            f"Unsupported audit session; audit the MP4 in a new workspace with kit {FORMAT_VERSION}")
    require(isinstance(value.get("source"),dict) and isinstance(value["source"].get("path"),str) and isinstance(value["source"].get("sha256"),str),"Invalid session source")
    require(all(isinstance(value.get(k), list) for k in ("passes", "shots", "cuts")),
            "Invalid session cuts, passes or shots")
    cache=FrameCache(Path(value["source"]["path"]),path.parent/".cache"/"frames",log=path.parent/"performance.jsonl")
    require(value.get("runtime_signature")==cache.signature,"Session runtime differs; prepare a new workspace")
    require(cache.source_hash==value["source"]["sha256"],"Source changed; prepare a new workspace/session")
    expected=make_shots(cache,value["cuts"])
    require(value["shots"]==expected,"Session cut/PTS metadata changed; prepare a new workspace/session")
    for p in value["passes"]:
        require(p.get("id")==pass_id(value,p["record"]),"Sampling pass identity mismatch")
        r=p["record"];shot=next((s for s in expected if s["shot"]==r["shot_id"]),None)
        require(shot is not None and shot["start_s"]<=r["start_s"]<r["end_s"]<=shot["end_s"],"Pass outside shot")
        indices=selected_indices(cache.times,r["start_s"],r["end_s"],r["sampling_fps"] or 6,
                    native=r["mode"]=="frame-by-frame",source_fps=cache.info["fps"]["numerator"]/cache.info["fps"]["denominator"])
        require(indices==r["selected_frame_indices"] and isinstance(r["viewed_frame_indices"], list)
                and all(type(i) is int and i in indices for i in r["viewed_frame_indices"]),"Session selection/viewed mismatch")
    return path,value,cache

def bind_audit(audit, session, cache):
    expected = [(s["shot"], s["start_s"], s["end_s"],
                 "cut" if i + 1 < len(session["shots"]) else "end")
                for i, s in enumerate(session["shots"])]
    require(isinstance(audit, dict) and audit.get("schema_version") == FORMAT_VERSION
            and audit.get("id") == cache.source.stem,
            "Audit format or source ID differs from the session")
    require(isinstance(audit.get("shots"), list) and
            all(isinstance(shot, dict) for shot in audit["shots"]) and
            [tuple(shot.get(key) for key in ("shot", "start_s", "end_s", "transition"))
             for shot in audit["shots"]] == expected,
            "Audit shot IDs, boundaries or transitions differ from the session; prepare a new workspace")
    return audit


def _digest(value):
    return hashlib.sha256(dumps(value).encode()).hexdigest()


def camera_binding(session):
    return _digest({key: session[key] for key in ("format_version", "runtime_signature", "source", "cuts", "shots")})


def shot_camera_digests(shot):
    composition = shot.get("composition", {})
    require(isinstance(composition, dict), f"{shot['shot']}/composition: expected an object")
    production_start = {"production_start": composition["production_start"]} if "production_start" in composition else {}
    return {"camera": _digest(shot.get("camera")), "production_start": _digest(production_start)}


def checked_camera_shots(session):
    checkpoint = session.get("camera_check")
    require(isinstance(checkpoint, dict), "Run check-camera before continuing the audit")
    require(checkpoint.get("binding") == camera_binding(session),
            "Camera check source or cut mapping changed; prepare a new workspace")
    shots = checkpoint.get("shots")
    require(isinstance(shots, dict) and set(shots) == {row["shot"] for row in session["shots"]}
            and all(isinstance(value, dict) and set(value) == {"camera", "production_start"}
                    for value in shots.values()), "Invalid camera check record")
    return shots


def require_current_camera(session, audit):
    checked = checked_camera_shots(session)
    changed = [f"{shot['shot']}/{field}" for shot in audit["shots"]
               for field, digest in shot_camera_digests(shot).items() if checked[shot["shot"]][field] != digest]
    require(not changed, "Camera changed after check-camera: " + ", ".join(changed))
    return checked


def save_camera_check(path, session, shots):
    session["camera_check"] = {"binding": camera_binding(session), "shots": shots}
    atomic(path, dumps(session).encode())


def make_shots(cache,cuts):
    require(isinstance(cuts,list) and all(type(i) is int and 0<i<len(cache.times) for i in cuts) and cuts==sorted(set(cuts)),
            "Cuts must be ordered unique native indices after frame0 and before source end")
    rows=[];bounds=[0,*cuts,len(cache.times)]
    for n,(lo,hi) in enumerate(zip(bounds,bounds[1:]),1):
        start=cache.times[lo];end=cache.times[hi] if hi<len(cache.times) else cache.info["duration_s"]
        rows.append({"shot":f"shot-{n:02d}","start_s":start,"end_s":end,"first":lo,"last":hi-1,
                     "middle":nearest(cache.times,(start+end)/2,start,end)})
    return rows

def pass_id(session,record):
    selected={k:v for k,v in record.items() if k!="viewed_frame_indices" and k!="reason"}
    return hashlib.sha256(dumps({"source":session["source"]["sha256"],"cuts":session["cuts"],"selection":selected}).encode()).hexdigest()[:24]

def record_for(cache,shot,start,end,*,fps=6,native=False,reason):
    native=native or shot["end_s"]-shot["start_s"]<1 or cache.info["fps"]["numerator"]/cache.info["fps"]["denominator"]<=6
    indices=selected_indices(cache.times,start,end,fps,native=native,
                             source_fps=cache.info["fps"]["numerator"]/cache.info["fps"]["denominator"])
    return {"shot_id":shot["shot"],"start_s":start,"end_s":end,"mode":"frame-by-frame" if native else "sampling",
            "sampling_fps":None if native else fps,"selected_frame_indices":indices,"viewed_frame_indices":[],"reason":reason}

def materialize(path,session,cache,records):
    pending=[]
    for r in records:
        pid=pass_id(session,r)
        old=next((p for p in session["passes"] if p["id"]==pid),None)
        if old is None:pending.append({"id":pid,"record":r})
    if not pending:
        event(path.parent/"performance.jsonl","sampling",reused=True,new_frames=0)
        return
    frames=cache.extract_many([i for p in pending for i in p["record"]["selected_frame_indices"]])
    font=ImageFont.truetype(str(Path(__file__).resolve().parents[1]/"assets/fonts/DejaVuSans.ttf"),14)
    for p in pending:
        out=workspace(path.parent/"passes"/p["id"]);out.mkdir(parents=True,exist_ok=True)
        ids=p["record"]["selected_frame_indices"];rows=[]
        for i in ids:
            photo=out/f"frame-{i:06d}.jpg";atomic(photo,frames[i])
            rows.append({"frame_index":i,"timestamp_s":cache.times[i],"path":str(photo)})
        sheets=[]
        for offset in range(0,len(ids),24):
            chunk=ids[offset:offset+24];w=200;h=round(w*cache.info["height"]/cache.info["width"])
            canvas=Image.new("RGB",(4*w,((len(chunk)+3)//4)*(h+30)),"#202020");draw=ImageDraw.Draw(canvas)
            for n,i in enumerate(chunk):
                x=(n%4)*w;y=(n//4)*(h+30)
                with Image.open(io.BytesIO(frames[i])) as im:canvas.paste(im.resize((w,h)),(x,y+30))
                draw.text((x+4,y+7),f"F{i} · {cache.times[i]:.3f}s",font=font,fill="white")
            dest=out/f"sheet-{offset//24+1:03d}.jpg";canvas.save(dest,quality=90);canvas.close();sheets.append(str(dest))
        p["frames"]=rows;p["sheets"]=sheets;session["passes"].append(p)
    atomic(path,dumps(session).encode())

def add_pass(session_path,shot_id,*,start=None,end=None,fps=10,native=False,reason):
    path,session,cache=load_session(session_path)
    shot=next((s for s in session["shots"] if s["shot"]==shot_id),None)
    require(shot is not None,"Unknown session shot")
    start=shot["start_s"] if start is None else start;end=shot["end_s"] if end is None else end
    require(shot["start_s"]<=start<end<=shot["end_s"],"Deepening outside shot; use exact session PTS")
    require(isinstance(reason,str) and reason.strip(),"Describe the visual question for deepening")
    record=record_for(cache,shot,start,end,fps=fps,native=native,reason=reason)
    with timed(path.parent/"performance.jsonl","sample",shot=shot_id):
        materialize(path,session,cache,[record])
    return {"session":str(path),"passes":session["passes"],"cache":cache.stats}

def add_frames(session_path,indices,*,reason):
    path,session,cache=load_session(session_path)
    require(isinstance(reason,str) and reason.strip(),"Describe why these native selections are needed")
    require(isinstance(indices,list) and indices and all(type(i) is int and 0<=i<len(cache.times) for i in indices),
            "Select valid native indices")
    records=[]
    for i in sorted(set(indices)):
        shot=next(s for s in session["shots"] if s["first"]<=i<=s["last"])
        end=min(shot["end_s"],cache.times[i+1] if i+1<len(cache.times) else shot["end_s"])
        records.append(record_for(cache,shot,cache.times[i],end,native=True,reason=reason))
    with timed(path.parent/"performance.jsonl","selected-frames"):
        materialize(path,session,cache,records)
    return {"session":str(path),"passes":session["passes"],"cache":cache.stats}

def mark_viewed(session_path,pid=None,indices=None,*,all_frames=False,all_passes=False):
    path,session,cache=load_session(session_path)
    require(all_passes != (pid is not None),"Choose --all-passes or explicit --pass-id")
    ids=[p["id"] for p in session["passes"]] if all_passes else ([pid] if isinstance(pid,str) else pid)
    items=[p for p in session["passes"] if p["id"] in ids]
    require(items and len(items)==len(set(ids)),"Unknown/duplicate pass ID")
    require(all_frames != (indices is not None),"Choose explicit frame indices or --all")
    for item in items:
        selected=item["record"]["selected_frame_indices"];seen=selected if all_frames else indices
        require(isinstance(seen,list) and all(type(i) is int for i in seen) and set(seen)<=set(selected),"Viewed indices outside selected pass")
        item["record"]["viewed_frame_indices"]=sorted(set(item["record"]["viewed_frame_indices"])|set(seen))
    cache.ensure_source()
    atomic(path,dumps(session).encode())
    result=[{"pass":p["id"],"viewed":len(p["record"]["viewed_frame_indices"]),
             "selected":len(p["record"]["selected_frame_indices"]),
             "complete":p["record"]["viewed_frame_indices"]==p["record"]["selected_frame_indices"]} for p in items]
    event(path.parent/"performance.jsonl","viewed-declaration",passes=result)
    return result[0] if len(result)==1 else {"passes":result}
