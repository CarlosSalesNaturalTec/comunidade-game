## 1. Núcleo — leitura dos vinculáveis e artefatos do próprio Mestre

- [x] 1.1 Acrescentar `Operacao.vinculo_com_guerreiros_e_guerreiras` ao conjunto `le` do Mestre
      e `Operacao.documentos_comprobatorios` ao `escreve` dele em
      `backend/src/nucleo/permissoes.py`; verificar pelo teste da matriz, que passa a recusar os
      demais papéis nas duas operações (`RF-09-62`, `RF-09-66`, design — decisões 1 e 3).
- [x] 1.2 Criar `GET /v1/guerreiros/vinculaveis` em `backend/src/nucleo/responsaveis/`,
      devolvendo nick e avatar dos Guerreiros e Guerreiras ativos das comunidades do Mestre em
      sessão, paginado pelo contrato de listagem do PRD-01; verificar que a resposta não traz
      nome civil, nascimento, imagem nem contato, e que criança de outra comunidade não aparece
      (`RF-09-62`, `RN-09-18`).
- [x] 1.3 Acrescentar `declarado_por_id` a `ArtefatoComprobatorio` e a migração Alembic
      correspondente, e gravar a persona do operador em `cadastrar_adulto_com_artefatos`;
      verificar que o schema sobe pelo Alembic e por `create_all`, e que a linha antiga
      permanece com o campo nulo (design — decisão 2).
- [x] 1.4 Criar `GET`, `POST` e `DELETE` de `/v1/mestres/{id}/artefatos` em
      `backend/src/nucleo/personas/rotas.py`, conferindo o `{id}` contra a persona em sessão e
      recusando a remoção do artefato que o Mestre não declarou; verificar 403 para outra
      persona, 403 para outro papel, 422 sem endereço ou sem rótulo e a permanência do artefato
      do cadastro (`RF-09-66`, `RF-09-67`, `RN-09-14`).

## 2. Testes do núcleo

- [x] 2.1 Testar a leitura dos vinculáveis em `backend/tests/`: o Mestre vê os ativos da sua
      comunidade por nick e avatar, criança de outra comunidade não aparece, papel sem
      permissão recebe 403 e nenhuma persona é criada pela rota (`RF-09-62`, `RN-01-20`).
- [x] 2.2 Testar os artefatos do próprio Mestre: publicação com endereço e rótulo, recusa de
      artefato incompleto (422), recusa de perfil alheio e de outro papel (403), remoção do que
      ele publicou, recusa da remoção do que o Admin declarou (403) e a leitura distinguindo a
      origem de cada um (`RF-09-66`, `RF-09-67`, `RN-09-14`).

## 3. App 09 — área Responsáveis

- [x] 3.1 Criar `apps/app-09-mestre/src/responsaveis/api.ts` com as chamadas de cadastro,
      vínculo, credencial provisória e leitura dos vinculáveis, e registrar a área na navegação
      do `App.tsx` (`RF-09-62` a `RF-09-65`).
- [x] 3.2 Criar a tela do fluxo — cadastro pelo nome, com a declaração da apresentação
      presencial; vínculo escolhendo o Guerreiro(a) por nick e avatar, com grau de parentesco
      exigido por vínculo; e a credencial opcional, com a senha provisória exibida uma vez e sem
      caminho de recuperação. O identificador do responsável já criado não é recriado na
      retentativa (`RF-09-62`, `RF-09-63`, `RF-09-65`, `RN-09-15`, `RN-09-23`, design —
      decisão 4).
- [x] 3.3 Apresentar a recusa do quarto vínculo como o teto de três por criança, em linguagem
      simples, sem a App contar vínculos por conta própria e sem desfazer o que já foi criado
      (`RF-09-64`, `RN-09-16`).

## 4. App 09 — Meu perfil

