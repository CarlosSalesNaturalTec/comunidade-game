# PRD-02 — App 03: Frontend de Gestão

## 1. Identificação

| Campo            | Valor                                                |
| ---------------- | ---------------------------------------------------- |
| PRD              | PRD-02                                               |
| Aplicação        | App 03 — Gestão administrativa                       |
| Onda             | 2                                                    |
| Situação         | aprovado                                             |
| Versão e data    | v12 — 2026-08-25                                     |
| Depende de       | PRD-01                                               |
| Documentos-fonte | 03 §§5, 8, 11, 12, 04 §§1–3, 05 §§2–5, 02 §§1, 4, 15 |

## 2. Contexto e objetivo

A App 03 é a mesa de comando do projeto. Nenhuma outra aplicação da etapa abre sem ela: é aqui
que o Admin cria a Comunidade Virtual e **agenda a aula que habilita o App 01**; é aqui que
Mestres, Apoiadores e responsáveis são cadastrados; e é aqui que a atividade ganha lastro antes
de existir. As **equipes não são cadastradas aqui**: elas se formam no App 01, a cada aula, e o
painel do dia apenas as mostra.

Ela também é a aplicação do **dia da aula**. Como o encontro é assíncrono — cada Guerreiro(a)
chega na sua hora e avança na sua missão —, o painel do dia substitui o controle visual de uma
turma em bloco: quem chegou, em que missão cada equipe está, quem aguarda aparelho, o que já foi
lançado e o que falta lançar antes de a aula acabar.

A fronteira com a App 09 é o critério de tudo o que entra aqui: **a gestão cadastra, aprova,
lança e confere; a autoria é do Mestre e vive lá**. Nesta aplicação o Mestre lê o painel do dia
e **conduz o Quiz ao Vivo das aulas que ministra** — quem está na frente da turma é quem tem de
poder tocar a partida.

## 3. Escopo

### 3.1 Dentro do escopo

- Cadastro de personas: Guerreiros e Guerreiras, Mestres, Apoiadores, responsáveis e Admins —
  **equipe não se cadastra aqui**: forma-se no App 01 e aparece no painel do dia.
- Criação da Comunidade Virtual e **agenda das aulas com comunidade, data, horário inicial e
  final** — é ela que habilita o App 01.
- Conferência do vínculo do Guerreiro(a) à comunidade herdada da aula.
- Cadastro de locais do território e tratamento das solicitações de novo local.
- Catálogo de poderes do Ciclo 01 e cadastro de atividade avulsa com pontuação, recompensas e
  o poder que ela desenvolve.
- Agenda de aulas on-line e presenciais, com reserva de recursos e bloqueio sem lastro.
- Lançamento das atividades realizadas e das entradas manuais do dia.
- Conferência das presenças vindas do App 01 e ajuste manual.
- Painel do dia do encontro em andamento, incluindo saldos e lançamentos pendentes.
- Condução do **Quiz ao Vivo** pelo Mestre da aula ou por um Admin, com o banco de perguntas
  cadastrado pelo Mestre na App 09.
- Controle do acervo didático: entrega dos exemplares Alpha, tombamento, ficha de vida e
  conferência de inventário.
- Gestão de recursos: registro e homologação de aportes, e **publicação das necessidades** das
  atividades pendentes de lastro.
- Filas de avaliação: solicitações de participação, **solicitações de dados**, solicitações
  dos responsáveis, desafios extras dos Apoiadores e a fila única de sugestões e propostas.
- Conteúdo institucional da vitrine — "Quem somos", "Contatos" e "Como apoiar".
- Aviso de coleta em toda tela que grava dado pessoal e área de leitura sobre o destino e o uso
  de cada dado.

### 3.2 Fora do escopo

- **Autoria de trilha, missão, conteúdo, quiz e desafio de coleta** — é a bancada do
  Mestre na App 09 (PRD-09) — inclusive as **atividades de cada missão** e a
  **recompensa de cada marco**. A App 03 cadastra apenas atividade avulsa, fora de trilha;
  acompanha o que foi publicado e, na auditoria por amostragem, pode despublicar com motivo.
- **Lançamento das atividades do próprio Mestre** — ele lança na App 09; aqui o Admin lança as
  demais e corrige o que precisar.
- Regras de pontuação, cadência de coleta e valoração de aporte: normatizadas nos documentos
  11, 02 e 04 e detalhadas nos PRD-08 e PRD-07.
- Telas de coleta do Guerreiro(a) (PRD-05) e conversa de cadastro do onboarding (PRD-04).
- **Notificação por e-mail**: no Ciclo 01 todo retorno acontece dentro da plataforma.
- **Transferência de Guerreiro(a) entre comunidades**: existe no modelo, mas não é operada no
  Ciclo 01.
- Relatório de efetividade ao Apoiador: é entrega da App 08 (PRD-14).
- **Empréstimo de bancada, guarda por equipe e fluxo de reposição do acervo permanente**: o
  Ciclo 01 opera tombamento, ficha de vida e badge, e o resto fica para o ciclo seguinte
  (documento 05 §3). Retira o antigo `RF-02-54`, cujo identificador não é reaproveitado.
- **Processos de auditoria ainda não implementados**: tela da trilha de auditoria (`RF-02-63`),
  amostragem das trilhas publicadas com despublicação (`RF-02-70`) e amostragem do corpus de
  apoio escolar (`RF-02-74` a `RF-02-76`, que já acompanhava o Ciclo 02) vão ao Ciclo 02, com a
  amostragem semanal de coleta (`RF-02-98`). O `GET /v1/auditoria` segue testado no backend, sem
  consumidor nesta aplicação no Ciclo 01 (documento 09).

## 4. Personas e permissões

| Persona   | O que faz nesta aplicação                                                             | O que não pode fazer                                                |
| --------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Admin     | Tudo: cadastros, aprovações, agenda, lançamentos, filas, acervo, recursos e auditoria | Registrar coleta no lugar do Guerreiro(a); criar conteúdo de trilha |
| Mestre    | Lê o painel do dia, conduz o Quiz ao Vivo e registra a infração das suas aulas        | Escrever nas demais rotas de gestão — o que é dele fica na App 09   |
| Visitante | Nada: a aplicação é inteiramente autenticada                                          | Acessar qualquer tela                                               |

O Mestre entra por login social, como todo adulto. Nesta aplicação ele lê o painel do dia,
conduz a partida de quiz das suas aulas e registra a infração ocorrida sobre atividade de
trilha que autora — nada além disso. A homologação da equipe da trilha passou à App 01, o
aparelho em que a equipe é formada: o `RF-02-94` foi transferido para o PRD-04 (`RF-04-62`) e
**não é reaproveitado**.

## 5. Jornadas principais

