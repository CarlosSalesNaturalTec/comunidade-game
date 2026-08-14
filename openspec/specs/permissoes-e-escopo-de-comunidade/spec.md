## Purpose

A chave diz qual aplicação chama; a sessão diz qual pessoa age. Esta capacidade cobre o que o
núcleo faz com essa informação: exigir persona autenticada em toda escrita e gravar a autoria,
conferir a matriz de permissões do PRD-01 §4 em toda operação, e aplicar o filtro por comunidade
em toda consulta de dado de comunidade — a plataforma é instância única, e é o filtro que separa
uma comunidade da vizinha.

## Requirements

### Requirement: Escrita exige persona autenticada e grava autoria

O núcleo SHALL exigir persona autenticada em toda rota de escrita, e SHALL registrar em toda
escrita bem-sucedida **quem** a fez, **com que papel** e **quando**, com fuso. A data do fato
NEVER SHALL ser substituída pela data do registro. Escrita sem credencial de persona SHALL ser
recusada, ainda que a chamada traga chave de aplicação vigente. (`RF-01-03`, `RN-01-34`)

A **credencial de dispositivo** é a **única exceção** a essa exigência, e alcança **uma única
operação**: gravar registro de coleta na série a que a credencial está presa. A escrita por
credencial de dispositivo SHALL continuar gravando autoria — a do **Guerreiro(a) coletor** da
série, com o papel dele —, de modo que a regra de autoria segue inteira e nenhuma escrita fica
sem autor. A exceção NEVER SHALL alcançar outra rota de escrita, e a credencial NEVER SHALL
valer como credencial de persona. (`RF-08-14`, `RN-08-23`)

A trilha de auditoria consultável de ações de Admin (`RF-01-29`) é de outra fatia: aqui nasce o
registro, não a rota que o consulta.

#### Scenario: Escrita autenticada registra autoria

- **WHEN** uma persona autenticada conclui uma escrita
- **THEN** o núcleo grava o autor, o papel dele e a data e hora com fuso

#### Scenario: Escrita sem persona é recusada

- **WHEN** uma escrita chega com chave de aplicação vigente e sem credencial de persona
- **THEN** o núcleo recusa a escrita e nada é gravado

#### Scenario: A data do fato sobrevive ao registro

- **WHEN** uma escrita informa a data do fato e o núcleo a grava
- **THEN** a data do fato permanece a informada, e a data do registro é gravada à parte

#### Scenario: A gravação de registro por dispositivo dispensa a persona

- **WHEN** um sensor grava registro de coleta apresentando a credencial de dispositivo da série,
  com chave de aplicação vigente e sem credencial de persona
- **THEN** o núcleo aceita a escrita e grava como autor o Guerreiro(a) coletor daquela série

#### Scenario: A exceção não alcança outra escrita

- **WHEN** uma chamada autenticada por credencial de dispositivo alcança qualquer rota de
  escrita que não seja a gravação de registro de coleta
- **THEN** o núcleo recusa, porque a exceção vale para uma única operação

### Requirement: A matriz de permissões por papel é conferida em toda operação

O núcleo SHALL conferir, em **toda** operação, a matriz de permissões do PRD-01 §4 contra o
papel da persona em sessão. Operação fora do que o papel permite SHALL ser recusada com **403**.
A conferência SHALL valer para leitura e para escrita, e NEVER SHALL depender de qual aplicação
fez a chamada. (`RF-01-16`, PRD-01 §§4, 9)

#### Scenario: Papel sem permissão recebe 403

- **WHEN** uma persona autenticada tenta uma operação que a matriz não concede ao papel dela
- **THEN** o núcleo responde 403 e não executa a operação

#### Scenario: Papel com permissão é atendido

- **WHEN** uma persona autenticada faz uma operação que a matriz concede ao papel dela
- **THEN** o núcleo executa a operação

#### Scenario: A aplicação de origem não muda o que o papel pode

- **WHEN** a mesma persona faz a mesma operação a partir de aplicações diferentes, cada uma com
  a sua chave vigente
- **THEN** o núcleo decide igual nos dois casos, pelo papel e não pela chave

### Requirement: Consulta de dado de comunidade aceita e aplica o filtro por comunidade

O núcleo SHALL aceitar o filtro por comunidade em toda consulta de dado de comunidade e SHALL
aplicá-lo ao resultado. Onde o filtro for obrigatório, a consulta que chegar sem ele SHALL ser
recusada com **422**. Resultado de uma comunidade NEVER SHALL aparecer na consulta filtrada por
outra. (`RF-01-18`, PRD-01 §9, documento 03 §1)

#### Scenario: A consulta filtrada devolve só a comunidade pedida

- **WHEN** uma consulta de dado de comunidade chega com o filtro de comunidade
- **THEN** o resultado traz apenas registros daquela comunidade

#### Scenario: Filtro obrigatório ausente é recusado

- **WHEN** uma consulta que exige o filtro de comunidade chega sem ele
- **THEN** o núcleo responde 422, indicando o campo em falta

#### Scenario: Instância única não mistura comunidades

- **WHEN** duas comunidades têm registros do mesmo tipo na mesma instância e uma consulta é
  filtrada por uma delas
- **THEN** nenhum registro da outra aparece no resultado