- [x] 4.1 Criar `apps/app-09-mestre/src/perfil/` com a leitura e a publicação dos artefatos por
      endereço e rótulo, sem campo de anexo, marcando em leitura os declarados no cadastro e
      oferecendo remoção só dos que o Mestre publicou; registrar a área na navegação
      (`RF-09-66`).
- [x] 4.2 Declarar na área que o cadastro de Mestre é ato exclusivo de Admin, com habilidade
      comprovada, sem oferecer campo algum para alterar nome, e-mail ou papel — a área só
      alcança os artefatos comprobatórios (`RF-09-67`, `RN-09-14`).

## 5. App 09 — camada de direitos

- [x] 5.1 Criar `apps/app-09-mestre/src/direitos/` com `AvisoDeColeta`, `ContextoDeDireitos` e
      `TelaDeDireitos`, esta com a tabela do PRD-09 §11 e as declarações em prosa da §11 —
      imagem real nunca exibida, criação original só na vitrine com autorização, pontuação
      negativa restrita, direitos exercidos pela App 07 —, sem escrita, exclusão ou exportação;
      registrar a área na navegação e o provedor no `App.tsx` (`RF-09-68`, `RN-09-18`,
      `RN-09-19`, design — decisão 5).
- [x] 5.2 Acrescentar o aviso de coleta, nomeando o dado daquela tela, às telas do responsável,
      do perfil, do conteúdo autoral da missão, da conferência de presença, do lançamento do
      desfecho, da ocorrência de conduta e da validação da criação original; verificar que
      nenhuma delas exige confirmação do aviso para enviar o formulário (`RF-09-68`).

## 6. Testes da App 09

- [x] 6.1 Testar a área Responsáveis: cadastro com a declaração presencial visível, vínculo com
      grau exigido, dois vínculos com graus distintos, escolha por nick e avatar sem imagem
      real, quarto vínculo recusado com o texto do teto e sem perder o já criado, e a senha
      provisória exibida uma vez e não recuperável (`RF-09-62` a `RF-09-65`, `RN-09-15`).
- [x] 6.2 Testar Meu perfil: publicação por endereço e rótulo, ausência de campo de anexo,
      artefato do cadastro marcado e sem remoção, remoção do próprio, e a ausência de qualquer
      caminho de cadastro de Mestre ou de edição do próprio cadastro (`RF-09-66`, `RF-09-67`).
- [x] 6.3 Testar a camada de direitos: a tabela da §11 apresentada com finalidade, base legal,
      retenção e quem acessa; o aviso levando à área; o aviso nomeando o dado da tela em que
      está; e a área sem escrita, exclusão ou exportação (`RF-09-68`).

## 7. Documentação, no mesmo PR

- [x] 7.1 Gravar as duas decisões do fundador de 2026-08-29 no documento-fonte de cada uma —
      documento 03 §9 (o Mestre lê os Guerreiros e Guerreiras que pode vincular, recortado pelas
      comunidades em que atua) e documento 02 §1 (o artefato declarado por Admin não é removido
      por quem foi cadastrado) — e a linha de cada uma em `docs/09-topicos-em-aberto-e-sugestoes.md`
      §1, em "Já decididos".
- [x] 7.2 Aplicar as decisões nos PRDs: PRD-01 §4 (as duas operações na linha do Mestre) e §9 (as
      rotas novas), e PRD-09 §9 (a leitura dos vinculáveis e as três rotas de artefato). Nenhum
      requisito novo — as rotas atendem `RF-09-62` e `RF-09-66`, que já existem.
- [x] 7.3 Marcar as fatias 10 e 11 do PRD-09 como implementadas em
      `openspec/cronograma-de-fatias.md`, com o slug desta change nas duas linhas. `docs/prds/index.md`,
      o documento 99 e a `nav` do `mkdocs.yml` não mudam: a situação do PRD-09 segue a mesma,
      nenhuma relação entre documentos muda e nenhum arquivo nasce em `docs/`.
