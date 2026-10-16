# Spec Delta

## ADDED Requirements

### Requirement: O ato da missão só aparece depois do último conteúdo

No aparelho do encontro, a App 01 SHALL **ocultar** o ato da missão — a sondagem e o desafio
de desbloqueio — enquanto o Guerreiro(a) não alcançar o **último conteúdo** da missão, e SHALL
apresentá-lo ao alcançá-lo. Missão **sem conteúdo algum** SHALL apresentar o ato de imediato.
(`RF-04-73`, `RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-45`, documento 15 §6, decisão do
fundador de 2026-10-16)

#### Scenario: O desafio não aparece antes do último conteúdo

- **WHEN** o Guerreiro(a) abre uma missão de quatro conteúdos que tem desafio de desbloqueio, e
  está no primeiro deles
- **THEN** a tela apresenta o conteúdo e o controle de avançar, e o desafio de desbloqueio não
  aparece em lugar nenhum dela

#### Scenario: Alcançado o último conteúdo, o ato aparece

- **WHEN** o Guerreiro(a) avança até o último conteúdo daquela missão
- **THEN** o desafio de desbloqueio passa a ser apresentado, no mesmo grupo do conteúdo

#### Scenario: Missão sem conteúdo apresenta o ato de imediato

- **WHEN** a missão apresentada não tem conteúdo algum declarado
- **THEN** o ato dela é apresentado assim que a missão abre, sem nada a percorrer antes

#### Scenario: Missão de um conteúdo só apresenta o ato junto dele

- **WHEN** a missão tem um único conteúdo, que já é o último
- **THEN** o ato é apresentado junto desse conteúdo, assim que a missão abre

#### Scenario: A sondagem segue a mesma regra do desafio

- **WHEN** a missão de sondagem de uma trilha tem conteúdo a percorrer
- **THEN** a sondagem só é apresentada ao se alcançar o último conteúdo dela, como o desafio de
  desbloqueio

#### Scenario: A missão seguinte recomeça com o ato oculto

- **WHEN** o Guerreiro(a) desbloqueia a missão e a seguinte abre no aparelho, com conteúdo a
  percorrer
- **THEN** a tela abre no primeiro conteúdo da missão nova, e o ato dela está oculto

### Requirement: O conteúdo que não carrega nunca prende o ato da missão

Enquanto o conteúdo da missão está sendo buscado, a App 01 SHALL manter o ato **oculto**.
**Falhando** a busca, SHALL apresentá-lo junto do aviso de erro: o gate existe para garantir o
percurso do conteúdo, e conteúdo que não pode ser servido não tem o que guardar — mantê-lo
fechado deixaria a missão sem saída. (`RF-04-73`, `RF-05-13`, decisão do fundador de
2026-10-16)

#### Scenario: O conteúdo que falha libera o ato

- **WHEN** a busca do conteúdo da missão falha e a tela apresenta o aviso de que não foi
  possível carregá-lo
- **THEN** o ato da missão é apresentado junto do aviso, e o Guerreiro(a) pode responder

#### Scenario: O ato não pisca enquanto o conteúdo é buscado

- **WHEN** a missão abre e o conteúdo dela ainda está sendo buscado
- **THEN** a tela apresenta o aviso de carregamento e o ato permanece oculto, sem aparecer para
  sumir quando a lista de conteúdos chegar

## MODIFIED Requirements

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

- **WHEN** a missão apresentada tem sondagem ou desafio de desbloqueio a responder, e o
  Guerreiro(a) já alcançou o último conteúdo dela
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
