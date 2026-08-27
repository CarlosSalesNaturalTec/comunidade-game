## MODIFIED Requirements

### Requirement: Ponto regular é creditado por trilha ou poder e nunca debitado

O núcleo SHALL creditar **ponto regular** por **trilha ou poder** — nunca globalmente — a partir
de um Resultado, de uma **Criação Original validada**, de uma **partida de quiz encerrada** ou de
um **registro de coleta válido**, conforme a fonte e o valor da tabela do documento 11 §5. Na
criação original **em equipe**, o valor SHALL ser creditado **integral a cada integrante** da
equipe da trilha que a entregou, sem divisão; na criação original **individual**, ao
**Guerreiro(a)** que a entregou, no mesmo valor — a modalidade NEVER SHALL alterar o valor
creditado a cada pessoa. Na partida de quiz, o crédito SHALL seguir a régua própria dela e
alcançar **cada integrante** da equipe. No registro de coleta, o crédito SHALL seguir a régua
própria dele e alcançar apenas o **coletor** da série.

O ponto regular NEVER SHALL ser **trocado por recompensa**: a troca alcança só o saldo de pontos
extras. Ele SHALL debitar **apenas por fato desfeito** — o **estorno de registro de coleta
invalidado** e a **ocorrência de conduta lançada**, ambos exercitáveis. O saldo NEVER
SHALL ficar negativo: débito maior que o saldo da trilha ou do poder SHALL pará-lo em **zero**.
O registro de ponto regular NEVER SHALL ser removido. (`RF-01-21`, `RF-01-57`, `RF-01-64`,
`RF-01-69`, `RF-08-09`, `RF-09-31`, `RN-01-38`, `RN-01-55`, invariante 23 do documento 99 §6,
11 §5)

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

#### Scenario: Criação original individual validada credita os mesmos 50 pontos

- **WHEN** o Mestre autor valida uma criação original entregue individualmente
- **THEN** o núcleo credita, à trilha da criação, os mesmos 50 pontos regulares ao Guerreiro(a)
  que a entregou

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
núcleo SHALL certificar os níveis **1** (inscrito na trilha **e** primeira atividade realizada, as
**duas** condições), **2** (um terço das missões obrigatórias desbloqueadas), **4** (todas as
obrigatórias desbloqueadas e ao menos um Resultado com mérito extra por auxílio aos colegas) e
**5 — Mestre Aprendiz** (a criação original da trilha validada pelo Mestre autor, certificada a
**cada integrante** da equipe que a entregou ou, na modalidade individual, ao **Guerreiro(a)**
que a entregou). A condição "inscrito" do nível 1 SHALL ser a
`InscricaoNaTrilha` da capacidade `inscricao-na-trilha`, e NEVER SHALL ser derivada de haver
`Resultado` na trilha: quem põe o Guerreiro(a) no percurso é ato dele, não lançamento do Mestre.
Nível conquistado SHALL **nunca regredir**, inclusive quando um **débito de ponto regular** reduz
o saldo do Guerreiro(a); o badge já concedido SHALL igualmente permanecer. (`RF-01-21`,
`RF-01-64`, `RF-01-70`, `RN-01-55`, `RF-05-09`, `RF-09-31`, `RN-05-43`, 11 §6)

#### Scenario: Primeira atividade realizada alcança o nível 1

- **WHEN** o Guerreiro(a) **inscrito** na trilha tem a primeira atividade dela com Resultado
  registrado
- **THEN** o núcleo certifica o nível 1 naquela trilha

#### Scenario: Resultado sem inscrição não alcança o nível 1

- **WHEN** um Guerreiro(a) não inscrito na trilha tem Resultado registrado numa atividade dela
- **THEN** o núcleo não certifica o nível 1, e o faz assim que a inscrição existir

#### Scenario: Inscrição sem atividade realizada não alcança o nível 1

- **WHEN** o Guerreiro(a) inscreve-se numa trilha e ainda não tem Resultado registrado nela
- **THEN** o núcleo não certifica o nível 1

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

#### Scenario: Criação original individual validada alcança o nível 5

- **WHEN** o Mestre autor da trilha valida uma criação original entregue individualmente
- **THEN** o núcleo certifica o nível 5 — Mestre Aprendiz — naquela trilha ao Guerreiro(a) que a
  entregou

### Requirement: Badge é conquistado por trilha ou por poder, nunca global

O núcleo SHALL conceder **badge** sempre vinculado a uma trilha ou a um poder, nunca de forma
global (11 §7), com **uma única exceção: o badge de protagonismo**, que é global porque a
proposta de evolução que o rende é sobre a plataforma inteira e não sobre uma trilha
(`RN-01-50`). Nesta capacidade o núcleo SHALL conceder o **badge de nível** a cada nível
certificado, o **badge de valores/causas** a Resultado de atividade de natureza "valores e
temas transversais", o **badge de autoria** a **cada integrante** da equipe cuja criação
original for validada pelo Mestre autor — ou, na modalidade individual, ao **Guerreiro(a)** que
a entregou — e o **badge de protagonismo** ao autor da sugestão
adotada pela gestão, na mesma operação em que a fila de avaliação grava o desfecho. O badge de
conquista **Guardião do Acervo** não nasce de Resultado nem de Criação Original — ele depende
de encontro presencial identificável (`Aula/Agenda`) — e fica para a fatia que o entregar.
(`RF-01-21`, `RF-01-64`, `RF-09-31`, `RN-01-50`, 11 §7)

#### Scenario: Badge de nível concedido ao certificar um nível

- **WHEN** o núcleo certifica um nível numa trilha
- **THEN** o núcleo concede o badge de nível correspondente àquela trilha

#### Scenario: Badge de valores/causas concedido por atividade da natureza

- **WHEN** o Guerreiro(a) tem Resultado de atividade de natureza "valores e temas transversais"
- **THEN** o núcleo concede o badge de valores/causas correspondente à trilha ou ao poder

#### Scenario: Badge de autoria concedido ao validar a criação original

- **WHEN** o Mestre autor da trilha valida a criação original entregue pela equipe da trilha
- **THEN** o núcleo concede o badge de autoria daquela trilha a cada integrante da equipe

#### Scenario: Badge de autoria concedido na criação original individual

- **WHEN** o Mestre autor da trilha valida uma criação original entregue individualmente
- **THEN** o núcleo concede o badge de autoria daquela trilha ao Guerreiro(a) que a entregou

#### Scenario: Badge de protagonismo concedido ao adotar a proposta

- **WHEN** um Admin conclui a avaliação de uma sugestão como **adotada**
- **THEN** o núcleo concede o badge de protagonismo ao autor, **sem vínculo com trilha ou
  poder**, na mesma operação em que credita os pontos extras

#### Scenario: Badge de protagonismo não se repete

- **WHEN** o desfecho **adotada** é gravado para uma sugestão cujo autor já recebeu o badge de
  protagonismo
- **THEN** o núcleo não concede o badge outra vez
