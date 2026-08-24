# Desenho — esqueleto da aula presencial e equipe da aula

## Context

Ver `proposal.md` — Why. O que o desenho precisa saber:

- A capacidade `equipe` já está consolidada em `openspec/specs/equipe/spec.md`, com sete
  requisitos, e `backend/src/nucleo/equipes/regra.py` os implementa e testa
  (`backend/tests/test_equipe.py`). Esta fatia **só abre a porta** — é o padrão que
  `etiqueta-ods-da-trilha-e-da-missao` e `banco-do-quiz-ao-vivo` já aplicaram duas vezes.
- A matriz de permissões já tem `equipe_que_forma_na_aula` e `equipes_da_aula_em_andamento`.
  Nenhuma entrada nova.
- `GET /v1/aulas/vigentes`, `POST /v1/sessoes/social`, `POST /v1/sessoes/guerreiro/confirmacao`
  e `GET /v1/eu` já estão no ar. A chave `app-01-aula-presencial` já é semeada nos dois
  ambientes por `chaves/semeadura.py`.
- `comum/` já traz o cliente do núcleo, a sessão do adulto, os tokens de design e os
  componentes de React que as Apps 03 e 09 usam.

O único problema novo desta fatia é de frontend: **um aparelho, duas sessões ao mesmo tempo**.

## Goals / Non-Goals

**Goals:**

- Abrir a porta HTTP de `equipes` sem reescrever recusa alguma da regra.
- Sustentar, no aparelho compartilhado, a sessão de trabalho do adulto e a sessão do
  Guerreiro(a) convivendo, sem que uma derrube a outra.
- Amarrar a sessão de trabalho à janela da aula sem inventar tolerância nem intervalo.

**Non-Goals:**

- Mexer em `equipes/regra.py`, `equipes/modelo.py` ou `test_equipe.py`.
- Mudar o comportamento de sessão das Apps 03 e 09.
- Qualquer superfície de câmera, mídia ou armazenamento local de dado de criança.

## Decisions

### 1. Duas sessões no mesmo aparelho, por chave de armazenamento parametrizada

`comum/autenticacao/armazenamentoDeSessao.ts` guarda o token numa **constante fixa** de
`sessionStorage`, e `ProvedorDeSessao` a consome direto. A App 01 precisa de duas sessões vivas
ao mesmo tempo: a de trabalho, do Mestre ou Admin, que dura a aula, e a do Guerreiro(a), que
dura um atendimento.

`ProvedorDeSessao` passa a aceitar a **chave de armazenamento** como propriedade, com o valor de
hoje como padrão. A App 01 o instancia duas vezes, aninhado, com chaves distintas; as Apps 03 e
09 seguem sem passar nada e sem mudança de comportamento.

- _Descartado_: um provedor novo só para a App 01 — duplicaria a restauração por `GET /v1/eu` e
  o tratamento de `sessao_invalida`, que é justamente o que `comum/` existe para não duplicar.
- _Descartado_: guardar a sessão do Guerreiro(a) em memória, sem `sessionStorage` — recarregar
  a aba no meio do encontro derrubaria o atendimento.

`sessionStorage`, e não `localStorage`, nas duas: o aparelho é compartilhado, e a sessão precisa
morrer com a aba (decisão já vigente, `armazenamentoDeSessao.ts`).

### 2. A sessão do Guerreiro(a) é limpa ao voltar à tela inicial

