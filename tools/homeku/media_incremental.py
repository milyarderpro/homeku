"""Byte-compatible subset executor; registered media2.2.0 stays immutable."""
import io
from PIL import Image, ImageDraw
from .media import expected_media
from .media_v2_2 import MAX_BYTES
from .video import extract_frame
from .common import require, sha256

def render_missing_media(folder, audit, source_path, source, config, selected_paths):
    # Materialize/preflight metadata only, before allocating any output bitmap.
    all_media=[entry for entry in expected_media(audit,source,config) if entry[0]['path'] in selected_paths];result=[]
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
