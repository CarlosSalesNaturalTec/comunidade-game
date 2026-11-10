# Spec Delta

## ADDED Requirements

### Requirement: Toda página individual traz a chamada "Quero apoiar", sem ação de acompanhar

A App 06 SHALL apresentar a chamada **"Quero apoiar"** nas **quatro** páginas individuais —
Guerreiro(a), comunidade, Mestre e Apoiador —, abrindo a porta do convite sem cadastro, login
ou dado do visitante. A página NEVER SHALL oferecer ação de **acompanhar** ou **favoritar**. O
**endereço** da porta NEVER SHALL mudar com o rótulo. (`RF-03-39`, `RF-03-42`, `RN-03-16`,
PRD-03 §5.5, decisões do fundador de 2026-10-11 e 2026-11-10)

#### Scenario: A página do Guerreiro(a) convida, sem acompanhar

- **WHEN** o visitante abre a página individual de um Guerreiro(a) com autorização vigente
- **THEN** a página traz a chamada "Quero apoiar" e nenhum botão "Quero acompanhar"

#### Scenario: A página da comunidade convida, sem acompanhar

- **WHEN** o visitante abre a página de uma Comunidade Virtual
- **THEN** a página traz a chamada "Quero apoiar" e nenhum botão "Quero acompanhar"

#### Scenario: A página do Mestre convida, sem acompanhar

- **WHEN** o visitante abre a página individual de um Mestre
- **THEN** a página traz a chamada "Quero apoiar" e nenhum botão "Quero acompanhar"

#### Scenario: A página do Apoiador convida, sem acompanhar

- **WHEN** o visitante abre a página individual de um Apoiador
- **THEN** a página traz a chamada "Quero apoiar" e nenhum botão "Quero acompanhar"

#### Scenario: O endereço da porta não mudou com o rótulo

- **WHEN** o visitante aciona a chamada "Quero apoiar", em qualquer tela que a traga
- **THEN** a porta abre no mesmo endereço público de antes, e nenhum endereço anterior fica
  sem resposta

## MODIFIED Requirements

### Requirement: A vitrine não guarda nada do visitante, no servidor ou no aparelho

A App 06 NEVER SHALL instalar cookie de rastreio, rastreador ou perfilamento do visitante, para
finalidade nenhuma, e NEVER SHALL guardar no aparelho preferência, escolha ou histórico de quem
visita. NEVER SHALL guardar **favorito** ou pessoa acompanhada, em lugar nenhum — nem no
servidor, nem no aparelho, nem em parâmetro de rota —, porque favoritar é função de **Apoiador
cadastrado na App 08**, e lá é leitura: não abre canal de contato. Havendo medição de audiência,
ela SHALL ser agregada e sem identificador de visitante. (`RF-03-38`, `RF-03-51`, `RN-03-15`,
`RN-03-16`, `RN-03-22`, PRD-03 §10)

#### Scenario: Nada é gravado no aparelho depois de uma visita inteira

- **WHEN** o visitante navega pela vitrine, troca de recorte e abre a pergunta do "Entrar"
- **THEN** nada da visita fica guardado no aparelho

#### Scenario: Nenhum rastreador de terceiro é carregado

- **WHEN** a vitrine carrega
- **THEN** nenhum cookie de rastreio, rastreador ou perfilamento é instalado

#### Scenario: Pedir para acompanhar não cria favorito

- **WHEN** o visitante, querendo acompanhar alguém, abre a página individual dessa pessoa,
  aciona "Quero apoiar" e depois recarrega a vitrine
- **THEN** nenhum favorito e nenhuma pessoa acompanhada existem em lugar nenhum, e a vitrine
  está idêntica à primeira visita

### Requirement: A vitrine não apresenta tela de "Como apoiar", e a chave PIX fica na porta

A App 06 NEVER SHALL exibir a seção **"Como apoiar"**, em recorte nenhum. A seção continua
existindo no núcleo, gravável por Admin e legível na leitura pública: o que sai é a tela. A
**chave PIX** da pessoa jurídica vinculada e as **necessidades de recurso em aberto** SHALL ser
oferecidas na **porta do convite**. (`RF-03-43`, `RF-03-45`, `RF-03-46`, `RF-03-47`, decisões do
fundador de 2026-10-11 e 2026-11-10)

#### Scenario: Nenhuma tela pública apresenta "Como apoiar"

- **WHEN** o visitante percorre a vitrine inteira, em qualquer recorte
- **THEN** nenhuma tela apresenta a seção "Como apoiar", e nenhuma navegação a oferece

#### Scenario: O Admin continua publicando "Como apoiar"

- **WHEN** um Admin publica o texto de "Como apoiar"
- **THEN** a publicação é aceita e fica legível pelo núcleo, como antes, sem tela pública que
  a apresente

#### Scenario: A chave PIX continua alcançável pelo visitante

- **WHEN** o visitante quer doar e não encontra mais a seção "Como apoiar"
- **THEN** a chave PIX e o titular continuam oferecidos na porta do convite

## REMOVED Requirements

### Requirement: Toda página individual traz a chamada "Quero apoiar", e acompanhar leva à mesma porta

**Reason**: Decisão do fundador de 2026-11-10 — sai a ação de acompanhar (`RF-03-40`
retirado); o botão só repetia o destino da chamada.
**Migration**: Substituído por "Toda página individual traz a chamada 'Quero apoiar', sem ação
de acompanhar". Acompanhar segue na App 08, para o Apoiador cadastrado (`RN-03-16`).

### Requirement: "Necessidades em aberto" é seção da abertura, e não um bloco de outra seção

**Reason**: Decisão do fundador de 2026-11-10 — a seção sai da abertura.
**Migration**: As necessidades seguem publicadas na porta do convite (`RF-03-43`, `RF-03-47`);
`GET /v1/vitrine/necessidades` não muda.
