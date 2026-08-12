## Purpose

A entrada do Guerreiro(a) é por **nick e imagem**, em aparelho que não é dele. Esta capacidade
cobre a abertura da sessão pela conferência do descritor, a recusa que não deixa um adulto
descobrir o nick de uma criança, a confirmação humana como alternativa equivalente para quem não
tem _template_ ou recusou a biometria, e a expiração curta que devolve o aparelho ao ponto de
apoio.

## ADDED Requirements

### Requirement: O Guerreiro(a) abre sessão por nick e imagem

O núcleo SHALL abrir sessão do Guerreiro(a) mediante **nick** e **descritor** gerado no aparelho.
O nick SHALL restringir a busca a um único Guerreiro(a) e o descritor SHALL confirmar a
identidade, por comparação com o _template_ guardado. A sessão aberta SHALL registrar que a
autenticação foi por biometria. A rota SHALL dispensar credencial de persona e SHALL continuar
exigindo chave de aplicação válida. (`RF-01-04`, `RF-01-05`, PRD-01 §§5.1, 9)

#### Scenario: Nick e descritor conferem

- **WHEN** chega um pedido de sessão com nick existente e descritor que confere com o _template_
- **THEN** o núcleo abre a sessão do Guerreiro(a) daquele nick, registrando a autenticação por
  biometria e o momento de expiração

#### Scenario: Pedido sem descritor é recusado

- **WHEN** chega um pedido de sessão de Guerreiro(a) sem descritor
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhuma sessão é aberta

#### Scenario: Não há entrada da criança por segredo memorizado

- **WHEN** se procura no núcleo um caminho de sessão de Guerreiro(a) por senha, PIN ou código
- **THEN** nenhum existe: a abertura é por descritor ou por confirmação humana, e nada mais

### Requirement: A recusa não revela se o nick existe

O núcleo SHALL responder **401** ao pedido de sessão cujo descritor não confere, e a resposta
SHALL ser indistinguível entre nick inexistente, Guerreiro(a) sem _template_ gravado e descritor
que não confere. A resposta SHALL orientar a chamar o Mestre. O núcleo SHALL NOT expor listagem,
busca parcial ou sugestão de nick em qualquer rota desta capacidade. (`RF-01-04`, `RN-01-22`,
PRD-01 §§9, 12)

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

### Requirement: Mestre ou Admin abre a sessão por confirmação humana

O núcleo SHALL permitir que um Mestre ou um Admin em sessão abra a sessão de um Guerreiro(a) por
confirmação presencial. A sessão aberta SHALL registrar que a autenticação foi por confirmação
humana e SHALL guardar **quem confirmou**. O caminho SHALL valer igualmente para o Guerreiro(a)
sem _template_ gravado, para a falha de reconhecimento e para quem recusou a biometria, e a
sessão resultante SHALL ter os mesmos direitos da aberta por biometria. Persona de qualquer outro
papel SHALL receber 403. (`RF-01-06`, `RN-01-16`, PRD-01 §§5.1, 9)

#### Scenario: Mestre confirma quem não tem _template_

- **WHEN** um Mestre em sessão confirma um Guerreiro(a) sem _template_ gravado
- **THEN** o núcleo abre a sessão, registra a autenticação por confirmação humana e guarda o
  Mestre como quem confirmou

#### Scenario: A recusa da biometria não fecha porta

- **WHEN** um Guerreiro(a) cujo responsável recusou a biometria tem a sessão aberta por
  confirmação de um Admin
- **THEN** a sessão vale como qualquer outra, sem restrição de rota decorrente da recusa

#### Scenario: Apoiador não confirma criança

- **WHEN** uma persona de papel diferente de Mestre ou Admin pede a confirmação
- **THEN** o núcleo responde 403 e nenhuma sessão é aberta

### Requirement: A sessão do Guerreiro(a) é curta e expira sozinha

O núcleo SHALL dar à sessão do Guerreiro(a) duração **declarada na implantação**, sem valor
padrão no código, e SHALL recusar com 401 qualquer chamada feita com sessão expirada. A expiração
SHALL acontecer sem intervenção humana. Uma sessão SHALL NOT dar acesso aos dados de outro
Guerreiro(a), em nenhuma circunstância. (`RF-01-04`, PRD-01 §§10, 12)

#### Scenario: Sessão expirada não responde

- **WHEN** uma chamada chega com token de sessão de Guerreiro(a) já expirado
- **THEN** o núcleo responde 401 e nada é lido nem escrito

#### Scenario: Uma sessão não alcança outro Guerreiro(a)

- **WHEN** dois Guerreiros abrem sessão no mesmo aparelho, um após o outro
- **THEN** cada token alcança apenas os dados do seu Guerreiro(a), e a expiração de um não
  interfere na do outro

#### Scenario: O ambiente que não declara a duração não sobe

- **WHEN** o núcleo é iniciado sem a duração da sessão do Guerreiro(a) declarada
- **THEN** o serviço falha na subida, sem assumir valor padrão
