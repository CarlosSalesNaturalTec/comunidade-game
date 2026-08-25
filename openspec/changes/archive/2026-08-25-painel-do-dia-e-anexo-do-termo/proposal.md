## Why

O PRD-02 §6.4 é o instrumento de controle do encontro (documento 05 §4), e é o único bloco do
PRD-02 sem nenhum requisito entregue. Hoje a gestão tem as escritas do encontro — agenda,
lançamento, quiz, troca — e não tem a leitura que diz **o que está acontecendo agora**: quem
chegou, em que missão cada equipe está, o que falta lançar antes de a aula acabar.

Os sete insumos que o painel agrega já estão no núcleo, e o último deles entrou na sétima fatia
do PRD-04 (`GET /v1/equipes/{id}/missao`). O `RF-09-50` do PRD-09, entregue na terceira fatia
daquele PRD, aponta para uma tela que ainda não existe.

Origem: **PRD-02**, §§6.3, 6.4 e 9, com o `RF-09-50` do **PRD-09** §6.6.

Requisitos atendidos: `RF-02-41`, `RF-02-42`, `RF-02-43`, `RF-02-44`, `RF-02-45`, `RF-02-46`,
`RF-02-47`, `RF-02-48`, `RF-02-68`, `RF-02-69` e `RF-09-50`, sob `RN-02-20`, `RN-02-21` e
`RN-02-22`. Alcança também o `RF-04-35` do **PRD-04**, no ponto em que ele diz "a missão **em
que está**".

## What Changes

- Nasce **`GET /v1/painel-do-dia`** (PRD-02 §9), de Mestre ou Admin, que devolve o estado do
  encontro em andamento numa leitura só: presenças, equipes com a missão de cada uma, quem
  aguarda aparelho, atividade prevista e recursos providos, saldo dos tipos de recurso do ponto
  de apoio, lançamentos pendentes e termos de biometria sem digitalização anexada
  (`RF-02-41` a `RF-02-47`, `RF-02-69`).
- A **equipe da aula passa a gravar qual atividade da programação está trabalhando**, e o
  painel a lê ao vivo (`RF-02-42`, `RF-04-35`). É a única escrita nova de domínio da fatia, e
  ela reverte uma frase da sétima fatia do PRD-04 — decisão do fundador, 2026-08-25, na
  pergunta que abriu esta change. A escolha **morre com a aula**, como toda a equipe da aula
  (documento 02 §5): ela é estado do encontro em andamento, não percurso da trilha, e continua
  valendo que a equipe da aula NEVER SHALL guardar progresso.
- **Fora essa escolha, nenhuma entidade nova e nenhuma coluna nova.** Todo o resto do painel é
  derivado do que já está gravado — agregação de leitura, no espírito da necessidade de recurso
  da quarta fatia do PRD-07.
- Nasce **`POST /v1/consentimentos/{id}/anexo`** (PRD-02 §9), de Admin, que anexa ao
  consentimento de tipo `biometria` a digitalização do termo assinado no encontro, pela porta
  de armazenamento e no mesmo formato do comprovante de aporte (`RF-02-68`).
- A **App 03** ganha a área **Painel do dia**, em leitura, que se atualiza sozinha por sondagem
  durante o encontro (`RF-02-48`), sem exibir imagem real de Guerreiro(a) (`RN-02-22`).
- A **App 01**, no caminho das trilhas, passa a declarar ao núcleo qual atividade da
  programação a equipe escolheu — sem a escrita, o painel nasceria com o campo do `RF-02-42`
  permanentemente vazio (`RF-04-35`).
- A **App 09** passa a levar o Mestre ao painel do dia da sua aula, a partir de Minhas turmas
  (`RF-09-50`).
- **Correção de redação do PRD-02**, sem decisão nova — três respostas do fundador em
  2026-08-25, no precedente do `RF-04-41` corrigido na sexta fatia do PRD-04:
  1. `RF-02-43` — "aguardando aparelho" é **derivado**: Guerreiro(a) com presença registrada na
     aula e ainda sem equipe formada nela. Não há entidade, coluna nem fila explícita. Aplica o
     documento 05 §4 ("quem chegou e ainda não pegou um aparelho", "um aparelho por equipe") e
     o §5 ("a plataforma não controla aparelhos no Ciclo 01").
  2. `RF-02-45` — "kits MDF" e "exemplares da linha Alpha" são **exemplo, não catálogo**: o
     painel mostra o saldo dos tipos de recurso do ponto de apoio da aula, pelo catálogo
     configurável da primeira fatia do PRD-07. O texto do `RF-02-45` e o critério de aceite
     correspondente da §12 são corrigidos para dizer isso.
  3. `RF-02-46` e `RF-02-47` **dizem a mesma coisa**: consolidam-se num requisito só, com os
     dois identificadores citados juntos, como o catálogo avulso fez com `RF-09-100` e
     `RF-09-101`.

## Capabilities

### New Capabilities

- `painel-do-dia`: a leitura agregada do encontro em andamento, servida ao Mestre e ao Admin —
  o que a compõe, como cada parte é derivada e o que ela nunca expõe.

### Modified Capabilities

- `consentimento`: o consentimento de tipo `biometria` passa a aceitar a digitalização do termo
  assinado, anexada pela gestão depois do ato (`RF-02-68`).
- `aplicacao-de-gestao`: a App 03 ganha a área Painel do dia, em leitura e com sondagem
  (`RF-02-41` a `RF-02-48`, `RF-02-69`).
- `area-do-mestre`: Minhas turmas passa a levar o Mestre ao painel do dia da aula dele
  (`RF-09-50`).
- `equipe`: a equipe da aula passa a gravar a atividade da programação que está trabalhando —
  cai a frase da sétima fatia que proibia gravar a escolha, e fica de pé a que proíbe guardar
  percurso (`RF-02-42`, `RF-04-35`).
- `aplicacao-da-aula-presencial`: a tela da programação passa a declarar a escolha da equipe
  (`RF-04-35`).

## Impact

- **Backend** — `backend/src/nucleo/painel_do_dia/` (novo, só leitura) e
  `backend/src/nucleo/consentimentos/` (a rota do anexo). Nenhuma migração de esquema.
- **Apps** — `apps/app-03-gestao/src/painel-do-dia/` (novo), a declaração da escolha em
  `apps/app-01-aula-presencial/src/trilhas/` e um caminho novo em
  `apps/app-09-mestre/src/turmas/`.
- **Reuso, sem recriar** — `Presenca` e a leitura da aula (`aula-e-presenca`), a missão da
  equipe (`equipe`), a `Reserva` e o saldo por ponto de apoio (`reserva-de-recurso`,
  `livro-razao`), o `Lancamento`, o `Consentimento` de tipo `biometria` e a
  `PortaDeArmazenamento` do comprovante de aporte. A sondagem segue o padrão da condução do
  quiz, já em `aplicacao-de-gestao`.
- **Documentação no mesmo PR** — `docs/prds/prd-02-frontend-de-gestao.md` (as três correções,
  nas §§6.3, 6.4, 12 e 13) e `docs/prds/index.md` (a narrativa da fatia). Sem linha nova no
  documento 09, sem arquivo novo em `docs/` e, portanto, sem alteração na `nav` do
  `mkdocs.yml`.
- **Fora do escopo**, pelo PRD-02 §3.2 — nenhuma escrita de Mestre além do quiz e da ocorrência
  (`RF-02-49`, já entregue), e o painel não lança: os lançamentos pendentes que ele lista são
  feitos nas rotas que já existem.
