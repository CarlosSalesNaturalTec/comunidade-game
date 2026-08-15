## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Quinta fatia dele e
vigésima primeira da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-10` (série interrompida após dois períodos de cadência
seguidos sem registro), `RF-08-11` (retomada pelo registro seguinte, sem recompor o período
parado), `RF-08-17` (o Guerreiro(a) consulta suas séries, a situação de cada uma e os pontos
que estão rendendo), `RN-08-07`, `RN-08-08` e o estado `encerrada` pelo fim da vigência do
desafio, que o PRD-08 declara em §3.1 e §8.

A fatia da série e do registro parou de propósito antes do ciclo de vida e nomeou esta por
escrito: a série abre `ativa` e assim permanece, e a transição "tem forma própria e precedente
pronto". O precedente é a change `ciclo-de-vida-da-chave-de-terceiro`, que decidiu que
transição por decurso de prazo **se decide na leitura e é persistida no mesmo ato**, porque o
Ciclo 01 roda sem agendador.

O encaixe já está escrito no código. `EstadoDaSerie` tem um único valor, `ativa`, com a
docstring apontando para esta entrega, e `SerieDeColeta.ultima_medicao_valida_em` existe,
gravado a cada registro válido e sem nenhum leitor — é o insumo declarado da transição.

É também o que fecha a pontuação recorrente. Enquanto a série não interrompe, o crédito do
Poder do Território não tem fim previsto: `RN-08-08` é a única regra que o faz cessar, e sem
ela o documento 11 §5 — "pontua enquanto a série está ativa; interrompeu, parou de render" —
não tem como recair sobre o núcleo.

### Por que a consulta do Guerreiro(a) entra aqui

`RF-08-17` estava encaminhado para a fatia do painel público. Ele vem para cá porque **é o
único lugar onde o estado se torna observável**: a gravação de registro sempre deixa a série
`ativa`, de modo que `interrompida` só aparece em leitura. O critério de aceite do PRD-08 §12
exige exatamente isso — "série sem registro por dois períodos de cadência **aparece** como
`interrompida` e para de creditar; o registro seguinte a devolve para `ativa`". Sem o leitor, a
fatia não é verificável contra o próprio PRD.

Ele traz junto a segunda metade do requisito, "os pontos que estão rendendo", que a fatia
anterior já deixou gravada em `RegistroDeColeta.pontos_creditados`.

## What Changes

- A série passa a **interromper** após **dois períodos de cadência seguidos sem registro
  válido**, e a interrupção **cessa o cômputo**: enquanto interrompida, a série não rende
  (`RF-08-10`, `RN-08-07`, `RN-08-08`).
- Os pontos já creditados **permanecem**. A interrupção NEVER estorna nada — estorno é ato de
  invalidação, de outra fatia (`RN-08-08`).
- A série **retoma** ao receber registro válido, **sem recompor o período parado**: os pontos
  dos períodos vazios não são recuperados (`RF-08-11`).
- O **registro que retoma credita normalmente**. O que se perde é o período parado, não o
  registro que volta — `RN-08-05` condiciona o crédito a registro válido e à quantidade que o
  desafio declara pontuar, e nenhuma outra condição se acrescenta (documento 02 §1).
- A série passa a **encerrar** pelo fim da vigência do desafio. `encerrada` é terminal: não
  retoma (PRD-08 §§3.1, 8).
- O estado passa a ser **derivado** da última medição válida, da cadência e da vigência, com a
  coluna `estado` mantida como espelho — o PRD-08 §8 já manda que ele seja "recalculado, não
  editado à mão".
- Nasce a **consulta das séries do Guerreiro(a)**, com o estado de cada uma e os pontos que
  está rendendo (`RF-08-17`).
- **Correção:** `SerieDeColeta.ultima_medicao_valida_em` deixa de andar para trás. Hoje ele
  recebe a data da medição sem comparação, de modo que registrar uma medição mais antiga depois
  de uma mais recente move o campo para o passado — o que contradiz a sua definição no PRD-08
  §8, "data da **última** medição válida". Nenhum leitor existia até agora; esta fatia o torna
  o insumo do estado.

### Fora do escopo

O que o PRD-08 §3.2 já exclui: importação de fontes públicas de dados; georreferenciamento por
coordenada de GPS; interface das telas de coleta; escolha do banco de séries temporais.

O que é do PRD-08 mas de outra fatia:

| Fica para                          | Porque                                                     |
| ---------------------------------- | ---------------------------------------------------------- |
| `RF-08-13`, `RN-08-09`, `RN-08-20` | auditoria por amostragem, invalidação e estorno            |
| `RN-08-16`                         | foto ou vídeo com pessoa identificável: recai na auditoria |
| `RN-08-19`                         | despersonalização por revogação do consentimento           |
| `RF-08-16`, `RF-08-19`, `RF-08-20` | painel público e exportação agregada                       |
| `RF-08-28`, `RN-08-12`, `RN-08-13` | anonimização e agregação: valem na saída publicada         |
| `RN-08-24`                         | piso de três coletores, que também vale na saída           |
| `RF-08-18`                         | consulta das séries pelo responsável, na App 07            |
| `RF-08-26`, `RF-08-27`             | cobertura de ODS e meta 17.18                              |
| `RF-08-03`                         | transferência de comunidade, fora do Ciclo 01              |

O PRD-08 §14 registra **nenhuma pendência remanescente**, e nenhuma linha aberta do documento
09 §1 alcança este recorte: a cadência, o valor do registro e a regra dos dois períodos já
estão decididos.

## Capabilities

### New Capabilities

Nenhuma. O ciclo de vida é comportamento da série, e a série já tem capability.

### Modified Capabilities

- `serie-de-coleta`: o estado deixa de ser fixo em `ativa` e passa a ter ciclo de vida —
  interrupção por dois períodos sem registro, retomada pelo registro seguinte e encerramento
  pelo fim da vigência —, derivado e persistido como espelho; a data da última medição válida
  passa a nunca retroceder; e o Guerreiro(a) passa a consultar as suas séries com o estado e os
  pontos de cada uma.

## Impact

- `backend/src/nucleo/coletas/modelo.py`: `EstadoDaSerie` ganha `interrompida` e `encerrada`.
- `backend/src/nucleo/coletas/regra.py`: nasce a derivação do estado; a gravação do registro
  passa a atualizar `ultima_medicao_valida_em` sem retroceder; nasce a consulta das séries do
  Guerreiro(a).
- `backend/src/nucleo/coletas/rotas.py`: nasce `GET /v1/series-de-coleta/minhas`.
- `backend/alembic/versions/`: **sem migração** — a coluna `estado` é `VARCHAR(16)` sem
  CHECK constraint, de modo que ampliar o domínio do enum não muda o schema.
- `backend/tests/`: testes do ciclo de vida, da derivação, do espelho e da consulta.
- Sem mudança em `docs/`: as duas decisões de desenho desta change são interpretação do que já
  está escrito em documento 02 §1, `RN-08-05` e PRD-08 §8 — não há regra nova a gravar no
  documento-fonte nem linha a mover no documento 09.
