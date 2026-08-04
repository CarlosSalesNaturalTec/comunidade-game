# PRD-02 — App 03: Frontend de Gestão

## 1. Identificação

| Campo            | Valor                                     |
| ---------------- | ----------------------------------------- |
| PRD              | PRD-02                                    |
| Aplicação        | App 03 — Gestão administrativa            |
| Onda             | 2                                         |
| Situação         | em revisão                                |
| Versão e data    | v1 — 2026-08-04                           |
| Depende de       | PRD-01                                    |
| Documentos-fonte | 03 §§5, 11, 12, 04 §§1–3, 05 §§2–5, 02 §4 |

## 2. Contexto e objetivo

A App 03 é a mesa de comando do projeto. Nenhuma outra aplicação da etapa abre sem ela: é aqui
que o Admin cria a Comunidade Virtual, define a comunidade default e libera o App 01; é aqui
que Mestres, Apoiadores, responsáveis e equipes são cadastrados; e é aqui que a atividade
ganha lastro antes de existir.

Ela também é a aplicação do **dia da aula**. Como o encontro é assíncrono — cada jogador chega
na sua hora e avança no seu ponto —, o painel do dia substitui o controle visual de uma turma
em bloco: quem chegou, em que ponto cada equipe está, quem aguarda aparelho, o que já foi
lançado e o que falta lançar antes de a aula acabar.

A fronteira com a App 09 é o critério de tudo o que entra aqui: **a gestão cadastra, aprova,
lança e confere; a autoria é do Mestre e vive lá**. Nesta aplicação o Mestre só lê o painel do
dia, para conduzir o encontro em andamento.

## 3. Escopo

### 3.1 Dentro do escopo

- Cadastro de personas: jogadores, Mestres, Apoiadores, responsáveis, Admins e equipes.
- Criação da Comunidade Virtual, marcação da default e **liberação do App 01**.
- Conferência e transferência do vínculo do jogador entre comunidades, com data.
- Cadastro de locais do território e tratamento das solicitações de novo local.
- Catálogo de poderes do Ciclo 01 e cadastro de atividades com pontuação, recompensas e
  recursos necessários.
- Agenda de aulas on-line e presenciais, com reserva de recursos e bloqueio sem lastro.
- Lançamento das atividades realizadas e das entradas manuais do dia.
- Conferência das presenças vindas do App 01 e ajuste manual.
- Painel do dia do encontro em andamento, incluindo saldos e devoluções pendentes.
- Condução do **Quiz ao Vivo**, com o banco de perguntas cadastrado pelo Mestre na App 09.
- Controle do acervo didático: entrega dos exemplares Alpha, tombamento, empréstimo de bancada
  e conferência de inventário.
- Gestão de recursos: registro e homologação de aportes e visão das necessidades em aberto.
- Filas de avaliação: solicitações de participação, solicitações dos responsáveis, desafios
  extras dos Apoiadores e a fila única de sugestões e propostas.
- Consulta da trilha de auditoria das ações de gestão.

### 3.2 Fora do escopo

- **Autoria de trilha, ponto de trilha, conteúdo, quiz e desafio de coleta** — é a bancada do
  Mestre na App 09 (PRD-09). A App 03 apenas acompanha o que foi publicado.
- **Lançamento das atividades do próprio Mestre** — ele lança na App 09; aqui o Admin lança as
  demais e corrige o que precisar.
- Regras de pontuação, cadência de coleta e valoração de aporte: normatizadas nos documentos
  11, 02 e 04 e detalhadas nos PRD-08 e PRD-07.
- Telas de coleta do jogador (PRD-05) e conversa de cadastro do onboarding (PRD-04).
- Notificação ativa por e-mail às filas — pendência do canal com os responsáveis.
- Relatório de efetividade ao Apoiador: é entrega da App 08 (PRD-14).

## 4. Personas e permissões

| Persona   | O que faz nesta aplicação                                                             | O que não pode fazer                                              |
| --------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Admin     | Tudo: cadastros, aprovações, agenda, lançamentos, filas, acervo, recursos e auditoria | Registrar coleta no lugar do jogador; criar conteúdo de trilha    |
| Mestre    | Lê o painel do dia do encontro em andamento                                           | Escrever em qualquer rota de gestão — o que é dele fica na App 09 |
| Visitante | Nada: a aplicação é inteiramente autenticada                                          | Acessar qualquer tela                                             |

O Mestre entra por login social, como todo adulto, e recebe apenas a leitura do painel do dia.

## 5. Jornadas principais

