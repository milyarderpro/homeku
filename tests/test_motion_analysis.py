"""Optional real OpenCV tests run in CI and the isolated motion environment."""
import importlib.util
import json
import unittest
from unittest.mock import patch
from PIL import Image,ImageDraw
from tests.test_camera_notation import CameraCase
from homeku.motion_analysis import dependencies,interval,motion_hints
from homeku.authoring import prepare
from homeku.common import sha256,LibraryError

class MotionFallbackTests(unittest.TestCase):
    def test_missing_dependency_is_nonfatal(self):
        im=Image.new("RGB",(100,100))
        with patch("homeku.motion_analysis.dependencies",return_value=None):
            self.assertEqual(interval(im,im,.2)["status"],"unavailable")
    def test_invalid_pts_is_rejected_before_tracking(self):
        im=Image.new("RGB",(100,100))
        for dt in [0,-1,float("inf"),float("nan")]:
            with self.assertRaises(LibraryError):interval(im,im,dt)

@unittest.skipUnless(importlib.util.find_spec("cv2") and importlib.util.find_spec("numpy"),"Optional motion dependencies not installed")
class MotionAnalysisTests(CameraCase):
    def test_known_2d_transform_and_native_delta_time(self):
        import cv2 as cv
        import numpy as np
        rng=np.random.default_rng(45)
        a=rng.integers(0,256,(240,320),dtype=np.uint8)
        matrix=np.array([[1.02,0,4],[0,1.02,-3]],dtype=np.float64)
        b=cv.warpAffine(a,matrix,(320,240))
        first=Image.fromarray(a);second=Image.fromarray(b)
        r=interval(first,second,.4)
        self.assertEqual(r["status"],"ok");self.assertGreaterEqual(r["inliers"],8)
        self.assertAlmostEqual(r["scale_2d"],1.02,delta=.015)
        self.assertAlmostEqual(r["dx_fraction"],7.2/320,delta=.008)
        self.assertAlmostEqual(r["dx_fraction_per_s"],r["dx_fraction"]/.4)
    def test_textureless_is_insufficient_not_static_verdict(self):
        im=Image.new("RGB",(160,240),"white");r=interval(im,im,.2)
        self.assertEqual(r["status"],"insufficient")
        self.assertNotIn("movement",r)
    def test_session_cache_reuse_and_no_audit_or_viewed_mutation(self):
        prep=prepare(self.source,[],self.work/"authoring")
        from pathlib import Path
        session=Path(prep["session"]);audit=Path(prep["audit"])
        before=(audit.read_bytes(),session.read_bytes())
        result=motion_hints(session,"shot-01",max_frames=6,width=160)
        self.assertLessEqual(len(result["indices"]),6);self.assertFalse(result["reused"])
        with patch("homeku.motion_analysis.interval",side_effect=AssertionError("must reuse statistics")):
            again=motion_hints(session,"shot-01",max_frames=6,width=160)
        self.assertTrue(again["reused"])
        self.assertEqual(before,(audit.read_bytes(),session.read_bytes()))
        for forbidden in ("movement","confidence","viewed_frame_indices"):
            self.assertNotIn(forbidden,result)
    def test_scope_and_work_budget_are_bounded(self):
        prep=prepare(self.source,[],self.work/"authoring")
        for kw in [{"max_frames":1000},{"width":5000},{"start":-1}]:
            with self.assertRaises(LibraryError):motion_hints(prep["session"],"shot-01",**kw)
