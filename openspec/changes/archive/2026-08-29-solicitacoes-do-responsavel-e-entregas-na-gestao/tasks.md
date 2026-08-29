## 1. Núcleo — a solicitação do responsável

- [x] 1.1 Criar `backend/src/nucleo/solicitacoes_do_responsavel/modelo.py` com
      `SolicitacaoDoResponsavel` e o enum `TipoDeSolicitacaoDoResponsavel` — acesso, correção,
      exclusão e esclarecimento —, os atributos do PRD-01 §8 no vocabulário do PRD-13
      (`responsavel_id`, `guerreiro_id`, `tipo`, `texto`, `situacao`, `registrado_em`, `prazo`,
      `tratado_por_id`, `desfecho`, `tratado_em`), reusando `SituacaoDaSolicitacao` da fila, e
      índices por responsável e por Guerreiro(a) (`RF-13-22`, `RF-13-24`, `RN-13-14`; design —
      decisões 1, 2 e 5). Verificação: cenários da tarefa 4.1.
- [x] 1.2 Criar `backend/src/nucleo/solicitacoes_do_responsavel/regra.py` com
      `abrir_solicitacao` — guarda de vínculo do responsável com o Guerreiro(a) (403), guarda de
      duplicata em aberto (409), situação recebida e prazo pela constante `PRAZO_DE_AVALIACAO`
      importada de `fila.regra` —, `listar_minhas_solicitacoes`, `listar_fila_do_admin`
      (da mais antiga para a mais recente), `registrar_tratamento` (recusa segundo desfecho) e
      `esta_em_atraso` derivado (`RF-13-22`, `RF-13-24`, `RF-13-25`, `RF-02-24`, `RF-02-66`,
      `RN-13-13`, `RN-13-14`; design — decisões 3, 6 e 7). Verificação: cenários da tarefa 4.1.
- [x] 1.3 Criar os erros do módulo em `backend/src/nucleo/erros.py` no padrão dos demais:
      solicitação idêntica em aberto (409) e solicitação já tratada (`RF-13-22`, `RF-02-24`).
- [x] 1.4 Criar `backend/src/nucleo/solicitacoes_do_responsavel/rotas.py` com
      `POST /v1/solicitacoes` e `GET /v1/eu/solicitacoes`, exigindo a operação
      `solicitacoes_e_propostas` do responsável, e `GET /v1/solicitacoes-do-responsavel` e
      `POST /v1/solicitacoes-do-responsavel/{id}/tratamento`, restritas a Admin; a saída do
      envio traz protocolo e prazo e nada mais, a do responsável e a do Admin trazem a marca de
      em atraso, e a do Admin traz também o nick do responsável e o do Guerreiro(a)
      (`RF-13-22`, `RF-13-24`, `RF-13-25`, `RF-13-26`, `RF-02-23`, `RF-02-24`, `RF-02-66`;
      design — decisões 4 e 8). Verificação: cenários da tarefa 4.2.
- [x] 1.5 Registrar o roteador em `backend/src/nucleo/principal.py` e criar a migração Alembic da
      tabela `solicitacao_do_responsavel`, encadeada na última revisão (`RF-13-24`).

## 2. Núcleo — a saída da entrega

- [x] 2.1 Em `backend/src/nucleo/recompensas_de_marco/rotas.py`, acrescentar a
      `EntregaDeRecompensaSaida` o tipo de recurso, a quantidade e o identificador do lançamento
      da baixa, sem nenhum valor em moedas ou em reais (`RF-02-50`, `RF-02-51`, `RN-02-17`;
      design — decisão 9). Verificação: cenários da tarefa 4.3.

## 3. App 03 — fila do responsável e entregas confirmadas

- [x] 3.1 Em `apps/app-03-gestao/src/filas/api.ts`, acrescentar a leitura da fila
      (`GET /v1/solicitacoes-do-responsavel`) e o tratamento
      (`POST /v1/solicitacoes-do-responsavel/{id}/tratamento`), tipando protocolo, tipo,
      situação, prazo, atraso, desfecho, quem tratou e quando (`RF-02-23`, `RF-02-24`).
- [x] 3.2 Em `ListaDeFilas.tsx` e `TelaDeFilas.tsx`, acrescentar a fila das solicitações do
      responsável com protocolo, tipo, situação e prazo de 7 dias, ordenada da mais antiga para
      a mais recente, com o responsável e o Guerreiro(a) por nick e o destaque **em atraso** para
      a solicitação sem desfecho com prazo vencido, que continua tratável (`RF-02-23`,
      `RF-02-66`). Verificação: cenários da tarefa 4.4.
