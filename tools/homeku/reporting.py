"""Human reports from authored data. Registered renderers are immutable versions."""
from __future__ import annotations
import re
from pathlib import Path
from .common import cell, require, sha256
from .media import FONT, BOLD_FONT, require_english_style_names, panel_label

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = {version: ROOT / f"tools/assets/templates/analysis-{version}.md" for version in ("2.0.0", "2.1.0", "2.1.1", "2.1.2")}


def render_config(*, quality=91, scale=1.0, columns=4, version="2.1.2"):
    require(version in TEMPLATES, "Unsupported report version")
    config = {"report": version, "template_sha256": sha256(TEMPLATES[version]), "media": version,
              "font_sha256": sha256(FONT), "jpeg_quality": quality, "panel_scale": scale, "columns": columns}
    if version in {"2.1.0", "2.1.1", "2.1.2"}:
        config["bold_font_sha256"] = sha256(BOLD_FONT)
    return config


def verify_renderer(config):
    version = config["report"]
    require(version in TEMPLATES and config["media"] == version, "Unsupported renderer/media version pair")
    require(config["template_sha256"] == sha256(TEMPLATES[version]), "Versioned report template hash mismatch")
    require(config["font_sha256"] == sha256(FONT), "Versioned bundled font hash mismatch")
    if version in {"2.1.0", "2.1.1", "2.1.2"}:
        require(config.get("bold_font_sha256") == sha256(BOLD_FONT), "Versioned bundled bold font hash mismatch")


def number(n):
    return f"{n:.3f}".rstrip("0").rstrip(".")


def table(columns, rows):
    return "\n".join(["| "+" | ".join(columns)+" |", "| "+" | ".join("---" for _ in columns)+" |"]+
                      ["| "+" | ".join(cell(v) for v in row)+" |" for row in rows])


