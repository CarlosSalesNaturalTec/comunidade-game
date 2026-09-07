## Why

Fatia **16 do PRD-09** (`openspec/cronograma-de-fatias.md`), o Meu perfil da App 09. Atende
`RF-09-114`, `RF-09-66`, `RF-09-67` e `RN-09-14`.

Dois buracos, um herdado e um aberto pelo uso.

**O herdado.** `RF-09-114` — *"Mestre define ou troca o próprio nick e avatar no card"* — é
requisito **essencial** e está sem tela. A change `2026-08-21-nick-de-adulto` entregou o
núcleo pela metade — `PUT /v1/eu/mestre/identidade` aceita o nick e **ignora o avatar**, que a
rota simétrica do Apoiador aceita — e anotou que a tela viria com o PRD-09; a change
`2026-08-29-responsavel-credencial-e-perfil-do-mestre` pôs `RF-09-114` **fora do escopo**
dizendo que a fatia do nick já o entregara. Cada uma contou com a outra, e nenhuma fatia do
cronograma reivindicou o requisito. `TelaDoPerfil` não tem campo de nick nem de avatar, embora
`openspec/specs/area-do-mestre/spec.md` já afirme que a área alcança "a prova de habilidade **e
a identidade do próprio Mestre**".

**O aberto pelo uso.** O Mestre publica (`POST`) e remove (`DELETE`) artefato, e não edita
nenhum. Corrigir um erro de digitação no que ele mesmo publicou obriga a remover e republicar;
no que o Admin declarou no cadastro, que `RN-09-14` torna irremovível por ele, **não há
correção possível**.

## What Changes

Três decisões do fundador, tomadas em 2026-09-06 para esta change, entram no documento 09 §1 e
no documento-fonte de cada uma antes de virar código (§ *Impact*).

- **O Mestre define e troca o próprio nick e avatar** (`RF-09-114`). `PUT
  /v1/eu/mestre/identidade` passa a aceitar **nick e avatar, cada um opcional**, no molde
  exato da rota do Apoiador; **sem o piso de moedas**, que é regra de marca do Apoiador
  (`RN-14-11`) e não alcança o Mestre. A unicidade global do nick e a conferência restrita a
  nicks de adulto continuam sendo do núcleo, sem mudança.
- **Nasce `GET /v1/eu/mestre/identidade`**, restrita ao Mestre, devolvendo o nick e o avatar
  vigentes — a sessão não os carrega, e sem ela a tela gravaria às cegas. Simétrica à do
  Apoiador, sem as moedas nem o piso. Decisão do fundador, 2026-09-06: o `RF-09-114` a exige e
  a §9 do PRD-09 não a trazia.
- **O Mestre edita rótulo e endereço dos artefatos do próprio perfil** — `PATCH
  /v1/mestres/{id}/artefatos/{artefato_id}` —, **inclusive o declarado pelo Admin no cadastro**,
  que **continua irremovível** por ele. Decisão do fundador, 2026-09-06: o documento 02 §1 diz
  hoje que a prova do cadastro "permanece", e a regra passa a ser *permanece e é editável pelo
  próprio adulto, nunca removível por ele*.
- **O núcleo guarda o rótulo e o endereço originais** do artefato do cadastro na primeira
  edição, e os serve à gestão, para que "permanece" não vire substituição sem rastro.
- **A ficha do adulto na App 03 mostra o original**: artefato do cadastro editado pelo Mestre
  aparece marcado, com o valor original ao lado do vigente. Leitura apenas — a gestão continua
  sem editar cadastro de adulto.
- **A App 09 ganha os campos de identidade no Meu perfil** e o caminho de editar cada artefato,
  mantendo a declaração de que a aplicação não cadastra Mestre nem edita nome, e-mail ou papel
  (`RF-09-67`, `RN-09-14`).

**Fora do escopo**, como o PRD-09 §§3.2 e 6.9 já excluem: o **cadastro de Mestre e de
Apoiador**, ato exclusivo de Admin na App 03; a **remoção** do artefato do cadastro pelo
Mestre, que `RN-09-14` mantém vedada; a **edição do próprio nome, e-mail ou papel** pelo
Mestre; e o **exercício dos direitos**, que chega pela App 07.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-do-adulto`: a rota de identidade do Mestre passa a aceitar o avatar além do nick,
  sem piso de moedas, e ganha a leitura da própria identidade.
- `prova-de-habilidade`: o Mestre passa a editar rótulo e endereço dos artefatos do próprio
  perfil, o do cadastro incluído, que segue irremovível por ele e guarda o valor original.
- `area-do-mestre`: o Meu perfil ganha o nick e o avatar do próprio Mestre e o caminho de
  editar cada artefato.
- `aplicacao-de-gestao`: a ficha do adulto marca o artefato do cadastro que o Mestre editou e
  mostra o valor original ao lado do vigente.

## Impact

- `backend/src/nucleo/personas/modelo.py` — `ArtefatoComprobatorio` ganha `endereco_original`,
  `rotulo_original` e `editado_em`, com a revisão do Alembic.
- `backend/src/nucleo/personas/regra.py` — `definir_avatar_do_mestre`, sem piso de moedas, e
  a edição de artefato com a guarda de posse e a preservação do original.
- `backend/src/nucleo/personas/rotas.py` — `PUT /v1/eu/mestre/identidade` passa a aceitar
  avatar; nasce `GET /v1/eu/mestre/identidade`; nasce `PATCH
  /v1/mestres/{id}/artefatos/{artefato_id}`; a saída dos adultos ganha o valor original.
- `apps/app-09-mestre/src/perfil/` — identidade e edição de artefato.
- `apps/app-03-gestao/src/personas/FichaDoAdulto.tsx` — a marca do editado e o valor original.
- Depende das changes `camada-visual-densa-e-navegacao-comum` e
  `tabela-e-ficha-de-personas-na-gestao`, que entregam a ficha que esta estende.
- Documentação no mesmo PR: `docs/02-conceito-do-jogo-e-gamificacao.md` §1 (a prova do cadastro
  passa a ser editável pelo próprio adulto e segue irremovível por ele); PRD-09 §9 (as duas
  rotas novas e o avatar na existente) e §15; `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (as
  três decisões do fundador de 2026-09-06); `openspec/cronograma-de-fatias.md` (a situação da
  fatia 16).
