## MODIFIED Requirements

### Requirement: Mestre, Admin ou responsável abre a sessão por confirmação humana

O núcleo SHALL permitir que um Mestre, um Admin ou o **responsável** em sessão abra a sessão de
um Guerreiro(a) por confirmação, informando o **nick**. O núcleo SHALL resolver o nick
internamente, restrito a `Papel.guerreiro` e por correspondência exata insensível a caixa, e
NEVER SHALL exigir ou aceitar um identificador de persona no pedido — fazê-lo abriria caminho
para uma busca por nick fora desta rota, que a capacidade `persona-e-credencial` veda para
qualquer persona, adulto autenticado incluído. Nick que não resolve a um Guerreiro(a) SHALL ser
recusado com **401**, numa resposta **indistinguível** entre nick inexistente e nick que
pertence a outro papel. A sessão aberta SHALL registrar que a autenticação foi por confirmação
humana e SHALL guardar **quem confirmou**. O caminho SHALL valer igualmente para o Guerreiro(a)
sem _template_ gravado, para a falha de reconhecimento e para quem recusou a biometria, e a
sessão resultante SHALL ter os mesmos direitos da aberta por biometria. Persona de qualquer
outro papel SHALL receber 403. (`RF-01-06`, `RN-01-16`, `RN-01-22`, PRD-01 §§5.1, 9, PRD-04 §9)

O Mestre e o Admin confirmam **qualquer** Guerreiro(a) — a autoridade deles é a do encontro. O
responsável confirma **apenas** os Guerreiros e Guerreiras sob a responsabilidade dele, por
vínculo de responsável **vigente**. Nick de Guerreiro(a) que não está sob a responsabilidade de
quem confirma SHALL ser recusado com **401**, numa resposta **indistinguível** — no corpo e no
tempo — da recusa por nick inexistente: distinguir as duas daria ao responsável um oráculo para
descobrir quais nicks existem, que é exatamente o que o `RN-01-22` veda. (`RF-01-74`,
`RN-01-58`, `RN-01-22`)

No **encontro** — pedido feito com a **chave do App 01** por Mestre ou Admin —, a confirmação
SHALL exigir o **PIN de confirmação** da persona em sessão, que é quem abriu a sessão de
trabalho do aparelho: só ela confirma ali. O núcleo SHALL conferir o PIN **antes** de resolver o
nick, para que a recusa de PIN nunca revele se o nick existe. Sem PIN cadastrado, com PIN
bloqueado ou com PIN errado, a confirmação SHALL ser recusada com o erro que diz qual dos três,
e nenhuma sessão é aberta. O erro de PIN conta para o bloqueio da capacidade
`pin-de-confirmacao`; a recusa do nick não conta. Fora do App 01, o pedido segue sem PIN, como
já era. (`RF-01-06`, `RN-01-59`, `RN-04-37`, documento 03 §1.1)

#### Scenario: Mestre confirma quem não tem _template_

- **WHEN** um Mestre em sessão confirma, pelo nick e pelo PIN certo, um Guerreiro(a) sem
  _template_ gravado
- **THEN** o núcleo abre a sessão, registra a autenticação por confirmação humana e guarda o
  Mestre como quem confirmou

#### Scenario: O responsável confirma quem está sob a responsabilidade dele

- **WHEN** um responsável em sessão confirma, pelo nick, um Guerreiro(a) com vínculo de
  responsável vigente com ele
- **THEN** o núcleo abre a sessão e guarda o responsável como quem confirmou

#### Scenario: O responsável não confirma criança alheia

- **WHEN** um responsável pede a confirmação do nick de um Guerreiro(a) que não está sob a
  responsabilidade dele
- **THEN** o núcleo responde 401, com o mesmo código e a mesma mensagem do nick inexistente, e
  nenhuma sessão é aberta

#### Scenario: A recusa do nick alheio não se distingue pelo tempo

- **WHEN** se comparam os tempos de resposta da recusa de um nick inexistente e da recusa de um
  nick que existe mas não é do responsável
- **THEN** o trabalho feito é o mesmo nos dois, e o tempo não separa um caso do outro

#### Scenario: Vínculo de responsável encerrado não confirma mais

- **WHEN** um responsável cujo vínculo com o Guerreiro(a) já terminou pede a confirmação dele
- **THEN** o núcleo responde 401, indistinguível da recusa por nick inexistente

#### Scenario: A recusa da biometria não fecha porta

- **WHEN** um Guerreiro(a) cujo responsável recusou a biometria tem a sessão aberta por
  confirmação de um Admin, pelo nick
- **THEN** a sessão vale como qualquer outra, sem restrição de rota decorrente da recusa

#### Scenario: Apoiador não confirma criança

- **WHEN** uma persona de papel diferente de Mestre, Admin ou responsável pede a confirmação
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

#### Scenario: No App 01, sem PIN não há confirmação

- **WHEN** o Mestre da sessão de trabalho pede a confirmação pelo App 01 sem enviar o PIN
- **THEN** o núcleo recusa a validação do corpo, e nenhuma sessão é aberta

#### Scenario: PIN errado é recusado antes do nick

- **WHEN** o Mestre envia pelo App 01 o PIN errado, com um nick que existe ou que não existe
- **THEN** o núcleo responde o erro de PIN recusado nos dois casos, e nenhuma sessão é aberta

#### Scenario: Adulto sem PIN cadastrado não confirma

- **WHEN** um Admin que nunca cadastrou PIN pede a confirmação pelo App 01
- **THEN** o núcleo responde o erro de PIN não cadastrado, e nenhuma sessão é aberta

#### Scenario: A confirmação pela App 05 segue sem PIN

- **WHEN** um responsável confirma pela App 05, pelo nick, um Guerreiro(a) sob a
  responsabilidade dele
- **THEN** o núcleo abre a sessão sem pedir PIN
