"""Version dispatcher and deterministic access to stored photographs."""
from PIL import Image
from . import media_v2_1_2 as legacy
from .common import require

FONT=legacy.FONT
BOLD_FONT=legacy.BOLD_FONT
MAX_PIXELS=legacy.MAX_PIXELS
SUPPORTED_MEDIA=(*legacy.SUPPORTED_MEDIA,'2.2.0')
wrap=legacy.wrap
seconds=legacy.seconds
panel_label=legacy.panel_label
require_english_style_names=legacy.require_english_style_names
titles=legacy.titles


def layout(*args,version='2.1.2',**kwargs):
    if version=='2.2.0':
        from .media_v2_2 import layout as new_layout
        return new_layout(*args,**kwargs)
    return legacy.layout(*args,version=version,**kwargs)


def expected_media(audit,source,config):
    if config['media']=='2.2.0':
        from .media_v2_2 import expected_media as implementation
    else:implementation=legacy.expected_media
    yield from implementation(audit,source,config)


def build_media(folder,audit,source_path,source,config):
    if config['media']=='2.2.0':
        from .video_cache import ACTIVE
        if ACTIVE.get() is not None:
            from .video_cache import cached_media
            return cached_media(folder,audit,source_path,source,config)
        from .media_v2_2 import build_media as implementation
    else:implementation=legacy.build_media
    return implementation(folder,audit,source_path,source,config)


def best_location(locations):
    order={'shot-collage':0,'overview':1,'storyboard':2}
    require(locations,'No stored photo location')
    return min(locations,key=lambda p:(-p['bbox'][2]*p['bbox'][3],order.get(p['kind'],3),p['path'],p['bbox']))


def crop_panel(folder,manifest,selection_id,output):
    matches=[{'path':m['path'],'kind':m['kind'],'bbox':p['bbox'],'scale':p['scale']}
             for m in manifest['media'] for p in m['panels'] if p['id']==selection_id]
    require(matches,'Unknown panel selection')
    require(not output.resolve().is_relative_to(folder.resolve()),'Keep extracted panel outside accepted reference')
    chosen=best_location(matches);x,y,w,h=chosen['bbox']
    with Image.open(folder/chosen['path']) as picture:result=picture.crop((x,y,x+w,y+h))
    output.parent.mkdir(parents=True,exist_ok=True);result.save(output,'PNG');result.close()
    return {'output':str(output),'width':w,'height':h,'source_panel':selection_id,'location':chosen}


def render_missing_media(*args, **kwargs):
    from .media_incremental import render_missing_media as implementation
    return implementation(*args, **kwargs)
