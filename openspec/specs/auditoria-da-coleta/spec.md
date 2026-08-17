## Purpose

A conferência do Mestre sobre os registros das séries dos seus desafios: a amostra semanal que
ele recebe, a confirmação que credita o que estava "a conferir" e a invalidação com motivo que
estorna os pontos sem apagar a medição. É a trava contra o dado inventado e o momento de ensinar
a medir — e é ela que fecha o ciclo de vida da situação do registro.

## Requirements

### Requirement: A amostra é de 10% dos registros da semana em cada série ativa, com o mínimo de um

O núcleo SHALL compor a amostra de auditoria por **série**, tomando **10% dos registros da
semana** de cada série, e SHALL entregar **ao menos um** registro por série que tenha registro na
semana. A amostra SHALL alcançar somente as séries dos **desafios de que o Mestre é autor**.
Série sem nenhum registro na semana NEVER SHALL aparecer na amostra. (`RN-08-20`, `RF-08-13`,
02 §1, PRD-08 §5.5)

#### Scenario: Série com trinta registros na semana rende três

- **WHEN** o Mestre pede a amostra de uma série com trinta registros gravados na semana
- **THEN** a amostra traz três registros daquela série

#### Scenario: Série com poucos registros rende um

- **WHEN** o Mestre pede a amostra de uma série com quatro registros gravados na semana
- **THEN** a amostra traz um registro daquela série, pelo piso

#### Scenario: Série sem registro na semana fica fora da amostra

- **WHEN** o Mestre pede a amostra e uma das suas séries não teve registro na semana
- **THEN** aquela série não aparece na amostra

#### Scenario: A amostra não alcança série de desafio alheio

- **WHEN** um Mestre pede a amostra e existe série ativa de desafio de que ele não é autor
- **THEN** nenhum registro daquela série aparece na amostra dele

### Requirement: Todo valor "a conferir" entra na amostra, fora do percentual

O núcleo SHALL incluir na amostra **todos** os registros marcados **"a conferir"** ainda não
auditados das séries alcançadas, **independentemente do percentual** e sem que eles consumam as
vagas dos 10%. Registro "a conferir" NEVER SHALL ficar fora da amostra da semana em que foi
gravado. (`RN-08-20`, `RN-08-26`, 02 §1)

#### Scenario: Os "a conferir" entram todos, além do percentual

- **WHEN** uma série tem trinta registros na semana, dos quais cinco estão "a conferir"
- **THEN** a amostra traz os cinco "a conferir" mais três sorteados entre os demais

#### Scenario: Série só com "a conferir" entrega todos eles

- **WHEN** uma série tem dois registros na semana, ambos "a conferir"
- **THEN** a amostra traz os dois

#### Scenario: "A conferir" já auditado não volta à amostra

- **WHEN** o Mestre pede a amostra e um registro "a conferir" da semana já foi confirmado antes
- **THEN** aquele registro não aparece de novo na amostra

### Requirement: Série ativa é apurada no instante da amostra

O núcleo SHALL apurar a situação de cada série **no instante em que a amostra é composta**, e
NEVER SHALL aproveitar situação apurada anteriormente. Série que passou a **interrompida** ou
**encerrada** antes do pedido da amostra NEVER SHALL contribuir com registro para ela, ainda que
tenha tido registro na semana. (`RN-08-20`, 02 §1)

#### Scenario: Série interrompida antes do pedido fica fora

- **WHEN** uma série teve registros na semana mas está interrompida no instante do pedido da
  amostra
- **THEN** nenhum registro dela entra na amostra

#### Scenario: Série encerrada antes do pedido fica fora

- **WHEN** uma série teve registros na semana mas o desafio venceu e ela está encerrada
- **THEN** nenhum registro dela entra na amostra

### Requirement: Só o Mestre autor do desafio audita, e o Admin não audita no lugar dele

O núcleo SHALL aceitar a confirmação e a invalidação de registro apenas do **Mestre autor do
desafio** da série a que o registro pertence, e SHALL recusar com **403** a de qualquer outra
persona, inclusive de outro Mestre e do Admin. A recusa NEVER SHALL alterar a situação do
registro. (`RF-08-13`, `RF-08-29`, PRD-08 §§4, 9)

#### Scenario: Mestre que não é autor do desafio é recusado

- **WHEN** um Mestre tenta invalidar registro de série de desafio de que não é autor
- **THEN** o núcleo responde 403 e o registro permanece como estava

#### Scenario: Guerreiro(a) não audita o próprio registro

- **WHEN** o coletor tenta confirmar um registro "a conferir" da sua própria série
- **THEN** o núcleo responde 403 e o registro permanece "a conferir"

### Requirement: A confirmação credita o registro "a conferir" e nunca credita duas vezes

O núcleo SHALL creditar, na **confirmação** de registro marcado **"a conferir"**, o ponto regular
que ele não recebeu na gravação, seguindo a mesma régua do registro válido — valor da tabela do
documento 11 §5, ao Poder do Território do coletor, e sujeito à **quantidade de registros que
pontuam no período**, apurada no instante da confirmação. A confirmação de registro **já válido**
SHALL apenas encerrar a auditoria dele e NEVER SHALL creditar de novo. Confirmação de registro
já auditado NEVER SHALL creditar segunda vez. (`RF-08-29`, `RN-08-26`, PRD-08 §5.5)

