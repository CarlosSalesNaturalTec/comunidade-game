## MODIFIED Requirements

### Requirement: O ranking público ordena por ponto regular e alcança só quem autorizou

O núcleo SHALL montar o ranking público a partir do **ponto regular** já creditado, e SHALL
incluir nele **apenas** Guerreiros e Guerreiras com autorização de divulgação vigente. A posição
SHALL ser calculada sobre o conjunto exibido, de modo que a exclusão de quem não autorizou não
abra buraco na numeração. O ranking SHALL aceitar filtro por comunidade e SHALL ser paginado,
como toda listagem. (`RF-01-21`, `RF-01-28`, `RN-01-10`, PRD-03 §9)

O ranking NEVER SHALL contar o débito das **ocorrências de conduta de ciclo já encerrado**: a
ocorrência sai do ranking ao fim do ciclo. O débito SHALL permanecer no saldo de ponto regular
do Guerreiro(a), porque o débito não desfaz percurso, e o lançamento SHALL permanecer
consultável pela gestão e pelo responsável. (`RF-02-100`, documento 11 §5)

#### Scenario: Ranking ordena por ponto regular

- **WHEN** uma consulta pública pede o ranking
- **THEN** os Guerreiros e Guerreiras vêm ordenados pelo ponto regular acumulado

#### Scenario: Quem não autorizou fica fora e a numeração não pula

- **WHEN** um Guerreiro(a) sem autorização teria a segunda maior pontuação
- **THEN** ele não aparece, e quem vem depois dele ocupa a segunda posição

#### Scenario: Ranking filtra por comunidade

- **WHEN** uma consulta pública pede o ranking de uma comunidade
- **THEN** a resposta traz apenas Guerreiros e Guerreiras daquela comunidade

#### Scenario: Ocorrência de ciclo encerrado não pesa no ranking

- **WHEN** o ranking é consultado depois do encerramento do ciclo, para um Guerreiro(a) que
  sofreu ocorrência de conduta naquele ciclo
- **THEN** a posição dele é calculada sem o débito daquela ocorrência

#### Scenario: Ocorrência do ciclo corrente segue pesando

- **WHEN** o ranking é consultado e há ocorrência de conduta lançada depois do último
  encerramento de ciclo
- **THEN** o débito daquela ocorrência continua contando na posição

#### Scenario: Sair do ranking não devolve ponto ao saldo

- **WHEN** o encerramento do ciclo tira do ranking a ocorrência de um Guerreiro(a)
- **THEN** o saldo de ponto regular dele permanece como ficou depois do débito
