# customizacao-do-kit Specification

## Purpose
A nova customização do kit recebido como recompensa de missão: quando ela se abre, como o
Guerreiro(a) a registra, como o Mestre da aula a julga ao vivo e o que a aprovação rende — o
ponto extra e o item do acervo.

## Requirements

### Requirement: A customização abre só depois do prático que apresenta o kit

O núcleo SHALL abrir a customização de um kit para o Guerreiro(a) **apenas** quando as duas
condições valem juntas: ele **recebeu** aquela recompensa de marco — há entrega registrada para
ele — **e** tem **aprovado** (julgado cumpriu) o desafio prático de uma missão que **declara**
aquela recompensa como kit apresentado. A comprovação desse prático é o **primeiro registro** do
kit. Kit recebido sem prático declarante aprovado NEVER SHALL aceitar registro de customização,
e a recusa SHALL ser **422** dizendo que a customização ainda não abriu. (`RF-01-84`,
`RF-09-141`, documento 11 §5)

#### Scenario: Kit recebido e prático aprovado abrem a customização

- **WHEN** o Guerreiro(a) recebeu o kit e o Mestre autor julgou que ele cumpriu o prático que
  declara aquele kit
- **THEN** o núcleo aceita registro de customização daquele kit

#### Scenario: Prático ainda não aprovado mantém a customização fechada

- **WHEN** o Guerreiro(a) recebeu o kit, mas o prático que o declara ainda aguarda julgamento ou
  foi julgado não cumprido
- **THEN** o núcleo recusa o registro com **422**, dizendo que a customização ainda não abriu

#### Scenario: Kit que nenhum prático declara não abre

- **WHEN** o Guerreiro(a) recebeu uma recompensa de marco que nenhum prático declara como kit
- **THEN** o núcleo recusa o registro de customização dela com **422**

#### Scenario: Recompensa que ele não recebeu não abre

- **WHEN** o Guerreiro(a) tenta registrar customização de uma recompensa que não lhe foi entregue
- **THEN** o núcleo recusa com **422**, e nada é gravado

### Requirement: O registro de customização traz a descrição e a mídia só do kit

O registro de customização SHALL trazer a **descrição** do que foi customizado, em texto — a
fala chega já transcrita no aparelho —, obrigatória e não em branco, e a **mídia** em **imagem ou
vídeo**, que entra pela **sessão de envio retomável** já usada pela comprovação do prático, com o
teto do tipo dela. O registro só fica **pronto para julgamento** quando o envio é confirmado.
Formato fora de imagem e vídeo SHALL ser recusado com **422**. Quem registra é o **próprio
Guerreiro(a)** em sessão, em casa ou no aparelho do encontro, ou o **Mestre da aula**, que
captura no encontro em nome do Guerreiro(a) com presença registrada naquela aula. O critério
"só o kit, sem rosto" é conferido pelo Mestre ao julgar, nunca pelo núcleo. (`RF-01-84`,
`RF-05-102`, `RF-04-80`, `RF-04-82`, documento 11 §5)

#### Scenario: O Guerreiro(a) registra em casa

- **WHEN** o Guerreiro(a) em sessão registra a customização de um kit aberto, com descrição, e
  conclui o envio de uma foto
- **THEN** o núcleo grava o registro pendente, pronto para o Mestre da aula julgar

#### Scenario: Descrição em branco é recusada

- **WHEN** o registro chega sem descrição, ou com ela só em espaços
- **THEN** o núcleo responde **422** nomeando o campo, e nada é gravado

#### Scenario: Formato que não é imagem nem vídeo é recusado

- **WHEN** o envio da mídia do registro declara um arquivo de áudio
- **THEN** o núcleo responde **422** dizendo que a customização aceita foto ou vídeo

#### Scenario: O Mestre da aula captura na hora

- **WHEN** o Mestre da aula registra, no encontro, a customização de um Guerreiro(a) com presença
  naquela aula, com a descrição dele e a foto tirada ali
- **THEN** o núcleo grava o registro pendente em nome do Guerreiro(a), com o Mestre como autor
  da escrita

#### Scenario: Outro Guerreiro(a) não registra por ele

- **WHEN** um Guerreiro(a) tenta registrar customização em nome de outro
- **THEN** o núcleo responde **403**, e nada é gravado

### Requirement: Um registro pendente por kit

Cada kit de cada Guerreiro(a) SHALL ter **no máximo um** registro de customização **pendente**.
Registrar de novo com um pendente aberto SHALL ser recusado com **422**, dizendo que há registro
aguardando o Mestre. Registro **reprovado**, **cancelado** ou **expirado** NEVER SHALL impedir
registro novo: **reenviar** é registrar de novo, e o reprovado permanece com o motivo, para a
criança ler por que não passou. (`RF-01-84`, `RF-05-103`)

#### Scenario: Segundo pendente do mesmo kit é recusado

