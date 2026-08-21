## Why

Origem: **PRD-01** (núcleo), com reflexo em **PRD-14** e **PRD-09**. Atende `RF-01-19`,
`RF-01-25`, `RN-01-22`, `RN-01-28`, `RN-01-30`, `RF-14-12`, `RF-14-13`, `RN-14-10` e
`RN-14-23`.

O nick do Apoiador passou a ser escolhido no **pré-cadastro**, que é porta pública sem login,
e `RF-14-13` recusa nick já usado. Como o nick é único em toda a plataforma, essa recusa
confirmaria a um visitante que o nick de uma criança existe — o oráculo que `RN-01-22`,
`RN-14-23` e o invariante 12 do documento 99 §6 vedam. A pendência "Conferência do nick no
pré-cadastro" (documento 09 §1) travava a fatia de cadastro de personas e foi decidida pelo
fundador, junto de outras quatro que a acompanham.

## What Changes

- **Nick vira atributo opcional da persona de adulto** — Apoiador e Mestre. Persona de adulto
  passa a ser criada sem nick e a recebê-lo depois; a exigência de nick continua valendo
  **só** para o Guerreiro(a), que nunca existe sem ele (`RF-01-19`).
- **A unicidade global do nick passa a alcançar o Mestre** — `RN-01-30` hoje cita apenas o
  Apoiador. O núcleo segue sendo a autoridade da unicidade no momento da gravação.
- **Mestre passa a ter nick e avatar** (`RF-14-12` por analogia; documento 02 §1 e 11 §8.2),
  sem o piso de 10 moedas do Apoiador, que é regra de marca do Apoiador (`RN-14-11`).
- **Conferência de disponibilidade de nick para adulto**, que varre **apenas nicks de adulto**
  e nunca alcança nick de Guerreiro(a). Vale em toda porta onde o próprio adulto escolhe: o
  pré-cadastro público (`RF-14-13`) e a troca pelo adulto autenticado. Sugestão de variações é
  permitida nessa conferência restrita; segue **vedada** qualquer listagem, busca parcial,
  completação ou sugestão que alcance nick de Guerreiro(a) (`RN-01-22`).
- **A solicitação de participação passa a carregar o nick** escolhido no pré-cadastro
  (`RF-01-25`), hoje ausente do modelo, e esse nick fica **reservado por 7 dias** a contar do
  envio, expirando sem desfecho.
- **Rota de identidade do adulto autenticado**, que define ou troca o **próprio nick**
  (PRD-01 §9), sujeita à conferência restrita e à unicidade global. O avatar do Mestre nasce
  aqui como **atributo**; a rota que o grava é do PRD-09, na mesma divisão que o spec já
  aplica ao avatar do Guerreiro(a).

Nenhuma remoção e nenhuma quebra: persona de adulto que já tenha nick permanece intacta.

## Capabilities

### New Capabilities

- `identidade-do-adulto`: conferência de disponibilidade de nick restrita a nicks de adulto,
  com sugestão de variações, e definição ou troca do próprio nick pelo adulto autenticado.

### Modified Capabilities

- `persona-e-credencial`: o nick deixa de ser atributo só de Guerreiro(a) e Apoiador e passa a
  alcançar o Mestre; a unicidade global passa a alcançar o nick do Mestre; persona de adulto
  passa a poder existir sem nick; o avatar passa a ser atributo também do Mestre; a vedação a
  descobrir ou sugerir nick passa a ser enunciada por **alcance** — nick de Guerreiro(a) —, e
  não por quem consulta.
- `fila-de-avaliacao`: a solicitação de participação passa a registrar o nick escolhido no
  pré-cadastro e a mantê-lo reservado por 7 dias.

## Impact

- **Núcleo (`backend/`)**: modelo de `Persona`, `Apoiador` e `SolicitacaoDeParticipacao`;
  migração de banco para o nick e o avatar do Mestre e para o nick e a reserva na solicitação;
  rota nova de disponibilidade de nick e rota nova de identidade do adulto, ambas sob `/v1`,
  com chave de aplicação e — na segunda — credencial de persona.
- **Proteção das rotas públicas**: a conferência no pré-cadastro é rota pública e herda o
  freio por origem já vigente para consulta de nick (`RF-01-65`).
- **Documentação, no mesmo PR**: documento 02 §1 (identidade do adulto e regra do nick),
  documento 11 §8.2 (card do Mestre), documento 09 (uma pendência movida para decidida e duas
  linhas já decididas revisadas), PRD-01, PRD-14, PRD-09 e `docs/prds/index.md`.
- **Fora do escopo**: telas da App 03, inclusive a edição do nick pelo Admin na colisão e o
  card que só publica com nick (change de cadastro de personas); desativação do ponto de apoio;
  o card do Mestre na vitrine (PRD-03).
