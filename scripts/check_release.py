"""Bind the deployable object to a recorded consultative review and QA receipts."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_manifest():
    names = ['index.html', 'app.js', 'styles.css', '404.html', 'CNAME', 'Dockerfile',
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
    if kind=='admission':
        return {k for k in current if k.startswith('data/')}|{'scripts/validate.py','scripts/build_data.py','docs/ingestion-contract.json','docs/research/relations.json','docs/research/frozen-manifest.json','docs/ASSETS.json'}
    if kind=='controls':
        return {k for k in current if k.startswith(('scripts/','tests/','data/'))}
    if kind=='browser':
        return {k for k in current if k.startswith('assets/')}|{'app.js','styles.css','index.html','data/knowledge.json','data/context.txt'}
    if kind=='docker':
        return {'Dockerfile','compose.yaml','deploy/nginx.conf','index.html','app.js','styles.css','data/knowledge.json','data/context.txt','assets/brand/heuristik-mark.svg'}
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
