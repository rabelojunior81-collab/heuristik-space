# Pesquisa de implantação Docker local

**Data da consulta:** 2026-11-04. **Escopo:** servir o produto estático em paralelo ao GitHub Pages, sem banco, volumes de estado, credenciais ou acesso público pela porta local. A pesquisa usa somente conteúdo público e documentação oficial.

## Estado observado no host

- CONFIRMADO: `docker` encontrado em `C:\Program Files\Docker\Docker\resources\bin\docker.exe`, versão 29.6.2.
- CONFIRMADO: `docker compose version` retorna Compose v5.3.1.
- CONFIRMADO: consulta `docker info --format '{{.ServerVersion}}'` retornou daemon 29.6.2.
- Nenhuma imagem foi baixada, nenhum container criado/iniciado e nenhuma configuração do host foi alterada. A consulta ao daemon foi apenas para versão.

## Duas opções

| Opção | Vantagem | Custo/limite para este caso |
|---|---|---|
| `nginx/nginx-unprivileged` (recomendada) | Projeto oficial do Docker NGINX mantido pela NGINX/F5; usuário sem root por padrão, porta 8080, PID e caminhos temporários sob `/tmp`; adequado para servir arquivos estáticos. | Requer configuração própria pequena para `/healthz` e o site. Não termina HTTPS; isso é adequado porque o domínio público já é servido no Pages. |
| Imagem oficial `nginx` (ex.: `nginx:1.30.6-alpine3.24`) | Distribuição oficial ampla, simples para servir arquivos. | A imagem padrão inicia como root e usa porta 80; para cumprir o contrato seria preciso adaptar usuário, porta, PID, diretórios graváveis e entrypoint. É trabalho e superfície de erro desnecessários frente à variante sem privilégios. |

O mantenedor publica atualizações da variante sem privilégios em lançamentos/CVEs críticos e semanalmente; tags mutáveis podem apontar para builds novos. Para repetibilidade, a consulta ao pacote oficial de imagens registrava `nginx/nginx-unprivileged:1.30.6-alpine3.24` com digest `sha256:44e74ca483234093081138b6d7b6f561d55557756a2deefc3a5056148defeb99`. Referência candidata: `nginx/nginx-unprivileged:1.30.6-alpine3.24@sha256:44e74ca483234093081138b6d7b6f561d55557756a2deefc3a5056148defeb99`. Revalidar tag e digest na implementação e registrar arquitetura; a versão/tag e o digest acima são evidência datada, não promessa de que continuarão atuais.

## Desenho proposto

Arquivos estáticos são copiados na imagem em build; sem bind mount da pasta do projeto. Copiar apenas `index.html`, `app.js`, `styles.css`, `data/` e `assets/`, evitando `.git`, documentação, scripts de ingestão e recibos de pesquisa no container. Manter o Pages e seu HTTPS como publicação canônica independente. O serviço Compose fica em `127.0.0.1:4173:8080`, acessível somente localmente, sem rede externa publicada, TLS ou proxy.

Dockerfile proposto (na raiz do projeto; referência do `FROM` deve ser atualizada após rechecagem do digest):

```dockerfile
FROM nginx/nginx-unprivileged:1.30.6-alpine3.24@sha256:44e74ca483234093081138b6d7b6f561d55557756a2deefc3a5056148defeb99
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY index.html app.js styles.css /usr/share/nginx/html/
COPY data/ /usr/share/nginx/html/data/
COPY assets/ /usr/share/nginx/html/assets/
```

Configuração NGINX proposta (`nginx/default.conf`):

