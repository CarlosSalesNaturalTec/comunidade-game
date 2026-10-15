# Spec Delta

## ADDED Requirements

### Requirement: A tela da missão apresenta quatro grupos separados por linha muda

Na tela do percurso, a App 01 SHALL apresentar quatro grupos **nesta ordem**, separados por
**linha muda**: o **conteúdo e o ato** da missão — a sondagem ou o desafio de desbloqueio —;
a **próxima missão e a bibliografia**; as **atividades do encontro**; e o **rodapé**. A linha
NEVER SHALL carregar rótulo nem ser anunciada, e o grupo que não tem conteúdo NEVER SHALL
apresentar a linha dele. (`RF-04-72`, `RF-04-73`, documento 15 §6, decisão do fundador de
2026-10-15)

#### Scenario: Os quatro grupos aparecem na ordem decidida

- **WHEN** o percurso de uma trilha é apresentado no aparelho do encontro
- **THEN** a tela apresenta, de cima para baixo, o conteúdo da missão, a próxima missão com a
  bibliografia, as atividades do encontro e o rodapé, com uma linha entre cada par de grupos

#### Scenario: O ato da missão fica junto do conteúdo

- **WHEN** a missão apresentada tem sondagem ou desafio de desbloqueio a responder
- **THEN** o que o Guerreiro(a) responde aparece no mesmo grupo do conteúdo, acima da primeira
  linha, e NEVER abaixo dela

#### Scenario: Grupo sem conteúdo não deixa linha na tela

- **WHEN** a missão é a última da trilha e não tem bibliografia, de modo que o grupo da próxima
  missão fica sem nada
- **THEN** aquele grupo não aparece e a sua linha não aparece com ele, sem sobrar separador
  entre dois grupos vizinhos

#### Scenario: A linha não é anunciada a quem usa leitor de tela

- **WHEN** a tela da missão é percorrida por leitor de tela
- **THEN** as linhas que separam os grupos não são anunciadas e não têm rótulo, e a fronteira
  entre grupos é dada pelos próprios títulos deles

#### Scenario: A trilha sem próxima missão mantém os grupos

- **WHEN** o Guerreiro(a) já desbloqueou todas as missões da trilha
- **THEN** a tela continua apresentando as atividades do encontro e o rodapé, cada um com a sua
  linha, em vez de encerrar na mensagem da trilha concluída

### Requirement: A bibliografia fica recolhida, e o crédito da trilha fica no rodapé

A App 01 SHALL apresentar a **bibliografia** da missão em bloco recolhível de resumo neutro,
no mesmo grupo da missão seguinte, e SHALL **omiti-la** quando a missão não tiver bibliografia.
O **crédito e a licença** da trilha NEVER SHALL aparecer no fluxo de leitura da missão: SHALL
ficar no **rodapé** da tela, recolhido e alcançável. (`RF-04-72`, `RF-05-11`, `RF-05-12`,
documento 15 §6.1)

#### Scenario: A bibliografia nasce fechada, com resumo neutro

- **WHEN** a missão apresentada tem bibliografia
- **THEN** ela aparece como bloco fechado de resumo neutro, junto da missão seguinte, e
  abre com título, capítulo e a disponibilidade no ponto de apoio ao ser acionada

#### Scenario: Missão sem bibliografia não apresenta o bloco

- **WHEN** a missão apresentada não tem bibliografia alguma
- **THEN** nenhum bloco de bibliografia aparece, nem fechado nem vazio

#### Scenario: O crédito sai do fluxo de leitura e vai ao rodapé

- **WHEN** o conteúdo de uma missão é apresentado
- **THEN** o crédito ao Mestre autor e a licença não aparecem logo abaixo do conteúdo, e sim no
  rodapé da tela, em bloco fechado que abre ao ser acionado

#### Scenario: A trilha concluída também credita a autoria

- **WHEN** o Guerreiro(a) alcança a trilha em que já desbloqueou todas as missões
- **THEN** o crédito ao Mestre autor e a licença continuam apresentados no rodapé daquela tela

### Requirement: O caminho ao catálogo de poderes aparece só onde é o único

A App 01 SHALL oferecer no rodapé da tela da missão o caminho ao **catálogo de poderes**
somente quando ele for o **único** caminho ao catálogo ali: o Guerreiro(a) inscrito em **uma**
trilha, que não alcança a lista de trilhas. Inscrito em **mais de uma**, a lista já alcança o
catálogo e o rodapé NEVER SHALL repetir o caminho. A aplicação NEVER SHALL deixar o
Guerreiro(a) sem caminho ao catálogo. (`RF-04-72`, `RF-04-74`, decisão do fundador de
2026-10-15)

#### Scenario: Com uma trilha inscrita, o rodapé oferece o catálogo

- **WHEN** o Guerreiro(a) inscrito em uma única trilha tem o percurso dela aberto, sem lista de
  trilhas no caminho
- **THEN** o rodapé oferece escolher outro poder, porque é o único caminho ao catálogo naquela
  tela

#### Scenario: Com mais de uma trilha, o rodapé não repete o caminho

- **WHEN** o Guerreiro(a) inscrito em duas trilhas ou mais tem o percurso de uma delas aberto
- **THEN** o rodapé não oferece escolher outro poder, e o caminho ao catálogo segue na
  lista das trilhas, alcançável por trocar de trilha

#### Scenario: Nenhuma inscrição fica sem caminho ao catálogo

- **WHEN** o Guerreiro(a) quer inscrever-se em outra trilha pelo aparelho do encontro, com
  qualquer número de inscrições já feitas
- **THEN** há sempre um caminho ao catálogo de poderes a partir da tela das trilhas e missões,
  cumprindo a inscrição sem teto
