## MODIFIED Requirements

### Requirement: O Guerreiro(a) percorre o conteúdo e a bibliografia da missão

A aplicação SHALL exibir o **conteúdo da missão** — texto, imagens, vídeo e arquivos — na ordem
em que o Mestre autor o dispôs, com o **crédito ao autor** e a **licença** que a trilha
publicada declara. A **bibliografia** SHALL indicar **título** e **capítulo** e, quando o
Guerreiro(a) tiver ponto de apoio, **se há exemplar disponível nele**; sem essa informação, a
disponibilidade SHALL ficar **indeterminada**, nunca afirmada nem negada por suposição.

A imagem e o vídeo enviados SHALL ser **exibidos** — a imagem visível e o vídeo reproduzível —,
e o arquivo de apoio SHALL ser alcançável pelo Guerreiro(a). A **referência do armazenamento**
NEVER SHALL aparecer na tela: ela não é conteúdo, não diz nada a quem lê e ocupa o lugar do que
o Mestre escreveu. Conteúdo cujo envio não foi concluído SHALL ser omitido ou dito pendente,
nunca apresentado como quebrado. (`RF-05-11`, `RF-05-12`)

#### Scenario: O conteúdo abre na ordem do autor

- **WHEN** o Guerreiro(a) abre uma missão desbloqueada
- **THEN** percorre o conteúdo dela na ordem declarada, com crédito ao Mestre autor e a licença

#### Scenario: A bibliografia diz onde encontrar o livro

- **WHEN** a missão traz bibliografia vinculada a exemplar do ponto de apoio do Guerreiro(a)
- **THEN** a tela indica título, capítulo e se há exemplar disponível nele

#### Scenario: Sem vínculo, a disponibilidade não é afirmada

- **WHEN** a bibliografia da missão não está vinculada a exemplar tombado
- **THEN** a tela mostra título e capítulo e nada afirma sobre disponibilidade

#### Scenario: A imagem do conteúdo aparece como imagem

- **WHEN** o Guerreiro(a) abre uma missão cujo conteúdo tem imagem com envio confirmado
- **THEN** a imagem é exibida na ordem em que o Mestre a dispôs

#### Scenario: A referência do armazenamento não chega à tela

- **WHEN** a missão traz conteúdo de imagem, vídeo ou arquivo
- **THEN** nenhuma referência de armazenamento é apresentada como se fosse o conteúdo

#### Scenario: Envio não concluído não aparece quebrado

- **WHEN** a missão traz conteúdo de arquivo cujo envio nunca foi confirmado
- **THEN** a tela o omite ou o diz pendente, e nada quebrado é apresentado
