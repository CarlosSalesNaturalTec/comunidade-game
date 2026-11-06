## ADDED Requirements

### Requirement: O freio por origem atrasa a repetição na consulta por nick e nos formulários

O núcleo SHALL contar por **origem** a consulta por nick exato e os envios dos formulários de
participação e de dados, e SHALL recusar com **429**, informando a espera, a que exceder o
limite da superfície na janela do documento 03 §8, com atraso crescente até o teto ali
declarado. NEVER SHALL exigir CAPTCHA, cadastro ou dado do visitante. (`RF-01-65`,
`RN-01-27`, `RN-03-08`)

#### Scenario: Consulta por nick dentro do limite responde

- **WHEN** uma origem consulta por nick exato dentro do limite da janela
- **THEN** o núcleo processa a consulta segundo as regras da rota

#### Scenario: Varredura de nicks encontra o freio

- **WHEN** uma origem excede o limite de consultas por nick na janela
- **THEN** o núcleo responde 429 e informa o tempo de espera

#### Scenario: O atraso cresce a cada repetição

- **WHEN** a mesma origem volta a exceder o limite depois de já ter sido freada
- **THEN** o tempo de espera informado é maior que o da recusa anterior, até o teto declarado

#### Scenario: O atraso não passa do teto

- **WHEN** uma origem insiste muito além do número de repetições que atingiria o teto
- **THEN** o tempo de espera informado é o teto, e não cresce além dele

#### Scenario: Envio repetido de formulário encontra o freio

- **WHEN** uma origem excede o limite de envios do formulário de participação ou do de dados na
  janela
- **THEN** o núcleo responde 429, informa o tempo de espera e não grava a solicitação

#### Scenario: O freio nunca pede CAPTCHA nem cadastro

- **WHEN** uma origem é freada em qualquer das superfícies
- **THEN** a resposta traz apenas a recusa e o tempo de espera, e nenhum caminho de liberação
  exige CAPTCHA, login ou dado do visitante

#### Scenario: Origens distintas não dividem o mesmo freio

- **WHEN** uma origem é freada numa superfície e outra origem chama a mesma superfície
- **THEN** a segunda é processada normalmente, dentro do próprio limite

#### Scenario: As superfícies contam separadamente

- **WHEN** uma origem é freada na consulta por nick e, em seguida, envia um formulário de
  participação pela primeira vez
- **THEN** o envio é processado, porque o limite de cada superfície é contado em separado

## REMOVED Requirements

### Requirement: O freio por origem atrasa a repetição nas superfícies públicas

**Reason**: a consulta ao assistente do Desenvolvedor deixou de ser superfície do freio porque
a rota saiu do núcleo — `RN-03-39` retirado, decisão do fundador de 2026-11-06. O resto do
requisito segue inteiro, sem mudança, em "O freio por origem atrasa a repetição na consulta por
nick e nos formulários".
**Migration**: nenhuma para as superfícies que ficam; a superfície `assistente_do_desenvolvedor`
e o limite dela saem da configuração.
