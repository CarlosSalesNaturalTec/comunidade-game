## MODIFIED Requirements

### Requirement: Valor fora da faixa esperada é aceito e marcado "a conferir"

O núcleo SHALL **aceitar e gravar** o registro cujo valor cai fora da **faixa esperada** —
mínimo e máximo — do tipo de coleta, e SHALL marcá-lo **"a conferir"**. A marca SHALL valer
qualquer que seja a origem do registro. O registro marcado "a conferir" NEVER SHALL creditar
ponto na gravação: ele entra obrigatoriamente na amostra de auditoria do Mestre, e é a
**confirmação** dele que o credita. O núcleo SHALL informar na resposta da gravação que aquele
registro não pontuou. Tipo sem faixa declarada NEVER SHALL produzir a marca. (`RF-08-12`,
`RN-08-26`, PRD-08 §5.3)

#### Scenario: Valor acima do máximo entra a conferir

- **WHEN** chega uma medição de valor acima do máximo da faixa esperada do tipo
- **THEN** o núcleo grava o registro, marca-o "a conferir", credita zero e responde indicando que
  ele não pontuou

#### Scenario: Valor abaixo do mínimo entra a conferir

- **WHEN** chega uma medição de valor abaixo do mínimo da faixa esperada do tipo
- **THEN** o núcleo grava o registro, marca-o "a conferir" e credita zero

#### Scenario: Valor dentro da faixa não recebe a marca

- **WHEN** chega uma medição de valor dentro da faixa esperada do tipo
- **THEN** o núcleo grava o registro sem a marca "a conferir"

#### Scenario: Tipo sem faixa declarada não produz a marca

- **WHEN** chega uma medição numa série cujo tipo de coleta não declara faixa esperada
- **THEN** o núcleo grava o registro sem a marca "a conferir"

### Requirement: O registro é somente inserção e o vínculo com o coletor é permanente

O núcleo NEVER SHALL apagar nem editar registro gravado: **valor**, **data da medição** e
**coletor** SHALL ser imutáveis depois de gravados, e a **situação** SHALL ser o único campo que
evolui. A situação SHALL evoluir apenas pelos atos da auditoria do Mestre — **confirmação** e
**invalidação** —, e a invalidação SHALL ser **terminal**. Rota de alteração e rota de exclusão
de registro NEVER SHALL existir; a correção se faz por invalidação e novo registro. O vínculo
entre registro e Guerreiro(a) coletor(a) SHALL ser **permanente**, inclusive depois da saída dele
do projeto. (`RN-08-10`, `RN-08-11`, `RF-08-13`, `RF-08-29`, invariante 7 do documento 99 §6,
PRD-08 §8)

#### Scenario: Não há rota de alteração de registro

- **WHEN** chega uma requisição para alterar o valor de um registro gravado
- **THEN** o núcleo responde 405 e o registro permanece como estava

#### Scenario: Não há rota de exclusão de registro

- **WHEN** chega uma requisição para apagar um registro gravado
- **THEN** o núcleo responde 405 e o registro permanece gravado

#### Scenario: A invalidação não apaga a medição

- **WHEN** um registro é invalidado na auditoria
- **THEN** valor, data da medição e coletor seguem gravados e inalterados, e só a situação mudou

#### Scenario: O coletor permanece no registro depois da saída do projeto

- **WHEN** o vínculo de um Guerreiro(a) com a comunidade é encerrado
- **THEN** os registros que ele gravou seguem apontando para ele como coletor
