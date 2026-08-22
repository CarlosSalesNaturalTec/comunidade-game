## MODIFIED Requirements

### Requirement: Etiqueta ODS presa a uma trilha ou a uma missão, nunca as duas

O núcleo SHALL manter a etiqueta ODS com um **objetivo** de **1 a 18** e uma **meta** opcional em
texto livre (`4.7`, `13.3`), presa a **exatamente uma** trilha **ou** a **exatamente uma**
missão — nunca as duas ao mesmo tempo, nem nenhuma das duas. Uma trilha ou missão SHALL aceitar
**mais de uma** etiqueta. Só o **Mestre autor** da trilha declara a etiqueta, dela ou de uma
missão dela — **autoria estrita**, a mesma da publicação e da culminância: nem outro Mestre nem
o **Admin** declaram, e os dois SHALL receber **403**. Etiqueta com objetivo fora de 1 a 18, ou
sem trilha nem missão, ou com as duas, SHALL ser recusada com **422**. (`RF-01-40`, `RF-01-45`,
`RF-01-16`, `RF-09-92`, `RF-09-98`, 11 §2.1)

#### Scenario: Mestre autor etiqueta a trilha

- **WHEN** o Mestre autor declara uma etiqueta com objetivo 4 e meta "4.7" na própria trilha
- **THEN** o núcleo grava a etiqueta vinculada àquela trilha

#### Scenario: Mestre autor etiqueta uma missão da trilha

- **WHEN** o Mestre autor declara uma etiqueta em uma missão da própria trilha
- **THEN** o núcleo grava a etiqueta vinculada àquela missão, não à trilha

#### Scenario: Trilha aceita mais de uma etiqueta

- **WHEN** o Mestre autor declara uma segunda etiqueta, com objetivo diferente, na mesma trilha
- **THEN** o núcleo grava as duas etiquetas

#### Scenario: Etiqueta com objetivo fora da faixa é recusada

- **WHEN** chega uma etiqueta com objetivo 0 ou 19
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Etiqueta sem trilha nem missão é recusada

- **WHEN** chega uma etiqueta sem trilha e sem missão vinculada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Etiqueta com trilha e missão ao mesmo tempo é recusada

- **WHEN** chega uma etiqueta vinculada a uma trilha e a uma missão ao mesmo tempo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta declarar etiqueta nela ou em uma missão
  dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Admin é recusado

- **WHEN** um Admin tenta declarar etiqueta numa trilha de um Mestre ou numa missão dela
- **THEN** o núcleo responde 403 e nada é gravado, porque o Admin não edita a trilha de um
  Mestre

## ADDED Requirements

### Requirement: A declaração substitui o conjunto de etiquetas do alvo

O núcleo SHALL aceitar do Mestre autor a **lista completa** de etiquetas de uma trilha ou de
uma missão e **substituir** por ela o conjunto que o alvo tinha: as etiquetas anteriores do
alvo SHALL ser apagadas e as recebidas gravadas, na mesma operação. A operação SHALL ser
**idempotente** — a mesma lista enviada duas vezes deixa o alvo no mesmo estado. Lista **vazia**
SHALL deixar o alvo sem etiqueta alguma, situação legal no Ciclo 01 (`RF-09-93`).

A substituição SHALL ser **escopada ao alvo**: a substituição na trilha NEVER SHALL alcançar as
etiquetas das missões dela, e a substituição numa missão NEVER SHALL alcançar as da trilha — é
o que preserva a precedência da etiqueta própria da missão.

Recusada qualquer etiqueta da lista, o núcleo SHALL recusar a **operação inteira**: nada é
gravado e o conjunto anterior do alvo permanece intacto. (`RF-09-92`, `RF-09-98`, `RF-09-93`,
`RF-01-45`)

#### Scenario: A lista recebida substitui o conjunto anterior

- **WHEN** a trilha tem etiquetas de objetivos 11 e 4, e o Mestre autor envia a lista com os
  objetivos 4 e 13
- **THEN** a trilha passa a ter os objetivos 4 e 13, e o objetivo 11 deixa de existir nela

