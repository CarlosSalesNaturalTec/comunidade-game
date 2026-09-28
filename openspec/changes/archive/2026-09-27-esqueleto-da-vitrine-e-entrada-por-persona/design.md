# Design

## Context

Nada do que esta fatia entrega é regra nova, e quase nada é padrão novo. A `camada-visual-comum`
já declara a camada de tema dos dois temperamentos e já atribui **Arena** à App 06, já serve as
duas famílias tipográficas pelo próprio domínio e já entrega `Dialogo`, `Botao`, `Cabecalho`,
`Aviso` e o sistema de ícone com o piso de acessibilidade do documento 15. A
`camada-de-acesso-comum` já monta a chamada por chave de aplicação. A chave `app-06-vitrine` está
semeada nos dois ambientes, o alvo de publicação `vitrine` já existe em `firebase.json` apontando
para `apps/app-06-vitrine/dist`, e `frontend-ci.yml` já alcança `apps/**` pelos _workspaces_.

Falta a pasta, falta a publicação e falta uma decisão que as sete fatias seguintes herdam: **como
a vitrine navega**. É o que este desenho fixa; o resto é aplicação de padrão consolidado.

## Goals / Non-Goals

**Goals:**

- A App 06 de pé no molde das outras seis, com o temperamento Arena e sem nada guardado no
  aparelho.
- Uma forma de navegação que as fatias 2 a 8 possam usar sem refazer o esqueleto: endereço real
  por seção, porque a §10 do PRD-03 pede indexação das seções institucionais e de comunidade e a
  jornada 5.7 pede que o endereço direto de uma página responda "não encontrado".
- A esteira de publicação da pasta, no mesmo PR que a cria.

**Non-Goals:**

- Consumir rota do núcleo: nenhuma tela desta fatia lê dado. O cliente de API entra montado, com
  a chave, para as fatias seguintes o usarem.
- Pré-renderização ou renderização no servidor: ver _Risks_.
- Conteúdo de cada recorte — o bloco do gestor público é `RF-03-63` a `RF-03-65`, fatia 3.

## Decisions

### 1. A pasta nasce no molde da App 08, com a Arena da App 05

`apps/app-06-vitrine/` copia a estrutura de `apps/app-08-apoiador/` — Vite, React, TS,
`index.html`, `vite.config.ts`, `tsconfig*`, `.env.example`, `README.md` e favicon — e declara
`data-temperamento="arena"` na raiz do documento, como `apps/app-05-guerreiro/index.html`. A pasta
entra no _workspace_ do `package.json` da raiz; nenhum workflow de CI nasce.

**Diferença de molde:** a vitrine **não depende de `comum/autenticacao`**. Aquele pacote guarda
token em `sessionStorage`, e a App 06 não pode guardar nada (`RF-03-51`, `RN-03-22`). Sem
`VITE_GOOGLE_CLIENT_ID`, sem provedor de sessão, sem `limparToken`.

### 2. A navegação é por endereço real, sobre a History API, sem dependência nova

Cada seção da vitrine tem um caminho próprio (`/`, `/pesquisadores`, `/gestores-publicos`, e o que
as fatias seguintes acrescentarem), lido de `window.location.pathname` e trocado por
`history.pushState`, com `popstate` para voltar. É código da própria aplicação — algumas dezenas
de linhas —, não biblioteca.

_Descartado:_ navegação só por estado da aplicação, como a App 03 faz com `?area=`: serve a uma
aplicação autenticada que ninguém indexa, e obrigaria a refazer o esqueleto na fatia 2, quando a
página individual precisa de endereço direto. _Descartado:_ uma biblioteca de rotas, que é escolha
de _framework_ não decidida nos documentos e não existe em nenhuma pasta do monorepo.

Para o endereço direto resolver, o alvo `vitrine` de `firebase.json` ganha a reescrita
`** → /index.html`, como o alvo `app-03` já tem.

### 3. O recorte de leitura é caminho, e não é guardado

O recorte corrente vem do caminho: a raiz é **sociedade civil** (`RF-03-25`) e os outros dois têm
caminho próprio, o que os torna compartilháveis e indexáveis. Nada é gravado: quem volta à raiz
volta ao recorte padrão, porque não há onde a escolha anterior estar (`RF-03-26`, `RF-03-51`).

