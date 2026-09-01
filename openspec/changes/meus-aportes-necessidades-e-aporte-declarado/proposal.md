## Why

A fatia 4 do PRD-14 (`openspec/cronograma-de-fatias.md`) entrega o **motivo pelo qual o
Apoiador entra na aplicação**: ver o que já aportou em moedas, ver o que falta às atividades e
declarar um aporte novo. As fatias 1 a 3 deram o esqueleto, a porta pública e a identidade; o
Apoiador cadastrado ainda não tem por onde aportar de novo, e a fatia 5 (missões, sustento e
selos) depende desta.

Recorte da fatia: `RF-14-21` a `RF-14-28`, `RN-14-07` a `RN-14-09`.

## What Changes

- **Meus aportes** na App 08: os aportes **homologados** do Apoiador, com data, tipo e destino,
  e o Poder Sustentador como total acumulado em moedas (`RF-14-21`, `RF-14-22`).
- **Necessidades em aberto** na App 08, lidas da rota pública já existente, com a atividade, a
  comunidade e o que falta em moedas (`RF-14-24`).
- **Declaração de aporte** pelo Apoiador em sessão, a partir de uma necessidade, de um valor
  sugerido da escada do perfil ou de um valor livre, com comprovante obrigatório (`RF-14-25`,
  `RF-14-26`).
- A declaração **nasce pendente**: não credita moeda, não compõe o Poder Sustentador e não
  abate o que falta a necessidade alguma (`RF-14-26`, `RN-14-07`).
- **Situação da declaração** — pendente, homologada ou recusada com motivo — visível ao
  Apoiador dentro da plataforma (`RF-14-27`).
- **Homologação por Admin**: o registro do aporte apontando a declaração de origem converte o
  valor em moedas e credita, e nunca é feito pelo próprio provedor (`RN-14-07`, `RN-14-08`).
- **Recusa por Admin**, com motivo obrigatório, para que o estado do `RF-14-27` seja alcançável
  — decisão do fundador de 2026-09-01: a rota nasce no núcleo nesta fatia e a tela da gestão
  fica para a fatia 16 do PRD-02.
- A aplicação **recusa aporte em material, serviço ou divulgação** e encaminha à gestão
  (`RF-14-28`).
- **Moedas em toda tela**, reais só naquela em que se declara a transferência (`RF-14-23`,
  `RN-14-09`).
- `GET /v1/meus-aportes` passa a trazer o **nome** do tipo de recurso e o destino junto dos
  identificadores, para que "Meus aportes" apresente tipo e destino sem rota de Admin
  (`RF-14-21`). A declaração pendente não entra nessa lista: ela vive na rota da situação, e só
  vira aporte ao ser homologada.

Fora do escopo, como o PRD-14 §3.2 já exclui: autocadastro do Apoiador, homologação do próprio
aporte e edição do ledger, aporte em material, serviço ou divulgação pela aplicação,
ressarcimento e recibo fiscal. Fora do recorte da fatia, por dependerem da fatia 5: a
declaração **a partir de uma missão** do `RF-14-25` e tudo que envolva `MissaoDoApoiador`,
`SeloDoApoiador` e nível de sustento.

## Capabilities

### New Capabilities

Nenhuma. A fatia estende capacidades que já existem.

### Modified Capabilities

- `aporte`: a declaração feita pelo Apoiador na App 08 nasce pendente, com comprovante e sem
  creditar nada; o Admin a homologa registrando o aporte com origem "App 08", ou a recusa com
  motivo, e nunca homologa o próprio (`RF-14-25` a `RF-14-28`, `RN-14-07`, `RN-14-08`).
- `poder-sustentador`: a saída de `GET /v1/meus-aportes` leva o nome do tipo de recurso e o
  destino, ao lado do Poder Sustentador em moedas (`RF-14-21`, `RF-14-22`, `RF-14-23`).
- `necessidade-de-recurso`: a saída publicada leva o **nome** do tipo de recurso, da comunidade
  e do ponto de apoio junto dos identificadores, para que a lista da App 08 apresente atividade
  e comunidade sem rota de Admin (`RF-14-24`).
- `area-do-apoiador`: as telas de "Meus aportes", de necessidades em aberto e de declaração do
  aporte, com o encaminhamento de quem quer aportar material ou serviço (`RF-14-21` a
  `RF-14-28`, `RN-14-09`).

## Impact

- Backend: `backend/src/nucleo/aportes/` (entidade da declaração, regra e rotas),
  `backend/src/nucleo/poder_sustentador/rotas.py`, `backend/src/nucleo/necessidades/`, uma
  migração Alembic e os testes do recorte.
- Frontend: `apps/app-08-apoiador/src/aportes/` (telas e API) e a navegação de `App.tsx`; a
  escada de valores sugeridos de `preCadastro/escada.ts` passa a ser compartilhada.
- Documentação: a decisão nova da recusa no documento 04 §2 e no documento 09 §1, e a linha
  da fatia 4 em `openspec/cronograma-de-fatias.md`.
