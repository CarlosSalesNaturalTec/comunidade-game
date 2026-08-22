## MODIFIED Requirements

### Requirement: A trilha tem situação de rascunho ou publicada

O núcleo SHALL manter a situação da trilha entre **rascunho**, **publicada** e
**despublicada** — três valores, conforme o PRD-09 §8 e a decisão do fundador de 2026-08-22. A
trilha em rascunho SHALL ser visível apenas ao Mestre autor e a Admin, e NEVER SHALL aparecer
em consulta pública. A trilha **despublicada** SHALL ser editável pelo Mestre autor como se
fosse rascunho, sem que a situação dela vire `rascunho`, e NEVER SHALL aparecer em consulta
pública. (`RF-01-20`, `RF-09-04`, `RF-09-11`, PRD-01 §8, PRD-09 §8)

#### Scenario: Rascunho não aparece a quem não é o autor

- **WHEN** uma persona que não é o Mestre autor nem Admin consulta as trilhas
- **THEN** as trilhas em rascunho não aparecem no resultado

#### Scenario: O Mestre autor vê o próprio rascunho

- **WHEN** o Mestre autor consulta as suas trilhas
- **THEN** as trilhas dele em rascunho aparecem no resultado

#### Scenario: Despublicada não aparece em consulta pública

- **WHEN** uma consulta pública alcança uma trilha despublicada
- **THEN** a trilha não é devolvida

#### Scenario: O Mestre autor edita a trilha despublicada

- **WHEN** o Mestre autor acrescenta ou altera missão de uma trilha despublicada
- **THEN** o núcleo aceita a escrita e a situação permanece despublicada

## ADDED Requirements

### Requirement: A publicação da trilha confere três travas e nenhuma outra

O núcleo SHALL publicar a trilha a pedido do **Mestre autor**, sem aprovação prévia de Admin
nem de outro Mestre, conferindo antes de qualquer escrita: **missão de sondagem** declarada,
ao menos **um desafio de coleta de dados reais** em alguma missão da trilha, e **culminância**
declarada. Faltando qualquer uma, o núcleo SHALL responder **422** nomeando **todas** as que
faltam, e a situação SHALL permanecer inalterada. O lastro de recompensa de marco NEVER SHALL
ser conferido na publicação. Pedido de publicação por Mestre que não é o autor SHALL responder
**403**. (`RF-09-05`, `RF-09-06`, `RF-09-07`, `RF-09-08`, `RF-09-82`, `RN-09-01`, `RN-09-02`,
`RN-09-03`, `RN-09-27`, `RN-09-29`, invariante 5)

#### Scenario: Trilha completa é publicada pelo autor

- **WHEN** o Mestre autor publica trilha que tem sondagem, desafio de coleta e culminância
- **THEN** o núcleo grava a situação publicada e devolve a trilha

#### Scenario: Trilha sem culminância é recusada

- **WHEN** o Mestre autor publica trilha com sondagem e desafio de coleta, e sem culminância
- **THEN** o núcleo responde 422 dizendo que falta a culminância, e a trilha segue como estava

#### Scenario: Trilha sem desafio de coleta é recusada

- **WHEN** o Mestre autor publica trilha com sondagem e culminância, e sem desafio de coleta
- **THEN** o núcleo responde 422 dizendo que falta o desafio de coleta

#### Scenario: Trilha sem missão de sondagem é recusada

- **WHEN** o Mestre autor publica trilha com desafio de coleta e culminância, e sem sondagem
- **THEN** o núcleo responde 422 dizendo que falta a missão de sondagem

#### Scenario: A recusa nomeia todas as travas que faltam

- **WHEN** o Mestre autor publica trilha à qual faltam as três
- **THEN** a recusa nomeia as três, e não apenas a primeira encontrada

#### Scenario: Recompensa de marco sem lastro não impede a publicação

- **WHEN** o Mestre autor publica trilha cujo marco promete recompensa sem lastro
- **THEN** o núcleo publica a trilha, porque o lastro é conferido na entrega

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor pede a publicação da trilha
- **THEN** o núcleo responde 403 e a situação permanece inalterada

