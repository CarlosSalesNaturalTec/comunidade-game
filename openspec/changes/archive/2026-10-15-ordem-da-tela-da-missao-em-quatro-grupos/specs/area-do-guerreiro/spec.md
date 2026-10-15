# Spec Delta

## MODIFIED Requirements

### Requirement: O Guerreiro(a) percorre o conteúdo e a bibliografia da missão

A aplicação SHALL exibir o **conteúdo da missão** — texto, imagens, vídeo e arquivos — na ordem
em que o Mestre autor o dispôs, **um conteúdo por vez**, com um controle de **avançar** que
leva ao seguinte; avançar SHALL apenas percorrer, e NEVER SHALL gravar nem submeter coisa
alguma. A tela SHALL dizer **onde o Guerreiro(a) está na sequência**, para que percorrer não
vire caminhar às cegas, e no último conteúdo NEVER SHALL oferecer avançar para lugar nenhum.
Missão com **um único** conteúdo NEVER SHALL apresentar controle de avançar. (`RF-05-11`,
documento 15 §6.4, decisão do fundador de 2026-09-26)

O **crédito ao autor** e a **licença** que a trilha publicada declara SHALL ser apresentados em
**bloco recolhível de resumo neutro** no **rodapé da tela**, fora do fluxo de leitura do
conteúdo: são metadado da obra, não o que a criança veio ler. Recolhido, o crédito SHALL
continuar **alcançável** — recolher não é suprimir, e a atribuição que a licença exige
continua sendo cumprida.
(`RF-05-11`, documento 15 §§6.1, 6.4)

A **bibliografia** SHALL ficar em **bloco recolhível de resumo neutro**, junto da missão
seguinte, e SHALL ser **omitida** quando a missão não tiver bibliografia. Aberta, SHALL
indicar **título** e **capítulo** e, quando o Guerreiro(a) tiver ponto de apoio, **se há
exemplar disponível nele**; sem essa informação, a disponibilidade SHALL ficar
**indeterminada**, nunca afirmada nem negada por suposição. (`RF-05-12`, documento 15 §6.1,
decisão do fundador de 2026-10-15)

A imagem e o vídeo enviados SHALL ser **exibidos** — a imagem visível e o vídeo reproduzível —,
e o arquivo de apoio SHALL ser alcançável pelo Guerreiro(a). A **referência do armazenamento**
NEVER SHALL aparecer na tela: ela não é conteúdo, não diz nada a quem lê e ocupa o lugar do que
o Mestre escreveu. Conteúdo cujo envio não foi concluído SHALL ser omitido ou dito pendente,
nunca apresentado como quebrado. (`RF-05-11`, `RF-05-12`)

#### Scenario: O conteúdo abre na ordem do autor

- **WHEN** o Guerreiro(a) abre uma missão desbloqueada com quatro conteúdos
- **THEN** o primeiro conteúdo da ordem declarada aparece sozinho, a tela diz onde ele está na
  sequência, e o controle de avançar leva ao segundo

#### Scenario: O último conteúdo não oferece avançar

- **WHEN** o Guerreiro(a) alcança o último conteúdo da missão
- **THEN** a tela não oferece avançar para outro conteúdo

#### Scenario: Conteúdo único não pagina

- **WHEN** a missão tem um único conteúdo
- **THEN** ele aparece sem controle de avançar

#### Scenario: O crédito está recolhido, e continua alcançável

- **WHEN** o Guerreiro(a) abre o conteúdo de uma missão
- **THEN** o crédito ao Mestre autor e a licença não aparecem no fluxo de leitura, e sim num
  bloco fechado de resumo neutro **no rodapé da tela**, que abre ao ser acionado

#### Scenario: A bibliografia diz onde encontrar o livro

- **WHEN** a missão traz bibliografia vinculada a exemplar do ponto de apoio do Guerreiro(a),
  e o Guerreiro(a) abre o bloco dela
- **THEN** a tela indica título, capítulo e se há exemplar disponível nele

#### Scenario: Sem vínculo, a disponibilidade não é afirmada

- **WHEN** a bibliografia da missão não está vinculada a exemplar tombado, e o bloco dela
  está aberto
- **THEN** a tela mostra título e capítulo e nada afirma sobre disponibilidade

#### Scenario: A imagem do conteúdo aparece como imagem

- **WHEN** o Guerreiro(a) alcança, na sequência, o conteúdo de imagem com envio confirmado
- **THEN** a imagem é exibida na posição em que o Mestre a dispôs

#### Scenario: A referência do armazenamento não chega à tela

- **WHEN** a missão traz conteúdo de imagem, vídeo ou arquivo
- **THEN** nenhuma referência de armazenamento é apresentada como se fosse o conteúdo

#### Scenario: Envio não concluído não aparece quebrado

- **WHEN** a missão traz conteúdo de arquivo cujo envio nunca foi confirmado
- **THEN** a tela o omite ou o diz pendente, e nada quebrado é apresentado

#### Scenario: A bibliografia nasce fechada, junto da missão seguinte

- **WHEN** o Guerreiro(a) abre uma missão que tem bibliografia
- **THEN** a bibliografia aparece como bloco fechado de resumo neutro, no mesmo grupo da
  missão seguinte, fora do fluxo de leitura do conteúdo

#### Scenario: Missão sem bibliografia não apresenta o bloco

- **WHEN** a missão aberta não tem bibliografia alguma
- **THEN** nenhum bloco de bibliografia aparece, nem fechado nem vazio

## ADDED Requirements

### Requirement: A tela da missão agrupa o conteúdo, o que se lê depois e o rodapé

A App 05 SHALL apresentar a tela da missão em grupos **separados por linha muda**, nesta
ordem: o **conteúdo e o ato** da missão — a sondagem, o desafio de desbloqueio e a entrega da
produção —; a **próxima missão e a bibliografia**; e o **rodapé**, com o crédito e a licença.
A linha NEVER SHALL carregar rótulo nem ser anunciada, e o grupo sem conteúdo NEVER SHALL
apresentar a linha dele. (`RF-05-08`, `RF-05-10`, `RF-05-11`, documento 15 §6, decisão do
fundador de 2026-10-15)

#### Scenario: Os grupos aparecem na ordem decidida

- **WHEN** o Guerreiro(a) abre o guia da trilha
- **THEN** a tela apresenta, de cima para baixo, o conteúdo da missão com o que há para
  responder, depois a próxima missão com a bibliografia, e por último o rodapé com o crédito,
  com uma linha entre cada par de grupos

#### Scenario: O ato da missão fica junto do conteúdo

- **WHEN** a missão aberta tem sondagem, desafio de desbloqueio ou entrega da produção
- **THEN** o que o Guerreiro(a) responde ou entrega aparece no mesmo grupo do conteúdo, acima
  da primeira linha

#### Scenario: Grupo sem conteúdo não deixa linha na tela

- **WHEN** a missão é a última da trilha e não tem bibliografia
- **THEN** o grupo da próxima missão não aparece, e a sua linha não aparece com ele

#### Scenario: O guia não oferece o catálogo de poderes

- **WHEN** o Guerreiro(a) tem o guia da trilha aberto
- **THEN** o rodapé não oferece escolher outro poder, porque a tela de trocar de trilha já
  alcança o catálogo
