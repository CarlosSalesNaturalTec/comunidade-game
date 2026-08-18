## ADDED Requirements

### Requirement: O aporte declara a destinação do que entra

O núcleo SHALL registrar em todo aporte a **destinação** do que entra — **lastro** ou
**ressarcimento**. Aporte sem destinação declarada SHALL nascer com destinação **lastro**, que é
o caso comum. Destinação fora dos dois valores previstos SHALL ser recusada com **422**.

O aporte de destinação **ressarcimento** SHALL creditar o **Poder Sustentador** de quem doou,
como qualquer outro aporte, e NÃO SHALL virar lastro: NÃO SHALL compor o saldo de recurso algum
e NÃO SHALL confirmar aula pendente de lastro. É o que impede o mesmo dinheiro de destravar uma
aula e devolver a quem absorveu.

Aporte de forma **absorção** NÃO SHALL ter destinação ressarcimento: quem absorve provê recurso,
não doa dinheiro para devolver a terceiro — a tentativa SHALL ser recusada com **422**.
(`RF-07-23`, `RN-07-38`, PRD-07 §8)

#### Scenario: Doação destinada a ressarcir credita sem virar lastro

- **WHEN** um Admin registra um aporte financeiro com destinação ressarcimento
- **THEN** o Poder Sustentador do doador sobe pelas moedas do aporte, e o saldo daquele tipo de
  recurso no ponto de apoio permanece como estava

#### Scenario: A receita destinada não confirma aula pendente de lastro

- **WHEN** existe uma aula pendente de lastro cuja falta é exatamente do tipo de recurso da
  doação, e entra um aporte de destinação ressarcimento que cobriria a diferença
- **THEN** a aula permanece pendente de lastro e nenhuma reserva é criada

#### Scenario: Aporte sem destinação declarada é de lastro

- **WHEN** um Admin registra um aporte sem declarar destinação
- **THEN** o aporte é gravado com destinação lastro e credita o saldo normalmente

#### Scenario: Absorção não se destina a ressarcimento

- **WHEN** um Mestre tenta registrar uma absorção com destinação ressarcimento
- **THEN** o núcleo responde 422 e nada é gravado

## MODIFIED Requirements

### Requirement: O aporte por absorção credita no ato e nasce ressarcível

O núcleo SHALL registrar **aporte por absorção** em nome do **Mestre ou Admin** que proveu o
recurso sem receber. A absorção SHALL **creditar no ato**, sem homologação, e o campo do Admin
homologador SHALL ficar vazio. O aporte por absorção de tipo de natureza **consumível, durável
ou financeira** SHALL nascer marcado como **ressarcível**, com situação de ressarcimento **em
aberto**. Persona de papel diferente de Mestre ou Admin SHALL receber **403**. Aporte registrado
pela gestão SHALL nascer **não ressarcível**.

A absorção de tipo de natureza **serviço** SHALL nascer **não ressarcível**, com situação de
ressarcimento **não se aplica**: quem absorve serviço dá tempo, não dinheiro, e não há
desembolso a devolver. Ela credita o **Poder Sustentador** e conta no **selo de absorções**
como qualquer outra.

A absorção SHALL poder declarar a **aula cuja necessidade atende** — é como quem cobre uma falta
publicada declara qual falta cobriu. A aula declarada SHALL ser uma aula existente e o tipo de
recurso do aporte SHALL ser um dos que aquela aula consome; fora disso, o registro SHALL ser
recusado com **422**. A necessidade segue **derivada**, sem tabela a referenciar: a declaração
liga o aporte à aula, não a um registro de necessidade. A aula SHALL ser gravada **apenas** na
forma absorção; aporte de outra forma que a declare SHALL ser recusado com **422**.

A absorção SHALL exigir o **valor de origem em reais** quando o tipo de recurso for de natureza
**consumível, durável ou financeira** — houve desembolso, e é esse valor que o ressarcimento
devolve; sem ele o registro SHALL ser recusado com **422**. Na natureza **serviço** o valor de
origem SHALL ficar **vazio** e NÃO SHALL ser exigido: o valor daquele aporte é o **em moedas**,
que a tabela de referência já fornece, e reais e moedas NÃO SHALL ser convertidos um no outro.
(`RF-07-06`, `RF-07-21`, `RF-07-28`, `RN-07-06`, `RN-07-24`, `RN-07-35`, `RN-07-39`,
PRD-07 §§8, 9, 12)

#### Scenario: Mestre absorve um recurso

- **WHEN** um Mestre em sessão registra um aporte por absorção com tipo, quantidade, ponto de
  apoio e o valor de origem em reais
- **THEN** o núcleo grava o aporte em nome dele, credita o saldo no ato, deixa o homologador
  vazio e marca o aporte como ressarcível com situação em aberto

#### Scenario: Admin absorve um recurso em nome próprio

- **WHEN** um Admin em sessão registra um aporte por absorção em nome de si mesmo
- **THEN** o núcleo grava e credita, sem aplicar a recusa da homologação em causa própria

#### Scenario: Apoiador não absorve

- **WHEN** um Apoiador em sessão tenta registrar um aporte por absorção
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Aporte da gestão não nasce ressarcível

- **WHEN** um Admin registra um aporte pela rota da gestão
- **THEN** o aporte é gravado com situação de ressarcimento "não se aplica"

#### Scenario: Mestre assume a necessidade publicada de uma aula

- **WHEN** um Mestre registra uma absorção declarando a aula cuja necessidade atende, de um tipo
  que aquela aula consome
- **THEN** o núcleo grava o aporte com a aula declarada e credita o saldo no ponto de apoio da
  aula

#### Scenario: Absorção de tipo que a aula não consome é recusada

- **WHEN** um Mestre declara uma aula cuja lista de recursos não inclui o tipo do aporte
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Absorção com desembolso exige o valor em reais

- **WHEN** um Mestre registra uma absorção de tipo de natureza consumível sem o valor de origem
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Absorção de serviço não exige valor em reais e não é ressarcível

- **WHEN** um Mestre registra uma absorção de tipo de natureza serviço sem o valor de origem
- **THEN** o núcleo grava o aporte com o valor de origem vazio, situação de ressarcimento "não
  se aplica", e o Poder Sustentador dele sobe pelas moedas do aporte

#### Scenario: Absorção de serviço não entra na fila de ressarcimento

- **WHEN** um Mestre absorve um serviço e um Admin consulta os aportes ressarcíveis
- **THEN** aquele aporte não aparece na fila, e a contagem de absorções do Mestre segue
  contando-o
