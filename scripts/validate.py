"""Admission: independent input contract + exact sources + qualified relations.
Mechanical PASS is not semantic comprehension, runtime or human acceptance.
"""
from pathlib import Path
import argparse,hashlib,json,re,unicodedata
from build_data import Body,term_pattern
ROOT=Path(__file__).resolve().parents[1]
def normalized(s):return ' '.join(re.findall(r'\w+',unicodedata.normalize('NFKC',str(s)).casefold()))
def load(p):return json.loads(p.read_text(encoding='utf8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(root,data_dir=None,allow_incomplete=False):
    root=Path(root);data_dir=Path(data_dir or root/'data');failures=[];warnings=[]
    def need(ok,msg):
        if not ok:failures.append(msg)
    contract=load(root/'docs/ingestion-contract.json');manifest_file=root/'docs/research/frozen-manifest.json';manifest=load(manifest_file)
    need(digest(manifest_file)==contract['manifest_sha256'],'Frozen manifest hash differs from independent contract')
    expected={s['slug']:s for s in contract['sources']}
    need(contract['source_count']==len(expected)==len(manifest['posts']) and len(expected)>0,'SPEC0.1 frozen source count differs')
    need(set(expected)=={s['slug'] for s in manifest['posts']},'Frozen manifest/contract IDs differ')
    knowledge=load(data_dir/'knowledge.json');edition=knowledge['edition'];sources=knowledge['sources'];nodes=knowledge['nodes'];refs=knowledge['references'];paths=knowledge['paths'];relations=knowledge.get('relations',[])
    ids={s['slug'] for s in sources};nodeids={n['id'] for n in nodes};refids={r['id'] for r in refs};relationids={r['id'] for r in relations}
    need(len(ids)==len(sources)==contract['source_count'],'Source IDs empty/duplicated/missing');need(ids==set(expected),'Independent source contract differs')
    need(len(nodeids)==len(nodes)>0,'Node IDs empty/duplicated');need(len(refids)==len(refs) and refids==set(contract['reference_ids']),'Independent reference contract differs')
    need(edition['blog_commit']==contract['blog_commit'],'Edition frozen commit differs');need(edition['source_domain']==contract['source_domain'],'Source domain differs')
    need(edition['version']==contract['edition_version'],'Edition version differs from contract');need(edition['source_count']==contract['source_count'],'Edition count differs')
    assignments={};reports={}
    for batch in (root/'docs/research').glob('batch-*.json'):
        if batch.name.endswith('-report.json'):
            for s in load(batch)['posts']:
                need(s['slug'] not in reports,'Duplicate reader receipt '+s['slug']);reports[s['slug']]=s
        else:
            for s in load(batch):
                need(s['slug'] not in assignments,'Duplicate assignment '+s['slug']);assignments[s['slug']]=s
    need(set(assignments)==set(expected)==set(reports),'Assignments/readers differ from independent frozen contract')
    declared_assets=load(root/'docs/ASSETS.json');asset_names={a['file'] for a in declared_assets}|{'assets/brand/heuristik-mark.svg','assets/brand/heuristik-banner.svg'}
    actual_assets={f.relative_to(root).as_posix() for f in (root/'assets').rglob('*') if f.is_file()}
    need(actual_assets==asset_names,'Asset inventory/provenance differs')
    for asset in declared_assets:need(digest(root/asset['file'])==asset['sha256'],'Asset source hash differs '+asset['file'])
    expected_files={'knowledge.json','coverage.json','context.txt','blog-status.json','update-queue.json'}|{'articles/'+s['slug']+'.json' for s in sources}
    actual_files={f.relative_to(data_dir).as_posix() for f in data_dir.rglob('*') if f.is_file()}
    need(actual_files==expected_files,'Unexpected or missing data file; publication allowlist differs')
    need(not any(f.is_symlink() for f in data_dir.rglob('*')),'Symlinks are not admitted in generated data')
    need(edition['inputs']['contract_sha256']==digest(root/'docs/ingestion-contract.json'),'Edition contract binding differs')
    need(edition['inputs']['relations_sha256']==digest(root/'docs/research/relations.json'),'Edition relations binding differs')
    for name,sha in edition['inputs']['readers'].items():need(sha==digest(root/'docs/research'/name),'Reader input hash differs '+name)
    for name,sha in edition['inputs']['external'].items():need(sha==digest(root/'docs/research/external'/name),'External input hash differs '+name)
    survey=load(data_dir/'blog-status.json');need(survey.get('status')=='PASS' and survey.get('source_base')=='https://'+contract['source_domain'] and survey.get('frozen_edition_commit')==contract['blog_commit'],'Blog survey invalid')
    # JSON canonicalization binds the value even when whitespace differs from the original run receipt.
    candidates=[f for f in (root/'docs/runs').rglob('blog-status.json') if digest(f)==edition['inputs']['blog_survey_sha256']]
    need(bool(candidates) and any(load(f)==survey for f in candidates),'Blog survey receipt not bound to edition')
    read=claims=checked_quotes=0;bodies={}
    for source in sources:
        slug=source['slug']
        if slug not in expected:continue
        need(bool(re.fullmatch(r'[\w.-]+',slug)),'Unsafe source slug '+slug)
        if not re.fullmatch(r'[\w.-]+',slug):continue
        article=load(data_dir/'articles'/f'{slug}.json');rawpath=root/'docs/research/source-html'/contract['blog_commit']/(slug+'.html.txt');raw=rawpath.read_bytes()
        need(digest(rawpath)==source['sha256']==article['sha256']==expected[slug]['sha256'],'Source hash mismatch '+slug)
        parser=Body();parser.feed(raw.decode('utf8'));body=parser.text();bodies[slug]=normalized(body)
        need(body==article['body'] and len(body)>40,'Extracted source body mismatch '+slug)
        need(not parser.capture and parser.depth==0,'Unclosed source content container '+slug)
        need(article['blog_commit']==edition['blog_commit'],'Article commit mismatch '+slug)
        need(all(article.get(k)==v for k,v in source.items()),'Article/index inconsistency '+slug)
        need(all(source.get(k)==expected[slug][k] for k in ('file','author','date')),'Frozen attribution differs '+slug)
        need(source['url']==f"https://{contract['source_domain']}/"+source['file'],'Source URL differs '+slug)
        report=reports.get(slug,{})
        need(report.get('sha256')==source['sha256'] and report.get('read_status')==source['read_status'],'Reader receipt hash/status differs '+slug)
        need(source.get('claims')==report.get('claims') and source.get('summary')==report.get('summary'),'Generated knowledge differs from reader report '+slug)
        if source['read_status']=='read':
            read+=1;need(len(source.get('summary',''))>=40,'Insufficient reading summary '+slug);need(bool(source.get('claims')),'Missing claims '+slug)
        elif not allow_incomplete:need(False,'Unread source '+slug)
        for c in source.get('claims',[]):
            claims+=1;quote=normalized(c.get('evidence_excerpt',''));match=bool(quote) and quote in bodies[slug];checked_quotes+=match
            need(match,'Evidence excerpt not found '+slug+': '+c.get('evidence_excerpt','')[:90]);need(all(c.get(k) for k in ('object','subject','relation','limitation','confidence')),'Unqualified claim '+slug)
    need(read==edition['read_count'] and (allow_incomplete or read==contract['source_count']),'Incomplete or inconsistent reading count')
    need(len(relationids)==len(relations)>=contract['minimum_relations'],'Qualified relation coverage below contract or duplicate IDs')
    need(relations==load(root/'docs/research/relations.json'),'Relations differ from natural editorial records')
    incidents=set()
    for r in relations:
        rid=r['id'];need(bool(r['source_ids']) and set(r['source_ids'])<=ids,'Orphan relation '+rid);need(bool(r['node_ids']) and set(r['node_ids'])<=nodeids,'Orphan relation node '+rid)
        need(r.get('relation_type') in ['aplicado','adaptado','inspirado','considerado','relatado','proposto'],'Unqualified relation type '+rid)
        need(all(r.get(k) for k in ('subject','object','problem','solution','result','limitations','confidence','lesson','next_step','occurred_at','incident_key')),'Incomplete heuristic relation '+rid)
        need(set(r.get('reference_ids',[]))<=refids,'Unknown relation reference '+rid)
        need(bool(r.get('evidence')),'Missing relation evidence '+rid)
        for e in r.get('evidence',[]):need(e.get('source_id') in r['source_ids'] and bool(normalized(e.get('excerpt',''))) and normalized(e.get('excerpt','')) in bodies.get(e.get('source_id'),''),'Unsupported relation excerpt '+rid)
        key=(r['incident_key'],r['subject'],r['object'],r['relation_type']);need(key not in incidents,'Duplicate conceptual occurrence '+rid);incidents.add(key)
    for n in nodes:
        need(set(n['source_ids'])<=ids,'Unknown node source '+n['id']);need('não demonstram uso' in n.get('selection_method',''),'Candidate grouping caveat missing '+n['id']);need(set(n.get('relation_ids',[]))<=relationids,'Unknown relation in node '+n['id'])
    for p in paths:need(set(p['node_ids'])<=nodeids,'Unknown path node '+p['id'])
    for r in refs:
        original=load(root/'docs/research/external'/(r['id']+'.json'))
        need(all(r.get(k)==original.get(k) for k in ['url','summary','sections','metrics']),'Reference report differs '+r['id'])
        need(r['url'].startswith('https://'),'Unsafe reference URL '+r['id']);need(set(r.get('lab_source_ids',[]))<=ids,'Unknown reference/source join '+r['id'])
    coverage=load(data_dir/'coverage.json');need(coverage['edition']==edition and coverage['sources']==[{k:s[k] for k in ('slug','file','sha256','read_status')} for s in sources],'Coverage export differs')
    text=(data_dir/'context.txt').read_text(encoding='utf8');need(text.startswith('DATA_ONLY'),'Export DATA_ONLY header missing');need('https://heuristik.space/' in text,'Wrong product URL in export');need((root/'CNAME').read_text().strip()==contract['product_domain'],'Product domain differs')
    for r in relations:need(r['id'] in text,'Relation absent from general context '+r['id'])
    bus=term_pattern(['Bus']);need(not bus.search('a busca trouxe um resultado'),'False positive Bus/busca');need(bool(bus.search('o bus conecta fontes')),'False negative Bus')
    tested_files={'data/'+f.relative_to(data_dir).as_posix():digest(f) for f in data_dir.rglob('*') if f.is_file()}
    for name in ['scripts/validate.py','scripts/build_data.py','docs/ingestion-contract.json','docs/research/relations.json','docs/research/frozen-manifest.json','docs/ASSETS.json']:tested_files[name]=digest(root/name)
    return {'tested_files':tested_files,'status':'FAIL' if failures else 'PASS','sources':len(sources),'read_count':read,'claims':claims,'quoted_evidence_checked':checked_quotes,'relations':len(relations),'nodes':len(nodes),'references':len(refs),'contract_sha256':digest(root/'docs/ingestion-contract.json'),'blog_survey_sha256':edition['inputs']['blog_survey_sha256'],'failures':failures,'warnings':warnings,'scope':'Independent frozen input integrity, attribution, quote localization and qualified relation schema. Not proof of comprehension, runtime, deploy or human acceptance.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--data',type=Path);p.add_argument('--allow-incomplete',action='store_true');p.add_argument('--out',type=Path);args=p.parse_args()
    try:result=validate(args.root.resolve(),args.data,args.allow_incomplete)
    except Exception as exc:result={'status':'FAIL','failures':[type(exc).__name__+': '+str(exc)]}
    if args.out:
        if args.out.exists():raise ValueError('Refusing to overwrite previous gate receipt')
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['status']!='PASS')
if __name__=='__main__':main()
