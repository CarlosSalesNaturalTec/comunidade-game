## Why

A trilha da App 09 já nasce, ganha missões, atividades, etiqueta ODS, culminância e vai ao ar —
mas a missão publicada **não tem o que ensinar**. Nada do que o Mestre escreve chega ao
Guerreiro(a): não há corpo de texto, imagem, vídeo, arquivo de apoio nem bibliografia. A Área do
Guerreiro(a) (PRD-05) percorre uma trilha que precisa ter conteúdo escrito antes, e esta é a
fatia que o cria.

É também a primeira fatia depois da elicitação de 2026-08-25, e três decisões daquela rodada a
encolhem: o custo de _cloud_ entra por fatura e **nenhuma medição por ato** é construída
(`RF-09-20`, `RN-09-07`), o vínculo da bibliografia com o exemplar tombado é **opcional**, e o
conteúdo de terceiros é registrado com a fonte em **campo de texto**, sem anexo (`RF-09-24`).

## What Changes

- Nasce a entidade `Conteudo` (PRD-09 §8): missão, tipo, corpo ou endereço, tamanho, autoria
  própria ou de terceiro e fonte. `POST /v1/missoes/{id}/conteudos` cria conteúdo de texto,
  imagem ou link externo (`RF-09-14`, `RF-09-15`).
- Nasce o **upload retomável** do vídeo e do arquivo de apoio, por
  `POST /v1/conteudos/{id}/arquivo`, com os limites de 200 MB e 20 MB por missão e a lista
  fechada de formatos — MP4, WebM, JPG, PNG, WebP, MP3 e PDF (`RF-09-16` a `RF-09-19`,
  `RF-09-115`, `RN-09-06`). O upload não passa pelo núcleo: o núcleo abre a sessão retomável e o
  cliente envia direto ao armazenamento, o que é o que sustenta "sobrevive à queda de rede sem
  recomeçar do zero".
- Nasce a entidade `BibliografiaDaMissao`, com `POST /v1/missoes/{id}/bibliografia`: título e
  capítulo em texto, e **opcionalmente** o exemplar tombado do acervo (`RF-09-21`). Havendo
  vínculo, a leitura diz se há exemplar no ponto de apoio e credita o Apoiador que o forneceu;
  não havendo, não diz nem credita (`RF-09-22`, `RF-09-23`).
- Conteúdo de terceiro exige **fonte registrada**: o núcleo recusa com 422 o conteúdo de
  terceiro sem fonte, no ato de criá-lo (`RF-09-24`, PRD-09 §§8, 9). A trava é do conteúdo, não
  da trilha — as travas da publicação seguem sendo **três e nenhuma outra**.
- A App 09 ganha a tela de conteúdo da missão — escrita, envio com progresso, bibliografia — e a
  **pré-visualização** da missão como o Guerreiro(a) a verá (`RF-09-25`, desejável).
- A trilha publicada passa a servir o conteúdo da missão sob a licença CC BY-SA já declarada,
  com crédito ao Mestre autor (`RN-09-05`).
- **Nenhuma medição de consumo de _cloud_ é construída**: nem contador de bytes, nem lançamento
  no livro-razão por envio. `RF-09-20` e `RN-09-07` são atendidos por ausência, e a fatia trava
  isso em teste (documento 04).

## Capabilities

### New Capabilities

- `conteudo-da-missao`: o corpo da missão — texto, imagem, link externo, vídeo e arquivo de
  apoio —, os limites e formatos aceitos, o upload retomável, a fonte do conteúdo de terceiro e
  a ausência deliberada de medição de _cloud_.
- `bibliografia-da-missao`: o vínculo entre a missão e o acervo — título e capítulo em texto,
  exemplar tombado opcional, disponibilidade no ponto de apoio e crédito ao Apoiador.

### Modified Capabilities

- `area-do-mestre`: a App 09 ganha as telas de conteúdo, de bibliografia e de pré-visualização
  da missão.

## Impact

- **Núcleo:** módulos novos `conteudos/` e `bibliografias/` em `backend/src/nucleo/`; migração
  com as duas tabelas. `trilhas/regra.py` **não é tocado**: nenhuma trava nova de publicação.
- **Armazenamento:** `PortaDeArmazenamento` ganha a abertura de sessão retomável, com adaptador
  de Cloud Storage em produção e equivalente em disco fora dela — hoje a porta só grava bytes de
  uma vez, o que serve ao comprovante de 20 MB e não ao vídeo de 200 MB.
- **App 09:** telas de conteúdo, bibliografia e pré-visualização.
- **Leitura pública:** `GET /v1/trilhas/{id}` passa a devolver o conteúdo e a bibliografia da
  missão.
- **Não toca:** livro-razão, catálogo de tipos de recurso e `patrimonio`, que a bibliografia só
  lê.
