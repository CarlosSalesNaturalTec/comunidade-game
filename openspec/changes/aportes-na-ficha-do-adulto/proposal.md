# Aportes na ficha do adulto

Origem: **PRD-02**, fatia **29** do `openspec/cronograma-de-fatias.md` (nova, aberta nesta
change). Decisões do fundador de 2026-11-17, em `/opsx:propose`:

1. A ficha de **Mestre e de Apoiador** na App 03 passa a mostrar os aportes de que a pessoa é
   provedora.
2. Cada aporte homologado aparece com data, tipo de recurso (nome e unidade), quantidade, valor
   em moedas, ponto de apoio, forma e destinação. Aparece também se **tem comprovante**, sem
   baixar o arquivo.
3. A ficha mostra o **total do Poder Sustentador** e, em lista separada, as **declarações
   pendentes** feitas pela App 08.
4. O **valor de origem em reais**, quando houver, aparece ao lado das moedas. É uma **exceção
   da gestão**: a ficha é só do Admin, não é pública. Essa exceção altera o documento 04 §1 e
   o invariante 16 do documento 99 §6.

Identificadores **novos** (nascem na revisão do PRD-02, no mesmo PR, pelo precedente da fatia
25):

- `RF-02-117`: o Admin vê na ficha do adulto os aportes homologados, o Poder Sustentador e as
  declarações pendentes.
- `RN-02-34`: na ficha da gestão, o valor de origem em reais sai sempre ao lado das moedas, e
  só ali.

Aplicados sem mudança: `RF-02-02`, `RF-02-03`, `RN-02-01` (a ficha segue de leitura),
`RF-07-17` e `RN-07-05` (a saída pública e a do Apoiador continuam sem reais), `RN-07-22` (o
comprovante não sai em rota pública) e PRD-07 §11 (o valor de origem é da gestão).

## Why

Para o Admin, o aporte registrado some. Ele credita o ponto de apoio, mas a ficha de quem
doou só mostra os artefatos do cadastro. Nenhuma tela da gestão diz quanto uma pessoa já
aportou, nem o que ela declarou pela App 08 e ainda espera homologação. Hoje, só o próprio
Apoiador enxerga isso, na App 08.

## What Changes

- **Núcleo**: nasce `GET /v1/provedores/{id}/aportes`, restrita ao Admin. Devolve três coisas
  do provedor:
  - os aportes homologados, do mais recente ao mais antigo, com o valor de origem em reais
    quando houver e a marca de comprovante;
  - o Poder Sustentador, pela mesma derivação de `poder_sustentador_de`;
  - as declarações pendentes.

  Guerreiro(a) e responsável respondem 404, como já acontece na leitura pública do Poder
  Sustentador.
- **App 03**: a `FichaDoAdulto` ganha a seção **Aportes**, com o total do Poder Sustentador,
  a tabela dos homologados e a lista das declarações pendentes. A ficha continua só de
  leitura.
- **Documentação**:
  - documento 04 §1: a exceção da gestão para os reais;
  - documento 99 §6, invariante 16;
  - documento 09 §1, "Já decididos";
  - PRD-02: §6.1, §7, §9, §13 e §15;
  - a linha da fatia 29 do cronograma.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `poder-sustentador`: nasce a leitura, pelo Admin, dos aportes, do Poder Sustentador e das
  declarações pendentes de um provedor, com o valor de origem em reais.
- `aplicacao-de-gestao`: a ficha do adulto ganha a seção de aportes.

## Impact

- **Backend**: `backend/src/nucleo/poder_sustentador/rotas.py` e um teste novo em
  `backend/tests/`. Nenhuma migração, porque todo campo já existe em `Aporte` e em
  `AporteDeclarado`.
- **App 03**: `apps/app-03-gestao/src/personas/FichaDoAdulto.tsx`, `personas/api.ts` e os
  testes de personas.
- **Outras aplicações**: nenhuma. `GET /v1/meus-aportes` e a vitrine continuam sem reais.
- **Risco declarado**: a ficha passa a ser o primeiro lugar da gestão que **mostra** as
  declarações da App 08. Homologar ou recusar uma declaração pela tela continua sem caminho na
  App 03, e esta fatia não abre esse caminho.
- **Fora do escopo** (PRD-02 §3.2 e decisão): baixar o comprovante, editar ou estornar aporte,
  e mostrar reais em qualquer outra tela.