### 5.1 Abrir a comunidade e habilitar o onboarding

1. O Admin cria a **Comunidade Virtual**, que nasce vazia.
2. Agenda a aula declarando **comunidade, data, horário inicial e final**.
3. Na data e no horário marcados, o **App 01 opera sozinho**: identifica a aula vigente e
   vincula cada novo cadastro à comunidade dela. Não há comunidade default nem chave de
   liberação.
4. Fora da janela de alguma aula agendada, o App 01 não abre.
5. Havendo, no mesmo horário, aulas presenciais em **comunidades diferentes**, o App 01
   pergunta uma vez, ao abrir, em qual está operando.
6. **No Ciclo 01 o Guerreiro(a) não muda de comunidade**: a conferência do vínculo existe, a
   transferência não.

### 5.2 Avaliar uma solicitação de participação

1. Pessoa ou instituição envia o formulário público da vitrine (App 06), com nome, e-mail,
   WhatsApp, pretensão e apresentação em texto livre — mais instituição e links, se quiser.
2. A solicitação entra na fila no status **recebida**, com o **prazo de 7 dias** correndo.
3. O Admin avalia, registra o parecer e conclui como **aceita** ou **recusada**, e a aplicação
   grava quem tratou e quando. Passados 7 dias sem desfecho, a solicitação aparece em atraso.
4. Aceita, a solicitação **abre o cadastro** de Mestre ou Apoiador já preenchido com o que veio
   do formulário — o cadastro é o ato do Admin, não da solicitação.
5. Recusada, nada é criado; o status fica disponível ao solicitante — no Ciclo 01 sem
   notificação por e-mail.

### 5.3 Cadastrar responsável e vincular Guerreiros e Guerreiras

1. O responsável se apresenta pessoalmente no encontro e informa e-mail e as crianças sob sua
   responsabilidade.
2. O Admin cadastra o responsável e vincula **Guerreiros e Guerreiras já cadastrados**, com o
   grau de parentesco de cada vínculo.
3. O quarto vínculo para o mesmo Guerreiro(a) é recusado, e os três anteriores seguem válidos.
4. Sem conta Google, o Admin cria a credencial de usuário e senha provisória.
5. O mesmo cadastro pode ter sido feito pelo Mestre na App 09 — a aplicação mostra quem o fez.

### 5.4 Planejar a aula e reservar os recursos

1. O Admin agenda a aula, on-line ou presencial, com **comunidade, data, horário inicial e
   final**, a atividade prevista e o ponto de apoio.
2. A aplicação consulta o livro-razão e **reserva** os recursos necessários.
3. Faltando lastro, a atividade fica **pendente de lastro** e a diferença é publicada como
   **necessidade de recurso** em três lugares: vitrine pública (App 06), área do Apoiador
   (App 08) e área dos Mestres da trilha (App 09).
4. O Apoiador aporta o que falta; o **Mestre**, vendo a pendência na App 09, pode assumi-la
   como **aporte por absorção**, em um ato de confirmação.
5. Suprida a necessidade, o núcleo confirma a atividade e efetiva a reserva; a aplicação
   apenas mostra a mudança.

### 5.5 Conduzir o encontro pelo painel do dia

1. Aberto o encontro, o painel mostra **quem já chegou**, com as presenças que o App 01
   registrou automaticamente.
2. Mostra, por equipe, **em que missão cada uma está** — a atividade que ela declarou pelo
   App 01 — e quem está aguardando aparelho, derivado de quem chegou e ainda não formou equipe.
3. Mostra a atividade prevista, os recursos providos e o **saldo dos tipos de recurso** do
   ponto de apoio da aula, pelo catálogo configurável da gestão.
4. Lista os **lançamentos pendentes** — o que falta lançar antes de a aula terminar.
5. O Mestre lê esse mesmo painel para circular entre as equipes; tudo o que ele escreve
   continua na App 09.
6. Presença que o reconhecimento não capturou é confirmada manualmente, com registro de quem
   confirmou.

### 5.6 Lançar a atividade realizada e as entradas do dia

1. O Admin lança a atividade realizada: data, mentores, Guerreiros, Guerreiras e equipes
   participantes.
2. Atribui o resultado de cada participante — **realizada**, **realizada com mérito** ou
   **mérito extra por auxílio aos colegas**.
3. Lança as entradas manuais do dia: presença, pontuação extra a quem ajudou o colega e
   **infração ocorrida na aula**.
4. O lançamento converte a reserva de recursos em **baixa** no livro-razão.
5. Toda a escrita é auditada com autor, papel, data e hora.

### 5.7 Conduzir o Quiz ao Vivo

1. O **Mestre que ministra a aula** — ou um Admin — abre a partida escolhendo o banco de
   perguntas do Mestre curador e as **equipes formadas no App 01** naquele encontro.
2. Ao dar o _start_, a pergunta aparece **simultaneamente** nos dispositivos logados na aula.
3. Cada equipe se consulta e responde pelo App 01.
4. A aplicação apura a **primeira resposta correta** por ordem de chegada e mostra o resultado.
5. Encerrada a partida, a pontuação é lançada automaticamente para as equipes.
6. Dispositivo que caiu volta na pergunta corrente, sem travar a partida.

### 5.8 Tratar as filas

1. **Desafio extra** proposto na App 08 chega já validado pelo Mestre da trilha; o Admin
   aprova ou recusa, e a aprovação só é aceita com o **lastro da recompensa registrado**.
2. **Solicitação do responsável** vinda da App 07 chega com protocolo e **prazo de 7 dias**; o
   Admin trata, registra o desfecho e a aplicação grava quem tratou e quando. Vencido o prazo
   sem desfecho, a solicitação aparece em atraso.
3. **Sugestões e propostas** das Apps 05, 07, 08 e 09 chegam a uma **fila única**, avaliadas
   com status e retorno a quem propôs.
4. **Solicitação de novo local** vinda da App 05 aparece com alerta enquanto está em aberto; o
   Admin aprova, criando o local, ou recusa com motivo — o Mestre da trilha faz o mesmo na
   App 09.

## 6. Requisitos funcionais

### 6.1 Cadastros e catálogo

