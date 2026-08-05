# PRD-05 — App 05: Área do Guerreiro(a) (jornada gamificada)

## 1. Identificação

| Campo            | Valor                                                    |
| ---------------- | -------------------------------------------------------- |
| PRD              | PRD-05                                                   |
| Aplicação        | App 05 — Área do Guerreiro(a)                            |
| Onda             | 3                                                        |
| Situação         | em revisão                                               |
| Versão e data    | v1 — 2026-08-05                                          |
| Depende de       | PRD-01, PRD-09                                           |
| Documentos-fonte | 02 §§1–8, 03 §§1.1, 7, 12, 05 §§3, 5, 11 §§2, 4, 5, 6, 7 |

## 2. Contexto e objetivo

A App 05 é a aplicação que o Guerreiro(a) abre todo dia. O PRD-09 garante que existe trilha
escrita; este PRD garante que a criança **sabe o que fazer com ela sem precisar perguntar a
ninguém**. O encontro é assíncrono por desenho — cada um chega em um horário e está em um ponto
diferente —, e sem uma aplicação que diga "o seu próximo passo é este", a dinâmica assíncrona
vira fila na frente do Mestre.

O que muda na operação do Ciclo 01: o Guerreiro(a) entra por nick e imagem no aparelho
compartilhado do ponto de apoio, vê o próximo ponto da trilha, faz o desafio de desbloqueio,
registra a medição do território da semana, responde ao Quiz ao Vivo do encontro, entrega a
criação original na culminância e acompanha o que conquistou. É também por aqui que ele
**propõe melhorias na plataforma** — o valor de protagonismo virando mecânica, não texto.

A aplicação é o lado do Guerreiro(a) de tudo o que os outros PRDs escrevem: a trilha vem do
PRD-09, as séries de coleta do PRD-08, as recompensas e o acervo do PRD-07, e o motor de
pontos, níveis e badges do documento 11. **Nada de novo é decidido sobre as regras do jogo
aqui** — o que este PRD define é como a criança as enxerga e as opera.

## 3. Escopo

### 3.1 Dentro do escopo

- **Entrada por nick e imagem** em aparelho compartilhado, com troca rápida de sessão.
- **Guia da trilha**: qual é o próximo ponto, o que já foi conquistado, o que está bloqueado e
  o que falta para desbloquear.
- **Escolha do poder** entre os do catálogo do ciclo e inscrição nas trilhas do poder.
- **Conteúdo do ponto de trilha** — texto, imagens, vídeo, arquivos e bibliografia de apoio —
  e o **desafio de desbloqueio** que abre o ponto seguinte.
- **Desafios semanais** (on-line, presencial, em equipe e em equipe com familiar) e **desafios
  extras de Apoiadores**, abertos ou direcionados.
- **Equipes**: as de que participa, o papel em cada uma e as atividades de cada equipe.
- **Séries de coleta do território**: próxima medição, histórico, situação da série, pontos que
  ela está rendendo, seleção do local e solicitação de novo local.
- **Quiz ao Vivo**: recebimento da pergunta e envio da resposta da equipe.
- **Criação original**: entrega na culminância e **portfólio** das criações validadas.
- **Progresso**: pontos, níveis 1 a 5 por trilha ou poder, badges e recompensas conquistadas
  nos marcos.
- **Ranking** da comunidade, por trilha ou poder, apenas com pontos regulares.
- **Acervo do Guerreiro(a)**: o exemplar da linha Alpha que é dele e os exemplares permanentes
  em uso de bancada, com a ficha de vida do livro.
- **Apoio às atividades escolares** por assistente de voz com IA, respondendo apenas a partir
  do conteúdo cadastrado pela gestão.
- **Canal de sugestões**, em texto ou áudio, com acompanhamento do status.
- **Aviso de coleta de dados** em toda tela que coleta, com acesso à área detalhada.

### 3.2 Fora do escopo

- **Autoria de trilha, conteúdo e desafio** — é a bancada do Mestre, na App 09.
- **Lançamento de atividade realizada, presença e mérito** — quem lança é o Mestre (App 09) ou
  o Admin (App 03); aqui só se consulta o resultado.
- **Condução da partida de Quiz ao Vivo** — abre e conduz quem ministra a aula, pela App 03.
- **Cadastro do próprio Guerreiro(a) e captura da imagem** — acontecem no onboarding (App 01).
- **Autorização de divulgação pública** — é ato do responsável, na App 07; aqui só se vê o
  estado do perfil.
- **Cadastro de equipe e de local do território** — são de Admin (App 03 e PRD-08).
- **Cadastro das disciplinas e do conteúdo do apoio escolar** — é do Mestre (App 09) ou do
  Admin (App 03); aqui o conteúdo só é consumido.
- **Conversa educacional aberta e Modo Ouvinte da aula** — são da App 02 (PRD-06); o
  assistente desta aplicação atende apenas ao apoio escolar, com corpus fechado.
- **Compra de recompensa com pontos**: não existe. Recompensa se conquista em marco.
- **Crédito de pontos pelo jogo** (App 04): o jogo lê progresso e debita, nunca credita.
- **Contato com Apoiadores, Mestres ou terceiros por mensagem** — não há canal de conversa
  entre pessoas nesta aplicação.
- **Troca de comunidade**: existe no modelo, não é operada no Ciclo 01.

## 4. Personas e permissões

| Persona      | O que faz nesta aplicação                                                            | O que não pode fazer                                                    |
| ------------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Guerreiro(a) | Percorre trilhas, realiza desafios, registra coleta, entrega criação e propõe        | Lançar o próprio resultado, editar pontos, ver dados de outra criança   |
| Mestre       | Abre a sessão do Guerreiro(a) sem imagem gravada e confirma a identidade no encontro | Usar a aplicação em nome dele para realizar desafio ou registrar coleta |
| Admin        | O mesmo do Mestre, quando é quem está na sala                                        | O mesmo do Mestre                                                       |
| Responsável  | Nada: acompanha pela App 07                                                          | Entrar                                                                  |
| Visitante    | Nada: a aplicação é inteiramente autenticada                                         | Acessar qualquer tela                                                   |

