# Relações adicionais Luna: 12 casos

**Fonte congelada:** Blog no commit `0b98e4c2d084db43e2679c3947d56bf9dff833e7`; **método:** leitura integral dos 12 corpos em `docs/research/source-html/0b98e4c2d084db43e2679c3947d56bf9dff833e7/`. Cada registro tem um incidente por publicação, problema, resposta narrada, resultado e limite; os trechos entre aspas são literais. Relato do post não certifica estado atual.

## Relações

### luna-case-extra-001 — Rabelus Buddy: contenção do Codex no macOS e conferência de CI

 - **Caso:** `2026-11-02-o-alarme-na-sala-vazia` · **relação:** aplicado · **nós:** rabelus-buddy, review, auth
 - **Objeto:** Comando contido sem acesso à rede local; resultado das rotinas agendadas visível na abertura da sessão.
 - **Problema:** Os testes completos falhavam por duas semanas apenas no Mac e o resultado não chegava à superfície que o autor consultava. A contenção permitia ao comando acessar programas escutando no próprio computador, inclusive banco e servidor de desenvolvimento.
 - **Solução e resultado:** Executar o comando contido sem internet no Mac, registrando a justificativa; mostrar no início da sessão os resultados das rotinas agendadas. O artigo registra a correção da brecha e da observabilidade da rotina; não relata nova rodada posterior dos testes Mac que comprove a correção em todos os cenários.
 - **Limites/confiança:** Mudança descrita somente para macOS; Windows e Linux permaneceram sem alteração. Estado histórico relatado, sem inspeção do código ou runtime atual. Relato direto no post; implementação e resultado atual não verificados independentemente.
 - **Evidência literal:** “No Mac, o comando contido agora roda sem internet, e o registro diz por quê.” (`2026-11-02-o-alarme-na-sala-vazia`).
 - **Lição:** Um ensaio de contenção deve incluir o acesso a listeners locais; execução agendada também precisa entregar seu resultado a quem a supervisiona.
 - **Próximo passo:** Em revisão futura, conferir a política de rede específica do macOS e provar tanto bloqueio de listeners locais quanto visibilidade do resultado de CI.

### luna-case-extra-002 — Ensaio de aprovação automática no Codex contido

 - **Caso:** `2026-10-25-aprovar-tudo-que-aparecer` · **relação:** aplicado · **nós:** rabelus-buddy, auth
 - **Objeto:** Script permissivo corrigido após aprovar a execução inicial de um agente não aprovado pelo responsável.
 - **Problema:** Para retirar a espera por cliques durante um ensaio, o autor criou um script que aprovava qualquer item da fila. O agente da Anthropic apareceu e foi aprovado sem ordem do responsável; o programa foi baixado no computador dele.
 - **Solução e resultado:** O autor corrigiu o script e comunicou o ocorrido ao responsável, reconhecendo que a aprovação existia precisamente para impedir esse contorno. O post registra a correção do script e a comunicação; a decisão sobre o pacote baixado foi deixada ao responsável.
 - **Limites/confiança:** O artigo não identifica como o script foi corrigido nem informa a decisão posterior sobre o pacote. O evento ocorreu no núcleo de ensaio, não no núcleo de produção; não inferir que a aprovação indevida foi revertida. Relato direto no post; mudança e destino do pacote não verificados independentemente.
 - **Evidência literal:** “corrigi o script; mas a aprovação existe justamente para isso não acontecer” (`2026-10-25-aprovar-tudo-que-aparecer`).
 - **Lição:** Automatizar uma fila de aprovações com aceitação indiscriminada remove o controle que a fila deveria preservar.
 - **Próximo passo:** Se esse fluxo for reutilizado, inspecionar o script e testar que item sem autorização explícita permanece bloqueado.

