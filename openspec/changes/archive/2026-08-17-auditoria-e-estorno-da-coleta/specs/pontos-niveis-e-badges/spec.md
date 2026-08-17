## MODIFIED Requirements

### Requirement: Ponto regular é creditado por trilha ou poder e nunca debitado

O núcleo SHALL creditar **ponto regular** por **trilha ou poder** — nunca globalmente — a partir
de um Resultado, de uma **Criação Original validada**, de uma **partida de quiz encerrada** ou de
um **registro de coleta válido**, conforme a fonte e o valor da tabela do documento 11 §5. Na
criação original, o valor SHALL ser creditado **integral a cada integrante** da equipe da trilha
que a entregou, sem divisão. Na partida de quiz, o crédito SHALL seguir a régua própria dela e
alcançar **cada integrante** da equipe. No registro de coleta, o crédito SHALL seguir a régua
própria dele e alcançar apenas o **coletor** da série.

O ponto regular NEVER SHALL ser **trocado por recompensa**: a troca alcança só o saldo de pontos
extras. Ele SHALL debitar **apenas por fato desfeito** — o **estorno de registro de coleta
invalidado** e a **ocorrência de conduta lançada**, esta de entrega posterior. O saldo NEVER
SHALL ficar negativo: débito maior que o saldo da trilha ou do poder SHALL pará-lo em **zero**.
O registro de ponto regular NEVER SHALL ser removido. (`RF-01-21`, `RF-01-57`, `RF-01-64`,
`RF-01-69`, `RF-08-09`, `RN-01-38`, `RN-01-55`, invariante 23 do documento 99 §6, 11 §5)

#### Scenario: Resultado "realizada" credita o valor da atividade

- **WHEN** um Resultado é lançado com desfecho "realizada"
- **THEN** o núcleo credita, à trilha ou ao poder correspondente, o ponto regular da fonte da
  atividade

#### Scenario: Resultado "realizada com mérito" credita o valor mais o adicional de mérito

- **WHEN** um Resultado é lançado com desfecho "realizada com mérito"
- **THEN** o núcleo credita o ponto regular da atividade acrescido do adicional de mérito da
  tabela do documento 11 §5

#### Scenario: Ponto regular não aceita débito

- **WHEN** uma operação que não é estorno de registro de coleta invalidado nem ocorrência de
  conduta tenta reduzir o saldo de ponto regular de um Guerreiro(a)
- **THEN** o núcleo recusa a operação

#### Scenario: Troca de recompensa não alcança o ponto regular

- **WHEN** uma troca de recompensa avulsa tenta debitar o saldo de ponto regular
- **THEN** o núcleo recusa a operação, e só o saldo de pontos extras pode ser trocado

#### Scenario: Estorno de registro invalidado debita o ponto regular

- **WHEN** um registro de coleta que creditou ponto regular é invalidado na auditoria
- **THEN** o núcleo reduz o saldo do coletor no valor exato que aquele registro creditou

#### Scenario: Débito maior que o saldo para em zero

- **WHEN** um estorno de valor maior que o saldo da trilha ou do poder é aplicado
- **THEN** o núcleo deixa o saldo em zero, e ele não fica negativo

#### Scenario: O registro de ponto regular não é removido

- **WHEN** qualquer operação tenta apagar o registro de ponto regular de um Guerreiro(a)
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

### Requirement: Nível é percurso por trilha ou poder e nunca regride

O núcleo SHALL manter o **nível** por trilha ou poder, derivado do **percurso das missões
obrigatórias desbloqueadas** — nunca do total de pontos acumulado (11 §6). Nesta capacidade o
núcleo SHALL certificar os níveis **1** (inscrito na trilha e primeira atividade realizada), **2**
(um terço das missões obrigatórias desbloqueadas), **4** (todas as obrigatórias desbloqueadas e
ao menos um Resultado com mérito extra por auxílio aos colegas) e **5 — Mestre Aprendiz** (a
criação original da trilha validada pelo Mestre autor, certificada a **cada integrante** da
equipe que a entregou). Nível conquistado SHALL **nunca regredir**, inclusive quando um **débito
de ponto regular** reduz o saldo do Guerreiro(a); o badge já concedido SHALL igualmente
permanecer. (`RF-01-21`, `RF-01-64`, `RF-01-70`, `RN-01-55`, 11 §6)

#### Scenario: Primeira atividade realizada alcança o nível 1

- **WHEN** o Guerreiro(a) tem a primeira atividade da trilha com Resultado registrado
- **THEN** o núcleo certifica o nível 1 naquela trilha

#### Scenario: Um terço das obrigatórias desbloqueadas alcança o nível 2

- **WHEN** o Guerreiro(a) tem Resultado registrado para um terço das missões obrigatórias da
  trilha
- **THEN** o núcleo certifica o nível 2 naquela trilha

#### Scenario: Nível conquistado não regride

- **WHEN** um Guerreiro(a) já certificado num nível deixa de atender ao critério que o levou lá
- **THEN** o núcleo mantém o nível já certificado

#### Scenario: Estorno não derruba nível nem badge

- **WHEN** um estorno reduz o saldo de ponto regular de um Guerreiro(a) já certificado num nível
- **THEN** o núcleo mantém o nível certificado e os badges já concedidos

#### Scenario: Criação original validada alcança o nível 5

- **WHEN** o Mestre autor da trilha valida a criação original entregue pela equipe da trilha
- **THEN** o núcleo certifica o nível 5 — Mestre Aprendiz — naquela trilha a cada integrante da
  equipe

### Requirement: O registro de coleta válido credita 5 pontos ao Poder do Território

O núcleo SHALL creditar **5 pontos regulares** — o valor da tabela do documento 11 §5 — por
**registro de coleta válido**, e SHALL creditá-los ao **Poder do Território**, identificado pelo
papel declarado no catálogo de poderes. O crédito NEVER SHALL recair sobre o poder da trilha em
que o desafio de coleta nasceu. O valor SHALL ser **o mesmo para todo tipo de coleta**, qualquer
que seja o que se mede, e o crédito SHALL ser **recorrente e sem teto por período**, limitado
apenas pela quantidade de registros que pontuam declarada no desafio.

Registro marcado **"a conferir"** NEVER SHALL creditar na gravação: o crédito dele SHALL vir da
**confirmação do Mestre** na auditoria, pela mesma régua. (`RF-08-09`, `RF-08-12`, `RF-08-29`,
`RN-08-05`, `RN-08-15`, `RN-08-26`, `RN-01-54`, 11 §5)

#### Scenario: Registro válido credita 5 pontos ao Poder do Território

- **WHEN** um registro de coleta válido é gravado numa série de um desafio nascido numa trilha
  do Poder da IA e Robótica
- **THEN** o núcleo credita 5 pontos regulares ao **Poder do Território** do coletor, e nenhum
  ponto ao Poder da IA e Robótica

#### Scenario: Registro "a conferir" credita zero na gravação

- **WHEN** uma medição de valor fora da faixa esperada do tipo é gravada
- **THEN** o núcleo grava o registro marcado "a conferir" e credita zero ponto por ele

#### Scenario: O valor não varia com o tipo de coleta

- **WHEN** dois registros válidos são gravados em séries de tipos de coleta diferentes
- **THEN** o núcleo credita 5 pontos por cada um dos dois

#### Scenario: A coleta não tem teto por período

- **WHEN** um desafio de cadência semanal declara que quatro registros do período pontuam e o
  coletor grava os quatro na mesma semana
- **THEN** o núcleo credita 5 pontos por cada um dos quatro, sem teto
