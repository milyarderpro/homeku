"""Active media: explicit selections, shared blocks and bounded allocation."""
from __future__ import annotations
import io
import math
from PIL import Image, ImageDraw, ImageFont
from .common import read_json, require, safe_relative, sha256
from .render_assets import BOLD_FONT, FONT, LAYOUT, MAX_BYTES, MAX_PIXELS, titles, wrap
from .camera_pattern import shot_pattern
from .derivations import camera_summary, selections
from .video import extract_frame


def preflight(width, height, path):
    require(width > 0 and height > 0 and width * height <= MAX_PIXELS and max(width, height) <= 65000,
            f'{path}: pixel/JPEG limit exceeded; choose explicit panel/overview/storyboard scale')


def layout(selections, source, title, *, columns=3, scale=1.0, overview=False,
           area_labels=None, camera=None, pattern=None, multi_area=False):
    require(selections and math.isfinite(scale) and 0 < scale <= 1 and 1 <= columns <= 6, 'Invalid media layout')
    spec = read_json(LAYOUT)
    fw, fh = round(source['width'] * scale), round(source['height'] * scale)
    require(fw > 0 and fh > 0, 'Panel scale too small')
    cell = max(fw, spec['minimum_cell_width'])
    unit = cell / spec['reference_panel_width']
    px = lambda key: max(1, round(spec[key] * unit))
    gap, bottom = px('margin'), px('bottom_padding')
    cols = len(selections) if overview else min(columns, len(selections))
    width = cols * cell + (cols + 1) * gap
    # Reject impossible source dimensions before measuring text or allocating a bitmap.
    preflight(width, fh + 2 * gap, 'media layout')
    fonts = {key: ImageFont.truetype(str(path), px(size)) for key,path,size in [
        ('heading', BOLD_FONT, 'identity_size' if overview else 'heading_size'),
        ('caption', FONT, 'caption_size'), ('caption_bold', BOLD_FONT, 'caption_size'),
        ('time', FONT, 'time_size'), ('caption_time', FONT, 'caption_time_size')]}
    texts = []
    def line_height(key):return math.ceil(fonts[key].size * spec['line_height'])
    def add(text, key, x, y, region):
        texts.append({'text':text, 'font':key, 'x':x, 'y':y, 'region':region})
    def lines(text, key, x, y, available, region):
        for line in wrap(text, fonts[key], available):
            add(line,key,x,y,region);y += line_height(key)
        return y
    heading = title if isinstance(title,dict) else {'title':title,'subtitle':''}
    usable = width - 2 * gap
    y = gap
    if overview:
        y = lines(heading['title'],'heading',gap,y,usable,'title')
        header = max(y+gap,px('overview_header_height'))
    else:
        timing = heading.get('subtitle','')
        tw = fonts['time'].getlength(timing)
        room = usable - tw - 2 * gap
        if timing and room >= cell * 0.5:
            ty = gap + fonts['heading'].getmetrics()[0] - fonts['time'].getmetrics()[0]
            add(timing,'time',width-gap-tw,ty,'header_time')
            y = max(lines(heading['title'],'heading',gap,y,room,'title'), ty+line_height('time'))
        else:
            y = lines(heading['title'],'heading',gap,y,usable,'title')
            if timing:y = lines(timing,'time',gap,y,usable,'header_time')
        header = max(y+gap,px('header_height'))
    captions = []
    for p in selections:
        if overview:
            name=' / '.join((area_labels or {}).get(a,a) for a in p['area_ids'])
            rows=[[(v,'caption_bold')] for v in wrap(f"{p['shot_id'][5:]} · {name}",fonts['caption_bold'],cell)]
            rows += [[(v,'caption_time')] for v in wrap(f"Overview · {p['timestamp_s']:.2f}s",fonts['caption_time'],cell)]
        else:
            moment={'start':'Start','end':'End'}.get(p['role'])
            if moment is None:
                moment='Middle' if not multi_area and p['role']=='middle' else p['label']
            suffix=f" · {p['timestamp_s']:.2f}s"
            if fonts['caption_bold'].getlength(moment)+fonts['caption_time'].getlength(suffix)<=cell:
                rows=[[(moment,'caption_bold'),(suffix,'caption_time')]]
            else:
                rows=[[(v,'caption_bold')] for v in wrap(moment,fonts['caption_bold'],cell)]
                rows += [[(suffix.strip(),'caption_time')]]
        captions.append(rows)
    def caption_height(rows):
        return sum(max(line_height(key) for _,key in row) for row in rows)
    placements=[];row_y=header;last_bottom=header
    for offset in range(0,len(selections),cols):
        chunk=selections[offset:offset+cols]
        cap_height=max(caption_height(rows) for rows in captions[offset:offset+cols])
        for j,p in enumerate(chunk):
            cell_x=gap+j*(cell+gap);x=cell_x+(cell-fw)//2
            placements.append({'selection_id':p['id'], 'bbox':[x,row_y,fw,fh], 'scale':scale})
            cy=row_y+fh+px('caption_gap')
            for row in captions[offset+j]:
                ascent=max(fonts[key].getmetrics()[0] for _,key in row);cx=cell_x
                for text,key in row:
                    add(text,key,cx,cy+ascent-fonts[key].getmetrics()[0],'caption')
                    cx+=fonts[key].getlength(text)
                cy+=max(line_height(key) for _,key in row)
        last_bottom=row_y+fh+px('caption_gap')+cap_height
        row_y=last_bottom+gap
    if camera is not None:
        y=last_bottom+px('camera_gap')
        label='camera:';prefix=f" ({pattern or '—'}) "
        add(label,'caption_bold',gap,y,'camera_label')
        x=gap+fonts['caption_bold'].getlength(label)
        # The first line shares the label baseline; continuation starts at left margin.
        words=(prefix+camera).split();current='';first=True
        while words:
            available=width-gap-x
            word=words.pop(0)
            require(fonts['caption'].getlength(word)<=usable,'Camera word exceeds canvas width')
            trial=current+(' ' if current else ' ' if first else '')+word
            if fonts['caption'].getlength(trial)>available and current:
                add(current,'caption',x,y,'camera');y+=line_height('caption');x=gap;current=word;first=False
            elif fonts['caption'].getlength(trial)>available:
                y+=line_height('caption');x=gap;current=word;first=False
            else:current=trial
        if current:add(current,'caption',x,y,'camera')
        last_bottom=max(t['y']+fonts[t['font']].getbbox(t['text'])[3] for t in texts if t['region'].startswith('camera'))
    else:
        # Tight final padding uses the final visible glyph, rather than a spare line box.
        last_bottom=max(t['y']+fonts[t['font']].getbbox(t['text'])[3] for t in texts)
    height=math.ceil(last_bottom+bottom)
    preflight(width,height,'media layout')
    return {'width':width,'height':height,'panels':placements,'blocks':[]}, {'texts':texts,'fonts':fonts,'spec':spec}



