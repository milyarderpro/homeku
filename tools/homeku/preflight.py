"""Collect independent input errors before any final JPEG is rendered."""
import copy
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from .common import LibraryError, read_json, require
from .versions import JSON_CONTRACTS, DEFAULT_REPORT, schema_name
from .video import frame_times,probe_video,nearest

ROOT=Path(__file__).resolve().parents[2]

def check_inputs(source,audit,audit_info,*,config=None,limit=100,supersedes=None,purpose="reference"):
    errors=[];seen=set()
    def add(path,group,message,action="Perbaiki field yang ditunjuk, lalu jalankan check-input/draft kembali."):
        key=(path,message)
        if key not in seen and len(errors)<limit:
            seen.add(key);errors.append({"path":path,"group":group,"message":message,"action":action})
    def capture(path,group,fn,action=None):
        try:
            return fn()
        except LibraryError as exc:
            add(path,group,str(exc),action or "Gunakan prepare/complete untuk metadata mekanis; koreksi isi pengamatan secara eksplisit.")
    if not isinstance(audit,dict) or audit.get("schema_version") not in JSON_CONTRACTS:
        add("/schema_version","schema","Unsupported JSON audit source")
        return {"ok":False,"errors":errors,"context":None}
    version=audit["schema_version"]
    def schema(value,spec,path):
        rows=sorted(Draft202012Validator(spec,format_checker=FormatChecker()).iter_errors(value),
                    key=lambda e:str(list(e.path)))
        for e in rows:
            pointer=path+"/"+"/".join(str(k).replace("~","~0").replace("/","~1") for k in e.path)
            action="Pakai enum yang didukung: "+str(e.validator_value) if e.validator=="enum" else "Lengkapi struktur sesuai template; jangan mengarang fakta."
            add(pointer,"schema",e.message,action)
        return not rows
    valid_audit=schema(audit,read_json(ROOT/"docs/contracts"/schema_name("audit",version)),"/audit")
    logs=copy.deepcopy(audit_info) if isinstance(audit_info,dict) else audit_info
    if isinstance(logs,dict):logs.setdefault("created_at",datetime.now(timezone.utc).isoformat())
    manifest_spec=read_json(ROOT/"docs/contracts"/schema_name("manifest",version))["properties"]
    valid_logs=schema(logs,manifest_spec["audit"],"/audit-info")
    valid_header=True
    for key,value in (("supersedes",supersedes),("purpose",purpose)):
        valid_header=schema(value,manifest_spec[key],"/manifest/"+key) and valid_header
    # Structural failures are cheap and independent. No metadata/decode/render yet.
    if not valid_audit or not valid_logs or not valid_header:
        return {"ok":False,"errors":errors,"context":None}
    source=Path(source)
    if not source.is_file():
        add("/source","source","Source unavailable")
        return {"ok":False,"errors":errors,"context":None}
    capture("/id","identity",lambda:require(source.stem==audit["id"] and source.suffix.casefold()==".mp4","ID must match original MP4 stem"))
    info=capture("/source","metadata",lambda:probe_video(source),"Periksa MP4 asli yang bisa dibaca ffprobe.")
    times=capture("/source","timestamps",lambda:frame_times(source)) if info is not None else None
    if info is None or times is None:
        return {"ok":False,"errors":errors,"context":None}
    from .models import validate_audit
    from .markdown import component
    from .validation import validate_audit_logs,validate_frame_reviews
    # Enumerate common independent failures; then run the canonical global checks.
    shot_ids={s["shot"] for s in audit["shots"]}
    for i,r in enumerate(audit["relations"]):
        capture(f"/relations/{i}","scope",lambda r=r:require(r["from"] in shot_ids and r["to"] in shot_ids,
             "Unknown related shot; area IDs belong in area_relations"))
    for i,s in enumerate(audit["shots"]):
        if len(s["area_ids"])==1:
            want=capture(f"/shots/{i}/interval","timeline",lambda s=s:nearest(times,(s["start_s"]+s["end_s"])/2,s["start_s"],s["end_s"]))
            capture(f"/shots/{i}/panels/1","midpoint",lambda s=s,want=want:require(
                len(s["panels"])==3 and s["panels"][1]["frame_index"]==want,
                f"Middle panel must be nearest native midpoint F{want}"),"Jalankan complete; lihat frame midpoint yang diusulkan jika belum viewed.")
        for j,p in enumerate(s["phases"]):
            capture(f"/shots/{i}/phases/{j}/components_parsed","notation",
                lambda p=p:require(p["components_parsed"]==[component(c.strip(),version) for c in p["components"].split("+")],
                                  "Parsed component metadata differs from raw notation"),"Jalankan complete; metadata parser tidak perlu diketik ulang.")
    for i,r in enumerate(logs["frame_reviews"]):
        capture(f"/audit-info/frame_reviews/{i}","frames",
            lambda r=r:validate_frame_reviews([r],audit["shots"],source,info,contract_version=version,times=times,check_coverage=False),
            "Gunakan pass session/mark-viewed yang benar; jangan membulatkan PTS atau mengarang viewed.")
    audit_ok=capture("/audit","semantics",lambda:validate_audit(audit,info["duration_s"],times))
    capture("/audit-info","coverage",lambda:validate_audit_logs(logs,audit,source,info,times=times))
    if audit_ok is not None:
        from .reporting import render_config,verify_renderer,render_report
        from .media import expected_media
        config=config or render_config(version=DEFAULT_REPORT[version])
        capture("/render","renderer",lambda:verify_renderer(config))
        capture("/analysis.md","report",lambda:render_report(audit,config))
        capture("/media","layout",lambda:list(expected_media(audit,info,config)))
    return {"ok":not errors,"errors":errors,"context":{"info":info,"times":times,"logs":logs}}

def require_inputs(source,audit,audit_info,*,config=None,**kwargs):
    result=check_inputs(source,audit,audit_info,config=config,**kwargs)
    if not result["ok"]:
        import json
        raise LibraryError("Input preflight failed before media render: "+json.dumps(result["errors"],ensure_ascii=False))
    return result["context"]
