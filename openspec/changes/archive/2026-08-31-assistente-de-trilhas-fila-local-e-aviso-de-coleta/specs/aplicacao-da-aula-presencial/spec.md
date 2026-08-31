## ADDED Requirements

### Requirement: A equipe alcança o assistente de trilhas pela programação e pergunta por texto ou por fala

A App 01 SHALL oferecer o **assistente de trilhas** a partir da programação do encontro, para o
Guerreiro(a) em sessão que integra a equipe, e SHALL aceitar a pergunta **por texto** e **por
fala**, com a alternativa por texto **sempre disponível** — a sala é barulhenta e a fala pode
não sair.

A aplicação SHALL apresentar a resposta em tela e SHALL manter a conversa daquele atendimento
visível enquanto ele durar. A aplicação NEVER SHALL oferecer o assistente a quem não tem sessão
de Guerreiro(a) aberta. (`RF-04-36`, `RF-04-39`, PRD-04 §§5.8, 14)

#### Scenario: A equipe chega ao assistente pela programação

- **WHEN** a equipe está na programação do encontro com a atividade corrente declarada
- **THEN** o assistente de trilhas é alcançável dali

#### Scenario: As duas formas de perguntar estão em tela

- **WHEN** a tela do assistente é apresentada
- **THEN** a equipe pode escrever a pergunta e pode falá-la, sem que uma exclua a outra

#### Scenario: A resposta aparece na tela da equipe

- **WHEN** o núcleo devolve a resposta do assistente
- **THEN** a aplicação a apresenta em tela, junto da pergunta que a originou

### Requirement: O microfone abre por ação do Guerreiro(a) e fecha ao fim da fala

A App 01 SHALL abrir o microfone **somente** quando o Guerreiro(a) aciona o botão de falar, e
SHALL fechá-lo **ao fim da fala**. A aplicação NEVER SHALL manter o microfone aberto entre uma
pergunta e outra, NEVER SHALL captar o áudio ambiente da aula e NEVER SHALL transcrever a
conversa da turma.

O áudio da pergunta SHALL seguir ao núcleo e NEVER SHALL ser gravado no aparelho compartilhado
— nem em arquivo, nem em armazenamento do navegador. (`RF-04-39`, `RF-04-40`, `RN-04-20`,
`RN-04-21`, PRD-04 §11)

#### Scenario: Sem toque não há captação

- **WHEN** a tela do assistente está aberta e ninguém aciona o botão de falar
- **THEN** o microfone permanece fechado e nada é captado

#### Scenario: Terminada a fala, o microfone fecha

- **WHEN** o Guerreiro(a) encerra a pergunta falada
- **THEN** a aplicação fecha o microfone antes de enviar a pergunta

#### Scenario: O áudio não fica no aparelho

- **WHEN** a pergunta falada é enviada
- **THEN** nenhum áudio permanece no aparelho depois do envio

### Requirement: A recusa e o encaminhamento aparecem à equipe como resposta, nunca como erro

A App 01 SHALL apresentar a **recusa explicada** da pergunta fora do corpus e o
**encaminhamento à App 05** da pergunta de tarefa escolar como **resposta do assistente**, na
mesma tela e no mesmo lugar de qualquer outra. A aplicação NEVER SHALL apresentá-las como falha,
erro ou tela de exceção — a equipe perguntou o que podia perguntar.

Não vindo resposta alguma do núcleo, a aplicação SHALL dizer em **uma frase** que o assistente
não respondeu agora e SHALL oferecer perguntar de novo. (`RF-04-37`, `RF-04-38`, PRD-04 §§5.8,
9)

#### Scenario: A recusa vem como resposta

- **WHEN** o núcleo devolve a recusa explicada de uma pergunta fora do corpus
- **THEN** a aplicação a apresenta como resposta do assistente, com a orientação de procurar um
  Mestre no encontro, e nenhuma tela de erro aparece

#### Scenario: A tarefa escolar é encaminhada em tela

- **WHEN** o núcleo devolve o encaminhamento à App 05
- **THEN** a aplicação diz à equipe que esse apoio é da App 05, sem apresentar erro

