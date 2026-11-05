# Spec Delta

## ADDED Requirements

### Requirement: A camada comum entrega o visor da câmera

A camada comum SHALL entregar o **visor da câmera** usado por toda tela que abre a câmera para
reconhecer um rosto, nas Apps 01 e 05. O visor SHALL apresentar **apenas o fluxo ao vivo**:
nenhum quadro capturado aparece nele, antes ou depois de gerar o descritor. O visor NEVER SHALL
receber `MediaStream`, quadro ou pixel — ele **empresta um lugar** ao módulo de biometria, que é
quem anexa o vídeo. (`RF-05-95`, `RN-05-53`, `RN-04-34`, documento 99 §6 invariante 12)

#### Scenario: Uma aplicação apresenta o visor

- **WHEN** uma aplicação da plataforma abre a câmera para reconhecer um rosto
- **THEN** ela apresenta o visor da camada comum, e não um visor próprio

#### Scenario: O visor não recebe a imagem

- **WHEN** o visor é apresentado
- **THEN** ele recebe apenas o lugar onde o vídeo será anexado, e nenhum quadro, pixel ou fluxo
  passa por ele

#### Scenario: O visor vazio não ocupa a tela

- **WHEN** o visor está montado e nenhum vídeo foi anexado ainda
- **THEN** ele não aparece na tela e não reserva espaço

### Requirement: O visor espelha a imagem na horizontal

O visor SHALL espelhar o fluxo na horizontal, de modo que quem se move para a direita se veja ir
para a direita, como num espelho de verdade. O visor SHALL caber na tela do celular modesto, sem
que o vídeo imponha a sua dimensão própria ao resto da tela. (`RF-05-95`, documento 03 §3.2)

#### Scenario: Quem se move para a direita se vê ir para a direita

- **WHEN** a pessoa diante da câmera se move para um lado
- **THEN** a imagem no visor se move para o mesmo lado

#### Scenario: O visor não estoura a tela do celular

- **WHEN** o visor é apresentado num aparelho de tela estreita
- **THEN** ele se limita à largura disponível e a uma fração da altura, sem empurrar o resto da
  tela para fora

### Requirement: Quem usa o visor declara as frases do laço

As frases que o visor apresenta sobre o que o laço está vendo SHALL ser declaradas por **quem o
usa**, porque o público de cada tela é outro: a tela que um Mestre opera fala com quem opera, e a
entrada da App 05 fala com uma criança de 6 anos. A camada NEVER SHALL fixar uma redação única
para as duas. (`RF-05-95`, PRD-05 §10, PRD-04 §10)

#### Scenario: Duas telas, duas redações

- **WHEN** a tela que um adulto opera e a entrada da criança apresentam o mesmo estado do laço
- **THEN** cada uma apresenta a sua própria frase, pelo mesmo visor
