## ADDED Requirements

### Requirement: O caminho das trilhas leva a equipe à programação do encontro

Escolhida a equipe do momento, a App 01 SHALL mostrar à equipe a **programação do encontro**:
para cada atividade presencial declarada naquela aula, a **missão** em que ela está, o
**conteúdo** da missão e a **atividade do dia**, com a bibliografia de apoio (`RF-04-35`,
jornada 5.8).

Havendo mais de uma atividade no encontro, a aplicação SHALL apresentá-las como **escolha da
equipe** — nenhuma é eleita pela aplicação, e a escolha NEVER SHALL ser enviada ao núcleo. É o
encontro assíncrono do documento 05 §4: cada equipe avança no seu ritmo.

A aplicação SHALL mostrar o conteúdo da missão nos tipos que o núcleo serve — texto formatado,
imagem, link externo, vídeo e arquivo de apoio —, com a **fonte** do conteúdo de terceiro e o
**crédito ao Mestre autor** que a trilha publicada declara. Encontro sem programação declarada
SHALL exibir aviso em linguagem simples, e não erro nem tela vazia.

Nenhuma tela deste caminho SHALL exibir dado pessoal de Guerreiro(a): a equipe segue
identificada por **avatar e nick**, como já vale para a tela das equipes (`RF-04-34`,
`RN-04-14`). (`RF-04-35`, `RF-04-29`, `RN-04-15`, documento 05 §4, PRD-04 §9)

#### Scenario: A equipe vê a missão, o conteúdo e a atividade do dia

- **WHEN** a equipe escolhida entra no caminho das trilhas num encontro com programação
  declarada
- **THEN** a aplicação mostra a missão, o conteúdo dela e a atividade do dia

#### Scenario: Duas atividades no encontro viram escolha da equipe

- **WHEN** a programação do encontro traz duas atividades, de trilhas diferentes
- **THEN** a aplicação apresenta as duas e a equipe escolhe, sem que a escolha seja enviada ao
  núcleo

#### Scenario: Encontro sem programação avisa em linguagem simples

- **WHEN** a equipe entra no caminho das trilhas e a programação do encontro está vazia
- **THEN** a aplicação avisa que o encontro ainda não tem atividade declarada, sem erro na tela

#### Scenario: O conteúdo de terceiro sai com a fonte

- **WHEN** a missão do dia tem conteúdo de terceiro
- **THEN** a aplicação exibe a fonte registrada junto do conteúdo

#### Scenario: Nenhum dado pessoal aparece no caminho das trilhas

- **WHEN** a equipe percorre as telas do caminho das trilhas
- **THEN** os integrantes aparecem apenas por avatar e nick, e nenhuma imagem de Guerreiro(a) é
  exibida

### Requirement: Sem rede, o conteúdo da missão já carregado continua legível

A App 01 SHALL manter legível, com a rede fora, o **conteúdo da missão já carregado** naquele
aparelho, para que a equipe siga trabalhando durante a queda. A aplicação NEVER SHALL exigir
nova chamada ao núcleo para reexibir o que já mostrou.

Com a rede fora, a aplicação SHALL avisar que a programação **não pode ser atualizada**, e
NEVER SHALL enfileirar leitura para reenvio — a programação é leitura, não fato a sincronizar.
(`RF-04-58`, documento 03 §3.4)

#### Scenario: A rede cai e o conteúdo segue na tela

- **WHEN** a rede cai enquanto a equipe lê o conteúdo da missão do dia
- **THEN** o conteúdo já carregado continua legível e a equipe segue trabalhando

#### Scenario: Sem rede, a programação não se atualiza e a aplicação avisa

- **WHEN** a equipe pede a programação do encontro com a rede fora
- **THEN** a aplicação avisa que não consegue atualizar agora e mantém o que já tinha

#### Scenario: Leitura não vai para fila

- **WHEN** a rede volta depois de a equipe ter navegado o conteúdo sem rede
- **THEN** a aplicação não envia nada ao núcleo por conta dessas leituras
