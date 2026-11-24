"""2.1 compatibility, report/media and complete technical pipeline in isolated roots."""
import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from PIL import Image, ImageDraw
from jsonschema import Draft202012Validator
from tests.fixtures.factory import make_v2_inputs, isolated_root, make_folder, package_folder
from homeku.common import LibraryError, dumps, read_json, sha256, snapshot_hash
from homeku.models import validate_audit, schema_check, evidence_inventory
from homeku.reporting import render_config, render_report
from homeku.exporter import assemble_v2, review_v2, export_v2
from homeku.validation import validate_folder, CODE_ROOT, extract_package
from homeku.engine import ingest, check, build
from homeku.reader import read_reference, extract_panel, extract_shot_image, search
from homeku.media import best_location
from homeku.media_v2_2 import layout, expected_media
from homeku.generation import render


class V21CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shared=tempfile.TemporaryDirectory();base=Path(cls.shared.name)
        cls.source,cls.path,cls.info=make_v2_inputs(base/'input',rid='new-media',multi=True,version='2.1')
        cls.audit=read_json(cls.path)
        result=assemble_v2(cls.source,cls.path,cls.info,base/'candidate',purpose='fixture',include_source=True,columns=3)
        cls.template=Path(result['candidate']);cls.manifest=read_json(cls.template/'manifest.json')
    @classmethod
    def tearDownClass(cls):cls.shared.cleanup()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.work=Path(self.temp.name)
        self.folder=self.work/'candidate'/self.template.name;shutil.copytree(self.template,self.folder)
        self.root=isolated_root(self.work/'repo')
    def tearDown(self):self.temp.cleanup()
    def publish(self):
        result=export_v2(self.folder,self.work/'packages',snapshot_hash(self.folder))
        outcome=ingest(self.root,[Path(result['package'])]);self.assertEqual(outcome['results'][0]['status'],'imported',outcome)
        return Path(result['package'])
    def test_schemas_are_local_and_version_specific(self):
        for name in ['audit','manifest','reference-reader','search-index']:
            s=read_json(CODE_ROOT/f'docs/contracts/{name}-v2-1.schema.json');Draft202012Validator.check_schema(s)
            self.assertNotIn('"$ref"',json.dumps(s))
        with self.assertRaises(LibraryError):schema_check(self.audit,'audit-v2.schema.json')
        for mutation in [lambda a:a['shots'][0]['overviews'][0].pop('composition_summary'),lambda a:a['shots'][0]['phases'][0].pop('depth_direction'),lambda a:a['shots'][0]['overviews'][0].update(composition_summary='line\nbreak'),lambda a:a['shots'][0]['phases'][0].update(depth_direction='OUT'),lambda a:a['shots'][0].update(camera_summary='bad\nnotation')]:
            a=copy.deepcopy(self.audit);mutation(a)
            with self.assertRaises(LibraryError):validate_audit(a)
    def test_media_n_plus_two_and_repeated_identity_locations(self):
        ms=self.manifest['media'];self.assertEqual([m['kind'] for m in ms],['shot-collage','overview','storyboard'])
        self.assertEqual(len(list((self.folder/'media').glob('*.jpg'))),3)
        self.assertEqual(len({p['bbox'][1] for p in ms[1]['panels']}),1)
        block=ms[2]['blocks'][0];self.assertEqual(block['derived_from'],ms[0]['path']);self.assertEqual(block['bbox'][2:], [ms[0]['width'],ms[0]['height']])
        _,model,_=validate_folder(self.folder,self.work);inventory=evidence_inventory(model)
        self.assertEqual(len(inventory['p-start']['locations']),2)
        self.assertEqual(inventory['p-start']['path'],'media/shot-01.jpg')
        self.assertEqual(inventory['overview-living']['path'],'media/overview.jpg')
    def test_caption_camera_fonts_and_text_boxes(self):
        a=copy.deepcopy(self.audit);source={**self.manifest['source'],'width':720,'height':1280}
        p=copy.deepcopy(a['shots'][0]['panels'][:3]);p[1].update(role='middle',label='Entrance reveal')
        _,d=layout(p,source,'Multi-area',multi_area=True)
        self.assertTrue(any('Entrance reveal' in t['text'] for t in d['texts']))
        for cols in (1,3,4):
            meta,design=layout(a['shots'][0]['panels'],source,{'title':'SHOT 01 · Living / Kitchen — '+('Long area ' * 5),'subtitle':'0.00–1.20s · 1.20s'},columns=cols,camera=a['shots'][0]['camera_summary']+' toward a distant garden window and the left kitchen counter.'*5,pattern='IN → OUT')
            draw=ImageDraw.Draw(Image.new('RGB',(1,1)))
            self.assertEqual(design['fonts']['caption'].size,44)
            camera=[t for t in design['texts'] if t['region'].startswith('camera')]
            self.assertEqual(camera[0]['text'],'camera:');self.assertEqual(camera[0]['font'],'caption_bold')
            self.assertTrue(all(t['font']=='caption' for t in camera[1:]))
            self.assertTrue(any('shot-01 start 0.00s' in t['text'] for t in design['texts']))
            for t in design['texts']:
                left,top,right,bottom=draw.textbbox((t['x'],t['y']),t['text'],font=design['fonts'][t['font']])
                self.assertGreaterEqual(left,0);self.assertLessEqual(right,meta['width']);self.assertLessEqual(bottom,meta['height'])
                for p in meta['panels']:
                    x,y,w,h=p['bbox'];self.assertFalse(left<x+w and right>x and top<y+h and bottom>y,(t,p))
            self.assertAlmostEqual(meta['height']-max(t['y']+design['fonts'][t['font']].getbbox(t['text'])[3] for t in camera),30,delta=1)
    def test_overview_uses_frame_not_present_in_collage(self):
        a=copy.deepcopy(self.audit);p=a['shots'][0]['overviews'][0];p.update(frame_index=2,timestamp_s=0.2)
        path=self.work/'audit.json';path.write_text(dumps(a));result=assemble_v2(self.source,path,self.info,self.work/'new',purpose='fixture',include_source=True)
        m=read_json(Path(result['candidate'])/'manifest.json');self.assertIn(2,[p['frame_index'] for p in m['media'][1]['panels']])
        self.assertNotIn(2,[p['frame_index'] for p in m['media'][0]['panels']])
    def test_report_six_sections_quotes_grouping_and_full_narratives(self):
        report=(self.folder/'analysis.md').read_text()
        self.assertEqual(sum(line.startswith('## ') for line in report.splitlines()),6)
        self.assertIn('| Shot | Time (s) | Duration | Area/Scene | Camera Movement |',report)
        self.assertNotIn('Gerakan singkat',report);self.assertNotIn('```',report)
        self.assertIn('**Camera Pattern:** IN.',report)
        self.assertIn('#### **A. Desain area**',report)
        self.assertIn('##### **living**',report)
        self.assertIn('##### **kitchen**',report)
        self.assertIn('![Kolase Shot 01](media/shot-01.jpg)',report)
        for d in self.audit['shots'][0]['design']:
            for key in ['architecture','furnishings','environment']:self.assertIn('> '+d[key],report)
        self.assertLess(report.index('**Lingkungan**'),report.index('##### **kitchen**'))
        for p in self.audit['shots'][0]['overviews']:self.assertIn('> '+p['composition_summary'],report)
        self.assertIn('**Camera:** '+self.audit['shots'][0]['camera_summary'],report)
        self.assertIn('**60–90 m²**',report)
        start=next(line for line in report.splitlines() if line.startswith('- **Camera Start:**'))
        composition=self.audit['shots'][0]['composition']
        for key in ['camera_position','camera_direction','view_angle']:self.assertIn(composition[key],start)
        self.assertNotIn(composition['camera_height'],start)
        self.assertNotIn(composition['camera_tilt'],start)
    def test_roundtrip_revision_and_no_video_stored_media_reads(self):
        receipt=review_v2(self.folder,self.work/'review.md');self.assertEqual(receipt['snapshot_sha256'],snapshot_hash(self.folder))
        pkg=self.publish();self.assertEqual(check(self.root)['references'],1)
        self.assertEqual(ingest(self.root,[pkg])['changed'],[])
        self.assertEqual(build(self.root,full=True)['changed'],[])
        entry=read_json(self.root/'data/registry.json')['references']['new-media'];self.assertEqual(entry['contract_version'],'2.1')
        full=read_reference(self.root,'new-media',part='full');self.assertEqual(full['schema_version'],'2.4')
        for key,value in self.audit.items():
            if key=='shots':
                for original,projected in zip(value,full['reference']['shots']):
                    for k,v in original.items():self.assertEqual(v,projected[k])
            else:self.assertEqual(value,full['reference'][key])
        for pointer,proof in full['provenance'].items():
            node=full
            for part in pointer.strip('/').split('/'):node=node[int(part)] if isinstance(node,list) else node[part]
            if proof.get('json'):
                node=self.audit
                for part in proof['source_pointer'].strip('/').split('/') if proof['source_pointer'] else []:node=node[int(part)] if isinstance(node,list) else node[part]
        area=read_reference(self.root,'new-media',part='area',shot='shot-01',area='kitchen-1')
        self.assertEqual(len(area['shot']['route']),2);self.assertEqual(len(area['shot']['design']),1)
        self.assertEqual(search(self.root,route=['living','kitchen'])['total'],1)
        source=self.root/'video/new-media.mp4';source.rename(source.with_suffix('.hidden'))
        for panel in ['p-start','overview-living']:
            extract_panel(self.root,'new-media',panel,self.work/f'{panel}.png')
        extract_shot_image(self.root,'new-media','shot-01',self.work/'shot.jpg')
        extract_shot_image(self.root,'new-media','shot-01',self.work/'block.png',from_storyboard=True)
        with Image.open(self.work/'block.png') as picture:self.assertEqual(picture.size,(self.manifest['media'][0]['width'],self.manifest['media'][0]['height']))
        with self.assertRaisesRegex(LibraryError,'Canonical source changed'):extract_panel(self.root,'new-media','p-start',self.work/'native.jpg',native=True)
    def test_snapshot_mutations_and_new_inventory_tampering_fail(self):
        for name in ['audit.json','analysis.md','manifest.json','media/overview.jpg','media/storyboard.jpg','media/shot-01.jpg']:
            p=self.folder/name;before=p.read_bytes();digest=snapshot_hash(self.folder);p.write_bytes(before+b' ')
            with self.assertRaisesRegex(LibraryError,'changed since'):export_v2(self.folder,self.work/'packages',digest)
            p.write_bytes(before)
        for change in [lambda m:m['media'][-1]['blocks'][0]['bbox'].__setitem__(0,1),lambda m:m['render'].update(storyboard_scale=.5),lambda m:m.update(contract_version='2.0')]:
            manifest=copy.deepcopy(self.manifest);change(manifest);(self.folder/'manifest.json').write_text(dumps(manifest))
            with self.assertRaises(LibraryError):validate_folder(self.folder,self.work)
        (self.folder/'manifest.json').write_text(dumps(self.manifest))
    def test_scaled_storyboard_bbox_and_best_available_resolution(self):
        for key in ['scale','overview_scale','storyboard_scale']:
            with self.assertRaisesRegex(LibraryError,'finite'):
                render_config(version='2.2.0',**{key:float('nan')})
        config=render_config(version='2.2.0',scale=.5,overview_scale=1.0,storyboard_scale=.5)
        media=list(expected_media(self.audit,self.manifest['source'],config));board=media[-1][0]
        for p in board['panels']:
            x,y,w,h=p['bbox'];self.assertLessEqual(x+w,board['width']);self.assertLessEqual(y+h,board['height']);self.assertGreater(w,0)
        candidates=[{'path':'z','kind':'storyboard','bbox':[0,0,720,1280],'scale':1},{'path':'a','kind':'overview','bbox':[0,0,360,640],'scale':.5}]
        self.assertEqual(best_location(candidates)['path'],'z')
        candidates.append({**candidates[0],'path':'b','kind':'shot-collage'})
        self.assertEqual(best_location(list(reversed(candidates)))['path'],'b')
    def test_media_limit_fails_before_bitmap_allocation(self):
        with patch('homeku.media_v2_2.Image.new',side_effect=AssertionError('must preflight')):
            with self.assertRaisesRegex(LibraryError,'pixel/JPEG'):
                list(expected_media(self.audit,{**self.manifest['source'],'width':9000,'height':9000},render_config(version='2.2.0')))
        a=copy.deepcopy(self.audit);a['shots']=[copy.deepcopy(a['shots'][0]) for _ in range(200)]
        with self.assertRaisesRegex(LibraryError,'pixel/JPEG'):
            list(expected_media(a,{**self.manifest['source'],'width':720,'height':1280},render_config(version='2.2.0')))
    def test_versioned_draft_keeps_old_source_default_and_rejects_cross_pair(self):
        source,path,info=make_v2_inputs(self.work/'old',rid='old-source')
        result=assemble_v2(source,path,info,self.work/'old-candidate',include_source=True,purpose='fixture')
        self.assertEqual(read_json(Path(result['candidate'])/'manifest.json')['render']['report'],'2.1.2')
        with self.assertRaisesRegex(LibraryError,'requires source 2.1'):assemble_v2(source,path,info,self.work/'wrong',version='2.2.0',purpose='fixture')
        with self.assertRaisesRegex(LibraryError,'requires renderer 2.2.0'):assemble_v2(self.source,self.path,self.info,self.work/'wrong21',version='2.1.2',purpose='fixture')
    def test_mixed_collection_and_300_model_index_remain_light(self):
        self.publish();legacy=make_folder(self.work/'legacy',rid='old-md')
        self.assertEqual(ingest(self.root,[package_folder(legacy,self.work/'old-md-r0001.zip')])['results'][0]['status'],'imported')
        source,path,info=make_v2_inputs(self.work/'oldjson',rid='old-json')
        result=assemble_v2(source,path,info,self.work/'oldjson-candidate',purpose='fixture',include_source=True)
        pkg=export_v2(Path(result['candidate']),self.work/'oldjson-packages',result['snapshot_sha256'])
        self.assertEqual(ingest(self.root,[Path(pkg['package'])])['results'][0]['status'],'imported')
        self.assertEqual(check(self.root)['references'],3)
        self.assertIsNone(read_reference(self.root,'old-json')['camera_pattern'])
        _,model,_=validate_folder(self.folder,self.work);models={}
        for i in range(300):
            rid=f'many-{i:03d}';m=copy.deepcopy(model);m['id']=rid;m['source']['path']=f'video/{rid}.mp4';models[rid]=m
        outputs=render(self.root,models);index=outputs['data/search-index.json']
        self.assertLess(len(index.encode()),4_000_000);self.assertNotIn('composition_summary',index);self.assertNotIn('frame_reviews',index)
        self.assertEqual(len(json.loads(index)['references']),300)
    def test_active_21_kit_pipeline_in_empty_workspace(self):
        from tests.test_audit import kit_builder
        workspace=self.work/'chat';workspace.mkdir()
        with zipfile.ZipFile(io.BytesIO(kit_builder.build_bytes())) as archive:archive.extractall(workspace)
        result=subprocess.run([sys.executable,str(workspace/'homeku_runtime.py'),'--output',str(workspace)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(read_json(workspace/'template-audit.json')['schema_version'],'2.4')
        info=self.work/'info.json';info.write_text(dumps(self.info))
        def run(*args):
            p=subprocess.run([sys.executable,str(workspace/'tools/audit.py'),*map(str,args)],capture_output=True,text=True,cwd=workspace)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr);return json.loads(p.stdout)
        inspected=run('inspect',self.source)
        self.assertEqual(inspected['source_sha256'],sha256(self.source))
        self.assertEqual(inspected['frame_count'],12)
        baseline=run('sample',self.source,'--output',self.work/'baseline','--shot-id','shot-01')
        self.assertEqual(baseline['review_record_template']['viewed_frame_indices'],[])
        native=run('sample',self.source,'--output',self.work/'native','--native','--start',0,'--end',.4,'--shot-id','shot-01','--reason','Synthetic portable test')
        self.assertEqual(native['selection']['mode'],'frame-by-frame')
        self.assertEqual(native['review_record_template']['viewed_frame_indices'],[])
        template=read_json(workspace/'template-audit.json')
        self.assertLessEqual(set(template['shots'][0]['overviews'][0]),set(self.audit['shots'][0]['overviews'][0]))
        self.assertIn('motion_observations',template['shots'][0]['phases'][0])
        draft=run('draft-v2',self.source,self.path,'--audit-info',info,'--output',self.work/'portable','--include-source')
        review=run('review',draft['candidate'],'--output',self.work/'review-new.md')
        package=run('export-v2',draft['candidate'],'--output',self.work/'portable-zips','--receipt',review['receipt'])
        self.assertEqual(package['snapshot_sha256'],draft['snapshot_sha256'])
        self.assertEqual(ingest(self.root,[Path(package['package'])])['results'][0]['status'],'imported')

    def test_explicit_new_revision_and_batch_failure_do_not_corrupt_state(self):
        self.publish();rid=self.audit['id'];entry=read_json(self.root/'data/registry.json')['references'][rid]
        a=copy.deepcopy(self.audit);a['revision']=2;a['shots'][0]['facts'][0]['value']='new accepted configuration'
        path=self.work/'revised-audit.json';path.write_text(dumps(a))
        result=assemble_v2(self.source,path,self.info,self.work/'revision',purpose='fixture',include_source=True,supersedes={'revision':1,'content_sha256':'0'*64})
        bad=export_v2(Path(result['candidate']),self.work/'bad',result['snapshot_sha256'])
        failed=ingest(self.root,[Path(bad['package'])]);self.assertEqual(failed['results'][0]['status'],'failed')
        self.assertEqual(read_json(self.root/'data/registry.json')['references'][rid],entry)
        result=assemble_v2(self.source,path,self.info,self.work/'revision',purpose='fixture',include_source=True,supersedes={'revision':1,'content_sha256':entry['content_sha256']})
        with patch('homeku.media.build_media',side_effect=AssertionError('export must not reencode')):
            good=export_v2(Path(result['candidate']),self.work/'good',result['snapshot_sha256'])
        broken=self.work/'broken-r0001.zip';broken.write_bytes(b'not a ZIP')
        outcome=ingest(self.root,[broken,Path(good['package'])]);self.assertEqual([r['status'] for r in outcome['results']],['failed','imported'])
        self.assertEqual(read_json(self.root/'data/registry.json')['references'][rid]['revision'],2)
        self.assertEqual(search(self.root,configuration='new accepted configuration')['total'],1)
        self.assertEqual(check(self.root)['references'],1)

    def test_normal_three_panels_and_scaled_render_decode(self):
        source,path,info=make_v2_inputs(self.work/'normal-new',rid='normal-new',version='2.1')
        result=assemble_v2(source,path,info,self.work/'normal-candidate',purpose='fixture',include_source=True,scale=.75,overview_scale=.5,storyboard_scale=.5)
        folder=Path(result['candidate']);manifest=read_json(folder/'manifest.json');validate_folder(folder,self.work)
        self.assertEqual(len(manifest['media'][0]['panels']),3)
        self.assertEqual(len({p['bbox'][1] for p in manifest['media'][0]['panels']}),1)
        for m in manifest['media']:
            with Image.open(folder/m['path']) as pic:self.assertEqual(pic.size,(m['width'],m['height']))
        report=(folder/'analysis.md').read_text();self.assertNotIn('##### **',report)
        self.assertNotIn('**Movement Timeline**',report)

    def test_mixed_neutral_unknown_phases_and_dynamic_panels(self):
        from homeku.markdown import component
        from homeku.camera_pattern import shot_pattern
        a=copy.deepcopy(self.audit);s=a['shots'][0];original=copy.deepcopy(s['phases'][0])
        s['phases']=[]
        for i,(start,end,raw,direction) in enumerate([(0,.4,'Orbit Left (~15°)','NO IN/OUT'),(.4,.8,'Dolly-Out (~1.3×)','OUT'),(.8,1.2,'Dolly-In (~1.3×)','IN')],1):
            phase=copy.deepcopy(original);phase.update(phase=f'phase-{i:02d}',start_s=start,end_s=end,components=raw,components_parsed=[component(raw)],depth_direction=direction)
            s['phases'].append(phase)
        s['camera_summary']=' → '.join(p['components'] for p in s['phases'])+'.'
        validate_audit(a);self.assertEqual(shot_pattern(s),'OUT → IN')
        report=render_report(a,render_config(version='2.2.0'));self.assertIn('**Camera Pattern:** (OUT → IN).',report)
        s['phases'][1]['depth_direction']=None;validate_audit(a);self.assertIsNone(shot_pattern(s))
        self.assertIn('**Camera Pattern:** —.',render_report(a,render_config(version='2.2.0')))
        for count in [4,6,8]:
            panels=[copy.deepcopy(s['panels'][0])]
            for index in range(1,count-1):
                p=copy.deepcopy(s['panels'][1]);p.update(id=f'event-{index}',frame_index=index,timestamp_s=index/10,role='reveal',label=f'Room reveal {index}');panels.append(p)
            panels.append(copy.deepcopy(s['panels'][-1]))
            meta,_=layout(panels,self.manifest['source'],'Dynamic continuous take',columns=3,camera=s['camera_summary'],pattern=shot_pattern(s))
            self.assertEqual(len(meta['panels']),count)
            self.assertGreater(meta['panels'][-1]['bbox'][1],meta['panels'][0]['bbox'][1])

    def test_shot_image_cli_reads_both_stored_forms_without_video(self):
        self.publish();source=self.root/'video/new-media.mp4';source.unlink()
        for args,name in [([], 'whole.jpg'),(['--from-storyboard'], 'block.png')]:
            result=subprocess.run([sys.executable,str(CODE_ROOT/'tools/library.py'),'--root',str(self.root),'shot-image','new-media','shot-01','--output',str(self.work/name),*args],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertTrue((self.work/name).is_file())
