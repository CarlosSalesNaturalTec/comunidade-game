## Why

Origem: **PRD-04** (App 01 — aula presencial), §6.2, jornada 5.8. Atende `RF-04-35`, e no
que a decisão nova alcança a autoria, `RF-09-42`, `RF-09-69` e `RF-09-73` do **PRD-09**.

Cinco fatias puseram a criança dentro do encontro — ela se cadastra, entra por reconhecimento,
forma equipe, joga o Quiz ao Vivo e troca pontos extras. A sexta deu à missão o que ensinar
(`conteudo-e-bibliografia-da-missao`). Falta o momento 5 do encontro, o "grosso do encontro"
do documento 05 §4: a equipe abrir o aparelho e ver **em que missão está, o conteúdo e a
atividade do dia**. Sem ele o App 01 não sustenta a autonomia que o encontro assíncrono
pressupõe, e o Mestre volta a ser quem diz a cada equipe o que fazer.

A rota que o PRD-04 §9 já prevê — `GET /v1/equipes/{id}/missao` — **não tem de onde
responder**. A `Aula` declara comunidade, ponto de apoio, data, horários, recursos e situação,
e nada sobre trilha, missão ou atividade; a `Atividade` pertence a uma missão e não conhece
encontro algum. A leitura "suas turmas" (`RF-09-42`) hoje devolve as aulas do Mestre **e** as
atividades dele lado a lado, sem vínculo declarado entre as duas — é junção por comunidade e
autoria, não programação de encontro.

## What Changes

**Decisão nova do fundador, 2026-08-25: o Mestre autor declara, na sua atividade, a aula em
que ela acontece.** É o vínculo que faltava, e nasce no documento-fonte antes de virar código.
A alternativa — a aula declarar a trilha — foi descartada: quem agenda a aula é Admin
(`RF-01-20`), e a atividade é do Mestre autor (`RF-01-16`); pôr a programação na aula tiraria
do autor a decisão sobre a própria atividade.

**Núcleo:**

- A `Atividade` passa a declarar, **opcionalmente**, a **aula** em que acontece. Atividade
  on-line e assíncrona segue sem aula; é o vínculo que torna concreto o "presenciais **do
  encontro**" que o `RF-09-73` já pedia. Só o **Mestre autor** da trilha o declara, pela
  matriz de posse que já vale para trilha, missão e atividade (`RF-01-16`).
- Nasce `GET /v1/equipes/{id}/missao`, do **Guerreiro(a) em sessão** e restrita a **integrante
  daquela equipe**. Devolve a **programação do encontro**: todas as atividades presenciais
  vinculadas à aula da equipe, cada uma com a sua missão, o conteúdo e a bibliografia
  (`RF-04-35`).
- **A programação é lista, e a equipe escolhe** (fundador, 2026-08-25). O encontro do documento
  05 §4 tem vários Mestres e várias trilhas ao mesmo tempo, e cada equipe avança no seu ritmo:
  uma atividade por aula seria camisa de força, e uma atividade escolhida pela equipe seria
  estado numa equipe que morre com a aula (documento 02 §5). Nada de estado novo.
- A leitura "suas turmas" passa a trazer, em cada atividade, a aula que ela declarou
  (`RF-09-42`, `RF-09-73`).

**App 09 — o Mestre declara:** `FormularioDeAtividade` ganha a escolha da aula, alimentada
pelas turmas que o Mestre já lê. Campo opcional, oferecido no formato presencial.

**App 01 — a equipe consome:** o **caminho das trilhas** da tela inicial, que hoje leva só à
formação de equipe, passa a levar da equipe escolhida à programação do encontro — missão,
conteúdo, bibliografia e atividade do dia. Sem rede, o conteúdo já carregado continua legível
(`RF-04-58`, na parte que é desta fatia).

## Capabilities

### New Capabilities

Nenhuma. As quatro capacidades tocadas já existem.

### Modified Capabilities

- `atividade-de-trilha`: a atividade declara, opcionalmente, a aula em que acontece, e só o
  Mestre autor da trilha o faz.
- `equipe`: a rota da programação do encontro, servida ao integrante da equipe em sessão.
- `aula-e-presenca`: a leitura "suas turmas" traz a aula declarada em cada atividade.
- `aplicacao-da-aula-presencial`: o caminho das trilhas mostra a programação do encontro à
  equipe, e o conteúdo já carregado sobrevive à queda de rede.

## Impact

- `backend/src/nucleo/trilhas/modelo.py`, `regra.py` e `rotas.py`: coluna `aula_id` na
  `Atividade`, guarda de autoria e saída.
- `backend/src/nucleo/equipes/rotas.py` e `regra.py`: rota nova da programação.
- `backend/src/nucleo/aulas/regra.py`: a leitura de turmas passa a trazer a aula da atividade.
- `backend/alembic/`: **uma migração** — coluna nova, anulável, sem preencher registro antigo.
- `backend/src/nucleo/permissoes.py`: **não muda**. O Guerreiro(a) lê a própria equipe e a
  trilha publicada pelas operações que já tem.
- `apps/app-09-mestre/src/trilhas/FormularioDeAtividade.tsx` e `api.ts`.
- `apps/app-01-aula-presencial/src/trilhas/` (novo), `src/inicio/`, `src/api/`.
- Documentação: o documento-fonte da decisão (documento 05 §4), o documento 09, o PRD-04 §9
  no contrato da rota, o PRD-09 §6.6 e `docs/prds/index.md`. O documento 99 não muda — a
  relação entre documentos é a mesma.

## Fora do escopo

Reproduz o que o PRD-04 §3.2 já exclui, e o que a fatia deixa para depois:

- **Desafio de desbloqueio** (`RF-09-26`) e **qualquer estado de progressão de missão**. O
  fundador ainda não decidiu se o desbloqueio é fato do Guerreiro(a) na trilha ou da equipe; a
  capacidade `pontos-niveis-e-badges` hoje deriva nível de Resultado registrado por
  Guerreiro(a), e esta fatia **não toca** nisso.
- **Entrega da produção da missão e devolutiva** (`RF-04-45` a `RF-04-47`).
- **Assistente de trilhas** (`RF-04-36` a `RF-04-40`).
- **Fila local sem rede** (`RF-04-23` a `RF-04-25`) e captura de quem se cadastrou sem imagem
  (`RF-04-16`).
- **Painel do dia da App 03** (`RF-02-08`, `RF-02-41` a `RF-02-49`, `RF-02-69`). Ele consome o
  que esta fatia cria — `RF-02-42` e `RF-02-44` —, mas não existe ainda: entra inteiro na
  fatia dele, não pela metade (fundador, 2026-08-25).
