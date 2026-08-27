# CLAUDE.md — Regras de trabalho neste repositório

Repositório do **Comunidade Game** — plataforma educacional gamificada, open source, para
comunidades periféricas. É um **monorepo**: a documentação do produto em `docs/`, o
planejamento da implementação em `openspec/` e o código — o Backend API, as oito aplicações e
os jogos. O desenho das pastas está no documento 03 §1.2.

## Estado atual

1. **Feito:** revisão e validação humana de todos os documentos de `docs/` (agosto de 2026).
2. **Feito:** os treze **PRDs** (_Product Requirements Documents_) do Ciclo 01, em
   `docs/prds/`, escritos a partir de `docs/08-base-para-prds.md` e aprovados pelo fundador.
3. **Agora:** implementação dos PRDs, conduzida pelo framework de **SDD** (_Spec-Driven
   Development_) **OpenSpec**, uma fatia por _change_.

Qual PRD está em implementação não se escreve aqui — é estado, e muda a cada entrega. Onde
lê-lo:

| Para saber                          | Leia                                                        |
| ----------------------------------- | ----------------------------------------------------------- |
| A situação de cada PRD              | `docs/prds/index.md` — só a tabela do topo                  |
| Qual é a próxima fatia, e o recorte | `openspec/cronograma-de-fatias.md` — só o bloco do PRD alvo |
| As fatias já entregues de um PRD    | `openspec/cronograma-de-fatias.md` — o mesmo bloco          |
| A ordem em que os PRDs viram código | documento 99 §9 — não é a ordem do documento 08             |
| As changes em andamento             | `openspec list`, `openspec status --change <nome>`          |
| O porquê de uma fatia já fechada    | `openspec/changes/archive/<slug>/`                          |

Código entra **apenas** por uma _change_ do OpenSpec cujos artefatos foram aprovados pelo
fundador. PRD novo ou revisão de PRD existente segue as regras de `docs/prds/` abaixo.

Qual fatia vem a seguir **não se redescobre a cada change**: está no
`openspec/cronograma-de-fatias.md`, com número, recorte (`RF-XX-nn`, `RN-XX-nn`), dependência e
situação. `/opsx:propose fatia N do PRD-XX` basta; `/opsx:explore` é para pensar quando algo não
está claro, não etapa obrigatória. Fatia que não está lá, ou recorte que precisa mudar, é
decisão de planejamento: pergunte ao fundador e corrija o cronograma antes de abrir a change.

## Hierarquia de autoridade

| Nível | Artefato                                | Papel                                |
| ----- | --------------------------------------- | ------------------------------------ |
| 1     | `docs/01-*` a `docs/14-*` e `docs/99-*` | regra de negócio (fonte única)       |
| 2     | `docs/prds/`                            | requisitos de produto (RF-XX, RN-XX) |
| 3     | `openspec/changes/<change>/`            | plano de execução                    |
| 4     | código                                  | execução                             |

Cada nível apenas executa o de cima. Conflito resolve-se pelo nível superior — nunca ajustando
o PRD ao código já escrito.

**Decisão nova nunca nasce num PRD nem num artefato do OpenSpec.** O fluxo é sempre:
documento-fonte (doc 99 §1) → linha movida no documento 09 de "Decisões pendentes" para "Já
decididos" → PRD afetado → change. Requisito faltando, ambíguo ou em contradição com o PRD:
**pare e pergunte ao fundador**; não preencha lacuna com suposição.

Stack, hospedagem, armazenamento das séries temporais e reconhecimento facial já estão
decididos no documento 03 — aplique o que está lá, não reabra. O que segue pendente está na
§14 do PRD alvo e no documento 09 §1.

## Regras de redação e revisão dos documentos de `docs/`

Valem para **toda** solicitação de ajuste de texto nessa pasta — novas seções, correções,
reescritas ou incorporação de decisões novas.

### 1. Concisão é requisito, não estilo

