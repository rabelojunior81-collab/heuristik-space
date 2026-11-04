"""Filesystem regression checks; semantic validation is exercised separately."""
from pathlib import Path
from datetime import datetime, timezone
import json
import sys
import unittest
from unittest.mock import patch
import uuid

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT/'scripts'))
import promote


class PromotionControls(unittest.TestCase):
    def setUp(self):
        self.root = PROJECT/'.runtime'/('promotion-test-'+uuid.uuid4().hex)
        (self.root/'data').mkdir(parents=True)
        (self.root/'docs').mkdir()
        (self.root/'data/value.json').write_text('{"v":0}', encoding='utf8')
        (self.root/'docs/ingestion-contract.json').write_text('{"blog_commit":"fixture-cut"}', encoding='utf8')
        self.survey = self.root/'docs/blog-status.json'
        self.survey.write_text(json.dumps({'status':'PASS','source_base':'https://rabelus.com.br',
            'frozen_edition_commit':'fixture-cut','checked_at':datetime.now(timezone.utc).isoformat()}), encoding='utf8')

    def candidate(self, name, value):
        path = self.root/name
        path.mkdir()
        (path/'value.json').write_text(json.dumps({'v':value}), encoding='utf8')
        return path

    def test_two_cycles_with_same_final_directory_name(self):
        a = self.candidate('candidate-a',1)
        b = self.candidate('candidate-b',2)
        # Here the contract is intentionally a stub: this test isolates real directory
        # movement/barriers. Other tests validate the full 373-source candidate.
        with patch.object(promote,'ROOT',self.root), patch.object(promote,'validate',return_value={
                'status':'PASS','contract_sha256':'filesystem-fixture-only','blog_survey_sha256':promote.digest(self.survey)}):
            promote.promote(a,self.root/'docs/runs/cycle-a/promotion',self.survey)
            promote.promote(b,self.root/'docs/runs/cycle-b/promotion',self.survey)
        self.assertEqual(json.loads((self.root/'data/value.json').read_text())['v'],2)
        backups = list((self.root/'.runtime').glob('backup-*'))
        self.assertEqual(len(backups),2)
        self.assertEqual(sorted(json.loads((p/'value.json').read_text())['v'] for p in backups),[0,1])
        self.assertFalse((self.root/'.runtime/promotion-pending.json').exists())

    def test_candidate_changes_during_staging_are_rejected(self):
        candidate=self.candidate('candidate-a',1)
        real_copy=promote.shutil.copytree
        def racing_copy(source,destination):
            value=real_copy(source,destination)
            (candidate/'value.json').write_text('{"v":99}',encoding='utf8')
            return value
        before=(self.root/'data/value.json').read_bytes()
        with patch.object(promote,'ROOT',self.root), patch.object(promote,'validate',return_value={
                'status':'PASS','contract_sha256':'fixture','blog_survey_sha256':promote.digest(self.survey)}), patch.object(promote.shutil,'copytree',side_effect=racing_copy):
            with self.assertRaisesRegex(ValueError,'Candidate changed'):
                promote.promote(candidate,self.root/'docs/runs/race/promotion',self.survey)
        self.assertEqual((self.root/'data/value.json').read_bytes(),before)

    def test_pending_interruption_preserves_current_data(self):
        candidate = self.candidate('candidate-a',1)
        runtime = self.root/'.runtime'
        runtime.mkdir()
        barrier = runtime/'promotion-pending.json'
        barrier.write_text('{"status":"UNKNOWN"}',encoding='utf8')
        before = (self.root/'data/value.json').read_bytes()
        with patch.object(promote,'ROOT',self.root), patch.object(promote,'validate',return_value={
                'status':'PASS','contract_sha256':'filesystem-fixture-only','blog_survey_sha256':promote.digest(self.survey)}):
            with self.assertRaisesRegex(ValueError,'Interrupted/pending'):
                promote.promote(candidate,self.root/'docs/runs/cycle/promotion',self.survey)
        self.assertEqual((self.root/'data/value.json').read_bytes(),before)
        self.assertEqual(barrier.read_text(),'{"status":"UNKNOWN"}')


if __name__=='__main__':
    unittest.main()
