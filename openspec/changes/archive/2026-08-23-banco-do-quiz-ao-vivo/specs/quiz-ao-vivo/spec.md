## MODIFIED Requirements

### Requirement: A pergunta de quiz é de múltipla escolha com quatro alternativas

O núcleo SHALL manter a **pergunta de quiz**, de autoria de um **Mestre**, com enunciado,
**exatamente quatro alternativas**, a indicação de qual delas é a correta e o **vínculo com a
missão a que ela se refere**, de onde a trilha decorre. A pergunta SHALL recusar número de
alternativas diferente de quatro, SHALL recusar o cadastro sem alternativa correta declarada e
SHALL recusar o cadastro sem a missão declarada. O núcleo NÃO SHALL guardar tempo-limite de
resposta: o ritmo é de quem conduz a partida. A pergunta NÃO SHALL ter situação: ela nasce
disponível e assim permanece — a anulação é da partida, nunca dela, e a mesma pergunta serve a
partidas diferentes. (`RF-09-36`, `RF-09-37`, `RF-09-38`, `RF-09-39`, `RF-01-36`, `RF-01-03`,
documento 05 §5, documento 09)

#### Scenario: Pergunta com quatro alternativas e uma correta é aceita

- **WHEN** um Mestre cadastra uma pergunta com enunciado, quatro alternativas, a correta
  indicada e a missão a que ela se refere
- **THEN** o núcleo grava a pergunta com a autoria, a data e a hora do cadastro, e com a
  trilha decorrente da missão

#### Scenario: Pergunta com três alternativas é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta com três alternativas
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

#### Scenario: Pergunta sem alternativa correta é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta sem indicar qual alternativa é a correta
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

#### Scenario: Pergunta sem missão declarada é recusada

- **WHEN** um Mestre tenta cadastrar uma pergunta sem declarar a missão a que ela se refere
- **THEN** o núcleo responde 422 e nenhuma pergunta é gravada

## ADDED Requirements

### Requirement: O Mestre lê o próprio banco de perguntas, filtrado por trilha e missão

O núcleo SHALL servir ao **Mestre em sessão** as perguntas de que ele é autor, e SHALL aceitar
o filtro por **trilha** e por **missão** para que ele monte o banco de uma aula. A leitura SHALL
devolver somente as perguntas do próprio Mestre: o banco de um Mestre NÃO SHALL aparecer para
outro. A leitura SHALL ser paginada pelas convenções do núcleo. (`RF-09-40`, `RF-09-41`,
`RF-01-16`)

#### Scenario: Mestre lê o próprio banco

- **WHEN** um Mestre consulta o seu banco de perguntas
- **THEN** o núcleo devolve, paginadas, as perguntas de que ele é autor, com enunciado,
  alternativas, alternativa correta, missão e trilha

#### Scenario: Filtro por missão devolve só as perguntas daquela missão

- **WHEN** um Mestre consulta o seu banco filtrando por uma missão
- **THEN** o núcleo devolve apenas as perguntas vinculadas àquela missão

#### Scenario: Filtro por trilha devolve as perguntas de todas as missões dela

- **WHEN** um Mestre consulta o seu banco filtrando por uma trilha
- **THEN** o núcleo devolve as perguntas vinculadas a qualquer missão daquela trilha

#### Scenario: O banco de um Mestre não aparece para outro

- **WHEN** um Mestre consulta o seu banco e existem perguntas cadastradas por outro Mestre
- **THEN** o núcleo devolve apenas as perguntas do Mestre em sessão

#### Scenario: Guerreiro(a) não alcança o banco de perguntas

- **WHEN** um Guerreiro(a) tenta ler o banco de perguntas
- **THEN** o núcleo responde 403 e nenhuma pergunta é devolvida
