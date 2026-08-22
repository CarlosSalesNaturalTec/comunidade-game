# Tasks — esqueleto da Área do Mestre e autoria da trilha

Ritmo de verificação no `CLAUDE.md`: a cada tarefa de código roda só o teste do recorte; a
suíte do backend e o Biome rodam **uma vez**, ao fechar o grupo. Esta change não toca `docs/`,
`mkdocs.yml` nem `.md` da raiz — `npm run lint` e `mkdocs build` **não** rodam.

## 1. Modelo e migração (PRD-09 §8)

- [ ] 1.1 Acrescentar a `Missao` as colunas `titulo`, `etapa_do_ciclo` e `cadencia_de_retomada`
      em `trilhas/modelo.py` — `titulo` obrigatório, `etapa_do_ciclo` enum fechado nos quatro
      valores do documento 11 §2.4, `cadencia_de_retomada` anulável e lista de dias (decisões 3
      e 5). Verificar: `uv run pytest tests/test_missao.py -x` verde
- [ ] 1.2 Acrescentar a `Atividade` as colunas `titulo` (obrigatório) e `descricao` (anulável)
      em `trilhas/modelo.py` (`RF-09-69`, decisão 5). Verificar:
      `uv run pytest tests/test_atividade.py -x` verde
- [ ] 1.3 Estender `criar_missao` e `criar_atividade` em `trilhas/regra.py` para receber e
      recusar os campos novos — missão sem título e atividade sem título respondem 422, etapa
      fora dos quatro valores responde 422, missão sem retomada é aceita. Verificar:
      `uv run pytest tests/test_missao.py tests/test_atividade.py -x` verde
- [ ] 1.4 Escrever a função `declarar_cadencia_de_retomada` em `trilhas/regra.py`, com a posse
      conferida por `conferir_posse_da_trilha` e a cadência nova substituindo a anterior
      (`RF-09-83`). Verificar: teste novo em `tests/test_missao.py` cobrindo declarar,
      substituir e recusar Mestre não autor
- [ ] 1.5 Gerar a migração Alembic das cinco colunas em duas etapas — coluna anulável,
      preenchimento com o identificador, `NOT NULL` (decisão 8). Verificar: `alembic upgrade
      head` e `alembic downgrade -1` correm em base com dado de desenvolvimento
- [ ] 1.6 Conferir que os 31 arquivos de teste que chamam `criar_trilha`, `criar_missao` e
      `criar_atividade` seguem passando com os campos novos. Verificar: `uv run pytest -x`
      verde uma vez, ao fechar o grupo

## 2. Porta HTTP da autoria (PRD-09 §9)

- [ ] 2.1 Criar `backend/src/nucleo/trilhas/rotas.py` com `POST /trilhas`, traduzindo o corpo
      para `criar_trilha` sem reescrever regra (`RF-09-01`, decisão 1). Verificar: teste novo
      `tests/test_trilha_rota.py` cobrindo criação, poder fora da natureza de Guerreiro(a)
      (422) e chamada sem persona em sessão
- [ ] 2.2 Acrescentar `GET /trilhas/minhas`, devolvendo as trilhas do Mestre autor com missões
      aninhadas na ordem da posição e atividades dentro de cada missão (`RF-09-04`, decisão 2).
      Verificar: `tests/test_trilha_rota.py` cobrindo rascunho próprio devolvido, rascunho
      alheio ausente e consulta sem filtro de comunidade aceita
- [ ] 2.3 Acrescentar `POST /trilhas/{id}/missoes` (`RF-09-02`, `RF-09-03`, `RF-09-80`,
      `RF-09-81`). Verificar: `tests/test_trilha_rota.py` cobrindo criação, missão sem
      obrigatoriedade (422), sondagem fora da primeira posição (422), segunda sondagem (422) e
      Mestre não autor (403)
- [ ] 2.4 Acrescentar `POST /missoes/{id}/atividades` (`RF-09-69`, `RF-09-70`). Verificar:
      `tests/test_trilha_rota.py` cobrindo criação, atividade sem formato (422), natureza nova
      aceita e Mestre não autor da trilha (403)
- [ ] 2.5 Acrescentar `POST /missoes/{id}/retomada` (`RF-09-83`, `RF-09-101`, decisão 4).
      Verificar: `tests/test_trilha_rota.py` cobrindo declarar, substituir e Mestre não autor
- [ ] 2.6 Registrar o roteador em `principal.py` e conferir que as três rotas órfãs passam a
      ser alcançáveis. Verificar: teste de integração criando trilha → missão → atividade por
      HTTP e, com os identificadores devolvidos, chamando `POST /desafios-de-coleta` e
      `POST /trilhas/{id}/recompensas-de-marco` com sucesso
- [ ] 2.7 Fechar o backend: `ruff format .`, `ruff check --fix .` e `uv run pytest` — uma vez

## 3. Camada de acesso em `comum/` (decisão 6)

- [ ] 3.1 Criar `comum/api/` com `cliente.ts` e `tipos.ts` movidos da App 03, mantendo a
      assinatura exata de `chamarNucleo(caminho, opcoes)`, e acrescentar
      `configurarAcessoAoNucleo({ chaveDeAplicacao, urlDoNucleo })` com falha explícita na
      chamada não configurada. Verificar: `cliente.test.ts` movido junto e verde, mais teste
      novo da chamada antes da configuração