### 5.1 Abrir a comunidade e liberar o onboarding

1. O Admin cria a **Comunidade Virtual**, que nasce vazia.
2. Marca uma delas como **comunidade default do onboarding**.
3. **Libera o App 01**, em ato próprio e registrado — sem comunidade default marcada, a
   liberação é recusada.
4. A partir daí o App 01 opera e todo jogador cadastrado nasce vinculado à comunidade default.
5. Suspender a liberação interrompe novos cadastros sem afetar quem já entrou.

### 5.2 Avaliar uma solicitação de participação

1. Pessoa ou instituição envia o formulário público da vitrine (App 06).
2. A solicitação entra na fila com data, contato, pretensão, links comprobatórios e
   justificativa, no status **recebida**.
3. O Admin avalia, registra o parecer e conclui como **aceita** ou **recusada**, e a aplicação
   grava quem tratou e quando.
4. Aceita, a solicitação **abre o cadastro** de Mestre ou Apoiador já preenchido com o que veio
   do formulário — o cadastro é o ato do Admin, não da solicitação.
5. Recusada, nada é criado; o solicitante recebe o status, sem acesso à plataforma.

### 5.3 Cadastrar responsável e vincular jogadores

1. O responsável se apresenta pessoalmente no encontro e informa e-mail e as crianças sob sua
   responsabilidade.
2. O Admin cadastra o responsável e vincula **jogadores já cadastrados**, com o grau de
   parentesco de cada vínculo.
3. O quarto vínculo para o mesmo jogador é recusado, e os três anteriores seguem válidos.
4. Sem conta Google, o Admin cria a credencial de usuário e senha provisória.
5. O mesmo cadastro pode ter sido feito pelo Mestre na App 09 — a aplicação mostra quem o fez.

### 5.4 Planejar a aula e reservar os recursos

1. O Admin agenda a aula, on-line ou presencial, com a atividade prevista e o ponto de apoio.
2. A aplicação consulta o livro-razão e **reserva** os recursos necessários.
3. Faltando lastro, o agendamento é **recusado** com a lista do que falta, que entra na visão
   pública de necessidades.
4. Suprida a necessidade por aporte homologado, o Admin repete o agendamento.

### 5.5 Conduzir o encontro pelo painel do dia

1. Aberto o encontro, o painel mostra **quem já chegou**, com as presenças que o App 01
   registrou automaticamente.
2. Mostra, por equipe, **em que ponto de trilha cada uma está** e quem está aguardando
   aparelho.
3. Mostra a atividade prevista, os recursos providos, o **saldo de kits MDF** e de exemplares
   Alpha, e as **devoluções pendentes** de bancada.
4. Mostra os **lançamentos pendentes** — o que precisa ser lançado antes de a aula terminar.
5. O Mestre lê esse mesmo painel para circular entre as equipes; tudo o que ele escreve
   continua na App 09.
6. Presença que o reconhecimento não capturou é confirmada manualmente, com registro de quem
   confirmou.

### 5.6 Lançar a atividade realizada e as entradas do dia

1. O Admin lança a atividade realizada: data, mentores, jogadores e equipes participantes.
2. Atribui o resultado de cada participante — **realizada**, **realizada com mérito** ou
   **mérito extra por auxílio aos colegas**.
3. Lança as entradas manuais do dia: presença, pontuação extra a quem ajudou o colega e
   **infração ocorrida na aula**.
4. O lançamento converte a reserva de recursos em **baixa** no livro-razão.
5. Toda a escrita é auditada com autor, papel, data e hora.

### 5.7 Conduzir o Quiz ao Vivo

1. O Admin abre a partida escolhendo o banco de perguntas do Mestre curador e as **equipes
   presentes** no encontro.
2. Ao dar o _start_, a pergunta aparece **simultaneamente** nos dispositivos logados na aula.
3. Cada equipe se consulta e responde pela App 05.
4. A aplicação apura a **primeira resposta correta** por ordem de chegada e mostra o resultado.
5. Encerrada a partida, a pontuação é lançada automaticamente para as equipes.
6. Dispositivo que caiu volta na pergunta corrente, sem travar a partida.

### 5.8 Tratar as filas

1. **Desafio extra** proposto na App 08 chega já validado pelo Mestre da trilha; o Admin
   aprova ou recusa, e a aprovação só é aceita com o **lastro da recompensa registrado**.
2. **Solicitação do responsável** vinda da App 07 chega com protocolo; o Admin trata, registra
   o desfecho e a aplicação grava quem tratou e quando.
