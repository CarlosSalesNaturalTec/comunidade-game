# Painel do território, séries e cobertura da Agenda 2030

Origem: **PRD-03 — App 06: Vitrine pública**, §§5.2, 5.3, 6.2, 7, 9 e 12. **Fatia 3** do
PRD-03 no `openspec/cronograma-de-fatias.md`.

Atende `RF-03-02` (parte), `RF-03-15` a `RF-03-24`, `RF-03-63` a `RF-03-65`, `RN-03-09`,
`RN-03-10`, `RN-03-19`, `RN-03-20` e `RN-03-28`.

Quatro decisões do fundador de 2026-09-28, tomadas na elicitação desta fatia:

1. O **número de Guerreiros e Guerreiras vinculados** sai na leitura pública da comunidade
   como **atributo de vitalidade do card** (documento 11 §§8.2, 8.3), declaradamente **não**
   como quinto indicador do documento 02 §1 — a trava dos quatro indicadores continua valendo
   para os indicadores.
2. A **metodologia** do `RF-03-17` e do `RF-03-18` é publicada **por recorte publicado** —
   o par tipo de coleta × local —, nunca por série individual: a série é de um coletor, e
   `RN-03-10` a proíbe de sair.
3. A **representação visual** do `RF-03-21` é **genérica**, derivada de dado real, sem forma
   visual por tipo de coleta — o catálogo não tem esse campo, e criá-lo seria decisão nova.
4. `GET /v1/comunidades/{id}/ods`, previsto no PRD-03 §9, **não é criado**: a cobertura sai
   pela rota agregada, que já devolve objetivos e ciclo por comunidade. A linha do PRD-03 §9
   é corrigida nesta change.

`RF-03-02` segue **parcial**, como a fatia 2 o deixou: entra aqui a seção **comunidades**;
Mestres e Apoiadores são da fatia 7, e batalhas não têm fatia.

## Why

Os dois recortes que existem para o dado do território — **pesquisadores** e **gestores
públicos** — chegam hoje a três seções que dizem "chega em entrega própria". O núcleo já
publica a série agregada, a lista de comunidades com os quatro indicadores e a cobertura de
ODS, com o piso de coletores aplicado: o dado está de pé e não tem tela.

Falta também no núcleo o que torna o painel **legível**. A série pública sai com momento,
valor e recorte — e mais nada: quem lê não sabe o que se mede, em que cadência, de que
origem, sobre quantos registros válidos, nem se aquele recorte ainda está vivo. Série sem
metodologia não é evidência, é número solto, e é exatamente o que os `RF-03-17` a `RF-03-19`
exigem que a vitrine declare. O mesmo vale para a carta da Comunidade Virtual: sem o número
de vinculados, ela seria carta pela metade, que a camada comum não apresenta.

## What Changes

### A série pública passa a declarar a metodologia do recorte (núcleo)

`GET /v1/comunidades/{id}/series` passa a devolver, junto de cada ponto, a **metodologia do
recorte** a que ele pertence: **o que mede** — nome e unidade do tipo de coleta —, as
**cadências** das séries que compõem o recorte, o **período coberto** pela primeira e pela
última medição publicada, as **origens** da medição — manual, voz ou sensor — e o **número de
registros válidos** do recorte no período consultado (`RF-03-17`, `RF-03-18`).

O recorte sai marcado **inativo** quando nenhuma série que o compõe está ativa, sem
desaparecer da resposta (`RF-03-19`, documento 11 §8.3). Nada disso identifica coletor: a
metodologia é do recorte, que já passou pelo piso de coletores distintos (`RN-03-10`,
`RN-08-12`).

### A leitura pública da comunidade passa a levar a vitalidade (núcleo)

`GET /v1/comunidades` e `GET /v1/comunidades/{id}` passam a devolver o **número de Guerreiros
e Guerreiras vinculados** à comunidade, contagem agregada que nunca isola ninguém. Ele é o
atributo de **vitalidade** do card do documento 11 §8.2, e sai **ao lado** dos quatro
indicadores do documento 02 §1, nunca como um quinto — a supressão por piso continua
alcançando só os quatro. Sem entidade nova, sem rota nova e sem migração.

### A carta ganha a variante Comunidade Virtual (camada comum)

