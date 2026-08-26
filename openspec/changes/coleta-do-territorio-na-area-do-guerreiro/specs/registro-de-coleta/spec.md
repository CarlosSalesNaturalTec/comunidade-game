## ADDED Requirements

### Requirement: O Guerreiro(a) consulta o histórico da própria série

O núcleo SHALL devolver ao **Guerreiro(a) em sessão** o histórico dos registros de uma série
**dele**, do mais recente ao mais antigo, cada registro com o **momento da medição**, o
**valor** e a **unidade** quando houver, a **mídia** quando ela for o próprio registro, a
**origem**, a **situação**, a marca **"a conferir"** e os **pontos creditados**. A consulta
SHALL ser paginada como toda listagem do núcleo.

O registro **invalidado** SHALL sair com o **motivo** que o Mestre autor declarou na
invalidação, em linguagem que a criança leia. Nenhum outro registro SHALL carregar motivo.
(`RF-05-37`, `RF-05-38`, `RN-05-09`, PRD-05 §§5.4, 6.4)

A consulta SHALL recusar com **403** a série de **outro** coletor e a persona de **outro
papel** — o Mestre audita pela porta da auditoria, não por esta. (`RN-05-21`)

#### Scenario: O histórico traz data e valor de cada registro

- **WHEN** um Guerreiro(a) consulta o histórico de uma série sua
- **THEN** o núcleo devolve os registros dela, do mais recente ao mais antigo, cada um com o
  momento da medição, o valor e a unidade, a origem, a situação e os pontos creditados

#### Scenario: O registro a conferir aparece como tal, sem pontos

- **WHEN** o histórico inclui um registro marcado "a conferir" ainda não confirmado
- **THEN** ele sai com a marca e com zero ponto creditado

#### Scenario: O registro invalidado exibe o motivo

- **WHEN** o histórico inclui um registro que o Mestre autor invalidou
- **THEN** ele sai com a situação `invalidada` e com o motivo declarado na invalidação

#### Scenario: A invalidação de um registro não apaga os demais

- **WHEN** o Guerreiro(a) consulta o histórico de uma série que teve um registro invalidado
- **THEN** os demais registros continuam no histórico com os pontos que creditaram

#### Scenario: O histórico de série alheia é recusado

- **WHEN** um Guerreiro(a) consulta o histórico de uma série de outro coletor
- **THEN** o núcleo responde 403 e nada é devolvido

#### Scenario: Outro papel não lê pela porta do Guerreiro(a)

- **WHEN** um Mestre ou um Admin chama a consulta do histórico da série
- **THEN** o núcleo responde 403

#### Scenario: A série interrompida preserva o histórico

- **WHEN** um Guerreiro(a) consulta o histórico de uma série interrompida
- **THEN** o núcleo devolve todos os registros dela, com os pontos já creditados intactos
