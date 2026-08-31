## Why

Origem: **PRD-04** (App 01 — aula presencial), §§5.5, 5.6, 5.8, 6.1, 6.2, 8, 9, 11 e 13.
Fatias **10**, **11** e **12** do `openspec/cronograma-de-fatias.md`, numa change só (fundador,
2026-08-30). Atende `RF-04-36` a `RF-04-40`, `RN-04-19` a `RN-04-21` (fatia 10); `RF-04-23` a
`RF-04-25`, `RN-04-13` (fatia 11); `RF-04-26` e `RF-04-27` (fatia 12).

Nove fatias puseram a criança no encontro e a equipe diante da trilha: ela se cadastra, entra
por reconhecimento, forma equipe, lê a programação, joga o Quiz ao Vivo, entrega a produção e
troca pontos extras. Faltam as três coisas que fecham o App 01 e que nenhuma outra aplicação
faz por ele:

- O **assistente de trilhas** — o terceiro verbo do caminho das trilhas, ao lado de ler e
  produzir. Sem ele, a equipe que não entende um conceito só tem a fila do Mestre; e a
  entidade `ConsultaAoAssistente`, declarada no PRD-04 §8, **não existe no núcleo**.
- A **fila local**. A aplicação já reconhece a queda de rede tela a tela — quiz e programação
  —, mas a **presença**, o único fato que o PRD manda enfileirar, hoje se perde: quem chega
  com a rede fora não entra na aula.
- O **aviso de coleta** e o **encerramento da conversa**. A App 01 coleta dado de criança em
  toda tela do onboarding e não diz, em lugar nenhum, o que coleta nem para onde vai; e a
  conversa acaba sem dizer à criança como ela entra da próxima vez.

## What Changes

### Decisões do fundador, 2026-08-30

**O corpus do assistente é a missão corrente e as já percorridas.** O documento 03 §4.2 diz
"corpus fechado no conteúdo que os Mestres cadastraram" sem recortar quais missões. O
assistente responde a partir do conteúdo da **missão da atividade corrente da equipe** e das
**missões anteriores da mesma trilha** — o que a equipe já percorreu. Missão à frente na
trilha fica fora: adiantá-la contornaria o desbloqueio. As alternativas foram descartadas —
só a missão corrente recusaria conceito de missão anterior que a equipe legitimamente retoma,
e a trilha inteira entregaria conteúdo ainda bloqueado. Entra no documento 03 §4.2 e no
PRD-04 §13.

**O registro que falha na sincronização fica no aparelho, nesta fatia.** O PRD-04 §5.6.5 quer
a falha como pendência do painel do dia, mas nenhum `RF` a enuncia e a fila local é estado do
aparelho, que o núcleo nunca vê: listá-la no painel exigiria requisito e rota novos. Nesta
fatia a App 01 mostra ao **Mestre presente** o que ainda está na fila e o que falhou. A
`§5.6.5` vira pendência no documento 09 §1.

**A resposta do assistente sai sem a etiqueta de IA nesta fatia.** O documento 03 §7.1 exige
etiqueta visível com link para a **nota de transparência da vitrine**, que é do PRD-03 e ainda
não existe. A etiqueta inteira — texto e link — fica para a fatia que entregar a nota. Vira
pendência no documento 09 §1.

### Núcleo — consulta ao assistente (fatia 10)

- Nasce a entidade **`ConsultaAoAssistente`** — equipe **ou** Guerreiro(a), assistente
  (trilhas ou apoio escolar), transcrição da pergunta e da resposta, momento —, como o PRD-04
  §8 a declara. Nesta fatia só o assistente **de trilhas** a escreve, pela equipe; o apoio
  escolar da App 05 é do Ciclo 02 e reusa a mesma entidade.
- Nasce `POST /v1/assistente/trilhas/consultas` (PRD-04 §9), do **Guerreiro(a) em sessão** e
  restrita a **integrante da equipe**, aceitando a pergunta por **texto ou áudio**.
- A resposta vem **apenas do corpus** montado a partir do conteúdo daquelas missões
  (`RF-04-36`, `RN-04-19`). Pergunta fora dele recebe **recusa explicada** com a orientação de
  procurar um Mestre no encontro — 200, no corpo, como o PRD-04 §9 define (`RF-04-37`).
  Pergunta de **tarefa escolar** recebe o encaminhamento à App 05, sem resposta aqui
  (`RF-04-38`).
- O **áudio da pergunta é descartado assim que transcrito** e nunca é persistido; guarda-se a
  transcrição da pergunta e a da resposta (`RF-04-40`, `RN-04-21`) — o mesmo desenho de
  `producao-da-missao`.

### App 01 — assistente (fatia 10)

