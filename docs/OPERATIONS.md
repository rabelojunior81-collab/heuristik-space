# Operação, atualização e recuperação

## Executar

Prévia: `python -m http.server 8780 --bind 127.0.0.1` na raiz. Python e Node são ferramentas de desenvolvimento/verificação; o visitante do Pages precisa de navegador com JavaScript.

Runtime adicional: `docker compose up -d --build`. Endereço: `http://127.0.0.1:4173/`. Use `docker compose ps` para estado/saúde e `docker compose logs --tail 80 web` para diagnóstico. `docker compose stop web` interrompe por decisão humana; `docker compose start web` retoma. Não parar ou recriar serviços de outro projeto.

`unless-stopped` recupera saída do processo e volta com o daemon, respeitando parada manual. Healthcheck em `/healthz` indica saúde; não reinicia sozinho um processo congelado. Host e Docker precisam estar ativos. Este projeto não configura inicialização do Docker no logon ou antes do login. GitHub Pages é independente do computador local.

## Imagem e persistência

NGINX unprivileged Alpine, com digest imutável no Dockerfile conferido diretamente no registry em 04/11/2026. Sem pacotes adicionais. UID 101, raiz somente leitura, tmpfs de 16 MiB, capabilities removidas, no-new-privileges, limites de 128 MiB/0,5 CPU/64 PIDs e logs limitados. Porta publicada somente em loopback.

Sem volumes: o conhecimento é público, estático e versionado dentro da imagem. Recriar o contêiner não apaga esses arquivos. Não há banco pessoal mutável no runtime.

Fontes primárias: [imagem mantida](https://github.com/nginx/docker-nginx-unprivileged), [reinício Docker](https://docs.docker.com/engine/containers/start-containers-automatically/), [Compose](https://docs.docker.com/reference/compose-file/services/) e [build](https://docs.docker.com/build/building/best-practices/). A proposta inicial do leitor continha outra referência de imagem; o executor substituiu pela referência resolvida no registry e preservou o intake como tentativa.

Atualizar: consultar release/tag estável, resolver digest, revisar diff, registrar versões, construir e testar. Guardar imagem anterior antes de trocar. Rollback por revisão Git anterior mais rebuild/recriação controlada, ou imagem anterior registrada. Não fazer prune global.

## Ingerir uma edição

1. Abrir run com intenção, versão e contrato. Conferir CNAME vigente do Blog e autorização do corte. Fonte nova exige leitura integral/revisão; contrato não é derivado da saída.
2. `python scripts/inspect_blog.py --blog ../lars-rabelus/blog` cria recibo novo de manifesto/HTTP/TLS/hash/diferenças. É snapshot, não monitoramento permanente.
3. Consolidar relatórios/relações. `python scripts/build_data.py --blog ../lars-rabelus/blog --output .runtime/candidate-N/data --blog-survey docs/runs/SURVEY/blog-status.json` recusa diretório existente e não escreve na base servida.
4. `python scripts/validate.py --data .runtime/candidate-N/data --out docs/runs/RUN/admission.json`. FAIL bloqueia promoção.
5. Conferir semântica/controles negativos. `python scripts/promote.py --candidate .runtime/candidate-N/data --run docs/runs/RUN --blog-survey docs/runs/SURVEY/blog-status.json` exige vistoria PASS da mesma origem/corte e deste ciclo diário. Base anterior fica preservada em `.runtime`.
6. QA real em 375/390/1440, testes, review consultivo e tratamento dos achados. Atualizar estado/changelog e sincronizar caminhos próprios.
7. Workflow valida, empacota e publica o mesmo SHA. Conferir Pages/HTTPS/bytes/interface e emitir recibo. Aceite humano é separado.

## Falha ou interrupção

Cada tentativa tem run próprio. Se existir `.runtime/promotion-pending.json`, conferir intenção, estágio, backup e base antes de recuperação explícita. Não apagar a barreira para tentar novamente. DNS/TLS não autorizam desligar HTTPS nem mudar domínio por inferência. Reverter somente delta próprio, preservando histórico e posses alheias.

Recuperação de promoção: interromper novos escritores; preservar uma cópia da intenção e inventariar os hashes da base, do candidato, do estágio e do backup. Se não houver intenção, um estágio órfão não prova promoção: arquivá-lo com registro, sem substituir a base. Com intenção, comparar cada árvore com os hashes nela registrados. Base íntegra anterior significa promoção não concluída; base íntegra candidata significa concluir somente o recibo após conferir o backup. Base ausente exige restaurar o backup anterior comprovado; árvore divergente exige diagnóstico, sem sobrepor dados. Só depois registrar a decisão e arquivar a barreira e os estágios, preservando evidências. Os controles exercitam falha durante staging, barreira pendente e ciclos distintos; não simulam corte de energia em cada instrução nem certificam essa recuperação manual de ponta a ponta.

## Rotina completa registrada

`python scripts/ingest.py --blog ../lars-rabelus/blog` cria um run novo, registra intenção/etapas/falhas com horárioUTC e fsync, vistoria o Blog, gera candidato separado e executa admissão mais controles negativos. `--promote` instala apenas a base local depois desses gates; publicação ainda exige QA, revisão e selo. As evidências ficam em docs/runs e o candidato em .runtime.

A edição0.1.0 tem373 fontes; futuras edições usam o tamanho declarado no contrato de entrada, não um contador produzido pela saída. Novo corte exige revisão versionada de contrato/corpus/manifesto e recibos dos artigos afetados. O workflow de Pages rejeita objeto diferente do manifesto revisado e recibos nãoPASS. Não há cron de publicação nem chamada automática a modelos.

O servidor usa um worker NGINX para a cota de 0,5 CPU. A imagem declara versão do aplicativo0.1.0; revisão Git não é inferida de labels da base. Identidade do runtime é conferida por imagem e hashes de conteúdo nos recibos.

O selo exige quatro camadas distintas vinculadas aos arquivos pertinentes. Browser e Docker incluem todos os corpos lazy, ativos, página404 e documentos empacotados. O ensaio Docker confere cada arquivo servido; no browser a captura de hashes delimita o objeto do ensaio, sem alegar inspeção visual individual de373 fontes. Alterar esses arquivos invalida o recibo da camada, mesmo após nova revisão. Deploy é restrito explicitamente à main, inclusive disparo manual.
