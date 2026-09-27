# Esqueleto da vitrine e entrada por persona

Origem: **PRD-03 — App 06: Vitrine pública**, §§3, 4, 5.9, 6.2, 6.5, 7 e 10.
**Fatia 1** do PRD-03 no `openspec/cronograma-de-fatias.md`.

Atende `RF-03-01`, `RF-03-25`, `RF-03-26`, `RF-03-50`, `RF-03-51`, `RF-03-58` a `RF-03-62`,
`RN-03-01`, `RN-03-21`, `RN-03-22`, `RN-03-27` e `RN-03-33`.
`RF-03-62` é atendido **em parte** — a orientação do Mestre nomeia o formulário de participação
sem link, porque o formulário nasce na fatia 4 (§_Fora do escopo_).

## Why

Das oito aplicações do Ciclo 01, a vitrine é a última sem pasta — e é a que ocupa a **raiz do
domínio**. O núcleo já serve quase tudo o que ela mostra: as seis rotas de
`leitura-publica-da-vitrine`, as do território, as necessidades e as três solicitações públicas,
todas com o freio por origem, e a chave `app-06-vitrine` já está semeada nos dois ambientes. Não
há cliente que consuma nada disso, e as sete fatias seguintes do PRD-03 não têm onde entrar.

Falta também a porta de entrada da plataforma inteira: hoje cada aplicação só é alcançável por
quem já conhece o endereço dela. O botão "Entrar" da vitrine é o encaminhamento que o documento
03 §1.1 previu e que nenhuma aplicação pode oferecer no lugar dela.

## What Changes

### A App 06 nasce, com o temperamento Arena e sem nada guardado no aparelho (PRD-03 §§3, 10)

`apps/app-06-vitrine/` entra no monorepo no molde das outras seis, consumindo `comum/`:

- abre **sem login e sem cadastro**, e nenhuma tela oferece área restrita (`RF-03-01`,
  `RN-03-01`);
- declara o temperamento **Arena** na raiz do documento, cuja camada de tema já existe em
  `camada-visual-comum` (documento 15 §6);
- chama o núcleo com a **chave da própria aplicação** e sem credencial de persona: o visitante
  segue anônimo (`RN-03-33`);
- **não grava nada do visitante** — nem cookie, nem rastreador, nem preferência no aparelho
  (`RF-03-51`, `RN-03-22`);
- **não veicula publicidade nem patrocínio**, e nenhum espaço da página é reservado a isso
  (`RF-03-50`, `RN-03-21`).

Nenhuma rota nova e nenhuma entidade: a fatia é de cliente. O que a aplicação consome nesta
fatia é a navegação; as seções com cards, o painel do território, os formulários e o
institucional são as fatias 2 a 8.

### Os três recortes de leitura entram como navegação (PRD-03 §6.2)

A aplicação abre no recorte **sociedade civil** sem que se escolha nada, e oferece os recortes
**pesquisadores** e **gestores públicos** (`RF-03-25`). Trocar de recorte é navegação: muda a
porta de entrada e a ordem, não o conteúdo, não o direito de acesso e não cria área restrita,
cadastro nem coleta de dado (`RF-03-26`). O recorte corrente **não é guardado** em lugar nenhum.

O bloco em destaque do gestor público (`RF-03-63` a `RF-03-65`) e o conteúdo de cada recorte
chegam com as fatias que os têm — 3 em diante. Aqui o recorte é o esqueleto que as recebe.

### O botão "Entrar" encaminha cada persona à aplicação dela (PRD-03 §5.9)

Sempre visível, o botão pergunta **quem está entrando** e encaminha (`RF-03-58`, `RF-03-59`):
Guerreiro(a) à App 05, responsável à App 07, Mestre à App 09, Apoiador à App 08, gestão à App 03
e o **aparelho da aula** à App 01. A vitrine **nunca autentica**: nick e imagem, login social e
usuário e senha são conferidos na aplicação de destino (`RN-03-27`).