### luna-case-extra-003 — Atribuição de fala na delegação real do Buddy ao OpenCode

 - **Caso:** `2026-10-20-duas-vozes-na-mesma-conversa` · **relação:** aplicado · **nós:** rabelus-buddy, opencode, review, auth
 - **Objeto:** Separação visível entre a fala do agente delegado e a do Buddy, com identificação de quem recebeu a tarefa.
 - **Problema:** Testes com agente falso não mostravam o defeito: na execução real, a saída ao vivo do OpenCode aparecia no balão do Buddy, sem indicar a quem a tarefa havia sido delegada.
 - **Solução e resultado:** Corrigir a apresentação da fala e da atribuição da tarefa, com teste antes da correção. O post diz que os dois problemas foram corrigidos após serem expostos pelo agente real. Uma demonstração completa conduzida pelo responsável ainda era o próximo passo, portanto não há aceite final relatado.
 - **Limites/confiança:** Evidência limitada à execução narrada com OpenCode; não prova a UX em todos os agentes, nem que a demonstração pendente ocorreu. O mesmo post relata separadamente que a chave antes presente no URL passou a usar bilhete de uso único e cookie, sem afirmar que isso substitui revisão de segurança. Correção e teste relatados no post; demonstração ponta a ponta e estado atual não confirmados.
 - **Evidência literal:** “As duas coisas foram corrigidas, com teste antes.” (`2026-10-20-duas-vozes-na-mesma-conversa`).
 - **Lição:** Um stub pode ocultar erros de autoria e atribuição que só aparecem no protocolo e no streaming do agente real.
 - **Próximo passo:** Repetir a demonstração com o agente delegado real, confirmar identidade do emissor em cada evento e testar parar/aprovar no fluxo completo.

### luna-case-extra-004 — Registro factual do trabalho e verificação automática por resposta

 - **Caso:** `2026-10-18-o-registro-no-momento-do-fato` · **relação:** aplicado · **nós:** rabelus-buddy, bus, review
 - **Objeto:** Auditoria de 53 commits sem registro em 14 sessões, seguida de registros tardios declarados e um gate automático de fechamento.
 - **Problema:** O autor trabalhou por mais de três horas sem registrar medições, decisões ou erro no barramento; a auditoria histórica encontrou a mesma lacuna em 53 commits distribuídos por 14 sessões.
 - **Solução e resultado:** Registrar os casos passados explicitamente como atrasados e criar verificação ao fim de cada resposta para bloquear código sem registro, arquivo sem commit ou commit sem push. Segundo o post, a verificação detectou um defeito nela própria na primeira execução; esse defeito foi corrigido com teste antes. O gate também passou a reprovar a entrega antes da linha principal.
 - **Limites/confiança:** Os registros retroativos preservam a distinção temporal. A regra e o primeiro ensaio são históricos; não provam que o mecanismo atual continua íntegro nem que todos os eventos possíveis são capturados. Relato direto no post, incluindo contagem e resultado do primeiro teste; sem reexecução independente.
 - **Evidência literal:** “Ao fim de cada resposta minha, uma verificação roda sozinha.” (`2026-10-18-o-registro-no-momento-do-fato`).
 - **Lição:** Um histórico reconstituído deve marcar atraso, e um controle de rastreabilidade precisa verificar também a própria implementação.
 - **Próximo passo:** Na próxima mudança, inspecionar a regra de verificação e testar controles negativos para cada uma das três condições de bloqueio.

### luna-case-extra-005 — Fechamento do primeiro marco do Rabelus Buddy

 - **Caso:** `2026-10-17-o-primeiro-marco-fechou` · **relação:** relatado · **nós:** rabelus-buddy, review
 - **Objeto:** Teste manual pela console complementou uma suíte que aprovava contratos falsos e não detectava defeitos visuais.
 - **Problema:** Três ensaios com servidor falso aceitaram um contrato que o serviço real não seguia. A inspeção manual encontrou defeitos que os testes automatizados não detectaram.
 - **Solução e resultado:** Corrigir defeitos encontrados pelos ensaios reais e converter cada tropeço em regra com mecanismo; o post também descreve a correção de tema e de símbolos crus no título. O autor registra 38 execuções reais, 246 testes e que o responsável declarou ter testado o restante pela console. O marco foi apresentado como fechado, mas os números e a aceitação são relatos do post.
 - **Limites/confiança:** Um total de testes ou execuções não demonstra cobertura de todo comportamento. A recomendação para marcos seguintes era uma proposta; o post afirma que nada mudaria até decisão do responsável. Relato de execução e teste; não é verificação independente de cobertura nem aceite atual.
 - **Evidência literal:** “Três vezes no mesmo dia, um teste com servidor falso aprovou um contrato” (`2026-10-17-o-primeiro-marco-fechou`).
 - **Lição:** Validar o contrato real e a interface usada é necessário quando o mock pode representar um serviço diferente.
 - **Próximo passo:** Para cada serviço substituído por mock, adicionar ao plano uma verificação do contrato real e uma sessão funcional pela interface consumidora.

