# Spec Delta

## ADDED Requirements

### Requirement: A vitrine não apresenta seção de poderes nem página de poder

A App 06 NEVER SHALL apresentar seção de poderes, card de poder ou página individual de poder.
O poder continua existindo como atributo público do Guerreiro(a), no card e na página dele, e
`GET /v1/vitrine/poderes` continua pública para quem constrói sobre a API — o que sai é a tela.
(`RF-03-02`, `RF-03-39`, decisão do fundador de 2026-10-11)

#### Scenario: A abertura não traz seção de poderes

- **WHEN** a raiz do domínio é aberta
- **THEN** nenhuma seção de poderes aparece, e nenhuma seção promete página de poder

#### Scenario: O poder segue aparecendo no Guerreiro(a)

- **WHEN** o visitante abre a página individual de um Guerreiro(a) com autorização vigente
- **THEN** os poderes dele continuam apresentados, com os níveis, como atributo da pessoa

#### Scenario: A rota pública de poderes continua respondendo

- **WHEN** uma aplicação de terceiro com chave válida consulta a leitura pública de poderes
- **THEN** o núcleo responde como antes, sem depender de a vitrine ter seção para isso

### Requirement: "Necessidades em aberto" é seção da abertura, e não um bloco de outra seção

A App 06 SHALL apresentar as necessidades de recurso em aberto como **seção própria da
abertura**, com o rótulo "Necessidades em aberto". A seção NEVER SHALL depender de o visitante
passar pela porta do convite, e NEVER SHALL ficar pendurada em outra seção. (`RF-03-47`,
decisão do fundador de 2026-10-11)

#### Scenario: A seção aparece por si na abertura

- **WHEN** a raiz do domínio é aberta e há necessidade de recurso em aberto
- **THEN** a seção "Necessidades em aberto" lista as necessidades, sem exigir que o visitante
  abra a porta do convite nem outra seção

#### Scenario: Sem necessidade em aberto, a seção diz isso

- **WHEN** a raiz do domínio é aberta e não há necessidade de recurso em aberto
- **THEN** a seção continua presente e diz que não há necessidade em aberto

### Requirement: "Contatos" exibe o texto publicado que o núcleo devolve

A App 06 SHALL exibir a seção **"Contatos"** com o texto publicado, na ordem do recorte, sem
publicidade nem patrocínio. A exibição SHALL vir do que o núcleo devolve, e nenhum valor SHALL
ficar escrito na aplicação. (`RF-03-45`, `RN-03-21`)

#### Scenario: "Contatos" mostra o que o Admin publicou

- **WHEN** o visitante abre "Contatos" com o texto publicado
- **THEN** a tela mostra o texto publicado, sem depender de nova versão da aplicação

#### Scenario: Seção não publicada diz isso

- **WHEN** "Contatos" não tem texto publicado
- **THEN** a tela diz que o conteúdo ainda não foi publicado

### Requirement: A vitrine não apresenta tela de "Como apoiar", e a chave PIX fica na porta

A App 06 NEVER SHALL exibir a seção **"Como apoiar"**, em recorte nenhum. A seção continua
existindo no núcleo, gravável por Admin e legível na leitura pública: o que sai é a tela. A
**chave PIX** da pessoa jurídica vinculada SHALL ser oferecida na **porta do convite**, e as
**necessidades de recurso em aberto**, em seção própria da abertura. (`RF-03-45`, `RF-03-46`,
`RF-03-47`, decisão do fundador de 2026-10-11)

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

## RENAMED Requirements

- FROM: `### Requirement: Toda página individual traz a chamada "Quero participar", e acompanhar leva à mesma porta`
- TO: `### Requirement: Toda página individual traz a chamada "Quero apoiar", e acompanhar leva à mesma porta`

## MODIFIED Requirements

### Requirement: A abertura tem herói, com ilustração em primeiro plano

A abertura da vitrine SHALL apresentar, antes das seções, um **herói** com a ilustração
do elenco em primeiro plano, a frase que diz o que o projeto é, e as ações que a vitrine
já oferece — "Quero apoiar" e "Entrar". NEVER SHALL oferecer ação que a vitrine não
tenha em outra tela.

O "Entrar" da vitrine é **do herói, e só dele**: nenhuma outra tela pública o apresenta, e
o cabeçalho NEVER SHALL trazer um segundo. Dois botões de mesmo nome na mesma tela não
acrescentam ação alguma e atrapalham quem navega por leitor de tela (decisão do fundador de
2026-10-10).

