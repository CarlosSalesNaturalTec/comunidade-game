# Esqueleto da aula presencial e equipe da aula

Origem: **PRD-04 — App 01: Aula presencial**, §§6.1 e 6.2. Primeira fatia do PRD-04.

Atende `RF-04-02`, `RF-04-03`, `RF-04-05`, `RF-04-30`, `RF-04-31`, `RF-04-32`, `RF-04-33`,
`RF-04-34` e `RF-04-59`; atende em parte `RF-04-01` e `RF-04-29`.

## Why

O módulo `equipes` do núcleo está escrito e testado desde a change `aula-presenca-e-equipe` —
`criar_equipe`, `entrar_na_equipe`, `sair_da_equipe`, `homologar_equipe_da_trilha` e
`equipes_da_aula`, com os dois tetos, os dois tempos de vida e o papel do integrante — e **não
tem uma única rota**. A capacidade `equipe` está consolidada em `openspec/specs/equipe/spec.md`
com sete requisitos, e nenhum deles é alcançável por HTTP.

A consequência não fica dentro do PRD-04. Como `criar_equipe` é restrita ao Guerreiro(a) pelo
invariante 15, e o Guerreiro(a) só forma equipe no encontro presencial, a ausência da App 01
trava, hoje, requisitos de três PRDs diferentes:

| Travado hoje                                  | PRD    | Por quê                                        |
| --------------------------------------------- | ------ | ---------------------------------------------- |
| `RF-09-41` — banco do Quiz disponível na partida | PRD-09 | abrir partida exige equipe **da aula**        |
| Quiz ao Vivo conduzido na App 03              | PRD-02 | idem, e o vínculo aparelho–equipe é dela      |
| Criação original entregue e validada          | PRD-09 | `entregar_criacao_original` exige `equipe_id` |
| Área do Guerreiro(a)                          | PRD-05 | piso de dependência é o PRD-09, já em curso   |

`criacoes_originais` é o segundo módulo órfão nessa cadeia: regra e modelo prontos, sem rotas,
e sem equipe formada a fila de validação do Mestre nasceria vazia. Abrir a porta de `equipes` é
o primeiro nó do laço.

Esta fatia abre a porta e entrega o cliente dela — a terceira aplicação do repositório —,
seguindo o mesmo desenho das duas anteriores: `esqueleto-da-gestao-e-cadastro-de-comunidade`
para a App 03 e `esqueleto-da-area-do-mestre-e-autoria-da-trilha` para a App 09.

## What Changes

### A porta HTTP da equipe (PRD-04 §9)

As rotas são as que o PRD-04 §9 declara. Nenhuma regra nova: os dois tetos, a equipe de aula
encerrada, a participação em mais de uma equipe da mesma aula e a vedação de Admin e Mestre
alterarem composição já estão em `equipes/regra.py` e são reexpostas, não reescritas.

| Rota                                    | Persona      | Atende                              |
| --------------------------------------- | ------------ | ----------------------------------- |
| `GET /v1/aulas/{id}/equipes`            | Guerreiro(a) | `RF-04-34`, `RF-04-33`              |
| `POST /v1/aulas/{id}/equipes`           | Guerreiro(a) | `RF-04-30`, `RF-04-59`              |
| `POST /v1/equipes/{id}/integrantes`     | Guerreiro(a) | `RF-04-30`, `RF-04-31`, `RF-04-59`  |
| `DELETE /v1/equipes/{id}/integrantes/eu` | Guerreiro(a) | `RF-04-30`                          |

A matriz de permissões já tem as duas operações de que elas dependem —
`equipe_que_forma_na_aula` para escrever e `equipes_da_aula_em_andamento` para ler —, sem
entrada nova.

A saída do `GET` mostra **avatar e nick** e nada mais (`RF-04-34`, invariante 11).

### A App 01

Nasce `apps/app-01-aula-presencial/`, Mobile First, com o que o encontro exige antes de
qualquer conteúdo:

- **Sessão de trabalho do aparelho** (`RF-04-05`, `RF-04-02`, `RF-04-03`): o Mestre ou o Admin
  entra por login social; a aplicação lê `GET /v1/aulas/vigentes` — rota já no ar — e decide.
  Nenhuma aula vigente, não abre. Uma, assume a comunidade dela. Mais de uma, pergunta **uma
  única vez** em qual está operando. A sessão dura a janela da aula, conforme o PRD-04 §13.
