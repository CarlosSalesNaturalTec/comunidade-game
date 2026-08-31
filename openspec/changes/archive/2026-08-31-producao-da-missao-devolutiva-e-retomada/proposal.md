# Produção da missão, devolutiva e retomada

Fatia 7 do **PRD-05 — Área do Guerreiro(a)**.

Atende `RF-05-74` a `RF-05-80`, sob `RN-05-05` e `RN-05-35` a `RN-05-38`.

## Why

A jornada §5.3 do PRD-05 termina em três passos que ainda não existem para o Guerreiro(a)
sozinho: **entregar a produção**, **receber a devolutiva construtiva** e **rever a missão na
retomada** que o Mestre agendou. As fatias 1 a 6 entregaram o percurso, o desbloqueio, a
coleta, a carteira, a criação original e os desafios em aberto — a missão abre, o conteúdo é
lido, o desbloqueio é submetido, e aí a tela acaba.

A entidade `ProducaoDaMissao` já está de pé desde a fatia 9 do PRD-04, com `guerreiro_id`
reservado exatamente para esta fatia (PRD-05 §8), mas só a **equipe** entrega, pelo App 01,
`POST /v1/equipes/{id}/producao`. As duas rotas da §9 do PRD que faltam —
`POST /v1/eu/missoes/{id}/producao` e `GET /v1/eu/retomadas` — seguem sem implementação, e a
App 05 não tem nem a tela de entrega nem a de retomadas.

Sem esta fatia o `RN-05-35` fica sem cumprimento na App 05: toda atividade exige produção do
Guerreiro(a), e hoje quem estuda sozinho não tem por onde entregá-la.

### Decisões de recorte levadas ao fundador

Duas ambiguidades do recorte foram ao fundador antes da redação:

1. **Onde vive o "a retomada pontua uma vez por agendamento"** (`RF-05-80`, `RN-05-38`), já
   que o `RN-05-05` reserva o nascimento do ponto ao `Resultado` lançado pelo Mestre. O
   fundador decidiu: **só na App 05**. A retomada aparece em `GET /v1/eu/retomadas` enquanto
   o agendamento está aberto e sai da lista quando o Guerreiro(a) entrega a produção dele;
   refazer por conta própria segue possível pela tela da missão, mas nunca reabre um
   agendamento nem aparece como retomada. Nenhuma trava nova no `Resultado`, nenhuma coluna
   nova, nenhuma migração.
2. **Quem é "quem recusa foto ou áudio"** no `RF-05-78`. O fundador decidiu: **a criança, na
   hora da entrega**. As três formas seguem sempre oferecidas, e quem não quiser fotografar
   nem gravar escolhe texto ou o caminho "entrego ao Mestre no encontro", apresentado com o
   mesmo destaque. Nenhuma consulta a consentimento entra nesta fatia, e a porta individual
   fica com a mesma superfície da porta de equipe já entregue.

## What Changes

**Núcleo**

- `POST /v1/eu/missoes/{id}/producao` (PRD-05 §9): a entrega **individual** da produção, em
  texto, áudio ou foto do manuscrito, sobre a `ProducaoDaMissao` que já existe — desta vez com
  `guerreiro_id` preenchido e `equipe_id` em branco (`RF-05-74`). A leitura descarta foto e
  áudio e grava só transcrição e devolutiva (`RF-05-76`, `RN-05-36`), e a devolutiva é o mesmo
  retorno construtivo da porta de equipe (`RF-05-75`), que **não credita ponto algum**
  (`RF-05-77`, `RN-05-05`).
- `GET /v1/eu/retomadas` (PRD-05 §9): as missões que voltaram para revisão espaçada, com o
  prazo de cada agendamento, derivadas da `cadencia_de_retomada` que o Mestre declarou na
  missão e do momento do desbloqueio do Guerreiro(a) (`RF-05-79`). O agendamento já atendido
  por uma produção dele sai da lista (`RF-05-80`, `RN-05-38`).
- Nenhuma migração de esquema e nenhuma rota de crédito de pontos: quem lança o resultado
  segue sendo o Mestre (`RN-05-05`, `RN-05-35`).

**App 05 — Área do Guerreiro(a)**

- Tela de **entrega da produção** dentro da missão: escrever, gravar a fala ou fotografar o
  que fez à mão (`RF-05-74`), com o aviso, antes de enviar, de que a foto e o áudio são
  descartados na leitura (`RF-05-76`).
- A **devolutiva** é exibida como retorno construtivo, apontando o próximo passo (`RF-05-75`),
  e a tela diz, na mesma altura, que ela **não vale ponto** e que o resultado fica "aguardando
  lançamento" até o Mestre (`RF-05-77`).
- Caminho **"entrego ao Mestre no encontro"** com o mesmo destaque das outras formas: quem não
  quer ser fotografado nem gravado não perde a missão e a tela diz isso (`RF-05-78`,
  `RN-05-37`).
- Bloco de **retomadas**: as missões que voltaram, com o prazo de cada uma e a explicação de
  que rever fixa (`RF-05-79`). Entregue a produção da retomada, ela sai da lista; refazer por
  conta própria segue aberto pela tela da missão, dito na tela que não rende ponto novo
  (`RF-05-80`).

### Fora do escopo

Reproduz o que o PRD já exclui (PRD-05 §3.2), sem exclusão nova:

- **Lançamento de resultado, presença ou mérito** — é ato do Mestre ou do Admin (`RN-05-06`).
- **Declaração da cadência de retomada** — é da App 09, entregue (`RF-09-83`, `RF-09-101`).
- **Desafio extra na Área do Guerreiro(a)** (`RF-05-20`, `RF-05-21`) — é a fatia 8.
- **Apoio escolar por assistente de voz**, canal de sugestões e acervo — Ciclo 02.
- Qualquer medição, cota ou lançamento do consumo do modelo — o custo é recurso de nuvem, na
  régua que a porta de equipe já fixou (`RF-09-90`).

## Capabilities

### New Capabilities

Nenhuma. O recorte estende capacidades que já existem.

### Modified Capabilities

- `producao-da-missao`: a entrega passa a ter **duas portas** — a da equipe, que já existe, e
  a **individual** do Guerreiro(a) em sessão sobre uma missão do próprio percurso. Descarte de
  mídia, devolutiva sem crédito e desfecho da leitura indisponível valem igual nas duas.
- `area-do-guerreiro`: as retomadas em aberto do Guerreiro(a) passam a ser derivadas e
  alcançáveis por HTTP, e a App 05 ganha a entrega da produção, a exibição da devolutiva, o
  caminho da recusa de foto e áudio e o bloco das retomadas.

## Impact

- `backend/src/nucleo/producoes/` — `regra.py` (a entrega individual, ao lado da de equipe) e
  `rotas.py` (`POST /v1/eu/missoes/{id}/producao`).
- `backend/src/nucleo/trilhas/` — `regra.py` (derivação das retomadas em aberto) e `rotas.py`
  (`GET /v1/eu/retomadas`).
- Nenhuma migração de esquema: `ProducaoDaMissao` já admite `guerreiro_id`, e a
  `cadencia_de_retomada` já está na `Missao`.
- `apps/app-05-guerreiro/src/trilha/` — entrega da produção, devolutiva e retomadas; e
  `src/api/trilha.ts`.
- Documentação: a linha da fatia 7 em `openspec/cronograma-de-fatias.md` — situação e slug.
