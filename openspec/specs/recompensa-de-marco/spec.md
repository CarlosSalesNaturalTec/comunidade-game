## Purpose

A recompensa que o Guerreiro(a) **conquista** ao alcançar um marco da trilha — o livro da linha
Alpha, a camisa e o kit em MDF —, da declaração que o Mestre autor faz na trilha até a entrega
confirmada no encontro, que dá **baixa definitiva** no livro-razão e nunca custa ponto algum.

## Requirements

### Requirement: O Mestre autor declara qual marco concede qual recompensa

O núcleo SHALL permitir que o **Mestre autor da trilha** declare, para um marco dela, qual tipo
de recurso é concedido como recompensa e em que **quantidade**. Só o Mestre autor SHALL escrever
a recompensa de marco da sua trilha, como já vale para todo o restante dela.

O marco SHALL ser uma **missão** da trilha — o marco de uso corrente do documento 02 §8.1, e por
onde saem a camisa, o livro e o kit. As outras três espécies que o documento 02 §8.1 admite —
etapa, batalha e culminância — NÃO SHALL ser aceitas enquanto o núcleo não puder verificar que
foram alcançadas: `Batalha` é do PRD-10 e `Culminancia`, do PRD-09, e a etapa do ciclo ainda não
é atributo da `Missao`. Declarar marco inverificável tornaria inexequível a recusa por marco não
alcançado, do mesmo modo que a trilha sem ponto de apoio tornava inexequível a conferência de
lastro na publicação.

A declaração NEVER SHALL aceitar preço, saldo de pontos ou qualquer contrapartida do
Guerreiro(a): a recompensa de marco é **conquistada, nunca comprada nem trocada** (`RF-09-71`,
`RN-09-26`, `RN-09-39`, invariante 23, 02 §8.1).

#### Scenario: Mestre autor declara a recompensa de um marco

- **WHEN** o Mestre autor de uma trilha declara que o desbloqueio de uma missão dela concede 30
  unidades de um tipo de recurso
- **THEN** o núcleo grava a recompensa de marco com a trilha, o marco, o tipo e a quantidade

#### Scenario: Mestre que não é autor não declara

- **WHEN** um Mestre que não é autor da trilha tenta declarar uma recompensa de marco nela
- **THEN** o núcleo recusa e nada é gravado

#### Scenario: A declaração não aceita preço

- **WHEN** chega uma declaração de recompensa de marco com preço em pontos extras ou em moedas
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Marco que não é missão é recusado

- **WHEN** o Mestre autor declara uma recompensa de marco cujo marco é etapa, batalha ou
  culminância
- **THEN** o núcleo responde 422 dizendo que só a missão é aceita como marco, e nada é gravado

### Requirement: A recompensa de marco não declara ponto de apoio

O núcleo NEVER SHALL vincular a `RecompensaDeMarco` a um ponto de apoio nem a uma Comunidade
Virtual: ela pende da **trilha**, que é bem comum da plataforma e alcança todas as comunidades.
Quem declara **onde** o recurso saiu SHALL ser a entrega, não a declaração do marco.

Em consequência, o lastro NEVER SHALL ser exigido na declaração nem na publicação da trilha —
não há ponto de apoio contra o qual conferir saldo. A garantia de que nenhuma recompensa é
entregue sem estar provida SHALL ser cumprida **no ato da entrega** (`RF-09-72`, `RN-09-27`,
`RN-01-42`, invariante 9, 02 §8.1).

#### Scenario: Não há ponto de apoio na recompensa de marco

- **WHEN** se procura no núcleo um vínculo de ponto de apoio ou de comunidade na recompensa de
  marco
- **THEN** nenhum existe: o ponto de apoio é atributo da entrega

#### Scenario: A trilha publica sem conferência de lastro

- **WHEN** um Mestre autor publica uma trilha cujo marco declara recompensa e nenhum ponto de
  apoio tem saldo daquele tipo
- **THEN** a trilha é publicada normalmente, e a falta só recusa a entrega quando ela for
  tentada

### Requirement: O Mestre da comunidade confirma a entrega

O núcleo SHALL registrar a entrega da recompensa de marco a um Guerreiro(a) por ato de **Mestre
vinculado à Comunidade Virtual do Guerreiro(a)**, gravando o **ponto de apoio** de onde o
recurso saiu, o Mestre que entregou e a data. A entrega SHALL ser **uma por Guerreiro(a)** que
alcança o marco, e a `RecompensaDeMarco` NEVER SHALL guardar situação de entrega própria: a
quantidade declarada é N e cada entrega é registro próprio, como a `Troca` é do item de catálogo
avulso.

O Admin NEVER SHALL ser quem confirma a entrega: quem estava no encontro é quem entrega
(`RF-07-13`, `RF-09-76`, `RF-02-50`, `RF-02-51`, `RN-02-17`, 02 §8.1, 05 §3).

#### Scenario: Mestre da comunidade entrega a recompensa

- **WHEN** um Mestre vinculado à comunidade de um Guerreiro(a) que alcançou o marco confirma a
  entrega num ponto de apoio com saldo
