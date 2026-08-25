## ADDED Requirements

### Requirement: O aparelho entra na partida pela sessão do Guerreiro(a), e a equipe vem do núcleo

A App 01 SHALL levar quem escolhe o caminho do quiz à **entrada do Guerreiro(a) por nick e
imagem** quando não houver sessão dele aberta, nunca ao cadastro — o mesmo caminho da entrada
já em uso. Aberta a sessão, a aplicação SHALL perguntar ao núcleo as partidas da aula e SHALL
usar **a equipe que o núcleo derivou**, sem oferecer escolha de equipe em tela alguma. O
vínculo entre o aparelho e a equipe é **estado do próprio aparelho**, guardado na sessão dele e
desfeito ao fim do atendimento; a aplicação NEVER SHALL enviá-lo ao núcleo como registro nem
supor que o núcleo o guarde (documento 05 §5, decisão do fundador de 2026-08-25).

Não havendo partida na aula, ou não disputando o Guerreiro(a) por nenhuma equipe, a aplicação
SHALL dizê-lo em uma frase e SHALL oferecer a volta ao início, sem tela de resposta.
(`RF-04-41`, `RF-04-42`)

#### Scenario: Sem sessão aberta, o quiz leva à entrada

- **WHEN** alguém escolhe o caminho do quiz sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada por nick e imagem, e nenhuma tela de cadastro aparece

#### Scenario: A equipe não é escolhida em tela

- **WHEN** o Guerreiro(a) entra e o núcleo devolve a equipe pela qual ele disputa
- **THEN** a aplicação usa aquela equipe, e em nenhum momento pede que ele escolha entre equipes

#### Scenario: Sem partida, a tela explica e volta

- **WHEN** a aula não tem partida aberta, ou o Guerreiro(a) não disputa por nenhuma equipe
- **THEN** a aplicação explica em uma frase e oferece a volta ao início, sem tela de resposta

#### Scenario: O atendimento seguinte não herda a equipe

- **WHEN** o atendimento termina e outro Guerreiro(a) entra no mesmo aparelho
- **THEN** a equipe do atendimento anterior não aparece, e a do novo vem do núcleo

### Requirement: A tela da partida acompanha a pergunta por sondagem a cada 2 segundos

A App 01 SHALL manter a tela da partida atualizada **sondando o núcleo a cada 2 segundos**, sem
recarga manual e sem conexão longa (documento 03 §1, decisão do fundador de 2026-08-25). A
pergunta no ar SHALL aparecer com o enunciado e as quatro alternativas. Sondagem que falha por
rede NEVER SHALL derrubar a partida nem apagar o que já está na tela: a aplicação SHALL avisar
que perdeu contato e SHALL retomar a pergunta corrente na sondagem seguinte, ainda que outra
tenha entrado no ar enquanto o aparelho esteve fora. (`RF-04-41`, `RF-04-58`, PRD-04 §12)

#### Scenario: A pergunta aparece sem recarga

- **WHEN** quem conduz põe uma pergunta no ar
- **THEN** ela aparece no aparelho da equipe na sondagem seguinte, sem que ninguém recarregue

#### Scenario: A rede caída no meio da pergunta não tira a equipe da partida

- **WHEN** a rede cai durante uma pergunta e volta depois de outra ter entrado no ar
- **THEN** a tela avisa que perdeu contato, mantém o que exibia e passa a mostrar a pergunta
  corrente, sem recuperar a que perdeu

#### Scenario: Entre uma pergunta e outra a tela espera

- **WHEN** nenhuma pergunta está no ar
- **THEN** a aplicação diz que a próxima pergunta está por vir, sem oferecer resposta

### Requirement: A equipe responde uma vez, e a aplicação recusa a segunda antes de enviar

A App 01 SHALL enviar **uma** resposta por equipe e pergunta e SHALL recusar a segunda **antes
de chegar ao núcleo**, dizendo em linguagem simples que a equipe já respondeu. A resposta
enviada SHALL valer para todos os integrantes da equipe. Recusada a segunda pelo núcleo — por
reenvio que cruzou com outro aparelho da mesma equipe —, a aplicação SHALL apresentar a mesma
mensagem, sem tratar a recusa como erro do aparelho. Enviada a resposta, a alternativa
escolhida SHALL permanecer em tela até a pergunta seguinte. (`RF-04-43`, PRD-04 §12)

#### Scenario: A equipe responde e a escolha fica em tela

- **WHEN** a equipe escolhe uma alternativa e envia
- **THEN** a aplicação confirma o envio e mantém a alternativa escolhida em tela até a pergunta
  seguinte

#### Scenario: A segunda tentativa é recusada na tela

- **WHEN** alguém tenta responder de novo a mesma pergunta no mesmo aparelho
- **THEN** a aplicação recusa antes de enviar, dizendo que a equipe já respondeu

