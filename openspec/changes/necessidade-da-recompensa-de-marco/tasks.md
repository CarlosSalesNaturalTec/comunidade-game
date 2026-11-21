# Tasks

## 1. Núcleo

- [ ] 1.1 Migração Alembic: `comunidade_virtual_id` e `trilha_id` anuláveis, com chave
      estrangeira, em `aporte`, `aporte_declarado` e `missao_do_apoiador`;
      `missao_do_apoiador.aula_id` anulável, com `CheckConstraint` de aula **ou** comunidade +
      trilha; modelos atualizados (`RF-07-28`, `RF-02-102`, `RF-14-25`, design — decisões 3, 5).
- [ ] 1.2 `necessidades/regra.py`: `NecessidadeDeRecurso` com `especie`, `trilha_id`,
      `trilha_nome` e campos da aula opcionais; derivação da recompensa — ponto da aula
      anterior, trilhas com atividade em aula não cancelada, vínculos vigentes menos entregas,
      ordem pela atividade mais antiga —; saída da aula antes da recompensa; filtro do Mestre
      pelas comunidades dele (`RF-07-54`, `RF-07-18`, `RF-07-27`, `RF-09-56`, design — decisões
      1, 2, 4).
- [ ] 1.3 `necessidades/rotas.py`: a saída das duas rotas com os campos novos (`RF-07-27`,
      `RF-03-47`, `RF-09-56`).
- [ ] 1.4 `aportes/regra.py` e `aportes/rotas.py`: absorção com `comunidade_virtual_id` e
      `trilha_id`, recusando 422 com aula junto, ponto diferente do da aula anterior, trilha sem
      recompensa do tipo ou aporte que não é absorção; declaração de origem necessidade com aula
      **ou** comunidade + trilha (`RF-07-28`, `RF-09-57`, `RF-14-25`, design — decisão 6).
- [ ] 1.5 `missoes_do_apoiador/regra.py` e `rotas.py`: publicação pela necessidade da
      recompensa, conferida pela chave da espécie; `tem_necessidade_por_tras` com a mesma chave
      (`RF-02-102`, `RF-02-103`, `RN-14-31`, design — decisão 7).

## 2. Núcleo — testes

- [ ] 2.1 `tests/test_necessidade_da_recompensa_de_marco.py`: falta pelos vínculos vigentes
      menos entregas; duas recompensas do mesmo tipo somam; vínculo encerrado não conta;
      recompensa coberta some; trilha sem atividade, aula passada e aula cancelada; ponto da
      aula anterior e comunidade sem aula anterior; ordem entre trilhas; campos publicados, sem
      reais nem pessoa; filtro do Mestre (`RF-07-54`, `RF-07-18`, `RF-07-27`, `RF-09-56`).
- [ ] 2.2 No mesmo arquivo: absorção que abate, ponto diferente recusado, aula e trilha juntas
      recusadas, aporte da gestão com trilha recusado; missão pela necessidade da recompensa,
      recusa sem necessidade e saída da leitura pública quando a falta fecha; declaração pela
      recompensa pendente e declaração sem aula nem trilha recusada (`RF-07-28`, `RF-02-102`,
      `RF-02-103`, `RF-14-25`).
- [ ] 2.3 Ajuste dos testes existentes de necessidade, missão e aporte que leem a saída antiga
      (`RF-07-27`).

## 3. Aplicações

- [ ] 3.1 App 03: `recursos/api.ts`, `recursos/ListaDeNecessidades.tsx` e
      `recursos/TelaDeRecursos.tsx` com a trilha no lugar da aula e a chave pela espécie;
      `missoes-do-apoiador/PublicacaoDeMissao.tsx` envia comunidade e trilha; testes
      (`RF-02-58`, `RF-02-102`).
- [ ] 3.2 App 06: `necessidades/ListaDeNecessidades.tsx` e `api/leituras.ts` com a trilha no
      lugar da data; teste (`RF-03-47`).
- [ ] 3.3 App 08: `aportes/TelaDeNecessidadesEmAberto.tsx` e
      `aportes/TelaDeDeclaracaoDeAporte.tsx` com a trilha e o envio de comunidade e trilha;
      `preCadastro/TelaDePreCadastro.tsx` descreve a necessidade pela trilha; testes
      (`RF-14-24`, `RF-14-25`, `RF-14-02`).
- [ ] 3.4 App 09: `recursos/api.ts`, `recursos/ListaDeNecessidades.tsx` e
      `recursos/AbsorcaoDaNecessidade.tsx` com a trilha e o envio de comunidade e trilha, sem
      dizer que confirma aula; testes (`RF-09-56`, `RF-09-57`).

## 4. Documentação

- [ ] 4.1 Documento 04 §1, item da recompensa de marco, e a linha "Consumo do encontro e
      recompensa de marco" do documento 09: ordem pela atividade em aula mais antiga, aula não
      cancelada e comunidade sem aula anterior sem necessidade (`RF-07-54`); fatia 14 marcada
      implementada no `openspec/cronograma-de-fatias.md`, com o slug. PRDs, `docs/prds/index.md`,
      documento 99 e `mkdocs.yml` não mudam.
