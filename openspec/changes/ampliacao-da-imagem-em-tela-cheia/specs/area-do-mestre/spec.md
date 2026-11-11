# Spec Delta

## MODIFIED Requirements

### Requirement: A mídia exibida pela App 09 usa moldura de tamanho fixo

Toda imagem e todo vídeo que a App 09 busca do núcleo em bytes — o conteúdo da missão na
pré-visualização, a imagem da pergunta do quiz na pré-visualização e a imagem da pergunta na
edição do desafio de desbloqueio — SHALL ser exibidos numa moldura de **tamanho fixo**, igual
para os três casos, sem crescer além dela: a imagem ou o vídeo inteiro cabe dentro da moldura,
sem ser cortado para preenchê-la, e o espaço que sobrar fica em branco. (`RF-09-25`,
`RF-09-119`, decisão do fundador de 2026-09-17)

A **imagem** na moldura — nas três telas acima, no conteúdo exibido no cadastro da missão e na
comprovação em foto dos desbloqueios pendentes — SHALL ser um controle que, acionado por toque,
clique ou teclado, a abre **inteira, sem corte, no maior tamanho que a tela comporta**, sobre a
tela atual; fecha pelo botão **"Fechar"**, pela tecla `Esc` e pelo toque fora dela, devolvendo o
foco à imagem. O **vídeo** NEVER SHALL ganhar a ampliação. (`RF-09-25`, `RF-09-119`,
`RF-09-132`, decisão do fundador de 2026-11-11)

#### Scenario: Imagem grande cabe na moldura fixa, sem cortar

- **WHEN** o Mestre autor abre a pré-visualização de uma missão cujo conteúdo tem uma foto de
  alta resolução
- **THEN** a foto aparece inteira, dentro da moldura de tamanho fixo, sem estourar o layout

#### Scenario: Vídeo usa a mesma moldura da imagem

- **WHEN** o Mestre autor abre a pré-visualização de uma missão cujo conteúdo tem vídeo
- **THEN** o vídeo aparece na mesma moldura de tamanho fixo que a imagem usa

#### Scenario: Tocar na imagem a abre em tela cheia

- **WHEN** o Mestre toca numa imagem exibida em moldura fixa — conteúdo, pergunta ou
  comprovação em foto
- **THEN** a imagem abre inteira, sem corte, no maior tamanho que a tela comporta

#### Scenario: A imagem ampliada fecha e devolve o foco

- **WHEN** a imagem está ampliada e o Mestre aciona "Fechar", tecla `Esc` ou toca fora dela
- **THEN** a imagem ampliada fecha e o foco volta à imagem na moldura

#### Scenario: A moldura não amplia ao ser tocada

- **WHEN** o Mestre toca num vídeo exibido em moldura fixa
- **THEN** a moldura não amplia o vídeo; só os controles nativos dele respondem

#### Scenario: A imagem anexada na edição do desafio usa a mesma moldura

- **WHEN** o Mestre autor abre o quiz de uma pergunta que tem imagem anexada
- **THEN** a imagem aparece na mesma moldura de tamanho fixo que a pré-visualização usa

