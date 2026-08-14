## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Quarta fatia dele e
vigésima da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-22` (Guerreiro(a) solicita a inclusão de local ausente, e a
solicitação entra na fila de aprovação), `RF-08-23` (Mestre da trilha ou Admin aprova ou
recusa, com motivo na recusa), `RF-08-24` (Mestre e Admin veem alerta das solicitações em
aberto) e `RN-08-18` (local nasce de cadastro do Admin ou de solicitação aprovada; o pedido em
si não cria local). Do PRD-01, `RF-01-03` (autoria de toda escrita autenticada), `RF-01-16`
(matriz de permissões por papel) e `RF-01-18` (filtro por comunidade em consulta de dado de
comunidade).

A primeira fatia do PRD-08 adiou estes três requisitos por escrito, e disse por quê: a
`SolicitacaoDeLocal` chega à trilha pelo **desafio de origem**, e sem `DesafioDeColeta` não
havia como escopar qual Mestre avalia sem inventar regra transitória. O desafio existe desde a
segunda fatia, e a trilha é alcançada por `missao.trilha_id` — o mesmo caminho que a emissão da
credencial de dispositivo já percorre.

É a última superfície que falta para o local nascer de outra origem que não o Admin. O critério
de aceite do PRD-08 §12 mede exatamente isso: solicitação aprovada pelo Mestre da trilha cria o
local e **libera a abertura da série**; recusada, devolve o motivo ao Guerreiro(a).

## What Changes

- Nasce a **`SolicitacaoDeLocal`**, com os atributos que o PRD-08 §8 declara: solicitante,
  comunidade, desafio de origem, nível pretendido, rótulo, justificativa, situação, avaliador e
  motivo da recusa (`RF-08-22`).
- O Guerreiro(a) solicita na **sua comunidade vigente** e para um **desafio de coleta** — é o
  desafio que prende a solicitação à trilha e, por ela, ao Mestre que avalia (`RF-08-22`,
  `RN-08-02`).
- A avaliação é ato de **Admin ou do Mestre autor da trilha** do desafio de origem, o mesmo
  escopo que o Mestre já tem sobre a própria trilha. Mestre de outra trilha recebe **403**
  (`RF-08-23`).
- **Aprovar cria o local**; recusar exige **motivo**. O pedido em si NEVER cria local, em
  nenhuma situação (`RN-08-18`).
- O local criado pela aprovação nasce sob as **mesmas regras de hierarquia** do local que o
  Admin cadastra — pai do nível imediatamente acima, da mesma comunidade, só o nível
  `comunidade` sem pai. A aprovação muda **quem cria**, nunca o que vale para o local
  (`RF-08-04`).
- A **lista de solicitações em aberto** alimenta o alerta das Apps 03 e 09, filtrada por
  comunidade como toda consulta de dado de comunidade. O Admin vê todas as daquela comunidade;
  o Mestre, só as dos desafios das **suas** trilhas (`RF-08-24`, `RF-01-18`).
- A situação percorre **recebida → aprovada** ou **recebida → recusada**, e o desfecho grava
  **quem avaliou** e **quando**. Solicitação já avaliada não se reavalia.

### Por que não é a quinta natureza da fila de avaliação

A primeira fatia do PRD-08 deixou esse achado registrado, e ele se confirma. A capacidade
`fila-de-avaliacao` tem o requisito **"Nenhuma solicitação cria cadastro, persona ou acesso"**,
válido "em nenhuma das quatro naturezas e em nenhuma situação — **inclusive quando aprovadas**".
`RN-08-18` manda o oposto: a aprovação **cria o local**. Some-se que o avaliador pode ser o
Mestre da trilha, e não só um Admin.

Daí decorre o que esta fatia NEVER herda: o **prazo de 7 dias** das quatro naturezas. Nada no
PRD-08 o estende à solicitação de local, e `RF-08-24` fala em solicitação **em aberto**, não em
atraso. Declarar prazo aqui seria criar regra que o PRD não tem.

### Fora do escopo

O que o PRD-08 §3.2 já exclui: importação de fontes públicas de dados; georreferenciamento por
coordenada de GPS; interface das telas de coleta; escolha do banco de séries temporais.

O que é do PRD-08 mas de outra fatia:

| Fica para                          | Porque                                                      |
| ---------------------------------- | ----------------------------------------------------------- |
| `RF-08-10`, `RF-08-11`             | ciclo de vida da série: interrupção, retomada, encerramento |
| `RF-08-13`                         | invalidação e estorno, com a amostra semanal do Mestre      |
| `RF-08-16`, `RF-08-19`, `RF-08-20` | painel público e exportação agregada                        |
| `RF-08-17`, `RF-08-18`             | consulta das séries pelo Guerreiro(a) e pelo responsável    |
| `RF-08-26`, `RF-08-27`             | cobertura de ODS e meta 17.18                               |
| `RF-08-28`, `RN-08-24`             | piso de três coletores: vale na saída publicada             |
| `RN-08-19`                         | despersonalização por revogação do consentimento            |
| `RF-08-03`                         | transferência de comunidade, fora do Ciclo 01 (invariante 4) |

Fica fora também a **consulta do Guerreiro(a) ao status da própria solicitação**. Ela é
`RF-05-32`, do PRD-05, e a §9 daquele PRD não lista rota que a sirva — a lacuna está no PRD-05,
não neste recorte, e não se preenche dentro de um artefato do OpenSpec. Está anotada em
`design.md` como pergunta ao fundador para a entrega da App 05.

O PRD-08 §14 registra **nenhuma pendência remanescente**, e nenhuma linha aberta do documento 09
§1 alcança este recorte.

## Capabilities

### New Capabilities

- `solicitacao-de-local`: a solicitação de novo local pelo Guerreiro(a) — o que ela carrega, a
  comunidade e o desafio de origem que a prendem à trilha, a avaliação por Admin ou pelo Mestre
  autor daquela trilha, a aprovação que cria o local sob as regras de hierarquia vigentes, a
  recusa com motivo obrigatório, o ciclo de situação que não se reavalia, a lista de abertas
  que alimenta o alerta com o recorte de cada papel, e o que ela NEVER faz — criar local no
  ato do pedido e herdar o prazo das quatro naturezas da fila.

### Modified Capabilities

- `local-do-territorio`: o requisito vigente **"Admin cadastra o local, e o local não nasce de
  outra origem nesta entrega"** declara o cadastro por Admin como única origem e aponta
  `RF-08-22` a `RF-08-24` como de fatia posterior. Passa a valer que o local nasce de **duas**
  origens — o cadastro direto do Admin e a **aprovação de solicitação** por Admin ou pelo
  Mestre autor da trilha do desafio de origem —, e que as duas gravam o local sob as mesmas
  regras de hierarquia. A recusa com 403 a quem não é Admin permanece para o cadastro direto
  (`RF-08-04`, `RF-08-23`, `RN-08-18`).

## Impact

- `backend/src/nucleo/locais/`: a entidade `SolicitacaoDeLocal`, as regras de solicitação e de
  avaliação, e a separação do portão de autorização do núcleo de validação da hierarquia, que
  hoje vive dentro de `cadastrar_local` — detalhada em `design.md`.
- `backend/src/nucleo/permissoes.py`: a operação de solicitar local, nova no conjunto de escrita
  do Guerreiro(a), e a de listar em aberto; `aprovacao_de_local`, que a matriz já declara para o
  Mestre, ganha a sua primeira rota.
- `backend/src/nucleo/principal.py`: as três rotas novas.
- `backend/alembic/`: migração da tabela `solicitacao_de_local`.
- `backend/tests/`: solicitação em comunidade que não é a do Guerreiro(a) recusada; solicitação
  por quem não é Guerreiro(a) recusada; aprovação por Admin e pelo Mestre autor; recusa do
  Mestre de outra trilha com 403; aprovação criando o local e recusa exigindo motivo; pedido
  que não cria local; hierarquia inválida recusada na aprovação sem consumir a solicitação;
  solicitação já avaliada que não se reavalia; lista de abertas sem filtro de comunidade
  recusada com 422; e o recorte por trilha do Mestre na lista.
- `docs/prds/prd-01-backend-api.md` §4: a matriz de personas e permissões ganha **a solicitação
  de novo local** entre o que o Guerreiro(a) escreve — ver "Omissão corrigida", abaixo. É a
  única mudança em `docs/`. O PRD-08 segue "aprovado" em `docs/prds/index.md`, como nas três
  fatias anteriores dele; o documento 09 não muda, porque não há decisão nova; e o documento 99
  não muda, porque nenhuma relação entre documentos foi alterada.

## Decisões que esta fatia recebeu

Duas ambiguidades apareceram ao recortar a fatia e foram levadas ao fundador. Ambas se
resolveram **dentro do que os PRDs já dizem** — nenhuma percorre o fluxo de decisão nova,
porque nenhuma grava regra em documento-fonte.

**De onde vem o local pai na aprovação.** O PRD-08 §8 lista os atributos da `SolicitacaoDeLocal`
e **não há local pai entre eles**; mas todo local abaixo do nível `comunidade` exige pai
(`RF-08-04`). Os PRDs que descrevem a jornada — PRD-02 §5.4, PRD-09 §5.9.1 e `RF-05-32` — dizem
apenas "aprova, criando o local", sem declarar quem informa o pai.

**Decisão: o avaliador informa o local pai no ato da avaliação.** É o "como" de "criando o
local", coerente com `RN-08-18` — se o ato de criação é do avaliador, é o payload dele que
completa o local. Mantém a solicitação exatamente como o PRD-08 §8 a descreve, sem atributo
inventado, e não altera o que `RF-05-32` diz que o Guerreiro(a) declara.

**O alcance de "todas" na lista do Admin.** `RF-08-24` põe Mestre e Admin diante das
solicitações em aberto sem dizer o recorte de cada um. O do Mestre o PRD dá: as das suas
trilhas. O do Admin não.

**Decisão: o Admin vê todas as solicitações da comunidade filtrada** — de qualquer trilha e de
qualquer Mestre. É aplicação da matriz de permissões, em que o Admin já lê tudo, e **preserva o
filtro obrigatório por comunidade** que `RF-01-18` impõe a toda consulta de dado de comunidade e
que a rota irmã `GET /locais` já aplica. O "todas" contrasta com o recorte por trilha do Mestre,
não com o filtro por comunidade.

## Omissão corrigida no PRD-01 §4

A matriz de personas e permissões do PRD-01 §4 lista **"aprovação de local"** entre o que o
Mestre escreve — e a `Operacao.aprovacao_de_local` já existe no código desde a semeadura da
matriz —, mas **não lista a solicitação** entre o que o Guerreiro(a) escreve. `RF-08-22` e
`RF-05-32` atribuem o ato a ele sem ambiguidade.

Levado ao fundador, ficou decidido tratar como **omissão da matriz**, não como negação: a §4
já rastreia este domínio pelo lado do avaliador, e o silêncio do lado do solicitante é lacuna
de redação. A linha do Guerreiro(a) passa a incluir **a solicitação de novo local**, no mesmo PR
desta change — o precedente é o commit `52e5420`, que acrescentou à mesma matriz a emissão da
credencial de dispositivo pelo Mestre.

**Não é decisão nova** e por isso não percorre o fluxo do documento-fonte e do documento 09:
`RF-08-22` já é a regra, e a matriz apenas deixa de contradizê-la por omissão.
