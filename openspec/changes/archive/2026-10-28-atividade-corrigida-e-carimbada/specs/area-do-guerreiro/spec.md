# Spec Delta

## MODIFIED Requirements

### Requirement: O Guerreiro(a) lê os próprios desafios em aberto

O núcleo SHALL servir, em `GET /v1/eu/desafios`, o que o Guerreiro(a) **em sessão** tem em
aberto, em **dois conjuntos apartados**: os **semanais** e os **extras**.

Os **semanais** SHALL ser as **atividades em aberto** dele: as das missões que ele já
**desbloqueou**, nas trilhas em que está **inscrito**, e para as quais o Mestre ainda **não
lançou Resultado** para ele. Cada atividade SHALL trazer **modalidade** e **formato**, além do
título, da descrição, da produção esperada e da missão e trilha a que pertence.

Atividade **carimbada** pelo Mestre autor NEVER SHALL entrar nos semanais: ela foi removida da
missão e não há mais o que o Guerreiro(a) entregue por ela. Sem essa exclusão a subtração pelo
Resultado lançado nunca a alcançaria — atividade removida antes de qualquer lançamento ficaria
na lista para sempre (`RN-09-47`).

Os **extras** SHALL ser os desafios extras publicados, vigentes e elegíveis a ele, na forma da
capacidade `desafio-extra`.

A leitura SHALL alcançar apenas o Guerreiro(a) da sessão, identificado pelo contexto e nunca
por identificador vindo do cliente, e NEVER SHALL devolver atividade de trilha em que ele não
está inscrito, de missão que ele ainda não desbloqueou nem atividade cujo Resultado já foi
lançado para ele. Guerreiro(a) sem nada em aberto SHALL receber **200** com os **dois conjuntos
vazios**, nunca erro. Persona que não é Guerreiro(a) SHALL receber **403**. (`RF-05-19`,
`RF-05-20`, `RN-05-21`, `RN-05-06`, `RN-09-47`)

#### Scenario: As atividades das missões desbloqueadas são devolvidas

- **WHEN** um Guerreiro(a) em sessão consulta os próprios desafios e tem missões desbloqueadas
  com atividades sem Resultado lançado
- **THEN** o núcleo devolve essas atividades no conjunto dos semanais, cada uma com modalidade
  e formato

#### Scenario: Atividade de missão ainda bloqueada não aparece

- **WHEN** existe atividade numa missão que o Guerreiro(a) ainda não desbloqueou
- **THEN** essa atividade não entra na leitura

#### Scenario: Atividade já lançada pelo Mestre sai da lista

- **WHEN** o Mestre lança o Resultado do Guerreiro(a) numa atividade que estava em aberto
- **THEN** a leitura seguinte não a devolve mais

#### Scenario: Atividade de trilha em que não se inscreveu não aparece

- **WHEN** existe atividade em trilha na qual o Guerreiro(a) não está inscrito
- **THEN** essa atividade não entra na leitura

#### Scenario: Os dois conjuntos vêm apartados na mesma resposta

- **WHEN** o Guerreiro(a) em sessão tem atividade em aberto e desafio extra elegível
- **THEN** a resposta traz a atividade entre os semanais e o desafio extra entre os extras, sem
  misturar os dois conjuntos

#### Scenario: Sem nada em aberto a resposta é conjunto vazio

- **WHEN** o Guerreiro(a) em sessão não tem nenhuma atividade em aberto nem desafio extra
  elegível
- **THEN** o núcleo responde 200 com os dois conjuntos vazios, nunca erro

#### Scenario: Persona que não é Guerreiro(a) não lê

- **WHEN** um Mestre, Admin, Apoiador ou responsável em sessão consulta a rota
- **THEN** o núcleo responde 403 e nada é devolvido

#### Scenario: Atividade removida pelo Mestre sai dos semanais

- **WHEN** o Mestre autor remove uma atividade de missão que o Guerreiro(a) já desbloqueou, sem
  que houvesse Resultado lançado
- **THEN** ela deixa de aparecer entre os semanais dele