| ID          | Requisito                                                                                           | Prioridade |
| ----------- | --------------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-01`  | Admin cadastra e edita Guerreiros e Guerreiras, com nome, nascimento, nick e avatar                 | essencial  |
| `RF-02-02`  | Admin cadastra Mestre declarando os links de currículo, portfólio, redes e documentos externos      | essencial  |
| `RF-02-03`  | Admin cadastra Apoiador declarando os mesmos links e os termos de doação                            | essencial  |
| `RF-02-04`  | Aplicação recusa o cadastro de Mestre ou Apoiador sem ao menos um artefato comprobatório            | essencial  |
| `RF-02-05`  | Admin inclui novo Admin manualmente                                                                 | essencial  |
| `RF-02-06`  | Admin cadastra responsável e vincula Guerreiros e Guerreiras já cadastrados, com grau de parentesco | essencial  |
| `RF-02-07`  | Admin cria credencial de usuário e senha provisória para adulto sem conta social                    | essencial  |
| `RF-02-08`  | Painel do dia lista as equipes formadas no App 01 naquela aula, com os integrantes de cada uma      | essencial  |
| `RF-02-09`  | Aplicação não cria, edita nem desfaz equipe: a composição é dos Guerreiros e Guerreiras             | essencial  |
| `RF-02-10`  | Admin mantém o catálogo de poderes do ciclo                                                         | essencial  |
| `RF-02-99`  | Admin encerra o ciclo corrente num ato isolado, que não declara o ciclo seguinte                    | essencial  |
| `RF-02-100` | Encerramento expurga o motivo das ocorrências de conduta do ciclo e as tira do ranking              | essencial  |
| `RF-02-11`  | Admin cria Comunidade Virtual, que nasce vazia                                                      | essencial  |
| `RF-02-12`  | Agenda da aula exige comunidade, data, horário inicial e horário final                              | essencial  |
| `RF-02-13`  | App 01 opera apenas dentro da janela de uma aula agendada, sem chave de liberação                   | essencial  |
| `RF-02-14`  | Aplicação expõe as aulas vigentes da data e do horário, para o App 01 escolher a comunidade         | essencial  |
| `RF-02-15`  | Admin confere o vínculo do Guerreiro(a) à comunidade herdada da aula                                | essencial  |
| `RF-02-16`  | Admin cadastra locais do território na hierarquia da comunidade                                     | essencial  |
| `RF-02-17`  | Admin consulta os desafios de coleta de trilha publicada, com cadência, vigência e séries ativas    | desejável  |

### 6.2 Filas de avaliação

| ID         | Requisito                                                                                                                                      | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-18` | Fila de solicitações exibe nome, e-mail, WhatsApp, pretensão, apresentação, instituição e links                                                | essencial  |
| `RF-02-19` | Admin conclui a solicitação como aceita ou recusada, com parecer, autor e data registrados                                                     | essencial  |
| `RF-02-65` | Solicitação de participação sem desfecho em 7 dias aparece em atraso na fila                                                                   | essencial  |
| `RF-02-20` | Solicitação aceita abre o cadastro de Mestre ou Apoiador pré-preenchido, sem criar acesso                                                      | essencial  |
| `RF-02-77` | Fila de solicitações de dados exibe solicitante, instituição, finalidade declarada e recorte pedido                                            | essencial  |
| `RF-02-78` | Admin aprova ou recusa a solicitação de dados, com motivo, autor e data registrados                                                            | essencial  |
| `RF-02-93` | Fila da solicitação de dados apresenta ao Admin o critério de aprovação: solicitante identificado, finalidade compatível e não reidentificação | essencial  |
| `RF-02-79` | Entrega aprovada é gratuita e anonimizada, com registro do que foi entregue e a quem                                                           | essencial  |
| `RF-02-21` | Fila de solicitações de novo local alerta enquanto houver solicitação em aberto                                                                | essencial  |
| `RF-02-22` | Admin aprova a solicitação de local, criando-o, ou recusa com motivo                                                                           | essencial  |
| `RF-02-23` | Fila de solicitações dos responsáveis exibe protocolo, tipo, situação e o prazo de 7 dias                                                      | essencial  |
| `RF-02-24` | Admin registra o desfecho da solicitação do responsável, com quem tratou e quando                                                              | essencial  |
| `RF-02-66` | Solicitação de responsável sem desfecho em 7 dias aparece em atraso na fila                                                                    | essencial  |
| `RF-02-25` | Fila única reúne sugestões e propostas das Apps 05, 07, 08 e 09, identificando autor e persona                                                 | essencial  |
| `RF-02-26` | Admin avalia a sugestão, muda o status e registra o retorno a quem propôs                                                                      | essencial  |
| `RF-02-80` | Admin edita o conteúdo institucional da vitrine, com autor e data do que publicou                                                              | essencial  |
| `RF-02-83` | Fila do pré-cadastro exibe a identificação, o aporte declarado e o comprovante anexado                                                         | essencial  |
| `RF-02-84` | Admin valida o comprovante e homologa o aporte, que é convertido em moedas                                                                     | essencial  |
| `RF-02-85` | Aprovação cria o cadastro de Apoiador e publica o card na vitrine com o total em moedas                                                        | essencial  |
| `RF-02-86` | Pré-cadastro sem comprovante legível é recusado com motivo, sem criar cadastro nem aporte                                                      | essencial  |
| `RF-02-87` | Admin lê a fila das solicitações de chave, com quem pediu e o que pretende construir                                                           | essencial  |
| `RF-02-88` | Admin aprova ou recusa a solicitação de chave, com parecer e autoria                                                                           | essencial  |
| `RF-02-89` | Aprovação emite a chave e exibe o identificador e o segredo uma única vez, para entrega ao solicitante                                         | essencial  |
| `RF-02-90` | Painel mostra as chaves emitidas com prazo de apresentação, URL apresentada e situação                                                         | essencial  |
| `RF-02-91` | Painel destaca as chaves com prazo a vencer e as revogadas automaticamente por prazo vencido                                                   | essencial  |
| `RF-02-92` | Admin revoga chave a qualquer tempo, com motivo registrado                                                                                     | essencial  |
| `RF-02-27` | Fila de desafios extras mostra apenas os já validados pelo Mestre da trilha                                                                    | essencial  |
| `RF-02-28` | Admin aprova o desafio extra, e a aprovação é recusada sem o lastro da recompensa registrado                                                   | essencial  |

### 6.3 Atividades, agenda e lançamentos

