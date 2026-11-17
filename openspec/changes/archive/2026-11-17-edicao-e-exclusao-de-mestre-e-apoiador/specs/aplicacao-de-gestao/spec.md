## MODIFIED Requirements

### Requirement: A gestão apresenta as personas em tabela

A App 03 SHALL apresentar em **tabela** as listas de Mestres, de Apoiadores e de Guerreiros e
Guerreiras da área Personas, com as colunas que o núcleo já serve para cada papel. A tabela de
adultos SHALL trazer uma coluna de **nick** que, quando vazia, declara que a pessoa **não
aparece em superfície pública**, sem NEVER sugerir nick algum, e SHALL **marcar o adulto
desativado**. (`RF-02-01`, `RN-14-10`, `RN-01-30`, `RF-02-119`)

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

#### Scenario: O desativado aparece marcado

- **WHEN** a lista traz um Apoiador desativado
- **THEN** a linha dele declara que está desativado

### Requirement: A gestão abre a ficha do adulto com os artefatos comprobatórios

A App 03 SHALL abrir, a partir da linha de um Mestre ou de um Apoiador, uma **ficha** com nome,
e-mail, WhatsApp, nick e os **artefatos comprobatórios** que sustentaram o cadastro, cada um com
**rótulo** e **endereço**, o endereço alcançável como link. A ficha SHALL oferecer ao Admin
**editar** nome, e-mail e WhatsApp e **incluir, corrigir e remover** artefato, com as recusas do
núcleo apresentadas no próprio formulário. A ficha NEVER SHALL oferecer alteração de nick já
gravado, de papel nem dos termos de doação. (`RF-02-02`, `RF-02-03`, `RF-02-04`, `RN-02-01`,
`RF-02-117`)

#### Scenario: A prova do cadastro é conferível

- **WHEN** o Admin abre a ficha de um Mestre cadastrado
- **THEN** vê cada artefato comprobatório dele com o rótulo e o endereço, e alcança o endereço
  a partir da própria ficha

#### Scenario: O Admin corrige o cadastro

- **WHEN** o Admin edita o WhatsApp de um Apoiador na ficha e salva
- **THEN** a ficha passa a mostrar o valor novo

#### Scenario: A recusa do último artefato aparece na ficha

- **WHEN** o Admin tenta remover o único artefato de um Mestre
- **THEN** a ficha mostra a recusa e o artefato continua listado

#### Scenario: A ficha não troca nick nem papel

- **WHEN** o Admin percorre a ficha de um adulto com nick
- **THEN** não lhe é oferecido campo para alterar o nick, o papel ou os termos de doação

#### Scenario: A ficha oferece gravar o nick que falta

- **WHEN** o Admin abre a ficha de um adulto que está sem nick
- **THEN** lhe é oferecido gravar o nick que a pessoa passou por fora, sem que nenhum nick seja
  sugerido

### Requirement: A ficha do adulto mostra o artefato de cadastro que o Mestre editou

A App 03 SHALL marcar, na ficha do adulto, o artefato **declarado no cadastro** que o próprio
adulto editou, apresentando o **rótulo e o endereço originais** ao lado dos vigentes. Artefato
nunca editado pelo adulto NEVER SHALL exibir marca nem valor original. A correção feita pelo
Admin NEVER SHALL apagar nem substituir o valor original guardado. (`RF-02-04`, `RN-02-01`,
`RN-09-14`, `RF-02-117`, decisão do fundador de 2026-09-06)

#### Scenario: O Admin vê o que foi mexido

- **WHEN** o Admin abre a ficha de um Mestre que editou um artefato do cadastro
- **THEN** aquele artefato aparece marcado, com o valor original ao lado do vigente

#### Scenario: Artefato intocado aparece limpo

- **WHEN** a ficha traz um artefato que ninguém editou
- **THEN** ele aparece sem marca e sem valor original

#### Scenario: A correção do Admin preserva o original

- **WHEN** o Admin corrige um artefato que o Mestre já havia editado
- **THEN** o valor original segue ao lado do vigente

## ADDED Requirements

### Requirement: A ficha do adulto exclui, desativa e reativa

A ficha do adulto SHALL oferecer ao Admin **excluir**, **desativar** e **reativar**, cada ação
com confirmação. Recusada a exclusão porque o adulto é usado, a ficha SHALL apresentar a recusa e
oferecer a desativação. Excluído, o adulto SHALL sumir da tabela; desativado ou reativado, a
marca da linha e da ficha SHALL acompanhar. (`RF-02-118`, `RF-02-119`, `RN-02-34`, `RN-02-35`)

#### Scenario: Exclusão recusada leva à desativação

- **WHEN** o Admin confirma a exclusão de um Apoiador com aporte
- **THEN** a ficha mostra que ele não pode ser excluído e oferece desativá-lo

#### Scenario: Exclusão confirmada

- **WHEN** o Admin confirma a exclusão de um Mestre nunca usado
- **THEN** a ficha fecha e o Mestre não aparece mais na tabela

#### Scenario: Desativado oferece reativar

- **WHEN** o Admin abre a ficha de um adulto desativado
- **THEN** a ficha declara a desativação e oferece reativar, e não oferece desativar
