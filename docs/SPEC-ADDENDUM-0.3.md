# Aditamento 0.3 — runtime Docker e retomada

Estado: AUTORIZADO pelo Pai nesta conversa em 04/11/2026: “Aprovado, em todos os escopos”, aprovação da explicação Docker/Pages e “pode prosseguir”. Herda SPEC0.1 e aditamento0.2. Sem novas aprovações rotineiras no escopo.

R13 Runtime adicional: Docker/Compose mínimo para servir os mesmos arquivos estáticos do Pages; imagem mantida com versão/digest verificados em fonte oficial, sem root, sem privilégios adicionais, filesystem somente leitura e escritas temporárias em tmpfs. Sem banco, conta, backend ou volume de conhecimento mutável. Reinício unless-stopped, verificação HTTP de saúde e documentação de operação/atualização/rollback. Host e Docker precisam estar ligados; unhealthy não implica reinício automático por si só. Pages permanece independente desse host.

Plano anterior à implementação: pesquisar imagens oficiais mantidas, verificar runtime existente sem instalar/iniciar software alheio; construir configuração mínima com porta local; testar configuração/build/HTTP/saúde/reinício/recriação/persistência dos arquivos versionados se daemon disponível. Runtime ausente é NÃO VALIDADO, nunca simular teste. Não instalar Docker nem alterar inicialização do host por inferência.

Retomada: revisar correções recuperadas dos lotes2/3/4; corrigir51excertos do lote1; gerar candidato em diretório novo; conferir relações editoriais e controles negativos; publicar somente a edição admitida. Documentação atual deixa de tratar SPEC/plano como pendentes. Registros antigos continuam no Git/recibos históricos.

Aceite: Docker adicional não limita recursos da edição estática no Pages. Testes locais, Docker, revisão consultiva, Pages/HTTPS/bytes e aprovação humana são evidências separadas.
