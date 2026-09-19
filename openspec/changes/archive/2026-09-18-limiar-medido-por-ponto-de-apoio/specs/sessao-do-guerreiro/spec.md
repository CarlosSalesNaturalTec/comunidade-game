## MODIFIED Requirements

### Requirement: O Guerreiro(a) abre sessão por nick e imagem

O núcleo SHALL abrir sessão do Guerreiro(a) mediante **nick**, **descritor** gerado no aparelho
e a **aula** em que a entrada acontece. O nick SHALL restringir a busca a um único Guerreiro(a) e
o descritor SHALL confirmar a identidade, por comparação com o _template_ guardado. A sessão
aberta SHALL registrar que a autenticação foi por biometria. A rota SHALL dispensar credencial de
persona e SHALL continuar exigindo chave de aplicação válida. (`RF-01-04`, `RF-01-05`, PRD-01
§§5.1, 9)

A **aula** determina o ponto de apoio, e o ponto de apoio determina o **limiar** com que a
comparação é feita. O núcleo SHALL exigir que a aula esteja **vigente** e que o vínculo do
Guerreiro(a) seja da **comunidade dela** — o mesmo laço que o registro de presença já aplica —,
para que a escolha da aula NEVER SHALL alcançar o limiar de outra comunidade. (`RF-01-73`,
`RF-01-04`)

#### Scenario: Nick e descritor conferem

- **WHEN** chega um pedido de sessão com nick existente, aula vigente da comunidade dele e
  descritor que confere com o _template_
- **THEN** o núcleo abre a sessão do Guerreiro(a) daquele nick, registrando a autenticação por
  biometria e o momento de expiração

#### Scenario: O limiar aplicado é o do ponto de apoio da aula

- **WHEN** dois pontos de apoio têm limiares medidos diferentes
- **THEN** a comparação de cada entrada usa o limiar do ponto de apoio da aula informada, e não
  um valor comum às duas

#### Scenario: Pedido sem descritor é recusado

- **WHEN** chega um pedido de sessão de Guerreiro(a) sem descritor
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhuma sessão é aberta

#### Scenario: Pedido sem a aula é recusado

- **WHEN** chega um pedido de sessão de Guerreiro(a) sem a aula
- **THEN** o núcleo responde 422 indicando o campo em falta e nenhuma sessão é aberta

#### Scenario: Não há entrada da criança por segredo memorizado

- **WHEN** se procura no núcleo um caminho de sessão de Guerreiro(a) por senha, PIN ou código
- **THEN** nenhum existe: a abertura é por descritor ou por confirmação humana, e nada mais

### Requirement: A recusa não revela se o nick existe

O núcleo SHALL responder **401** ao pedido de sessão que não confere, e a resposta SHALL ser
indistinguível entre nick inexistente, Guerreiro(a) sem _template_ gravado, descritor que não
confere, **ponto de apoio sem limiar medido** e **aula que não vale para aquele Guerreiro(a)**.
A resposta SHALL orientar a chamar o Mestre. O núcleo SHALL NOT expor listagem, busca parcial ou
sugestão de nick em qualquer rota desta capacidade. (`RF-01-04`, `RN-01-22`, `RN-01-56`, PRD-01
§§9, 12)

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
