# convencoes-da-api Specification

## Purpose
Define o contrato que toda rota do Backend API obedece, qualquer que seja o domínio que ela
sirva: onde a rota vive, que forma tem um erro, como uma listagem se pagina e se filtra, como
data e hora trafegam e onde o contrato da API fica publicado. É a base que as demais fatias do
PRD-01 e as changes de PRD-08 e PRD-07 reaproveitam em vez de reinventar.
## Requirements
### Requirement: Toda rota de dados vive sob prefixo de versão

O núcleo SHALL expor toda rota de dados sob um prefixo de versão na própria rota, começando em
`/v1`. Rota de dados fora do prefixo não existe. (`RF-01-01`)

#### Scenario: Rota de dados responde sob o prefixo

- **WHEN** uma aplicação chama uma rota de dados do núcleo com o prefixo `/v1`
- **THEN** o núcleo processa a chamada normalmente

#### Scenario: Rota de dados sem prefixo não existe

- **WHEN** uma aplicação chama uma rota de dados sem o prefixo de versão
- **THEN** o núcleo responde 404, sem revelar se a rota existe sob algum prefixo

### Requirement: Erro tem corpo único

O núcleo SHALL responder todo erro com um corpo de forma única, contendo código do erro,
mensagem em linguagem simples e, quando o erro for de validação, o campo em falta. A mensagem
SHALL ser legível por quem não conhece o sistema e SHALL estar em português do Brasil.
(`RF-01-27`)

#### Scenario: Erro de validação nomeia o campo

- **WHEN** uma chamada chega sem um campo obrigatório
- **THEN** o núcleo responde 422 com código do erro, mensagem em linguagem simples e o nome do
  campo em falta

#### Scenario: Erro sem campo associado omite o campo

- **WHEN** uma chamada falha por motivo que não se prende a um campo específico
- **THEN** o núcleo responde com código e mensagem, e o corpo não traz campo em falta

#### Scenario: Mensagem de erro não vaza detalhe interno

- **WHEN** uma chamada provoca uma falha inesperada no núcleo
- **THEN** o núcleo responde 500 com o mesmo corpo único, sem rastro de pilha, nome de tabela,
  consulta ou caminho de arquivo na mensagem

### Requirement: Listagem se pagina e se filtra por contrato único

O núcleo SHALL paginar toda rota de listagem e SHALL aceitar, nas listagens de dado de
comunidade, filtro por comunidade, por período e por persona. A resposta paginada SHALL
informar como obter a página seguinte e SHALL ser estável entre chamadas consecutivas com os
mesmos parâmetros. (`RF-01-28`)

#### Scenario: Listagem devolve página e caminho para a seguinte

- **WHEN** uma aplicação chama uma rota de listagem sem informar paginação
- **THEN** o núcleo devolve a primeira página, com tamanho padrão declarado, e a informação de
  como pedir a seguinte

#### Scenario: Tamanho de página acima do teto é recusado

- **WHEN** uma aplicação pede uma página maior que o teto declarado
- **THEN** o núcleo responde 422 nomeando o parâmetro e o teto vigente

#### Scenario: Filtro não reconhecido é recusado

- **WHEN** uma aplicação envia um parâmetro de filtro que a rota não declara
- **THEN** o núcleo responde 422 nomeando o parâmetro, em vez de ignorá-lo em silêncio

### Requirement: Data e hora trafegam com fuso, e a data do fato não é a do registro

O núcleo SHALL representar toda data e hora com fuso explícito, na entrada e na saída, e SHALL
guardar a data do fato distinta da data do registro sempre que as duas puderem divergir. A data
do fato NEVER é substituída pela data do registro. (PRD-01 §9)

#### Scenario: Data e hora sem fuso é recusada

- **WHEN** uma aplicação envia data e hora sem fuso em um campo que o exige
- **THEN** o núcleo responde 422 nomeando o campo

#### Scenario: Data do fato preservada quando o envio atrasa

- **WHEN** um registro chega ao núcleo depois do momento em que o fato aconteceu, informando o
  momento do fato
- **THEN** o núcleo guarda o momento do fato como informado e o momento do registro à parte,
  e a consulta devolve os dois

### Requirement: Contrato da API é publicado fora do prefixo de versão

O núcleo SHALL publicar o schema OpenAPI e a interface de navegação do contrato **fora do
prefixo de versão** e sem exigir chave de aplicação, porque quem ainda não tem chave precisa
ler o contrato para decidir solicitá-la. O que se publica SHALL descrever rotas e formatos e
NEVER devolver dado de domínio. (`RF-01-30`, documento 03 §1.1)

#### Scenario: Schema responde sem chave

- **WHEN** um visitante sem chave de aplicação pede o schema OpenAPI
- **THEN** o núcleo devolve o schema

#### Scenario: Schema descreve as rotas sem servir dados

- **WHEN** o schema é lido
- **THEN** ele descreve rotas, parâmetros, formatos e erros, e não contém nenhum registro de
  Guerreiro(a), comunidade, aporte ou território

#### Scenario: Publicar o contrato não abre as rotas de dados

- **WHEN** um visitante que leu o schema chama, sem chave, uma rota de dados que ele descreve
- **THEN** o núcleo recusa a chamada pela regra da chave de aplicação

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
