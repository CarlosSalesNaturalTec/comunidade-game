## 1. Modelo de dados e migração

- [x] 1.1 Criar o modelo `Poder` com nome, descrição, natureza — `de_guerreiro` ou
      `derivado_do_aporte` — e vigência — `vigente` ou `ciclo_futuro` —, com `ComAutoria`
      (`RF-01-62`, `RN-01-43`, design — decisões).
- [x] 1.2 Criar o modelo `Trilha` com nome, objetivo, área do conhecimento, poder, Mestre autor e
      situação — `rascunho` ou `publicada` —, **sem coluna de comunidade** (`RF-01-20`,
      `RN-01-42`, `RF-09-04`, design — decisões).
- [x] 1.3 Criar o modelo `Missao` com trilha, posição, nível de dificuldade, a declaração de
      obrigatória ou opcional e `e_sondagem` (`RF-01-20`, documento 99 §6 invariantes 2 e 18).
- [x] 1.4 Criar o modelo `Atividade` com missão, modalidade e formato como enumerações fechadas,
      natureza como `String` e a produção esperada (`RF-01-20`, 11 §4, documento 99 §6
      invariante 19, design — decisões).
- [x] 1.5 Escrever a quinta migração Alembic criando `poder`, `trilha`, `missao` e `atividade`,
      sem tocar as tabelas das fatias anteriores, e conferir que ela sobe e desce.
- [x] 1.6 Declarar na mesma migração a unicidade de `(trilha_id, posicao)` como
      `DEFERRABLE INITIALLY IMMEDIATE`, com o comentário apontando a reordenação de `RF-09-02`
      como motivo (design — decisões).
- [x] 1.7 Declarar na mesma migração o índice único parcial que admite **uma** sondagem por
      trilha (`RF-01-20`, documento 99 §6 invariante 5, design — decisões).

## 2. Catálogo de poderes

- [x] 2.1 Acrescentar `Operacao.catalogo_de_poderes` ao vocabulário da matriz **sem** incluí-la em
      papel algum: o Admin já a alcança por `Operacao.tudo`, e negar por padrão é o que recusa os
      demais (`RF-01-62`, `RF-01-16`).
- [x] 2.2 Implementar a regra de cadastro, alteração e desativação de poder, gravando autoria e
      recusando com 422 o cadastro sem nome (`RF-01-62`, `RF-01-03`).
- [x] 2.3 Implementar a recusa do vínculo de trilha a poder de natureza `derivado_do_aporte`
      (`RN-01-43`, documento 99 §6 invariante 21).
- [x] 2.4 Verificar: Admin cadastra e a autoria fica gravada com fuso; Mestre recebe 403; poder
      sem nome recebe 422; trilha em poder derivado do aporte recebe 422; poder de ciclo futuro
      fica no catálogo, distinguível, e aceita vínculo de trilha (`RF-01-62`, `RN-01-43`).

## 3. Trilha

- [x] 3.1 Implementar a criação de trilha exigindo poder do catálogo e Mestre autor, com autoria,
      data e hora com fuso, e recusando com 422 a trilha sem poder (`RF-01-20`, `RF-01-03`).
- [x] 3.2 Implementar a conferência de **posse** como função própria de regra, aplicada depois da
      matriz: aceita o Mestre autor e o Admin, recusa outro Mestre com 403 (`RF-01-16`,
      PRD-01 §4, design — decisões).
- [x] 3.3 Implementar a situação da trilha e a leitura que esconde o rascunho de quem não é o
      Mestre autor nem Admin (`RF-01-20`, `RF-09-04`).
- [x] 3.4 Verificar: trilha sem poder recebe 422; Mestre que não é autor recebe 403; Admin alcança
      trilha de que não é autor; rascunho não aparece a terceiros e aparece ao autor (`RF-01-20`,
      `RF-01-16`).
- [x] 3.5 Verificar que a tabela `trilha` **não tem** coluna de comunidade e que a consulta de
      trilhas não exige nem aplica filtro por comunidade, respondendo sem 422 quando ele não vem
      (`RN-01-42`, `RF-01-18`, design — decisões).

## 4. Missão

- [x] 4.1 Implementar a criação de missão exigindo trilha, posição, nível de dificuldade e a
      declaração de obrigatória ou opcional (`RF-01-20`, documento 99 §6 invariantes 2 e 18).
- [x] 4.2 Implementar a regra da sondagem: no máximo uma por trilha e sempre na primeira posição,
      sem exigir que a trilha em rascunho já a tenha (`RF-01-20`, documento 99 §6 invariante 5).
- [x] 4.3 Verificar: missão sem trilha recebe 422; missão sem a declaração de obrigatória ou
      opcional recebe 422; segunda sondagem na mesma trilha recebe 422; sondagem fora da primeira
      posição recebe 422; trilha em rascunho sem sondagem é aceita (`RF-01-20`).
- [x] 4.4 Verificar que nenhum caminho do núcleo deriva a dificuldade da missão da idade do
      Guerreiro(a) (documento 99 §6 invariante 2).

## 5. Atividade

- [x] 5.1 Implementar a criação de atividade exigindo missão, com a escrita restrita ao Mestre
      autor da trilha e ao Admin pela mesma conferência de posse da tarefa 3.2 (`RF-01-20`,
      `RF-01-16`).
- [x] 5.2 Implementar os três eixos: modalidade e formato fechados nos valores do documento 11 §4
      e natureza aberta, normalizada antes de gravar (`RF-01-20`, `RF-09-70`, design — decisões
      e riscos).
- [x] 5.3 Implementar a exigência de produção declarada, recusando com 422 a atividade sem ela
      (`RF-01-20`, documento 99 §6 invariante 19).
- [x] 5.4 Verificar: atividade sem missão, sem modalidade, sem formato, com modalidade fora dos
      valores previstos e sem produção declarada recebem 422; natureza fora da lista do Ciclo 01
      é aceita; a combinação livre dos três eixos é aceita; Mestre que não é autor recebe 403
      (`RF-01-20`, `RF-09-70`, `RF-01-16`).

## 6. Esteira do backend

- [x] 6.1 Rodar `ruff format --check`, `ruff check` e `pytest` com a cobertura publicada no log,
      sem limiar que bloqueie. A fatia não cria pasta de topo, então não nasce workflow novo:
      `backend-ci.yml` já cobre `backend/**`.

## 7. Documentação

- [x] 7.1 Conferir que as duas decisões desta fatia continuam coerentes ao fim da implementação —
      documento 02 §§2 e 3, documento 09 e PRD-01 §§6, 7, 13 e 15, já gravados antes das specs.
- [x] 7.2 Atualizar `docs/prds/index.md` se a situação do PRD-01 mudar ao fim desta fatia.
- [x] 7.3 Rodar `npm run fix`, `npm run lint` e `mkdocs build --strict` antes de abrir o PR.
