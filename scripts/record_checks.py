"""Run controls and bind the observed result to their exact inputs."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import re
import os
import hashlib
import subprocess
import sys
from check_release import ROOT, object_manifest, required_inputs


def main(output):
    if output.exists() or output.with_suffix('.log').exists():
        raise ValueError('Receipt already exists')
    data_dir=Path(os.environ.get('HEURISTIK_TEST_DATA',str(ROOT/'data')))
    def snapshot():
        files={k:v for k,v in object_manifest().items() if not k.startswith('data/')}
        files.update({'data/'+f.relative_to(data_dir).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in data_dir.rglob('*') if f.is_file()})
        return files
    current = snapshot()
    names = required_inputs('controls', current)
    before = {name:current[name] for name in names}
    process = subprocess.run([sys.executable,'-X','utf8','-B','-m','unittest','discover','-s','tests','-v'],
                             cwd=ROOT,capture_output=True,text=True,encoding='utf8')
    log = (process.stdout+'\n'+process.stderr).replace(str(ROOT),'<project>')
    count = re.search(r'Ran (\d+) tests?',log)
    after = snapshot()
    stable = all(after.get(name)==digest for name,digest in before.items())
    result = {'status':'PASS' if process.returncode==0 and count and int(count.group(1))>0 and stable else 'FAIL',
              'checked_at':datetime.now(timezone.utc).isoformat(),
              'tests_run':int(count.group(1)) if count else None,
              'tested_files':before,'inputs_unchanged':stable,
              'scope':'Admission, negative controls, filesystem promotion fixtures and release proof binding; not human acceptance.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.with_suffix('.log').write_text(log,encoding='utf8',newline='\n')
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(result['status'],result['tests_run'],'tests; inputs stable:',stable)
    raise SystemExit(result['status']!='PASS')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    main(parser.parse_args().out)
