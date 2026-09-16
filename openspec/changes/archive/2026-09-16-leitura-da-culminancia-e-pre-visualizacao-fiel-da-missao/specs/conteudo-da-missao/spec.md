## MODIFIED Requirements

### Requirement: O arquivo é enviado em sessão retomável, sem passar pelo núcleo

O núcleo SHALL abrir, a pedido do Mestre autor, uma **sessão de envio retomável** para o
conteúdo de imagem, vídeo ou arquivo, e SHALL devolver ao cliente o endereço da sessão. Os
bytes NEVER SHALL trafegar pelo núcleo: o cliente envia direto ao armazenamento, e o núcleo
guarda apenas a **referência**. A sessão SHALL admitir continuação a partir do ponto já
recebido, de modo que a queda de rede NEVER SHALL obrigar a recomeçar do zero. Encerrado o
envio, o Mestre autor SHALL confirmá-lo, e só então o conteúdo passa a servir bytes.

O endereço devolvido SHALL ser **alcançável pela aplicação que vai enviar**: o armazenamento
SHALL admitir o envio partindo do endereço próprio de cada aplicação do projeto, com o
cabeçalho de posição que o protocolo retomável exige, e SHALL devolver ao cliente o cabeçalho
que diz de onde retomar. Endereço que a aplicação não alcança NEVER SHALL ser tratado como
sessão aberta: sem isso o envio é barrado **antes** de o armazenamento ser chamado, e nenhuma
recusa do núcleo explica ao Mestre o que houve. A exigência vale em **todos os ambientes**,
qualquer que seja o armazenamento por trás.

Na confirmação do envio, o núcleo SHALL gravar, junto da referência e do tamanho, o **tipo do
arquivo** tal como o armazenamento o apurou — nunca o tipo declarado na abertura da sessão,
que o recebido pode desmentir. É esse tipo gravado que permite servir os bytes de volta de
modo que a aplicação os exiba; sem ele, o arquivo enviado é indistinguível de dado binário
qualquer. Conteúdo gravado antes desta exigência SHALL seguir legível, com o tipo
indeterminado.
(`RF-09-16`, `RF-09-17`, `RF-09-19`, `RF-09-115`, `RN-01-28`, PRD-09 §§9, 10)

#### Scenario: A sessão é aberta e o endereço volta ao cliente

- **WHEN** o Mestre autor pede o envio do arquivo de um conteúdo dele
- **THEN** o núcleo abre a sessão retomável e devolve o endereço por onde o cliente enviará

#### Scenario: O envio partindo da aplicação do projeto é admitido

- **WHEN** a aplicação do Mestre envia os bytes ao endereço da sessão, a partir do endereço
  próprio dela, declarando a posição da parte
- **THEN** o armazenamento aceita o envio e nenhuma etapa anterior ao armazenamento o barra

#### Scenario: A retomada lê do armazenamento de onde continuar

- **WHEN** a aplicação consulta quanto a sessão já recebeu
- **THEN** o cabeçalho que diz de onde retomar chega à aplicação, e ela continua do ponto certo

#### Scenario: Queda de rede não recomeça o envio

- **WHEN** o envio cai depois de parte dos bytes recebidos e o cliente retoma a mesma sessão
- **THEN** o envio continua do ponto já recebido, sem recomeçar

#### Scenario: Os bytes não passam pelo núcleo

- **WHEN** um envio de 200 MB é concluído
- **THEN** o núcleo guarda apenas a referência do arquivo, e nenhum byte é gravado em tabela

#### Scenario: Conteúdo sem envio confirmado não serve bytes

- **WHEN** um conteúdo de vídeo é lido antes de o envio ser confirmado
- **THEN** o conteúdo é apresentado sem arquivo, e nenhuma referência quebrada é servida

#### Scenario: Sessão pedida por quem não é o autor é recusada

- **WHEN** um Mestre que não é o autor pede a sessão de envio de um conteúdo
- **THEN** o núcleo responde **403** e nenhuma sessão é aberta

#### Scenario: A confirmação grava o tipo apurado no armazenamento

- **WHEN** o Mestre autor confirma o envio de uma imagem
- **THEN** o núcleo grava o tipo do arquivo tal como o armazenamento o apurou, junto da
  referência e do tamanho

#### Scenario: Conteúdo gravado antes da exigência segue legível

- **WHEN** os bytes de um conteúdo enviado antes de o tipo passar a ser gravado são lidos
- **THEN** eles são servidos com o tipo indeterminado, e nenhum erro é respondido

## ADDED Requirements

### Requirement: O arquivo do conteúdo é servido a quem pode ver a missão

O núcleo SHALL servir os **bytes** do conteúdo de imagem, vídeo ou arquivo de apoio ao **Mestre
autor** da trilha e ao **Guerreiro(a) inscrito** nela — os mesmos que já leem a missão —, e a
**ninguém mais**: persona alheia SHALL receber **403**. A leitura SHALL acompanhar o **tipo do
arquivo** gravado na confirmação do envio, para que a aplicação o exiba em vez de descrevê-lo.
Conteúdo sem envio confirmado SHALL responder **404**, do mesmo modo que a leitura já o
apresenta sem arquivo. A referência do armazenamento NEVER SHALL ser apresentada a pessoa
alguma como se fosse o conteúdo. O **envio** continua fora do núcleo; só a **saída** dos bytes
passa por ele. (`RF-05-11`, `RF-09-14`, `RF-09-16`, `RF-09-17`, `RF-09-25`, `RN-01-28`)

#### Scenario: O Mestre autor lê os bytes do próprio conteúdo

- **WHEN** o Mestre autor pede o arquivo de um conteúdo de missão dele, com o envio confirmado
- **THEN** o núcleo devolve os bytes, acompanhados do tipo gravado do arquivo

#### Scenario: O Guerreiro(a) inscrito lê os bytes

- **WHEN** um Guerreiro(a) inscrito na trilha pede o arquivo de um conteúdo de missão dela
- **THEN** o núcleo devolve os bytes, acompanhados do tipo gravado do arquivo

#### Scenario: Persona que não é autora nem inscrita é recusada

- **WHEN** uma persona que não é o Mestre autor nem está inscrita na trilha pede o arquivo
- **THEN** o núcleo responde **403** e nenhum byte é servido

#### Scenario: Conteúdo sem arquivo responde não encontrado

- **WHEN** o arquivo de um conteúdo de texto, ou de um conteúdo cujo envio nunca foi
  confirmado, é pedido
- **THEN** o núcleo responde **404** e nenhum byte é servido

#### Scenario: A leitura alcança trilha em rascunho, para o autor

- **WHEN** o Mestre autor pede o arquivo de um conteúdo de missão de trilha em rascunho
- **THEN** o núcleo devolve os bytes, porque a autoria basta e a publicação não é exigida
