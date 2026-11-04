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
