## Why

Origem: **PRD-04** (App 01 — aula presencial), §§6.2, 8, 9 e 11. Fatias **8** e **9** do
`openspec/cronograma-de-fatias.md`, numa change só (fundador, 2026-08-30). Atende `RF-04-61`,
`RF-04-62`, `RF-04-45` a `RF-04-47` e `RN-04-31`.

Sete fatias puseram a criança no encontro e a equipe diante da programação: ela se cadastra,
entra por reconhecimento, forma equipe da aula, joga o Quiz ao Vivo, troca pontos extras e lê
em que missão está. O que a equipe faz depois de ler — **produzir** — não tem para onde ir, e
a **equipe da trilha**, sujeito da criação original que encerra a trilha, não tem como nascer.

Duas lacunas concretas:

- O núcleo já sabe criar e homologar equipe da trilha (`criar_equipe`,
  `homologar_equipe_da_trilha`, operação `homologacao_da_equipe_da_trilha` na matriz), mas
  **nenhuma rota HTTP** as expõe: a única porta de equipe vincula sempre à aula. Sem sujeito,
  a criação original em equipe da App 05 (`RF-05-40`, `RF-05-41`) lê uma equipe que ninguém
  cria.
- A `ProducaoDaMissao` **não existe no núcleo**. Ela está declarada só no PRD-05 §8, e o
  PRD-04 §8 diz que o caminho das trilhas acrescenta duas entidades — `RespostaDeQuiz` e
  `ConsultaAoAssistente` —, sem citá-la; o §9 não tem rota para a entrega. Sem ela, os
  `RF-04-45` a `RF-04-47` não têm onde gravar.

## What Changes

**Recorte da fatia 8 corrigido.** O cronograma previa `RN-04-17` e `RN-04-22` nesta fatia; as
duas são regras da **partida de quiz**, já atendidas nas fatias 6 e 7 (`quiz-ao-vivo` e
`aplicacao-da-aula-presencial`). A regra que a equipe da trilha traz é a `RN-01-44` — uma
equipe por trilha percorrida —, já vigente em `equipe`. A linha do cronograma se corrige nesta
change.

**Decisão nova do fundador, 2026-08-30: a produção entregue no App 01 é da equipe.** A
entrega gera **um** registro, vinculado à **equipe da aula** e à **atividade corrente** que
ela declarou, válido para todos os integrantes — o mesmo desenho da `RespostaDeQuiz`
(`RN-04-22`). A `ProducaoDaMissao` do PRD-05 §8 ganha o vínculo com a equipe, e o Guerreiro(a)
fica em branco quando a entrega é coletiva. As alternativas — um registro por integrante, ou
o registro só de quem entregou — foram descartadas: a primeira repete a mesma transcrição
cinco vezes, e a segunda apaga do histórico dos demais uma produção que foi de todos.

**Decisão nova do fundador, 2026-08-30: a fatia 9 cria a `ProducaoDaMissao` no núcleo**,
inteira como o PRD-05 §8 a declara. A fatia 7 do PRD-05 depois só acrescenta a porta
individual do Guerreiro(a) — `POST /v1/eu/missoes/{id}/producao` — sobre a entidade já de pé.

**Núcleo — equipe da trilha (fatia 8):**

- Nascem `POST /v1/trilhas/{id}/equipes`, do **Guerreiro(a) em sessão**, e
  `POST /v1/equipes/{id}/homologacao`, do **Mestre ou Admin** — as duas já previstas no
  PRD-04 §9 (`RF-04-61`, `RF-04-62`). As duas reexpõem as recusas já vigentes de `equipe`,
  sem afrouxar nenhuma: os dois tetos de composição, a equipe única por trilha e o
  congelamento depois da homologação.
- A programação do encontro passa a trazer, em cada item, a **trilha** da missão. É o que o
  aparelho precisa para oferecer a formação da equipe daquela trilha; hoje a saída para em
  `missao_id`.

**Núcleo — produção da missão (fatia 9):**

- Nasce a entidade `ProducaoDaMissao` — equipe, Guerreiro(a), missão, atividade, forma de
  entrega, transcrição, devolutiva e momento — **sem a foto e sem o áudio**, descartados na
  leitura (`RF-04-46`, documento 03 §12.2).
