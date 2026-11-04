"""Controls must reject coherent-looking but unsupported generated editions."""
import copy
import json
from pathlib import Path
import sys
import os
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate as gate
DATA = Path(os.environ.get('HEURISTIK_TEST_DATA', str(ROOT/'data')))
from build_data import Body, term_pattern


class AdmissionControls(unittest.TestCase):
    def altered(self, file_name, change):
        original = gate.load
        def load(path):
            value = original(path)
            if Path(path).name == file_name:
                value = copy.deepcopy(value)
                change(value)
            return value
        with patch.object(gate, 'load', side_effect=load):
            result = gate.validate(ROOT, DATA)
        self.assertEqual(result['status'], 'FAIL', result)
        return result

    def test_current_edition(self):
        result = gate.validate(ROOT, DATA)
        self.assertEqual(result['status'], 'PASS', result['failures'][:5])

    def test_missing_source_even_with_reduced_count(self):
        def change(k):
            k['sources'].pop()
            k['edition']['read_count'] -= 1
            k['edition']['source_count'] -= 1
        result=self.altered('knowledge.json', change)
        self.assertIn('Independent source contract differs',result['failures'])

    def test_missing_reader_receipt(self):
        self.altered('batch-1-report.json', lambda report: report['posts'].pop())

    def test_unread_source(self):
        self.altered('knowledge.json', lambda k: k['sources'][0].update(read_status='not_read'))

    def test_changed_source_hash(self):
        self.altered('knowledge.json', lambda k: k['sources'][0].update(sha256='0' * 64))

    def test_unlocatable_quote(self):
        def change(k):
            k['sources'][0]['claims'][0]['evidence_excerpt'] = 'fabricated evidence 9f1a'
        result=self.altered('knowledge.json', change)
        self.assertTrue(any('Evidence excerpt not found' in f for f in result['failures']))

    def test_truncated_article(self):
        slug = gate.load(DATA / 'knowledge.json')['sources'][0]['slug']
        result=self.altered(slug + '.json', lambda article: article.update(body=article['body'][:80]))
        self.assertTrue(any('Extracted source body mismatch' in f for f in result['failures']))

    def test_orphan_and_forged_relation(self):
        def change(k):
            k['relations'][0]['source_ids'] = ['unknown-source']
            k['relations'][0]['evidence'][0]['excerpt'] = 'fabricated 81f5'
        self.altered('knowledge.json', change)

    def test_failed_source_survey(self):
        self.altered('blog-status.json', lambda survey: survey.update(status='FAIL'))

    def test_retired_source_domain(self):
        self.altered('knowledge.json', lambda k: k['edition'].update(source_domain='rabelus.online'))

    def test_asset_without_provenance(self):
        result=self.altered('ASSETS.json', lambda assets: assets.pop())
        self.assertIn('Asset inventory/provenance differs',result['failures'])

    def test_missing_reference(self):
        self.altered('knowledge.json', lambda k: k['references'].pop())

    def test_extractor_nested_inline_and_tail(self):
        parser = Body()
        parser.feed('<h1>Title</h1><header>private chrome</header>'
                    '<div class="post-content"><p>Start <b>bold</b>.</p>'
                    '<div><p>Nested</p><script>not body</script></div>'
                    '<p>Final sentinel</p></div><footer>not article</footer>')
        text = parser.text()
        self.assertIn('Start bold.', text)
        self.assertIn('Nested', text)
        self.assertTrue(text.endswith('Final sentinel'))
        self.assertNotIn('not body', text)
        self.assertNotIn('not article', text)
        self.assertNotIn('Title', text)
        self.assertFalse(parser.capture)

    def test_bus_is_not_busca(self):
        matcher = term_pattern(['Bus'])
        self.assertFalse(matcher.search('a busca retornou um resultado'))
        self.assertTrue(matcher.search('o bus conecta fontes'))


if __name__ == '__main__':
    unittest.main()
