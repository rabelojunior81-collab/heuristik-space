# Reconstituição pública do tratamento

NÃO é captura literal do transporte. Objeto corrigido5b413a0331f89969e90a407bd237e872d58757129da3c37df7308a43a31ca3a3,475arquivos. O revisor recebeu required_inputs, controles novos e descrições de Docker/browser/workflow/recuperação.22controlesPASS, runtime inteiro HTTP/bytesDockerPASS; novo reciboIAB401entradas mais prova anterior de código idêntico; limitações de download/Markdown/reboot/aceite declaradas. Os trechos abaixo provêm do código local conferido do mesmo objeto.

## scripts/check_release.py

```
"""Bind the deployable object to a recorded consultative review and QA receipts."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_manifest():
    names = ['index.html', 'app.js', 'styles.css', '404.html', 'CNAME', '.nojekyll', 'Dockerfile',
             'compose.yaml', '.dockerignore', '.gitattributes', 'README.md', 'LICENSE', 'package.json',
             'CONTRIBUTING.md', 'SECURITY.md', 'CODE_OF_CONDUCT.md', 'CHANGELOG.md',
             'docs/ingestion-contract.json', 'docs/research/frozen-manifest.json',
             'docs/research/relations.json', 'docs/SPEC.md', 'docs/SPEC-ADDENDUM-0.2.md',
             'docs/SPEC-ADDENDUM-0.3.md', 'docs/GOVERNANCE.md', 'docs/ARCHITECTURE.md',
             'docs/OPERATIONS.md', 'docs/RESEARCH.md', 'docs/ASSETS.md', 'docs/ASSETS.json']
    files = {ROOT / name for name in names}
    for directory, pattern in [('assets', '**/*'), ('data', '**/*'), ('scripts', '*.py'),
                               ('tests', '*.py'), ('deploy', '*'),
                               ('.github/workflows', '*.yml'),
                               ('docs/research', 'batch-*-report.json'),
                               ('docs/research/external', '*.json')]:
        files.update(f for f in (ROOT / directory).glob(pattern) if f.is_file())
    return {f.relative_to(ROOT).as_posix(): sha(f) for f in sorted(files)}


def fingerprint(manifest):
    return hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def required_inputs(kind, current):
    runtime = {k for k in current if k.startswith(('data/', 'assets/'))}
    runtime |= {'index.html', 'app.js', 'styles.css', '404.html'}
    runtime |= {'docs/' + name for name in ['GOVERNANCE.md', 'ASSETS.md', 'ASSETS.json',
                                           'RESEARCH.md', 'ARCHITECTURE.md', 'OPERATIONS.md']}
    if kind=='admission':
        return {k for k in current if k.startswith('data/')}|{'scripts/validate.py','scripts/build_data.py','docs/ingestion-contract.json','docs/research/relations.json','docs/research/frozen-manifest.json','docs/ASSETS.json'}
    if kind=='controls':
        return {k for k in current if k.startswith(('scripts/','tests/','data/'))}
    if kind=='browser':
        return runtime | {'CNAME', '.nojekyll', 'scripts/package_site.py'}
    if kind=='docker':
        return runtime | {'Dockerfile', 'compose.yaml', '.dockerignore', 'deploy/nginx.conf',
                          'scripts/test_docker.py'}
    raise ValueError('Unknown QA kind')


def check():
    release = json.loads((ROOT / 'docs/release.json').read_text(encoding='utf8'))
    current = object_manifest()
    if current != release['object_files']:
        raise ValueError('Release object changed; reopen affected review/QA before resealing')
    review_file = ROOT / release['review_file']
    if sha(review_file) != release['review_sha256']:
        raise ValueError('Review receipt changed')
    review = json.loads(review_file.read_text(encoding='utf8'))
    if review['object_sha256'] != fingerprint(current) or review['unresolved_high'] != 0:
        raise ValueError('Review object differs or high findings remain open')
    receipts=release['qa_receipts']
    kinds=[r['kind'] for r in receipts]
    if set(kinds)!={'admission','controls','browser','docker'} or len(kinds)!=4:
        raise ValueError('All four distinct QA layers are required')
    if review.get('reviewer_model')==review.get('executor_model') or not review.get('reviewer_model') or not review.get('executor_model'):
        raise ValueError('Distinct reviewer model is required')
    for receipt in receipts:
        file = ROOT / receipt['file']
        if sha(file) != receipt['sha256']:
            raise ValueError('QA receipt changed: ' + receipt['file'])
        result = json.loads(file.read_text(encoding='utf8'))
        if result.get('status') != 'PASS':
            raise ValueError('QA not PASS: ' + receipt['file'])
        tested=result.get('tested_files',{})
        if not required_inputs(receipt['kind'],current)<=set(tested):
            raise ValueError('QA input coverage missing: '+receipt['kind'])
        if any(current.get(name)!=digest for name,digest in tested.items()):
            raise ValueError('QA refers to changed inputs: '+receipt['kind'])
    print('PASS release object', fingerprint(current), len(current), 'files')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args()
    check()

```

## tests/test_release.py

```
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

```

## scripts/test_docker.py

