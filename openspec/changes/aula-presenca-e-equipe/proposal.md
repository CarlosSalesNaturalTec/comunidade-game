## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Nona fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-20` (parcial — `Aula/Agenda`, `Presenca` e `Equipe`),
`RF-01-32`, `RF-01-37`, `RF-01-38`, `RF-01-39` (parcial — a metade das várias equipes da
aula), `RF-01-03`, `RF-01-16`, `RF-01-18`.

A aula agendada é a dependência que a oitava fatia nomeou ao adiar `RF-01-36` a `RF-01-39`, e
é o que falta para fechar `RF-01-20`: trilha, missão, atividade e resultado já entregues,
`Aula/Agenda`, `Presenca` e `Equipe` ainda não. A matriz de permissões guarda quatro assentos
vazios desde a segunda fatia — `equipe_que_forma_na_aula`, `resposta_de_quiz_da_equipe`,
`equipes_da_aula_em_andamento` e `conducao_do_quiz_ao_vivo_das_suas_aulas` —, e esta fatia
ocupa os dois primeiros que dependem só da equipe.

Nenhuma pendência da §14 do PRD-01 nem do documento 09 §1 alcança este recorte: *Formação das
equipes*, *Equipes*, *Aplicação de cada tipo de aula*, *Comunidade do onboarding* e *App 01
com a rede fora* estão todas em "Já decididos".

## What Changes

### Aula agendada

- Nasce a **Aula/Agenda**, com comunidade, data, horário inicial e final (PRD-01 §8). É dela
  que sai a comunidade do cadastro novo e é a existência dela que habilita o onboarding —
  não há parâmetro de liberação separado.
- Nasce a **derivação das aulas vigentes**: as aulas cuja data e faixa de horário contêm o
  momento corrente (`RF-01-32`). Havendo aulas de comunidades diferentes no mesmo horário, a
  derivação devolve todas — quem escolhe é o App 01, ao abrir (documento 09, *Comunidade do
  onboarding*).
- A escrita da aula é do **Admin**: PRD-01 §4 dá a ele os cadastros, e o Mestre lê o painel
  do dia sem escrever em gestão (`RF-01-17`, já na matriz). Nenhuma entrada nova na matriz.

### Presença

- Nasce a **Presença**: quem esteve na aula, com o modo de comprovação — reconhecimento ou
  confirmação de Mestre ou Admin — e o registro de quem confirmou (`RF-01-20`, `RF-01-03`),
  no mesmo desenho que a sessão do Guerreiro(a) já usa desde a terceira fatia.
- A presença é **única por aula e Guerreiro(a)**: o reenvio do App 01 depois de operar com a
  rede fora não duplica o registro (PRD-01 §10, escrita tolerante a rede instável; documento
  09, *App 01 com a rede fora*).

### Equipe

- Nasce a **Equipe**, presa a exatamente uma aula e criada pelo próprio Guerreiro(a), que
  entra como primeiro integrante (`RF-01-37`).
- A equipe **encerra com a aula e não é reaproveitada**: equipe de uma aula não aparece em
  outra (`RF-01-37`).
- O núcleo **recusa o sexto integrante** e o **segundo integrante de 17 anos ou mais** na
  mesma equipe (`RF-01-38`). Como a faixa do Guerreiro(a) é 6–16 (invariante 2), o integrante
  de 17 anos ou mais é o que **não tem papel de Guerreiro(a)** — o núcleo não guarda data de
  nascimento, e a leitura vem do invariante, não de regra nova.
- O mesmo Guerreiro(a) **integra mais de uma equipe da mesma aula** (`RF-01-39`, primeira
  metade).
- Formar equipe e entrar nela é escrita do Guerreiro(a) pela operação
  `equipe_que_forma_na_aula`, e a leitura das equipes da aula em andamento pela operação
  `equipes_da_aula_em_andamento` — as duas já concedidas na matriz desde a segunda fatia.

### O que esta fatia não tem, e não é omissão

**O Quiz ao Vivo** (`RF-01-36` e a segunda metade de `RF-01-39` — uma equipe só por partida)
fica para a décima fatia. Ele não é só entidade: é a quarta fonte automática do motor de
pontuação (documento 11 §5), com aparelho vinculado por equipe, ordem de chegada no servidor
e anulação de pergunta pelo Mestre. `PerguntaDeQuiz`, `PartidaDeQuiz` e `RespostaDeQuiz`
nascem lá, sobre a `Equipe` que esta fatia entrega.

**O lastro da aula** (`RN-01-07`, invariante 9) segue fora, pelo mesmo motivo que já valeu na
quinta fatia: a reserva de recursos no agendamento precisa do livro-razão do PRD-07, que é a
entrega nº 3 do documento 99 §9. A aula nasce sem a trava, e a trava chega com o ledger.

