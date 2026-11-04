# SPEC0.1 — Heuristik Space

Estado: APROVADA pelo Pai, resposta nominal “Aprovar SPEC0.1” na conversa Codex em03/11/2026. Fonte: direção aprovada na conversa e briefing de criação do projeto em03/11/2026, com correção posterior de domínio. Esta revisão materializa o contrato antes da implementação.

## Resultado e escopo

Plataforma pública estática de conhecimento do Lab, em heuristik.space, repo público heuristik-space. Pesquisa integral dos373posts publicados do corpus0b98e4c, com contagem por arquivo/idioma, SHA e recibos; novos posts após o corte entram como atualização posterior. Cruzar com39referências da wiki GitHub e identificar também ferramentas/soluções próprias além daquela lista. O inventário contempla todos os autores e períodos. Tradução tem recibo próprio, sem duplicar a contagem de uma mesma ocorrência conceitual.

## Requisitos observáveis

R01 Fontes: cada artigo tem recibo, resumo de leitura, data/autor/hash; mapa de cobertura revela leituras não concluídas. Leitura mecânica não equivale a compreensão integral.
R02 Conhecimento: fichas de projetos, soluções, frameworks/configurações, caminhos por problema, autor e assunto; fonte por alegação, cronologia e grau de certeza. Separar usado/adaptado/inspirado/considerado/semelhança; runtime atual não inferido do post.
R03 Navegação: busca local normalizada com sinônimos e pesos explicáveis, filtros combináveis, rotas/link profundo para ficha/caminho, fontes retornáveis; lista vazia, erro de dados e retorno navegável. Sem chamar embeddings remotos ou prometer busca semântica neural.
R04 Agentes: copiar URL/ficha/contexto geral, exportações TXT/JSON DATA_ONLY com fontes e limites, alternativa de seleção/download se clipboard indisponível. Tudo gerado dos registros naturais de pesquisa.
R05 Visual: bege escuro e vidro chanfrado, cantos8–14px como proposta, luz quente e objeto3D decorativo leve em CSS/SVG, movimento discreto com prefers-reduced-motion. Nova identidade; fonte aberta próxima da referência. Fênix/passagem como proposta de logomarca própria, sem afirmar emblema canônico de toda a Família.
R06 Mobile primeiro:375×812e390×844 e desktop1440×900, sem rolagem horizontal; alvos de interação confortáveis, foco visível, navegação teclado, headings/labels, contraste legível, backdrop-filter com fallback. Nada de autoplay de áudio/vídeo.
R07 Mídias: selecionar ativos pertinentes do Blog, verificar contexto/licença/proveniência e atribuir em registro de créditos; evitar copiar mídias de terceiros com direitos desconhecidos. Imagens otimizadas/lazyload e áudio/vídeo só por demanda quando pertinente ao conteúdo.
R08 Open source: README visual com marca/links/arquitetura/execução/contribuição/limites; LICENSE código próprio, créditos/licenças dos ativos separados, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG e docs da metodologia e atualização dos dados. Não publicar dados privados, identificadores de sessão ou runtime.
R09 Entrega: repo público, Pages habilitado, CNAME heuristik.space; comprovar DNS/TLS, build exato, HTTP e conteúdo, interface real no browser; post final no Blog rabelus.com.br com URL e limites reais.

## Fronteiras e autoridade

A ordem atual autoriza pasta/repo públicos, Pages/domínio, pesquisa e desenho proposto. Instalações, gasto extra, contas novas, alteração de outras casas, adoção de tecnologias nos produtos do Lab e publicação de dados privados ficam fora. Alteração material da estética, navegação ou conteúdo volta ao Pai. Revogação por instrução explícita interrompe o efeito dependente. Proposta técnica: HTML/CSS/JS e dados estáticos, sem build nem backend pago; nenhuma dependência de runtime instalada. Funcionalidades remotas/autenticação/analytics não pertencem a esta revisão; a aprovação confirma esses limites.

## Provas e rollback

Pesquisa: cobertura373 e conferência amostral do orquestrador, evidências por alegação. Produto: testes reais de busca/filtros/links/cópia/fallback, validação de dados e caminhos inválidos; screenshots e estadosDOM em viewports definidos; desempenho/movimento e teclado. Deploy: commit +Pages +HTTP/TLS e paridade de arquivos selecionados. Rollback por commit próprio, sem apagar conteúdo, reescrever história ou tocar configuração alheia. Falha de DNS/conta não é contornada.

Gates: aprovação desta SPEC antes do plano/implementação; autorização do plano antes da execução; review consultivo por etapa com pacote público/hash e limites; prova objetiva e visual antes de conclusão. Aceitação final do Pai será solicitada após a apresentação real; não será inferida. Campos inaplicáveis propostos: banco/autenticação/backend/instalação/modelo pago, porque o produto desta revisão é estático e público. Revisão aprovada não dispensa testes nem direitos de mídia.
