# Proposal

**PRD de origem:** PRD-04 — Aula presencial (App 01).
**Cronograma:** fatia **21** do bloco do PRD-04.
**Identificadores atendidos:** `RF-04-72` — **novo**, a criar na revisão do PRD-04 —, alterando
`RF-04-01`, `RF-04-67` e `RN-04-40`, e alcançando `RF-04-35`, `RF-04-68`, `RF-05-08`, `RF-05-10` e
`RF-05-17`.

**Depende** de duas coisas, nenhuma delas resolvível aqui:

1. O PR de revisão do **documento 03 §3**, que hoje determina que "registrada a presença, o
   atendimento termina — formar equipe é outro momento". É a fonte do `RF-04-67`, e esta fatia a
   contraria.
2. O PR de revisão do **PRD-04**, que cria o `RF-04-72` e altera `RF-04-01`, `RF-04-67` e
   `RN-04-40`.

## Trava a resolver antes da implementação

### O fato que decide

O documento 11 §2.2 diz da sondagem: ela **"abre a trilha ao ser respondida, não ao ser
acertada"**. Não é avaliação — é o portão. Sem respondê-la, o percurso não anda.

Com o recorte de **leitura apenas**, a consequência é concreta: a criança recém-inscrita que
abrir a trilha no aparelho do encontro verá a sondagem, entenderá que é o primeiro passo e
**não poderá dá-lo ali**. A tela anuncia um percurso que não se move, e o passo que falta só
existe na App 05.

E há um segundo caso, mais grave que o primeiro. A inscrição em trilha é da App 05
(`RF-05-09`), usada em casa. **Quem não tem aparelho em casa não se inscreve, não responde
sondagem e não desbloqueia missão em lugar nenhum** — e o aparelho do encontro é o único a que
essa criança tem acesso. Num projeto para comunidades periféricas, isso não é detalhe de
recorte.

### As três opções, e o que cada uma custa

**Opção A — leitura apenas** (o recorte escrito nesta proposta).

| | |
| --- | --- |
| A criança faz no encontro | vê as trilhas inscritas, a missão atual, a seguinte trancada com o motivo e as atividades da equipe |
| Requisitos novos alcançados | nenhum além do `RF-04-72` |
| Rotas | nenhuma escrita |
| Custo em código | o menor: os componentes promovidos entram com a escrita desligada |
| O que fica quebrado | a sondagem visível e não respondível; quem não tem aparelho em casa não começa trilha nenhuma |

**Opção B — leitura, mais sondagem e desbloqueio.**

| | |
| --- | --- |
| Acrescenta | responder à sondagem, que abre a trilha, e ao desafio de desbloqueio — quiz aferido pelo núcleo a 60%, ou prático declarado e julgado pelo Mestre autor |
| Requisitos alcançados | `RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`, `RN-05-45` a `RN-05-47` |
| Rotas | `POST /v1/eu/missoes/{id}/desbloqueio` — **já existe** |
| Custo em código | **baixo**: `Sondagem` e `DesafioDeDesbloqueio` já existem e já estarão em `comum/` por esta fatia; é ligar o que a decisão 3 do `design.md` deixa opcional |
| Custo real | de **escopo**: o PRD-04 passa a abrigar atos que hoje são só do PRD-05, e a §3.2 dele precisa deixar de excluí-los |

O desbloqueio é **do Guerreiro(a), nunca da equipe** (documento 11 §2.2), e no aparelho
compartilhado cada atendimento já é de um Guerreiro(a) só — a sessão dele — então nada no
modelo se quebra.

**Opção C — B, mais entrega individual da produção.**

| | |
| --- | --- |
| Acrescenta | `RF-05-74` a `RF-05-77`: entrega por texto, fala transcrita ou foto, com devolutiva construtiva que não credita ponto |
| Colisão | a App 01 **já entrega produção por equipe** (`RF-04-45`), no caminho das equipes. Duas entregas na mesma aplicação, possivelmente sobre a mesma missão, exigem regra dizendo qual vale — e isso é decisão de produto, não de tela |

### Recomendação

**Opção B.** O custo em código é quase nulo, porque os componentes já estarão promovidos; sem
ela a fatia entrega uma tela que anuncia um percurso que não anda; e é o que dá à criança sem
aparelho em casa uma porta de entrada na trilha. A **opção C fica fora**: a colisão com a
entrega por equipe é decisão de produto e merece fatia própria.

### A pergunta que sobra dentro da B

A inscrição em trilha e a escolha do poder (`RF-05-09`) **entram também**? Sem elas, a criança
sem aparelho em casa continua sem começar: a sondagem só aparece depois de a inscrição existir.
Abrir a inscrição no encontro é coerente com o precedente da **troca por recompensa**, que o
PRD-04 §3.2 atribui à App 01 justamente por ser presencial. Mas amplia a fatia outra vez, e é
decisão do fundador.

### O que muda nos artefatos se a resposta não for A

O `RF-04-72` cresce ou ganha um irmão; a §3.2 do PRD-04 deixa de excluir os atos admitidos; e
neste delta o requisito "A tela SHALL ser de **leitura**" se inverte, com os cenários "A tela
não escreve nada" trocados pelos da sondagem e do desbloqueio. O `design.md` já prevê o ponto de
entrada: a decisão 3 deixa a escrita opcional nos componentes promovidos.

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
  | nenhuma trilha inscrita         | que não há inscrição, e que inscrever-se acontece na App 05 |

- O percurso mantém o padrão da App 05: **a missão atual e a seguinte trancada, com o motivo** —
  não a lista inteira. Para quem acabou de se inscrever, a missão atual **é a sondagem**, porque é
  ela a próxima do percurso: "começar pela sondagem" sai do dado, sem regra nova.
- As **atividades da aula** aparecem junto, pelas equipes do Guerreiro(a) naquela aula.
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

  `GET /v1/eu/equipes` substitui o `GET /v1/equipes/{id}/missao` previsto no cronograma: ela já
  devolve `aula_id` e as atividades de cada equipe, o que dispensa descobrir a equipe primeiro — e
  a App 01 **não** tem como identificar a equipe do Guerreiro(a) pela lista da aula, porque
  `IntegranteDaEquipe` traz só avatar, nick e papel, por exigência do `RN-04-14`.

### Fora do escopo

O que o PRD-04 §3.2 já exclui — em particular, apoio escolar, coleta de território, ranking e canal
de sugestões, que são a App 05. Além disso, e sujeito à trava acima:

- **Responder à sondagem e ao desafio de desbloqueio** no encontro (`RF-05-13`, `RF-05-14`,
  `RF-05-89`).
- **Entrega individual da produção** da missão (`RF-05-74`) — a entrega por **equipe** do
  `RF-04-45` continua onde está, no caminho das equipes.
- **Inscrever-se em trilha** e escolher poder (`RF-05-09`): a tela diz onde acontece.
- A lista inteira do percurso e a distinção entre missão realizada, liberada e bloqueada,
  retiradas do escopo pelo fundador em 2026-09-25.
- Progresso, retomadas e culminância (`RF-05-15`, `RF-05-39`, `RF-05-79`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o desfecho da presença deixa de terminar o atendimento como único
  desfecho, a tela inicial ganha o caminho do percurso, e a App 01 passa a apresentar o percurso do
  Guerreiro(a) e as atividades das equipes dele na aula (`RF-04-72`, `RF-04-01`, `RF-04-67`,
  `RN-04-40`).

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
