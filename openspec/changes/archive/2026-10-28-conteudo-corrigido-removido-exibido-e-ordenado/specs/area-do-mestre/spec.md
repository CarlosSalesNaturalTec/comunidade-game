# Spec Delta

## MODIFIED Requirements

### Requirement: O Mestre escreve o conteúdo da missão

A App 09 SHALL oferecer ao Mestre autor, dentro da missão, a escrita do **conteúdo**: texto
formatado com imagens, link para vídeo hospedado fora da plataforma, e o envio de vídeo e de
arquivo de apoio. A aplicação SHALL apresentar o conteúdo já escrito na ordem declarada e
permitir reordená-lo, alterá-lo e removê-lo em **qualquer situação da
trilha**, publicada inclusive. Nenhum campo SHALL pedir código,
HTML, marcação ou configuração técnica, e NEVER SHALL oferecer a escrita em missão de trilha de
outro Mestre. A aplicação SHALL salvar o rascunho do texto automaticamente, de modo que queda de
rede NEVER SHALL perder o que já foi escrito. (`RF-09-14`, `RF-09-15`, `RF-09-24`,
`RF-09-123`, `RF-09-124`, `RF-09-126`, `RN-09-16`, PRD-09 §§6.3, 10)

#### Scenario: Mestre escreve o texto da missão

- **WHEN** o Mestre autor escreve o texto da missão e confirma
- **THEN** a aplicação grava o conteúdo no núcleo e passa a apresentá-lo na missão

#### Scenario: Mestre aponta vídeo hospedado fora

- **WHEN** o Mestre autor informa o endereço de um vídeo hospedado fora da plataforma
- **THEN** a aplicação grava o link como conteúdo, sem enviar arquivo algum

#### Scenario: Conteúdo de terceiro pede a fonte na própria tela

- **WHEN** o Mestre autor marca o conteúdo como de terceiro
- **THEN** a aplicação pede a fonte em campo de texto e não confirma sem ela

#### Scenario: Rascunho sobrevive à queda de rede

- **WHEN** a rede cai enquanto o Mestre autor escreve o texto da missão
- **THEN** o que foi escrito permanece, e a aplicação retoma dali quando a rede volta

#### Scenario: Nenhum campo pede jargão técnico

- **WHEN** o Mestre autor percorre a tela de conteúdo inteira
- **THEN** nenhum campo pede código, HTML, marcação nem configuração técnica

A aplicação SHALL apresentar o conteúdo já gravado toda vez que o Mestre autor volta à missão,
em sessão nova inclusive, e não apenas dentro da sessão em que foi escrito: a lista de
conteúdo NEVER SHALL aparecer vazia quando a missão tem conteúdo gravado. (`RF-09-14`,
`RF-09-15`)

#### Scenario: O conteúdo gravado reabre em sessão nova

- **WHEN** o Mestre autor anexou uma imagem como conteúdo da missão, saiu da aplicação e volta
  à mesma missão
- **THEN** a tela apresenta a imagem já gravada na lista de conteúdo, e não uma lista vazia

#### Scenario: Vários conteúdos de tipos diferentes reabrem juntos

- **WHEN** o Mestre autor declarou texto, imagem e vídeo na mesma missão e volta a ela em
  sessão nova
- **THEN** a tela apresenta os três, na ordem em que foram declarados

#### Scenario: Corrigir e remover alcançam a trilha publicada

- **WHEN** o Mestre autor corrige o texto de um conteúdo e remove outro, numa missão de trilha
  já publicada
- **THEN** a aplicação grava as duas operações, sem pedir que a trilha seja despublicada

## ADDED Requirements

### Requirement: O bloco Conteúdo identifica cada conteúdo que lista

A App 09 SHALL apresentar, para cada conteúdo da missão, um **rótulo** que o distinga dos
demais, e NEVER SHALL identificar um conteúdo apenas pelo valor do tipo, que repete entre
conteúdos diferentes e não permite escolher qual corrigir. A autoria SHALL aparecer em todo
conteúdo, e a fonte em todo conteúdo de terceiro. (`RF-09-125`, `RF-09-24`,
PRD-09 §§6.3, 10)

#### Scenario: Três conteúdos de texto se distinguem na lista

- **WHEN** a missão tem três conteúdos de texto e o Mestre autor abre o bloco Conteúdo
- **THEN** cada um traz as primeiras palavras do próprio corpo, e nenhuma linha diz apenas
  "texto"

#### Scenario: O conteúdo com arquivo é identificado pelo tipo e pelo tamanho

