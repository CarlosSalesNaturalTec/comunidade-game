# Spec Delta

## MODIFIED Requirements

### Requirement: A App 01 apresenta o percurso do Guerreiro(a) e as atividades das equipes dele

A App 01 SHALL apresentar, a quem tem presença registrada no encontro, o **percurso do próprio
Guerreiro(a)**: as trilhas em que ele está inscrito e, na trilha escolhida, a **missão atual** e a
**seguinte trancada, com o motivo do bloqueio**. A missão seguinte e o motivo SHALL ficar em
**bloco recolhível de resumo neutro**, fora do fluxo de leitura da missão atual: adiantam o que
o Guerreiro(a) ainda não desbloqueou, e a tela existe para ele trabalhar a missão de agora.
Recolhidos, SHALL continuar **alcançáveis** — recolher não é suprimir, e o que a missão
seguinte desbloqueia e o motivo do bloqueio seguem apresentados. NEVER SHALL apresentar a lista
inteira do percurso nem classificar missão como realizada: é o mesmo recorte que a App 05 já
atende, e ele vale aqui sem alteração. (`RF-04-72`, `RF-05-08`, `RF-05-10`, `RF-05-17`,
documento 15 §§6.1, 6.4, decisão do fundador de 2026-09-26)

O aviso que a **própria missão trancada** apresenta a quem tenta abri-la NEVER SHALL ser
recolhido: ali o motivo é a resposta à ação, não informação secundária.

Havendo **mais de uma** trilha inscrita, a aplicação SHALL apresentar a lista das trilhas e SHALL
abrir o percurso da que for escolhida. Havendo **uma**, SHALL abrir o percurso dela direto, sem
lista intermediária. Não havendo **nenhuma**, SHALL levar ao **catálogo de poderes do ciclo**, onde
o Guerreiro(a) escolhe o poder e **inscreve-se na trilha ali mesmo**. (`RF-04-72`, `RF-04-74`)

A inscrição no encontro SHALL seguir as mesmas regras da App 05: a escolha do poder NEVER SHALL ser
teto — ele SHALL poder inscrever-se em quantas trilhas quiser, de um ou de vários poderes — e a
aplicação NEVER SHALL oferecer desinscrição, porque a inscrição não se desfaz. Inscrever-se de novo
na mesma trilha SHALL devolver a inscrição existente, sem erro. Feita a inscrição, a aplicação SHALL
abrir o percurso daquela trilha no mesmo atendimento, na **sondagem**, que é a próxima missão dele.
(`RF-04-74`, `RF-05-09`, `RN-05-43`, `RN-05-44`)

#### Scenario: A missão seguinte aparece trancada, com o motivo

- **WHEN** o percurso de uma trilha é apresentado
- **THEN** a missão atual aparece no fluxo de leitura, e a seguinte trancada fica num bloco
  fechado de resumo neutro, que abre dizendo por que está trancada

#### Scenario: A missão trancada aberta responde com o motivo, sem recolher

- **WHEN** o Guerreiro(a) tenta abrir uma missão que ainda está trancada
- **THEN** o motivo do bloqueio aparece direto na tela, não dentro de um bloco recolhido

#### Scenario: Uma trilha inscrita abre direto no percurso

- **WHEN** o Guerreiro(a) com uma única trilha inscrita alcança as trilhas e missões
- **THEN** a aplicação apresenta o percurso daquela trilha, sem lista de trilhas no caminho

#### Scenario: Inscrito no encontro, o percurso abre na sondagem

- **WHEN** o Guerreiro(a) escolhe um poder e inscreve-se numa trilha pelo aparelho do encontro
- **THEN** o percurso daquela trilha abre no mesmo atendimento, apresentando a missão de sondagem

#### Scenario: Mais de uma trilha inscrita apresenta a lista

- **WHEN** o Guerreiro(a) inscrito em duas trilhas ou mais alcança as trilhas e missões
- **THEN** a aplicação apresenta a lista das trilhas, e a escolhida abre o percurso dela

#### Scenario: Sem inscrição, a tela leva ao catálogo de poderes

- **WHEN** o Guerreiro(a) sem inscrição alguma alcança as trilhas e missões
- **THEN** a aplicação apresenta os poderes do ciclo e as trilhas publicadas de cada um, com o
  caminho de se inscrever

#### Scenario: A inscrição não se desfaz e não tem teto

- **WHEN** o Guerreiro(a) já inscrito escolhe outra trilha, ou a mesma de novo
- **THEN** a nova inscrição acontece e a repetida devolve a que já existe, sem erro; em nenhum
  momento a tela oferece desinscrever-se

#### Scenario: Quem acabou de se inscrever começa na sondagem

- **WHEN** o Guerreiro(a) recém-inscrito abre o percurso da trilha
- **THEN** a missão apresentada é a sondagem, porque é a próxima do percurso segundo o núcleo

#### Scenario: As atividades da aula vêm pelas equipes do Guerreiro(a)

- **WHEN** o Guerreiro(a) integra equipe na aula em curso
- **THEN** as atividades daquela equipe aparecem junto do percurso

