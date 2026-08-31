## Why

Fatia **3 do PRD-13** (`openspec/cronograma-de-fatias.md`) — **Autorização única**. Atende
`RF-13-13` a `RF-13-21` e `RN-13-05` a `RN-13-11`.

A App 07 já entra, lista os vinculados e mostra a evolução (fatias 1 e 2), mas o ato que dá
razão à aplicação continua sem porta: **conceder e revogar a autorização única**. O núcleo já
guarda o `Consentimento` somente inserção e já deriva a vigência com a recusa prevalecendo —
vitrine, ranking, portfólio e elenco do jogo já leem por ela —, e quem escreve hoje é apenas a
gestão, pela `POST /v1/consentimentos` do termo impresso. Falta o caminho do próprio
responsável. Sem ele a divulgação pública não tem de onde nascer e a hipótese **H2** do Ciclo
01 não tem instrumento.

## What Changes

- **Leitura da autorização pelo responsável** — `GET /v1/eu/guerreiros/{id}/autorizacao`: o
  estado vigente em três valores — **vigente**, **suspensa** e **não autorizada** —, quem
  motivou a suspensão com data e hora, e o histórico de cada concessão e revogação com a versão
  do termo (`RF-13-18`, `RF-13-21`).
- **Escrita da autorização pelo responsável** — `POST /v1/eu/guerreiros/{id}/autorizacao`:
  concede e revoga em nome próprio, com origem `propria` e a versão do termo carimbada pelo
  núcleo (`RF-13-14`, `RF-13-15`, `RN-13-10`). Recusas previstas na PRD-13 §9: 403 sem vínculo,
  409 na concessão havendo recusa vigente de outro responsável e 409 na revogação sem concessão
  própria vigente. Reenvio da mesma decisão não gera segundo registro (PRD-13 §10).
- **Estado suspenso por divergência** derivado do mesmo histórico somente inserção, sem coluna
  de estado: há concessão de um responsável e recusa de outro (`RF-13-17`, `RN-13-07`).
- **Solicitação aberta pela suspensão** na fila da App 03, pelo núcleo, do tipo
  `esclarecimento`, em nome de quem recusou e **uma só enquanto estiver em aberto** para aquele
  Guerreiro(a) (`RF-13-19` — decisão do fundador, 2026-08-31).
- **Telas da autorização na App 07**: o que a autorização libera e o que não depende dela antes
  de qualquer botão (`RF-13-13`), a alternativa equivalente enquanto não houver autorização
  (`RF-13-20`), o estado suspenso com quem o motivou (`RF-13-18`) e o histórico (`RF-13-21`).
- `RF-13-16` e `RN-13-11` **não pedem código novo**: vitrine, ranking, portfólio e elenco do
  jogo já filtram pela vigência derivada. A fatia os cobre por cenário, provando que a
  revogação do responsável os retira do que é público sem apagar registro algum.
- **Documentação**: a decisão do fundador sobre a solicitação da divergência entra no documento
  09 §1 e é aplicada no PRD-13 §§6.3 e 9.

## Capabilities

### New Capabilities

Nenhuma. A fatia estende capacidades que já existem.

### Modified Capabilities

- `consentimento`: as duas rotas do responsável sobre a própria autorização, os três estados
  derivados do histórico, o histórico com autoria e versão do termo, as recusas 403/409 e a
  idempotência do reenvio (`RF-13-14`, `RF-13-15`, `RF-13-17`, `RF-13-18`, `RF-13-21`,
  `RN-13-05` a `RN-13-11`).
- `solicitacao-do-responsavel`: a solicitação aberta pelo próprio núcleo quando a suspensão
  nasce, do tipo `esclarecimento`, uma só por Guerreiro(a) enquanto estiver sem desfecho
  (`RF-13-19`).
- `area-dos-responsaveis`: as telas da autorização na App 07 — declaração antes do ato, ato,
  estado, alternativa equivalente e histórico (`RF-13-13`, `RF-13-15`, `RF-13-18`, `RF-13-20`,
  `RF-13-21`).

## Impact

- `backend/src/nucleo/consentimentos/` — `regra.py` (derivação dos três estados, histórico e
  registro pelo próprio responsável) e `rotas.py` (as duas rotas `/v1/eu/...`).
- `backend/src/nucleo/solicitacoes_do_responsavel/` — abertura da solicitação da suspensão,
  com a guarda de uma só em aberto por Guerreiro(a); migração da marca que a distingue.
- `apps/app-07-responsaveis/src/autorizacao/` — tela, chamadas e testes; navegação entre
  evolução e autorização em `src/vinculados/TelaDeVinculados.tsx`.
- `docs/09-topicos-em-aberto-e-sugestoes.md` §1 e `docs/prds/prd-13-area-dos-responsaveis.md`
  §§6.3, 9, 13; `openspec/cronograma-de-fatias.md`.
- Sem entidade nova (PRD-13 §8), sem provedor novo e sem custo em livro-razão: nenhum ato desta
  fatia tem custo.
