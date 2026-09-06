## ADDED Requirements

### Requirement: A gestão apresenta as personas em tabela

A App 03 SHALL apresentar em **tabela** as listas de Mestres, de Apoiadores e de Guerreiros e
Guerreiras da área Personas, com as colunas que o núcleo já serve para cada papel. A tabela de
adultos SHALL trazer uma coluna de **nick** que, quando vazia, declara que a pessoa **não
aparece em superfície pública**, sem NEVER sugerir nick algum. (`RF-02-01`, `RN-14-10`,
`RN-01-30`)

#### Scenario: Os Mestres cadastrados aparecem

- **WHEN** o Admin abre Personas e escolhe Mestres
- **THEN** vê em tabela os Mestres cadastrados, com nome, e-mail e nick

#### Scenario: Quem está sem nick é sinalizado sem sugestão

- **WHEN** um adulto cadastrado ainda não tem nick
- **THEN** a coluna de nick declara que ele não aparece em superfície pública, e nenhum nick é
  proposto pela tela

#### Scenario: Nenhum cadastro ainda

- **WHEN** o papel escolhido não tem nenhum cadastro
- **THEN** a área diz que não há cadastro, em vez de apresentar tabela vazia sem explicação

### Requirement: A gestão abre a ficha do adulto com os artefatos comprobatórios

A App 03 SHALL abrir, a partir da linha de um Mestre ou de um Apoiador, uma **ficha de
leitura** com nome, e-mail, WhatsApp, nick e os **artefatos comprobatórios** que sustentaram o
cadastro, cada um com **rótulo** e **endereço**, o endereço alcançável como link. A ficha NEVER
SHALL oferecer edição de nome, e-mail, WhatsApp ou artefato, nem alteração de papel.
(`RF-02-02`, `RF-02-03`, `RF-02-04`, `RN-02-01`)

#### Scenario: A prova do cadastro é conferível

- **WHEN** o Admin abre a ficha de um Mestre cadastrado
- **THEN** vê cada artefato comprobatório dele com o rótulo e o endereço, e alcança o endereço
  a partir da própria ficha

#### Scenario: A ficha não edita o cadastro

- **WHEN** o Admin percorre a ficha de um Mestre ou de um Apoiador
- **THEN** não lhe é oferecido campo algum para alterar nome, e-mail, WhatsApp, artefato ou
  papel

#### Scenario: A ficha oferece gravar o nick que falta

- **WHEN** o Admin abre a ficha de um adulto que está sem nick
- **THEN** lhe é oferecido gravar o nick que a pessoa passou por fora, sem que nenhum nick seja
  sugerido
