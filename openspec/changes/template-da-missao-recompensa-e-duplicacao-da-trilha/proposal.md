## Why

Origem: **PRD-09 — Área do Mestre**, fatias **12** e **13** do
`openspec/cronograma-de-fatias.md`.

- Fatia 12 — **Template da missão por IA**: `RF-09-85` a `RF-09-91`, `RF-09-95`, `RF-09-116`,
  `RN-09-33` e `RN-09-34`.
- Fatia 13 — **Recompensa por desbloqueio e duplicação de trilha**: `RF-09-13`, `RF-09-84` e
  `RF-09-75`.

O template é a última função do documento 03 §11 sem código: hoje o Mestre monta a missão do
zero e descobre o que falta só quando a publicação recusa. A fatia 13 fecha a recompensa pelo
lado que o documento 11 §2.2 descreve — o **desbloqueio** libera —, que o núcleo hoje deriva do
`Resultado`, e dá ao Mestre a fila do que precisa entregar e o atalho de partir de uma trilha
que já existe.

As duas fatias vão numa change só, a pedido do fundador: são pequenas, tocam a mesma aplicação
e o mesmo branch. Ao fechar, **duas linhas** do cronograma mudam de situação.

**Correção de recorte:** o `RF-09-116` (o template sugere a retomada em 2, 7 e 21 dias do
desbloqueio) não constava de nenhuma fatia do cronograma, e é função do template — entra no
recorte da fatia 12 e a linha do cronograma é corrigida nesta change, conforme o `CLAUDE.md`.

**Decisão nova do fundador (2026-08-29):** o `RF-09-88` e a `RN-09-34` falam em "trilha de
poder técnico", e nenhum documento dizia o que torna um poder técnico. O fundador decidiu:
**o poder técnico é marcado no catálogo, declarado por Admin** — mesmo princípio que a `RN-01-54`
já aplica ao papel do poder, nunca deduzido do nome. A decisão vai ao documento 02 §2, ao
documento 09 §1 e ao PRD-01 nesta mesma change, antes de virar código.

## What Changes

**Fatia 12 — Template da missão**

- O Mestre autor cadastra, em texto corrente, o **tópico que quer ensinar** e recebe a
  **estrutura sugerida** da missão, no formato do documento 11 §2.2 (`RF-09-85`).
- O template **aponta as lacunas** da missão que já existe: sem atividade, atividade sem
  produção do Guerreiro(a), retomada não declarada (`RF-09-86`).
- A sugestão inclui a **etiqueta ODS** derivada do tópico (`RF-09-95`) e a **cadência de
  retomada** em 2, 7 e 21 dias do desbloqueio (`RF-09-116`).
- Em trilha de **poder técnico**, a estrutura sugerida traz ao menos uma **atividade
  desplugada** (`RF-09-88`, `RN-09-34`).
- O template **não escreve o conteúdo** da missão, e o Mestre segue autor creditado
  (`RF-09-87`, `RN-09-33`).
- Nada entra na trilha sem o Mestre **aceitar, recusar ou alterar** cada sugestão
  (`RF-09-89`).
- Nenhum consumo do modelo é medido nem lançado: o custo entra pela fatura de _cloud_
  (`RF-09-90`), como a capacidade `conteudo-da-missao` já faz com o armazenamento.
- A tela não pede do Mestre conhecimento técnico algum (`RF-09-91`).
- Rota nova: `POST /v1/missoes/{id}/estrutura` (PRD-09 §9).

**Fatia 13 — Recompensa por desbloqueio e duplicação**

- **MODIFICAÇÃO DE COMPORTAMENTO:** o marco alcançado passa a ser o **desbloqueio da missão**
  pelo Guerreiro(a), e não mais a existência de `Resultado` numa atividade dela. É o que o
  `RF-09-84`, o documento 03 §11 e o documento 11 §2.2 dizem; a derivação por `Resultado` foi
  escrita na fatia 10 do PRD-07, quando a capacidade `desbloqueio-da-missao` ainda não existia.
  Alcança a recusa da entrega e a leitura do Guerreiro(a).
- O Mestre autor declara a recompensa **no desbloqueio da missão**, com quantidade
  (`RF-09-84`), pela tela da App 09 que ainda não existia.
- O marco alcançado com recompensa declarada vira **pendência de entrega** listada para o
  Mestre da comunidade (`RF-09-75`).
- O Mestre **duplica** uma trilha existente como ponto de partida de outra, em rascunho e sob
  a autoria de quem duplicou (`RF-09-13`).

**Catálogo de poderes**

- O poder ganha a marca **técnico**, declarada por Admin no cadastro, legível na gestão e lida
  pelo template (`RF-01-62`, `RN-01-54`, decisão do fundador de 2026-08-29).

## Capabilities

### New Capabilities

- `template-da-missao`: o tópico em texto corrente vira estrutura sugerida e checklist de
  lacunas; o que o modelo propõe e o que o núcleo confere; nada entra sem confirmação do
  Mestre; nenhum consumo medido.

### Modified Capabilities

- `recompensa-de-marco`: o marco alcançado passa a ser o desbloqueio da missão, não o
  `Resultado`; a recompensa conquistada e ainda não entregue vira pendência de entrega para o
  Mestre da comunidade.
- `trilha-e-missao`: o Mestre duplica trilha existente como rascunho próprio.
- `catalogo-de-poderes`: o poder declara, no catálogo, se é técnico.
- `area-do-mestre`: telas do template, da recompensa declarada no desbloqueio, da fila de
  entregas pendentes e da duplicação da trilha.

## Impact

- **Núcleo** (`backend/src/nucleo/`): módulo novo do template, com porta e adaptadores no
  padrão de `armazenamento/` (porta, fábrica, adaptador local e adaptador Gemini); alterações
  em `recompensas_de_marco/`, `trilhas/` e `poderes/`; migração Alembic para a entidade
  `SugestaoDeEstrutura` (PRD-09 §8), a recompensa presa ao desbloqueio e a marca do poder.
- **App 09** (`apps/app-09-mestre/`): tela do template na autoria da missão, declaração da
  recompensa no desbloqueio, fila de entregas pendentes em Minhas turmas e o botão de duplicar
  na lista de trilhas.
- **App 03** (`apps/app-03-gestao/`): a marca de poder técnico no formulário do catálogo.
- **App 05** (`apps/app-05-guerreiro/`): nenhuma alteração de tela — a leitura das recompensas
  conquistadas passa a responder ao desbloqueio pelo lado do núcleo.
- **Documentação**: documento 02 §2 e documento 09 §1 (decisão do poder técnico), PRD-01
  (`RF-01-62`, `RN-01-54`), `docs/prds/index.md` e `openspec/cronograma-de-fatias.md` (fatias
  12 e 13, e o `RF-09-116` no recorte da 12).
- **Configuração**: credencial e modelo do Gemini como parâmetro, no padrão de
  `armazenamento_bucket_cloud_storage`; fora de produção, o adaptador local não exige
  credencial.

### Fora do escopo

O que o PRD-09 §3.2 já exclui, e em especial a **geração de conteúdo por IA**: a aplicação
monta estrutura e aponta lacunas; quem escreve o conteúdo da missão é o Mestre, autor
creditado na licença. Também ficam de fora as trilhas de ciclo futuro e a curadoria pedagógica
prévia.
