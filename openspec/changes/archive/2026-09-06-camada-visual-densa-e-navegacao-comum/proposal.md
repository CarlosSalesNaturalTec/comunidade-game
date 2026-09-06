## Why

Fatia **transversal, sem PRD** (`openspec/cronograma-de-fatias.md`, bloco *Infraestrutura
transversal*). Entra na capability `camada-visual-comum`, ancorada em **PRD-02 §10** e no
**documento 15 §§4, 5, 6 e 12**. Nenhum `RF`/`RN` novo: a fatia faz o código cumprir o que o
documento 15 já decidiu.

O documento 15 §6 põe a **tabela em primeira classe** no temperamento Operação — Apps 03, 07,
08 e 09 — e a §4 declara os **marcos de largura** `768 · 1024 · 1280` e a grade de colunas.
Nada disso existe no código:

- `comum/react` exporta sete componentes e **nenhum é tabela ou diálogo**; cada aplicação
  reescreve o seu. `.cg-tabela-de-direitos` está **copiada idêntica** em `app-03-gestao`,
  `app-08-apoiador` e `app-09-mestre`.
- `comum/tokens.css` **não declara** os marcos de largura nem a grade de colunas da §4.
- Classes usadas em JSX **sem definição em CSS nenhum**: `.cg-navegacao-de-area` e
  `.cg-navegacao-de-area__alerta` — a navegação **inteira** da App 09 —, além de
  `.lista-de-personas*` e `.cg-campo-de-artefato` na App 03.
- A saída da sessão está montada **em cada tela**: 19 chamadas de `Cabecalho` com a ação
  "Sair" em 16 telas da App 03, e 9 na App 09. O `App.tsx` das duas tem a navegação e **não**
  tem a saída, e o `acao` do `Cabecalho` fica ocupado pelo Sair em vez da ação da própria tela.

## What Changes

- **Decisão do fundador, 2026-09-06 — densidade progressiva na Operação.** O documento 15 §6
  ganha uma linha: o **piso continua sendo o celular em pé** — o caso que dimensiona a
  interface, como PRD-02 §10 já declara —, e **a partir do marco de `768` px da §4** o
  temperamento Operação assume densidade maior: tabela com mais colunas, diálogo e painel lado
  a lado. Nenhum marco novo e nenhuma regressão no celular.
- **`comum/tokens.css` passa a declarar os marcos de largura e a grade de colunas** do
  documento 15 §4, hoje ausentes, mais a largura de área densa que a tabela exige.
- **`comum/react` ganha três componentes**: `Tabela` (cabeçalho, linhas e a rolagem horizontal
  própria em tela estreita), `Dialogo` (sobre o elemento `dialog` nativo, com foco preso,
  fechamento por `Esc` e rótulo acessível) e `NavegacaoDeAreas` (as áreas da aplicação com a
  área corrente marcada por `aria-current` e a **saída da sessão uma única vez**).
- **`Moldura` ganha a largura de área densa.** A largura de leitura de 64 caracteres continua
  o padrão e segue valendo para texto corrido; a tabela pede a outra.
- **Apps 03 e 09 adotam `NavegacaoDeAreas`** e as 28 montagens de "Sair" nas telas saem — a
  saída passa a existir **uma vez**, no menu. O `acao` do `Cabecalho` fica livre para a ação
  da própria tela.
- **As três cópias de `.cg-tabela-de-direitos` são substituídas por `Tabela`**, e a classe
  órfã `.cg-navegacao-de-area` desaparece com a adoção do componente.

**Fora do escopo:** as Apps 01, 04, 05, 07 e 08, que não têm navegação de áreas e têm no
máximo uma saída cada — só a tabela de direitos das Apps 08 e 09 é alcançada, por ser a
duplicata; o temperamento **Arena**, que o documento 15 §6 deixa para quando a primeira
aplicação dele precisar; e a **tela de personas** da App 03, que é a fatia 18 do PRD-02.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `camada-visual-comum`: ganha a densidade progressiva do temperamento Operação, os marcos de
  largura e a grade de colunas do documento 15 §4, o contrato da tabela, o do diálogo e o da
  navegação de áreas com saída única.

## Impact

- `comum/tokens.css` — marcos de largura, grade de colunas e largura de área densa.
- `comum/react/` — `Tabela.tsx`, `Dialogo.tsx` e `NavegacaoDeAreas.tsx` novos; `Moldura.tsx`
  com a largura densa; `estilos.css` e `indice.ts`.
- `apps/app-03-gestao/` — `App.tsx` adota `NavegacaoDeAreas`; 16 telas perdem a ação "Sair";
  `index.css` perde a tabela duplicada e a navegação local.
- `apps/app-09-mestre/` — `App.tsx` adota `NavegacaoDeAreas`; 9 telas perdem a ação "Sair";
  `index.css` perde a tabela duplicada.
- `apps/app-08-apoiador/src/index.css` — perde a tabela duplicada.
- Documentação no mesmo PR: `docs/15-identidade-visual.md` §6 (a densidade progressiva);
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (a decisão do fundador de 2026-09-06);
  `openspec/cronograma-de-fatias.md` (a situação da fatia transversal).
