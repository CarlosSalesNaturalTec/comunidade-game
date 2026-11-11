# Spec Delta

## MODIFIED Requirements


### Requirement: A mídia exibida ao Guerreiro(a) usa moldura de tamanho fixo

Toda imagem e todo vídeo que a aplicação busca do núcleo em bytes — o conteúdo da missão e a
imagem da pergunta do desafio de desbloqueio — SHALL ser exibidos numa moldura de **tamanho
fixo**, igual para os dois casos, sem crescer além dela: a imagem ou o vídeo inteiro cabe
dentro da moldura, sem ser cortado para preenchê-la, e o espaço que sobrar fica em branco.
(`RF-05-11`, `RF-09-119`, decisão do fundador de 2026-09-17)

A **imagem** na moldura SHALL ser um controle que, acionado por toque, clique ou teclado, a abre
**inteira, sem corte, no maior tamanho que a tela comporta**, sobre a tela atual; fecha pelo
botão **"Fechar"**, pela tecla `Esc` e pelo toque fora dela, devolvendo o foco à imagem.
Ampliar NEVER SHALL trocar o item da sequência nem gravar coisa alguma, e o **vídeo** NEVER
SHALL ganhar a ampliação. (`RF-05-11`, `RF-05-13`, decisão do fundador de 2026-11-11)

Enquanto a mídia da vez está sendo buscada, a moldura SHALL **dizer que está carregando** e
NEVER SHALL apresentar a mídia de **outro** item nem o erro de outro item: alcançado um item
novo na sequência, a moldura SHALL partir do zero. Mídia obsoleta sob o item errado é
informação falsa, não espera. (`RF-05-11`, `RF-09-119`, decisão do fundador de 2026-10-16)

Enquanto a moldura carrega, os controles de **avançar e voltar** da sequência SHALL ficar
indisponíveis, para que a troca não se acumule sobre uma mídia que ainda não chegou. A trava
SHALL ceder quando a busca **falha**: mídia que não abriu NEVER SHALL prender quem percorre a
sequência, sob pena de a rede ruim virar beco sem saída. (decisão do fundador de 2026-10-16)

#### Scenario: Imagem grande do conteúdo cabe na moldura fixa, sem cortar

- **WHEN** o Guerreiro(a) abre uma missão cujo conteúdo tem uma foto de alta resolução
- **THEN** a foto aparece inteira, dentro da moldura de tamanho fixo, sem estourar o layout

#### Scenario: Vídeo do conteúdo usa a mesma moldura da imagem

- **WHEN** o Guerreiro(a) abre uma missão cujo conteúdo tem vídeo
- **THEN** o vídeo aparece na mesma moldura de tamanho fixo que a imagem usa

#### Scenario: A imagem da pergunta do desbloqueio usa a mesma moldura

- **WHEN** o Guerreiro(a) abre o desafio de desbloqueio de uma pergunta que tem imagem
- **THEN** a imagem aparece na mesma moldura de tamanho fixo que o conteúdo da missão usa

#### Scenario: Tocar na imagem a abre em tela cheia

- **WHEN** o Guerreiro(a) toca numa imagem do conteúdo da missão ou da pergunta do desbloqueio
- **THEN** a imagem abre inteira, sem corte, no maior tamanho que a tela comporta

#### Scenario: A imagem ampliada fecha e devolve o foco

- **WHEN** a imagem está ampliada e o Guerreiro(a) aciona "Fechar", tecla `Esc` ou toca fora
  dela
- **THEN** a imagem ampliada fecha, o foco volta à imagem na moldura e o item da sequência é o
  mesmo

#### Scenario: A moldura não amplia ao ser tocada

- **WHEN** o Guerreiro(a) toca num vídeo exibido em moldura fixa
- **THEN** a moldura não amplia o vídeo; só os controles nativos dele respondem

#### Scenario: A moldura diz que está carregando

- **WHEN** o Guerreiro(a) alcança um item cuja mídia ainda está sendo buscada
- **THEN** a moldura diz que está carregando, e avançar e voltar ficam indisponíveis

#### Scenario: A mídia do item anterior não fica na tela

- **WHEN** o Guerreiro(a) vai de um item com imagem direto para outro item com imagem
- **THEN** a imagem do item anterior desaparece de imediato, e a moldura carrega a do item
  alcançado

#### Scenario: O erro de um item não gruda no seguinte

- **WHEN** a mídia de um item não abre e o Guerreiro(a) avança para o item seguinte
- **THEN** o aviso de falha não acompanha o item novo, cuja mídia é buscada do zero

#### Scenario: Mídia que não abre libera a navegação

- **WHEN** a busca da mídia do item da vez falha
- **THEN** a tela avisa que ela não abriu e avançar e voltar voltam a estar disponíveis