O Guerreiro(a) vê **apenas os próprios dados**. As únicas informações de terceiros que a
aplicação exibe são as públicas do ranking e as das equipes de que ele participa — sempre por
avatar e nick.

## 5. Jornadas principais

### 5.1 Entrar no aparelho compartilhado do ponto de apoio

1. O Guerreiro(a) informa o **nick** e a câmera captura a imagem para conferência contra o
   _template_ gravado no onboarding.
2. Conferida, a sessão abre direto no guia da trilha, sem senha e sem PIN.
3. **Sem câmera no aparelho, não há entrada.** A aplicação diz isso em linguagem simples.
4. Falhando a conferência, o **Mestre ou Admin presente abre a sessão** confirmando quem é —
   é o mesmo fallback do onboarding, e é o único caminho para quem ainda não tem imagem
   gravada.
5. Ao sair, ou por inatividade, a sessão encerra e a tela volta ao pedido de nick — o aparelho
   é do ponto de apoio, não da criança.
6. Nenhuma imagem fica guardada no aparelho.

### 5.2 Saber o que fazer agora

1. A tela inicial abre no **próximo ponto de trilha**: o que é, o que precisa ser feito e o
   que ele desbloqueia.
2. Abaixo, o que está **em aberto hoje**: desafio semanal da semana, medição do território
   pendente e desafio extra vigente.
3. O que está **bloqueado** aparece com o motivo — "falta desbloquear o ponto 3" —, nunca como
   cadeado mudo.
4. O progresso mostra o **nível na trilha e o que falta para o próximo**, em pontos de trilha
   desbloqueados: nível é percurso, não saldo.
5. Quem participa de mais de uma trilha alterna entre elas sem perder o contexto de nenhuma.

### 5.3 Desbloquear um ponto de trilha

1. O Guerreiro(a) abre o ponto e percorre o conteúdo — texto, imagens, vídeo e arquivos —, com
   a bibliografia de apoio indicando **título, capítulo e se há exemplar no seu ponto de
   apoio**.
2. Realiza as atividades daquele ponto, individuais ou em equipe, presenciais ou on-line.
3. Faz o **desafio de desbloqueio**: quiz ou desafio prático declarado pelo Mestre autor.
4. Passando, o ponto seguinte abre na hora e o percurso avança.
5. Não passando, ele pode tentar de novo — a trilha é de dificuldade gradual e não elimina
   ninguém.
6. Os **pontos da atividade** só entram quando o Mestre lança o resultado; a aplicação deixa
   claro o que está "aguardando lançamento".

### 5.4 Registrar uma medição do território

1. A série ativa mostra **quando é a próxima medição** e quantos pontos ela está rendendo.
2. O Guerreiro(a) escolhe o **local** entre os cadastrados; faltando, **solicita a inclusão**,
   que vai para o Mestre da trilha ou para um Admin.
3. Registra o valor — digitado, por voz, por foto ou por vídeo — e o registro **nasce válido e
   pontua na hora**.
4. Valor **fora da faixa declarada** no desafio entra como **a conferir**, sem pontuar, até o
   Mestre validar — e a tela explica por que, sem acusar ninguém.
5. Faltando duas cadências seguidas, a série é marcada como **interrompida**: os pontos já
   ganhos permanecem e a tela mostra como retomar.
6. O histórico da série fica visível, com o que foi registrado e quando.

### 5.5 Jogar o Quiz ao Vivo

1. O Mestre abre a partida na App 03 e **vincula um aparelho a cada equipe**.
2. A pergunta aparece simultaneamente em todos os aparelhos da aula, com quatro alternativas e
   sem tempo próprio.
3. A equipe se consulta e responde pelo seu aparelho; a resposta vale para **todos os
   integrantes**.
4. Toda equipe que acerta pontua, e a primeira a acertar recebe o bônus.
5. Caindo a rede de um aparelho no meio da pergunta, a partida continua e o aparelho volta ao
   estado corrente ao reconectar.
6. Equipe sem aparelho responde pelo aparelho do Mestre — falta de celular não tira ninguém da
   partida.

### 5.6 Entregar a criação original da culminância

1. Concluída a trilha, a culminância mostra **o que a criação precisa ser** e o critério com
   que será validada, escritos pelo Mestre autor.
2. O Guerreiro(a) — ou a equipe, com o papel de cada integrante — entrega a criação: texto,
   imagem, vídeo, arquivo ou link.
3. O Mestre autor valida. Validada, ela entra no **portfólio** com autoria creditada e libera o
   badge de autoria.
4. Devolvida para ajuste, **a autoria não se perde** e o motivo aparece em linguagem simples.
5. A criação **só aparece publicamente se o responsável tiver autorizado a divulgação**; sem
   autorização, ela existe no portfólio interno do Guerreiro(a).

### 5.7 Conquistar recompensa e cuidar do acervo

1. Alcançado um marco com recompensa declarada, a aplicação avisa **o que foi conquistado** e
   que a entrega será confirmada pelo Mestre — não há saldo debitado, porque recompensa não se
   compra.
2. O **acervo do Guerreiro(a)** mostra o exemplar da linha Alpha recebido na abertura da trilha
   — que é dele, sem devolução — e os exemplares permanentes em uso de bancada.
3. Cada exemplar permanente tem a **ficha de vida**: quem usou, quando e em que estado voltou.
4. Devolução em bom estado ao fim do ciclo concede o badge **Guardião do Acervo**.
5. **Dano acidental não gera pontuação negativa nem dívida**, e a tela diz isso antes de o
   Guerreiro(a) relatar qualquer problema com o material.

### 5.8 Pedir ajuda em uma atividade escolar

1. O Guerreiro(a) abre o apoio escolar, escolhe a **disciplina** entre as cadastradas e
   pergunta **por voz ou por texto**.
2. O assistente responde a partir **exclusivamente** do conteúdo que Mestres ou Admins
   cadastraram para aquela disciplina, em áudio e em texto, na linguagem da faixa etária.
3. A resposta **explica e conduz ao raciocínio**: dá o caminho, o exemplo e a próxima
   pergunta — **não entrega a tarefa pronta**.
