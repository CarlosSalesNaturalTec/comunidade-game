## 1. Núcleo — a atividade fora de trilha

- [x] 1.1 Em `backend/src/nucleo/trilhas/modelo.py`, tornar `Atividade.missao_id` opcional,
      acrescentar `poder_id` com chave estrangeira para `poder` e o `CheckConstraint` que exige
      missão **ou** poder, nunca os dois nem nenhum (`RF-02-29`; design — decisões 1 e 2).
      Verificação: `uv run pytest tests/test_atividade.py -x` segue verde.
- [x] 1.2 Criar a revisão Alembic correspondente em `backend/alembic/versions/` (design —
      Migration Plan). Verificação: `alembic upgrade head` e `alembic downgrade -1` correm sem
      erro sobre o banco de teste.
- [x] 1.3 Criar `backend/src/nucleo/atividades/regra.py` com `cadastrar_atividade_avulsa`:
      exige Admin (403 aos demais), exige título, modalidade, formato, natureza, produção
      esperada e poder (422 indicando o campo), fecha modalidade e formato nos valores do
      documento 11 §4, recusa poder inexistente e recusa a declaração simultânea de missão
      (`RF-02-29`). Verificação: `uv run pytest tests/test_atividade_avulsa.py -x`.
- [x] 1.4 Criar `backend/src/nucleo/atividades/rotas.py` com `POST /v1/atividades` (PRD-02 §9) e
      registrá-la em `principal.py` como rota de dados (`RF-02-29`). Verificação:
      `uv run pytest tests/test_atividade_avulsa_rota.py -x`.
- [x] 1.5 Garantir em `trilhas.regra.criar_atividade` que a atividade de trilha segue exigindo a
      missão e nunca declara poder (`RF-02-29`). Verificação: coberto pela tarefa 1.3.

## 2. Núcleo — lançamento e pontuação da atividade avulsa

- [x] 2.1 Em `backend/src/nucleo/pontuacao/regra.py`, `creditar_pontuacao_do_resultado` passa a
      receber **trilha ou poder**: com poder, credita o ponto regular pelo motor do documento 11
      §5 e não avalia nível nem concede o badge de valores e causas (`RF-02-29`; design —
      decisão 4). Verificação: `uv run pytest tests/test_pontuacao.py -x`.
- [x] 2.2 Em `backend/src/nucleo/resultados/regra.py`, `registrar_resultado` desvia pela ausência
      de missão: pula a conferência de posse da trilha, exige Admin (403 ao Mestre) e credita
      pelo poder da atividade (`RF-02-29`, `RF-02-33`). Verificação:
      `uv run pytest tests/test_resultado.py -x`.

## 3. App 03 — recursos declarados no agendamento

- [x] 3.1 Em `apps/app-03-gestao/src/agenda/api.ts`, levar `recursos_declarados` no
      agendamento e `recursos_faltantes` na leitura da aula (`RF-02-31`, `RF-02-32`).
- [x] 3.2 Em `apps/app-03-gestao/src/agenda/FormularioDeAgendamento.tsx`, acrescentar os pares de
      tipo de recurso e quantidade — acrescentar, remover, recusar quantidade não positiva no
      próprio campo — lendo o catálogo por `listarTiposDeRecurso` (`RF-02-31`). Verificação:
      cenários da tarefa 6.1.

## 4. App 03 — área Recursos

- [x] 4.1 Criar `apps/app-03-gestao/src/recursos/api.ts` com o registro do aporte por
      `POST /v1/aportes` (multipart, com comprovante) e a leitura de
      `GET /v1/vitrine/necessidades` (`RF-02-57`, `RF-02-58`; design — decisão 5).
- [x] 4.2 Criar `RegistroDeAporte.tsx`: provedor entre os adultos cadastrados, tipo, quantidade,
      ponto de apoio da comunidade escolhida, data, forma e comprovante — exigido quando o tipo o
      exige —, apresentando no campo as recusas do núcleo e o valor em moedas devolvido, nunca em
      reais (`RF-02-57`, `RN-02-19`).
