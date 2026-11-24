"""Render the human report directly from the compact audit and native PTS."""
import re
from . import FORMAT_VERSION
from .camera_pattern import video_pattern
from .common import require
from .derivations import camera_summary, phase_tempo_text, selections, tempo_segments
from .render_assets import TEMPLATE, claim_text, number, require_english_style_names
from .report_validation import display, lines, table, validate_report


def render_report(audit, frames):
    require(audit.get("schema_version") == FORMAT_VERSION, "Unsupported audit format for report")
    require_english_style_names(audit)
    template = TEMPLATE.read_text(encoding="utf-8")
    headings = re.findall(r"^## [1-6]\. .+$", template, re.M)
    groups = re.findall(r"^#### \*\*[ABC]\. .+\*\*$", template, re.M)
    require(len(headings) == 6 and len(groups) == 3, "Invalid active report template")
    design = audit["design"]
    styles, size = design["styles"], design["size"]
    areas = {area["id"]: area for area in audit["areas"]}
    labels = {key: display(area["label"]) for key, area in areas.items()}
    shots = audit["shots"]

    def names(ids):
        return " / ".join(labels[key] for key in ids)

    def feature(*aspects):
        return "; ".join(display(claim_text(claim)) for claim in design["features"]
                         if claim["aspect"] in aspects) or "—"

    def style_list(claims):
        return "; ".join(display(claim_text(claim)) for claim in claims) or "—"

    area = size["floor_area_m2"]
    name = display(design["name"])
    parts = [f"# {audit['id']} — {name}", '<a id="profil-dna"></a>', headings[0],
             lines([("Nama desain", name), ("Gaya utama", f"**{display(claim_text(styles['primary']))}**"),
                    ("Pengaruh gaya", style_list(styles["influences"])),
                    ("Gaya interior", style_list(styles["interior"])),
                    ("Ciri khas", feature("distinctive-features")),
                    ("Warna & material", feature("palette", "material-hierarchy")),
                    ("Suasana dan lingkungan", feature("environment", "lighting"))]), headings[1],
             table(["Aspek", "Estimasi visual"], [(f"**{label}**", value) for label, value in [
                 ("Ukuran rumah", display(claim_text(size["scale"]))),
                 ("Bentuk bangunan", feature("massing")),
                 ("Lantai & bentuk atap", display(claim_text(size["levels"])) +
                  (" · " + feature("roof") if feature("roof") not in {"—", "unknown"} else "")),
                 ("Tapak bangunan", display(claim_text(size["footprint"]))),
                 ("Proporsi utama", display(claim_text(size["proportions"]))),
                 ("Perkiraan luas lantai", f"**{number(area['min'])}–{number(area['max'])} m²**")]]),
             headings[2], f"Durasi {shots[-1]['end_s']:.2f}s · {len(shots)} shot.",
             "**Camera Pattern:** " + video_pattern(shots) + ".",
             table(["Shot", "Time (s)", "Duration", "Area/Scene", "Camera Movement"], [
                 (shot["shot"][5:], f"{shot['start_s']:.2f}–{shot['end_s']:.2f}",
                  f"{shot['end_s']-shot['start_s']:.2f}s", names(shot["area_ids"]),
                  display(camera_summary(shot))) for shot in shots]),
             headings[3], "![Overview wide seluruh area](media/overview.jpg)"]
    for selected in selections(audit, frames):
        if selected["role"] == "overview":
            shot_index, selection_index = (int(selected["source_pointer"].split("/")[i]) for i in (2, 4))
            overview = shots[shot_index]["overviews"][selection_index]
            parts += [f"**Shot {selected['shot_id'][5:]} · {names(selected['area_ids'])} · {selected['timestamp_s']:.2f}s**",
                      "> " + display(overview["composition_summary"])]
    parts += [headings[4], "![Storyboard seluruh shot dengan panel dan camera](media/storyboard.jpg)", headings[5]]
    for index, shot in enumerate(shots):
        sid = shot["shot"]
        multi = len(shot["area_ids"]) > 1
        composition, camera = shot["composition"], shot["camera"]
        if index:
            parts.append("---")
        parts += [f'<a id="{sid}"></a>', f"### Shot {sid[5:]} · {names(shot['area_ids'])}",
                  f"**Time:** {shot['start_s']:.2f}–{shot['end_s']:.2f}s · **Duration:** {shot['end_s']-shot['start_s']:.2f}s"]
        if multi:
            parts.append("**Shot Type:** Continuous shot · Multi area · No cut.")
        parts += [f"![Kolase Shot {sid[5:]}](media/{sid}.jpg)", groups[0]]
        order = {aid: j for j, aid in enumerate(shot["area_ids"])}
        for block in sorted(shot["design"], key=lambda block: min(order[aid] for aid in block["area_ids"])):
            if multi:
                parts.append(f"##### **{names(block['area_ids'])}**")
            for heading, key in (("Arsitektur", "architecture"), ("Furnitur & dekorasi", "furnishings"),
                                 ("Lingkungan", "environment")):
                parts += [f"**{heading}**", "> " + display(block[key]["text"])]
        rows = [
            ("Fokus", display(composition["focus"])),
            ("Camera Start", " · ".join(display(composition[key]) for key in
                                       ("camera_position", "camera_direction", "view_angle",
                                        "camera_height", "camera_tilt"))),
            ("Framing", display(composition["start_composition"]) + " → " + display(composition["end_composition"])),
            ("Lighting", display(composition["lighting"])),
            ("Foreground dan kedalaman", display(composition["foreground"]) + " · " + display(composition["depth"])),
            ("Reveal", display(composition["reveal"])),
            ("Kesesuaian gerak", display(composition["motion_compatibility"])),
        ]
        if multi:
            route = " → ".join(f"{labels[r['area_id']]} ({r['start_s']:.2f}–{r['end_s']:.2f}s · "
                               f"{display(r['connector'])} · {display(r['focus'])})" for r in shot.get("route", []))
            rows += [("Area", names(shot["area_ids"])), ("Rute kamera", route or "—")]
        parts += [groups[1], lines(rows)]
        if multi:
            visibility = []
            for aid in shot["area_ids"]:
                intervals = [(max(v["start_s"], shot["start_s"]), min(v["end_s"], shot["end_s"]))
                             for v in areas[aid]["visible_intervals"]]
                visibility.append(labels[aid] + " · " + ", ".join(f"{a:.2f}–{b:.2f}s"
                                                                 for a, b in intervals if a < b))
            parts += ["**Hubungan antararea**", lines([
                ("Penghubung area", "; ".join(display(r["description"]) for r in shot.get("area_relations", [])) or "—"),
                ("Peralihan", "; ".join(visibility)),
                ("Orientasi ruang", display(shot["continuity"]) if "continuity" in shot else "—"),
            ])]
        tempo = camera["tempo"]
        parts += [groups[2], display(camera["description"]), "**Tempo:** " + display(tempo["description"])]
        if "segments" in tempo:
            parts.append(lines([(f"{segment['start_s']:.2f}–{segment['end_s']:.2f}s · {segment['label']}",
                                 display(segment["description"])) for segment in tempo_segments(shot)]))
        if "journey" in camera:
            parts.append("**Alur visual:** " + display(camera["journey"]))
        if multi or len(camera["phases"]) > 1:
            parts += ["**Movement Timeline**", table(["Time (s)", "Area & fokus", "Camera Movement", "Tempo"], [
                (f"{p['start_s']:.2f}–{p['end_s']:.2f}",
                 names(p.get("area_ids", shot["area_ids"])) + " · " + display(p["focus"]),
                 display(p["notation"]), display(phase_tempo_text(shot, p))) for p in camera["phases"]])]
        parts.append("**Camera:** " + display(camera_summary(shot)))
        if "notes" in shot:
            parts.append("**Catatan:** " + display(shot["notes"]))
    if "notes" in audit:
        parts.append("**Catatan referensi:** " + display(audit["notes"]))
    return validate_report("\n\n".join(parts) + "\n", audit, frames)