#### Scenario: O assistente que não respondeu convida a tentar de novo

- **WHEN** o núcleo responde que a resposta está indisponível
- **THEN** a aplicação explica em uma frase e oferece perguntar de novo

### Requirement: A conversa com o assistente termina com o atendimento

A App 01 SHALL descartar a conversa com o assistente ao fim do atendimento, junto com a sessão
do Guerreiro(a), e NEVER SHALL apresentá-la ao próximo que usar o aparelho. A conversa NEVER
SHALL ser gravada no armazenamento do navegador: o que sobrevive é a transcrição no núcleo, que
é do Mestre e da gestão, não da tela seguinte. (`RF-04-28`, PRD-04 §§10, 11)

#### Scenario: O próximo atendimento não vê a conversa anterior

- **WHEN** um atendimento termina e outro Guerreiro(a) abre o assistente no mesmo aparelho
- **THEN** nenhuma pergunta ou resposta do atendimento anterior aparece

### Requirement: Sem rede o assistente fica indisponível, e nenhuma pergunta é enfileirada

A App 01 SHALL apresentar o assistente como **indisponível** enquanto não houver rede, dizendo-o
em uma frase, e NEVER SHALL enfileirar pergunta para envio posterior — resposta que chega depois
do encontro não serve à equipe que perguntou. Voltando a rede, a aplicação SHALL voltar a
aceitar perguntas. (`RF-04-58`, PRD-04 §5.6)

#### Scenario: Sem rede a pergunta não é oferecida

- **WHEN** a equipe tenta perguntar com o aparelho sem rede
- **THEN** a aplicação diz que o assistente está indisponível sem rede, e nada é enfileirado

#### Scenario: Voltando a rede, o assistente volta

- **WHEN** a rede volta
- **THEN** a aplicação volta a aceitar a pergunta, por texto e por fala

### Requirement: A aplicação avisa na tela que está operando sem conexão

A App 01 SHALL apresentar, em **toda tela**, um aviso de que está operando **sem conexão**
enquanto a rede estiver fora, e SHALL retirá-lo assim que a rede voltar. O aviso SHALL dizer, em
linguagem simples, o que continua funcionando e o que não funciona agora — o Mestre na porta
precisa saber sem sair da tela. (`RF-04-23`, `RF-04-24`, PRD-04 §5.6)

#### Scenario: A queda de rede aparece em tela

- **WHEN** uma chamada ao núcleo falha por falta de rede
- **THEN** a aplicação passa a apresentar o aviso de operação sem conexão

#### Scenario: Voltando a rede, o aviso sai

- **WHEN** a rede volta e uma chamada ao núcleo é concluída
- **THEN** a aplicação retira o aviso de operação sem conexão

### Requirement: Sem rede, a presença confirmada pelo Mestre entra na fila local

A App 01 SHALL continuar registrando a **presença** com a rede fora: o Mestre ou o Admin da
sessão de trabalho confirma a criança **pelo nick**, e o registro SHALL entrar na **fila local**
do aparelho, com a **hora do fato** — a hora em que a criança chegou.

A fila SHALL guardar **apenas presença**: nick, hora do fato e a aula do encontro. Ela NEVER
SHALL guardar imagem, fotografia, descritor ou _template_ de criança, e NEVER SHALL enfileirar
cadastro, resposta de quiz, produção da missão, troca ou consulta ao assistente. (`RF-04-23`,
`RN-04-12`, `RN-04-13`, PRD-04 §8)

#### Scenario: A criança que chega sem rede entra na aula

- **WHEN** a rede está fora e o Mestre confirma pelo nick a criança que chegou
- **THEN** a aplicação enfileira a presença com a hora do fato e diz à criança que ela está na
  aula

#### Scenario: A fila não guarda imagem

- **WHEN** se examina o que a aplicação guardou no aparelho durante a queda
- **THEN** há apenas presença enfileirada, e nenhuma imagem, descritor ou _template_

#### Scenario: Só a presença é enfileirada

- **WHEN** a rede cai durante um cadastro, uma partida, uma entrega de produção ou uma troca
- **THEN** nada disso vai para a fila local

