"""Mechanical authoring helpers; observations are written by the auditor."""
import copy
import json
import re
from pathlib import Path
from .common import dumps,read_json,require
from .video_cache import FrameCache,atomic
from .audit_performance import timed,event
from .audit_session import workspace,make_shots,record_for,materialize,load_session
from .markdown import component

ROOT=Path(__file__).resolve().parents[2]

def prepare(source,cuts,output,*,resume=False,contract_version="2.5"):
    require(contract_version in {"2.4","2.5"},"Unsupported working authoring contract")
    output=workspace(output);output.mkdir(parents=True,exist_ok=True)
    session_path=output/"session.json";audit_path=output/"audit.json";info_path=output/"audit-info.json"
    if session_path.exists():
        require(resume,"Workspace already prepared; use --resume to preserve observations")
        path,session,cache=load_session(session_path)
        require(contract_version==session["contract_version"],"Session contract differs; select its original version")
        require(Path(source).resolve()==cache.source and cuts==session["cuts"],"Source/cuts differ; use a new workspace")
        records=[]
        for shot in session["shots"]:
            r=record_for(cache,shot,shot["start_s"],shot["end_s"],reason="Baseline6FPS/native dan batas shot dari cut terkonfirmasi.")
            records.append(r)
            if shot["middle"] not in r["selected_frame_indices"]:
                i=shot["middle"];end=min(shot["end_s"],cache.times[i+1] if i+1<len(cache.times) else shot["end_s"])
                records.append(record_for(cache,shot,cache.times[i],end,native=True,reason="Lihat satu frame midpoint untuk calon panel, bukan pendalaman gerak."))
        materialize(path,session,cache,records)
        return {"session":str(path),"audit":str(audit_path),"audit_info":str(info_path),
                "resumed":True,"shots":session["shots"],"passes":session["passes"],"cache":cache.stats}
    require(not any(p.exists() for p in (audit_path,info_path)),"Refusing to overwrite existing audit source")
    with timed(output/"performance.jsonl","prepare"):
        cache=FrameCache(source,output/".cache"/"frames",log=output/"performance.jsonl")
        rid=cache.source.stem
        require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}",rid) and cache.source.suffix.casefold()==".mp4","Use the canonical MP4 filename")
        session={"version":"1.0","contract_version":contract_version,"source":{"path":str(cache.source),"sha256":cache.source_hash},
                 "cuts":cuts,"shots":make_shots(cache,cuts),"passes":[]}
        # A template is an incomplete working source, not an audit claim.
        audit=read_json(ROOT/"audit/template-audit.json");audit["schema_version"]=contract_version;audit["id"]=rid
        base=copy.deepcopy(audit["shots"][0]);audit["shots"]=[]
        audit["areas"]=[] # Physical area identities are assigned after viewing.
        for row in session["shots"]:
            shot=copy.deepcopy(base);shot["shot"]=row["shot"];shot["start_s"]=row["start_s"];shot["end_s"]=row["end_s"]
            for p in shot["panels"]:
                p["id"]=f"s{row['shot'][5:]}-{p['role']}";p["shot_id"]=row["shot"]
                p["frame_index"]=row[{"start":"first","middle":"middle","end":"last"}[p["role"]]]
                p["timestamp_s"]=cache.times[p["frame_index"]];p["area_ids"]=[]
            for p in shot["overviews"]:
                p["id"]=f"s{row['shot'][5:]}-overview";p["shot_id"]=row["shot"];p["area_ids"]=[]
                p["frame_index"]=None;p["timestamp_s"]=None
            shot["area_ids"]=[]
            for d in shot["design"]:d["area_ids"]=[]
            for p in shot["phases"]:
                p["start_s"]=row["start_s"];p["end_s"]=row["end_s"];p["area_ids"]=[]
            shot["tempo_profile"][0]["start_s"]=row["start_s"];shot["tempo_profile"][0]["end_s"]=row["end_s"]
            audit["shots"].append(shot)
        atomic(audit_path,dumps(audit).encode())
        atomic(info_path,(ROOT/"audit/template-audit-info.json").read_bytes())
        atomic(session_path,dumps(session).encode())
        records=[]
        for shot in session["shots"]:
            r=record_for(cache,shot,shot["start_s"],shot["end_s"],reason="Baseline6FPS/native dan batas shot dari cut terkonfirmasi.")
            records.append(r)
            if shot["middle"] not in r["selected_frame_indices"]:
                i=shot["middle"];end=min(shot["end_s"],cache.times[i+1] if i+1<len(cache.times) else shot["end_s"])
                records.append(record_for(cache,shot,cache.times[i],end,native=True,
                                          reason="Lihat satu frame midpoint untuk calon panel, bukan pendalaman gerak."))
        materialize(session_path,session,cache,records)
    return {"session":str(session_path),"audit":str(audit_path),"audit_info":str(info_path),"resumed":False,
            "shots":session["shots"],"passes":session["passes"],"cache":cache.stats,
            "next":"Inspect sheets, fill observations/areas/Overview; declare viewed explicitly; complete then draft."}

