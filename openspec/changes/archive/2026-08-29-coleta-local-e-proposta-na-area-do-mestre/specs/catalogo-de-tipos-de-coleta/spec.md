## ADDED Requirements

### Requirement: O catálogo é legível por quem escolhe entre os tipos

O núcleo SHALL expor o catálogo de tipos de coleta em **leitura**, para a persona autenticada
que escreve o desafio de coleta — o **Mestre** — e para o **Admin** que o cadastra. Sem essa
leitura o Mestre não tem entre o que escolher, e `RF-09-27` não se cumpre: o catálogo é o
vocabulário do desafio, e o Mestre NEVER SHALL criar tipo novo ao escrever o desafio.
(`RF-09-27`, `RF-08-05`, `RF-08-06`, `RF-01-28`, PRD-08 §4)

Cada tipo SHALL sair com o **nome**, a **forma de registro**, a **unidade** e a **faixa
esperada** quando houver, e a indicação de estar **ativo** — para que a aplicação nunca ofereça
um tipo desativado, que o núcleo recusaria na criação do desafio. A leitura SHALL ser paginada
como toda listagem do núcleo.

A leitura NEVER SHALL criar, alterar nem desativar tipo: o cadastro segue privativo do Admin.
Persona de papel que não escreve desafio nem cadastra tipo — Guerreiro(a), responsável e
Apoiador — SHALL receber **403**.

#### Scenario: O Mestre lê o catálogo para escolher o tipo

- **WHEN** um Mestre em sessão consulta o catálogo de tipos de coleta
- **THEN** o núcleo devolve os tipos cadastrados, cada um com nome, forma de registro, unidade
  e faixa esperada quando houver, e a indicação de estar ativo

#### Scenario: O tipo por evidência sai sem unidade e sem faixa

- **WHEN** a leitura devolve um tipo cuja forma de registro é `foto` ou `vídeo`
- **THEN** ele sai sem unidade e sem faixa esperada, porque não produz valor a comparar

#### Scenario: O tipo desativado sai assinalado

- **WHEN** o catálogo tem um tipo desativado e a leitura é consultada
- **THEN** o tipo aparece assinalado como não ativo, para que a aplicação não o ofereça

#### Scenario: O Admin lê o mesmo catálogo

- **WHEN** um Admin em sessão consulta o catálogo de tipos de coleta
- **THEN** o núcleo devolve a mesma listagem

#### Scenario: A leitura não altera o catálogo

- **WHEN** o catálogo é consultado
- **THEN** nenhum tipo é criado, alterado ou desativado por essa consulta

#### Scenario: Papel que não escolhe nem cadastra é recusado

- **WHEN** um Guerreiro(a), um responsável ou um Apoiador consulta o catálogo de tipos de coleta
- **THEN** o núcleo responde 403
