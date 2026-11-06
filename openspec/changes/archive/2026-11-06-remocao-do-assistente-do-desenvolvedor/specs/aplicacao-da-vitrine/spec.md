## MODIFIED Requirements

### Requirement: A Área do Apoiador Desenvolvedor é seção da vitrine e reúne quatro coisas

A App 06 SHALL oferecer a **Área do Apoiador Desenvolvedor** em endereço próprio, pública e sem
login, como **seção da vitrine** — nunca uma nona aplicação (`RN-03-29`).

A área SHALL reunir, na mesma tela, as quatro coisas do `RF-03-67`: o **link da documentação**
publicada com MkDocs, o **link da documentação da API** — a interface Swagger que o núcleo
publica fora de `/v1`, aberta e sem chave —, o **formulário de solicitação de chave** e o
**link do repositório no GitHub** (decisão do fundador de 2026-11-06).

A área NEVER SHALL pedir login, cadastro ou qualquer dado do visitante fora dos campos do
formulário de chave, e NEVER SHALL oferecer conversa com assistente.

#### Scenario: A área abre com as quatro coisas

- **WHEN** um visitante abre a Área do Apoiador Desenvolvedor
- **THEN** a tela traz o link da documentação, o link da documentação da API, o formulário de
  chave e o link do repositório, sem pedir login

#### Scenario: O link da documentação da API aponta a interface do núcleo

- **WHEN** o visitante aciona o link da documentação da API
- **THEN** ele abre, em nova aba, a interface Swagger do núcleo configurado para a vitrine, sem
  chave

#### Scenario: A área não oferece assistente

- **WHEN** a área abre
- **THEN** não há chat, mensagem de abertura nem campo de pergunta, e nenhuma consulta a
  assistente é enviada ao núcleo

### Requirement: A área detalhada explica o que a plataforma coleta, de quem, para quê e por quanto tempo

A App 06 SHALL oferecer a **área detalhada** em endereço próprio, explicando em **linguagem
simples**, para cada dado, **o que a plataforma coleta, de quem, para quê e por quanto tempo**,
e SHALL declarar que a **vitrine não coleta dado do visitante**: sem login, sem cadastro, sem
cookie de rastreio e sem perfilamento. (`RF-03-52`, `RF-03-53`, `RN-03-22`, PRD-03 §11)

#### Scenario: A área detalhada traz a tabela de coleta em linguagem simples

- **WHEN** o visitante abre a área detalhada
- **THEN** ela lista cada dado com de quem é, para quê serve e por quanto tempo é guardado

#### Scenario: A área declara que a vitrine não coleta do visitante

- **WHEN** o visitante lê a área detalhada
- **THEN** ela declara que a vitrine não coleta dado de quem visita, não instala cookie de
  rastreio nem perfila

#### Scenario: Abrir a área não deixa rastro

- **WHEN** o visitante abre a área detalhada e recarrega a página
- **THEN** `localStorage`, `sessionStorage` e cookie seguem vazios

## REMOVED Requirements

### Requirement: O assistente abre explicando a arquitetura, sem esperar a primeira pergunta

**Reason**: o assistente de chat saiu da Área do Apoiador Desenvolvedor — decisão do fundador
de 2026-11-06; `RF-03-68` e `RF-03-81` retirados do PRD-03.
**Migration**: quem chega sem saber o que perguntar lê a documentação (MkDocs) e a
documentação da API (Swagger), linkadas na área.

### Requirement: Toda mensagem do assistente termina com a escolha do próximo passo

**Reason**: o assistente saiu da área — decisão do fundador de 2026-11-06; `RF-03-69`
retirado do PRD-03.
**Migration**: nenhuma; não há mais mensagem de assistente.

### Requirement: A conversa não sobrevive à página, e nada dela é guardado no aparelho

**Reason**: sem assistente não há conversa — decisão do fundador de 2026-11-06. O "não guardar
nada do visitante" segue garantido pelo requisito "A vitrine não guarda nada do visitante, no
servidor ou no aparelho".
**Migration**: nenhuma.

### Requirement: A área segue utilizável com o assistente fora do ar

**Reason**: sem assistente não há indisponibilidade dele — decisão do fundador de 2026-11-06;
`RF-03-72` retirado do PRD-03.
**Migration**: nenhuma; documentação, Swagger, repositório e formulário são links e tela
próprios, sem dependência entre si.
