# Spec Delta

## ADDED Requirements

### Requirement: A mídia do conteúdo da missão na App 01 usa a moldura de tamanho fixo

Toda imagem e todo vídeo do conteúdo da missão que a App 01 exibe — na programação do encontro
e no percurso do Guerreiro(a), na missão e na pergunta do desafio de desbloqueio — SHALL ser
buscados **em bytes do núcleo** e exibidos na moldura de **tamanho fixo** do documento 15 §12,
inteiros e sem corte. A tela NEVER SHALL apresentar a referência do armazenamento no lugar da
mídia. (`RF-04-35`, `RF-04-72`, `RF-04-73`, decisão do fundador de 2026-09-17)

#### Scenario: A imagem da programação abre na moldura fixa

- **WHEN** a equipe alcança, na programação do encontro, um conteúdo de imagem
- **THEN** a imagem aparece inteira, dentro da moldura de tamanho fixo, buscada do núcleo

#### Scenario: O vídeo da programação usa a mesma moldura

- **WHEN** a equipe alcança, na programação do encontro, um conteúdo de vídeo
- **THEN** o vídeo aparece na mesma moldura de tamanho fixo que a imagem usa

#### Scenario: A imagem que não abre avisa, sem prender a sequência

- **WHEN** a busca da imagem do conteúdo falha
- **THEN** a moldura avisa que ela não abriu e o controle de avançar segue disponível

### Requirement: A imagem da moldura na App 01 abre em tela cheia ao toque

Toda imagem exibida na moldura fixa da App 01 SHALL ser um **controle**: acioná-lo por toque,
clique ou teclado SHALL abrir a imagem **inteira, sem corte, no maior tamanho que a tela
comporta**, sobre a tela atual. A imagem ampliada SHALL fechar pelo botão **"Fechar"**, pela
tecla `Esc` e pelo toque fora dela, devolvendo o foco à imagem que a abriu. Vídeo NEVER SHALL
ganhar a ampliação. (`RF-04-35`, `RF-04-73`, decisão do fundador de 2026-11-11)

#### Scenario: Tocar na imagem abre a imagem em tela cheia

- **WHEN** a equipe toca numa imagem do conteúdo da missão
- **THEN** a imagem abre inteira, sem corte, ocupando o maior tamanho que a tela comporta

#### Scenario: A imagem ampliada fecha pelo botão, pelo Esc e pelo toque fora

- **WHEN** a imagem está ampliada e quem usa aciona "Fechar", tecla `Esc` ou toca fora dela
- **THEN** a imagem ampliada fecha e o foco volta à imagem na moldura

#### Scenario: A imagem é alcançável pelo teclado e anunciada como ampliável

- **WHEN** quem usa leitor de tela ou teclado chega à imagem na moldura
- **THEN** ela é anunciada como controle que amplia a imagem e abre com `Enter` ou `Espaço`

#### Scenario: A ampliação não troca de conteúdo nem grava nada

- **WHEN** a equipe amplia e fecha a imagem de um conteúdo
- **THEN** a sequência segue no mesmo conteúdo, e nada é gravado nem enviado ao núcleo

#### Scenario: O vídeo não amplia pela moldura

- **WHEN** a equipe toca num vídeo exibido na moldura
- **THEN** só os controles nativos do vídeo respondem, e nenhuma ampliação se abre
