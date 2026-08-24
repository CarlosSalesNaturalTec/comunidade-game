## MODIFIED Requirements

### Requirement: Mestre ou Admin abre a sessão por confirmação humana

O núcleo SHALL permitir que um Mestre ou um Admin em sessão abra a sessão de um Guerreiro(a) por
confirmação presencial, informando o **nick**. O núcleo SHALL resolver o nick internamente,
restrito a `Papel.guerreiro` e por correspondência exata insensível a caixa, e NEVER SHALL
exigir ou aceitar um identificador de persona no pedido — fazê-lo abriria caminho para uma busca
por nick fora desta rota, que a capacidade `persona-e-credencial` veda para qualquer persona,
adulto autenticado incluído. Nick que não resolve a um Guerreiro(a) SHALL ser recusado com
**401**, numa resposta **indistinguível** entre nick inexistente e nick que pertence a outro
papel. A sessão aberta SHALL registrar que a autenticação foi por confirmação humana e SHALL
guardar **quem confirmou**. O caminho SHALL valer igualmente para o Guerreiro(a) sem _template_
gravado, para a falha de reconhecimento e para quem recusou a biometria, e a sessão resultante
SHALL ter os mesmos direitos da aberta por biometria. Persona de qualquer outro papel SHALL
receber 403. (`RF-01-06`, `RN-01-16`, `RN-01-22`, PRD-01 §§5.1, 9, PRD-04 §9)

#### Scenario: Mestre confirma quem não tem _template_

- **WHEN** um Mestre em sessão confirma, pelo nick, um Guerreiro(a) sem _template_ gravado
- **THEN** o núcleo abre a sessão, registra a autenticação por confirmação humana e guarda o
  Mestre como quem confirmou

#### Scenario: A recusa da biometria não fecha porta

- **WHEN** um Guerreiro(a) cujo responsável recusou a biometria tem a sessão aberta por
  confirmação de um Admin, pelo nick
- **THEN** a sessão vale como qualquer outra, sem restrição de rota decorrente da recusa

#### Scenario: Apoiador não confirma criança

- **WHEN** uma persona de papel diferente de Mestre ou Admin pede a confirmação
- **THEN** o núcleo responde 403 e nenhuma sessão é aberta

#### Scenario: Nick inexistente é recusado sem revelar o motivo

- **WHEN** um Mestre pede a confirmação de um nick que não corresponde a nenhuma persona
- **THEN** o núcleo responde 401, sem indicar se o nick não existe

#### Scenario: Nick de quem não é Guerreiro(a) é recusado da mesma forma

- **WHEN** um Mestre pede a confirmação de um nick que pertence a um Mestre ou Apoiador
- **THEN** o núcleo responde 401, com o mesmo código e a mesma mensagem do nick inexistente

#### Scenario: A rota não aceita identificador de persona

- **WHEN** chega um pedido de confirmação com um identificador de persona no lugar do nick
- **THEN** o núcleo recusa a validação do corpo, e nenhuma sessão é aberta
