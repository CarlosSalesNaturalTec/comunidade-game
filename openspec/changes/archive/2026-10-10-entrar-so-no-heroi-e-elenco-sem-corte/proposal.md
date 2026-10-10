# Proposal

**PRD de origem:** PRD-03 — Vitrine pública (App 06).
**Linha no cronograma:** linha `—` do bloco do PRD-03, criada por esta change. Corrige e
completa `2026-10-10-acabamento-da-abertura-da-vitrine`, que ainda não foi integrada.
**Recorte:** `RF-03-58` — **cujo enunciado muda** —, e `RF-03-01` e `RF-03-51`, preservados.

## Why

Duas coisas, vistas pelo fundador na vitrine publicada em 2026-10-10:

1. **O elenco cortava.** A sangria da change anterior usava `100vw` com `overflow-x: clip` no
   herói — e o corte recortava exatamente a sangria que deveria proteger. A quarta figura
   ficava partida na borda do visor. Medido no navegador: as figuras saíam no tamanho natural,
   somando 2254 px num visor de 360 px.
2. **O "Entrar" só faz sentido onde a decisão é tomada.** A change anterior o moveu para o
   herói na abertura e o manteve no cabeçalho das demais telas, o que o deixou em dois lugares
   diferentes conforme a tela. **Decisão do fundador de 2026-10-10:** na vitrine o "Entrar"
   existe **somente no herói** — logo, somente na abertura.

A segunda é **decisão nova de regra**, e não de implementação: o documento 03 §8 diz "Botão
**Entrar**, sempre visível", e é de lá que o `RF-03-58` deriva. Desce pelo fluxo — documento
03 → documento 09 → PRD-03 → change.

## What Changes

- **BREAKING (regra) — o "Entrar" é da abertura.** Deixa de existir no cabeçalho de toda tela
  pública e passa a existir **uma vez**, no herói, ao lado do "Quero participar". Quem está em
  outro recorte alcança a entrada pela marca, que leva à abertura.
- **O cabeçalho da vitrine deixa de ter estado.** Sem o botão, não há diálogo a abrir: ele sai
  de ilha e passa a sair no documento servido, sem custar JS em nenhuma tela.
- **Correção do corte do elenco.** A altura das figuras passa a ser tirada da **largura do
  herói**, por consulta de contêiner, e não da largura do visor: a regra se corrige sozinha em
  qualquer tela e não depende de saber quanto respiro a moldura tem. Saem o `100vw`, a margem
  negativa e o `overflow-x: clip`.

**O que não muda:** o par de ações, as cores das duas, a saudação, o rótulo "Início", a
navegação em uma linha e o tamanho da frase — tudo entregue pela change anterior e mantido.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: o requisito do "Entrar" é **substituído** — deixa de exigir o botão
  em toda tela pública e passa a situá-lo na abertura, no herói —, e o requisito do herói
  perde a frase que ainda admitia o botão no cabeçalho das demais telas.

A correção do corte **não vira requisito**: a spec já exige que a ilustração apareça em
primeiro plano e que a composição preserve a ordem das quatro figuras. "Não cortar" é defeito
contra o que já está escrito, e fica guardado por teste.

## Impact

**Documentação — a decisão desce pelo fluxo, nesta ordem:**

| Nível | Arquivo | O que muda |
| --- | --- | --- |
| 1 | `docs/03-plataforma-e-arquitetura.md` §8 | "sempre visível" passa a "na abertura, no herói" |
| 1 | `docs/08-base-para-prds.md` | as duas menções passam a resumir a regra nova em uma frase |
| 1 | `docs/09-topicos-em-aberto-e-sugestoes.md` §1 | linha nova em "Já decididos" |
| 2 | `docs/prds/prd-03-vitrine-publica.md` | `RF-03-58` e a jornada §5.9 |

O documento 99 **não muda**: nenhuma relação entre documentos se altera — o `RF-03-58`
continua derivando do documento 03 §8. `mkdocs.yml` não muda: nenhum arquivo nasce.

**Código — `apps/app-06-vitrine/` apenas:**

| Arquivo | O que muda |
| --- | --- |
| `src/componentes/CabecalhoDaVitrine.tsx` | perde o botão, o estado e o diálogo |
| `src/layouts/Vitrine.astro` | o cabeçalho deixa de ser ilha; cai a propriedade `comHeroi` |
| `src/index.css` | a altura do elenco passa a vir da largura do herói |

**Testes:** os que acionam o "Entrar" fora da abertura passam a alcançá-lo na abertura;
`saidaDoBuild.test.ts` troca o guarda "as demais telas seguem com o Entrar do cabeçalho" por
"nenhuma tela além da abertura traz Entrar", e ganha o guarda do elenco inteiro.

**Ritmo de verificação:** a change toca `docs/`, então **rodam também** `npm run lint` e
`mkdocs build --strict`, além de Biome e Vitest da App 06.
