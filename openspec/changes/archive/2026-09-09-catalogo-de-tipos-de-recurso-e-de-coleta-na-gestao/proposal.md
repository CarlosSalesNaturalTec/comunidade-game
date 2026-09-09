# Catálogo de tipos de recurso e de coleta na gestão

**PRD de origem:** PRD-02 — Frontend de gestão (App 03), fatia **19** do
`openspec/cronograma-de-fatias.md`.
**Requisitos atendidos:** `RF-02-107`, `RF-02-108` — criados por esta change, ver "Decisão de
planejamento" abaixo.

## Why

Os dois catálogos que o Admin mantém — **tipos de recurso** e **tipos de coleta** — não têm
tela em aplicação alguma. O núcleo serve as rotas de cadastro e de leitura dos dois desde as
fatias do PRD-07 e do PRD-08, mas ninguém as chama: não há semeadura nem comando de CLI, e por
isso os catálogos nascem vazios e assim permanecem.

A consequência aparece na App 09, duas fatias adiante: o seletor de **tipo de recurso** da
recompensa pelo desbloqueio (fatia 13 do PRD-09) e o de **tipo de coleta** do desafio de coleta
(fatia 7 do PRD-09) abrem só com "Selecione". As duas fatias estão marcadas implementadas e são,
na prática, inalcançáveis pelo Mestre.

## Decisão de planejamento

O cadastro dos dois catálogos **pela gestão, por Admin** já está decidido e gravado em
`docs/09-topicos-em-aberto-e-sugestoes.md` §1, em "Já decididos": _Cadastro do catálogo de tipos
de coleta_ (documento-fonte 02 §1) e _Economia de recursos e ledger_ (documento-fonte 04 §1). Os
requisitos existem nos PRDs donos — `RF-07-01`, `RF-07-02`, `RF-08-05`.

O que faltava era o requisito do PRD-02 que transforma a decisão em tela — lacuna de redação, não
decisão nova: a §6.1 já é "Cadastros e catálogo", já traz o espelho do `RF-02-10` para os poderes,
e o `RF-02-45` já fala do catálogo "configurável da gestão" sem que nada o torne configurável.
Confirmado com o fundador em 2026-09-09; a fatia 19 foi acrescentada ao cronograma antes desta
proposta.

O enunciado dos dois requisitos novos é **"cadastra e lista"**, não o "mantém" do `RF-02-10`: o
núcleo hoje só oferece criar e listar (ver Impacto).

## What Changes

- A App 03 ganha a área **Catálogos**, ao lado de **Poderes**, reunindo os dois catálogos da
  plataforma. Ela não tem seletor de comunidade: catálogo é bem comum, não dado de comunidade —
  é a razão pela qual Poderes já é área própria (decisão do fundador, 2026-09-09).
- Catálogo de **tipos de recurso** — lista e cadastro, com a primeira vigência do valor de
  referência no mesmo ato, que é como a rota já funciona (`RF-02-107`).
- Catálogo de **tipos de coleta** — lista e cadastro, com unidade e faixa esperada exigidas
  apenas do tipo que se mede por número (`RF-02-108`).
- O PRD-02 ganha os dois requisitos na §6.1, as duas rotas já existentes na §9 e uma pendência
  nova na §14; a mesma pendência entra na tabela do documento 09 §1.

Nenhuma rota nova e nenhuma migração: o molde `Lista + Formulário` já está escrito em
`apps/app-03-gestao/src/poderes/`, que é o precedente em tudo — inclusive em ser área própria.

## Capabilities

### New Capabilities

Nenhuma. As capacidades de núcleo dos dois catálogos — `catalogo-de-tipos-de-recurso` e
`catalogo-de-tipos-de-coleta` — já existem e **não mudam**: a fatia é de tela.

### Modified Capabilities

- `aplicacao-de-gestao`: ganha os requisitos das duas telas de catálogo — o que cada uma
  apresenta, quem alcança o cadastro, o que o formulário exige de cada forma de registro e como a
  recusa do núcleo é apresentada (`RF-02-107`, `RF-02-108`).

## Impact

**Código** — `apps/app-03-gestao/`: pasta nova `src/catalogos/` com a tela da área e as duas
duplas de lista e formulário, mais a entrada da área em `src/App.tsx`. As chamadas de tipo de
recurso ficam onde já estão, em `src/recursos/api.ts`, que a nova pasta importa. Esteira do Biome
e do Vitest já existe para `apps/*`; nenhuma esteira nova.

**Rotas consumidas, todas já entregues** — `POST /v1/tipos-de-recurso`,
`GET /v1/tipos-de-recurso`, `POST /v1/tipos-de-coleta`, `GET /v1/tipos-de-coleta`. Escrita
privativa do Admin nas duas; leitura de tipo de recurso aberta a Admin e Mestre.

**Documentação, no mesmo PR** — PRD-02 §§6.1, 9 e 14; documento 09 §1; a linha 19 do
`openspec/cronograma-de-fatias.md`, que fecha como implementada.

**Limite herdado do núcleo, que a fatia não corrige e registra como pendência:** não há rota para
**editar** tipo de recurso ou de coleta, para **abrir vigência nova** do valor de referência
(`RF-07-02` tem regra e modelo, não rota) nem para **desativar** tipo de coleta
(`desativar_tipo_de_coleta` existe sem rota). `TipoDeRecurso` não tem a coluna `ativo`. A spec
`catalogo-de-tipos-de-coleta` já diz "cadastrar, alterar e desativar", e só a primeira tem porta
de entrada. Tipo cadastrado é, hoje, imutável — e o de recurso desaparece da listagem quando a
vigência fecha, porque a leitura filtra por valor vigente na data.

## Fora do escopo

- **Editar, desativar e abrir vigência nova** nos dois catálogos — sem rota no núcleo; sai como
  pendência do PRD-02 §14 e do documento 09 §1 (decisão do fundador, 2026-09-09).
- **`RF-07-03`** — cadastro de tipo novo no ato do registro do aporte, sem interromper o fluxo.
  É requisito do PRD-07, vive na tela do `RegistroDeAporte` e é criação embutida, não catálogo;
  fatia própria (decisão do fundador, 2026-09-09).
- O que a §3.2 do PRD-02 já exclui, em especial as **regras de valoração de aporte e de cadência
  de coleta**, normatizadas nos documentos 04 e 02 e detalhadas nos PRD-07 e PRD-08: a App 03
  cadastra o vocabulário, não a regra.
