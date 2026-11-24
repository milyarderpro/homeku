"""Bounded, source-backed search and partial reads. No semantic inference or AI calls."""
from __future__ import annotations
from .versions import JSON_CONTRACTS
import copy
from .common import content_hash, read_json, require, sha256
from .generation import generator_fingerprint
from .models import schema_check

POSITIVE={"observed","uncertain"}


def _registry(root):
    from .engine import registry_at
    return registry_at(root)


def _generated(root,path):
    build=read_json(root/"data/build.json")
    require(isinstance(build,dict) and isinstance(build.get("outputs"),dict),"Build metadata invalid; run library.py build")
    require(build.get("generator_fingerprint")==generator_fingerprint(root),"Generated data stale; run library.py build")
    expected=build.get("projection_sha256",{}).get(path.rsplit("/",1)[-1].removesuffix(".json")) if path.startswith("data/projections/") else build["outputs"].get(path)
    require(expected is not None and (root/path).is_file() and sha256(root/path)==expected,"Generated data changed; run library.py build")
    return read_json(root/path)


def _aliases(root,group,value):
    taxonomy=read_json(root/"data/taxonomy.json")
    for key,names in taxonomy.get(group,{}).items():
        if value.casefold() in {n.casefold() for n in [key,*names]}:return key.casefold()
    return value.casefold()


def search(root,*,style=None,style_role="primary-style",style_relation=None,scale=None,area=None,configuration=None,tempo=None,movement=None,camera_qualifier=None,route=None,limit=10,offset=0,include_uncertain=True):
    require(1<=limit<=50 and offset>=0,"Search limit must be 1–50 and offset nonnegative")
    index=_generated(root,"data/search-index.json");registry=_registry(root)["references"]
    require({r["id"] for r in index["references"]}==set(registry),"Registry/index differ; run build")
    allowed=POSITIVE if include_uncertain else {"observed"}
    areas=[_aliases(root,"areas",v) for v in (area or [])]
    wanted_route=[_aliases(root,"areas",v) for v in (route or [])]
    def facet(entry,aspect,value,group):
        return any(c["aspect"]==aspect and c["state"] in allowed and c["canonical"].casefold()==_aliases(root,group,value) for c in entry["profile_facets"])
    matches=[]
    for r in index["references"]:
        require(registry[r["id"]]["revision"]==r["revision"],"Stale revision in index")
        if style:
            direct=facet(r,style_role,style,"styles")
            related=style_relation and any(c["relation"]==style_relation and c["state"] in allowed and _aliases(root,"styles",c["to"])==_aliases(root,"styles",style) and facet(r,"primary-style",c["from"],"styles") for c in r.get("style_relations",[]))
            if not direct and not related:continue
        if scale and not facet(r,"apparent-scale",scale,"scales"):continue
        selected=[]
        for s in r["shots"]:
            if areas and not set(areas)<=set(a.casefold() for a in s["areas_canonical"]):continue
            if tempo and tempo not in s["tempos"]:continue
            if movement and _aliases(root,"movements",movement) not in {v.casefold() for v in s["movements"]}:continue
            if camera_qualifier and camera_qualifier.casefold() not in {v.casefold() for v in s["camera_qualifiers"]}:continue
            if configuration and not any(f["state"] in allowed and f["value"].casefold()==configuration.casefold() for f in s["design_facets"]):continue
            if wanted_route:
                actual=[_aliases(root,"areas",v) for v in s["route"]]
                # A route filter always matches one continuous shot, never joined cuts.
                if not s["multi_area"] or not any(actual[i:i+len(wanted_route)]==wanted_route for i in range(len(actual)-len(wanted_route)+1)):continue
            selected.append(s)
        if selected:matches.append({**{k:r[k] for k in ("id","title","revision","json","profile_facets")},"shots":selected})
    return {"schema_version":"2.5","total":len(matches),"offset":offset,"limit":limit,"results":matches[offset:offset+limit],
            "next_offset":offset+limit if offset+limit<len(matches) else None}


def load_reader(root,rid):
    registry=_registry(root)["references"]
    require(rid in registry,"Reference is not active in registry")
    payload=_generated(root,f"data/projections/{rid}.json")
    schema_check(payload,"reference-reader-v2-5.schema.json")
    require(payload["reference"]["content_sha256"]==registry[rid]["content_sha256"]==content_hash(root/"references"/rid),"Reference changed outside ZIP revision")
    return payload


