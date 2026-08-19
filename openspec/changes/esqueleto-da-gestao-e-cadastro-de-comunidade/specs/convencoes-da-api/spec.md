## ADDED Requirements

### Requirement: A chamada é aceita de qualquer origem, sem cookie credenciado

O núcleo SHALL aceitar chamada de **qualquer origem** e SHALL responder ao _preflight_ dos
cabeçalhos que a chave de aplicação e a sessão usam. O núcleo NEVER SHALL exigir cookie
credenciado: as duas credenciais viajam em cabeçalho, e a proteção está nelas, na cota por
chave e no freio por origem — não no navegador. (documento 03 §1, princípio 2)

#### Scenario: Frontend em endereço próprio alcança a API

- **WHEN** uma aplicação do projeto, servida em endereço diferente do núcleo, chama uma rota
  de dados pelo navegador
- **THEN** o navegador conclui a chamada, com a chave de aplicação e a credencial de persona
  apresentadas em cabeçalho

#### Scenario: Preflight responde antes da chamada

- **WHEN** o navegador antecede a chamada com `OPTIONS`, por ela levar os cabeçalhos da chave
  e da sessão
- **THEN** o núcleo responde permitindo esses cabeçalhos, e a chamada segue

#### Scenario: A origem aberta não dispensa credencial

- **WHEN** uma chamada chega de origem qualquer sem chave de aplicação válida
- **THEN** o núcleo a recusa como recusaria de qualquer outra origem — a abertura é de
  origem, nunca de credencial
