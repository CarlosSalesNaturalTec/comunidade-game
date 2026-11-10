# Spec Delta

## ADDED Requirements

### Requirement: A sondagem no aparelho do encontro tem o retorno, a tela final e o refazer

Na App 01, a sondagem SHALL ter o mesmo retorno por pergunta, a mesma tela final com Refazer e
Concluir e o mesmo caminho de refazer pelo rodapé da trilha que a App 05 apresenta, sem
divergir dela. (`RF-04-78`, `RF-04-73`, `RF-05-99`, `RF-05-100`, `RF-05-101`)

#### Scenario: A sondagem no encontro dá retorno por pergunta

- **WHEN** o Guerreiro(a) responde uma pergunta da sondagem no aparelho do encontro
- **THEN** o símbolo de acerto ou de erro aparece por 2 segundos e a pergunta seguinte é
  apresentada

#### Scenario: A sondagem no encontro termina com o total

- **WHEN** o Guerreiro(a) responde a última pergunta da sondagem no aparelho do encontro
- **THEN** a tela mostra o total de acertos e de erros, com Refazer e Concluir

#### Scenario: No encontro também se refaz pelo rodapé

- **WHEN** o Guerreiro(a) abre no aparelho do encontro uma trilha cuja sondagem já respondeu
- **THEN** o rodapé oferece Refazer a sondagem
