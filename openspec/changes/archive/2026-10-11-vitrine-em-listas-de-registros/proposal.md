# Proposal

Origem: **PRD-03 — Vitrine pública (App 06)**, linha `—` do bloco do PRD-03 em
`openspec/cronograma-de-fatias.md` ("A vitrine em listas de registros, e os Guerreiros fora da
listagem", situação `em andamento`). Não é fatia nova do PRD: é mudança de comportamento, no
padrão das quatro linhas `—` anteriores.

Recorte: **modifica** `RF-03-02`, `RF-03-03`, `RF-03-05`, `RF-03-12`, `RF-03-13` e `RN-03-26`;
**remove** `RF-03-04`; **atende** `RF-03-82`, `RF-03-83` e `RN-03-40`, novos. **Preserva**
`RF-03-06`, `RF-03-08`, `RF-03-09`, `RF-03-11`, `RF-03-14`, `RF-03-51`, `RF-03-55` a
`RF-03-57`, `RF-03-66`, `RF-03-79`, `RF-03-80`, `RN-03-02`, `RN-03-06`, `RN-03-07`, `RN-03-18`
e `RN-14-38`.

As sete decisões do fundador de 2026-10-11 que a originam já desceram aos documentos-fonte, ao
documento 09 §1 e ao PRD-03 no commit `c0e6e05`, antes desta change.

## Why

As seções de leitura da vitrine apresentavam **card por registro** — grade de cards em Mestres
e Apoiadores, carrossel de 5 segundos nos Guerreiros, texto corrido no Ranking e no Portfólio.
Com o acervo crescendo, o card deixou de servir para **encontrar** alguém: ele ocupa a tela de
um registro por vez e não dá ao visitante nem a dimensão da lista nem uma forma de percorrê-la.

## What Changes

- As seções de leitura passam a **lista de registros**: uma linha por registro, com o avatar
  quando o registro tem um, os dados principais da carta, e a linha abrindo a página individual.
- Cada lista exibe **10 registros por página**, com avançar e voltar e a posição em texto.
- **BREAKING** — a seção de **Guerreiros e Guerreiras perde a listagem** e fica só com a
  consulta por nick exato. Cai com ela a **rotação de 5 segundos** (`RF-03-04` removido). Quem
  tem divulgação autorizada segue público pelo **ranking** e pelo **portfólio**, como o
  `RF-03-12` sempre permitiu.
- **BREAKING** — `GET /v1/vitrine/guerreiros` **permanece pública** e deixa de ser consumida
  pela vitrine, pelo mesmo precedente de `/vitrine/poderes`.
- O **Ranking** ganha avatar e clique; o **Portfólio** passa a ordem decrescente e cada nick de
  autor abre a página dele; a **Comunidade Virtual** sai **sem avatar**.
- **Mestres e Apoiadores** passam à ordem **alfabética** pela identificação exibida, no núcleo
  — o que fecha divergência que já existia entre a spec e a implementação.
- A carta **não sai da plataforma**: deixa de ser a porta e passa a morar na página individual,
  com a composição do documento 11 §8.2 intacta.

## Capabilities

### New Capabilities

Nenhuma. A forma de apresentação é comportamento da App 06 e pertence a
`aplicacao-da-vitrine`; a ordem das listagens é contrato de leitura e pertence a
`leitura-publica-da-vitrine`. Criar capacidade para "lista paginada" seria nomear a tarefa, não
um comportamento durável do sistema.

### Modified Capabilities

- `aplicacao-da-vitrine`: a seção de Guerreiros e Guerreiras deixa de ter listagem e perde a
  rotação (requisito **removido**); a forma de cada seção de leitura passa a lista de registros
  paginada; a porta da página individual passa da carta para a linha; a vitrine deixa de
  consumir a listagem de Guerreiros.
- `leitura-publica-da-vitrine`: a listagem de Mestres e a de Apoiadores passam a responder em
  **ordem alfabética** pela identificação exibida, e o portfólio de criações originais, em
  **ordem decrescente** por data de validação.

## Impact

- **Núcleo** (`backend/src/nucleo/`): `_paginar_adultos_publicos` em `vitrine/publico.py` — o
  keyset passa a ser alfabético sobre a identificação exibida, com a junção do nick resolvida
  na consulta; `listar_criacoes_publicas` em `vitrine/rotas.py` — inverte a ordem e o keyset.
  `/vitrine/rankings` e `/v1/comunidades` **não mudam**: já ordenam por posição e por
  `(nome, id)`.
- **App 06** (`apps/app-06-vitrine/src/`): as seis seções de leitura, o componente de lista
  paginada, e `api/leituras.ts` — as leituras passam a aceitar cursor e `listarGuerreiros` sai.
  `SecaoDeAdultos.tsx` e o consumo de `SequenciaPaginada` em `SecaoDeGuerreiros.tsx` saem.
- **Camada comum** (`comum/react/`): **não se mexe**. `SequenciaPaginada` fica — tem quatro
  consumidores fora da vitrine e é o documento 15 §6.4; `CartaDoPersonagem` fica, porque a
  carta continua montando as quatro páginas individuais.
- **Contrato de API**: nenhuma rota nasce, sai ou muda de forma. O que muda é a **ordem** de
  três listagens, e o cliente passa a usar `tamanho` e `cursor`, que já existiam.
- **Documentação**: já entregue no commit `c0e6e05` (documentos 03 §8, 08, 09 §1, 11 §§8.1 e
  8.2, 15 §5 e PRD-03). Resta a situação da linha no cronograma, ao arquivar.

## Fora do escopo

O que o PRD-03 §3.2 já exclui. Em particular, e porque a exploração os levantou:

- **Página individual da criação original** — não existe no documento 11 §8.2, e criá-la seria
  requisito novo. É por isso que a linha do portfólio não é clicável: os **nicks** são.
- **Representação visual da comunidade na linha** e **foto da comunidade** — a foto não existe
  na plataforma, pendência aberta no documento 09.
- **Seção de batalhas** — o dado é do PRD-10 e `/vitrine/batalhas` não existe.
- **Total de registros e endereço direto para a página N** — exigiria trocar cursor por
  deslocamento em toda listagem do núcleo; consequência aceita pelo fundador.
