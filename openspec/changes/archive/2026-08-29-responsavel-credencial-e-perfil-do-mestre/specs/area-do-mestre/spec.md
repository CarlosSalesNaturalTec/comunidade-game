## ADDED Requirements

### Requirement: O Mestre cadastra o responsável que se apresentou no encontro

A App 09 SHALL oferecer ao Mestre em sessão o cadastro da persona de **responsável**, com o
**nome** dela. A tela SHALL declarar que o cadastro pressupõe que o responsável **se apresentou
pessoalmente**, e a aplicação NEVER SHALL oferecer caminho de cadastro à distância — solicitação,
convite ou autocadastro do responsável. A tela NEVER SHALL exigir e-mail, documento ou
digitalização do termo: são atos da gestão, na App 03. O responsável SHALL ser a **única**
persona que a App 09 cadastra. (`RF-09-62`, `RN-09-15`, invariante 3 do documento 99 §6)

#### Scenario: O Mestre cadastra o responsável

- **WHEN** o Mestre informa o nome do responsável apresentado no encontro e confirma
- **THEN** a aplicação cadastra a persona de responsável e segue para o vínculo

#### Scenario: A tela declara a apresentação presencial

- **WHEN** o Mestre abre o cadastro de responsável
- **THEN** a tela declara que o cadastro pressupõe a apresentação pessoal do responsável

#### Scenario: Cadastro sem nome é recusado em linguagem simples

- **WHEN** o Mestre confirma o cadastro sem informar o nome
- **THEN** a aplicação aponta o campo em falta, em linguagem simples, e nada é cadastrado

#### Scenario: A App 09 não cadastra outra persona

- **WHEN** o Mestre percorre a área de responsáveis
- **THEN** não lhe é oferecido cadastrar Guerreiro(a), Mestre, Apoiador nem Admin

### Requirement: O Mestre vincula os Guerreiros e Guerreiras declarando o parentesco

A App 09 SHALL permitir que o Mestre vincule ao responsável recém-cadastrado os Guerreiros e
Guerreiras **já ativos** que ele pode alcançar, escolhidos numa lista servida pelo núcleo e
apresentada por **nick e avatar**. Cada vínculo SHALL exigir o **grau de parentesco em texto
livre**, e o grau SHALL ser declarado **por vínculo**, ainda que o mesmo responsável seja
vinculado a mais de uma criança. A aplicação NEVER SHALL exibir imagem real de Guerreiro(a) nem
oferecer caminho para criar a persona da criança a partir daqui. (`RF-09-62`, `RF-09-63`,
`RN-09-18`, invariante 12 do documento 99 §6)

#### Scenario: O vínculo é criado com o grau declarado

- **WHEN** o Mestre escolhe um Guerreiro(a) da lista e informa o grau de parentesco
- **THEN** a aplicação cria o vínculo com aquele grau e o apresenta entre os já criados

#### Scenario: Cada vínculo tem o seu grau

- **WHEN** o Mestre vincula o mesmo responsável a dois Guerreiros e Guerreiras
- **THEN** cada vínculo pede e guarda o seu grau, sem que um herde o do outro

#### Scenario: Vínculo sem grau de parentesco é recusado

- **WHEN** o Mestre tenta vincular sem informar o grau de parentesco
- **THEN** a aplicação aponta o campo em falta e nenhum vínculo é criado

#### Scenario: A escolha do Guerreiro(a) é por nick e avatar

- **WHEN** o Mestre abre a lista de quem pode vincular
- **THEN** vê nick e avatar de cada Guerreiro(a), e nenhuma imagem real

### Requirement: O quarto vínculo é recusado em linguagem simples

A App 09 SHALL apresentar a recusa do **quarto** vínculo de responsável ao mesmo Guerreiro(a)
como o que é — o teto de três por criança —, em linguagem simples, sem código nem jargão. A
aplicação NEVER SHALL contar os vínculos por conta própria para bloquear a tela antes de tentar:
o teto é conferido pelo núcleo. Os três vínculos vigentes SHALL continuar válidos depois da
recusa, e o vínculo recusado NEVER SHALL desfazer o cadastro do responsável já criado.
(`RF-09-64`, `RN-09-15`, PRD-09 §12)

