## 1. As duas famílias servidas pelo próprio domínio

- [ ] 1.1 Copiar para `comum/fontes/` os quatro `.woff2` variáveis — Atkinson Hyperlegible
      Next no eixo de peso e Archivo no eixo de largura, cada um nos subconjuntos `latin` e
      `latin-ext` —, com a licença OFL de cada família e um `README.md` registrando família,
      versão, origem e data da cópia. Requisito "As duas famílias tipográficas são servidas
      pelo próprio domínio" (PRD-02 §10, documento 15 §4; design — Decisions).
- [ ] 1.2 Escrever `comum/fontes.css` com os quatro `@font-face`, nomeando as famílias como o
      documento 15 §4 as nomeia, com o `unicode-range` de cada subconjunto, a faixa de peso, a
      de largura do Archivo e a apresentação imediata na família de reserva. Cobre os cenários
      "Nenhuma fonte vem de fora", "O nome declarado no token é o que a fonte atende" e "Texto
      legível enquanto a fonte não chegou".
- [ ] 1.3 Ampliar o mapa de `exports` e a lista de `files` de `comum/package.json` para
      `./fontes.css` e `./react`, mantendo `./tokens.css` como está. Requisito "O jogo consome
      a camada sem depender do framework das aplicações".

## 2. A camada de componentes em `comum/react`

- [ ] 2.1 Criar `comum/tsconfig.json` e a configuração de Vitest de `comum/`, e acrescentar
      `--largura-de-leitura` à camada semântica de `comum/tokens.css` com o valor que o
      documento 15 §4 já fixa (design — Decisions).
- [ ] 2.2 `Botao` e `Moldura`: alvo de toque de ao menos 48 px, ao menos 8 px de separação
      entre alvos vizinhos, contorno de foco visível e a largura de leitura aplicada pela
      moldura. Requisitos "Todo elemento acionável cumpre o alvo de toque e mostra o foco" e
      "O texto respeita a largura de leitura e o corpo mínimo".
- [ ] 2.3 `Campo`: gera o próprio identificador e amarra rótulo, mensagem de erro e estado
      inválido ao campo, de modo que quem o alcança depois receba a mensagem junto.
      Requisito "O erro de um campo é anunciado no próprio campo".
- [ ] 2.4 `Aviso`, `Cabecalho` e `EstadoDaLista`, e o `comum/react/indice.ts` exportando os
      seis componentes e seus tipos: o que interrompe se distingue do que informa o
      andamento, todo aviso leva rótulo textual que o identifica sem depender da cor, e o
      estado vazio é apresentado como informação. Requisitos "Nenhum estado se comunica
      apenas por cor" e "A camada não impõe movimento".

## 3. As três telas da App 03 revestidas

- [ ] 3.1 `apps/app-03-gestao/src/index.css`: importar `comum/fontes.css` e remover o
      `min-height` global, que hoje alcança inclusive o botão desenhado pelo Google
      Identity Services (design — Decisions).
- [ ] 3.2 `TelaDeEntrada` consumindo `Moldura`, `Cabecalho`, `Botao` e `Aviso`, sem tocar em
      `BotaoDeEntradaGoogle` nem no contexto de sessão. Requisito modificado "A aplicação
      cumpre o piso de acessibilidade das oito aplicações".
- [ ] 3.3 `TelaDeComunidades` e `ListaDeComunidades` como lista densa do temperamento
      Operação, com a ausência de indicadores do território apresentada como informação e
      nunca como erro. Requisito modificado "A aplicação apresenta as comunidades já
      criadas" (`RF-08-30`, `RF-08-31`, `RN-08-28`).
- [ ] 3.4 `FormularioDeComunidade` consumindo `Campo` e `Aviso`, preservando a validação e as
      recusas que já existem (`RN-02-04`, `RN-08-01`). Cobre o cenário "Erro de campo
      anunciado no próprio campo".

## 4. Testes

- [ ] 4.1 Testes de `comum/react`: a fiação de `Campo` — rótulo, mensagem e estado inválido
      ligados ao campo, e a soltura ao corrigir —, os dois papéis de `Aviso` e a exportação
      do índice. Cobre os cenários dos requisitos "O erro de um campo é anunciado no próprio
      campo" e "Nenhum estado se comunica apenas por cor".
- [ ] 4.2 Ampliar `apps/app-03-gestao/src/comunidades/comunidades.test.tsx` com o erro de
      campo alcançado depois de surgir e com a comunidade sem indicadores apresentada sem
      aviso de erro; conferir que os testes de entrada e de cliente de API seguem passando
      sem alteração.

## 5. Cache, conferência à mão e documentação

- [ ] 5.1 `firebase.json`: regra de cache longo para os arquivos com impressão digital no
      nome, que passam a incluir as fontes (design — Decisions).
- [ ] 5.2 Conferir à mão, uma vez, o que o jsdom não prova — contraste de 4,5:1 em texto e
      3:1 em componente, alvo de toque de 48 px medido e o desenho das duas famílias nas
      três telas, no claro e no escuro, na largura de um celular — e registrar o resultado
      no `README.md` da App 03.
- [ ] 5.3 Gravar as decisões novas: `docs/03-plataforma-e-arquitetura.md` §1.2 (o que
      `comum/` abriga), `docs/15-identidade-visual.md` §12 (a camada compartilhada passa a
      ter componentes além dos tokens) e `docs/09-topicos-em-aberto-e-sugestoes.md` (as
      quatro decisões). Nenhum arquivo novo em `docs/`, portanto nenhuma entrada na `nav`;
      `docs/prds/index.md` e o documento 99 não mudam, porque a situação do PRD-02 e a
      relação entre documentos seguem as mesmas.
