# Proposal

## Why

Fatia **25 do PRD-09** (`openspec/cronograma-de-fatias.md`). Atende `RF-09-127`, `RF-09-128`,
`RN-09-47`, `RN-09-48` e `RN-09-49`, as cinco entradas que as decisões do fundador de
2026-10-27 criam no PRD-09 §§6.1 e 7.

A atividade da missão é rua de mão única, como o conteúdo era até a fatia 24. O núcleo só sabe
criar (`POST /v1/missoes/{id}/atividades`); não há `PATCH` nem `DELETE`. Na App 09 o bloco
Atividades imprime `titulo — modalidade / formato` com os valores crus do enum e oferece um
botão só: "Nova atividade". Título trocado, modalidade errada ou produção esperada mal
redigida são permanentes, e o único caminho de correção é acrescentar outra atividade ao lado
da errada — que o Guerreiro(a) também vê, e para a qual o Mestre também vai ter de lançar
Resultado.

A falta pesa mais aqui que no conteúdo, por três motivos.

**A atividade é a porta do ponto.** Ela é o que o Guerreiro(a) realiza e de onde nascem o
`Resultado` e o ponto regular. Atividade errada não é texto feio na tela: é lançamento errado,
e `RF-09-47` veda editar ou remover Resultado gravado. Quem erra o enunciado da atividade hoje
não tem como consertar nem como tirá-la do caminho.

**Cinco tabelas apontam para `atividade`** — `resultado`, `producao_da_missao`,
`partida_de_quiz`, `ocorrencia_de_conduta` e `equipe.atividade_corrente_id`. Apagar a linha de
verdade, como a fatia 24 pôde fazer com o conteúdo, aqui levaria consigo o fato gravado ou o
deixaria órfão. É a mesma situação que `remover_pergunta_do_desbloqueio` já resolveu
carimbando: a pergunta sai da leitura e permanece guardada, porque a tentativa registrada
aponta para ela (`RN-05-47`).

**A atividade existe em estado vivo.** Diferente do conteúdo, ela é escolhida pela equipe no
encontro (`equipe.atividade_corrente_id`) e pode ter uma Partida de Quiz **aberta** correndo
sobre ela. Remover sem olhar isso deixaria o painel do dia anunciando missão corrente de
atividade que não existe mais, ou derrubaria uma partida no meio para a turma.

## What Changes

As duas decisões do fundador de 2026-10-27, mais as duas elicitadas na abertura desta change,
entram no documento 03 §11, no documento 09 §1 e no PRD-09 §§6.1, 7 e 9 antes de virar código
(§ *Impact*).

- **Nasce `PATCH /v1/atividades/{id}`** (`RF-09-127`), privativo do **Mestre autor** da trilha
  a que a missão da atividade pertence, alcançando **título**, **descrição**, **modalidade**,
  **formato** e **produção esperada**. Autoria **estrita**, como a fatia 24 fixou para o
  conteúdo: a criação aceita o Admin, a correção não — ele audita e despublica a trilha, não a
  redige.
  As recusas da criação valem na correção: título vazio, modalidade ou formato fora dos
  valores previstos e produção esperada vazia respondem **422**.
- **A `natureza` fica fora** (`RN-09-49`), no espelho do que `RN-09-45` fixou para o tipo do
  conteúdo. Ela não é rótulo: o núcleo exige `natureza == competição ao vivo` para abrir
  Partida de Quiz e concede o badge de valores e causas quando a natureza é essa. Corrigi-la
  desmancharia a partida já corrida e mudaria o badge dos lançamentos seguintes. Trocar a
  natureza é remover a atividade e cadastrar outra. Decisão do fundador, 2026-10-27.
- **Corrigir o `formato` para fora do presencial limpa a `aula_id`** (`RN-09-48`): atividade
  on-line com aula declarada é exatamente o estado que `criar_atividade` já recusa na criação,
  e deixá-lo nascer pela correção seria abrir pela porta de trás o que a porta da frente
  barra. A aula **não** é campo do `PATCH` — declará-la segue sendo da criação.
- **Nasce `DELETE /v1/atividades/{id}`** (`RF-09-128`), privativo do Mestre autor, que
  **carimba** a atividade em vez de apagá-la (`RN-09-47`): ela sai de toda leitura de autoria
  e de execução, e os quatro fatos que a apontam — `resultado`, `producao_da_missao`,
  `partida_de_quiz` e `ocorrencia_de_conduta` — seguem intactos e seguem resolvendo a
  atividade que nomeiam. Ponto já creditado não se estorna: `RF-09-47` veda.
- **O estado vivo é tratado, não ignorado.** O carimbo **zera `atividade_corrente_id`** das
  equipes que apontavam a atividade — o painel do dia deixa de anunciar missão corrente que
  não existe mais — e é **recusado com 422** enquanto houver Partida de Quiz **aberta** sobre
  ela: partida em curso se encerra antes, não se apaga por baixo da turma. Decisão do
  fundador, 2026-10-27.
- **As duas rotas recusam a atividade avulsa.** `/v1/atividades/{id}` com `poder_id` — o
  cadastro da gestão, que é do Admin pela App 03 (`RF-02-29`) — responde **422**: esta fatia é
  da atividade de trilha, e a avulsa tem matriz de permissão, campos obrigatórios e âncora de
  ponto próprios.
