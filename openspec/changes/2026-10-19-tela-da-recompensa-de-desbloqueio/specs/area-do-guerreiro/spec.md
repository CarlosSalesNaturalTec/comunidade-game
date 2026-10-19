# Spec Delta

## ADDED Requirements

### Requirement: A recompensa conquistada entra antes da próxima missão

Alcançado o marco que concede recompensa, a aplicação SHALL apresentar a **tela da recompensa**
**antes** da próxima missão do percurso, e NEVER SHALL levar o Guerreiro(a) direto à missão
seguinte deixando a conquista por descobrir na lista de conquistas. A tela SHALL trazer, de
cima para baixo: o **trio de estrelas**, o **nome do que foi conquistado** com a quantidade, o
aviso em linguagem simples de que **a entrega é confirmada pelo Mestre** no encontro, e o
controle de **avançar**, que leva à próxima missão. (`RF-05-45`, PRD-05 §5.6)

#### Scenario: A sondagem respondida apresenta a recompensa do marco

- **WHEN** o Guerreiro(a) responde a missão de sondagem que é marco com recompensa declarada
- **THEN** a tela da recompensa é apresentada antes da próxima missão, com o trio de estrelas, o
  nome do recurso, a quantidade e o aviso de que o Mestre confirma a entrega

#### Scenario: O quiz que desbloqueia apresenta a recompensa do marco

- **WHEN** o Guerreiro(a) passa no quiz do desbloqueio de uma missão que é marco com recompensa
- **THEN** a tela da recompensa é apresentada antes da missão seguinte

#### Scenario: Avançar leva à próxima missão

- **WHEN** o Guerreiro(a) aciona avançar na tela da recompensa
- **THEN** a próxima missão do percurso é apresentada

#### Scenario: Marco sem recompensa não interrompe o percurso

- **WHEN** o Guerreiro(a) desbloqueia uma missão que não tem recompensa declarada
- **THEN** nenhuma tela de recompensa é apresentada, e a próxima missão abre como já abria

#### Scenario: A tela não vende nem mostra custo

- **WHEN** a tela da recompensa é apresentada
- **THEN** nenhum caminho de adquirir a recompensa é oferecido, nenhum ponto é debitado e nenhum
  valor em moedas ou em reais aparece

### Requirement: A tela da recompensa aparece uma vez, e no prático só depois do Mestre

A tela da recompensa SHALL ser apresentada **uma vez** por recompensa conquistada: avançar
SHALL dar **ciência** dela, e a tela NEVER SHALL voltar a interromper o percurso depois disso,
ainda que a entrega siga aguardando o Mestre. Sendo o desbloqueio **desafio prático**, a tela
NEVER SHALL ser apresentada antes de o **Mestre autor** julgar que o Guerreiro(a) passou;
enquanto ele não julga, o percurso SHALL seguir dizendo que a missão aguarda o Mestre.
(`RF-05-14`, `RF-05-45`, `RN-05-50`)

#### Scenario: Voltar à trilha não reapresenta a recompensa

- **WHEN** o Guerreiro(a) avança na tela da recompensa e volta à trilha depois
- **THEN** a tela não é apresentada de novo, e o percurso abre na missão

#### Scenario: A recompensa sem ciência espera o Guerreiro(a) voltar

- **WHEN** o Guerreiro(a) conquistou recompensa e saiu da aplicação antes de avançar
- **THEN** ao voltar à trilha a tela da recompensa é apresentada, porque a ciência não foi dada

#### Scenario: O prático não julgado não apresenta recompensa

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático de missão que é marco com
  recompensa e o Mestre autor ainda não julgou
- **THEN** nenhuma tela de recompensa é apresentada, e o percurso diz que a missão aguarda o
  Mestre

#### Scenario: Julgado o prático, a recompensa aparece na volta

- **WHEN** o Mestre autor julga que o Guerreiro(a) passou e ele volta à trilha depois
- **THEN** a tela da recompensa é apresentada antes da próxima missão

#### Scenario: Duas recompensas conquistadas saem uma por tela

- **WHEN** o Guerreiro(a) tem duas recompensas conquistadas sem ciência
- **THEN** cada uma é apresentada na sua própria tela, em sequência, e o último avançar leva à
  missão

## MODIFIED Requirements

### Requirement: A App 05 avisa a recompensa conquistada e nunca a vende

A aplicação SHALL exibir as recompensas de marco que o Guerreiro(a) **conquistou**, dizendo em
linguagem simples que **a entrega é confirmada pelo Mestre** e mostrando, de cada uma, o **nome
do tipo de recurso** com a quantidade — sem o nome, a criança não distingue o livro da camisa
nem do kit — e se já foi entregue ou se aguarda. O aviso SHALL acontecer **nos dois momentos**:
no instante em que o marco é alcançado, no percurso da trilha, e na lista de conquistas, que
permanece. A aplicação NEVER SHALL oferecer nenhuma forma de **comprar** recompensa
de marco, com ponto de qualquer natureza. (`RF-05-45`, `RF-05-46`, `RN-05-07`, `RN-05-41`,
PRD-05 §5.6)

#### Scenario: Marco alcançado avisa a conquista

- **WHEN** o Guerreiro(a) alcança um marco que concede recompensa
- **THEN** a tela de conquistas mostra a recompensa e diz que o Mestre confirma a entrega

#### Scenario: A lista nomeia o que foi conquistado

- **WHEN** o Guerreiro(a) abre a lista de conquistas
- **THEN** cada recompensa traz o nome do tipo de recurso e a quantidade, nunca a quantidade
  sozinha

#### Scenario: A entrega feita aparece como feita

- **WHEN** o Mestre já confirmou a entrega
- **THEN** a mesma recompensa aparece como entregue, com a data

#### Scenario: Nenhuma tela vende recompensa de marco

- **WHEN** o Guerreiro(a) percorre carteira, catálogo e conquistas
- **THEN** em nenhuma delas há caminho de adquirir recompensa de marco com pontos