- **THEN** o núcleo grava a entrega com o Guerreiro(a), o ponto de apoio, o Mestre e a data

#### Scenario: Duas entregas da mesma recompensa de marco

- **WHEN** dois Guerreiros e Guerreiras alcançam o mesmo marco e recebem a recompensa
- **THEN** o núcleo grava duas entregas, e a recompensa de marco segue sem situação de entrega
  própria

#### Scenario: Admin não confirma a entrega

- **WHEN** um Admin tenta confirmar a entrega de uma recompensa de marco
- **THEN** o núcleo recusa e nada é gravado

### Requirement: Cinco condições recusam a entrega antes de qualquer escrita

O núcleo SHALL recusar a entrega com **422**, sem gravar nada e sem mover saldo algum, quando:

1. o tipo de recurso da recompensa for de natureza **durável** — o saldo durável é patrimônio e
   nunca lastreia recompensa;
2. o **lastro** não se confirmar no ato — a quantidade disponível do tipo no **ponto de apoio da
   entrega** for menor que a quantidade da recompensa;
3. a **quantidade** declarada na recompensa de marco já estiver esgotada pelas entregas
   anteriores;
4. o Mestre **não estiver vinculado à comunidade** do Guerreiro(a);
5. o Guerreiro(a) **não tiver alcançado o marco** declarado, conforme o percurso que a
   capacidade `pontos-niveis-e-badges` já deriva dos `Resultado`s.

A resposta SHALL dizer qual das condições recusou. O lastro SHALL ser reverificado **no ato da
entrega**, e não na declaração do marco nem na publicação da trilha, porque a trilha é bem comum
e o saldo é de um ponto de apoio (`RF-07-13`, `RN-07-07`, `RN-09-26`, `RN-09-27`, invariante 9,
02 §8.1, 02 §8.2).

#### Scenario: Recompensa de tipo durável não é entregue

- **WHEN** um Mestre confirma a entrega de uma recompensa cujo tipo de recurso é de natureza
  durável
- **THEN** o núcleo responde 422 dizendo que o saldo durável é patrimônio, e nada é gravado

#### Scenario: Lastro é reverificado no ato da entrega

- **WHEN** um Mestre confirma a entrega de uma recompensa de quantidade 1 num ponto de apoio
  cujo saldo disponível daquele tipo é zero
- **THEN** o núcleo responde 422 dizendo que falta lastro, e nada é gravado

#### Scenario: Quantidade esgotada recusa a entrega

- **WHEN** um Mestre confirma a entrega de uma recompensa de marco de quantidade 30 que já teve
  30 entregas registradas
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre de outra comunidade não entrega

- **WHEN** um Mestre confirma a entrega a um Guerreiro(a) de Comunidade Virtual diferente
  daquela a que ele está vinculado
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Marco não alcançado recusa a entrega

- **WHEN** um Mestre confirma a entrega a um Guerreiro(a) que não tem Resultado registrado para
  a missão declarada como marco
- **THEN** o núcleo responde 422 dizendo que o marco não foi alcançado, e nada é gravado

#### Scenario: Recusa não move nada

- **WHEN** qualquer das cinco condições recusa a entrega
- **THEN** nenhuma entrega é gravada, nenhum lançamento é emitido e o saldo do ponto de apoio
  segue como estava

### Requirement: A entrega dá baixa definitiva numa operação só

O núcleo SHALL executar, numa **única operação atômica**, a gravação da entrega e o **lançamento
de débito** da quantidade da recompensa, do tipo de recurso dela, no **ponto de apoio da
entrega**, valorado em moedas pela vigência do valor de referência na data. Falhando qualquer
parte, nenhuma SHALL persistir.

A baixa SHALL ser **definitiva**: NÃO SHALL existir devolução, reserva de recompensa entre
encontros nem estado intermediário entre alcançar o marco e receber. A entrega NEVER SHALL
debitar ponto regular nem ponto extra do Guerreiro(a) — nem o saldo disponível, nem o acumulado
(`RF-07-13`, `RN-07-08`, `RN-07-14`, `RN-09-26`, `RN-07-36`, invariantes 9 e 23, 05 §3).

#### Scenario: A entrega move as duas coisas juntas

- **WHEN** uma entrega de quantidade 1 é confirmada num ponto de apoio cujo saldo daquele tipo é
  30
- **THEN** o núcleo grava a entrega, emite o débito de uma unidade e o saldo daquele tipo naquele
  ponto de apoio passa a 29

#### Scenario: Falha em qualquer parte desfaz tudo

- **WHEN** o lançamento de débito falha durante o registro da entrega
- **THEN** a entrega não é gravada e o saldo do ponto de apoio não muda

#### Scenario: A entrega não toca o ponto do Guerreiro(a)

- **WHEN** uma entrega de recompensa de marco é confirmada
- **THEN** o saldo de ponto regular e o de ponto extra do Guerreiro(a) permanecem exatamente como
  estavam, disponível e acumulado

#### Scenario: Não há devolução da recompensa entregue

- **WHEN** se procura no núcleo um caminho para devolver ou estornar uma recompensa de marco
  entregue
