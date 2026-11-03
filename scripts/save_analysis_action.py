"""Homeku v1.3: process ChatGPT-reviewed requests without AI in Actions."""
from __future__ import annotations
import argparse
import html
import json
import math
import os
import re
import shutil
import subprocess
from pathlib import Path
import yaml
from storyboard import generate_storyboard
from validate_analysis import validate, validate_narratives

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def fmt(x):
    if x is None:
        return "Tidak diketahui"
    if isinstance(x, bool):
        return "Ya" if x else "Tidak"
    if isinstance(x, list):
        return ", ".join(map(fmt, x)) if x else "—"
    return str(x).replace("_", " ").replace("|", r"\|").replace("\n", " ")

def row(a, b):
    return "| " + fmt(a) + " | " + fmt(b) + " |"

def narrative_text(text):
    """Render reviewed prose as literal text, never executable Markdown or HTML."""
    if text is None:
        return "Tidak ada detail yang tercatat."
    escaped = html.escape(" ".join(text.split()), quote=False)
    return re.sub(r'([\\`*_{}\[\]()#+!|>~-])', r'\\\1', escaped)

def markdown(d, rid, narratives=None):
    v, a, vs, st, q = (d[k] for k in ["video","architecture","visual_style","video_structure","analysis_quality"])
    b = a["building_scale"]
    area = b["estimated_floor_area_m2"]
    area_text = "Tidak diketahui" if area["min"] is None else str(area["min"]) + "–" + str(area["max"]) + " m²"
    lines = ["# " + v["id"] + " — " + fmt(a["primary_style"]).title(),
             "", "<!-- homeku_request_id: " + rid + " -->", "",
             "**Sumber data:** [analysis.yaml](analysis.yaml) · **Status:** " + fmt(q["status"]) +
             " · **Diverifikasi manusia:** " + fmt(q["human_verified"]), "",
             "## 1. Informasi Video", "", "| Informasi | Nilai |", "|---|---|"]
    for k, value in [("ID",v["id"]),("File asli",v["filename"]),("Durasi",v["duration_s"]),
                     ("Resolusi",v.get("resolution")),("FPS",v.get("fps")),
                     ("Rasio",v.get("aspect_ratio")),("Jumlah shot",v["shot_count"])]:
        lines.append(row(k,value))
    lines += ["","## 2. Storyboard Gabungan","","![Storyboard](storyboard.jpg)","",
              "## 3. Identitas Desain","","| Aspek | Hasil analisis |","|---|---|"]
    for k,value in [("Gaya utama",a["primary_style"]),("Wilayah terkait gaya desain",a.get("common_regions") or None),
                    ("Pengaruh gaya",a.get("secondary_influences")),
                    ("Ciri eksterior",a.get("exterior_features")),("Gaya interior",a.get("interior_style")),
                    ("Confidence gaya",a.get("style_confidence"))]:
        lines.append(row(k,value))
    lines += ["","## 4. Ukuran & Proporsi Bangunan","","| Aspek | Estimasi visual |","|---|---|"]
    for k,value in [("Ukuran yang terlihat",b["perceived_size"]),("Bentuk bangunan",b["building_form"]),
                    ("Skala vertikal",b["vertical_scale"]),("Tapak bangunan",b["footprint"]),
                    ("Perkiraan luas lantai",area_text),("Confidence",b["confidence"])]:
        lines.append(row(k,value))
    lines += ["","> Luas adalah perkiraan visual, bukan ukuran terukur.","",
              "## 5. Warna, Pencahayaan, dan Atmosfer","","| Warna dominan | HEX (perkiraan) |","|---|---|"]
    for item in vs.get("dominant_colors",[]):
        lines.append(row(item.get("name"),item.get("hex_approx")))
    lines += ["","| Aspek | Hasil analisis |","|---|---|"]
    for k,value in [("Pencahayaan",vs.get("lighting")),("Lingkungan",vs.get("setting")),
                    ("Musim yang tampak",vs.get("season_appearance")),("Mood",vs.get("mood"))]:
        lines.append(row(k,value))
    lines += ["","## 6. Struktur dan Timeline Video","",
              "**Jenis:** " + fmt(st.get("type")) + " · **Tempo:** " + fmt(st.get("overall_pace")) +
              " · **Transisi:** " + fmt(st.get("transition_pattern")),"",
              "| Shot | Waktu (detik) | Durasi | Area/Scene | Gerakan Kamera |","|---|---|---|---|---|"]
    for i,s in enumerate(d["shots"],1):
        lines.append("| Shot %02d | %s–%s | %.2f | %s | %s |" % (
            i,s["start_s"],s["end_s"],s["end_s"]-s["start_s"],fmt(s.get("scene")),fmt(s["camera"].get("movements"))))
    lines += ["","## 7. Analisis per Shot",""]
    for i,s in enumerate(d["shots"],1):
        lines += ["### Shot %02d — %s" % (i,fmt(s.get("scene"))),"",
                  '<img src="shot-%02d.jpg" alt="Shot %02d" width="360">' % (i,i),"",
                  "**Waktu:** %s–%s detik" % (s["start_s"],s["end_s"]),"",
                  "| Komponen | Pengamatan |","|---|---|"]
        fr,cam,details = s["framing"],s["camera"],s["visible_details"]
        for k,value in [("Fokus utama",s.get("focal_subject")),
                        ("Framing awal → akhir",fmt(fr.get("start"))+" → "+fmt(fr.get("end"))),
                        ("Sudut pandang",fr.get("view_angle")),("Gerakan kamera",cam.get("movements")),
                        ("Kecepatan kamera",cam.get("speed")),("Pencahayaan",s.get("lighting")),
                        ("Transisi keluar",s.get("transition_out"))]:
            lines.append(row(k,value))
        lines += ["","**Detail yang terlihat**",""]
        if narratives is None:
            # Backward compatibility for approved requests predating v1.3.
            lines += ["- **Arsitektur:** "+fmt(details.get("architectural")),
                      "- **Furnitur dan properti:** "+fmt(details.get("furniture_and_props")),
                      "- **Lingkungan:** "+fmt(details.get("environment")),""]
        else:
            for category, label in (("architectural", "Arsitektur"),
                                    ("furniture_and_props", "Furnitur dan properti"),
                                    ("environment", "Lingkungan")):
                lines += ["**"+label+"**", "",
                          narrative_text(narratives[s["id"]][category]["text"]), ""]
        lines += ["**Catatan pengamatan:** "+fmt(s.get("observation_note")),"",
                  "**Confidence:** Kamera "+fmt(s["confidence"].get("camera"))+
                  " · Detail visual "+fmt(s["confidence"].get("visual_details")),""]
    lines += ["## 8. Kualitas dan Ketidakpastian Analisis","",
              "| Parameter | Hasil |","|---|---|"]
    for k,value in [("Status",q.get("status")),("Verifikasi manusia",q.get("human_verified")),
                    ("Ketepatan timestamp",q.get("timestamp_precision")),
                    ("Ketidakpastian",q.get("uncertainties"))]:
        lines.append(row(k,value))
    lines += ["","**Catatan:** "+fmt(q.get("notes")),"",
              "---","","*Laporan ini diturunkan dari [analysis.yaml](analysis.yaml).*",""]
    return "\n".join(lines)