A camada comum passa a montar a variante **Comunidade Virtual** do documento 11 §8.2 — nome,
território, representação visual, séries ativas e vinculados —, sob a mesma regra das demais:
carta pela metade não se apresenta. Com ela entra a **representação visual** do documento
11 §8.3, genérica e derivada de dado real: contorno com o nome desde a comunidade recém-criada
(`RF-03-20`), presença de cada tipo de coleta ativo e crescimento pelo volume de registros
válidos (`RF-03-21`).

### A App 06 ganha o painel do território, a cobertura e o bloco do gestor

- Seção **Comunidades Virtuais**: cards pela carta nova, cada um abrindo a **página da
  comunidade** em endereço próprio, com as séries históricas do território agregadas até o
  bairro (`RF-03-15`, `RN-03-09`) e sem nick, nome, avatar ou código de coletor em tela
  alguma (`RF-03-16`, `RN-03-10`).
- Cada recorte do painel declara a **metodologia** e os **registros válidos** (`RF-03-17`,
  `RF-03-18`), e o recorte inativo aparece **sinalizado, sem sumir** (`RF-03-19`).
- Seção **Cobertura da Agenda 2030**, por comunidade e por ciclo (`RF-03-22`), com o destaque
  da **meta 17.18** e o **ODS 18** citado como adoção voluntária do Brasil, não como objetivo
  da ONU (`RF-03-23`, `RN-03-20`). Nenhuma etiqueta aparece vinculada a um Guerreiro(a)
  (`RF-03-24`, `RN-03-19`).
- O recorte **gestores públicos** abre com o **bloco em destaque** (`RF-03-63`): para que a
  plataforma serve ao município, com os usos concretos do dado e o caminho para pedir o
  conjunto completo (`RF-03-64`), e com os limites declarados — dado agregado, nunca por
  Guerreiro(a), e que **não substitui indicador oficial** (`RF-03-65`, `RN-03-28`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-publica-do-territorio`: a série pública passa a declarar a metodologia e o estado
  do recorte, e a leitura pública da comunidade passa a levar o número de vinculados, ao lado
  dos quatro indicadores e fora da regra do quinto indicador.
- `camada-visual-comum`: a carta ganha a variante Comunidade Virtual e a representação visual
  do documento 11 §8.3.
- `aplicacao-da-vitrine`: a App 06 ganha a seção de comunidades com card e página, o painel
  do território com metodologia e sinal de inativo, a cobertura da Agenda 2030 e o bloco do
  gestor público.

## Impact

- **Backend**: `backend/src/nucleo/coletas/regra.py` (a projeção da série pública e a
  contagem de vinculados), `backend/src/nucleo/comunidades/regra.py` e `rotas.py`. Nenhuma
  entidade, nenhuma migração e nenhuma rota nova; a exportação do território
  (`exportacao-do-territorio`) não muda de formato.
- **Código novo**: a variante Comunidade Virtual e a representação visual em `comum/`, e as
  telas da seção de comunidades, da página da comunidade, do painel do território, da
  cobertura e do bloco do gestor em `apps/app-06-vitrine/src/`.
- **Código lido**: `comum/react/CartaDoPersonagem.tsx` e `comum/carta/`,
  `apps/app-06-vitrine/src/api/leituras.ts` e `navegacao/recortes.ts`,
  `backend/src/nucleo/ods/regra.py` e `backend/src/nucleo/vitrine/rotas.py`.
- **Documentação**: a linha 3 do cronograma; a correção da linha de
  `GET /v1/comunidades/{id}/ods` no PRD-03 §9; as quatro decisões do fundador de 2026-09-28
  no documento 09 §1. `docs/prds/index.md` não muda — o PRD-03 segue `aprovado` enquanto
  houver fatia em aberto.
- **Fora do escopo**, como o PRD-03 §3.2 já exclui: login, cadastro e área restrita;
  favorito e qualquer preferência do visitante; publicidade, patrocínio e rastreamento; a
  avaliação da solicitação de dados e a entrega do conjunto, que são atos de Admin na App 03;
  e **dado abaixo do bairro**, que só sai na entrega aprovada. Fora desta fatia, mas dentro
  do PRD-03: os formulários públicos, inclusive o de solicitação de dados que as duas telas
  citam em texto (fatia 4), o institucional (fatia 5), as necessidades em aberto (fatia 6),
  Mestres e Apoiadores (fatia 7) e a Área do Apoiador Desenvolvedor (fatia 8). Fora por não
  ter dado: a seção de **batalhas** do `RF-03-02`, que é do PRD-10.
