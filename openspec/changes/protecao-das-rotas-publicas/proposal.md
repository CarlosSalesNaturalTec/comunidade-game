## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Décima segunda fatia, na ordem do
documento 99 §9.

**Requisitos atendidos:** `RF-01-55` (cota da faixa da chave, com 429 no excesso),
`RF-01-65` (freio por origem na consulta por nick e nos formulários de participação e de
dados), `RN-01-27` (limite por origem e janela, com atraso progressivo, sem exigir cadastro
do visitante), `RN-01-45` (a origem nunca é gravada) e `RN-01-46` (solicitação de chave sem
freio por origem).

As onze fatias anteriores pararam aqui. A décima primeira registrou que os requisitos
restantes esperavam "os números da proteção das rotas públicas", pendentes no documento 09
§1 — e a pendência acabou de ser decidida pelo fundador e gravada no documento-fonte
(03 §§1, 8), movida no documento 09 e aplicada ao PRD-01 e ao PRD-03. Esta change é a
primeira que pode derivar dela.

Ela vem antes das rotas que protege de propósito. A cota por chave vale para **toda** rota
sob `/v1`, e todas já existem; o freio por origem compartilha com ela a mesma janela
deslizante. Entregar as duas juntas evita escrever a mesma contagem duas vezes e faz as
fatias seguintes — vitrine pública, fila de avaliação, ciclo de vida da chave — nascerem já
protegidas, em vez de precisarem de emenda depois. É o mesmo raciocínio do middleware de
auditoria da fatia anterior: infraestrutura que não se esquece, em vez de disciplina de quem
escreve rota depois.

## What Changes

- Nasce a **cota de consulta por chave**, em duas faixas. A faixa não é conceito novo: o
  modelo `ChaveDeAplicacao` já guarda `NaturezaDaChave` com `do_projeto` e `de_terceiro`
  desde a primeira fatia, e a cota se prende a essa coluna. O excesso responde **429**
  (`RF-01-55`).
- Nasce o **freio por origem**, aplicável à consulta por nick exato e ao envio dos
  formulários de participação e de dados, com atraso progressivo a cada repetição
  (`RF-01-65`, `RN-01-27`).
- Nasce a **identificação da origem** por resumo criptográfico do IP com sal rotativo,
  mantida **só em memória** pela janela do freio e **nunca gravada em banco** (`RN-01-45`).
- A **solicitação de chave fica sem freio por origem** — nova solicitação é sempre possível
  —, protegida apenas pela cota da chave da vitrine (`RN-01-46`).
- Os dois limites são **transversais**: entram como middleware sob `/v1`, e nenhuma rota
  precisa declarar nada para ser coberta pela cota. O freio por origem, que vale só nas
  três superfícies nomeadas, se prende a elas por declaração da própria rota.
- A implantação do Ciclo 01 passa a exigir **Cloud Run sem escala horizontal** — no máximo
  um contêiner de cada vez —, porque a contagem vive em memória (documento 03 §1,
  princípio 13).

### As superfícies do freio ainda não existem

Nenhuma das três rotas que o freio por origem protege foi entregue: a consulta por nick
(`RF-01-33`), o formulário de participação (`RF-01-25`) e o de dados (`RF-01-46`) são de
fatias seguintes. Esta change entrega o **mecanismo** do freio e o prende às rotas quando
elas nascerem; a cota por chave, essa sim, passa a valer de imediato em tudo o que já está
no ar.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação,
cadência de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração
do descritor no aparelho; exclusão do _template_; telemetria da Batalha de Laser e
personalização por IA.

O que é do PRD-01 mas de outra fatia:

| Fica para                        | Porque                                            |
| -------------------------------- | ------------------------------------------------- |
| `RF-01-33`, `RF-01-34`, `RF-01-43` | rotas de vitrine pública                        |
| `RF-01-25`, `RF-01-46`           | fila única de avaliação                           |
| `RF-01-49` a `RF-01-53`          | ciclo de vida da chave de terceiro                |
| `RF-01-47`                       | documento 09, "Entrega do conjunto de dados"      |
| `RF-01-22`, `RF-01-59`           | contrato de leitura dos jogos                     |
| `RF-01-24`, `RF-01-60`, `RF-01-57`, `RF-01-58` | livro-razão, PRD-07               |
| `RF-01-23` (restante), `RF-01-41` | território, PRD-08                               |
| `RF-01-31`                       | PRD-01 §14, pendência declarada                   |

Fica fora também a **base legal do resumo do IP**: é pendência aberta nesta mesma decisão
(documento 09 e PRD-01 §14), e nenhum artefato do OpenSpec a resolve.

## Capabilities

### New Capabilities

- `protecao-das-rotas-publicas`: a cota de consulta por faixa de chave com 429 no excesso, o
  freio por origem com atraso progressivo nas três superfícies nomeadas, a identificação da
  origem por resumo do IP mantido só em memória, e a ausência de freio na solicitação de
  chave.

### Modified Capabilities

- `chave-de-aplicacao`: a chave vigente passa a poder ser recusada com **429** por exceder a
  cota da sua faixa. Até aqui a única recusa da capacidade era o **401** de chave ausente,
  inválida ou revogada, e a spec afirma que a recusa não diferencia os motivos — o 429 é
  recusa de outra natureza, sobre chave reconhecida e vigente, e precisa ficar explícito que
  ele não contradiz aquela regra.

## Impact

- `backend/src/nucleo/`: módulo novo `protecao/` — a janela deslizante compartilhada, a cota
  por faixa, o freio por origem e o resumo do IP. Lê `chaves` (a `NaturezaDaChave` já
  existente) e `erros` (o corpo único de `RF-01-27`).
- `backend/src/nucleo/principal.py`: registra o middleware da cota, ao lado do de auditoria.
- `backend/src/nucleo/chaves/`: **nenhuma mudança de modelo** — a faixa já é a coluna
  `natureza`. Nenhuma migração do Alembic nesta fatia: a contagem não vai a banco.
- `docs/`: nada a atualizar. A decisão já entrou nos documentos 03, 09, PRD-01 e PRD-03 no
  commit que a gravou, antes desta change. `docs/prds/index.md` não muda de situação: o
  PRD-01 segue "aprovado", fatiado em changes.

## Questões que ficam para o `design.md`

1. **Como o tempo de espera chega a quem foi freado.** O PRD-01 §9 e o PRD-03 dizem "429,
   com o tempo de espera", sem prescrever o meio. A escolha entre o cabeçalho `Retry-After`,
   um campo no corpo único de erro ou os dois é desenho de execução, não regra de produto.
2. **Onde vive a janela deslizante** dentro do processo, e como o sal da origem roda sem
   zerar o freio no meio de uma janela.
3. **Como a cota distingue "consulta"** das demais chamadas — se ela conta toda chamada sob
   `/v1` ou só as de leitura. O documento 03 §8 diz "cota de consulta"; o recorte exato é
   leitura de desenho sobre o texto vigente, e vai declarado no design.