3. **Sugestões e propostas** das Apps 05, 07, 08 e 09 chegam a uma **fila única**, avaliadas com
   status e retorno a quem propôs.
4. **Solicitação de novo local** vinda da App 05 aparece com alerta enquanto está em aberto; o
   Admin aprova, criando o local, ou recusa com motivo — o Mestre da trilha faz o mesmo na
   App 09.

## 6. Requisitos funcionais

### 6.1 Cadastros e catálogo

| ID         | Requisito                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-01` | Admin cadastra e edita jogadores, com nome, nascimento, nick, avatar e situação                 | essencial  |
| `RF-02-02` | Admin cadastra Mestre anexando currículo, portfólios, redes sociais e documentos externos       | essencial  |
| `RF-02-03` | Admin cadastra Apoiador anexando os mesmos artefatos e os termos de doação                      | essencial  |
| `RF-02-04` | Aplicação recusa o cadastro de Mestre ou Apoiador sem ao menos um artefato comprobatório        | essencial  |
| `RF-02-05` | Admin inclui novo Admin manualmente                                                             | essencial  |
| `RF-02-06` | Admin cadastra responsável e vincula jogadores já cadastrados, com grau de parentesco           | essencial  |
| `RF-02-07` | Admin cria credencial de usuário e senha provisória para adulto sem conta social                | essencial  |
| `RF-02-08` | Admin cadastra equipe de até cinco integrantes, indicando a composição permitida pela atividade | essencial  |
| `RF-02-09` | Aplicação recusa equipe com mais de um familiar de 17 anos ou mais                              | essencial  |
| `RF-02-10` | Admin mantém o catálogo de poderes do ciclo                                                     | essencial  |
| `RF-02-11` | Admin cria Comunidade Virtual, que nasce vazia                                                  | essencial  |
| `RF-02-12` | Admin marca exatamente uma comunidade como default do onboarding                                | essencial  |
| `RF-02-13` | Admin libera e suspende o funcionamento do App 01, em ato registrado                            | essencial  |
| `RF-02-14` | Aplicação recusa a liberação do App 01 enquanto não houver comunidade default marcada           | essencial  |
| `RF-02-15` | Admin transfere jogador entre comunidades, com a data da mudança preservada                     | essencial  |
| `RF-02-16` | Admin cadastra locais do território na hierarquia da comunidade                                 | essencial  |
| `RF-02-17` | Admin consulta os desafios de coleta publicados, com cadência, vigência e séries ativas         | desejável  |

### 6.2 Filas de avaliação

| ID         | Requisito                                                                                      | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-18` | Fila de solicitações de participação exibe data, contato, pretensão, links e justificativa     | essencial  |
| `RF-02-19` | Admin conclui a solicitação como aceita ou recusada, com parecer, autor e data registrados     | essencial  |
| `RF-02-20` | Solicitação aceita abre o cadastro de Mestre ou Apoiador pré-preenchido, sem criar acesso      | essencial  |
| `RF-02-21` | Fila de solicitações de novo local alerta enquanto houver solicitação em aberto                | essencial  |
| `RF-02-22` | Admin aprova a solicitação de local, criando-o, ou recusa com motivo                           | essencial  |
| `RF-02-23` | Fila de solicitações dos responsáveis exibe protocolo, tipo, prazo e situação                  | essencial  |
| `RF-02-24` | Admin registra o desfecho da solicitação do responsável, com quem tratou e quando              | essencial  |
| `RF-02-25` | Fila única reúne sugestões e propostas das Apps 05, 07, 08 e 09, identificando autor e persona | essencial  |
| `RF-02-26` | Admin avalia a sugestão, muda o status e registra o retorno a quem propôs                      | essencial  |
| `RF-02-27` | Fila de desafios extras mostra apenas os já validados pelo Mestre da trilha                    | essencial  |
| `RF-02-28` | Admin aprova o desafio extra, e a aprovação é recusada sem o lastro da recompensa registrado   | essencial  |

### 6.3 Atividades, agenda e lançamentos