### Requirement: Sem rede, cadastro novo e reconhecimento facial ficam indisponíveis

A App 01 SHALL apresentar o **cadastro novo** e a **entrada por reconhecimento facial** como
indisponíveis enquanto não houver rede, com aviso na tela dizendo por quê: o descritor nasce no
aparelho, mas a **comparação é no núcleo**, e nenhuma imagem de criança fica guardada no
aparelho compartilhado.

A aplicação SHALL oferecer, no lugar deles, a **confirmação pelo Mestre ou Admin** — a
alternativa equivalente que o `RN-04-09` garante. (`RF-04-24`, `RN-04-12`, PRD-04 §5.6)

#### Scenario: Sem rede o onboarding não abre

- **WHEN** alguém escolhe o caminho do onboarding com a rede fora
- **THEN** a aplicação diz que o cadastro exige rede e não coleta dado algum

#### Scenario: Sem rede a câmera não é oferecida

- **WHEN** o Guerreiro(a) chega à entrada com a rede fora
- **THEN** a aplicação não oferece a entrada por reconhecimento e encaminha à confirmação pelo
  Mestre ou Admin

### Requirement: A fila sincroniza sozinha, preservando a hora do fato e sem duplicar

A App 01 SHALL sincronizar a fila local **sozinha**, assim que a rede voltar, sem ato de
ninguém, enviando cada presença com a **hora do fato** — nunca a hora do envio. O núcleo devolve
o registro já existente sem erro, e a aplicação SHALL tratar essa devolução como **sucesso**,
retirando o item da fila: presença reenviada NEVER SHALL virar registro novo nem erro em tela.

Sincronizado o item, a aplicação SHALL **descartá-lo da fila**. (`RF-04-25`, `RN-04-13`,
PRD-04 §§5.6, 8)

#### Scenario: A rede volta e a fila anda sozinha

- **WHEN** a rede volta com presenças na fila local
- **THEN** a aplicação as envia sem que ninguém acione nada

#### Scenario: A hora do fato é a da chegada

- **WHEN** uma presença enfileirada às 14h é enviada às 15h
- **THEN** a presença registrada no núcleo aponta a hora da chegada, não a do envio

#### Scenario: O reenvio não duplica nem alarma

- **WHEN** o núcleo devolve o registro que já existia para uma presença da fila
- **THEN** a aplicação tira o item da fila sem apresentar erro, e nenhum registro novo nasce

#### Scenario: Sincronizada, a presença some do aparelho

- **WHEN** uma presença da fila é sincronizada
- **THEN** ela é descartada do aparelho e não é reenviada de novo

### Requirement: O que falha na sincronização fica visível ao Mestre presente

A App 01 SHALL apresentar ao **Mestre ou Admin da sessão de trabalho** o que ainda está na fila
e o que **falhou** ao sincronizar — o nick e a hora do fato de cada um —, e SHALL permitir que
ele **tente de novo**. A aplicação NEVER SHALL apresentar essa lista ao Guerreiro(a) nem em tela
de atendimento dele.

A falha de sincronização NEVER SHALL ser reportada ao núcleo nesta fatia: a fila é estado do
aparelho, e listá-la no painel do dia é pendência aberta (PRD-04 §5.6.5, documento 09 §1,
decisão do fundador de 2026-08-30). (`RF-04-23`, `RF-04-25`, `RN-04-14`)

#### Scenario: O Mestre vê o que ainda não subiu

- **WHEN** o Mestre em sessão de trabalho consulta a fila local
- **THEN** a aplicação lista o nick e a hora do fato de cada presença pendente ou falha

#### Scenario: O Mestre tenta de novo

- **WHEN** o Mestre aciona a nova tentativa de um item que falhou
- **THEN** a aplicação o reenvia, e o retira da fila se o núcleo o aceitar

#### Scenario: A fila não aparece para a criança

- **WHEN** um Guerreiro(a) usa o aparelho
- **THEN** nenhuma tela dele apresenta a fila local nem o nick de outra criança

### Requirement: A tela inicial e a tela de captura avisam o que a aplicação coleta

