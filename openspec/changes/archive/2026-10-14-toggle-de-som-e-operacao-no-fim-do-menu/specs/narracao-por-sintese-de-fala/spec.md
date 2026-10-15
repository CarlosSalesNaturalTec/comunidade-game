# Spec Delta

## ADDED Requirements

### Requirement: A narração nasce desligada, e o toque que a liga é o gesto que a arma

A narração SHALL nascer **desligada**, e a aplicação SHALL oferecer um **alternador** que a liga
e desliga. O navegador exige gesto da pessoa antes da primeira fala: o próprio acionamento que
**liga** SHALL ser esse gesto. A camada NEVER SHALL exigir um controle de **iniciar** à parte, e
NEVER SHALL tentar falar antes de um gesto. (documento 15 §5.1, decisão do fundador de
2026-10-14)

#### Scenario: Nasce desligada no aparelho que nunca escolheu

- **WHEN** a aplicação abre num aparelho onde ninguém escolheu ligar nem desligar
- **THEN** a narração está desligada, e nenhuma tela é falada sozinha

#### Scenario: Ligar já arma, sem segundo controle

- **WHEN** alguém liga a narração pelo alternador
- **THEN** as telas seguintes falam o que declararam, e nenhum controle de iniciar é apresentado
  em momento algum

#### Scenario: Desligada, nada fala sozinho

- **WHEN** a narração está desligada e uma tela que declara narração é aberta
- **THEN** nada é falado sozinho, e nenhuma mensagem de erro aparece

### Requirement: O estado da narração é do aparelho e não sobrevive à recarga

O estado escolhido SHALL valer para o **aparelho**, não para a pessoa: SHALL persistir entre
atendimentos no mesmo carregamento da aplicação e NEVER SHALL acompanhar o Guerreiro(a) a outro
aparelho. NEVER SHALL sobreviver a **recarregar a aplicação** — ali a narração nasce de novo
desligada. Quem escolhe NEVER SHALL prender a escolha de quem vier depois. (documento 15 §5.1,
decisão do fundador de 2026-10-14)

#### Scenario: A escolha persiste entre atendimentos e não viaja com a pessoa

- **WHEN** alguém liga a narração e outro atendimento começa no mesmo aparelho
- **THEN** ela continua ligada ali, quem chega pode desligá-la, e nada disso acompanha o
  Guerreiro(a) a outro aparelho

#### Scenario: A recarga devolve a narração ao desligado

- **WHEN** a narração está ligada e a aplicação é recarregada
- **THEN** ela volta a estar desligada, e ligar de novo é o gesto que a arma

### Requirement: O alternador pode ser só glifo, com o estado dito pela forma

O alternador SHALL poder ser apresentado **só por glifo**. Nesse caso o estado SHALL ser dito
pela **forma** do glifo e pelo estado de pressionado do controle — NEVER SHALL depender de cor
sozinha nem de frase escrita na tela —, e o **rótulo** SHALL alcançar quem navega por leitor de
tela. (documento 15 §§5, 5.1, decisão do fundador de 2026-10-14)

#### Scenario: O estado do alternador se reconhece sem cor

- **WHEN** o alternador é apresentado só por glifo, ligado e desligado
- **THEN** cada estado se reconhece pela forma do glifo e pelo estado de pressionado, sem
  depender da cor

#### Scenario: O rótulo chega a quem não vê o desenho

- **WHEN** quem navega por leitor de tela alcança o alternador
- **THEN** o rótulo dele é anunciado, e nenhuma descrição do desenho toma o lugar do rótulo

### Requirement: O texto longo se ouve com a narração desligada

O controle de ouvir o **texto longo** NEVER SHALL depender do alternador: quem o aciona está
pedindo aquela leitura, e o próprio acionamento é o gesto que o navegador exige. Exigir o
alternador ligado tiraria a leitura do texto longo de quem mais precisa dela, agora que a
narração nasce desligada. (documento 15 §5.1, decisão do fundador de 2026-10-14)

#### Scenario: O texto longo se ouve com a narração desligada

- **WHEN** a narração está desligada e o controle de ouvir o texto longo é acionado
- **THEN** aquele texto é falado, e as telas continuam não falando sozinhas

#### Scenario: Sem síntese no navegador o controle não é oferecido

- **WHEN** o navegador não oferece síntese de fala
- **THEN** o controle de ouvir o texto longo não é apresentado, e nenhuma mensagem de erro
  aparece

## REMOVED Requirements

### Requirement: A narração liga e desliga, e o estado é do aparelho

**Reason**: O padrão **inverteu** por decisão do fundador de 2026-10-14: a narração nasce
desligada, a escolha deixa de sobreviver à recarga da aplicação, o controle passa a poder ser
só glifo e o estado "ligada e ainda não armada" — que exigia um controle de **iniciar** à parte
— deixa de existir. O controle de ouvir o texto longo também deixa de depender do liga e
desliga. Substituído pelos quatro requisitos acrescentados nesta change, um por comportamento.

**Migration**: Nada a migrar no dado: a escolha nunca foi gravada fora do aparelho e agora não
é gravada em lugar algum. A aplicação que montava o controle de iniciar o remove; quem quer a
narração a liga pelo alternador, e esse toque a arma.
