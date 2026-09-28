# Cards, páginas e portfólio dos Guerreiros e Guerreiras

Origem: **PRD-03 — App 06: Vitrine pública**, §§5.1, 5.6, 5.7, 6.1, 6.3, 7, 9 e 12.
**Fatia 2** do PRD-03 no `openspec/cronograma-de-fatias.md`.

Atende `RF-03-02` (parte), `RF-03-03` a `RF-03-06`, `RF-03-08`, `RF-03-09`, `RF-03-11` a
`RF-03-14`, `RF-03-36`, `RF-03-37`, `RN-03-02` a `RN-03-08` e `RN-03-34`.

Dois requisitos saem **em parte**, declarados:

- `RF-03-08` — o portfólio exibe trilha, data e autoria por nick; **título** não existe no
  modelo da criação original, e inventá-lo seria decisão nova (decisão do fundador,
  2026-09-28).
- `RF-03-02` — a fatia entrega as seções **Guerreiros e Guerreiras** e **poderes**; a de
  poderes sai sem os **Mestres responsáveis** do documento 11 §8.2, que chegam com a rota de
  Mestres da fatia 7 (decisão do fundador, 2026-09-28). Comunidades são da fatia 3, Mestres e
  Apoiadores da 7, e batalhas não têm fatia.

## Why

A vitrine tem esqueleto desde a fatia 1 e nenhuma das seções tem conteúdo: a seção de
Guerreiros e Guerreiras, que é a razão de a vitrine existir, ainda diz "chega na próxima
entrega". É por ela que o efeito de **H2** fica visível — só aparece quem teve autorização — e
é ela que dá endereço público à criança que o responsável autorizou.

O núcleo serve hoje quase tudo, mas **não o suficiente para montar a carta**: a listagem
`/vitrine/guerreiros` devolve avatar e nick, e a composição do card que o documento 11 §§8.1 e
8.2 exige — badges, poderes com níveis, desempenho e criações originais — só sairia com uma
consulta por nick para cada card, o que o freio por origem barra em trinta consultas por dez
minutos. Carta pela metade não se apresenta (documento 11 §8.2), e o card rotativo **é** a
carta. Por isso esta fatia leva núcleo, ao contrário do que a linha 2 do cronograma previa.

## What Changes

### A projeção pública do Guerreiro(a) passa a ser a carta inteira (núcleo)

`GET /v1/vitrine/guerreiros` e `GET /v1/vitrine/guerreiros/{nick}` passam a devolver, além de
avatar e nick, o que a variante Guerreiro(a) do documento 11 §8.2 exige: **badges**, **poderes
com níveis**, **desempenho** — posição no ranking público e pontos regulares — e as **criações
originais** creditadas a ele. Mesma projeção nas duas rotas, mesmo portão da divulgação, e nada
de pessoal atravessa (`RN-03-02`, `RN-03-04`). Sem rota nova e sem entidade nova.

`GET /v1/vitrine/criacoes` passa a devolver a **data de validação** e o **nome da trilha** de
cada criação, que o portfólio do `RF-03-08` exige e que a rota não trazia.

### A seção de Guerreiros e Guerreiras ganha cards, páginas e busca (App 06)

- Cards **rotativos a cada 5 segundos** (`RF-03-04`), que respeitam `prefers-reduced-motion` e
  **nunca** são a única via ao conteúdo (documento 15 §§5, 8.1).
- Cada card abre a **página individual**, em endereço próprio (`RF-03-03`), com a composição do
  documento 11 §8.2.
- Card e página exibem **só** avatar, nick, badges, poderes e desempenho (`RF-03-05`), mais as
  criações que o §8.2 pede, e **nenhuma tela** exibe imagem real, nome civil, rede social ou
  contato (`RF-03-06`, `RN-03-04`, `RN-03-05`).
- **Busca por nick exato** (`RF-03-11`), sem sugestão, completação ou lista (`RF-03-12`,
  `RN-03-06`), com a **mesma resposta** para nick inexistente e nick sem autorização
  (`RN-03-07`).
