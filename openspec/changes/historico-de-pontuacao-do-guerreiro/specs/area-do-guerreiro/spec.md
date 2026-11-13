## ADDED Requirements

### Requirement: A App 05 mostra o histórico de pontuação do próprio Guerreiro(a)

A carteira da App 05 SHALL abrir o **histórico de pontuação** do Guerreiro(a) em sessão, do
mais recente ao mais antigo: data, origem em linguagem simples, valor com sinal, conta, trilha
ou poder e, na ocorrência de conduta, o **motivo**. Ponto regular e ponto extra SHALL aparecer
cada um com o seu glifo, ficha e rótulo, e a lista SHALL carregar mais lançamentos sob pedido.
A leitura SHALL ser a do próprio, sem identificador de persona. (`RF-05-104`, `RN-01-68`,
documento 15 §9, invariante 24)

#### Scenario: O Guerreiro(a) vê como chegou ao saldo

- **WHEN** o Guerreiro(a) abre o histórico na carteira
- **THEN** a App 05 mostra os lançamentos do mais recente ao mais antigo, cada um com data,
  origem e valor

#### Scenario: Conduta aparece com motivo

- **WHEN** o histórico traz uma ocorrência de conduta
- **THEN** a linha mostra a data, o débito e o motivo escrito pelo Mestre

#### Scenario: Linha de saldo anterior

- **WHEN** o histórico chega ao começo
- **THEN** a última linha é a de saldo anterior, com o total da data da implantação

#### Scenario: Sem pontuação

- **WHEN** um Guerreiro(a) que nunca pontuou abre o histórico
- **THEN** a App 05 mostra o aviso de que ainda não há lançamento, sem erro
