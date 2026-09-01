## Purpose

Governa a prova pública do apoio: os documentos comprobatórios que o Apoiador declara — currículo,
portfólio, redes sociais, termos de doação e comprovantes, sempre como link —, o estado pendente
em que eles nascem, o ato de Admin que os anexa ao cadastro e os publica, e a leitura que o
Apoiador tem do que já está na página dele.

## Requirements

### Requirement: O Apoiador declara o comprobatório do próprio apoio, sempre como link

O núcleo SHALL expor rota em que a persona de **Apoiador em sessão** declara documento
comprobatório do próprio apoio — currículo, portfólio, rede social, termo de doação ou
comprovante —, cada um com **endereço** e **rótulo** do que aponta. A rota SHALL exigir
credencial de persona e SHALL alcançar **apenas a própria persona**; persona de outro papel SHALL
receber **403**. O núcleo NEVER SHALL aceitar anexo de arquivo como documento comprobatório: a
prova é link declarado. Documento sem endereço ou sem rótulo SHALL ser recusado com **422**.
(`RF-14-18`, `RN-02-01`, documento 02 §1, PRD-14 §9)

#### Scenario: O Apoiador declara o currículo e o termo de doação

- **WHEN** um Apoiador em sessão declara dois documentos, cada um com endereço e rótulo
- **THEN** o núcleo grava os dois na persona dele

#### Scenario: Documento sem rótulo é recusado

- **WHEN** um Apoiador declara documento sem endereço, ou sem rótulo
- **THEN** o núcleo responde 422 indicando o campo em falta, e nada é gravado

#### Scenario: Persona de outro papel não usa a rota

- **WHEN** uma persona que não é Apoiador chama a rota de documentos do Apoiador
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O documento enviado pelo Apoiador nasce pendente e não vai a público

Documento comprobatório declarado **pelo próprio Apoiador** SHALL nascer **sem anexação** e
NEVER SHALL aparecer em leitura pública enquanto um Admin não o anexar ao cadastro. O envio
NEVER SHALL publicar por si só, e o Apoiador NEVER SHALL dispor de rota que o publique.
Documento declarado por **Admin no cadastro** da persona SHALL continuar publicado como já
estava — a anexação é o que ele já é. (`RF-14-19`, `RN-14-12`, PRD-14 §§5.9, 11)

#### Scenario: O documento enviado não aparece em público

- **WHEN** um Apoiador declara um documento e uma leitura pública consulta a página dele
- **THEN** o documento não aparece, porque nenhum Admin o anexou

#### Scenario: O Apoiador não publica o próprio documento

- **WHEN** um Apoiador tenta publicar o documento que declarou
- **THEN** não há rota que o faça: a publicação é ato de Admin

#### Scenario: O que o Admin declarou no cadastro permanece publicado

- **WHEN** um Apoiador cadastrado com artefato comprobatório declarado por Admin declara depois
  um documento próprio
- **THEN** o do cadastro segue publicado e o novo fica pendente

### Requirement: É a anexação pelo Admin que publica o documento

O núcleo SHALL expor rota em que um **Admin** anexa ao cadastro do Apoiador um documento que ele
declarou, e a anexação SHALL ser o que o **publica**. A rota SHALL registrar **quem anexou e
quando**. Persona que não seja Admin SHALL receber **403**, e o documento SHALL permanecer
pendente. Documento inexistente, ou que não seja daquele Apoiador, SHALL receber **404**.
Anexação repetida sobre documento já anexado SHALL manter o documento publicado, sem trocar a
autoria da primeira. (`RF-14-19`, `RN-14-12`, `RF-02-101`, decisão do fundador, 2026-09-01,
documento 02 §1)

#### Scenario: Anexado, o documento passa a valer em público

- **WHEN** um Admin anexa ao cadastro o documento que o Apoiador declarou
- **THEN** o núcleo o marca como publicado, com quem anexou e quando

#### Scenario: Quem não é Admin não anexa

- **WHEN** um Apoiador, um Mestre ou um responsável tenta anexar o documento
- **THEN** o núcleo responde 403 e o documento continua pendente

#### Scenario: Documento de outro Apoiador não é alcançado

- **WHEN** um Admin tenta anexar, ao cadastro de um Apoiador, documento que é de outro
- **THEN** o núcleo responde 404 e nada muda

### Requirement: O Apoiador lê o que enviou e o que já está publicado

O núcleo SHALL responder à persona de **Apoiador em sessão** a lista dos próprios documentos
comprobatórios, cada um com endereço, rótulo e a marca de **publicado ou pendente**. A leitura
SHALL alcançar **apenas a própria persona** e NEVER SHALL trazer documento de outro Apoiador.
(`RF-14-20`, `RN-14-12`, PRD-14 §5.9)

#### Scenario: A leitura distingue o publicado do pendente

- **WHEN** um Apoiador com um documento anexado e outro ainda não anexado lê os próprios
  documentos
- **THEN** a resposta traz os dois, um marcado como publicado e o outro como pendente

#### Scenario: O documento alheio fica de fora

- **WHEN** um Apoiador lê os próprios documentos e outro Apoiador também tem documentos
- **THEN** a resposta traz apenas os da persona em sessão
