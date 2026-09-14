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
(`RF-09-16`, `RF-09-17`, `RF-09-19`, `RN-01-28`, PRD-09 §§9, 10)

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
