# Batch 1 — notas incrementais (125 fontes)

## Estado

- 125/125 artigos, incluindo as traduções EN, lidos integralmente por partes; hashes SHA-256, metadados e recibos estão em `batch-1-report.json`.
- `read_status` foi conferido para 125/125; não há `not_read`.
- As fontes são posts públicos documentais, não prova do estado/runtime atual. Os resumos/claims são relato ou interpretação explicitamente qualificada, não adoção derivada de menção.
- A leitura foi organizada por lotes para contornar limite de saída; extração de HTML serviu para exibir texto e não substituiu a leitura dos corpos completos.

## Entidades e relações

`projects` e `technologies` listam nomes de projeto/tecnologia encontrados nos corpos, sem inferir uso ou adoção pela menção. Relações afirmadas e limites ficam nos claims, com excerto do artigo. `media` lista referências presentes no HTML; direitos não foram presumidos e permanecem unknown salvo evidência expressa.

## Síntese transversal provisória

Os artigos repetem cinco fronteiras: pedido e interpretação; configuração/rótulo e execução efetiva; teste unitário/mock e consumidor real; capability e autorização; relato de correção e prova de adoção/aceite. Casos destacados incluem versões diferentes do mesmo `dsh`, telemetria baseada em fonte legada, evento/commit sem push, dado persistido sem visualização, mock que não reproduz política real, container saudável sem prova de boot/recuperação, e aplicação pública de teste sem curadoria comercial.

Padrões fortes de acerto narrado: medir antes/depois no alvo real; distinguir hipótese/relato/confirmado; preservar artefatos e registrar rollback; testar falha/controle negativo; manter owner/canal explícitos; parar em lacunas de prova. Padrões de falha narrados: green incompleto, UI não observada, ferramenta de QA sem validação, escopo ou autorização inferidos, fontes/versões stale, correção posterior apresentada como se fosse anterior. Estes são temas da amostra selecionada, não taxa estatística de falhas da família.

## Fontes e limites

O artigo 2 explicitamente reporta auditoria documental de 52 itens selecionados, não de todo o catálogo. Nenhum post público estabelece estado atual dos hosts. Confirmação de runtime, direitos de mídia, aceitação humana e adoção em cada harness permanecem fora desta leitura. Os campos `media` permanecem sem direitos confirmados quando o post não os documenta; ausência de informação é registrada como unknown e não como autorização.
