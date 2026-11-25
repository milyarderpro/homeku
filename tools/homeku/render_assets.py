"""Shared rendering assets and literal display helpers for the active format."""
from pathlib import Path
from . import FORMAT_VERSION
from .common import cell, require, sha256

ROOT = Path(__file__).resolve().parents[2]
FONT = ROOT / "tools/assets/fonts/DejaVuSans.ttf"
BOLD_FONT = ROOT / "tools/assets/fonts/DejaVuSans-Bold.ttf"
TEMPLATE = ROOT / "tools/assets/templates/analysis.md"
PROFILE_TEMPLATE = ROOT / "tools/assets/templates/analysis-profile.md"
LAYOUT = ROOT / "tools/assets/layouts/media.json"
ALIGNED_LAYOUT = LAYOUT.with_name("media-aligned.json")
DEFAULT_COLUMNS = 5
MAX_PIXELS = 60_000_000
MAX_BYTES = 95 * 1024 * 1024


def report_template(audit):
    return PROFILE_TEMPLATE if "house_type" in audit["design"] else TEMPLATE


def number(value):
    return f"{value:.3f}".rstrip("0").rstrip(".")


def seconds(value):
    return f"{value:.2f}s"


def table(columns, rows):
    return "\n".join(["| " + " | ".join(columns) + " |",
                      "| " + " | ".join("---" for _ in columns) + " |"] +
                     ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows])


def claim_text(claim):
    value = claim.get("value")
    return "unknown" if value is None else str(value)


def feature_text(audit, aspect, fallback="unknown"):
    values = [claim_text(c) for c in audit["design"]["features"] if c["aspect"] == aspect]
    return "; ".join(values) if values else fallback


def require_english_style_names(audit):
    styles = audit["design"]["styles"]
    values = [styles["primary"], *styles["influences"], *styles["interior"]]
    require(all(c["value"] is None or isinstance(c["value"], str) for c in values),
            "Style names must be authored as English technical names, without translation")


def area_names(area_ids, labels):
    return " / ".join(labels[area_id] for area_id in area_ids)


def titles(audit):
    labels = {a["id"]: a["label"] for a in audit["areas"]}
    result = {s["shot"]: {
        "title": f"SHOT {s['shot'][5:]} · {area_names(s['area_ids'], labels)}",
        "subtitle": f"{s['start_s']:.2f}–{s['end_s']:.2f}s · {seconds(s['end_s'] - s['start_s'])}"
    } for s in audit["shots"]}
    result["storyboard"] = {
        "title": f"{audit['id']} — {claim_text(audit['design']['styles']['primary'])} — "
                 f"{seconds(audit['shots'][-1]['end_s'])} — {len(audit['shots'])} shot",
        "subtitle": ""}
    return result


def wrap(text, font, width):
    lines=[]
    for paragraph in text.split("\n"):
        current=""
        for word in paragraph.split():
            candidate=(current+" "+word).strip()
            if current and font.getlength(candidate)>width:
                lines.append(current);current=""
            # Only unusually long unbroken tokens need character-level wrapping.
            if font.getlength(word)>width:
                for char in word:
                    if current and font.getlength(current+char)>width:
                        lines.append(current);current=""
                    current+=char
            else:
                current=(current+" "+word).strip()
        lines.append(current)
    return lines

def resolve_layout(fingerprint):
    for path in (LAYOUT, ALIGNED_LAYOUT):
        if sha256(path) == fingerprint:
            return path
    require(False, "Unknown media layout fingerprint")


def render_config(*, template_path=TEMPLATE, layout_path=ALIGNED_LAYOUT, quality=91, scale=1.0,
                  columns=DEFAULT_COLUMNS, overview_scale=1.0, storyboard_scale=1.0):
    require(type(quality) is int and 30 <= quality <= 100, "JPEG quality must be 30–100")
    require(type(columns) is int and 1 <= columns <= 6, "Collage columns must be 1–6")
    require(all(type(value) in {float, int} and 0 < value <= 1
                for value in (scale, overview_scale, storyboard_scale)),
            "Media scales must be in (0, 1]")
    return {"format_version": FORMAT_VERSION, "template_sha256": sha256(template_path),
            "font_sha256": sha256(FONT), "bold_font_sha256": sha256(BOLD_FONT),
            "layout_sha256": sha256(layout_path), "jpeg_quality": quality, "panel_scale": scale,
            "columns": columns, "overview_scale": overview_scale, "storyboard_scale": storyboard_scale}


def verify_renderer(config, audit):
    template_path = report_template(audit)
    layout_path = resolve_layout(config["layout_sha256"])
    expected = render_config(template_path=template_path, layout_path=layout_path, quality=config["jpeg_quality"],
                             scale=config["panel_scale"],
                             columns=config["columns"], overview_scale=config["overview_scale"],
                             storyboard_scale=config["storyboard_scale"])
    require(config == expected, "Renderer assets or configuration differ from the audit profile")
    return template_path