```nginx
server {
    listen 8080;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location = /healthz {
        access_log off;
        default_type text/plain;
        return 200 "ok\n";
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Compose proposto (limites iniciais conservadores, a calibrar com observação de uso real):

```yaml
services:
  web:
    build: .
    ports:
      - "127.0.0.1:4173:8080"
    restart: unless-stopped
    read_only: true
    tmpfs:
      - /tmp:size=16m,mode=1777
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    mem_limit: 128m
    cpus: 0.50
    pids_limit: 64
    healthcheck:
      test: ["CMD", "wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8080/healthz"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
```

`wget` deve ser confirmado dentro da variante de imagem na validação do build; se não existir, usar uma imagem/probe que já esteja disponível na própria imagem ou healthcheck externo sem adicionar pacotes à imagem. `read_only` e execução como usuário sem root dependem de todos os caminhos temporários do NGINX permanecerem sob `/tmp`; a configuração padrão da imagem já move PID e temporários para lá. Não adicionar volume: conteúdo é recriado da árvore versionada e não há estado mutável a persistir.

## Saúde, reinício e segurança operacional

O healthcheck verifica resposta HTTP local em `/healthz`; `unhealthy` é um estado de observabilidade e não reinicia sozinho o container. `restart: unless-stopped` reinicia o processo/container após saída, inclusive crash, mas não reage somente a falhas contínuas de healthcheck. Para falha de probe com processo vivo, consultar `docker compose ps`, `docker inspect` e logs; aplicar `docker compose restart web` após diagnóstico. Não alegar autorrecuperação de processo travado.

`read_only`, `tmpfs` limitado, `cap_drop: ALL` e `no-new-privileges` reduzem escrita e privilégios. A porta publicada em loopback reduz exposição na rede; verificar que Docker Desktop/host mantém o bind estritamente local. O container não contém banco, segredos ou estado de usuário. `unless-stopped` cobre restart automático após reboot conforme comportamento do daemon/serviço Docker Desktop; o daemon precisa estar ativo.

## Validação a executar na fase de implementação

1. `docker compose config --quiet` e `docker compose build --pull --no-cache` após revalidar digest.
2. `docker compose up -d`; conferir usuário não-root (`docker inspect`), `ReadonlyRootfs`, capacidades removidas, `SecurityOpt`, health status e limites aplicados.
3. HTTP 200 para `/`, `/healthz`, `data/knowledge.json`, `data/context.txt` e um ativo; comparar hashes/conteúdo desses arquivos com fontes locais.
4. HTTP 404 para caminho inexistente; testar carregamento real de busca/filtros e deep links/âncoras no browser local. Conferir portas bindadas apenas em 127.0.0.1.
5. Provar política de reinício em teste isolado: parar/start manual, reinício de processo e cenário de healthcheck falhando. Registrar explicitamente que healthcheck não reinicia container por si.
6. Rebuild depois de atualização de dependência/dados e confirmar rollback pelo commit anterior e `docker compose up -d --build`; sem apagar imagens/artefatos de evidência.

Esses testes não foram executados nesta pesquisa; nenhum container foi iniciado. Pages, DNS, TLS e interface pública continuam sendo gates próprios da publicação web, independentes do Docker local.

## Fontes oficiais consultadas

- [Docker Compose services reference](https://docs.docker.com/reference/compose-file/services/) — `read_only`, `tmpfs`, `cap_drop`, `security_opt`, `restart` e configuração de serviços; consultado em 2026-11-04.
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile) — `USER` e `HEALTHCHECK`; consultado em 2026-11-04.
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/) — serviço sem privilégios quando possível; consultado em 2026-11-04.
- [NGINX Unprivileged Docker Image README](https://github.com/nginx/docker-nginx-unprivileged/blob/main/README.md) — porta 8080, PID/temp paths sob `/tmp`, política de publicação e recomendação de digest; consultado em 2026-11-04.
- [Pacotes e tags publicados da imagem NGINX sem privilégios](https://github.com/nginx/docker-nginx-unprivileged/pkgs/container/nginx-unprivileged/versions?filters%5Bversion_type%5D=tagged) — variante Alpine stable, tag, digest e data de publicação exibidos; consultado em 2026-11-04.
- [Imagem oficial NGINX](https://hub.docker.com/_/nginx) — tags oficiais estáveis; consultado em 2026-11-04.

