PRD-04 (App 01 — Aula presencial). Fatia sem número no `openspec/cronograma-de-fatias.md`
(linha "Aula cancelada não sai das vigentes, e modelos da Human ausentes no build") — correção
de bug preexistente sobre fatias já entregues (1 a 13, todas `implementado`), não requisito
novo. Atende `RF-01-32`; a parte de biometria não tem RF/RN próprio — está coberta pela
pendência "Peso dos modelos da biblioteca Human" do PRD-04 §14, já registrada como "desenho de
implementação, não requisito novo".

## Why

Três defeitos reportados no App 01, com duas causas raiz: (1) `aulas_vigentes` no núcleo não
exclui aula cancelada, então o aparelho abre e opera numa aula que não devia mais estar
disponível; (2) os modelos da biblioteca Human nunca foram provisionados no build de nenhum
app que os usa, então a captura de imagem do onboarding 404 nos `.json` do modelo, e a entrada
por reconhecimento (nick + câmera, usada também para abrir trilha e quiz ao vivo) trava com
`TypeError: Cannot read properties of undefined (reading 'inputNodes')` ao tentar rodar
inferência sobre um modelo que não carregou. O segundo defeito já tinha sido identificado no
`design.md` de `esqueleto-da-area-do-guerreiro-e-fim-de-ciclo` (2026-08-26), marcado para
"levar ao fundador", e ficou sem decisão nem correção por três semanas.

## What Changes

- `aulas_vigentes` (`backend/src/nucleo/aulas/regra.py`) exclui aula com
  `situacao == cancelada` da derivação de vigentes — alcança a rota pública
  `GET /v1/aulas/vigentes`, o aparelho da App 01 (`AparelhoDaAula.tsx`) e o painel do dia da
  App 09, que reusa a mesma função.
- Passo de build copia, de `node_modules/@vladmandic/human/models/`, os cinco modelos
  habilitados em `comum/biometria/biometria.ts` (`blazeface`, `antispoof`, `liveness`,
  `faceres`, `facemesh`) para `public/modelos-de-biometria/` de `app-01-aula-presencial` e de
  `app-05-guerreiro` — os dois apps que importam `comum/biometria`. Nenhuma mudança em
  `comum/biometria/biometria.ts`: `modelBasePath` já aponta para o caminho certo, faltava o
  arquivo existir.
- Nenhuma rota, contrato de API ou tela muda de comportamento visível além de deixar de
  apresentar/aceitar uma aula cancelada como disponível, e de a entrada por reconhecimento
  passar a funcionar (ela já era o comportamento especificado — hoje só falha por 404).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aula-e-presenca`: o Requirement "A disponibilidade do App 01 é derivada da aula vigente no
  momento" para de dizer que a derivação ocorre "sem nenhum parâmetro de liberação separado" —
  passa a excluir explicitamente a aula cancelada, com o scenario correspondente.

A parte de biometria não move nenhuma capability: `aplicacao-da-aula-presencial` já especifica
a entrada por reconhecimento como comportamento vigente (PRD-04, `RF-04-13`, `RF-04-14`); o
defeito é o build não entregar o modelo que essa especificação já pressupõe, não uma mudança de
requisito.

## Impact

- **Backend**: `backend/src/nucleo/aulas/regra.py` (`aulas_vigentes`); teste novo em
  `backend/tests/test_aula.py`; nenhuma migração — `situacao` já existe em `Aula`.
- **Build do frontend**: `apps/app-01-aula-presencial/` e `apps/app-05-guerreiro/` passam a
  gerar `public/modelos-de-biometria/` a partir de `node_modules/@vladmandic/human/models/`.
  Aumenta o peso do artefato de build de cada um (pendência conhecida do PRD-04 §14, não
  resolvida por esta change).
- **Dependência**: nenhuma nova — `@vladmandic/human` já é dependência direta dos dois apps e
  de `comum/`.
- **Sem impacto** em `comum/biometria/biometria.ts`, em `TelaDeCaptura.tsx` nem em
  `TelaDeEntradaDoGuerreiro.tsx` — nenhum dos dois muda de código, só passam a encontrar o
  modelo que já esperavam.
