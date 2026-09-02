## MODIFIED Requirements

### Requirement: O Guerreiro(a) lê os próprios desafios em aberto

O núcleo SHALL servir, em `GET /v1/eu/desafios`, o que o Guerreiro(a) **em sessão** tem em
aberto, em **dois conjuntos apartados**: os **semanais** e os **extras**.

Os **semanais** SHALL ser as **atividades em aberto** dele: as das missões que ele já
**desbloqueou**, nas trilhas em que está **inscrito**, e para as quais o Mestre ainda **não
lançou Resultado** para ele. Cada atividade SHALL trazer **modalidade** e **formato**, além do
título, da descrição, da produção esperada e da missão e trilha a que pertence.

Os **extras** SHALL ser os desafios extras publicados, vigentes e elegíveis a ele, na forma da
capacidade `desafio-extra`.

A leitura SHALL alcançar apenas o Guerreiro(a) da sessão, identificado pelo contexto e nunca
por identificador vindo do cliente, e NEVER SHALL devolver atividade de trilha em que ele não
está inscrito, de missão que ele ainda não desbloqueou nem atividade cujo Resultado já foi
lançado para ele. Guerreiro(a) sem nada em aberto SHALL receber **200** com os **dois conjuntos
vazios**, nunca erro. Persona que não é Guerreiro(a) SHALL receber **403**. (`RF-05-19`,
`RF-05-20`, `RN-05-21`, `RN-05-06`)

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

## ADDED Requirements

### Requirement: A App 05 mostra os desafios extras vigentes, apartados dos semanais

A App 05 SHALL apresentar ao Guerreiro(a), no bloco dos desafios e **apartados dos semanais**,
os **desafios extras vigentes** que lhe são elegíveis, cada um com a **recompensa oferecida**,
a **quantidade disponível**, o **período de vigência**, o **critério** para conquistá-la, o
**formato** — presencial ou on-line — e a trilha (e a missão, quando houver) a que se prende,
em linguagem da criança. O desafio **direcionado** SHALL ser apresentado como dirigido a ela,
sem nomear terceiro. Guerreiro(a) sem desafio extra elegível SHALL ver uma mensagem que diz
isso, e NEVER SHALL receber lista vazia sem explicação.

A tela SHALL dizer que os pontos do desafio extra são **extras** e não contam para o nível, e
NEVER SHALL oferecer concluir, disputar, comprar ou trocar o desafio: no Ciclo 01 a conclusão é
lançada fora desta aplicação. (`RF-05-20`, `RF-05-21`, `RN-05-18`, `RN-05-06`)

#### Scenario: Cada desafio extra diz recompensa, quantidade e vigência

- **WHEN** o Guerreiro(a) abre o bloco dos desafios e tem desafio extra elegível
- **THEN** vê cada um com a recompensa oferecida, a quantidade disponível, o período de
  vigência e o critério para conquistá-la

#### Scenario: Os extras não se misturam aos semanais

- **WHEN** o Guerreiro(a) tem desafio semanal e desafio extra ao mesmo tempo
- **THEN** a tela mostra os dois em blocos distintos, cada um identificado como o que é

#### Scenario: O esgotado continua visível, dizendo que acabou

- **WHEN** um desafio extra vigente já teve todas as recompensas entregues
- **THEN** ele continua na tela, marcado como esgotado, em vez de desaparecer sem explicação

#### Scenario: Sem desafio extra a tela explica

- **WHEN** o Guerreiro(a) não tem nenhum desafio extra elegível
- **THEN** a tela diz isso em linguagem simples, sem lista vazia muda

#### Scenario: A tela diz que o ponto extra não sobe nível

- **WHEN** o Guerreiro(a) vê os pontos que um desafio extra vale
- **THEN** a tela informa que são pontos extras e que não contam para o nível da trilha

#### Scenario: Nenhuma ação de concluir ou trocar é oferecida

- **WHEN** o Guerreiro(a) percorre os desafios extras
- **THEN** nenhuma ação de concluir, disputar, comprar ou trocar aparece
