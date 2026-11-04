"""Package only public runtime files; no Git, research intake, raw captures or runtime."""
from pathlib import Path
import argparse,shutil,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def package(output):
    output=Path(output).resolve()
    if output.exists():raise ValueError('Output exists: use a new directory')
    output.mkdir(parents=True)
    for name in ['index.html','app.js','styles.css','CNAME','.nojekyll','404.html']:
        f=ROOT/name
        if f.exists():shutil.copy2(f,output/name)
    for name in ['data','assets']:shutil.copytree(ROOT/name,output/name)
    docs=output/'docs';docs.mkdir()
    for name in ['GOVERNANCE.md','ASSETS.md','ASSETS.json','RESEARCH.md','ARCHITECTURE.md','OPERATIONS.md']:
        f=ROOT/'docs'/name
        if f.exists():shutil.copy2(f,docs/name)
    files={str(f.relative_to(output)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(output.rglob('*')) if f.is_file()}
    (output/'release-files.json').write_text(json.dumps(files,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'files':len(files),'bytes':sum(f.stat().st_size for f in output.rglob('*') if f.is_file()),'output':str(output)}))
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);package(ap.parse_args().out)