4. Sendo a pergunta fora do conteúdo cadastrado, o assistente **diz que ainda não tem esse
   material** e orienta a procurar um Mestre no encontro. Não inventa resposta.
5. Sendo a pergunta imprópria, sensível ou sobre pessoas, o assistente recusa em linguagem
   acolhedora e registra a ocorrência para a gestão, sem expor a criança.
6. Pedido de dado pessoal — de si ou de um colega — nunca é atendido.
7. Quem recusou o uso do assistente, ou o responsável que o recusou, continua com a
   **alternativa equivalente**: perguntar ao Mestre no encontro.

### 5.9 Propor uma melhoria

1. O Guerreiro(a) registra a sugestão em **texto ou áudio de até 60 segundos**, que é
   transcrito.
2. A sugestão entra na **fila única da gestão**, a mesma que recebe as propostas do
   responsável, do Apoiador e do Mestre.
3. Ele acompanha o status: recebida, em avaliação, adotada ou não adotada, com o motivo em
   linguagem simples.
4. **Registrar não pontua.** Adotada, a proposta rende **pontos extras e o badge de
   protagonismo** — quem joga também constrói o jogo.
5. O retorno acontece em até 7 dias, dentro da plataforma.

## 6. Requisitos funcionais

### 6.1 Entrada e sessão

| ID         | Requisito                                                                             | Prioridade |
| ---------- | ------------------------------------------------------------------------------------- | ---------- |
| `RF-05-01` | Guerreiro(a) entra informando o nick e submetendo a imagem à conferência biométrica   | essencial  |
| `RF-05-02` | Aplicação recusa a entrada em aparelho sem câmera, explicando em linguagem simples    | essencial  |
| `RF-05-03` | Mestre ou Admin presente abre a sessão do Guerreiro(a) quando a conferência falha     | essencial  |
| `RF-05-04` | Mestre ou Admin abre a sessão de quem ainda não tem imagem gravada                    | essencial  |
| `RF-05-05` | Sessão encerra ao sair e por inatividade, devolvendo a tela ao pedido de nick         | essencial  |
| `RF-05-06` | Nenhuma imagem de Guerreiro(a) é armazenada no aparelho compartilhado                 | essencial  |
| `RF-05-07` | Troca de sessão entre dois Guerreiros e Guerreiras acontece sem reiniciar a aplicação | essencial  |

### 6.2 Guia da trilha e progressão

| ID         | Requisito                                                                                 | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------- | ---------- |
| `RF-05-08` | Tela inicial abre no próximo ponto de trilha, com o que fazer e o que ele desbloqueia     | essencial  |
| `RF-05-09` | Guerreiro(a) escolhe o poder entre os do catálogo do ciclo e se inscreve nas trilhas dele | essencial  |
| `RF-05-10` | Ponto bloqueado exibe o motivo do bloqueio e o que falta para abri-lo                     | essencial  |
| `RF-05-11` | Guerreiro(a) percorre o conteúdo do ponto: texto, imagens, vídeo, arquivos e bibliografia | essencial  |
| `RF-05-12` | Bibliografia indica título, capítulo e se há exemplar disponível no seu ponto de apoio    | essencial  |
| `RF-05-13` | Guerreiro(a) realiza o desafio de desbloqueio e o ponto seguinte abre na hora ao passar   | essencial  |
| `RF-05-14` | Desafio de desbloqueio não passado pode ser repetido, sem eliminar o Guerreiro(a)         | essencial  |
| `RF-05-15` | Progresso exibe o nível na trilha e quantos pontos de trilha faltam para o próximo nível  | essencial  |
| `RF-05-16` | Aplicação exibe pontos, badges e recompensas conquistadas, por trilha ou poder            | essencial  |
| `RF-05-17` | Guerreiro(a) inscrito em mais de uma trilha alterna entre elas preservando o contexto     | essencial  |
| `RF-05-18` | Resultado ainda não lançado pelo Mestre aparece como "aguardando lançamento"              | essencial  |

### 6.3 Desafios, atividades e equipes

| ID         | Requisito                                                                                   | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------- | ---------- |
| `RF-05-19` | Guerreiro(a) vê os desafios semanais vigentes, com modalidade e formato de cada um          | essencial  |
| `RF-05-20` | Guerreiro(a) vê os desafios extras vigentes que lhe são elegíveis, abertos ou direcionados  | essencial  |
| `RF-05-21` | Desafio extra exibe a recompensa oferecida, a quantidade disponível e o período de vigência | essencial  |
| `RF-05-22` | Guerreiro(a) vê as equipes de que participa, o papel em cada uma e as atividades delas      | essencial  |
| `RF-05-23` | Atividade de equipe exibe os integrantes por avatar e nick, sem qualquer dado pessoal       | essencial  |
| `RF-05-24` | Aplicação não permite ao Guerreiro(a) criar, editar ou desfazer equipe                      | essencial  |

### 6.4 Quiz ao Vivo

| ID         | Requisito                                                                                  | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------ | ---------- |
| `RF-05-25` | Aparelho recebe a pergunta corrente da partida aberta na App 03, com quatro alternativas   | essencial  |
| `RF-05-26` | Aparelho vinculado a uma equipe envia uma única resposta, válida para todos os integrantes | essencial  |
| `RF-05-27` | Aplicação recusa segunda resposta da mesma equipe para a mesma pergunta                    | essencial  |
| `RF-05-28` | Aparelho que perde a rede durante a pergunta volta ao estado corrente ao reconectar        | essencial  |
| `RF-05-29` | Resultado da pergunta aparece para a equipe assim que quem conduz a partida o libera       | essencial  |

### 6.5 Coleta de dados do território

