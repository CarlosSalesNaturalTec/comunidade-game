## Why

**PRD de origem:** PRD-01 — Backend API (núcleo). Quinta fatia, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-01-20` (a parte de trilha, missão e atividade).

As quatro fatias anteriores fecharam a identidade: os cinco papéis do PRD-01 §4 têm caminho de
entrada, e o que resta do núcleo é domínio. Este é o primeiro pedaço dele, e é o pedaço de que
todos os outros dependem. Ponto nasce de realização, realização é de uma atividade, atividade
pertence a uma missão e missão pertence a uma trilha: sem essa cadeia não há o que pontuar, o
que desbloquear nem o que autorar.

Quem conduz a autoria é o PRD-09, liberado só depois do PRD-01. É esta fatia que lhe entrega o
objeto — `RF-09-01` cria trilha "vinculada a um poder do catálogo", e o catálogo, a trilha e a
missão precisam existir no núcleo antes de existir a tela que os escreve.

Ela é pequena de propósito e para onde a dependência começa: entrega a **estrutura**, não a
pontuação.

## What Changes

- Nasce o **Poder**, catálogo a que toda trilha se vincula, com os poderes do documento 02 §2 e
  a marcação de quais valem no Ciclo 01 (`RF-01-20`).
- Nasce a **Trilha**, de autoria de um Mestre e vinculada a um poder, com situação de rascunho
  ou publicada — a transição entre as duas é do PRD-09 (`RF-01-20`).
- Nasce a **Missão**, ordenada dentro da trilha, declarada **obrigatória ou opcional** e com o
  **nível de dificuldade** próprio; a de **sondagem** é a que abre a trilha (`RF-01-20`).
- Nasce a **Atividade**, sempre pertencente a uma missão, classificada nos **três eixos** do
  documento 11 §4 — modalidade, formato e natureza —, que se combinam livremente (`RF-01-20`).
- A **trilha é do Mestre autor**: o papel Mestre escreve as suas e não as de outro Mestre, como
  o PRD-01 §4 declara. A matriz de `RF-01-16`, que já é conferida em toda operação, passa a ter
  objeto de domínio; a autoria gravada por `RF-01-03` passa a ter o que creditar.
- A dificuldade é atributo declarado da missão e **nunca deriva da idade** (invariante 2), e só
  a missão **obrigatória** entra no denominador do percurso (invariante 18) — a conta dos níveis
  é de outra fatia, mas o dado de que ela depende nasce aqui.
- Toda atividade **exige produção** do Guerreiro(a) (invariante 19): a natureza declarada é o
  que registra o que se produz.

### O que esta fatia não tem, e não é omissão

**Nenhuma rota de autoria.** Criar, ordenar, paginar e publicar trilha são `RF-09-01` a
`RF-09-13`, `RF-09-69` a `RF-09-72` e `RF-09-80` a `RF-09-84` — do PRD-09, e o PRD-01 §9 não
declara nenhuma delas. Aqui nascem a **entidade e as invariantes**, como a terceira fatia
entregou `Consentimento` sem criar rota que o escrevesse.

**As três travas de publicação** (invariante 5) não são conferidas aqui. A sondagem já é
atributo da missão, mas o desafio de coleta é PRD-08 e a culminância é PRD-09; a conferência
das três é `RF-09-06`, `RF-09-07` e `RF-09-82`, na aplicação que publica.

**O lastro** (`RN-01-07`, invariante 9) precisa dos recursos do PRD-07, que é a entrega nº 3.
A atividade nasce sem a trava, e a trava chega com o livro-razão.

**`DesafioDeDesbloqueio` fica de fora.** Ele não está em `RF-01-20`, e a sua forma de quiz
depende das entidades de `RF-01-36`, da fatia da aula.

**`Conteudo`, `BibliografiaDaMissao`, `Culminancia`, `RecompensaDeMarco` e
`SugestaoDeEstrutura`** têm os atributos definidos no PRD-09, como o PRD-01 §8 declara.

### Fora do escopo

O que o PRD-01 §3.2 já exclui: interface de qualquer aplicação; regras de pontuação, cadência
de coleta e valoração de aporte; captura da imagem, conversa de cadastro e geração do descritor
no aparelho; exclusão do _template_; telemetria da Batalha de Laser e personalização por IA.

O que é do PRD-01 mas de outra fatia, por dependência declarada ou por pendência aberta:

| Fica para                                        | Porque                                                             |
| ------------------------------------------------ | ------------------------------------------------------------------ |
| `RF-01-20`, nas partes de equipe e presença      | as duas pendem de `Aula/Agenda`, da fatia da operação da aula      |
| `RF-01-20`, na parte de resultado                | o resultado é a realização que credita ponto, da fatia seguinte    |
| `RF-01-21`                                       | nível 3 exige série de coleta (PRD-08) e nível 5, culminância      |
| `RF-01-22`, `RF-01-56` a `RF-01-60`              | as duas contas de ponto e a troca, que depende do PRD-07           |
| `RF-01-32`, `RF-01-36` a `RF-01-39`              | aula agendada, equipe e Quiz ao Vivo                               |
| `RF-01-40` a `RF-01-45`                          | a etiqueta ODS propaga para coleta (PRD-08) e desafio extra        |
| `RF-01-43`                                       | documento 09, "Números da proteção das rotas públicas"             |
| `RF-01-49` a `RF-01-53`, `RF-01-55`              | documento 09, "Números da proteção das rotas públicas"             |
| `RF-01-23` a `RF-01-26`, `RF-01-29`, `RF-01-46`, `RF-01-47` | território, ledger, fila de avaliação e auditoria       |

A **pontuação negativa** do documento 11 §5 fica fora de qualquer fatia por ora: o **prazo de
guarda do registro de infração** é pendência declarada no PRD-01 §14 e precisa ser decidida no
documento-fonte antes de virar código.

### Perguntas ao fundador, antes de escrever as specs

Duas lacunas que nenhum artefato do OpenSpec pode preencher por suposição:

1. **A trilha é dado de comunidade?** `RF-01-18` manda filtrar por comunidade "toda consulta de
   dado de comunidade", e a plataforma é instância única. Nem o PRD-01 nem o PRD-09 dizem se a
   trilha se vincula a uma Comunidade Virtual ou se é bem comum da plataforma, visível a todas
   — o que a licença CC BY-SA do conteúdo publicado sugere, sem declarar.
2. **Quem cria o catálogo de poderes?** `RF-09-01` fala em "poder do catálogo", e o documento 02
   §2 lista os poderes, mas nenhum requisito diz se ele é semeado na implantação, como as chaves
   de `RF-01-54`, ou cadastrado por Admin. O documento 02 §2 ainda marca dois poderes como
   `[Proposta]`, e o **Poder Sustentador** é do Apoiador e não recebe trilha — o catálogo mistura
   duas naturezas.

## Capabilities

### New Capabilities

- `catalogo-de-poderes`: o poder como catálogo a que a trilha se vincula, com a marcação do que
  vale no Ciclo 01 e a distinção entre poder de trilha e poder derivado do apoio.
- `trilha-e-missao`: a trilha do Mestre autor, as missões ordenadas dentro dela, a declaração de
  obrigatória ou opcional, o nível de dificuldade e a missão de sondagem que a abre.
- `atividade-de-trilha`: a atividade sempre vinculada a uma missão e classificada nos três eixos
  do documento 11 §4, com a exigência de produção do Guerreiro(a).

### Modified Capabilities

Nenhuma. `permissoes-e-escopo-de-comunidade` já confere a matriz "em toda operação" e não muda
de requisito por ganhar entidades novas; a posse da trilha pelo Mestre autor é requisito da
própria `trilha-e-missao`.

## Impact

- `backend/src/nucleo/`: módulo novo para o domínio da trilha — poder, trilha, missão e
  atividade —, com os três eixos da taxonomia como enumerações do documento 11 §4.
- `backend/alembic/`: migração para as quatro entidades e para a ordenação das missões dentro
  da trilha.
- `backend/src/nucleo/permissoes.py`: a posse da trilha pelo Mestre autor entra como conferência
  de autoria, ao lado da conferência de papel que já existe.
- Nenhuma rota nova sob `/v1`: as rotas de autoria são do PRD-09.
- `docs/`: nada a alterar enquanto as duas perguntas acima não forem respondidas. Se alguma
  virar decisão, ela é gravada no documento-fonte e movida no documento 09 **antes** das specs,
  e `docs/prds/index.md` recebe a situação ao fim da implementação.
