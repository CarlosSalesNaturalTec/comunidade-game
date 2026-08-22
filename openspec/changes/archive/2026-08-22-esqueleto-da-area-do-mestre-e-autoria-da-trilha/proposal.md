# Esqueleto da Área do Mestre e autoria da trilha

Origem: **PRD-09 — Área do Mestre**, §6.1. Primeira fatia do PRD-09.

## Why

A trilha é o eixo do domínio: nove entidades do núcleo apontam para `trilha` ou `missao` —
ponto regular, nível, badge, criação original, etiqueta ODS, desafio de coleta, recompensa de
marco, atividade e partida de quiz. A regra dela está escrita e testada em
`trilhas/regra.py` desde a fatia `poder-trilha-missao-e-atividade`, mas **nenhuma porta HTTP a
alcança**: `trilhas/` é um dos onze módulos do núcleo com `modelo.py` e `regra.py` e sem
`rotas.py`.

A consequência já é concreta. Três rotas entregues e cobertas por teste são inalcançáveis
hoje, porque exigem um identificador que nenhuma porta sabe criar:

| Rota entregue                            | Exige                    | Quem cria hoje |
| ---------------------------------------- | ------------------------ | -------------- |
| `POST /v1/desafios-de-coleta`            | `missao_id`              | ninguém        |
| `POST /v1/trilhas/{id}/recompensas-de-marco` | `trilha_id`, `missao_id` | ninguém    |
| `POST /v1/aulas/{id}/lancamentos`        | `atividade_id`           | ninguém        |

Esta fatia abre a porta e entrega o cliente dela. Sem cliente, `POST /v1/trilhas` nasceria
como um quarto portal órfão — e o cliente não pode ser a App 03, porque o `RF-02-71` do PRD-02
dá ao Admin a leitura da autoria **sem editá-la**, e o §4 do PRD-09 repete: o Admin não edita
a trilha de um Mestre. Quem escreve trilha é o Mestre, na App 09.

## What Changes

### A porta HTTP da autoria (PRD-09 §9)

As rotas são as que o PRD-09 §9 declara. Nenhuma regra nova: as recusas — poder obrigatório e
de natureza de Guerreiro(a), posse do Mestre autor, sondagem única e na primeira posição,
declaração de obrigatória ou opcional, três eixos da atividade — já estão em
`trilhas/regra.py` e são reexpostas, não reescritas.

| Rota                            | Persona | Atende                                         |
| ------------------------------- | ------- | ---------------------------------------------- |
| `POST /v1/trilhas`              | Mestre  | `RF-09-01`                                     |
| `GET /v1/trilhas/minhas`        | Mestre  | `RF-09-04`                                     |
| `POST /v1/trilhas/{id}/missoes` | Mestre  | `RF-09-02`, `RF-09-03`, `RF-09-80`, `RF-09-81` |
| `POST /v1/missoes/{id}/atividades` | Mestre | `RF-09-69`, `RF-09-70`                        |
| `POST /v1/missoes/{id}/retomada`| Mestre  | `RF-09-83`, `RF-09-101`                        |

### Os rótulos que faltam no modelo (PRD-09 §8)

O núcleo tem a regra e não tem os rótulos: as entidades nasceram nas fatias do PRD-01 para
sustentar pontuação, nível e badge, e funcionam como chave estrangeira, não como conteúdo que
um Mestre escreve. A `Missao` não tem título; a `Atividade` também não. Entram os atributos
que o PRD-09 §8 já declara e que a autoria exige:

| Entidade    | Atributos novos                                        | Atende                   |
| ----------- | ------------------------------------------------------ | ------------------------ |
| `Missao`    | `titulo`, `etapa_do_ciclo`, `cadencia_de_retomada`     | `RF-09-03`, `RF-09-83`   |
| `Atividade` | `titulo`, `descricao`                                  | `RF-09-69`               |

### A App 09 e a camada de acesso comum

Nasce `apps/app-09-mestre/`, com entrada do Mestre por login social, sessão e a autoria de
trilha → missão → atividade de ponta a ponta (PRD-09 §4, §6.1).

