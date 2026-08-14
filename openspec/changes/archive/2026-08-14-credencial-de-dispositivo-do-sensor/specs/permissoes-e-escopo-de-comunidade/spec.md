## MODIFIED Requirements

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
