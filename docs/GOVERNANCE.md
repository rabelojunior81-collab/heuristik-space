# Governança de ingestão e evolução

**Heuristik Space — by Rabelus Lab.** Cada um é UM! Todos, são UM!
Organização é Lindo! Antes, durante e depois, SEMPRE!

Esta rotina nasce dos controles editoriais do Blog e da direção expressa do Pai.
Não substitui a governança das casas dos membros, nem publica seus dados privados.

## Antes: declarar, congelar e conferir

1. Registrar a intenção, revisão da SPEC/plano e limites autorizados no STATE.
2. Sincronizar fontes e criar diretório de execução novo em `docs/runs/`. Nada de
   sobrescrever recibos passados ou reusar um PASS para outro conteúdo.
3. Executar `python scripts/inspect_blog.py --blog /caminho/clone-do-blog`.
   O endereço vem do CNAME do Blog, não de URL histórica. A vistoria liga domínio,
   manifesto, revisão local, HTTP/TLS, hashes por artigo e diferença desde o corte.
4. Fontes novas/modificadas ficam pendentes de leitura integral e conferência.
   O hash do recibo de leitura deve corresponder aos bytes da fonte. Inventário,
   extração mecânica ou leitura de cabeçalhos não passam pelo gate de leitura.

## Durante: construir e revisar

5. Leitores registram corpo integral examinado, resumo substantivo, entidades,
   relações, excertos, aprendizados, cronologia e limites nos relatórios naturais.
   Inferência e semelhança ficam separadas de uso/adaptação/inspiração declarados.
6. Orquestrador confere trechos e interpretações, reconcilia contagens e traduções,
   compara com a pesquisa externa e registra divergências. Múltiplas narrativas
   do mesmo caso não viram múltiplos incidentes automaticamente.
7. Gerar a edição a partir das fontes: `python scripts/build_data.py --blog ...`.
   `--allow-incomplete` serve somente a preview explicitamente incompleto.
8. Validar dados, fontes, links e exportações; executar controles negativos. A
   revisão consultiva usa modelo distinto, pacote público/hash e limites reais.
   Qualidade semântica é responsabilidade de leitura/revisão, não de uma contagem.
9. Toda tentativa tem resultado/erro e tratamento no journal. Corrigir com novo
   evento e commit; não apagar a tentativa ou converter o erro em sucesso.

## Depois: demonstrar o que foi publicado

10. Testar busca/filtros, detalhes/retorno, teclado, cópia real/fallback, estados
    vazios/erro e viewports375/390/1440. Guardar superfície e estado apresentados.
11. Congelar manifesto de arquivos e SHA; enviar somente delta próprio. Pages
    deve publicar o mesmo SHA. Conferir HTTPS, HTTP200, destino e bytes de arquivos
    representativos, incluindo dados e exportações. QA local não prova deploy.
12. Criar recibo com fonte/status do Blog, cobertura, testes, review, commit/build,
    URLs e limites. Atualizar STATE/CHANGELOG/README e versão; tag por edição.
    Publicar relato factual no Blog quando previsto, com o domínio do produto.
13. Falha posterior abre correção vinculada à edição anterior; rollback por
    commit próprio. Histórico, autoria, evidências e registros anteriores ficam.

## Gates por ciclo

| Gate | Critério | Bloqueia |
|---|---|---|
| Fonte | Blog correto, manifesto não vazio, HTTP/TLS e bytes coerentes | Admissão da ingestão |
| Leitura | Toda fonte do corte com corpo integral lido e hash correspondente | Publicação de edição integral |
| Semântica | Excertos localizáveis, relações qualificadas, amostra interpretada e review | Incorporação de alegações |
| Dados | IDs/fontes íntegros, esquema, exportações e links seguros | Edição candidata |
| Produto | Testes reais e controles negativos, QA móvel/desktop | Promoção |
| Publicação | SHA/build/HTTPS/HTTP/bytes correspondentes | Declaração de entrega pública |
| Fechamento | Registro antes/durante/depois e pendências explícitas | Conclusão da unidade |

`data/blog-status.json` é a projeção pública da última vistoria aceita. É um
snapshot datado, não monitoramento em tempo real. O recibo original do ciclo
continua em `docs/runs/`. Mudanças na fonte alimentam a fila da próxima ingestão,
não alteram silenciosamente o conhecimento publicado.

O gate estrutural canônico da Argenta continua uma ferramenta distinta do Blog.
Heuristik possui controles próprios; nunca recebe um PASS Argenta por analogia.
Testes, revisão consultiva e aceite humano são provas diferentes. A autorização
de execução completa do Pai não autoriza gastos, credenciais ou escopo privado.
