## Why

Origem: **PRD-07** §8 (economia e livro-razão) e **PRD-02** (App 03). Atende `RF-07-47`,
`RN-07-33`, `RN-07-01` e `RN-02-21`, e aplica a decisão do fundador que fechou a pendência
"Desativação de ponto de apoio" do documento 09 §1.

O ponto de apoio já nasce com a marca de **ativo** e a gestão já a lê, mas **não existe operação
que a mude**: o documento 05 §2 e o PRD-07 §8 previam o espaço ativo sem dizer quem o desativa,
o que acontece com aula já agendada ali e o que acontece com o saldo ainda guardado. Enquanto
isso durar, um ponto de apoio que fechou continua sendo escolhível no agendamento.

O fundador decidiu: **o Admin desativa e reativa**; a desativação é **bloqueada enquanto houver
aula futura** naquele espaço; e o **saldo guardado é transferido por lançamento** antes de o
espaço sair de operação.

## What Changes

- **Desativar e reativar ponto de apoio**, operação de Admin, com motivo e autoria registrados.
- **Bloqueio por aula futura**: ponto de apoio com aula agendada ainda por acontecer NÃO é
  desativado, e a recusa diz quantas aulas o prendem. Como reserva de recurso herda a aula, o
  bloqueio por aula futura já cobre as reservas ativas.
- **Transferência de saldo entre pontos de apoio**, por par de lançamentos — débito na origem e
  crédito no destino, com motivo —, que é o que esvazia o espaço antes de desativá-lo.
- **Ponto de apoio inativo deixa de ser escolhível no agendamento** de aula nova, sem que
  nenhuma aula passada perca o vínculo com ele.
- **Telas da App 03** para desativar, reativar e transferir saldo, no módulo de pontos de apoio
  que já existe.

## Capabilities

### Modified Capabilities

- `ponto-de-apoio`: nasce a operação de desativar e reativar, com o bloqueio por aula futura e
  a autoria registrada.
- `livro-razao`: nasce a transferência de saldo entre pontos de apoio, como par de lançamentos.
- `aula-e-presenca`: o agendamento passa a recusar ponto de apoio inativo.
- `aplicacao-de-gestao`: a App 03 ganha desativar, reativar e transferir saldo.

## Impact

- **Núcleo (`backend/`)**: `pontos_de_apoio/` ganha a operação e a rota; `livro_razao/` ganha a
  transferência; `aulas/regra.py` passa a recusar ponto de apoio inativo no agendamento.
  Migração apenas se a marca de ativo ainda não tiver motivo e autoria da mudança.
- **App 03 (`apps/app-03-gestao/src/pontos-de-apoio/`)**: módulo já existe e recebe as ações.
- **Documentação, no mesmo PR**: documento 05 §2 (quem desativa, o bloqueio e o destino do
  saldo), documento 09 (pendência movida para os já decididos), PRD-07 §8 e PRD-02, que ganham
  o requisito da operação, e `docs/prds/index.md`.
- **Fora do escopo**: a conferência de inventário (`RF-07-20`), que segue pendente e corre fora
  da plataforma no Ciclo 01; a modalidade da aula, cuja pendência foi resolvida pela via de que
  a aula on-line não existe no Ciclo 01 e por isso não gera trabalho de código.