def process(root,branch):
    require(branch in ("main","actions-jpg-test"),"Unexpected branch")
    req = json.loads((root/"requests/save.json").read_text(encoding="utf-8"))
    if req.get("status")=="idle":
        return {"status":"idle"}
    require(req.get("schema_version")=="1.0" and req.get("status")=="approved","Invalid request state")
    rid=req.get("request_id")
    require(isinstance(rid,str) and bool(re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{7,79}",rid)),"Invalid request_id")
    src=req.get("video") or {}
    path,sha=src.get("path"),src.get("blob_sha")
    require(isinstance(path,str) and bool(re.fullmatch(r"video/[A-Za-z0-9][A-Za-z0-9_.-]*\.mp4",path)),"Invalid video path")
    require(isinstance(sha,str) and bool(re.fullmatch(r"[0-9a-f]{40}",sha)),"Invalid video blob_sha")
    for md in (root/"references").glob("VID-*/analysis.md"):
        if "<!-- homeku_request_id: "+rid+" -->" in md.read_text(encoding="utf-8"):
            return {"status":"already_saved","video_id":md.parent.name,"request_id":rid}
    source=root/path
    require(source.is_file() and source.stat().st_size>0,"MP4 missing in video/: "+path)
    require(git("rev-parse","HEAD:"+path)==sha,"Video Git blob SHA mismatch")
    raw=req.get("analysis_yaml")
    require(isinstance(raw,str) and len(raw)>100,"Missing analysis_yaml")
    data=yaml.safe_load(raw)
    require(isinstance(data,dict) and str(data.get("schema_version"))=="2.1","Invalid YAML schema")
    v,shots=data["video"],data["shots"]
    times=req.get("keyframe_times_s")
    require(v["filename"]==source.name,"Wrong analysis filename")
    require(isinstance(shots,list) and 1<=len(shots)<=99 and v["shot_count"]==len(shots),"Invalid shots")
    require(isinstance(times,list) and len(times)==len(shots),"Wrong timestamp count")
    for i,(s,t) in enumerate(zip(shots,times),1):
        require(isinstance(t,(int,float)) and not isinstance(t,bool) and math.isfinite(t),"Invalid keyframe time")
        require(s["id"]=="shot-%02d"%i and float(s["start_s"])<=t<float(s["end_s"]),"Keyframe outside shot")
    narratives = req["shot_narratives"] if "shot_narratives" in req else None
    if "shot_narratives" in req:
        validate_narratives(data, narratives)
    existing={int(x.name[4:]) for x in (root/"references").glob("VID-*") if x.is_dir() and re.fullmatch(r"VID-\d{3,}",x.name)}
    number=1
    while number in existing:
        number+=1
    vid="VID-%03d"%number
    dest=root/"references"/vid
    require(not dest.exists(),"Folder already exists")
    data["video"]["id"]=vid
    dest.mkdir(parents=True)
    try:
        frames=[]
        for i,(s,t) in enumerate(zip(shots,times),1):
            s["keyframe"]="references/%s/shot-%02d.jpg"%(vid,i)
            jpg=dest/("shot-%02d.jpg"%i)
            subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",
                            "-ss","%.3f"%t,"-i",str(source),"-frames:v","1","-q:v","2",str(jpg)],check=True)
            require(jpg.is_file() and jpg.stat().st_size>0,"FFmpeg failed for "+jpg.name)
            frames.append(jpg)
        generate_storyboard(frames, dest/"storyboard.jpg", video=data["video"], architecture=data["architecture"], shots=shots)
        (dest/"analysis.yaml").write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding="utf-8")
        (dest/"analysis.md").write_text(markdown(data,rid,narratives),encoding="utf-8")
        info=validate(dest,vid)
        result={"status":"saved","request_id":rid,"video_id":vid,"video_path":path,
                "source_blob_sha":sha,"shot_count":len(shots),"file_count":len(info["files"]),
                "run_id":os.getenv("GITHUB_RUN_ID")}
        (root/"requests/result.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        return result
    except Exception:
        shutil.rmtree(dest,ignore_errors=True)
        raise

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=Path.cwd())
    parser.add_argument("--branch",required=True)
    args=parser.parse_args()
    print(json.dumps(process(args.root.resolve(),args.branch),indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