| ID         | Requisito                                                                                  | Prioridade |
| ---------- | ------------------------------------------------------------------------------------------ | ---------- |
| `RF-05-30` | Guerreiro(a) vê as suas séries, a próxima medição e os pontos que cada série está rendendo | essencial  |
| `RF-05-31` | Guerreiro(a) seleciona o local do registro entre os cadastrados pela gestão                | essencial  |
| `RF-05-32` | Guerreiro(a) solicita a inclusão de local faltante e acompanha o status da solicitação     | essencial  |
| `RF-05-33` | Registro aceita valor digitado, ditado por voz, foto ou vídeo, com a origem gravada        | essencial  |
| `RF-05-34` | Registro dentro da faixa declarada nasce válido e pontua na hora                           | essencial  |
| `RF-05-35` | Registro fora da faixa declarada entra como "a conferir", sem pontuar, e a tela explica    | essencial  |
| `RF-05-36` | Série interrompida é sinalizada com o histórico preservado e o caminho de retomada         | essencial  |
| `RF-05-37` | Guerreiro(a) consulta o histórico da própria série, com data e valor de cada registro      | essencial  |
| `RF-05-38` | Registro invalidado pelo Mestre aparece com o motivo, e só ele perde os pontos             | essencial  |

### 6.6 Criação original e portfólio

| ID         | Requisito                                                                                     | Prioridade |
| ---------- | --------------------------------------------------------------------------------------------- | ---------- |
| `RF-05-39` | Culminância exibe o que a criação precisa ser e o critério de validação do Mestre autor       | essencial  |
| `RF-05-40` | Guerreiro(a) entrega a criação original em texto, imagem, vídeo, arquivo ou link              | essencial  |
| `RF-05-41` | Criação de equipe registra o papel de cada integrante na entrega                              | essencial  |
| `RF-05-42` | Criação devolvida para ajuste preserva a autoria e exibe o motivo em linguagem simples        | essencial  |
| `RF-05-43` | Portfólio reúne as criações validadas do Guerreiro(a), com trilha, data e autoria             | essencial  |
| `RF-05-44` | Portfólio indica quais criações estão públicas e quais dependem de autorização do responsável | essencial  |

### 6.7 Recompensas, acervo e perfil

| ID         | Requisito                                                                                 | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------- | ---------- |
| `RF-05-45` | Marco alcançado avisa a recompensa conquistada e que a entrega é confirmada pelo Mestre   | essencial  |
| `RF-05-46` | Aplicação não oferece nenhuma forma de comprar recompensa com saldo de pontos             | essencial  |
| `RF-05-47` | Acervo do Guerreiro(a) distingue o exemplar próprio da linha Alpha dos permanentes em uso | essencial  |
| `RF-05-48` | Exemplar permanente exibe a ficha de vida: quem usou, quando e em que estado voltou       | essencial  |
| `RF-05-49` | Tela do acervo informa que dano acidental não gera pontuação negativa nem dívida          | essencial  |
| `RF-05-50` | Guerreiro(a) vê o estado do seu perfil público e se a divulgação foi autorizada           | essencial  |
| `RF-05-51` | Guerreiro(a) escolhe e altera as características do próprio avatar                        | desejável  |

### 6.8 Ranking, sugestões e avisos

| ID         | Requisito                                                                                 | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------- | ---------- |
| `RF-05-52` | Ranking exibe posições da comunidade por trilha ou poder, somente com pontos regulares    | essencial  |
| `RF-05-53` | Guerreiro(a) vê sempre a própria posição no ranking, mesmo sem divulgação autorizada      | essencial  |
| `RF-05-54` | Guerreiro(a) registra sugestão em texto ou em áudio de até 60 segundos, transcrito        | essencial  |
| `RF-05-55` | Sugestão registrada exibe o status até o retorno da gestão, com motivo quando não adotada | essencial  |
| `RF-05-56` | Proposta adotada credita pontos extras e o badge de protagonismo ao autor                 | essencial  |
| `RF-05-57` | Toda tela que coleta dado traz aviso discreto do que coleta, com acesso à área detalhada  | essencial  |

### 6.9 Apoio às atividades escolares

| ID         | Requisito                                                                                       | Prioridade |
| ---------- | ----------------------------------------------------------------------------------------------- | ---------- |
| `RF-05-58` | Guerreiro(a) escolhe a disciplina entre as cadastradas e pergunta por voz ou por texto          | essencial  |
| `RF-05-59` | Assistente responde em áudio e em texto, na linguagem da faixa de 6 a 16 anos                   | essencial  |
| `RF-05-60` | Resposta é construída exclusivamente a partir do conteúdo cadastrado da disciplina escolhida    | essencial  |
| `RF-05-61` | Pergunta fora do conteúdo cadastrado recebe recusa explícita, com orientação de procurar Mestre | essencial  |
| `RF-05-62` | Assistente explica e conduz ao raciocínio, sem entregar a tarefa escolar pronta                 | essencial  |
| `RF-05-63` | Pergunta imprópria ou sensível é recusada em linguagem acolhedora e registrada para a gestão    | essencial  |
| `RF-05-64` | Assistente não fornece nem solicita dado pessoal do Guerreiro(a) ou de terceiros                | essencial  |
| `RF-05-65` | Tela do apoio escolar avisa que a resposta é gerada por IA e o que isso significa               | essencial  |
| `RF-05-66` | Guerreiro(a) que recusou o assistente segue com a alternativa de perguntar ao Mestre            | essencial  |
| `RF-05-67` | Consumo do modelo é lançado como recurso de _cloud_ no livro-razão                              | essencial  |
| `RF-05-68` | Mestre e Admin veem as recusas registradas das suas turmas, para ajustar o conteúdo cadastrado  | desejável  |

## 7. Regras de negócio

