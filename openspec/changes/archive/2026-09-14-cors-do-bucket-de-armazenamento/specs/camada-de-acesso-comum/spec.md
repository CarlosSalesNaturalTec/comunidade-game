## MODIFIED Requirements

### Requirement: A camada apresenta o erro do núcleo no corpo único do PRD-01

A camada de acesso SHALL entregar a quem a consome o erro do núcleo com o **código**, a
**mensagem** e o **campo** quando houver, preservando o corpo único da API, para que a tela
possa apontar o campo em falta sem interpretar texto. Isso vale em **toda** chamada da camada,
inclusive no **envio de bytes** da sessão retomável: a recusa que traga corpo de erro SHALL
chegar a quem a consome como as demais, e a camada NEVER SHALL substituí-la por texto próprio.
Quando não houver corpo de erro — a falha que acontece antes de a resposta existir —, a camada
SHALL dizer que a falha foi no envio, sem se apresentar como recusa do núcleo. (`RF-01-02`,
`RF-09-19`, convenções da API)

#### Scenario: Erro de validação chega com o campo

- **WHEN** o núcleo recusa uma escrita por campo obrigatório em falta
- **THEN** a camada entrega o código, a mensagem e o nome do campo, e a tela o aponta

#### Scenario: O corpo do erro não é reinterpretado

- **WHEN** o núcleo devolve um erro de código desconhecido pela aplicação
- **THEN** a camada o entrega como veio, sem substituir a mensagem por texto próprio

#### Scenario: A recusa no envio de bytes chega com o motivo

- **WHEN** o envio de uma parte é recusado com o corpo de erro único da API
- **THEN** a camada entrega o código e a mensagem daquela recusa, e a tela mostra o motivo em
  vez de uma frase própria

#### Scenario: Falha sem resposta se apresenta como falha de envio

- **WHEN** o envio de uma parte falha antes de qualquer resposta chegar
- **THEN** a camada diz que o envio falhou, e NEVER SHALL atribuir ao núcleo uma recusa que ele
  não deu