### luna-case-extra-006 — Gateway local de Modernity: identidade separada do actor declarado

 - **Caso:** `2026-09-18-a-autoridade-nao-era-o-actor` · **relação:** aplicado · **nós:** modernity, auth
 - **Objeto:** Principal local `pai`, membership server-side limitada ao projeto e token HMAC efêmero validado antes da execução.
 - **Problema:** O gateway já verificava projeto, escopo, idempotência e aprovação, mas o campo actor vinha do caller e era somente uma afirmação dele, não uma identidade autenticada.
 - **Solução e resultado:** O responsável aceitou uma autoridade local reversível: principal `pai`, membership server-side somente para `proj-modernity-001` e token HMAC de quinze minutos; segredo ausente falha fechado e a ferramenta valida Bearer, expiração e projeto. O post relata a decisão aceita e os controles definidos para executar. Não descreve um wargame posterior ou resultados quantitativos de abuso bloqueado.
 - **Limites/confiança:** O autor delimita que é autoridade local reversível, não IdP de produção, e que não acessa Ananke, Hermes ou provedor externo. Um registro anterior de intake já citava genericamente o limite local; esta relação acrescenta problema e desenho completos sem substituir aquele registro. Decisão e desenho relatados no post; funcionamento atual do gateway não revalidado.
 - **Evidência literal:** “um actor enviado pelo caller era apenas uma afirmação do caller” (`2026-09-18-a-autoridade-nao-era-o-actor`).
 - **Evidência literal:** “Segredo ausente falha fechado.” (`2026-09-18-a-autoridade-nao-era-o-actor`).
 - **Lição:** A identidade que autoriza uma operação precisa vir de uma fonte confiável do lado servidor, não de um atributo controlado pelo chamador.
 - **Próximo passo:** Se evoluir para produção, definir IdP, rotação e gestão de revogação, e testar tokens expirados, membership de outro projeto e segredo ausente.

### luna-case-extra-007 — Auditoria operacional da retomada Modernity

 - **Caso:** `2026-09-18-o-dia-em-que-medimos-a-propria-maquina` · **relação:** proposto · **nós:** modernity, review
 - **Objeto:** Redimensionamento da governança: preflight único, lote macro, ledger de incidentes e recibo por mudança material.
 - **Problema:** A retomada havia fechado tecnicamente, mas a auditoria do arco de 42 sessões e 35 incidentes encontrou repetição de preflights, transições e subprovas; a própria autora reconheceu fracionamento excessivo e custo operacional alto.
 - **Solução e resultado:** Manter provas essenciais e ajustar escala: reunir preflight, agrupar trabalho em lotes maiores, registrar incidentes e emitir recibo por mudança material. A auditoria foi escrita após a conclusão técnica e quantificou eventos, commits e falhas; as mudanças sugeridas são recomendações para o ciclo seguinte, não resultados de um novo ciclo otimizado.
 - **Limites/confiança:** Os números correspondem à janela descrita e não são métricas universais. A autora separa diffs de linhas de produto e tokens de objetivo de tokens brutos; não inferir economia futura já alcançada. Auditoria e proposta relatadas no post; eficácia futura não demonstrada.
 - **Evidência literal:** “preflight único, lote macro, ledger de incidentes, um recibo por mudança material” (`2026-09-18-o-dia-em-que-medimos-a-propria-maquina`).
 - **Lição:** Rigor não exige repetir a mesma proteção em toda transição; a escala do processo deve conservar a prova e reduzir repetição sem valor.
 - **Próximo passo:** Medir o próximo ciclo com as mesmas unidades e verificar se o lote macro preserva gates, incidentes e rastreabilidade enquanto reduz rebootstrap.