| ID         | Requisito                                                                                          | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-29` | Admin cadastra atividade avulsa, fora de trilha, com o poder que ela desenvolve                    | essencial  |
| `RF-02-71` | Admin consulta as atividades e as recompensas de marco autoradas pelo Mestre, sem editá-las        | essencial  |
| `RF-02-30` | Admin agenda aula on-line ou presencial, com atividade prevista e ponto de apoio                   | essencial  |
| `RF-02-31` | Agendamento reserva os recursos necessários no livro-razão                                         | essencial  |
| `RF-02-95` | Admin, ou Mestre da comunidade da aula, cancela aula agendada com motivo, liberando a reserva      | essencial  |
| `RF-02-32` | Atividade sem lastro fica pendente de lastro e publica a necessidade na vitrine e nas Apps 08 e 09 | essencial  |
| `RF-02-67` | Aplicação mostra a atividade confirmada e a reserva efetivada pelo aporte que supre a falta        | essencial  |
| `RF-02-33` | Admin lança atividade realizada com data, mentores, Guerreiros, Guerreiras e equipes               | essencial  |
| `RF-02-34` | Lançamento atribui a cada participante realizada, com mérito ou mérito extra por auxílio           | essencial  |
| `RF-02-35` | Lançamento da atividade realizada converte a reserva em baixa de recursos                          | essencial  |
| `RF-02-36` | Admin confere as presenças vindas do App 01 e ajusta manualmente, com registro do ajuste           | essencial  |
| `RF-02-68` | Admin anexa ao consentimento a digitalização do termo de biometria assinado no encontro            | essencial  |
| `RF-02-37` | Admin registra infração ocorrida na aula, vinculada ao encontro e ao Guerreiro(a)                  | essencial  |
| `RF-02-38` | Admin lança pontuação negativa com motivo e item do Código de Conduta, sem revisão de terceiro     | essencial  |
| `RF-02-39` | Admin lança pontuação extra ao Guerreiro(a) que ajudou o colega                                    | essencial  |
| `RF-02-40` | Admin corrige lançamento por novo lançamento de ajuste, sem apagar o original                      | essencial  |

### 6.4 Painel do dia

| ID                     | Requisito                                                                                                                             | Prioridade |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-41`             | Painel do dia lista quem já chegou, com a presença registrada pelo App 01                                                             | essencial  |
| `RF-02-42`             | Painel mostra, por equipe, a missão em que ela está                                                                                   | essencial  |
| `RF-02-43`             | Painel mostra quem está aguardando aparelho — derivado de quem tem presença sem equipe formada na aula, sem entidade nem fila própria | essencial  |
| `RF-02-44`             | Painel mostra atividade prevista e recursos providos do encontro                                                                      | essencial  |
| `RF-02-45`             | Painel mostra o saldo dos tipos de recurso do ponto de apoio da aula, pelo catálogo configurável da gestão                            | essencial  |
| `RF-02-46`, `RF-02-47` | Painel lista os lançamentos pendentes do encontro — o que falta lançar antes de a aula terminar                                       | essencial  |
| `RF-02-69`             | Painel lista os termos de biometria assinados e ainda sem digitalização anexada                                                       | essencial  |
| `RF-02-48`             | Painel atualiza sozinho durante o encontro, sem recarga manual                                                                        | essencial  |
| `RF-02-49`             | Mestre lê o painel do dia e recebe recusa em toda escrita que não seja a do Quiz ao Vivo e da infração das suas atividades            | essencial  |

### 6.5 Acervo, recursos e Quiz ao Vivo