#### Scenario: A recusa do núcleo por outro aparelho da equipe não vira erro

- **WHEN** o núcleo recusa a resposta porque outro aparelho da mesma equipe já respondeu
- **THEN** a aplicação apresenta a mesma mensagem de que a equipe já respondeu, sem tela de erro

### Requirement: O resultado aparece à equipe quando quem conduz o libera

A App 01 SHALL manter oculto o resultado da pergunta enquanto quem conduz não o liberar, e
NEVER SHALL revelar a alternativa correta antes disso. Liberado, a aplicação SHALL apresentar a
**alternativa correta**, **se a equipe acertou** e **qual equipe chegou primeiro**. A aplicação
NEVER SHALL exibir pontuação da partida: o crédito é do encerramento e aparece pelos pontos do
Guerreiro(a), não por esta tela. (`RF-04-44`)

#### Scenario: Antes da liberação nada do resultado aparece

- **WHEN** a equipe respondeu e quem conduz ainda não liberou o resultado
- **THEN** a tela não mostra a alternativa correta nem diz se a equipe acertou

#### Scenario: Liberado, a equipe vê se acertou

- **WHEN** quem conduz libera o resultado
- **THEN** a tela mostra a alternativa correta, se a equipe acertou e qual equipe chegou
  primeiro

#### Scenario: A tela da partida não mostra pontuação

- **WHEN** o resultado de qualquer pergunta é liberado
- **THEN** nenhuma pontuação da partida aparece em tela

### Requirement: Sem rede, a resposta de quiz fica indisponível e a partida não trava

A App 01 SHALL manter legível a pergunta já carregada quando a rede cair, e SHALL apresentar a
resposta como **indisponível** enquanto não houver rede, dizendo-o em uma frase. A aplicação
NEVER SHALL enfileirar resposta de quiz para envio posterior — a ordem de chegada no servidor é
o critério de desempate, e resposta atrasada falsearia a disputa. Voltando a rede, a aplicação
SHALL retomar a sondagem e SHALL permitir a resposta da pergunta corrente, se a equipe ainda
não respondeu. (`RF-04-58`, documento 05 §5)

#### Scenario: A pergunta carregada continua legível sem rede

- **WHEN** a rede cai com uma pergunta em tela
- **THEN** o enunciado e as alternativas continuam legíveis

#### Scenario: Sem rede a resposta não é oferecida

- **WHEN** a equipe tenta responder com o aparelho sem rede
- **THEN** a aplicação diz que a resposta está indisponível sem rede, e nada é enfileirado

#### Scenario: Voltando a rede, a equipe responde a pergunta corrente

- **WHEN** a rede volta e a equipe ainda não respondeu a pergunta corrente
- **THEN** a aplicação retoma a sondagem e oferece a resposta

## MODIFIED Requirements

### Requirement: A tela inicial oferece os dois caminhos e volta ao início a cada atendimento

A App 01 SHALL apresentar, na tela inicial, os dois caminhos — **onboarding** e **trilhas**. Ao
fim de cada atendimento, a aplicação SHALL voltar à tela inicial e NEVER SHALL exibir dado do
atendimento anterior. Quem escolhe **trilhas** sem sessão de Guerreiro(a) aberta SHALL ser
levado à entrada do Guerreiro(a), nunca ao cadastro.

Com o **momento de troca aberto**, a tela inicial SHALL apresentar também o caminho da **troca
por recompensa avulsa**, ao lado dos dois. Fechado o momento — que é o estado em que a aplicação
começa —, o caminho NEVER SHALL aparecer.

A tela inicial SHALL apresentar ainda o caminho do **quiz**, sempre disponível na sessão de
trabalho: diferentemente da troca, o PRD-04 não põe a partida atrás de um momento aberto por
Mestre, e é a própria tela do quiz que diz não haver partida quando não há. (`RF-04-01`,
`RF-04-28`, `RF-04-41`, `RF-04-49`, PRD-04 §12)

#### Scenario: Os dois caminhos aparecem

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o caminho do onboarding e o caminho das trilhas

#### Scenario: Trilhas sem sessão leva à entrada, não ao cadastro

- **WHEN** alguém escolhe trilhas sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada do Guerreiro(a), e nenhuma tela de cadastro aparece

#### Scenario: O atendimento seguinte começa limpo

- **WHEN** um atendimento termina e a aplicação volta à tela inicial
- **THEN** nenhum dado do atendimento anterior aparece em tela alguma

#### Scenario: O terceiro caminho só existe com o momento de troca aberto

- **WHEN** o Mestre abre o momento de troca
- **THEN** a tela inicial passa a apresentar também o caminho da troca, e volta a escondê-lo
  quando o momento é fechado

#### Scenario: O caminho do quiz não depende de momento aberto

- **WHEN** a sessão de trabalho está aberta e o momento de troca está fechado
- **THEN** a tela inicial apresenta o caminho do quiz