- **Tela inicial** com os dois caminhos, onboarding e trilhas (`RF-04-01`, em parte: o caminho
  do onboarding entra desabilitado, com o motivo em uma linha).
- **Entrada do Guerreiro(a)** por `POST /v1/sessoes/guerreiro/confirmacao` (`RF-04-29`, em
  parte — ver decisão 1).
- **Equipes da aula**: criar, entrar, sair, com o papel declarado, e a lista por avatar e nick.

`frontend-ci.yml` já filtra por `apps/**`, `package.json` já declara o workspace `apps/*`,
`firebase.json` já aponta o alvo `aula` para `apps/app-01-aula-presencial/dist` e a chave de
aplicação `app-01-aula-presencial` já é semeada nos dois ambientes. Faltam a entrada do alvo
em `.firebaserc` e o `app-01-deploy.yml`, espelho do da App 09.

### Três decisões do fundador, 2026-08-24

1. **A primeira fatia entra sem câmera.** Todo Guerreiro(a) entra por
   `POST /v1/sessoes/guerreiro/confirmacao`, com o Mestre ou Admin confirmando a identidade
   no encontro. Não é regra nova: é o caminho que o `RF-04-15` e a jornada 5.5 já preveem para
   quem não tem _template_ gravado, e a operação `confirmacao_de_identidade_do_guerreiro` já
   está na matriz. `RF-04-29` fica atendido em parte, e a captura por nick e imagem entra com
   a fatia do onboarding.

   Revisto durante a implementação (`/opsx:apply`, 2026-08-24): a rota, herdada de uma fatia
   anterior, exige `guerreiro_id`, e nenhuma rota resolve o nick digitado nesse identificador
   — criar uma violaria o invariante da capacidade `persona-e-credencial` que veda busca por
   nick de Guerreiro(a) **por quem quer que pergunte**, adulto autenticado incluído. A rota
   passa a receber o **nick**, resolvendo-o internamente e recusando de forma indistinguível
   entre nick inexistente e nick que não é de Guerreiro(a) — o mesmo padrão que a abertura por
   biometria já usa. Ver design.md — decisão 1.1.
2. **Mestre e Admin cadastram Guerreiro(a).** Hoje `POST /v1/guerreiros` exige `Operacao.tudo`
   — só Admin. O PRD-04 §9 quer o autocadastro sob a sessão de trabalho do aparelho, que o
   `RF-04-05` abre a **Mestre ou Admin**. A matriz do PRD-01 §4 ganha a operação de cadastro de
   Guerreiro(a) para o Mestre. Decisão gravada agora; **o código dela é da fatia do
   onboarding**, não desta.
3. **A conferência de nick do onboarding fica atrás da sessão de trabalho do aparelho.** O
   PRD-04 §9 declara `GET /v1/guerreiros/nick/disponivel` como pública, o que contradiz a
   decisão de 2026-08-21 — a conferência pública varre **só nicks de adulto**, nunca o de
   Guerreiro(a), para não abrir o oráculo que a pendência vedava, e o documento 09 §104 já
   proíbe sugerir e completar na busca pública. A conferência do onboarding passa a exigir a
   sessão do aparelho; a rota pública `GET /v1/nicks/disponibilidade`, que já existe, segue
   adulto-only e intocada. Decisão gravada agora; **o código dela é da fatia do onboarding**.

## Capabilities

### New Capabilities

- `aplicacao-da-aula-presencial`: a App 01 — a sessão de trabalho do aparelho amarrada à janela
  da aula agendada, a tela inicial dos dois caminhos, a entrada do Guerreiro(a) no encontro e a
  formação da equipe da aula. Irmã de `aplicacao-de-gestao` e `area-do-mestre`.

### Modified Capabilities

- `equipe`: a capacidade ganha a **porta HTTP** que faltava — as quatro rotas do PRD-04 §9 — e
  o requisito da **leitura das equipes da aula** pelo Guerreiro(a) em sessão, restrita a avatar
  e nick. Nenhum dos sete requisitos vigentes muda de comportamento.
