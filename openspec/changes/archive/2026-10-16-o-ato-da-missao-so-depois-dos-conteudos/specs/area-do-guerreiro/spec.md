# Spec Delta

## ADDED Requirements

### Requirement: O ato da missão só aparece depois do último conteúdo

A App 05 SHALL **ocultar** o ato da missão — a sondagem e o desafio de desbloqueio — enquanto
o Guerreiro(a) não alcançar o **último conteúdo** da missão, e SHALL apresentá-lo ao
alcançá-lo. Missão **sem conteúdo algum** SHALL apresentar o ato de imediato. A **entrega da
produção** NEVER SHALL ser alcançada por esta regra. (`RF-05-11`, `RF-05-13`, `RF-05-14`,
`RF-05-89`, `RN-05-45`, documento 15 §6, decisão do fundador de 2026-10-16)

#### Scenario: O desafio não aparece antes do último conteúdo

- **WHEN** o Guerreiro(a) abre uma missão de quatro conteúdos que tem desafio de desbloqueio, e
  está no primeiro deles
- **THEN** a tela apresenta o conteúdo e o controle de avançar, e o desafio de desbloqueio não
  aparece em lugar nenhum dela

#### Scenario: Alcançado o último conteúdo, o ato aparece

- **WHEN** o Guerreiro(a) avança até o último conteúdo daquela missão
- **THEN** o desafio de desbloqueio passa a ser apresentado, no mesmo grupo do conteúdo

#### Scenario: Missão sem conteúdo apresenta o ato de imediato

- **WHEN** a missão aberta não tem conteúdo algum declarado
- **THEN** o ato dela é apresentado assim que a missão abre, sem nada a percorrer antes

#### Scenario: Missão de um conteúdo só apresenta o ato junto dele

- **WHEN** a missão tem um único conteúdo, que já é o último
- **THEN** o ato é apresentado junto desse conteúdo, assim que a missão abre

#### Scenario: A sondagem que abre a trilha segue a mesma regra

- **WHEN** o Guerreiro(a) se inscreve numa trilha cuja missão de sondagem tem conteúdo a
  percorrer
- **THEN** a sondagem só é apresentada ao se alcançar o último conteúdo dela

#### Scenario: A entrega da produção não depende do percurso do conteúdo

- **WHEN** o Guerreiro(a) abre uma missão **já desbloqueada** que oferece a entrega da produção
- **THEN** a entrega é apresentada como sempre foi, em qualquer conteúdo da missão

#### Scenario: A missão seguinte recomeça com o ato oculto

- **WHEN** o Guerreiro(a) desbloqueia a missão e a seguinte abre no guia, com conteúdo a
  percorrer
- **THEN** a tela abre no primeiro conteúdo da missão nova, e o ato dela está oculto

### Requirement: O conteúdo que não carrega nunca prende o ato da missão

Enquanto o conteúdo da missão está sendo buscado, a App 05 SHALL manter o ato **oculto**.
**Falhando** a busca, SHALL apresentá-lo junto do aviso de erro: o gate existe para garantir o
percurso do conteúdo, e conteúdo que não pode ser servido não tem o que guardar — mantê-lo
fechado deixaria a missão sem saída. (`RF-05-11`, `RF-05-13`, decisão do fundador de
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

- **WHEN** a missão aberta tem entrega da produção, ou tem sondagem ou desafio de desbloqueio
  com o último conteúdo já alcançado
- **THEN** o que o Guerreiro(a) responde ou entrega aparece no mesmo grupo do conteúdo, acima
  da primeira linha

#### Scenario: Grupo sem conteúdo não deixa linha na tela

- **WHEN** a missão é a última da trilha e não tem bibliografia
- **THEN** o grupo da próxima missão não aparece, e a sua linha não aparece com ele

#### Scenario: O guia não oferece o catálogo de poderes

- **WHEN** o Guerreiro(a) tem o guia da trilha aberto
- **THEN** o rodapé não oferece escolher outro poder, porque a tela de trocar de trilha já
  alcança o catálogo
