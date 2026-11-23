"""Chat-side candidates/ZIPs: legacy Markdown or authored V2 JSON by explicit version."""

from __future__ import annotations

import bisect
import hashlib
import io
import math
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .common import LibraryError, dumps, read_json, require, sha256
from .markdown import parse
from .validation import CODE_ROOT, extract_package, validate_folder
from .video import probe_video, frame_times, nearest, extract_frame, selected_indices


def sample(source, output, fps=10.0, start=0.0, end=None, *, native=False, shot_id=None, reason=None):
    """Temporary audit evidence only. The selected frames are not yet viewed."""
    require(math.isfinite(fps) and 0 < fps <= 240, "Sampling fps must be in (0, 240]")
    require(not output.exists() or (output.is_dir() and not any(output.iterdir())),
            "Use a fresh sampling output directory for each audit pass; old evidence is not merged")
    info = probe_video(source)
    times = frame_times(source)
    end = info["duration_s"] if end is None else end
    require(0 <= start < end <= info["duration_s"] + 0.001, "Sampling interval outside video")
    source_fps = info["fps"]["numerator"] / info["fps"]["denominator"]
    indices = selected_indices(times, start, end, fps, native=native, source_fps=source_fps)
    require(len(indices) <= 1000, "Use bounded audit intervals rather than thousands of images at once")
    output.mkdir(parents=True, exist_ok=True)
    expression = "+".join(f"eq(n\\,{index})" for index in indices)
    try:
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-protocol_whitelist", "file,pipe", "-i", str(source),
                        "-map", f"0:{info['video_stream_index']}", "-vf", "select=" + expression, "-vsync", "0",
                        "-q:v", "2", "-threads", "1", str(output / "selected-%06d.jpg")],
                       check=True, capture_output=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as error:
        raise LibraryError(f"Cannot extract selected native frames: {error}") from error
    extracted = sorted(output.glob("selected-*.jpg"))
    require(len(extracted) == len(indices), "Decoded frame count differs from selected native PTS")
    rows = []
    for index, original in zip(indices, extracted):
        path = output / f"frame-{index:06d}.jpg"
        original.rename(path)
        rows.append({"frame_index": index, "timestamp_s": times[index], "path": path.name})
    font = ImageFont.load_default()
    for offset in range(0, len(rows), 24):
        chunk = rows[offset:offset + 24]
        thumb_width = 200
        thumb_height = round(thumb_width * info["height"] / info["width"])
        row_height = thumb_height + 28
        sheet = Image.new("RGB", (4 * thumb_width, ((len(chunk) + 3) // 4) * row_height), "#202020")
        draw = ImageDraw.Draw(sheet)
        for cell, row in enumerate(chunk):
            x, y = (cell % 4) * thumb_width, (cell // 4) * row_height
            with Image.open(output / row["path"]) as picture:
                sheet.paste(picture.resize((thumb_width, thumb_height)), (x, y + 28))
            draw.text((x + 4, y + 6), f"f{row['frame_index']}  {row['timestamp_s']:.3f}s", font=font, fill="white")
        sheet.save(output / f"sheet-{offset // 24 + 1:03d}.jpg", quality=90)
    report = {"source_sha256": sha256(source), "source": info, "frames": rows,
              "selection": {"start_s": start, "end_s": end, "mode": "frame-by-frame" if native else "sampling",
                            "sampling_fps": None if native else fps, "source_fps": source_fps,
                            "selected_count": len(indices), "boundary_indices": [indices[0], indices[-1]]},
              "review_record_template": {"shot_id": shot_id or "unknown", "start_s": start, "end_s": end,
                                         "mode": "frame-by-frame" if native else "sampling", "sampling_fps": None if native else fps,
                                         "selected_frame_indices": indices, "viewed_frame_indices": [],
                                         "reason": reason or "Baseline 10 FPS; fill only frames actually viewed."},
              "note": "Extracted frames are not a declaration that an AI viewed them."}
    (output / "sampling.json").write_text(dumps(report))
    return report


def storyboard(folder, shots, media):
    by_path = {m["path"]: m for m in media}
    width = min(720, shots[0]["source_width"]) if "source_width" in shots[0] else 720
    width = max(360, width)
    font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    font = ImageFont.truetype(str(font_path), 20) if font_path.exists() else ImageFont.load_default()
    pictures = []
    for shot in shots:
        name = f"media/{shot['shot']}/area-overview.jpg"
        with Image.open(folder / name) as picture:
            image = picture.copy()
        height = round(width * image.height / image.width)
        pictures.append((shot, name, image.resize((width, height))))
    height = sum(picture.height + 68 for _, _, picture in pictures)
    require(width * height <= 60_000_000, "Storyboard exceeds image pixel limit; shorten/split the source reference")
    board = Image.new("RGB", (width, height), "#171717")
    draw = ImageDraw.Draw(board)
    y = 0
    for shot, name, picture in pictures:
        label = f"{shot['shot']} | {'; '.join(shot['areas'])}"
        draw.text((10, y + 7), label, font=font, fill="white")
        draw.text((10, y + 34), f"source {by_path[name]['timestamp_s']:.3f}s", font=font, fill="white")
        board.paste(picture, (0, y + 68))
        y += picture.height + 68
    path = folder / "media/storyboard.jpg"
    board.save(path, "JPEG", quality=91)
    return {"path": "media/storyboard.jpg", "kind": "storyboard", "sha256": sha256(path), "shot_id": None,
            "timestamp_s": None, "width": width, "height": height, "derived_from": [name for _, name, _ in pictures], "crop": None}


def assemble(source, analysis, audit_info, output_root, *, extras=None, include_source=False,
             supersedes=None, purpose="reference", reviewed_sha256=None):
    """Build a fresh candidate. reviewed_sha256 pins an explicitly reviewed MD.

    The helper checks a digest, not human intent. The chat must obtain the user's
    content acceptance before passing that digest for a final export.
    """
    require(source.is_file() and analysis.is_file(), "Source MP4 and latest analysis.md are required")
    original_bytes = analysis.read_bytes()
    original_hash = hashlib.sha256(original_bytes).hexdigest()
    try:
        text = original_bytes.decode("utf-8")
    except UnicodeError as error:
        raise LibraryError("analysis.md is not UTF-8") from error
    require("{{" not in text and "}}" not in text, "Unfilled template placeholders")
    model = parse(text)
    rid = model["id"]
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", rid), "Invalid reference ID")
    require(source.stem == rid, "Reference ID must match the original source filename stem")
    require(source.suffix.casefold() == ".mp4", "Source must be an MP4")
    require(isinstance(audit_info, dict) and "reviewed_ranges" in audit_info and "ai" in audit_info,
            "audit-info requires actual reviewed_ranges and known AI identity")
    if reviewed_sha256 is not None:
        require(reviewed_sha256 == original_hash, "Analysis changed since chat review; review the latest revision before final export")
    metadata = {"path": f"video/{rid}.mp4", "sha256": sha256(source), **probe_video(source)}
    times = frame_times(source)
    output_root.mkdir(parents=True, exist_ok=True)
    destination = output_root / rid
    require(not destination.resolve().is_relative_to((CODE_ROOT / "references").resolve()),
            "Use a chat candidate folder; active references must be published through ingest")
    require(not analysis.resolve().is_relative_to(destination.resolve()), "Keep the input MD outside the generated candidate folder")
    require(not source.resolve().is_relative_to(destination.resolve()), "Keep the original video outside the generated candidate folder")
    if destination.exists():
        require(destination.is_dir() and not destination.is_symlink() and (destination / "manifest.json").is_file(),
                "Refusing to replace an unmanaged candidate folder")
        previous = read_json(destination / "manifest.json")
        require(isinstance(previous, dict) and previous.get("id") == rid and isinstance(previous.get("media"), list),
                "Refusing to replace an unmanaged candidate folder")
        owned = {"analysis.md", "manifest.json", "source.mp4"} | {m.get("path") for m in previous["media"] if isinstance(m, dict)}
        require(all(not p.is_symlink() and (not p.is_file() or p.relative_to(destination).as_posix() in owned)
                    for p in destination.rglob("*")), "Unmanaged files in candidate folder; choose a fresh output folder")
    with tempfile.TemporaryDirectory(prefix=".assemble-", dir=output_root) as work_name:
        work = Path(work_name)
        folder = work / rid
        folder.mkdir()
        (folder / "analysis.md").write_bytes(original_bytes)
        media, frame_cache = [], {}
        def save_frame(shot, kind, timestamp, path=None, crop=None):
            index = nearest(times, timestamp, shot["start_s"], shot["end_s"])
            actual = times[index]
            if kind == "area-overview":
                require(abs(actual - timestamp) <= 0.000001,
                        f"{shot['shot']}: overview must use actual PTS {actual:.9f}, not {timestamp}; correct the draft before review")
            if index not in frame_cache:
                frame_cache[index] = extract_frame(source, index, metadata["video_stream_index"])
            name = path or f"media/{shot['shot']}/{kind}.jpg"
            target = folder / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(io.BytesIO(frame_cache[index])) as picture:
                if crop is not None:
                    x, y, width, height = crop
                    require(kind == "detail" and min(x, y) >= 0 and min(width, height) > 0 and
                            x + width <= picture.width and y + height <= picture.height, f"Invalid crop: {name}")
                    image = picture.crop((x, y, x + width, y + height))
                    image.save(target, "JPEG", quality=94)
                    size = image.size
                else:
                    target.write_bytes(frame_cache[index])
                    size = picture.size
            media.append({"path": name, "kind": kind, "sha256": sha256(target), "shot_id": shot["shot"],
                          "timestamp_s": actual, "width": size[0], "height": size[1], "derived_from": [], "crop": crop})
        by_shot = {s["shot"]: s for s in model["shots"]}
        for shot in model["shots"]:
            save_frame(shot, "area-overview", shot["composition"]["overview_timestamp_s"])
            save_frame(shot, "start", shot["start_s"])
            save_frame(shot, "middle", (shot["start_s"] + shot["end_s"]) / 2)
            last = bisect.bisect_left(times, shot["end_s"]) - 1
            save_frame(shot, "end", times[last])
        extras = extras or []
        require(isinstance(extras, list), "extras must be a list")
        for item in extras:
            require(set(item) == {"shot_id", "path", "timestamp_s", "crop"}, "Invalid extras fields")
            require(item["shot_id"] in by_shot, "Unknown extra-media shot")
            pattern = r"media/" + re.escape(item["shot_id"]) + r"/(reveal|detail)-[0-9]{2,}\.jpg"
            match = re.fullmatch(pattern, item["path"])
            require(match is not None and item["path"] not in {m["path"] for m in media}, "Invalid/duplicate extra-media path")
            save_frame(by_shot[item["shot_id"]], match[1], item["timestamp_s"], item["path"], item["crop"])
        media.insert(0, storyboard(folder, model["shots"], media))
        manifest = {"contract_version": model["format_version"], "purpose": purpose, "id": rid, "revision": model["revision"],
                    "supersedes": supersedes, "source": metadata, "audit": {**model["coverage"], "reviewed_ranges": audit_info["reviewed_ranges"],
                    **({"frame_reviews": audit_info["frame_reviews"]} if "frame_reviews" in audit_info else {}),
                    "ai": audit_info["ai"], "created_at": audit_info.get("created_at", datetime.now(timezone.utc).isoformat())}, "media": media}
        (folder / "manifest.json").write_text(dumps(manifest), encoding="utf-8")
        if include_source:
            shutil.copyfile(source, folder / "source.mp4")
        _, validated, _ = validate_folder(folder, work, source_overrides={rid: source})
        require(sha256(analysis) == original_hash, "Input analysis changed during export")
        package_name = f"{rid}-r{model['revision']:04d}.zip"
        package = work / package_name
        with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(folder.rglob("*")):
                if path.is_file():
                    info = zipfile.ZipInfo(f"{rid}/{path.relative_to(folder).as_posix()}", date_time=(1980, 1, 1, 0, 0, 0))
                    info.external_attr = 0o100644 << 16
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, path.read_bytes())
        unpacked = extract_package(package, work / "round-trip")
        _, checked, _ = validate_folder(unpacked, work, package_name, source_overrides={rid: source})
        require(checked["content_sha256"] == validated["content_sha256"], "ZIP round-trip differs from candidate")
        require(sha256(unpacked / "analysis.md") == original_hash, "ZIP does not contain latest reviewed MD")
        if destination.exists():
            require(not destination.is_symlink(), "Candidate destination may not be a symlink")
            shutil.rmtree(destination)
        os.replace(folder, destination)
        zip_dir = output_root / "packages"
        zip_dir.mkdir(exist_ok=True)
        os.replace(package, zip_dir / package_name)
    return {"id": rid, "revision": model["revision"], "analysis_sha256": original_hash,
            "content_sha256": validated["content_sha256"], "package": str(zip_dir / package_name),
            "candidate": str(destination), "media_count": len(media), "source_included": include_source,
            "mode": "reviewed-export" if reviewed_sha256 is not None else "draft-for-chat-review"}


def assemble_v2(source, audit_path, audit_info, output_root, *, supersedes=None, purpose="reference",
                include_source=False, quality=91, scale=1.0, columns=4, version=None, overview_scale=1.0, storyboard_scale=1.0):
    """Create a candidate only. No ZIP or acceptance is inferred from drafting."""
    from .models import validate_audit
    from .media import build_media
    from .reporting import render_config, render_report
    from .common import snapshot_hash
    require(source.is_file() and audit_path.is_file(),"MP4 and authored audit.json required")
    authored=audit_path.read_bytes();audit=read_json(audit_path)
    require(isinstance(audit,dict),"Audit JSON must be an object")
    info={"path":f"video/{audit.get('id','')}.mp4","sha256":sha256(source),**probe_video(source)}
    validate_audit(audit,info["duration_s"],frame_times(source))
    rid=audit["id"]
    require(source.stem==rid and source.suffix.casefold()==".mp4","ID must match original MP4 stem")
    require(isinstance(audit_info,dict),"Actual audit metadata required")
    output_root.mkdir(parents=True,exist_ok=True);destination=output_root/rid
    require(not destination.resolve().is_relative_to((CODE_ROOT/"references").resolve()),"Active references change through ingest only")
    require(not source.resolve().is_relative_to(destination.resolve()) and not audit_path.resolve().is_relative_to(destination.resolve()),"Keep input source outside candidate")
    if destination.exists():
        require(destination.is_dir() and not destination.is_symlink(),"Invalid existing candidate")
        old=read_json(destination/"manifest.json") if (destination/"manifest.json").is_file() else {}
        require(old.get("contract_version") in {"2.0", "2.1"} and old.get("id")==rid,"Refusing to replace unmanaged candidate")
        owned={"audit.json","analysis.md","manifest.json","source.mp4"}|{m["path"] for m in old["media"]}
        require(all(not f.is_symlink() and (not f.is_file() or f.relative_to(destination).as_posix() in owned) for f in destination.rglob("*")),"Unmanaged files in candidate folder")
    with tempfile.TemporaryDirectory(prefix=".v2-draft-",dir=output_root) as work_name:
        folder=Path(work_name)/rid;folder.mkdir()
        (folder/"audit.json").write_bytes(authored)
        kwargs={}
        if audit["schema_version"] == "2.1":
            require(version in {None,"2.2.0"},"Source 2.1 requires renderer 2.2.0")
            kwargs.update(version="2.2.0",overview_scale=overview_scale,storyboard_scale=storyboard_scale)
        else:
            require(version != "2.2.0", "Renderer 2.2.0 requires source 2.1")
            require(overview_scale==1.0 and storyboard_scale==1.0,"Combined media scales require source 2.1")
            if version is not None:kwargs["version"]=version
        config=render_config(quality=quality,scale=scale,columns=columns,**kwargs)
        media=build_media(folder,audit,source,info,config)
        (folder/"analysis.md").write_text(render_report(audit,config),encoding="utf-8",newline="\n")
        logs=dict(audit_info)
        logs.setdefault("created_at",datetime.now(timezone.utc).isoformat())
        manifest={"contract_version":audit["schema_version"],"id":rid,"revision":audit["revision"],"supersedes":supersedes,
                  "purpose":purpose,"source":info,"audit":logs,"audit_sha256":sha256(folder/"audit.json"),"render":config,"media":media}
        (folder/"manifest.json").write_text(dumps(manifest),encoding="utf-8")
        if include_source:shutil.copyfile(source,folder/"source.mp4")
        validate_folder(folder,output_root,source_overrides={rid:source})
        require(sha256(source)==info["sha256"] and audit_path.read_bytes()==authored,"Source changed during draft assembly")
        # Keep the old candidate until the replacement is complete and validated.
        backup=Path(work_name)/"previous-candidate"
        if destination.exists():os.replace(destination,backup)
        try:
            os.replace(folder,destination)
        except OSError:
            if backup.exists():os.replace(backup,destination)
            raise
    return {"mode":"draft-for-chat-review","candidate":str(destination),"snapshot_sha256":snapshot_hash(destination),
            "media_count":len(media),"media_bytes":sum((destination/m["path"]).stat().st_size for m in media)}


def review_v2(candidate, output, source=None):
    """Produce readable cards and a separate receipt; this is not user approval."""
    from .common import snapshot_hash
    from .reporting import review_report
    digest=snapshot_hash(candidate)
    overrides={candidate.name:source} if source else None
    manifest,_,_=validate_folder(candidate,candidate.parent,source_overrides=overrides)
    require(manifest["contract_version"] in {"2.0", "2.1"},"Use the explicit legacy workflow for this contract")
    require(not output.resolve().is_relative_to(candidate.resolve()),"Receipt/cards must remain outside candidate")
    audit=read_json(candidate/"audit.json")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(review_report(audit,manifest["render"],candidate.as_posix()),encoding="utf-8")
    require(snapshot_hash(candidate)==digest,"Candidate changed during review generation")
    receipt=output.with_suffix(output.suffix+".json")
    receipt.write_text(dumps({"candidate":str(candidate),"snapshot_sha256":digest,"report":str(output)}),encoding="utf-8")
    return {"review":str(output),"receipt":str(receipt),"snapshot_sha256":digest}


def export_v2(candidate, output_root, reviewed_sha256, source=None):
    """Package reviewed bytes; never regenerate images, timestamps or narratives."""
    from .common import snapshot_hash
    require(snapshot_hash(candidate)==reviewed_sha256,"Candidate changed since whole-snapshot review")
    overrides={candidate.name:source} if source else None
    manifest,_,_=validate_folder(candidate,candidate.parent,source_overrides=overrides)
    require(manifest["contract_version"] in {"2.0", "2.1"},"Use the explicit legacy workflow for this contract")
    output_root.mkdir(parents=True,exist_ok=True)
    require(not output_root.resolve().is_relative_to(candidate.resolve()),"ZIP output must stay outside candidate")
    filename=f"{manifest['id']}-r{manifest['revision']:04d}.zip"
    destination=output_root/filename
    with tempfile.TemporaryDirectory(prefix=".v2-export-",dir=output_root) as work_name:
        work=Path(work_name);target=work/filename
        with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as archive:
            for p in sorted(candidate.rglob("*")):
                if p.is_file():
                    info=zipfile.ZipInfo(f"{candidate.name}/{p.relative_to(candidate).as_posix()}",date_time=(1980,1,1,0,0,0))
                    info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
                    archive.writestr(info,p.read_bytes())
        unpacked=extract_package(target,work/"roundtrip")
        validate_folder(unpacked,candidate.parent,filename,overrides)
        require(snapshot_hash(unpacked)==reviewed_sha256 and snapshot_hash(candidate)==reviewed_sha256,"Export snapshot mismatch")
        os.replace(target,destination)
    return {"mode":"reviewed-export","package":str(destination),"snapshot_sha256":reviewed_sha256,
            "package_sha256":sha256(destination),"package_bytes":destination.stat().st_size}
