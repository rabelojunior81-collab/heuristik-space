"""Read-only Blog status survey, linked to every Heuristik ingestion receipt."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.request import Request,urlopen,HTTPRedirectHandler,build_opener
from urllib.parse import quote,urlsplit
import argparse,hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
class SameOrigin(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if urlsplit(newurl).scheme!='https' or urlsplit(newurl).netloc!=urlsplit(req.full_url).netloc:raise ValueError('Cross-origin/HTTP redirect refused')
        return super().redirect_request(req,fp,code,msg,headers,newurl)
def git(blog,ref,path):return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=blog)
def fetch(url):
    with build_opener(SameOrigin()).open(Request(url,headers={'User-Agent':'Heuristik-Space-Source-Survey/0.1','Cache-Control':'no-cache'}),timeout=25) as response:return response.status,response.url,response.read()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--blog',type=Path,required=True);ap.add_argument('--out',type=Path);args=ap.parse_args()
    stamp=datetime.now(timezone.utc);out=args.out or ROOT/'docs/runs'/stamp.strftime('%Y%m%dT%H%M%SZ');out.mkdir(parents=True,exist_ok=False)
    corpus=json.loads((ROOT/'docs/research/corpus.json').read_text(encoding='utf8'));frozen=corpus['blog_commit'];head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=args.blog).decode().strip();host=git(args.blog,'HEAD','CNAME').decode().strip()
    if not re.fullmatch(r'[a-z0-9.-]+',host) or host=='rabelus.online':raise ValueError('Invalid/retired source domain')
    base='https://'+host;expected=git(args.blog,head,'posts-manifest.json');status,final,public=fetch(base+'/posts-manifest.json');manifest=json.loads(public);snapshot=json.loads(git(args.blog,frozen,'posts-manifest.json'));known={x['slug']:x for x in snapshot['posts']};items=manifest['posts'];results=[]
    def check(item):
        path=item['file']
        if not path.startswith('posts/') or '..' in path.split('/') or '\\' in path:raise ValueError('Invalid public source path')
        url=base+'/'+quote(path);row={'slug':item['slug'],'file':path,'url':url}
        try:
            code,actual,body=fetch(url);local=git(args.blog,head,path);digest=hashlib.sha256(body).hexdigest();row.update(http=code,final_url=actual,sha256=digest,checkout_sha256=hashlib.sha256(local).hexdigest(),equal_checkout=body==local)
            row['new_since_cut']=item['slug'] not in known
            if item['slug'] in known:row['changed_since_cut']=hashlib.sha256(git(args.blog,frozen,known[item['slug']]['file'])).hexdigest()!=digest
        except Exception as exc:row.update(error=str(exc),equal_checkout=False)
        return row
    with ThreadPoolExecutor(max_workers=5) as pool:
        jobs=[pool.submit(check,item) for item in items]
        for job in as_completed(jobs):
            results.append(job.result())
            if len(results)%25==0:print(f'Blog sources surveyed: {len(results)}/{len(items)}',flush=True)
    ids={x['slug'] for x in items};results.sort(key=lambda x:x['slug']);ok=status==200 and public==expected and all(x.get('http')==200 and x['equal_checkout'] for x in results)
    report={'checked_at':stamp.isoformat(),'source_base':base,'checkout_commit':head,'frozen_edition_commit':frozen,'manifest_http':status,'manifest_final_url':final,'manifest_sha256':hashlib.sha256(public).hexdigest(),'manifest_equal_checkout':public==expected,'posts':len(items),'new_since_cut':[x['slug'] for x in results if x.get('new_since_cut')],'changed_since_cut':[x['slug'] for x in results if x.get('changed_since_cut')],'removed_since_cut':sorted(set(known)-ids),'sources':results,'status':'PASS' if ok else 'FAIL','scope':'Public TLS/HTTP/content survey. It does not replace deep reading, semantic review or current runtime acceptance.'}
    target=out/'blog-status.json';target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print(str(target),report['status'],flush=True)
    raise SystemExit(not ok)
if __name__=='__main__':main()
