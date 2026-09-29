# Spec Delta

## MODIFIED Requirements

### Requirement: O freio por origem atrasa a repetição nas superfícies públicas

O núcleo SHALL contar por **origem** as chamadas à consulta por nick exato, aos envios dos
formulários de solicitação de participação e de solicitação de dados e às **consultas ao
assistente do Desenvolvedor**, e SHALL recusar com **429** a que exceder o limite daquela
superfície na janela declarada no documento 03 §8. A
recusa SHALL informar o tempo de espera. O atraso SHALL crescer a cada repetição, a partir do
valor inicial e até o teto declarados no documento 03 §8. O freio NEVER SHALL exigir CAPTCHA,
cadastro ou qualquer dado do visitante. (`RF-01-65`, `RN-01-27`, `RN-03-08`, 03 §8)

A consulta ao assistente do Desenvolvedor é superfície freada porque cada pergunta consome
modelo pago numa rota aberta a qualquer visitante, sem login (decisão do fundador de
2026-09-29). Ela NEVER SHALL dividir contagem com as demais superfícies.

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

#### Scenario: A repetição da pergunta ao assistente encontra o freio

- **WHEN** uma origem excede o limite de consultas ao assistente do Desenvolvedor na janela
- **THEN** o núcleo responde 429, informa o tempo de espera e nenhuma pergunta vai ao modelo

#### Scenario: O freio do assistente não alcança a solicitação de chave

- **WHEN** uma origem é freada no assistente do Desenvolvedor e, em seguida, envia o formulário
  de solicitação de chave
- **THEN** o envio é processado, porque a solicitação de chave não tem freio por origem

