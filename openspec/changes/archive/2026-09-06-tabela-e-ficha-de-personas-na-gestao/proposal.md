## Why

Fatia **18 do PRD-02** (`openspec/cronograma-de-fatias.md`), a área Personas da App 03. Atende
`RF-02-01`, `RF-02-02`, `RF-02-03`, `RF-02-04`, `RN-02-01` e `RN-14-10`. **Nenhum requisito
novo e nenhuma rota nova** — decisão do fundador de 2026-09-06.

O artefato comprobatório é o que sustenta o cadastro de Mestre e de Apoiador: `RF-02-04` recusa
o cadastro sem ao menos um, e `RN-02-01` o define como link declarado. O núcleo o serve —
`GET /v1/mestres` e `GET /v1/apoiadores` devolvem `artefatos` em cada item —, o cliente o tipa
em `AdultoDaLista`, e **a tela o descarta**: `ListaDeAdultos` desenha nome, e-mail e nick, e
nada mais. O Admin não tem por onde conferir a prova que ele mesmo exigiu no cadastro.

Junto disso, a área inteira está sem forma: `.lista-de-personas`, `.lista-de-personas__item`,
`.lista-de-personas__nome`, `.lista-de-personas__detalhe`, `.lista-de-personas__nick` e
`.cg-campo-de-artefato` são usadas em JSX e **não existem em CSS nenhum**. A lista sai como
itens de texto colados, e o caminho de gravar o nick de quem está sem ele — que `RF-02-01` e
`RN-14-10` exigem e que já está implementado — some no meio delas.

## What Changes

- **As listas de Mestres, de Apoiadores e de Guerreiros e Guerreiras passam a tabela**, pelo
  componente `Tabela` da camada comum, com as colunas que cada papel já traz do núcleo.
- **Cada linha de adulto abre uma ficha de leitura** — o `Dialogo` da camada comum — com nome,
  e-mail, WhatsApp, nick e os **artefatos comprobatórios**, cada um com rótulo e endereço, o
  endereço alcançável como link (`RF-02-02`, `RF-02-03`, `RF-02-04`, `RN-02-01`).
- **A sinalização de quem está sem nick sai da linha para a coluna própria**, e o caminho de
  gravá-lo — que já existe e não muda de regra — passa a ser oferecido pela ficha
  (`RF-02-01`, `RN-14-10`).
- **As classes órfãs deixam de existir**: `.lista-de-personas*` some com a tabela, e
  `.cg-campo-de-artefato` ganha a forma que o formulário de artefatos sempre presumiu.

**Fora do escopo**, e cada um por um motivo declarado:

- **Editar o cadastro de adulto** — nome, e-mail, WhatsApp ou artefatos de Mestre e Apoiador.
  `RF-02-01` dá ao Admin "cadastra **e edita**" apenas para Guerreiro(a); `RF-02-02` e
  `RF-02-03` dizem só "cadastra", e não existe rota de edição de adulto no núcleo. Fica para o
  Ciclo 02 por decisão do fundador de 2026-09-06.
- **Trocar nick já gravado pela gestão.** O caminho existente grava o nick de quem está sem
  ele; a troca é do próprio adulto, e o documento 02 §1 já a atribui a ele.
- **Digitar o nick no formulário de cadastro.** O documento 02 §1 diz que o Mestre define o
  nick no primeiro acesso e que o do Apoiador vem do pré-cadastro; o campo condicionado ao
  pré-cadastro em `FormularioDeAdulto` **é desenho, não defeito**, e permanece como está
  (decisão do fundador, 2026-09-06).
- **A vitrine institucional e o Apoiador na gestão**, que são a fatia 16, ainda em aberto.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-de-gestao`: a área Personas passa a apresentar Mestres, Apoiadores e Guerreiros e
  Guerreiras em tabela, e a abrir a ficha de leitura de um adulto com os artefatos
  comprobatórios que sustentaram o cadastro dele.

## Impact

- `apps/app-03-gestao/src/personas/` — `ListaDeAdultos.tsx` e `ListaDeGuerreiros.tsx` passam a
  `Tabela`; nasce `FichaDoAdulto.tsx` sobre o `Dialogo`; `TelaDeAdultos.tsx` liga a linha à
  ficha; `personas.test.tsx` cobre o novo.
- `apps/app-03-gestao/src/index.css` — a forma do campo de artefato; as classes órfãs de lista
  saem.
- Depende da fatia transversal `camada-visual-densa-e-navegacao-comum`, que entrega `Tabela` e
  `Dialogo`.
- Documentação no mesmo PR: `openspec/cronograma-de-fatias.md` (a situação da fatia 18) e
  `docs/09-topicos-em-aberto-e-sugestoes.md` §1 (a decisão do fundador de 2026-09-06 sobre o
  que fica fora). Nenhum documento-fonte muda: a fatia não cria regra.