- [x] 3.3 Criar `apps/app-03-gestao/src/filas/TratamentoDaSolicitacaoDoResponsavel.tsx` no molde
      de `AvaliacaoDeDados`: o texto do pedido, o desfecho aceito ou recusado com o texto do que
      foi tratado, a exibição de quem tratou e quando depois do registro, e a solicitação já
      tratada apresentada em leitura, sem novo tratamento (`RF-02-24`). Verificação: cenários da
      tarefa 4.4.
- [x] 3.4 Em `apps/app-03-gestao/src/acervo/api.ts`, acrescentar a leitura das entregas
      (`GET /v1/entregas`) com os campos novos (`RF-02-50`, `RF-02-51`).
- [x] 3.5 Criar `apps/app-03-gestao/src/acervo/ListaDeEntregas.tsx` e ligá-la a `TelaDoAcervo`:
      Guerreiro(a), tipo de recurso, Mestre que entregou, ponto de apoio e data resolvidos por
      nome no mapa que a tela já monta, a baixa definitiva indicada, nenhum valor em moedas ou
      reais e nenhum caminho de confirmar, corrigir ou desfazer entrega (`RF-02-50`, `RF-02-51`,
      `RN-02-17`; design — decisão 10). Verificação: cenários da tarefa 4.5.

## 4. Testes

- [x] 4.1 Criar `backend/tests/test_solicitacao_do_responsavel.py` cobrindo a regra: abertura nos
      quatro tipos com protocolo e prazo de 7 dias, pedido de exclusão aceito como os demais,
      Guerreiro(a) não vinculado recusado, duplicata em aberto recusada e aceita depois do
      desfecho, atraso derivado que não fecha a solicitação, tratamento que grava quem tratou e
      quando, segundo desfecho recusado e desfecho que não apaga nem despersonaliza nada
      (`RF-13-22`, `RF-13-24`, `RF-02-24`, `RF-02-66`, `RN-13-12`, `RN-13-13`, `RN-13-14`,
      `RN-13-22`).
- [x] 4.2 Criar `backend/tests/test_solicitacao_do_responsavel_rota.py` cobrindo as quatro rotas:
      envio que devolve só protocolo e prazo, leitura das próprias sem alcançar as de outro
      responsável, fila do Admin com atraso e nicks, tratamento pelo Admin, e recusa de papel —
      persona de outro papel na abertura, Mestre na fila e no tratamento (`RF-13-22`,
      `RF-13-25`, `RF-13-26`, `RF-02-23`, `RF-02-24`, `RN-13-13`).
- [x] 4.3 Em `backend/tests/test_entrega_de_recompensa.py`, cobrir a saída ampliada: tipo de
      recurso, quantidade e lançamento da baixa presentes para o Admin, e nenhum valor em moedas
      ou reais em nenhuma persona (`RF-02-50`, `RF-02-51`, `RN-02-17`).
- [x] 4.4 Em `apps/app-03-gestao/src/filas/filas.test.tsx`, cobrir a fila nova: protocolo, tipo,
      situação e prazo na lista, destaque de atraso que não bloqueia o tratamento, desfecho que
      passa a exibir quem tratou e quando, e solicitação tratada em leitura (`RF-02-23`,
      `RF-02-24`, `RF-02-66`).
- [x] 4.5 Em `apps/app-03-gestao/src/acervo/acervo.test.tsx`, cobrir a lista de entregas:
      exemplar Alpha e camisa com Guerreiro(a), Mestre, ponto de apoio, data e baixa definitiva,
      ausência de qualquer valor e ausência de caminho de escrita (`RF-02-50`, `RF-02-51`,
      `RN-02-17`).

## 5. Documentação

- [x] 5.1 Em `openspec/cronograma-de-fatias.md`: marcar a fatia 14 do PRD-02 e a linha
      **Entregas confirmadas** como implementadas, com o slug desta change; reescrever o recorte
      da fatia 4 do PRD-13, que perde o núcleo da solicitação e mantém as telas da App 07 e o
      que só ela decide (`RF-13-23`, `RF-13-27`, `RF-13-28`, `RF-13-43`, `RF-13-44`, `RN-13-12`,
      `RN-13-22`).
- [x] 5.2 Em `docs/`: registrar no documento 09 §1, como decisão do fundador de 2026-08-29, a
      separação da fatia 14 do PRD-02 da fatia 4 do PRD-13, com o núcleo da solicitação vindo na
      primeira; retirar do PRD-02 §9 a rota `POST /v1/entregas`, resíduo da decisão de
      2026-08-19 que já passou `RF-02-50` e `RF-02-51` de escrita para leitura; e anotar no
      PRD-13 §9 que a abertura e a leitura das próprias solicitações já estão no núcleo. Nenhum
      arquivo novo em `docs/` e nenhuma mudança em `docs/prds/index.md` — a situação do PRD-02 e
      a do PRD-13 não mudam.