```
"""Probe only this Compose project; preserve receipts and keep the service running."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import subprocess
import time
from urllib.request import urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, encoding='utf8', stderr=subprocess.STDOUT).strip()


def inspect():
    cid = run('docker', 'compose', 'ps', '-q', 'web')
    return json.loads(run('docker', 'inspect', cid))[0]


def ready():
    for _ in range(45):
        state = inspect()
        if state['State'].get('Health', {}).get('Status') == 'healthy':
            return state
        time.sleep(1)
    raise AssertionError('Container did not become healthy in 45 seconds')


def main(output, exercise_restart):
    if output.exists():
        raise ValueError('Refusing to overwrite previous Docker receipt')
    from check_release import object_manifest,required_inputs
    initial_files=object_manifest()
    initial_inputs={name:initial_files[name] for name in required_inputs('docker',initial_files)}
    checks = []
    def need(ok, name):
        checks.append({'check': name, 'pass': bool(ok)})
        if not ok:
            raise AssertionError(name)
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'checks': checks}
    try:
        before = ready()
        host = before['HostConfig']
        need(before['Config']['User'] == '101:101', 'Non-root UID/GID')
        need(host['ReadonlyRootfs'], 'Read-only root filesystem')
        need('ALL' in host['CapDrop'] and any('no-new-privileges' in s for s in host['SecurityOpt']), 'Dropped capabilities / no new privileges')
        need(host['PortBindings']['8080/tcp'][0]['HostIp'] == '127.0.0.1', 'Loopback binding')
        need(host['RestartPolicy']['Name'] == 'unless-stopped', 'Restart policy')
        need(host['Memory'] == 128 * 1024 ** 2 and host['PidsLimit'] == 64, 'Resource bounds')
        need(run('docker', 'compose', 'exec', '-T', 'web', 'id', '-u') == '101', 'Effective process UID')
        runtime_names = [name for name in initial_inputs
                         if name.startswith(('assets/', 'data/', 'docs/'))
                         or name in ('index.html', 'app.js', 'styles.css', '404.html')]
        for name in sorted(runtime_names):
            with urlopen('http://127.0.0.1:4173/' + name, timeout=5) as response:
                body = response.read()
                need(response.status == 200 and body == (ROOT / name).read_bytes(), 'HTTP / bytes ' + name)
        with urlopen('http://127.0.0.1:4173/healthz', timeout=5) as response:
            need(response.read() == b'ok\n', 'Health HTTP response')
        try:
            urlopen('http://127.0.0.1:4173/unknown-heuristik-test-path', timeout=5)
            need(False, 'Unknown path rejected')
        except HTTPError as exc:
            need(exc.code == 404, 'Unknown path rejected')
        if exercise_restart:
            stopped=subprocess.run(['docker','compose','exec','-T','web','sh','-c','kill -TERM 1'],cwd=ROOT,capture_output=True)
            result['process_exit_probe_returncode']=stopped.returncode
            time.sleep(2)
            after = ready()
            need(after['Id'] == before['Id'] and after['RestartCount'] > before['RestartCount'], 'Automatic recovery after own process exit')
            run('docker', 'compose', 'up', '-d', '--force-recreate', 'web')
            recreated = ready()
            need(recreated['Id'] != before['Id'], 'Own service recreated')
            with urlopen('http://127.0.0.1:4173/data/knowledge.json', timeout=5) as response:
                need(response.read() == (ROOT/'data/knowledge.json').read_bytes(), 'Knowledge persists across recreation')
        current = inspect()
        current_files=object_manifest()
        need(all(current_files.get(name)==sha for name,sha in initial_inputs.items()),'Tested Docker inputs unchanged')
        result['tested_files']=initial_inputs
        result.update(status='PASS', image=current['Image'], health=current['State']['Health']['Status'], restart_count=current['RestartCount'], nginx=run('docker','compose','exec','-T','web','nginx','-v'), scope='Local image/HTTP/content, constraints and optional process-exit/recreation. Not host reboot, frozen-process auto-heal, Pages or human acceptance.')
    except Exception as exc:
        result.update(status='FAIL', error=str(exc))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(result['status'] != 'PASS')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--exercise-restart', action='store_true')
    args = ap.parse_args()
    main(args.out, args.exercise_restart)

```

## .github/workflows/pages.yml

```
name: Edition gates and Pages
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: pages-${{ github.ref }}
  cancel-in-progress: false
jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
      - uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6
        with:
          python-version: '3.14'
      - run: python scripts/validate.py
      - run: python -m unittest discover -s tests -v
      - run: node --check app.js
      - run: python scripts/check_release.py
      - run: python scripts/package_site.py --out _site
      - uses: actions/upload-pages-artifact@7b1f4a764d45c48632c6b24a0339c27f5614fb0b # v4
        with:
          path: _site
  deploy:
    if: github.event_name != 'pull_request' && github.ref == 'refs/heads/main'
    needs: validate
    runs-on: ubuntu-24.04
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Publish validated edition
        id: deployment
        uses: actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e # v4

```

Recuperação operacional: preservar intenção/base/candidato/stage/backup, comparar hashes antes de qualquer restauração, não apagar barreira para tentar novamente; estados e limites em docs/OPERATIONS.md. Não foi ensaiada perda de energia em cada instrução.
