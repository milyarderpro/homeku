"""Human report 2.2.4: layout only, preserving every authored narrative."""
import re
from .common import require
from .reporting_v2_legacy import number
from .media import require_english_style_names
from .camera_pattern import video_pattern


def table(columns, rows):
    def cell(value):
        return str(value).replace("|", r"\|")
    return "\n".join(["| " + " | ".join(columns) + " |",
                      "| " + " | ".join("---" for _ in columns) + " |"] +
                     ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows])


def quote(value):
    return '\n'.join('> '+line for line in value.splitlines())


def render_report(a,template):
    require(a['schema_version']=='2.5','Renderer 2.2.4 requires audit source 2.5')
    require_english_style_names(a)
    from .report_validation import display_audit, validate_report
    source = a
    a = display_audit(a, escape=True)
    text=template.read_text(encoding='utf-8')
    headings=re.findall(r'^## [1-6]\. .+$',text,re.M)
    groups=re.findall(r'^#### \*\*[ABC]\. .+\*\*$',text,re.M)
    require(len(headings)==6 and len(groups)==3,'Invalid registered report 2.2.0 template')
    i,z=a['identity'],a['size'];labels={v['id']:v['label'] for v in a['areas']}
    names=lambda ids:' / '.join(labels[k] for k in ids)
    time=lambda n:f'{n:.2f}'
    parts=[f"# {a['id']} — {i['name']}",'<a id="profil-dna"></a>',headings[0],
           '\n'.join(f'- **{label}:** {value}' for label,value in [
               ('Nama desain',i['name']),('Gaya utama',f"**{i['primary_style']}**"),('Pengaruh gaya',i['influences']),
               ('Gaya interior',i['interior_style']),('Ciri khas','; '.join(i['distinctive_features'])),
               ('Warna & material',i['palette']),('Suasana dan lingkungan',i['mood_environment'])]),headings[1],
           table(['Aspek','Estimasi visual'],[(f'**{label}**',value) for label,value in [
               ('Ukuran rumah',z['scale']),('Bentuk bangunan',z['massing']),('Lantai & bentuk atap',z['vertical']),
               ('Tapak bangunan',z['footprint']),('Proporsi utama',z['proportions']),
               ('Perkiraan luas lantai',f"**{number(z['floor_area_m2']['min'])}–{number(z['floor_area_m2']['max'])} m²**")]]),
           headings[2],a['timeline_notes'],'**Camera Pattern:** '+video_pattern(a['shots'])+'.',
           table(['Shot','Time (s)','Duration','Area/Scene','Camera Movement'],[
               (s['shot'][5:],f"{time(s['start_s'])}–{time(s['end_s'])}",f"{s['end_s']-s['start_s']:.2f}s",names(s['area_ids']),s['camera_summary']) for s in a['shots']]),
           headings[3],'![Overview wide seluruh area](media/overview.jpg)']
    for s in a['shots']:
        for p in s['overviews']:
            parts += [f"**Shot {s['shot'][5:]} · {names(p['area_ids'])} · {p['timestamp_s']:.2f}s**",quote(p['composition_summary'])]
    parts += [headings[4],'![Storyboard seluruh shot dengan panel dan camera](media/storyboard.jpg)',headings[5]]
    for index,s in enumerate(a['shots']):
        sid=s['shot'];multi=len(s['area_ids'])>1;c=s['composition']
        if index:parts.append('---')
        parts += [f'<a id="{sid}"></a>',f"### Shot {sid[5:]} · {names(s['area_ids'])}",
                  f"**Time:** {time(s['start_s'])}–{time(s['end_s'])}s · **Duration:** {s['end_s']-s['start_s']:.2f}s"]
        if multi:parts.append('**Shot Type:** Continuous shot · Multi area · No cut.')
        parts += [f'![Kolase Shot {sid[5:]}](media/{sid}.jpg)',groups[0]]
        # Each authored design group appears once, in first visible area order.
        order={aid:j for j,aid in enumerate(s['area_ids'])}
        for d in sorted(s['design'],key=lambda d:min(order[aid] for aid in d['area_ids'])):
            if multi:parts.append(f"##### **{names(d['area_ids'])}**")
            for title,key in [('Arsitektur','architecture'),('Furnitur & dekorasi','furnishings'),('Lingkungan','environment')]:
                parts += [f'**{title}**',quote(d[key])]
        parts.append(groups[1])
        rows=[('Fokus',c['focus']),('Camera Start','; '.join(c[key] for key in ['camera_position','camera_direction','view_angle'])),
              ('Framing',c['start_composition']+' → '+c['end_composition']),('Lighting',c['lighting'])]
        if multi:
            rows += [('Area',names(s['area_ids'])),('Rute kamera',' → '.join(f"{labels[r['area_id']]} ({r['start_s']:.2f}–{r['end_s']:.2f}s; {r['connector']}; {r['focus']})" for r in s['route']) or 'Kamera tidak berpindah antararea.')]
        parts.append('\n'.join(f'- **{key}:** {value}' for key,value in rows))
        if multi:
            visibility='; '.join(f"{labels[aid]}: "+', '.join(f"{max(v['start_s'],s['start_s']):.2f}–{min(v['end_s'],s['end_s']):.2f}s" for v in next(a for a in a['areas'] if a['id']==aid)['visible_intervals'] if v['start_s']<s['end_s'] and v['end_s']>s['start_s']) for aid in s['area_ids'])
            parts += ['**Hubungan antararea**','\n'.join(f'- **{key}:** {value}' for key,value in [
                ('Penghubung area','; '.join(r['description'] for r in s['area_relations']) or 'Hubungan belum dipastikan.'),
                ('Peralihan',visibility),('Orientasi ruang',s['continuity'])])]
        parts += [groups[2],s['camera_simple'],'**Tempo:** '+s['rhythm']]
        if s['journey_dna']:parts.append('**Alur visual:** '+s['journey_dna'])
        if multi or len(s['phases'])>1:
            parts += ['**Movement Timeline**',table(['Time (s)','Area & fokus','Camera Movement','Tempo'],[
                (f"{p['start_s']:.2f}–{p['end_s']:.2f}",names(p['area_ids'])+' · '+p['focus'],p['components'],
                 '; '.join(t['description'] for t in s['tempo_profile'] if t['start_s']<p['end_s'] and t['end_s']>p['start_s'])) for p in s['phases']])]
        parts.append('**Camera:** '+s['camera_summary'])
    return validate_report('\n\n'.join(parts)+'\n', source)