#### Scenario: Confirmar "a conferir" credita o valor da tabela

- **WHEN** o Mestre autor confirma um registro "a conferir" numa série cujo período ainda não
  esgotou a quantidade que pontua
- **THEN** o núcleo credita o ponto regular ao Poder do Território do coletor e marca o registro
  como válido e auditado

#### Scenario: Confirmar registro já válido não credita de novo

- **WHEN** o Mestre autor confirma um registro que já era válido e já tinha creditado
- **THEN** o núcleo encerra a auditoria dele sem creditar ponto algum

#### Scenario: "A conferir" confirmado fora da quantidade do período credita zero

- **WHEN** o Mestre autor confirma um registro "a conferir" cujo período já teve a quantidade
  declarada de registros pontuando
- **THEN** o núcleo marca o registro como válido e auditado, e credita zero

#### Scenario: Confirmar duas vezes não credita duas vezes

- **WHEN** o Mestre autor confirma de novo um registro que já confirmou
- **THEN** o núcleo não credita ponto algum pela segunda confirmação

### Requirement: A invalidação exige motivo, estorna o valor creditado e mantém o registro

O núcleo SHALL aceitar a **invalidação** de registro somente com **motivo** declarado, e SHALL
gravar quem invalidou, quando e o motivo. A invalidação SHALL **estornar exatamente o valor que
aquele registro creditou** ao Poder do Território do coletor — e **zero** quando ele nada
creditou, como o registro "a conferir" ainda não confirmado e o excedente da quantidade do
período. O registro NEVER SHALL ser apagado: ele SHALL permanecer gravado e consultável, marcado
como **inválido**. A invalidação NEVER SHALL creditar outro registro em lugar dele, ainda que a
vaga do período fique livre. (`RF-08-13`, `RN-08-09`, `RN-08-10`, PRD-08 §5.5)

#### Scenario: Invalidação sem motivo é recusada

- **WHEN** o Mestre autor tenta invalidar um registro sem declarar motivo
- **THEN** o núcleo responde 422 e o registro permanece válido

#### Scenario: Invalidar registro que creditou estorna o valor exato

- **WHEN** o Mestre autor invalida um registro que creditou o valor da tabela ao Poder do
  Território
- **THEN** o núcleo reduz o saldo do coletor naquele mesmo valor, e o registro segue gravado
  como inválido

#### Scenario: Invalidar "a conferir" não confirmado estorna zero

- **WHEN** o Mestre autor invalida um registro "a conferir" que ainda não tinha sido confirmado
- **THEN** o núcleo não reduz saldo algum, porque ele nunca creditou

#### Scenario: Invalidar excedente do período estorna zero

- **WHEN** o Mestre autor invalida um registro que fora gravado além da quantidade que pontua no
  período e creditou zero
- **THEN** o núcleo não reduz saldo algum

#### Scenario: A vaga liberada não credita outro registro

- **WHEN** o Mestre autor invalida o único registro que pontuou num período em que outros foram
  gravados como excedentes
- **THEN** nenhum dos excedentes passa a pontuar

#### Scenario: O registro invalidado continua consultável

- **WHEN** se consulta a série depois da invalidação de um registro dela
- **THEN** o registro aparece, marcado como inválido, com o motivo e quem invalidou

### Requirement: A invalidação é terminal e o registro invalidado não volta a valer

O núcleo NEVER SHALL devolver registro **invalidado** à situação válida, e SHALL recusar a
confirmação de registro já invalidado. A correção de medição invalidada SHALL se fazer por
**novo registro**, nunca pela reversão da invalidação. (`RN-08-10`, PRD-08 §5.5)

#### Scenario: Confirmar registro invalidado é recusado

- **WHEN** o Mestre autor tenta confirmar um registro que já invalidou
- **THEN** o núcleo recusa a operação e o registro permanece inválido

#### Scenario: Invalidar de novo não estorna de novo

- **WHEN** o Mestre autor invalida um registro que já estava invalidado
- **THEN** o núcleo não reduz o saldo do coletor uma segunda vez

### Requirement: O registro invalidado sai de toda saída agregada do território

O núcleo NEVER SHALL compor valor, contagem ou contagem de coletores de recorte publicado com
registro **invalidado**, e a exclusão SHALL valer para o painel público, a exportação e a
cobertura de ODS. O registro SHALL seguir gravado e consultável pela gestão e pelo Mestre.
(`RN-08-09`, `RN-08-12`, PRD-08 §§5.6, 12)

#### Scenario: Registro invalidado deixa de compor o painel público

- **WHEN** um registro que já compunha o agregado público da comunidade é invalidado
- **THEN** a consulta pública seguinte devolve o agregado sem ele

#### Scenario: Registro invalidado deixa de compor a exportação

- **WHEN** a exportação da comunidade é pedida depois da invalidação de um registro do período
- **THEN** o arquivo sai sem aquele registro no agregado
