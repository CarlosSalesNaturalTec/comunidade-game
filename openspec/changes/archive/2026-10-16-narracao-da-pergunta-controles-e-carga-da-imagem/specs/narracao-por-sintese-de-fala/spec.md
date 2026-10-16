# Spec Delta

## MODIFIED Requirements

### Requirement: A camada lê em voz alta o texto que a tela declara

A camada comum SHALL oferecer, às oito aplicações, a leitura em voz alta de texto em **pt-BR**
pela síntese de fala do navegador. O que se fala SHALL ser **declarado pela tela**: a camada
NEVER SHALL extrair texto do documento apresentado, nem ler rótulo de interface, para que a
narração diga o que a tela quis dizer e não o que ela por acaso contém.

Ao **entrar numa tela**, a camada SHALL falar sozinha apenas o **texto curto** que aquela tela
declara — título da tela, enunciado de pergunta e aviso. Texto **longo** — o conteúdo de uma
missão — NEVER SHALL ser falado sozinho: SHALL esperar um controle próprio, acionado por quem
quer ouvi-lo. (documento 15 §5.1)

Onde a tela apresenta uma **sequência um item por vez**, cada item alcançado SHALL ser falado
como se fosse a entrada numa tela: avançar e **retornar** SHALL falar o item da vez, e a fala
anterior SHALL ser cancelada antes dela. A fala SHALL ser disparada pela **identidade do
item**, nunca pela reapresentação do mesmo item, para que a tela não fale em laço. (documento
15 §§5.1, 6.4, decisão do fundador de 2026-10-16)

Sendo o item uma **pergunta de quiz**, o texto curto dela SHALL compreender o **enunciado e as
alternativas**: ouvir a pergunta sem as respostas possíveis deixaria quem ainda não lê sem como
responder, e nenhuma informação SHALL existir apenas para quem lê. As alternativas SHALL ser
faladas a partir do **dado que a tela declara**, e NEVER SHALL ser lidas do documento
apresentado. (documento 15 §5.1, decisão do fundador de 2026-10-16)

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

#### Scenario: Avançar na sequência fala o item alcançado

- **WHEN** a narração está ligada e quem percorre uma sequência um item por vez avança ao
  seguinte
- **THEN** o item alcançado é falado, e a fala do anterior é cancelada antes dela

#### Scenario: Retornar ao item anterior o fala de novo

- **WHEN** a narração está ligada e quem percorre a sequência volta ao item anterior
- **THEN** aquele item é falado de novo, como ao ser alcançado pela primeira vez

#### Scenario: O item reapresentado não fala duas vezes

- **WHEN** a tela reapresenta o mesmo item da sequência sem que a posição mude
- **THEN** nada é falado de novo, e a fala em curso não é interrompida

#### Scenario: A pergunta do quiz fala o enunciado e as alternativas

- **WHEN** a narração está ligada e quem responde um quiz alcança uma pergunta
- **THEN** o enunciado dela é falado e, em seguida, as alternativas que a tela declara

### Requirement: A narração não substitui nem concorre com o leitor de tela

A camada NEVER SHALL acrescentar ao documento apresentado texto que exista **só para ser
falado**: o que ela fala é texto que a tela **já apresenta**, ou uma frase montada a partir do
dado declarado que vai **direto à síntese**, sem nunca entrar na tela. É assim que leitor de
tela não anuncia nada em dobro — não há nó a esconder —, e é por isso que texto já escrito
NEVER SHALL ser marcado `aria-hidden` por ser também falado: esconder o que está na tela
tiraria de quem usa leitor de tela o que a narração apenas reforça. A narração SHALL ser
**camada a mais**: o piso de acessibilidade do documento 15 §5 SHALL continuar cumprido com ela
desligada, e nenhuma informação SHALL existir **apenas** em voz. (documento 15 §5.1, decisão do
fundador de 2026-10-16)

#### Scenario: Leitor de tela não anuncia a narração em dobro

- **WHEN** um leitor de tela percorre uma tela que declara narração
- **THEN** nada existe no documento só para a narração, e por isso nada é anunciado em dobro

#### Scenario: A frase montada para a voz não chega ao documento

- **WHEN** a tela declara uma narração montada a partir de dado seu, como o enunciado e as
  alternativas de uma pergunta reunidos numa frase
- **THEN** aquela frase vai à síntese sem ser escrita na tela, e o leitor de tela segue lendo o
  enunciado e as alternativas como a tela os apresenta

#### Scenario: O que está escrito na tela continua alcançável

- **WHEN** um leitor de tela percorre uma tela cuja narração fala um texto que ela já apresenta
- **THEN** aquele texto continua sendo anunciado por ele, porque não existe só para a voz

#### Scenario: Desligada, a tela continua completa

- **WHEN** a narração está desligada
- **THEN** toda informação da tela continua legível e alcançável, sem que nada dependa de voz
