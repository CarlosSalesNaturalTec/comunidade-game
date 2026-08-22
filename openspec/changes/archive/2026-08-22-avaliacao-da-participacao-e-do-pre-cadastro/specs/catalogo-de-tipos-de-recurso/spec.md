## ADDED Requirements

### Requirement: A gestão lê o catálogo de tipos de recurso

O núcleo SHALL devolver os tipos de recurso cadastrados com **nome**, **natureza**,
**unidade**, se **exige comprovante** e o **valor em moedas vigente** na data da consulta,
ordenados por nome. A leitura SHALL exigir **Admin** em sessão — a mesma restrição do
cadastro —, e os demais papéis SHALL receber **403**. (`RF-07-01`, `RF-01-16`)

Tipo de recurso sem valor de referência vigente na data da consulta NEVER SHALL quebrar a
leitura dos demais: ele SHALL sair da listagem, e os outros SHALL vir normalmente.

#### Scenario: Admin lê o catálogo com o valor vigente

- **WHEN** um Admin em sessão consulta os tipos de recurso
- **THEN** vêm todos os cadastrados, com nome, natureza, unidade e o valor em moedas da
  vigência corrente

#### Scenario: Quem não é Admin não lê o catálogo

- **WHEN** um Mestre em sessão consulta os tipos de recurso
- **THEN** o núcleo responde 403
