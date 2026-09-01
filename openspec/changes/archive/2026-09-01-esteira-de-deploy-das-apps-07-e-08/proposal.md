## Why

As Apps 07 e 08 estão completas e testadas, e **não têm endereço**. As seis fatias do PRD-13
fecharam e a fatia 1 do PRD-14 também; a esteira de CI alcança as duas desde o primeiro
_commit_ — `frontend-ci.yml` dispara por `apps/**` e roda `npm run test --workspaces
--if-present` —, mas nenhuma das duas é publicada: falta o alvo em `.firebaserc` e o workflow
de publicação. Das seis aplicações que existem em `apps/`, quatro publicam e duas não.

O `CLAUDE.md` prevê o caso: _"a change que cria uma pasta de código entrega, no mesmo PR, a
esteira daquela pasta"_. Na App 08 o adiamento foi declarado — a change
`esqueleto-da-app-08-e-desafio-extra` pôs a implantação em Non-Goals e anotou o risco. Na App
07 passou batido: a change `esqueleto-da-app-07-e-evolucao-do-guerreiro` só menciona "a esteira
de CI da pasta". O README das duas registra a lacuna com a mesma frase — _"Ainda não
implantada: o alvo de hosting … não existe em `.firebaserc`"_.

**Esta change não tem `RF-XX-nn` nem `RN-XX-nn`, e não é de um PRD.** É infraestrutura
transversal, como `isolamento-transacional-dos-testes`: não altera comportamento de produto,
não tem delta de spec e declara `skip_specs: true`. Entra na tabela **Infraestrutura
transversal (sem PRD)** do `openspec/cronograma-de-fatias.md`. Change sem identificador é
exceção à regra de rastreabilidade, e por isso precisa do aval explícito do fundador antes do
`/opsx:apply`.

Nada aqui é decisão nova. O endereço de cada aplicação em subdomínio próprio, a saída estática
no Firebase Hosting e a chave por aplicação e por ambiente são decisões vigentes do documento
03 §§1, 1.2; o desenho da esteira já foi exercido quatro vezes, em `app-01`, `app-03`, `app-05`
e `app-09`. Esta change replica esse desenho, não o reabre.

## What Changes

- `.firebaserc` ganha os dois alvos de _hosting_ que faltam: `responsavel` →
  `comunidade-game-responsavel` e `apoiador` → `comunidade-game-apoiador`, no padrão de nome
  dos cinco já existentes. O `firebase.json` **não muda**: os dois alvos já estão lá,
  apontando para `apps/app-07-responsaveis/dist` e `apps/app-08-apoiador/dist`.
- Nascem `.github/workflows/app-07-deploy.yml` e `.github/workflows/app-08-deploy.yml`,
  espelhos de `app-05-deploy.yml` — publicação **somente após _merge_ em `main`**, restrita
  aos caminhos da pasta, com Workload Identity Federation e a versão fixa da Firebase CLI.
- A seção **Implantação** do README das duas aplicações deixa de dizer "Ainda não implantada"
  e passa a apontar o workflow, o alvo e o segredo de cada uma.
- `openspec/cronograma-de-fatias.md` ganha uma linha na tabela **Infraestrutura transversal
  (sem PRD)**.
- Nenhuma mudança em `backend/`, em `apps/*/src/`, em `comum/` ou em `docs/`.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. A change não altera comportamento observável de produto: `.openspec.yaml` declara
`skip_specs: true`.

## Impact

- `.firebaserc` — dois alvos de _hosting_ acrescentados ao mapa do projeto
  `comunidade-game-506017`.
- `.github/workflows/app-07-deploy.yml` e `.github/workflows/app-08-deploy.yml` — novos.
- `apps/app-07-responsaveis/README.md` e `apps/app-08-apoiador/README.md` — seção Implantação.
- `openspec/cronograma-de-fatias.md` — uma linha.
- **Fora do repositório, pré-requisito da primeira publicação:** os dois _sites_ de _hosting_
  precisam existir no console do Firebase, e os segredos `APP07_CHAVE_DE_APLICACAO` e
  `APP08_CHAVE_DE_APLICACAO` precisam estar semeados no repositório — as chaves por aplicação
  e por ambiente do documento 03 §1, princípio 2. Sem eles o workflow falha no primeiro
  disparo. O do responsável o fundador confirmou nesta sessão; o do Apoiador segue anotado no
  design.
- Sem impacto em rota, contrato de API, modelo de dados, migração ou documentação de `docs/`.
  A esteira de CI não muda: `frontend-ci.yml` já alcança as duas pastas.
