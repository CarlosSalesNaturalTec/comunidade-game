## MODIFIED Requirements

### Requirement: A ocorrência é somente inserção e o motivo tem guarda pelo ciclo

O núcleo SHALL tratar a ocorrência de conduta como registro **somente inserção**: alterar ou
remover uma ocorrência gravada SHALL ser recusado. A correção se faz por ocorrência nova, nunca
por edição.

O **motivo** SHALL ter guarda limitada ao **ciclo em que a ocorrência aconteceu**, e o campo
SHALL ser anulável para que apagá-lo não apague o lançamento. Apagado o motivo, a ocorrência
SHALL permanecer consultável com **valor, data e autor**, e nenhuma rota SHALL devolver o motivo
apagado. (`RF-09-46`, `RN-01-52`, `RF-01-57`, 03 §12.2)

Quem apaga o motivo é o **encerramento do ciclo**, e mais nada: o expurgo SHALL alcançar todas
as ocorrências que ainda guardam motivo, e NEVER SHALL ser exposto como ato avulso sobre uma
ocorrência. A anulação do motivo é a **única** alteração que a regra de somente inserção
admite; toda outra SHALL continuar recusada, inclusive fora do ORM. (`RF-02-100`)

#### Scenario: Ocorrência gravada não se altera

- **WHEN** qualquer operação tenta alterar ou remover uma ocorrência de conduta já gravada
- **THEN** o núcleo recusa a operação

#### Scenario: Ocorrência sem motivo guardado não o devolve

- **WHEN** uma ocorrência de conduta cujo motivo já foi apagado é lida em qualquer rota
- **THEN** a saída traz valor, data e autor, e não traz o motivo

#### Scenario: Apagar o motivo não desfaz o débito

- **WHEN** o motivo de uma ocorrência de conduta é apagado
- **THEN** o saldo de ponto regular do Guerreiro(a) permanece como ficou depois do débito

#### Scenario: O encerramento do ciclo expurga os motivos guardados

- **WHEN** o encerramento do ciclo é executado e há ocorrências de conduta com motivo guardado
- **THEN** o motivo de todas elas é anulado, e cada lançamento permanece com valor, data e autor

#### Scenario: O expurgo não altera nada além do motivo

- **WHEN** o expurgo do encerramento do ciclo alcança uma ocorrência de conduta
- **THEN** valor, data, autor, aula, atividade e Guerreiro(a) daquela ocorrência permanecem
  como estavam

#### Scenario: Não há como apagar o motivo de uma ocorrência isolada

- **WHEN** qualquer operação tenta anular o motivo de uma ocorrência de conduta fora do
  encerramento do ciclo
- **THEN** o núcleo recusa a operação