- `sessao-do-guerreiro`: o requisito "Mestre ou Admin abre a sessão por confirmação humana"
  passa a receber **nick**, não `guerreiro_id`, resolvendo-o internamente e recusando de forma
  indistinguível entre nick inexistente e nick que não é de Guerreiro(a) — preserva o invariante
  de `persona-e-credencial` que a rota anterior, sem consumidor até aqui, não respeitava.

## Impact

| Onde                                                 | O quê                          |
| ---------------------------------------------------- | ------------------------------ |
| `backend/src/nucleo/equipes/rotas.py`                | arquivo novo                   |
| `backend/src/nucleo/principal.py`                    | registro do roteador           |
| `backend/src/nucleo/sessoes/rotas.py`                | entrada da confirmação: nick, não `guerreiro_id` |
| `backend/src/nucleo/personas/regra.py`               | resolução interna de nick de Guerreiro(a) |
| `backend/src/nucleo/erros.py`                        | classe `ConfirmacaoDeGuerreiroRecusada`  |
| `apps/app-01-aula-presencial/`                       | pasta nova                     |
| `.firebaserc`, `.github/workflows/app-01-deploy.yml` | alvo e esteira de publicação   |

Sem migração Alembic: nenhuma coluna nova. `equipes/regra.py`, `equipes/modelo.py` e
`backend/tests/test_equipe.py` não são reescritos.

Documentação no mesmo PR: PRD-04 §9 (a conferência de nick deixa de ser pública) e §14 (saem as
três pendências decididas), PRD-01 §4 e documento 02 §1 (a matriz ganha o cadastro de
Guerreiro(a) pelo Mestre), documento 09 (as três linhas novas em "Já decididos", e a linha do
`RF-09-61` que volta ao ciclo seguinte), `docs/prds/index.md` (situação do PRD-04 e narrativa
da fatia) e `docs/prds/prd-09-area-do-mestre.md` §6.8 (`RF-09-61` alinhado à decisão de
conservação do acervo, que já está no documento 09).

## Fora do escopo

Reproduz o que o PRD-04 §3.2 já exclui, mais o limite desta fatia:

| O quê                                             | Por quê                                    |
| ------------------------------------------------- | ------------------------------------------ |
| Conversa conduzida por IA, áudio e chat           | PRD-04 §6.1; fatia do onboarding           |
| Câmera, vivacidade, descritor e _template_        | `RF-04-13`, `-14`, `-48`; idem             |
| Consentimento do responsável                      | `RF-04-11`, `-12`; `consentimentos` sem rota |
| Cadastro do novo Guerreiro(a) e conferência de nick | `RF-04-07` a `-10`; decisões 2 e 3        |
| Presença registrada na atividade                  | `RF-04-17` a `-21`; fatia do onboarding    |
| Fila local e sincronização sem rede               | `RF-04-23` a `-25`                         |
| Missão, conteúdo, entrega da produção, assistente | `RF-04-35` a `-40`; dependem do PRD-09 §6.3 |
| Quiz ao Vivo no aparelho da equipe                | `RF-04-41` a `-44`; condução é da App 03   |
| Troca por recompensa avulsa                       | PRD-04 §6.3; depende do momento de troca   |
| Homologação da equipe **da trilha**               | `RF-01-63`; é ato do Mestre, na App 09     |
| Guarda do _template_ e conferência no login       | PRD-04 §3.2 — é o PRD-01                   |
| Cadastro de responsável e anexo do termo assinado | PRD-04 §3.2 — App 03 e App 09              |
| Agenda das aulas e ajuste de presenças            | PRD-04 §3.2 — App 03                       |

## Pendências levantadas — decisão do fundador

Nenhuma trava esta fatia.

1. **`RF-02-71` continua sem rota**, terceira change seguida. Já registrado nas §14 do PRD-02 e
   do PRD-09; não alcança esta fatia.

A duração da sessão de trabalho depois do fim da janela **não** virou pendência: o desenho a
resolve relendo `GET /v1/aulas/vigentes` — que é exatamente `inicio_em ≤ agora ≤ fim_em` — a
cada volta à tela inicial, sem inventar tolerância nem intervalo de sondagem.
