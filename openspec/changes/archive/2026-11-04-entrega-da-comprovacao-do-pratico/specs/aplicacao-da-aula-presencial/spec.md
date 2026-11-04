# Spec Delta

## ADDED Requirements

### Requirement: A App 01 entrega a comprovação do prático na tela do desbloqueio

A App 01 SHALL apresentar o **critério de aceite**, a **forma aceita** e o **aviso** da mídia
guardada, e SHALL **receber a comprovação**, na mesma tela do desbloqueio em que já submete o
quiz. O comportamento SHALL ser o **mesmo** da App 05 e NEVER SHALL divergir dela em exigência,
aviso ou alternativa. (`RF-04-76`, `RF-05-91`, `RF-05-92`, `RN-05-51`)

#### Scenario: O Guerreiro(a) entrega a comprovação no encontro, pelo aparelho da aula

- **WHEN** o Guerreiro(a) em sessão na App 01 abre uma missão cujo desbloqueio é prático
- **THEN** a tela apresenta o critério, a forma aceita e o aviso, e recebe a comprovação como a
  App 05 a recebe

#### Scenario: A alternativa de entrega no encontro também vale na App 01

- **WHEN** o Guerreiro(a) na App 01 escolhe entregar ao Mestre no encontro
- **THEN** a declaração segue sem mídia, como na App 05, sem ser tratada como falha

#### Scenario: A exigência da comprovação não divergiu entre as duas aplicações

- **WHEN** o mesmo prático é aberto na App 01 e na App 05
- **THEN** as duas exigem a comprovação, apresentam o mesmo aviso e oferecem a mesma
  alternativa
