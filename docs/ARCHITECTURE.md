# Arquitetura

Heuristik Space é uma aplicação estática: HTML, CSS, JavaScript ES Modules e JSON/TXT. O visitante não precisa de backend, banco, autenticação ou chave de modelo. GitHub Pages executa todas as funções previstas, independentemente do host local. Docker serve uma cópia adicional do aplicativo.

## Fluxo e moradas

Blog público → vistoria datada → corte Git/manifesto congelados → recibos de leitura → relações editoriais → candidato novo → admissão → promoção recuperável → QA/review → commit/Pages/bytes públicos.

- `docs/ingestion-contract.json`: entrada congelada independente da saída, com fontes, hashes, domínios e obrigações.
- `docs/research/batch-*-report.json`: resumos, alegações, limites, autoria e recibos da leitura distribuída.
- `docs/research/relations.json`: relações consolidadas editorialmente; coincidência de nomes não demonstra adoção.
- `data/knowledge.json`: índice do navegador; corpos integrais ficam em `data/articles/`, carregados sob demanda.
- `data/context.txt`: contexto DATA_ONLY com fontes e limites. Exportação não concede autoridade a agentes.
- `docs/runs/`: tentativas e recibos imutáveis. `.runtime/`: estágios e backups locais ignorados, sem publicação.

Menções candidatas e relações qualificadas permanecem separadas. Tradução não vira outra ocorrência conceitual. Histórias descrevem seu próprio momento; o aplicativo não sonda runtimes privados dos irmãos.

## Busca e interface

Busca local com acentos normalizados, sinônimos explícitos e peso maior no título. É lexical enriquecida, sem embeddings ou envio remoto da consulta. Quatro vistas, filtros de assunto/autoria, percursos, links profundos, fontes retornáveis e exportações. Conteúdo é escapado antes da renderização; links admitem apenas HTTP/HTTPS. Artigos usam caminhos controlados por slug validado.

## Publicação e recuperação

Pages recebe pacote por allowlist de `scripts/package_site.py`, sem Git, capturas brutas ou runtime. Docker usa o mesmo código e dados com UID 101, raiz somente leitura e porta de loopback. SHA de build, bytes públicos, inspeção da interface e aceite humano são provas distintas.

`promote.py` valida antes de tocar `data/`, registra intenção durável, confere baseline e preserva a árvore anterior em `.runtime/backup-*`. Interrupção deixa barreira para inspeção antes de nova promoção. Renomeações, Git e deploy não são uma única transação; não há promessa de atomicidade em power-loss ou alta disponibilidade. Versões públicas permanecem no Git. Rollback usa commit próprio e nova publicação, preservando trabalho concorrente.
