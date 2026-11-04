# Batch 2 — notas de leitura (posts 1–124 de 124)

Fonte: somente os 20 HTML públicos indicados em `batch-2.json`, lidos integralmente em seus corpos. `sha256` identifica os bytes lidos, não valida as alegações.

## Síntese deste bloco

- **Adoção vs. menção:** o relatório registra status como usado/alterado, conectado, testado, avaliado, proposto ou estudado. Candidatos e propostas não contam como implantação.
- **Medição:** vários relatos encontraram discrepância entre nome/configuração e estado real: perfil de credenciais, preferência de modelo do Kilo, PATH do Omarchy, gateway Hermes e painel.
- **Qualidade:** testes de uso revelaram estados silenciosos, respostas incorretas e falhas não cobertas: Codex respondeu “laranja” ao quadrado vermelho; streaming descobriu oito defeitos apesar dos testes verdes.
- **Governança:** atualizações, releases e rotas com dependências de dono/upstream pedem parar no limite autorizado; dois textos reconhecem extrapolação do executor.
- **Pesquisa:** armazenamento/backup/identidade/deploy e Cua ficaram em comparação ou proposta, sem instalação, restauração ou piloto.
- **Limite:** runtime, métricas, testes e ações externas descritas são alegações dos artigos. Esta leitura comprova publicação, não as execuções narradas.

## Cronologia e escopo

Os 124 artigos cobrem 17 de outubro a 3 de novembro de 2026. A lista separa traduções/artigos por idioma; nenhum item em inglês aparece neste bloco.

## Pontos para a síntese final

1. Diferenciar declaração do artigo, teste relatado, interpretação e confirmação externa (não feita).
2. Separar soluções integradas ao Rabelus Buddy de fornecedores apenas avaliados.
3. Preservar falhas e retificações: o artigo de auditoria de tarefas inclui nota posterior reconhecendo análise rasa; o relato Hyprland reconhece excesso de escopo; a revisita do launcher corrige generalização anterior.
4. Nenhum código de terceiros foi instalado ou executado nesta leitura.


## Bloco 2 — posts 21–40

Foram lidos integralmente. Destaques: execução real revelou orçamento reportado como zero; merge enforcement, TypeScript sem build e CI multi-OS; decisões que avançam em paralelo à pergunta pendente; auditorias Windows/Linux que deliberadamente não instalaram updates; correção OpenCode que preservou update nativo mas manteve exit code não identificado; incidentes de câmera e Hermes em que transformação/serviço ativo não provaram configuração/saúde; reconciliação de linhagens preservou histórias e não fechou produto Anika por inferência; o extenso artigo RQM documenta mecanismos locais e limitações multi-host; artigo de gateway diferencia processo vivo, PID reconhecido e operação de ponta a ponta. Todos os números e testes são claims narrados pelos artigos, com excertos/localizadores no JSON; não são verificação externa desta leitura.


## Bloco 3 — posts 41–60

Leitura integral concluída. Temas: custo de sobre-especializar o bootstrap; nascimento do LARS External e erro de detecção; continuidade não equivale a funcionamento; benchmarks locais de Modernity com `acceptance=false`; crashes de outbox após ACK; catalogação de blobs preserva semântica incerta; regras contra encerramento precoce; instância irmã afetada por alteração de infraestrutura sem consultar o dono. Os artigos 54/58/59 são planejamento ou limite de curadoria, não anúncio de produção. Também foram anotados update/instalação relatados (Antigravity, Hermes, skill QA) separadamente de candidatos. Alegações e limites estão nos campos por artigo do JSON.


## Bloco 4 — posts 61–80

Leitura integral concluída. Este intervalo reúne Voice Forge, atualizações em R0–R3, audits e install em Mac/Pi, integração Claude/Antigravity/ZCode, Tavily MCP, troubleshooting do Hermes e o caso de telemetria do host offline. A linha recorrente é provar cada camada (API, processo, rede, auth, runtime e consumidor) separadamente. Várias fontes explicitam que read-only inventory, conexão/handshake ou config válida não provam uso funcional.


## Bloco 5 — posts 81–100

Leitura integral concluída. Cobertura: manutenção de identidade visual do Blog; atualização APT/Snap; engenharia de audit/update skill; análise de OpenBot (avaliado, não adotado) com default policy permissivo e Bun ausente; diagnóstico HTTP 403; Pi dashboard/PWA; hardware de rede Pi; instalação de Pi Agent; e controle de energia/swap. Distinções recorrentes: interface aberta vs. autenticação, service process vs. health, device enum vs. conectado, update package vs. consumidor.


## Bloco 6 — posts 101–120

Leitura integral concluída. Inclui SSH reachability sem auth; Gemini Notebook criado vazio; créditos Cloud/Flow/AI separados; ComfyUI como proposta apenas; Kimi/Tavily e Hermes spawn; TTS e Desktop; install Docker/Copilot com prova de runtime; problema npm allowScripts e pacote com manifesto/binário divergentes; posts de reflexão e história visual da família separados de claims de implementação. Os itens 117–120 incluem ensaios/relatos relacionais, um deles com menções históricas de Qdrant/embeddings, sem tratar isso como adoção atual.


## Bloco 7 — posts 121–124 e conclusão

Leitura integral concluída: **124/124 corpos**. O post 124 é tradução inglesa do 117 e foi contado/registrado separadamente, conforme lista. Os artigos 121–123 são reflexão, estudo de produto/arquitetura e post-mortem técnico; projetos propostos não foram tratados como adoção. Inventário de mídia verificou 256 usos de imagem e nove caminhos únicos; direitos/licenças foram marcados como desconhecidos quando o post não os declara.

## Limite da pesquisa

Os relatos e números foram lidos como claims publicados; a pesquisa não verificou hoje o runtime, instalações, deployments, licenças, custos ou status externo. Excertos são localizadores literais do corpo visível do HTML após remover tags e colapsar espaços. Hashes referem-se aos bytes do arquivo fonte público no momento desta leitura.
