## Why

**PRD de origem:** PRD-08 — Comunidades Virtuais e dados do território. Última fatia dele e
vigésima sexta da esteira, na ordem do documento 99 §9.

**Requisitos atendidos:** `RF-08-30` (rota pública lista as comunidades com os quatro
indicadores do documento 02 §1), `RF-08-31` e `RN-08-28` (comunidade abaixo do piso sai na
lista sem os indicadores), `RN-08-29` (cálculo dos quatro indicadores, com o de séries ativas
apurado no instante da consulta), `RN-08-12` (anonimização na saída, nunca no armazenamento) e,
do PRD-01, `RF-01-28` (listagem paginada), `RF-01-18` (filtro por comunidade), `RF-01-02` e
`RN-01-32` (rota pública sem credencial de persona, nunca sem chave de aplicação).

`GET /comunidades` é a **única rota que o PRD-08 §9 declara e que nunca foi construída**. A
fatia `leitura-publica-do-territorio` a deixou explicitamente de fora, e disse por quê: o PRD
nomeava a rota mas não declarava **quais** indicadores ela devolve, e artefato do OpenSpec não
inventa lista. A pergunta foi ao fundador e voltou decidida.

Hoje o visitante só chega ao território **se já souber o identificador de uma comunidade** —
`GET /comunidades/{id}` existe, a lista não. É a porta de entrada da vitrine que falta: sem
ela, o dado público do território é consultável apenas por quem já está dentro.

### O que foi decidido antes desta change

Três decisões percorreram o fluxo — documento-fonte, documento 09 e PRD — antes de a change
existir:

1. **Comunidade abaixo do piso sai na lista, sem os indicadores.** A comunidade é o topo da
   hierarquia e não há nível acima a que somá-la, então a regra de subir o recorte não tem para
   onde apontar. Some o número, nunca a comunidade.
2. **Continuidade** é a média, entre as séries da comunidade, da fração dos períodos de
   cadência esperados com ao menos um registro válido.
3. **Séries ativas ao fim do ciclo** se apura **no instante da consulta** enquanto o ciclo
   corre — a mesma régua que o documento 02 §1 já fixou para a auditoria por amostragem. O
   ciclo é rótulo declarado na implantação e não tem calendário.

A segunda e a terceira não estavam na pauta: os quatro indicadores estavam apenas **nomeados**
no documento 02 §1, e a referência era **circular** — o documento 09 mandava ao PRD-08 §12, que
mandava de volta ao 02 §1. A lacuna apareceu ao preparar esta fatia e foi fechada na fonte.

## What Changes

- Nasce a **lista pública de comunidades**: rota de consulta paginada, **sem credencial de
  persona** e com **chave de aplicação obrigatória**, na mesma régua das demais rotas públicas
  do território (`RF-08-30`, `RF-01-02`, `RN-01-32`).
- Cada comunidade sai com **nome, localização e os quatro indicadores** do documento 02 §1:
  séries abertas, séries ativas ao fim do ciclo, registros válidos e continuidade
  (`RF-08-30`, `RN-08-29`).
- **Continuidade** é apurada como a média, entre as séries da comunidade, da fração dos
  períodos de cadência esperados que tiveram ao menos um registro válido (`RN-08-29`).
- **Séries ativas ao fim do ciclo** conta as séries em estado `ativa` **no instante da
  consulta**, e a resposta declara o **rótulo do ciclo corrente** que a configuração já guarda
  (`RN-08-29`).
- O **piso de coletores distintos** passa a valer sobre a lista: comunidade abaixo do piso
  **permanece na resposta**, com nome e localização, e os **quatro indicadores saem nulos**
  (`RF-08-31`, `RN-08-28`). É o oposto do que a série pública faz com o recorte abaixo do piso,
  que é suprimi-lo — e a diferença tem razão: lá há nível acima a que somar, aqui não há.
- A resposta **não leva coletor**: nem identificador, nem nick, nem contagem que isole um. Os
  indicadores são contagens agregadas da comunidade inteira (`RN-08-12`).
- A consulta é **paginada** no contrato de listagem do núcleo — `cursor`, `tamanho` — e devolve
  **422** para parâmetro não declarado (`RF-01-28`).
- Apenas registro de situação **válida** entra na contagem de registros válidos e na apuração
  da continuidade. Registro invalidado na auditoria do Mestre sai das duas.

### Fora do escopo

O que o PRD-08 §3.2 já exclui segue excluído — importação de fontes públicas, GPS por
coordenada, interface das telas e escolha do banco de séries. Além disso, e por recorte desta
fatia:

| Fica para                    | Porque                                                              |
| ---------------------------- | ------------------------------------------------------------------- |
| `RF-08-20`                   | crescimento visual do painel: é frontend, documento 11 §8.3         |
| `RF-08-18`                   | consulta do responsável pela App 07: é PRD-13                       |
| `RN-08-19`                   | despersonalização por revogação do consentimento                    |
| `RF-08-03`                   | transferência entre comunidades: fora do Ciclo 01 por decisão       |
| ordenação por indicador      | o PRD não declara ordem; a lista sai estável por nome               |
| filtro por faixa de indicador | nenhum `RF` o declara, e o volume do Ciclo 01 não o justifica       |

**A cobertura de ODS da comunidade não entra**: ela já sai em `GET /v1/vitrine/ods/cobertura`,
construída na fatia `exportacao-do-territorio-e-ods-das-series`, e `RF-08-26` fala do painel,
que é frontend.

**Nenhum indicador novo entra.** São quatro, e são os do documento 02 §1 — a change não
acrescenta um quinto por conveniência.

## Capabilities

### New Capabilities

Nenhuma. A rota é a superfície de leitura pública do território que a capacidade
`leitura-publica-do-territorio` já define, estendida com a lista que faltava.

### Modified Capabilities

- `leitura-publica-do-territorio`: ganha a **lista de comunidades com os quatro indicadores** e
  a regra de que a comunidade abaixo do piso **permanece na lista sem os indicadores** — o
  tratamento oposto ao que a mesma capacidade já dá ao recorte da série abaixo do piso, que é
  suprimi-lo. A capacidade passa a declarar as duas regras lado a lado, para que a diferença
  fique escrita e não pareça contradição.

## Impact

- `backend/src/nucleo/comunidades/regra.py`: a apuração dos quatro indicadores por comunidade e
  a aplicação do piso sobre eles.
- `backend/src/nucleo/comunidades/rotas.py`: a rota `GET /comunidades`, paginada e sem
  dependência de persona.
- `backend/src/nucleo/coletas/regra.py`: a consulta dos períodos de cadência esperados por
  série, que a continuidade exige e que ainda não existe.
- `backend/tests/`: comunidade com três coletores que sai com os quatro indicadores;
  comunidade com dois que sai sem eles; comunidade vazia; continuidade de série sem nenhum
  período vencido; continuidade de série com período vencido e sem registro; registro
  invalidado fora das duas contagens; ausência de coletor em toda a resposta; consulta sem
  chave recusada com 401; consulta sem sessão aceita; parâmetro não declarado recusado com 422.
