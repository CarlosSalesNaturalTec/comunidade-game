# Criação original e portfólio

Fatia 5 do **PRD-05 — Área do Guerreiro(a)**, com o recorte da validação vindo do **PRD-09 —
Área do Mestre**.

Atende `RF-05-39` a `RF-05-44` e `RF-09-31` a `RF-09-34`, sob `RN-05-13`, `RN-05-14`,
`RN-05-21`, `RN-09-04` e `RN-09-19`.

## Why

O invariante 5 do documento 99 §6 exige que toda trilha termine em criação original
apresentada publicamente, com autoria creditada. O núcleo já tem o registro, a regra de
entrega, a de validação, a pontuação e o badge; a vitrine já lê as criações validadas. Falta o
meio: **nenhuma rota HTTP entrega nem valida uma criação original**, e nenhuma tela a exibe.
Na prática, uma trilha do Ciclo 01 ainda não tem como terminar.

Esta é também a fatia que fecha a jornada §5.5 do PRD-05, imediatamente depois da fatia 4, que
entregou a inscrição na trilha, o guia do percurso e o desbloqueio da missão.

## What Changes

**Núcleo**

- Expõe a entrega sob a culminância: `POST /v1/culminancias/{id}/criacoes` (PRD-05 §9). A
  trilha da entrega é a da culminância endereçada; entrega em trilha sem culminância alcançada
  é recusada com 409.
- A entrega passa a ser **individual ou de equipe**, regida pela `modalidade` que o Mestre
  autor já declara na culminância (`RF-05-40`, documento 02 §4). Hoje a `CriacaoOriginal` só
  aceita equipe.
- A produção passa a aceitar **texto, imagem, vídeo, arquivo ou link** (`RF-05-40`), no mesmo
  padrão de tipo e envio que `ConteudoDaMissao` já firmou na App 09.
- A devolução passa a registrar o **motivo** em linguagem simples (`RF-05-42`, `RF-09-34`). A
  autoria não muda em nenhuma transição (`RN-05-13`, `RN-09-04`).
- `GET /v1/eu/portfolio` (PRD-05 §9): as criações validadas do Guerreiro(a), com trilha, data,
  autoria e a situação de exposição pública (`RF-05-43`, `RF-05-44`).
- Fila e decisão do Mestre autor: as criações entregues a validar, a validação e a devolução
  com motivo (`RF-09-31`, `RF-09-34`).
- O crédito dos 50 pontos, do nível 5 e do badge de autoria alcança o **autor individual**
  quando a modalidade é individual; em equipe segue integral a cada integrante, sem rateio
  (`RF-09-31`).
- O filtro de autorização da vitrine alcança o autor individual, além dos integrantes da
  equipe (`RF-09-33`, `RN-09-19`).

**App 05 — Área do Guerreiro(a)**

- Tela da culminância com o que a criação precisa ser e o critério de validação escritos pelo
  Mestre autor (`RF-05-39`).
- Entrega da criação, com o papel de cada integrante quando é de equipe (`RF-05-40`,
  `RF-05-41`).
- Devolução exibida com o motivo em linguagem simples, sem perda de autoria (`RF-05-42`).
- Portfólio das criações validadas, marcando o que está público e o que depende de autorização
  do responsável (`RF-05-43`, `RF-05-44`).

**App 09 — Área do Mestre**

- Fila das criações originais entregues nas trilhas de que o Mestre é autor, com a autoria e o
  papel de cada integrante (`RF-09-31`, `RF-09-32`).
- Validar, creditando autoria e liberando o badge; devolver com motivo (`RF-09-31`,
  `RF-09-34`).
- A tela informa que a criação validada só vai à vitrine com autorização do responsável
  (`RF-09-33`).

### Fora do escopo

Reproduz o que os PRDs já excluem, sem exclusão nova:

- Autoria da trilha, da culminância e do critério de validação — é da App 09 e já foi entregue
  (PRD-05 §3.2).
- Formação e homologação da equipe da trilha — acontecem no App 01 (`RN-05-12`, PRD-05 §3.2).
- Autorização de divulgação pública — é ato do responsável, na App 07; aqui só se lê o estado
  (PRD-05 §3.2).
- Exibição pública das criações — é da vitrine (App 06, PRD-03), que já lê o que foi validado.
- Acervo do Guerreiro(a), canal de sugestões e apoio escolar — Ciclo 02 (PRD-05 §3.2).

## Capabilities

### New Capabilities

Nenhuma. O recorte estende capacidades que já existem.

### Modified Capabilities

- `criacao-original`: entrega individual ou de equipe conforme a modalidade da culminância;
  produção em texto, imagem, vídeo, arquivo ou link; motivo registrado na devolução; entrega
  endereçada pela culminância e recusada quando a trilha não a alcançou.
- `culminancia`: a modalidade declarada rege quem entrega a criação, e a culminância passa a
  ser o endereço da entrega.
- `pontos-niveis-e-badges`: os 50 pontos, o nível 5 e o badge de autoria alcançam o autor
  individual quando a criação é individual.
- `leitura-publica-da-vitrine`: o filtro de autorização vigente alcança o autor individual,
  além dos integrantes da equipe.
- `area-do-guerreiro`: telas da culminância, da entrega e do portfólio.
- `area-do-mestre`: fila das criações a validar, validação e devolução com motivo.

## Impact

- `backend/src/nucleo/criacoes_originais/` — `modelo.py` (equipe opcional, guerreiro,
  tipo de produção, mídia, motivo da devolução, unicidade), `regra.py` e `rotas.py` (nova).
- `backend/src/nucleo/pontuacao/regra.py` — crédito ao autor individual.
- `backend/src/nucleo/vitrine/rotas.py` — filtro de autorização do autor individual.
- `backend/src/nucleo/principal.py` — registro do roteador novo.
- Migração de esquema da tabela `criacao_original`.
- `apps/app-05-guerreiro/src/` — culminância, entrega e portfólio, e o cliente de API.
- `apps/app-09-mestre/src/` — fila, validação e devolução, e o cliente de API.
- Documentação: `docs/prds/index.md` ganha uma linha na tabela de fatias do PRD-05.