#### Scenario: Sem equipe na aula, a tela distingue os dois vazios

- **WHEN** o Guerreiro(a) não integra equipe alguma na aula em curso
- **THEN** a tela diz que não há equipe dele no encontro, com enunciado distinto do de encontro sem
  programação declarada

#### Scenario: O Guerreiro(a) responde à sondagem no encontro

- **WHEN** o Guerreiro(a) recém-inscrito abre a trilha no aparelho do encontro e responde à sondagem
- **THEN** a trilha abre, independentemente de quantas ele acertou, e o percurso aberto é apresentado
  no mesmo atendimento

#### Scenario: O quiz do desbloqueio é aferido pelo núcleo

- **WHEN** o Guerreiro(a) submete o quiz de desbloqueio de uma missão pelo aparelho do encontro
- **THEN** a submissão leva todas as perguntas de uma vez, ao fim da sequência, e a devolutiva diz
  quantas ele acertou

#### Scenario: O desafio prático fica aguardando o Mestre

- **WHEN** o Guerreiro(a) declara ter cumprido um desafio prático de desbloqueio
- **THEN** a missão passa a aguardar o Mestre autor, e em nenhum momento aparece como reprovada

#### Scenario: A entrega individual não acontece por este caminho

- **WHEN** o percurso é apresentado no aparelho do encontro
- **THEN** não há como entregar produção individual da missão por essa tela, e a entrega por equipe
  segue no caminho das equipes

#### Scenario: Sem rede, o percurso não abre

- **WHEN** a rede está fora e alguém escolhe o caminho das trilhas
- **THEN** a aplicação diz que o caminho precisa de rede, como já faz nos caminhos das equipes, do
  quiz e da troca, e nada é enfileirado

### Requirement: O caminho das trilhas leva a equipe à programação do encontro

A App 01 SHALL apresentar à equipe, no caminho das Equipes, em que **missão** da trilha ela
está, o **conteúdo** da missão e a **atividade do dia**, com a bibliografia de apoio
(`RF-04-35`, jornada 5.8).

Havendo mais de uma atividade no encontro, a aplicação SHALL apresentá-las como **escolha da
equipe** — nenhuma é eleita pela aplicação, e a escolha NEVER SHALL ser enviada ao núcleo. É o
encontro assíncrono do documento 05 §4: cada equipe avança no seu ritmo.

A aplicação SHALL mostrar o conteúdo da missão nos tipos que o núcleo serve — texto formatado,
imagem, link externo, vídeo e arquivo de apoio —, **um conteúdo por vez**, com um controle de
**avançar** que leva ao seguinte; avançar SHALL apenas percorrer, e NEVER SHALL gravar nem
enviar coisa alguma. A tela SHALL dizer **onde a equipe está na sequência**, e conteúdo
**único** NEVER SHALL apresentar controle de avançar. A **fonte** do conteúdo de terceiro SHALL
acompanhar o conteúdo a que pertence, e NEVER SHALL ser recolhida: é atribuição de autoria
alheia, não metadado da obra do Mestre. Encontro sem programação declarada SHALL exibir aviso
em linguagem simples, e não erro nem tela vazia. (documento 15 §6.4, decisão do fundador de
2026-09-26)

Nenhuma tela deste caminho SHALL exibir dado pessoal de Guerreiro(a): a equipe segue
identificada por **avatar e nick**, como já vale para a tela das equipes (`RF-04-34`,
`RN-04-14`). (`RF-04-35`, `RF-04-29`, `RN-04-15`, documento 05 §4, PRD-04 §9)

#### Scenario: A equipe vê a missão, o conteúdo e a atividade do dia

- **WHEN** a equipe escolhida entra no caminho das trilhas num encontro com programação
  declarada
- **THEN** a aplicação mostra a missão, o primeiro conteúdo dela e a atividade do dia

#### Scenario: Duas atividades no encontro viram escolha da equipe

- **WHEN** a programação do encontro traz duas atividades, de trilhas diferentes
- **THEN** a aplicação apresenta as duas e a equipe escolhe, sem que a escolha seja enviada ao
  núcleo

#### Scenario: O conteúdo do dia sai um por vez

- **WHEN** a missão do dia traz três conteúdos
- **THEN** o primeiro aparece sozinho, a tela diz onde a equipe está na sequência, e o controle
  de avançar leva ao segundo

#### Scenario: O conteúdo de terceiro sai com a fonte

- **WHEN** a equipe alcança, na sequência, um conteúdo de terceiro
- **THEN** a aplicação exibe a fonte registrada junto do conteúdo, no fluxo de leitura, não
  recolhida

#### Scenario: Nenhum dado pessoal aparece no caminho das trilhas

- **WHEN** a equipe percorre as telas do caminho das trilhas
- **THEN** os integrantes aparecem apenas por avatar e nick, e nenhuma imagem de Guerreiro(a) é
  exibida

#### Scenario: Encontro sem programação avisa em linguagem simples

- **WHEN** a equipe entra no caminho das trilhas num encontro sem programação declarada
- **THEN** a tela avisa em linguagem simples, sem erro e sem tela vazia
