# Reconstituição pública do pacote inicial

NÃO é captura literal do transporte. A exportação nativa estava opaca; a tentativa original foi invalidada e preservada. A revisão real recebeu trechos/descrições públicos do objeto c959c686edd9bad9604433ed5e434cd5d0733af4f9b42117f2350be10e76307c. Estes arquivos legíveis documentam o código público pertinente e o escopo, sem declarar igualdade byte a byte ao prompt enviado. Ferramentas/shell/browser/subagentes/persistência proibidos no pedido; isolamento mecânico não comprovado.

Objeto: pesquisa373fontes/906claims/55relações/39referências; app estático com busca/filtros/cópia; quatro camadas deQA; Docker local reinício/recriação; CI/Pages/TLS/público ainda devidos naquele momento. Revisão estratégica por GPT-6.1-Terra, contextualizada/não independente.

## scripts/promote.py — revisão pública7359dea

```python
"""Promote a validated data candidate with durable intent and recoverable backup.
Git/deployment are separate transactions. Pending interrupted promotion fails closed.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,shutil
from validate import validate,load,digest
ROOT=Path(__file__).resolve().parents[1]
def manifest(path):return {str(f.relative_to(path)).replace('\\','/'):digest(f) for f in sorted(path.rglob('*')) if f.is_file()}
def durable(path,obj):
    with path.open('x',encoding='utf8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
def promote(candidate,run,blog_receipt):
    candidate=Path(candidate).resolve();run=Path(run).resolve()
    if not candidate.is_relative_to(ROOT) or not run.is_relative_to(ROOT):raise ValueError('Candidate and run must stay inside this project')
    run.mkdir(parents=True,exist_ok=True)
    if not candidate.is_dir() or candidate==ROOT/'data':raise ValueError('Separate candidate directory required')
    candidate_before=manifest(candidate)
    result=validate(ROOT,candidate)
    if result['status']!='PASS':raise ValueError('Candidate FAIL: '+str(result['failures'][:3]))
    if result.get('blog_survey_sha256')!=digest(blog_receipt):raise ValueError('Promotion survey differs from the validated candidate receipt')
    blog=load(blog_receipt)
    if blog['status']!='PASS' or blog['source_base']!='https://rabelus.com.br' or blog['frozen_edition_commit']!=load(ROOT/'docs/ingestion-contract.json')['blog_commit']:raise ValueError('Blog survey failed/domain/cut differs')
    checked=datetime.fromisoformat(blog['checked_at']);age=(datetime.now(timezone.utc)-checked).total_seconds()
    if not 0<=age<=86400:raise ValueError('Blog survey must be refreshed within this daily cycle')
    runtime=ROOT/'.runtime';runtime.mkdir(exist_ok=True);pending=runtime/'promotion-pending.json'
    if pending.exists():raise ValueError('Interrupted/pending promotion; inspect receipt and backups before manual recovery')
    promotion_key=hashlib.sha256(run.relative_to(ROOT).as_posix().encode()).hexdigest()[:16]
    stage=runtime/('stage-'+promotion_key);backup=runtime/('backup-'+promotion_key)
    if stage.exists() or backup.exists() or (run/'promotion.json').exists():raise ValueError('Run already attempted; inspect old receipt, use a new run')
    shutil.copytree(candidate,stage);before=manifest(ROOT/'data');after=manifest(stage)
    if after!=candidate_before or manifest(candidate)!=candidate_before:raise ValueError('Candidate changed during validation/staging; served data untouched')
    intent={'at':datetime.now(timezone.utc).isoformat(),'candidate':after,'previous':before,'backup':str(backup.relative_to(ROOT)),'status':'PENDING','blog_survey_sha256':digest(blog_receipt),'contract_sha256':result['contract_sha256']}
    durable(pending,intent)
    if manifest(ROOT/'data')!=before:raise ValueError('Served data changed concurrently; pending receipt retained')
    os.replace(ROOT/'data',backup)
    try:os.replace(stage,ROOT/'data')
    except Exception:
        os.replace(backup,ROOT/'data');raise
    if manifest(ROOT/'data')!=after:raise ValueError('Promoted content mismatch; retain barrier for recovery')
    durable(run/'promotion.json',{**intent,'status':'PROMOTED','validation':result,'blog_survey':str(Path(blog_receipt).resolve().relative_to(ROOT))})
    os.replace(pending,run/'promotion-intent.json')
    print('PROMOTED',len(after),'files; prior data preserved in',backup)
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--run',type=Path,required=True);ap.add_argument('--blog-survey',type=Path,required=True);a=ap.parse_args();promote(a.candidate,a.run,a.blog_survey)

```

## scripts/check_release.py — revisão pública7359dea

```python
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

```
