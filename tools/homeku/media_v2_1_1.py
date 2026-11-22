"""Versioned native-frame media; caption layout is separate from photo bounds."""
from __future__ import annotations

import io
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from . import media_v2_0, media_v2_1
from .common import require, sha256
from .video import extract_frame

ROOT = Path(__file__).resolve().parents[2]
FONT = ROOT / "tools/assets/fonts/DejaVuSans.ttf"
BOLD_FONT = ROOT / "tools/assets/fonts/DejaVuSans-Bold.ttf"
MAX_PIXELS = 60_000_000
SUPPORTED_MEDIA = ("2.0.0", "2.1.0", "2.1.1")
wrap = media_v2_0.wrap
crop_panel = media_v2_0.crop_panel


def seconds(value):
    """Display precision only: source selections retain exact native timestamps."""
    return f"{value:.2f}s"


def require_english_style_names(audit):
    require(audit["identity"].get("style_names_language") == "en",
            "Renderer 2.1+ requires identity.style_names_language=en; author English style names without automatic translation")


def panel_label(panel, multi_area=False):
    if multi_area and panel["role"] not in {"start", "end"}:
        return panel["label"]
    return {"start": "Start", "middle": "Middle", "end": "End"}.get(panel["role"], panel["label"])


def titles(audit, version="2.1.1"):
    if version == "2.0.0":
        return media_v2_0.titles(audit)
    if version == "2.1.0":
        return media_v2_1.titles(audit)
    require(version == "2.1.1", "Unsupported media version")
    require_english_style_names(audit)
    labels = {area["id"]: area["label"] for area in audit["areas"]}
    result = {}
    for shot in audit["shots"]:
        result[shot["shot"]] = {
            "title": f"SHOT {shot['shot'][5:]} · {' / '.join(labels[a] for a in shot['area_ids'])}",
            "subtitle": f"{shot['start_s']:.2f}–{shot['end_s']:.2f}s · {seconds(shot['end_s'] - shot['start_s'])}",
        }
    result["storyboard"] = {
        "title": f"{audit['id']} — {audit['identity']['primary_style']} — {seconds(audit['shots'][-1]['end_s'])} — {len(audit['shots'])} shot",
        "subtitle": "",
    }
    return result