- [ ] 3.2 Criar `comum/autenticacao/` com `ContextoDeSessao`, `armazenamentoDeSessao` e
      `BotaoDeEntradaGoogle` movidos da App 03, recebendo o client ID por parâmetro em vez de
      ler variável de ambiente. Verificar: `entrada.test.tsx` e
      `BotaoDeEntradaGoogle.test.tsx` movidos e verdes
- [ ] 3.3 Apontar as 61 chamadas dos 11 `api.ts` da App 03 para `comum/api`, e chamar
      `configurarAcessoAoNucleo` uma vez no `main.tsx` a partir do `api/configuracao.ts` que
      fica na aplicação. Verificar: `npm test -w app-03-gestao` verde, sem mudança de
      comportamento
- [ ] 3.4 Conferir que a App 03 continua construindo. Verificar: `npm run build -w
      app-03-gestao` sem erro de tipo

## 4. App 09 — esqueleto e entrada (PRD-09 §4)

- [ ] 4.1 Criar `apps/app-09-mestre/` espelhando a pilha da App 03 — Vite, React 19,
      TypeScript, Vitest, Biome, `comum: "*"` — com `package.json`, `vite.config.ts`,
      `tsconfig.json` e `index.html`. Verificar: `npm run build -w app-09-mestre` sem erro
- [ ] 4.2 Montar a entrada por login social consumindo `comum/autenticacao`, com a chave e a
      URL do núcleo em `api/configuracao.ts` próprio da App 09. Verificar: teste cobrindo que
      sem sessão só a entrada aparece e que a chamada leva a chave da App 09
- [ ] 4.3 Recusar Guerreiro(a) na entrada, em linguagem simples, e apresentar a orientação de
      solicitar participação pela vitrine a conta social sem cadastro. Verificar: teste
      cobrindo as duas recusas, sem código de erro cru na tela
- [ ] 4.4 Devolver o Mestre à entrada quando o núcleo recusa a sessão, distinguindo essa recusa
      da recusa de chave. Verificar: teste cobrindo sessão expirada e recusa de chave com
      desfechos diferentes

## 5. App 09 — autoria da trilha (PRD-09 §6.1)

- [ ] 5.1 Tela de criação de trilha, com seletor que oferece só poder ativo e de natureza de
      Guerreiro(a) (`RF-09-01`). Verificar: teste cobrindo criação, campo obrigatório em falta
      apontado no próprio campo e Poder Sustentador ausente do seletor
- [ ] 5.2 Lista das trilhas do Mestre, com nome, poder, área e situação, alimentada por
      `GET /trilhas/minhas` (`RF-09-04`). Verificar: teste cobrindo rascunho próprio presente e
      rascunho alheio ausente
- [ ] 5.3 Tela de missões da trilha — acrescentar com título, posição, dificuldade,
      obrigatoriedade e etapa do ciclo, apresentadas na ordem da posição (`RF-09-02`,
      `RF-09-03`, `RF-09-80`). Verificar: teste cobrindo criação, obrigatoriedade em falta e
      ordenação por posição
- [ ] 5.4 Marcação da missão de sondagem, com a recusa da segunda sondagem e da sondagem fora
      da primeira posição em linguagem simples; rascunho sem sondagem é aceito (`RF-09-81`).
      Verificar: teste cobrindo os três casos
- [ ] 5.5 Tela de atividades da missão, com título, descrição, modalidade, formato, natureza e
      produção esperada (`RF-09-69`, `RF-09-70`). Verificar: teste cobrindo criação, atividade
      sem modalidade apontada no campo e natureza nova aceita
- [ ] 5.6 Declaração da cadência de retomada da missão, com o caminho de deixá-la sem retomada
      (`RF-09-83`). Verificar: teste cobrindo declarar e deixar sem retomada
- [ ] 5.7 Conferir que nenhum campo da autoria pede código, marcação ou configuração técnica, e
      que toda recusa do núcleo chega traduzida (`RF-09-12`). Verificar: teste cobrindo que a
      recusa apresentada não traz o código do erro

## 6. Publicação da App 09

- [ ] 6.1 Acrescentar o alvo `mestre` ao `.firebaserc` — o `firebase.json` já o declara.
      Verificar: `firebase target:list` reconhece o alvo
- [ ] 6.2 Criar `.github/workflows/app-09-deploy.yml`, espelho do `app-03-deploy.yml`, filtrado
      por `apps/app-09-mestre/**`, `comum/**` e os arquivos do Firebase. Verificar: o workflow
      valida no CI e não dispara em mudança fora desses caminhos
- [ ] 6.3 Fechar o frontend: `npx biome format --write .`, `npx biome check .` e
      `npm test` nas duas aplicações — uma vez

## 7. Documentação da change (`CLAUDE.md` §3)

- [ ] 7.1 Atualizar `docs/prds/index.md` com a primeira fatia do PRD-09 — o que entrou, as três
      rotas órfãs destravadas e o que segue pendente. Verificar: a situação do PRD-09 continua
      **aprovado**, porque a fatia não o esgota
- [ ] 7.2 Registrar no documento 09 a decisão nova do fundador — o formato da cadência de
      retomada — e as três pendências levantadas na proposal. Verificar: as linhas entram na
      tabela de decisões pendentes ou de já decididos, conforme o caso
- [ ] 7.3 Atualizar o documento 99 §8 com a App 09 e a relação nova entre PRD-09 e PRD-02.
      Verificar: os invariantes do §6 seguem válidos
- [ ] 7.4 Rodar a esteira de documentação, que só agora é exigida porque o grupo 7 tocou
      `docs/`. Verificar: `npm run fix`, `npm run lint` e `mkdocs build --strict` sem erro
