## ADDED Requirements

### Requirement: A App 05 mostra as duas contas de ponto extra, separadas

A aplicação SHALL exibir ao Guerreiro(a) em sessão o **acumulado** e o **saldo disponível** de
pontos extras **separados e rotulados**, sem somá-los e sem confundi-los com o ponto regular. A
tela SHALL dizer, em linguagem simples, que o acumulado **só cresce** e que o trocável é o
**saldo disponível**. (`RF-05-82`, `RN-05-39`, `RN-05-40`, `RN-05-42`, PRD-05 §5.6)

#### Scenario: As duas contas aparecem distintas

- **WHEN** o Guerreiro(a) abre a carteira
- **THEN** vê o acumulado e o saldo disponível como dois números rotulados, nunca somados

#### Scenario: Ponto regular não entra na carteira

- **WHEN** a carteira é exibida
- **THEN** nenhum ponto regular é somado nem apresentado como trocável

#### Scenario: A carteira é só a própria

- **WHEN** o Guerreiro(a) abre a carteira
- **THEN** nenhuma conta de outra criança é exibida

### Requirement: A App 05 mostra o catálogo avulso e não troca nada

A aplicação SHALL exibir o **catálogo avulso da Comunidade Virtual** do Guerreiro(a), com o
**preço em pontos extras** e o **estoque** de cada item, e SHALL informar que a troca é feita
**presencialmente, com o Mestre, ao fim do encontro**. A aplicação NEVER SHALL oferecer troca
nem reserva de item — a execução é do App 01. (`RF-05-83`, `RF-05-86`, `RF-05-87`, PRD-05 §§3.2,
5.6)

#### Scenario: O catálogo abre com preço e estoque

- **WHEN** o Guerreiro(a) abre o catálogo avulso
- **THEN** vê os itens ativos da sua comunidade, cada um com preço em pontos extras e estoque

#### Scenario: Nenhum botão de troca ou reserva

- **WHEN** o catálogo é exibido
- **THEN** nenhuma ação de trocar ou reservar item é oferecida, e a tela explica que a troca
  acontece no encontro, com o Mestre

#### Scenario: Catálogo vazio não quebra a tela

- **WHEN** a comunidade ainda não tem item ativo cadastrado
- **THEN** a tela explica que ainda não há recompensa avulsa disponível, sem erro nem tela vazia

### Requirement: A App 05 mostra o histórico das próprias trocas

A aplicação SHALL exibir o histórico das trocas do Guerreiro(a), cada uma com o **item**, o
**preço cobrado** na data e a **data**. NEVER SHALL exibir valor em moedas nem em reais.
(`RF-05-88`, `RN-05-21`)

#### Scenario: O histórico traz item, preço e data

- **WHEN** o Guerreiro(a) abre o histórico de trocas
- **THEN** vê cada troca sua com item, preço cobrado e data

#### Scenario: O preço exibido é o cobrado na época

- **WHEN** a tabela de preços mudou depois de uma troca
- **THEN** o histórico continua mostrando o preço que foi cobrado naquela troca

#### Scenario: Nenhum custo em moedas ou reais

- **WHEN** o histórico é exibido
- **THEN** nenhum campo traz valor em moedas nem em reais

### Requirement: A App 05 avisa a recompensa conquistada e nunca a vende

A aplicação SHALL exibir as recompensas de marco que o Guerreiro(a) **conquistou**, dizendo em
linguagem simples que **a entrega é confirmada pelo Mestre** e mostrando, de cada uma, se já foi
entregue ou se aguarda. A aplicação NEVER SHALL oferecer nenhuma forma de **comprar** recompensa
de marco, com ponto de qualquer natureza. (`RF-05-45`, `RF-05-46`, `RN-05-07`, `RN-05-41`,
PRD-05 §5.6)

#### Scenario: Marco alcançado avisa a conquista

- **WHEN** o Guerreiro(a) alcança um marco que concede recompensa
- **THEN** a tela de conquistas mostra a recompensa e diz que o Mestre confirma a entrega

#### Scenario: A entrega feita aparece como feita

- **WHEN** o Mestre já confirmou a entrega
- **THEN** a mesma recompensa aparece como entregue, com a data

#### Scenario: Nenhuma tela vende recompensa de marco

- **WHEN** o Guerreiro(a) percorre carteira, catálogo e conquistas
- **THEN** em nenhuma delas há caminho de adquirir recompensa de marco com pontos

### Requirement: A App 05 mostra o estado do perfil público e não o altera

A aplicação SHALL exibir ao Guerreiro(a) o estado do **próprio perfil público** — se a
**divulgação foi autorizada** —, em linguagem simples e sem termo jurídico, dizendo que quem
decide é o responsável, na App 07. A aplicação NEVER SHALL oferecer caminho de conceder, recusar
ou revogar a autorização, e NEVER SHALL exibir qual responsável decidiu nem quando. (`RF-05-50`,
`RN-05-14`, `RN-05-21`, PRD-05 §3.2)

#### Scenario: O perfil diz se a divulgação está autorizada

- **WHEN** o Guerreiro(a) abre o próprio perfil
- **THEN** a tela diz se a divulgação foi autorizada, em linguagem de criança

#### Scenario: A criança não decide sobre a própria divulgação

- **WHEN** o perfil é exibido
- **THEN** nenhuma ação de autorizar ou revogar é oferecida, e a tela diz que quem decide é o
  responsável

#### Scenario: O perfil não expõe o ato do adulto

- **WHEN** o perfil é exibido
- **THEN** nenhum responsável, data ou motivo de decisão aparece

### Requirement: A App 05 mostra o ranking da turma com a própria posição sempre visível

A aplicação SHALL exibir o ranking da Comunidade Virtual do Guerreiro(a), **por trilha ou por
poder**, somente com **pontos regulares**, alcançando **a turma inteira** — inclusive quem não
tem divulgação autorizada. A **própria posição** SHALL estar sempre visível, ainda que fora da
faixa exibida. De cada colega a tela SHALL mostrar **apenas avatar, nick e posição**.
(`RF-05-52`, `RF-05-53`, `RF-05-84`, `RN-05-16`, `RN-05-18`, `RN-05-21`)

#### Scenario: A turma inteira aparece

- **WHEN** o Guerreiro(a) abre o ranking
- **THEN** vê os colegas da sua comunidade, inclusive os sem divulgação autorizada

#### Scenario: A própria posição nunca some

- **WHEN** o Guerreiro(a) está fora das primeiras posições exibidas
- **THEN** a tela mostra assim mesmo em que posição ele está

#### Scenario: A alternância entre trilha e poder mantém a leitura

- **WHEN** o Guerreiro(a) troca o recorte entre trilha e poder
- **THEN** o ranking é reordenado pelo ponto regular daquele recorte

#### Scenario: Nenhum dado pessoal de colega na tela

- **WHEN** o ranking é exibido
- **THEN** cada colega aparece só por avatar, nick e posição, sem imagem real nem nome civil

#### Scenario: Ponto extra não aparece no ranking

- **WHEN** o ranking é exibido
- **THEN** nenhuma posição considera ou mostra ponto extra
