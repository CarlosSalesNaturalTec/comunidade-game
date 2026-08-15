## 1. Domínio do estado

- [x] 1.1 Ampliar `EstadoDaSerie` com `interrompida` e `encerrada`, substituindo a docstring
      que apontava esta entrega como posterior (`RF-08-10`, `RF-08-11`, PRD-08 §§3.1, 8).
- [x] 1.2 Conferir que nenhuma migração do Alembic é necessária: a coluna `estado` é
      `VARCHAR(16)` sem CHECK constraint, e `Base.metadata.create_all()` dos testes segue
      criando a tabela igual (design — sem migração do Alembic).

## 2. Apuração do estado

- [x] 2.1 Escrever a função de derivação do estado a partir de `ultima_medicao_valida_em`,
      `aberta_em`, `cadencia`, `vigencia_fim` do desafio e do momento da apuração, com a ordem
      `encerrada` → `interrompida` → `ativa` (`RF-08-10`, `RF-08-11`, PRD-08 §8).
- [x] 2.2 Contar os períodos com `periodo_de_cadencia`, sem subtrair datas: interrompida
      quando `P(agora)` for ao menos o terceiro período a partir de `P(âncora)`, sendo a
      âncora a última medição válida ou, na falta dela, a data de abertura (`RN-08-07`,
      design — a régua dos períodos).
- [x] 2.3 Escrever a persistência do espelho: gravar `estado` apenas quando o derivado
      divergir do gravado, e nunca ler a coluna como fonte (design — o estado é derivado).
- [x] 2.4 Testar a régua nas três cadências — diária, semanal e mensal —, cobrindo um período
      vazio (segue `ativa`) e dois períodos vazios (`interrompida`) (`RN-08-07`).
- [x] 2.5 Testar que a série sem nenhum registro conta os períodos a partir da data de
      abertura (`RF-08-10`).
- [x] 2.6 Testar que `encerrada` prevalece sobre `interrompida` quando as duas condições
      valem ao mesmo tempo, e que série encerrada não retoma (PRD-08 §§3.1, 8).
- [x] 2.7 Testar que uma leitura sem transição não escreve, e que a leitura no instante da
      transição grava o espelho uma única vez (design — guarda de divergência).

## 3. Gravação do registro

- [x] 3.1 Passar `ultima_medicao_valida_em` a receber o maior entre o valor gravado e a data
      da medição, em vez da atribuição incondicional de hoje (PRD-08 §8).
- [x] 3.2 Testar que uma medição mais antiga enviada depois de uma mais recente é gravada e
      **não** move o campo para trás, e que a mais recente o avança (PRD-08 §8).
- [x] 3.3 Conferir que o caminho de crédito não consulta `estado` em nenhum ponto, de modo que
      o registro que retoma credita como qualquer outro (`RF-08-11`, `RN-08-05`).
- [x] 3.4 Testar que o registro gravado numa série `interrompida` credita os pontos dele e
      devolve a série a `ativa` (`RF-08-11`, `RN-08-05`).
- [x] 3.5 Testar que a retomada não recupera os pontos dos períodos parados (`RF-08-11`,
      `RN-08-08`).
- [x] 3.6 Testar que a interrupção não estorna ponto algum já creditado (`RN-08-08`).

## 4. Consulta das séries do Guerreiro(a)

- [x] 4.1 Escrever a consulta que devolve as séries do Guerreiro(a) da sessão com desafio,
      local, cadência, estado derivado e a soma dos pontos creditados pelos registros válidos
      de cada uma (`RF-08-17`, PRD-08 §9).
- [x] 4.2 Expor `GET /v1/series-de-coleta/minhas`, sob chave de aplicação e sessão de
      Guerreiro(a), recusando com **403** persona de outro papel (`RF-08-17`).
- [x] 4.3 Testar que a consulta devolve só as séries do Guerreiro(a) da sessão, mesmo havendo
      séries de outros coletores no mesmo desafio e local (`RN-08-04`, `RF-08-17`).
- [x] 4.4 Testar que a consulta apresenta como `interrompida` a série que passou dois períodos
      sem registro, sem que nenhuma escrita tenha ocorrido desde a última medição — é o
      critério de aceite do PRD-08 §12 (`RF-08-10`, `RF-08-17`).
- [x] 4.5 Testar o critério de aceite do PRD-08 §12 de ponta a ponta: série sem registro por
      dois períodos aparece `interrompida` e para de creditar; o registro seguinte a devolve
      para `ativa` (`RF-08-10`, `RF-08-11`).

## 5. Fechamento

- [x] 5.1 Rodar `ruff format --check .`, `ruff check .` e `pytest` no `backend/`, com as três
      passando.
- [x] 5.2 Conferir os invariantes do documento 99 §6 que este recorte toca: guarda permanente
      do dado de território com o coletor identificado, e nenhum ponto creditado pelo jogo.
- [x] 5.3 Documentação: nada a alterar em `docs/` — as decisões desta change são interpretação
      de documento 02 §1, `RN-08-05` e PRD-08 §8, sem regra nova, sem linha a mover no
      documento 09, sem mudança de situação em `docs/prds/index.md` e sem arquivo novo na
      `nav` do `mkdocs.yml`. Rodar mesmo assim `npm run fix`, `npm run lint` e
      `mkdocs build --strict` antes de abrir o PR, confirmando que seguem verdes.
