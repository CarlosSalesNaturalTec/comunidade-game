## 1. Leituras que faltam no núcleo

- [x] 1.1 `coletas/regra.py` e `coletas/rotas.py`: `GET /v1/tipos-de-coleta`, paginada, com nome,
      forma de registro, unidade, faixa esperada e `ativo` de cada tipo; 403 para Guerreiro(a),
      responsável e Apoiador. Verificar por `tests/test_tipo_de_coleta.py` — Mestre e Admin leem,
      tipo por evidência sai sem unidade e sem faixa, tipo desativado sai assinalado
      (`RF-09-27`, `RF-08-05`, `RF-01-28`).
- [x] 1.2 `trilhas/rotas.py`: aninhar os desafios de coleta em cada missão da saída de
      `GET /v1/trilhas/minhas`, com os cinco atributos e o tipo resolvido; rascunho servido como
      publicada. Verificar por `tests/test_trilha_rota.py` — o desafio declarado aparece na
      missão, missão sem desafio vem com lista vazia, trilha de outro autor não aparece
      (`RF-09-27`, `RF-09-28`, `RF-09-04`).
- [x] 1.3 `fila/regra.py` e `fila/rotas.py`: `GET /v1/sugestoes/minhas`, do autor em sessão,
      paginada, com alvo, texto, situação, prazo, `em_atraso` derivado, data do desfecho e
      motivo do retorno — **sem** o `parecer`. Verificar por `tests/test_fila_rota.py` — o autor
      vê só as suas, a não adotada traz o motivo, o prazo vencido sai em atraso, o parecer não
      sai (`RF-09-55`, `RF-01-25`, `RN-02-25`).

## 2. Desafio de coleta na App 09

- [x] 2.1 `apps/app-09-mestre/src/trilhas/api.ts`: tipos e chamadas de `GET /v1/tipos-de-coleta`,
      `POST /v1/desafios-de-coleta` e o desafio aninhado em `TrilhaDoMestre`. Verificar pela
      compilação do pacote e pelo uso nas telas de 2.2 e 2.3 (`RF-09-27`, `RF-09-28`).
- [x] 2.2 `trilhas/FormularioDeDesafioDeColeta.tsx`: tipo escolhido entre os **ativos** do
      catálogo, cadência, vigência, granularidade entre os seis níveis e registros que pontuam;
      unidade e forma de registro do tipo escolhido apresentadas; nenhum campo de etiqueta ODS e
      nenhuma ação de criar tipo. A recusa do núcleo vira mensagem em linguagem simples com o
      campo apontado (`RF-09-27`, `RF-09-28`, `RN-09-36`, `RN-09-16`).
- [x] 2.3 `trilhas/ListaDeMissoes.tsx` e `trilhas/TelaDaTrilha.tsx`: apresentar os desafios já
      declarados em cada missão, inclusive em rascunho, e a missão sem desafio como tal, com a
      ação de declarar oferecida só ao autor (`RF-09-27`, `RF-09-28`).

## 3. Território e proposta na App 09

- [x] 3.1 `apps/app-09-mestre/src/territorio/api.ts`: lista pública de comunidades, solicitações
      em aberto por comunidade e avaliação da solicitação, com a varredura que soma o total para
      o alerta (design — decisão 4) (`RF-09-53`, `RF-09-54`).
- [x] 3.2 `territorio/TelaDeTerritorio.tsx` e `territorio/AvaliacaoDeSolicitacao.tsx`:
      solicitações em aberto agrupadas por comunidade, com nível pretendido, rótulo,
      justificativa e desafio de origem; aprovar exigindo o local pai da hierarquia daquela
      comunidade e recusar exigindo motivo; nenhuma ação de cadastrar local ou criar comunidade;
      a avaliada sai da lista e o erro do núcleo vira mensagem simples (`RF-09-53`, `RN-09-16`).
- [x] 3.3 `apps/app-09-mestre/src/propostas/api.ts` e `propostas/TelaDePropostas.tsx`: registro
      da proposta em texto — sem áudio — e a lista das próprias com situação, prazo, desfecho e
      motivo do retorno; nenhuma ação de avaliar (`RF-09-55`, `RN-09-23`).
- [x] 3.4 `App.tsx`: as áreas "Território" e "Propostas" na navegação, com o contador do alerta
      na primeira enquanto houver solicitação em aberto, some quando a última é tratada
      (`RF-09-54`).

## 4. Testes das telas

- [x] 4.1 `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`: os cenários de "O Mestre declara o
      desafio de coleta da missão" e de "A App 09 apresenta os desafios de coleta já declarados"
      — declaração completa, tipo vindo do catálogo sem ação de criar, unidade apresentada,
      vigência invertida virando mensagem simples, rascunho mostrando o desafio, missão sem
      desafio, ausência do campo de etiqueta ODS e de ação em trilha alheia.
- [x] 4.2 `apps/app-09-mestre/src/territorio/territorio.test.tsx`: os cenários de "O Mestre
      avalia a solicitação de novo local" e de "A App 09 alerta enquanto houver solicitação sem
      desfecho" — aprovação com local pai, recusa barrada sem motivo, ausência de solicitação de
      trilha alheia, ausência de cadastro de local e de comunidade, hierarquia inválida em
      linguagem simples, alerta presente e alerta que some, e alerta que não depende de escolher
      comunidade.
- [x] 4.3 `apps/app-09-mestre/src/propostas/propostas.test.tsx`: os cenários de "O Mestre
      registra a proposta de evolução e acompanha o status" — registro em texto, ausência de
      áudio, desfecho não adotado com o motivo e sem e-mail, lista sem proposta de outra persona
      e ausência da ação de avaliar.

## 5. Documentação

- [x] 5.1 `openspec/cronograma-de-fatias.md`: marcar as fatias **7** e **8** do PRD-09 como
      implementadas, com o slug desta change nas duas linhas. Nada muda em `docs/`: a change não
      tomou decisão nova, não alterou requisito de PRD, não mudou a situação do PRD-09 nem a
      relação entre documentos, e não criou arquivo novo em `docs/`.