- **WHEN** o Guerreiro(a) tem registro pendente de um kit e tenta registrar outro do mesmo kit
- **THEN** o núcleo responde **422**, e o pendente anterior permanece

#### Scenario: O reprovado permite registro novo

- **WHEN** o registro do Guerreiro(a) foi reprovado e ele registra outra customização do kit
- **THEN** o núcleo grava o registro novo, e o reprovado segue com o motivo

### Requirement: O Guerreiro(a) acompanha os próprios registros e cancela o pendente

O núcleo SHALL devolver ao **Guerreiro(a) em sessão**, numa rota sem identificador de persona,
os **kits cuja customização está aberta** — cada um com o último registro aprovado, a começar
pela comprovação do prático — e os **registros** dele, cada um com a **situação** — pendente,
aprovado, reprovado, cancelado ou expirado — e, no reprovado, o **motivo**. Ele SHALL poder
**cancelar** o próprio registro **pendente**; registro já julgado, cancelado ou expirado NEVER
SHALL ser cancelado, e a recusa é **422**. (`RF-05-103`, `RF-01-86`)

#### Scenario: O Guerreiro(a) lê os kits abertos e os registros

- **WHEN** o Guerreiro(a) em sessão consulta as suas customizações
- **THEN** o núcleo devolve os kits abertos, com o último registro aprovado, e os registros dele
  com a situação e, no reprovado, o motivo

#### Scenario: O Guerreiro(a) cancela o pendente

- **WHEN** o Guerreiro(a) cancela o próprio registro pendente
- **THEN** o registro passa a cancelado e o kit volta a aceitar registro novo

#### Scenario: Registro julgado não se cancela

- **WHEN** o Guerreiro(a) tenta cancelar um registro já aprovado
- **THEN** o núcleo responde **422**, e o registro segue aprovado

### Requirement: O Mestre da aula julga a customização no encontro

O julgamento SHALL ser ato de **Mestre vinculado à comunidade da aula** informada, sobre registro
**pendente** com a mídia confirmada, de Guerreiro(a) com **presença registrada e não anulada**
naquela aula. Ele SHALL ter dois desfechos: **aprovado**, que credita **1 ponto extra** ao
Guerreiro(a) e leva o registro ao **acervo**, na trilha da recompensa, com a descrição como
título; e **reprovado**, que exige **motivo** em linguagem simples, lido pelo Guerreiro(a).
Persona que não é Mestre, ou Mestre de outra comunidade, SHALL receber **403**; Guerreiro(a) sem
presença na aula, registro sem mídia confirmada ou já julgado SHALL ser recusado com **422**. A
aprovação SHALL obedecer à regra de uma pontuação por bem e por encontro. (`RF-01-85`,
`RF-04-82`, `RF-04-83`, `RN-01-66`)

#### Scenario: Aprovado credita 1 extra e entra no acervo

- **WHEN** o Mestre da aula aprova o registro pendente de um Guerreiro(a) presente
- **THEN** o núcleo credita 1 ponto extra no acumulado e no saldo disponível dele, nenhum ponto
  regular, e o registro passa a aprovado, como item do acervo

#### Scenario: Reprovado sem motivo é recusado

- **WHEN** o Mestre da aula reprova um registro sem motivo
- **THEN** o núcleo responde **422** nomeando o motivo, e o registro segue pendente

#### Scenario: Guerreiro(a) sem presença na aula não é julgado

- **WHEN** o Mestre julga, numa aula, o registro de Guerreiro(a) sem presença registrada nela
- **THEN** o núcleo responde **422**, e o registro segue pendente

#### Scenario: Mestre de outra comunidade não julga

- **WHEN** um Mestre informa uma aula de comunidade a que ele não está vinculado
- **THEN** o núcleo responde **403**, e nada muda

#### Scenario: Registro julgado não se julga de novo

- **WHEN** o Mestre tenta julgar um registro já aprovado ou reprovado
- **THEN** o núcleo responde **422**, e nenhum ponto é creditado de novo

### Requirement: A mídia da customização é servida a quem pode vê-la

O núcleo SHALL servir os bytes da mídia do registro de customização ao **próprio Guerreiro(a)**
e a **Mestre vinculado à comunidade** dele, que é quem julga no encontro. Qualquer outra persona
SHALL receber **403**. A leitura pública segue o portão do acervo público, na capability
`leitura-publica-da-vitrine`. (`RF-01-84`, `RF-04-81`)

#### Scenario: O Mestre da comunidade vê a mídia

- **WHEN** um Mestre vinculado à comunidade do Guerreiro(a) pede a mídia de um registro dele
- **THEN** o núcleo devolve os bytes, com o tipo do arquivo declarado

#### Scenario: Outro Guerreiro(a) não vê a mídia

- **WHEN** um Guerreiro(a) pede a mídia do registro de outro
- **THEN** o núcleo responde **403**, e nada é servido
