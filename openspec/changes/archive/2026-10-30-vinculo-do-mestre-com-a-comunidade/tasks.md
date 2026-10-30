# Tasks

## 1. Modelo e migração

- [x] 1.1 Criar, em `backend/src/nucleo/comunidades/modelo.py`, o **vínculo do Mestre com a
      Comunidade Virtual** — persona, comunidade e data de início, **sem `data_fim`** — e a
      relação `Persona.comunidades_do_mestre`, com índice único por par para não abrir vínculo
      repetido; verificar que `Base.metadata` traz a tabela e que o par duplicado é recusado
      pelo índice (`RN-08-02`, `RN-01-05`, spec `comunidade-virtual`).
- [x] 1.2 Criar, em `backend/src/nucleo/aulas/modelo.py`, `MestreDaAula` (aula × mestre, N:N),
      com índice único por par; verificar em `Base.metadata` (`RF-02-30`, spec
      `aula-e-presenca`).
- [x] 1.3 Escrever a revisão Alembic que cria as duas tabelas vazias e verificar a **paridade**
      entre `alembic upgrade head` e `Base.metadata`, no mesmo teste que a correção
      `2026-09-10-migracao-das-tabelas-de-recompensa-de-marco` instituiu — o `conftest` monta o
      schema com `create_all` e não pega a falta.

## 2. Vínculo do Mestre e escopo único de comunidade

- [x] 2.1 Em `comunidades/regra.py`, escrever `abrir_vinculo_do_mestre` — recusa papel que não
      seja Mestre, não repete vínculo existente — e `comunidades_do_mestre`, que devolve o
      conjunto de ids; manter `abrir_vinculo` recusando papel diverso de Guerreiro(a)
      (`RN-08-02`, spec `comunidade-virtual`).
- [x] 2.2 Em `comunidades/regra.py`, escrever o **escopo único de leitura** que devolve
      conjunto de ids — Admin declara a comunidade e recebe conjunto de um, Mestre recebe as
      dele, conjunto vazio significa lista vazia e nunca erro — e remover as três cópias de
      `escopo_de_comunidade_da_leitura` de `aulas/regra.py`, `pontos_de_apoio/regra.py` e a
      lógica embutida em `patrimonio.listar_acervo` (design — decisão 3).
- [x] 2.3 Substituir a fixture `criar_vinculo_jogador(mestre, …)` por fixture do vínculo do
      Mestre em `backend/tests/conftest.py`, e migrar as 63 chamadas dos 24 arquivos de teste;
      verificar que a suíte passa sem nenhum `VinculoJogador` com `guerreiro_id` de Mestre
      (design — decisão 5).
- [x] 2.4 Escrever `backend/tests/test_vinculo_do_mestre.py` cobrindo os cenários de
      `comunidade-virtual`: Mestre vinculado a duas comunidades, vínculo do Guerreiro(a)
      recusando Mestre com 422, Mestre sem vínculo lendo vazio e nunca erro, aula cancelada que
      não desfaz o vínculo, e ausência de rota que o encerre.

## 3. Agendamento com Mestres

- [x] 3.1 Em `aulas/regra.py`, fazer `agendar_aula` exigir **um ou mais Mestres** — 422 com o
      campo em falta quando vier nenhum, 422 quando a persona escalada não for Mestre —,
      gravar `MestreDaAula` e **abrir o vínculo** de cada Mestre com a comunidade da aula na
      mesma operação (`RF-02-30`, `RF-01-20`, spec `aula-e-presenca`).
- [x] 3.2 Em `aulas/rotas.py`, receber os Mestres no corpo de `POST /v1/aulas` e devolvê-los na
      saída da aula; verificar o contrato pelo OpenAPI (`RF-02-30`, documento 03 §1).
- [x] 3.3 Cobrir os cenários novos de `aula-e-presenca`: aula escalada com dois Mestres, aula
      sem Mestre recusada com 422, persona que não é Mestre recusada na escalação, o
      agendamento que vincula o Mestre à comunidade e o segundo agendamento que não repete o
      vínculo. Os de **regra** ficaram em `tests/test_vinculo_do_mestre.py`, junto dos demais
      do vínculo, e não em `test_aula.py` como esta linha previa; o de **rota** — corpo sem
      Mestre recusado e os escalados na saída — está em `test_aula_rota.py`.

## 4. Os oito pontos de leitura e as duas guardas de escrita

