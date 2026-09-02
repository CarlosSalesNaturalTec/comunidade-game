## 1. A conclusão do desafio extra no núcleo

- [x] 1.1 Criar `ConclusaoDeDesafioExtra` em `backend/src/nucleo/desafios_extras/modelo.py` —
      desafio, guerreiro, `ComMomentoDoFato`, `recompensa_entregue`,
      `pontos_extras_creditados` —, com `UniqueConstraint(desafio_id, guerreiro_id)` e os
      `event.listen` de `before_update`/`before_delete` que a tornam somente inserção, no padrão
      de `ponto_extra.modelo`. Verificar pelo modelo importado em `python -c` e pelos testes de
      1.4 (`RF-14-42`, design — decisões 1 e 2).
- [x] 1.2 Escrever a migração Alembic aditiva da tabela nova, com o índice único e os gatilhos
      de imutabilidade; conferir que `alembic upgrade head` e o `downgrade` correspondente
      rodam limpos sobre o banco de teste (design — Migration Plan).
- [x] 1.3 Acrescentar `registrar_conclusao_de_desafio_extra()` a
      `backend/src/nucleo/desafios_extras/regra.py`, recusando desafio não publicado e segunda
      conclusão do mesmo Guerreiro(a); e derivar `quantidade_restante` como a disponível menos
      as conclusões com recompensa entregue, com piso em zero, no lugar do valor fixo que a
      fatia 1 devolvia em `rotas._saida` (`RF-14-37`, `RF-14-42`, design — decisões 2 e 3).
- [x] 1.4 Cobrir a entidade e a regra em `backend/tests/test_conclusao_de_desafio_extra.py`:
      conclusão guarda quem, quando e quanto rendeu; segunda conclusão do mesmo Guerreiro(a)
      recusada; conclusão de desafio não publicado recusada; `UPDATE` e `DELETE` recusados
      também fora do ORM; quantidade restante descontada e nunca negativa, inclusive na leitura
      de `GET /v1/eu/desafios-extras` (`RF-14-37`, `RF-14-42`).

## 2. A leitura da efetividade

- [x] 2.1 Criar o módulo `backend/src/nucleo/efetividade_do_apoio/` (`__init__.py`, `regra.py`,
      `rotas.py`), sem modelo próprio, e registrar o roteador em
      `backend/src/nucleo/principal.py` com `incluir_roteador_de_dados` (design — decisão 4).
- [x] 2.2 Em `regra.py`, montar os desafios do proponente separados entre propostos, publicados
      e concluídos, com a contagem de conclusões, a trilha e o período — data da primeira e da
      última conclusão (`RF-14-41`, `RF-14-42`).
- [x] 2.3 Em `regra.py`, resolver os concluintes exibíveis filtrando pela expressão de
      `consentimentos.regra.condicao_de_autorizacao_vigente` na própria consulta, devolvendo
      avatar e nick apenas de quem passa e contando os demais só no agregado; e podar o desafio
      `direcionado` antes de qualquer consulta de concluinte, devolvendo somente
      `houve_conclusao` (`RF-14-45`, `RF-14-46`, `RF-14-47`, `RN-14-22`, design — decisões 6 e
      7).
- [x] 2.4 Em `regra.py`, montar as moedas aportadas com o que custearam — necessidade ou
      `MissaoDoApoiador` da declaração de origem, `DesafioExtra` que o aporte lastreia, ou
      aporte livre —, somando só aporte homologado e sem nenhum valor em reais (`RF-14-43`,
      `RN-14-07`, `RN-14-09`, design — decisão 9).
- [x] 2.5 Em `regra.py`, montar a cobertura de ODS nos dois níveis: as etiquetas herdadas por
      desafio, de `resolver_etiquetas_da_missao` ou `cobertura_por_trilha`, e a agregação por
      Comunidade Virtual — do `VinculoJogador` vigente na data do fato, por
      `comunidades.regra.resolver_vinculo_na_data` — com o rótulo de
      `configuracao.ciclo_rotulo` (`RF-14-44`, `RN-14-28`, design — decisão 8).
- [x] 2.6 Em `rotas.py`, expor `GET /v1/eu/desafios-extras/efetividade`, restrita ao Apoiador em
      sessão, sem identificador de outro Apoiador no caminho ou em parâmetro, devolvendo o
      painel montado em 2.2 a 2.5 (`RF-14-40`, PRD-14 §9).
- [x] 2.7 Cobrir a rota e a regra em `backend/tests/test_efetividade_do_apoio.py`: painel vivo
      que já contabiliza a conclusão do mesmo dia e ausência de qualquer rota de relatório
      fechado; desafios separados por situação e nenhum desafio de outro proponente; contagem,
      trilha e período, e contagem zero sem período; aporte pendente fora do painel e nenhum
      valor em reais; cobertura por comunidade e ciclo, etiquetas herdadas do desafio sem
      conclusão, e nenhuma cobertura ligada a Guerreiro(a); avatar e nick só com divulgação
      autorizada, contagem-só sem ela e sumiço do avatar após a revogação; direcionado com
      apenas `houve_conclusao`, concluído ou não; outro papel recusado (`RF-14-40` a
      `RF-14-47`, `RN-14-21`, `RN-14-22`, `RN-14-28`).

## 3. A área de efetividade na App 08

- [x] 3.1 Criar `apps/app-08-apoiador/src/efetividade/api.ts` com o cliente de
      `GET /v1/eu/desafios-extras/efetividade`, no padrão dos demais `api.ts` da aplicação
      (`RF-14-40`).
- [x] 3.2 Criar `apps/app-08-apoiador/src/efetividade/TelaDeEfetividade.tsx` com os desafios por
      situação, a contagem com trilha e período, as moedas com o que custearam, a cobertura de
      ODS, a declaração de que o painel é vivo e não há relatório fechado, e o estado de quem
      ainda não propôs nenhum desafio (`RF-14-40` a `RF-14-44`, `RN-14-21`).
- [x] 3.3 Exibir os concluintes só por avatar e nick, o restante apenas como contagem, e o
      direcionado apenas como concluído ou não, sem nenhum campo de mensagem, contato ou ação
      que aproxime o Apoiador da criança (`RF-14-45`, `RF-14-46`, `RF-14-47`, `RN-14-20`).
- [x] 3.4 Ligar a área "Efetividade" na navegação de `apps/app-08-apoiador/src/App.tsx`, no
      padrão das demais áreas (`RF-14-40`).
- [x] 3.5 Cobrir a tela em `apps/app-08-apoiador/src/efetividade/efetividade.test.tsx`: a área
      reúne desafios, moedas e ODS; declara que o painel é vivo; orienta quem não propôs nada;
      mostra avatar e nick só de quem autorizou e conta os demais; mostra o direcionado apenas
      como concluído; e nenhuma tela oferece campo de mensagem ou contato (`RF-14-40` a
      `RF-14-47`).

## 4. Documentação

- [x] 4.1 Marcar a fatia 6 do PRD-14 como `implementado` em
      `openspec/cronograma-de-fatias.md`, trocando o recorte previsto pelo slug
      `efetividade-do-apoio`, e anotar no bloco do PRD-09 que o ato de registrar a conclusão do
      desafio extra — cuja entidade esta fatia criou só para leitura — ainda não tem fatia.
      Nenhuma decisão de produto nova foi tomada: `docs/`, `docs/prds/index.md`, o documento 99
      e a `nav` do `mkdocs.yml` seguem como estão.