| ID         | Regra                                                                                              | Invariante (doc 99 §6) | Fonte            |
| ---------- | -------------------------------------------------------------------------------------------------- | ---------------------- | ---------------- |
| `RN-05-01` | O Guerreiro(a) entra por nick e imagem em toda sessão; sem câmera não há entrada                   | 12                     | 03 §1.1          |
| `RN-05-02` | Enquanto não houver imagem gravada, quem abre a sessão é o Mestre ou um Admin presente             | 3                      | 03 §1.1          |
| `RN-05-03` | Nível é percurso da trilha, não volume de pontos, e nível conquistado não regride                  | 2                      | 11 §6            |
| `RN-05-04` | Níveis e badges são por trilha ou poder, nunca globais                                             | —                      | 02 §7, 11 §§6, 7 |
| `RN-05-05` | Pontos só nascem de atividade realizada proposta por Mestre e da coleta do território              | 8                      | 11 §§1, 5        |
| `RN-05-06` | A aplicação não lança resultado, presença nem mérito: quem lança é o Mestre ou o Admin             | —                      | 02 §4, 03 §11    |
| `RN-05-07` | Recompensa é conquistada em marco da trilha, nunca comprada com saldo de pontos                    | —                      | 02 §8            |
| `RN-05-08` | Registro de coleta nasce válido e pontua na hora; valor fora da faixa fica "a conferir"            | 6                      | 02 §1, 11 §5.1   |
| `RN-05-09` | A invalidação por amostragem estorna apenas o registro invalidado                                  | 6                      | 02 §1, 11 §5.1   |
| `RN-05-10` | Duas cadências seguidas sem registro interrompem a série, sem perder os pontos já creditados       | 6                      | 02 §1            |
| `RN-05-11` | O local do registro é escolhido entre os cadastrados; faltando, o Guerreiro(a) solicita inclusão   | —                      | 02 §1            |
| `RN-05-12` | Um aparelho por equipe na partida de quiz, com a resposta valendo para todos os integrantes        | —                      | 05 §5            |
| `RN-05-13` | A criação original carrega a autoria por toda a vida do registro, inclusive quando devolvida       | 5                      | 02 §4, 11 §7     |
| `RN-05-14` | Criação original só é exposta publicamente com autorização do responsável                          | 11                     | 03 §12           |
| `RN-05-15` | O Guerreiro(a) é representado exclusivamente por avatar e nick, nunca por imagem real              | 12                     | 03 §§3.3, 12     |
| `RN-05-16` | Ranking usa somente pontos regulares e segue a mesma regra de exibição da vitrine                  | —                      | 11 §8.1          |
| `RN-05-17` | Registrar sugestão não pontua; a proposta adotada rende pontos extras e badge                      | —                      | 03 §7, 11 §5     |
| `RN-05-18` | Pontos extras não alimentam níveis: são computados isoladamente                                    | —                      | 11 §5            |
| `RN-05-19` | Dano acidental ao acervo não gera pontuação negativa nem dívida para a família                     | —                      | 13 §3            |
| `RN-05-20` | Dificuldade gradual acessível a toda a faixa de 6 a 16 anos, sem segmentação por idade             | 2                      | 02 §4            |
| `RN-05-21` | O Guerreiro(a) vê apenas os próprios dados; de terceiros, só avatar, nick e posição pública        | 10                     | 03 §12           |
| `RN-05-22` | Não há canal de conversa entre pessoas nesta aplicação                                             | 10                     | 03 §12           |
| `RN-05-23` | O App 04 lê o progresso e debita pontos; nenhum crédito parte do jogo                              | 8                      | 11 §8.4          |
| `RN-05-24` | No Ciclo 01 o Guerreiro(a) não muda de comunidade                                                  | 4                      | 02 §1            |
| `RN-05-25` | O apoio escolar responde só a partir do conteúdo cadastrado por Mestre ou Admin; fora dele, recusa | —                      | 03 §7            |
| `RN-05-26` | Filtros de segurança de conteúdo no nível mais restritivo em toda interação com a criança          | —                      | 03 §§4, 7        |
| `RN-05-27` | O assistente não substitui o Mestre: explica e conduz, sem entregar a tarefa pronta                | —                      | 03 §7            |
| `RN-05-28` | Recusar o assistente não exclui ninguém: a alternativa é perguntar ao Mestre no encontro           | 11                     | 03 §§7, 12       |
| `RN-05-29` | O consumo do modelo de IA é custo de _cloud_ atribuído no livro-razão                              | 9                      | 04 §1            |
| `RN-05-30` | A plataforma declara o uso de IA, e a tela do apoio escolar diz isso à criança                     | —                      | 01 §7, 03 §1     |

## 8. Modelo de dados

A aplicação é majoritariamente **leitora**: trilha e conteúdo vêm do PRD-09, séries e registros
do PRD-08, recompensas e acervo do PRD-07, e pontos, níveis e badges do núcleo (PRD-01). Este
PRD **acrescenta quatro entidades** ao núcleo — `RespostaDeQuiz`, `DisciplinaDeApoio`,
`ConteudoDeApoio` e `ConsultaDeApoio` — e escreve em outras quatro que já existem.

```text
ESCREVE (por ato do Guerreiro(a))       LÊ (definidos em outro PRD)
RegistroDeColeta        (PRD-08)        Trilha / PontoDeTrilha    (PRD-09)
SolicitacaoDeLocal      (PRD-08)        Conteudo / Bibliografia   (PRD-09)
CriacaoOriginal         (PRD-09)        Culminancia               (PRD-09)
SugestaoOuProposta      (PRD-01)        Atividade / Resultado     (PRD-01)
RespostaDeQuiz          [entidade nova] Equipe / Presenca         (PRD-01)
ConsultaDeApoio         [entidade nova] Ponto / Nivel / Badge     (PRD-01)
Avatar (características)                RecompensaDeMarco         (PRD-09)
                                        ItemPatrimonial           (PRD-07)
                                        DesafioExtra              (PRD-01)
                                        DisciplinaDeApoio    [nova, escrita na App 09/03]
                                        ConteudoDeApoio      [nova, escrita na App 09/03]
```

| Entidade            | Atributos essenciais                                                                                            |
| ------------------- | --------------------------------------------------------------------------------------------------------------- |
| `RespostaDeQuiz`    | partida, pergunta, equipe, aparelho vinculado, alternativa escolhida, momento de chegada no servidor, acerto    |
| `Nivel`             | Guerreiro(a), trilha ou poder, número (1 a 5), data da conquista — derivado do percurso, nunca editado          |
| `DisciplinaDeApoio` | nome, faixa de dificuldade, situação (ativa ou inativa), autor do cadastro (Mestre ou Admin)                    |
| `ConteudoDeApoio`   | disciplina, título, corpo ou arquivo, fonte, autor do cadastro, data — é o corpus fechado que o modelo consulta |
| `ConsultaDeApoio`   | Guerreiro(a), disciplina, pergunta transcrita, situação (respondida, fora do corpus, recusada), data e hora     |

