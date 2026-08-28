## ADDED Requirements

### Requirement: Toda tela que grava dado pessoal avisa o que ali se coleta

A aplicação SHALL exibir um **aviso discreto** do que está sendo coletado em toda tela em que a
gestão grava dado pessoal — o cadastro de Guerreiro(a), de Mestre, de Apoiador, de Admin e de
responsável; a conferência de presença; o lançamento do desfecho da atividade; o registro de
infração; o anexo da digitalização do termo; e a avaliação da solicitação de participação e da
solicitação de dados. Cada aviso SHALL nomear o dado daquela tela, na linha correspondente da
tabela do PRD-02 §11, e SHALL oferecer o acesso à área detalhada de direitos. O aviso NEVER
SHALL bloquear a tela, NEVER SHALL exigir confirmação para continuar e NEVER SHALL impedir o
envio do formulário. (`RF-02-64`, PRD-02 §11, documento 03 §12)

#### Scenario: A tela de cadastro traz o aviso

- **WHEN** o Admin abre o cadastro de Guerreiro(a)
- **THEN** um aviso discreto informa o que aquela tela coleta e dá acesso à área detalhada de
  direitos

#### Scenario: A tela de lançamento traz o aviso do dado dela

- **WHEN** o Admin abre o lançamento do desfecho da atividade ou o registro de infração
- **THEN** o aviso nomeia o dado daquela tela, e não o de outra

#### Scenario: O aviso não atrapalha o uso

- **WHEN** o aviso está exibido numa tela de cadastro ou de lançamento
- **THEN** a gestão preenche e envia o formulário sem confirmar o aviso, e nada na tela fica
  bloqueado por ele

### Requirement: A App 03 abre a área Direitos e dados, em leitura

A aplicação SHALL oferecer uma área **Direitos e dados**, alcançável pelo menu e por todo aviso
de coleta, que apresenta, para cada dado que a gestão coleta, a **finalidade**, a **base legal**,
o **prazo de retenção** e **quem acessa**, conforme a tabela do PRD-02 §11. A área SHALL
declarar também que a gestão não vê a imagem do Guerreiro(a), que o responsável exerce os
direitos pela App 07, que o registro de dado do território é **despersonalizado e não apagado**,
e que a infração fica restrita à gestão e ao responsável daquele Guerreiro(a). A área é de
**leitura**: NEVER SHALL oferecer escrita, exclusão ou exportação de dado. (`RF-02-64`,
PRD-02 §11)

#### Scenario: A área apresenta o destino de cada dado

- **WHEN** o Admin abre a área Direitos e dados
- **THEN** vê, para cada dado coletado, a finalidade, a base legal, o prazo de retenção e quem
  acessa

#### Scenario: O aviso leva à área

- **WHEN** a gestão aciona o acesso à área detalhada a partir do aviso de uma tela que coleta
- **THEN** chega à área Direitos e dados

#### Scenario: A área diz que o dado do território não se apaga

- **WHEN** o Admin lê a área Direitos e dados
- **THEN** encontra declarado que o registro de dado do território é despersonalizado, não
  apagado

### Requirement: Consentimento recusado não retira o Guerreiro(a) do lançamento

A aplicação NEVER SHALL usar a recusa ou a revogação de um consentimento para deixar um
Guerreiro(a) de fora do lançamento, da conferência de presença ou do registro de infração. A
lista dessas telas SHALL ser a do encontro inteiro, sem filtro por consentimento, e a aplicação
NEVER SHALL oferecer caminho que exclua alguém da atividade por causa da decisão do
responsável. (`RN-02-23`, PRD-01 `RN-01-21`, invariante 11 do documento 99 §6)

#### Scenario: Quem não tem autorização aparece no lançamento

- **WHEN** o Admin abre o lançamento de um encontro em que há Guerreiro(a) cujo responsável
  recusou a autorização
- **THEN** esse Guerreiro(a) aparece na lista como qualquer outro, e o desfecho dele é lançado
  normalmente

#### Scenario: A tela não oferece excluir por consentimento

- **WHEN** a gestão percorre o lançamento, a conferência de presença e o registro de infração
- **THEN** nenhuma delas oferece filtro, marcação ou ação que retire alguém por causa do
  consentimento

### Requirement: A autoria da trilha é do Mestre, e a gestão não oferece caminho para ela

A aplicação NEVER SHALL oferecer ao Admin cadastrar ou editar trilha, missão, conteúdo da
missão, atividade de missão, recompensa de marco ou desafio de coleta — a autoria é do Mestre,
na App 09. A área Atividades SHALL cadastrar **apenas atividade avulsa, fora de trilha**, e a
área Território SHALL apresentar os desafios de coleta publicados **em leitura**. Onde a
fronteira se confunde, a tela SHALL dizer, em uma linha, que aquilo se faz na App 09.
(`RN-02-24`, PRD-02 §§3.2, 4)

#### Scenario: A gestão não cadastra trilha nem missão

- **WHEN** o Admin percorre as áreas da App 03
- **THEN** não encontra caminho para criar ou editar trilha, missão, conteúdo, atividade de
  missão, recompensa de marco ou desafio de coleta

#### Scenario: A área Atividades diz o que cadastra e o que não cadastra

- **WHEN** o Admin abre a área Atividades
- **THEN** a tela cadastra atividade avulsa e diz, em uma linha, que a atividade de missão é
  autoria do Mestre, na App 09

#### Scenario: O desafio de coleta é só leitura

- **WHEN** o Admin abre os desafios de coleta publicados na área Território
- **THEN** os lê sem qualquer caminho de criação ou edição