| ID         | Requisito                                                                                | Prioridade |
| ---------- | ---------------------------------------------------------------------------------------- | ---------- |
| `RF-02-29` | Admin cadastra atividade com pontuação, recompensas e recursos necessários               | essencial  |
| `RF-02-30` | Admin agenda aula on-line ou presencial, com atividade prevista e ponto de apoio         | essencial  |
| `RF-02-31` | Agendamento reserva os recursos necessários no livro-razão                               | essencial  |
| `RF-02-32` | Agendamento sem lastro é recusado, com a lista do que falta                              | essencial  |
| `RF-02-33` | Admin lança atividade realizada com data, mentores, jogadores e equipes                  | essencial  |
| `RF-02-34` | Lançamento atribui a cada participante realizada, com mérito ou mérito extra por auxílio | essencial  |
| `RF-02-35` | Lançamento da atividade realizada converte a reserva em baixa de recursos                | essencial  |
| `RF-02-36` | Admin confere as presenças vindas do App 01 e ajusta manualmente, com registro do ajuste | essencial  |
| `RF-02-37` | Admin registra infração ocorrida na aula, vinculada ao encontro e ao jogador             | essencial  |
| `RF-02-38` | Admin lança pontuação negativa com motivo e referência ao item do Código de Conduta      | essencial  |
| `RF-02-39` | Admin lança pontuação extra ao jogador que ajudou o colega                               | essencial  |
| `RF-02-40` | Admin corrige lançamento por novo lançamento de ajuste, sem apagar o original            | essencial  |

### 6.4 Painel do dia

| ID         | Requisito                                                                    | Prioridade |
| ---------- | ---------------------------------------------------------------------------- | ---------- |
| `RF-02-41` | Painel do dia lista quem já chegou, com a presença registrada pelo App 01    | essencial  |
| `RF-02-42` | Painel mostra, por equipe, o ponto de trilha em que ela está                 | essencial  |
| `RF-02-43` | Painel mostra quem está aguardando aparelho                                  | essencial  |
| `RF-02-44` | Painel mostra atividade prevista e recursos providos do encontro             | essencial  |
| `RF-02-45` | Painel mostra o saldo de kits MDF e de exemplares da linha Alpha             | essencial  |
| `RF-02-46` | Painel mostra as devoluções de bancada pendentes antes do fim da aula        | essencial  |
| `RF-02-47` | Painel lista os lançamentos pendentes do encontro                            | essencial  |
| `RF-02-48` | Painel atualiza sozinho durante o encontro, sem recarga manual               | essencial  |
| `RF-02-49` | Mestre acessa o painel do dia em leitura e recebe recusa em qualquer escrita | essencial  |

### 6.5 Acervo, recursos e Quiz ao Vivo

| ID         | Requisito                                                                                          | Prioridade |
| ---------- | -------------------------------------------------------------------------------------------------- | ---------- |
| `RF-02-50` | Admin registra a entrega do exemplar Alpha na abertura da trilha, com baixa definitiva             | essencial  |
| `RF-02-51` | Admin registra a entrega da camisa ao jogador inscrito, com baixa definitiva                       | essencial  |
| `RF-02-52` | Admin tomba o exemplar permanente com título, tombo, ponto de apoio e responsável designado        | essencial  |
| `RF-02-53` | Aplicação mantém a ficha de vida do exemplar, com estado de conservação e histórico de uso         | essencial  |
| `RF-02-54` | Gestão registra empréstimo de bancada e devolução, com estado de conservação                       | essencial  |
| `RF-02-55` | Perda ou dano gera necessidade de reposição, sem débito ao jogador nem à família                   | essencial  |
| `RF-02-56` | Admin realiza a conferência de inventário do módulo e publica o resultado na prestação de contas   | desejável  |
| `RF-02-57` | Admin registra e homologa aporte com provedor, tipo, comprovante e valor em moedas                 | essencial  |
| `RF-02-58` | Aplicação exibe as necessidades de recurso em aberto das atividades previstas                      | essencial  |
| `RF-02-59` | Admin abre partida de Quiz ao Vivo com o banco do Mestre curador e as equipes presentes            | essencial  |
| `RF-02-60` | Partida exibe a pergunta simultaneamente nos dispositivos logados na aula                          | essencial  |
| `RF-02-61` | Partida apura a primeira resposta correta por ordem de chegada e mostra o resultado                | essencial  |
| `RF-02-62` | Encerrada a partida, a pontuação é lançada automaticamente às equipes                              | essencial  |
| `RF-02-63` | Admin consulta a trilha de auditoria das ações de gestão, com filtro por autor, período e entidade | essencial  |
| `RF-02-64` | Toda tela que coleta dado exibe o aviso discreto e o acesso à área detalhada de direitos           | essencial  |

## 7. Regras de negócio

