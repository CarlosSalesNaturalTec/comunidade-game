## 1. Módulo da comunidade e do vínculo

- [x] 1.1 Criar `backend/src/nucleo/comunidades/` com `modelo.py`, movendo `ComunidadeVirtual`
      de `personas/modelo.py` sem mudar o nome da tabela (`RF-08-01`)
- [x] 1.2 Declarar `VinculoJogador` em `comunidades/modelo.py` com Guerreiro(a), comunidade,
      data de início, data de fim e Admin responsável, conforme PRD-08 §8 (`RF-08-02`)
- [x] 1.3 Declarar o índice parcial único de um vínculo vigente por Guerreiro(a)
      (`RN-08-02`, `RN-01-05`, design — Decisions)
- [x] 1.4 Escrever `comunidades/regra.py`: criação da comunidade só por Admin, com nome,
      localização e granularidade máxima, e recusa 422 do campo em falta (`RF-08-01`,
      `RN-08-01`)
- [x] 1.5 Acrescentar a `comunidades/regra.py` a abertura do vínculo e a recusa do segundo
      vínculo vigente, traduzindo o erro do índice em mensagem simples (`RF-08-02`,
      `RN-08-02`)
- [x] 1.6 Escrever `comunidades/rotas.py` com a criação da comunidade por Admin, e 403 para
      qualquer outro papel (`RF-08-01`, `RN-08-01`)

## 2. Módulo dos locais

- [x] 2.1 Criar `backend/src/nucleo/locais/modelo.py` com `Local` — comunidade, nível, rótulo
      e local pai —, o enum ordenado dos seis níveis, o `UNIQUE (id, comunidade_id)` e a
      chave estrangeira composta do pai (`RF-08-04`, design — Decisions)
- [x] 2.2 Declarar o `CheckConstraint` que permite pai vazio somente no nível `comunidade`
      (`RF-08-04`)
- [x] 2.3 Escrever `locais/regra.py`: cadastro só por Admin, e recusa 422 do pai que não é do
      nível imediatamente acima (`RF-08-04`, `RN-08-18`)
- [x] 2.4 Escrever `locais/rotas.py` com o cadastro por Admin e a consulta paginada com
      filtro por comunidade (`RF-08-04`, `RF-01-18`, `RF-01-28`)
- [x] 2.5 Registrar os dois roteadores novos em `backend/src/nucleo/principal.py`

## 3. Troca da coluna pelo vínculo

- [x] 3.1 Criar em `comunidades/regra.py` o helper de filtro de personas por comunidade e a
      `relationship` do vínculo vigente na `Persona` (design — Decisions)
- [x] 3.2 Trocar os seis pontos de leitura de `Persona.comunidade_virtual_id` pelo helper:
      `vitrine/publico.py`, `vitrine/rotas.py`, `aulas/regra.py` e os três de `ods/regra.py`
      (`RN-01-05`)
- [x] 3.3 Ajustar `personas/regra.py` para exigir a comunidade na criação do Guerreiro(a) e
      abrir o vínculo, em vez de gravar a coluna (`RF-08-02`, `RN-01-05`)
- [x] 3.4 Ajustar `aulas/regra.py` para que a comunidade do vínculo venha da aula agendada e
      recusar comunidade declarada no corpo (`RF-08-02`, `RN-08-02`)
- [x] 3.5 Escrever a migração do Alembic na ordem do plano de migração do `design.md`: criar
      tabelas, copiar os vínculos, criar o índice, derrubar a coluna e o `CheckConstraint`,
      com `downgrade` que reconstrói a coluna

## 4. Testes

- [x] 4.1 Comunidade recém-criada responde sem nenhum local — critério de aceite do PRD-08
      §12 (`RF-08-01`, `RN-08-01`)
- [x] 4.2 Criação de comunidade por persona que não é Admin devolve 403, e sem os atributos
      declarados devolve 422 (`RF-08-01`, `RN-08-01`)
- [x] 4.3 Guerreiro(a) cadastrado no onboarding aparece vinculado à comunidade da aula sem
      tê-la informado — critério de aceite do PRD-08 §12 (`RF-08-02`, `RN-08-02`)
- [x] 4.4 Criação de Guerreiro(a) com comunidade declarada no corpo é recusada (`RF-08-02`)
- [x] 4.5 Segundo vínculo vigente é recusado e o existente permanece (`RN-08-02`, `RN-01-05`)
- [x] 4.6 Guerreiro(a) não é criado sem comunidade (`RN-01-05`)
- [x] 4.7 Nenhuma rota transfere Guerreiro(a) entre comunidades: a tentativa devolve 404
      (documento 99 §6 invariante 4)
- [x] 4.8 Local com pai do nível imediatamente acima é aceito; pai de nível errado, pai de
      outra comunidade e nível diferente de `comunidade` sem pai são recusados com 422
      (`RF-08-04`)
- [x] 4.9 Cadastro de local por persona que não é Admin devolve 403 (`RF-08-04`, `RN-08-18`)
- [x] 4.10 A listagem de locais devolve só os da comunidade filtrada, paginada (`RF-01-18`,
      `RF-01-28`)
- [x] 4.11 Rodar a suíte inteira e confirmar que os testes de vitrine, ODS e aula passam sem
      mudança de expectativa depois da troca da coluna (`RN-01-05`)
- [x] 4.12 Rodar `ruff format --check .`, `ruff check .` e `pytest` em `backend/`

## 5. Documentação

- [x] 5.1 Passar o PRD-01 à situação **implementado** em `docs/prds/index.md` e acrescentar
      esse sexto valor à linha do vocabulário das situações
- [x] 5.2 Conferir que nada mais em `docs/` muda: não houve decisão nova de produto, o
      rótulo de ciclo ficou como parâmetro de operação, e a relação entre documentos não
      mudou — logo, documentos 09 e 99, PRDs e `nav` do `mkdocs.yml` seguem como estão
- [x] 5.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR
