## Context

Ver `proposal.md` — Why. O que o núcleo já tem, e que esta fatia usa sem alterar:
`desafios_extras` (fatia 1: modelo, proposta e leitura do proponente), `aportes` e
`poder_sustentador` (fatia 4), `missoes_do_apoiador` e `selos_do_apoiador` (fatia 5),
`consentimentos.regra.autorizacao_de_divulgacao_vigente`, `ods.regra`
(`resolver_etiquetas_da_missao`, `cobertura_por_trilha`) e
`comunidades.regra.resolver_vinculo_na_data`.

Três restrições do núcleo moldam o desenho e não se contornam aqui:

- **`Trilha` não tem comunidade** (`RN-01-42`): a trilha é bem comum. A Comunidade Virtual da
  agregação só pode vir de quem concluiu, pelo `VinculoJogador` vigente na data do fato.
- **Ciclo não é entidade** (`fim-de-ciclo`): é rótulo declarado na implantação, em
  `configuracao.ciclo_rotulo`, do mesmo jeito que a cobertura de ODS da trilha já o carrega.
- **Nada registra a conclusão de um `DesafioExtra`** hoje. O ato de registrá-la — atribuir a
  recompensa e creditar os pontos extras — é do PRD-09 e ainda não tem fatia. Decisão do
  fundador, 2026-09-02: esta fatia cria a entidade e a lê; o ato fica para o PRD-09.

## Goals / Non-Goals

**Goals:**

- Uma leitura só, `GET /v1/eu/desafios-extras/efetividade`, que responde tudo que o painel
  precisa, sem o front-end cruzar rotas.
- A poda do dado de criança acontece **na consulta**, não na serialização: o que não pode sair
  não chega a ser lido.

**Non-Goals:**

- Nenhuma rota de escrita de conclusão nesta fatia; nenhuma baixa de reserva na entrega
  (`RF-07-39`, `RF-07-40`).
- Nenhum cache, materialização ou agregado persistido.

## Decisions

1. **A conclusão nasce em `desafios_extras/modelo.py`, como `ConclusaoDeDesafioExtra`** —
   desafio, guerreiro, `data_do_fato` (`ComMomentoDoFato`), `recompensa_entregue` e
   `pontos_extras_creditados`. É do agregado `DesafioExtra`, não do painel: quem a escreverá é
   o PRD-09, e o painel só a lê. _Alternativa descartada:_ módulo próprio, que separaria a
   entidade das guardas que a protegem.
2. **A entidade nasce sem rota, com as guardas já postas.** `regra.registrar_conclusao_de_
   desafio_extra()` confere desafio publicado e ausência de conclusão anterior do mesmo
   Guerreiro(a); `UniqueConstraint(desafio, guerreiro)` sustenta o mesmo fora do ORM, e os
   `event.listen` de `before_update`/`before_delete` fazem dela somente inserção, no padrão de
   `PontoExtra`. É o mesmo desenho da fatia 1, que criou as situações deixando as transições
   para fora dela. _Alternativa descartada:_ deixar as guardas para a fatia do PRD-09, o que
   publicaria uma tabela sem regra.
3. **A quantidade restante passa a ser derivada** — disponível menos as conclusões com
   recompensa entregue, com piso em zero —, na função que a fatia 1 já deixou em
   `desafios_extras.regra`. Nenhuma coluna de contador. _Alternativa descartada:_ contador
   materializado no `DesafioExtra`, que exigiria transação de duas escritas e envelheceria.
4. **A leitura do painel vive em `backend/src/nucleo/efetividade_do_apoio/`**, com `regra.py` e
   `rotas.py` e nenhum modelo. É leitura agregada que cruza quatro domínios — desafios,
   aportes, ODS e consentimento —, e não cabe em nenhum deles. _Alternativa descartada:_
   estender `desafios_extras/rotas.py`, que passaria a importar aportes e consentimento.
5. **Painel vivo = consulta sob demanda.** Nada é materializado, o que faz a revogação da
   autorização de divulgação surtir efeito na leitura seguinte sem nenhum expurgo. É também o
   que garante `RN-14-21` por construção: não há artefato fechado para existir.
6. **O direcionado é podado antes da leitura.** Desafio de modalidade `direcionado` não passa
   pela consulta de concluintes: a regra devolve apenas `houve_conclusao`, e nem avatar nem
   nick nem `VinculoJogador` chegam a ser consultados. _Alternativa descartada:_ ler tudo e
   omitir na saída, que deixa o dado a um descuido de serialização de distância (`RF-14-47`).
7. **Avatar e nick saem por filtro na consulta**, com
   `consentimentos.regra.condicao_de_autorizacao_vigente` — a mesma expressão que as
   superfícies públicas já usam — e não por `if` depois de carregar a `Persona`. Quem não passa
   no filtro entra só na contagem, que é contada à parte (`RF-14-45`, `RF-14-46`).
8. **A cobertura de ODS sai em dois níveis.** Por desafio: as etiquetas herdadas, de
   `resolver_etiquetas_da_missao` quando há missão declarada e de `cobertura_por_trilha` quando
   não há — disponíveis mesmo sem conclusão. Agregada: por Comunidade Virtual, que vem do
   `VinculoJogador` de quem concluiu na data do fato, com o rótulo do ciclo de
   `configuracao.ciclo_rotulo`. É a única leitura possível dado que a trilha não tem comunidade
   (`RF-14-44`, `RN-14-28`).
9. **"O que as moedas custearam"** sai do que o núcleo já liga ao aporte homologado: a
   necessidade ou a `MissaoDoApoiador` que a declaração de origem apontou
   (`AporteDeclarado.origem_da_escolha`, `aula_id`/`tipo_de_recurso_id`,
   `missao_do_apoiador_id`) e o `DesafioExtra` cujo `aporte_id` aponta para ele. Aporte sem
   nenhum dos dois sai como aporte livre. Nada é inferido além disso.
10. **Nada entra no livro-razão**: a fatia é leitura pura, sem operação com custo, sem escrita
    de território e sem série temporal.

## Risks / Trade-offs

- **O painel nasce com contagem zero** até a fatia do PRD-09 que registra a conclusão chegar →
  é o preço da decisão 1, e a tela declara que nada foi concluído ainda em vez de exibir painel
  vazio sem explicação. Os oito `RF` ficam verificáveis desde já, porque os testes semeiam a
  conclusão pela função de regra.
- **A agregação por comunidade só existe onde há conclusão** → desafio publicado sem conclusão
  aparece com as etiquetas herdadas e fora da agregação, o que a spec já declara.
- **Consulta que cruza quatro domínios pode ficar cara** com muitos desafios → a leitura é por
  proponente, cujo volume é pequeno no Ciclo 01; nenhum índice novo além do da unicidade da
  conclusão. Se o volume crescer, o passo seguinte é índice, não materialização.
- **Entidade publicada sem quem a escreva** é superfície ociosa até o PRD-09 → mitigada pelas
  guardas da decisão 2, que impedem a tabela de aceitar linha inválida por qualquer via.

## Migration Plan

Uma migração Alembic aditiva: cria `conclusao_de_desafio_extra` com o índice único e os
gatilhos de imutabilidade, no padrão de `ponto_extra`. Não altera tabela existente, não move
dado e o `downgrade` derruba a tabela e os gatilhos. Rota nova, sem quebra de contrato: o único
efeito sobre leitura existente é o valor de `quantidade_restante` em
`GET /v1/eu/desafios-extras`, que passa a descontar conclusões — sem conclusão registrada, o
valor é o de hoje.