| ID         | Regra                                                                                          | Invariante | Fonte      |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------- | ---------- |
| `RN-02-01` | Mestre e Apoiador são cadastrados só por Admin, com artefato comprobatório anexado             | 3          | 02 §1      |
| `RN-02-02` | Novo Admin só entra por inclusão manual de outro Admin                                         | 3          | 02 §1      |
| `RN-02-03` | Solicitação de participação não cria cadastro nem acesso                                       | 3          | 02 §1      |
| `RN-02-04` | Comunidade Virtual é criada apenas por Admin e nasce vazia                                     | 4          | 02 §1      |
| `RN-02-05` | Sem comunidade default marcada, o App 01 não opera                                             | 4          | 02 §1      |
| `RN-02-06` | Transferência de comunidade preserva a data — o dado pertence à comunidade vigente no registro | 4          | 02 §1      |
| `RN-02-07` | Equipe tem no máximo cinco integrantes e no máximo um familiar de 17 anos ou mais              | 15         | 02 §5      |
| `RN-02-08` | Cada jogador tem no máximo três responsáveis, com grau de parentesco em texto livre            | 3          | 02 §1      |
| `RN-02-09` | Nenhuma atividade é agendável sem lastro dos recursos                                          | 9          | 04 §1      |
| `RN-02-10` | Desafio extra só é aprovado por Admin depois da validação do Mestre da trilha                  | —          | 04 §3      |
| `RN-02-11` | Desafio extra só é publicado com o lastro da recompensa registrado                             | 9          | 04 §3      |
| `RN-02-12` | Lançamento não é editado nem apagado: correção é novo lançamento de ajuste                     | —          | 04 §1      |
| `RN-02-13` | Pontuação negativa aplica o Código de Conduta e exige motivo registrado                        | —          | 02 §4      |
| `RN-02-14` | Descuido acidental com material comum não é infração e não gera pontuação negativa             | —          | 05 §3      |
| `RN-02-15` | Sobre o livro próprio do jogador não incide pontuação negativa em hipótese alguma              | —          | 05 §3      |
| `RN-02-16` | Perda ou dano de material comum não gera débito ao jogador nem à família                       | —          | 05 §3      |
| `RN-02-17` | Exemplar da linha Alpha e camisa entregues têm baixa definitiva no livro-razão                 | —          | 05 §3      |
| `RN-02-18` | Exemplar permanente não sai do ponto de apoio: o uso é de bancada, com retirada registrada     | —          | 05 §3      |
| `RN-02-19` | Aporte aparece publicamente em moedas da plataforma, nunca em reais                            | 16         | 04 §1      |
| `RN-02-20` | Mestre acessa esta aplicação apenas em leitura do painel do dia                                | —          | 03 §5      |
| `RN-02-21` | Toda escrita da gestão é registrada na trilha de auditoria, com autor, papel, data e hora      | —          | 03 §1      |
| `RN-02-22` | Nenhuma tela de gestão exibe a imagem real do jogador — a representação é o avatar             | 12         | 03 §12     |
| `RN-02-23` | Nenhuma recusa de consentimento exclui o jogador da atividade nem do lançamento                | 11         | 03 §12     |
| `RN-02-24` | Autoria de trilha, conteúdo e desafio de coleta é do Mestre, na App 09                         | —          | 03 §§5, 11 |

## 8. Modelo de dados

A App 03 é **consumidora**: quase todas as entidades que ela toca já estão definidas no
PRD-01, no PRD-07 (economia) e no PRD-08 (território). O que segue é o mapa do que a aplicação
escreve, com uma única entidade nova.

```text
CADASTRA                 AGENDA E LANÇA          FILAS QUE TRATA
Jogador                  Aula/Agenda             SolicitacaoDeParticipacao
Mestre                   Atividade               SolicitacaoDeLocal
Apoiador                 Presenca                SolicitacaoDoResponsavel
Admin                    Resultado               SugestaoOuProposta
Responsavel              Lancamento              DesafioExtra
VinculoResponsavel       PartidaDeQuiz
Credencial               Reserva                 CONFERE (leitura)
Equipe                                           SerieDeColeta
ComunidadeVirtual        ACERVO                  DesafioDeColeta
Local                    ItemPatrimonial         Auditoria
Poder                    Emprestimo
ParametroDeOperacao      Aporte
```

| Entidade              | Atributos essenciais                                                                            |
| --------------------- | ----------------------------------------------------------------------------------------------- |
| `ParametroDeOperacao` | aplicação, liberada, comunidade default exigida, quem liberou, data e hora, motivo da suspensão |

`ParametroDeOperacao` é a **única entidade nova** deste PRD e sustenta a liberação do App 01.
Ela é somente inserção: suspender e reliberar são registros novos, não edição do anterior — é
o que permite responder "o onboarding estava liberado naquele dia?".