def render_report(a, config):
    verify_renderer(config)
    if config["report"] in {"2.1.0", "2.1.1", "2.1.2"}:
        require_english_style_names(a)
    # The registered copy of the approved template pins headings and card groups.
    template=TEMPLATES[config["report"]].read_text(encoding="utf-8")
    headings=re.findall(r"^## [1-5]\. .+$",template,re.M)
    groups=re.findall(r"^#### [ABC]\. .+$",template,re.M)
    require(len(headings)==5 and len(groups)==3,"Invalid registered report template")
    i,z=a["identity"],a["size"];labels={v["id"]:v["label"] for v in a["areas"]}
    def names(ids):return " / ".join(labels[k] for k in ids)
    parts=[f"# {a['id']} — {i['name']}", '<a id="profil-dna"></a>', headings[0],
      "\n".join(f"- **{title}:** {value}" for title,value in [
      ("Nama desain rumah",i["name"]),("Gaya utama",i["primary_style"]),("Pengaruh gaya",i["influences"]),
      ("Gaya interior",i["interior_style"]),("Ciri pengenal","; ".join(i["distinctive_features"])),
      ("Palet utama",i["palette"]),("Suasana dan lingkungan",i["mood_environment"])]),headings[1],
      table(["Aspek","Estimasi visual"],[("Ukuran rumah",z["scale"]),("Bentuk bangunan",z["massing"]),
       ("Skala vertikal",z["vertical"]),("Tapak bangunan",z["footprint"]),("Proporsi utama",z["proportions"]),
       ("Perkiraan luas lantai",f"**{number(z['floor_area_m2']['min'])}–{number(z['floor_area_m2']['max'])} m²**")]),
      headings[2],a["timeline_notes"],
      table(["Shot","Waktu (detik)","Durasi","Area/Scene","Gerakan singkat","Ritme"],
        [(s["shot"][5:],f"{number(s['start_s'])}–{number(s['end_s'])}",f"{number(s['end_s']-s['start_s'])} detik",names(s["area_ids"]),s["camera_simple"],s["rhythm"]) for s in a["shots"]]),
      headings[3],"![Storyboard overview seluruh area](media/storyboard.jpg)",headings[4]]
    for index,s in enumerate(a["shots"]):
        sid=s["shot"];multi=len(s["area_ids"])>1
        if index:parts.append("---")
        parts += [f'<a id="{sid}"></a>',f"### Shot {sid[5:]} — {names(s['area_ids'])} · {number(s['end_s']-s['start_s'])} detik"]
        if multi:parts.append("**Jenis shot:** berkelanjutan, multi area, tanpa cut.")
        parts += [f"![Kolase Shot {sid[5:]}](media/{sid}.jpg)","**Urutan panel:** "+panel_sequence(s, config)+".",groups[0]]
        for title,key in [("Arsitektur","architecture"),("Furnitur dan properti","furnishings"),("Lingkungan","environment")]:
            parts.append(f"**{title}**")
            for d in s["design"]:
                prefix=f"**{names(d['area_ids'])}.** " if multi else ""
                parts.append(prefix+d[key])
        parts.append(groups[1]);c=s["composition"]
        rows=[]
        if multi:
            rows += [("Area yang terlihat",names(s["area_ids"])),("Rute kamera"," → ".join(labels[r["area_id"]]+f" ({number(r['start_s'])}–{number(r['end_s'])} s; {r['connector']})" for r in s["route"]) or "Kamera tidak berpindah antararea.")]
        rows += [("Fokus utama",c["focus"]),("Posisi kamera awal",c["camera_position"]+"; "+c["camera_direction"]+"; "+c["view_angle"]),
                 ("Framing awal → akhir",c["start_composition"]+" → "+c["end_composition"]),("Pencahayaan",c["lighting"])]
        parts.append(table(["Aspek","Penjelasan"],rows))
        if multi:
            parts.append("**Hubungan antararea**")
            parts.append(table(["Aspek","Penjelasan"],[("Penghubung area","; ".join(r["description"] for r in s["area_relations"]) or "Hubungan belum dipastikan."),
              ("Peralihan yang terlihat","; ".join(f"{labels[k]}: "+", ".join(f"{number(v['start_s'])}–{number(v['end_s'])} s" for v in [{"start_s":max(v["start_s"],s["start_s"]),"end_s":min(v["end_s"],s["end_s"])} for v in next(a for a in a["areas"] if a["id"]==k)["visible_intervals"] if v["start_s"]<s["end_s"] and v["end_s"]>s["start_s"]]) for k in s["area_ids"])),
              ("Kesinambungan ruang",s["continuity"])]))
        parts += [groups[2],"**Bahasa sederhana**",s["camera_simple"],"**Ritme:** "+s["rhythm"]]
        if s["journey_dna"]:parts.append("**DNA perjalanan:** "+s["journey_dna"])
        if multi or len(s["phases"])>1:
            parts += ["**Timeline gerakan**","Semua waktu dihitung dari awal video.",
              table(["Waktu (detik)","Area dan fokus","Gerakan Kamera","Ritme"],
              [(f"{number(p['start_s'])}–{number(p['end_s'])}",names(p["area_ids"])+" · "+p["focus"],p["components"],
                "; ".join(t["description"] for t in s["tempo_profile"] if t["start_s"]<p["end_s"] and t["end_s"]>p["start_s"])) for p in s["phases"]])]
        parts += ["**Notasi teknis**","```text\n"+s["camera_summary"]+"\n```"]
    return "\n\n".join(parts)+"\n"


def review_report(audit, config, media_prefix=None):
    text=render_report(audit,config)
    if media_prefix:
        text=re.sub(r"\]\((media/[^)]+)\)",lambda m:f"]({media_prefix}/{m[1]})",text)
    return text


def panel_sequence(shot, config):
    if config["report"] == "2.0.0":
        return " → ".join(f"{p['label']} ({number(p['timestamp_s'])} s)" for p in shot["panels"])
    return " → ".join(f"{panel_label(p, len(shot['area_ids']) > 1)} · {p['timestamp_s']:.2f}s" for p in shot["panels"])