A App 01 SHALL apresentar, na **tela inicial** e na **tela de captura da imagem**, um aviso
**discreto** do que a aplicação coleta, com um **caminho alcançável** para a área detalhada de
direitos. O aviso SHALL estar em linguagem de criança e NEVER SHALL ocupar a tela a ponto de
disputar com o que se está fazendo — o aparelho é operado de pé, na porta da aula.
(`RF-04-26`, `RN-03-23`, PRD-04 §§10, 11)

#### Scenario: A tela inicial traz o aviso

- **WHEN** a tela inicial é apresentada
- **THEN** ela traz o aviso discreto do que a aplicação coleta, com caminho para a área
  detalhada

#### Scenario: A tela de captura traz o aviso

- **WHEN** a tela de captura da imagem é apresentada
- **THEN** ela traz o aviso do que está sendo coletado ali, com caminho para a área detalhada

### Requirement: A área detalhada diz o destino de cada dado e o canal do responsável

A App 01 SHALL apresentar uma **área detalhada de direitos**, alcançável dos avisos, dizendo em
linguagem simples, para **cada dado que a aplicação coleta**: para que serve, por quanto tempo
fica e quem o acessa — como o PRD-04 §11 os declara.

A área SHALL dizer ainda que:

- a **fotografia é apagada** assim que o _template_ é gerado, e nunca sai do aparelho;
- a **imagem nunca é exibida** a ninguém — não vira avatar, não vai para a vitrine, não aparece
  em ranking e não é mostrada a outro Guerreiro(a);
- **recusar a biometria não exclui ninguém**: a confirmação do Mestre no encontro é a
  alternativa equivalente;
- **pedido de acesso, correção ou exclusão é do responsável, pela App 07, com resposta em 7
  dias** — a aplicação NEVER SHALL atendê-los nem prometer atendê-los.

(`RF-04-26`, `RN-04-06`, `RN-04-08`, `RN-04-09`, `RN-04-14`, PRD-04 §11)

#### Scenario: A área detalha cada dado coletado

- **WHEN** alguém abre a área detalhada de direitos
- **THEN** ela apresenta, para cada dado coletado, a finalidade, o prazo de guarda e quem acessa

#### Scenario: A área diz o canal e o prazo

- **WHEN** a área detalhada é lida até o fim
- **THEN** ela diz que o pedido de acesso, correção ou exclusão é feito pelo responsável na
  App 07, com resposta em 7 dias

#### Scenario: A aplicação não recebe pedido de direitos

- **WHEN** alguém procura, na área detalhada, um jeito de pedir exclusão ali mesmo
- **THEN** não há nenhum: a aplicação apenas informa o canal

### Requirement: A conversa do onboarding encerra dizendo como entrar da próxima vez

A App 01 SHALL encerrar o atendimento do onboarding dizendo ao Guerreiro(a), em linguagem
simples, **como ele entra da próxima vez**, conforme o cadastro tenha ficado com ou sem imagem:

- **com imagem capturada**: pelo nick e pela câmera;
- **sem imagem** — sem responsável presente, sem câmera no aparelho ou por recusa da biometria
  —: pelo nick, com a **confirmação do Mestre ou do Admin** no encontro, dito como o caminho
  normal dele e nunca como falta.

Dita a despedida, a aplicação SHALL voltar à tela inicial, pronta para o próximo.
(`RF-04-27`, `RF-04-28`, `RN-04-09`, PRD-04 §§5.2, 5.3)

#### Scenario: Quem capturou a imagem ouve o caminho da câmera

- **WHEN** o cadastro termina com a imagem capturada
- **THEN** a aplicação diz que da próxima vez ele entra pelo nick e pela câmera

#### Scenario: Quem ficou sem imagem ouve o caminho do Mestre

- **WHEN** o cadastro termina sem imagem
- **THEN** a aplicação diz que da próxima vez ele entra pelo nick, com o Mestre confirmando, sem
  tratar isso como problema

#### Scenario: A despedida devolve o aparelho ao início

- **WHEN** a despedida é apresentada e o atendimento se encerra
- **THEN** a aplicação volta à tela inicial, sem dado algum do atendimento anterior
