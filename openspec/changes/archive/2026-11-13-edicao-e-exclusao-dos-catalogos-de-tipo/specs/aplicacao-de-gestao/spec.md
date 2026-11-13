## ADDED Requirements

### Requirement: O Admin altera o tipo de recurso pela aplicação

A App 03 SHALL oferecer ao **Admin**, em cada tipo de recurso da área Catálogos, o caminho
**Editar**, que abre o formulário com os valores atuais e permite alterar o **nome**, a
**unidade** e a marca de **exige comprovante**. A **natureza** SHALL ser apresentada como
leitura, e NEVER SHALL ser oferecida para alteração.

O mesmo caminho SHALL permitir abrir **vigência nova** do **valor em moedas** e do **preço em
pontos extras**, cada um com o seu **início de vigência**, e SHALL apresentar o valor e o preço
vigentes de que se parte. A aplicação SHALL dizer que a vigência nova **não reescreve** a
anterior — ela se encerra no dia de início da nova. Abrir vigência é **opcional** em cada régua:
a edição que só corrige o nome NEVER SHALL abrir vigência alguma.

A recusa do núcleo — nome ou unidade em branco, valor negativo ou com mais de duas casas, preço
fracionário ou abaixo do piso — SHALL ser apresentada **em linguagem simples**, no campo que a
originou, e nada SHALL ser apresentado como alterado. O caminho NEVER SHALL ser oferecido a
quem não é Admin (`RN-02-20`), e a escrita bem-sucedida SHALL aparecer na trilha de auditoria
com autor, papel, data e hora (`RN-02-21`). (`RF-02-113`, `RF-07-51`, `RF-07-02`, `RF-07-43`,
`RF-07-44`, `RN-07-04`)

#### Scenario: Admin corrige o nome do tipo

- **WHEN** um Admin em sessão edita um tipo de recurso, altera o nome e confirma
- **THEN** a lista passa a apresentar o nome novo, e nenhuma vigência é aberta

#### Scenario: A natureza aparece sem poder ser alterada

- **WHEN** o Admin abre a edição de um tipo de recurso
- **THEN** a natureza aparece como leitura, sem campo que a altere

#### Scenario: Admin abre vigência nova do valor

- **WHEN** o Admin informa valor em moedas novo com início de vigência e confirma
- **THEN** a lista passa a apresentar o valor novo a partir do dia de início, e a aplicação disse
  que a vigência anterior se encerra nesse dia

#### Scenario: Preço abaixo do piso é recusado no campo

- **WHEN** o Admin informa preço em pontos extras menor que o piso e confirma
- **THEN** a aplicação apresenta a recusa em linguagem simples, no campo do preço, e nada é
  apresentado como alterado

#### Scenario: Quem não é Admin não alcança a edição

- **WHEN** um Mestre em sessão abre a área Catálogos
- **THEN** o caminho Editar não lhe é oferecido em tipo algum

### Requirement: O Admin altera o tipo de coleta pela aplicação

A App 03 SHALL oferecer ao **Admin**, em cada tipo de coleta da área Catálogos, o caminho
**Editar**, que abre o formulário de tipo de coleta com os valores atuais e permite alterar
**todos os campos** — nome, forma de registro, unidade e faixa esperada —, sob as mesmas regras
de apresentação do cadastro: forma escolhida entre as três, unidade e faixa exigidas só na forma
**número** e retiradas ao trocar para **foto** ou **vídeo**.

Ao trocar a **forma de registro** de um tipo, a aplicação SHALL avisar, antes de confirmar, que
os registros já gravados não mudam e que os registros novos dos desafios que usam o tipo passam
a seguir a forma nova. A recusa do núcleo SHALL ser apresentada **em linguagem simples**, no
campo que a originou, e nada SHALL ser apresentado como alterado. O caminho NEVER SHALL ser
oferecido a quem não é Admin (`RN-02-20`), e a escrita bem-sucedida SHALL aparecer na trilha de
auditoria (`RN-02-21`). (`RF-02-114`, `RF-08-32`, `RF-08-05`, `RF-08-12`)

#### Scenario: Admin altera a faixa esperada

- **WHEN** um Admin em sessão edita um tipo de coleta por número, altera a faixa e confirma
- **THEN** a lista passa a apresentar a faixa nova

#### Scenario: Trocar a forma avisa do efeito nos desafios

- **WHEN** o Admin troca a forma de registro de um tipo de coleta na edição
- **THEN** a aplicação avisa que os registros gravados não mudam e que os registros novos seguem
  a forma nova, antes de deixar confirmar

#### Scenario: Trocar para foto retira unidade e faixa

- **WHEN** o Admin troca a forma de um tipo por número para foto
- **THEN** a aplicação deixa de pedir unidade e faixa, e o tipo é gravado sem as duas

### Requirement: O Admin desativa, reativa e exclui o tipo pela aplicação

