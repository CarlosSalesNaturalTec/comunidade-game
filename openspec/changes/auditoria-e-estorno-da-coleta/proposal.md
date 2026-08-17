## Why

O PRD-08 fecha com uma fatia só: a **auditoria por amostragem** do Mestre sobre os registros de
coleta, com a **confirmação** que credita e a **invalidação** que estorna. Ela estava travada
desde a primeira fatia da coleta pela contradição entre o estorno que `RF-08-13` exige e o
`RF-01-57` vigente, que proibia debitar ponto regular em qualquer operação.

A contradição foi levada ao fundador e resolvida: **ponto regular debita por fato desfeito,
nunca por troca**. A investigação mostrou que a proibição absoluta excedia a própria fonte — o
documento 11 §5 já classificava a **pontuação negativa de conduta como regular**, de modo que
`RF-01-57` travava também o `RF-02-38` do PRD-02, que ninguém tinha notado. Junto com ela veio a
segunda decisão: o valor **"a conferir" não pontua até a confirmação do Mestre**, como os
documentos 02 §1 e 11 §5 sempre disseram e o PRD-08 §5.3 tinha lido ao contrário.

As duas decisões já percorreram o fluxo — documento-fonte, documento 09 e PRD — nos commits
`8225312` e `4738651` deste branch. Esta change é o quarto nível: o código.

## What Changes

- Nasce a **amostra semanal** de auditoria do Mestre: **10% dos registros da semana em cada
  série ativa, com o mínimo de um**, e **todo valor "a conferir" entra obrigatoriamente**, fora
  do percentual. Série ativa é apurada **no instante da amostra**, nunca aproveitada de apuração
  anterior (`RN-08-20`).
- Nasce a **confirmação** do Mestre sobre o registro auditado. Confirmar registro "a conferir"
  **credita** os pontos que ele ainda não tinha; confirmar registro já válido apenas encerra a
  auditoria dele, **sem creditar de novo** (`RF-08-29`, `RN-08-26`).
- Nasce a **invalidação** com motivo, que **estorna** o valor exato creditado por aquele
  registro e o mantém gravado, marcado como inválido (`RF-08-13`, `RN-08-09`).
- **BREAKING** — o registro fora da faixa esperada passa a **nascer sem crédito**. Hoje ele
  credita na gravação e a marca "a conferir" só o destina à amostra; passa a creditar zero até a
  confirmação (`RF-08-12`, `RN-08-26`). Alcança a resposta da gravação de registro, que já
  informa se pontuou; no Ciclo 01 a App 05 ainda não a consome.
- **BREAKING** — o ponto regular deixa de recusar todo débito. O listener do ORM e o gatilho do
  PostgreSQL que hoje recusam qualquer redução de `PontoRegular` dão lugar a uma trava mais
  estreita: **o saldo nunca fica negativo** e **nível e badge conquistados não regridem**, mas a
  redução por fato desfeito é aceita (`RF-01-57`, `RF-01-69`, `RF-01-70`, `RN-01-55`).
- A **ocorrência de conduta** do `RF-02-38` **não entra nesta change** — ela é do PRD-02, de onda
  posterior. O que entra é a capacidade de debitar que ela também exigirá.
- O escopo é o do **Mestre autor do desafio** da série: os demais recebem **403**, como já vale
  para a emissão da credencial de dispositivo e como o PRD-08 §9 declara.

## Capabilities

### New Capabilities

- `auditoria-da-coleta`: a conferência do Mestre sobre os registros das séries dos seus
  desafios — a composição da amostra semanal, a confirmação que credita o "a conferir", a
  invalidação com motivo que estorna e a imutabilidade do que foi auditado. É a superfície que
  fecha o ciclo de vida da situação do registro, que até aqui só sabia nascer.

### Modified Capabilities

- `pontos-niveis-e-badges`: o requisito "Ponto regular é creditado por trilha ou poder e nunca
  debitado" passa a admitir o **débito por fato desfeito**, com o piso em zero e sem regressão
  de nível ou badge; e o crédito da coleta passa a **não alcançar o registro "a conferir"** até
  a confirmação.
- `registro-de-coleta`: o requisito do valor fora da faixa deixa de dizer que ele "credita
  pontos normalmente"; e a situação do registro, hoje o único campo que evolui sem que nada a
  faça evoluir, ganha as transições **confirmado** e **invalidado**.

## Impact

- `backend/src/nucleo/coletas/`: a superfície de auditoria — composição da amostra, confirmação
  e invalidação — ao lado da série e do registro que as fatias anteriores entregaram.
- `backend/src/nucleo/pontuacao/`: o débito de ponto regular, com o piso em zero; o listener
  `_recusar_debito_de_ponto_regular` e `_recusar_remocao_de_ponto_regular` são revistos, não
  removidos — a recusa de `DELETE` permanece.
- `backend/alembic/`: migração que troca a função `recusar_debito_de_ponto_regular` e o gatilho
  `trg_ponto_regular_nunca_debita` pela trava estreita, e acrescenta ao registro os campos da
  auditoria (quem auditou, quando, motivo da invalidação).
- `backend/src/nucleo/permissoes.py`: a operação de auditoria da coleta, escopada ao Mestre
  autor do desafio.
- `backend/src/nucleo/principal.py`: as duas rotas novas no roteador de coletas.
- `backend/tests/`: amostra com o piso de um e o percentual, "a conferir" sempre na amostra,
  série ativa apurada no instante, confirmação que credita uma vez só, invalidação que estorna o
  valor exato, "a conferir" invalidado que estorna zero, estorno que para em zero, nível que não
  regride, e o 403 do Mestre que não é autor do desafio.
- `docs/`: **nada a fazer nesta change**. As duas decisões já foram gravadas nos
  documentos-fonte (02 §1, 03 §§1.1 e 12.3, 11 §5, 99 §6), no documento 09 e nos PRDs 01, 04 e
  08, com `docs/prds/index.md` atualizado, nos commits `8225312` e `4738651` deste branch.