- Nasce `POST /v1/equipes/{id}/producao`, do **Guerreiro(a) em sessão** e restrita a
  **integrante daquela equipe**, ancorada na atividade corrente declarada. **Rota nova, que o
  PRD-04 §9 ainda não tem** — entra nele nesta change.
- A devolutiva é **construtiva e não credita ponto algum**: nenhum `Resultado`, nenhum
  lançamento, nenhuma progressão nascem dela; quem lança o resultado é o Mestre (`RF-04-47`,
  documento 11 §§2.2, 5).
- A devolutiva **sempre opera** no aparelho da equipe, sem consultar chave de personalização
  de integrante algum (`RN-04-31`, documento 03 §7.1).

**App 01:**

- O caminho das trilhas passa a oferecer, na programação, **formar a equipe da trilha** da
  atividade escolhida, com as mesmas recusas em linguagem simples da equipe da aula.
- O **Mestre presente homologa ali mesmo**, sob a sessão de trabalho do aparelho — revoga o
  que a fatia 7 escreveu, que mandava homologar na App 09.
- A equipe **entrega a produção** por texto, fala ou foto do manuscrito e lê a devolutiva na
  tela. Quem recusa foto e áudio entrega por texto, sem perder a missão.

## Capabilities

### New Capabilities

- `producao-da-missao`: a entrega da produção pela equipe, a devolutiva construtiva que não
  credita ponto e o descarte de foto e áudio na leitura.

### Modified Capabilities

- `equipe`: as duas rotas HTTP da equipe da trilha — criação pelo Guerreiro(a) e homologação
  pelo Mestre — e a trilha em cada item da programação do encontro.
- `aplicacao-da-aula-presencial`: a App 01 passa a formar a equipe da trilha e a oferecer a
  homologação ao Mestre em sessão de trabalho — **BREAKING**: o requisito que hoje a proíbe é
  removido, e a metade dele que continua valendo (a gestão não forma equipe, `RN-04-18`) passa
  para o requisito da homologação — e ganha a tela da entrega da produção com a devolutiva.

## Impact

- `backend/src/nucleo/equipes/rotas.py`: duas rotas novas; `trilha_id` e `trilha_titulo` no
  item da programação.
- `backend/src/nucleo/producoes/` (novo): `modelo.py`, `regra.py`, `rotas.py`, `porta.py`,
  `local.py`, `nuvem.py` e `fabrica.py` — a porta da devolutiva no mesmo padrão de
  `template_de_missao` (local fora de produção, Gemini em produção).
- `backend/src/nucleo/permissoes.py`: operação nova da produção da equipe.
  `homologacao_da_equipe_da_trilha` já está na matriz e **não muda**.
- `backend/alembic/`: **uma migração** — a tabela nova.
- `apps/app-01-aula-presencial/src/trilhas/` e `src/api/`: formação da equipe da trilha,
  homologação pelo Mestre e entrega da produção.
- Documentação: documento 03 §4.2 (documento-fonte da decisão), documento 09 §1, PRD-04 §§8,
  9 e 13, PRD-05 §8 (a entidade ganha a equipe) e `openspec/cronograma-de-fatias.md`. O
  documento 99 **não muda** — nenhuma relação entre documentos se altera. `docs/prds/index.md`
  **não muda** — o PRD-04 segue "aprovado".

## Fora do escopo

Reproduz o que o PRD-04 §3.2 já exclui, e o que estas duas fatias deixam para depois:

- **Assistente de trilhas** (`RF-04-36` a `RF-04-40`, `RN-04-19` a `RN-04-21`): fatia 10.
- **Fila local sem rede** (`RF-04-23` a `RF-04-25`, `RN-04-13`): fatia 11.
- **Aviso de coleta e encerramento do cadastro** (`RF-04-26`, `RF-04-27`): fatia 12.
- **Porta individual da produção** (`RF-05-74` a `RF-05-78`) e **retomada** (`RF-05-79`,
  `RF-05-80`): fatia 7 do PRD-05.
- **Lançamento do resultado pelo Mestre**: já é de `resultado-de-atividade`; esta fatia só
  garante que a devolutiva não o antecipa.
- **Desafio de desbloqueio** e qualquer estado de progressão de missão.
- **Criação original em equipe da trilha** (`RF-05-40`, `RF-05-41`): já entregue na fatia 5 do
  PRD-05; esta fatia só lhe dá o sujeito que faltava.
- **Guarda de foto e áudio**: não há. Nenhum dos dois é persistido, em lugar algum.
