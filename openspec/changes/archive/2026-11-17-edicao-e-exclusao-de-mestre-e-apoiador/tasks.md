## 1. Núcleo

- [x] 1.1 Migração Alembic e modelo: `persona.desativada_em` (`timestamptz`, nulo), sem retroação;
      `AdultoSaida` ganha `ativo` (`RF-02-119`, `RN-02-35`)
- [x] 1.2 `personas/regra.py`: `alterar_adulto` (nome, e-mail, WhatsApp; troca o identificador da
      credencial de login social; colisão de e-mail vira 422) e os atos de artefato pela gestão —
      incluir, corrigir sem tocar o original, remover recusando o último (`RF-02-117`,
      `RF-02-04`, `RN-02-01`)
- [x] 1.3 `personas/regra.py`: `excluir_adulto` pelo `esta_em_uso`, ignorando nick, credencial,
      sessão e artefato, que saem junto; uso e corrida viram 422 que aponta a desativação
      (`RF-02-118`, `RN-02-34`)
- [x] 1.4 `personas/regra.py`: `desativar_adulto` (revoga credenciais, encerra sessões, grava a
      marca) e `reativar_adulto` (limpa a marca, reativa só o login social revogado pela
      desativação) (`RF-02-119`, `RN-02-35`)
- [x] 1.5 `personas/rotas.py`: `PATCH`, `DELETE`, `POST .../desativacao`, `POST .../reativacao` e
      as rotas de `artefatos-da-gestao` para `/v1/mestres` e `/v1/apoiadores`, restritas a Admin,
      com `extra="forbid"` e 404 para papel trocado (`RF-02-117` a `RF-02-119`)
- [x] 1.6 Login social e por usuário e senha recusam o desativado; `vitrine/` filtra o desativado
      na listagem e na leitura por identificador de Mestres e Apoiadores (`RF-02-119`,
      `RN-02-35`)

## 2. App 03

- [x] 2.1 `personas/api.ts`: chamadas de alterar, excluir, desativar, reativar e dos artefatos da
      gestão; tipo do adulto ganha `ativo` (`RF-02-117` a `RF-02-119`)
- [x] 2.2 `FichaDoAdulto.tsx`, `EdicaoDoAdulto.tsx` e `ArtefatosDoAdulto.tsx` (novos): edição de nome, e-mail e WhatsApp,
      inclusão, correção e remoção de artefato, recusa do núcleo no formulário, sem campo de nick
      já gravado, papel ou termos (`RF-02-117`, `RF-02-04`)
- [x] 2.3 `AcoesDoAdulto.tsx` (novo), `FichaDoAdulto.tsx` e `ListaDeAdultos.tsx`: excluir, desativar e reativar com confirmação;
      recusa da exclusão oferece desativar; linha e ficha marcam o desativado (`RF-02-118`,
      `RF-02-119`, `RN-02-34`, `RN-02-35`)

## 3. Testes

- [x] 3.1 `tests/test_edicao_e_exclusao_de_adulto.py` (novo), edição: alteração e troca de e-mail com login pelo novo,
      colisão de e-mail, nick no corpo, último artefato, correção preservando o original, 403 para
      não Admin, 404 para papel trocado (`RF-02-117`)
- [x] 3.2 `tests/test_edicao_e_exclusao_de_adulto.py`, exclusão e desativação: exclusão do nunca usado,
      recusa com aporte e com trilha, desativação que derruba a sessão e recusa o login, fatos
      inalterados, reativação, ausência na vitrine e 404 na página individual (`RF-02-118`,
      `RF-02-119`, `RN-02-34`, `RN-02-35`)
- [x] 3.3 `personas/personas.test.tsx` e `api.test.ts`: edição na ficha, recusa do último artefato,
      ausência de campo de nick, exclusão recusada levando à desativação, exclusão confirmada,
      marca do desativado e reativação (`RF-02-117` a `RF-02-119`)

## 4. Documentação

- [x] 4.1 Documento 02 §1 com a decisão (edição, exclusão do nunca usado, desativação e
      reativação); linha "O que a fatia 18 do PRD-02 deixa fora" do documento 09 §1 revista e
      decisão nova em "Já decididos"; PRD-02 com `RF-02-117` a `RF-02-119` em §6.1, `RN-02-34` e
      `RN-02-35` em §7, `RF-02-02`/`RF-02-03` alterados, rotas na §9, §13 e §15; fatia 29 como
      `implementado` no cronograma. Sem arquivo novo em `docs/`, sem mudança no documento 99
