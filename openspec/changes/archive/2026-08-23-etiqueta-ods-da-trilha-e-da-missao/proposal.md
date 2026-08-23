# Etiqueta ODS da trilha e da missão

Origem: **PRD-09 — Área do Mestre**, §6.1. Terceira fatia do PRD-09.

Atende `RF-09-92`, `RF-09-98`, `RF-09-93` e `RF-09-94`, sob `RF-01-16`, `RF-01-40`,
`RF-01-45` e `RN-01-23`.

## Why

A capacidade `etiqueta-ods` está inteira no núcleo desde a change
`apoio-escolar-e-etiqueta-ods` — `criar_etiqueta_ods`, `resolver_etiquetas_da_missao` e as
três coberturas — e **nunca teve porta HTTP**. `backend/src/nucleo/ods/` não tem `rotas.py`.
Nenhum Mestre etiquetou nada até hoje, e não há como etiquetar.

A consequência sai pela vitrine: `GET /vitrine/ods/cobertura` já está no ar, e responde sobre
uma base que ninguém consegue alimentar. A cobertura da Agenda 2030 — o número que o
documento 11 §8 põe diante de edital — é estruturalmente zero enquanto a porta não abrir.

Duas fatias anteriores destravaram a autoria e a publicação da trilha. Esta fecha o §6.1 do
PRD-09: é o que resta da autoria depois que a trilha já publica.

## What Changes

### A substituição do conjunto de etiquetas (`RF-09-92`, `RF-09-98`)

`POST /v1/trilhas/{id}/ods` e `POST /v1/missoes/{id}/ods` recebem a **lista completa** de
etiquetas do alvo e **substituem** o que havia: o que estava é apagado, o que veio é gravado.
A rota é idempotente, e é a forma executável do "declara **ou altera**" do PRD-09 §9 numa rota
só, sem identidade de etiqueta na URL.

A spec vigente já exige que trilha e missão aceitem **mais de uma** etiqueta, e o `RF-09-92`
fala em "os ODS **que ela toca**": o que se substitui é o conjunto, não uma linha. Lista vazia
deixa o alvo sem etiqueta — situação legal no Ciclo 01 por `RF-09-93`.

A substituição é **escopada ao alvo**: o POST na trilha alcança apenas as etiquetas da trilha
e nunca as das missões dela; o POST na missão, o inverso. É o que preserva a precedência do
`RF-01-45`, em que a etiqueta própria da missão prevalece sobre a da trilha.

Apagar não repercute em lugar nenhum: **nenhuma entidade guarda chave estrangeira para
`EtiquetaOds.id`**. O `DesafioDeColeta` resolve a etiqueta por derivação a cada leitura, e a
spec `etiqueta-ods` já traz dois cenários escritos supondo a troca que nunca teve porta —
"Mudar a etiqueta da missão muda a do desafio" e "Trocar a etiqueta não reprocessa pontuação".
Esta fatia liga a porta que os torna exercitáveis de ponta a ponta.

### A autoria estrita (`RF-09-92`) — correção do código à fonte

`criar_etiqueta_ods` chama hoje `conferir_posse_da_trilha`, que **aceita o Admin**. O
documento 11, em "Etiqueta ODS da trilha", diz que **o Mestre autor** declara, e a spec
`etiqueta-ods` diz "Só o Mestre autor da trilha declara a etiqueta". Quem destoa é o código.

Passa a valer `conferir_autoria_estrita_da_trilha` — a mesma conferência que a fatia da
publicação adotou porque o Admin não edita a trilha de um Mestre. Admin recebe **403**.

**Não é decisão nova**: é o código alcançando o que o documento-fonte já manda. Sem linha no
documento 09 e sem alteração de documento-fonte.

### A leitura das etiquetas (`RF-09-92`, `RF-09-98`)

`TrilhaSaida`, `TrilhaComMissoesSaida` e `MissaoSaida` não devolvem etiqueta alguma. Sem isso
o Mestre não vê o que declarou — e substituir exige ver o que está lá — e a trilha pública não
mostra os ODS que toca. As três saídas passam a carregar as etiquetas do respectivo alvo, em
`GET /v1/trilhas/minhas` e no `GET /v1/trilhas/{id}` público.

### A cobertura da trilha (`RF-09-94`)

`GET /v1/trilhas/minhas` e `GET /v1/trilhas/{id}` passam a devolver a **cobertura de ODS
resultante** da trilha — a união dos objetivos dela e das missões dela —, por
`cobertura_por_trilha`, que já existe. Agregação por trilha, nunca por Guerreiro(a)
(`RN-01-24`).

### A App 09 (PRD-09 §4, §6.1)

Tela de ODS dentro da trilha e dentro da missão, com a lista corrente carregada para edição, o
objetivo de 1 a 18 e a meta opcional em texto livre, e a cobertura resultante da trilha.

## Capabilities

### New Capabilities

Nenhuma. A capacidade `etiqueta-ods` já existe e é a desta fatia.

### Modified Capabilities

- `etiqueta-ods`: nasce a **substituição do conjunto** de etiquetas de uma trilha ou de uma
  missão, escopada ao alvo; a declaração passa a exigir **autoria estrita** do Mestre autor,
  recusando o Admin; as etiquetas e a **cobertura da trilha** passam a ser legíveis nas saídas
  de trilha e de missão.
- `area-do-mestre`: a App 09 ganha a declaração e a substituição da etiqueta ODS da trilha e
  da missão, e a leitura da cobertura resultante.

## Impact

| Onde                                          | O quê                                                     |
| --------------------------------------------- | --------------------------------------------------------- |
| `backend/src/nucleo/ods/rotas.py`             | arquivo novo — as duas rotas de substituição              |
| `backend/src/nucleo/ods/regra.py`             | substituir conjunto; autoria estrita em `criar_etiqueta_ods` |
| `backend/src/nucleo/trilhas/rotas.py`         | etiquetas nas três saídas e cobertura da trilha           |
| `backend/src/nucleo/principal.py`             | registro do roteador                                      |
| `apps/app-09-mestre/src/`                     | tela de ODS da trilha e da missão, e a cobertura          |
| `docs/prds/index.md`                          | o parágrafo da terceira fatia do PRD-09                   |

`EtiquetaOds` **não muda** — objetivo de 1 a 18, meta opcional, `CheckConstraint` de trilha ou
missão e `ComAutoria` seguem como estão. Sem migração Alembic.

Destrava a base de `GET /vitrine/ods/cobertura`, hoje no ar sobre tabela que ninguém alimenta.

## Fora do escopo

O PRD-09 §3.2 já exclui o que não é do Ciclo 01. Esta fatia recorta ainda, dentro do que o
PRD inclui:

| O quê                                            | Por quê                                                     |
| ------------------------------------------------ | ----------------------------------------------------------- |
| Trava de publicação sem etiqueta (`RF-09-96`, `RF-09-97`) | o próprio requisito a data do **Ciclo 02**; `RF-09-93` mantém o Ciclo 01 publicando com ou sem, e entra como teste de regressão |
| Etiqueta sugerida pelo template (`RF-09-95`)     | desejável, e é da fatia do template de missão (§6.2), que depende do Gemini |
| Cobertura por poder e por comunidade             | `RF-01-42`; já entregues e legíveis em `GET /vitrine/ods/cobertura` |
| Etiqueta do desafio extra                        | a entidade `DesafioExtra` não existe; herda pela mesma regra quando vier |