- **WHEN** a missão tem um conteúdo de imagem com o envio confirmado
- **THEN** a linha dele traz o tipo em palavras e o tamanho do arquivo — o núcleo guarda a
  referência, nunca o nome do arquivo —, e a do conteúdo sem envio confirmado diz que o envio
  está pendente

#### Scenario: O link é identificado pelo domínio

- **WHEN** a missão tem um conteúdo de link externo
- **THEN** a linha dele traz o domínio do endereço

#### Scenario: A fonte do terceiro aparece na linha

- **WHEN** um dos conteúdos da missão é declarado de terceiro
- **THEN** a linha dele traz a fonte declarada

### Requirement: O bloco Conteúdo exibe o conteúdo, e o arquivo só quando o Mestre pede

A App 09 SHALL **exibir** no bloco Conteúdo cada conteúdo já gravado: o texto e o link externo
de imediato, e a imagem, o vídeo e o arquivo de apoio **sob demanda**, por comando do Mestre
autor. A aplicação NEVER SHALL buscar os bytes de conteúdo algum antes desse comando. A mídia
exibida SHALL usar a moldura de tamanho fixo que a App 09 já aplica, e o conteúdo sem envio
confirmado SHALL ser dito **pendente**. (`RF-09-125`, `RN-09-46`, PRD-09 §§6.3, 10)

#### Scenario: O texto aparece sem pedir nada

- **WHEN** o Mestre autor abre o bloco Conteúdo de uma missão com conteúdo de texto
- **THEN** o texto é exibido, e nenhuma requisição de arquivo é feita

#### Scenario: Abrir a tela não busca arquivo algum

- **WHEN** o Mestre autor abre a trilha numa etapa cujas missões têm vídeo e imagem gravados
- **THEN** nenhuma requisição dos bytes desses arquivos é feita até ele pedir a exibição

#### Scenario: A imagem é exibida quando o Mestre pede

- **WHEN** o Mestre autor comanda a exibição de um conteúdo de imagem
- **THEN** a aplicação busca os bytes e os exibe na moldura de tamanho fixo

#### Scenario: Conteúdo sem envio confirmado é dito pendente

- **WHEN** o Mestre autor comanda a exibição de um conteúdo cujo envio nunca foi confirmado
- **THEN** a aplicação diz que o envio está pendente, e nada aparece quebrado

### Requirement: O bloco Conteúdo corrige, remove e move cada conteúdo

A App 09 SHALL oferecer, em cada conteúdo listado, o caminho de **corrigi-lo** — corpo,
endereço, autoria e fonte —, de **removê-lo** e de **movê-lo** para cima ou para baixo. A
correção SHALL reaproveitar a tela da escrita, com o rascunho automático guardado **por
conteúdo**. A aplicação NEVER SHALL oferecer a troca do tipo nem a do arquivo.
(`RF-09-123`, `RF-09-124`, `RF-09-126`, `RN-09-45`, `RN-09-16`, PRD-09 §§6.3, 10)

#### Scenario: O Mestre corrige o texto já gravado

- **WHEN** o Mestre autor comanda a correção de um conteúdo de texto e confirma o corpo novo
- **THEN** a aplicação grava a correção e passa a apresentar o corpo corrigido na lista

#### Scenario: O rascunho de uma edição não invade outra

- **WHEN** o Mestre autor começa a corrigir um conteúdo, sai sem confirmar e abre a correção de
  outro conteúdo da mesma missão
- **THEN** cada um retoma o próprio rascunho, e nenhum texto aparece no conteúdo errado

#### Scenario: O Mestre remove um conteúdo

- **WHEN** o Mestre autor comanda a remoção de um conteúdo
- **THEN** a aplicação o remove pelo núcleo e deixa de apresentá-lo na lista

#### Scenario: O Mestre move um conteúdo na lista

- **WHEN** o Mestre autor comanda subir um conteúdo que está em segundo lugar
- **THEN** a lista passa a apresentá-lo em primeiro, na ordem que o núcleo gravou

#### Scenario: Trocar o tipo é dito, não oferecido

- **WHEN** o Mestre autor abre a correção de um conteúdo de vídeo
- **THEN** a tela não oferece trocar o tipo nem o arquivo, e diz que para isso o caminho é
  remover e cadastrar outro

#### Scenario: A recusa do núcleo chega com o motivo

- **WHEN** a correção é recusada por deixar vazio o corpo de um conteúdo de texto
- **THEN** a tela apresenta o motivo que o núcleo declarou, e não uma falha genérica
