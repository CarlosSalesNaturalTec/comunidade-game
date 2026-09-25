# Proposal

**PRD de origem:** PRD-04 — Aula presencial (App 01).
**Cronograma:** fatia **21** do bloco do PRD-04.
**Identificadores atendidos:** `RF-04-72`, `RF-04-73` e `RF-04-74` — **novos**, a criar na revisão
do PRD-04 —, alterando `RF-04-01`, `RF-04-67` e `RN-04-40`, e alcançando `RF-04-35`, `RF-04-68`,
`RF-05-08`, `RF-05-09`, `RF-05-10`, `RF-05-13`, `RF-05-14`, `RF-05-17`, `RF-05-89`, `RN-05-20`,
`RN-05-43`, `RN-05-44` e `RN-05-45` a `RN-05-47`.

**Depende** de duas coisas, nenhuma delas resolvível aqui:

1. O PR de revisão do **documento 03 §3**, que hoje determina que "registrada a presença, o
   atendimento termina — formar equipe é outro momento". É a fonte do `RF-04-67`, e esta fatia a
   contraria.
2. O PR de revisão do **PRD-04**, que cria o `RF-04-72`, o `RF-04-73` e o `RF-04-74`, altera
   `RF-04-01`, `RF-04-67` e `RN-04-40`, e declara na §3.2 que a inscrição, a sondagem e o
   desbloqueio passam a ser desta aplicação por decisão do fundador de 2026-09-25 — só a entrega
   individual da produção segue fora.

## A decisão que recortou esta fatia

A fatia nasceu recortada como **leitura apenas**, e a trava foi levada ao fundador com três opções
medidas. Em 2026-09-25 ele escolheu a **opção B**: leitura, **mais a sondagem e o desbloqueio**, sem
a entrega individual da produção.

### O fato que pesou

O documento 11 §2.2 diz da sondagem que ela **"abre a trilha ao ser respondida, não ao ser
acertada"**. Não é avaliação — é o portão. Com leitura apenas, a criança recém-inscrita veria a
sondagem no aparelho do encontro, entenderia que é o primeiro passo e **não poderia dá-lo ali**: a
tela anunciaria um percurso que não se move.

E o caso que pesou mais: a inscrição em trilha é da App 05 (`RF-05-09`), usada em casa. **Quem não
tem aparelho em casa não responde sondagem nem desbloqueia missão em lugar nenhum**, e o aparelho do
encontro é o único a que essa criança tem acesso.

### O que a opção B traz, e o que ficou fora

| | |
| --- | --- |
| Entra | responder à sondagem, que abre a trilha, e submeter o desafio de desbloqueio — quiz aferido pelo núcleo a 60%, ou prático declarado e julgado pelo Mestre autor |
| Requisitos | `RF-04-73` (novo), `RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`, `RN-05-45` a `RN-05-47` |
| Rota | `POST /v1/eu/missoes/{id}/desbloqueio` — **já existe** |
| Custo em código | **baixo**: `Sondagem` e `DesafioDeDesbloqueio` já existem e são promovidos a `comum/` por esta mesma fatia; a App 01 **liga** o que a decisão 3 do `design.md` deixa opcional |
| Fica fora | a **entrega individual** da produção (`RF-05-74`), que colidiria com a entrega por **equipe** do `RF-04-45`, já existente nesta aplicação: duas entregas sobre a mesma missão exigiriam regra que nenhum documento declara |

O desbloqueio é **do Guerreiro(a), nunca da equipe** (documento 11 §2.2), e no aparelho compartilhado
cada atendimento já é de um Guerreiro(a) só — a sessão dele —, então nada no modelo se quebra.

### A inscrição em trilha também entra

A pergunta que sobrava dentro da B — se a **inscrição em trilha e a escolha do poder** (`RF-05-09`)
também acontecem no encontro — foi respondida pelo fundador em 2026-09-25: **sim**. Pelo mesmo
argumento que decidiu a opção B, levado às últimas consequências: **sem inscrição não há sondagem a
responder**, e a criança sem aparelho em casa seguiria sem começar trilha alguma. O precedente é o
da troca por recompensa, que o PRD-04 atribui à App 01 justamente por ser presencial.

Com ela, os **três atos individuais de partida** da trilha acontecem no aparelho do encontro —
inscrição, sondagem e desbloqueio —, e só a **entrega individual da produção** fica fora. Quem não
tem inscrição alguma chega ao catálogo de poderes do ciclo e inscreve-se ali, sem teto de quantas
trilhas e sem desinscrição, que não existe. Feita a inscrição, o percurso abre no mesmo atendimento,
na sondagem.

Nada mais segue em aberto nesta fatia.

## Why

Registrada a presença, o atendimento termina e a criança volta à tela inicial (`RF-04-67`, fatia
18, decisão de 2026-09-23). Quem chega ao encontro e não vai formar equipe naquele momento não tem,
no aparelho da aula, nenhum caminho até a própria trilha: o percurso individual — trilhas inscritas,
missão em que está, o que vem depois — vive só na App 05, usada em casa.

Decisão do fundador de 2026-09-25: o aparelho do encontro passa a levar ao percurso, por dois
caminhos — o desfecho da presença e a tela inicial.

## What Changes

- A tela **"Presença registrada"** passa a oferecer, ao lado de voltar ao início, o acesso às
  **trilhas e missões do jogador**. A sessão do Guerreiro(a) já está aberta nesse momento — a
  aplicação chama `entrarComToken` antes de trocar de tela —, então o acesso não pede nick nem rosto
  de novo.
- A **tela inicial** ganha o mesmo caminho, para quem registrou a presença antes. Como os caminhos
  das equipes, do quiz e da troca, ele abre a sessão pela entrada do Guerreiro(a) e passa pela
  guarda de presença do `RN-04-40`.