### Requirement: A trilha publicada declara a licença e credita o Mestre autor

O núcleo SHALL entregar a trilha publicada em leitura **pública**, com a licença **CC BY-SA**
do conteúdo e o crédito ao **Mestre autor**. A leitura pública SHALL servir somente trilha na
situação publicada: rascunho e despublicada SHALL responder como não encontrada.
(`RF-09-09`, `RN-09-05`, PRD-09 §9)

#### Scenario: Leitura pública da trilha publicada

- **WHEN** a trilha publicada é consultada na rota pública
- **THEN** o núcleo devolve a trilha com a licença CC BY-SA e o crédito ao Mestre autor

#### Scenario: Rascunho não é servido na rota pública

- **WHEN** uma trilha em rascunho é consultada na rota pública
- **THEN** o núcleo responde como não encontrada

#### Scenario: Despublicada não é servida na rota pública

- **WHEN** uma trilha despublicada é consultada na rota pública
- **THEN** o núcleo responde como não encontrada

### Requirement: Só o Admin despublica, sempre com motivo, e o autor lê o motivo

O núcleo SHALL permitir que **somente Admin** despublique trilha publicada, **sempre com
motivo** — pedido sem motivo SHALL responder 422 e pedido de Mestre SHALL responder **403**. A
despublicação SHALL gravar, junto da situação, o **motivo**, o **autor** do ato, o **papel**
dele e o **momento**, e o núcleo SHALL entregar o motivo ao **Mestre autor** na leitura das
trilhas dele. Despublicar NEVER SHALL alterar missão, atividade, resultado, presença ou
pontuação já gravados: o percurso já realizado pelos Guerreiros e Guerreiras permanece
íntegro. (`RF-09-10`, `RF-09-11`, `RN-09-01`)

#### Scenario: Admin despublica com motivo

- **WHEN** um Admin despublica trilha publicada informando o motivo
- **THEN** o núcleo grava a situação despublicada com motivo, autor, papel e momento

#### Scenario: Despublicação sem motivo é recusada

- **WHEN** um Admin despublica sem informar motivo
- **THEN** o núcleo responde 422 e a trilha segue publicada

#### Scenario: Mestre não despublica

- **WHEN** o Mestre autor pede a despublicação da própria trilha
- **THEN** o núcleo responde 403 e a trilha segue publicada

#### Scenario: O Mestre autor lê o motivo

- **WHEN** o Mestre autor consulta as trilhas dele depois de uma despublicação
- **THEN** o motivo registrado pelo Admin vem junto da trilha despublicada

#### Scenario: O percurso já realizado permanece

- **WHEN** uma trilha com resultados e presenças já gravados é despublicada
- **THEN** nenhum resultado, presença ou ponto é alterado ou removido

#### Scenario: Trilha em rascunho não é despublicável

- **WHEN** um Admin pede a despublicação de trilha em rascunho
- **THEN** o núcleo responde 422 e a situação permanece rascunho

### Requirement: O Mestre autor republica a trilha despublicada pelas mesmas travas

O núcleo SHALL aceitar do **Mestre autor** a publicação de trilha na situação
**despublicada**, conferindo as **mesmas três travas** da primeira publicação, sem aprovação
de Admin. A republicação SHALL limpar o motivo da despublicação e gravar a nova procedência da
situação. (`RF-09-05`, `RF-09-11`, `RN-09-01`, decisão do fundador de 2026-08-22)

#### Scenario: Autor republica a trilha corrigida

- **WHEN** o Mestre autor publica trilha despublicada que atende às três travas
- **THEN** o núcleo grava a situação publicada e o motivo da despublicação deixa de acompanhá-la

#### Scenario: A republicação confere as travas de novo

- **WHEN** o Mestre autor publica trilha despublicada de que a culminância foi removida
- **THEN** o núcleo responde 422 e a trilha segue despublicada

#### Scenario: Trilha já publicada não republica

- **WHEN** o Mestre autor pede a publicação de trilha que já está publicada
- **THEN** o núcleo responde 422 e a situação permanece publicada
