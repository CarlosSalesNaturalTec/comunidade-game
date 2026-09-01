## MODIFIED Requirements

### Requirement: A necessidade publicada leva o recurso, a aula e o lugar, nunca reais

Cada necessidade SHALL sair com **tipo de recurso, quantidade que falta, valor em moedas,
comunidade, ponto de apoio, data e horário da aula**, e SHALL identificar-se pelo par **aula +
tipo de recurso**. O tipo de recurso, a comunidade e o ponto de apoio SHALL sair com o **nome**
ao lado do identificador, para que a leitura se apresente a quem não tem acesso às rotas de
cadastro da gestão. A saída NÃO SHALL trazer valor em reais, em campo algum, nem dado de
pessoa: a necessidade descreve recurso, aula e lugar, e nada de quem participa dela. A mesma
saída SHALL valer para a rota pública e para a do Mestre. (`RF-07-27`, `RF-03-47`, `RN-07-05`,
`RF-14-24`, `RN-14-09`, invariante 16 do documento 99 §6, documento 04 §1)

#### Scenario: A necessidade traz os campos publicados

- **WHEN** uma necessidade é lida em qualquer das duas rotas
- **THEN** ela traz tipo de recurso, quantidade que falta, valor em moedas, comunidade, ponto
  de apoio, data e horário da aula, e identifica a aula e o tipo

#### Scenario: Os nomes acompanham os identificadores

- **WHEN** uma necessidade é lida em qualquer das duas rotas
- **THEN** o tipo de recurso, a comunidade e o ponto de apoio saem com o nome ao lado do
  identificador

#### Scenario: Nenhuma saída traz reais

- **WHEN** a lista de necessidades é lida
- **THEN** nenhum campo da resposta traz valor em reais

#### Scenario: Nenhuma saída traz pessoa

- **WHEN** a lista de necessidades é lida
- **THEN** nenhum campo da resposta identifica Guerreiro(a), responsável ou provedor
