## ADDED Requirements

### Requirement: A App 05 abre na próxima missão do Guerreiro(a)

A aplicação SHALL abrir o bloco da trilha na **próxima missão** do Guerreiro(a) em sessão,
dizendo **o que fazer** e **o que ela desbloqueia**, sem que a criança precise procurar em
menu. O Guerreiro(a) inscrito em **mais de uma trilha** SHALL alternar entre elas **preservando
o contexto** de cada uma — a missão aberta numa trilha continua aberta ao voltar a ela. Sem
nenhuma inscrição, a tela SHALL levar à escolha do poder, nunca a uma tela vazia sem saída.
(`RF-05-08`, `RF-05-17`, PRD-05 §5.2)

#### Scenario: A tela inicial já mostra o que fazer agora

- **WHEN** o Guerreiro(a) inscrito abre o bloco da trilha
- **THEN** vê a próxima missão, o que precisa ser feito nela e o que ela desbloqueia

#### Scenario: Alternar de trilha não perde o contexto

- **WHEN** o Guerreiro(a) inscrito em duas trilhas alterna para a outra e volta
- **THEN** cada trilha reabre no ponto em que ele a deixou

#### Scenario: Sem inscrição, a tela oferece o caminho

- **WHEN** um Guerreiro(a) sem nenhuma inscrição abre o bloco da trilha
- **THEN** a tela o leva à escolha do poder, em vez de mostrar tela vazia

### Requirement: O Guerreiro(a) escolhe o poder e inscreve-se nas trilhas dele

A aplicação SHALL exibir os **poderes do catálogo do ciclo** e, escolhido um, as **trilhas
publicadas** dele, permitindo ao Guerreiro(a) **inscrever-se**. A escolha do poder NEVER SHALL
ser teto: ele SHALL poder inscrever-se em **quantas trilhas quiser**, de um ou de vários
poderes. A tela NEVER SHALL oferecer desinscrição, porque a inscrição não se desfaz.
(`RF-05-09`, `RN-05-43`, `RN-05-44`)

#### Scenario: Escolher o poder leva às trilhas dele

- **WHEN** o Guerreiro(a) escolhe um poder do catálogo
- **THEN** vê as trilhas publicadas daquele poder, com o caminho de se inscrever em cada uma

#### Scenario: Inscrição confirmada abre o percurso

- **WHEN** o Guerreiro(a) se inscreve numa trilha
- **THEN** a trilha passa a constar entre as dele e o percurso abre na missão de sondagem

#### Scenario: Nenhuma tela oferece desinscrever

- **WHEN** o Guerreiro(a) abre uma trilha em que está inscrito
- **THEN** nenhuma ação de sair, cancelar ou desfazer a inscrição é oferecida

### Requirement: A missão bloqueada diz o motivo, nunca é cadeado mudo

A aplicação SHALL exibir a missão **bloqueada** com o **motivo do bloqueio** e **o que falta
para abri-la**, em linguagem que a faixa de 6 a 16 anos entenda. NEVER SHALL exibir bloqueio
sem explicação. A missão **opcional** SHALL vir **marcada como tal**, com a tela dizendo que
ela **não conta** no que falta para o próximo nível. (`RF-05-10`, `RF-05-81`, `RN-05-20`,
`RN-05-33`)

#### Scenario: O bloqueio nomeia o que falta

- **WHEN** o Guerreiro(a) vê uma missão que ainda não pode abrir
- **THEN** a tela diz qual missão falta desbloquear, em linguagem simples

#### Scenario: A opcional aparece marcada e fora da conta

- **WHEN** o percurso traz uma missão opcional
- **THEN** ela aparece marcada como opcional, e a tela diz que ela não conta para o próximo
  nível

### Requirement: O Guerreiro(a) percorre o conteúdo e a bibliografia da missão

A aplicação SHALL exibir o **conteúdo da missão** — texto, imagens, vídeo e arquivos — na ordem
em que o Mestre autor o dispôs, com o **crédito ao autor** e a **licença** que a trilha
publicada declara. A **bibliografia** SHALL indicar **título** e **capítulo** e, quando o
Guerreiro(a) tiver ponto de apoio, **se há exemplar disponível nele**; sem essa informação, a
disponibilidade SHALL ficar **indeterminada**, nunca afirmada nem negada por suposição.
(`RF-05-11`, `RF-05-12`)

#### Scenario: O conteúdo abre na ordem do autor