- [x] 4.1 Passar ao escopo único, trocando `== id` por pertinência ao conjunto:
      `patrimonio.listar_acervo` (`RF-07-11`), `pontos_de_apoio` (`RF-07-47`),
      `aulas.escopo_de_comunidade_da_leitura` (`RF-02-41` a `RF-02-47`), `necessidades`
      (`RF-07-27`, que já recebe `comunidade_ids`) e as duas leituras de `responsaveis`
      (`RF-09-62`, `RF-09-122`).
- [x] 4.2 Passar `painel_do_dia._resolver_aula` ao conjunto de comunidades e **explicitar o
      desempate** — havendo mais de uma aula vigente, serve a de início mais antigo (spec
      `painel-do-dia`, `RF-01-32`, `RF-01-18`).
- [x] 4.3 Passar `recompensas_de_marco.listar_entregas_pendentes` ao conjunto, reunindo as
      pendências de todas as comunidades do Mestre, e `registrar_entrega` à pertinência — o
      Mestre confirma quando a comunidade do Guerreiro(a) estiver entre as dele (`RF-09-75`,
      `RF-09-76`, `RF-07-13`, spec `recompensa-de-marco`).
- [x] 4.4 Passar a guarda de `cancelar_aula` à pertinência, mantendo o enunciado vigente —
      Admin ou Mestre vinculado à comunidade da aula (`RF-01-72`, `RF-02-95`).
- [x] 4.5 Cobrir os pontos de leitura e as guardas nos arquivos de teste que já os exercitam —
      `test_patrimonio_rota.py`, `test_ponto_de_apoio.py`, `test_necessidade.py`,
      `test_responsavel.py`, `test_guerreiros_vinculaveis_rota.py`, `test_painel_do_dia.py`,
      `test_aula.py`, `test_entregas_pendentes.py` e `test_entrega_de_recompensa.py` —, com o
      Mestre vinculado a **duas** comunidades em cada um, para provar o plural que as specs já
      exigiam; incluir o desempate do painel e a fila que reúne as duas comunidades.

- [x] 4.6 Passar ao conjunto os **seis pontos que só apareceram na implementação**: o
      histórico de entregas (`RF-07-13`), em que o **Admin passa a ler todas** por decisão do
      fundador de 2026-10-30; o registro e o histórico da troca avulsa (`RF-07-35`,
      `RF-07-36`); e os três do catálogo avulso — a guarda de operação sobre o item, o
      cadastro e a leitura (`RF-07-33`, `RF-09-103`).
- [x] 4.7 Cobrir os seis em `test_entrega_de_recompensa.py`, `test_trocas.py` e
      `test_catalogo_avulso.py`, com o Mestre vinculado a duas comunidades, e incluir o Admin
      lendo o histórico de entregas de mais de uma comunidade sem declarar filtro.

## 5. App 03 — seleção de Mestres no agendamento

- [x] 5.1 Em `apps/app-03-gestao/src/agenda/FormularioDeAgendamento.tsx`, acrescentar a seleção
      de **um ou mais Mestres**, alimentada por `listarMestres` (`GET /v1/mestres`) **sem
      recorte por comunidade**, e impedir a confirmação sem Mestre, apontando a falta no
      próprio campo (`RF-02-30`, spec `aplicacao-de-gestao`, design — decisão 4).
- [x] 5.2 Cobrir em `apps/app-03-gestao/src/agenda/agenda.test.tsx` os cenários novos de
      `aplicacao-de-gestao`: agendamento com Mestres, agendamento sem Mestre apontado no campo
      e os Mestres oferecidos sem recorte por comunidade.

## 6. Documentação

- [x] 6.1 No mesmo PR: marcar a linha desta change como implementada, com o slug, em
      `openspec/cronograma-de-fatias.md`; acrescentar os Mestres à `Aula/Agenda` no **PRD-01
      §8** e no **PRD-02 §8**; tornar `RF-02-30` obrigatório quanto aos Mestres e passar
      `RF-02-59` do singular "Mestre da aula" ao plural; registrar no **documento 99 §6** que o
      invariante 4 passa a ter a metade do Mestre; e gravar no `docs/09` §1 a decisão de
      2026-10-30 sobre o **alcance do Admin no histórico de entregas**, corrigindo o PRD-02
      (`RF-02-50`, `RF-02-51`) e o PRD-07 (`RF-07-13`), que o mandavam ler pela comunidade a
      que está vinculado. `docs/prds/index.md` **não muda** — nenhum PRD mudou de situação.

## Workflow follow-up

- Arquivar a change depois da aprovação do fundador, com merge commit — nunca squash.