- A escolha de persona **não é guardada**: quem volta encontra a mesma pergunta (`RF-03-60`).
- Nenhuma tela do "Entrar" revela nick, conta ou a existência de cadastro — sem lista, sem
  sugestão, sem confirmação (`RF-03-61`).
- Quem não tem cadastro recebe a orientação da **sua** persona, sem promessa de acesso
  (`RF-03-62`): pré-cadastro da App 08 para quem quer ser Apoiador, formulário de participação
  para quem quer ser Mestre, e **procurar a gestão no encontro** para responsável e
  Guerreiro(a).

### A esteira da pasta nova sai no mesmo PR

`frontend-ci.yml` já alcança `apps/**` pelos _workspaces_, e a pasta só precisa entrar no
`package.json` da raiz. Falta a **publicação**: `app-06-deploy.yml` no molde das outras seis e o
alvo `vitrine` em `.firebaserc` — o alvo já existe em `firebase.json`, apontando para
`apps/app-06-vitrine/dist`, e ganha aqui a reescrita que faz um endereço direto resolver.

## Capabilities

### New Capabilities

- `aplicacao-da-vitrine`: a App 06 — a superfície pública sem login nem cadastro na raiz do
  domínio, o temperamento Arena, a ausência de cookie, rastreador, publicidade e preferência de
  visitante, os três recortes de leitura como navegação e o botão "Entrar" que encaminha cada
  persona à aplicação dela sem autenticar ninguém.

### Modified Capabilities

Nenhuma. `camada-visual-comum` já declara a camada de tema da Arena e já atribui o temperamento
Arena à App 06; `camada-de-acesso-comum` já entrega a chamada por chave de aplicação; e
`leitura-publica-da-vitrine` não muda de requisito — esta fatia não consome rota nenhuma dela.

## Impact

- **Código novo**: `apps/app-06-vitrine/`, `.github/workflows/app-06-deploy.yml`, o alvo
  `vitrine` em `.firebaserc`, a reescrita do mesmo alvo em `firebase.json` e a pasta no
  _workspace_ do `package.json` da raiz.
- **Código lido**: `apps/app-08-apoiador/` e `apps/app-05-guerreiro/` (molde da pasta e da
  Arena), `comum/react` (camada visual e ícone), `comum/api` (cliente e chave), `firebase.json`,
  `.firebaserc` e `.github/workflows/app-08-deploy.yml`.
- **Sem backend**: nenhuma rota, nenhuma entidade, nenhuma migração. A chave `app-06-vitrine` já
  está semeada.
- **Documentação**: a fatia 1 marcada como implementada no cronograma e o PRD-03 passado a em
  implementação em `docs/prds/index.md`. Nenhuma decisão nova, nenhum arquivo novo em `docs/`.
- **Fora do escopo**, como o PRD-03 §3.2 já exclui: login, cadastro e área restrita; favorito e
  qualquer preferência do visitante; o pré-cadastro de Apoiador, que é tela da App 08; avaliação
  das solicitações, emissão de chave e entrega de dados, atos de Admin na App 03; edição do
  conteúdo institucional; o jogo da App 04; qualquer canal de contato com Guerreiro(a) ou
  família; notificação por e-mail; publicidade e patrocínio; e dado abaixo do bairro. Fora desta
  fatia, mas dentro do PRD-03: os cards e as páginas individuais, o portfólio e os rankings
  (fatia 2), o painel do território e a cobertura da Agenda 2030 com o bloco do gestor (fatia
  3), os dois formulários públicos (fatia 4), o institucional, a transparência e a nota sobre IA
  (fatia 5), a chamada "Quero participar" e as necessidades em aberto (fatia 6), Mestres e
  Apoiadores (fatia 7) e a Área do Apoiador Desenvolvedor (fatia 8). Fora por dependência de
  fatia posterior: o **link** do formulário de participação na orientação de `RF-03-62`, que a
  fatia 4 cria — aqui a orientação nomeia o caminho em texto, sem link quebrado, como a porta
  pública da App 08 já faz com o endereço da vitrine.
