## Purpose

O corpo da missão — o que o Guerreiro(a) lê, assiste e baixa. Cobre o texto formatado, a
imagem, o link externo, o vídeo e o arquivo de apoio hospedados pela plataforma, os limites e
formatos aceitos, o upload retomável, a fonte exigida do conteúdo de terceiro e a ausência
deliberada de qualquer medição de consumo de nuvem.

## ADDED Requirements

### Requirement: O conteúdo pertence a uma missão e só o Mestre autor o escreve

O núcleo SHALL vincular todo `Conteudo` a uma **missão**, e NEVER SHALL aceitar conteúdo sem
missão. A escrita SHALL ser privativa do **Mestre autor da trilha** a que a missão pertence:
pedido de outro Mestre SHALL responder **403**, e o Admin NEVER SHALL escrever conteúdo — ele
audita e despublica a trilha, não a redige. O conteúdo SHALL ser ordenado dentro da missão, e a
ordem SHALL ser declarada pelo Mestre. (`RF-09-14`, `RF-09-15`, `RN-09-16`, PRD-09 §§8, 9)

#### Scenario: Mestre autor escreve o conteúdo da sua missão

- **WHEN** o Mestre autor cria conteúdo de texto numa missão da própria trilha
- **THEN** o núcleo grava o conteúdo vinculado àquela missão, na ordem declarada

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha cria conteúdo numa missão dela
- **THEN** o núcleo responde **403** e nada é gravado

#### Scenario: Admin não escreve conteúdo

- **WHEN** um Admin cria conteúdo numa missão
- **THEN** o núcleo responde **403** e nada é gravado

### Requirement: O conteúdo declara o tipo, e cada tipo traz o que lhe cabe

O núcleo SHALL aceitar `Conteudo` de cinco tipos — **texto**, **imagem**, **link externo**,
**vídeo** e **arquivo** — e SHALL exigir de cada um o que lhe corresponde: texto traz o corpo
formatado; link externo traz o endereço; imagem, vídeo e arquivo nascem sem bytes e os recebem
depois, pela sessão de envio. Conteúdo de texto sem corpo, ou de link externo sem endereço,
SHALL responder **422**. O núcleo NEVER SHALL exigir do Mestre marcação técnica, HTML ou código
para escrever o texto. (`RF-09-14`, `RF-09-15`, `RN-09-16`, PRD-09 §8)

#### Scenario: Texto formatado é gravado

- **WHEN** o Mestre autor cria conteúdo de texto com o corpo escrito
- **THEN** o núcleo grava o conteúdo com o corpo, sem exigir marcação alguma

#### Scenario: Link externo é gravado com o endereço

- **WHEN** o Mestre autor cria conteúdo de link externo apontando um vídeo hospedado fora
- **THEN** o núcleo grava o endereço, sem baixar nem hospedar o vídeo apontado

#### Scenario: Texto sem corpo é recusado

- **WHEN** chega conteúdo de texto sem corpo
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Conteúdo de arquivo nasce sem bytes

- **WHEN** o Mestre autor cria conteúdo de vídeo ou de arquivo
- **THEN** o núcleo grava o conteúdo sem bytes, pronto para receber o envio

### Requirement: Conteúdo de terceiro sem fonte registrada é recusado

O núcleo SHALL exigir de todo `Conteudo` a declaração de **autoria** — própria do Mestre ou de
**terceiro** — e, sendo de terceiro, SHALL exigir a **fonte**, em campo de texto. Conteúdo de
terceiro sem fonte SHALL responder **422** no ato de criá-lo. O núcleo NEVER SHALL exigir
anexo, documento de autorização ou comprovante de uso: a decisão do fundador de 2026-08-25
fixou a fonte em texto e nada além. (`RF-09-24`, documento 03 §11, PRD-09 §§8, 9)

#### Scenario: Conteúdo de terceiro com fonte é aceito

- **WHEN** o Mestre autor cria conteúdo declarado de terceiro, informando a fonte em texto
- **THEN** o núcleo grava o conteúdo com a fonte declarada

#### Scenario: Conteúdo de terceiro sem fonte é recusado

- **WHEN** chega conteúdo declarado de terceiro sem fonte
- **THEN** o núcleo responde **422** e nada é gravado

#### Scenario: Conteúdo próprio dispensa fonte

- **WHEN** o Mestre autor cria conteúdo declarado de autoria própria, sem informar fonte
- **THEN** o núcleo grava o conteúdo, e nada é recusado

#### Scenario: Nenhum anexo de autorização é pedido

- **WHEN** conteúdo de terceiro é criado com a fonte em texto e sem anexo algum
- **THEN** o núcleo o aceita, e NEVER SHALL exigir documento de autorização

### Requirement: O arquivo é enviado em sessão retomável, sem passar pelo núcleo

O núcleo SHALL abrir, a pedido do Mestre autor, uma **sessão de envio retomável** para o
conteúdo de imagem, vídeo ou arquivo, e SHALL devolver ao cliente o endereço da sessão. Os
bytes NEVER SHALL trafegar pelo núcleo: o cliente envia direto ao armazenamento, e o núcleo
guarda apenas a **referência**. A sessão SHALL admitir continuação a partir do ponto já
recebido, de modo que a queda de rede NEVER SHALL obrigar a recomeçar do zero. Encerrado o
envio, o Mestre autor SHALL confirmá-lo, e só então o conteúdo passa a servir bytes.
(`RF-09-16`, `RF-09-17`, `RF-09-19`, `RN-01-28`, PRD-09 §§9, 10)

