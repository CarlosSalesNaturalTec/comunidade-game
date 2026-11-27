## MODIFIED Requirements

### Requirement: O Admin inclui outro Admin e cadastra o responsável com o vínculo

A App 03 SHALL oferecer ao Admin a inclusão manual de outro Admin (`RF-02-05`) e o cadastro de
responsável com o **vínculo** a Guerreiros e Guerreiras já cadastrados, declarando o **grau de
parentesco** em texto livre (`RF-02-06`). A aplicação SHALL impedir o quarto vínculo de um
mesmo Guerreiro(a), respeitando o teto de três responsáveis, e SHALL oferecer a criação de
**credencial de usuário e senha provisória** para o adulto sem conta social (`RF-02-07`).
(`RN-02-02`, `RN-02-08`, invariante 3 do documento 99 §6)

O cadastro do responsável SHALL declarar o **nome** dele, e NEVER SHALL ser enviado sem o
nome: é sobre esse nome que se apoia o consentimento que autoriza a captura da imagem da
criança, e o núcleo o exige de toda aplicação que cadastra responsável. (`RF-02-06`,
`responsavel-e-vinculo`)

O cadastro SHALL oferecer o **e-mail** do responsável como campo **opcional**, declarando que é
o e-mail da conta Google com que ele entrará na App 07. A recusa do e-mail já usado por outra
pessoa SHALL ser dita em linguagem simples, no campo. (`RF-02-06`, `RF-01-92`, decisão do
fundador de 2026-11-27)

Cada vínculo já criado que a aplicação apresenta SHALL identificar o **Guerreiro(a) pelo
nick**, ao lado do grau de parentesco. O parentesco sozinho NEVER SHALL bastar: ele se
repete entre irmãos, e o Admin precisa conferir a quem cada vínculo se refere para saber se
o ato que acabou de praticar está certo. O Guerreiro(a) sem nick gravado SHALL ser
apresentado de modo que a linha continue distinguível. (`RF-02-06`)

#### Scenario: Admin inclui outro Admin

- **WHEN** um Admin em sessão informa nome e e-mail de um novo Admin e confirma
- **THEN** o Admin novo passa a existir, sem nenhum caminho de autocadastro envolvido

#### Scenario: O responsável é cadastrado com o nome dele

- **WHEN** o Admin informa o nome do responsável e confirma o cadastro
- **THEN** o responsável passa a existir com o nome declarado, e o cadastro segue para o
  vínculo

#### Scenario: O responsável é cadastrado com o e-mail da conta Google

- **WHEN** o Admin informa nome e e-mail do responsável e confirma o cadastro
- **THEN** o responsável passa a existir com o e-mail, e pode entrar na App 07 pela conta
  Google desse e-mail

#### Scenario: E-mail já usado é explicado no campo

- **WHEN** o Admin cadastra um responsável com e-mail que já é de outra pessoa
- **THEN** a aplicação explica, no campo do e-mail, que ele já é usado por outro cadastro

#### Scenario: Cadastro sem nome não chega ao núcleo

- **WHEN** o Admin tenta cadastrar um responsável sem informar o nome
- **THEN** a aplicação pede o nome e não envia o cadastro

#### Scenario: Responsável é vinculado com grau de parentesco

- **WHEN** o Admin cadastra um responsável e o vincula a um Guerreiro(a) declarando o
  parentesco
- **THEN** o vínculo passa a existir com o parentesco declarado

#### Scenario: O vínculo confirmado identifica o Guerreiro(a) pelo nick

- **WHEN** o Admin vincula um Guerreiro(a) a um responsável e o vínculo é criado
- **THEN** a linha do vínculo apresenta o nick daquele Guerreiro(a) junto do grau de
  parentesco declarado

#### Scenario: Dois vínculos de mesmo parentesco continuam distinguíveis

- **WHEN** o mesmo responsável é vinculado a dois Guerreiros e Guerreiras, os dois com o
  parentesco "Pai"
- **THEN** as duas linhas se distinguem pelo nick de cada Guerreiro(a), e não aparecem como
  duas linhas iguais

#### Scenario: Guerreiro(a) sem nick gravado não apaga a linha

- **WHEN** o vínculo criado alcança um Guerreiro(a) que ainda não tem nick gravado
- **THEN** a linha permanece visível e sinaliza a ausência do nick, sem sumir nem ficar
  reduzida ao parentesco sozinho

#### Scenario: Quarto responsável é barrado

- **WHEN** o Admin tenta vincular um quarto responsável ao mesmo Guerreiro(a)
- **THEN** a aplicação explica o teto de três e o vínculo não é criado

#### Scenario: Adulto sem conta social recebe senha provisória

- **WHEN** o Admin cria credencial de usuário e senha provisória para um adulto cadastrado
- **THEN** a aplicação exibe a senha provisória uma vez, para entrega, e não a recupera depois

### Requirement: A gestão apresenta os responsáveis cadastrados e retoma o vínculo de um deles

