# PRDs — Documentos de Requisitos de Produto

Esta pasta reúne os **PRDs** (_Product Requirements Documents_) do Comunidade Game, derivados
do documento 08 e escritos um a um, na ordem das ondas abaixo. Cada PRD segue o
[modelo de PRD](00-modelo-de-prd.md) e vale para o **Ciclo 01** (Guerreira Zeferina,
ago–dez/2026).

O PRD é artefato **derivado**: ele aplica as regras dos documentos 01–15 e não cria regra
própria. As regras de escrita, o fluxo de decisão das pendências e o processo de entrega estão
no `CLAUDE.md`, na raiz do repositório; o mapa de dependências entre PRDs está no documento 99.

## Situação da esteira

| PRD                                       | Assunto                                | Aplicação | Onda | Situação     |
| ----------------------------------------- | -------------------------------------- | --------- | ---- | ------------ |
| [PRD-08](prd-08-comunidades-virtuais.md)  | Comunidades Virtuais e território      | —         | 1    | implementado |
| [PRD-07](prd-07-economia-e-ledger.md)     | Economia de recursos e ledger          | —         | 1    | aprovado     |
| [PRD-01](prd-01-backend-api.md)           | Backend API (núcleo)                   | —         | 1    | implementado |
| [PRD-02](prd-02-frontend-de-gestao.md)    | Frontend de gestão                     | App 03    | 2    | aprovado     |
| [PRD-04](prd-04-aula-presencial.md)       | Aula presencial (onboarding e trilhas) | App 01    | 2    | aprovado     |
| [PRD-09](prd-09-area-do-mestre.md)        | Área do Mestre (autoria e operação)    | App 09    | 3    | aprovado     |
| [PRD-05](prd-05-area-do-guerreiro.md)     | Área do Guerreiro(a)                   | App 05    | 3    | aprovado     |
| [PRD-13](prd-13-area-dos-responsaveis.md) | Área dos pais e responsáveis           | App 07    | 4    | aprovado     |
| [PRD-03](prd-03-vitrine-publica.md)       | Vitrine pública                        | App 06    | 4    | aprovado     |
| [PRD-14](prd-14-area-do-apoiador.md)      | Área do Apoiador                       | App 08    | 5    | aprovado     |
| [PRD-10](prd-10-batalhas.md)              | Batalhas e eventos presenciais         | —         | 5    | aprovado     |
| [PRD-12](prd-12-jogo-em-javascript.md)    | App 04: Jogo em JavaScript             | App 04    | 5    | aprovado     |
| [PRD-11](prd-11-personalizacao-por-ia.md) | Personalização por IA                  | —         | 5    | aprovado     |

Situações possíveis: **não iniciado**, **em elicitação**, **em redação**, **em revisão**,
**aprovado** e **implementado**. O link para o documento aparece nesta tabela quando ele entra
na pasta.

O PRD-01 volta a **implementado**: a change `ponto-de-apoio-e-tabela-de-referencia`, primeira
fatia do PRD-07, entregou o `PontoDeApoio` e fechou o `RF-01-71` — a aula passa a declarar
**em qual ponto de apoio acontece**, exigido e da mesma comunidade dela. Era a última pendência
do PRD-01. Antes disso, a change `auditoria-e-estorno-da-coleta` entregou o débito de ponto
regular por fato desfeito (`RF-01-57`, `RF-01-69`, `RF-01-70`, `RN-01-55`) e a queda da
credencial de dispositivo ao **encerramento da série** (`RF-01-68`).

O PRD-07 segue em implementação. A primeira fatia entregou, além do `PontoDeApoio`, o
catálogo de **tipos de recurso** e o **valor de referência em moedas** versionado por vigência
(`RF-07-01`, `RF-07-02`), com o **responsável pelo acervo designado depois do cadastro**
(`RF-07-49`, `RN-07-34`).

A segunda fatia entregou o **livro-razão** — lançamento imutável, de natureza crédito, débito
ou ajuste, recusado a alterar ou remover também fora do ORM (`RF-07-19`, `RN-07-15`), e o saldo
por tipo de recurso **e ponto de apoio**, sempre derivado dos lançamentos e recontável
(`RF-07-07`, `RN-07-36`) — e o **aporte**: registro pelo Admin, valorado pela vigência da
tabela **na data do aporte** (`RF-07-04`, `RF-07-05`, `RN-07-03`), a absorção de Mestre ou
Admin que credita no ato, sem homologação, e nasce **ressarcível** (`RF-07-06`, `RF-07-21`,
`RN-07-35`), o comprovante em PDF, JPG ou PNG (`RN-07-22`) e a homologação do aporte declarado
no pré-cadastro, que credita só nesse ato (`RF-07-30`, `RN-07-21`).

A terceira fatia entregou a **reserva** — o vínculo entre a aula e o recurso que ela consome,
que compromete o saldo sem movimentá-lo (`RF-07-08`, `RN-07-01`). O agendamento passa a
declarar os recursos consumidos e a reservá-los no ponto de apoio da aula: havendo disponível
para todos, a aula nasce **confirmada**; faltando qualquer parcela, nasce **pendente de
lastro**, sem reserva alguma. O **lançamento da atividade realizada** grava os resultados dos
participantes e, na mesma operação, converte cada reserva em **baixa** — um débito por reserva
— e leva a aula a **realizada** (`RF-07-09`, `RF-02-35`, `RN-07-36`). O **cancelamento**, de
Admin ou Mestre da comunidade da aula, **libera** as reservas (`RF-01-72`, `RF-02-95`) — fecha
o `RF-01-72` do PRD-01, a primeira escrita de gestão do Mestre. A reserva nunca expira por
decurso de prazo. O **aporte que fecha a diferença confirma a aula pendente de lastro no mesmo
ato**, sem ato humano de confirmação (`RN-07-37`) — o `RF-02-67` deixa de atribuir esse ato à
App 03 e passa a apenas mostrá-lo.

O documento 09 mantém a pendência de **quem desativa um ponto de apoio**. **Empréstimo de
bancada e reposição solidária saíram do escopo** — o documento 05 já os adiava, e o PRD
divergia da fonte. No Ciclo 01 ficam o tombamento, a ficha de vida e a conferência de
inventário. Seguem para as próximas fatias a necessidade publicada e a cobertura parcial da
aula pendente de lastro, o Poder Sustentador, a prestação de contas pública, o ressarcimento, o
patrimônio, o catálogo avulso e o desafio extra.

O PRD-08 volta a **implementado**: a change `lista-publica-de-comunidades` entregou o
`GET /comunidades` com os quatro indicadores do documento 02 §1 (`RF-08-30`, `RF-08-31`),
última fatia do PRD-08. A pendência que a travava foi decidida — comunidade abaixo do piso sai
na lista sem os indicadores —, e com ela veio o cálculo dos quatro indicadores, que estava
apenas nomeado. A entrega do conjunto abaixo do bairro segue fora do escopo — corre fora da
plataforma no Ciclo 01.

A coluna **Onda** é a ordem em que os PRDs foram **escritos**, e o motivo de cada onda está
no documento 08. Ela não é a ordem em que o código entra: essa está no documento 99 §9.

O **PRD-06 — Assistente por voz e Modo Ouvinte** foi extinto: o App 02 passou a fazer parte do
App 01 e o Modo Ouvinte saiu do produto. O que restou dele está no PRD-04.
