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
invalidado** e a **ocorrência de conduta lançada**, ambos exercitáveis. O saldo NEVER
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

#### Scenario: Ocorrência de conduta lançada debita o ponto regular

- **WHEN** o Mestre da aula ou um Admin lança uma ocorrência de conduta contra um Guerreiro(a)
- **THEN** o núcleo reduz o saldo dele, na trilha ou no poder da ocorrência, no valor lançado

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
