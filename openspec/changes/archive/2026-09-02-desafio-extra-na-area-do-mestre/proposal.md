## Why

Fatia **15 do PRD-09** (`openspec/cronograma-de-fatias.md`), a Área do Mestre no desafio
extra. Atende `RF-09-51`, `RF-09-52`, `RF-09-105` a `RF-09-112`, `RN-09-11`, `RN-09-40` a
`RN-09-42`.

A entidade `DesafioExtra` nasce em `em_validacao_do_mestre` desde a fatia 1 do PRD-14, e a
fatia da gestão já entregou a fila do Admin, a aprovação que reserva a recompensa e o
encerramento. Falta o meio do caminho: **ninguém valida**. Toda proposta de Apoiador fica
parada, porque a única transição para `em_aprovacao_do_admin` não existe. E o Mestre, que o
documento 04 §3 põe como proponente ao lado do Apoiador, ainda não propõe.

O recorte da fatia foi corrigido nesta change, por decisão do fundador de 2026-09-02: ele
cita `RN-09-40` a `RN-09-42` — teto de 10 pontos, dispensa da validação para o Mestre autor e
reserva na publicação —, que são as regras da proposta do próprio Mestre (PRD-09 §6.11), mas
omitia os `RF-09-105` a `RF-09-112` que as enunciam. A fatia entrega os dois lados.

## What Changes

- **O Mestre valida ou recusa o desafio extra proposto para a sua trilha** (`RF-09-51`): a
  validação grava o **parecer** e leva a situação a `em_aprovacao_do_admin`; a recusa exige o
  **motivo** e leva a `recusado`. Só o Mestre **autor da trilha** valida; qualquer outra
  persona recebe 403 (`RN-09-11`).
- **O recusado pelo Mestre não chega à fila do Admin** (`RF-09-52`) — a fila já filtra por
  `em_aprovacao_do_admin`, e é a recusa que passa a existir.
- **Fila do que há para validar**: `GET /v1/desafios-extras/a-validar`, restrita ao Mestre em
  sessão, com os desafios em `em_validacao_do_mestre` das trilhas de que ele é autor. Rota
  nova, por decisão do fundador de 2026-09-02 — o `RF-09-51` a exige e a §9 do PRD-09 não a
  trazia. Nenhuma resposta identifica Guerreiro(a): do direcionado sai o nick como o
  proponente o digitou.
- **O Mestre propõe desafio extra** (`RF-09-105` a `RF-09-107`, `RF-09-111`), pela mesma rota
  `POST /v1/desafios-extras` do Apoiador, ampliada ao papel Mestre por decisão do fundador de
  2026-09-02. Mesma trilha em andamento, mesmo teto de 10 pontos de qualquer proponente
  (`RN-09-40`), mesmo custeio — absorção do proponente ou saldo de recurso existente — e, no
  direcionado, a **justificativa pedagógica** no lugar da justificativa de vínculo
  (`RF-09-111`, documento 04 §3).
- **A situação de nascimento passa a depender do proponente** (`RF-09-108`, `RF-09-109`,
  `RN-09-41`): proposta do Mestre **autor da trilha** nasce em `em_aprovacao_do_admin`, com a
  dispensa registrada; a de outro Mestre e a do Apoiador seguem nascendo em
  `em_validacao_do_mestre`. A aprovação de Admin continua exigida em todos os casos, e a
  publicação segue reservando a recompensa (`RF-09-110`, `RF-09-112`, `RN-09-42`) — já
  entregues pela fatia da gestão, aqui apenas alcançadas pelo proponente novo.
- **`GET /v1/eu/desafios-extras` passa a servir qualquer proponente**, não só o Apoiador, para
  o Mestre acompanhar o desfecho do que propôs.
- **App 09 ganha a área Desafios extras**: a fila do que validar, o ato de validar com parecer
  ou recusar com motivo, o formulário da proposta própria e a lista do que o Mestre propôs
  com a situação de cada um.

**Fora do escopo**, como o PRD-09 §3.2 e o cronograma já excluem: a **aprovação final**, ato
privativo de Admin inclusive quando quem propõe é o Mestre — já entregue; o **ato de registrar
a conclusão** de um desafio extra, que o cronograma deixa para uma fatia do PRD-09 ainda sem
número; e a **trilha de auditoria** das escritas do Mestre (`RF-09-48`), adiada ao Ciclo 02.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `desafio-extra`: a validação do Mestre com parecer, a recusa com motivo, a fila do que ele
  tem a validar, o Mestre como proponente e a situação de nascimento decidida pelo proponente.
- `area-do-mestre`: ganha a área Desafios extras da App 09 — validar, recusar, propor e
  acompanhar.

## Impact

- `backend/src/nucleo/desafios_extras/` — `modelo.py` ganha `parecer_do_mestre`; `regra.py`
  ganha a validação, a recusa, a fila do Mestre e a escolha da situação de nascimento, e
  `propor_desafio_extra` passa a aceitar o Mestre; `rotas.py` ganha `/validacao` e
  `/a-validar`, e amplia `POST /desafios-extras` e `GET /eu/desafios-extras`.
- `backend/alembic/versions/` — migração da coluna nova.
- `backend/src/nucleo/permissoes.py` — o papel Mestre ganha `propostas_de_desafio_extra` em
  escrita.
- `apps/app-09-mestre/` — área nova `desafiosExtras`, com a rota no `App.tsx`.
- Documentação no mesmo PR: PRD-09 §9 (as duas rotas) e §15; PRD-01 §4 (a matriz, que o
  documento 04 §3 já contradizia ao não listar o Mestre como proponente);
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (as decisões do fundador de 2026-09-02);
  `openspec/cronograma-de-fatias.md` (o recorte corrigido e a situação da fatia 15).
