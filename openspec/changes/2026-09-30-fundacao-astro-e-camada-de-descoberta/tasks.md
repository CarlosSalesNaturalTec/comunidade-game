# Tasks

## 1. Fundação Astro

- [ ] 1.1 Acrescentar `astro`, `@astrojs/react` e `@astrojs/check` à App 06 e criar
      `astro.config.mjs` com `output: "static"` e a integração React; verificar que
      `npx astro build` produz `dist/` com HTML real (documento 03 §1, princípio 13)
- [ ] 1.2 Criar o layout base em `src/layouts/`, com `lang="pt-BR"`,
      `data-temperamento="arena"`, os `@import` de `comum/tokens.css` e
      `comum/fontes.css` e o encaixe de título, descrição e canônica; verificar que o
      documento gerado traz as fontes do próprio domínio e nenhuma requisição a
      terceiro (`RF-03-51`, documento 15 §1, princípio 6)
- [ ] 1.3 Extrair a carga de dados de build para `.ts` ao lado das páginas — conteúdo
      institucional e lista de comunidades, sobre `src/api/leituras.ts` — e derrubar o
      build quando o núcleo não responder; verificar com o núcleo inalcançável que
      `astro build` falha em vez de publicar casca vazia (design — decisão 4)

## 2. Rotas estáticas e ilhas

- [ ] 2.1 Criar as páginas institucionais — `/`, `/o-que-coletamos`,
      `/quero-participar` — com o conteúdo no documento e os componentes de hoje como
      ilhas `client:visible` nas seções de cards, ranking e necessidades; verificar que
      o documento servido traz o conteúdo sem executar script (`RF-03-01`, `RF-03-45`,
      `RF-03-52`, `RF-03-02`, `RF-03-47`)
- [ ] 2.2 Criar `/comunidades/[id]` com `getStaticPaths` sobre a lista do build: nome e
      território no documento, painel do território em ilha; verificar que a casca abre
      sem script e que o painel reflete a leitura da visita, não a da publicação
      (`RF-03-02`, `RF-03-15`, `RF-03-03`)
- [ ] 2.3 Criar as cascas de formulário e de Desenvolvedor — `/participar`,
      `/solicitar-dados`, `/desenvolvedor`, `/apresentar-url` — com o componente atual
      em ilha `client:load`; verificar que os testes de componente dos quatro seguem
      verdes (`RF-03-27` a `RF-03-35`, `RF-03-67`, `RF-03-77`)
- [ ] 2.4 Isolar em ilha própria a rolagem até a âncora de `SecoesInstitucionais.tsx`,
      hoje sobre `window.location.hash`, para a seção renderizar no documento
      (`RF-03-45`, `RF-03-48`)
- [ ] 2.5 Criar a casca `noindex` das páginas de pessoa, que lê o caminho no aparelho e
      monta Guerreiro(a), Mestre ou Apoiador; verificar que o documento servido não traz
      avatar, nick, badges, poderes nem desempenho (`RF-03-03`, `RF-03-07`, `RF-03-13`,
      `RF-03-14`, design — decisão 3)

## 3. Camada de descoberta

- [ ] 3.1 Dar título, descrição e canônica próprios a cada endereço indexável, sem
      revelar nick ou nome de Guerreiro(a) na prévia de compartilhamento; verificar que
      duas telas indexáveis não repetem o mesmo título (`RF-03-03`, `RF-03-06`,
      `RF-03-61`)
- [ ] 3.2 Publicar `robots.txt`, barrando a casca de pessoa, e o endpoint
      `sitemap.xml.ts` com os endereços institucionais e de comunidade do build;
      verificar em unidade que a montagem exclui pessoa e formulário (`RF-03-51`,
      `RN-03-21`, `RN-03-22`, design — decisão 5)
- [ ] 3.3 Declarar no `firebase.json` os `rewrite` de `/guerreiros/**`, `/mestres/**` e
      `/apoiadores/**` para a casca `noindex`, o `X-Robots-Tag` nos mesmos caminhos e o
      `**` como fallback atrás dos arquivos reais; verificar que a etiqueta e o
      cabeçalho saem juntos e que nenhum endereço institucional os recebe (`RF-03-13`,
      `RF-03-14`, invariante 12 do documento 99)

## 4. Limpeza da casca antiga e esteiras

- [ ] 4.1 Remover `index.html`, `App.tsx`, `main.tsx`, `src/navegacao/` e
      `vite.config.ts`, trocando a navegação entre rotas estáticas por `<a href>`;
      verificar que o `voltar` da recusa do convite segue devolvendo à navegação e que
      quem chega por endereço direto sai para a raiz (`RF-03-44`, `RN-03-15`)
- [ ] 4.2 Trocar o `build` da App 06 para `astro check && astro build` e ajustar
      `app-06-deploy.yml` e `frontend-ci.yml`; verificar que `npm run build
      --workspaces --if-present` alcança a App 06 e que erro de tipo a barra

## 5. Testes

- [ ] 5.1 Escrever o teste da saída do build, sobre `dist/`, cobrindo os cenários das
      specs: conteúdo no documento institucional e na área detalhada, casca da
      comunidade sem o painel, documento da pessoa sem perfil, `noindex` presente nas
      três páginas de pessoa e ausente no institucional, `sitemap.xml` com comunidade e
      sem pessoa nem formulário
- [ ] 5.2 Escrever os testes de unidade da montagem do `sitemap.xml` e dos metadados de
      cabeça, cobrindo exclusão de pessoa e de formulário e a ausência de dado de
      Guerreiro(a) na prévia
- [ ] 5.3 Rodar os 26 arquivos de teste de componente existentes e corrigir o que a
      troca de casca quebrou, sem alterar comportamento de tela

## 6. Documentação

- [ ] 6.1 Marcar a fatia 9 como `implementado` no `openspec/cronograma-de-fatias.md`,
      com o slug da change. Nenhuma decisão nova foi tomada nesta change, nenhum PRD
      muda, a situação do PRD-03 em `docs/prds/index.md` não muda, nenhuma relação entre
      documentos muda e nenhum arquivo nasce em `docs/` — nada mais a atualizar
