## MODIFIED Requirements

### Requirement: Ponto regular é creditado por trilha ou poder e nunca debitado

O núcleo SHALL creditar **ponto regular** por **trilha ou poder** — nunca globalmente — a partir
de um Resultado, de uma **Criação Original validada**, de uma **partida de quiz encerrada** ou de
um **registro de coleta válido**, conforme a fonte e o valor da tabela do documento 11 §5. Na
criação original, o valor SHALL ser creditado **integral a cada integrante** da equipe da trilha
que a entregou, sem divisão. Na partida de quiz, o crédito SHALL seguir a régua própria dela e
alcançar **cada integrante** da equipe. No registro de coleta, o crédito SHALL seguir a régua
própria dele e alcançar apenas o **coletor** da série. O ponto regular SHALL **nunca ser
debitado**, em nenhuma operação. (`RF-01-21`, `RF-01-64`, `RF-08-09`, `RN-01-38`, 11 §5)

#### Scenario: Resultado "realizada" credita o valor da atividade

- **WHEN** um Resultado é lançado com desfecho "realizada"
- **THEN** o núcleo credita, à trilha ou ao poder correspondente, o ponto regular da fonte da
  atividade

#### Scenario: Resultado "realizada com mérito" credita o valor mais o adicional de mérito

- **WHEN** um Resultado é lançado com desfecho "realizada com mérito"
- **THEN** o núcleo credita o ponto regular da atividade acrescido do adicional de mérito da
  tabela do documento 11 §5

#### Scenario: Ponto regular não aceita débito

- **WHEN** qualquer operação tenta reduzir o saldo de ponto regular de um Guerreiro(a)
- **THEN** o núcleo recusa a operação

#### Scenario: Criação original validada credita 50 pontos regulares

- **WHEN** o Mestre autor valida uma criação original entregue por uma equipe de três integrantes
- **THEN** o núcleo credita, à trilha da criação, 50 pontos regulares integrais a **cada um** dos
  três

#### Scenario: O valor da criação original não se divide pela equipe

- **WHEN** duas equipes de tamanhos diferentes têm a criação original validada na mesma trilha
- **THEN** cada integrante das duas recebe os mesmos 50 pontos, sem rateio pelo tamanho

#### Scenario: Partida de quiz encerrada credita a trilha da atividade

- **WHEN** uma partida de quiz sobre uma atividade da trilha 1 é encerrada com acertos
- **THEN** o núcleo credita o ponto regular apurado à trilha 1, e não à aula nem a outra trilha

#### Scenario: Registro de coleta válido credita apenas o coletor

- **WHEN** um registro de coleta válido é gravado numa série
- **THEN** o núcleo credita o ponto regular ao coletor daquela série, e a nenhum outro
  Guerreiro(a)

## ADDED Requirements

### Requirement: O registro de coleta válido credita 5 pontos ao Poder do Território

O núcleo SHALL creditar **5 pontos regulares** — o valor da tabela do documento 11 §5 — por
**registro de coleta válido**, e SHALL creditá-los ao **Poder do Território**, identificado pelo
papel declarado no catálogo de poderes. O crédito NEVER SHALL recair sobre o poder da trilha em
que o desafio de coleta nasceu. O valor SHALL ser **o mesmo para todo tipo de coleta**, qualquer
que seja o que se mede, e o crédito SHALL ser **recorrente e sem teto por período**, limitado
apenas pela quantidade de registros que pontuam declarada no desafio. (`RF-08-09`, `RN-08-05`,
`RN-08-15`, `RN-01-54`, 11 §5)

#### Scenario: Registro válido credita 5 pontos ao Poder do Território

- **WHEN** um registro de coleta válido é gravado numa série de um desafio nascido numa trilha
  do Poder da IA e Robótica
- **THEN** o núcleo credita 5 pontos regulares ao **Poder do Território** do coletor, e nenhum
  ponto ao Poder da IA e Robótica

#### Scenario: O valor não varia com o tipo de coleta

- **WHEN** dois registros válidos são gravados em séries de tipos de coleta diferentes
- **THEN** o núcleo credita 5 pontos por cada um dos dois

#### Scenario: A coleta não tem teto por período

- **WHEN** um desafio de cadência semanal declara que quatro registros do período pontuam e o
  coletor grava os quatro na mesma semana
- **THEN** o núcleo credita 5 pontos por cada um dos quatro, sem teto

### Requirement: Só pontuam os registros do período até a quantidade que o desafio declara

O núcleo SHALL contar, para cada **período de cadência** da série, quantos registros válidos já
pontuaram, e SHALL creditar **zero** ao registro que exceder a **quantidade de registros que
pontuam** declarada no desafio. O registro excedente SHALL ser **gravado e válido** como
qualquer outro — só não credita. O período SHALL ser apurado pela **data da medição**, e a
contagem SHALL reiniciar a cada período novo. O núcleo SHALL informar na resposta se aquele
registro pontuou. (`RN-08-06`, `RF-08-09`, PRD-08 §§9, 12)

#### Scenario: O segundo registro do período credita zero quando só um pontua

- **WHEN** o desafio declara que um registro do período pontua e o coletor grava o segundo
  registro da mesma semana
- **THEN** o núcleo grava o registro como válido, credita zero ponto e responde indicando que
  ele não pontuou

#### Scenario: O primeiro registro do período seguinte volta a pontuar

- **WHEN** o coletor grava o primeiro registro da semana seguinte, num desafio de cadência
  semanal em que um registro pontua
- **THEN** o núcleo credita 5 pontos, porque a contagem reiniciou no período novo

#### Scenario: A quantidade que pontua é contada pela data da medição

- **WHEN** o coletor envia, já na semana seguinte, um segundo registro cuja medição aconteceu na
  semana anterior, e o desafio declara que um registro do período pontua
- **THEN** o núcleo credita zero, porque o período do registro é o da medição, em que já houve
  registro que pontuou

### Requirement: Nenhum jogo credita ponto de coleta

O núcleo NEVER SHALL aceitar crédito de ponto de coleta vindo de partida de jogo, do App 04 ou
de qualquer rota de leitura exposta aos jogos. O crédito da coleta SHALL nascer exclusivamente
do **registro válido** gravado na série. (`RN-08-17`, `RF-01-22`, invariante 8 do documento 99
§6)

#### Scenario: Rota de jogo não credita ponto de coleta

- **WHEN** uma chamada vinda do contrato de leitura dos jogos tenta creditar ponto de coleta
- **THEN** o núcleo recusa a chamada e nenhum ponto é creditado

#### Scenario: O crédito da coleta nasce do registro

- **WHEN** pontos do Poder do Território de um Guerreiro(a) são consultados
- **THEN** todo ponto ali acumulado tem como origem um registro de coleta válido
