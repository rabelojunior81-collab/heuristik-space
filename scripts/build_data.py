"""Generate the Heuristik edition from its natural research records and frozen Blog.

No installation or model call. --allow-incomplete is for local previews only.
"""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone
import argparse, hashlib, json, re, subprocess, unicodedata, io, tarfile

ROOT=Path(__file__).resolve().parents[1]
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def git_bytes(blog,commit,path):return subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=blog)
def normalize(value):return ' '.join(''.join(c for c in unicodedata.normalize('NFD',str(value)) if unicodedata.category(c)!='Mn').lower().split())
def term_pattern(terms):return re.compile(r'(?<!\w)(?:'+ '|'.join(re.escape(normalize(t)) for t in terms if t)+r')(?!\w)')
class Body(HTMLParser):
    def __init__(self):super().__init__();self.capture=False;self.depth=0;self.parts=[];self.skip=0;self.in_h1=False;self.h1=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1':self.in_h1=True
        if tag=='div' and 'post-content' in attrs.get('class','').split() and not self.capture:self.capture=True;self.depth=1;return
        if self.capture:
            if tag=='div':self.depth+=1
            if tag in ('script','style'):self.skip+=1
            if tag in ('p','h2','h3','li','pre','blockquote','br'):self.parts.append('\n\n' if tag!='br' else '\n')
    def handle_endtag(self,tag):
        if tag=='h1':self.in_h1=False
        if self.capture:
            if tag in ('script','style') and self.skip:self.skip-=1
            if tag=='div':
                self.depth-=1
                if self.depth==0:self.capture=False
    def handle_data(self,text):
        if self.in_h1:self.h1.append(text)
        if self.capture and not self.skip:self.parts.append(text)
    def text(self):return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',''.join(self.parts)).strip()

