"""Report dispatcher; accepted renderers and their templates remain immutable."""
import re
import math
from . import reporting_v2_legacy as legacy
from .common import require, sha256
from .media import FONT, BOLD_FONT

ROOT=legacy.ROOT
TEMPLATES={**legacy.TEMPLATES,'2.2.0':ROOT/'tools/assets/templates/analysis-2.2.0.md','2.2.1':ROOT/'tools/assets/templates/analysis-2.2.1.md','2.2.2':ROOT/'tools/assets/templates/analysis-2.2.2.md','2.2.3':ROOT/'tools/assets/templates/analysis-2.2.3.md'}
number=legacy.number
table=legacy.table
panel_sequence=legacy.panel_sequence


def render_config(*,quality=91,scale=1.0,columns=4,version='2.1.2',overview_scale=1.0,storyboard_scale=1.0):
    if version not in {'2.2.0','2.2.1','2.2.2','2.2.3'}:
        require(overview_scale==1.0 and storyboard_scale==1.0,'Combined media scales require renderer 2.2.0')
        return legacy.render_config(quality=quality,scale=scale,columns=columns,version=version)
    from .media_v2_2 import LAYOUT
    config={'report':version,'media':'2.2.0','template_sha256':sha256(TEMPLATES[version]),
            'font_sha256':sha256(FONT),'bold_font_sha256':sha256(BOLD_FONT),'layout_sha256':sha256(LAYOUT),
            'jpeg_quality':quality,'panel_scale':scale,'columns':columns,
            'overview_scale':overview_scale,'storyboard_scale':storyboard_scale}
    verify_renderer(config)
    return config


def verify_renderer(config):
    if config['report'] not in {'2.2.0','2.2.1','2.2.2','2.2.3'}:return legacy.verify_renderer(config)
    from .media_v2_2 import LAYOUT
    from jsonschema import Draft202012Validator
    from .common import read_json
    version=config['report']
    schemas={'2.2.0':'v2-1','2.2.1':'v2-2','2.2.2':'v2-3','2.2.3':'v2-4'}
    schema=read_json(ROOT/f'docs/contracts/manifest-{schemas[version]}.schema.json')['properties']['render']
    require(not list(Draft202012Validator(schema).iter_errors(config)),'Invalid renderer 2.2.0 configuration')
    require(all(math.isfinite(config[key]) for key in ('panel_scale','overview_scale','storyboard_scale')), 'Media scales must be finite')
    for key,path in [('template_sha256',TEMPLATES[version]),('font_sha256',FONT),('bold_font_sha256',BOLD_FONT),('layout_sha256',LAYOUT)]:
        require(config[key]==sha256(path),f'Versioned renderer {key} mismatch')


def render_report(audit,config):
    version=config['report']
    if version not in {'2.2.0','2.2.1','2.2.2','2.2.3'}:return legacy.render_report(audit,config)
    verify_renderer(config)
    if version=='2.2.3':
        from .reporting_v2_2_3 import render_report as implementation
    elif version=='2.2.2':
        from .reporting_v2_2_2 import render_report as implementation
    elif version=='2.2.1':
        from .reporting_v2_2_1 import render_report as implementation
    else:
        from .reporting_v2_2 import render_report as implementation
    return implementation(audit,TEMPLATES[version])


def review_report(audit,config,media_prefix=None):
    text=render_report(audit,config)
    if media_prefix:text=re.sub(r'\]\((media/[^)]+)\)',lambda m:f']({media_prefix}/{m[1]})',text)
    return text