def notation(text,version="2.4"):
    require(isinstance(text,str) and "{{" not in text and "→" not in text,"Fill one phase notation before complete")
    if version=="2.5":
        from .camera_notation import normalize
        text=normalize(text)
    clauses=[]
    for raw in text.strip().rstrip(".").split("+"):
        raw=raw.strip()
        for estimate in component(raw,version)["estimates"]:
            if not re.search(r"\([^)]*"+re.escape(estimate)+r"[^)]*\)",raw):
                raw=raw.replace(estimate,"("+estimate+")",1)
        clauses.append(raw)
    return " + ".join(clauses)

def complete(audit_path,*,session_path=None,info_path=None):
    audit_path=workspace(audit_path);original=read_json(audit_path);a=copy.deepcopy(original)
    require(a.get("schema_version") in {"2.4","2.5"},"complete only edits working source2.4/2.5; never converts old audits")
    require(session_path is not None,"Complete requires the source-bound session")
    path,session,cache=load_session(session_path)
    require(a.get("id")==cache.source.stem and [s["shot"] for s in a["shots"]]==[s["shot"] for s in session["shots"]],
            "Audit/session ID or shots differ")
    require(a["schema_version"]==session["contract_version"],"Audit/session contracts differ; never converts old audits")
    changes=[]
    def assign(obj,key,value,pointer):
        if obj.get(key)!=value:
            obj[key]=value;changes.append(pointer+"/"+key)
    with timed(path.parent/"performance.jsonl","complete"):
        for si,(s,row) in enumerate(zip(a["shots"],session["shots"])):
            label=f"/shots/{si}";assign(s,"start_s",row["start_s"],label);assign(s,"end_s",row["end_s"],label)
            for group in ("panels","overviews"):
                for j,p in enumerate(s[group]):
                    if group=="panels":
                        if p["role"]=="start":assign(p,"frame_index",row["first"],label+f"/{group}/{j}")
                        if p["role"]=="end":assign(p,"frame_index",row["last"],label+f"/{group}/{j}")
                        if p["role"]=="middle" and len(s["area_ids"])==1:assign(p,"frame_index",row["middle"],label+f"/{group}/{j}")
                    index=p["frame_index"]
                    require(type(index) is int and row["first"]<=index<=row["last"],"Select a valid native frame for every panel/Overview before complete")
                    assign(p,"timestamp_s",cache.times[index],label+f"/{group}/{j}")
                    require(p["shot_id"]==s["shot"],"Conflicting selection shot_id; fix its scope explicitly")
            for pi,p in enumerate(s["phases"]):
                loc=label+f"/phases/{pi}"
                if len(s["phases"])==1:
                    assign(p,"start_s",row["start_s"],loc);assign(p,"end_s",row["end_s"],loc)
                text=notation(p["components"],a["schema_version"]);assign(p,"components",text,loc)
                parsed=[component(c.strip(),a["schema_version"]) for c in text.split("+")]
                assign(p,"components_parsed",parsed,loc)
                observations=p["motion_observations"]
                indices=[o["component_index"] for o in observations]
                require(len(indices)==len(set(indices)) and all(0<=i<len(parsed) for i in indices),
                        "Conflicting component observation indices; fix explicitly before complete")
                if set(indices)!=set(range(len(parsed))):
                    by_index={o["component_index"]:o for o in observations}
                    filled=[by_index.get(i,{"component_index":i,"evidence":list(p["evidence"]),
                        "basis":"{{OBSERVATION_BASIS}}","estimate_basis":"{{VISUAL_ESTIMATE_BASIS}}" if parsed[i]["estimates"] else None,
                        "alternatives":None,"scale_measurement":None}) for i in range(len(parsed))]
                    assign(p,"motion_observations",filled,loc)

            if len(s["tempo_profile"])==1:
                assign(s["tempo_profile"][0],"start_s",row["start_s"],label+"/tempo_profile/0")
                assign(s["tempo_profile"][0],"end_s",row["end_s"],label+"/tempo_profile/0")
            assign(s,"camera_summary"," → ".join(p["components"] for p in s["phases"])+".",label)
        values=[p["value"] for p in a["profile"] if p["aspect"]=="style-influence" and p["state"] in {"observed","uncertain"}]
        assign(a["identity"],"influences","; ".join(values) if values else "unknown","/identity")
        info_target=workspace(info_path or path.parent/"audit-info.json")
        info=read_json(info_target)
        info["frame_reviews"]=[copy.deepcopy(p["record"]) for p in session["passes"]]
        info["reviewed_ranges"]=[{"start_s":0,"end_s":cache.info["duration_s"],"mode":"sampling"}]
        atomic(audit_path,dumps(a).encode());atomic(info_target,dumps(info).encode())
        event(path.parent/"performance.jsonl","complete-changes",paths=changes)
    return {"audit":str(audit_path),"audit_info":str(info_target),"changes":changes,"next":"check-input or draft-v2; observations remain authored by AI."}