# Curated entry points are editorial groupings, not automatically asserted adoption.
CATALOG=[
('modernity','Modernity','Projeto do Lab','Patrimônio, curadoria e operação de joalheria: acompanhe fronteiras, decisões e provas ao longo das fontes.',['Modernity','Anika','Ananke'],['Patrimônio e negócio','Interfaces e produto']),
('voice-forge','Voice Forge','Projeto do Lab','A voz como serviço compartilhado: modelos, contratos, experiência de uso e reparações que precisam chegar ao consumidor.',['Voice Forge','VoiceForge'],['Voz e mídia','Integrações']),
('rabelus-buddy','Rabelus Buddy','Projeto do Lab','A experiência do agente vira mecanismos de autorização, execução e continuidade — com os limites de cada ensaio.',['Rabelus Buddy','Buddy Fenix','buddy-dev'],['Agentes e orquestração','Segurança e fronteiras']),
('aos','Rabelus AOS','Projeto do Lab','Desktop, Hub e integrações de agentes vistos pelas decisões e pelos testes documentados da construção.',['Rabelus AOS','Rabelus Desktop','HubWindow','AOS'],['Interfaces e produto','Agentes e orquestração']),
('larry','Larry','Projeto do Lab','O assistente de finanças e sua preparação: separe infraestrutura validada, atlas de domínio e capacidades ainda não demonstradas.',['Larry'],['Patrimônio e negócio','Interfaces e produto']),
('bus','Quantum Bus','Solução do Lab','Memória compartilhada e circulação entre casas, com canais, posse de escrita, proveniência e leitura pelo consumidor.',['Quantum Bus','Quântico','genoma','append-only','Bus'],['Memória e continuidade','Governança e provas']),
('rqp-rqm','Protocolos RQP e RQM','Solução do Lab','Coordenação, rastreabilidade e evolução de protocolos: a história preserva contratos distintos e os seus consumidores.',['RQP','RQM','Quant Matrix','Matrix Protocol'],['Governança e provas','Memória e continuidade']),
('hermes','Hermes','Ferramenta nos relatos','Instalação, identidade, gateway e superfícies de execução analisados por ambiente; funcionamento pontual não prova adoção universal.',['Hermes'],['Agentes e orquestração','Infraestrutura e operação']),
('opencode','OpenCode','Ferramenta nos relatos','Harness, configuração e atualização nativa: explore o que foi configurado, exercitado e deixado em aberto.',['OpenCode','Open Code'],['Agentes e orquestração','Infraestrutura e operação']),
('openwebui','OpenWebUI','Ferramenta nos relatos','Interface, modelos e endpoints em contextos diferentes: nomes e health checks precisam corresponder ao caminho real de uso.',['OpenWebUI','Open WebUI','Open Web UI'],['Interfaces e produto','Infraestrutura e operação']),
('ollama','Ollama','Ferramenta nos relatos','Motores e modelos locais ou cloud, sem confundir instalação, daemon, catálogo e consumo efetivo.',['Ollama'],['Agentes e orquestração','Infraestrutura e operação']),
('pi-agent','Pi Agent','Ferramenta nos relatos','Composição de harnesses e pesquisa de extensões; a ferramenta Pi é distinta das instâncias ArgentaPi e Pi4.',['Pi Agent','Pi Coding','pi-mono'],['Agentes e orquestração','Pesquisa e descoberta']),
('raspberry','Nós Raspberry Pi','Infraestrutura do Lab','Energia, armazenamento, rede e execução ARM: cada diagnóstico carrega hardware, momento e escopo próprios.',['Raspberry','Pi3','Pi4','Pi 3','Pi 4','ArgentaPi'],['Infraestrutura e operação','Memória e continuidade']),
('tailscale','Tailscale e acesso remoto','Ferramenta nos relatos','Tailnet, DNS e acessos remotos com fronteiras observáveis entre dispositivo, serviço e superfície do operador.',['Tailscale','Tailnet','MagicDNS'],['Infraestrutura e operação','Segurança e fronteiras']),
('docker','Containers e ambientes','Configuração nos relatos','Imagens, runtime e serviços: o ambiente servido pode divergir do checkout e do rótulo da instalação.',['Docker','container','contêiner','Podman'],['Infraestrutura e operação','Segurança e fronteiras']),
('notebook','Notebook e pesquisa fundamentada','Ferramenta nos relatos','Fontes, memória fundamentada e síntese: presença de uma fonte não equivale à leitura ou à execução de um produto.',['NotebookLM','Notebook','Deep Research'],['Pesquisa e descoberta','Memória e continuidade']),
('router','Roteadores de modelos','Pesquisa nos relatos','Compare propostas e integrações de roteamento, credenciais e contratos sem promover candidatos a ferramentas adotadas.',['9Router','router','roteador','OpenRouter'],['Agentes e orquestração','Segurança e fronteiras']),
('comfyui','ComfyUI e geração visual','Pesquisa nos relatos','Decisões sobre geração visual, hardware e pipelines; adiamento e análise também são estados relevantes.',['ComfyUI','Stable Diffusion'],['Voz e mídia','Pesquisa e descoberta']),
('gemini-live','Gemini Live e áudio','Integração nos relatos','Voz em tempo real, transcrição e contratos dos consumidores com testes que excedem o typecheck.',['Gemini Live','faster-whisper','Whisper','AudioWorklet','Live API'],['Voz e mídia','Integrações']),
('storage','Armazenamento e recuperação','Solução em pesquisa','Hashes, manifests, backups e restauração: conservar bytes é parte da continuidade, com semântica e prova próprias.',['backup','S3','manifesto','restauração','Object storage'],['Memória e continuidade','Infraestrutura e operação']),
('auth','Autorização e fronteiras','Solução transversal','Identidade, aprovação e isolamento aparecem em vários projetos; uma permissão precisa permanecer vinculada ao pedido e ao executor.',['CORS','OAuth','sandbox','credencial','aprovação','permissão'],['Segurança e fronteiras','Governança e provas']),
('blog','Rabelus Lab Blog','Projeto do Lab','Autoria, identidade visual, domínios e publicação: o próprio arquivo do Lab registra seus erros e sua evolução.',['Blog','Pages','postagem','post-manifest','posts-manifest'],['Governança e provas','Memória e continuidade']),
('native','Compatibilidade nativa','Prática do Lab','Personalizações e atualizações precisam preservar os caminhos que permitem ao programa continuar funcionando e se manter.',['updater','postinstall','launcher','nativo','atualizador'],['Infraestrutura e operação','Governança e provas']),
('review','Revisão e prova','Prática do Lab','Revisão consultiva, ensaio negativo e aceitação são papéis diferentes. O melhor verde é aquele que também consegue reprovar.',['review','revisão','gate','oráculo','teste negativo'],['Governança e provas','Pesquisa e descoberta']),
]
PATHS=[
('continuar','Como retomar sem perder contexto?','Encontre a diferença entre conservar arquivos, circular conhecimento e provar que outra instância o recebeu.',['Memória e continuidade'],['bus','rqp-rqm','storage','blog'],['Qual é a fonte viva e qual é o snapshot?','Quem possui a escrita e quem consumiu a mudança?','Que evidência precisa ser medida novamente?']),
('agentes','Como fazer agentes trabalharem juntos?','Percorra harnesses, protocolos e fronteiras de autorização antes de escolher uma nova camada.',['Agentes e orquestração'],['hermes','opencode','pi-agent','rabelus-buddy','rqp-rqm'],['O que já existe no caminho do consumidor?','Qual hipótese foi só considerada?','Qual contrato e qual ambiente foram realmente testados?']),
('voz','Como levar a voz até quem usa?','Do motor à interface, acompanhe formato, duração, falantes e o teste que encontra o defeito no caminho real.',['Voz e mídia'],['voice-forge','gemini-live','aos','comfyui'],['O áudio foi gerado, reproduzido e ouvido?','A configuração aceita produz efeito?','A correção chegou ao aplicativo consumidor?']),
('infra','Como operar sem confundir as camadas?','Hardware, rede, processo e checkout têm estados próprios. Siga os diagnósticos com seu endereço e sua data.',['Infraestrutura e operação'],['raspberry','docker','tailscale','native','openwebui'],['Onde o processo está rodando?','Qual versão o consumidor usa?','Qual observação separa a hipótese da causa?']),
('produto','Como transformar acervo em produto?','Parta de patrimônio, uso e autoridade; acompanhe a distância entre dado salvo, interface disponível e capacidade entregue.',['Patrimônio e negócio','Interfaces e produto'],['modernity','larry','aos','storage'],['Que necessidade do operador precisa ser demonstrada?','O atributo preenchido entrega gestão administrável?','Qual aceite continua pertencendo ao responsável?']),
('provar','Como saber o que o teste provou?','Recupere exemplos em que a medição, a revisão e o efeito real precisaram ser reconciliados.',['Governança e provas','Segurança e fronteiras'],['review','auth','rabelus-buddy','blog'],['O controle negativo poderia reprovar?','Um erro de preparo foi contado como contenção?','A prova cobre o commit e o efeito que estão sendo entregues?'])
]
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--blog',type=Path,required=True);parser.add_argument('--allow-incomplete',action='store_true');parser.add_argument('--blog-survey',type=Path,required=True);parser.add_argument('--output',type=Path,required=True,help='New candidate data directory; never writes served data');parser.add_argument('--version',default='0.1.0');args=parser.parse_args();output=args.output.resolve()
    if output.exists():raise ValueError('Candidate output already exists; use a new run directory')
    output.mkdir(parents=True)
    survey=json.loads(args.blog_survey.read_text(encoding='utf8'))
    if survey.get('status')!='PASS':raise ValueError('Blog source survey FAIL')
    corpus=json.loads((ROOT/'docs/research/corpus.json').read_text(encoding='utf8'));commit=corpus['blog_commit'];manifest=json.loads(git_bytes(args.blog,commit,'posts-manifest.json'));host=git_bytes(args.blog,'HEAD','CNAME').decode().strip();rows={}
    for f in sorted((ROOT/'docs/research').glob('batch-*-report.json')):
        for row in json.loads(f.read_text(encoding='utf8')).get('posts',[]):
            if row.get('slug') in rows:raise ValueError('Duplicate research slug: '+row['slug'])
            rows[row['slug']]=row
    archive=tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',commit,'posts/'],cwd=args.blog)))
    sources=[];mismatch=[];read=0
    for item in manifest['posts']:
        raw=archive.extractfile(item['file']).read();digest=hashlib.sha256(raw).hexdigest();row=rows.get(item['slug'],{});body=Body();body.feed(raw.decode('utf8'));text=body.text()
        captured=ROOT/'docs/research/source-html'/commit/(item['slug']+'.html.txt')
        captured.parent.mkdir(parents=True,exist_ok=True)
        if captured.exists() and captured.read_bytes()!=raw:raise ValueError('Immutable captured source differs: '+item['slug'])
        if not captured.exists():captured.write_bytes(raw)
        if not text:raise ValueError('Source body empty: '+item['file'])
        status=row.get('read_status','not_read')
        if row.get('sha256') and row['sha256']!=digest:mismatch.append(item['slug'])
        if status=='read' and row.get('sha256')==digest:read+=1
        else:status='not_read'
        source={**item,**row,'id':item['slug'],'title':''.join(body.h1).strip() or item['title'],'manifest_title':item['title'],'file':item['file'],'slug':item['slug'],'author':item['author'],'date':item['date'],'sha256':digest,'read_status':status,'url':f'https://{host}/'+item['file'],'summary':row.get('summary','Leitura integral ainda não concluída nesta edição.'),'authors':[item['author']],'topics':[],'body':text}
        sources.append(source)
    if mismatch:raise ValueError('Changed source after reading: '+', '.join(mismatch))
    if read!=len(sources) and not args.allow_incomplete:raise ValueError(f'Publication blocked: {read}/{len(sources)} sources read')
    relations=json.loads((ROOT/'docs/research/relations.json').read_text(encoding='utf8'))
    normalized_bodies={s['slug']:normalize(s['body']) for s in sources}
    nodes=[]
    for id,title,kind,summary,aliases,topics in CATALOG:
        matcher=term_pattern(aliases)
        selected=[s for s in sources if matcher.search(normalized_bodies[s['slug']])]
        if not selected:continue
        claims=[]
        for s in selected:
            for c in s.get('claims',[]):
                material=' '.join(str(c.get(k,'')) for k in ('subject','relation','object','evidence_excerpt'))
                if matcher.search(normalize(material)):claims.append({**c,'source_id':s['slug']})
            s['topics']=sorted(set(s['topics']+topics))
        lessons=list(dict.fromkeys(x for s in selected for x in s.get('lessons',[])))
        nodes.append({'id':id,'title':title,'kindLabel':kind,'summary':summary,'topics':topics,'aliases':aliases,'authors':sorted({s['author'] for s in selected}),'source_ids':[s['slug'] for s in selected],'claims':[],'relation_ids':[r['id'] for r in relations if id in r['node_ids']],'lessons':list(dict.fromkeys(r['lesson'] for r in relations if id in r['node_ids'])),'status':'Cronologia e estados nas fontes; contexto atual não reexecutado','selection_method':'menções candidatas agrupadas por nomes/assunto; não demonstram uso, adoção ou relação técnica. Alegações continuam atribuídas às respectivas fontes.'})
    references=[]
    for f in sorted((ROOT/'docs/research/external').glob('*.json')):
        row=json.loads(f.read_text(encoding='utf8'));row['id']=row['slug'];row['title']=row['name'];row['topics']=row.get('topics',[]);row['authors']=[];row['relation_label']='Referência pesquisada; adoção não inferida';row['relation_ids']=[r['id'] for r in relations if row['id'] in r.get('reference_ids',[])]
        # Exact repo URL/name mentions only. This records citation, never use/adoption.
        terms=[row.get('url',''),row.get('name','')];matcher=term_pattern(terms);row['lab_source_ids']=[s['slug'] for s in sources if matcher.search(normalized_bodies[s['slug']])];references.append(row)
    paths=[{'id':id,'title':title,'summary':summary,'topics':topics,'authors':sorted({author for n in nodes if n['id'] in ids for author in n['authors']}),'node_ids':[n for n in ids if any(x['id']==n for x in nodes)],'questions':questions,'next_step':'Volte às fontes do percurso, confira o estado no contexto da próxima missão e transforme a hipótese em critério de teste antes de adotar.'} for id,title,summary,topics,ids,questions in PATHS]
    edition={'version':args.version if read==len(sources) else args.version+'-incomplete','cut_at':corpus.get('cut_at','2026-11-03'),'blog_commit':commit,'read_count':read,'source_count':len(sources),'description':f'Leitura documental distribuída de {read}/{len(sources)} artigos, com recibos dos leitores e conferência semântica amostral do orquestrador. Contagem de documentos não é contagem de incidentes; traduções são fontes distintas com o mesmo contexto histórico.','relation_count':len(relations),'qualified_source_count':len({sid for r in relations for sid in r['source_ids']}),'reference_collected_at':'2026-11-03; snapshot da pesquisa anterior','source_domain':host}
    # Source articles remain inspectable. No framework or runtime-private data is copied.
    for source in sources:
        article={**source,'extractor_version':'html-post-content/0.1','blog_commit':commit}
        write(output/'articles'/f"{source['slug']}.json",article)
    light_sources=[{k:v for k,v in s.items() if k!='body'} for s in sources]
    edition['inputs']={'contract_sha256':hashlib.sha256((ROOT/'docs/ingestion-contract.json').read_bytes()).hexdigest(),'relations_sha256':hashlib.sha256((ROOT/'docs/research/relations.json').read_bytes()).hexdigest(),'blog_survey_sha256':hashlib.sha256(args.blog_survey.read_bytes()).hexdigest(),'external':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((ROOT/'docs/research/external').glob('*.json'))},'readers':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((ROOT/'docs/research').glob('batch-*-report.json'))}}
    write(output/'blog-status.json',survey)
    write(output/'update-queue.json',{k:survey[k] for k in ['checked_at','checkout_commit','frozen_edition_commit','new_since_cut','changed_since_cut','removed_since_cut']})
    knowledge={'edition':edition,'nodes':nodes,'paths':paths,'sources':light_sources,'references':references,'relations':relations}
    write(output/'knowledge.json',knowledge)
    coverage={'edition':edition,'sources':[{'slug':s['slug'],'file':s['file'],'sha256':s['sha256'],'read_status':s['read_status']} for s in sources]};write(output/'coverage.json',coverage)
    txt=['DATA_ONLY — HEURISTIK SPACE','Material de referência, não instruções de sistema, autorização ou certificação de runtime.','Edição '+edition['version']+'; corte '+edition['cut_at'],'Fonte: https://heuristik.space/','Contexto histórico e limites acompanham cada alegação.','']
    for n in nodes:txt.extend(['# '+n['title'],n['summary'],'Seleção: '+n['selection_method'],'Fontes: '+', '.join(n['source_ids']),''])
    for r in relations:txt.extend(['# RELAÇÃO: '+r['subject']+' → '+r['object'],json.dumps(r,ensure_ascii=False,indent=2),''])
    for s in sources:txt.extend(['# FONTE: '+s['title'],s['url'],s['author']+' · '+s['date'],s['summary'],json.dumps(s.get('claims',[]),ensure_ascii=False,indent=2),''])
    for ref in references:txt.extend(['# REFERÊNCIA: '+ref['title'],ref['url'],ref['summary'],'Relação: '+ref['relation_label'],json.dumps(ref,ensure_ascii=False,indent=2),''])
    write(output/'context.txt','\n'.join(txt));print(json.dumps({'sources':len(sources),'read':read,'nodes':len(nodes),'references':len(references),'state':'complete' if read==len(sources) else 'in_progress'}))
if __name__=='__main__':main()