| ID         | Requisito                                                                                          | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-50` | Aplicação mostra a entrega do exemplar Alpha confirmada pelo Mestre, com a baixa definitiva        | essencial  |
| `RF-02-51` | Aplicação mostra a entrega da camisa confirmada pelo Mestre ao Guerreiro(a) inscrito, com a baixa  | essencial  |
| `RF-02-52` | Admin tomba o exemplar permanente com título, tombo, ponto de apoio e responsável designado        | essencial  |
| `RF-02-96` | Admin desativa e reativa ponto de apoio, sempre com motivo; a lista distingue o inativo do ativo   | essencial  |
| `RF-02-97` | Admin transfere saldo de um tipo de recurso entre pontos de apoio, com o saldo da origem mostrado  | essencial  |
| `RF-02-53` | Aplicação mantém a ficha de vida do exemplar, com estado de conservação e histórico de uso         | essencial  |
| `RF-02-55` | Perda ou dano é anotado na ficha de vida, sem débito ao Guerreiro(a) nem à família                 | essencial  |
| `RF-02-56` | Admin realiza a conferência de inventário do módulo e publica o resultado na prestação de contas   | desejável  |
| `RF-02-57` | Admin registra e homologa aporte com provedor, tipo, comprovante e valor em moedas                 | essencial  |
| `RF-02-58` | Aplicação exibe as necessidades de recurso em aberto das atividades previstas                      | essencial  |
| `RF-02-59` | Mestre da aula ou Admin abre partida de Quiz ao Vivo com o banco do curador e as equipes da aula   | essencial  |
| `RF-02-60` | Partida exibe a pergunta simultaneamente nos dispositivos logados na aula                          | essencial  |
| `RF-02-61` | Partida fixa uma equipe por Guerreiro(a) e aceita uma resposta por equipe e por pergunta           | essencial  |
| `RF-02-62` | Partida credita toda equipe que acerta e o bônus à primeira, por ordem de chegada no servidor      | essencial  |
| `RF-02-72` | Quem conduz a partida pode anular a pergunta contestada, sem crédito para ninguém                  | essencial  |
| `RF-02-73` | Encerrada a partida, a pontuação é lançada automaticamente às equipes, respeitado o teto           | essencial  |
| `RF-02-74` | Admin audita por amostragem o conteúdo de apoio escolar dos Mestres e despublica com motivo        | essencial  |
| `RF-02-76` | Aplicação abre a amostra mensal de auditoria com 10% do conteúdo novo e 100% do que gerou recusa   | essencial  |
| `RF-02-98` | Aplicação abre a amostra semanal de coleta com 10% dos registros por série ativa, mínimo de um     | essencial  |
| `RF-02-75` | Aplicação recusa cadastro de conteúdo de apoio escolar por Admin: o corpus é autoria do Mestre     | essencial  |
| `RF-02-63` | Admin consulta a trilha de auditoria das ações de gestão, com filtro por autor, período e entidade | essencial  |
| `RF-02-64` | Toda tela que coleta dado exibe o aviso discreto e o acesso à área detalhada de direitos           | essencial  |
| `RF-02-70` | Admin audita por amostragem as trilhas publicadas e despublica com motivo registrado               | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                                                        | Invariante | Fonte      |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------- |
| `RN-02-01` | Mestre e Apoiador são cadastrados só por Admin, com link comprobatório declarado                                             | 3          | 02 §1      |
| `RN-02-02` | Novo Admin só entra por inclusão manual de outro Admin                                                                       | 3          | 02 §1      |
| `RN-02-03` | Solicitação de participação não cria cadastro nem acesso                                                                     | 3          | 02 §1      |
| `RN-02-26` | Nenhum conjunto de dados sai sem aprovação de Admin, e a entrega é gratuita e anonimizada                                    | 17         | 03 §12.3   |
| `RN-02-27` | Nenhuma chave é emitida sem aprovação de Admin; o formulário da vitrine só enfileira o pedido                                | 3          | 03 §8      |
| `RN-02-28` | O segredo da chave é exibido uma única vez e não é recuperável depois                                                        | —          | 03 §1      |
| `RN-02-29` | Chave sem URL apresentada em 30 dias é revogada pelo núcleo, sem ato de Admin                                                | —          | 03 §8      |
| `RN-02-30` | O encerramento do ciclo não congela indicador: os quatro da lista pública seguem apurados no instante da consulta            | —          | 02 §1      |
| `RN-02-04` | Comunidade Virtual é criada apenas por Admin e nasce vazia                                                                   | 4          | 02 §1      |
| `RN-02-05` | Sem aula agendada para a data e o horário, o App 01 não opera                                                                | 4          | 02 §1      |
| `RN-02-06` | O Guerreiro(a) não muda de comunidade no Ciclo 01; a transferência existe no modelo, com data                                | 4          | 02 §1      |
| `RN-02-07` | Equipe tem no máximo cinco integrantes e no máximo um familiar de 17 anos ou mais                                            | 15         | 02 §5      |
| `RN-02-08` | Cada Guerreiro(a) tem no máximo três responsáveis, com grau de parentesco em texto livre                                     | 3          | 02 §1      |
| `RN-02-09` | Atividade sem lastro fica pendente e publica a necessidade; realizada, nunca sem recurso                                     | 9          | 04 §1      |
| `RN-02-10` | Desafio extra só é aprovado por Admin depois da validação do Mestre da trilha                                                | —          | 04 §3      |
| `RN-02-11` | Desafio extra só é publicado com o lastro da recompensa registrado                                                           | 9          | 04 §3      |
| `RN-02-12` | Lançamento não é editado nem apagado: correção é novo lançamento de ajuste                                                   | —          | 04 §1      |
| `RN-02-13` | Pontuação negativa é lançada pelo Mestre ou pelo Admin, com motivo e sem revisão de terceiro                                 | —          | 02 §4      |
| `RN-02-14` | Descuido acidental com material comum não é infração e não gera pontuação negativa                                           | —          | 05 §3      |
| `RN-02-15` | Sobre o livro próprio do Guerreiro(a) não incide pontuação negativa em hipótese alguma                                       | —          | 05 §3      |
| `RN-02-16` | Perda ou dano de material comum não gera débito ao Guerreiro(a) nem à família                                                | —          | 05 §3      |
| `RN-02-17` | Exemplar da linha Alpha e camisa entregues têm baixa definitiva no livro-razão                                               | —          | 05 §3      |
| `RN-02-18` | Exemplar permanente não sai do ponto de apoio; a retirada registrada é do ciclo seguinte                                     | —          | 05 §3      |
| `RN-02-19` | Aporte aparece publicamente em moedas da plataforma, nunca em reais                                                          | 16         | 04 §1      |
| `RN-02-20` | Mestre acessa esta aplicação para ler o painel do dia, conduzir a partida de quiz e registrar a infração das suas atividades | —          | 03 §5      |
| `RN-02-21` | Toda escrita da gestão é registrada na trilha de auditoria, com autor, papel, data e hora                                    | —          | 03 §1      |
| `RN-02-22` | Nenhuma tela de gestão exibe a imagem real do Guerreiro(a) — a representação é o avatar                                      | 12         | 03 §12     |
| `RN-02-23` | Nenhuma recusa de consentimento exclui o Guerreiro(a) da atividade nem do lançamento                                         | 11         | 03 §12     |
| `RN-02-24` | Autoria de trilha, conteúdo, atividades da missão, marco e coleta é do Mestre, na App 09                                     | —          | 03 §§5, 11 |
| `RN-02-25` | No Ciclo 01 não há notificação por e-mail: todo retorno acontece dentro da plataforma                                        | —          | 03 §9      |

## 8. Modelo de dados

A App 03 é **consumidora**: todas as entidades que ela toca já estão definidas no PRD-01, no
PRD-07 (economia) e no PRD-08 (território). O que segue é o mapa do que a aplicação escreve.

```text
CADASTRA                 AGENDA E LANÇA          FILAS QUE TRATA
Guerreiro(a)                  Aula/Agenda             SolicitacaoDeParticipacao
Mestre                   Atividade               SolicitacaoDeDados
Apoiador                 Presenca                SolicitacaoDeLocal
Admin                    Resultado               SolicitacaoDoResponsavel
Responsavel              Lancamento              SugestaoOuProposta
VinculoResponsavel       PartidaDeQuiz           DesafioExtra
Credencial               Reserva
Equipe                                           CONFERE (leitura)
ComunidadeVirtual        ACERVO                  SerieDeColeta
Local                    ItemPatrimonial         DesafioDeColeta
Poder                    Emprestimo              Auditoria
                         Aporte
```

| Entidade      | Atributos essenciais                                                                                                                                                                |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Aula/Agenda` | comunidade, data, horário inicial, horário final, modalidade, ponto de apoio, atividade prevista, Mestre, situação (prevista, pendente de lastro, confirmada, realizada, cancelada) |

**Este PRD não cria entidade nova.** `Aula/Agenda` já existe no PRD-01 e recebe aqui os
atributos que sustentam duas decisões: **comunidade, data e horários** — que habilitam o App 01
e dão a comunidade do novo cadastro — e a **situação**, que distingue a atividade pendente de
lastro da confirmada.

A infração e a pontuação negativa são `OcorrenciaDeConduta`, entidade do núcleo (`RF-01-57`),
vinculada ao encontro e à atividade, ao Guerreiro(a) e ao motivo registrado. Correção de
lançamento é `Lancamento` de ajuste referenciando o original, conforme o PRD-07.

## 9. Contratos de API

A aplicação consome as convenções do PRD-01 — prefixo `/v1`, token de sessão, erro em formato
único, listagem paginada com filtro de comunidade, período e persona. As rotas de território e
de livro-razão são as dos PRD-08 e PRD-07 e não se repetem aqui.