A infração e a pontuação negativa **não criam entidade**: são `Resultado` de valor negativo,
vinculado ao encontro ou à atividade, ao jogador e ao motivo registrado. Correção de
lançamento é `Lancamento` de ajuste referenciando o original, conforme o PRD-07.

## 9. Contratos de API

A aplicação consome as convenções do PRD-01 — prefixo `/v1`, token de sessão, erro em formato
único, listagem paginada com filtro de comunidade, período e persona. As rotas de território e
de livro-razão são as dos PRD-08 e PRD-07 e não se repetem aqui.

| Método | Rota                                              | Autenticação    | Descrição                                                   |
| ------ | ------------------------------------------------- | --------------- | ----------------------------------------------------------- |
| POST   | `/v1/jogadores`                                   | Admin           | Cadastra jogador pela gestão                                |
| POST   | `/v1/mestres`                                     | Admin           | Cadastra Mestre com artefatos comprobatórios                |
| POST   | `/v1/apoiadores`                                  | Admin           | Cadastra Apoiador com artefatos e termos de doação          |
| POST   | `/v1/admins`                                      | Admin           | Inclui novo Admin manualmente                               |
| POST   | `/v1/equipes`                                     | Admin           | Cadastra equipe e seus integrantes                          |
| POST   | `/v1/poderes`                                     | Admin           | Mantém o catálogo de poderes                                |
| PATCH  | `/v1/parametros/app-01`                           | Admin           | Libera ou suspende o funcionamento do App 01                |
| GET    | `/v1/solicitacoes-de-participacao`                | Admin           | Fila das solicitações vindas da vitrine                     |
| POST   | `/v1/solicitacoes-de-participacao/{id}/avaliacao` | Admin           | Aceita ou recusa, com parecer e autor                       |
| GET    | `/v1/solicitacoes-do-responsavel`                 | Admin           | Fila das solicitações vindas da App 07                      |
| POST   | `/v1/solicitacoes-do-responsavel/{id}/tratamento` | Admin           | Registra o desfecho, com quem tratou e quando               |
| GET    | `/v1/sugestoes`                                   | Admin           | Fila única de sugestões e propostas das Apps 05, 07, 08, 09 |
| POST   | `/v1/sugestoes/{id}/avaliacao`                    | Admin           | Muda o status e registra o retorno a quem propôs            |
| GET    | `/v1/desafios-extras/pendentes`                   | Admin           | Desafios já validados pelo Mestre, aguardando aprovação     |
| POST   | `/v1/desafios-extras/{id}/aprovacao`              | Admin           | Aprova, exigindo lastro registrado, ou recusa com motivo    |
| POST   | `/v1/atividades`                                  | Admin           | Cadastra atividade com pontuação, recompensa e recursos     |
| POST   | `/v1/aulas`                                       | Admin           | Agenda a aula e dispara a reserva de recursos               |
| POST   | `/v1/aulas/{id}/lancamentos`                      | Admin           | Lança a atividade realizada e os resultados                 |
| POST   | `/v1/aulas/{id}/presencas`                        | Admin           | Confirma ou ajusta presença, com registro do ajuste         |
| POST   | `/v1/aulas/{id}/ocorrencias`                      | Admin           | Registra infração e a pontuação negativa correspondente     |
| GET    | `/v1/painel-do-dia`                               | Mestre ou Admin | Estado do encontro em andamento, em leitura                 |
| POST   | `/v1/partidas-de-quiz`                            | Admin           | Abre a partida com banco de perguntas e equipes             |
| POST   | `/v1/partidas-de-quiz/{id}/perguntas`             | Admin           | Dá o _start_ da pergunta corrente                           |
| POST   | `/v1/partidas-de-quiz/{id}/encerramento`          | Admin           | Encerra a partida e lança a pontuação                       |
| POST   | `/v1/entregas`                                    | Admin           | Registra entrega de exemplar Alpha ou camisa, com baixa     |
| GET    | `/v1/auditoria`                                   | Admin           | Trilha de auditoria, com filtro por autor e período         |

Erros previstos: liberação do App 01 sem comunidade default (422, com a rota de marcação);
cadastro de Mestre ou Apoiador sem artefato anexado (422); sexto integrante de equipe (422);
segundo familiar de 17 anos ou mais na equipe (422); quarto responsável do mesmo jogador
(422); agendamento sem lastro (422, com a lista do que falta); aprovação de desafio extra sem
validação do Mestre (409) ou sem lastro (422); tentativa de editar lançamento (405); escrita
de Mestre em rota de gestão (403).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**: o painel do dia é operado **em pé, no celular**, andando
  entre as bancadas — é o caso de uso que dimensiona a interface, não a mesa do escritório.
