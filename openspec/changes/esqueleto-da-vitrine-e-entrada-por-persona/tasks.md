## 1. A pasta da App 06 e a esteira dela

- [ ] 1.1 Criar `apps/app-06-vitrine/` no molde de `apps/app-08-apoiador/` — `package.json`,
      `vite.config.ts`, `tsconfig*`, `index.html` com `lang="pt-BR"` e
      `data-temperamento="arena"`, `public/favicon.svg`, `README.md` e `.env.example` — **sem**
      dependência de `comum/autenticacao` e sem `VITE_GOOGLE_CLIENT_ID`, e registrar a pasta no
      _workspace_ do `package.json` da raiz (`RF-03-01`, `RN-03-01`, documento 15 §6, design —
      decisão 1)
- [ ] 1.2 Criar `src/api/configuracao.ts` com `CHAVE_DE_APLICACAO`, `URL_DO_NUCLEO` e os seis
      endereços de destino do "Entrar", todos por variável de ambiente e sem valor gravado no
      código, e o cliente de API da vitrine sobre `comum/api`, que leva a chave da aplicação e
      **nenhuma** credencial de persona (`RN-03-33`, design — decisões 1 e 4)
- [ ] 1.3 Criar `.github/workflows/app-06-deploy.yml` no molde de `app-08-deploy.yml`, com
      `--only hosting:vitrine` e `secrets.APP06_CHAVE_DE_APLICACAO`; acrescentar o alvo
      `vitrine` em `.firebaserc` apontando para `comunidade-game-vitrine`; e acrescentar ao alvo
      `vitrine` de `firebase.json` a reescrita `** → /index.html`, que faz o endereço direto
      resolver (`RF-03-01`, design — decisões 2 e 6)

## 2. A navegação, os recortes e o esqueleto das seções

- [ ] 2.1 Implementar `src/navegacao/` sobre a History API — caminho lido de
      `window.location.pathname`, troca por `history.pushState`, volta por `popstate` —, sem
      dependência nova e sem nada guardado no aparelho (`RF-03-01`, `RF-03-26`, `RF-03-51`,
      design — decisão 2)
- [ ] 2.2 Implementar os três recortes de leitura como caminho: raiz em **sociedade civil**, e
      `/pesquisadores` e `/gestores-publicos` alcançáveis pela navegação, sem área restrita, sem
      cadastro, sem coleta e sem guardar o recorte escolhido (`RF-03-25`, `RF-03-26`, `RN-03-01`,
      `RN-03-22`)
- [ ] 2.3 Montar `src/App.tsx` e o `Cabecalho` da vitrine com o temperamento Arena e as seções
      nomeadas que as fatias 2 a 8 preenchem, **sem** espaço reservado a publicidade ou
      patrocínio em lugar nenhum do _layout_ (`RF-03-50`, `RN-03-21`, design — decisão 5)

## 3. O botão "Entrar" e o encaminhamento por persona

- [ ] 3.1 Implementar `src/entrada/BotaoDeEntrada.tsx` sempre visível no cabeçalho, abrindo o
      `Dialogo` de `comum/react` com a pergunta de quem está entrando e as seis personas do
      PRD-03 §5.9 — Guerreiro(a), responsável, Mestre, Apoiador, gestão e aparelho da aula —, sem
      escolha pré-marcada e sem encaminhar antes da resposta (`RF-03-58`, `RF-03-60`)
- [ ] 3.2 Encaminhar cada persona ao endereço da aplicação dela pelas variáveis da decisão 4, sem
      campo de nick, imagem, senha ou login em tela alguma da vitrine, e sem lista, sugestão,
      completação ou confirmação de que uma conta existe (`RF-03-59`, `RF-03-61`, `RN-03-27`)
- [ ] 3.3 Implementar a orientação de quem ainda não tem cadastro, por persona: pré-cadastro da
      App 08 para quem quer ser Apoiador, **procurar a gestão no encontro** para responsável e
      Guerreiro(a), e o formulário de participação **nomeado em texto, sem link**, para quem quer
      ser Mestre, enquanto a fatia 4 não o criar — em nenhum caso prometendo acesso (`RF-03-62`,
      design — riscos)

## 4. Testes da App 06

- [ ] 4.1 Em `apps/app-06-vitrine/src/testes/`, cobrir a abertura e os recortes com os critérios
      de aceite do PRD-03 §12: a vitrine abre inteira sem pedir login nem cadastro e nenhuma tela
      oferece área restrita; a raiz é o recorte sociedade civil; os outros dois recortes estão na
      navegação e trocar de recorte não bloqueia nada nem pede cadastro; e nenhuma tela exibe
      publicidade ou patrocínio (`RF-03-01`, `RF-03-25`, `RF-03-26`, `RF-03-50`, `RN-03-01`,
      `RN-03-21`)
- [ ] 4.2 Cobrir o "Entrar": o botão aparece em toda tela; o diálogo pergunta a persona antes de
      encaminhar; cada uma das seis personas vai ao endereço da sua aplicação; nenhuma tela pede
      credencial nem revela nick, conta ou cadastro; a escolha não sobrevive à visita e a
      pergunta volta sem opção pré-marcada; e a orientação de quem não tem cadastro é a da
      própria persona, com o formulário do Mestre em texto sem link (`RF-03-58` a `RF-03-62`,
      `RN-03-27`)
- [ ] 4.3 Cobrir a ausência de rastro: percorrida uma visita inteira — navegação, troca de
      recorte e o diálogo do "Entrar" —, nada fica em `localStorage`, `sessionStorage` nem em
      cookie, e a chamada ao núcleo leva a chave da aplicação e nenhuma credencial de persona
      (`RF-03-51`, `RF-03-60`, `RN-03-22`, `RN-03-33`)

## 5. Documentação

- [ ] 5.1 Marcar a fatia 1 do PRD-03 como `implementado` em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug da change e
      anotando na linha que `RF-03-62` saiu sem o link do formulário de participação, que a fatia
      4 acrescenta; e passar o PRD-03 a em implementação na tabela de `docs/prds/index.md`.
      Nenhuma decisão nova, nenhum arquivo novo em `docs/` e nada a mudar no documento 99 nem na
      `nav` do `mkdocs.yml`
