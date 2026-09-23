## ADDED Requirements

### Requirement: A equipe nasce com nome obrigatório e único na aula ou na trilha

O núcleo SHALL exigir, na criação da equipe da aula e na da trilha, um **nome** em texto livre,
com **1 a 20 caracteres** depois de aparados os espaços das pontas. O nome SHALL ser **único**
entre as equipes da **mesma aula** — ou da **mesma trilha** —, comparado sem distinguir
maiúsculas de minúsculas e sem os espaços das pontas. O núcleo SHALL gravar o nome aparado.
Nome ausente, em branco, acima de 20 caracteres ou repetido SHALL ser recusado com **422** e
nada é gravado. O mesmo nome em aulas ou trilhas diferentes SHALL ser aceito. (`RF-04-69`,
`RN-04-39`, documento 02 §5)

#### Scenario: A equipe da aula nasce com o nome dado

- **WHEN** um Guerreiro(a) em sessão cria a equipe da aula com o nome "Leões"
- **THEN** o núcleo responde 201 e a equipe é gravada com o nome "Leões"

#### Scenario: A equipe da trilha nasce com o nome dado

- **WHEN** um Guerreiro(a) em sessão cria a equipe da trilha com um nome válido
- **THEN** o núcleo responde 201 e a equipe é gravada com aquele nome

#### Scenario: Criar sem nome é recusado

- **WHEN** chega a criação de equipe sem nome, ou com nome só de espaços
- **THEN** o núcleo responde 422 e nenhuma equipe é criada

#### Scenario: Nome acima de 20 caracteres é recusado

- **WHEN** chega a criação de equipe com um nome de 21 caracteres
- **THEN** o núcleo responde 422 e nenhuma equipe é criada

#### Scenario: Nome repetido na mesma aula é recusado, sem distinguir caixa

- **WHEN** a aula já tem a equipe "Leões" e chega a criação de outra chamada " leões "
- **THEN** o núcleo responde 422 e nenhuma equipe é criada

#### Scenario: Nome repetido na mesma trilha é recusado

- **WHEN** a trilha já tem uma equipe com aquele nome e chega a criação de outra igual
- **THEN** o núcleo responde 422 e nenhuma equipe é criada

#### Scenario: O mesmo nome em aulas diferentes é aceito

- **WHEN** a aula de ontem teve a equipe "Leões" e hoje um Guerreiro(a) cria outra "Leões"
- **THEN** o núcleo cria a equipe de hoje

### Requirement: Quem integra a equipe a renomeia, enquanto a composição está aberta

O núcleo SHALL expor `PATCH /v1/equipes/{id}` sob a **sessão do Guerreiro(a)** e a chave de
aplicação. **Qualquer integrante** da equipe SHALL poder trocar o nome, com a mesma regra da
criação — tamanho e unicidade na aula ou na trilha, sem contar a própria equipe. Quem não
integra a equipe SHALL receber **403**, e Admin e Mestre também. A troca SHALL travar junto com
a composição: equipe de aula encerrada ou equipe da trilha homologada SHALL recusar a troca com
**422**. (`RF-04-70`, `RN-04-39`, `RF-01-16`, documento 02 §5)

#### Scenario: Integrante renomeia a equipe

- **WHEN** um integrante em sessão pede a troca do nome da equipe para um nome livre na aula
- **THEN** o núcleo responde 200 com a equipe já com o nome novo

#### Scenario: Mudar só a caixa do próprio nome é aceito

- **WHEN** a equipe "leões" pede a troca do próprio nome para "Leões"
- **THEN** o núcleo aceita, porque a única equipe com esse nome é ela mesma

#### Scenario: Renomear para nome de outra equipe da aula é recusado

- **WHEN** um integrante pede um nome que outra equipe da mesma aula já usa
- **THEN** o núcleo responde 422 e o nome não muda

#### Scenario: Quem não integra não renomeia

- **WHEN** um Guerreiro(a) que não integra a equipe pede a troca do nome dela
- **THEN** o núcleo responde 403 e o nome não muda

#### Scenario: A gestão não renomeia

- **WHEN** um Admin ou um Mestre em sessão pede a troca do nome de uma equipe
- **THEN** o núcleo responde 403 e o nome não muda

#### Scenario: Equipe de aula encerrada não troca de nome

- **WHEN** um integrante pede a troca do nome de uma equipe cuja aula já se encerrou
- **THEN** o núcleo responde 422 e o nome não muda

#### Scenario: Equipe da trilha homologada não troca de nome

- **WHEN** um integrante pede a troca do nome de uma equipe da trilha já homologada
- **THEN** o núcleo responde 422 e o nome não muda

## MODIFIED Requirements

### Requirement: A leitura das equipes da aula devolve apenas avatar e nick

O núcleo SHALL devolver, em `GET /v1/aulas/{id}/equipes`, as equipes vinculadas **àquela** aula,
cada uma com o **nome** e com os integrantes identificados **apenas por avatar e nick**. A
leitura NEVER SHALL devolver nome civil, data de nascimento, imagem, _template_ biométrico ou
qualquer outro dado pessoal do Guerreiro(a), e NEVER SHALL trazer equipe de outra aula nem
equipe da trilha. A leitura SHALL ser restrita à persona em sessão pela operação
`equipes_da_aula_em_andamento` da matriz. (`RF-04-34`, `RN-04-14`, `RF-01-37`, documento 99 §6
invariantes 11 e 12)

#### Scenario: As equipes daquela aula são devolvidas

- **WHEN** um Guerreiro(a) em sessão consulta as equipes de uma aula
- **THEN** o núcleo devolve as equipes vinculadas àquela aula, cada uma com o nome e os
  integrantes

#### Scenario: Só avatar e nick de cada integrante

- **WHEN** a leitura devolve os integrantes de uma equipe
- **THEN** cada integrante traz avatar e nick, e nenhum outro dado pessoal

#### Scenario: Equipe da trilha não aparece na leitura da aula

- **WHEN** existem equipes de trilha além das equipes da aula consultada
- **THEN** o núcleo devolve apenas as equipes da aula, sem as da trilha

#### Scenario: Aula sem equipe devolve conjunto vazio

- **WHEN** a aula consultada ainda não tem equipe formada
- **THEN** o núcleo responde 200 com conjunto vazio, nunca erro
