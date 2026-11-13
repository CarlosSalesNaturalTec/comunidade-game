# Edição e exclusão dos catálogos de tipo

**PRD de origem:** PRD-02 — Frontend de gestão (App 03), fatia **27** do
`openspec/cronograma-de-fatias.md`; alcança o PRD-07 (tipo de recurso) e o PRD-08 (tipo de
coleta), donos das regras de núcleo dos dois catálogos.
**Requisitos atendidos:** `RF-02-113`, `RF-02-114`, `RF-02-115`, `RF-07-51`, `RF-07-52`,
`RN-07-40`, `RF-08-32`, `RN-08-30` — **novos**, a criar na revisão dos PRDs 02, 07 e 08 no mesmo
PR; alteram `RF-07-01` ("cadastra e mantém") e aplicam `RF-07-02` e `RF-07-43`.

## Why

Tipo cadastrado nos dois catálogos é, hoje, **imutável**: o núcleo serve criar e listar, e não há
rota para corrigir um nome errado, trocar a unidade, abrir vigência nova do valor em moedas
(`RF-07-02` tem regra e modelo, não rota), desativar tipo de coleta (regra sem rota) nem apagar
um cadastro feito por engano. É a pendência "Os catálogos de tipo não têm edição nem
desativação" do documento 09 §1, levantada pela fatia 19 do PRD-02.

## Decisão de planejamento

Decisão do fundador de **2026-11-13**, tomada ao pedir esta change; a fatia 27 foi acrescentada
ao cronograma antes desta proposta. Cinco partes:

1. **Excluir** remove o tipo **só se nunca usado** — nenhuma linha de nenhuma tabela aponta para
   ele. Tipo já usado é recusado, e o caminho dele é a **desativação**.
2. **Tipo de recurso** — alteram-se **nome, unidade e exige comprovante**. A **natureza fica
   fixa**, porque decide se há valor de origem em reais a declarar. Valor em moedas e preço em
   pontos extras mudam **abrindo vigência nova**, como `RF-07-02` e `RF-07-43` já mandam.
3. **Tipo de coleta** — alteram-se **todos os campos**, inclusive a forma de registro, sob as
   mesmas validações do cadastro.
4. **Tipo de recurso ganha a marca de ativo.** Desativado bloqueia **só escolha nova**: some dos
   seletores e é recusado em escolha nova; o que já existe — saldo, reserva, recompensa
   declarada, item avulso, lançamento — segue inalterado. É a regra que o tipo de coleta já tem.
5. **Reativação** pelo Admin, nos dois catálogos, no precedente do ponto de apoio.

A decisão entra no documento-fonte de cada catálogo — documento 04 §1 (tipo de recurso) e
documento 02 §1 (tipo de coleta) — e a linha do documento 09 §1 passa de "Decisões pendentes" a
"Já decididos", no mesmo PR.

## What Changes

- **Núcleo, tipo de recurso** — rotas novas, restritas ao Admin: alterar (nome, unidade, exige
  comprovante), abrir vigência nova do valor em moedas, desativar, reativar e excluir. A leitura
  `GET /v1/tipos-de-recurso` passa a trazer a marca **ativo**. O preço em pontos extras já tem
  rota de registro e de histórico (`RF-07-43`), que a edição reaproveita.
- **Núcleo, tipo de coleta** — rotas novas, restritas ao Admin: alterar todos os campos,
  desativar, reativar e excluir. A regra de alteração (só nome) e a de desativação já existem em
  `coletas/regra.py`, sem rota.
- **Núcleo, escolha nova** — os atos que **escolhem** um tipo de recurso passam a recusar o
  desativado: agendar aula com recurso declarado, registrar aporte, homologar declaração,
  absorção avulsa, declarar recompensa de marco, item do catálogo avulso e desafio extra. O que
  segue fato já existente — absorção de necessidade publicada, missão do Apoiador sobre
  necessidade publicada, transferência de saldo — não é escolha nova e segue aceito.
- **App 03, área Catálogos** — cada tipo ganha **Editar**, **Desativar**/**Reativar** e
  **Excluir** para o Admin; a edição do tipo de recurso traz, além dos campos, a vigência nova do
  valor e do preço. A lista de tipos de recurso passa a mostrar a marca de ativo, como a de coleta
  já mostra. Exclusão pede confirmação; a recusa por uso aparece em linguagem simples, apontando a
  desativação.
- **Seletores de escolha nova** nas Apps 03 e 09 deixam de oferecer tipo de recurso desativado; a
  leitura por nome (extrato, acervo, fila de entregas) segue com todos.
- **Leva migração Alembic**: a coluna `ativo` em `tipo_de_recurso`, nascendo verdadeira.

### Fora do escopo

- `RF-07-03`, o cadastro do tipo no ato do aporte — fatia própria, como já registrado na 19.
- Alterar a **natureza** do tipo de recurso (decisão 2).
- Corrigir ou apagar **vigência** já registrada — vigência só se abre, nunca se reescreve
  (`RF-07-02`).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `catalogo-de-tipos-de-recurso`: alteração dos três campos, vigência nova do valor por rota,
  marca de ativo com desativação e reativação, exclusão só do tipo nunca usado, e leitura com a
  marca de ativo (`RF-07-51`, `RF-07-52`, `RN-07-40`).
- `catalogo-de-tipos-de-coleta`: alteração de todos os campos, desativação e reativação por rota,
  exclusão só do tipo nunca usado (`RF-08-32`, `RN-08-30`).
- `aplicacao-de-gestao`: a área Catálogos ganha editar, desativar, reativar e excluir nos dois
  catálogos, a lista de recurso mostra a marca de ativo, e os seletores de escolha nova da App 03
  deixam de oferecer o tipo desativado (`RF-02-113` a `RF-02-115`).
- `area-do-mestre`: o seletor de tipo de recurso da recompensa de marco, na App 09, deixa de
  oferecer o tipo desativado (`RF-07-52`).

## Impact

- **Backend** — `backend/src/nucleo/recursos/` (modelo, regra, rotas), `coletas/` (regra,
  rotas), e a guarda de tipo ativo nas rotas de escolha nova: `aulas`, `aportes`,
  `recompensas_de_marco`, `catalogo_avulso`, `desafios_extras`. Uma
  migração Alembic. Rotas novas: `PATCH`, `DELETE`, `POST …/desativacao`, `POST …/reativacao`
  em `/v1/tipos-de-recurso/{id}` e `/v1/tipos-de-coleta/{id}`, e
  `POST /v1/tipos-de-recurso/{id}/valores-de-referencia`.
- **App 03** — `src/catalogos/` (listas, formulários de edição, confirmação de exclusão) e o
  filtro de ativos nos seletores de `agenda/`, `recursos/` (registro de aporte) e `filas/`
  (homologação do aporte).
- **App 09** — o filtro de ativos no seletor da recompensa de marco, em `autoria/`; a absorção usa o
  tipo da necessidade e não tem seletor.
- **Documentação, no mesmo PR** — PRDs 02, 07 e 08 (requisitos novos e alterados, rotas na §9,
  pendência removida da §14), documentos 04 §1 e 02 §1, documento 09 §1, documento 99 §5/§8 se a
  rastreabilidade mudar, e a linha da fatia 27 no cronograma.
- Esteiras do backend e de `apps/*` já existem; nenhuma esteira nova.
