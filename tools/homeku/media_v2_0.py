"""Versioned real-frame collages. Captions never overlap source photographs."""
from __future__ import annotations
import io
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .common import LibraryError, require, sha256
from .video import extract_frame

ROOT = Path(__file__).resolve().parents[2]
FONT = ROOT / "tools/assets/fonts/DejaVuSans.ttf"
MAX_PIXELS = 60_000_000


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


def layout(selections, source, title, *, single_row=False, columns=4, scale=1.0):
    """Pure layout metadata, also used for validation without re-encoding JPEGs."""
    require(selections and 0 < scale <= 1 and 1 <= columns <= 6, "Invalid media layout")
    require(FONT.is_file(), "Bundled font missing")
    fw, fh = round(source["width"]*scale), round(source["height"]*scale)
    require(fw > 0 and fh > 0, "Panel scale too small")
    cols = len(selections) if single_row else min(len(selections), columns)
    font_size = max(14, min(28, round(fw*0.035)))
    font = ImageFont.truetype(str(FONT), font_size)
    gap = max(12, font_size)
    cell_width = max(fw, 240)
    width = cols*cell_width+(cols+1)*gap
    title_font = ImageFont.truetype(str(FONT), font_size+8)
    header_lines = wrap(title, title_font, width-2*gap)
    header = (font_size+16)*len(header_lines)+2*gap
    labels = [wrap(f"{i+1:02d} · {p['role']} · {p['label']}\n{p['shot_id']} · {p['timestamp_s']:.3f} s", font, cell_width) for i,p in enumerate(selections)]
    caption = max(len(lines) for lines in labels)*(font_size+6)+gap
    stride = fh+caption+gap
    rows = math.ceil(len(selections)/cols)
    height = header+rows*stride+gap
    require(width*height <= MAX_PIXELS and max(width,height) <= 65000, "Collage exceeds pixel/JPEG limits; choose a smaller explicit panel_scale")
    placements = []
    for i, p in enumerate(selections):
        x = gap+(i%cols)*(cell_width+gap)+(cell_width-fw)//2
        y = header+(i//cols)*stride
        placements.append({"id":p["id"],"selection_id":p["id"],"shot_id":p["shot_id"],"area_ids":p["area_ids"],
                           "frame_index":p["frame_index"],"timestamp_s":p["timestamp_s"],"bbox":[x,y,fw,fh],"scale":scale})
    return {"width":width,"height":height,"panels":placements}, (font, title_font, header_lines, labels, gap, cell_width)


def titles(audit):
    labels = {a["id"]:a["label"] for a in audit["areas"]}
    result = {}
    for s in audit["shots"]:
        result[s["shot"]] = f"Shot {s['shot'][5:]} · {' / '.join(labels[a] for a in s['area_ids'])} · {s['start_s']:.3f}–{s['end_s']:.3f} s · {s['end_s']-s['start_s']:.3f} detik"
    result["storyboard"] = f"{audit['id']} — {audit['identity']['name']} · {audit['shots'][-1]['end_s']:.3f} detik · {len(audit['shots'])} shot"
    return result


def expected_media(audit, source, config):
    heading = titles(audit)
    for s in audit["shots"]:
        metadata,_ = layout(s["panels"],source,heading[s["shot"]],columns=3 if len(s["area_ids"])==1 else config["columns"],scale=config["panel_scale"])
        yield {"path":f"media/{s['shot']}.jpg","kind":"shot-collage","shot_id":s["shot"],**metadata}, s["panels"], heading[s["shot"]], False
    choices = [p for s in audit["shots"] for p in s["overviews"]]
    metadata,_ = layout(choices, source, heading["storyboard"],single_row=True,scale=config["panel_scale"])
    yield {"path":"media/storyboard.jpg","kind":"storyboard","shot_id":None,**metadata}, choices, heading["storyboard"], True


def build_media(folder, audit, source_path, source, config):
    result, cache = [], {}
    for meta, selections, title, single in expected_media(audit, source, config):
        _, (font,title_font,header,labels,gap,cell_width) = layout(selections,source,title,single_row=single,
             columns=3 if meta["kind"]=="shot-collage" and len(next(s for s in audit["shots"] if s["shot"]==meta["shot_id"])["area_ids"])==1 else config["columns"],scale=config["panel_scale"])
        board = Image.new("RGB",(meta["width"],meta["height"]),"#f5f3ed")
        draw = ImageDraw.Draw(board)
        draw.multiline_text((gap,gap),"\n".join(header),font=title_font,fill="#21483e",spacing=8)
        for panel, caption in zip(meta["panels"], labels):
            index=panel["frame_index"]
            if index not in cache:
                cache[index]=extract_frame(source_path,index,source["video_stream_index"])
            with Image.open(io.BytesIO(cache[index])) as frame:
                picture=frame.convert("RGB")
            x,y,w,h = panel["bbox"]
            if picture.size != (w,h): picture=picture.resize((w,h),Image.Resampling.LANCZOS)
            board.paste(picture,(x,y))
            draw.multiline_text((x-(cell_width-w)//2,y+h+gap//2),"\n".join(caption),font=font,fill="#21483e",spacing=6)
        target=folder/meta["path"];target.parent.mkdir(parents=True,exist_ok=True)
        board.save(target,"JPEG",quality=config["jpeg_quality"],subsampling=0,optimize=False,progressive=False)
        result.append({**meta,"sha256":sha256(target)})
    return result


def crop_panel(folder, manifest, selection_id, output):
    matches=[(m,p) for m in manifest["media"] for p in m["panels"] if p["id"]==selection_id]
    require(len(matches)==1,"Unknown/nonunique panel selection")
    require(output.resolve()!=folder.resolve() and not output.resolve().is_relative_to(folder.resolve()), "Keep extracted panel outside accepted reference")
    m,p=matches[0];x,y,w,h=p["bbox"]
    with Image.open(folder/m["path"]) as picture:
        result=picture.crop((x,y,x+w,y+h))
    output.parent.mkdir(parents=True,exist_ok=True);result.save(output, "PNG")
    return {"output":str(output),"width":w,"height":h,"source_panel":selection_id}
