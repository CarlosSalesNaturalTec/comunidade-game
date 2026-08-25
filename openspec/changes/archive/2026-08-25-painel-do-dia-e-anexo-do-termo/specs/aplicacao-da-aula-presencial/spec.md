## ADDED Requirements

### Requirement: A equipe declara pelo aparelho em que atividade da programação está

A App 01 SHALL oferecer, na tela da programação do encontro, a **escolha** da atividade em que a
equipe vai trabalhar, e SHALL declará-la ao núcleo. É o que enche a missão de cada equipe no
painel do dia da App 03 (`RF-02-42`) e o que fecha o "a missão **em que está**" do `RF-04-35`.

A escolha SHALL ser **trocável** durante o encontro, quantas vezes a equipe quiser, e a tela
SHALL mostrar qual está corrente. A aplicação NEVER SHALL escolher por conta própria quando a
programação traz mais de uma atividade: sem declaração da equipe, a escolha fica em branco.

A declaração SHALL exigir rede. Sem rede, o **conteúdo já carregado continua legível** e a
aplicação SHALL dizer que a escolha não é declarada agora, **sem enfileirar** a declaração —
mesma regra da resposta de quiz, porque o que o painel mostra tem de ser o que está acontecendo
(`RF-04-58`). (`RF-04-35`, `RF-02-42`, `RF-04-58`, PRD-04 §6.2)

#### Scenario: A equipe escolhe a atividade e o aparelho declara

- **WHEN** a equipe escolhe uma das atividades da programação
- **THEN** a aplicação declara a escolha ao núcleo e a apresenta como corrente

#### Scenario: A equipe troca de atividade no mesmo encontro

- **WHEN** a equipe escolhe outra atividade da programação
- **THEN** a aplicação declara a nova e passa a apresentá-la como corrente

#### Scenario: Programação com duas atividades não é decidida pela aplicação

- **WHEN** a programação traz duas atividades e a equipe não escolheu nenhuma
- **THEN** a aplicação não declara escolha alguma e a tela segue sem corrente

#### Scenario: Sem rede, a escolha não é declarada nem enfileirada

- **WHEN** a equipe tenta escolher com o aparelho sem rede
- **THEN** a aplicação diz que a escolha está indisponível sem rede, o conteúdo já carregado
  segue legível e nada é enfileirado
