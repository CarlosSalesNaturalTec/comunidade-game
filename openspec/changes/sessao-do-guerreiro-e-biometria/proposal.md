## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Quarta fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-04`, `RF-01-05`, `RF-01-06`, `RF-01-07`, `RF-01-08`,
`RF-01-19` (a parte do nick), `RN-01-14`, `RN-01-15`, `RN-01-16`, `RN-01-17`, `RN-01-22`,
`RN-01-30`.

As três fatias anteriores entregaram o porteiro da aplicação, o do adulto e quem responde pela
criança. Falta a própria criança entrar. `RN-01-17` não deixa o núcleo gravar o _template_ sem
consentimento do responsável registrado, e esse registro passou a existir na fatia anterior —
era o que travava esta.

É a última peça de identidade do PRD-01: entregue ela, os cinco papéis do §4 têm caminho de
entrada, e o que resta do núcleo é domínio, não autenticação.

## What Changes

- O Guerreiro(a) passa a abrir sessão por **nick e imagem**, com o descritor gerado no aparelho:
  o nick restringe a busca, o descritor confirma (`RF-01-04`, `RF-01-05`).
- A sessão do Guerreiro(a) nasce **curta e expira sozinha**, com duração declarada na
  implantação — parâmetro sem valor padrão no código, como a do adulto (`RF-01-04`).
- Imagem não reconhecida responde **401 sem revelar se o nick existe**, com a orientação de
  chamar o Mestre (`RF-01-04`, `RN-01-22`).
- Mestre ou Admin passa a **abrir a sessão por confirmação humana**, com registro de quem
  confirmou. Um só caminho para os três casos: sem _template_ gravado, falha de reconhecimento e
  biometria recusada (`RF-01-06`, `RN-01-16`).
- Nasce a **credencial biométrica**: o núcleo recebe o descritor, guarda o _template_ **cifrado**
  e o confere no login. **Nenhuma rota o devolve**, e nenhuma rota aceita imagem (`RF-01-05`,
  `RN-01-14`, `RN-01-15`).
- A gravação do _template_ é **recusada com 422 enquanto não houver consentimento do responsável
  registrado** — é assim que `RF-01-07` acontece, sem fila de descritores à espera de aprovação
  (`RF-01-07`, `RN-01-17`).
- Mestre ou Admin passa a **recadastrar** a imagem de referência pela mesma rota, com registro de
  quem recadastrou (`RF-01-08`).
- **Todo acesso ao _template_ é auditado**, inclusive cada comparação de login, com guarda
  permanente — decisão gravada no documento 03 §3.3 e aplicada ao PRD-01 §11 (`RN-01-14`).
- O **nick** passa a ser atributo da persona do Guerreiro(a), **único em toda a plataforma**, sem
  o qual não há entrada. A busca por nick é sempre exata: o núcleo não lista, não completa e não
  sugere (`RF-01-19`, `RN-01-22`, `RN-01-30`).

### O que esta fatia não tem, e não é omissão

A rota que **cria** o Guerreiro(a) não é do PRD-01: `POST /v1/guerreiros` e
`GET /v1/guerreiros/nick/disponivel` estão no PRD-04, que conduz o autocadastro no encontro. O
PRD-01 §9 não declara nenhuma das duas.

O que cabe aqui é o que `RF-01-19` põe sob a guarda do núcleo — a **entidade e as invariantes**
do nick — e as rotas de sessão e de descritor, que o PRD-01 §9 declara. É o mesmo recorte da
fatia anterior, que entregou a entidade `Consentimento` sem criar rota que a escrevesse.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência de
coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração do descritor no
aparelho; telemetria da Batalha de Laser e personalização por IA.

O que é do PRD-01 mas de outra fatia, por dependência declarada ou por pendência aberta:

| Fica para                           | Porque                                                            |
| ----------------------------------- | ----------------------------------------------------------------- |
| `RF-01-32`                          | a aula agendada que habilita o App 01 é entidade de operação      |
| `RF-01-33` e `RF-01-34`             | a consulta pública por nick é rota de vitrine, de outra fatia     |
| `RF-01-17`                          | o painel do dia só existe quando App 03 e App 09 existirem        |
| `RF-01-29`                          | a trilha de auditoria consultável é rota de Admin, de outra fatia |
| `RF-01-49` a `RF-01-53`, `RF-01-55` | documento 09, "Números da proteção das rotas públicas"            |
| `RF-01-20` a `RF-01-26`, `RF-01-30` a `RF-01-47`, `RF-01-56` a `RF-01-60` | domínio, ODS, operação e rotas públicas de conteúdo |

O **teto de tentativas** por chegada segue com `RN-01-27` no documento 09, como nas duas fatias
anteriores. A **duração da sessão** e o **limiar de comparação** não são pendência: são parâmetro
declarado na implantação, sem valor padrão no código (documento 09, "Parâmetros da entrada do
Guerreiro(a)").

## Capabilities

### New Capabilities

- `sessao-do-guerreiro`: abertura de sessão por nick e imagem, a recusa que não revela o nick, a
  confirmação humana como alternativa equivalente e a expiração curta.
- `template-biometrico`: guarda cifrada do _template_, conferência no login, gravação condicionada
  ao consentimento, recadastro e auditoria de todo acesso.

### Modified Capabilities

- `persona-e-credencial`: o nick passa a ser atributo do Guerreiro(a), único em toda a plataforma
  e obrigatório para a entrada; a busca por nick é exata, sem listagem nem sugestão.

## Impact

- `backend/src/nucleo/`: módulos novos para a credencial biométrica e para a sessão do
  Guerreiro(a); `sessoes/` ganha os dois caminhos de abertura que `ComoAutenticou` já previa
  (`biometria` e `confirmacao_humana`); `personas/` ganha o nick.
- `backend/alembic/`: migração para o nick, para a credencial biométrica e para o registro de
  acesso ao _template_.
- `backend/src/nucleo/configuracao.py`: duração da sessão do Guerreiro(a) e limiar de comparação,
  ambos sem valor padrão — o ambiente que não declarar não sobe, como já vale para a sessão do
  adulto. Entra também a chave de cifragem, que o Cloud Run popula a partir do Secret Manager e
  outra hospedagem popula direto, preservando a portabilidade do documento 03 §1.
- `docs/`: as decisões desta fatia já estão gravadas — documento 03 §3.3, PRD-01 §§11, 13 e 14 e
  documento 09. Resta a situação em `docs/prds/index.md`, se ela mudar ao fim da implementação.
