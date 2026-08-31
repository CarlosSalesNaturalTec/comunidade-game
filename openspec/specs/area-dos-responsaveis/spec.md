## Purpose

A App 07, porta do responsável: por onde ele entra, o que a aplicação lhe mostra dos Guerreiros
e Guerreiras vinculados a ele, e o que ela deliberadamente não oferece — cadastro, vínculo,
criança de terceiro e o que a criança faz sozinha.

## Requirements

### Requirement: A Área dos responsáveis é inteiramente autenticada e se identifica por chave

A App 07 SHALL apresentar a entrada a quem não tem sessão aberta, e NEVER SHALL servir tela de
dado de criança sem sessão de responsável. Toda chamada ao núcleo SHALL levar a **chave da
própria aplicação** e, havendo sessão, a credencial da persona. (`RF-13-01`, `RF-01-02`,
`RN-01-32`)

#### Scenario: Visitante sem sessão

- **WHEN** alguém abre a App 07 sem sessão aberta
- **THEN** só a entrada é apresentada, e nenhuma tela de dado de criança

#### Scenario: A aplicação se identifica com a própria chave

- **WHEN** a App 07 chama uma rota de dados do núcleo
- **THEN** a chamada leva a chave da App 07, e não a de outra aplicação

### Requirement: O responsável entra por login social ou por usuário e senha da gestão

A App 07 SHALL oferecer os dois caminhos de entrada do responsável: **login social** e
**usuário e senha** criados pela gestão. NEVER SHALL oferecer autocadastro. (`RF-13-01`,
`RN-13-01`)

#### Scenario: Entrada por login social

- **WHEN** um responsável já cadastrado entra por login social
- **THEN** a sessão é aberta e ele alcança as telas da aplicação

#### Scenario: Entrada por usuário e senha

- **WHEN** um responsável já cadastrado entra com o usuário e a senha criados pela gestão
- **THEN** a sessão é aberta e ele alcança as telas da aplicação

#### Scenario: Não há por onde se cadastrar

- **WHEN** o responsável percorre a entrada da aplicação
- **THEN** não há caminho de autocadastro

### Requirement: A senha provisória tranca todas as demais telas

A App 07 SHALL exigir a **troca da senha provisória** antes de qualquer outra tela, e NEVER
SHALL apresentar dado de criança enquanto a troca não acontecer. Não SHALL existir caminho de
contorno da troca. (`RF-13-02`)

#### Scenario: Entrada com senha provisória

- **WHEN** um responsável entra com a senha provisória criada pela gestão
- **THEN** a única tela apresentada é a da troca de senha

#### Scenario: Depois da troca

- **WHEN** o responsável troca a senha provisória
- **THEN** ele alcança a lista dos vinculados

### Requirement: Login não cria cadastro, e a recusa orienta a procurar a gestão

A App 07 SHALL recusar a entrada de conta **sem cadastro prévio** de responsável, e a recusa
SHALL orientar a **procurar a gestão no encontro**. A entrada NEVER SHALL criar persona.
(`RF-13-03`, `RN-13-02`)

#### Scenario: Conta social sem cadastro prévio

- **WHEN** alguém entra por login social com uma conta que não corresponde a responsável
  cadastrado
- **THEN** a entrada é recusada, a tela orienta a procurar a gestão no encontro e nenhuma
  persona é criada

### Requirement: A aplicação lista apenas os vinculados, com o grau de parentesco

A App 07 SHALL apresentar ao responsável **apenas os Guerreiros e Guerreiras vinculados a ele**,
cada um com o **grau de parentesco** declarado no cadastro. NEVER SHALL apresentar criança não
vinculada, nem por busca, nem por endereço direto. (`RF-13-04`, `RN-13-04`)

#### Scenario: A lista traz os vinculados com o parentesco

- **WHEN** um responsável com dois vinculados abre a aplicação
- **THEN** os dois aparecem, cada um com o grau de parentesco declarado

#### Scenario: Criança não vinculada não aparece nem por busca

- **WHEN** o responsável procura por um Guerreiro(a) que não é seu vinculado
- **THEN** a aplicação não o apresenta, e a recusa do núcleo não revela dado algum daquela
  criança

### Requirement: O responsável alterna entre os vinculados sem sair da aplicação

A App 07 SHALL permitir ao responsável com mais de um vinculado **alternar entre eles** sem
encerrar a sessão e sem voltar à entrada. (`RF-13-05`)

#### Scenario: Troca de criança

- **WHEN** o responsável está vendo a evolução de um vinculado e escolhe outro
- **THEN** a aplicação passa a apresentar o segundo, com a mesma sessão

### Requirement: A aplicação não cadastra responsável nem cria ou edita vínculo

A App 07 NEVER SHALL oferecer tela de cadastro de responsável, de criação de vínculo, de edição
de vínculo ou de mudança do grau de parentesco: tudo isso é ato da gestão. (`RF-13-06`,
`RN-13-01`)

#### Scenario: Nenhum caminho de cadastro ou de vínculo

- **WHEN** o responsável percorre todas as telas da aplicação
- **THEN** não há caminho de cadastro de responsável nem de criação, edição ou remoção de
  vínculo

### Requirement: O painel apresenta a evolução do vinculado, com o nível como percurso

A App 07 SHALL apresentar, do vinculado escolhido, **presença, atividades realizadas, pontos,
poderes, badges e nível**, o **progresso de cada trilha como percurso** — o que foi concluído e
o que falta —, e as **criações originais validadas** com título, trilha e data. O nível NEVER
SHALL ser apresentado como saldo de pontos. (`RF-13-07`, `RF-13-08`, `RF-13-10`)

#### Scenario: Painel de um vinculado com histórico

- **WHEN** o responsável abre o painel de um vinculado que tem presença, atividades, pontos,
  poderes, badges, nível, trilha em andamento e criação validada
- **THEN** a tela apresenta todos esses itens, com o progresso da trilha em missões concluídas e
  faltantes

#### Scenario: O nível não é saldo

- **WHEN** a tela apresenta o nível do vinculado
- **THEN** o que o exprime é o percurso da trilha, e não o saldo de pontos

### Requirement: A ocorrência de conduta é apresentada com motivo e data

A App 07 SHALL apresentar as **ocorrências de conduta** do vinculado, cada uma com o **motivo**
e a **data**, em linguagem simples e sem código de erro. Ocorrência sem motivo guardado SHALL
ser apresentada com a data, sem inventar texto no lugar do motivo. (`RF-13-09`, `RN-13-21`)

#### Scenario: Ocorrência com motivo

- **WHEN** o vinculado tem ocorrência de conduta com motivo guardado
- **THEN** a tela a apresenta com o motivo e a data

#### Scenario: Ocorrência de ciclo anterior

- **WHEN** o vinculado tem ocorrência cujo motivo já foi apagado pelo encerramento do ciclo
- **THEN** a tela a apresenta com a data e sem motivo, sem texto substituto

### Requirement: Nenhuma tela expõe o que a criança faz sozinha nem dado de outra criança

A App 07 NEVER SHALL apresentar consulta ao assistente, transcrição de apoio escolar ou dado
identificável de **outra criança** — nem em equipe, nem em ranking, nem em criação coletiva.
(`RF-13-11`, `RF-13-12`, `RN-13-20`)

#### Scenario: Vinculado que usou o assistente e integra equipe

- **WHEN** o responsável percorre o painel de um vinculado que fez consultas ao assistente, teve
  apoio escolar transcrito e integra equipe de trilha
- **THEN** nenhuma tela apresenta consulta, transcrição ou dado identificável das outras
  crianças
