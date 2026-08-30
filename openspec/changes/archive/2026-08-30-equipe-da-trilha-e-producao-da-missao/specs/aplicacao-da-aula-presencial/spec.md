## ADDED Requirements

### Requirement: A equipe forma a equipe da trilha pelo aparelho, a partir da programação

A App 01 SHALL oferecer, na programação do encontro, a formação da **equipe da trilha** da
atividade que a equipe escolheu: o Guerreiro(a) em sessão **cria** a equipe daquela trilha ou
**entra** na que já existe, declarando o **papel** que terá, sem aprovação de terceiro.

A aplicação SHALL apresentar as recusas do núcleo em **linguagem simples**, sem código de erro
cru: o sexto integrante, o segundo integrante de 17 anos ou mais e a segunda equipe da mesma
trilha. Enquanto a equipe da trilha **não** estiver homologada, a aplicação SHALL oferecer a
entrada e a saída; depois de homologada, NEVER SHALL oferecer nenhuma das duas.
(`RF-04-61`, `RN-01-44`, documento 99 §6 invariante 15)

#### Scenario: A formação parte da atividade escolhida

- **WHEN** a equipe declarou a atividade que está trabalhando e abre a formação da equipe da
  trilha
- **THEN** a aplicação forma a equipe da **trilha daquela atividade**, sem pedir que alguém a
  escolha de novo

#### Scenario: Guerreiro(a) cria a equipe da trilha e entra nela

- **WHEN** um Guerreiro(a) em sessão cria a equipe da trilha
- **THEN** a equipe nasce com ele como primeiro integrante, sem aprovação de ninguém

#### Scenario: A segunda equipe da mesma trilha é recusada em linguagem simples

- **WHEN** um Guerreiro(a) que já integra uma equipe daquela trilha tenta criar outra
- **THEN** a aplicação apresenta a recusa em linguagem simples e ele segue na primeira

#### Scenario: Equipe homologada não oferece entrar nem sair

- **WHEN** a tela da equipe da trilha já homologada é apresentada
- **THEN** nenhuma ação de entrar ou de sair é oferecida

### Requirement: O Mestre presente homologa a equipe da trilha no mesmo aparelho

A App 01 SHALL oferecer a **homologação da equipe da trilha** ao **Mestre** sob a **sessão de
trabalho do aparelho**, no mesmo encontro em que a equipe se formou. A aplicação SHALL
apresentar a composição — avatar, nick e papel de cada integrante — antes de homologar, e SHALL
declarar que a composição **fica fixa** a partir dali.

A homologação NEVER SHALL ser oferecida ao **Guerreiro(a)** em sessão, e a App 01 SHALL seguir
sem oferecer a Mestre ou Admin a **formação** ou a **alteração da composição** de equipe alguma
— homologar não é formar. Decisão do fundador, 2026-08-26: as duas coisas acontecem na App 01.
(`RF-04-62`, `RN-04-18`, `RF-01-16`, documento 99 §6 invariante 15)

#### Scenario: O Mestre homologa sob a sessão de trabalho

- **WHEN** o Mestre em sessão de trabalho homologa a equipe da trilha formada no encontro
- **THEN** a aplicação registra a homologação e a composição fica fixa

#### Scenario: A composição é mostrada antes de homologar

- **WHEN** a tela de homologação é apresentada
- **THEN** ela mostra avatar, nick e papel de cada integrante e avisa que a composição fica fixa

#### Scenario: O Guerreiro(a) não vê a homologação

- **WHEN** um Guerreiro(a) em sessão abre a tela da equipe da trilha
- **THEN** nenhuma ação de homologar é oferecida a ele

#### Scenario: A sessão de trabalho segue sem formar equipe

- **WHEN** a sessão de trabalho do aparelho está aberta
- **THEN** a aplicação oferece homologar, e não oferece criar equipe, entrar nem sair

### Requirement: A equipe entrega a produção da missão pelo aparelho e lê a devolutiva

A App 01 SHALL oferecer à equipe, na atividade que ela declarou estar trabalhando, a **entrega
da produção** em **uma** de três formas: **texto** digitado, **fala** gravada pelo microfone ou
**foto** do que a equipe fez à mão. A tela SHALL apresentar a **produção esperada** declarada na
atividade, para a equipe saber o que entregar.

