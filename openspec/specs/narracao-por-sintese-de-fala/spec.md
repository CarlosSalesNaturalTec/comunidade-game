# narracao-por-sintese-de-fala Specification

## Purpose
A camada que lê em voz alta, em pt-BR, o texto que cada tela declara, para quem ainda não lê
com fluência, não enxerga ou lê com esforço — e para dar ludicidade à plataforma. Define o
liga e desliga, o que fala sozinho e o que espera toque, qual dado do Guerreiro(a) pode ser
sintetizado e o limite da camada perante o leitor de tela.

## Requirements

### Requirement: A camada lê em voz alta o texto que a tela declara

A camada comum SHALL oferecer, às oito aplicações, a leitura em voz alta de texto em **pt-BR**
pela síntese de fala do navegador. O que se fala SHALL ser **declarado pela tela**: a camada
NEVER SHALL extrair texto do documento apresentado, nem ler rótulo de interface, para que a
narração diga o que a tela quis dizer e não o que ela por acaso contém.

Ao **entrar numa tela**, a camada SHALL falar sozinha apenas o **texto curto** que aquela tela
declara — título da tela, enunciado de pergunta e aviso. Texto **longo** — o conteúdo de uma
missão — NEVER SHALL ser falado sozinho: SHALL esperar um controle próprio, acionado por quem
quer ouvi-lo. (documento 15 §5.1)

Trocar de tela SHALL **cancelar** a fala em curso antes de iniciar a seguinte, para que a
narração da tela que passou não se sobreponha à tela nova.

#### Scenario: A tela fala o que declarou, ao ser aberta

- **WHEN** uma tela que declara narração é aberta com a narração ligada
- **THEN** a camada fala o texto curto declarado por ela, e nada mais da tela

#### Scenario: O conteúdo longo espera o toque

- **WHEN** a tela apresenta conteúdo de missão em texto
- **THEN** ele não é falado ao entrar na tela, e só é falado quando o controle próprio dele é
  acionado

#### Scenario: Trocar de tela cala a fala anterior

- **WHEN** a pessoa sai de uma tela enquanto a narração dela ainda fala
- **THEN** a fala é cancelada, e só então a tela seguinte fala o que declarou

### Requirement: Só o nick do Guerreiro(a) pode ser sintetizado

A voz pode ser **de rede**, e nesse caso o texto sai do aparelho para ser sintetizado. A camada
SHALL ser a **única fronteira** por onde esse texto passa, e dos dados do Guerreiro(a) SHALL
admitir **apenas o nick**. Nome, data de nascimento, vínculo, comunidade e qualquer outro dado
pessoal NEVER SHALL ser aceito para síntese — e o recuso SHALL estar no **contrato da camada**,
não numa recomendação: uma tela NEVER SHALL conseguir entregar à narração um dado que não seja
o nick. (documento 03 §§1.12, 12)

O restante do que se fala SHALL ser **texto da própria plataforma** — o que a tela declarou —,
nunca conteúdo captado da criança.

#### Scenario: A saudação fala o nick

- **WHEN** uma tela declara narração que cumprimenta quem chegou
- **THEN** o nick do Guerreiro(a) é falado, e nenhum outro dado dele

#### Scenario: Nenhum outro dado pessoal alcança a síntese

- **WHEN** uma tela tenta entregar à narração o nome do Guerreiro(a) ou outro dado pessoal
- **THEN** a camada não o aceita, e o dado não chega ao serviço que sintetiza

### Requirement: A narração não substitui nem concorre com o leitor de tela

O texto que a camada fala SHALL ser marcado `aria-hidden`, para que leitor de tela não o
anuncie em dobro. A narração SHALL ser **camada a mais**: o piso de acessibilidade do documento
15 §5 SHALL continuar cumprido com ela desligada, e nenhuma informação SHALL existir **apenas**
em voz. (documento 15 §5.1)

#### Scenario: Leitor de tela não anuncia a narração em dobro

- **WHEN** um leitor de tela percorre uma tela que declara narração
- **THEN** o texto que existe para a narração não é anunciado por ele

#### Scenario: Desligada, a tela continua completa

- **WHEN** a narração está desligada
- **THEN** toda informação da tela continua legível e alcançável, sem que nada dependa de voz

### Requirement: Sem voz disponível, a camada cala sem alarme

Não havendo rede, a camada SHALL usar uma **voz local** do aparelho, se houver. Não havendo voz
alguma que sirva, ou não oferecendo o navegador a síntese de fala, a camada SHALL ficar **em
silêncio** e NEVER SHALL apresentar mensagem de erro: nada se perde, e um aviso a cada tela
custaria mais que o silêncio. A tela SHALL seguir inteiramente utilizável. (documento 03 §1.12)

#### Scenario: Sem rede, a voz local assume

- **WHEN** a rede está fora e o aparelho tem voz local em pt-BR
- **THEN** a narração continua, por essa voz

#### Scenario: Sem voz alguma, a tela segue sem alarme

- **WHEN** o navegador não oferece síntese de fala, ou nenhuma voz serve
- **THEN** nada é falado, nenhuma mensagem de erro aparece, e a tela segue utilizável

### Requirement: Os componentes comuns declaram a narração deles

O **cabeçalho de tela** e o **aviso** da camada comum SHALL declarar a própria narração a
partir do texto que já recebem, para que a maior parte das telas fale sem roteiro avulso. Quem
monta o componente SHALL poder **substituir** esse texto por outro, quando o que está escrito
na tela não for o que convém ouvir, e SHALL poder **calar** aquele componente.

Isso NEVER SHALL equivaler a extrair texto do documento: o que se fala é a **propriedade
declarada** por quem montou a tela, não o que o navegador renderizou.

#### Scenario: O cabeçalho fala o título da tela

- **WHEN** uma tela monta o cabeçalho comum com um título e a narração está ligada
- **THEN** o título é falado ao entrar na tela

#### Scenario: Quem monta troca o que se ouve

- **WHEN** uma tela declara, no cabeçalho, uma narração diferente do título escrito
- **THEN** o que é falado é a narração declarada, e o título escrito permanece na tela

#### Scenario: Um componente pode ser calado

- **WHEN** uma tela declara que determinado aviso não deve ser falado
- **THEN** ele aparece na tela e não é narrado

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