#### Scenario: Lista vazia deixa o alvo sem etiqueta

- **WHEN** o Mestre autor envia lista vazia para uma trilha etiquetada
- **THEN** a trilha fica sem etiqueta alguma, e nada é recusado por causa disso

#### Scenario: A substituição é idempotente

- **WHEN** o Mestre autor envia duas vezes a mesma lista para o mesmo alvo
- **THEN** o alvo fica com o mesmo conjunto que teria após o primeiro envio

#### Scenario: Substituir na trilha não toca as etiquetas das missões

- **WHEN** o Mestre autor substitui as etiquetas da trilha e uma missão dela tem etiqueta
  própria
- **THEN** a etiqueta própria da missão permanece, e continua prevalecendo para ela

#### Scenario: Substituir na missão não toca as etiquetas da trilha

- **WHEN** o Mestre autor substitui as etiquetas de uma missão
- **THEN** as etiquetas da trilha permanecem inalteradas

#### Scenario: Uma etiqueta inválida recusa a operação inteira

- **WHEN** a lista enviada traz um objetivo válido e um objetivo 19
- **THEN** o núcleo responde 422, nada é gravado e o conjunto anterior do alvo permanece

#### Scenario: A substituição não reprocessa pontuação

- **WHEN** o Mestre autor substitui as etiquetas de uma trilha que já tem registros creditados
- **THEN** nenhum ponto é recalculado, estornado ou creditado por causa da substituição

### Requirement: As etiquetas declaradas são legíveis na trilha e na missão

O núcleo SHALL devolver as etiquetas declaradas — objetivo e meta — junto da trilha e de cada
missão, tanto na leitura das **trilhas do próprio Mestre** quanto na leitura **pública** da
trilha publicada. A etiqueta apresentada em uma missão SHALL ser a **declarada nela**, sem
substituí-la pela da trilha na saída: a precedência resolve o vínculo, não a leitura da
autoria. (`RF-09-92`, `RF-09-98`, `RF-09-09`)

#### Scenario: O Mestre autor lê as etiquetas que declarou

- **WHEN** o Mestre autor lê as próprias trilhas
- **THEN** cada trilha traz as etiquetas dela e cada missão traz as etiquetas próprias dela

#### Scenario: A trilha pública traz os ODS que toca

- **WHEN** alguém lê uma trilha publicada
- **THEN** a trilha traz as etiquetas declaradas nela e nas missões dela

#### Scenario: Missão sem etiqueta própria sai sem etiqueta na leitura

- **WHEN** uma missão não tem etiqueta própria e a trilha tem
- **THEN** a missão sai sem etiqueta na leitura, e a etiqueta da trilha continua sendo a que
  prevalece nos vínculos dela

### Requirement: A cobertura de ODS da trilha é legível junto da trilha

O núcleo SHALL devolver, junto da trilha, a **cobertura de ODS resultante** dela — o conjunto
de objetivos distintos da trilha e das missões dela —, na leitura do Mestre autor e na leitura
pública. A cobertura SHALL carregar o **rótulo do ciclo** em que foi apurada e NEVER SHALL ser
apurada por Guerreiro(a). (`RF-09-94`, `RF-01-42`, `RN-01-24`)

#### Scenario: A cobertura soma a trilha e as missões dela

- **WHEN** a trilha tem etiqueta de objetivo 4 e uma missão dela tem etiqueta de objetivo 13
- **THEN** a cobertura devolvida junto da trilha traz os objetivos 4 e 13

#### Scenario: A cobertura não repete objetivo declarado duas vezes

- **WHEN** a trilha e uma missão dela têm etiqueta do mesmo objetivo 4
- **THEN** a cobertura traz o objetivo 4 uma única vez

#### Scenario: Trilha sem etiqueta tem cobertura vazia

- **WHEN** nem a trilha nem as missões dela têm etiqueta declarada
- **THEN** a cobertura devolvida é vazia, e nada é recusado por causa disso

#### Scenario: A cobertura carrega o rótulo do ciclo

- **WHEN** a cobertura da trilha é devolvida
- **THEN** ela vem acompanhada do rótulo do ciclo declarado na implantação