- Painel do dia legível em tela pequena, com o estado do encontro visível sem rolagem longa.
- Atualização do painel tolerante a rede instável: reconexão automática, sem perder o que já
  foi lançado.
- Quiz ao Vivo com sincronização em tempo real entre dispositivos e desempate por ordem de
  chegada da resposta, tolerando queda e volta de aparelho durante a partida.
- Lançamento em lote de uma turma inteira sem recarregar a tela a cada jogador.
- Escrita idempotente: reenviar o mesmo lançamento por falha de rede não duplica o registro.
- Desempenho em celular modesto, o mesmo do ponto de apoio.
- Linguagem simples nas telas e nos erros; nenhum jargão de TI, porque o Mestre pode ser de
  humanas, artes, esportes ou cultura.
- Acessibilidade digital e idioma pt-BR; código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                      | Finalidade                        | Base legal        | Retenção                 | Quem acessa          |
| ---------------------------------- | --------------------------------- | ----------------- | ------------------------ | -------------------- |
| Cadastro do jogador                | Identificação e operação          | consentimento     | enquanto durar o vínculo | gestão e responsável |
| Presença e resultado de atividade  | Registro da participação          | consentimento     | enquanto durar o vínculo | gestão e responsável |
| Infração e pontuação negativa      | Aplicação do Código de Conduta    | interesse público | enquanto durar o vínculo | gestão e responsável |
| Contato do responsável             | Canal oficial com a família       | consentimento     | enquanto durar o vínculo | gestão               |
| Artefatos comprobatórios de adulto | Provar habilidade ou apoio        | consentimento     | enquanto durar o vínculo | gestão e visitante   |
| Solicitação de participação        | Avaliar quem pede para participar | consentimento     | enquanto durar a fila    | gestão               |
| Auditoria das ações de gestão      | Rastreabilidade                   | interesse público | permanente               | Admin                |

- A gestão **não vê a imagem do jogador**: a aplicação mostra avatar e nick, e a conferência
  biométrica acontece no núcleo, sem devolver imagem nem _template_.
- O responsável consulta pela App 07 **quem acessou** os dados da criança; é a trilha de
  auditoria desta aplicação que responde a isso.
- Pedido de acesso, correção ou exclusão chega pela fila da App 07 e é tratado aqui, com
  protocolo e desfecho registrados — **o registro de dado do território não é apagado**, e a
  resposta ao responsável diz isso.
- Toda tela que coleta dado traz o aviso discreto do que está sendo coletado, com acesso à área
  detalhada de destino e uso.
- O registro de infração é dado sensível de criança: fica restrito à gestão e ao responsável do
  jogador, nunca aparece em rota pública, ranking ou vitrine.

## 12. Critérios de aceite e métricas

- Liberação do App 01 é recusada enquanto não houver comunidade default marcada, e aceita no
  instante seguinte à marcação.
- Suspender a liberação impede novo cadastro no App 01 e não afeta jogador já cadastrado.
- Cadastro de Mestre sem nenhum artefato anexado é recusado.
- Solicitação de participação aceita **não** cria acesso: o Mestre só existe depois do cadastro
  feito pelo Admin.
- Equipe com seis integrantes, ou com dois familiares de 17 anos ou mais, é recusada.
- Quarto vínculo de responsável ao mesmo jogador é recusado e os três anteriores seguem.
- Agendamento sem lastro é recusado com a lista do que falta, e a mesma lista aparece nas
  necessidades públicas em moedas.
- Lançamento da atividade realizada baixa exatamente os recursos reservados no agendamento.
- Tentativa de editar um lançamento devolve 405, e a correção aparece como ajuste com o
  original preservado.
- Presença registrada pelo App 01 aparece no painel do dia sem lançamento manual; a confirmação
  manual grava quem confirmou.
- Painel do dia mostra saldo de kits MDF, devoluções pendentes e lançamentos pendentes do
  encontro em andamento.
- Mestre autenticado lê o painel do dia e recebe 403 em qualquer escrita de gestão.
- Partida de quiz com um aparelho fora do ar durante a pergunta é concluída, e o aparelho volta
  na pergunta corrente.
- Desafio extra sem validação do Mestre não aparece na fila de aprovação; com validação e sem
  lastro, a aprovação é recusada.
- Nenhuma tela da gestão exibe imagem real de jogador.
- Toda escrita bem-sucedida aparece na trilha de auditoria com autor, papel e data e hora.

