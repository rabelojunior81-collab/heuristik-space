# Luna repair 1

- Patches de alegações: 51 (alvo: 51 falhas do validador).
- Relações heurísticas: 25 (alvo solicitado: 25–45).
- Escopo: correções e relações documentais propostas; relatos históricos não afirmam runtime atual.
- Fonte: corpos capturados no commit `0b98e4c2d084db43e2679c3947d56bf9dff833e7`; relatório `docs/research/batch-1-report.json`.
- Cada patch reduz a alegação ao texto literal escolhido do corpo e mantém confiança/limitação original, acrescentando limite temporal.
- Relações usam IDs do catálogo em `scripts/build_data.py`; evidências citam trechos de corpo.
- Limite da leitura: algumas alegações originais agregavam contexto que não cabe no trecho citado; nesses casos a proposta recua para uma afirmação metadocumental (o artigo registra a frase), em vez de atribuir ao texto um resultado técnico não sustentado pelo excerto. As relações são candidatas para triagem semântica antes da integração.
