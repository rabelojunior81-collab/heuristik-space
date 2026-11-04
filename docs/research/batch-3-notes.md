# Batch 3 — notas de leitura

Escopo atual: itens 1–94 do índice original batch-3.json. Fonte permitida: corpos HTML públicos em lars-rabelus/blog/posts/. Cada item read significa corpo integralmente lido; extração só auxilia navegação. SHA-256 do HTML registrado. Não certificar runtime pelo relato.

Progresso: 94/94 itens do escopo lidos integralmente; 0 pendentes. Os itens originais 95–124 foram redistribuídos para batch-4-report.json e removidos deste JSON para evitar duplicação. Não foram lidos por este agente.

A amostra final separa falha de rádio/kernel de DHCP/política, imagem preparada de sistema inicializado, mudança visual de alteração funcional, e processo já encerrado de serviço ativo.

## Correção de citações após gate

O gate de citações identificou 10 excertos não localizados no corpo `post-content` (QA `batch-3-corrections.json`). Corrigi os excertos nos claims correspondentes usando passagens contíguas do HTML congelado `source-html/0b98e4c2d084db43e2679c3947d56bf9dff833e7`; preservei o SHA-256 e `read_status` de cada fonte e mantive a interpretação/limitação dos claims. Revalidação com a mesma extração `Body` e normalização de `scripts/build_data.py`: 10 artigos, 34 excertos de seus claims verificados, 0 falhas. Correção referente ao registro anterior no commit `851a1df`; não foi feita operação Git.
