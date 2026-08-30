## ADDED Requirements

### Requirement: O Mestre duplica trilha existente como ponto de partida de outra

O núcleo SHALL permitir que um **Mestre** duplique uma trilha do catálogo, criando uma trilha
**nova em rascunho** cujo **autor é quem duplicou** — mesmo quando a origem é de outro Mestre,
porque a trilha publicada é **bem comum** da plataforma, sob licença CC BY-SA.

A cópia SHALL trazer o poder, a área do conhecimento, o objetivo, as **missões** com a ordem,
o título, a dificuldade, a obrigatoriedade, a natureza de sondagem, a etapa do ciclo, a cadência
de retomada e o desafio de desbloqueio de cada uma, e as **atividades** de cada missão com
modalidade, formato e natureza. O nome SHALL vir marcado como cópia, para que as duas não se
confundam na lista do Mestre.

A cópia NEVER SHALL trazer o que é **fato de pessoa** nem o que é lastro da origem: inscrição,
desbloqueio, resultado, criação original, entrega, recompensa de marco, registro de coleta e
auditoria ficam **todos** com a trilha de origem. A trilha de origem NEVER SHALL ser alterada
pela duplicação, e a nova SHALL nascer **sem versão publicada** e sem percurso algum. Duplicar
trilha em **rascunho** de outro Mestre SHALL ser recusado com **403**: rascunho é visível apenas
ao autor. Persona que não é Mestre SHALL ser recusada com **403**. (`RF-09-13`, `RF-09-04`,
`RN-09-05`, documento 03 §11)

#### Scenario: Mestre duplica trilha publicada de outro autor

- **WHEN** um Mestre duplica uma trilha publicada escrita por outro Mestre
- **THEN** o núcleo cria uma trilha nova em rascunho, com ele como autor, trazendo as missões e
  as atividades da origem

#### Scenario: A cópia não traz percurso nem fato de pessoa

- **WHEN** a trilha de origem tem inscritos, desbloqueios, resultados e recompensas de marco
  declaradas
- **THEN** a trilha nova nasce sem inscrição, sem desbloqueio, sem resultado e sem recompensa de
  marco alguma

#### Scenario: A origem não é alterada

- **WHEN** um Mestre duplica uma trilha
- **THEN** a trilha de origem permanece exatamente como estava, com a mesma situação, o mesmo
  autor e o mesmo percurso

#### Scenario: A cópia nasce em rascunho

- **WHEN** um Mestre duplica uma trilha publicada
- **THEN** a trilha nova consta em rascunho, visível apenas a ele, e não aparece na consulta
  pública

#### Scenario: Rascunho de outro Mestre não se duplica

- **WHEN** um Mestre tenta duplicar uma trilha em rascunho de outro Mestre
- **THEN** o núcleo responde 403 e nada é criado

#### Scenario: Quem não é Mestre não duplica

- **WHEN** uma persona que não é Mestre pede a duplicação de uma trilha
- **THEN** o núcleo responde 403 e nada é criado