def read_reference(root,rid,*,part="identity",shot=None,area=None):
    payload=load_reader(root,rid);m=payload["reference"]
    context={"id":rid,"revision":m["revision"],"format_version":m["format_version"],"paths":payload["paths"]}
    if part=="full":return payload
    if part=="identity":
        return {**context,"identity":m.get("identity"),"size":m.get("size"),"profile":m.get("profile",[]),
                "camera_pattern":m.get("camera_pattern"), "profile_notes":m.get("profile_notes"),"palette_notes":m.get("palette_notes")}
    require(part in {"shot","area"},"Unknown reader part")
    require(shot is not None,"A shot ID is required for shot/area reads")
    found=next((s for s in m["shots"] if s["shot"]==shot),None)
    require(found is not None,"Unknown shot")
    selected=copy.deepcopy(found)
    if part=="area":
        require(m["format_version"] in JSON_CONTRACTS and area in found["area_ids"],"Area reads require an explicit V2 area ID in this shot")
        selected["design"]=[d for d in found["design"] if area in d["area_ids"]]
        selected["facts"]=[f for f in found["facts"] if area in f["area_ids"]]
        selected["area"]=next(a for a in m["areas"] if a["id"]==area)
        # Keep complete camera phases/route so a crop does not imply a new shot.
    keys={key for group in (selected["facts"],selected["phases"],selected.get("area_relations",[])) for c in group for key in c["evidence"]}
    if m["format_version"] in JSON_CONTRACTS:keys|={p["id"] for p in selected["panels"]+selected["overviews"]}
    else:keys|={k for k,v in payload["evidence_inventory"].items() if v.get("shot_id")==shot}
    return {**context,"shot":selected,"evidence_inventory":{k:payload["evidence_inventory"][k] for k in sorted(keys)},
            "provenance":{k:v for k,v in payload["provenance"].items() if v.get("md","").endswith("#"+shot) or v.get("source_pointer","").startswith(f"/shots/{m['shots'].index(found)}/")}}


def extract_panel(root,rid,panel,output,*,native=False):
    from .media import crop_panel
    from .video import extract_frame
    payload=load_reader(root,rid);m=payload["reference"]
    require(not output.resolve().is_relative_to(root.resolve()),"Use a temporary output outside repository")
    require(panel in payload["evidence_inventory"],"Unknown panel/evidence ID")
    item=payload["evidence_inventory"][panel]
    if native or item["path"].startswith("video/"):
        require("frame_index" in item,"Legacy panel has no native frame-index identity")
        source=root/m["source"]["path"]
        require(source.is_file() and sha256(source)==m["source"]["sha256"],"Canonical source changed")
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_bytes(extract_frame(source,item["frame_index"],m["source"]["video_stream_index"]))
        return {"output":str(output),"frame_index":item["frame_index"],"timestamp_s":item["timestamp_s"]}
    require(m["format_version"] in JSON_CONTRACTS,"Use legacy source media directly")
    return crop_panel(root/"references"/rid,{"media":m["media"]},panel,output)


def extract_shot_image(root,rid,shot,output,*,from_storyboard=False):
    """Read accepted media only; never open the MP4 for a stored collage/block."""
    import shutil
    from PIL import Image
    payload=load_reader(root,rid);model=payload["reference"]
    require(not output.resolve().is_relative_to(root.resolve()),"Use a temporary output outside repository")
    require(any(s["shot"]==shot for s in model["shots"]),"Unknown shot")
    folder=root/"references"/rid
    if from_storyboard:
        board=next((m for m in model["media"] if m["kind"]=="storyboard"),None)
        block=next((b for b in (board or {}).get("blocks",[]) if b["shot_id"]==shot),None)
        require(block is not None,"This media version has no full shot block in Storyboard")
        x,y,w,h=block["bbox"]
        with Image.open(folder/board["path"]) as picture:result=picture.crop((x,y,x+w,y+h))
        output.parent.mkdir(parents=True,exist_ok=True);result.save(output,'PNG');result.close()
        return {"output":str(output),"width":w,"height":h,"source":board["path"],"block":block}
    item=next((m for m in model["media"] if m["kind"]=="shot-collage" and m["shot_id"]==shot),None)
    require(item is not None,"This source version has no shot collage")
    output.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(folder/item["path"],output)
    return {"output":str(output),"width":item["width"],"height":item["height"],"source":item["path"]}