**A pontuação da criação original em equipe** — documento 11 §5, "50, integrais a cada
integrante" — não entra aqui. A `Equipe` que esta fatia cria começa e termina **na aula**
(`RF-01-37`), e a criação original é a culminância **da trilha**: a equipe da aula não é
sujeito de um registro que atravessa o ciclo. Isso é pergunta ao fundador, não decisão de
artefato (ver abaixo).

**As rotas** de `aulas`, `presencas` e `equipes` não são deste PRD: estão declaradas no
PRD-04 §9 (App 01) e no PRD-02 §9 (App 03), e o PRD-01 §9 diz expressamente que as rotas de
domínio ficam nos PRDs que as definem. Como nas fatias 5 a 8, esta entrega é entidade e
regra.

**O painel do dia** (`RF-01-17`) é leitura da App 03, requisito do PRD-02.

### Perguntas ao fundador, que esta fatia não resolve sozinha

1. **Criação original em equipe.** O documento 11 §5 e o documento 09 creditam os 50 pontos e
   o badge de autoria "integralmente a cada integrante da equipe", mas a equipe é da aula e a
   culminância é da trilha. Falta dizer que agrupamento credita a culminância.
2. **Papel do integrante.** O documento 02 §5 diz que "o registro guarda o papel de cada
   membro" — quem constrói, quem registra, quem apresenta, quem media. Nem `RF-01-20` nem o
   PRD-01 §8 declaram esse atributo, e ele não entra por suposição: é da equipe, do resultado,
   ou nenhum dos dois no Ciclo 01?
3. **Familiar e modalidade.** O documento 02 §5 admite o familiar "quando a atividade
   permitir", e a atividade já tem a modalidade `em_equipe_com_familiar`; a equipe, porém, é
   da aula, não da atividade. `RF-01-38` é verificável como está — no máximo um —, e é o que
   esta fatia implementa; a amarração à modalidade fica pendente de decisão.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração do
descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e personalização
por IA.

O que é do PRD-01 mas de outra fatia:

| Fica para                                  | Porque                                             |
| ------------------------------------------ | -------------------------------------------------- |
| `RF-01-36`, segunda metade de `RF-01-39`   | Quiz ao Vivo, décima fatia                         |
| `RN-01-07` na aula                         | reserva de recursos depende do PRD-07              |
| `RF-01-23`, `RF-01-24`                     | território (PRD-08) e livro-razão (PRD-07)         |
| `RF-01-25`, `RF-01-46`, `RF-01-47`         | fila de avaliação e entrega do conjunto de dados   |
| `RF-01-29`                                 | entidade `Auditoria` e a consulta de Admin         |
| `RF-01-33`, `RF-01-34`, `RF-01-43`         | documento 09, "Números da proteção das rotas públicas" |
| `RF-01-49` a `RF-01-53`, `RF-01-55`        | documento 09, "Números da proteção das rotas públicas" |

## Capabilities

### New Capabilities

- `aula-e-presenca`: a aula agendada com comunidade, data e horários, a derivação das aulas
  vigentes no momento corrente e o registro de presença por reconhecimento ou por confirmação
  de Mestre ou Admin, único por aula e Guerreiro(a).
- `equipe-da-aula`: a equipe formada pelo Guerreiro(a) dentro de uma aula, que encerra com
  ela sem reaproveitamento, com o teto de cinco integrantes e o limite de um integrante de 17
  anos ou mais.

### Modified Capabilities

Nenhuma. `permissoes-e-escopo-de-comunidade` não muda de requisito: as operações que a equipe
usa já estão concedidas na matriz desde a segunda fatia, e esta fatia apenas passa a exercê-las.
`trilha-e-missao` e `resultado-de-atividade` também não mudam — a aula não altera o
comportamento delas, e o vínculo entre atividade realizada e aula não está em `RF-01-20`.

## Impact

- `backend/src/nucleo/`: módulos novos `aulas/` (`Aula`, `Presenca`, a derivação das aulas
  vigentes e a regra de unicidade da presença) e `equipes/` (`Equipe`, `IntegranteDaEquipe` e
  as regras de composição), lendo `persona`, `comunidade_virtual` e a matriz de permissões já
  existentes.
- `backend/alembic/`: migração para `aula`, `presenca`, `equipe` e `integrante_da_equipe`.
- Nenhuma rota nova sob `/v1`: como nas fatias 5 a 8, entidade e regra — as rotas de aula e
  presença são do PRD-02 e do PRD-04, e as de equipe, do PRD-04.
- `docs/`: nenhuma decisão nova nesta fatia. As três perguntas acima, se respondidas, mudam
  documento-fonte, documento 09 e PRD antes de virar código — nunca dentro desta change.
  `docs/prds/index.md` recebe a situação atualizada se ela mudar ao fim da implementação.
