# Tasks

## 1. Núcleo — tipo de recurso

- [x] 1.1 Marca de ativo: coluna `ativo` em `TipoDeRecurso` e migração Alembic com
      `server_default true` (`RF-07-52`; design — decisão 7). Verifica: `alembic upgrade head` e
      `downgrade -1` sem erro sobre o banco de teste, e tipo existente lido como ativo.
- [x] 1.2 `recursos/regra.py`: `alterar_tipo_de_recurso` (nome, unidade, exige comprovante;
      natureza recusada com 422), `desativar_`/`reativar_tipo_de_recurso`,
      `exigir_tipo_de_recurso_ativo` e `excluir_tipo_de_recurso` com o helper de "nunca usado"
      por `Base.metadata`, excluindo as vigências, que saem junto (`RF-07-51`, `RF-07-52`,
      `RN-07-40`; design — decisões 2 e 4). Verifica: testes da 4.1.
- [x] 1.3 `recursos/rotas.py`: `PATCH`, `DELETE`, `POST …/desativacao`, `POST …/reativacao` e
      `POST …/valores-de-referencia` em `/v1/tipos-de-recurso/{id}`, 404 para id inexistente, e
      `ativo` na saída da leitura (`RF-07-51`, `RF-07-52`, `RN-07-40`, `RF-07-02`; design —
      decisão 1). Verifica: testes da 4.2.
- [x] 1.4 Guarda de escolha nova: chamar `exigir_tipo_de_recurso_ativo` em `agendar_aula`,
      `registrar_aporte`, `registrar_aporte_por_absorcao` só quando sem aula,
      `declarar_recompensa_de_marco`, `cadastrar_item` do catálogo avulso e
      `propor_desafio_extra` (`RF-07-52`; design — decisão 6). Verifica: testes da 4.3.

## 2. Núcleo — tipo de coleta

- [x] 2.1 `coletas/regra.py`: `alterar_tipo_de_coleta` passa a aceitar os quatro campos e valida
      o tipo resultante por `_conferir_unidade_e_faixa`; `reativar_tipo_de_coleta`;
      `excluir_tipo_de_coleta` pelo mesmo helper de "nunca usado" (`RF-08-32`, `RN-08-30`;
      design — decisões 3 e 4). Verifica: testes da 4.4.
- [x] 2.2 `coletas/rotas.py`: `PATCH` (ausente mantém, nulo retira, por `model_fields_set`),
      `DELETE`, `POST …/desativacao` e `POST …/reativacao` em `/v1/tipos-de-coleta/{id}`, sob
      `Operacao.catalogo_de_tipos_de_coleta` "escreve", 404 para id inexistente (`RF-08-32`,
      `RN-08-30`; design — decisões 1 e 3). Verifica: testes da 4.4.

## 3. Aplicações

- [x] 3.1 App 03, `src/recursos/api.ts` e `src/catalogos/api.ts`: `ativo` no tipo de recurso e
      as chamadas de alterar, desativar, reativar, excluir, vigência nova do valor, registro e
      histórico do preço (`RF-02-113` a `RF-02-115`). Verifica: `api.test.ts`.
- [x] 3.2 App 03, `src/catalogos/`: edição do tipo de recurso em componente próprio (natureza em
      leitura, vigência nova opcional do valor e do preço, com o vigente de partida e o aviso de
      que a anterior se encerra), `FormularioDeTipoDeColeta` com `tipoEmEdicao` e o aviso de troca
      de forma, marca de ativo na lista de recurso, e Desativar/Reativar/Excluir em dois passos no
      molde de `DesativarPoder`, tudo só para Admin (`RF-02-113`, `RF-02-114`, `RF-02-115`;
      design — decisão 8). Verifica: testes da 4.5.
- [x] 3.3 Seletores de escolha nova filtram `ativo`: `FormularioDeAgendamento`,
      `RegistroDeAporte` e `HomologacaoDoAporte` na App 03; o seletor da recompensa em
      `autoria/` na App 09, com `ativo` no tipo de `src/recursos/api.ts` dela (`RF-07-52`,
      `RF-09-84`). Verifica: testes da 4.6.

## 4. Testes

- [x] 4.1 `tests/test_tipo_de_recurso.py`: alterar os três campos, natureza recusada, unidade em
      branco, vigências intocadas; desativar,
      reativar e idempotência; excluir nunca usado (vigências saem junto) e recusar o usado por
      aporte, reserva, recompensa e item avulso; 403 do Mestre em cada ato (`RF-07-51`,
      `RF-07-52`, `RN-07-40`).
- [x] 4.2 `tests/test_tipo_de_recurso_rota.py`: as cinco rotas novas — 200/201/204, 404, 403 e
      422 —, vigência nova do valor encerrando a anterior, valor com três casas recusado, e
      `ativo` na leitura com o desativado assinalado (`RF-07-51`, `RF-07-52`, `RF-07-02`).
- [x] 4.3 Guarda de escolha nova em `tests/test_tipo_de_recurso_desativado.py`, um teste por
      ato (agendamento, registro de aporte, absorção sem aula, recompensa, item avulso, desafio
      extra) e os que seguem aceitos com tipo desativado: absorção com aula e transferência
      (`RF-07-52`). A homologação passa pela mesma `registrar_aporte`.
- [x] 4.4 `tests/test_tipo_de_coleta.py` e `tests/test_coletas_rota.py`: alterar faixa, trocar
      número→foto retirando unidade e faixa, foto→número sem faixa recusado, registro gravado
      intocado e registro novo pela forma nova; desativar e reativar com desafio novo
      recusado/aceito; excluir nunca usado e recusar o escolhido por desafio; 403 e 404
      (`RF-08-32`, `RN-08-30`).
- [x] 4.5 App 03, `src/catalogos/catalogos.test.tsx`: editar recurso (nome sem vigência, natureza
      em leitura, vigência nova do valor, preço abaixo do piso no campo), editar coleta (faixa,
      aviso de troca de forma, troca para foto), desativar/reativar, confirmação da exclusão,
      recusa por uso em linguagem simples, tipo excluído sai da lista, marca de inativo por texto,
      e nenhum caminho de escrita para Mestre (`RF-02-113` a `RF-02-115`).
- [x] 4.6 Seletores: tipo desativado ausente no agendamento (App 03) e na declaração de
      recompensa (App 09), e o filtro `apenasAtivos` que o registro de aporte e a homologação
      usam, em `api.test.ts`; a recompensa já declarada segue com o nome do tipo (`RF-07-52`,
      `RF-09-84`).

## 5. Documentação

- [x] 5.1 Decisão de 2026-11-13 no documento 04 §1 (tipo de recurso) e no documento 02 §1 (tipo
      de coleta), em uma frase cada; a linha "Os catálogos de tipo não têm edição nem desativação"
      passa de "Decisões pendentes" a "Já decididos" no documento 09 §1; PRD-02 (`RF-02-113` a
      `RF-02-115`, rotas na §9, pendência retirada da §14), PRD-07 (`RF-07-51`, `RF-07-52`,
      `RN-07-40`, alterando `RF-07-01`) e PRD-08 (`RF-08-32`, `RN-08-30`, alterando `RF-08-05`);
      fatia 27 marcada `implementado` com o slug no `openspec/cronograma-de-fatias.md`. O
      documento 99, `docs/prds/index.md` e a `nav` não mudam: nenhuma relação entre documentos
      nem situação de PRD mudou. Verifica: os identificadores novos aparecem nos três PRDs.
