"""Classification sequence tests; no video audit is claimed."""
import copy
import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from homeku.camera_pattern import shot_pattern, video_pattern, validate_direction, provenance
from homeku.common import LibraryError


def shot(*directions):
    return {'phases':[{'phase':f'phase-{i+1:02d}','depth_direction':d,'start_s':i,'end_s':i+1,'evidence':['p-start']} for i,d in enumerate(directions)]}


class CameraPatternTests(unittest.TestCase):
    def test_sequence_and_neutral_phases(self):
        for values,expected in [(['IN'],'IN'),(['OUT'],'OUT'),(['NO IN/OUT','IN','IN'],'IN'),(['IN','NO IN/OUT','OUT','OUT','IN'],'IN → OUT → IN'),(['NO IN/OUT']*2,'NO IN/OUT'),(['IN',None,'OUT'],None),([],None)]:
            with self.subTest(values=values):self.assertEqual(shot_pattern(shot(*values)),expected)
    def test_video_has_exactly_one_slot_per_take(self):
        self.assertEqual(video_pattern([shot('IN'),shot('OUT','IN'),shot('NO IN/OUT'),shot(None)]),'IN – (OUT → IN) – NO IN/OUT – —')
    def test_missing_legacy_classification_is_not_inferred(self):
        self.assertIsNone(shot_pattern({'phases':[{'components':'Dolly-In (~2×)'}]}))
    def test_only_explicit_translation_is_checked(self):
        for motion in ['Orbit Left','Pan Right','Zoom-In','other']:
            validate_direction({'depth_direction':'OUT','components_parsed':[{'movement':motion}]})
        for direction in ['IN','NO IN/OUT']:
            with self.assertRaisesRegex(LibraryError,'conflicts'):
                validate_direction({'depth_direction':direction,'components_parsed':[{'movement':'Dolly-Out'}]})
        validate_direction({'depth_direction':None,'components_parsed':[{'movement':'Dolly-Out'}]})
        with self.assertRaisesRegex(LibraryError,'Split opposing'):
            validate_direction({'depth_direction':'IN','components_parsed':[{'movement':'Dolly-Out'},{'movement':'Dolly-In'}]})
    def test_provenance_keeps_neutral_and_unknown(self):
        s=shot('NO IN/OUT',None,'OUT');before=copy.deepcopy(s);p=provenance(s,3)
        self.assertEqual(s,before);self.assertEqual(len(p),3)
        self.assertEqual(p[1]['source_pointer'],'/shots/3/phases/1/depth_direction')
        self.assertIsNone(p[1]['depth_direction'])