Imutabilidade e derivação:

- `Nivel` é **calculado** a partir dos pontos de trilha desbloqueados, do mérito extra e da
  culminância validada. Não é campo que se escreve à mão, e **não regride**.
- `RespostaDeQuiz` é única por equipe e por pergunta; a segunda tentativa é recusada.
- `RegistroDeColeta` fora da faixa nasce na situação **a conferir** e só passa a válido pela
  validação do Mestre.
- `CriacaoOriginal` devolvida muda de situação, nunca de autoria.
- O saldo de pontos da trilha **nunca fica negativo**, e a pontuação negativa não altera nível
  nem badge já conquistados.
- `ConteudoDeApoio` é **o único insumo** da resposta do assistente: não havendo conteúdo
  cadastrado para a disciplina, a consulta é recusada em vez de respondida.
- `ConsultaDeApoio` **não gera pontos** e não alimenta nível, badge nem ranking: pedir ajuda
  não é realização.

## 9. Contratos de API

A aplicação segue as convenções do PRD-01 — prefixo `/v1`, token de sessão, erro em formato
único. As rotas de coleta e de solicitação de local são do PRD-08 e as de acervo, do PRD-07;
aparecem aqui apenas quando o ato é do Guerreiro(a).

| Método | Rota                                  | Autenticação | Descrição                                                     |
| ------ | ------------------------------------- | ------------ | ------------------------------------------------------------- |
| POST   | `/v1/sessoes/guerreiro`               | pública      | Abre sessão com nick e imagem, conferidos contra o _template_ |
| POST   | `/v1/sessoes/guerreiro/assistida`     | Mestre/Admin | Abre sessão do Guerreiro(a) sem imagem gravada ou após falha  |
| DELETE | `/v1/sessoes/guerreiro`               | Guerreiro(a) | Encerra a sessão no aparelho compartilhado                    |
| GET    | `/v1/eu/trilhas`                      | Guerreiro(a) | Trilhas em que está inscrito, com o próximo ponto de cada uma |
| POST   | `/v1/eu/trilhas/{id}/inscricao`       | Guerreiro(a) | Inscreve-se na trilha de um poder do catálogo do ciclo        |
| GET    | `/v1/eu/trilhas/{id}/pontos/{ordem}`  | Guerreiro(a) | Conteúdo do ponto, bibliografia e desafio de desbloqueio      |
| POST   | `/v1/eu/pontos/{id}/desbloqueio`      | Guerreiro(a) | Submete o desafio de desbloqueio do ponto                     |
| GET    | `/v1/eu/progresso`                    | Guerreiro(a) | Pontos, nível por trilha ou poder, badges e o que falta       |
| GET    | `/v1/eu/desafios`                     | Guerreiro(a) | Desafios semanais e extras vigentes e elegíveis               |
| GET    | `/v1/eu/equipes`                      | Guerreiro(a) | Equipes de que participa, com papel e atividades              |
| GET    | `/v1/eu/series`                       | Guerreiro(a) | Séries de coleta, próxima medição, situação e pontos rendidos |
| POST   | `/v1/series/{id}/registros`           | Guerreiro(a) | Registra a medição, com local, valor ou mídia e origem        |
| POST   | `/v1/solicitacoes-de-local`           | Guerreiro(a) | Solicita a inclusão de local faltante                         |
| GET    | `/v1/partidas-de-quiz/{id}/pergunta`  | Guerreiro(a) | Pergunta corrente da partida aberta na aula                   |
| POST   | `/v1/partidas-de-quiz/{id}/respostas` | Guerreiro(a) | Envia a resposta da equipe pelo aparelho vinculado            |
| POST   | `/v1/culminancias/{id}/criacoes`      | Guerreiro(a) | Entrega a criação original, individual ou de equipe           |
| GET    | `/v1/eu/portfolio`                    | Guerreiro(a) | Criações validadas, com situação de exposição pública         |
| GET    | `/v1/eu/recompensas`                  | Guerreiro(a) | Recompensas conquistadas em marcos e situação da entrega      |
| GET    | `/v1/eu/acervo`                       | Guerreiro(a) | Exemplar próprio e permanentes em uso, com a ficha de vida    |
| GET    | `/v1/rankings/{comunidade}`           | pública      | Ranking por trilha ou poder, somente com pontos regulares     |
| POST   | `/v1/sugestoes`                       | Guerreiro(a) | Registra sugestão em texto ou áudio na fila única da gestão   |
| GET    | `/v1/eu/sugestoes`                    | Guerreiro(a) | Status das próprias sugestões                                 |
| GET    | `/v1/apoio-escolar/disciplinas`       | Guerreiro(a) | Disciplinas ativas com conteúdo cadastrado                    |
| POST   | `/v1/apoio-escolar/consultas`         | Guerreiro(a) | Pergunta em texto ou áudio; responde a partir do corpus       |
| PATCH  | `/v1/eu/avatar`                       | Guerreiro(a) | Altera as características do próprio avatar                   |

Erros previstos: entrada sem câmera disponível (422); conferência biométrica sem
correspondência (401), com o caminho da sessão assistida; consulta a dado de outro
Guerreiro(a) (403); segunda resposta da mesma equipe para a mesma pergunta (409); registro em
série interrompida sem retomada (409); entrega de criação em trilha sem culminância alcançada
(409); tentativa de lançar resultado, presença ou pontos (403); qualquer rota de crédito de
pontos a partir do jogo (404, por não existir); consulta a disciplina sem conteúdo cadastrado
(422); consulta recusada pelos filtros de segurança (422, com a ocorrência registrada).

## 10. Requisitos não funcionais

- Web App responsivo **Mobile First**, projetado para o **celular modesto do ponto de apoio** —
  é o aparelho de referência, não o caso extremo.
- **Aparelho compartilhado é a condição normal de uso**: troca de sessão em poucos segundos,
  nenhum dado do Guerreiro(a) anterior visível na tela seguinte e nenhuma imagem no aparelho.
- **Rede instável**: a entrada exige rede, porque a conferência da imagem acontece no núcleo; o
  conteúdo já carregado do ponto de trilha continua legível durante uma queda. O apoio escolar
  **só opera com rede** — o modelo roda no backend — e diz isso claramente quando indisponível.
