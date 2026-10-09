# Tasks

## 1. A configuração de acesso ao núcleo alcança o navegador

- [x] 1.1 Mover para `src/api/nucleo.ts` a configuração idempotente do acesso ao
      núcleo (`configurarUmaVez`, hoje em `src/build/dados.ts`) e chamá-la em
      `lerDoNucleo`, antes de cada leitura, com `CHAVE_DE_APLICACAO` e
      `URL_DO_NUCLEO` de `src/api/configuracao.ts` (`RN-03-33`, design — decisão 1)
- [x] 1.2 Fazer `src/build/dados.ts` consumir a mesma função, sem flag própria, para
      o build e o navegador compartilharem um idioma só (`RF-03-45`, design —
      decisão 1)
- [x] 1.3 Em arquivo de teste novo que **nunca** chama `configurarAcessoAoNucleo`,
      dublar só o `fetch`, apresentar uma seção de leitura e afirmar que a chamada
      saiu levando `X-Chave-Aplicacao` da App 06 e nenhum cabeçalho de sessão —
      cenários "Uma seção de leitura alcança o núcleo na visita" e "A leitura que
      falha falha pelo núcleo, e não pela configuração" (`RF-03-02`, `RN-03-33`,
      design — decisão 5)
- [x] 1.4 No mesmo arquivo, cobrir o cenário "O conteúdo da publicação não supre a
      leitura da visita": com o `fetch` dublado respondendo, nenhuma seção de leitura
      fica no aviso de erro (`RF-03-02`, `RF-03-15`)

## 2. Cada endereço público é servido pelo documento da rota

- [x] 2.1 Declarar `"cleanUrls": true` no alvo `vitrine` do `firebase.json`,
      preservando `build.format: "file"` e a ordem vigente dos `rewrites`
      (`RF-03-25`, `RF-03-26`, PRD-03 §10, design — decisão 2)
- [x] 2.2 Em `src/descoberta/enderecos.ts`, estender a cobertura da casca de pessoa
      ao endereço `/app` que o `cleanUrls` cria, mantendo `/app.html`: o `robots.txt`
      barra os dois (`RF-03-13`, `RF-03-14`, invariante 12 do documento 99, design —
      decisão 3)
- [x] 2.3 No `firebase.json`, fazer a regra de `X-Robots-Tag` da casca casar os dois
      endereços, `/app` e `/app.html` (`RF-03-14`, design — decisão 3)
- [x] 2.4 Escrever o resolvedor de endereço servido — dado um caminho pedido, qual
      arquivo o serve —, aplicando a precedência documentada do Firebase (arquivo
      exato, `cleanUrls`, índice de diretório, `rewrites` na ordem) sobre o
      `firebase.json` real e a árvore real de `dist/`, em unidade e sem rede
      (design — decisão 4)
- [x] 2.5 Afirmar com o resolvedor que cada endereço público é servido pelo documento
      da própria rota, e nunca pela casca: os três recortes, a área detalhada, a
      porta do convite, os dois formulários, a Área do Apoiador Desenvolvedor e a
      página de comunidade — cenários "Um recorte de leitura abre no endereço
      próprio", "A página da comunidade abre no endereço que o sitemap declara" e "O
      endereço público não depende da extensão do arquivo" (`RF-03-15`, `RF-03-25`,
      `RF-03-26`, `RF-03-42`, `RF-03-52`, `RF-03-67`, `RF-03-77`)
- [x] 2.6 Afirmar que a casca de pessoa atende **só** o que não tem arquivo
      publicado, que os três prefixos de pessoa continuam chegando a ela e que
      nenhum endereço institucional ou de comunidade recebe a etiqueta de não
      indexar — cenário "A casca de pessoa atende só o que não tem arquivo
      publicado" (`RF-03-13`, `RF-03-14`, `RF-03-15`)
- [x] 2.7 Afirmar em `src/testes/hospedagem.test.ts` que o alvo `vitrine` declara
      `cleanUrls`, para que retirá-lo volte a falhar no CI em vez de em produção
      (`RF-03-25`, `RF-03-26`)
- [x] 2.8 Afirmar que todo endereço do `sitemap.xml` é servido pelo documento da rota
      dele — é a junta que o defeito atravessou: o sitemap convidava o buscador a dez
      endereços que respondiam com a casca `noindex` (PRD-03 §10, `RF-03-14`)

## 3. Verificação integrada e documentação

- [x] 3.1 Conferir que as nove seções de leitura da abertura, as três páginas de
      pessoa e a página de comunidade apresentam dado com os dois defeitos
      corrigidos juntos — nenhuma no aviso de erro e nenhum endereço na casca
      (`RF-03-02`, `RF-03-03`, `RF-03-04`, `RF-03-07`, `RF-03-08`, `RF-03-10`,
      `RF-03-15`, `RF-03-22`, `RF-03-47`)
- [x] 3.2 Registrar a correção em `openspec/cronograma-de-fatias.md`: linha **sem
      número** no bloco do PRD-03, nomeando a regressão da fatia 9 e o slug desta
      change, com a situação `implementado`. Nada em `docs/`, nos PRDs, no documento
      09 nem na `nav` do `mkdocs.yml`: a change não toma decisão nova, não muda
      requisito, não muda a situação do PRD-03 e não cria arquivo
