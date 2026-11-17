## MODIFIED Requirements

### Requirement: O Admin cadastra e edita o Guerreiro(a) pela aplicação

A App 03 SHALL oferecer ao Admin o cadastro de Guerreiro(a) com nome, data de nascimento e nick,
e a edição do que já foi cadastrado. O formulário NEVER SHALL pedir o avatar: no cadastro, a
aplicação SHALL gravar um **avatar sorteado** do catálogo fechado da camada comum; na edição,
SHALL preservar o avatar já gravado e, só quando não houver nenhum, gravar um sorteado. Quem
troca o avatar é o próprio Guerreiro(a), na App 05. A aplicação SHALL apontar o campo em falta
antes de chamar o núcleo e SHALL apresentar em linguagem simples a recusa por nick em uso, **sem
dizer de quem é o nick**. A aplicação NEVER SHALL exibir a imagem do Guerreiro(a): a
representação é o avatar. (`RF-02-01`, `RN-02-22`, `RN-02-23`, invariante 12 do documento 99
§6, PRD-02 §11, documento 15 §7)

#### Scenario: Admin cadastra o Guerreiro(a)

- **WHEN** um Admin em sessão informa nome, nascimento e nick, escolhe a aula e confirma
- **THEN** o Guerreiro(a) passa a existir com um avatar sorteado do catálogo, e a aplicação o
  apresenta entre os cadastrados

#### Scenario: O formulário não pede avatar

- **WHEN** um Admin abre o cadastro ou a edição de um Guerreiro(a)
- **THEN** o formulário não tem campo de avatar, e o aviso de coleta cita só nome, data de
  nascimento e nick

#### Scenario: A edição preserva o avatar gravado

- **WHEN** um Admin corrige o nome de um Guerreiro(a) que já tem avatar e confirma
- **THEN** a aplicação reenvia o mesmo avatar, e o desenho do Guerreiro(a) não muda

#### Scenario: Guerreiro(a) sem avatar recebe um sorteado na edição

- **WHEN** um Admin edita um Guerreiro(a) sem avatar gravado e confirma
- **THEN** a aplicação envia um avatar sorteado do catálogo, e o núcleo não recusa por avatar em
  falta

#### Scenario: Nick em uso é explicado sem revelar o dono

- **WHEN** o núcleo recusa o cadastro porque o nick já está em uso
- **THEN** a aplicação pede outro nick, sem informar quem o usa nem de que papel

#### Scenario: A gestão não vê a imagem da criança

- **WHEN** um Admin abre o cadastro de um Guerreiro(a)
- **THEN** a tela mostra avatar e nick, e nenhuma imagem real aparece
