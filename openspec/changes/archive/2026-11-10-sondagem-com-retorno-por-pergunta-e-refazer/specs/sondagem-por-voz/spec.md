# Spec Delta

## MODIFIED Requirements

### Requirement: Ao fim da janela, a resposta é enviada sozinha

Ao fim dos 5 segundos, o microfone SHALL fechar e a resposta SHALL ser marcada na pergunta, que
SHALL passar pelo **retorno de 2 segundos** de acerto ou de erro e avançar para a seguinte; na
**última** pergunta, a sondagem SHALL ser **submetida** sem toque e apresentar a tela final. A
resposta falada SHALL substituir a escolha por toque naquela pergunta. (`RF-05-97`, `RF-05-99`,
`RF-05-100`)

#### Scenario: A resposta falada avança a sondagem

- **WHEN** a janela de uma pergunta que não é a última termina
- **THEN** o microfone fecha, a resposta fica marcada, o retorno de acerto ou de erro aparece por
  2 segundos e a pergunta seguinte é apresentada e falada

#### Scenario: A última resposta submete a sondagem

- **WHEN** a janela da última pergunta termina
- **THEN** depois do retorno a sondagem é submetida, e a tela final mostra o total de acertos e
  de erros, como na resposta por toque