Os documentos são lidos por **pessoas**. Escreva o mínimo necessário para a decisão ficar
clara: tabela e lista antes de parágrafo, uma frase antes de três. **Corte a justificativa
redundante** — quando a razão for indispensável para não se perder a intenção, guarde-a em
**uma** frase. Não repita a mesma ideia na abertura, no corpo e no fechamento da seção, e não
use ênfase decorativa: negrito só no que é definição, regra ou termo do domínio.

**Exceções:** `docs/08-base-para-prds.md` e os arquivos de `docs/prds/` **podem** ter
detalhamento extenso. Só eles.

### 2. Fonte única — nunca duplicar

Cada assunto tem **um** documento normativo, listado em `docs/99-mapa-de-referencias.md` §1.
Ao alterar uma regra, altere **o documento-fonte** dela. Outro documento que precise mencionar
o assunto resume em **uma frase**, sem repetir a regra completa, a tabela nem os números. Ao
encontrar duplicidade, consolide no documento-fonte e reduza a menção nos demais.

`docs/prds/index.md` é **índice**, não diário: registra a situação de cada PRD e nada mais. A
lista das fatias — as entregues e as que faltam — é do `openspec/cronograma-de-fatias.md`; o
requisito, a decisão e o porquê de uma fatia moram no `proposal.md`/`design.md` da change
(`openspec/changes/archive/`) e, quando for decisão nova, no documento 09 §1. Fechar uma fatia
muda **uma linha** do cronograma, nunca acrescenta parágrafo a `index.md`; texto que reconta o
que outro documento já registra é a duplicidade que esta regra proíbe.

### 3. Referências entre documentos ficam no doc 99

- Os documentos 01–15 **não** carregam links `[XX §Y](arquivo.md#ancora)` entre si. Quando o
  leitor humano precisar mesmo ser encaminhado, escreva em texto simples: _"(documento 05)"_.
  A exceção é `docs/index.md`, cuja função é justamente indexar e linkar os demais.
- Todo o mapa de relações — fonte única, dependências, conceitos, aplicações → PRDs,
  rastreabilidade e invariantes — vive em `docs/99-mapa-de-referencias.md`, que existe para
  orientar agentes de IA, não humanos. **Toda alteração que mude a relação entre documentos
  exige atualizar o doc 99.**

### 4. Preservar o sentido original

Melhorar a redação **nunca** significa mudar a decisão. Mantenha as definições vigentes, os
números, os nomes próprios e o tom do projeto (linguagem direta, popular quando couber, sem
jargão corporativo). Não invente regra, número, prazo nem provedor: o que falta decidir é
marcado como pendência. Não remova uma definição por parecer redundante sem verificar se o
outro documento realmente a contém.

### 5. Marcações padronizadas

- **`[Proposta]`** — ideia ainda **não decidida** pelo fundador. Tudo que não estiver marcado é
  definição vigente.
- **`> **A definir:**`** — lacuna que precisa de número ou critério. Toda pendência nova deve
  também entrar na tabela do documento 09.
- **`**Definição vigente**`** — decisão tomada, quando o contraste com uma proposta próxima
  ajudar o leitor.

### 6. Coerência e formatação

- Antes de fechar a edição, confira os **invariantes** de `docs/99-mapa-de-referencias.md` §6.
  Contradizer um deles é erro de documentação, não variação de redação.
- Confira numeração de seções contínua, títulos coerentes com `docs/index.md` e com a `nav` do
  `mkdocs.yml`, e tabelas com totais que fecham.
- Português do Brasil, linhas de até ~95 caracteres fora de tabelas e blocos de código.
- Títulos em sentença (`## 3. Trilhas`), não em caixa alta. Negrito não é título: se é título,
  use `####`.