- **Áudio no navegador**: captação e reprodução por `navigator.mediaDevices.getUserMedia`, com
  reconhecimento e síntese de fala em pt-BR, na mesma base técnica da App 02.
- **Linguagem de criança de 6 anos**: nenhum termo técnico, nenhum código de erro exposto e
  todo bloqueio explicado pelo que falta fazer.
- **Acessibilidade digital**: contraste, alvos de toque grandes, leitura por voz do conteúdo e
  operação possível sem digitação — pela mesma razão que a sugestão aceita áudio.
- Desempenho: a tela inicial abre no próximo ponto sem exigir navegação por menu.
- Escrita idempotente: reenviar o mesmo registro de coleta por falha de rede não duplica.
- Idioma pt-BR; código aberto.

## 11. LGPD e proteção da criança

| Dado coletado                    | Finalidade                            | Base legal        | Retenção                     | Quem acessa              |
| -------------------------------- | ------------------------------------- | ----------------- | ---------------------------- | ------------------------ |
| Imagem da entrada                | Conferir que é o próprio Guerreiro(a) | consentimento     | não é armazenada na entrada  | núcleo, em conferência   |
| Registro de coleta do território | Construir a Comunidade Virtual        | interesse público | permanente, com autoria      | gestão, público agregado |
| Criação original                 | Autoria, portfólio e culminância      | consentimento     | permanente, com autoria      | gestão e responsável     |
| Sugestão em texto ou áudio       | Evolução da plataforma                | consentimento     | enquanto durar o vínculo     | gestão                   |
| Respostas de quiz e progresso    | Registro da participação e pontuação  | consentimento     | enquanto durar o vínculo     | gestão e responsável     |
| Características do avatar        | Representação pública do Guerreiro(a) | consentimento     | enquanto durar o vínculo     | público                  |
| Pergunta do apoio escolar        | Responder à dúvida da atividade       | consentimento     | transcrição, prazo a definir | gestão                   |

- **Consentimento**: a participação segue a adesão em duas etapas — o cadastro livre já permite
  usar a aplicação, e a **divulgação pública** depende de autorização do responsável, dada na
  App 07. A tela de perfil mostra qual é o estado vigente.
- **Alternativa a quem recusa**: sem imagem gravada, o Guerreiro(a) entra com a sessão aberta
  pelo Mestre ou Admin presente. Recusa nunca exclui da atividade.
- **Aviso visível**: toda tela que coleta dado traz o aviso discreto do que se coleta, com
  acesso à área detalhada sobre destino e uso.
- **Pedidos de acesso, correção e exclusão** são feitos pelo responsável na App 07; a
  aplicação não os recebe. O registro de coleta do território **não é apagado**, e o texto da
  área detalhada diz isso em linguagem simples.
- **Nenhuma imagem real é exibida** em qualquer tela — a representação é sempre por avatar.
- **Nenhum dado pessoal de terceiros** aparece: das outras crianças, só avatar, nick e posição
  no ranking.
- A **pontuação negativa** é dado sensível: o Guerreiro(a) vê a sua, com o motivo, e ela nunca
  aparece em ranking, vitrine ou tela de colega.
- **Apoio escolar com IA**: a pergunta da criança sai do aparelho para o modelo de linguagem, e
  a tela diz isso antes da primeira pergunta, em linguagem simples. O **corpus fechado** é
  também salvaguarda de dados: o modelo responde sobre o material cadastrado, não sobre a
  criança. Nenhum dado pessoal do Guerreiro(a) compõe a pergunta enviada ao modelo, e o
  histórico de consultas fica restrito à gestão — nunca aparece em vitrine, ranking ou App 08.
- **Recusa do assistente** é registrada como qualquer outra recusa e não exclui ninguém: a
  alternativa é perguntar ao Mestre no encontro.

## 12. Critérios de aceite e métricas

- Guerreiro(a) com imagem gravada entra por nick e imagem em poucos segundos; sem câmera, a
  aplicação recusa e explica.
- Falhando a conferência, o Mestre abre a sessão e o Guerreiro(a) opera normalmente.
- Encerrada a sessão, a tela seguinte não mostra nenhum dado do Guerreiro(a) anterior.
- A tela inicial mostra o próximo ponto sem que a criança precise procurar em menu.
- Ponto bloqueado exibe o que falta; desbloqueado o ponto anterior, o seguinte abre na hora.
- Progresso mostra o nível e quantos pontos de trilha faltam para o próximo — e não sobe de
  nível por acúmulo de coleta.
- Nível conquistado não cai depois de uma série interrompida nem de pontuação negativa.
- Registro dentro da faixa pontua na hora; fora da faixa entra como "a conferir" e não pontua.
- Registro invalidado pelo Mestre perde só os seus pontos, e a série continua.
- Duas cadências sem registro marcam a série como interrompida, com os pontos anteriores
  intactos.
- Em partida de quiz, a equipe responde uma vez; a segunda tentativa é recusada e a rede caída
  no meio da pergunta não impede a equipe de continuar.
- Criação de equipe entregue registra o papel de cada integrante; devolvida, mantém a autoria.
- Criação validada de Guerreiro(a) sem autorização do responsável aparece no portfólio interno
  e **não** na vitrine.
- Nenhuma tela oferece comprar recompensa com pontos.
- Sugestão registrada por áudio de 45 segundos é transcrita, entra na fila e exibe status;
  adotada, credita pontos extras sem alterar o nível.
- Pergunta sobre conteúdo cadastrado é respondida em áudio e texto; a mesma pergunta em uma
  disciplina sem conteúdo cadastrado é recusada com a orientação de procurar o Mestre.
- Pergunta que pede a tarefa pronta recebe explicação e caminho, não a resposta final.
- Pergunta imprópria é recusada em linguagem acolhedora e aparece na ocorrência da gestão, sem
  exposição da criança.
- Nenhuma consulta ao apoio escolar credita ponto, badge ou posição no ranking.
- Nenhuma tela exibe imagem real, nome civil ou qualquer dado pessoal de outra criança.

