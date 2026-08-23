## Purpose

A etiqueta ODS é o rótulo descritivo que liga trilha e missão aos Objetivos de Desenvolvimento
Sustentável — sem pesar no motor de pontuação — e a base da cobertura que a plataforma agrega.

## Requirements

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

### Requirement: A etiqueta de missão prevalece sobre a da trilha nos vínculos dela

O núcleo SHALL resolver, para qualquer vínculo que dependa da etiqueta de uma missão, a etiqueta
**declarada na própria missão** quando existir; na falta dela, a etiqueta da **trilha**. (`RF-01-
45`, 11 §2.1)

#### Scenario: Missão com etiqueta própria prevalece sobre a da trilha

- **WHEN** uma missão tem etiqueta própria diferente da etiqueta da trilha
- **THEN** o núcleo resolve, para aquela missão, a etiqueta própria dela

#### Scenario: Missão sem etiqueta própria herda a da trilha

- **WHEN** uma missão não tem etiqueta própria e a trilha tem etiqueta declarada
- **THEN** o núcleo resolve, para aquela missão, a etiqueta da trilha

### Requirement: A etiqueta não pontua e não é poder

O núcleo NEVER SHALL creditar ponto, certificar nível ou conceder badge a partir de uma etiqueta
ODS, e a etiqueta NEVER SHALL ser confundida com um poder do catálogo. (`RN-01-23`, 11 §2.1)

#### Scenario: Declarar etiqueta não credita pontuação

- **WHEN** o Mestre autor declara uma etiqueta em uma trilha ou missão
- **THEN** nenhum ponto, nível ou badge é concedido a ninguém por causa dela

### Requirement: Cobertura de ODS agrega por trilha, poder e comunidade, nunca por Guerreiro(a)

O núcleo SHALL agregar a cobertura de ODS — o conjunto de objetivos distintos etiquetados — por
**trilha**, por **poder** (a união das etiquetas das trilhas vinculadas a ele), por
**comunidade** e por **ciclo**. A cobertura NEVER SHALL ser exposta nem calculada por
Guerreiro(a) individual. (`RF-01-42`, `RN-01-24`, 11 §2.1)

A cobertura **por comunidade** SHALL ter **duas fontes**, somadas em união:

1. as etiquetas das **trilhas** em que há Guerreiro(a) daquela comunidade com **Resultado
   registrado**;
2. as etiquetas dos **desafios de coleta** com **série aberta** por Guerreiro(a) daquela
   comunidade — a etiqueta que o desafio herdou da missão, ou da trilha.

A segunda fonte SHALL valer ainda que nenhuma trilha da comunidade tenha Resultado registrado:
a comunidade que só coletou cobre o objetivo do desafio que coletou. O estado da série NEVER
SHALL alterar a cobertura — série ativa, interrompida e encerrada contam igual, porque a
cobertura mede **alcance declarado**, não continuidade. (`RF-08-26`, `RF-08-25`, `RN-08-22`,
documento 04 §4)

O **ciclo** é o quarto eixo, exigido por `RF-01-42` e sem o qual `RF-01-43` não se cumpre. Ele
SHALL ser o **rótulo declarado na implantação**, não uma entidade com período: `Ciclo` não é
entidade em nenhum PRD, e o calendário do Ciclo 01 segue pendente no documento 09 §1. Toda
agregação SHALL carregar o rótulo do ciclo em que foi apurada. (`RF-01-42`, `RF-01-43`,
invariantes 13 e 20 do documento 99 §6)

#### Scenario: Cobertura por trilha soma os objetivos da trilha e das missões dela

- **WHEN** a trilha tem etiqueta de objetivo 4 e uma missão dela tem etiqueta de objetivo 13
- **THEN** a cobertura da trilha inclui os objetivos 4 e 13

#### Scenario: Cobertura por poder soma as trilhas vinculadas a ele

- **WHEN** duas trilhas do mesmo poder têm etiquetas de objetivos diferentes
- **THEN** a cobertura do poder inclui os dois objetivos

#### Scenario: Cobertura por comunidade soma as trilhas em curso na comunidade

- **WHEN** um Guerreiro(a) de uma comunidade tem Resultado registrado numa trilha etiquetada
- **THEN** a cobertura daquela comunidade inclui o objetivo da trilha

#### Scenario: Cobertura por comunidade soma os desafios de coleta com série aberta

