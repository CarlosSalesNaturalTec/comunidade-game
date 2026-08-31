## 1. Núcleo — derivação e regra da autorização

- [x] 1.1 Em `backend/src/nucleo/consentimentos/regra.py`, derivar o **estado da autorização**
      em três valores a partir da subconsulta da decisão mais recente por responsável que já
      existe: `vigente`, `suspensa` (concessão e recusa convivendo) e `nao_autorizada`. Devolver
      junto, no estado suspenso, o responsável cuja recusa prevalece e o momento dela.
      `condicao_de_autorizacao_vigente` e seus chamadores não mudam. (`RF-13-17`, `RF-13-18`,
      `RN-13-07`, `RN-13-11`)
- [x] 1.2 Na mesma regra, montar o **histórico da autorização** de um Guerreiro(a): todas as
      decisões de `autorizacao_de_divulgacao` dos responsáveis vinculados, da mais recente à mais
      antiga, cada uma com quem decidiu, a versão do termo, a origem e o momento. Sem alcançar
      `biometria`. (`RF-13-21`, `RN-13-06`, `RN-13-10`)
- [x] 1.3 Na mesma regra, escrever `decidir_autorizacao`: guarda de vínculo vigente (403), os
      dois 409 da PRD-13 §9 — concessão com recusa mais recente de **outro** responsável,
      revogação sem concessão vigente de **nenhum** responsável — e a idempotência do reenvio
      da mesma decisão, que devolve o registro existente sem gravar. A revogação não exige que
      o próprio responsável tenha concedido antes: é assim que a divergência nasce. Grava por
      `registrar_consentimento`, com origem `propria` e o próprio responsável como quem opera.
      (`RF-13-14`, `RF-13-15`, `RN-13-05`, `RN-13-07`, `RN-13-10`)
- [x] 1.4 Acrescentar em `backend/src/nucleo/erros.py` os erros dos dois 409, com a mensagem em
      linguagem simples e, no da concessão colidente, o estado e a orientação de procurar a
      gestão. (`RF-13-17`, PRD-13 §§9, 10)

## 2. Núcleo — solicitação aberta pela suspensão

- [x] 2.1 Em `backend/src/nucleo/solicitacoes_do_responsavel/modelo.py`, acrescentar o campo
      booleano que marca a solicitação **aberta pela suspensão**, com padrão falso, e a migração
      Alembic correspondente em `backend/alembic/versions/`. A fila do Admin continua lendo o
      tipo `esclarecimento` como qualquer outro. (`RF-13-19`, design — decisão 4)
- [x] 2.2 Em `backend/src/nucleo/solicitacoes_do_responsavel/regra.py`, escrever
      `abrir_solicitacao_da_divergencia`: só quando o estado passa a `suspensa`, em nome de quem
      recusou, tipo `esclarecimento`, texto escrito pelo núcleo em linguagem simples, situação
      recebida e prazo de 7 dias; **não abre** havendo outra da divergência sem desfecho para
      aquele Guerreiro(a), e nunca levanta erro que recuse a recusa. A guarda de duplicata do
      responsável (409) permanece intocada e não alcança esta. (`RF-13-19`, `RF-13-22`,
      `RN-13-14`)
- [x] 2.3 Encadear a abertura ao ato de decidir, no mesmo commit da recusa. (`RF-13-19`)

## 3. Núcleo — rotas do responsável

- [x] 3.1 Em `backend/src/nucleo/consentimentos/rotas.py`, expor
      `GET /v1/eu/guerreiros/{id}/autorizacao` — estado, quem motivou a suspensão com data e
      hora, e o histórico —, restrita ao papel responsável pela matriz e ao vínculo vigente por
      `exigir_vinculo_do_responsavel`. (`RF-13-18`, `RF-13-21`, `RN-13-04`)
- [x] 3.2 No mesmo arquivo, expor `POST /v1/eu/guerreiros/{id}/autorizacao`, recebendo só a
      decisão e devolvendo o registro e o estado resultante; a versão do termo vem da
      configuração e nunca do corpo. (`RF-13-14`, `RF-13-15`, `RN-13-10`)

## 4. Testes do núcleo

