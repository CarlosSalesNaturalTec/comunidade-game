## Context

Fatia de tela sobre núcleo pronto. As duas capacidades de núcleo —
`openspec/specs/catalogo-de-tipos-de-recurso/` e `openspec/specs/catalogo-de-tipos-de-coleta/` —
já especificam e implementam criar e listar; nada nelas muda. O motivo está em `proposal.md`, e o
comportamento das telas, em `specs/aplicacao-de-gestao/spec.md`.

O padrão de tela de catálogo já está consolidado em `apps/app-03-gestao/src/poderes/`
(`TelaDePoderes` + `ListaDePoderes` + `FormularioDePoder` + `api.ts`), entregue pela fatia 5. Esta
fatia o repete duas vezes. O que segue são apenas as escolhas que ela decide.

## Goals / Non-Goals

**Goals:** desbloquear os dois seletores da App 09 pelo caminho mais curto, reusando o molde de
`poderes/` sem tocar em núcleo.

**Non-Goals:** editar, desativar e abrir vigência nova — sem rota, viram pendência; `RF-07-03`,
fatia própria. Ambos em `proposal.md` — Fora do escopo.

## Decisions

**1. Área própria `Catálogos`, e não dentro de Recursos ou Território.** O catálogo é bem comum
da plataforma; as áreas Recursos e Território operam sob comunidade, e hospedar neles uma lista
não filtrada por comunidade convida o Admin a ler o catálogo como sendo daquela comunidade.
`Poderes` já é área própria por essa razão, com a decisão registrada no comentário de
`TelaDePoderes.tsx`. Decisão do fundador, 2026-09-09.
_Descartado:_ cada catálogo na área que o consome — quebra o precedente de `Poderes` e exige
avisar em texto que a lista ignora o seletor. _Descartado:_ os dois em Recursos — "tipo de coleta"
não se procura em "Recursos".

**2. Pasta nova `src/catalogos/`, e as chamadas de tipo de recurso ficam em `src/recursos/api.ts`.**
`listarTiposDeRecurso` já vive lá e é consumida por `RegistroDeAporte`, `ListaDeNecessidades` e
`AbsorcaoDaNecessidade`; `cadastrarTipoDeRecurso` entra ao lado dela, e `src/catalogos/` importa
as duas. As chamadas de tipo de coleta nascem em `src/catalogos/api.ts`, porque não existem em
lugar nenhum da App 03.
_Descartado:_ mover a API de recurso para `catalogos/` — mexe em três telas que já passam.
_Descartado:_ duplicar `listarTiposDeRecurso` — duas verdades sobre a mesma rota.

**3. As duas listas leem de formas diferentes, porque as rotas são diferentes.**
`GET /v1/tipos-de-recurso` devolve lista simples, já ordenada por nome pelo núcleo.
`GET /v1/tipos-de-coleta` é paginada por cursor: a leitura segue `proximo_cursor` até o fim, como
`src/territorio/api.ts` já faz com os locais. Nenhuma das duas ordena no cliente.

**4. O aviso do valor vigente é texto fixo da lista, não estado calculado.** A rota de tipo de
recurso descarta o tipo sem valor de referência vigente na data — comportamento correto e já
especificado. A aplicação não tem como distinguir "não existe" de "existe com vigência futura",
porque o núcleo não devolve o segundo. Então a lista diz sempre, em uma linha, que traz os tipos
com valor vigente na data.
_Descartado:_ pedir rota que devolva o tipo sem valor vigente — é núcleo, e a fatia é de tela.

**5. O formulário de tipo de coleta é condicional na forma de registro.** Escolhida `número`,
unidade e faixa passam a ser exigidas antes de confirmar; escolhida `foto` ou `vídeo`, somem do
formulário. É a leitura do `CheckConstraint` que o núcleo já impõe, trazida para antes do envio —
a recusa do núcleo continua sendo apresentada quando vier.

**6. Sem custo, sem série temporal.** Nenhuma das operações da fatia lança no livro-razão nem
grava dado de território: são cadastros de vocabulário. As escritas entram na trilha de auditoria
pelo caminho que o núcleo já usa em toda escrita da gestão (`RN-02-21`) — a tela não faz nada
para isso.

## Risks / Trade-offs

**Cadastrar tipo com vigência futura e não o ver na lista** → a decisão 4 põe o aviso na lista; o
campo de início de vigência nasce com a data de hoje, que é o caso corrente.

**Tipo de recurso cadastrado errado não tem conserto pela plataforma** → limite conhecido do
núcleo, registrado como pendência no PRD-02 §14 e no documento 09 §1. Não se resolve nesta fatia.

**Área nova na navegação** → `Catálogos` fica ao lado de `Poderes`, que segue onde está: mover
`Poderes` para dentro dela seria mexer numa tela que já passa, fora do recorte.