- **THEN** nenhum existe: a baixa é definitiva, e correção se faz por lançamento de ajuste

### Requirement: Perda ou dano da recompensa entregue nunca vira dívida

O núcleo NEVER SHALL emitir débito de ponto regular, débito de ponto extra ou cobrança de
qualquer espécie ao Guerreiro(a) ou à família dele por perda, dano ou extravio de recompensa de
marco entregue. Sobre o **livro próprio do Guerreiro(a)** NEVER SHALL incidir pontuação negativa
em hipótese alguma (`RN-07-09`, `RN-02-15`, `RN-02-16`, 05 §3).

#### Scenario: Perda da recompensa entregue não gera débito

- **WHEN** um Guerreiro(a) perde ou danifica o livro da linha Alpha que recebeu
- **THEN** nenhum débito de ponto é emitido, nenhuma cobrança é registrada e a participação dele
  segue inalterada

### Requirement: O histórico da entrega é lido sem moedas e sem reais

O núcleo SHALL expor o histórico das entregas filtrado por persona: o Guerreiro(a) lê as
**próprias**, e o Mestre e o Admin leem as da **comunidade** a que estão vinculados. A saída
SHALL trazer a recompensa, o marco, a trilha, o ponto de apoio, a data, o **tipo de recurso**
entregue, a **quantidade** e o **identificador do lançamento** da baixa — sem o que a gestão não
distingue o exemplar da linha Alpha da camisa nem mostra a baixa definitiva —, e NEVER SHALL
trazer o valor em moedas nem o valor em reais do recurso entregue: o custo segue no lançamento,
invisível para a criança (`RF-07-13`, `RN-07-05`, `RF-02-50`, `RF-02-51`, `RN-02-17`,
invariante 16, 02 §8).

#### Scenario: Guerreiro(a) lê as próprias entregas

- **WHEN** um Guerreiro(a) consulta o histórico de entregas
- **THEN** recebe apenas as suas, com recompensa, marco, trilha, ponto de apoio e data

#### Scenario: O histórico não mostra o custo

- **WHEN** qualquer persona consulta o histórico de entregas
- **THEN** nenhum campo traz valor em moedas nem em reais

#### Scenario: A gestão distingue o recurso entregue e alcança a baixa

- **WHEN** um Admin consulta o histórico de entregas
- **THEN** cada entrega traz o tipo de recurso, a quantidade e o identificador do lançamento que
  deu a baixa definitiva

### Requirement: O Guerreiro(a) lê as recompensas que conquistou, entregues ou não

O núcleo SHALL expor, ao **Guerreiro(a) em sessão**, as recompensas de marco cujo **marco ele já
alcançou**, em qualquer trilha que percorra. Cada uma SHALL trazer a **trilha**, o **marco**, o
**tipo de recurso**, a **quantidade** e a **situação da entrega**: entregue, com a data, ou
**aguardando a confirmação do Mestre**. (`RF-05-45`, `RF-07-13`, `RN-09-26`)

O marco alcançado SHALL ser derivado do **mesmo percurso** que a recusa de entrega já confere na
capacidade — a consulta é uma só e não se duplica. A leitura NEVER SHALL antecipar as demais
condições da entrega — lastro no ponto de apoio e quantidade esgotada —, que são reverificadas
no ato pelo Mestre; ela diz o que foi conquistado, não o que será entregue.

A saída NEVER SHALL trazer valor em moedas nem em reais, pela mesma razão que o histórico de
entregas não os traz, e NEVER SHALL oferecer caminho de aquisição: recompensa de marco se
conquista e nunca se compra, com ponto de qualquer natureza. (`RF-05-46`, `RN-05-07`,
`RN-05-41`, invariantes 16 e 23)

#### Scenario: Marco alcançado aparece como conquistado

- **WHEN** um Guerreiro(a) alcança o marco declarado numa trilha que percorre
- **THEN** a recompensa daquele marco passa a aparecer na leitura dele, aguardando a confirmação
  do Mestre

#### Scenario: Marco não alcançado não aparece

- **WHEN** a trilha tem recompensa declarada num marco que o Guerreiro(a) ainda não alcançou
- **THEN** ela não aparece na leitura dele

#### Scenario: A recompensa entregue mostra a data

- **WHEN** o Mestre já confirmou a entrega
- **THEN** a mesma recompensa aparece como entregue, com a data da confirmação

#### Scenario: A leitura não antecipa a recusa da entrega

- **WHEN** o ponto de apoio está sem lastro do tipo de recurso da recompensa conquistada
- **THEN** ela continua aparecendo como conquistada e aguardando o Mestre, e a conferência do
  lastro segue acontecendo no ato da entrega

#### Scenario: Nenhum valor de custo chega à criança

- **WHEN** o Guerreiro(a) lê as recompensas conquistadas
- **THEN** nenhum campo traz valor em moedas nem em reais

#### Scenario: Só as próprias recompensas

- **WHEN** um Guerreiro(a) consulta esta leitura
- **THEN** recebe apenas as recompensas do próprio percurso, e nenhuma de outra criança
