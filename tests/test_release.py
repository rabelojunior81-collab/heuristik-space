"""A green label alone must not satisfy the publication contract."""
from pathlib import Path
import json
import sys
import unittest
from unittest.mock import patch
import uuid

PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/'scripts'))
import check_release as gate


class ReleaseControls(unittest.TestCase):
    def setUp(self):
        self.root=PROJECT/'.runtime'/('release-test-'+uuid.uuid4().hex)
        (self.root/'docs/qa').mkdir(parents=True)
        names=['app.js','styles.css','index.html','data/knowledge.json','data/context.txt',
               'data/articles/example.json','404.html','CNAME','.nojekyll','.dockerignore',
               'docs/GOVERNANCE.md','docs/ASSETS.md','docs/RESEARCH.md',
               'docs/ARCHITECTURE.md','docs/OPERATIONS.md','scripts/package_site.py','scripts/test_docker.py',
               'Dockerfile','compose.yaml','deploy/nginx.conf','assets/brand/heuristik-mark.svg',
               'scripts/validate.py','scripts/build_data.py','docs/ingestion-contract.json',
               'docs/research/relations.json','docs/research/frozen-manifest.json','docs/ASSETS.json']
        self.current={name:'fixture-'+str(i) for i,name in enumerate(names)}
        self.release={'object_files':self.current,'review_file':'docs/review.json','qa_receipts':[]}
        self.write('docs/review.json',{'object_sha256':gate.fingerprint(self.current),'unresolved_high':0,
                                     'reviewer_model':'Terra','executor_model':'Sol'})
        self.release['review_sha256']=gate.sha(self.root/'docs/review.json')
        for kind in ['admission','controls','browser','docker']:
            name='docs/qa/'+kind+'.json'
            self.write(name,{'status':'PASS','tested_files':{key:self.current[key] for key in gate.required_inputs(kind,self.current)}})
            self.release['qa_receipts'].append({'kind':kind,'file':name,'sha256':gate.sha(self.root/name)})
        self.save()

    def write(self,name,obj):
        (self.root/name).write_text(json.dumps(obj),encoding='utf8')

    def save(self):
        self.write('docs/release.json',self.release)

    def invoke(self):
        with patch.object(gate,'ROOT',self.root),patch.object(gate,'object_manifest',return_value=self.current):
            return gate.check()

    def test_all_bound_layers_pass(self):
        self.invoke()

    def test_empty_qa_does_not_pass(self):
        self.release['qa_receipts']=[]
        self.save()
        with self.assertRaisesRegex(ValueError,'four distinct QA'):
            self.invoke()

    def test_rehashed_stale_browser_receipt_does_not_pass(self):
        name='docs/qa/browser.json'
        value=json.loads((self.root/name).read_text())
        value['tested_files']['app.js']='old-version-hash'
        self.write(name,value)
        for receipt in self.release['qa_receipts']:
            if receipt['kind']=='browser':receipt['sha256']=gate.sha(self.root/name)
        self.save()
        with self.assertRaisesRegex(ValueError,'changed inputs: browser'):
            self.invoke()

    def mutate_reviewed_file(self, name):
        self.current[name]='new-reviewed-version'
        self.release['object_files']=self.current
        review=json.loads((self.root/'docs/review.json').read_text())
        review['object_sha256']=gate.fingerprint(self.current)
        self.write('docs/review.json',review)
        self.release['review_sha256']=gate.sha(self.root/'docs/review.json')
        # Rebind other layers so the named layer must detect its own stale input.
        for receipt in self.release['qa_receipts']:
            if receipt['kind'] in ('admission','controls'):
                self.write(receipt['file'],{'status':'PASS','tested_files':{
                    key:self.current[key] for key in gate.required_inputs(receipt['kind'],self.current)}})
                receipt['sha256']=gate.sha(self.root/receipt['file'])
        self.save()

    def test_changed_lazy_body_requires_new_browser_qa(self):
        self.mutate_reviewed_file('data/articles/example.json')
        with self.assertRaisesRegex(ValueError,'changed inputs: browser'):
            self.invoke()

    def test_changed_packaged_document_requires_new_docker_qa(self):
        self.mutate_reviewed_file('docs/OPERATIONS.md')
        browser=self.release['qa_receipts'][2]
        self.write(browser['file'],{'status':'PASS','tested_files':{
            key:self.current[key] for key in gate.required_inputs('browser',self.current)}})
        browser['sha256']=gate.sha(self.root/browser['file'])
        self.save()
        with self.assertRaisesRegex(ValueError,'changed inputs: docker'):
            self.invoke()


if __name__=='__main__':
    unittest.main()
