"""Media guidance and geometry on synthetic normal and multi-area takes."""
import copy
import unittest
from pathlib import Path
from PIL import Image
from . import test_prepare
from homeku.common import LibraryError, read_json
from homeku.media import build_media, expected_media
from homeku.render_assets import render_config
from homeku.video import frame_times, probe_video

ROOT = Path(__file__).resolve().parents[1]


class MediaTests(test_prepare.VideoFixture, unittest.TestCase):
    def inputs(self, name):
        source = self.video("camera-" + name)
        audit = read_json(ROOT / "audit/examples" / name / "audit.json")
        return source, audit, probe_video(source), frame_times(source)

    def test_collages_and_overview_use_approved_captions(self):
        for name in ("normal", "multi"):
            with self.subTest(name=name):
                source, audit, info, times = self.inputs(name)
                config = render_config(columns=2)
                plan = list(expected_media(audit, info, config, times))
                shot, overview, storyboard = [item[0] for item in plan]
                self.assertEqual(len(shot["panels"]), len(audit["shots"][0]["panels"]))
                self.assertEqual(len({p["bbox"][1] for p in shot["panels"]}),
                                 1 if name == "normal" else 2)
                self.assertEqual(len({p["bbox"][1] for p in overview["panels"]}), 1)
                self.assertEqual(len(storyboard["blocks"]), 1)
                art = plan[0][2]
                captions = [t for t in art["texts"] if t["region"] == "caption"]
                self.assertEqual(captions[0]["text"], "Start")
                self.assertEqual(captions[0]["font"], "caption_bold")
                self.assertEqual(captions[1]["text"], " · 0.00s")
                self.assertLess(art["fonts"][captions[1]["font"]].size,
                                art["fonts"][captions[0]["font"]].size)
                self.assertGreater(captions[0]["y"], shot["panels"][0]["bbox"][1])
                self.assertEqual([t["text"] for t in art["texts"] if t["region"] == "header_time"],
                                 ["0.00–1.20s · 1.20s"])
                output = self.work / name
                rows = build_media(output, audit, source, info, config, times, plan=plan)
                self.assertEqual(len(rows), len(audit["shots"]) + 2)
                for row in rows:
                    with Image.open(output / row["path"]) as img:
                        self.assertEqual(img.format, "JPEG")
                        self.assertEqual(img.size, (row["width"], row["height"]))

    def test_storyboard_blocks_stack_vertically_and_overview_does_not(self):
        _, audit, info, times = self.inputs("normal")
        second = copy.deepcopy(audit["shots"][0])
        second.update(shot="shot-02", start_s=1.2, end_s=2.4)
        audit["shots"].append(second)
        plan = list(expected_media(audit, info, render_config(), times))
        overview, storyboard = [meta for meta, _, _ in plan[-2:]]
        left, right = [p["bbox"] for p in overview["panels"]]
        self.assertEqual(left[1], right[1])
        self.assertGreater(right[0], left[0] + left[2])
        top, bottom = [p["bbox"] for p in storyboard["blocks"]]
        self.assertGreater(bottom[1], top[1] + top[3])
        self.assertEqual(len(plan), 4)

    def test_oversize_geometry_is_rejected_in_layout(self):
        _, audit, info, times = self.inputs("normal")
        info["width"] = info["height"] = 15000
        with self.assertRaisesRegex(LibraryError, "pixel/JPEG limit"):
            list(expected_media(audit, info, render_config(), times))

    def test_manifest_has_off_panel_evidence_without_full_pts_and_crops(self):
        from homeku.audit_session import mark_viewed
        from homeku.authoring import complete, prepare
        from homeku.common import dumps, sha256
        from homeku.media import crop_panel, crop_storyboard
        from homeku.package_manifest import build_manifest, validate_frame_map
        source, audit, info, times = self.inputs("normal")
        work = prepare(source, [], self.work / "audit")
        Path(work["audit"]).write_text(dumps(audit))
        logs = {"method": "Fixture", "limitations": "Synthetic fixture",
                "ai": {"provider": "fixture", "model": "fixture", "model_build": None}}
        Path(work["audit_info"]).write_text(dumps(logs))
        mark_viewed(work["session"], all_frames=True, all_passes=True)
        complete(work["audit"], session_path=work["session"])
        config = render_config()
        folder = self.work / "candidate"
        media = build_media(folder, audit, source, info, config, times)
        source_info = {**info, "path": "video/camera-normal.mp4", "sha256": sha256(source)}
        manifest = build_manifest(audit, source_info, read_json(Path(work["audit_info"])),
                                  sha256(Path(work["audit"])), config, times, media,
                                  purpose="fixture")
        validate_frame_map(manifest, audit, times)
        self.assertIn("2", manifest["frames"])
        self.assertLess(len(manifest["frames"]), len(times))
        self.assertNotIn(2, {p["frame_index"] for p in manifest["selections"]})
        p = crop_panel(folder, manifest, "s01-panel-01", self.work / "panel.png")
        with Image.open(self.work / "panel.png") as crop, Image.open(folder / p["location"]["path"]) as original:
            x, y, w, h = p["location"]["bbox"]
            self.assertEqual(crop.tobytes(), original.crop((x, y, x+w, y+h)).tobytes())
        block = crop_storyboard(folder, manifest, "shot-01", self.work / "block.jpg")
        with Image.open(self.work / "block.jpg") as crop:
            self.assertEqual(crop.size, (block["width"], block["height"]))
        manifest["frames"]["2"] += 0.001
        with self.assertRaisesRegex(LibraryError, "native"):
            validate_frame_map(manifest, audit, times)

    def test_long_titles_and_caption_labels_remain_within_layout(self):
        _, audit, info, times = self.inputs("multi")
        audit["areas"][0]["label"] = "Living dengan bukaan tinggi dan ceruk panjang di samping pintu"
        audit["shots"][0]["panels"][1]["label"] = "Peralihan menuju meja panjang dan rak penyimpanan dapur"
        plan = list(expected_media(audit, info, render_config(columns=1, storyboard_scale=.6), times))
        shot, _, design = plan[0]
        for row in design["texts"]:
            box = design["fonts"][row["font"]].getbbox(row["text"])
            self.assertGreaterEqual(row["x"] + box[0], 0)
            self.assertLessEqual(row["x"] + box[2], shot["width"])
            self.assertLessEqual(row["y"] + box[3], shot["height"])
        self.assertEqual(len({p["bbox"][1] for p in shot["panels"]}), 4)
