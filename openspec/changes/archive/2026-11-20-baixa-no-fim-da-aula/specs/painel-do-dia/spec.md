## REMOVED Requirements

### Requirement: O painel lista o que falta lançar antes de a aula terminar

**Reason**: a atividade realizada deixou de ser pendência, porque a aula não tem fechamento (`RN-07-43`, `RF-02-46`).

**Migration**: substituído por "O painel lista a digitalização do termo que falta anexar".

## ADDED Requirements

### Requirement: O painel lista a digitalização do termo que falta anexar

O painel SHALL listar os **lançamentos pendentes do encontro**: a **digitalização do termo de
biometria** assinado no encontro e ainda não anexada (`RF-02-69`). A atividade realizada NEVER
SHALL ser pendência: a aula não tem fechamento, e a passagem a realizada é do sistema no fim do
horário.

O painel SHALL apenas **listar**: ele NEVER SHALL lançar, e cada pendência SHALL ser resolvida
na rota que já a atende. (`RF-02-46`, `RF-02-47`, `RF-02-69`, `RN-02-12`, `RN-07-43`)

#### Scenario: A atividade não lançada não é pendência

- **WHEN** o painel é consultado numa aula em andamento sem resultado lançado
- **THEN** nenhuma pendência de atividade realizada aparece

#### Scenario: Termo de biometria sem digitalização é pendência

- **WHEN** um Guerreiro(a) do encontro tem consentimento de biometria e nenhuma digitalização
  anexada
- **THEN** o painel o lista entre os termos que aguardam digitalização

#### Scenario: Anexada a digitalização, a pendência sai

- **WHEN** um Admin anexa a digitalização do termo
- **THEN** a consulta seguinte do painel não traz mais aquele termo entre as pendências

#### Scenario: O painel não lança

- **WHEN** o painel é consultado
- **THEN** nenhuma escrita acontece por causa da consulta, e as pendências seguem como estavam