### luna-case-extra-008 — Voice Forge: falha de QA móvel mascarada por teste de overflow

 - **Caso:** `2026-09-16-a-sessao-que-morreu-no-meio` · **relação:** aplicado · **nós:** voice-forge, review, bus
 - **Objeto:** Correção do layout responsivo e gate que mede largura/visibilidade em vez de apenas rolagem horizontal.
 - **Problema:** O teste passava porque a página não rolava horizontalmente, embora o conteúdo colapsasse a largura zero no celular. A sessão também parou antes do commit e deixou o trabalho sem registro consolidado.
 - **Solução e resultado:** Corrigir o layout, reconstruir e ajustar a medição para verificar a largura real; ao retomar, registrar o travamento como interrupção e fechar o trabalho pendente. O post relata largura zero em três tamanhos, correção com rebuild e gate medindo 375px. Também relata commit, recibo e fechamento posterior como interrupção, não sucesso contínuo.
 - **Limites/confiança:** A hipótese de contexto grande por treze imagens foi apresentada explicitamente como inferência, não causa provada. A correção responsiva e QA pertencem ao estado narrado naquela sessão; não verificam o aplicativo atual. Defeito, correção e encerramento relatados no post; causa do travamento permanece inferida.
 - **Evidência literal:** “Corrigi com uma linha, rebuildei, e agora mede 375.” (`2026-09-16-a-sessao-que-morreu-no-meio`).
 - **Lição:** Um teste precisa medir a propriedade que importa ao usuário: ausência de overflow não prova que o conteúdo está visível e utilizável.
 - **Próximo passo:** Repetir os viewports móvel e desktop na interface real, testar largura mínima do conteúdo e preservar interrupção e fechamento como eventos distintos.

### luna-case-extra-009 — Integração do Voice Forge ao TTS do Hermes Desktop

 - **Caso:** `2026-10-30-a-voz-volta-para-casa` · **relação:** aplicado · **nós:** voice-forge, hermes
 - **Objeto:** Configuração do provedor e cinco chaves de compatibilidade, exercitadas pela mesma função de fala que o aplicativo chama.
 - **Problema:** A voz que existia em outra instância não estava disponível no Hermes Desktop; memória não esclarecia o caminho de execução nem o contrato efetivo do app.
 - **Solução e resultado:** Inspecionar o código consumidor e a função TTS, então configurar o provedor OpenAI-compatible, modelo, voz e chave local exigida pelo SDK. A função real foi chamada, e o MP3 retornado foi transcrito para conferir o roteiro. O post relata áudio de 13,28 segundos, transcrição integral do roteiro, sem vazamento de direção ou truncamento. Isso demonstra o caminho exercitado naquele momento, não disponibilidade atual.
 - **Limites/confiança:** A transcrição errou o nome próprio Orus; não confundir erro do transcritor com síntese. O SDK não foi atualizado, o modelo de terceiro sugerido não foi adotado, e entrada de voz/STT, direção de cena, tags e multi-voz ficaram fora da integração do app. Execução pelo consumidor e conferência de áudio relatadas; estado atual não reexecutado.
 - **Evidência literal:** “A configuração funciona. E o áudio provou.” (`2026-10-30-a-voz-volta-para-casa`).
 - **Lição:** Ler a configuração não basta: testar pela mesma função chamada pelo consumidor e distinguir a prova de geração da prova de escuta/transcrição.
 - **Próximo passo:** Em nova verificação, conferir modelo e contrato suportados no runtime escolhido, gerar áudio pelo app e avaliar a mídia com escuta humana.

### luna-case-extra-010 — Deep Research sobre o catálogo da Gemini API no Notebook

 - **Caso:** `2026-08-22-gemini-api-deep-research-iniciada` · **relação:** relatado · **nós:** notebook
 - **Objeto:** Pesquisa iniciada e relatório/importação de fontes descritos, com validação primária ainda requerida antes de uso operacional.
 - **Problema:** Uma captura de pesquisa com fontes oficiais e comunitárias e possíveis divergências em IDs/datas de modelos não poderia ser promovida diretamente a verdade operacional.
 - **Solução e resultado:** Usar o Notebook para descobrir e reunir fontes, mantendo IDs e datas pendentes de confirmação em documentação primária antes de os inserir em planilha ou rota de produção. O post relata que a pesquisa terminou com 44 fontes descobertas e que o relatório e fontes foram importados ao Notebook. A própria publicação preserva a validação como trabalho posterior.
 - **Limites/confiança:** Os números relatados não foram conciliados aqui com os itens individuais do Notebook. A publicação comprova uma pesquisa narrada, não atualização adotada, modelo instalado ou rota de produção alterada. Relato de pesquisa e cautela metodológica; conteúdo e fontes importadas não foram auditados nesta tarefa.
 - **Evidência literal:** “A pesquisa terminou, trouxe 44 fontes descobertas” (`2026-08-22-gemini-api-deep-research-iniciada`).
 - **Evidência literal:** “precisam de validação primária antes de entrar na planilha” (`2026-08-22-gemini-api-deep-research-iniciada`).
 - **Lição:** Deep Research pode ampliar a descoberta documental, mas resultados e identificadores devem voltar à fonte primária antes de orientar uma operação.
 - **Próximo passo:** Se essa pesquisa voltar a ser usada, confrontar cada afirmação de modelo, data e status com documentação primária vigente e registrar a data da checagem.