#### Scenario: O quarto vínculo é recusado com a razão dita

- **WHEN** o Mestre tenta vincular um responsável a um Guerreiro(a) que já tem três vínculos
  vigentes
- **THEN** a aplicação informa que a criança já tem o teto de três responsáveis, e o vínculo não
  é criado

#### Scenario: A recusa não perde o que já foi feito

- **WHEN** o quarto vínculo é recusado depois de o responsável já ter sido cadastrado
- **THEN** o responsável cadastrado permanece, os vínculos já criados permanecem, e o Mestre
  segue de onde estava

### Requirement: O Mestre cria a credencial provisória do responsável sem conta Google

A App 09 SHALL permitir que o Mestre crie, para o responsável que acabou de cadastrar, a
**credencial de usuário e senha provisória** destinada a quem não tem conta Google. A aplicação
SHALL exibir a senha provisória **uma única vez**, para entrega em mãos, SHALL avisar que ela não
volta a aparecer e NEVER SHALL oferecer caminho para recuperá-la ou reexibi-la. A aplicação NEVER
SHALL enviar a credencial por e-mail nem por mensageria. O caminho SHALL ser **opcional**: o
responsável com conta Google é cadastrado e vinculado sem credencial alguma. (`RF-09-65`,
`RN-09-23`, documento 03 §1.1)

#### Scenario: A senha provisória aparece uma vez

- **WHEN** o Mestre cria a credencial informando o usuário do responsável
- **THEN** a aplicação mostra a senha provisória com o aviso de que ela não aparece de novo

#### Scenario: A senha não se recupera

- **WHEN** o Mestre sai da tela depois de ver a senha provisória
- **THEN** não lhe é oferecido caminho algum para reexibir ou recuperar aquela senha

#### Scenario: O responsável com conta Google dispensa a credencial

- **WHEN** o Mestre conclui o cadastro e o vínculo sem criar credencial
- **THEN** a aplicação encerra o fluxo normalmente, sem exigir usuário nem senha

### Requirement: O Mestre publica a prova da própria habilidade

A App 09 SHALL oferecer ao Mestre em sessão a área do **próprio perfil**, onde ele publica
**currículo, portfólio, redes sociais e artefatos comprobatórios** da sua habilidade. Cada um
SHALL ser declarado como **endereço e rótulo** — link, nunca upload de arquivo —, e a aplicação
NEVER SHALL oferecer campo de anexo nesta área. A área SHALL apresentar os artefatos declarados
por Admin no cadastro dele em **leitura**, marcados como tais, e SHALL oferecer a remoção apenas
dos que o próprio Mestre publicou. (`RF-09-66`, `RN-02-01`, documento 02 §1)

#### Scenario: O Mestre publica o currículo

- **WHEN** o Mestre acrescenta ao perfil um artefato com endereço e rótulo
- **THEN** a aplicação o publica e ele passa a constar da prova de habilidade dele

#### Scenario: A área não aceita arquivo

- **WHEN** o Mestre abre a área do próprio perfil
- **THEN** só lhe são oferecidos os campos de endereço e rótulo, e nenhum campo de anexo

#### Scenario: O artefato do cadastro fica, marcado

- **WHEN** o perfil traz artefatos declarados por Admin no cadastro do Mestre
- **THEN** eles aparecem marcados como declarados no cadastro, sem caminho de remoção

#### Scenario: O Mestre remove o que ele mesmo publicou

- **WHEN** o Mestre remove um artefato que ele publicou
- **THEN** ele deixa de constar do perfil, e os demais permanecem

### Requirement: A App 09 não cadastra Mestre nem cria acesso de Mestre

A App 09 NEVER SHALL oferecer caminho para **cadastrar Mestre**, criar acesso de Mestre,
convidar outro Mestre ou alterar o papel de qualquer persona. A área do perfil SHALL declarar
que o cadastro de Mestre é ato exclusivo de Admin, com habilidade comprovada, e que a
aplicação alcança apenas a prova de habilidade e a identidade do próprio Mestre. A aplicação
NEVER SHALL oferecer ao Mestre a edição do próprio nome, e-mail ou papel. (`RF-09-67`,
`RN-09-14`, invariante 3 do documento 99 §6)

