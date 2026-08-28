## Why

Fatia 13 do **PRD-02** (`openspec/cronograma-de-fatias.md`, bloco PRD-02). A App 03 coleta
dado pessoal de criança em cadastro, lançamento, conferência de presença, registro de infração
e anexo do termo, e não exibe o aviso que o PRD-02 §11 exige nem oferece onde ler o destino e o
uso de cada dado. Junto dele faltam as duas guardas que protegem esse mesmo território: a
recusa de consentimento que não pode excluir ninguém do lançamento, e a fronteira de autoria
com a App 09 — nenhuma das duas está assegurada por tela ou por teste na gestão.

Identificadores atendidos: `RF-02-64`, `RN-02-23`, `RN-02-24`.

**A fatia perdeu os dois recortes de auditoria por decisão do fundador**: `RF-02-63` (tela da
trilha de auditoria) e `RF-02-70` (auditoria por amostragem das trilhas publicadas, com
despublicação) vão ao **Ciclo 02**, com todos os demais processos de auditoria ainda não
implementados. A entrega da fatia passa a ser o aviso e as guardas.

## What Changes

- A App 03 ganha a área **Direitos e dados**, em leitura: para cada dado que a gestão coleta,
  a finalidade, a base legal, o prazo de retenção e quem acessa, na tabela do PRD-02 §11, com
  os pontos que a §11 declara em prosa — a gestão não vê a imagem do Guerreiro(a), o
  responsável exerce os direitos pela App 07, o registro de território é despersonalizado e
  não apagado, e a infração fica restrita à gestão e ao responsável (`RF-02-64`).
- Toda tela da App 03 que grava dado pessoal passa a exibir um **aviso discreto** do que ali se
  coleta, com acesso à área Direitos e dados. O aviso NUNCA bloqueia a tela nem exige
  confirmação para continuar (`RF-02-64`).
- As telas de lançamento, de conferência de presença e de registro de infração passam a
  assegurar que **recusa ou revogação de consentimento não retira o Guerreiro(a) do
  lançamento**: a lista é a do encontro inteiro, sem filtro por consentimento e sem caminho que
  exclua alguém por causa dele (`RN-02-23`).
- A gestão passa a declarar, onde a fronteira se confunde, que **autoria de trilha, missão,
  conteúdo, atividade de missão, marco e desafio de coleta é do Mestre, na App 09**: a área
  Atividades cadastra apenas atividade avulsa, fora de trilha, e a área Território lê os
  desafios publicados sem oferecer autoria (`RN-02-24`).

## Capabilities

### New Capabilities

Nenhuma. A fatia é toda da App 03, cuja capacidade já existe.

### Modified Capabilities

- `aplicacao-de-gestao`: ganha o aviso de coleta em toda tela que grava dado pessoal e a área
  Direitos e dados (`RF-02-64`), a garantia de que consentimento recusado não exclui do
  lançamento (`RN-02-23`) e a fronteira de autoria com a App 09 (`RN-02-24`).

## Impact

- `apps/app-03-gestao/` — área nova de direitos, componente de aviso consumido pelas telas que
  gravam dado pessoal, e o menu da aplicação.
- Nenhuma mudança no `backend/`: a fatia não move contrato de API nem regra do núcleo.
- `openspec/cronograma-de-fatias.md` — a fatia 13 muda de entrega e de recorte; `RF-02-63` e
  `RF-02-70` saem para o Ciclo 02, com os demais processos de auditoria não implementados.
- `docs/` — a decisão do fundador entra no documento 09 e nas §§3.2, 13 e 14 do PRD-02, e na
  §14 do PRD-09, cujos recortes de auditoria também foram adiados. O PRD-13 não muda.

## Fora do escopo

- O que o PRD-02 §3.2 já exclui e esta fatia toca de perto: **autoria de trilha, missão,
  conteúdo, quiz e desafio de coleta**, com as atividades da missão e a recompensa de marco —
  é a bancada do Mestre na App 09; e as **telas de coleta do Guerreiro(a)**, do PRD-05.
- Por decisão do fundador, ao Ciclo 02: `RF-02-63`, `RF-02-70`, `RF-02-74` a `RF-02-76`,
  `RF-02-98`, `RF-09-35`, `RN-09-21` e `RF-09-48`. O **histórico de acessos do responsável**
  (`RF-13-30`) **permanece no Ciclo 01**, na fatia 5 do PRD-13, e com ele o `RF-13-31`, que
  pende dele.
- Generalizar o aviso para as demais aplicações (`RF-04-26`, `RF-09-68`, `RF-13-41`,
  `RF-14-58`): cada uma o entrega na fatia dela, com a linguagem do seu público.