A App 03 SHALL oferecer ao **Admin**, em cada tipo de **recurso** e de **coleta** da área
Catálogos, **Desativar** quando o tipo está ativo e **Reativar** quando está desativado, e
**Excluir** em qualquer dos dois estados. A aplicação SHALL dizer, junto de Desativar, que o tipo
deixa de ser oferecido em escolha nova e que nada do que já existe com ele muda.

Excluir SHALL pedir **confirmação** antes de chamar o núcleo, dizendo que só se exclui tipo
nunca usado. Recusada a exclusão por **uso**, a aplicação SHALL apresentar a recusa **em
linguagem simples**, dizendo que o tipo está em uso e que pode ser desativado, e o tipo SHALL
seguir na lista. Excluído o tipo, ele SHALL sair da lista.

O caminho NEVER SHALL ser oferecido a quem não é Admin (`RN-02-20`), e a escrita bem-sucedida
SHALL aparecer na trilha de auditoria (`RN-02-21`). (`RF-02-115`, `RF-07-52`, `RN-07-40`,
`RF-08-32`, `RN-08-30`)

#### Scenario: Admin desativa um tipo de recurso

- **WHEN** um Admin em sessão desativa um tipo de recurso ativo
- **THEN** a lista passa a apresentar o tipo assinalado como inativo, com o caminho Reativar

#### Scenario: Admin reativa um tipo de coleta

- **WHEN** um Admin em sessão reativa um tipo de coleta desativado
- **THEN** a lista passa a apresentar o tipo como ativo

#### Scenario: A exclusão pede confirmação

- **WHEN** o Admin escolhe Excluir em um tipo
- **THEN** a aplicação pede confirmação, dizendo que só se exclui tipo nunca usado, e nada é
  enviado ao núcleo sem ela

#### Scenario: Tipo em uso não é excluído

- **WHEN** o Admin confirma a exclusão de um tipo que o núcleo recusa por estar em uso
- **THEN** a aplicação diz, em linguagem simples, que o tipo está em uso e pode ser desativado,
  e o tipo segue na lista

#### Scenario: Tipo nunca usado sai da lista

- **WHEN** o Admin confirma a exclusão de um tipo nunca usado
- **THEN** o tipo sai da lista

#### Scenario: Quem não é Admin não alcança desativar nem excluir

- **WHEN** um Mestre em sessão abre a área Catálogos
- **THEN** nenhum dos caminhos Desativar, Reativar e Excluir lhe é oferecido

### Requirement: Os seletores de escolha nova da App 03 não oferecem tipo de recurso desativado

Os seletores de tipo de recurso em que o Admin **escolhe** um tipo para um fato novo — o
agendamento da aula, o registro de aporte e a homologação da declaração de aporte — NEVER SHALL
oferecer tipo **desativado**. As telas que só **leem** o tipo pelo nome — extrato do ponto de
apoio, acervo, saldo e necessidades — SHALL seguir apresentando o nome do tipo desativado.
(`RF-07-52`, `RF-02-115`, `RF-02-31`, `RF-02-57`, `RF-02-84`)

#### Scenario: O agendamento não oferece tipo desativado

- **WHEN** o Admin abre o agendamento da aula e há um tipo de recurso desativado
- **THEN** o tipo desativado não aparece entre os recursos que a aula pode declarar

#### Scenario: O saldo de tipo desativado segue com nome

- **WHEN** um ponto de apoio tem saldo de um tipo de recurso desativado
- **THEN** o saldo aparece com o nome e a unidade do tipo, como antes

## MODIFIED Requirements

### Requirement: A área Catálogos apresenta os tipos de recurso com o valor vigente

A App 03 SHALL apresentar cada **tipo de recurso** com **nome**, **natureza**, **unidade**, a
marca de **exige comprovante**, o **valor em moedas vigente** na data da consulta e a indicação
de estar **ativo**. O tipo **desativado** SHALL sair assinalado como tal, por rótulo textual e
nunca só por cor, como já sai o tipo de coleta.

O núcleo devolve apenas o tipo com **valor de referência vigente na data**. A aplicação SHALL
informar, junto da lista, que é isso que ela mostra, para que o tipo cadastrado com vigência
futura não seja lido como cadastro perdido. (`RF-02-107`, `RF-02-115`, `RF-07-01`, `RF-07-02`,
`RF-07-52`)

#### Scenario: A lista traz o valor da vigência corrente

- **WHEN** o adulto em sessão abre a área Catálogos e há tipos de recurso com valor vigente
- **THEN** a aplicação apresenta cada tipo com nome, natureza, unidade, a marca de exige
  comprovante, o valor em moedas da vigência corrente e a indicação de estar ativo

#### Scenario: O tipo desativado aparece assinalado

- **WHEN** o catálogo tem um tipo de recurso desativado
- **THEN** a aplicação o apresenta assinalado como inativo, por texto

#### Scenario: A lista diz que mostra apenas o que tem valor vigente

- **WHEN** a área apresenta o catálogo de tipos de recurso
- **THEN** a aplicação informa que a lista traz os tipos com valor de referência vigente na data
