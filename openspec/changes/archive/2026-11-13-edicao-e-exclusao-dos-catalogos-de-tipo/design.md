# Design

## Context

Os dois catálogos e a área Catálogos já existem: `openspec/specs/catalogo-de-tipos-de-recurso`,
`catalogo-de-tipos-de-coleta` e os requisitos da área em `aplicacao-de-gestao` (fatia 19 do
PRD-02). Estado de partida no código:

- `nucleo/recursos/` — `TipoDeRecurso` sem marca de ativo; rotas de cadastro, leitura e preço em
  pontos (registro e histórico). `registrar_valor_de_referencia` já abre vigência nova, mas só é
  chamada pelo cadastro.
- `nucleo/coletas/regra.py` — `alterar_tipo_de_coleta` (só nome) e `desativar_tipo_de_coleta`
  existem **sem rota**; a escrita passa por `Operacao.catalogo_de_tipos_de_coleta`.
- `tipo_de_recurso.id` é chave estrangeira de onze tabelas (livro-razão, aporte, aporte
  declarado, reserva, recurso declarado da aula, recompensa de marco, item avulso, desafio
  extra, missão do Apoiador, valor e preço de referência); `tipo_de_coleta.id`, só do desafio de
  coleta.
- App 03, `src/catalogos/` — listas e formulários de cadastro; o molde de edição e de
  desativação em dois passos está em `src/poderes/` (`FormularioDePoder` com `emEdicao`,
  `DesativarPoder`).

## Goals / Non-Goals

**Goals:** alterar, desativar, reativar e excluir nos dois catálogos, pelo núcleo e pela App 03;
vigência nova do valor e do preço pela edição; o tipo de recurso desativado fora da escolha nova.

**Non-Goals:** alterar a natureza; corrigir ou apagar vigência registrada; `RF-07-03`; filtro de
inativos na leitura por nome.

## Decisions

1. **Rotas, no precedente do núcleo.** Para `/v1/tipos-de-recurso/{id}` e
   `/v1/tipos-de-coleta/{id}`: `PATCH` (alteração parcial, `extra="forbid"`), `DELETE` (204),
   `POST …/desativacao` e `POST …/reativacao` (precedente de `pontos-de-apoio`), e
   `POST /v1/tipos-de-recurso/{id}/valores-de-referencia`, irmã da rota de preço que já existe.
   Id inexistente no caminho responde **404** (`NaoEncontrado`). Alternativa descartada: `PUT`
   com o tipo inteiro — obrigaria a reenviar a natureza só para recusá-la.
2. **Natureza recusada com mensagem, não por `extra="forbid"`.** A entrada do `PATCH` de recurso
   aceita `natureza` como campo opcional só para a regra responder 422 dizendo que a natureza não
   se altera; com `extra="forbid"` o 422 sairia genérico.
3. **Alteração do tipo de coleta valida o tipo resultante.** `alterar_tipo_de_coleta` passa a
   aceitar os quatro campos, monta o estado final (o enviado sobre o atual) e reaproveita
   `_conferir_unidade_e_faixa`. Para limpar unidade e faixa ao trocar para foto ou vídeo, o
   `PATCH` distingue campo **ausente** (mantém) de **nulo** (retira), por
   `model_fields_set`.
4. **"Nunca usado" pelo próprio esquema.** Um helper percorre `Base.metadata` atrás de toda
   chave estrangeira que aponta para a tabela do tipo e faz `EXISTS` em cada uma, excluindo as
   vigências de valor e de preço, que saem junto com o tipo. Tabela nova que referencie o tipo
   entra na conferência sem tocar no helper. A `IntegrityError` de corrida entre a conferência e o
   `DELETE` vira o mesmo 422 de "em uso". Alternativa descartada: lista fixa de tabelas — envelhece
   na primeira fatia que criar referência nova.
5. **Recusa por uso é 422**, como toda recusa de regra do núcleo; o projeto não usa 409.
6. **Guarda de tipo ativo na regra, não na rota.** `exigir_tipo_de_recurso_ativo` em
   `recursos/regra.py`, chamada nas regras dos atos de escolha nova: agendar aula (recurso
   declarado), `registrar_aporte` (inclui a homologação), absorção **sem** aula, declarar
   recompensa de marco, cadastrar item avulso e propor desafio extra. Absorção com aula, missão
   do Apoiador, transferência, entrega e troca seguem fato existente e **não** a chamam.
7. **Migração Alembic** acrescenta `tipo_de_recurso.ativo` `NOT NULL` com `server_default
   true`: todo tipo existente nasce ativo, sem retroação.
8. **App 03.** `FormularioDeTipoDeColeta` ganha `tipoEmEdicao`, no molde de
   `FormularioDePoder`. A edição de recurso é componente próprio — natureza em leitura e duas
   seções opcionais de vigência nova —, porque o cadastro grava tipo e primeira vigência num ato
   só e a edição não. O preço vigente vem da rota de histórico que já existe. Desativar, Reativar
   e Excluir seguem `DesativarPoder`: confirmação em dois passos dentro da linha. Os seletores de
   escolha nova (`FormularioDeAgendamento`, `RegistroDeAporte`, `HomologacaoDoAporte` e o da
   recompensa na App 09) filtram `ativo` no próprio componente; `listarTiposDeRecurso` segue
   devolvendo todos, porque também serve leitura por nome.

## Risks / Trade-offs

- **Trocar a forma de registro de tipo já usado** muda o que os desafios existentes exigem do
  registro novo — decisão do fundador de 2026-11-13. Mitigação: o aviso na edição (spec da App
  03) e os registros gravados intocados.
- **Tipo de recurso com vigência futura não aparece na lista**, então não se edita nem se exclui
  até o dia de início — limitação herdada da fatia 19, mantida.
- **Exclusão física** apaga a linha do tipo, com a autoria que ela guardava; o ato fica na
  trilha central, que o middleware de `nucleo/auditoria/` grava em toda escrita sob `/v1` e que
  é somente inserção. Aceitável porque só sai tipo que nenhum fato referencia.