Hipóteses do Ciclo 01 (documento 10): este PRD **sustenta H1** — é a aplicação que mede quantos
Guerreiros e Guerreiras iniciam uma trilha e quantos permanecem até a culminância. Sustenta
**H4**, porque a progressão por dificuldade e o mérito por auxílio são o que faz a turma de 6 a
16 anos funcionar sem segmentar por idade. E instrumenta o critério de **protagonismo** da
avaliação do ciclo: número de criações originais apresentadas e de sugestões registradas.

## 13. Decisões tomadas neste PRD

| Decisão                                                                    | Gravada em      | Linha do doc 09                       |
| -------------------------------------------------------------------------- | --------------- | ------------------------------------- |
| Nível é percurso da trilha, com gates dos níveis 1 a 5 e sem regressão     | 11 §6           | Níveis 1 a 5 — critério de progressão |
| Quiz ao Vivo: um aparelho por equipe, todos que acertam pontuam, desempate | 05 §5 e 11 §5   | Pontuação e regras do Quiz ao Vivo    |
| Criação original vale 50 pontos e badge, integrais a cada integrante       | 11 §5 e 02 §4   | Criação original — pontos e badge     |
| Valores de mérito, batalha, badge de conduta e pontuação negativa (−5)     | 11 §5           | Demais valores do motor de pontuação  |
| Travas de integridade dos pontos, incluindo o valor fora de faixa          | 11 §5.1 e 02 §1 | Integridade dos pontos (antifraude)   |
| Canal de sugestões: texto ou áudio de 60 s, adotada rende extras e badge   | 03 §7           | Canal de sugestões do Guerreiro(a)    |
| Reparação que zera a ocorrência de conduta                                 | 13 §3           | Reparação de ocorrência de conduta    |
| Apoio escolar por assistente de voz na App 05, com IA e corpus fechado     | 03 §§4, 7       | Apoio às atividades escolares         |

As entidades `RespostaDeQuiz`, `DisciplinaDeApoio`, `ConteudoDeApoio` e `ConsultaDeApoio`
foram acrescentadas ao modelo do PRD-01, e `Nivel` passou a ser derivado do percurso. O badge
**de protagonismo** entrou no catálogo do documento 11 §7. O cadastro das disciplinas e do
conteúdo de apoio entrou na App 09 (PRD-09) e na App 03 (PRD-02), e o **apoio às atividades
escolares saiu do Modo Conversa da App 02** (documento 03 §4 e documento 08, PRD-06).

## 14. Pendências que permanecem

- **Cota e custo da IA do apoio escolar**: o consumo é recurso de _cloud_ no livro-razão
  (`RF-05-67`), mas falta o teto de uso por Guerreiro(a) ou por ciclo e o que a aplicação faz
  quando a cota se esgota — sem isso, o `RF-05-58` opera sem limite de gasto.
- **Registro de coleta com a rede fora**: se vai para fila local no aparelho, como a presença
  do App 01, ou se é bloqueado até reconectar. A entrada já exige rede pela conferência da
  imagem.
- **Tempo de inatividade** que encerra a sessão no aparelho compartilhado — o comportamento
  está definido no `RF-05-05`, o número não.
- **Retenção do áudio e da transcrição** da sugestão e da pergunta do apoio escolar: apagar o
  áudio na transcrição, como se faz com a fotografia do onboarding, e por quanto tempo a
  transcrição fica guardada. É o único campo "a definir" da tabela de LGPD deste PRD.
- **Curadoria do conteúdo de apoio escolar**: quem confere o que Mestres e Admins cadastram
  como corpus, no mesmo espírito da auditoria por amostragem das trilhas.
- **Ranking interno**: hoje segue a regra da vitrine e exibe apenas quem tem divulgação
  autorizada. Se a intenção for mostrar a turma inteira dentro da aplicação logada, é decisão
  a tomar e a gravar no documento 03 §12.
- **Catálogo de qual marco entrega qual recompensa** no Ciclo 01: a regra está decidida, o
  catálogo não. **Trava** o `RF-05-45` na prática, não no desenho.
- **Acessibilidade de quem não tem aparelho nem dados móveis** fora do ponto de apoio: os
  desafios on-line entre encontros pressupõem acesso que nem todo Guerreiro(a) tem.

## 15. Rastreabilidade

| Requisito               | Origem                                                                   |
| ----------------------- | ------------------------------------------------------------------------ |
| `RF-05-01` a `RF-05-07` | 03 §1.1 (entrada por nick e imagem) e PRD-04 (onboarding e fallback)     |
| `RF-05-08` a `RF-05-18` | 03 §7 (guia da trilha), 11 §§2, 6 (anatomia e níveis)                    |
| `RF-05-19` a `RF-05-24` | 02 §5 e 11 §§4, 5 (equipes, taxonomia e desafios), 04 §3 (extras)        |
| `RF-05-25` a `RF-05-29` | 05 §5 (Quiz ao Vivo) e PRD-02 (condução da partida)                      |
| `RF-05-30` a `RF-05-38` | 02 §1 e PRD-08 (séries, locais e validade do registro)                   |
| `RF-05-39` a `RF-05-44` | 02 §4, 11 §7 e PRD-09 (culminância, autoria e validação)                 |
| `RF-05-45` a `RF-05-49` | 02 §8 (recompensa em marco) e 05 §3 (acervo e ficha de vida)             |
| `RF-05-50` e `RF-05-51` | 03 §12 (adesão em duas etapas) e 02 §1 (avatar)                          |
| `RF-05-52` e `RF-05-53` | 11 §8.1 (rankings com pontos regulares)                                  |
| `RF-05-54` a `RF-05-56` | 03 §7 (canal de sugestões) e 11 §§5, 7 (pontos extras e badge)           |
| `RF-05-57`              | 03 §12 (aviso visível de coleta e área detalhada)                        |
| `RF-05-58` a `RF-05-66` | 03 §7 (apoio escolar com corpus fechado) e 03 §4 (filtros de segurança)  |
| `RF-05-67` e `RF-05-68` | 04 §1 (custo de _cloud_ no livro-razão) e 01 §7 (transparência sobre IA) |
