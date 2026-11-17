"""Extract deterministic temporal samples without changing source packages."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont, ImageStat
from knowledge_library import ROOT, dump, load_release, read_archives
from verify_source_integrity import sha256_file


def video_duration(path):
    value = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=duration", "-show_entries", "format=duration",
        "-of", "json", str(path)], text=True))
    stream = value.get("streams", [{}])[0].get("duration")
    return float(stream or value["format"]["duration"])


def extract_frame(video, timestamp, target, width=320):
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                    "-ss", f"{timestamp:.6f}", "-i", str(video), "-frames:v", "1",
                    "-vf", f"scale={width}:-2", "-q:v", "4", str(target)],
                   check=True, stdout=subprocess.DEVNULL)
    if not target.is_file():
        raise ValueError(f"No frame at {timestamp}: {video}")
    with Image.open(target) as image:
        image.verify()


def dhash(path):
    with Image.open(path) as image:
        gray = image.convert("L")
        # Content crop prevents letterbox bars dominating appearance matching.
        mask = gray.point(lambda value: 255 if value > 18 else 0)
        box = mask.getbbox()
        if box:
            gray = gray.crop(box)
        contrast = float(ImageStat.Stat(gray).stddev[0])
        small = gray.resize((9, 8))
        values = list(small.getdata())
    bits = 0
    for row in range(8):
        for col in range(8):
            bits = (bits << 1) | int(values[row * 9 + col] > values[row * 9 + col + 1])
    return f"{bits:016x}", round(contrast, 3)


def sample_reference(root, source, document):
    root = Path(root)
    ident = source["reference_id"]
    folder = root / "knowledge/temporal" / ident
    index_path = folder / "index.json"
    if index_path.exists():
        existing = json.loads(index_path.read_text())
        if existing["source"] == source and all(
            (root / frame["path"]).is_file() and sha256_file(root / frame["path"]) == frame["sha256"]
            for shot in existing["shots"] for frame in shot["frames"]
        ) and (folder / "contact.jpg").exists() and sha256_file(folder / "contact.jpg") == existing["contact_sha256"]:
            return existing
        raise ValueError(f"Temporal source/assets changed: {ident}; explicit rebuild required")
    video = root / source["source_path"]
    duration = video_duration(video)
    shots = []
    for shot in document["shots"]:
        a = max(float(shot["start_s"]), 0)
        b = min(float(shot["end_s"]), duration)
        if b <= a:
            raise ValueError(f"Source duration does not support {ident}/{shot['id']}")
        pad = min(0.12, (b - a) / 8)
        times = [a + pad, (a + b) / 2, b - pad]
        frames = []
        for label, time in zip(("start", "middle", "end"), times):
            target = folder / f"{shot['id']}-{label}.jpg"
            extract_frame(video, time, target)
            visual_hash, contrast = dhash(target)
            frames.append({"label": label, "timestamp_s": round(time, 6),
                           "path": target.relative_to(root).as_posix(),
                           "sha256": sha256_file(target), "dhash": visual_hash,
                           "contrast": contrast})
        shots.append({"shot_id": shot["id"], "annotation_start_s": a,
                      "annotation_end_s": float(shot["end_s"]), "sample_end_limit_s": b,
                      "frames": frames})
    # 3-column overview is an analytical derivative, not a production storyboard.
    width, cell_height, top = 240, 458, 66
    canvas = Image.new("RGB", (width * 3, top + cell_height * len(shots)), "#f3f1eb")
    draw = ImageDraw.Draw(canvas)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 15) if Path(font_path).exists() else ImageFont.load_default()
    draw.text((10, 8), f"{ident} | START / MIDDLE / END", fill="#202820", font=font)
    draw.text((10, 31), "Sampled evidence; not all frames or certified physical camera motion", fill="#202820", font=font)
    for row, shot in enumerate(shots):
        for col, frame in enumerate(shot["frames"]):
            with Image.open(root / frame["path"]) as original:
                picture = original.convert("RGB")
                picture.thumbnail((width - 8, cell_height - 40))
                x = col * width + (width - picture.width) // 2
                y = top + row * cell_height
                canvas.paste(picture, (x, y))
            draw.text((col * width + 4, top + row * cell_height + cell_height - 35),
                      f"{shot['shot_id']} {frame['label']} {frame['timestamp_s']:.2f}s",
                      fill="#202820", font=font)
    canvas.save(folder / "contact.jpg", quality=86)
    result = {"schema_version": "1.0", "source": source,
              "sampling_method": "start_middle_end_inside_annotation_clamped_to_video_stream",
              "video_stream_duration_s": duration, "shots": shots,
              "contact_path": (folder / "contact.jpg").relative_to(root).as_posix(),
              "contact_sha256": sha256_file(folder / "contact.jpg"),
              "limitations": ["Three samples do not prove what happens between sampled timestamps.",
                             "Annotations may have approximate cut boundaries.",
                             "Dolly versus zoom and physical continuity remain interpretations."]}
    index_path.write_text(dump(result), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--references", nargs="*")
    args = parser.parse_args()
    release = load_release(args.root)
    refs = read_archives(args.root)
    for source in release["references"]:
        ident = source["reference_id"]
        if args.references and ident not in args.references:
            continue
        value = sample_reference(args.root, source, refs[ident])
        print(f"{ident}: {len(value['shots'])} sampled shots", flush=True)


if __name__ == "__main__":
    main()
