## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Nona fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-20` (parcial — `Aula/Agenda`, `Presenca` e `Equipe`),
`RF-01-32`, `RF-01-37`, `RF-01-38`, `RF-01-39` (parcial — a metade das várias equipes da
aula), `RF-01-63`, `RF-01-64`, `RN-01-44`, `RF-01-03`, `RF-01-16`, `RF-01-18`.

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

- Nasce a **Equipe**, criada pelo próprio Guerreiro(a), que entra como primeiro integrante, em
  **dois tempos de vida** — a da aula e a da trilha (documento 02 §5). É uma entidade só, e o
  vínculo declara qual das duas ela é: aula **ou** trilha, nunca as duas.
- A **equipe da aula** encerra com a aula e não é reaproveitada: equipe de uma aula não
  aparece em outra (`RF-01-37`).
- A **equipe da trilha** é formada pelos Guerreiros e Guerreiras e **homologada pelo Mestre**;
  da homologação em diante ela não recebe nem perde integrante (`RF-01-63`, `RN-01-44`). É uma
  por trilha percorrida, o mesmo alcance da unicidade que `CriacaoOriginal` já tem.
- A criação original passa a ser creditada **a cada integrante** da equipe da trilha que a
  entregou, com o **papel de cada um** guardado (`RF-01-64`, documento 02 §4). Fecha a dívida
  que a sétima fatia deixou anotada em `pontuacao/regra.py`.
- O núcleo não confere onde a homologação acontece: "em encontro presencial" é regra de
  operação, e a aplicação que a carrega segue pendente no documento 09.
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

**A validação da criação original** segue sendo ato do Mestre autor, pela rota do PRD-09: esta
fatia muda a quem o crédito vai — cada integrante da equipe da trilha —, não quem valida.

**As rotas** de `aulas`, `presencas` e `equipes` não são deste PRD: estão declaradas no
PRD-04 §9 (App 01) e no PRD-02 §9 (App 03), e o PRD-01 §9 diz expressamente que as rotas de
domínio ficam nos PRDs que as definem. Como nas fatias 5 a 8, esta entrega é entidade e
regra.

**O painel do dia** (`RF-01-17`) é leitura da App 03, requisito do PRD-02.

### Decisão nova aplicada antes desta change

A equipe fixa da criação original foi decidida pelo fundador durante a exploração e **subiu a
hierarquia antes de virar plano**, na ordem que o `CLAUDE.md` exige: gravada no documento-fonte
(02 §§4 e 5), registrada no documento 09 em "Já decididos", aplicada ao PRD-01 — `RF-01-37`
reescrito, `RF-01-63`, `RF-01-64` e `RN-01-44` novos, matriz da §4, modelo da §8, aceite da
§12 e rastreabilidade da §15 — e refletida no invariante 15 do documento 99. Só então entrou
aqui.

Segue em aberto, e não trava esta fatia: **o familiar e a modalidade**. O documento 02 §5
admite o familiar "quando a atividade permitir", e a atividade já tem a modalidade
`em_equipe_com_familiar`; a equipe, porém, é da aula ou da trilha, não da atividade.
`RF-01-38` é verificável como está — no máximo um —, e é o que esta fatia implementa.

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
- `equipe`: a equipe formada pelo Guerreiro(a) nos dois tempos de vida — a da aula, que encerra
  com ela sem reaproveitamento, e a da trilha, fixa depois de homologada pelo Mestre —, com o
  teto de cinco integrantes, o limite de um integrante de 17 anos ou mais e o papel de cada um.

### Modified Capabilities

- `criacao-original`: a criação original deixa de ser registro só do autor e passa a ser da
  equipe da trilha, com o papel de cada integrante (`RF-01-64`, `RN-01-13` preservado — o autor
  segue creditado por toda a vida do registro).
- `pontos-niveis-e-badges`: os pontos, o nível 5 e o badge de autoria da criação original passam
  a alcançar cada integrante da equipe da trilha, e não só quem entregou (`RF-01-21`,
  `RF-01-64`).

`permissoes-e-escopo-de-comunidade` **não** entra: o requisito dela é genérico — "conferir a
matriz do PRD-01 §4 em toda operação" —, e a matriz é dado do PRD, não texto do spec. As duas
células novas mudam o PRD, já atualizado, e quem escreve o quê na equipe está declarado na
capability `equipe`.

## Impact

- `backend/src/nucleo/`: módulos novos `aulas/` (`Aula`, `Presenca`, a derivação das aulas
  vigentes e a regra de unicidade da presença) e `equipes/` (`Equipe`, `IntegranteDaEquipe`, as
  regras de composição e a homologação), lendo `persona`, `comunidade_virtual`, `trilha` e a
  matriz de permissões já existentes.
- `backend/src/nucleo/permissoes.py`: duas operações novas na matriz — a equipe da trilha para
  o Guerreiro(a) e a homologação para o Mestre.
- `backend/src/nucleo/criacoes_originais/` e `pontuacao/`: a criação original passa a referenciar
  a equipe da trilha, e o crédito dos pontos e do badge de autoria alcança cada integrante.
  Some o comentário "sem equipe nesta fatia" de `pontuacao/regra.py`.
- `backend/alembic/`: migração para `aula`, `presenca`, `equipe` e `integrante_da_equipe`, e a
  alteração de `criacao_original` — a unicidade por (autor, trilha) passa a ser por
  (equipe da trilha, trilha).
- Nenhuma rota nova sob `/v1`: como nas fatias 5 a 8, entidade e regra — as rotas de aula e
  presença são do PRD-02 e do PRD-04, as de equipe são do PRD-04, e a da homologação nasce no
  PRD da aplicação que o documento 09 ainda vai definir.
- `docs/`: a decisão da equipe fixa **já foi gravada** nos documentos 02, 09, 99 e no PRD-01,
  antes desta proposta. `docs/prds/index.md` recebe a situação atualizada se ela mudar ao fim
  da implementação.
