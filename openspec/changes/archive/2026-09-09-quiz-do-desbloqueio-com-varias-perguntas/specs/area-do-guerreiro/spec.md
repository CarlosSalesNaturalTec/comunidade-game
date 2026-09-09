## MODIFIED Requirements

### Requirement: O Guerreiro(a) faz o desafio de desbloqueio e repete sem ser punido

A aplicação SHALL permitir ao Guerreiro(a) **realizar o desafio de desbloqueio** da missão. No
**quiz**, a tela SHALL apresentar **todas as perguntas** do desafio, na ordem declarada pelo
Mestre autor, e SHALL submeter as respostas **de uma vez só**, nunca uma pergunta por
submissão; pergunta ainda **sem resposta** SHALL ser sinalizada antes do envio. **Passando**, a
missão seguinte SHALL abrir **na hora**, sem recarregar a aplicação nem esperar ato de
terceiro. **Não passando**, a tela SHALL dizer **quantas perguntas ele acertou** e de quantas, e
SHALL oferecer **tentar de novo** em linguagem acolhedora, sem contagem de fracassos, sem
punição e sem qualquer mensagem que elimine ou classifique a criança. Na **missão de sondagem**,
a tela NEVER SHALL apresentar o resultado como aprovação ou reprovação: respondida, a trilha
segue. (`RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-20`, `RN-05-45`, `RN-05-46`)

#### Scenario: Passar abre a seguinte na hora

- **WHEN** o Guerreiro(a) responde a todas as perguntas do quiz, submete e passa
- **THEN** a missão seguinte aparece aberta imediatamente no percurso dele

#### Scenario: A submissão leva todas as respostas de uma vez

- **WHEN** o Guerreiro(a) abre um quiz de seis perguntas
- **THEN** a tela mostra as seis e só envia quando ele conclui, numa única submissão

#### Scenario: Pergunta sem resposta é sinalizada

- **WHEN** o Guerreiro(a) tenta enviar o quiz com uma pergunta ainda sem alternativa escolhida
- **THEN** a tela aponta a pergunta que falta e não envia

#### Scenario: Não passar convida a tentar de novo

- **WHEN** o Guerreiro(a) submete o quiz e não passa
- **THEN** a tela diz quantas perguntas ele acertou, de quantas, e o convida a tentar de novo,
  sem punição e sem exibir contagem de fracassos

#### Scenario: A sondagem não fala em aprovação

- **WHEN** o Guerreiro(a) responde a missão de sondagem
- **THEN** a tela agradece e segue para a trilha, sem dizer que ele passou ou não passou
