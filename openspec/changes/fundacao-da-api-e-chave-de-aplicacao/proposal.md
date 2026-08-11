## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Primeira entrega da ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-01`, `RF-01-02`, `RF-01-27`, `RF-01-28`, `RF-01-48`,
`RF-01-54`, `RN-01-32`, `RN-01-33`, `RN-01-34`, `RN-01-35`.

Nenhuma das oito aplicações conversa entre si: todas conversam com o núcleo. Antes de existir
persona, trilha ou território, precisa existir o porteiro — a chave de aplicação, que
`RN-01-32` põe na frente de toda rota de dados — e o contrato que todas as demais changes
reaproveitam: prefixo de versão, formato único de erro e listagem paginada com filtros.

Esta change é o piso das outras doze fatias do PRD-01. Ela existe para ser pequena: entrega o
que não depende de autenticação de persona e para exatamente onde a dependência começa. A
emissão de chave por Admin (`RF-01-50`) fica de fora porque exige uma sessão que ainda não
existe; o que entra aqui é a chave como **conferência** e as chaves do próprio projeto,
semeadas na implantação por `RF-01-54`, que é justamente o caminho que não passa por Admin.

## What Changes

- Nasce a pasta `backend/` do documento 03 §1.2, com a aplicação FastAPI em Python 3.12 e a
  esteira de CI dela — `.github/workflows/backend-ci.yml`, disparado só por `backend/**`,
  rodando `ruff format --check`, `ruff check` e `pytest`, as três bloqueando o merge.
- Toda rota de dados passa a viver sob o prefixo `/v1` (`RF-01-01`).
- Toda chamada a uma rota sob `/v1` passa a exigir chave de aplicação válida, inclusive as de
  consulta pública; sem ela, **401 que não diferencia chave ausente, inválida ou revogada**
  (`RF-01-48`, `RN-01-32`).
- Nasce a distinção entre **rota pública** e **rota autenticada**: a pública dispensa a
  credencial de persona, nunca a chave (`RF-01-02`, `RN-01-34`). As rotas públicas de conteúdo
  em si chegam nas changes seguintes; aqui nasce o mecanismo que as permitirá.
- A chave é da aplicação e não amplia direito de ninguém: não identifica visitante e não
  autoriza escrita (`RN-01-33`, `RN-01-34`).
- A implantação semeia **16 chaves** — as oito aplicações do projeto em cada um dos dois
  ambientes —, sem prazo de apresentação, guardando apenas o resumo criptográfico do segredo,
  devolvido uma única vez (`RF-01-54`, `RN-01-35`).
- Erro passa a ter corpo único, com código, mensagem em linguagem simples e campo em falta
  (`RF-01-27`).
- Listagem passa a ter contrato único de paginação e de filtros por comunidade, período e
  persona (`RF-01-28`). Nenhuma listagem existe ainda nesta change: o contrato nasce aqui e é
  exercitado pela primeira vez em `GET /v1/chaves`, na change do ciclo de vida da chave.
- O schema OpenAPI e a interface passam a ser publicados **fora do prefixo `/v1` e sem chave**,
  conforme o documento 03 §1.1.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem e geração do descritor no aparelho;
telemetria da Batalha de Laser e personalização por IA.

O que é do PRD-01 mas de outra fatia, por dependência declarada:

| Fica para                     | Porque                                                       |
| ----------------------------- | ------------------------------------------------------------ |
| `RF-01-03` a `RF-01-19`       | exigem persona autenticada, que esta change não entrega      |
| `RF-01-49` a `RF-01-53`       | solicitação, emissão e revogação exigem um Admin em sessão   |
| `RF-01-55` e `RN-01-27`       | os números seguem pendentes no documento 09                  |
| `RF-01-20` a `RF-01-26`, `RF-01-29` a `RF-01-47`, `RF-01-56` a `RF-01-60` | domínio, auditoria e rotas públicas de conteúdo |

## Capabilities

### New Capabilities

- `convencoes-da-api`: prefixo de versão em toda rota de dados, corpo único de erro, contrato
  de paginação e filtros, data e hora com fuso, e publicação do schema OpenAPI fora do
  prefixo. Atende `RF-01-01`, `RF-01-27`, `RF-01-28`.
- `chave-de-aplicacao`: conferência da chave em toda chamada sob `/v1`, o 401 indistinto,
  a distinção entre rota pública e autenticada, e as chaves do projeto semeadas por aplicação
  e por ambiente. Atende `RF-01-02`, `RF-01-48`, `RF-01-54`, `RN-01-32` a `RN-01-35`.

### Modified Capabilities

Nenhuma: `openspec/specs/` está vazio, esta é a primeira change do repositório.

## Impact

- **Pasta nova:** `backend/` — primeira pasta de código do monorepo, com a esteira de CI dela
  no mesmo PR, como o documento 03 §1.2 e o `CONTRIBUTING.md` exigem.
- **Workflow novo:** `.github/workflows/backend-ci.yml`, disparado só por `backend/**`. Não
  toca a esteira da documentação, que segue como está.
- **Banco:** primeira migração, criando `ChaveDeAplicacao` com os atributos do PRD-01 §8,
  incluindo o `ambiente` gravado nesta rodada de decisões.
- **Contrato para as demais changes:** todas as fatias seguintes do PRD-01 — e as changes de
  PRD-08 e PRD-07 — dependem do middleware de chave e do formato de erro que nascem aqui.
- **Sem implantação:** a change entrega contêiner e migração portáteis, não a subida no Cloud
  Run. O que sobe em produção é decisão de operação, fora do recorte.
- **Documentação:** o documento 03 §§1, 1.1 e 1.13, o documento 09, o PRD-01 e o
  `CONTRIBUTING.md` já foram atualizados pelas decisões que destravaram esta change.