- [x] 4.1 Em `backend/tests/test_consentimento.py`, os cenários de regra: os três estados
      (concessão de um e recusa de outro dá suspensa; recusa isolada dá não autorizada; sem
      decisão dá não autorizada; todos concederam dá vigente), a suspensa retirando do que é
      público sem apagar registro, a participação que segue apesar do estado, a idempotência do
      reenvio, a decisão contrária que sempre grava e os dois 409, inclusive quem recusou
      voltando atrás. (`RF-13-14` a `RF-13-17`, `RN-13-07` a `RN-13-11`)
- [x] 4.2 Em `backend/tests/test_consentimento_rota.py`, os cenários das duas rotas: concessão e
      revogação pelo responsável, 403 sem vínculo e para outro papel, versão do termo que não vem
      do cliente, conceder divulgação que não concede biometria, leitura com histórico ordenado,
      leitura do estado suspenso nomeando quem recusou, histórico vazio e leitura que não alcança
      biometria nem criança não vinculada. (`RF-13-14`, `RF-13-15`, `RF-13-18`, `RF-13-21`,
      `RN-13-04`, `RN-13-06`)
- [x] 4.3 Em `backend/tests/test_solicitacao_do_responsavel.py`, os cenários da divergência:
      recusa que suspende abre a solicitação; recusa isolada e concessão não abrem; segunda
      recusa com a primeira em aberto não abre outra; tratada a primeira, a suspensão nova abre a
      sua; esclarecimento do responsável não bloqueia a divergência e a divergência não bloqueia
      o pedido do responsável; e a solicitação aparecendo na fila do Admin. (`RF-13-19`,
      `RF-13-22`, `RN-13-14`)

## 5. App 07 — telas da autorização

- [x] 5.1 Criar `apps/app-07-responsaveis/src/autorizacao/api.ts` com as chamadas das duas rotas
      e os tipos do estado, de quem motivou a suspensão e do histórico. (`RF-13-18`, `RF-13-21`)
- [x] 5.2 Criar `apps/app-07-responsaveis/src/autorizacao/TelaDeAutorizacao.tsx`: a declaração do
      que a autorização libera e do que não depende dela antes de qualquer botão; conceder e
      revogar dizendo o efeito no mesmo ato; os três estados em linguagem simples, com quem
      motivou a suspensão, data e hora; a alternativa equivalente sempre que não estiver vigente;
      o histórico com quem decidiu e a versão do termo; a falha de rede que diz que a decisão não
      foi registrada; e o 409 da concessão colidente apresentado como orientação de procurar a
      gestão, sem código de erro. (`RF-13-13` a `RF-13-15`, `RF-13-18`, `RF-13-20`, `RF-13-21`,
      `RN-13-05`, `RN-13-06`, `RN-13-08` a `RN-13-10`)
- [x] 5.3 Em `apps/app-07-responsaveis/src/vinculados/TelaDeVinculados.tsx`, acrescentar a
      navegação entre evolução e autorização do vinculado escolhido, mantendo a alternância entre
      vinculados nas duas. (`RF-13-05`, `RN-13-04`)
- [x] 5.4 Criar `apps/app-07-responsaveis/src/autorizacao/autorizacao.test.tsx` com os cenários
      das telas: declaração antes do botão e ausência de decisão por finalidade; concessão e
      revogação com o efeito dito; falha de rede que não dá a decisão por tomada; alternativa
      equivalente nos dois estados não vigentes; suspensa nomeando quem recusou; concessão
      colidente virando orientação; histórico ordenado e sem caminho de editar ou apagar; e a ida
      e volta entre evolução e autorização com troca de vinculado. (`RF-13-13` a `RF-13-15`,
      `RF-13-18`, `RF-13-20`, `RF-13-21`, `RF-13-05`)

## 6. Documentação

- [x] 6.1 Gravar a decisão do fundador de 2026-08-31 — a solicitação da divergência entra na fila
      como `esclarecimento`, em nome de quem recusou, uma só enquanto estiver em aberto por
      Guerreiro(a) — no documento 09 §1, e aplicá-la no PRD-13: o enunciado do `RF-13-19` (§6.3),
      a menção na §9 e a linha na §13. Marcar a fatia 3 do PRD-13 como implementada em
      `openspec/cronograma-de-fatias.md`, com o slug da change. `docs/prds/index.md`, o documento
      99 e a `nav` do `mkdocs.yml` não mudam: nenhum arquivo nasce, nenhuma relação entre
      documentos muda e a situação do PRD-13 segue a mesma. (`RF-13-19`)