def layout(selections, source, title, *, single_row=False, columns=4, scale=1.0,
           version="2.1.1", area_labels=None, multi_area=False):
    if version == "2.0.0":
        return media_v2_0.layout(selections, source, title, single_row=single_row,
                                columns=columns, scale=scale)
    if version == "2.1.0":
        return media_v2_1.layout(selections, source, title, single_row=single_row,
            columns=columns, scale=scale, area_labels=area_labels, multi_area=multi_area)
    require(version == "2.1.1", "Unsupported media version")
    require(selections and 0 < scale <= 1 and 1 <= columns <= 6, "Invalid media layout")
    require(FONT.is_file() and BOLD_FONT.is_file(), "Bundled regular/bold font missing")
    fw, fh = round(source["width"] * scale), round(source["height"] * scale)
    require(fw > 0 and fh > 0, "Panel scale too small")
    cols = len(selections) if single_row else min(len(selections), columns)
    gap = max(20, round(fw * 0.035))
    cell_width = max(fw, 320)
    width = cols * cell_width + (cols + 1) * gap
    caption_size = min(128, max(22, round(cell_width * 0.10)),
                       max(22, round(fw * 0.06), round(width / 86) if single_row else 0))
    old_heading_size = min(180, max(caption_size + 12, round(width / 48)))
    old_subtitle_size = max(20, caption_size - 3)
    heading_size = max(1, round(old_heading_size * 0.85))
    caption_size = max(1, round(caption_size * 0.85))
    subtitle_size = max(18, round(old_subtitle_size * 0.85)) if single_row else max(18, round(heading_size * 0.75))
    fonts = {
        "heading": ImageFont.truetype(str(BOLD_FONT), heading_size),
        "caption": ImageFont.truetype(str(BOLD_FONT), caption_size),
        "time": ImageFont.truetype(str(FONT), subtitle_size),
    }
    sizes = {"heading": heading_size, "caption": caption_size, "time": subtitle_size}
    texts = []

    def line_height(key):
        return math.ceil(sizes[key] * 1.5)

    def add_text(text, key, x, y, region):
        texts.append({"text": text, "font": key, "x": x, "y": y, "region": region})

    heading = title if isinstance(title, dict) else {"title": title, "subtitle": ""}
    y = gap
    usable = width - 2 * gap
    if single_row:
        for line in wrap(heading["title"], fonts["heading"], usable):
            add_text(line, "heading", gap, y, "title")
            y += line_height("heading")
        if heading.get("subtitle"):
            for line in wrap(heading["subtitle"], fonts["time"], usable):
                add_text(line, "time", gap, y, "header_time")
                y += line_height("time")
        header = y + gap
    else:
        # A bounded title column leaves all timing data beside it, even after wrapping.
        measured = max(fonts["heading"].getlength(line) for line in heading["title"].split("\n"))
        title_width = min(measured, usable * 0.43)
        title_lines = wrap(heading["title"], fonts["heading"], title_width)
        for line in title_lines:
            add_text(line, "heading", gap, y, "title")
            y += line_height("heading")
        time_x = gap + title_width + 2 * gap
        time_width = width - gap - time_x
        timing = []
        if heading.get("subtitle"):
            timing.extend(wrap(heading["subtitle"], fonts["time"], time_width))
        stamps = []
        for index, panel in enumerate(selections):
            label = panel_label(panel, multi_area)
            if multi_area:
                label = f"{index + 1:02d} · {label}"
            stamps.append(f"{label} {seconds(panel['timestamp_s'])}")
        timing.extend(wrap(" · ".join(stamps), fonts["time"], time_width))
        time_y = gap
        for line in timing:
            add_text(line, "time", time_x, time_y, "header_time")
            time_y += line_height("time")
        header = max(y, time_y) + gap

    labels = area_labels or {}
    captions = []
    for index, panel in enumerate(selections):
        if single_row:
            name = " / ".join(labels.get(a, a) for a in panel["area_ids"])
            label = f"{panel['shot_id'][5:]} · {name}"
            lines = [(line, "caption") for line in wrap(label, fonts["caption"], cell_width)]
            lines += [(line, "time") for line in wrap(f"Overview · {seconds(panel['timestamp_s'])}", fonts["time"], cell_width)]
            captions.append((lines, False))
            continue
        label = panel_label(panel, multi_area)
        if multi_area:
            label = f"{index + 1:02d} · {label}"
        lines = [(line, "caption") for line in wrap(label, fonts["caption"], cell_width)]
        captions.append((lines, False))
    caption_height = max(
        max(line_height(key) for _, key in lines) if inline else sum(line_height(key) for _, key in lines)
        for lines, inline in captions
    )
    stride = fh + gap + caption_height + gap
    rows = math.ceil(len(selections) / cols)
    height = header + rows * stride
    require(width * height <= MAX_PIXELS and max(width, height) <= 65000,
            "Collage exceeds pixel/JPEG limits; choose a smaller explicit panel_scale")
    placements = []
    for index, (panel, (lines, inline)) in enumerate(zip(selections, captions)):
        cell_x = gap + (index % cols) * (cell_width + gap)
        x = cell_x + (cell_width - fw) // 2
        y = header + (index // cols) * stride
        placements.append({
            "id": panel["id"], "selection_id": panel["id"], "shot_id": panel["shot_id"],
            "area_ids": panel["area_ids"], "frame_index": panel["frame_index"],
            "timestamp_s": panel["timestamp_s"], "bbox": [x, y, fw, fh], "scale": scale,
        })
        caption_x, caption_y = cell_x, y + fh + gap
        for text, key in lines:
            add_text(text, key, caption_x, caption_y, "caption_time" if key == "time" else "caption")
            if inline:
                caption_x += fonts[key].getlength(text)
            else:
                caption_y += line_height(key)
    return {"width": width, "height": height, "panels": placements}, {
        "texts": texts, "fonts": fonts, "caption_size": caption_size, "heading_size": heading_size,
    }


def expected_media(audit, source, config):
    version = config["media"]
    if version == "2.0.0":
        yield from media_v2_0.expected_media(audit, source, config)
        return
    if version == "2.1.0":
        yield from media_v2_1.expected_media(audit, source, config)
        return
    heading = titles(audit, version)
    labels = {area["id"]: area["label"] for area in audit["areas"]}
    for shot in audit["shots"]:
        metadata, _ = layout(shot["panels"], source, heading[shot["shot"]],
            columns=3 if len(shot["area_ids"]) == 1 else config["columns"], scale=config["panel_scale"],
            area_labels=labels, multi_area=len(shot["area_ids"]) > 1, version=version)
        yield {"path": f"media/{shot['shot']}.jpg", "kind": "shot-collage",
               "shot_id": shot["shot"], **metadata}, shot["panels"], heading[shot["shot"]], False
    choices = [panel for shot in audit["shots"] for panel in shot["overviews"]]
    metadata, _ = layout(choices, source, heading["storyboard"], single_row=True,
                          scale=config["panel_scale"], area_labels=labels, version=version)
    yield {"path": "media/storyboard.jpg", "kind": "storyboard", "shot_id": None,
           **metadata}, choices, heading["storyboard"], True


def build_media(folder, audit, source_path, source, config):
    if config["media"] == "2.0.0":
        return media_v2_0.build_media(folder, audit, source_path, source, config)
    if config["media"] == "2.1.0":
        return media_v2_1.build_media(folder, audit, source_path, source, config)
    result, cache = [], {}
    labels = {area["id"]: area["label"] for area in audit["areas"]}
    by_shot = {shot["shot"]: shot for shot in audit["shots"]}
    for meta, selections, title, single in expected_media(audit, source, config):
        multi = not single and len(by_shot[meta["shot_id"]]["area_ids"]) > 1
        _, design = layout(selections, source, title, single_row=single,
            columns=config["columns"] if multi else 3, scale=config["panel_scale"],
            area_labels=labels, multi_area=multi, version=config["media"])
        canvas = Image.new("RGB", (meta["width"], meta["height"]), "#f5f3ed")
        draw = ImageDraw.Draw(canvas)
        for panel in meta["panels"]:
            index = panel["frame_index"]
            if index not in cache:
                cache[index] = extract_frame(source_path, index, source["video_stream_index"])
            with Image.open(io.BytesIO(cache[index])) as frame:
                picture = frame.convert("RGB")
            x, y, w, h = panel["bbox"]
            if picture.size != (w, h):
                picture = picture.resize((w, h), Image.Resampling.LANCZOS)
            draw.rectangle((x - 1, y - 1, x + w, y + h), outline="#cbd1c9", width=1)
            canvas.paste(picture, (x, y))
        for text in design["texts"]:
            draw.text((text["x"], text["y"]), text["text"], font=design["fonts"][text["font"]],
                      fill="#213d34" if text["font"] != "time" else "#536259")
        target = folder / meta["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(target, "JPEG", quality=config["jpeg_quality"], subsampling=0,
                    optimize=False, progressive=False)
        result.append({**meta, "sha256": sha256(target)})
    return result