- O caminho das trilhas ganha a **tela do assistente**, alcançável da programação, com pergunta
  por **texto** e por **voz**. O microfone abre por ação do Guerreiro(a) e **fecha ao fim da
  fala**: não há captação do áudio ambiente (`RF-04-39`, `RN-04-20`).
- A conversa fica **na tela, na sessão do atendimento**, e some com ele — o aparelho é
  compartilhado.
- **Sem rede o assistente fica indisponível**, dito em uma frase, sem enfileirar pergunta
  alguma (`RF-04-58`).

### App 01 — fila local (fatia 11)

- A aplicação **avisa na tela que está sem conexão** e, com a rede fora, a presença confirmada
  pelo Mestre ou Admin **entra na fila local** em vez de se perder (`RF-04-23`).
- **Cadastro novo e reconhecimento facial ficam indisponíveis** sem rede, com aviso na tela: o
  descritor nasce no aparelho, mas a comparação é no núcleo (`RF-04-24`).
- Voltando a rede, a fila **sincroniza sozinha, preservando a hora do fato** e sem duplicar
  registro reenviado — o núcleo já devolve o registro existente sem erro (`RF-04-25`,
  `RN-04-13`).
- A fila guarda **apenas presença**, nunca imagem nem descritor, e é descartada assim que
  sincroniza (`RN-04-12`, PRD-04 §8). O que falhar fica visível ao Mestre presente.

### App 01 — aviso de coleta e encerramento (fatia 12)

- A **tela inicial** e a **tela de captura** passam a trazer o aviso discreto do que a
  aplicação coleta, com caminho para a **área detalhada de direitos** (`RF-04-26`, PRD-04 §11).
- A área detalhada diz, em linguagem de criança, o que se coleta, para que serve, por quanto
  tempo fica e quem acessa, e que **pedido de acesso, correção ou exclusão é do responsável,
  pela App 07, com resposta em 7 dias** — a aplicação não os atende (PRD-04 §11).
- A conversa do onboarding **encerra dizendo como o Guerreiro(a) entra da próxima vez**:
  por nick e imagem quem capturou, por confirmação do Mestre quem ficou sem imagem
  (`RF-04-27`, `RN-04-09`).

## Capabilities

### New Capabilities

- `consulta-ao-assistente`: a consulta ao assistente de trilhas — corpus fechado do conteúdo
  das missões percorridas, recusa explicada fora dele, encaminhamento da tarefa escolar à
  App 05, e a guarda só da transcrição.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: a tela do assistente no caminho das trilhas; a fila local de
  presença, com o aviso de operação sem conexão e o bloqueio de cadastro e reconhecimento; o
  aviso de coleta com a área detalhada de direitos; e o encerramento da conversa do onboarding.

## Impact

- `backend/src/nucleo/assistente/` (novo): `modelo.py`, `regra.py`, `rotas.py`, `porta.py`,
  `local.py`, `nuvem.py` e `fabrica.py` — a porta do assistente no mesmo padrão de
  `producoes` e `template_de_missao` (local fora de produção, Gemini em produção).
- `backend/src/nucleo/permissoes.py`: operação nova da consulta ao assistente.
- `backend/alembic/`: **uma migração** — a tabela nova.
- `apps/app-01-aula-presencial/src/`: tela do assistente em `trilhas/`, fila local e aviso de
  conexão no `sessao-de-trabalho/` e no `onboarding/`, aviso de coleta e área detalhada, e o
  encerramento da conversa.
- Documentação: documento 03 §4.2 (recorte do corpus), documento 09 §1 (a decisão do corpus e
  as duas pendências novas), PRD-04 §§8, 9, 13 e 14, e `openspec/cronograma-de-fatias.md`. O
  documento 99 **não muda** — nenhuma relação entre documentos se altera. `docs/prds/index.md`
  **não muda** — o PRD-04 segue "aprovado".

## Fora do escopo

Reproduz o que o PRD-04 §3.2 já exclui, e o que estas três fatias deixam para depois:

- **Apoio escolar** (`RF-05-58` a `RF-05-70`): é da App 05 e do Ciclo 02. Aqui só existe o
  encaminhamento — a pergunta escolar não é respondida no App 01 (`RF-04-38`).
- **Etiqueta de IA e nota de transparência**: fatia do PRD-03 que entregar a nota da vitrine.
- **Pendência da sincronização no painel do dia** (PRD-04 §5.6.5): pendência do documento 09.
- **Personalização por IA que perfila**: não existe. O assistente adapta na sessão e nada
  infere nem guarda sobre a criança (documento 03 §7.1).
- **Fila local de qualquer outro fato**: a fila guarda só presença. Resposta de quiz, produção,
  troca, cadastro e consulta ao assistente **nunca** são enfileirados.
- **Guarda do áudio**: não há. Nem o da pergunta ao assistente, nem o da produção.
- **Auditoria por amostragem da reescrita** (documento 03 §7.1): não tem `RF` no PRD-04.
