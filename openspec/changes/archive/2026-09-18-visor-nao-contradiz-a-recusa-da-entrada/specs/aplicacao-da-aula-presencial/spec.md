## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra por nick e imagem, e a presença é registrada na entrada

A App 01 SHALL oferecer, no caminho das trilhas, a entrada por **nick e imagem**: o nick
informado na tela e o **descritor gerado no próprio aparelho**, na ordem prova de vivacidade e
depois descritor facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser
descartada sem sair do aparelho e NEVER SHALL ser gravada nem enviada.

A tela SHALL apresentar o **visor ao vivo** da câmera enquanto a captura acontece, e SHALL
detectar **em laço** até a vivacidade passar ou o tempo se esgotar, em vez de julgar um único
quadro. O **quadro capturado** NEVER SHALL voltar à tela. (`RF-04-64`, `RN-04-34`)

O **retorno abstrato do laço** — rosto procurado, rosto encontrado, pessoa confirmada — SHALL
valer apenas enquanto a captura acontece, e NEVER SHALL permanecer na tela depois de a
tentativa ter desfecho. Nenhuma tela SHALL apresentar, ao mesmo tempo, o retorno do laço e o
desfecho da tentativa: quem opera leria as duas frases como um único julgamento contraditório.
(`RF-04-64`, `RN-04-34`)

Reconhecido o Guerreiro(a), a aplicação SHALL abrir a sessão dele e SHALL registrar a
**presença do dia no modo reconhecimento**, no mesmo atendimento. Presença já constante do
encontro NEVER SHALL ser duplicada nem tratada como erro: a aplicação SHALL avisar que ela já
existe e voltar à tela inicial. (`RF-04-18`, `RF-04-19`, `RF-04-29`, `RN-04-12`, `RN-04-06`,
PRD-04 §5.4)

#### Scenario: Nick e imagem conferem

- **WHEN** o Guerreiro(a) informa o nick e a câmera captura a imagem dele na chegada
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra a presença do dia por
  reconhecimento

#### Scenario: A presença do encontro já constava

- **WHEN** um Guerreiro(a) já com presença registrada naquela aula é reconhecido de novo
- **THEN** a aplicação avisa que a presença já existe, não duplica registro algum e volta à
  tela inicial

#### Scenario: Nenhuma imagem de criança sai do aparelho

- **WHEN** a entrada por nick e imagem acontece
- **THEN** nenhuma requisição carrega fotografia, e nenhuma imagem fica gravada no aparelho
  compartilhado

#### Scenario: Quem chega se vê no visor antes de a captura julgar

- **WHEN** a entrada por nick e imagem abre a câmera
- **THEN** o visor ao vivo aparece na tela, e a detecção segue em laço até aprovar ou o tempo
  se esgotar

#### Scenario: O retorno do laço não sobrevive à recusa do núcleo

- **WHEN** a vivacidade é confirmada e, em seguida, o núcleo recusa a abertura da sessão
- **THEN** a tela apresenta apenas a frase da recusa, e o retorno do laço já não está na tela

#### Scenario: O retorno do laço não sobrevive à falha de preparo nem à vivacidade reprovada

- **WHEN** a tentativa termina por preparo que falhou ou por vivacidade reprovada
- **THEN** a tela apresenta apenas a frase daquele desfecho, sem o retorno do laço ao lado

#### Scenario: Sem câmera, a entrada segue pela confirmação humana

- **WHEN** o aparelho não tem câmera disponível
- **THEN** a aplicação não oferece a captura e encaminha o Guerreiro(a) à confirmação de Mestre
  ou Admin, sem deixá-lo fora da aula
