#!/usr/bin/env python3
"""Isolated technical benchmark; never ingests or claims a new visual audit."""
import argparse
import copy
import json
import sys
import time
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from homeku.audit_session import workspace
from homeku.common import dumps,read_json,require
from homeku.exporter import assemble_v2,_assemble_v2
from homeku.markdown import component
from homeku.preflight import check_inputs

def benchmark(source,audit_path,audit_info,output):
    output=workspace(output)
    require(not output.exists() or not any(output.iterdir()),"Use an empty benchmark workspace")
    output.mkdir(parents=True,exist_ok=True)
    a=read_json(audit_path);info=copy.deepcopy(audit_info)
    info.setdefault("created_at",datetime.now(timezone.utc).isoformat())
    info["method"]+="; isolated technical benchmark, no new visual inspection"
    info["ai"]={"provider":"synthetic-benchmark","model":"not-a-visual-audit","model_build":None}
    cases=[]
    def run(name,value,*,cache=False):
        path=output/(name+".json");path.write_text(dumps(value))
        start=time.perf_counter()
        if cache:
            result=assemble_v2(source,path,info,output/"candidate",purpose="fixture",cache_dir=output/"cache"/"frames")
        else:
            result=_assemble_v2(source,path,info,output/"baseline",purpose="fixture")
        manifest=read_json(Path(result["candidate"])/"manifest.json")
        row={"case":name,"seconds":round(time.perf_counter()-start,6),
             "media":{m["path"]:m["sha256"] for m in manifest["media"]},"cache":result.get("cache")}
        cases.append(row)
        return row
    # Baseline uses the unchanged registered media engine with no frame cache.
    baseline=run("uncached",a)
    cold=run("cold",a,cache=True)
    warm=run("warm",a,cache=True)
    metadata=copy.deepcopy(a);metadata["shots"][0]["phases"][0]["basis"]+=" Benchmark-only metadata correction."
    revised=run("metadata",metadata,cache=True)
    camera=copy.deepcopy(a);p=camera["shots"][0]["phases"][0]
    p["components"]+=" toward benchmark-only target"
    p["components_parsed"]=[component(c.strip()) for c in p["components"].split("+")]
    camera["shots"][0]["camera_summary"]=" → ".join(v["components"] for v in camera["shots"][0]["phases"])+"."
    run("camera",camera,cache=True)
    invalid=copy.deepcopy(info);invalid["frame_reviews"][0]["mode"]="native"
    start=time.perf_counter();bad=check_inputs(source,a,invalid,purpose="fixture")
    for row in cases:
        row["changed_media"]=[name for name,digest in row["media"].items() if baseline["media"].get(name)!=digest]
    result={"kind":"homeku.technical-benchmark","source_contract":a["schema_version"],
            "new_visual_audit":False,"cases":cases,
            "invalid_preflight":{"seconds":round(time.perf_counter()-start,6),"ok":bad["ok"],"errors":bad["errors"]},
            "parity":baseline["media"]==cold["media"]==warm["media"]==revised["media"],
            "note":"Tool durations only; synthetic candidate revisions are not reference acceptance or provider turnaround times."}
    (output/"benchmark.json").write_text(dumps(result))
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("source",type=Path);parser.add_argument("audit",type=Path)
    parser.add_argument("--audit-info",type=Path,required=True);parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(benchmark(args.source.resolve(),args.audit.resolve(),read_json(args.audit_info),args.output.resolve()),ensure_ascii=False,indent=2))
