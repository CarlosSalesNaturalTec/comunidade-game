## 1. Núcleo — modelo e migração

- [ ] 1.1 `ArtefatoComprobatorio` ganha `endereco_original`, `rotulo_original` e `editado_em`,
      os três nulos, com a revisão do Alembic que cria e derruba as colunas (`RN-09-14`,
      design — decisão 3, Migration Plan). Verificar por `alembic upgrade head` e
      `alembic downgrade -1` no banco de teste.

## 2. Núcleo — regra

- [ ] 2.1 `definir_avatar_do_mestre`: grava o avatar do Mestre em sessão **sem** consultar
      moeda acumulada, opaco à forma do valor, no molde do avatar do Apoiador menos o piso
      (`RF-09-114`, `RN-14-11`, design — decisão 1).
- [ ] 2.2 `editar_artefato_do_mestre`: altera rótulo e endereço de artefato do próprio perfil,
      o declarado no cadastro incluído; na **primeira** edição de artefato de cadastro grava
      `endereco_original`, `rotulo_original` e `editado_em`, e nas seguintes preserva o
      original já guardado (`RF-09-66`, `RN-09-14`, design — decisões 3 e 4).

## 3. Núcleo — rotas

- [ ] 3.1 `PUT /v1/eu/mestre/identidade` passa a receber `nick` e `avatar`, cada um opcional, e
      a devolver os dois; a entrada só de nick deixa de existir (`RF-09-114`, design —
      decisão 1).
- [ ] 3.2 `GET /v1/eu/mestre/identidade`, restrita ao Mestre, devolvendo nick e avatar
      vigentes e nenhum dado de moeda; outro papel recebe 403 (`RF-09-114`, design —
      decisão 2).
- [ ] 3.3 `PATCH /v1/mestres/{id}/artefatos/{artefato_id}`, com a mesma guarda de perfil
      próprio da publicação e da remoção: 403 para perfil alheio, 404 para artefato que não é
      do perfil (`RF-09-66`, `RN-09-14`, design — decisão 4).
- [ ] 3.4 A saída dos adultos em `GET /v1/mestres` e `GET /v1/apoiadores` passa a trazer, por
      artefato, o rótulo e o endereço originais quando houver, para a gestão distinguir o que
      foi editado (`RF-02-04`, design — decisão 5).

## 4. App 09 — Meu perfil

- [ ] 4.1 `perfil/api.ts` ganha a leitura e a gravação da identidade e a edição de artefato.
- [ ] 4.2 `TelaDoPerfil.tsx` apresenta o nick e o avatar vigentes e oferece definir ou trocar
      cada um, sem sugerir nick e sem condicionar o avatar a moeda; nick em uso é recusado sem
      identificar de quem é (`RF-09-114`, `RN-01-30`, `RN-14-10`).
- [ ] 4.3 `TelaDoPerfil.tsx` oferece editar rótulo e endereço de cada artefato, o do cadastro
      incluído — que segue marcado e sem caminho de remoção —, mantendo a declaração de que o
      cadastro de Mestre é ato exclusivo de Admin (`RF-09-66`, `RF-09-67`, `RN-09-14`).

## 5. App 03 — o original na ficha

- [ ] 5.1 `FichaDoAdulto.tsx` marca o artefato de cadastro editado e mostra o valor original ao
      lado do vigente, sem oferecer editar, restaurar ou remover (`RF-02-04`, `RN-02-01`,
      `RN-09-14`, design — decisão 5).

## 6. Testes

- [ ] 6.1 Núcleo, identidade do Mestre: grava nick e avatar juntos e cada um em separado; grava
      avatar sem moeda alguma; recusa nick em uso sem revelar de quem é; a leitura devolve os
      dois vazios quando nunca definidos; outro papel recebe 403 na leitura e na gravação
      (cenários das duas requirements de `identidade-do-adulto`).
- [ ] 6.2 Núcleo, edição de artefato: corrige o publicado pelo próprio; corrige o do cadastro e
      ele permanece no perfil; a remoção do de cadastro segue recusada; perfil alheio recebe
      403; a primeira edição fixa o original, a segunda o preserva, e o artefato intocado não
      tem original (cenários das duas requirements de `prova-de-habilidade`).
- [ ] 6.3 App 09, `perfil.test.tsx`: o perfil mostra nick e avatar vigentes ou a ausência
      deles; grava o nick sem sugerir nenhum; edita o endereço de um artefato; o do cadastro
      oferece editar e não oferece remover; nenhum campo de nome, e-mail ou papel aparece
      (cenários das duas requirements de `area-do-mestre`).
- [ ] 6.4 App 03, `personas.test.tsx`: a ficha marca o artefato de cadastro editado com o valor
      original ao lado do vigente, o intocado aparece limpo, e nenhum caminho de edição é
      oferecido à gestão (cenário da requirement de `aplicacao-de-gestao`).

## 7. Documentação

- [ ] 7.1 Documento 02 §1: a prova declarada pelo Admin no cadastro passa a ser **editável pelo
      próprio adulto e irremovível por ele**, guardando o valor original — a frase que hoje diz
      apenas "permanece". Documento 09 §1: mover para *Já decididos* as três decisões do
      fundador de 2026-09-06 — o avatar do Mestre sem piso, a leitura da própria identidade e a
      edição do artefato de cadastro com o original guardado. PRD-09 §9: as duas rotas novas e
      o avatar na rota existente; PRD-09 §15 se a rastreabilidade mudar. Marcar a fatia 16 como
      implementada em `openspec/cronograma-de-fatias.md`. Nenhum arquivo novo em `docs/`, logo
      nenhuma entrada nova na `nav` do `mkdocs.yml`; a relação entre documentos não muda, logo
      o documento 99 não é tocado.