- **WHEN** o Guerreiro(a) abre uma missão desbloqueada
- **THEN** percorre o conteúdo dela na ordem declarada, com crédito ao Mestre autor e a licença

#### Scenario: A bibliografia diz onde encontrar o livro

- **WHEN** a missão traz bibliografia vinculada a exemplar do ponto de apoio do Guerreiro(a)
- **THEN** a tela indica título, capítulo e se há exemplar disponível nele

#### Scenario: Sem vínculo, a disponibilidade não é afirmada

- **WHEN** a bibliografia da missão não está vinculada a exemplar tombado
- **THEN** a tela mostra título e capítulo e nada afirma sobre disponibilidade

### Requirement: O Guerreiro(a) responde à sondagem que abre a trilha

A aplicação SHALL apresentar a **missão de sondagem** como o primeiro passo da trilha recém
inscrita, e a tela SHALL dizer, em linguagem simples, que ela serve para **o Mestre ajustar** o
que vem pela frente e que o resultado dela **não muda o nível** de ninguém. NEVER SHALL
apresentar a sondagem como prova nem exibir acerto e erro como nota. (`RF-05-72`, `RF-05-73`,
`RN-05-34`)

#### Scenario: A sondagem abre a trilha

- **WHEN** o Guerreiro(a) abre uma trilha em que acabou de se inscrever
- **THEN** a missão de sondagem é o primeiro passo apresentado

#### Scenario: A tela explica para que serve a sondagem

- **WHEN** o Guerreiro(a) está respondendo a sondagem
- **THEN** a tela diz que ela serve para o Mestre ajustar e que não muda o nível dele

### Requirement: O Guerreiro(a) faz o desafio de desbloqueio e repete sem ser punido

A aplicação SHALL permitir ao Guerreiro(a) **realizar o desafio de desbloqueio** da missão.
**Passando**, a missão seguinte SHALL abrir **na hora**, sem recarregar a aplicação nem esperar
ato de terceiro. **Não passando**, a tela SHALL oferecer **tentar de novo** em linguagem
acolhedora, sem contagem de fracassos, sem punição e sem qualquer mensagem que elimine ou
classifique a criança. (`RF-05-13`, `RF-05-14`, `RN-05-20`)

#### Scenario: Passar abre a seguinte na hora

- **WHEN** o Guerreiro(a) realiza o desafio de desbloqueio e passa
- **THEN** a missão seguinte aparece aberta imediatamente no percurso dele

#### Scenario: Não passar convida a tentar de novo

- **WHEN** o Guerreiro(a) realiza o desafio e não passa
- **THEN** a tela o convida a tentar de novo, sem punição e sem exibir contagem de fracassos

### Requirement: O progresso mostra o nível e o que falta, nunca saldo de pontos

A aplicação SHALL exibir, por trilha ou poder, o **nível** do Guerreiro(a) e **quantas missões
obrigatórias faltam** para o próximo — nível é **percurso**, não saldo. SHALL exibir também os
**pontos, badges e recompensas conquistadas** por trilha ou poder, nunca de forma global, e
NEVER SHALL apresentar o nível como decorrência do total de pontos. Resultado ainda **não
lançado pelo Mestre** SHALL aparecer como **"aguardando lançamento"**, e a aplicação NEVER
SHALL lançar resultado, presença ou mérito. (`RF-05-15`, `RF-05-16`, `RF-05-18`, `RN-05-03`,
`RN-05-04`, `RN-05-06`)

#### Scenario: O progresso diz quantas faltam

- **WHEN** o Guerreiro(a) abre o progresso de uma trilha
- **THEN** vê o nível atual e quantas missões obrigatórias faltam para o próximo

#### Scenario: Nada sobe de nível por acúmulo de pontos

- **WHEN** o Guerreiro(a) acumula pontos sem desbloquear missão obrigatória
- **THEN** o nível exibido não muda

#### Scenario: O que o Mestre ainda não lançou aparece como tal

- **WHEN** o Guerreiro(a) cumpriu uma atividade cujo Resultado o Mestre ainda não lançou
- **THEN** a tela mostra "aguardando lançamento", sem creditar ponto nem avançar o nível

#### Scenario: Nenhuma tela lança resultado

- **WHEN** o Guerreiro(a) percorre qualquer tela do bloco da trilha
- **THEN** nenhuma ação de lançar resultado, presença ou mérito é oferecida
