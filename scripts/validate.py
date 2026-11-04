"""Heuristik local admission gates. Mechanical coverage is not semantic acceptance."""
from pathlib import Path
import argparse,hashlib,json,re,unicodedata
from build_data import Body,term_pattern
ROOT=Path(__file__).resolve().parents[1]
def normalized(s):return ' '.join(re.findall(r'\w+',unicodedata.normalize('NFKC',str(s)).casefold()))
def validate(root,allow_incomplete=False):
    failures=[];warnings=[]
    def need(ok,msg):
        if not ok:failures.append(msg)
    knowledge=json.loads((root/'data/knowledge.json').read_text(encoding='utf8'));edition=knowledge['edition'];sources=knowledge['sources'];nodes=knowledge['nodes'];refs=knowledge['references'];paths=knowledge['paths'];ids={s['slug'] for s in sources};nodeids={n['id'] for n in nodes}
    need(len(ids)==len(sources)>0,'Source IDs empty/duplicated');need(len(nodeids)==len(nodes)>0,'Node IDs empty/duplicated');need(len({r['id'] for r in refs})==len(refs),'Reference IDs duplicated')
    if not allow_incomplete:need(edition['read_count']==len(sources),'Incomplete reading blocks publication')
    expected={}
    for batch in (root/'docs/research').glob('batch-*.json'):
        if batch.name.endswith('-report.json'):continue
        for source in json.loads(batch.read_text(encoding='utf8')):
            need(source['slug'] not in expected,'Duplicate research assignment '+source['slug']);expected[source['slug']]=source
    need(set(expected)==ids,'Assignments/source corpus diverge');read=0;claims=0;checked_quotes=0;parser_checks=[]
    for source in sources:
        slug=source['slug'];need(bool(re.fullmatch(r'[\w.-]+',slug)),'Unsafe source slug '+slug);article=json.loads((root/'data/articles'/f'{slug}.json').read_text(encoding='utf8'));raw=(root/'docs/research/source-html'/edition['blog_commit']/(slug+'.html.txt')).read_bytes();need(hashlib.sha256(raw).hexdigest()==source['sha256']==article['sha256'],'Source hash mismatch '+slug)
        parser=Body();parser.feed(raw.decode('utf8'));body=parser.text();need(body==article['body'] and len(body)>40,'Extracted source body mismatch '+slug);need(article['blog_commit']==edition['blog_commit'],'Article commit mismatch '+slug)
        need(source['file']==expected[slug]['file'] and source['author']==expected[slug]['author'],'Source attribution differs '+slug)
        if source['read_status']=='read':
            read+=1;need(len(source.get('summary',''))>=40,'Insufficient reading summary '+slug);need(bool(source.get('claims')),'Missing source claims '+slug)
        elif not allow_incomplete:need(False,'Unread source '+slug)
        for claim in source.get('claims',[]):
            claims+=1;excerpt=claim.get('evidence_excerpt','');need(bool(claim.get('object')) and bool(claim.get('subject')) and bool(claim.get('relation')),'Incomplete claim '+slug);need(bool(claim.get('limitation')) and bool(claim.get('confidence')),'Unqualified claim '+slug)
            quote=normalized(excerpt);match=bool(quote) and quote in normalized(body)
            need(match,'Evidence excerpt not found '+slug+': '+excerpt[:130]);checked_quotes+=match
        parser_checks.append({'slug':slug,'start':body[:100],'end':body[-100:],'chars':len(body)})
    need(read==edition['read_count'],'Reading count mismatch')
    for n in nodes:
        need(set(n['source_ids'])<=ids,'Unknown node source '+n['id']);need('não demonstram uso' in n.get('selection_method',''),'Candidate grouping caveat missing '+n['id'])
        for c in n.get('claims',[]):need(c.get('source_id') in ids,'Unknown claim source '+n['id'])
    for p in paths:need(set(p['node_ids'])<=nodeids,'Unknown path node '+p['id'])
    for r in refs:
        need(r['url'].startswith('https://'),'Unsafe reference URL '+r['id']);need(set(r.get('lab_source_ids',[]))<=ids,'Unknown reference/source join '+r['id'])
    text=(root/'data/context.txt').read_text(encoding='utf8');need(text.startswith('DATA_ONLY'),'Export DATA_ONLY header missing');need('https://heuristik.space/' in text,'Wrong product URL in export');need((root/'CNAME').read_text().strip()=='heuristik.space','Product domain differs from user decision')
    # Positive/negative controls exercise the ambiguous-name boundary.
    bus=term_pattern(['Bus']);need(not bus.search('a busca trouxe um resultado'),'False positive Bus/busca');need(bool(bus.search('o bus conecta fontes')),'False negative Bus');need(bool(term_pattern(['Voice Forge']).search('o voice forge atende aos e modernity')),'Multi-project term control')
    result={'status':'FAIL' if failures else 'PASS','sources':len(sources),'read_count':read,'claims':claims,'quoted_evidence_checked':checked_quotes,'nodes':len(nodes),'references':len(refs),'failures':failures,'warnings':warnings,'scope':'Integrity, attribution, quote localization and coverage. Not proof of semantic comprehension, runtime, deploy or human acceptance.'}
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--allow-incomplete',action='store_true');p.add_argument('--out',type=Path);args=p.parse_args()
    try:result=validate(args.root.resolve(),args.allow_incomplete)
    except Exception as exc:result={'status':'FAIL','failures':[type(exc).__name__+': '+str(exc)]}
    if args.out:
        if args.out.exists():raise ValueError('Refusing to overwrite previous gate receipt')
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['status']!='PASS')
if __name__=='__main__':main()