A App 03 SHALL apresentar, na sub-área **Responsáveis**, os responsáveis já cadastrados que o
núcleo lhe serve, cada um com o **nome** e com os Guerreiros e Guerreiras vinculados por
**nick**, **nome** e **grau de parentesco**. Responsável **sem vínculo** SHALL aparecer na
lista, sinalizado como tal — é o cadastro interrompido, e é o que a lista existe para revelar.
Vinculado sem nick ou sem nome SHALL ter a ausência sinalizada, sem sumir da linha.
(`RF-02-111`, decisão de exibição do fundador de 2026-11-26)

A aplicação SHALL oferecer, a partir de um responsável da lista, **vincular outro
Guerreiro(a)** a ele, declarando o grau de parentesco, sem exigir novo cadastro. O teto de
três responsáveis por Guerreiro(a) SHALL continuar a ser explicado quando o núcleo o recusar.
(`RF-02-111`, `RF-02-06`, `RN-02-08`, invariante 3 do documento 99 §6)

Cada linha SHALL apresentar o **acesso** do responsável: o e-mail do login social e o usuário
da credencial de usuário e senha, quando existem, e a indicação de **sem acesso** quando nenhum
dos dois existe. A lista NEVER SHALL apresentar senha, nem imagem real, nascimento ou contato
do Guerreiro(a). (`RF-02-111`, `RF-01-92`, decisão do fundador de 2026-11-27) A tela SHALL exibir o aviso de coleta
que toda tela de dado pessoal da gestão já exibe. (`RF-02-111`, `RF-02-64`, `RN-02-22`,
`RN-02-23`)

#### Scenario: A sub-área Responsáveis apresenta quem já está cadastrado

- **WHEN** o Admin abre a sub-área Responsáveis
- **THEN** vê os responsáveis cadastrados, cada um com o nome e com os vinculados por nick,
  nome e grau de parentesco

#### Scenario: Cadastro interrompido aparece sinalizado

- **WHEN** existe responsável cadastrado sem nenhum vínculo
- **THEN** ele aparece na lista, marcado como sem Guerreiro(a) vinculado

#### Scenario: O Admin retoma um responsável e vincula outro Guerreiro(a)

- **WHEN** o Admin escolhe um responsável da lista e vincula um Guerreiro(a) declarando o
  grau de parentesco
- **THEN** o vínculo é criado e passa a constar entre os vinculados daquele responsável, sem
  que um novo responsável tenha sido cadastrado

#### Scenario: O teto de três continua explicado na retomada

- **WHEN** o Admin retoma um responsável e tenta vinculá-lo a um Guerreiro(a) que já tem três
  responsáveis vigentes
- **THEN** a aplicação explica o teto de três e o vínculo não é criado

#### Scenario: Lista vazia é dita, não some

- **WHEN** nenhum responsável foi cadastrado ainda
- **THEN** a tela diz que não há cadastro e continua oferecendo cadastrar um

#### Scenario: A linha mostra como o responsável entra

- **WHEN** o Admin lê a lista e um responsável tem e-mail e usuário de acesso
- **THEN** a linha dele apresenta o e-mail e o usuário

#### Scenario: Responsável sem acesso é sinalizado

- **WHEN** um responsável não tem e-mail nem usuário de acesso
- **THEN** a linha dele o marca como sem acesso

#### Scenario: A lista não expõe credencial nem dado civil da criança

- **WHEN** o Admin lê a lista
- **THEN** nenhuma linha traz senha, nem imagem real, nascimento ou contato de Guerreiro(a)

## ADDED Requirements

### Requirement: O Admin edita a ficha do responsável

A App 03 SHALL oferecer ao Admin, a partir de um responsável da lista, **editar a ficha**:
**nome** e **e-mail**, apresentados com o valor vigente. Esvaziar o e-mail SHALL ser declarado
como retirada do acesso pela conta Google, sem tocar a credencial de usuário e senha. As
recusas do núcleo SHALL ser ditas em linguagem simples, no campo. Ao salvar, a lista volta
atualizada. (`RF-02-121`, `RF-01-92`)

#### Scenario: O Admin corrige o nome do responsável

- **WHEN** o Admin abre a ficha de um responsável, altera o nome e salva
- **THEN** a lista volta com o nome novo, e os vinculados seguem os mesmos

#### Scenario: O Admin dá o acesso pela conta Google

- **WHEN** o Admin grava o e-mail de um responsável que não tinha
- **THEN** a lista volta mostrando o e-mail na coluna de acesso dele

#### Scenario: A retirada do e-mail é declarada antes de salvar

- **WHEN** o Admin esvazia o e-mail na ficha
- **THEN** a tela declara que o responsável deixará de entrar pela conta Google, e ao salvar o
  e-mail some da coluna de acesso

#### Scenario: Nome em branco não chega ao núcleo

- **WHEN** o Admin esvazia o nome e tenta salvar
- **THEN** a aplicação pede o nome e não envia a alteração
