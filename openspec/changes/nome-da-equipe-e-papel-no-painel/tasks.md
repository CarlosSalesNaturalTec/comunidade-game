# Tasks

## 1. Núcleo — nome da equipe

- [ ] 1.1 Modelo e migração Alembic: `equipe.nome` (`String(20)`, `NOT NULL`), preenchimento
      "Equipe N" por aula ou trilha em ordem de `registrado_em, id`, e os dois índices únicos
      parciais sobre `lower(nome)` declarados também no modelo — `RF-04-69`, `RN-04-39`,
      design 1, 2 e 6. Verificar: `alembic upgrade head` e `downgrade -1` rodam no Postgres de
      teste, e uma base com equipes sem nome sobe com "Equipe 1", "Equipe 2"… em cada aula.
- [ ] 1.2 `equipes/regra.py`: validação do nome (aparado, 1 a 20, `campo="nome"`) e da
      unicidade na aula ou na trilha, sem caixa, com a própria equipe excluída na troca;
      `criar_equipe` recebe `nome` obrigatório; nova `renomear_equipe` com a ordem 403 da
      gestão → 403 de não integrante → trava de `_confirmar_equipe_aberta` → 422 do nome —
      `RF-04-69`, `RF-04-70`, `RN-04-39`, `RF-01-16`, design 1 a 3. Verificar: testes da 4.1.
- [ ] 1.3 `equipes/rotas.py`: `nome` nas entradas de `POST /v1/aulas/{id}/equipes` e
      `POST /v1/trilhas/{id}/equipes`, `PATCH /v1/equipes/{id}` sob
      `equipe_que_forma_na_aula`/`escreve`, e `nome` em `EquipeSaida` — `RF-04-34`,
      `RF-04-69`, `RF-04-70`, design 3 e 4. Verificar: testes da 4.2.
- [ ] 1.4 `painel_do_dia/regra.py`: `nome` em `EquipeDoPainelSaida` e integrantes como
      `IntegranteDoPainelSaida` com `papel` — `RF-02-08`, design 5. Verificar: testes da 4.3.
- [ ] 1.5 Os testes que criam equipe por `criar_equipe` ou por `Equipe(...)` (conftest e cerca
      de vinte arquivos em `backend/tests/`) passam a dar um nome, único por aula ou trilha
      dentro de cada teste — sem mudar o que cada teste confere. Verificar: a suíte do backend
      volta verde.

## 2. App 01 — nome ao criar e renomear

- [ ] 2.1 `comum/react/Campo.tsx`: `maxLength` opcional repassado ao `<input>`, sem mudar quem
      não o usa — design 7. Verificar: teste do componente com e sem o limite.
- [ ] 2.2 `src/api/equipes.ts`: `nome` em `Equipe`, `criarEquipe` e `criarEquipeDaTrilha`
      recebem `nome`, e nova `renomearEquipe(equipeId, nome, token)` —
      `RF-04-69`, `RF-04-70`. Verificar: testes da 4.4 e 4.5.
- [ ] 2.3 `src/equipes/TelaDeEquipes.tsx`: campo "Nome da equipe" (máximo 20) com "Criar
      equipe" desabilitado enquanto vazio; cada equipe com o nome como título; "Trocar o
      nome" só nas que o Guerreiro(a) integra, com a recusa do núcleo em linguagem simples e o
      nome anterior mantido — `RF-04-34`, `RF-04-69`, `RF-04-70`, `RN-04-36`, design 7.
      Verificar: testes da 4.4.
- [ ] 2.4 `src/trilhas/EquipeDaTrilha.tsx`: o mesmo campo na criação, a equipe da trilha pelo
      nome e "Trocar o nome" só antes da homologação — `RF-04-69`, `RF-04-70`, design 7.
      Verificar: testes da 4.5.

## 3. App 03 — painel do dia

- [ ] 3.1 `src/painel-do-dia/api.ts` e `TelaDoPainelDoDia.tsx`: `nome` na equipe e `papel` no
      integrante; o item mostra o nome e a lista "nick — papel", só o nick sem papel, sem
      ação de escrita — `RF-02-08`, `RF-02-09`, design 8. Verificar: testes da 4.6.

## 4. Testes

- [ ] 4.1 `backend/tests/test_equipe.py`: criar com nome, sem nome, só espaços, 21 caracteres,
      repetido na aula sem caixa, repetido na trilha, mesmo nome em aulas diferentes; renomear
      por integrante, só a caixa do próprio nome, para nome de outra equipe, por não
      integrante, por Admin e Mestre, com aula encerrada e com trilha homologada — spec
      `equipe`.
- [ ] 4.2 `backend/tests/test_equipe_rota.py` e `test_equipe_da_trilha_rota.py`: 201 com o nome
      nas duas criações, 422 sem nome, `PATCH` 200/403/422, e o nome na leitura das equipes da
      aula sem dado pessoal algum além de avatar e nick — spec `equipe`.
- [ ] 4.3 `backend/tests/test_painel_do_dia.py`: equipe pelo nome, integrante com e sem papel,
      nome novo na consulta seguinte à troca — spec `painel-do-dia`.
- [ ] 4.4 `apps/app-01-aula-presencial/src/equipes/equipes.test.tsx`: criar sem nome não envia,
      criar com nome envia o nome, nome repetido em linguagem simples, equipes pelo nome com
      avatar e nick, "Trocar o nome" só nas que integra, recusa da troca mantendo o nome
      anterior — spec `aplicacao-da-aula-presencial`.
- [ ] 4.5 `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`: criação da equipe da
      trilha com nome, nome repetido na trilha em linguagem simples, sem "Trocar o nome" depois
      da homologação — spec `aplicacao-da-aula-presencial`.
- [ ] 4.6 `apps/app-03-gestao/src/painel-do-dia/painel-do-dia.test.tsx`: equipe pelo nome,
      integrante com papel e só pelo nick sem papel, nenhum caminho para renomear — spec
      `aplicacao-de-gestao`.

## 5. Documentação

- [ ] 5.1 Gravar as duas regras decididas na elicitação (comparação sem caixa e sem espaços;
      troca travada com a composição): uma frase no documento 02 §5, o acréscimo na linha
      "Presença e equipes em caminhos separados, e a equipe com nome" do documento 09, e o
      texto de `RF-04-70` e `RN-04-39` no PRD-04. Ao fechar, a fatia 17 do PRD-04 vira
      `implementado` em `openspec/cronograma-de-fatias.md`, com o slug da change.
      `docs/prds/index.md`, o documento 99 e o `mkdocs.yml` não mudam — nenhuma situação de
      PRD, relação entre documentos ou arquivo novo.
