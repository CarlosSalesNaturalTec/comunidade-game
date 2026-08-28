# Aporte, necessidade e atividade avulsa na gestão

**PRD de origem:** PRD-02 — Frontend de gestão (App 03).
**Fatia:** 11 do bloco PRD-02 do `openspec/cronograma-de-fatias.md`.
**Atende:** `RF-02-29`, `RF-02-31`, `RF-02-32`, `RF-02-57`, `RF-02-58`, `RF-02-67`.

## Why

A App 03 já agenda a aula, mas não declara o que ela consome: sem isso nenhuma aula nasce
**pendente de lastro** pela gestão, a necessidade de recurso nunca é publicada e o invariante
9 do documento 99 §6 — nenhuma atividade sem lastro — fica sem superfície na gestão. Do outro
lado, o Admin só homologa aporte quando ele veio declarado no pré-cadastro (`RF-02-84`): o
registro avulso do `RF-02-57`, que é a porta comum de crédito do livro-razão, não existe. Esta
fatia fecha o circuito do documento 04 §1 — a aula declara, falta lastro, a necessidade é
publicada, o aporte entra e a aula se confirma sozinha — e acrescenta o cadastro da atividade
avulsa, que é o único cadastro de atividade que cabe à gestão (PRD-02 §3.2).

## What Changes

### Recorte ajustado — decisão do fundador nesta change

O cronograma previa `RF-02-29`, `RF-02-57`, `RF-02-58` e `RF-02-67`. O recorte previsto é
previsão, não contrato, e três pontos foram levados ao fundador antes da escrita:

| Ponto levado                                                                  | Decisão                                                             |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `RF-02-31` e `RF-02-32` ficaram adiados na fatia da agenda por falta de rota  | absorvidos aqui — sem eles a necessidade não existe para ser lida    |
| A pontuação da atividade avulsa não tem trilha em que pousar                  | a atividade avulsa declara o **poder** que desenvolve, e credita nele |
| `RF-02-29` fala em "recursos necessários" da atividade                        | o documento 04 §1 vence: quem declara e reserva recurso é a **aula**  |

As duas últimas são decisão nova e seguem o fluxo da hierarquia de autoridade: documento-fonte
(11 §5 e 04 §1), linha do documento 09 §1 e o `RF-02-29` e a §3.1 do PRD-02 corrigidos.

### Backend

- Cadastro da **atividade avulsa**, fora de trilha, por Admin (`RF-02-29`): `POST /v1/atividades`
  do PRD-02 §9, com título, descrição, modalidade, formato, natureza, produção esperada e o
  **poder** que ela desenvolve. `Atividade.missao_id` passa a admitir vazio, e o poder declarado
  é exigido exatamente quando não há missão.
- Lançamento do resultado de atividade avulsa (`RF-02-29`): sem trilha a conferir, o ato é
  restrito ao Admin e o ponto regular credita no **poder declarado**, pelo mesmo motor do
  documento 11 §5. Nível e badge de valores e causas continuam sendo percurso de trilha e não se
  movem pela avulsa.

### App 03

- **Agenda** — o agendamento declara os pares de tipo de recurso e quantidade que a aula consome
  e dispara a reserva (`RF-02-31`); a aula sem lastro aparece **pendente de lastro** e a falta
  vira necessidade publicada (`RF-02-32`).
- **Recursos** — área nova, com o registro e a homologação do aporte pela gestão, com provedor,
  tipo, quantidade, ponto de apoio, data, forma, comprovante e o valor em moedas devolvido pelo
  núcleo (`RF-02-57`), e a lista das necessidades de recurso em aberto (`RF-02-58`).
- Registrado o aporte que fecha a falta, a área mostra a **aula confirmada e a reserva
  efetivada**, sem ato humano de confirmação à parte (`RF-02-67`).
- **Atividades** — cadastro da atividade avulsa pelo Admin, com o poder e o tipo escolhidos; a
  pontuação vem do motor e não se digita (`RF-02-29`).

Nenhuma rota existente muda de contrato. `POST /aportes`, `GET /vitrine/necessidades`,
`GET /tipos-de-recurso`, `POST /aulas` e `GET /aulas` já existem e ficam como estão.

### O que fica para depois — e por quê

Nada disto é exclusão nova: o PRD-02 §3.1 mantém tudo em escopo, e a fatia apenas não alcança.

| Adiado                                        | Trava                                                          |
| --------------------------------------------- | -------------------------------------------------------------- |
| Atividade prevista no agendamento (`RF-02-30`) | pede a leitura da autoria do Mestre pelo Admin — PRD-02 §14     |
| Consulta da autoria do Mestre (`RF-02-71`)     | sem rota declarada — pendência aberta do PRD-02 §14             |
| Acervo e patrimônio na gestão                  | fatia 12                                                        |

## Capabilities

### New Capabilities

- `atividade-avulsa`: o cadastro, por Admin, da atividade fora de trilha — o poder que ela
  desenvolve, os três eixos do documento 11 §4 e o crédito do ponto regular naquele poder.

### Modified Capabilities

- `aplicacao-de-gestao`: o agendamento passa a declarar os recursos da aula; nasce a área
  Recursos, com o registro do aporte e a leitura das necessidades em aberto; nasce a área
  Atividades, com o cadastro da avulsa.
- `resultado-de-atividade`: o lançamento de atividade **sem missão** dispensa a conferência de
  posse da trilha, é restrito ao Admin e credita pelo poder declarado.

## Impact

- `backend/src/nucleo/trilhas/modelo.py` — `missao_id` opcional e `poder_id` na `Atividade`, com
  a migração correspondente.
- `backend/src/nucleo/` — módulo da atividade avulsa (regra e rotas), `resultados/regra.py` e
  `pontuacao/regra.py`.
- `apps/app-03-gestao/src/` — `agenda/`, `recursos/`, `atividades/` e a navegação do `App.tsx`.
- Documentação: documento 11 §5, documento 04 §1 (menção), documento 09 §1, PRD-02 (`RF-02-29`
  e §3.1) e a linha da fatia 11 no `openspec/cronograma-de-fatias.md`.