def expected_media(audit, source, config, frames):
    labels = {a["id"]: a["label"] for a in audit["areas"]}
    headings = titles(audit)
    all_selections = list(selections(audit, frames))
    by_shot = {shot["shot"]: [] for shot in audit["shots"]}
    choices = []
    for selected in all_selections:
        if selected["role"] == "overview":
            choices.append(selected)
        else:
            by_shot[selected["shot_id"]].append(selected)
    shots = []
    for shot in audit["shots"]:
        sid = shot["shot"]
        panels = by_shot[sid]
        multi = len(shot["area_ids"]) > 1
        meta, design = layout(panels, source, headings[sid], columns=config["columns"] if multi else 3,
                              scale=config["panel_scale"], camera=camera_summary(shot),
                              pattern=shot_pattern(shot), multi_area=multi)
        meta.update(path=f"media/{sid}.jpg", kind="shot-collage")
        shots.append((sid, meta))
        yield meta, panels, design
    identity = headings["storyboard"]["title"]
    meta, design = layout(choices, source, identity, overview=True, area_labels=labels,
                          scale=config["overview_scale"])
    meta.update(path="media/overview.jpg", kind="overview")
    yield meta, choices, design
    spec=read_json(LAYOUT);scale=config['storyboard_scale']
    unit=max(source['width']*config['panel_scale'],spec['minimum_cell_width'])/spec['reference_panel_width']*scale
    gap=max(1,round(spec['block_gap']*unit));margin=max(1,round(spec['margin']*unit))
    width=max(round(m['width']*scale) for _, m in shots)
    font=ImageFont.truetype(str(BOLD_FONT),max(1,round(spec['identity_size']*unit)))
    header_lines=wrap(identity,font,width-2*margin)
    header=margin+len(header_lines)*math.ceil(font.size*spec['line_height'])+margin
    height=header+sum(round(m['height']*scale) for _, m in shots)+gap*(len(shots)-1)
    preflight(width,height,'media/storyboard.jpg')
    panels=[];blocks=[];y=header
    for sid, m in shots:
        w,h=round(m['width']*scale),round(m['height']*scale);require(w>0 and h>0,'Storyboard scale too small')
        x=(width-w)//2;sx,sy=w/m['width'],h/m['height']
        blocks.append({'shot_id':sid,'bbox':[x,y,w,h],'derived_from':m['path']})
        for p in m['panels']:
            px,py,pw,ph=p['bbox'];left,top=round(px*sx),round(py*sy)
            bw,bh=round((px+pw)*sx)-left,round((py+ph)*sy)-top
            require(bw>0 and bh>0,'Storyboard photo scale too small')
            panels.append({**p,'bbox':[x+left,y+top,bw,bh],'scale':p['scale']*scale})
        y+=h+gap
    yield {'path':'media/storyboard.jpg','kind':'storyboard','width':width,'height':height,'panels':panels,'blocks':blocks},[],{'font':font,'header_lines':header_lines,'margin':margin,'line_height':math.ceil(font.size*spec['line_height']),'spec':spec}



