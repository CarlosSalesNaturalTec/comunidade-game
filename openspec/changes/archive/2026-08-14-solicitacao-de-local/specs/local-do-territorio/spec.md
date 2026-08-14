## MODIFIED Requirements

### Requirement: Admin cadastra o local, e o local não nasce de outra origem nesta entrega

O núcleo SHALL permitir que o local nasça de **duas origens, e de nenhuma outra**: o
**cadastro direto por Admin** e a **aprovação de solicitação de novo local** do Guerreiro(a),
avaliada por um Admin ou pelo **Mestre autor da trilha** do desafio de origem. No cadastro
direto, apenas um Admin SHALL cadastrar local, e persona de qualquer outro papel SHALL receber
**403**. As duas origens SHALL gravar o local sob as **mesmas regras de hierarquia** — pai do
nível imediatamente acima, da mesma comunidade, e apenas o nível `comunidade` sem pai. O pedido
do Guerreiro(a), enquanto não aprovado, NEVER SHALL criar local. (`RF-08-04`, `RF-08-22`,
`RF-08-23`, `RN-08-18`, PRD-08 §§5.3, 8)

#### Scenario: Persona que não é Admin não cadastra local

- **WHEN** um Mestre, um Guerreiro(a), um responsável ou um Apoiador tenta cadastrar local
  diretamente
- **THEN** o núcleo recusa com **403**, e nenhum local é criado

#### Scenario: A comunidade nasce sem local e ganha os que o Admin cadastra

- **WHEN** um Admin cria a comunidade e depois cadastra os locais do território
- **THEN** a consulta à comunidade devolve, antes do cadastro, nenhum local, e depois dele,
  os locais cadastrados na hierarquia

#### Scenario: Aprovação de solicitação é a segunda origem do local

- **WHEN** um Admin ou o Mestre autor da trilha do desafio de origem aprova uma solicitação de
  novo local
- **THEN** o núcleo cria o local na hierarquia da comunidade da solicitação, com o nível e o
  rótulo pedidos, sob as mesmas regras de hierarquia do cadastro direto

#### Scenario: Local criado pela aprovação obedece à hierarquia

- **WHEN** a aprovação informa local pai de nível que não é o imediatamente acima ou de outra
  comunidade
- **THEN** o núcleo recusa com **422**, e nenhum local é criado — a origem muda quem cria,
  nunca o que vale para o local