Entregue, a aplicação SHALL apresentar a **devolutiva** que o núcleo devolveu, e SHALL dizer,
na própria tela, que ela **não vale ponto** e que o resultado é lançado pelo Mestre. Devolutiva
que não veio numa entrega por texto SHALL ser apresentada como tal, com a entrega registrada —
nunca como perda do que a equipe escreveu; entrega por fala ou foto que o núcleo recusou por
leitura indisponível SHALL ser apresentada como pedido de reenvio, em linguagem simples.

O microfone SHALL abrir por **ação do Guerreiro(a)** e fechar ao fim da fala; a aplicação NEVER
SHALL captar o áudio ambiente da aula. A aplicação NEVER SHALL guardar no aparelho a foto ou o
áudio da produção depois de enviá-los. (`RF-04-45`, `RF-04-46`, `RF-04-47`, `RN-04-20`,
`RN-04-12`, documento 03 §12.2)

#### Scenario: A equipe entrega por texto

- **WHEN** a equipe escreve a produção e envia
- **THEN** a aplicação registra a entrega e apresenta a devolutiva devolvida pelo núcleo

#### Scenario: A equipe entrega por fala

- **WHEN** um integrante toca o botão de falar, grava a produção e envia
- **THEN** o microfone fecha ao fim da fala e a aplicação envia o áudio, sem guardá-lo no
  aparelho

#### Scenario: A equipe entrega a foto do manuscrito

- **WHEN** a equipe fotografa o que fez à mão e envia
- **THEN** a aplicação envia a foto e não a mantém no aparelho depois do envio

#### Scenario: A tela diz que a devolutiva não vale ponto

- **WHEN** a devolutiva é apresentada
- **THEN** a tela diz, em linguagem simples, que ela não credita ponto e que quem lança o
  resultado é o Mestre

#### Scenario: A produção esperada aparece antes da entrega

- **WHEN** a tela da entrega é apresentada
- **THEN** ela mostra a produção esperada declarada na atividade

#### Scenario: Devolutiva que não veio não perde a entrega por texto

- **WHEN** o núcleo registra a produção em texto sem devolutiva
- **THEN** a aplicação confirma a entrega e avisa que o retorno não veio desta vez

#### Scenario: Leitura indisponível pede reenvio

- **WHEN** o núcleo recusa a entrega por fala ou foto porque a leitura não veio
- **THEN** a aplicação pede o reenvio em linguagem simples, sem dizer que a produção se perdeu

### Requirement: Quem recusa foto e áudio entrega por texto, sem perder a missão

A App 01 SHALL oferecer a entrega **por texto** como alternativa sempre disponível: a equipe
que não quiser usar foto nem microfone SHALL entregar assim mesmo, **sem perder a missão**.
A aplicação NEVER SHALL condicionar a entrega ao uso da câmera ou do microfone.
(`RF-04-45`, `RN-04-09`, documento 99 §6 invariante 11)

#### Scenario: A entrega por texto está sempre oferecida

- **WHEN** a tela da entrega é apresentada
- **THEN** a forma texto está entre as oferecidas, qualquer que seja o aparelho

#### Scenario: Aparelho sem câmera nem microfone entrega assim mesmo

- **WHEN** o aparelho não tem câmera nem microfone disponíveis
- **THEN** a aplicação oferece a entrega por texto e a equipe conclui a produção

## REMOVED Requirements

### Requirement: A App 01 não forma equipe pela gestão nem homologa equipe da trilha

**Reason**: A decisão do fundador de 2026-08-26 (documento 09 §1, "Onde a equipe da trilha é
formada e homologada") trouxe a homologação para a App 01, revogando a que mandava homologar
fora dela. A metade que continua valendo — a gestão não forma nem altera composição de equipe
(`RN-04-18`) — passa para o requisito "O Mestre presente homologa a equipe da trilha no mesmo
aparelho", com o cenário "A sessão de trabalho segue sem formar equipe".

**Migration**: Nenhuma. Nada no produto oferecia a homologação; ela nasce nesta change, e a
vedação de a gestão formar equipe segue vigente no requisito que a absorveu.
