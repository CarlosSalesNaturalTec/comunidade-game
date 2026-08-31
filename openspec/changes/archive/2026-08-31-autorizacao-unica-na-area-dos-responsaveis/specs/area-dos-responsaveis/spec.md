## ADDED Requirements

### Requirement: A tela declara o que a autorização libera e o que não depende dela, antes do ato

A App 07 SHALL apresentar, **antes de qualquer botão de decisão**, o que a autorização única
libera — divulgação do perfil, do histórico e das criações, imagem em fotos e vídeos de eventos e
captação da produção por foto do manuscrito ou áudio — e o que **não** depende dela: a
participação nas atividades, que é livre, e a biometria do onboarding, que tem termo impresso
próprio. O texto SHALL estar em **linguagem simples de adulto**, sem jargão jurídico e sem código
de erro. A tela NEVER SHALL oferecer decisão separada por finalidade: a autorização é uma só.
(`RF-13-13`, `RN-13-05`, `RN-13-06`)

#### Scenario: A declaração vem antes da decisão

- **WHEN** o responsável abre a tela da autorização de um vinculado
- **THEN** o que a autorização libera e o que não depende dela aparecem antes de qualquer botão
  de conceder ou revogar

#### Scenario: Uma decisão só, para tudo

- **WHEN** o responsável percorre a tela da autorização
- **THEN** não há caminho de autorizar a divulgação sem a imagem em eventos, nem qualquer outra
  decisão por finalidade separada

### Requirement: O responsável concede e revoga pela tela, com o efeito dito no mesmo ato

A App 07 SHALL oferecer ao responsável **conceder** e **revogar** a autorização do vinculado
escolhido, e SHALL dizer, no mesmo ato, o efeito do que ele acaba de fazer: concedida, o perfil
passa a aparecer na vitrine e nos rankings públicos; revogada, perfil, criações e elenco do jogo
saem do que é público **na hora**, sem apagar nada e sem prejuízo da participação. A tela NEVER
SHALL sugerir que a revogação apaga registro ou tira a criança de atividade. (`RF-13-14`,
`RF-13-15`, `RF-13-16`, `RN-13-08`, `RN-13-09`)

Conceder e revogar **exigem rede**, porque geram registro versionado. Falhando a chamada, a App
07 SHALL dizer que a decisão **não foi registrada** e NEVER SHALL apresentar sucesso, apresentar
o estado novo ou dar a decisão por tomada. (PRD-13 §10)

#### Scenario: Concessão e o que ela produz

- **WHEN** o responsável concede a autorização de um vinculado
- **THEN** a tela passa a apresentar o estado vigente e diz que o perfil passa a aparecer na
  vitrine e nos rankings públicos

#### Scenario: Revogação e o que ela produz

- **WHEN** o responsável revoga a autorização de um vinculado
- **THEN** a tela diz que perfil, criações e elenco do jogo saem do que é público na hora, que
  nada é apagado e que a participação segue

#### Scenario: Sem rede, nada é dado por registrado

- **WHEN** a chamada da decisão falha por rede
- **THEN** a tela diz que a decisão não foi registrada, e o estado apresentado continua sendo o
  anterior

### Requirement: A tela informa a alternativa equivalente enquanto não houver autorização

A App 07 SHALL apresentar, sempre que a autorização do vinculado **não estiver vigente** — não
autorizada ou suspensa —, a **alternativa equivalente** em vigor: o Guerreiro(a) entrega a
produção ao Mestre no encontro, participa de tudo e não aparece publicamente. A tela NEVER SHALL
apresentar a ausência de autorização como perda, punição ou pendência da criança. (`RF-13-20`,
`RN-13-09`)

#### Scenario: Sem autorização, a alternativa aparece

- **WHEN** o responsável abre a tela de um vinculado sem autorização vigente
- **THEN** a tela apresenta a entrega da produção ao Mestre no encontro como alternativa, e diz
  que a criança participa de tudo

#### Scenario: A alternativa também vale no estado suspenso

- **WHEN** a autorização do vinculado está suspensa
- **THEN** a mesma alternativa equivalente é apresentada

### Requirement: O estado suspenso aparece com quem o motivou, data e hora

A App 07 SHALL apresentar os **três estados** da autorização do vinculado — vigente, suspensa e
não autorizada — em linguagem simples, e, estando **suspensa**, SHALL nomear **quem a motivou**
com a **data e a hora** daquela recusa, e dizer que a gestão vai tratar com a família. A tela
NEVER SHALL apresentar o estado suspenso como erro nem oferecer caminho de sobrepor a recusa do
outro responsável. (`RF-13-17`, `RF-13-18`, `RN-13-07`)

Recebendo a recusa do núcleo à concessão que colide com a recusa de outro responsável, a App 07
SHALL apresentar o estado suspenso e a **orientação de procurar a gestão**, nunca um código de
erro. (PRD-13 §§9, 10)

#### Scenario: Suspensa nomeia quem recusou

- **WHEN** o responsável abre a tela de um vinculado cuja autorização está suspensa
- **THEN** a tela diz que está suspensa, quem a motivou, quando, e que a gestão vai tratar com a
  família

#### Scenario: A concessão que colide vira orientação, não erro

- **WHEN** o responsável concede e o núcleo recusa porque outro responsável tem recusa vigente
- **THEN** a tela apresenta o estado suspenso e a orientação de procurar a gestão, sem código de
  erro

### Requirement: O histórico da autorização mostra cada decisão, com a versão do termo

A App 07 SHALL apresentar o **histórico da autorização** do vinculado — cada concessão e cada
revogação, do mais recente ao mais antigo, com **quem decidiu**, a **versão do termo**, a data e
a hora. A tela NEVER SHALL oferecer caminho de editar ou apagar decisão do histórico: o registro
é somente inserção. (`RF-13-21`, `RN-13-10`)

#### Scenario: Histórico de quem concedeu, revogou e concedeu de novo

- **WHEN** o responsável abre o histórico de um vinculado com três decisões registradas
- **THEN** as três aparecem, da mais recente à mais antiga, cada uma com quem decidiu, a versão
  do termo, a data e a hora

#### Scenario: Nada se apaga no histórico

- **WHEN** o responsável percorre o histórico
- **THEN** não há caminho de editar nem de apagar decisão alguma

### Requirement: O responsável alcança a autorização do vinculado sem sair da aplicação

A App 07 SHALL oferecer, do vinculado escolhido, o caminho entre a **evolução** e a
**autorização** sem encerrar a sessão e sem voltar à entrada, e SHALL manter a alternância entre
vinculados válida nas duas. A tela da autorização NEVER SHALL alcançar Guerreiro(a) não
vinculado. (`RF-13-05`, `RN-13-04`)

#### Scenario: Da evolução à autorização e de volta

- **WHEN** o responsável está na evolução de um vinculado e escolhe a autorização
- **THEN** a aplicação apresenta a autorização daquele vinculado, com a mesma sessão, e o
  caminho de volta à evolução

#### Scenario: Trocar de vinculado troca a autorização apresentada

- **WHEN** o responsável está na autorização de um vinculado e escolhe outro
- **THEN** a aplicação passa a apresentar a autorização do segundo
