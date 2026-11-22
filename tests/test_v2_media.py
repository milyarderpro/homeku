"""Collage/photo provenance and pixel bounds, with real synthetic test frames."""
import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from tests.fixtures.factory import make_v2_inputs
from homeku.common import LibraryError,read_json,dumps,sha256
from homeku.exporter import assemble_v2
from homeku.media import layout, crop_panel
from homeku.reporting import render_config
from homeku.validation import validate_folder


class V2MediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name)
        cls.source,cls.audit,cls.info=make_v2_inputs(cls.root/"input",multi=True)
        result=assemble_v2(cls.source,cls.audit,cls.info,cls.root/"candidate",include_source=True,purpose="fixture",columns=3)
        cls.folder=Path(result["candidate"]);cls.manifest=read_json(cls.folder/"manifest.json")
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_dynamic_multi_row_collage_and_single_row_storyboard(self):
        items=self.manifest["media"];self.assertEqual(len(items),2)
        collage,board=items
        self.assertEqual(len(collage["panels"]),4)
        self.assertGreater(collage["panels"][3]["bbox"][1],collage["panels"][0]["bbox"][1])
        self.assertEqual(len({p["bbox"][1] for p in board["panels"]}),1)
        for m in items:
            for p in m["panels"]:
                x,y,w,h=p["bbox"]
                self.assertEqual((w,h),(96,160))
                self.assertLessEqual(x+w,m["width"]);self.assertLessEqual(y+h,m["height"])
        self.assertEqual(len(list((self.folder/"media").rglob("*.jpg"))),2)

    def test_normal_is_exactly_three_columns_and_no_duplicate_jpegs(self):
        source,audit,info=make_v2_inputs(self.root/"normal")
        result=assemble_v2(source,audit,info,self.root/"normal-output",purpose="fixture",include_source=True)
        m=read_json(Path(result["candidate"])/"manifest.json")["media"][0]
        self.assertEqual(len(m["panels"]),3)
        self.assertEqual(len({p["bbox"][1] for p in m["panels"]}),1)

    def test_crop_returns_only_photo_without_caption(self):
        target=self.root/"cropped.png"
        crop_panel(self.folder,self.manifest,"p-reveal",target)
        with Image.open(target) as pic:self.assertEqual(pic.size,(96,160))
        with self.assertRaisesRegex(LibraryError,"outside accepted"):
            crop_panel(self.folder,self.manifest,"p-reveal",self.folder/"extra.png")

    def test_bad_bbox_hash_and_native_pts_cannot_hide_in_manifest(self):
        import shutil
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/self.folder.name;shutil.copytree(self.folder,folder)
            manifest=copy.deepcopy(self.manifest);manifest["media"][0]["panels"][0]["bbox"][0]+=1
            (folder/"manifest.json").write_text(dumps(manifest))
            with self.assertRaisesRegex(LibraryError,"provenance"):
                validate_folder(folder,Path(d))

    def test_pixel_limit_checked_before_allocating_canvas(self):
        audit=read_json(self.audit);source={**self.manifest["source"],"width":9000,"height":9000}
        with self.assertRaisesRegex(LibraryError,"pixel/JPEG"):
            layout(audit["shots"][0]["panels"],source,"Fixture",columns=4)

    def test_dynamic_count_is_not_fixed_to_five(self):
        from homeku.models import validate_audit
        from homeku.video import frame_times
        audit=read_json(self.audit);shot=audit["shots"][0]
        for count in (4,6,8):
            mid_indices=list(range(4,10))[:count-2]
            selected=[copy.deepcopy(shot["panels"][0])]
            for index in mid_indices:
                p=copy.deepcopy(shot["panels"][1]);p.update(id=f"dynamic-{index}",frame_index=index,timestamp_s=index/10)
                selected.append(p)
            selected.append(copy.deepcopy(shot["panels"][-1]));shot["panels"]=selected
            # Evidence uses native-only frames so selected panel count is independent.
            for claim in audit["profile"]+shot["facts"]+shot["phases"]+shot["area_relations"]+audit["identity"]["style_relations"]:
                if claim["evidence"]:
                    claim["evidence"]=["frame:shot-01:4"] if not claim.get("area_ids") or claim["area_ids"]!=["kitchen-1"] else ["frame:shot-01:11"]
            validate_audit(audit,1.2,frame_times(self.source))
            meta,_=layout(selected,self.manifest["source"],"Fixture dynamic",columns=3)
            self.assertEqual(len(meta["panels"]),count)

    def test_overview_may_use_native_frame_outside_collage(self):
        from homeku.models import validate_audit
        from homeku.video import frame_times
        a=read_json(self.audit);p=a["shots"][0]["overviews"][0]
        p.update(frame_index=2,timestamp_s=0.2)
        validate_audit(a,1.2,frame_times(self.source))
        self.assertNotIn(2,[v["frame_index"] for v in a["shots"][0]["panels"]])

    def test_new_captions_are_bold_compact_and_do_not_repeat_labels(self):
        from homeku.media import titles
        a=read_json(self.audit);a["identity"]["primary_style"]="Organic Modern Cottage"
        p=copy.deepcopy(a["shots"][0]["panels"][:3])
        for panel,role,timestamp in zip(p,["start","middle","end"],[0,2.366666667,4.7]):
            panel.update(role=role,label="Tampilan awal yang tidak boleh berulang",timestamp_s=timestamp)
        meta,design=layout(p,{**self.manifest["source"],"width":720,"height":1280},titles(a)["shot-01"])
        texts=[t["text"] for t in design["texts"]]
        self.assertIn("Start",texts);self.assertIn("Middle",texts);self.assertIn("End",texts)
        self.assertIn(" · 2.37s",texts)
        self.assertLess(design["fonts"]["caption_time"].size,design["fonts"]["caption"].size)
        self.assertFalse(any("Tampilan awal" in t or "shot-01 ·" in t for t in texts))
        self.assertIn("Bold",design["fonts"]["heading"].getname()[1])
        self.assertIn("Bold",design["fonts"]["caption"].getname()[1])
        self.assertEqual(len({p["bbox"][1] for p in meta["panels"]}),1)

    def test_storyboard_uses_primary_style_and_same_shot_number_for_multiple_areas(self):
        from homeku.media import titles
        a=read_json(self.audit);a["identity"]["primary_style"]="Organic Modern Cottage";a["identity"]["name"]="Nama kreatif tidak dipakai"
        title=titles(a)["storyboard"]
        self.assertEqual(title["title"],f"{a['id']} — Organic Modern Cottage — 1.20s — 1 shot")
        panels=a["shots"][0]["overviews"]
        _,design=layout(panels,{**self.manifest["source"],"width":720,"height":1280},title,single_row=True,area_labels={"living-1":"Living room","kitchen-1":"Kitchen"})
        texts=[t["text"] for t in design["texts"]]
        self.assertIn("01 · Living room",texts);self.assertIn("01 · Kitchen",texts)
        self.assertIn("Overview · 1.10s",texts)
        self.assertGreater(design["caption_size"],28)

    def test_long_headers_and_captions_fit_without_overlapping_photos(self):
        a=read_json(self.audit);panels=a["shots"][0]["panels"]
        panels[1]["label"]="Entrance reveal through the open-plan living room toward the kitchen and garden"
        source={**self.manifest["source"],"width":720,"height":1280}
        meta,design=layout(panels,source,{"title":"A long storyboard or shot title "*12,"subtitle":"0.00–1.20s · 1.20s"},columns=3,multi_area=True)
        from PIL import ImageDraw
        draw=ImageDraw.Draw(Image.new("RGB",(1,1)))
        for text in design["texts"]:
            left,top,right,bottom=draw.textbbox((text["x"],text["y"]),text["text"],font=design["fonts"][text["font"]])
            self.assertGreaterEqual(left,0);self.assertLessEqual(right,meta["width"])
            self.assertGreaterEqual(top,0);self.assertLessEqual(bottom,meta["height"])
            for panel in meta["panels"]:
                x,y,w,h=panel["bbox"]
                self.assertFalse(left<x+w and right>x and top<y+h and bottom>y)
        texts=[t["text"] for t in design["texts"]]
        self.assertTrue(any("Entrance reveal" in t for t in texts))

    def test_legacy_20_candidate_stays_valid_with_original_snapshot(self):
        from unittest.mock import patch
        from homeku.common import snapshot_hash
        from homeku.reporting import render_config as original_config
        source,path,info=make_v2_inputs(self.root/"legacy20",rid="layout-legacy20")
        audit=read_json(path);audit["identity"].pop("style_names_language");path.write_text(dumps(audit))
        with patch("homeku.reporting.render_config",side_effect=lambda **kwargs:original_config(version="2.0.0",**kwargs)):
            result=assemble_v2(source,path,info,self.root/"old-layout",include_source=True,purpose="fixture")
        folder=Path(result["candidate"]);digest=snapshot_hash(folder)
        config=read_json(folder/"manifest.json")["render"]
        self.assertEqual(config["media"],"2.0.0");self.assertNotIn("bold_font_sha256",config)
        validate_folder(folder,self.root)
        self.assertEqual(snapshot_hash(folder),digest)

    def test_multi_area_middle_role_keeps_event_label_instead_of_generic_middle(self):
        from homeku.media import panel_label
        from homeku.reporting import panel_sequence
        a=read_json(self.audit);shot=a["shots"][0];panel=shot["panels"][1]
        panel.update(role="middle",label="Entrance reveal")
        self.assertEqual(panel_label(panel,True),"Entrance reveal")
        self.assertEqual(panel_label(panel,False),"Middle")
        self.assertIn("Entrance reveal",panel_sequence(shot,render_config()))
        _,design=layout(shot["panels"],self.manifest["source"],"Multi area",multi_area=True)
        self.assertTrue(any("Entrance reveal" in t["text"] for t in design["texts"]))

    def test_wide_storyboard_keeps_all_caption_text_inside_its_own_column(self):
        a=read_json(self.audit);original=a["shots"][0]["overviews"][0]
        panels=[{**original,"id":f"wide-{i}"} for i in range(40)]
        meta,design=layout(panels,self.manifest["source"],"Many overview panels",single_row=True,area_labels={"living-1":"Living"})
        from PIL import ImageDraw
        draw=ImageDraw.Draw(Image.new("RGB",(1,1)))
        caption_texts=[t for t in design["texts"] if t["font"]!="heading"]
        # Each photo is centered in a cell of at least 320 pixels.
        centers=[p["bbox"][0]+p["bbox"][2]/2 for p in meta["panels"]]
        for text in caption_texts:
            left,top,right,bottom=draw.textbbox((text["x"],text["y"]),text["text"],font=design["fonts"][text["font"]])
            center=min(centers,key=lambda c:abs(c-(left+right)/2))
            self.assertGreaterEqual(left,center-160)
            self.assertLessEqual(right,center+160)
            self.assertLessEqual(bottom,meta["height"])

    def test_header_has_only_interval_and_duration_and_small_times_stay_with_panels(self):
        from homeku.media import titles
        a=read_json(self.audit);shot=a["shots"][0]
        meta,design=layout(shot["panels"],{**self.manifest["source"],"width":720,"height":1280},titles(a)["shot-01"],multi_area=True)
        header=[t for t in design["texts"] if t["region"]=="header_time"]
        titles_text=[t for t in design["texts"] if t["region"]=="title"]
        self.assertEqual(len(header),1)
        self.assertEqual(header[0]["text"],"0.00–1.20s · 1.20s")
        self.assertGreater(header[0]["x"],titles_text[0]["x"])
        captions=[t for t in design["texts"] if t["region"].startswith("caption")]
        for panel in shot["panels"]:
            self.assertTrue(any(f"{panel['timestamp_s']:.2f}s" in t["text"] for t in captions))
        self.assertLess(design["fonts"]["caption_time"].size,design["fonts"]["caption"].size)
        label=captions[0];time=captions[1]
        self.assertGreater(time["x"],label["x"])
        self.assertEqual(label["y"]+design["fonts"][label["font"]].getmetrics()[0],time["y"]+design["fonts"][time["font"]].getmetrics()[0])
        self.assertGreater(label["y"],meta["panels"][0]["bbox"][1]+meta["panels"][0]["bbox"][3])

    def test_titles_and_area_labels_shrink_fifteen_percent_and_time_font_is_subordinate(self):
        from homeku import media_v2_1
        panels=read_json(self.audit)["shots"][0]["panels"]
        source={**self.manifest["source"],"width":720,"height":1280}
        for board in (False,True):
            _,old=media_v2_1.layout(panels,source,"Readable title",single_row=board)
            _,new=layout(panels,source,"Readable title",single_row=board)
            for key in ("heading_size","caption_size"):
                self.assertAlmostEqual(new[key],old[key]*0.85,delta=0.51)
            if not board:
                self.assertAlmostEqual(new["fonts"]["time"].size/new["heading_size"],0.75,delta=0.02)

    def test_previous_21_candidate_keeps_its_layout_and_snapshot(self):
        from unittest.mock import patch
        from homeku.common import snapshot_hash
        from homeku.reporting import render_config as original_config
        source,path,info=make_v2_inputs(self.root/"legacy21",rid="layout-legacy21",multi=True)
        with patch("homeku.reporting.render_config",side_effect=lambda **kwargs:original_config(version="2.1.0",**kwargs)):
            result=assemble_v2(source,path,info,self.root/"old-layout21",include_source=True,purpose="fixture")
        folder=Path(result["candidate"]);digest=snapshot_hash(folder)
        validate_folder(folder,self.root)
        self.assertEqual(snapshot_hash(folder),digest)
        self.assertEqual(read_json(folder/"manifest.json")["render"]["media"],"2.1.0")

    def test_single_column_multi_area_header_wraps_without_losing_timing(self):
        a=read_json(self.audit);panels=a["shots"][0]["panels"]
        meta,design=layout(panels,self.manifest["source"],{"title":"SHOT 01 · Exterior Living room Kitchen","subtitle":"0.00–1.20s · 1.20s"},columns=1,multi_area=True)
        from PIL import ImageDraw
        draw=ImageDraw.Draw(Image.new("RGB",(1,1)))
        for t in design["texts"]:
            left,top,right,bottom=draw.textbbox((t["x"],t["y"]),t["text"],font=design["fonts"][t["font"]])
            self.assertGreaterEqual(left,0);self.assertLessEqual(right,meta["width"])
            self.assertLessEqual(bottom,meta["height"])
            for p in meta["panels"]:
                x,y,w,h=p["bbox"]
                self.assertFalse(left<x+w and right>x and top<y+h and bottom>y)

    def test_previous_211_candidate_stays_valid_and_uses_its_frozen_layout(self):
        from unittest.mock import patch
        from homeku.common import snapshot_hash
        from homeku.reporting import render_config as original_config
        source,path,info=make_v2_inputs(self.root/"legacy211",rid="layout-legacy211")
        with patch("homeku.reporting.render_config",side_effect=lambda **kwargs:original_config(version="2.1.1",**kwargs)):
            result=assemble_v2(source,path,info,self.root/"old-layout211",include_source=True,purpose="fixture")
        folder=Path(result["candidate"]);digest=snapshot_hash(folder)
        validate_folder(folder,self.root)
        self.assertEqual(snapshot_hash(folder),digest)
        self.assertEqual(read_json(folder/"manifest.json")["render"]["media"],"2.1.1")
