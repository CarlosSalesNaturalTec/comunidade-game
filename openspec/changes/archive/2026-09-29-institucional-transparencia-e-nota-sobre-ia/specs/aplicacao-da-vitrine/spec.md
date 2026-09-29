## ADDED Requirements

### Requirement: "Quem somos" exibe o texto publicado, a nota de transparência sobre IA e o bloco "Licenças"

A App 06 SHALL exibir a seção **"Quem somos"** com o texto publicado, e a **nota de
transparência sobre IA** SHALL viver **dentro dela**, e não em seção própria, com **endereço
estável** a que o texto reescrito por IA nas demais aplicações possa apontar. O bloco
**"Licenças"** SHALL aparecer na mesma seção, e a nota SHALL remeter a ele quanto ao gerado com
auxílio de IA. Seção sem texto publicado SHALL dizer que o conteúdo **ainda não foi publicado**.
(`RF-03-45`, `RF-03-48`, PRD-03 §3.1)

#### Scenario: A nota aparece dentro de "Quem somos"

- **WHEN** o visitante abre "Quem somos" com a nota publicada
- **THEN** a nota e o bloco "Licenças" aparecem dentro da seção, cada um sob o seu título

#### Scenario: O endereço da nota leva direto a ela

- **WHEN** o visitante abre o endereço da nota de transparência
- **THEN** a vitrine mostra "Quem somos" com a nota em foco

#### Scenario: Seção sem texto não inventa conteúdo

- **WHEN** o núcleo devolve a seção sem texto
- **THEN** a tela diz que o conteúdo ainda não foi publicado, e nenhum texto de exemplo aparece

### Requirement: O vídeo de apresentação é um acesso, e nunca um player de terceiro embutido

Havendo link de vídeo em "Quem somos", a App 06 SHALL oferecer o **acesso ao vídeo de
apresentação** por link, e NEVER SHALL embutir player nem carregar recurso de terceiro ao abrir
a página, para não instalar cookie ou rastreador. Sem link, a seção SHALL sair sem espaço
vazio. (`RF-03-49`, `RF-03-51`, `RN-03-22`)

#### Scenario: Com link, a tela oferece o vídeo sem carregar terceiro

- **WHEN** "Quem somos" chega com o link do vídeo
- **THEN** a tela oferece o acesso ao vídeo, e nenhuma requisição a terceiro parte da vitrine
  antes de o visitante acionar o link

#### Scenario: Sem link, a seção não deixa espaço vazio

- **WHEN** "Quem somos" chega sem link de vídeo
- **THEN** nada aparece no lugar do vídeo

### Requirement: "Contatos" e "Como apoiar" exibem o que foi publicado, e "Como apoiar" traz a chave PIX

A App 06 SHALL exibir a seção **"Contatos"** e a seção **"Como apoiar"** com o texto publicado,
na ordem do recorte, sem publicidade nem patrocínio. Em "Como apoiar" SHALL aparecer a **chave
PIX da pessoa jurídica vinculada**, com o titular. A exibição SHALL vir do que o núcleo devolve,
e nenhum valor SHALL ficar escrito na aplicação. (`RF-03-45`, `RF-03-46`, `RN-03-21`)

#### Scenario: A chave PIX aparece em "Como apoiar"

- **WHEN** o visitante abre "Como apoiar" com o texto semeado
- **THEN** a tela mostra a chave PIX e o titular

#### Scenario: A chave publicada é a que o Admin editou

- **WHEN** o Admin republica "Como apoiar" com outra chave
- **THEN** a tela mostra a chave nova, sem depender de nova versão da aplicação

#### Scenario: Seção não publicada diz isso

- **WHEN** "Contatos" não tem texto publicado
- **THEN** a tela diz que o conteúdo ainda não foi publicado

### Requirement: Toda tela traz o aviso de coleta, com acesso à área detalhada

A App 06 SHALL exibir, em **toda tela**, incluindo a página individual, a da comunidade e os
formulários, um aviso **discreto** de que a vitrine **não coleta dado de quem visita** e de que
só os formulários gravam o que a pessoa digita, com acesso à **área detalhada**. O aviso NEVER
SHALL bloquear a tela nem exigir confirmação, e NEVER SHALL guardar no aparelho que foi visto ou
acionado. (`RN-03-23`, `RF-03-51`, PRD-03 §11)

#### Scenario: O aviso está em toda tela

- **WHEN** o visitante abre um recorte, a página de um Guerreiro(a), a página de uma comunidade
  ou um formulário
- **THEN** cada uma traz o aviso, com o acesso à área detalhada

#### Scenario: O aviso não interrompe e não deixa rastro

- **WHEN** o visitante usa a tela sem acionar o aviso
- **THEN** nada é bloqueado ou pedido, e nada é gravado no aparelho

### Requirement: A área detalhada explica o que a plataforma coleta, de quem, para quê e por quanto tempo

A App 06 SHALL oferecer a **área detalhada** em endereço próprio, explicando em **linguagem
simples**, para cada dado, **o que a plataforma coleta, de quem, para quê e por quanto tempo**,
e SHALL declarar que a **vitrine não coleta dado do visitante**: sem login, sem cadastro, sem
cookie de rastreio e sem perfilamento. SHALL declarar também que a conversa com o assistente do
Desenvolvedor não é guardada. (`RF-03-52`, `RF-03-53`, `RN-03-22`, PRD-03 §11)

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