- Tabelas para catálogos e regras comparativas; blocos de código apenas para diagramas ASCII,
  trechos de código e payloads — **sempre com linguagem** (diagrama ASCII usa ` ```text `).
- **Todo arquivo novo em `docs/` precisa entrar na `nav` do `mkdocs.yml`**, senão o build
  `--strict` falha. Links de domínios que bloqueiam robôs (LinkedIn, Google Drive, Phaser)
  ficam em `.lycheeignore` e são conferidos à mão quando mudarem.

## Regras dos PRDs (`docs/prds/`)

Valem todas as regras acima, com as diferenças abaixo.

### 1. O PRD é derivado — nunca fonte única

O PRD **aplica** as regras dos documentos 01–15; não cria regra própria. Decisão nova tomada
durante a escrita de um PRD segue o fluxo da hierarquia de autoridade acima, e o PRD a aplica
**sem repetir** tabela, número ou texto normativo. Regra que existe apenas dentro de um PRD
está no lugar errado.

### 2. Elicitação antes da redação

Antes de escrever um PRD, listar as pendências do documento 09 e as questões em aberto do
documento 08 que **travam** aquele PRD e perguntá-las ao fundador. Não preencher lacuna com
suposição nem escrever o PRD inteiro marcado como `[Proposta]`.

### 3. Estrutura e extensão

- Estrutura obrigatória: `docs/prds/00-modelo-de-prd.md`. Nenhuma seção é suprimida; seção
  sem conteúdo recebe "não se aplica" com o motivo em uma linha.
- Requisitos e regras recebem identificador (`RF-XX-nn`, `RN-XX-nn`) e enunciado verificável.
- Detalhamento extenso é permitido; a **linha de 95 caracteres continua valendo**.
- Um PRD cita outro pelo identificador (_"PRD-01"_), em texto simples, sem link. O mapa de
  arquivos e dependências fica no documento 99 §8.

### 4. Entrega

Um branch e um PR por PRD, aprovado antes do próximo. No mesmo PR: o arquivo do PRD, a
situação atualizada em `docs/prds/index.md`, a entrada na `nav` do `mkdocs.yml`, o documento
99 §8 e o que a decisão nova mudou nos documentos-fonte e no documento 09.

## Regras de implementação (`openspec/`)

A implementação é conduzida pelo **OpenSpec**. As regras de cada artefato estão em
`openspec/config.yaml` — este arquivo não as repete.

### 1. Rastreabilidade obrigatória

- A `proposal` nomeia o PRD de origem e os identificadores (`RF-XX-nn`, `RN-XX-nn`) que
  atende; `specs` e `tasks` repetem o identificador em cada item.
- Os invariantes do documento 99 §6 valem para o código como valem para o texto.

### 2. Fluxo

| Etapa                                     | Comando              |
| ----------------------------------------- | -------------------- |
| Pensar antes de abrir change              | `/opsx:explore`      |
| Criar a change e os artefatos             | `/opsx:propose`      |
| Criar a change vazia, para conduzir à mão | `/opsx:new`          |
| Avançar um artefato por vez               | `/opsx:continue`     |
| Gerar de uma vez o que falta              | `/opsx:ff`           |
| Implementar as tarefas                    | `/opsx:apply`        |
| Verificar antes de fechar                 | `/opsx:verify`       |
| Arquivar a change concluída               | `/opsx:archive`      |
| Arquivar várias de uma vez                | `/opsx:bulk-archive` |

Os artefatos de cada change ficam em `openspec/changes/<change>/`, na ordem `proposal` →
`specs` → `design` → `tasks`; ao arquivar, o delta é consolidado em `openspec/specs/`.
`openspec list`, `openspec status --change <nome>` e `openspec validate --all` conferem o
estado pelo terminal. Os comandos e as skills em `.claude/` são vendorizados do OpenSpec e se
atualizam com `openspec update` — não os edite à mão; o que precisar ser ajustado para este
projeto entra em `openspec/config.yaml` ou aqui.

### 3. Documentação a cada change

A documentação do MkDocs anda junto com a implementação: **nenhuma change fecha deixando o
site desatualizado**. No mesmo PR, atualize o que aquela change mudou — só isso:

| Se a change                          | Atualize                                                               |
| ------------------------------------ | ---------------------------------------------------------------------- |
| Tomou uma decisão nova               | o documento-fonte (doc 99 §1) e o documento 09                         |
| Mudou um requisito por essa decisão  | o PRD afetado                                                          |
| Fechou uma fatia                     | `openspec/cronograma-de-fatias.md` — a situação e o slug daquela linha |
| Mudou a situação de um PRD           | `docs/prds/index.md` — a coluna da tabela, nunca um parágrafo novo     |
| Mudou a relação entre documentos     | o documento 99                                                         |
| Criou ou renomeou arquivo em `docs/` | a `nav` do `mkdocs.yml`                                                |

Documento técnico novo em `docs/` só entra por decisão do fundador: `docs/` é a documentação
do produto, e o plano de execução vive em `openspec/changes/`.

### 4. Entrega

Um branch e um PR por change, aprovado antes do próximo. No mesmo PR: os artefatos em
`openspec/changes/<change>/`, o código, os testes e a documentação da §3. O merge usa
**merge commit — nunca squash**, e o site só vai ao GitHub Pages **depois do merge em
`main`** — nunca a partir de um PR. `openspec/` fica fora do lint de documentação e fora do
site MkDocs.

## Ritmo de verificação — cada coisa roda uma vez

**Regra geral: uma verificação roda uma vez por estado da árvore.** Se nada mudou desde a
última execução verde, o resultado já é conhecido — repita-o, não reexecute.

| Momento                                                     | O que roda                                                  |
| ----------------------------------------------------------- | ----------------------------------------------------------- |
| `/opsx:apply`, a cada tarefa de código                      | só os testes do recorte: `uv run pytest tests/test_x.py -x` |
| `/opsx:apply`, uma vez ao fechar as tarefas                 | `ruff format .`, `ruff check --fix .` e `pytest` no backend |
| Só se a change tocou `docs/`, `mkdocs.yml` ou `.md` da raiz | `npm run fix`, `npm run lint`, `mkdocs build --strict`      |
| `/opsx:verify` e `/opsx:archive`                            | **nada** — conferem artefato e árvore, não repetem a suíte  |
| CI, no PR                                                   | tudo, com cobertura — é a autoridade final                  |

- **`/opsx:verify` e `/opsx:archive` não re-executam teste, lint nem build.** Se `git status`
  está limpo e o HEAD é o mesmo da última suíte verde, não há o que reexecutar. Só volte a
  rodar o que foi afetado por arquivo modificado depois dela.
- Teste quebrado: itere com `uv run pytest --lf -x`; a suíte inteira roda de novo uma única
  vez, quando o laço fechar.
- A **cobertura é medida no CI**, não no laço local: `pytest` local sai em modo silencioso.
- `npm run fix` corrige o que é corrigível; `npm run lint` confirma. Não rode nenhum dos dois
  quando a change não tocou texto.

### As três esteiras

| Pasta                   | Verificações que bloqueiam o merge      | Comandos locais                                                          |
| ----------------------- | --------------------------------------- | ------------------------------------------------------------------------ |
| `backend/`              | Ruff (formatador e linter) e pytest     | `ruff format --check .`, `ruff check .`, `pytest`                        |
| `apps/*` e `jogos/*`    | Biome (formatador e linter) e Vitest    | `biome format --check .`, `biome check .`, `vitest run`                  |
| `docs/` e `.md` da raiz | markdownlint, Prettier, Lychee e MkDocs | `npm run lint`, `lychee --config lychee.toml .`, `mkdocs build --strict` |

- O backend é Python **3.12**, com Ruff nos conjuntos **`E`, `F`, `I`, `UP` e `B`**. Ruff e
  Biome fazem formatador e _linter_ numa ferramenta só.
- A **cobertura é medida sem limiar que bloqueie** no Ciclo 01, e é medida no CI.
- Cada workflow em `.github/workflows/` dispara só pelo caminho que cobre. **A change que cria
  uma pasta de código entrega, no mesmo PR, a esteira daquela pasta.**
- O deploy do site (`docs-deploy.yml`) acontece **somente após merge em `main`**.

Preparação do ambiente local (uma vez):

```bash
npm install
python -m venv .venv && .venv/Scripts/activate   # Linux/macOS: source .venv/bin/activate
pip install -r requirements-docs.txt
cd backend && uv sync --dev                      # Postgres de teste em CG_DSN_BANCO_TESTE
```

## Economia de contexto e de tempo

O gargalo de uma change não é escrever código: é reler o que já foi lido e reexecutar o que já
passou. Valem para qualquer agente que trabalhe aqui:

- **Leia o PRD alvo uma vez por change**, não uma vez por artefato. Numa sessão que vai da
  `proposal` às `tasks`, o PRD já está no contexto.
- Leitura dirigida, não integral: a §14 do PRD (pendências que travam a fatia), as seções que
  cobrem os `RF`/`RN` do recorte, e o documento 99 §§4, 5, 6 e 8. O PRD inteiro só quando a
  fatia atravessar o documento todo.
- Para saber o que já existe, leia `openspec/specs/<capability>/spec.md` — é o consolidado.
  `openspec/changes/archive/` é histórico: só abra quando precisar do porquê de uma decisão.
- **Não recalcule o que falta de um PRD.** Varrer `openspec/changes/archive/` para descobrir
  quais `RF`/`RN` já foram atendidos é caro e engana: o identificador aparece também nas seções
  de fora do escopo. O cronograma existe para isso — leia o bloco do PRD alvo.
- `openspec/cronograma-de-fatias.md` e `docs/09-topicos-em-aberto-e-sugestoes.md` só crescem —
  leia a parte que a tarefa exige, não o arquivo inteiro por hábito: no cronograma, o bloco do
  PRD alvo; em `docs/09`, a linha da pendência ou decisão pelo nome dela. Use `Read` com
  `offset`/`limit`, ou grep pelo identificador, em vez de carregar o arquivo todo.
- **Não abra subagente** para sincronizar specs, arquivar change ou verificar implementação:
  o agente da sessão já tem o contexto, e um subagente o reconstrói do zero.
- `/opsx:verify` confere o diff da change (`git diff --stat main...HEAD`) contra `tasks.md` e
  as specs do delta — não faz varredura de palavra-chave pelo código inteiro.
- Comando que despeja arquivo grande no contexto (`cat` de PRD, `pytest` verboso, `git diff`
  sem `--stat`) só quando a saída for mesmo usada.

## Checklist antes de entregar

Documentação e PRD:

- [ ] O texto ficou **menor** que antes, sem perder definição, e nenhuma regra foi duplicada?
- [ ] Nenhum link cruzado entre documentos 01–15 foi introduzido?
- [ ] O doc 99 foi atualizado, se alguma relação entre documentos mudou, e as pendências novas
      entraram no doc 09?
- [ ] Os invariantes do doc 99 §6 continuam válidos e a numeração de seções está contínua?
- [ ] Arquivo novo ou renomeado entrou na `nav` do `mkdocs.yml`?
- [ ] Se for PRD: todas as seções do modelo preenchidas, cada decisão nova gravada no
      documento-fonte e movida no documento 09, `docs/prds/index.md` e o doc 99 §8 atualizados?

Change do OpenSpec:

- [ ] A change corresponde a uma fatia do `openspec/cronograma-de-fatias.md`, e a situação
      daquela linha ficou correta ao fechar?
- [ ] Cada requisito e cada tarefa cita o `RF-XX-nn` ou `RN-XX-nn` do PRD que atende?
- [ ] Nenhum artefato criou regra, número, prazo ou provedor que não esteja no PRD, e as
      dúvidas foram levadas ao fundador em vez de resolvidas por suposição?
- [ ] Os invariantes do documento 99 §6 continuam válidos no que foi implementado?
- [ ] O código foi para a pasta que o documento 03 §1.2 define, e pasta nova saiu com a
      esteira de CI dela?
- [ ] A documentação que a change mudou entrou no mesmo PR?
- [ ] O ritmo de verificação foi cumprido — suíte verde uma vez, sem repetição no `verify` nem
      no `archive`?