- **WHEN** um Guerreiro(a) de uma comunidade abre série sobre um desafio de coleta cuja
  etiqueta herdada é o objetivo 11
- **THEN** a cobertura daquela comunidade inclui o objetivo 11

#### Scenario: Comunidade que só coletou cobre o objetivo do desafio

- **WHEN** uma comunidade não tem nenhum Resultado registrado e tem uma série aberta sobre
  desafio etiquetado
- **THEN** a cobertura daquela comunidade traz o objetivo do desafio, e não fica vazia

#### Scenario: O estado da série não altera a cobertura

- **WHEN** a única série de um desafio etiquetado na comunidade está interrompida ou encerrada
- **THEN** a cobertura daquela comunidade continua incluindo o objetivo do desafio

#### Scenario: Cobertura nunca é calculada por Guerreiro(a)

- **WHEN** se procura no núcleo uma função que agregue cobertura de ODS por Guerreiro(a)
- **THEN** nenhuma existe: as agregações são por trilha, poder, comunidade e ciclo

#### Scenario: Toda agregação carrega o rótulo do ciclo

- **WHEN** a cobertura é apurada por qualquer um dos eixos
- **THEN** o resultado carrega o rótulo do ciclo declarado na implantação

### Requirement: O desafio de coleta herda a etiqueta ODS da missão, ou da trilha

O núcleo SHALL resolver a etiqueta ODS do desafio de coleta pela etiqueta declarada na **missão**
a que ele se vincula e, na falta dela, pela etiqueta da **trilha** — a mesma resolução que já vale
para qualquer vínculo que dependa da etiqueta de uma missão. A herança SHALL ser **derivada**, não
declarada: o Mestre NEVER SHALL declarar etiqueta própria no desafio, e a etiqueta do desafio
SHALL acompanhar a da missão ou da trilha quando ela mudar. Missão e trilha ambas sem etiqueta
SHALL produzir desafio **sem etiqueta**, situação normal no Ciclo 01, em que a etiqueta ainda não
é obrigatória. (`RF-08-25`, `RF-01-41`, `RN-08-21`, 11 §2.1)

#### Scenario: Desafio herda a etiqueta da missão que o criou

- **WHEN** a missão a que o desafio se vincula tem etiqueta própria de objetivo 13, e a trilha tem
  etiqueta de objetivo 4
- **THEN** o núcleo resolve, para aquele desafio, o objetivo 13

#### Scenario: Desafio recua para a etiqueta da trilha

- **WHEN** a missão a que o desafio se vincula não tem etiqueta própria e a trilha tem etiqueta de
  objetivo 4
- **THEN** o núcleo resolve, para aquele desafio, o objetivo 4

#### Scenario: Sem etiqueta na missão nem na trilha, o desafio fica sem etiqueta

- **WHEN** nem a missão nem a trilha têm etiqueta declarada
- **THEN** o desafio é criado sem etiqueta, e nada é recusado por causa disso

#### Scenario: A etiqueta do desafio não é declarada pelo Mestre

- **WHEN** chega um desafio de coleta com etiqueta ODS declarada nele
- **THEN** o núcleo responde 422, porque a etiqueta do desafio é derivada da missão ou da trilha

#### Scenario: Mudar a etiqueta da missão muda a do desafio

- **WHEN** o Mestre autor troca a etiqueta da missão depois de o desafio já existir
- **THEN** o desafio passa a resolver a etiqueta nova, sem alteração no próprio desafio

### Requirement: A etiqueta herdada pelo desafio não altera pontuação, cadência nem validade

O núcleo NEVER SHALL usar a etiqueta ODS do desafio de coleta para creditar ou negar ponto,
alterar a cadência declarada no desafio ou decidir a validade de um registro. A etiqueta é
**descritiva**: serve à cobertura agregada, e a mudança dela NEVER SHALL reprocessar pontuação
alguma. (`RN-08-21`, `RN-01-23`, 11 §2.1)

#### Scenario: Desafio etiquetado pontua igual ao não etiquetado

- **WHEN** dois desafios de coleta idênticos, um etiquetado e outro não, recebem o mesmo registro
  válido
- **THEN** os dois creditam exatamente o mesmo valor

#### Scenario: Trocar a etiqueta não reprocessa pontuação

- **WHEN** a etiqueta da trilha de um desafio muda depois de já haver registros creditados
- **THEN** nenhum ponto é recalculado, estornado ou creditado por causa da troca

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
