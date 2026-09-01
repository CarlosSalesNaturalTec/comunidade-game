## Context

Ver `proposal.md` — Why. O padrão de publicação já está consolidado em quatro workflows —
`app-01-deploy.yml`, `app-03-deploy.yml`, `app-05-deploy.yml` e `app-09-deploy.yml` —, todos
com a mesma forma: gatilho por `push` em `main` restrito aos caminhos da pasta, `npm ci` na
raiz do monorepo, `npm run build` na pasta da aplicação com as variáveis `VITE_*` do ambiente,
autenticação por Workload Identity Federation e `firebase deploy --only hosting:<alvo>`.

O que falta às Apps 07 e 08 é só isso. O `firebase.json` já traz os alvos `responsavel` e
`apoiador` apontando para o `dist` de cada uma — foram escritos junto com os demais, quando o
arquivo nasceu. As duas aplicações são gêmeas na forma: mesmo `build` (`tsc -b && vite build`)
e as mesmas três variáveis (`VITE_CHAVE_DE_APLICACAO`, `VITE_GOOGLE_CLIENT_ID`,
`VITE_URL_DO_NUCLEO`), como o `.env.example` de cada uma registra.

## Goals / Non-Goals

**Goals:**

- As Apps 07 e 08 publicadas em `responsavel.comunidadegame.org` e
  `apoiador.comunidadegame.org` (documento 03 §1), pelo mesmo desenho das outras quatro.
- Nenhuma divergência entre as seis esteiras: o que muda de uma para outra é a pasta, o alvo
  e o segredo da chave — mais nada.

**Non-Goals:**

- **Criar os _sites_ no console do Firebase** e **semear os segredos**: são atos de
  infraestrutura e de implantação, fora do repositório. Ver Risks.
- **Ambiente de _preview_ por PR.** Nenhuma das quatro esteiras existentes tem, e o
  `CLAUDE.md` fixa que a publicação acontece somente após _merge_ em `main`.
- **Reverter o contorno de `VITE_URL_DO_NUCLEO`.** Depende de ato do TI, sem prazo; a
  pendência está no documento 09 e o contorno se repete aqui como nas outras quatro.

## Decisions

### Dois workflows, e não um só com matriz

Cada aplicação recebe o seu, no molde de `app-05-deploy.yml`. O `CLAUDE.md` fixa que _"cada
workflow em `.github/workflows/` dispara só pelo caminho que cobre"_: um workflow com matriz
sobre as duas aplicações publicaria as duas a cada _merge_ que tocasse qualquer uma, e o
`concurrency` de uma bloquearia a outra. Duplicação de ~70 linhas é o preço, e é o preço que
as outras quatro já pagam — uniformidade vale mais que economia de linha em arquivo que
quase não muda.

_Alternativa descartada:_ workflow reutilizável (`workflow_call`) parametrizado por pasta e
alvo — divergiria das quatro esteiras existentes e exigiria reescrevê-las para valer a pena.

### O nome do _site_ segue `comunidade-game-<alvo>`

`comunidade-game-responsavel` e `comunidade-game-apoiador`, no padrão dos cinco já mapeados
em `.firebaserc` (`comunidade-game-api`, `-app-03`, `-mestre`, `-aula`, `-minhaarea`). O do
responsável foi confirmado pelo fundador nesta sessão; o do Apoiador aplica o mesmo padrão.

### `comum/**` continua no gatilho das duas

Como nas quatro existentes: a camada visual comum entra no _bundle_ de cada aplicação, e
_merge_ que a altere precisa republicar quem a consome. O efeito é que um _commit_ em `comum/`
dispara as seis publicações — é o comportamento correto, não um excesso.

### A versão da Firebase CLI permanece fixa em `15.28.1`

A mesma das quatro. A CLI é baixada a cada publicação; sem fixá-la, o comportamento do deploy
muda sozinho entre duas execuções. Subir a versão é ato revisado, e subir em todas de uma vez.

## Risks / Trade-offs

- **O _site_ de _hosting_ não existe no console do Firebase no primeiro disparo** → o
  workflow falha no passo de publicação, e nada é publicado — falha alta e inofensiva,
  reexecutável por `workflow_dispatch` assim que o _site_ existir. Mesmo desenho aceito em
  `app-01-deploy.yml`, cujo _commit_ registra que _"o alvo `comunidade-game-aula` precisa
  existir no console do Firebase antes do primeiro disparo"_. O do responsável o fundador
  confirmou; **o `comunidade-game-apoiador` continua pendente e é pré-requisito da App 08**.
- **Os segredos `APP07_CHAVE_DE_APLICACAO` e `APP08_CHAVE_DE_APLICACAO` não estarem semeados**
  → a aplicação sobe com a chave vazia e o núcleo não responde a ela. Comportamento esperado
  e já aceito na App 05, cujo design registra que _"até as duas chaves de aplicação serem
  semeadas, o núcleo não responde a ela"_. A publicação não depende do segredo; o
  funcionamento sim.
- **O contorno de `VITE_URL_DO_NUCLEO` se espalha para a quinta e a sexta esteira** → seis
  lugares a reverter quando o TI liberar `*.comunidadegame.org`, em vez de quatro. O
  comentário `TEMPORÁRIO` se repete em cada uma, e a pendência está no documento 09; reverter
  é uma linha por arquivo, tudo numa change.
- **Publicar não é conferir** → nenhum passo do workflow verifica que a aplicação subiu de
  pé. É o mesmo limite das quatro existentes; conferência de saúde pós-publicação não está
  decidida em nenhum documento e não se inventa aqui.
