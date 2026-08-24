## ADDED Requirements

### Requirement: O caminho do onboarding cadastra o Guerreiro(a) no encontro

A App 01 SHALL oferecer, na tela inicial, o caminho do **onboarding** em estado operante, e por
ele SHALL conduzir o cadastro do Guerreiro(a) coletando **nome**, **nick**, **forma de
tratamento**, **data de nascimento** e **características do avatar**. A aplicação NEVER SHALL
perguntar a comunidade: ela vem da aula vigente adotada na sessão de trabalho. O cadastro SHALL
ser feito **na presença** de Mestre ou Admin, cuja sessão de trabalho autentica a escrita sem
tornar-se autora dela. (`RF-04-01`, `RF-04-07`, `RF-04-10`, `RN-04-02`, `RN-04-04`, PRD-04 §12,
documento 99 §6 invariante 3)

Nesta fatia o cadastro é **formulário guiado**, não conversa conduzida por modelo de IA: a
condução por áudio e chat é de fatia posterior, e até lá a ordem dos campos é a da tela.

#### Scenario: O caminho do onboarding está alcançável

- **WHEN** a sessão de trabalho do aparelho está aberta e a tela inicial é apresentada
- **THEN** o caminho do onboarding é alcançável e conduz ao cadastro do Guerreiro(a)

#### Scenario: O cadastro coleta os cinco dados

- **WHEN** uma criança chega ao caminho do onboarding
- **THEN** a aplicação coleta nome, nick, forma de tratamento, data de nascimento e
  características do avatar, e não conclui o cadastro faltando qualquer um deles

#### Scenario: A comunidade nunca é perguntada à criança

- **WHEN** o cadastro do encontro é concluído
- **THEN** o Guerreiro(a) fica vinculado à comunidade da aula vigente, e em nenhum momento a
  aplicação lhe perguntou qual é

#### Scenario: Sem sessão de trabalho não há cadastro

- **WHEN** não há sessão de trabalho do aparelho aberta
- **THEN** o caminho do onboarding não é alcançável e nenhum cadastro é enviado ao núcleo

### Requirement: A aplicação recusa o nick em uso e oferece as variações devolvidas pelo núcleo

A App 01 SHALL apresentar a recusa de **nick já usado** em linguagem simples, sem código de erro
cru, e SHALL oferecer as **variações** que o núcleo devolveu na própria recusa, aceitando que a
criança escolha uma delas e conclua o cadastro. A aplicação NEVER SHALL afirmar que um nick está
disponível antes de o núcleo aceitar a gravação, e NEVER SHALL dizer de quem é o nick em uso nem
de que papel. (`RF-04-08`, `RN-04-05`, PRD-04 §12)

#### Scenario: Nick em uso é recusado sem concluir o cadastro

- **WHEN** a criança conclui o cadastro com um nick já usado por qualquer persona
- **THEN** a aplicação apresenta a recusa em linguagem simples e nenhum cadastro passa a existir

#### Scenario: A variação sugerida é aceita

- **WHEN** a criança escolhe uma das variações oferecidas na recusa e conclui de novo
- **THEN** o cadastro é criado com a variação escolhida

#### Scenario: A recusa não revela o dono do nick

- **WHEN** a recusa de nick é apresentada
- **THEN** ela não diz de quem é o nick nem de que papel é a persona que o tem

### Requirement: Idade fora da faixa interrompe o cadastro e chama o Mestre ou o Admin

A App 01 SHALL interromper o cadastro quando a data de nascimento informada resultar em idade
**fora da faixa de 6 a 16 anos**, SHALL orientar a chamar o Mestre ou o Admin presente, e NEVER
SHALL criar o cadastro. (`RF-04-09`, `RN-04-11`, PRD-04 §12, documento 99 §6 invariante 2)

#### Scenario: Idade abaixo da faixa não cria cadastro

- **WHEN** a data de nascimento informada resulta em idade menor que 6 anos
- **THEN** a aplicação interrompe o cadastro, orienta a chamar o Mestre ou o Admin, e nenhuma
  persona passa a existir

#### Scenario: Idade acima da faixa não cria cadastro

- **WHEN** a data de nascimento informada resulta em idade maior que 16 anos
- **THEN** a aplicação interrompe o cadastro, orienta a chamar o Mestre ou o Admin, e nenhuma
  persona passa a existir

#### Scenario: Idade dentro da faixa segue

- **WHEN** a data de nascimento informada resulta em idade entre 6 e 16 anos, inclusive nos
  extremos
- **THEN** o cadastro segue sem interrupção

### Requirement: O cadastro do encontro nasce ativo, sem imagem, e registra a presença no mesmo ato

A App 01 SHALL criar o cadastro **ativo**, sem exigir autorização do responsável para que ele
exista, e **sem imagem** — nesta fatia nenhuma captura é oferecida. A **presença do dia** na
aula vigente SHALL ser registrada **no mesmo ato** do cadastro, de modo que nenhum Guerreiro(a)
recém-cadastrado fique sem a presença do encontro em que se cadastrou. Nenhuma requisição da
aplicação SHALL carregar fotografia, e nenhuma imagem SHALL ser gravada no aparelho
compartilhado. (`RF-04-15`, `RF-04-17`, `RF-04-28`, `RN-04-10`, `RN-04-12`, PRD-04 §12)

#### Scenario: O cadastro nasce ativo e sem imagem

- **WHEN** o cadastro do encontro é concluído
- **THEN** o Guerreiro(a) passa a existir ativo, sem _template_ biométrico, e participa de tudo

#### Scenario: A presença do dia acompanha o cadastro

- **WHEN** o cadastro do encontro é concluído
- **THEN** a presença daquele Guerreiro(a) na aula vigente está registrada, sem ato adicional de
  ninguém

#### Scenario: Cadastro recusado não deixa presença órfã

- **WHEN** o cadastro é recusado pelo núcleo por qualquer motivo
- **THEN** nenhuma persona e nenhuma presença passam a existir

#### Scenario: Nenhuma imagem sai do aparelho nesta fatia

- **WHEN** qualquer cadastro do encontro acontece
- **THEN** nenhuma requisição carrega fotografia e nenhuma imagem fica gravada no aparelho

#### Scenario: O atendimento seguinte começa limpo depois de um cadastro

- **WHEN** um cadastro termina e a aplicação volta à tela inicial
- **THEN** nenhum dado da criança recém-cadastrada aparece em tela alguma

### Requirement: A App 01 não oferece captura, consentimento nem entrada por imagem nesta fatia

A App 01 NEVER SHALL oferecer, no caminho do onboarding desta fatia, a captura de imagem, o
registro de consentimento ou a entrada do Guerreiro(a) por reconhecimento facial. A criança que
chega **sem o responsável** é atendida por inteiro, e a criança que chega **com** o responsável é
atendida pelo mesmo caminho, ficando a captura para quando ela for oferecida. Nenhuma recusa
SHALL deixar o Guerreiro(a) fora da aula. (`RF-04-15`, `RN-04-09`, PRD-04 §§3.2, 5.3, documento
99 §6 invariante 11)

#### Scenario: A criança sem o responsável é atendida por inteiro

- **WHEN** uma criança chega ao onboarding sem o responsável
- **THEN** o cadastro é concluído, ativo e sem imagem, e ela participa da aula

#### Scenario: Nenhuma tela pede consentimento nesta fatia

- **WHEN** o caminho do onboarding é percorrido
- **THEN** nenhuma tela de termo de consentimento é apresentada e nenhum consentimento é enviado
  ao núcleo
