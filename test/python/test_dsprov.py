import unittest
from zensols.cli import CliHarness
from zensols.persist import Stash
from zensols.dsprov import NoteSpan, AdmissionMatch, ApplicationFactory


class TestApplication(unittest.TestCase):
    def setUp(self):
        harn: CliHarness = ApplicationFactory.create_harness()
        self.stash: Stash = harn['dsprov_stash']

    def test_annotations(self):
        hadm_id = '139676'
        self.assertEqual(51, len(self.stash))
        self.assertTrue(hadm_id in self.stash)
        am: AdmissionMatch = self.stash[hadm_id]
        self.assertEqual(AdmissionMatch, type(am))
        self.assertEqual(hadm_id, am.hadm_id)
        self.assertEqual(4, len(am.note_matches))
        self.assertEqual(1, len(am.note_matches[0].antecedents))
        ds = am.note_matches[0].discharge_summary
        ant = am.note_matches[0].antecedents[0]
        self.assertEqual(NoteSpan, type(ds))
        self.assertEqual(NoteSpan, type(ant))
        self.assertEqual('902625', ant.note.row_id)
        should = '1.  Fat stranding and inflammatory change in the right lower quadrant in the'
        self.assertEqual(should, ant.text)
        self.assertNotEqual(should, ds.text)
        should = '1. Fat stranding and inflammatory change in the right lower quadrant in the'
        self.assertEqual(should, ds.norm_text)