- **Nasce `GET /v1/atividades/{id}/fatos`**, que devolve quantos fatos já apontam para a
  atividade e se há partida aberta — é o que a tela diz ao Mestre **antes** de confirmar a
  remoção (`RF-09-128`). Leitura sob demanda, no espírito de `RN-09-46`: contar cinco tabelas
  por atividade dentro de `GET /v1/trilhas/minhas` faria cada abertura da tela da trilha pagar
  a conta de uma remoção que quase nunca acontece.
- **O bloco Atividades da App 09 ganha corrigir e remover** (`RF-09-127`, `RF-09-128`), com o
  rótulo da modalidade e do formato em português — hoje a linha imprime `em_equipe_com_familiar
  / on_line_assincrona` ao Mestre, enquanto o formulário logo abaixo já tem os dois dicionários
  de rótulo. A remoção é confirmada depois de a tela dizer quantos fatos apontam.
- Toda leitura de autoria e de execução passa a ignorar a atividade carimbada: a trilha do
  Mestre e a pública, os semanais do Guerreiro(a) (`RF-05-19`), a programação do encontro e as
  atividades da equipe (`RF-04-35`), e nenhum fato novo — Resultado, produção, partida ou
  ocorrência — passa a apontá-la.

**Fora do escopo.** O **lançamento** já gravado não se edita nem se remove (`RF-09-47`), e
nenhum ponto, badge ou nível é estornado pela remoção da atividade — a correção de lançamento
é ajuste que referencia o original, e não é desta fatia. Seguem fora, como o PRD-09 §3.2 já
exclui, a **atividade avulsa** da gestão (`RF-02-29`, PRD-02) e a trilha de auditoria das
escritas do Mestre (`RF-09-48`), que foi ao Ciclo 02.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `atividade-de-trilha`: a atividade passa a se corrigir em título, descrição, modalidade,
  formato e produção esperada; a natureza não se altera; corrigir o formato para fora do
  presencial limpa a aula; a remoção carimba, zera a escolha corrente das equipes, é recusada
  com partida aberta e tira a atividade de toda leitura de autoria e de execução, sem que
  nenhum fato novo possa apontá-la.
- `area-do-mestre`: o bloco Atividades corrige e remove cada atividade, diz quantos fatos
  apontam para ela antes de confirmar e passa a nomear modalidade e formato em português.
- `equipe`: a programação do encontro e as atividades da equipe deixam de trazer atividade
  carimbada, a escolha corrente não a aceita e a escolha já declarada é zerada quando ela é
  removida.
- `area-do-guerreiro`: os semanais deixam de trazer atividade carimbada — hoje a subtração é
  só pelo Resultado lançado, e atividade removida sem Resultado nunca sairia da lista.

## Impact

- `backend/src/nucleo/trilhas/modelo.py` — `Atividade.removida_em`, a coluna do carimbo, no
  molde de `PerguntaDoDesbloqueio.substituida_em`.
- `backend/src/nucleo/trilhas/regra.py` — `corrigir_atividade` e `remover_atividade`, com a
  guarda de posse que `criar_atividade` já aplica, a recusa da avulsa, a limpeza da `aula_id`,
  a recusa por partida aberta e a limpeza do `atividade_corrente_id`; `fatos_da_atividade`, que
  conta as cinco tabelas; e o filtro do carimbo em `desafios_em_aberto_do_guerreiro`.
- `backend/src/nucleo/trilhas/rotas.py` — `PATCH`, `DELETE` e `GET .../fatos` de
  `/atividades/{id}`, e o filtro do carimbo nas duas leituras que aninham atividades na missão.
- `backend/src/nucleo/equipes/regra.py` — o filtro do carimbo em `atividades_disponiveis` e
  `atividades_da_equipe`, e a recusa em `declarar_escolha_da_equipe`.
- `backend/src/nucleo/painel_do_dia/regra.py` — o filtro do carimbo em `_atividades_previstas`,
  que repete a mesma programação do encontro que a equipe lê.
- `backend/src/nucleo/resultados/regra.py`, `producoes/regra.py`, `quiz/regra.py` e
  `ocorrencias_de_conduta/regra.py` — a recusa de fato novo sobre atividade carimbada.
- `backend/alembic/versions/` — revisão que acrescenta `removida_em` a `atividade`.
- `apps/app-09-mestre/src/trilhas/api.ts` — as três chamadas novas.
- `apps/app-09-mestre/src/trilhas/FormularioDeAtividade.tsx` — passa a servir criação **e**
  correção, com os dois dicionários de rótulo exportados para a lista usar.
- `apps/app-09-mestre/src/trilhas/ListaDeMissoes.tsx` — o bloco Atividades com rótulo em
  português, editar e remover, com a contagem dos fatos na confirmação.
- Documentação, no mesmo PR: documento 03 §11 (marcador novo), documento 09 §1 (a linha da
  decisão), PRD-09 §6.1 (os dois `RF`), §7 (as três `RN`) e §9 (as três rotas), e a situação
  da fatia 25 no `openspec/cronograma-de-fatias.md`.
