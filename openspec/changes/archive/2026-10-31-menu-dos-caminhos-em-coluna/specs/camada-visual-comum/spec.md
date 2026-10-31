# Spec Delta

## ADDED Requirements

### Requirement: A camada comum entrega a lista de caminhos em cartão, um por linha

A camada comum SHALL entregar um componente de **lista de caminhos** que apresenta cada caminho
como **cartão** com glifo e **rótulo em frase**, sempre em **coluna**: um cartão por linha, com
o glifo **ao lado** do rótulo, em qualquer largura de tela. (`RF-05-08`, PRD-05 §10, documento
15 §§5, 6.5, 11.1, decisão do fundador de 2026-10-31)

#### Scenario: A lista mantém o glifo ao lado do rótulo

- **WHEN** a lista de caminhos é apresentada
- **THEN** cada cartão traz o glifo ao lado do rótulo, e não acima dele
- **AND** os cartões aparecem um por linha, em qualquer largura de tela

#### Scenario: O cartão alcança o alvo de toque

- **WHEN** um cartão de caminho é apresentado
- **THEN** ele cumpre o alvo de toque e a separação do vizinho que a camada comum exige

#### Scenario: O glifo não substitui o rótulo

- **WHEN** um cartão de caminho é apresentado
- **THEN** o rótulo em frase continua sendo o nome acessível do cartão, e o glifo o acompanha
  sem tomar o lugar dele

## REMOVED Requirements

### Requirement: A camada comum entrega a lista de caminhos em cartão

**Reason**: Decisão do fundador de 2026-10-31. A disposição em **grade** existia para o caso em
que caminhos e conteúdo convivem na mesma tela — a Área do Guerreiro(a) antes desta fatia — e
fica sem consumidor quando a área passa a separar menu e conteúdo. O documento 15 §6.5 já manda
coluna onde os caminhos são a tela, de modo que a lista passa a ter uma disposição só.

**Migration**: Substituído por "A camada comum entrega a lista de caminhos em cartão, um por
linha", que mantém o cartão, o glifo, o rótulo em frase e o alvo de toque. Quem passava a
disposição deixa de passá-la; a App 01 já usava coluna e não muda de comportamento.

### Requirement: A lista de caminhos marca o caminho corrente sem depender de cor

**Reason**: O caminho corrente só tinha sentido na grade, única disposição em que os caminhos
continuavam na tela com um bloco aberto. Depois da decisão do fundador de 2026-10-31 nenhuma
aplicação declara caminho corrente: na Área do Guerreiro(a) o menu e o conteúdo passam a telas
separadas, e a tela inicial da App 01 nunca teve caminho aberto.

**Migration**: A regra de marcar o item corrente por sinal além da cor (documento 15 §5)
permanece vigente e continua atendida pelo componente de **navegação de áreas** da camada comum,
que as Apps 03 e 09 usam. Quem precisar de navegação persistente com item corrente usa esse
componente, não a lista de caminhos.
