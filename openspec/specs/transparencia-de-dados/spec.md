## Purpose

A resposta do núcleo à pergunta que a família faz: o que a plataforma guarda desta criança,
para que serve cada dado e por quanto tempo ele fica — o catálogo declarado das tabelas de
LGPD, dito a quem responde pelo Guerreiro(a) e a mais ninguém.

## Requirements

### Requirement: O núcleo declara o que guarda de um Guerreiro(a), com finalidade e prazo

O núcleo SHALL responder, para um Guerreiro(a), a lista dos **dados armazenados** dele, cada um
com a **finalidade** e o **prazo de guarda**, em **linguagem simples**. A lista SHALL sair da
tabela de LGPD do PRD-01 §11 e dos prazos do documento 03 §12.2 — é catálogo **declarado**, não
inventário de linhas da base —, e cada dado SHALL indicar se o núcleo **o guarda hoje** daquele
Guerreiro(a), para que a família não leia como armazenado o que não existe. (`RF-13-29`,
PRD-13 §11, documento 03 §12)

A resposta SHALL trazer apenas **dado, finalidade, prazo e se está guardado**: NEVER SHALL
trazer o **conteúdo** de nenhum deles.

#### Scenario: A consulta devolve o catálogo do vinculado

- **WHEN** o responsável consulta os dados armazenados de um vinculado
- **THEN** o núcleo devolve cada dado com a finalidade, o prazo de guarda e se está guardado
  hoje

#### Scenario: O que não existe aparece como não guardado

- **WHEN** o Guerreiro(a) não tem _template_ biométrico, porque a captura não aconteceu ou o
  apagamento já correu
- **THEN** a linha do _template_ aparece como não guardada, e não some da lista

#### Scenario: O catálogo não devolve conteúdo

- **WHEN** o responsável consulta os dados armazenados
- **THEN** a resposta não traz o valor de dado algum — nem nome, nem _template_, nem texto de
  ocorrência, nem produção

### Requirement: A transparência do dado é restrita ao responsável vinculado

O núcleo SHALL responder o catálogo apenas ao **responsável em sessão vinculado** àquele
Guerreiro(a). Responsável sem vínculo vigente SHALL receber **403**, e a recusa NEVER SHALL
revelar dado algum da criança, inclusive se ela existe. Persona de outro papel SHALL receber
**403** na mesma rota. (`RN-13-04`)

#### Scenario: Guerreiro(a) não vinculado é recusado

- **WHEN** um responsável consulta o catálogo de um Guerreiro(a) que não é vinculado a ele
- **THEN** o núcleo responde 403 e não revela dado algum daquela criança

#### Scenario: Outro papel não alcança o catálogo

- **WHEN** um Guerreiro(a), um Mestre ou um Apoiador chama a rota do catálogo
- **THEN** o núcleo responde 403

### Requirement: O que a criança faz sozinha não entra na transparência da família

O catálogo SHALL nomear a **consulta ao assistente** e a **transcrição de apoio escolar** como
dados de acesso **restrito à gestão**, e NEVER SHALL devolver o conteúdo de nenhuma das duas ao
responsável: transparência com a família não é vigilância sobre a criança. (`RN-13-20`,
PRD-13 §11)

#### Scenario: A consulta ao assistente aparece como restrita à gestão

- **WHEN** o responsável consulta os dados armazenados do vinculado
- **THEN** a consulta ao assistente e a transcrição de apoio escolar aparecem com a finalidade e
  o prazo, marcadas como restritas à gestão

#### Scenario: O conteúdo da consulta nunca é servido ao responsável

- **WHEN** o responsável tenta alcançar o texto de uma consulta ao assistente ou de uma
  transcrição de apoio escolar
- **THEN** o núcleo recusa, e nenhuma rota da App 07 o devolve