É a segunda aplicação do repositório, e por isso a fatia sobe para `comum/` o que hoje vive
dentro da App 03 e vale para as oito: o cliente do núcleo (`api/cliente.ts`,
`api/configuracao.ts`, `api/tipos.ts`) e a sessão (`ContextoDeSessao`,
`armazenamentoDeSessao`, `BotaoDeEntradaGoogle`). A App 03 passa a consumir de `comum/`, sem
mudança de comportamento. Duplicar significaria dois lugares para corrigir quando o contrato
de erro único do PRD-01 mudar, e ele vale para todas as aplicações.

O `frontend-ci.yml` já filtra por `apps/**` e o `firebase.json` já declara o alvo `mestre`:
faltam a entrada do alvo em `.firebaserc` e o `app-09-deploy.yml`, espelho do da App 03.

## Capabilities

### New Capabilities

- `area-do-mestre`: a App 09 — aplicação inteiramente autenticada, entrada do Mestre por login
  social, sessão, e a autoria de trilha, missão e atividade. Irmã de `aplicacao-de-gestao`.
- `camada-de-acesso-comum`: o cliente do núcleo e a sessão do adulto compartilhados pelas oito
  aplicações — os dois cabeçalhos de toda chamada, o corpo de erro único do PRD-01 e a
  distinção entre recusa de chave e recusa de sessão.

### Modified Capabilities

- `trilha-e-missao`: a missão passa a ter **título**, **etapa do ciclo** e **cadência de
  retomada**; a trilha e a missão ganham a porta HTTP que faltava.
- `atividade-de-trilha`: a atividade passa a ter **título** e **descrição**, e ganha a porta
  HTTP.

## Impact

| Onde                                          | O quê                                      |
| --------------------------------------------- | ------------------------------------------ |
| `backend/src/nucleo/trilhas/rotas.py`         | arquivo novo                               |
| `backend/src/nucleo/trilhas/modelo.py`        | cinco colunas novas, com migração Alembic  |
| `backend/src/nucleo/principal.py`             | registro do roteador                       |
| `comum/api/`, `comum/autenticacao/`           | promovidos da App 03                       |
| `apps/app-03-gestao/src/`                     | passa a consumir de `comum/`               |
| `apps/app-09-mestre/`                         | pasta nova                                 |
| `.firebaserc`, `.github/workflows/app-09-deploy.yml` | alvo e esteira de publicação        |

Destrava, sem tocá-las, `POST /v1/desafios-de-coleta`,
`POST /v1/trilhas/{id}/recompensas-de-marco` e `POST /v1/aulas/{id}/lancamentos`.

## Fora do escopo

| O quê                                          | Por quê                                  |
| ---------------------------------------------- | ---------------------------------------- |
| Publicação, travas e despublicação             | `RF-09-05` a `-11`, `-82`; fatia própria |
| Conteúdo e bibliografia da missão              | PRD-09 §6.3, três entidades novas        |
| Culminância e desafio de desbloqueio           | PRD-09 §6.4                              |
| Etiqueta ODS declarada pelo Mestre             | PRD-09 §6.1, rotas próprias no §9        |
| Template de missão                             | PRD-09 §6.2, depende de IA               |
| Banco do Quiz, minhas turmas, lançamentos      | PRD-09 §§6.5, 6.6                        |
| `Atividade.recursos` do PRD-09 §8              | nenhum `RF` de §6.1 o exige              |
| `RF-02-71` — leitura da autoria pelo Admin     | pendência abaixo                         |

## Pendências levantadas — decisão do fundador

Nenhuma trava esta fatia; as três precisam de decisão antes das fatias seguintes.

1. **`RF-02-71` não tem rota.** O PRD-02 §9 não declara rota de leitura de trilha ou
   atividade, e o `GET /v1/trilhas/{id}` do PRD-09 §9 é público e serve trilha publicada — não
   serve ao Admin lendo rascunho. Sem decisão, o Admin não tem por onde consultar a autoria.
2. **A situação da trilha tem dois ou três valores?** O PRD-09 §8 lista rascunho, publicada e
   **despublicada**; o `RF-09-11` diz que a trilha despublicada **volta a rascunho** — dois
   estados. O núcleo e a spec `trilha-e-missao` implementaram dois. Trava a fatia de
   publicação.
3. **`RF-02-29` — atividade avulsa, fora de trilha.** O PRD-09 §8 a reconhece ("`Atividade`
   sem missão só existe como atividade avulsa da gestão"), mas `Atividade.missao_id` é
   `NOT NULL` e a spec `atividade-de-trilha` exige a missão. Trava a fatia de lançamentos do
   PRD-02.
