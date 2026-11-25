"""Coverage and evidence regressions for the compact format."""
import unittest
from .test_audit_preflight import normal
from homeku.audit_quality import validate_audit_logs, validate_frame_reviews
from homeku.common import LibraryError
from homeku.derivations import frame_map, selections
from homeku.package_manifest import validate_frame_map
from homeku.video import selected_indices


class AuditQualityTests(unittest.TestCase):
    def setUp(self):
        self.audit = normal()
        self.times = [i / 10 for i in range(12)]
        self.info = {"duration_s": 1.2, "fps": {"numerator": 10, "denominator": 1}}

    def review(self, rate, start=0, end=1.2, native=False):
        indices = selected_indices(self.times, start, end, rate, native=native)
        return {"shot_id": "shot-01", "start_s": start, "end_s": end,
                "mode": "frame-by-frame" if native else "sampling",
                "sampling_fps": None if native else rate, "selected_frame_indices": indices,
                "viewed_frame_indices": indices, "reason": "Fixture coverage"}

    def test_sparse_or_gapped_pass_cannot_replace_baseline(self):
        for passes in ([self.review(1)], [self.review(6, start=.2)]):
            with self.subTest(passes=passes), self.assertRaisesRegex(LibraryError, "6 FPS/native"):
                validate_frame_reviews(passes, self.audit["shots"], None, self.info, times=self.times)

    def test_evidence_outside_baseline_requires_explicit_declaration(self):
        logs = {"method": "Fixture", "limitations": "Fixture only",
                "ai": {"provider": "fixture", "model": "fixture", "model_build": None},
                "reviewed_ranges": [{"start_s": 0, "end_s": 1.2, "mode": "sampling"}],
                "frame_reviews": [self.review(6)]}
        self.assertNotIn(6, logs["frame_reviews"][0]["viewed_frame_indices"])
        with self.assertRaisesRegex(LibraryError, "not actually declared viewed"):
            validate_audit_logs(logs, self.audit, None, self.info, times=self.times)
        logs["frame_reviews"].append(self.review(6, .6, .7, native=True))
        validate_audit_logs(logs, self.audit, None, self.info, times=self.times)

    def test_palette_evidence_is_in_frame_map_and_requires_viewing(self):
        design = self.audit["design"]
        design.update(house_type={"value": "Tower House", "state": "uncertain", "evidence": [0]},
                      palette=[{"value": "Putih", "role": "Dominan", "hex": "#F0E8DA",
                                "state": "observed", "evidence": [4]}])
        logs = {"method": "Fixture", "limitations": "Fixture only",
                "ai": {"provider": "fixture", "model": "fixture", "model_build": None},
                "reviewed_ranges": [{"start_s": 0, "end_s": 1.2, "mode": "sampling"}],
                "frame_reviews": [self.review(6), self.review(6, .6, .7, native=True)]}
        self.assertEqual(frame_map(self.audit, self.times)["4"], .4)
        with self.assertRaisesRegex(LibraryError, "not actually declared viewed"):
            validate_audit_logs(logs, self.audit, None, self.info, times=self.times)
        logs["frame_reviews"].append(self.review(6, .4, .5, native=True))
        validate_audit_logs(logs, self.audit, None, self.info, times=self.times)

    def test_production_start_participates_in_viewed_and_offline_frame_validation(self):
        shot = self.audit["shots"][0]
        shot["composition"]["production_start"] = {
            "frame_index": 4, "composition_summary": "Framing jernih setelah transisi."}
        reviews = [self.review(6), self.review(6, .6, .7, native=True)]
        logs = {"method": "Fixture", "limitations": "Fixture only",
                "ai": {"provider": "fixture", "model": "fixture", "model_build": None},
                "reviewed_ranges": [{"start_s": 0, "end_s": 1.2, "mode": "sampling"}],
                "frame_reviews": reviews}
        frames = frame_map(self.audit, self.times)
        manifest = {"frames": frames, "selections": list(selections(self.audit, frames)), "audit": logs}
        self.assertEqual(frames["4"], .4)
        self.assertNotIn(4, {item["frame_index"] for item in manifest["selections"]})
        path = "/shots/0/composition/production_start/frame_index"
        with self.assertRaisesRegex(LibraryError, "/frame_reviews: frame not actually declared viewed for " + path):
            validate_audit_logs(logs, self.audit, None, self.info, times=self.times)
        with self.assertRaisesRegex(LibraryError, "/frame_reviews: frame not actually declared viewed for " + path):
            validate_frame_map(manifest, self.audit)
        reviews.append(self.review(6, .4, .5, native=True))
        validate_audit_logs(logs, self.audit, None, self.info, times=self.times)
        validate_frame_map(manifest, self.audit)
        frames["4"] = shot["end_s"]
        with self.assertRaisesRegex(LibraryError, path + ": frame PTS"):
            validate_frame_map(manifest, self.audit)

    def test_adjacent_baseline_passes_cover_shot_and_gaps_do_not(self):
        rows = [self.review(6, end=.5), self.review(6, start=.5)]
        validate_frame_reviews(rows, self.audit["shots"], None, self.info, times=self.times)
        rows[1] = self.review(6, start=.6)
        with self.assertRaisesRegex(LibraryError, "6 FPS/native"):
            validate_frame_reviews(rows, self.audit["shots"], None, self.info, times=self.times)
