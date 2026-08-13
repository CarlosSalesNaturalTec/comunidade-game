## Purpose

A proteção das rotas públicas é o que impede que a porta aberta da plataforma seja varrida ou
inundada: uma cota de leitura por faixa de chave, que barra o consumo abusivo da API, e um
freio por origem na consulta por nick e nos formulários públicos, que barra a varredura de
nicks de criança e a enchente na fila de avaliação — sem CAPTCHA, sem cadastro do visitante e
sem guardar nada sobre ele.

## ADDED Requirements

### Requirement: A cota de leitura se aplica por faixa da chave

O núcleo SHALL contar as chamadas de **leitura** de cada chave de aplicação numa janela
deslizante e SHALL recusar com **429** a chamada que exceder a cota da **faixa** daquela
chave. A faixa SHALL ser a natureza já registrada na chave — do projeto ou de terceiro —, e a
cota de cada faixa SHALL ser a declarada no documento 03 §8. A escrita NEVER SHALL entrar na
contagem. (`RF-01-55`, 03 §8)

#### Scenario: Leitura dentro da cota é processada

- **WHEN** uma aplicação faz uma chamada de leitura com chave vigente e ainda dentro da cota da
  sua faixa
- **THEN** o núcleo processa a chamada segundo as demais regras da rota

#### Scenario: Leitura acima da cota é recusada com 429

- **WHEN** uma aplicação excede, na janela corrente, a cota de leitura da faixa da sua chave
- **THEN** o núcleo responde 429 e não executa nada da rota

#### Scenario: A faixa de terceiro tem cota menor que a do projeto

- **WHEN** uma chave do projeto e uma chave de terceiro fazem o mesmo número de leituras, acima
  da cota de terceiro e abaixo da cota do projeto
- **THEN** a chave de terceiro recebe 429 e a chave do projeto é processada

#### Scenario: Escrita não consome a cota

- **WHEN** uma aplicação do projeto faz chamadas de escrita além do número que esgotaria a cota
  de leitura da sua faixa
- **THEN** nenhuma delas é recusada por cota, e a cota de leitura da chave segue intacta

#### Scenario: A janela deslizante libera a chave

- **WHEN** a janela avança e as chamadas mais antigas saem da contagem de uma chave que estava
  em 429
- **THEN** a chamada de leitura seguinte volta a ser processada, sem intervenção humana

### Requirement: O freio por origem atrasa a repetição nas superfícies públicas

O núcleo SHALL contar por **origem** as chamadas à consulta por nick exato e aos envios dos
formulários de solicitação de participação e de solicitação de dados, e SHALL recusar com
**429** a que exceder o limite daquela superfície na janela declarada no documento 03 §8. A
recusa SHALL informar o tempo de espera. O atraso SHALL crescer a cada repetição, a partir do
valor inicial e até o teto declarados no documento 03 §8. O freio NEVER SHALL exigir CAPTCHA,
cadastro ou qualquer dado do visitante. (`RF-01-65`, `RN-01-27`, 03 §8)

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

### Requirement: A origem se identifica sem guardar dado do visitante

O núcleo SHALL agrupar as chamadas por origem usando o **resumo criptográfico do endereço de
rede com sal rotativo**, mantido **apenas em memória** e **apenas pela janela** do freio. O
núcleo NEVER SHALL gravar em banco o endereço de rede, o seu resumo ou qualquer outro dado do
visitante, e NEVER SHALL usar cookie, rastreador ou identificador persistente para o freio.
(`RN-01-45`, `RN-01-27`, 03 §8)

#### Scenario: Nenhuma tabela recebe a origem

- **WHEN** o freio conta, atrasa e libera uma origem ao longo de várias janelas
- **THEN** nenhuma linha com o endereço de rede ou o seu resumo é gravada em banco

#### Scenario: O endereço em claro não sobrevive à contagem

- **WHEN** o núcleo agrupa uma chamada por origem
- **THEN** o que se guarda em memória é o resumo com sal, e não o endereço de rede

#### Scenario: O freio não usa cookie nem identificador persistente

- **WHEN** um visitante chama uma superfície freada
- **THEN** o núcleo não emite cookie, não pede identificador e não guarda preferência alguma
  para reconhecê-lo depois

### Requirement: A solicitação de chave não tem freio por origem

O núcleo NEVER SHALL aplicar freio por origem ao envio do formulário de solicitação de chave,
porque nova solicitação é sempre possível. Essa superfície SHALL permanecer protegida apenas
pela cota da faixa da chave da aplicação que a serve. (`RN-01-46`, `RN-01-36`, 03 §8)

#### Scenario: Envio repetido de solicitação de chave não é freado por origem

- **WHEN** a mesma origem envia solicitações de chave em número que freria a origem nos
  formulários de participação ou de dados
- **THEN** nenhuma delas é recusada por freio de origem

#### Scenario: A solicitação de chave segue sob a cota da chave da aplicação

- **WHEN** a aplicação que serve o formulário de solicitação de chave excede a cota da sua
  faixa
- **THEN** a recusa vem da cota, e não do freio por origem