As duas ações SHALL ser apresentadas como um **par de iguais**: lado a lado, de mesma
altura, mesma forma e mesmo peso, distinguidas **por cor e por rótulo**, nunca por
tamanho. A distinção NEVER SHALL se apoiar só na cor — o rótulo de cada uma já a carrega.
Qual cor cada uma recebe é do documento 15 §3.2, e não deste requisito.

O que o herói comunica NEVER SHALL depender da ilustração: some a ilustração — rede
fora, preferência do aparelho —, e a frase e as ações continuam de pé. A ilustração
NEVER SHALL entrar no caminho crítico da tela nem exigir recurso de domínio de terceiro.

A ilustração SHALL ser uma **composição**, e não quatro figuras em qualquer ordem: os dois
estudantes nas extremidades, e ao centro o professor ao lado da criatura que a mão dele
indica. A ordem NEVER SHALL mudar sem que a razão mude junto — o gesto do professor aponta
para o vazio se a criatura sair do lado dele. As quatro SHALL aparecer **inteiras**, sem
corte nem redução de uma em relação às outras, do celular modesto ao aparelho largo.
(documento 15 §§1, 3.2, 4, 6, 13.6; `RF-03-01`, `RF-03-51`, `RF-03-58`, `RN-03-21`)

#### Scenario: A abertura apresenta o herói antes das seções

- **WHEN** a raiz do domínio é aberta
- **THEN** o herói aparece antes da primeira seção, com a frase do projeto e as ações
  "Quero apoiar" e "Entrar"

#### Scenario: O "Entrar" do herói é o único da tela

- **WHEN** a abertura é apresentada
- **THEN** existe exatamente um "Entrar" na tela, o do herói, e o cabeçalho não traz
  nenhum

#### Scenario: As duas ações se leem como um par de iguais

- **WHEN** o herói é apresentado
- **THEN** "Quero apoiar" e "Entrar" aparecem lado a lado, de mesma altura, forma e
  peso, e cada uma se identifica pelo próprio rótulo, sem depender da cor

#### Scenario: Sem a ilustração, a abertura continua inteira

- **WHEN** a ilustração do herói não carrega
- **THEN** a frase e as duas ações continuam visíveis e acionáveis

#### Scenario: O herói não oferece ação que a vitrine não tenha

- **WHEN** o herói é apresentado
- **THEN** cada ação dele é uma que a vitrine oferece em outra tela, e nenhuma outra

#### Scenario: O herói não busca recurso de terceiro

- **WHEN** a abertura é servida
- **THEN** nenhuma requisição sai para domínio que não seja o próprio

#### Scenario: A composição põe o professor ao lado da criatura que ele indica

- **WHEN** a ilustração do herói é apresentada
- **THEN** o professor ocupa a posição vizinha à da criatura, do lado para onde a mão dele
  aponta, e os dois estudantes ficam nas extremidades

#### Scenario: As quatro figuras aparecem inteiras, em qualquer largura de tela

- **WHEN** a abertura é aberta num visor estreito de celular ou num aparelho largo
- **THEN** as quatro figuras cabem na largura disponível, nenhuma é cortada na borda e a
  tela não ganha rolagem horizontal

#### Scenario: Quem lê por leitor de tela ouve o elenco na ordem em que ele aparece

- **WHEN** a ilustração é alcançada por leitor de tela
- **THEN** ela é anunciada uma vez, como um grupo só, nomeando as quatro figuras na mesma
  ordem em que aparecem na tela

### Requirement: Toda página individual traz a chamada "Quero apoiar", e acompanhar leva à mesma porta

A App 06 SHALL apresentar, em **toda página individual** que publica, a chamada **"Quero
apoiar"**, e SHALL apresentar na mesma página a **ação de acompanhar ou favoritar**, que
SHALL levar à **mesma porta** da chamada. As duas SHALL abrir a porta do convite sem exigir
cadastro, login ou dado do visitante. Com as páginas de Mestre e de Apoiador publicadas, a
chamada SHALL aparecer nas **quatro** páginas individuais que a vitrine tem — Guerreiro(a),
comunidade, Mestre e Apoiador. O **endereço** da porta NEVER SHALL mudar com o rótulo: ele é
público e compartilhável. (`RF-03-39`, `RF-03-40`, `RF-03-42`, PRD-03 §5.5, decisão do
fundador de 2026-10-11)

#### Scenario: A página do Guerreiro(a) convida

- **WHEN** o visitante abre a página individual de um Guerreiro(a) com autorização vigente
- **THEN** a página traz a chamada "Quero apoiar" e a ação de acompanhar

#### Scenario: A página da comunidade convida

- **WHEN** o visitante abre a página de uma Comunidade Virtual
- **THEN** a página traz a chamada "Quero apoiar" e a ação de acompanhar

#### Scenario: A página do Mestre convida

