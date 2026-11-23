"""Media 2.2.0: explicit selections, shared shot blocks, bounded allocation."""
from __future__ import annotations
import io
import math
from PIL import Image, ImageDraw, ImageFont
from .common import read_json, require, sha256
from .media_v2_1_2 import FONT, BOLD_FONT, ROOT, wrap, require_english_style_names
from .camera_pattern import shot_pattern
from .video import extract_frame

LAYOUT = ROOT / 'tools/assets/layouts/media-2.2.0.json'
MAX_PIXELS = 60_000_000
MAX_BYTES = 95 * 1024 * 1024


def preflight(width, height, path):
    require(width > 0 and height > 0 and width * height <= MAX_PIXELS and max(width, height) <= 65000,
            f'{path}: pixel/JPEG limit exceeded; choose explicit panel/overview/storyboard scale')


def identity(audit):
    return f"{audit['id']} — {audit['identity']['primary_style']} — {audit['shots'][-1]['end_s']:.2f}s — {len(audit['shots'])} shot"


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
        ('time', FONT, 'time_size')]}
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
            name = ' / '.join((area_labels or {}).get(a,a) for a in p['area_ids'])
            caption = f"{p['shot_id'][5:]} · {name}"
            caption_lines = [(v,'caption_bold') for v in wrap(caption,fonts['caption_bold'],cell)]
            caption_lines += [(v,'caption') for v in wrap(f"Overview · {p['timestamp_s']:.2f}s",fonts['caption'],cell)]
        else:
            moment = p['role'] if p['role'] in {'start','end'} or not multi_area and p['role']=='middle' else p['label']
            caption = f"{p['shot_id']} {moment} {p['timestamp_s']:.2f}s"
            caption_lines = [(v,'caption') for v in wrap(caption,fonts['caption'],cell)]
        captions.append(caption_lines)
    placements=[];row_y=header;last_bottom=header
    for offset in range(0,len(selections),cols):
        chunk=selections[offset:offset+cols]
        cap_height=max(sum(line_height(key) for _,key in c) for c in captions[offset:offset+cols])
        for j,p in enumerate(chunk):
            cell_x=gap+j*(cell+gap);x=cell_x+(cell-fw)//2
            placements.append({k:p[k] for k in ('id','shot_id','area_ids','frame_index','timestamp_s')})
            placements[-1].update(selection_id=p['id'],bbox=[x,row_y,fw,fh],scale=scale)
            cy=row_y+fh+px('caption_gap')
            for text,key in captions[offset+j]:
                add(text,key,cell_x,cy,'caption');cy+=line_height(key)
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


def expected_media(audit, source, config):
    require_english_style_names(audit)
    labels={a['id']:a['label'] for a in audit['areas']}
    shots=[]
    for shot in audit['shots']:
        title={'title':f"SHOT {shot['shot'][5:]} · {' / '.join(labels[a] for a in shot['area_ids'])}",
               'subtitle':f"{shot['start_s']:.2f}–{shot['end_s']:.2f}s · {shot['end_s']-shot['start_s']:.2f}s"}
        meta,design=layout(shot['panels'],source,title,columns=3 if len(shot['area_ids'])==1 else config['columns'],
                           scale=config['panel_scale'],camera=shot['camera_summary'],pattern=shot_pattern(shot),multi_area=len(shot['area_ids'])>1)
        meta.update(path=f"media/{shot['shot']}.jpg",kind='shot-collage',shot_id=shot['shot'])
        shots.append(meta)
        yield meta,shot['panels'],design,False
    choices=[p for s in audit['shots'] for p in s['overviews']]
    meta,design=layout(choices,source,identity(audit),overview=True,area_labels=labels,scale=config['overview_scale'])
    meta.update(path='media/overview.jpg',kind='overview',shot_id=None)
    yield meta,choices,design,True
    spec=read_json(LAYOUT);scale=config['storyboard_scale']
    unit=max(source['width']*config['panel_scale'],spec['minimum_cell_width'])/spec['reference_panel_width']*scale
    gap=max(1,round(spec['block_gap']*unit));margin=max(1,round(spec['margin']*unit))
    width=max(round(m['width']*scale) for m in shots)
    font=ImageFont.truetype(str(BOLD_FONT),max(1,round(spec['identity_size']*unit)))
    header_lines=wrap(identity(audit),font,width-2*margin)
    header=margin+len(header_lines)*math.ceil(font.size*spec['line_height'])+margin
    height=header+sum(round(m['height']*scale) for m in shots)+gap*(len(shots)-1)
    preflight(width,height,'media/storyboard.jpg')
    panels=[];blocks=[];y=header
    for m in shots:
        w,h=round(m['width']*scale),round(m['height']*scale);require(w>0 and h>0,'Storyboard scale too small')
        x=(width-w)//2;sx,sy=w/m['width'],h/m['height']
        blocks.append({'shot_id':m['shot_id'],'bbox':[x,y,w,h],'scale':scale,'derived_from':m['path']})
        for p in m['panels']:
            px,py,pw,ph=p['bbox'];left,top=round(px*sx),round(py*sy)
            bw,bh=round((px+pw)*sx)-left,round((py+ph)*sy)-top
            require(bw>0 and bh>0,'Storyboard photo scale too small')
            panels.append({**p,'bbox':[x+left,y+top,bw,bh],'scale':p['scale']*scale})
        y+=h+gap
    yield {'path':'media/storyboard.jpg','kind':'storyboard','shot_id':None,'width':width,'height':height,'panels':panels,'blocks':blocks},[],{'font':font,'header_lines':header_lines,'margin':margin,'line_height':math.ceil(font.size*spec['line_height']),'spec':spec},False


def build_media(folder, audit, source_path, source, config):
    # Materialize/preflight metadata only, before allocating any output bitmap.
    all_media=list(expected_media(audit,source,config));result=[]
    for meta,selections,design,_ in all_media:
        canvas=Image.new('RGB',(meta['width'],meta['height']),design['spec']['background']);draw=ImageDraw.Draw(canvas)
        if meta['kind']=='storyboard':
            y=design['margin']
            for text in design['header_lines']:
                draw.text((design['margin'],y),text,font=design['font'],fill=design['spec']['foreground']);y+=design['line_height']
            for block in meta['blocks']:
                x,y,w,h=block['bbox']
                with Image.open(folder/block['derived_from']) as pic:
                    image=pic.convert('RGB')
                if image.size!=(w,h):image=image.resize((w,h),Image.Resampling.LANCZOS)
                canvas.paste(image,(x,y));image.close()
        else:
            for panel in meta['panels']:
                # Decode one frame at a time; no unbounded full-resolution frame cache.
                with Image.open(io.BytesIO(extract_frame(source_path,panel['frame_index'],source['video_stream_index']))) as pic:
                    image=pic.convert('RGB')
                x,y,w,h=panel['bbox']
                if image.size!=(w,h):image=image.resize((w,h),Image.Resampling.LANCZOS)
                canvas.paste(image,(x,y));image.close()
            for t in design['texts']:
                draw.text((t['x'],t['y']),t['text'],font=design['fonts'][t['font']],fill=design['spec']['foreground'])
        target=folder/meta['path'];target.parent.mkdir(parents=True,exist_ok=True)
        canvas.save(target,'JPEG',quality=config['jpeg_quality'],subsampling=0,optimize=False,progressive=False);canvas.close()
        require(target.stat().st_size<=MAX_BYTES,f"{meta['path']}: encoded file exceeds 95 MiB; choose explicit scale/quality")
        result.append({**meta,'sha256':sha256(target)})
    return result