| Método | Rota                                              | Autenticação    | Descrição                                                                   |
| ------ | ------------------------------------------------- | --------------- | --------------------------------------------------------------------------- |
| POST   | `/v1/guerreiros`                                  | Admin           | Cadastra Guerreiro(a) pela gestão                                           |
| POST   | `/v1/consentimentos/{id}/anexo`                   | Admin           | Anexa a digitalização do termo assinado no encontro                         |
| POST   | `/v1/mestres`                                     | Admin           | Cadastra Mestre com os links comprobatórios declarados                      |
| POST   | `/v1/apoiadores`                                  | Admin           | Cadastra Apoiador com os links e os termos de doação                        |
| POST   | `/v1/admins`                                      | Admin           | Inclui novo Admin manualmente                                               |
| GET    | `/v1/aulas/{id}/equipes`                          | Admin ou Mestre | Lista as equipes formadas no App 01 naquela aula                            |
| POST   | `/v1/poderes`                                     | Admin           | Mantém o catálogo de poderes                                                |
| GET    | `/v1/aulas/vigentes`                              | pública         | Aulas em curso na data e hora, para o App 01 identificar a comunidade       |
| GET    | `/v1/solicitacoes-de-participacao`                | Admin           | Fila das solicitações, com aporte declarado e comprovante                   |
| POST   | `/v1/solicitacoes-de-participacao/{id}/avaliacao` | Admin           | Aceita ou recusa, com parecer e autor                                       |
| GET    | `/v1/solicitacoes-de-dados`                       | Admin           | Fila dos pedidos de conjunto de dados                                       |
| POST   | `/v1/solicitacoes-de-dados/{id}/avaliacao`        | Admin           | Aprova ou recusa, com motivo, autor e o que foi entregue                    |
| GET    | `/v1/solicitacoes-de-chave`                       | Admin           | Fila dos pedidos de chave da Área do Apoiador Desenvolvedor                 |
| POST   | `/v1/solicitacoes-de-chave/{id}/avaliacao`        | Admin           | Aprova ou recusa, com parecer e autoria                                     |
| POST   | `/v1/chaves`                                      | Admin           | Emite a chave da solicitação aprovada e devolve o segredo uma vez           |
| GET    | `/v1/chaves`                                      | Admin           | Chaves emitidas, com prazo, URL apresentada e situação                      |
| DELETE | `/v1/chaves/{id}`                                 | Admin           | Revoga a chave, com motivo e autoria                                        |
| PUT    | `/v1/conteudo-institucional/{secao}`              | Admin           | Edita "Quem somos", "Contatos" ou "Como apoiar"                             |
| GET    | `/v1/solicitacoes-do-responsavel`                 | Admin           | Fila das solicitações vindas da App 07                                      |
| POST   | `/v1/solicitacoes-do-responsavel/{id}/tratamento` | Admin           | Registra o desfecho, com quem tratou e quando                               |
| GET    | `/v1/sugestoes`                                   | Admin           | Fila única de sugestões e propostas das Apps 05, 07, 08, 09                 |
| POST   | `/v1/sugestoes/{id}/avaliacao`                    | Admin           | Muda o status e registra o retorno a quem propôs                            |
| GET    | `/v1/desafios-extras/pendentes`                   | Admin           | Desafios já validados pelo Mestre, aguardando aprovação                     |
| POST   | `/v1/desafios-extras/{id}/aprovacao`              | Admin           | Aprova, exigindo lastro registrado, ou recusa com motivo                    |
| POST   | `/v1/atividades`                                  | Admin           | Cadastra atividade com pontuação, recompensa e recursos                     |
| POST   | `/v1/aulas`                                       | Admin           | Agenda a aula com comunidade, data e horários, e dispara a reserva          |
| POST   | `/v1/aulas/{id}/lancamentos`                      | Admin           | Lança a atividade realizada e os resultados, convertendo a reserva em baixa |
| POST   | `/v1/aulas/{id}/cancelamento`                     | Admin ou Mestre | Cancela a aula agendada com motivo e libera a reserva                       |
| POST   | `/v1/aulas/{id}/presencas`                        | Admin           | Confirma a presença que faltou, com registro de quem confirmou              |
| POST   | `/v1/aulas/{id}/presencas/{id}/anulacao`          | Admin           | Anula a presença registrada por engano, com motivo, sem apagar o registro   |
| POST   | `/v1/ocorrencias-de-conduta`                      | Mestre ou Admin | Registra infração e a pontuação negativa correspondente                     |
| GET    | `/v1/lancamentos`                                 | Admin           | Lançamentos de um ponto de apoio, filtro obrigatório de ponto de apoio      |
| GET    | `/v1/painel-do-dia`                               | Mestre ou Admin | Estado do encontro em andamento, em leitura                                 |
| POST   | `/v1/partidas-de-quiz`                            | Mestre ou Admin | Abre a partida com banco de perguntas e equipes                             |
| POST   | `/v1/partidas-de-quiz/{id}/perguntas`             | Mestre ou Admin | Dá o _start_ da pergunta corrente                                           |
| POST   | `/v1/partidas-de-quiz/{id}/resultado`             | Mestre ou Admin | Libera o resultado da pergunta no ar, sem creditar                          |
| POST   | `/v1/partidas-de-quiz/{id}/anulacoes`             | Mestre ou Admin | Anula a pergunta contestada, sem crédito para ninguém                       |
| GET    | `/v1/partidas-de-quiz/{id}`                       | Mestre ou Admin | Estado da partida, sondado a cada 2 segundos                                |
| POST   | `/v1/partidas-de-quiz/{id}/encerramento`          | Mestre ou Admin | Encerra a partida e lança a pontuação                                       |
| GET    | `/v1/entregas`                                    | Admin           | Lê as entregas confirmadas pelo Mestre, com tipo de recurso e baixa         |
| GET    | `/v1/auditoria`                                   | Admin           | Trilha de auditoria, com filtro por autor e período                         |

Erros previstos: agenda de aula sem comunidade ou sem horário final (422); consulta de aulas
vigentes fora de qualquer janela agendada (200 com lista vazia — é o que faz o App 01 não
abrir); cadastro de Mestre ou Apoiador sem link comprobatório (422); tentativa de editar equipe
formada no App 01 (403); quarto responsável do mesmo
Guerreiro(a) (422); aprovação de desafio extra sem validação do Mestre (409) ou sem lastro
(422); tentativa de editar lançamento (405); escrita de Mestre em rota de gestão que não seja a
do quiz ou a de ocorrência (403); condução de partida por Mestre que não ministra aquela aula
(403); anulação de presença já anulada (409) ou sem motivo (422); listagem de lançamentos sem o
filtro de ponto de apoio (422).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**: o painel do dia é operado **em pé, no celular**, andando
  entre as bancadas — é o caso de uso que dimensiona a interface, não a mesa do escritório.
- Painel do dia legível em tela pequena, com o estado do encontro visível sem rolagem longa.
- Atualização do painel por sondagem periódica a cada 10 segundos (documento 03 §1), tolerante
  a rede instável, sem perder o que já foi lançado.
- Quiz ao Vivo sincronizado entre dispositivos por sondagem periódica a cada 2 segundos
  (documento 03 §1), com desempate por ordem de chegada da resposta no servidor, tolerando
  queda e volta de aparelho durante a partida.
- Lançamento em lote de uma turma inteira sem recarregar a tela a cada Guerreiro(a).
- Escrita idempotente: reenviar o mesmo lançamento por falha de rede não duplica o registro.
- Desempenho em celular modesto, o mesmo do ponto de apoio.
- Linguagem simples nas telas e nos erros; nenhum jargão de TI, porque o Mestre pode ser de
  humanas, artes, esportes ou cultura.
