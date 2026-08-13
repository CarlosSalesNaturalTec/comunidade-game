## MODIFIED Requirements

### Requirement: Ponto regular é creditado por trilha ou poder e nunca debitado

O núcleo SHALL creditar **ponto regular** por **trilha ou poder** — nunca globalmente — a partir
de um Resultado, de uma **Criação Original validada** ou de uma **partida de quiz encerrada**,
conforme a fonte e o valor da tabela do documento 11 §5. Na criação original, o valor SHALL ser
creditado **integral a cada integrante** da equipe da trilha que a entregou, sem divisão. Na
partida de quiz, o crédito SHALL seguir a régua própria dela e alcançar **cada integrante** da
equipe. O ponto regular SHALL **nunca ser debitado**, em nenhuma operação. (`RF-01-21`,
`RF-01-64`, `RN-01-38`, 11 §5)

#### Scenario: Resultado "realizada" credita o valor da atividade

- **WHEN** um Resultado é lançado com desfecho "realizada"
- **THEN** o núcleo credita, à trilha ou ao poder correspondente, o ponto regular da fonte da
  atividade

#### Scenario: Resultado "realizada com mérito" credita o valor mais o adicional de mérito

- **WHEN** um Resultado é lançado com desfecho "realizada com mérito"
- **THEN** o núcleo credita o ponto regular da atividade acrescido do adicional de mérito da
  tabela do documento 11 §5

#### Scenario: Ponto regular não aceita débito

- **WHEN** qualquer operação tenta reduzir o saldo de ponto regular de um Guerreiro(a)
- **THEN** o núcleo recusa a operação

#### Scenario: Criação original validada credita 50 pontos regulares

- **WHEN** o Mestre autor valida uma criação original entregue por uma equipe de três integrantes
- **THEN** o núcleo credita, à trilha da criação, 50 pontos regulares integrais a **cada um** dos
  três

#### Scenario: O valor da criação original não se divide pela equipe

- **WHEN** duas equipes de tamanhos diferentes têm a criação original validada na mesma trilha
- **THEN** cada integrante das duas recebe os mesmos 50 pontos, sem rateio pelo tamanho

#### Scenario: Partida de quiz encerrada credita a trilha da atividade

- **WHEN** uma partida de quiz sobre uma atividade da trilha 1 é encerrada com acertos
- **THEN** o núcleo credita o ponto regular apurado à trilha 1, e não à aula nem a outra trilha

## ADDED Requirements

### Requirement: A partida de quiz credita 1 por acerto, 1 de bônus à primeira e no máximo 10

O núcleo SHALL apurar, ao encerrar a partida de quiz, **1 ponto regular por pergunta acertada**
pela equipe e **1 ponto de bônus** à **primeira equipe** que acertar cada pergunta, tomando a
ordem pelo **momento de chegada ao servidor**. O total creditado por partida SHALL ser limitado
a **10 pontos**; apuração acima do teto SHALL ser creditada como 10. O valor apurado SHALL ser
creditado a **cada integrante** da equipe, sem rateio pelo tamanho dela, na **trilha da
atividade** sobre a qual a partida corre. Pergunta anulada NÃO SHALL entrar na apuração.
(`RF-01-21`, `RF-01-36`, `RN-01-38`, `RN-01-42`, documento 11 §5, documento 05 §5)

#### Scenario: Acerto credita 1 ponto a cada integrante

- **WHEN** uma equipe de quatro integrantes acerta uma pergunta e não é a primeira a acertá-la
- **THEN** o núcleo credita 1 ponto regular a cada um dos quatro, na trilha da atividade da
  partida

#### Scenario: Primeira a acertar recebe o bônus

- **WHEN** duas equipes acertam a mesma pergunta e a resposta de uma chegou antes ao servidor
- **THEN** a que chegou antes recebe 2 pontos por integrante, e a outra recebe 1

#### Scenario: O teto de 10 por partida é respeitado

- **WHEN** uma equipe acumula apuração de 13 pontos numa mesma partida
- **THEN** o núcleo credita 10 pontos a cada integrante, e não 13

#### Scenario: O valor da partida não se divide pela equipe

- **WHEN** duas equipes de tamanhos diferentes acertam o mesmo número de perguntas na mesma
  partida
- **THEN** cada integrante das duas recebe o mesmo total, sem rateio pelo tamanho

#### Scenario: Pergunta anulada fica fora da apuração

- **WHEN** uma partida encerra com uma das perguntas anulada pelo Mestre
- **THEN** a apuração considera apenas as perguntas não anuladas, e nenhum ponto já creditado é
  debitado

#### Scenario: Erro não credita nem debita

- **WHEN** uma equipe erra uma pergunta da partida
- **THEN** o núcleo não credita ponto por ela e não reduz o saldo da equipe nem de nenhum
  integrante
