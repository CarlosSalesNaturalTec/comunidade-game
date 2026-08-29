## MODIFIED Requirements

### Requirement: O histórico da entrega é lido sem moedas e sem reais

O núcleo SHALL expor o histórico das entregas filtrado por persona: o Guerreiro(a) lê as
**próprias**, e o Mestre e o Admin leem as da **comunidade** a que estão vinculados. A saída
SHALL trazer a recompensa, o marco, a trilha, o ponto de apoio, a data, o **tipo de recurso**
entregue, a **quantidade** e o **identificador do lançamento** da baixa — sem o que a gestão não
distingue o exemplar da linha Alpha da camisa nem mostra a baixa definitiva —, e NEVER SHALL
trazer o valor em moedas nem o valor em reais do recurso entregue: o custo segue no lançamento,
invisível para a criança (`RF-07-13`, `RN-07-05`, `RF-02-50`, `RF-02-51`, `RN-02-17`,
invariante 16, 02 §8).

#### Scenario: Guerreiro(a) lê as próprias entregas

- **WHEN** um Guerreiro(a) consulta o histórico de entregas
- **THEN** recebe apenas as suas, com recompensa, marco, trilha, ponto de apoio e data

#### Scenario: O histórico não mostra o custo

- **WHEN** qualquer persona consulta o histórico de entregas
- **THEN** nenhum campo traz valor em moedas nem em reais

#### Scenario: A gestão distingue o recurso entregue e alcança a baixa

- **WHEN** um Admin consulta o histórico de entregas
- **THEN** cada entrega traz o tipo de recurso, a quantidade e o identificador do lançamento que
  deu a baixa definitiva