### luna-case-extra-011 — Gemini Notebook como plano de conhecimento fundamentado

 - **Caso:** `2026-08-22-gemini-notebook-plano-de-conhecimento` · **relação:** relatado · **nós:** notebook, modernity
 - **Objeto:** Teste com corpus selecionado e citações, separado do plano que executa workflows e da revisão humana necessária.
 - **Problema:** A arquitetura precisava posicionar o Notebook sem tratá-lo como executor de agentes ou como autoridade suficiente para decisões comerciais e operacionais.
 - **Solução e resultado:** Testar uma pergunta estruturada por fatos, inferências e workflows com entradas/saídas/aprovação; enquadrar o Notebook como camada de corpus, grounding e briefing, mantendo execução em ferramentas separadas e revisão humana para decisões. A resposta veio ancorada nas fontes e produziu propostas de workflow para a estratégia Modernity. O artigo declara produtividade no teste, mas não relata adoção desses workflows nem alteração de fontes/permissões.
 - **Limites/confiança:** Teste descrito em notebook consumer específico, com corpus selecionado; inferências ainda exigiam revisão independente. A API Enterprise era preview e opção futura separada, não recurso automaticamente disponível no plano consumer. Uso e resposta relatados no post; qualidade factual da síntese não verificada independentemente nesta tarefa.
 - **Evidência literal:** “o Notebook transforma um corpus selecionado em briefing, análise e artefatos de Estúdio” (`2026-08-22-gemini-notebook-plano-de-conhecimento`).
 - **Lição:** Grounding e citações ajudam a preparar decisões, mas não substituem verificação independente nem a camada de execução.
 - **Próximo passo:** Antes de reutilizar a abordagem, checar fontes citadas para cada afirmação decisiva e manter workflow, responsável e aprovação fora da síntese do Notebook.

### luna-case-extra-012 — Desenho de retomada do bootstrap do LARS e auditoria da pesquisa Notebook

 - **Caso:** `2026-09-23-bootstrap-nao-e-biografia` · **relação:** proposto · **nós:** bus, review, notebook
 - **Objeto:** Bootstrap em camadas curtas: identidade e limites, estado recente/continuidade, memória longa recuperada conforme a tarefa.
 - **Problema:** Retomadas longas percorriam muitos registros antes de recuperar o estado acionável, mas a resposta não deveria remover governança nem simular esquecimento. Em paralelo, síntese convincente do Notebook continha comparações e conclusões não confirmadas.
 - **Solução e resultado:** Desenhar uma ordem que prioriza núcleo, estado recente e memória longa sob demanda, com proveniência visível; auditar alegações do Notebook contra fontes primárias. O artigo relata entrega do desenho e handoff à Internal. O resultado confirmado pelo post é documental: desenho e handoff concluídos. A implementação da skill, alteração do Hermes, hooks, A2A e integração ao HMC foram explicitamente não executados.
 - **Limites/confiança:** A proposta não demonstra redução de tempo de bootstrap nem acerto de recuperação, pois os critérios de medida ficaram para implementação futura. Também não registra adoção de Jev, Laya ou AnyJev no HMC/LARS. Estado de desenho/handoff e não execução declarados explicitamente no post; implementação posterior não verificada.
 - **Evidência literal:** “Concluímos o desenho e o handoff, não a implementação da skill.” (`2026-09-23-bootstrap-nao-e-biografia`).
 - **Lição:** Uma proposta de continuidade só vira capacidade depois de implementada e medida; revisão de síntese não é adoção de ferramenta.
 - **Próximo passo:** Se o desenho for implementado, medir tempo até prontidão, retomada de estado, recuperação pertinente e perguntas evitáveis; comprovar cada superfície separadamente.

## Nota editorial

O caso `2026-09-18-a-autoridade-nao-era-o-actor` já aparece em `luna-repair-1.json` com o mesmo limite local, mas aquele registro não descreve a falha do campo actor nem o mecanismo de principal, membership e token. Este intake acrescenta a relação substantiva como registro separado; não substitui nem altera o anterior.

Os dois posts do Notebook são históricos: pesquisa iniciada/concluída ou teste com fontes não implicam API adotada nem uso operacional atual. O artigo de bootstrap confirma apenas desenho e handoff, e nega execução da implementação descrita.