def render_one(folder, meta, selected, design, source_path, source, config):
    width, height = meta["width"], meta["height"]
    with Image.new("RGB", (width, height), design["spec"]["background"]) as canvas:
        draw = ImageDraw.Draw(canvas)
        color = design["spec"]["foreground"]
        if meta["kind"] == "storyboard":
            y = design["margin"]
            for title in design["header_lines"]:
                draw.text((design["margin"], y), title, font=design["font"], fill=color)
                y += design["line_height"]
            items = [(block["bbox"], folder / block["derived_from"]) for block in meta["blocks"]]
        else:
            items = [(panel["bbox"], choice) for panel, choice in zip(meta["panels"], selected, strict=True)]
        for (x, y, w, h), item in items:
            if meta["kind"] != "storyboard":
                item = io.BytesIO(extract_frame(source_path, item["frame_index"], source["video_stream_index"]))
            with Image.open(item) as picture:
                with picture.convert("RGB") as rgb:
                    if rgb.size == (w, h):
                        canvas.paste(rgb, (x, y))
                    else:
                        with rgb.resize((w, h), Image.Resampling.LANCZOS) as resized:
                            canvas.paste(resized, (x, y))
        for title in design.get("texts", []):
            draw.text((title["x"], title["y"]), title["text"], font=design["fonts"][title["font"]], fill=color)
        target = folder / meta["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(target, "JPEG", quality=config["jpeg_quality"], subsampling=0,
                    optimize=False, progressive=False)
    require(target.stat().st_size <= MAX_BYTES,
            f"{meta['path']}: encoded file exceeds 95 MiB; choose explicit scale/quality")
    return {**meta, "sha256": sha256(target)}


def build_media(folder, audit, source_path, source, config, frames, *, plan=None):
    if plan is None:
        plan = list(expected_media(audit, source, config, frames))
    return [render_one(folder, meta, selected, design, source_path, source, config)
            for meta, selected, design in plan]


def best_location(locations):
    order={'shot-collage':0,'overview':1,'storyboard':2}
    require(locations,'No stored photo location')
    return min(locations,key=lambda p:(-p['bbox'][2]*p['bbox'][3],order.get(p['kind'],3),p['path'],p['bbox']))


def verify_stored_media(folder, relative, digest):
    from .audit_performance import safe_path
    require(safe_relative(relative).startswith("media/"), "Invalid stored media location")
    path = safe_path(folder / relative)
    require(path.is_file() and sha256(path) == digest, f"Stored media unavailable or changed: {relative}")
    return path


def crop_panel(folder, manifest, selection_id, output):
    matches = [{"path": row["path"], "kind": row["kind"], "sha256": row["sha256"],
                "bbox": p["bbox"], "scale": p["scale"]}
               for row in manifest["media"] for p in row["panels"] if p["selection_id"] == selection_id]
    require(not output.resolve().is_relative_to(folder.resolve()),
            "Keep extracted panel outside accepted reference")
    chosen = best_location(matches)
    source = verify_stored_media(folder, chosen["path"], chosen["sha256"])
    x, y, w, h = chosen["bbox"]
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as picture, picture.crop((x, y, x + w, y + h)) as cropped:
        cropped.save(output, "PNG")
    return {"output": str(output), "width": w, "height": h, "source_panel": selection_id,
            "location": {key: value for key, value in chosen.items() if key != "sha256"}}


def crop_storyboard(folder, manifest, shot_id, output):
    require(not output.resolve().is_relative_to(folder.resolve()),
            "Keep extracted block outside accepted reference")
    board = next((row for row in manifest["media"] if row["kind"] == "storyboard"), None)
    block = next((item for item in board.get("blocks", []) if item["shot_id"] == shot_id),
                 None) if board else None
    require(block is not None, f"Unknown storyboard shot: {shot_id}")
    x, y, w, h = block["bbox"]
    output.parent.mkdir(parents=True, exist_ok=True)
    source = verify_stored_media(folder, board["path"], board["sha256"])
    with Image.open(source) as picture, picture.crop((x, y, x + w, y + h)) as cropped:
        if output.suffix.casefold() == ".png":
            cropped.save(output, "PNG")
        else:
            cropped.save(output, "JPEG", quality=95, subsampling=0)
    return {"output": str(output), "width": w, "height": h, "source_shot": shot_id,
            "location": {"path": board["path"], "bbox": block["bbox"]}}