- [x] 4.3 Criar `ListaDeNecessidades.tsx`: tipo, quantidade que falta, valor em moedas — ausente
      quando não há vigência —, comunidade, ponto de apoio, data e horário da aula, em lista
      densa, com texto próprio para a lista vazia (`RF-02-58`).
- [x] 4.4 Criar `TelaDeRecursos.tsx`, que relê necessidades e agenda depois de cada aporte
      registrado e apresenta a aula confirmada e a reserva efetivada, sem ato manual de
      confirmação (`RF-02-67`), e ligá-la à navegação do `App.tsx`.

## 5. App 03 — área Atividades

- [x] 5.1 Criar `apps/app-03-gestao/src/atividades/api.ts` e `FormularioDeAtividadeAvulsa.tsx`:
      título, descrição, modalidade e formato em escolha fechada, natureza, produção esperada e
      poder do catálogo — sem campo de pontuação e sem campo de recurso (`RF-02-29`).
- [x] 5.2 Criar `TelaDeAtividades.tsx` com a lista do que foi cadastrado e ligá-la à navegação do
      `App.tsx`, oferecida só ao Admin (`RF-02-29`).

## 6. Testes

- [x] 6.1 `apps/app-03-gestao/src/agenda/agenda.test.tsx`: declarar dois recursos e agendar,
      recusa de quantidade zero no campo, e a aula devolvida como pendente de lastro
      (`RF-02-31`, `RF-02-32`).
- [x] 6.2 `apps/app-03-gestao/src/recursos/recursos.test.tsx`: registro do aporte com
      comprovante, bloqueio do tipo que o exige sem ele, recusa do aporte em causa própria,
      ausência de reais na tela, a necessidade com todos os campos, o tipo sem vigência sem
      valor, a lista vazia com texto, o aporte que fecha a falta confirmando a aula e o aporte
      parcial que mantém a necessidade abatida (`RF-02-57`, `RF-02-58`, `RF-02-67`).
- [x] 6.3 `apps/app-03-gestao/src/atividades/atividades.test.tsx`: cadastro da avulsa, ausência
      dos campos de pontuação e de recurso, recusa sem poder no campo e o caminho não oferecido a
      quem não é Admin (`RF-02-29`).
- [x] 6.4 `backend/tests/test_atividade_avulsa.py` e `test_atividade_avulsa_rota.py`: cadastro
      pelo Admin, 403 ao Mestre, 422 por campo em falta, modalidade fora dos valores, poder
      inexistente, missão e poder juntos, e a atividade de trilha que segue exigindo missão
      (`RF-02-29`).
- [x] 6.5 `backend/tests/test_resultado.py` e `test_pontuacao.py`: o Admin lança a avulsa e o
      ponto regular pousa no poder, o Mestre recebe 403, a trilha do Guerreiro(a) não se move e
      nenhum nível é certificado pelo lançamento (`RF-02-29`, `RF-02-33`).

## 7. Documentação

- [x] 7.1 Gravar as duas decisões novas: no documento 11 §5, que a atividade avulsa declara o
      **poder** em que o ponto regular pousa; no documento 09 §1, a linha "Pontuação da atividade
      cadastrada" acrescida disso e a linha nova sobre recurso ser declaração da aula. Corrigir no
      PRD-02 o enunciado do `RF-02-29` e a linha da §3.1, retirando "recursos necessários" do
      cadastro da atividade, e registrar as duas na §13. Marcar a fatia 11 como implementada em
      `openspec/cronograma-de-fatias.md`, com o recorte ampliado por `RF-02-31` e `RF-02-32`.
      Nenhum arquivo novo em `docs/`, logo nada muda na `nav` do `mkdocs.yml`;
      `docs/prds/index.md` só muda se a situação do PRD-02 mudar.
