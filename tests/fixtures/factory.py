"""Generate tiny real MP4/JPEG files with explicitly synthetic audit data."""

from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from homeku.common import dumps, sha256
from homeku.markdown import COMPOSITION, COVERAGE, FACTS, IDENTITY, PHASES, RELATIONS, TIMELINE
from homeku.validation import CODE_ROOT, probe_video


def table(columns, rows):
    return "\n".join(["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"] +
                     ["| " + " | ".join(str(c).replace("|", "\\|") for c in row) + " |" for row in rows])


def fields(values):
    return table(("field", "value"), values.items())


def make_base_video(folder):
    path = folder / "base.mp4"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i",
                    "testsrc2=size=96x160:rate=10", "-t", "1.2", "-c:v", "mpeg4", "-q:v", "5", "-an", str(path)], check=True)
    return path


def isolated_root(folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ".homeku-fixture-root").write_text("Synthetic test root only.\n")
    (folder / "data").mkdir()
    shutil.copyfile(CODE_ROOT / "data/taxonomy.json", folder / "data/taxonomy.json")
    (folder / "incoming").mkdir()
    return folder


def make_folder(parent, rid="fixture-demo", revision=1, supersedes=None, base=None,
                source_bytes=None, layout="raised tub platform", purpose="fixture", variant=0):
    folder = parent / rid
    folder.mkdir(parents=True)
    source = folder / "source.mp4"
    if source_bytes is None:
        base = base or make_base_video(parent)
        payload = (rid + str(variant)).encode()
        source_bytes = base.read_bytes() + struct.pack(">I4s", len(payload) + 8, b"free") + payload
    source.write_bytes(source_bytes)
    metadata = {"path": f"video/{rid}.mp4", "sha256": sha256(source), **probe_video(source)}
    audit = {"method": "synthetic-fixture", "reviewed_ranges": [{"start_s": 0, "end_s": 1.2, "mode": "sampling"}],
             "limitations": "Data sintetis untuk tes kontrak; bukan audit rumah atau video referensi.",
             "created_at": "2026-11-21T00:00:00Z", "ai": {"provider": "synthetic", "model": "not-an-audit", "model_build": None}}
    media, overviews = [], []
    for index, times in enumerate(((0.0, 0.3, 0.5), (0.6, 0.9, 1.1)), 1):
        sid = f"shot-{index:02d}"
        selected = times[0] if index == 1 else times[-1]
        for kind, timestamp in (("area-overview", selected), ("start", times[0]), ("middle", times[1]), ("end", times[2])):
            path = folder / "media" / sid / f"{kind}.jpg"
            path.parent.mkdir(parents=True, exist_ok=True)
            result = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", str(timestamp), "-i", str(source),
                                     "-frames:v", "1", "-f", "image2pipe", "-vcodec", "mjpeg", "-threads", "1", "-"], capture_output=True, check=True)
            path.write_bytes(result.stdout)
            media.append({"path": path.relative_to(folder).as_posix(), "sha256": sha256(path), "kind": kind,
                          "shot_id": sid, "timestamp_s": timestamp, "width": 96, "height": 160, "crop": None, "derived_from": []})
            if kind == "area-overview":
                overviews.append(path)
    board = Image.new("RGB", (240, 384), "white")
    for index, path in enumerate(overviews):
        with Image.open(path) as picture:
            board.paste(picture, (72, index * 192 + 32))
        label = "01 bathroom/laundry 0.00s" if index == 0 else "02 kitchen 1.10s"
        ImageDraw.Draw(board).text((4, index * 192 + 6), label, fill="black")
    board_path = folder / "media/storyboard.jpg"
    board.save(board_path, "JPEG", quality=90)
    media.insert(0, {"path": "media/storyboard.jpg", "sha256": sha256(board_path), "kind": "storyboard", "shot_id": None,
                    "timestamp_s": None, "width": 240, "height": 384, "crop": None,
                    "derived_from": [path.relative_to(folder).as_posix() for path in overviews]})
    chunks = ["# Synthetic fixture — not a reference", "", "## Identitas", "", fields(dict(zip(IDENTITY, ("1.0", rid, revision, f"Synthetic fixture {rid}")))),
              "", "## Ringkasan", "", "Contoh sintetis untuk validasi pustaka. Tidak menggambarkan rumah nyata.", "", "## Cakupan", "",
              fields({key: audit[key] for key in COVERAGE}), "", "## Timeline", "",
              table(TIMELINE, [("shot-01", 0, 0.6, "bathroom; laundry", "cut", "unknown"), ("shot-02", 0.6, 1.2, "kitchen", "end", "unknown")]),
              "", "![Storyboard](media/storyboard.jpg)"]
    for index, sid in enumerate(("shot-01", "shot-02")):
        comp = dict(zip(COMPOSITION, (0 if index == 0 else 1.1, "start" if index == 0 else "end", "Cakupan area paling jelas dalam fixture.", "-",
                    "Di dekat sudut masuk area; estimasi visual fixture.", "Serong menuju subjek.", "oblique", "unknown", "unknown", "Bukaan di tepi layar.",
                    "Lapisan dekat dan jauh.", "Bagian samping area terlihat.", "Cakupan awal.", "Cakupan akhir.", "Adaptasi posisi serong serta peran awal/akhir sesuai gerakan sumber.")))
        evidence = f"[awal](media/{sid}/start.jpg); [akhir](media/{sid}/end.jpg)"
        component = "Dolly-In (~1.3×) + gentle Pan Right (~15°)" if index == 0 else "Dolly-Out (~1.3×)"
        facts = [("f-01", "space", "bathroom" if index == 0 else "kitchen", "layout", layout if index == 0 else "curved island", "observed", "medium", evidence),
                 ("f-02", "furnishing", "bathroom" if index == 0 else "kitchen", "storage", "vanity cabinet", "not-visible", "low", evidence),
                 ("f-03", "material", "wall", "finish", "unknown", "unknown", "unknown", "-")]
        chunks += ["", f'<a id="{sid}"></a>', f"## Shot {sid}", "", "### Desain dan konfigurasi", "", "Contoh uraian sintetis; fakta untuk katalog berada pada tabel berikut.",
                   "", "### Fakta", "", table(FACTS, facts), "", "### Komposisi", "", fields(comp), "", f"![Gambaran area](media/{sid}/area-overview.jpg)",
                   "", "### Kamera", "", "```text", component + ".", "```", "",
                   table(PHASES, [("phase-01", index * 0.6, (index + 1) * 0.6, component, "subjek fixture", "moderate", "constant",
                   "Angka adalah contoh sintaks fixture, bukan pengukuran kamera.", evidence, "low", "Simulasi kontrak, bukan audit gerakan.")]),
                   "", "### Ketidakpastian", "", "Seluruh isi merupakan data uji sintetis."]
    chunks += ["", "## Hubungan antarshot", "", table(RELATIONS, []), "", "## Keterbatasan", "", audit["limitations"]]
    (folder / "analysis.md").write_text("\n".join(chunks) + "\n", encoding="utf-8")
    manifest = {"contract_version": "1.0", "purpose": purpose, "id": rid, "revision": revision, "supersedes": supersedes,
                "source": metadata, "audit": audit, "media": media}
    (folder / "manifest.json").write_text(dumps(manifest), encoding="utf-8")
    return folder


