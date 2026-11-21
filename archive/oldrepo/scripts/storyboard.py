"""Render a compact Homeku storyboard matching the approved five-portrait reference.

1–5 shots: one row with one column per shot. 6+ shots: three columns.
All information comes from the reviewed analysis YAML. No generative imagery.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

BG = "#F1F0EB"
INK = "#28372E"
MUTED = "#5F6660"
BORDER = "#C8C7C0"
MARGIN_X = 30
CARD_W = 252
CARD_H = 432
GAP_X = 12
GAP_Y = 94
HEADER_H = 103
FOOTER = 28


def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def fit_label(draw: ImageDraw.ImageDraw, raw: object, label_font, max_width: int) -> str:
    """Single-line ellipsis; never allow variable-length scene/camera to overlap panels."""
    label = str(raw or "—").replace("_", " ").strip()
    if draw.textbbox((0, 0), label, font=label_font)[2] <= max_width:
        return label
    while label and draw.textbbox((0, 0), label + "…", font=label_font)[2] > max_width:
        label = label[:-1]
    return (label.rstrip() + "…") if label else "…"


def clock(seconds: float) -> str:
    mins = int(seconds) // 60
    secs = seconds - mins * 60
    return f"{mins}:{secs:05.2f}"


def generate_storyboard(
    frames: list[Path],
    dest: Path,
    *,
    video: dict,
    architecture: dict,
    shots: list[dict],
) -> None:
    if not frames or len(frames) != len(shots):
        raise ValueError("Storyboard requires one actual frame per shot")

    count = len(frames)
    columns = count if count <= 5 else 3
    rows = math.ceil(count / columns)
    width = MARGIN_X * 2 + columns * CARD_W + (columns - 1) * GAP_X
    height = HEADER_H + (rows - 1) * (CARD_H + GAP_Y) + CARD_H + 88 + FOOTER

    board = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(board)
    title_font, meta_font = font(25, True), font(15)
    scene_font, desc_font = font(15, True), font(14)
    max_text_width = width - 2 * MARGIN_X
    stem = Path(str(video.get("filename") or "VIDEO")).stem.upper()
    title = fit_label(draw, stem + " · SHOT-BY-SHOT STORYBOARD", title_font, max_text_width)
    draw.text((MARGIN_X, 15), title, font=title_font, fill=INK)
    style = str(architecture.get("primary_style") or "").replace("_", " ").title()
    meta = f"{video.get('duration_s', '—')} detik  |  {count} shot  |  {style}"
    draw.text((MARGIN_X, 52), fit_label(draw, meta, meta_font, max_text_width), font=meta_font, fill=MUTED)

    for i, (source, shot) in enumerate(zip(frames, shots)):
        x = MARGIN_X + (i % columns) * (CARD_W + GAP_X)
        y = HEADER_H + (i // columns) * (CARD_H + GAP_Y)
        with Image.open(source) as original:
            image = ImageOps.pad(original.convert("RGB"), (CARD_W, CARD_H), method=Image.Resampling.LANCZOS, color=BG)
        # Rounded corners without distorting/cropping the source image.
        mask = Image.new("L", (CARD_W, CARD_H), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, CARD_W - 1, CARD_H - 1), radius=4, fill=255)
        board.paste(image, (x, y), mask)
        draw.rounded_rectangle((x, y, x + CARD_W - 1, y + CARD_H - 1), radius=4, outline=BORDER, width=1)

        label = str(shot.get("scene") or "scene").replace("_", " ").upper()
        heading = f"{i+1:02d} · {label}"
        draw.text((x + 5, y + CARD_H + 10), fit_label(draw, heading, scene_font, CARD_W - 10), font=scene_font, fill=INK)
        draw.text((x + 5, y + CARD_H + 35),
                  f"{clock(float(shot['start_s']))}–{clock(float(shot['end_s']))}",
                  font=desc_font, fill=MUTED)
        camera = shot.get("camera") or {}
        movements = camera.get("movements") or []
        if isinstance(movements, str):
            movements = [movements]
        movement_label = " + ".join(str(part).replace("_", "-") for part in movements) or "Camera: unknown"
        draw.text((x + 5, y + CARD_H + 59),
                  fit_label(draw, movement_label, desc_font, CARD_W - 10),
                  font=desc_font, fill=MUTED)

    dest.parent.mkdir(parents=True, exist_ok=True)
    board.save(dest, "JPEG", quality=91, optimize=True, subsampling=0)
