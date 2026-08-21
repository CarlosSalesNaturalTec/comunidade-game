## 1. Leitura no núcleo

- [x] 1.1 `GET /pontos-de-apoio` em `pontos_de_apoio/rotas.py`, com a regra de listagem em
      `pontos_de_apoio/regra.py`: `contrato_de_listagem` com o filtro de comunidade
      obrigatório, envelope `PaginaDeResultado`, escopo por papel no molde de `listar_acervo`
      (Admin declara a comunidade, Mestre herda do vínculo vigente, demais 403). A saída traz
      nome, comunidade, responsável designado — quando houver — e se está ativo (`RF-07-47`,
      `RF-07-49`, `RF-01-28`, `RF-01-18`, `RF-01-16`).
- [x] 1.2 `GET /aulas` em `aulas/rotas.py`, com a regra em `aulas/regra.py`: mesmo contrato de
      listagem, com os filtros universais de comunidade e período; a saída traz comunidade,
      ponto de apoio, data, horários, situação e o motivo do cancelamento quando houver
      (`RF-02-12`, `RF-01-28`, `RF-01-18`, `RF-01-16`).
- [x] 1.3 `GET /aulas/vigentes` em `aulas/rotas.py`, consumindo `aulas_vigentes` **sem
      alterá-la**: chave de aplicação sim, credencial de persona não, no molde das rotas de
      `vitrine/`; filtro de comunidade opcional; conjunto vazio responde 200 (`RF-02-14`,
      `RF-02-13`, `RF-01-32`, `RF-01-02`, `RN-02-05`).

## 2. Testes do núcleo

- [x] 2.1 Em `backend/tests/test_ponto_de_apoio.py`, os cenários da leitura: Admin lê filtrado
      por comunidade, Mestre lê só a do vínculo, Guerreiro(a) recebe 403, ponto de apoio sem
      responsável designado vem na lista, e listagem sem o filtro obrigatório recebe 422
      (`RF-07-47`, `RF-07-49`, `RF-01-18`).
- [x] 2.2 Em `backend/tests/test_aula.py`, os cenários da agenda: Admin lê, Mestre lê só as
      suas comunidades, Apoiador recebe 403, pendente de lastro e confirmada saem distintas
      sem que a leitura mude situação, e o filtro de período recorta a lista (`RF-02-12`,
      `RF-01-28`, `RF-01-18`).
- [x] 2.3 Ainda em `backend/tests/test_aula.py`, os cenários das vigentes pela rota: aplicação
      com chave e sem persona lê; fora de qualquer janela responde 200 com conjunto vazio;
      duas comunidades vigentes no mesmo momento saem ambas; sem chave a chamada é recusada
      (`RF-02-14`, `RF-02-13`, `RN-02-05`, PRD-02 §12).

## 3. Camada visual comum

- [x] 3.1 Campo de data e hora com fuso em `comum/react/`, exportado pelo `indice.ts`, com o
      erro associado ao campo como os demais campos da camada. Ele NUNCA produz horário sem
      fuso (design — decisão 4, documento 15 §12).
- [x] 3.2 Teste do campo em `comum/react/`: valor devolvido carrega fuso, valor inválido
      aponta o erro no próprio campo, e o campo é operável pelo teclado.

## 4. Ponto de apoio na App 03

- [x] 4.1 `apps/app-03-gestao/src/pontos-de-apoio/`: cliente de API (lista e cadastro), tela
      com lista densa e formulário de nome e comunidade, consumindo a camada de `comum/react/`.
      Ponto de apoio sem responsável aparece como informação, não como pendência; quem não é
      Admin não recebe o caminho de cadastro e lê a recusa em linguagem simples (`RF-07-47`,
      `RF-07-49`, `RN-07-34`).

## 5. Agenda na App 03

- [x] 5.1 `apps/app-03-gestao/src/agenda/`: cliente de API (agenda, agendamento e
      cancelamento) e tela com lista densa, filtros de comunidade e período, situação
      distinguível sem depender só de cor, e o motivo na aula cancelada (`RF-02-12`,
      `RF-01-18`, `RN-02-09`).
- [x] 5.2 Formulário de agendamento: comunidade, data, horário inicial, horário final e ponto
      de apoio, com o seletor de ponto de apoio refazendo a consulta filtrada pela comunidade
      escolhida (design — decisão 5). Horário final não posterior ao inicial e ponto de apoio
      de outra comunidade são apontados no próprio campo (`RF-02-12`, `RF-02-30`).
- [x] 5.3 Cancelamento com motivo obrigatório, alcançável pelo Admin e pelo Mestre da
      comunidade da aula, avisando antes de confirmar que a operação libera os recursos
      reservados e não se desfaz; aula com desfecho não oferece o caminho (`RF-02-95`,
      `RF-01-72`, `RN-02-20`).

## 6. Testes da App 03

- [x] 6.1 `apps/app-03-gestao/src/pontos-de-apoio/pontos-de-apoio.test.tsx`: cadastro
      completo, campo obrigatório em falta apontado no campo, ponto de apoio sem responsável
      apresentado como informação, e Mestre sem o caminho de cadastro (`RF-07-47`,
      `RF-07-49`).
- [x] 6.2 `apps/app-03-gestao/src/agenda/agenda.test.tsx`: agendamento completo com a aula
      nascendo confirmada, horário final inválido apontado no campo, seletor de ponto de apoio
      restrito à comunidade escolhida, situações distinguíveis na lista, Mestre lendo só as
      suas comunidades e o cancelamento com e sem motivo (`RF-02-12`, `RF-02-30`, `RF-02-95`,
      `RN-02-09`, `RN-02-20`).

## 7. Documentação

- [x] 7.1 `docs/09-topicos-em-aberto-e-sugestoes.md` §1 recebe a pendência da **modalidade da
      aula** — o PRD-02 §8 e o `RF-02-30` preveem aula on-line ou presencial, e a capacidade
      `aula-e-presenca` exige ponto de apoio em toda aula. Nenhum outro documento muda: a
      change não toma decisão nova, não altera requisito de PRD, não muda a situação de
      nenhum PRD, não muda relação entre documentos e não cria arquivo em `docs/`.