- **WHEN** o visitante abre a página individual de um Mestre
- **THEN** a página traz a chamada "Quero apoiar" e a ação de acompanhar

#### Scenario: A página do Apoiador convida

- **WHEN** o visitante abre a página individual de um Apoiador
- **THEN** a página traz a chamada "Quero apoiar" e a ação de acompanhar

#### Scenario: Acompanhar chega à porta do convite

- **WHEN** o visitante aciona a ação de acompanhar
- **THEN** a porta do convite abre, a mesma que a chamada "Quero apoiar" abre

#### Scenario: O endereço da porta não mudou com o rótulo

- **WHEN** o visitante aciona a chamada "Quero apoiar", em qualquer tela que a traga
- **THEN** a porta abre no mesmo endereço público de antes, e nenhum endereço anterior fica
  sem resposta

### Requirement: A porta oferece também doar pela chave PIX e ver as necessidades em aberto

A porta SHALL oferecer, a quem não quer se cadastrar agora, os dois caminhos que dispensam
cadastro: **doar pela chave PIX** da pessoa jurídica vinculada, a que o conteúdo institucional
guarda na seção "Como apoiar", e **ver as necessidades de recurso em aberto**. A chave PIX
SHALL vir do que o núcleo devolve, e nenhum valor SHALL ficar escrito na aplicação. Sendo a
porta o **único** lugar público onde a chave aparece, a porta NEVER SHALL deixar de oferecê-la
quando o núcleo a devolve. (`RF-03-43`, `RF-03-46`, PRD-03 §5.5, decisão do fundador de
2026-10-11)

#### Scenario: Quem não quer se cadastrar encontra o PIX

- **WHEN** o visitante abre a porta e o núcleo devolve a seção "Como apoiar" publicada
- **THEN** a porta mostra a chave PIX e o titular, sem pedir cadastro

#### Scenario: A porta mostra o que falta hoje

- **WHEN** o visitante abre a porta e há necessidade de recurso em aberto
- **THEN** a porta lista as necessidades em aberto

#### Scenario: A chave publicada é a que o Admin editou

- **WHEN** o Admin republica "Como apoiar" com outra chave
- **THEN** a porta mostra a chave nova, sem depender de nova versão da aplicação

## REMOVED Requirements

### Requirement: "Contatos" e "Como apoiar" exibem o que foi publicado, e "Como apoiar" traz a chave PIX

**Reason**: Decisão do fundador de 2026-10-11 — "Como apoiar" deixa de ter tela pública, e por
isso o requisito é **substituído** em vez de alterado: três dos cenários dele descrevem
comportamento que deixa de existir, não comportamento que muda. O que continua valendo foi
reescrito em dois requisitos acrescentados por esta change — "Contatos" exibindo o texto
publicado, e a proibição da tela de "Como apoiar" com a chave PIX na porta. O documento 03 §8,
o `RF-03-45` e o `RF-03-46` foram alterados antes desta change.

**Migration**: Nenhuma para o núcleo: a seção `como-apoiar` segue gravável pelo
`PUT /conteudo-institucional/{secao}`, segue na leitura pública e segue semeada com a chave PIX
e o titular do documento 04 §1 — a capacidade `conteudo-institucional` não muda. Para o
visitante, a chave PIX passa a ser alcançada pela porta do convite (`RF-03-43`), e as
necessidades de recurso em aberto, pela seção própria da abertura (`RF-03-47`). O Admin
continua editando as três seções pela App 03 (`RF-02-80`).

### Requirement: A seção de poderes apresenta cada poder com as trilhas dele

**Reason**: Decisão do fundador de 2026-10-11 — a seção de poderes sai da vitrine. Ela prometia
uma página individual de poder que nunca existiu, e com isso o `RF-03-39` seguia parcial desde a
fatia 6. Os Mestres responsáveis que ela derivava do autor das trilhas publicadas saem com ela.
O documento 03 §8 e o `RF-03-02` foram alterados antes desta change, e o `RF-03-02` passou de
seis seções com cards para cinco.

**Migration**: Nenhuma para quem consome a API: `GET /v1/vitrine/poderes` continua pública e
inalterada, e a capacidade `leitura-publica-da-vitrine` não muda — quem precisa dos poderes e das
trilhas de cada um lê a rota direto, pelo caminho que a Área do Apoiador Desenvolvedor
apresenta. Para o visitante, o poder segue visível como atributo do Guerreiro(a), no card e na
página dele (`RF-03-05`), e o Mestre segue alcançável pela seção de Mestres e pela página
individual dele (`RF-03-07`). Na vitrine, o consumo da rota no cliente é removido junto com a
seção.