- Acessibilidade digital no piso do documento 15 — **WCAG 2.2 AA**; idioma pt-BR; código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                      | Finalidade                        | Base legal        | Retenção                 | Quem acessa          |
| ---------------------------------- | --------------------------------- | ----------------- | ------------------------ | -------------------- |
| Cadastro do Guerreiro(a)           | Identificação e operação          | consentimento     | enquanto durar o vínculo | gestão e responsável |
| Presença e resultado de atividade  | Registro da participação          | consentimento     | enquanto durar o vínculo | gestão e responsável |
| Infração e pontuação negativa      | Aplicação do Código de Conduta    | interesse público | enquanto durar o vínculo | gestão e responsável |
| Contato do responsável             | Canal oficial com a família       | consentimento     | enquanto durar o vínculo | gestão               |
| Artefatos comprobatórios de adulto | Provar habilidade ou apoio        | consentimento     | enquanto durar o vínculo | gestão e visitante   |
| Solicitação de participação        | Avaliar quem pede para participar | consentimento     | enquanto durar a fila    | gestão               |
| Solicitação de dados               | Avaliar e registrar a entrega     | consentimento     | enquanto durar a fila    | gestão               |
| Auditoria das ações de gestão      | Rastreabilidade                   | interesse público | permanente               | Admin                |

- A gestão **não vê a imagem do Guerreiro(a)**: a aplicação mostra avatar e nick, e a
  conferência biométrica acontece no núcleo, sem devolver imagem nem _template_.
- O responsável consulta pela App 07 **quem acessou** os dados da criança; é a trilha de
  auditoria desta aplicação que responde a isso.
- Pedido de acesso, correção ou exclusão chega pela fila da App 07 e é tratado aqui, com
  protocolo e desfecho registrados — **o registro de dado do território é despersonalizado, não
  apagado**, e a
  resposta ao responsável diz isso.
- Toda tela que coleta dado traz o aviso discreto do que está sendo coletado, com acesso à área
  detalhada de destino e uso.
- O registro de infração é dado sensível de criança: fica restrito à gestão e ao responsável do
  Guerreiro(a), nunca aparece em rota pública, ranking ou vitrine.

## 12. Critérios de aceite e métricas

- Fora da janela de qualquer aula agendada, a consulta de aulas vigentes volta vazia e o App 01
  não abre; dentro dela, volta a aula com a sua comunidade.
- Duas aulas presenciais de comunidades diferentes no mesmo horário aparecem ambas na consulta,
  e é o App 01 que pergunta em qual está operando.
- Guerreiro(a) cadastrado no onboarding nasce vinculado à comunidade da aula, sem tê-la
  informado, e não existe tela de transferência de comunidade no Ciclo 01.
- Cadastro de Mestre sem nenhum link comprobatório declarado é recusado.
- Solicitação de participação aceita **não** cria acesso: o Mestre só existe depois do cadastro
  feito pelo Admin.
- Equipe com seis integrantes, ou com dois familiares de 17 anos ou mais, é recusada.
- Quarto vínculo de responsável ao mesmo Guerreiro(a) é recusado e os três anteriores seguem.
- Atividade sem lastro fica pendente e a falta aparece, em moedas, na vitrine pública, na área
  do Apoiador e na área do Mestre da trilha.
- Mestre que assume a necessidade pela App 09 gera aporte por absorção em seu nome, e a
  atividade passa a confirmada sem intervenção de Admin.
- Lançamento da atividade realizada baixa exatamente os recursos reservados no agendamento.
- Tentativa de editar um lançamento devolve 405, e a correção aparece como ajuste com o
  original preservado.
- Presença registrada pelo App 01 aparece no painel do dia sem lançamento manual; a confirmação
  manual grava quem confirmou.
- Painel do dia mostra o saldo dos tipos de recurso do ponto de apoio e os lançamentos
  pendentes do encontro em andamento.
- Mestre autenticado lê o painel do dia, abre e conduz a partida de quiz da sua aula, e recebe
  403 em qualquer outra escrita de gestão.
- Mestre que tenta conduzir a partida de uma aula que não é dele recebe 403.
- Pontuação negativa lançada pelo Mestre é efetivada na hora, sem aprovação de Admin, e aparece
  na trilha de auditoria com o nome dele.
- Partida de quiz com um aparelho fora do ar durante a pergunta é concluída, e o aparelho volta
  na pergunta corrente.
- Desafio extra sem validação do Mestre não aparece na fila de aprovação; com validação e sem
  lastro, a aprovação é recusada.
- Nenhuma tela da gestão exibe imagem real de Guerreiro(a).
- Toda escrita bem-sucedida aparece na trilha de auditoria com autor, papel e data e hora.

Hipóteses do Ciclo 01 (documento 10): este PRD é o instrumento de medição de **H3** — o
confronto entre lastro registrado e recursos necessários acontece no agendamento desta
aplicação. Ele também **habilita H1**, porque sem a liberação do App 01 não há cadastro a
contar, e dá à gestão a distribuição etária que **H4** observa.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                                      | Gravada em         | Linha do doc 09                                                |
| ------------------------------------------------------------------------------------------------------------ | ------------------ | -------------------------------------------------------------- |
| Não há comunidade default: a comunidade e a janela do App 01 vêm da aula agendada                            | 02 §1, 03 §§3, 5   | Comunidade do onboarding                                       |
| Fim de ciclo é ato de Admin na gestão, isolado, e não congela indicador                                      | 02 §1              | Gatilho do fim de ciclo                                        |
| No Ciclo 01 o Guerreiro(a) não muda de comunidade                                                            | 02 §1              | Troca de comunidade no Ciclo 01                                |
| Quiz ao Vivo conduzido pelo Mestre que ministra a aula, além do Admin                                        | 03 §§5, 11 e 05 §5 | Autenticação e arquitetura da API                              |
| Pontuação negativa lançada por Mestre e por Admin, sem revisão de terceiro                                   | 02 §4, 03 §§5, 11  | Lançamento de pontuação negativa                               |
| Falta de lastro publica necessidade na vitrine e nas Apps 08 e 09, com absorção assumida dali                | 04 §1              | Economia de recursos e ledger                                  |
| Dados mínimos e prazo de 7 dias da solicitação de participação                                               | 02 §1              | Dados e prazo da solicitação de participação                   |
| Prazo de 7 dias para as solicitações dos responsáveis                                                        | 03 §9              | Canal de comunicação com os responsáveis                       |
| Sem notificação por e-mail no Ciclo 01                                                                       | 03 §9              | Notificações no Ciclo 01                                       |
| Persona primária tratada por Guerreiro ou Guerreira                                                          | 02 §1              | Termo da persona primária                                      |
| Equipe da trilha homologada pelo Mestre na App 01, o aparelho do encontro                                    | 02 §5, 03 §5       | Onde a equipe da trilha é formada e homologada                 |
| Amostra da auditoria de coleta: 10% da semana por série ativa, mínimo de um                                  | 02 §1              | Composição da amostra de auditoria de coleta                   |
| Pontuação da atividade vem do motor do documento 11; o cadastro escolhe o tipo                               | 11 §5              | Pontuação da atividade cadastrada                              |
| Atividade avulsa credita no poder que declara, sem missão nem trilha em que pousar                           | 11 §5              | Pontuação da atividade cadastrada                              |
| Atividade avulsa não declara recurso — quem declara e reserva é a aula                                       | 04 §1, 11 §5       | Recurso da atividade avulsa                                    |
| Acervo permanente no Ciclo 01: tombamento, ficha de vida e badge                                             | 05 §3              | Estratégia de conservação do acervo permanente                 |
| Admin desativa e reativa ponto de apoio, bloqueado por aula futura e por saldo remanescente                  | 05 §2              | Desativação de ponto de apoio                                  |
| "Publicado" no `RF-02-17` é a trilha em situação `publicada` — o desafio não tem situação própria            | PRD-08 §8          | não se aplica — correção de redação                            |
| Processos de auditoria ainda não implementados vão ao Ciclo 02, exceto o histórico de acessos do responsável | 02 §3.2            | Processos de auditoria ainda não implementados vão ao Ciclo 02 |