Trocar de recorte muda a porta de entrada e a ordem, nunca o conjunto de dados públicos nem o
direito de acesso — a fatia entrega a navegação e a ordem; o conteúdo de cada recorte chega com a
fatia que o tem.

### 4. O "Entrar" é um diálogo de seis destinos, e os endereços vêm da esteira

O botão fica no `Cabecalho`, visível em toda tela, e abre o `Dialogo` de `comum/react` — que já
prende o foco, fecha por `Esc` e devolve o foco a quem abriu — com as seis personas do PRD-03
§5.9. Escolhida a persona, o destino é um endereço externo; escolhido "ainda não tenho cadastro",
a mesma tela dá a orientação daquela persona (`RF-03-62`).

Os seis endereços entram por **variável de ambiente do Vite**, uma por ambiente, como
`VITE_URL_DO_NUCLEO` já faz. O documento 03 §1.1 fixa os endereços de destino, mas as esteiras de
publicação usam hoje os `*.web.app` enquanto o domínio não passa no filtro da rede corporativa —
fixar o endereço no código quebraria em um dos dois ambientes.

_Descartado:_ gravar os endereços do documento 03 §1.1 no código.

### 5. Nada guardado é estrutural, não é limpeza

A aplicação não lê nem escreve `localStorage`, `sessionStorage`, IndexedDB ou cookie, e não carrega
recurso de domínio de terceiro — as fontes vêm de `comum/fontes`, servidas pelo próprio domínio. A
ausência é conferida por teste que percorre uma visita inteira, e não por uma rotina de limpeza:
não há o que limpar (`RF-03-51`, `RN-03-22`).

O espaço de publicidade não existe no _layout_ (`RF-03-50`): não é um bloco vazio nem um
componente desligado.

### 6. A publicação sai no molde das outras seis

`.github/workflows/app-06-deploy.yml` copia `app-08-deploy.yml`: gatilho por
`apps/app-06-vitrine/**`, `comum/**`, `firebase.json`, `.firebaserc` e o próprio arquivo;
autenticação por Workload Identity Federation; `firebase-tools` na mesma versão fixa das demais; e
`--only hosting:vitrine`. As variáveis são `VITE_CHAVE_DE_APLICACAO`
(`secrets.APP06_CHAVE_DE_APLICACAO`), `VITE_URL_DO_NUCLEO` e os seis endereços de destino — sem
`VITE_GOOGLE_CLIENT_ID`, que a vitrine não usa.

O alvo `vitrine` entra em `.firebaserc` apontando para o site `comunidade-game-vitrine`, no padrão
dos seis irmãos. Criar o site e apontar o **domínio da raiz** para ele são atos no console do
projeto, do fundador, como foi com `api.comunidadegame.org`.

## Risks / Trade-offs

- **Indexação de página renderizada no cliente.** A §10 do PRD-03 pede que as seções
  institucionais e de comunidade sejam indexáveis. Esta fatia entrega endereço real para cada uma,
  que é a condição necessária, mas o conteúdo é montado por JavaScript. Se a indexação não vier,
  pré-renderizar é decisão de arquitetura: vai ao fundador e ao documento 09, não se resolve aqui.
- **A vitrine só está de fato na raiz quando o domínio for apontado.** Até lá ela responde no
  endereço `*.web.app`, como as outras seis — `RF-03-01` fica cumprido no código e pendente na
  infraestrutura.
- **Seis endereços na esteira.** Endereço de aplicação que mude obriga a mexer no workflow. É o
  preço de não gravar endereço no código, e vale porque os dois ambientes já divergem hoje.
- **A orientação do Mestre nasce sem link.** `RF-03-62` só fica inteiro quando a fatia 4 criar o
  formulário de participação; até lá a orientação nomeia o caminho em texto, como a porta pública
  da App 08 já faz com o endereço da vitrine que ainda não existia.
- **Um esqueleto sem dado é difícil de avaliar.** A fatia entrega navegação e entrada, e as telas
  das seções chegam vazias, nomeadas pelo que virá. É o custo de a fatia 1 ser esqueleto, e o
  cronograma já a recortou assim.
