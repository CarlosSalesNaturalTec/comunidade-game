## 1. Núcleo — origem das chamadas

- [x] 1.1 Registrar em `backend/src/nucleo/principal.py` o middleware de origem: qualquer
      origem, sem credencial de cookie, permitindo os métodos das rotas e os cabeçalhos
      `X-Chave-Aplicacao` e `Authorization`. Nenhuma rota, corpo ou código de resposta muda.
- [x] 1.2 Cobrir em `backend/tests/` os cenários da capacidade `convencoes-da-api`: o
      `OPTIONS` de _preflight_ responde permitindo os dois cabeçalhos; a chamada de origem
      qualquer sem chave válida segue recusada como de qualquer outra origem.

## 2. Raiz do monorepo e o compartilhado

- [x] 2.1 Promover o `package.json` da raiz a manifesto do monorepo, declarando `workspaces`
      com `comum`, `apps/*` e `jogos/*`, e passar a excluir as pastas de código do
      `.prettierignore`. A esteira de texto continua como está.
- [x] 2.2 Criar `comum/` como pacote do espaço de trabalho, com o arquivo de tokens em CSS nas
      três camadas do documento 15 §12 — primitiva, semântica e tema —, no temperamento
      Operação do §6 (densidade alta, raio 4 px, 200 ms, sem movimento decorativo) e com os
      tokens de foco visível e de contraste do §5. A aplicação consome só a semântica e a de
      tema.
- [x] 2.3 Configurar o Biome para enxergar `comum/` e `apps/*`, sem colidir com o domínio do
      Prettier.

## 3. Esqueleto da App 03

- [x] 3.1 Criar `apps/app-03-gestao/` com React, TypeScript, Vite e Vitest, consumindo os
      tokens de `comum` e com a base responsiva Mobile First: alvo de toque de 48 px, foco
      sempre visível e `prefers-reduced-motion` respeitado (documento 15 §5, PRD-02 §10).
- [x] 3.2 Escrever o cliente de API: a chave em `X-Chave-Aplicacao` e a sessão em
      `Authorization: Bearer` em toda chamada, o corpo de erro único do PRD-01 e a **separação
      entre a recusa da chave e a recusa da sessão** (`RF-01-02`, `RN-01-32`, `RN-01-34`).
      Chave e _client ID_ entram por variável de ambiente do Vite, uma por ambiente.
- [x] 3.3 Implementar a entrada: o `id_token` pelo Google Identity Services,
      `POST /v1/sessoes/social`, o papel lido de `GET /v1/eu`, o token guardado em
      `sessionStorage` e a saída por `DELETE /v1/sessoes/atual`. A conta sem cadastro lê a
      orientação de solicitar participação pela vitrine (`RF-01-09`, `RF-01-10`).
- [x] 3.4 Proteger as telas de dados: sem sessão aberta, só a entrada aparece; sessão expirada
      ou encerrada devolve à entrada; o papel que governa o que se alcança é o que o núcleo
      devolveu, nunca uma escolha na tela (`RF-01-02`, `RF-01-09`).

## 4. Cadastro de Comunidade Virtual

- [x] 4.1 Apresentar as comunidades existentes a partir de `GET /v1/comunidades`, com a
      comunidade abaixo do piso de coletores aparecendo **sem os indicadores do território** e
      sem mensagem de erro (`RF-08-30`, `RF-08-31`, `RN-08-28`).
- [x] 4.2 Implementar o formulário de nome, localização e granularidade máxima e a criação por
      `POST /v1/comunidades`; a comunidade criada aparece entre as existentes (`RF-02-11`,
      `RN-02-04`).
- [x] 4.3 Tratar as recusas na tela: campo obrigatório em falta apontado no campo, sem criar
      nada; recusa por papel explicada em linguagem simples, sem código de erro cru; e o
      caminho de criação não oferecido a quem não é Admin (`RN-02-04`, `RN-08-01`, PRD-02 §4).

## 5. Esteira de CI da pasta

- [x] 5.1 Criar o workflow das pastas de JavaScript em `.github/workflows/`, disparado só
      pelos caminhos que cobre, com `biome format --check`, `biome check` e `vitest run`
      bloqueando o merge, e a cobertura medida sem limiar.

## 6. Testes

- [x] 6.1 Testar o cliente de API: os dois cabeçalhos presentes em toda chamada, o corpo de
      erro único interpretado e a recusa da chave distinguida da recusa da sessão.
- [x] 6.2 Testar a entrada e a sessão, pelos cenários das specs: Admin com cadastro entra e
      recebe o papel do núcleo; conta social sem cadastro lê a orientação e nenhuma sessão
      abre; sessão expirada devolve à entrada; a saída encerra no núcleo; sem sessão, nenhum
      dado de gestão aparece.
- [x] 6.3 Testar o cadastro de comunidade e o piso de acessibilidade: criação com os três
      campos, campo em falta apontado sem criar nada, recusa por papel explicada, comunidade
      recém-criada listada sem indicadores; e, na travessia pelo teclado, foco visível em todo
      elemento acionável.

## 7. Documentação

- [x] 7.1 Atualizar a situação do PRD-02 em `docs/prds/index.md` e corrigir em
      `openspec/config.yaml` o contexto que contradiz o documento 03: as ferramentas de
      frontend deixaram de ser pendência e a árvore do repositório ganhou `comum/`. As
      decisões de framework, hospedagem e origem já estão gravadas nos documentos 03, 09 e 99,
      e nenhum arquivo novo entra em `docs/` — a `nav` do `mkdocs.yml` não muda.