def package_folder(folder, target, include_source=True):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob("*")):
            if path.is_file() and (include_source or path.name != "source.mp4"):
                info = zipfile.ZipInfo(f"{folder.name}/{path.relative_to(folder).as_posix()}", date_time=(2026, 11, 21, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
    return target


def copy_fixture(parent, rid, template, revision=1, supersedes=None, source_bytes=None, layout=None):
    folder = parent / rid
    shutil.copytree(template, folder)
    manifest = json.loads((folder / "manifest.json").read_text())
    original = manifest["id"]
    manifest.update(id=rid, revision=revision, supersedes=supersedes)
    if source_bytes is None:
        payload = rid.encode()
        source_bytes = (folder / "source.mp4").read_bytes() + struct.pack(">I4s", len(payload) + 8, b"free") + payload
    (folder / "source.mp4").write_bytes(source_bytes)
    manifest["source"].update(path=f"video/{rid}.mp4", sha256=sha256(folder / "source.mp4"))
    (folder / "manifest.json").write_text(dumps(manifest))
    text = (folder / "analysis.md").read_text().replace(original, rid).replace("| revision | 1 |", f"| revision | {revision} |")
    if layout:
        text = text.replace("raised tub platform", layout)
    (folder / "analysis.md").write_text(text)
    return folder


def modernize(folder):
    """Upgrade a synthetic fixture to 1.1; never an audit of a real reference."""
    import re
    from homeku.exporter import frame_times, selected_indices
    from homeku.markdown import PROFILE, PROFILE_ASPECTS, parse
    document = folder / "analysis.md"
    text = document.read_text()
    old = parse(text)
    profile = []
    samples = {"primary-style": ("american cattage", "uncertain"), "apparent-scale": ("tiny", "uncertain"),
               "massing": ("bentuk l", "observed"), "distinctive-features": ("fixture-feature-new-label", "observed")}
    for i, aspect in enumerate(PROFILE_ASPECTS, 1):
        value, state = samples.get(aspect, ("unknown", "unknown"))
        profile.append((f"dna-{i:02d}", aspect, value, state, "medium" if state != "unknown" else "unknown",
                        "[area](media/shot-01/area-overview.jpg)" if state != "unknown" else "-"))
    text = text.replace("| format_version | 1.0 |", "| format_version | 1.1 |")
    text = text.replace("## Cakupan", "## Profil DNA\n\nInterpretasi profil fixture; bukan audit video nyata.\n\n" +
                        table(PROFILE, profile) + "\n\n## Palet dan suasana\n\nWarna fixture untuk menguji pelestarian narasi.\n\n## Cakupan", 1)
    text = text.replace("## Timeline\n", "## Timeline\n\nDua area fixture berurutan tanpa klaim adjacency.\n", 1)
    text = text.replace("### Desain dan konfigurasi", "### Ikhtisar\n\nIkhtisar pembeda fixture untuk kartu.\n\n### Desain dan konfigurasi")
    text = text.replace("### Komposisi\n", "### Komposisi\n\nPandangan awal fixture serong; bukan default frontal.\n")
    text = text.replace("### Kamera\n", "### Kamera\n\nRitme fixture sintetis, bukan pengukuran video rumah.\n")
    text = re.sub(r"(^\|[^\n]*\n(?:\|[^\n]*(?:\n|$))+)",
                  lambda m: "<details>\n<summary>Data fixture</summary>\n\n" + m[1] + "\n</details>\n", text, flags=re.M)
    document.write_text(text)
    manifest = json.loads((folder / "manifest.json").read_text())
    manifest["contract_version"] = "1.1"
    times = frame_times(folder / "source.mp4")
    reviews = []
    for shot in old["shots"]:
        indices = selected_indices(times, shot["start_s"], shot["end_s"], source_fps=10)
        reviews.append({"shot_id": shot["shot"], "start_s": shot["start_s"], "end_s": shot["end_s"],
                        "mode": "sampling", "sampling_fps": 10, "selected_frame_indices": indices,
                        "viewed_frame_indices": indices, "reason": "Synthetic declaration for isolated tests, not an actual audit."})
    manifest["audit"]["frame_reviews"] = reviews
    (folder / "manifest.json").write_text(dumps(manifest))
    return folder


def make_v2_inputs(parent, rid="v2-fixture", *, multi=False, revision=1, base=None):
    """Synthetic declarations only: real test-pattern MP4, no claimed visual audit."""
    from homeku.video import frame_times, selected_indices
    from homeku.markdown import PROFILE_ASPECTS, component
    parent.mkdir(parents=True,exist_ok=True)
    base=base or make_base_video(parent)
    source=parent/f"{rid}.mp4"
    payload=rid.encode();source.write_bytes(base.read_bytes()+struct.pack(">I4s",len(payload)+8,b"free")+payload)
    times=frame_times(source);end=probe_video(source)["duration_s"]
    area_ids=["living-1","kitchen-1"] if multi else ["bath-1"]
    labels=["living","kitchen"] if multi else ["bathroom"]
    areas=[{"id":aid,"label":label,"functions":[label] if multi else ["bathroom","laundry"],
            "visible_intervals":[{"start_s":0 if i==0 else 0.4,"end_s":1.0 if multi and i==0 else end}]} for i,(aid,label) in enumerate(zip(area_ids,labels))]
    def selection(key,index,role,ids,label):
        return {"id":key,"shot_id":"shot-01","area_ids":ids,"frame_index":index,"timestamp_s":times[index],"role":role,"label":label,"reason":"Pilihan sintetis untuk memeriksa kontrak panel."}
    if multi:
        panels=[selection("p-start",0,"start",[area_ids[0]],"Awal living"),selection("p-reveal",4,"reveal",area_ids,"Living and kitchen reveal"),selection("p-connector",7,"connector",area_ids,"Open-plan connection"),selection("p-end",11,"end",[area_ids[1]],"Akhir kitchen")]
        overviews=[selection("overview-living",0,"overview",[area_ids[0]],"Living"),selection("overview-kitchen",11,"overview",[area_ids[1]],"Kitchen")]
        evidence="p-reveal"
    else:
        panels=[selection("p-start",0,"start",area_ids,"Awal bathroom"),selection("p-middle",6,"middle",area_ids,"Tengah bathroom"),selection("p-end",11,"end",area_ids,"Akhir bathroom")]
        overviews=[selection("overview-bath",11,"overview",area_ids,"Bathroom dan laundry")];evidence="p-middle"
    def claim(key,value,state="observed",ids=None,proof=None):
        return {"id":key,"value":value,"state":state,"confidence":"medium" if state!="unknown" else "unknown","evidence":proof if proof is not None else [evidence],"area_ids":ids or [],"basis":"Fixture kontrak sintetis.","uncertainty":"Bukan pengamatan rumah nyata."}
    profile=[]
    for i,aspect in enumerate(PROFILE_ASPECTS,1):
        value={"primary-style":"american cattage","apparent-scale":"small","massing":"l-shaped","distinctive-features":"fixture-new-shape"}.get(aspect,"unknown")
        profile.append({**claim(f"dna-{i:02d}",value,"uncertain" if value!="unknown" else "unknown",proof=[evidence] if value!="unknown" else []),"aspect":aspect})
    facts=[]
    for i,aid in enumerate(area_ids):
        proof=["p-start" if i==0 else "p-end"]
        facts.append({**claim(f"f-{i+1:02d}","curved island" if multi else "raised tub platform",ids=[aid],proof=proof),"domain":"space","subject":labels[i],"attribute":"layout"})
    facts.append({**claim("f-absence","overhead cabinet","not-visible",ids=[area_ids[0]],proof=["frame:shot-01:2"]),"domain":"furnishing","subject":"cabinet","attribute":"storage"})
    facts.append({**claim("f-new-label","belum diketahui","unknown",ids=[area_ids[0]],proof=[]),"domain":"new-domain","subject":"unknown fixture","attribute":"new-attribute"})
    notation="Dolly-In (~1.3×) + gentle Pan Right (~15°)"
    phase={"phase":"phase-01","start_s":0,"end_s":end,"components":notation,"components_parsed":[component(v.strip()) for v in notation.split("+")],"area_ids":area_ids,"focus":"Perjalanan fixture","anchor":"Jangkar sintetis","tempo":"variable","speed_change":"accelerating","basis":"Data uji, bukan estimasi video rumah.","evidence":[evidence],"confidence":"low","uncertainty":"Gerakan sintetis untuk pengujian."}
    composition={k:"Deskripsi komposisi sintetis." for k in ("camera_position","camera_direction","camera_height","camera_tilt","foreground","depth","reveal","start_composition","end_composition","motion_compatibility","focus","lighting")}
    composition.update(camera_position="Dekat bukaan pada sisi kiri area.",camera_direction="Menghadap serong ke sudut belakang.",view_angle="oblique",start_composition="Wide dari sudut pintu",end_composition="Medium wide menuju bidang kerja",lighting="Cahaya jendela dari samping dengan lampu hangat.")
    relation={"id":"area-link-01","from":area_ids[0],"to":area_ids[-1],"relation":"open-plan","description":"Living terhubung ke kitchen melalui bukaan lebar.","state":"observed","confidence":"medium","evidence":[evidence],"basis":"Hubungan sintetis untuk tes.","uncertainty":"Tidak menggambarkan rumah nyata."}
    shot={"shot":"shot-01","start_s":0,"end_s":end,"transition":"end","continuity":"Satu pengambilan tanpa cut dalam fixture.","area_ids":area_ids,
          "route":[{"area_id":area_ids[0],"start_s":0,"end_s":0.7,"connector":"awal","focus":"living"},{"area_id":area_ids[1],"start_s":0.7,"end_s":end,"connector":"bukaan open plan","focus":"kitchen"}] if multi else [],
          "area_relations":[relation] if multi else [],
          "design":[{"area_ids":[aid],"architecture":"Susunan sintetis: dinding berpanel, bukaan tinggi di samping dan lantai papan. Semua uraian ini adalah data fixture, bukan hasil melihat rumah.","furnishings":"Susunan properti uji mencakup kabinet rendah di bawah bukaan dan rak ceruk pada sisi kanan.","environment":"Pemandangan luar tidak dinyatakan pada fixture ini."} for aid in area_ids],
          "facts":facts,"composition":composition,"camera_summary":notation+".","camera_simple":"Kamera bergerak maju sambil memutar pandangan perlahan ke kanan menuju bidang kerja.","rhythm":"Sedang di awal, kemudian cepat.",
          "tempo_profile":[{"start_s":0,"end_s":0.6,"tempo":"moderate","description":"Sedang di awal"},{"start_s":0.6,"end_s":end,"tempo":"fast","description":"Cepat pada bagian akhir"}],
          "journey_dna":"Awal living → penghubung terbuka → kitchen; tempo sedang menjadi cepat." if multi else "",
          "phases":[phase],"panels":panels,"overviews":overviews,"uncertainty":"Fixture sintetis, bukan audit.","review_summary":"Kartu uji sintetis.","composition_notes":"Catatan komposisi tersimpan.","camera_notes":"Catatan kamera tersimpan."}
    audit={"schema_version":"2.0","id":rid,"revision":revision,
           "identity":{"style_names_language":"en","name":"Rumah Fixture Sintetis","primary_style":"american cattage","influences":"Pengaruh fixture dicatat tanpa klaim sejarah.","interior_style":"cozy minimalist","distinctive_features":["Kabinet ceruk","Bukaan serong"],"palette":"Putih, kayu tampak terang dan aksen gelap.","mood_environment":"Terang dan hangat dalam contoh sintetis.",
                       "style_relations":[{"from":"american cattage","to":"cottage","relation":"family","state":"uncertain","confidence":"medium","evidence":[evidence],"basis":"Hubungan eksplisit fixture, bukan alias."}]},
           "size":{"scale":"small","massing":"l-shaped","vertical":"Satu tingkat pada fixture","footprint":"Kompak","proportions":"Lebar lebih dominan daripada tinggi","floor_area_m2":{"min":60,"max":90,"basis":"Rentang sintetis untuk tes.","uncertainty":"Bukan estimasi rumah nyata."}},
           "timeline_notes":"Durasi 1,2 detik, satu shot berkelanjutan tanpa cut; data sintetis.","profile":profile,"areas":areas,"shots":[shot],"relations":[],"limitations":"Seluruh isi merupakan data uji, bukan audit video referensi."}
    indices=selected_indices(times,0,end,10,source_fps=10)
    info={"method":"synthetic-fixture","limitations":"Pernyataan pemeriksaan sintetis untuk tes validator; bukan audit visual.","created_at":"2026-11-22T00:00:00Z","ai":{"provider":"synthetic","model":"not-an-audit","model_build":None},"reviewed_ranges":[{"start_s":0,"end_s":end,"mode":"sampling"}],
          "frame_reviews":[{"shot_id":"shot-01","start_s":0,"end_s":end,"mode":"sampling","sampling_fps":10,"selected_frame_indices":list(indices),"viewed_frame_indices":list(indices),"reason":"Log sintetis untuk menguji cakupan."}]}
    path=parent/"audit.json";path.write_text(dumps(audit),encoding="utf-8")
    return source,path,info