#### Scenario: Não há caminho para cadastrar Mestre

- **WHEN** o Mestre percorre todas as áreas da App 09
- **THEN** em nenhuma delas lhe é oferecido cadastrar Mestre ou criar acesso de Mestre

#### Scenario: O perfil declara de quem é o cadastro

- **WHEN** o Mestre abre a área do próprio perfil
- **THEN** lê que o cadastro de Mestre é exclusivo de Admin, com habilidade comprovada

#### Scenario: O Mestre não edita o próprio cadastro

- **WHEN** o Mestre percorre a área do próprio perfil
- **THEN** não lhe é oferecido campo algum para alterar nome, e-mail ou papel — a área só
  alcança os artefatos comprobatórios

### Requirement: Toda tela da App 09 que grava dado pessoal avisa o que ali se coleta

A App 09 SHALL exibir um **aviso discreto** do que está sendo coletado em toda tela em que grava
dado pessoal — o cadastro do responsável e o vínculo; o perfil do próprio Mestre; o conteúdo
autoral da missão; a conferência de presença; o lançamento do desfecho da atividade; a
ocorrência de conduta; e a validação da criação original. Cada aviso SHALL nomear o dado
**daquela** tela, na linha correspondente da tabela do PRD-09 §11, e SHALL oferecer o acesso à
área detalhada de direitos. O aviso NEVER SHALL bloquear a tela, NEVER SHALL exigir confirmação
para continuar e NEVER SHALL impedir o envio do formulário. (`RF-09-68`, PRD-09 §11,
documento 03 §12)

#### Scenario: A tela de cadastro do responsável traz o aviso

- **WHEN** o Mestre abre o cadastro do responsável
- **THEN** um aviso discreto informa o que aquela tela coleta e dá acesso à área detalhada

#### Scenario: O aviso nomeia o dado daquela tela

- **WHEN** o Mestre abre a ocorrência de conduta ou o lançamento do desfecho da atividade
- **THEN** o aviso nomeia o dado daquela tela, e não o de outra

#### Scenario: O aviso não atrapalha o uso

- **WHEN** o aviso está exibido numa tela de cadastro, de lançamento ou de validação
- **THEN** o Mestre preenche e envia o formulário sem confirmar o aviso, e nada fica bloqueado

### Requirement: A App 09 abre a área Direitos e dados, em leitura

A App 09 SHALL oferecer a área **Direitos e dados**, alcançável pela navegação e por **todo**
aviso de coleta, que apresenta, para cada dado que o Mestre coleta, a **finalidade**, a **base
legal**, o **prazo de retenção** e **quem acessa**, conforme a tabela do PRD-09 §11. A área SHALL
declarar também que o Mestre **não vê imagem real de Guerreiro(a)** em tela alguma, que a criação
original só vai à vitrine com autorização do responsável, que a pontuação negativa fica restrita
à gestão e ao responsável daquele Guerreiro(a), e que o pedido de acesso, correção ou exclusão
chega pela App 07 e é tratado pela gestão. A área é de **leitura**: NEVER SHALL oferecer escrita,
exclusão ou exportação de dado. (`RF-09-68`, `RN-09-18`, `RN-09-19`, PRD-09 §11)

#### Scenario: A área apresenta o destino de cada dado

- **WHEN** o Mestre abre a área Direitos e dados
- **THEN** vê, para cada dado coletado, a finalidade, a base legal, o prazo de retenção e quem
  acessa

#### Scenario: O aviso leva à área

- **WHEN** o Mestre aciona o acesso à área detalhada a partir do aviso de uma tela que coleta
- **THEN** chega à área Direitos e dados

#### Scenario: A área é só de leitura

- **WHEN** o Mestre lê a área Direitos e dados
- **THEN** não lhe é oferecida escrita, exclusão nem exportação de dado, e o pedido de direitos
  é declarado como caminho da App 07
