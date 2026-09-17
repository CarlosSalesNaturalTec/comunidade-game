## ADDED Requirements

### Requirement: A mídia exibida ao Guerreiro(a) usa moldura de tamanho fixo

Toda imagem e todo vídeo que a aplicação busca do núcleo em bytes — o conteúdo da missão e a
imagem da pergunta do desafio de desbloqueio — SHALL ser exibidos numa moldura de **tamanho
fixo**, igual para os dois casos, sem crescer além dela: a imagem ou o vídeo inteiro cabe
dentro da moldura, sem ser cortado para preenchê-la, e o espaço que sobrar fica em branco. A
moldura NEVER SHALL oferecer ampliação nem abrir a mídia em tamanho maior. (`RF-05-11`,
`RF-09-119`, decisão do fundador de 2026-09-17)

#### Scenario: Imagem grande do conteúdo cabe na moldura fixa, sem cortar

- **WHEN** o Guerreiro(a) abre uma missão cujo conteúdo tem uma foto de alta resolução
- **THEN** a foto aparece inteira, dentro da moldura de tamanho fixo, sem estourar o layout

#### Scenario: Vídeo do conteúdo usa a mesma moldura da imagem

- **WHEN** o Guerreiro(a) abre uma missão cujo conteúdo tem vídeo
- **THEN** o vídeo aparece na mesma moldura de tamanho fixo que a imagem usa

#### Scenario: A imagem da pergunta do desbloqueio usa a mesma moldura

- **WHEN** o Guerreiro(a) abre o desafio de desbloqueio de uma pergunta que tem imagem
- **THEN** a imagem aparece na mesma moldura de tamanho fixo que o conteúdo da missão usa

#### Scenario: A moldura não amplia ao ser tocada

- **WHEN** o Guerreiro(a) toca numa imagem ou num vídeo exibidos em moldura fixa
- **THEN** nada se amplia; a mídia permanece no mesmo tamanho