Voltar ao início encerra a sessão do Guerreiro(a) e apaga o token dele, para que o próximo
atendimento comece limpo (`RF-04-28`, PRD-04 §12: "nenhuma tela mostra dado do atendimento
anterior"). A sessão de trabalho não é tocada nisso — ela é do aparelho, não do atendimento.

### 3. A janela da aula é o próprio `GET /v1/aulas/vigentes`, não um relógio local

`aulas_vigentes` já é exatamente `inicio_em ≤ agora ≤ fim_em`. A App 01 relê a rota **ao abrir a
sessão de trabalho e a cada volta à tela inicial**, e encerra a sessão de trabalho quando a aula
escolhida deixa de aparecer entre as vigentes. Assim o núcleo continua sendo quem define
"vigente", e a fatia não inventa tolerância depois do `fim_em` nem intervalo de sondagem.

- _Descartado_: temporizador no aparelho contra o `fim_em` recebido — relógio de tablet
  emprestado erra, e a decisão passaria do núcleo para o aparelho.

### 4. A comunidade escolhida vive na sessão de trabalho

Havendo mais de uma aula vigente, a escolha (`RF-04-03`) é guardada junto do token de trabalho,
na mesma chave de `sessionStorage`, e some com ele. Recarregar a aba não repete a pergunta;
encerrar a sessão de trabalho, sim — que é o comportamento certo, porque a aula mudou.

### 5. As rotas de equipe seguem o formato já consolidado

`equipes/rotas.py` espelha `culminancias/rotas.py` e `ods/rotas.py`: roteador próprio,
registrado em `principal.py`, `exigir_permissao` para a operação da matriz, tradução dos erros de
`erros.py` pelo tratador único do PRD-01, e paginação por `contrato_de_listagem()` na leitura.

`DELETE /v1/equipes/{id}/integrantes/eu` usa `eu` no caminho, como o PRD-04 §9 declara: quem sai
é sempre a persona em sessão, e `sair_da_equipe` recebe o `persona_id` dela — nunca um
identificador vindo do cliente, que abriria caminho para tirar integrante alheio.

### 6. A saída da leitura é montada na rota, não no modelo

`GET /v1/aulas/{id}/equipes` monta avatar e nick a partir da `Persona` de cada integrante. Não
há projeção nova no modelo nem coluna nova: a restrição a avatar e nick (`RN-04-14`, invariante
11) é do contrato de saída, e fica visível no esquema Pydantic da rota — onde uma revisão futura
a encontra.

### 7. A App 01 nasce com o desenho das duas irmãs

Vite, React, TypeScript, Biome e Vitest, workspace `apps/*`, consumindo `comum/`. O
`app-01-deploy.yml` é espelho do `app-09-deploy.yml`, com `VITE_CHAVE_DE_APLICACAO` própria e o
mesmo contorno temporário de `VITE_URL_DO_NUCLEO` — que é pendência aberta do documento 09, não
decisão desta fatia.

Mobile First é requisito do PRD-04 §10 e já é o desenho de `comum/tokens.css`; a App 01 é a
primeira em que ele vale para criança em aparelho pequeno, com alto contraste e poucos elementos
por tela.

## Risks / Trade-offs

- **Duas sessões no mesmo aparelho podem se confundir na tela** → cada área lê explicitamente o
  provedor que lhe cabe; a área de equipes nunca alcança o provedor de trabalho, e a abertura da
  sessão de trabalho nunca alcança o do Guerreiro(a). Teste cobre as duas convivendo.
- **Parametrizar a chave de armazenamento toca `comum/`, que serve às três aplicações** → o
  valor padrão é o de hoje, e as Apps 03 e 09 não passam a propriedade; os testes de
  `comum/autenticacao` cobrem o padrão e a chave explícita.
- **A releitura de `aulas/vigentes` a cada volta à tela inicial custa uma chamada por
  atendimento** → é uma leitura pequena, e a alternativa é o relógio local do aparelho decidir a
  janela.
- **Toda entrada de Guerreiro(a) nesta fatia depende de um adulto presente** → é o caminho que o
  `RF-04-15` já prevê, e o PRD-04 §12 mede justamente a taxa de identificação automática contra
  confirmação humana. A fatia do onboarding é que a torna medível.
- **A App 01 estreia sem o caminho do onboarding** → a tela inicial apresenta os dois caminhos, e
  o do onboarding entra desabilitado com o motivo em uma linha, em vez de sumir — o
  `RF-04-01` pede os dois na tela.

## Migration Plan

Sem migração de dados: nenhuma coluna nova, nenhuma tabela nova, nenhum _backfill_.

Ordem de publicação: o núcleo primeiro (as rotas novas não quebram cliente algum — ninguém as
chama hoje), a App 01 depois. O alvo `aula` do Firebase Hosting precisa existir no projeto antes
do primeiro `app-01-deploy.yml` — ato de console, do fundador, como foi para o alvo `mestre`.

Reversão: remover o registro do roteador em `principal.py` devolve o núcleo ao estado anterior,
e a App 01 é pasta nova, sem consumidor.