Hipóteses do Ciclo 01 (documento 10): este PRD é o instrumento de medição de **H3** — o
confronto entre lastro registrado e recursos necessários acontece no agendamento desta
aplicação. Ele também **habilita H1**, porque sem a liberação do App 01 não há cadastro a
contar, e dá à gestão a distribuição etária que **H4** observa.

## 13. Decisões tomadas neste PRD

| Decisão                                                                                                         | Gravada em | Linha do doc 09                  |
| --------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------- |
| Liberação do App 01 é ato próprio do Admin, distinto da marcação da comunidade default, registrado e reversível | 03 §5      | Comunidade default do onboarding |

Duas questões em aberto que o documento 08 listava para este PRD foram **encerradas pelo que já
estava definido**, sem decisão nova: o Quiz ao Vivo é **módulo desta aplicação** (documento 03
§5 e documento 05 §5, que já põem a condução na App 03 e o banco de perguntas na App 09), e a
**trilha de auditoria das ações de Admin** foi definida no PRD-01, que a App 03 apenas
consulta.

## 14. Pendências que permanecem

- **Quem pode lançar pontuação negativa e com que auditoria.** Nesta aplicação o lançamento é
  de Admin, porque o Mestre só lê o painel do dia. Falta decidir se o Mestre registra a
  ocorrência pela App 09, qual a tipificação e se o lançamento exige revisão de um segundo
  Admin. **Trava**: a redação final do `RF-02-38` e o fluxo entre App 03 e App 09.
- **Pontuação e regras do Quiz ao Vivo**: pontos da vitória e das respostas corretas seguintes,
  se responde a equipe inteira ou um representante, critério de desempate e número de
  dispositivos por equipe. **Trava** o `RF-02-62`.
- **Formulário de solicitação de participação**: dados mínimos exigidos de pessoa e de
  instituição, triagem contra envio abusivo e prazo de resposta ao solicitante. **Trava** o
  conteúdo da fila (`RF-02-18`) e o alerta de atraso.
- **Prazos de resposta às solicitações dos responsáveis**, que definem quando a fila da App 07
  passa a marcar atraso nesta aplicação.
- **Estratégia de conservação do acervo permanente**: a validação da linha Include I —
  tombamento, ficha de vida, badge Guardião do Acervo e guarda por equipe — está pendente e
  pode reduzir o escopo dos `RF-02-52` a `RF-02-56`.
- **Pontuação das recompensas** cadastradas na atividade: os valores atuais são sugestão.

## 15. Rastreabilidade

| Requisito               | Origem                                                   |
| ----------------------- | -------------------------------------------------------- |
| `RF-02-01` a `RF-02-10` | 02 §§1, 5 e 03 §5 (cadastros e governança de personas)   |
| `RF-02-11` a `RF-02-17` | 02 §1, 03 §5 e PRD-08 (comunidade, default e território) |
| `RF-02-18` a `RF-02-20` | 02 §1 e 03 §§5, 8 (solicitação de participação)          |
| `RF-02-21` e `RF-02-22` | PRD-08 (solicitação de novo local)                       |
| `RF-02-23` e `RF-02-24` | 03 §9 (solicitações da área do responsável)              |
| `RF-02-25` e `RF-02-26` | 03 §§7, 9, 10, 11 (fila única de sugestões e propostas)  |
| `RF-02-27` e `RF-02-28` | 04 §3 e PRD-07 (desafios extras e lastro)                |
| `RF-02-29` a `RF-02-32` | 04 §1 e PRD-07 (atividade, agenda e regra de lastro)     |
| `RF-02-33` a `RF-02-35` | 02 §4 e 11 §5 (resultados e motor de pontuação)          |
| `RF-02-36`              | 03 §§3, 5 (presença vinda do onboarding)                 |
| `RF-02-37` a `RF-02-40` | 02 §4, 05 §3 e 13 (pontuação negativa e ajuste)          |
| `RF-02-41` a `RF-02-49` | 05 §4 e 03 §5 (encontro assíncrono e painel do dia)      |
| `RF-02-50` a `RF-02-56` | 05 §3 e PRD-07 (acervo, regime misto e patrimônio)       |
| `RF-02-57` e `RF-02-58` | 04 §1 e PRD-07 (aportes e necessidades)                  |
| `RF-02-59` a `RF-02-62` | 05 §5 (Quiz ao Vivo)                                     |
| `RF-02-63`              | PRD-01 (trilha de auditoria)                             |
| `RF-02-64`              | 03 §12 (aviso visível de coleta e área detalhada)        |
