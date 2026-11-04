"""One recorded ingestion cycle: survey, candidate, admission, negative controls.
Reading/editorial approval precede this command. Publishing is a separate gate.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import os
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main(blog, promote):
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    record = ROOT/'docs/runs'/run_id
    record.mkdir(parents=True, exist_ok=False)
    journal = record/'journal.jsonl'
    def event(name, **values):
        with journal.open('a', encoding='utf8', newline='\n') as file:
            file.write(json.dumps({'at':datetime.now(timezone.utc).isoformat(),
                                   'event':name, **values}, ensure_ascii=False)+'\n')
            file.flush()
            os.fsync(file.fileno())
    result = {'run':run_id, 'status':'IN_PROGRESS',
              'scope':'Ingestion integrity only; UI/review/deploy/human acceptance are separate.'}
    candidate = ROOT/'.runtime'/run_id/'data'
    def step(name, args, env=None):
        event('before', step=name)
        start = time.monotonic()
        process = subprocess.run([sys.executable, '-X', 'utf8', '-B', *args],
                                 cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf8')
        output = (process.stdout+'\n'+process.stderr).replace(str(ROOT), '<project>').replace(str(blog), '<blog>')
        (record/(name+'.log')).write_text(output, encoding='utf8', newline='\n')
        event('after', step=name, exit_code=process.returncode,
              elapsed_seconds=round(time.monotonic()-start,3))
        if process.returncode:
            raise RuntimeError(name+' failed; inspect '+str(record.relative_to(ROOT)))
        return output
    try:
        event('intention', promotion_requested=promote, contract='docs/ingestion-contract.json')
        step('source-survey', ['scripts/inspect_blog.py','--blog',str(blog),
                              '--out',str(record/'source')])
        survey = record/'source/blog-status.json'
        step('candidate', ['scripts/build_data.py','--blog',str(blog),'--output',str(candidate),
                           '--blog-survey',str(survey)])
        step('admission', ['scripts/validate.py','--data',str(candidate),'--out',str(record/'admission.json')])
        env = dict(os.environ, HEURISTIK_TEST_DATA=str(candidate))
        step('negative-controls', ['scripts/record_checks.py','--out',str(record/'controls.json')], env)
        if promote:
            step('promotion', ['scripts/promote.py','--candidate',str(candidate),
                               '--run',str(record/'promotion'),'--blog-survey',str(survey)])
        result.update(status='PASS', candidate=str(candidate.relative_to(ROOT)),
                      source_survey=str(survey.relative_to(ROOT)), locally_promoted=promote)
    except Exception as error:
        result.update(status='FAIL', error=str(error))
        event('failure', error=str(error))
    event('cycle_result', status=result['status'])
    (record/'receipt.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n',
                                     encoding='utf8', newline='\n')
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(result['status'] != 'PASS')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--blog', type=Path, required=True)
    ap.add_argument('--promote', action='store_true', help='Promote only locally after candidate gates; does not publish')
    args = ap.parse_args()
    main(args.blog.resolve(), args.promote)