#### Scenario: A sessão é aberta e o endereço volta ao cliente

- **WHEN** o Mestre autor pede o envio do arquivo de um conteúdo dele
- **THEN** o núcleo abre a sessão retomável e devolve o endereço por onde o cliente enviará

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

### Requirement: O envio aceita só a lista fechada de formatos

O núcleo SHALL aceitar no envio apenas **MP4, WebM, JPG, PNG, WebP, MP3 e PDF**, e SHALL
recusar com **422** qualquer outro formato, nomeando o que chegou e a lista aceita. A recusa
SHALL acontecer na abertura da sessão, antes de qualquer byte ser enviado. O que é enviado
NEVER SHALL passar por conferência prévia de conteúdo: cai na auditoria mensal por amostragem
do Admin, como a trilha. (`RF-09-115`, documento 03 §11)

#### Scenario: Formato da lista é aceito

- **WHEN** o Mestre autor abre sessão de envio para um vídeo MP4
- **THEN** o núcleo abre a sessão

#### Scenario: Formato fora da lista é recusado antes do envio

- **WHEN** o Mestre autor abre sessão de envio para um executável
- **THEN** o núcleo responde **422** nomeando a lista aceita, e nenhuma sessão é aberta

#### Scenario: Nada é conferido previamente

- **WHEN** um arquivo em formato aceito é enviado
- **THEN** o núcleo o guarda sem conferir o conteúdo, que fica sujeito à auditoria por amostragem

### Requirement: Cada arquivo tem o teto do seu tipo

O núcleo SHALL recusar com **413** o envio de **vídeo acima de 200 MB** e o de **arquivo de
apoio acima de 20 MB**, informando o tamanho recebido e o teto do tipo. O teto é de **cada
arquivo**, não da soma da missão: a missão SHALL admitir mais de um vídeo e mais de um arquivo,
cada um dentro do seu teto — decisão do fundador de 2026-08-25. A recusa SHALL acontecer na
abertura da sessão, pelo tamanho declarado, e de novo ao fim do envio, se o recebido divergir do
declarado. (`RF-09-16`, `RF-09-17`, `RF-09-18`, `RN-09-06`, PRD-09 §9)

#### Scenario: Vídeo dentro do teto é aceito

- **WHEN** o Mestre autor abre sessão para um vídeo de 180 MB
- **THEN** o núcleo abre a sessão

#### Scenario: Vídeo acima do teto é recusado

- **WHEN** o Mestre autor abre sessão para um vídeo de 240 MB
- **THEN** o núcleo responde **413** dizendo o tamanho recebido e o teto de 200 MB

#### Scenario: Arquivo de apoio acima do teto é recusado

- **WHEN** o Mestre autor abre sessão para um PDF de 32 MB
- **THEN** o núcleo responde **413** dizendo o tamanho recebido e o teto de 20 MB

#### Scenario: Dois vídeos na mesma missão são aceitos

- **WHEN** o Mestre autor envia um segundo vídeo de 150 MB à missão que já tem um de 180 MB
- **THEN** o núcleo aceita os dois, porque o teto é de cada arquivo

#### Scenario: Envio que diverge do tamanho declarado é recusado ao fim

- **WHEN** o envio conclui com mais bytes do que o tamanho declarado na abertura
- **THEN** o núcleo responde **413**, e o conteúdo NEVER SHALL passar a servir aquele arquivo

### Requirement: A trilha publicada serve o conteúdo da missão

A leitura pública da trilha publicada SHALL servir, por missão, o **conteúdo declarado**, na
ordem em que o Mestre o dispôs, sob a licença **CC BY-SA** e com o crédito ao **Mestre autor**
que a trilha já declara. Conteúdo de trilha em rascunho ou despublicada NEVER SHALL sair na
leitura pública. A fonte do conteúdo de terceiro SHALL acompanhar o conteúdo servido.
(`RF-09-09`, `RF-09-10`, `RF-09-24`, `RN-09-05`)

#### Scenario: Conteúdo da trilha publicada é servido

- **WHEN** alguém lê publicamente uma trilha publicada
- **THEN** cada missão traz o conteúdo dela na ordem declarada, com a licença e o crédito ao autor

#### Scenario: Conteúdo de rascunho não sai

- **WHEN** alguém lê publicamente uma trilha em rascunho
- **THEN** nenhum conteúdo é servido, como a trilha inteira já não é servida

#### Scenario: A fonte do terceiro acompanha o conteúdo

- **WHEN** uma missão publicada traz conteúdo declarado de terceiro
- **THEN** a fonte declarada acompanha o conteúdo servido

### Requirement: Nenhum consumo de nuvem é medido nem lançado

O núcleo NEVER SHALL medir, contar ou acumular bytes armazenados por missão, por trilha ou por
Mestre, e NEVER SHALL gerar lançamento no livro-razão por conta de envio de conteúdo. O custo de
_cloud_ entra pela **fatura do período**, como aporte por absorção, e nenhuma aplicação o apura
por ato — decisão do fundador de 2026-08-25. (`RF-09-20`, `RN-09-07`, documento 04)

#### Scenario: Envio não gera lançamento

- **WHEN** um vídeo de 200 MB é enviado e confirmado
- **THEN** nenhum lançamento entra no livro-razão, e nenhum saldo de recurso se altera

#### Scenario: Nenhum contador de bytes é mantido

- **WHEN** uma missão acumula vários conteúdos com arquivo
- **THEN** o núcleo NEVER SHALL expor total de bytes da missão, da trilha nem do Mestre