A **trilha de auditoria das ações de Admin**, questão que o documento 08 listava para este PRD,
foi definida no PRD-01 — a App 03 apenas a consulta.

## 14. Pendências que permanecem

- **Tipificação das infrações** que embasam a pontuação negativa — quem lança já está decidido;
  o catálogo de motivos nasce do Código de Conduta co-criado com os Guerreiros e Guerreiras, e
  por isso não é decisão a tomar antes da primeira turma.
- **`RF-02-71` não tem rota**: este PRD não declara a leitura da autoria — trilha, missão e
  atividade — pelo Admin, e o `GET /trilhas/{id}` do PRD-09 é público e serve trilha publicada,
  não o rascunho que o Admin precisa consultar. Sem decisão, o Admin não tem por onde ler o que
  os Mestres autoram.
- **Três consequências do adiamento da auditoria ao Ciclo 02, sobre o que já está
  implementado**: o registro de coleta "a conferir" fica sem validação do Mestre, a trilha
  publicada fica sem despublicação, e a trilha de auditoria fica sem consumidor nesta
  aplicação.

Quatro saíram desta lista, decididas e gravadas na §13: a composição da amostra de auditoria, a
pontuação da atividade cadastrada, a estratégia de conservação do acervo — que reduziu o escopo
de `RF-02-54` a `RF-02-55` — e a **triagem do formulário público**, resolvida pelos números do
freio por origem: 3 envios por hora, com atraso progressivo e sem CAPTCHA (documento 03 §8).

## 15. Rastreabilidade

| Requisito                | Origem                                                    |
| ------------------------ | --------------------------------------------------------- |
| `RF-02-01` a `RF-02-10`  | 02 §§1, 5 e 03 §5 (cadastros e governança de personas)    |
| `RF-02-99` e `RF-02-100` | 02 §1 e 11 §5 (encerramento do ciclo e seus dois efeitos) |
| `RF-02-11` a `RF-02-17`  | 02 §1, 03 §5 e PRD-08 (comunidade, default e território)  |
| `RF-02-18` a `RF-02-20`  | 02 §1 e 03 §§5, 8 (solicitação de participação)           |
| `RF-02-77` a `RF-02-79`  | 03 §12.3 (entrega de dados aprovada por Admin)            |
| `RF-02-93`               | 03 §12.3 (critério de aprovação da entrega)               |
| `RF-02-80`               | 03 §8 (conteúdo institucional da vitrine)                 |
| `RF-02-83` a `RF-02-86`  | 02 §1 e 04 §2 (pré-cadastro, comprovante e homologação)   |
| `RF-02-87` a `RF-02-92`  | 03 §§1, 8 (solicitação, emissão, prazo e revogação)       |
| `RF-02-21` e `RF-02-22`  | PRD-08 (solicitação de novo local)                        |
| `RF-02-23` e `RF-02-24`  | 03 §9 (solicitações da área do responsável)               |
| `RF-02-25` e `RF-02-26`  | 03 §§7, 9, 10, 11 (fila única de sugestões e propostas)   |
| `RF-02-27` e `RF-02-28`  | 04 §3 e PRD-07 (desafios extras e lastro)                 |
| `RF-02-29` a `RF-02-32`  | 04 §1 e PRD-07 (atividade, agenda e regra de lastro)      |
| `RF-02-33` a `RF-02-35`  | 02 §4 e 11 §5 (resultados e motor de pontuação)           |
| `RF-02-36`               | 03 §§3, 5 (presença vinda do onboarding)                  |
| `RF-02-37` a `RF-02-40`  | 02 §4, 05 §3 e 13 (pontuação negativa e ajuste)           |
| `RF-02-41` a `RF-02-49`  | 05 §4 e 03 §5 (encontro assíncrono e painel do dia)       |
| `RF-02-50` a `RF-02-56`  | 05 §3 e PRD-07 (acervo, regime misto e patrimônio)        |
| `RF-02-96` e `RF-02-97`  | 05 §2 e PRD-07 (desativação, reativação e transferência)  |
| `RF-02-57` e `RF-02-58`  | 04 §1 e PRD-07 (aportes e necessidades)                   |
| `RF-02-59` a `RF-02-62`  | 05 §5 (Quiz ao Vivo)                                      |
| `RF-02-72` e `RF-02-73`  | 05 §5 e 11 §5 (regras e pontuação da partida)             |
| `RF-02-74` a `RF-02-76`  | 03 §§5, 7, 11 (auditoria mensal do corpus e das trilhas)  |
| `RF-02-63`               | PRD-01 (trilha de auditoria)                              |
| `RF-02-64`               | 03 §12 (aviso visível de coleta e área detalhada)         |
| `RF-02-70`               | 03 §11 e PRD-09 (auditoria das trilhas publicadas)        |
| `RF-02-71`               | 11 §§2, 4 e PRD-09 (autoria da atividade e do marco)      |
| `RF-02-65`               | 02 §1 (prazo de 7 dias da solicitação de participação)    |
| `RF-02-66`               | 03 §9 (prazo de 7 dias da solicitação do responsável)     |
| `RF-02-67`               | 04 §1 e PRD-07 (suprido o lastro, confirma e reserva)     |
| `RF-02-68` e `RF-02-69`  | 03 §3.3 (digitalização do termo anexada pela gestão)      |