- A tela do percurso apresenta:

  | Situação                        | O que aparece                                              |
  | ------------------------------- | ---------------------------------------------------------- |
  | mais de uma trilha inscrita     | a lista das trilhas, e a escolhida abre o percurso dela    |
  | uma trilha inscrita             | direto o percurso dela                                     |
  | nenhuma trilha inscrita         | o catálogo de poderes do ciclo, para escolher e inscrever-se |

- O percurso mantém o padrão da App 05: **a missão atual e a seguinte trancada, com o motivo** —
  não a lista inteira. Para quem acabou de se inscrever, a missão atual **é a sondagem**, porque é
  ela a próxima do percurso: "começar pela sondagem" sai do dado, sem regra nova.
- As **atividades da aula** aparecem junto, pelas equipes do Guerreiro(a) naquela aula.
- Quem não tem inscrição alguma chega ao **catálogo de poderes do ciclo** e **inscreve-se** ali
  mesmo; feita a inscrição, o percurso abre na sondagem, no mesmo atendimento.
- O Guerreiro(a) **responde à sondagem** e **submete o desafio de desbloqueio** ali mesmo, pela
  porta que já existe. Respondida a sondagem, a trilha abre no mesmo atendimento.
- A **entrega individual** da produção **não** entra: a entrega por equipe do `RF-04-45` segue sendo
  a desta aplicação, no caminho das equipes.
- Os componentes de trilha da App 05 são **promovidos a `comum/`** e passam a servir as duas
  aplicações. As aplicações não se importam entre si — cada `package.json` de `apps/*` depende só de
  `comum` —, então reusar é promover.
- **Nenhuma rota nova.** Quatro leituras que já existem bastam:

  | Leitura                              | Serve                                                |
  | ------------------------------------ | ---------------------------------------------------- |
  | `GET /v1/eu/trilhas`                 | as trilhas inscritas, com a próxima missão de cada   |
  | `GET /v1/eu/trilhas/{id}/missoes/{ordem}` | a missão atual e a seguinte, com o motivo do bloqueio |
  | `GET /v1/eu/equipes`                 | as equipes do Guerreiro(a), **com as atividades de cada uma** |
  | `GET /v1/trilhas/{id}`               | conteúdo e bibliografia da missão                    |
  | `GET /v1/vitrine/poderes`            | o catálogo de poderes do ciclo, com as trilhas de cada um |
  | `POST /v1/eu/trilhas/{id}/inscricao` | a inscrição, que devolve a existente sem erro se repetida |

  As duas últimas entram com a inscrição, e são porta que **já existe**.
  `GET /v1/eu/equipes` substitui o `GET /v1/equipes/{id}/missao` previsto no cronograma: ela já
  devolve `aula_id` e as atividades de cada equipe, o que dispensa descobrir a equipe primeiro — e
  a App 01 **não** tem como identificar a equipe do Guerreiro(a) pela lista da aula, porque
  `IntegranteDaEquipe` traz só avatar, nick e papel, por exigência do `RN-04-14`.

### Fora do escopo

O que o PRD-04 §3.2 já exclui — em particular, apoio escolar, coleta de território, ranking e canal
de sugestões, que são a App 05. Além disso:

- **Entrega individual da produção** da missão (`RF-05-74`) — a entrega por **equipe** do
  `RF-04-45` continua onde está, no caminho das equipes.
- A lista inteira do percurso e a distinção entre missão realizada, liberada e bloqueada,
  retiradas do escopo pelo fundador em 2026-09-25.
- Progresso, retomadas e culminância (`RF-05-15`, `RF-05-39`, `RF-05-79`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o desfecho da presença deixa de terminar o atendimento como único
  desfecho, a tela inicial ganha o caminho do percurso, a App 01 passa a apresentar o percurso do
  Guerreiro(a) e as atividades das equipes dele na aula, e passa a admitir a **inscrição**, a
  **sondagem** e o **desbloqueio** no encontro (`RF-04-72`, `RF-04-73`, `RF-04-74`, `RF-04-01`,
  `RF-04-67`, `RN-04-40`).

**Sem delta** em `area-do-guerreiro`: a App 05 não muda de comportamento — os componentes mudam de
lugar, o que é desenho, não spec. **Sem delta** em `camada-visual-comum`: os componentes promovidos
são tela de domínio, e aquela capacidade é o contrato visual e de acessibilidade. As duas correções
ao que o cronograma previa entram na mesma change, como o `config.yaml` manda.

## Impact

- `comum/trilha/` — os componentes promovidos da App 05 e a fatia do cliente de API que eles usam.
- `comum/package.json` e `comum/tsconfig.json` — a exportação da pasta nova.
- `apps/app-05-guerreiro/src/trilha/` e `src/api/trilha.ts` — passam a consumir o que foi promovido,
  sem mudar comportamento.
- `apps/app-01-aula-presencial/src/trilhas/` — a tela do percurso no encontro.
- `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` — o caminho novo.
- `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx` — o desfecho da presença e
  o título do caminho novo, no mapa por caminho.
- `apps/app-01-aula-presencial/src/api/` — o cliente das leituras que faltam nesta aplicação.
- Os testes das duas aplicações e do `comum`.
- `openspec/cronograma-de-fatias.md` — a situação da fatia 21.
- `docs/03-plataforma-e-arquitetura.md`, `docs/prds/prd-04-aula-presencial.md` e
  `docs/09-topicos-em-aberto-e-sugestoes.md` — nos PRs de revisão, que entram antes.
- Sem alteração no núcleo, em rota ou em contrato de API.
