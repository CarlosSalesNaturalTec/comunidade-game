# Proposal

**PRD de origem:** PRD-04 — Aula presencial (App 01), **fatia 16** do
`openspec/cronograma-de-fatias.md`, criada pela revisão de 2026-09-23. A fatia atravessa os
PRDs 01, 02 e 09, como a fatia 15.

**Identificadores:** `RN-04-37`, `RN-04-38`, `RF-01-75`, `RN-01-59`, `RF-02-110` e `RF-09-121`
(novos); `RF-04-21`, `RF-04-23`, `RF-01-06` e `RF-02-43` (alterados).

## Why

Hoje o "Chamar Mestre ou Admin" do App 01 só troca de tela. A confirmação sai com o token da
sessão de trabalho, sem nenhum ato do adulto. Qualquer pessoa digita o nick de outra criança,
abre a sessão dela, entra em equipe e pontua por ela. E a presença fica registrada como
"confirmada" por um Mestre que nunca a viu. A decisão do fundador de 2026-09-23 (documento 09,
linha "Confirmação de identidade no encontro exige o PIN do adulto"; documento 03 §§1.1, 3.2
e 3.4) fecha essa brecha.

## What Changes

- **PIN de confirmação** do Mestre e do Admin, de 4 dígitos. O próprio adulto o cadastra e o
  troca: o Mestre na App 09 e o Admin na App 03 (`RF-09-121`, `RF-02-110`, `RF-01-75`). O
  núcleo guarda só o verificador.
- **Confirmação no App 01 exige o PIN** de quem abriu a sessão de trabalho, e só dele,
  digitado no ato. Sem PIN cadastrado ou com PIN bloqueado, o adulto não confirma. Cinco
  erros seguidos bloqueiam o PIN naquele aparelho até um novo login Google (`RF-04-21`,
  `RF-01-06`, `RN-04-37`, `RN-01-59`).
- **Sem rede**, o aparelho confere o PIN contra o verificador recebido ao abrir a sessão de
  trabalho. O PIN nunca fica no aparelho. A presença entra na fila e sincroniza depois
  (`RF-04-23`, `RN-04-38`).
- **Painel do dia:** a lista "Aguardando aparelho" passa a se chamar **"Sem equipe"**. A regra
  de derivação do `RF-02-43` não muda.
- **BREAKING:** `POST /v1/sessoes/guerreiro/confirmacao`, chamada com a chave do App 01 por
  Mestre ou Admin, passa a exigir `pin` no corpo. A confirmação pelo responsável na App 05
  (`RF-01-74`) não muda.

## Capabilities

### New Capabilities

- `pin-de-confirmacao`: cadastro e troca do PIN de 4 dígitos pelo Mestre e pelo Admin, guarda
  só do verificador, entrega do verificador ao aparelho da sessão de trabalho, conferência e
  bloqueio por erros seguidos (`RF-01-75`, `RN-01-59`, `RN-04-38`).

### Modified Capabilities

- `sessao-do-guerreiro`: a confirmação humana pelo App 01 exige o PIN de quem abriu a sessão
  de trabalho (`RF-01-06`, `RN-01-59`).
- `aplicacao-da-aula-presencial`: a confirmação na entrada pede o PIN; a fila sem rede só
  aceita presença com o PIN conferido no aparelho; o bloqueio vale naquele aparelho
  (`RF-04-21`, `RF-04-23`, `RN-04-37`, `RN-04-38`).
- `painel-do-dia`: a lista de espera passa a se chamar "Sem equipe" (`RF-02-43`).
- `area-do-mestre`: o Mestre cadastra e troca o próprio PIN (`RF-09-121`).
- `aplicacao-de-gestao`: o Admin cadastra e troca o próprio PIN, e o painel mostra "Sem
  equipe" (`RF-02-110`, `RF-02-43`).

## Fora do escopo

- A confirmação pelo responsável na App 05 (`RF-01-74`) e a do Mestre ou Admin na App 05. Lá,
  o adulto entra com o próprio login no momento de confirmar.
- O autocadastro, a homologação da equipe da trilha (`RF-04-62`) e a troca por recompensa
  avulsa. Esses atos continuam autenticados pela sessão de trabalho, como o PRD-04 §9 define.
- A falha de sincronização no painel do dia, que segue pendente (PRD-04 §14).

## Impact

- **Núcleo (`backend/`):** coluna do verificador na `Persona` e contador de erros na `Sessao`,
  com migração Alembic; rotas `PUT /v1/eu/pin-de-confirmacao` e
  `GET /v1/eu/pin-de-confirmacao/verificador`; a rota de confirmação passa a exigir o PIN; a
  sincronização da fila ganha uma rota que não abre sessão (design).
- **App 01:** campo de PIN na confirmação; busca do verificador ao abrir a sessão de trabalho;
  conferência sem rede; bloqueio local; sincronização da fila.
- **App 09 e App 03:** tela de cadastro e troca do PIN; na App 03, o novo rótulo do painel.
- **Operação:** antes do deploy, todo Mestre e todo Admin que abre o App 01 precisa cadastrar
  o PIN. Sem PIN, o adulto continua abrindo a sessão de trabalho, mas não confirma identidade.