- Quem não tem autorização vigente não aparece em card, página, portfólio ou ranking
  (`RF-03-13`, `RN-03-02`), e a revogação o retira na **leitura seguinte**, inclusive por
  endereço direto (`RF-03-14`, `RN-03-03`).
- A repetição da busca encontra a **espera crescente** do freio, explicada em linguagem simples,
  **sem CAPTCHA e sem cadastro** (`RF-03-36`, `RF-03-37`, `RN-03-08`). A origem continua sem ser
  gravada (`RN-03-34`) — regra do núcleo, já vigente.

### O portfólio e o ranking públicos entram (App 06)

Portfólio das criações originais autorizadas, com **trilha, data e autoria por nick**
(`RF-03-08`), e ranking público **só de pontos regulares** e **só de quem autorizou**
(`RF-03-09`).

### A seção de poderes entra com as trilhas de cada um (App 06)

Cada poder com as trilhas dele e a página do poder (`RF-03-02`, parte). Os Mestres responsáveis
do documento 11 §8.2 ficam para a fatia 7.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `leitura-publica-da-vitrine`: a projeção pública do Guerreiro(a) passa de avatar e nick para
  a carta do documento 11 §8.2, nas duas rotas, e a criação original pública passa a trazer a
  data de validação e o nome da trilha.
- `aplicacao-da-vitrine`: a App 06 ganha a seção de Guerreiros e Guerreiras com cards
  rotativos, as páginas individuais por endereço próprio, a busca por nick exato com a recusa
  indistinta e a espera crescente legível, o portfólio, o ranking e a seção de poderes.

## Impact

- **Backend**: `backend/src/nucleo/vitrine/rotas.py` e `publico.py` — projeção nova nas duas
  rotas de Guerreiro(a) e dois campos em `/vitrine/criacoes`. Nenhuma entidade, nenhuma
  migração, nenhuma rota nova, nenhum lançamento no livro-razão (leitura pública não tem custo
  de operação).
- **Código novo**: as telas da seção de Guerreiros e Guerreiras, da página individual, da busca,
  do portfólio, do ranking e dos poderes em `apps/app-06-vitrine/src/`, sobre a carta de
  `comum/react` e o cliente de `src/api/`.
- **Código lido**: `comum/react/CartaDoPersonagem.tsx` e `comum/carta/`, `comum/api/cliente.ts`
  (o `tempoDeEsperaEmSegundos` do freio já chega ao cliente), `backend/src/nucleo/pontuacao/
  regra.py` (a derivação do ranking) e `backend/src/nucleo/protecao/freio.py`.
- **Documentação**: a linha 2 do cronograma corrigida — a fatia leva núcleo, entrega a seção de
  poderes e sai parcial em `RF-03-02` e `RF-03-08` — e as duas decisões do fundador de
  2026-09-28 no documento 09 §1. `docs/prds/index.md` não muda: o PRD-03 segue `aprovado`
  enquanto houver fatia em aberto.
- **Fora do escopo**, como o PRD-03 §3.2 já exclui: login, cadastro e área restrita; favorito e
  qualquer preferência do visitante; canal de contato com Guerreiro(a) ou família; publicidade e
  patrocínio; dado abaixo do bairro. Fora desta fatia, mas dentro do PRD-03: o painel do
  território e a cobertura da Agenda 2030 (fatia 3), os formulários públicos (fatia 4), o
  institucional e a nota sobre IA (fatia 5), a chamada "Quero participar" de toda página
  individual — `RF-03-39` a `RF-03-41` — e as necessidades em aberto (fatia 6), Mestres e
  Apoiadores, com os Mestres responsáveis da página do poder (fatia 7), e a Área do Apoiador
  Desenvolvedor (fatia 8). Fora por não ter dado: a seção de **batalhas** do `RF-03-02`, que é
  do PRD-10. Fora por lacuna do modelo: o **título** da criação original, que nenhum
  documento-fonte define.
