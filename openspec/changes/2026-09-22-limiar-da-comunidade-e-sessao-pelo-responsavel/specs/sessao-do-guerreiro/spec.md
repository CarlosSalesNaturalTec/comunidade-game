## RENAMED Requirements

- FROM: `### Requirement: Mestre ou Admin abre a sessão por confirmação humana`
- TO: `### Requirement: Mestre, Admin ou responsável abre a sessão por confirmação humana`

## MODIFIED Requirements

### Requirement: O Guerreiro(a) abre sessão por nick e imagem

O núcleo SHALL abrir sessão do Guerreiro(a) mediante **nick** e **descritor** gerado no
aparelho. O nick SHALL restringir a busca a um único Guerreiro(a) e o descritor SHALL confirmar
a identidade, por comparação com o _template_ guardado. A sessão aberta SHALL registrar que a
autenticação foi por biometria. A rota SHALL dispensar credencial de persona e SHALL continuar
exigindo chave de aplicação válida. (`RF-01-04`, `RF-01-05`, PRD-01 §§5.1, 9)

A **aula** é **opcional** no pedido, e é a presença dela que escolhe de onde vem o limiar:

- **Com aula** — a entrada acontece no encontro. A aula determina o ponto de apoio, e o ponto de
  apoio determina o limiar. O núcleo SHALL exigir que a aula esteja **vigente** e que o vínculo
  do Guerreiro(a) seja da **comunidade dela** — o mesmo laço que o registro de presença já
  aplica —, para que a escolha da aula NEVER SHALL alcançar o limiar de outra comunidade.
  (`RF-01-73`, `RF-01-04`)
- **Sem aula** — a entrada acontece fora do encontro, em aparelho que não é de ponto de apoio
  algum. O limiar SHALL vir da **comunidade do vínculo vigente** do Guerreiro(a), pelo critério
  que a capacidade `template-biometrico` define. Não há como o pedido alcançar comunidade
  alheia: a busca parte do vínculo do próprio Guerreiro(a). (`RN-01-57`)

#### Scenario: Nick e descritor conferem

- **WHEN** chega um pedido de sessão com nick existente, aula vigente da comunidade dele e
  descritor que confere
- **THEN** o núcleo abre a sessão do Guerreiro(a) daquele nick, registrando a autenticação por
  biometria

#### Scenario: O limiar aplicado é o do ponto de apoio da aula

- **WHEN** dois pontos de apoio têm limiares medidos diferentes
- **THEN** a comparação de cada entrada usa o limiar do ponto de apoio da aula informada, e não
  o do outro

#### Scenario: Pedido sem descritor é recusado

- **WHEN** chega um pedido de sessão de Guerreiro(a) sem descritor
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhuma sessão é aberta

#### Scenario: Pedido sem a aula segue pelo limiar da comunidade

- **WHEN** chega um pedido de sessão de Guerreiro(a) sem a aula
- **THEN** o núcleo compara com o limiar da comunidade do vínculo vigente dele, em vez de
  recusar o pedido por campo em falta

#### Scenario: Pedido sem a aula é recusado

- **WHEN** chega um pedido sem aula de um Guerreiro(a) cujo vínculo já terminou, ou cuja
  comunidade não tem ponto de apoio algum com limiar medido
- **THEN** o núcleo recusa de forma indistinguível das demais causas, e nenhuma sessão é aberta

#### Scenario: Não há entrada da criança por segredo memorizado

- **WHEN** se procura no núcleo um caminho de sessão de Guerreiro(a) por senha, PIN ou código
- **THEN** nenhum existe: a abertura é por descritor ou por confirmação humana, e nada mais

### Requirement: A recusa não revela se o nick existe

O núcleo SHALL responder **401** ao pedido de sessão que não confere, e a resposta SHALL ser
indistinguível entre nick inexistente, Guerreiro(a) sem _template_ gravado, descritor que não
confere, **ponto de apoio sem limiar medido**, **aula que não vale para aquele Guerreiro(a)**,
**Guerreiro(a) sem vínculo vigente** e **comunidade sem nenhum ponto de apoio com limiar
medido**. A resposta SHALL orientar a chamar o Mestre. O núcleo SHALL NOT expor listagem, busca
parcial ou sugestão de nick em qualquer rota desta capacidade. (`RF-01-04`, `RN-01-22`,
`RN-01-56`, `RN-01-57`, PRD-01 §§9, 12)

O trabalho feito SHALL ser o mesmo nas sete causas, no caminho com aula e no caminho sem ela:
a indistinguibilidade alcança o **tempo**, não só o corpo da resposta. (`RN-01-22`, `RN-01-57`)

#### Scenario: Nick que não existe

- **WHEN** chega um pedido de sessão com nick inexistente
- **THEN** o núcleo responde 401 com o mesmo código e a mesma mensagem que devolveria a um
  descritor que não confere

#### Scenario: Descritor que não confere

- **WHEN** chega um pedido de sessão com nick existente e descritor que não confere
- **THEN** o núcleo responde 401 com a orientação de chamar o Mestre, sem dizer que o nick existe

#### Scenario: Guerreiro(a) ainda sem _template_

- **WHEN** chega um pedido de sessão de um Guerreiro(a) que ainda não tem _template_ gravado
- **THEN** o núcleo responde 401 indistinguível dos demais casos, e a entrada dele acontece pela
  confirmação humana

#### Scenario: Ponto de apoio sem limiar medido

- **WHEN** chega um pedido de sessão numa aula cujo ponto de apoio ainda não teve limiar medido
- **THEN** o núcleo responde 401 indistinguível dos demais casos, sem dizer que o limiar é que
  falta

#### Scenario: Aula que não é da comunidade do Guerreiro(a)

- **WHEN** chega um pedido de sessão com aula de outra comunidade, ou com aula não vigente
- **THEN** o núcleo responde 401 indistinguível dos demais casos, e nenhum limiar de outra
  comunidade é aplicado

#### Scenario: Comunidade sem nenhum limiar medido

- **WHEN** chega um pedido sem aula de um Guerreiro(a) cuja comunidade não tem ponto de apoio
  algum com limiar medido
- **THEN** o núcleo responde 401 indistinguível dos demais casos, sem dizer que a medição é que
  falta

#### Scenario: O tempo da resposta não separa o caminho com aula do caminho sem ela

- **WHEN** se comparam os tempos de resposta das recusas nos dois caminhos
- **THEN** o trabalho feito é equivalente, e o tempo não revela qual deles foi percorrido

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

#### Scenario: Mestre confirma quem não tem _template_

- **WHEN** um Mestre em sessão confirma, pelo nick, um Guerreiro(a) sem _template_ gravado
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
