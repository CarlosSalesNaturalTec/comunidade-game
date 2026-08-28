## ADDED Requirements

### Requirement: A App 03 abre a área Acervo sob a comunidade escolhida

A App 03 SHALL abrir a área **Acervo** com a escolha da comunidade, e SHALL apresentar os
exemplares permanentes ali tombados em **lista densa**, cada um com **título**, **número de
tombo**, **ponto de apoio**, **estado de conservação corrente** e o **responsável designado**
pelo acervo daquele ponto de apoio, com o **nome** e não com o identificador. O exemplar de
ponto de apoio ainda sem responsável SHALL aparecer assim mesmo, com a ausência apresentada como
informação e nunca como falha. A área NEVER SHALL apresentar valor em reais. Sem exemplar
tombado, a área SHALL dizê-lo em texto próprio, e NEVER SHALL apresentar lista vazia sem
explicação. (`RF-02-52`, `RF-02-53`, `RN-02-19`, PRD-02 §6.5)

#### Scenario: A área apresenta os exemplares da comunidade

- **WHEN** um Admin em sessão escolhe uma comunidade na área Acervo
- **THEN** vêm os exemplares tombados nos pontos de apoio daquela comunidade, cada um com
  título, número de tombo, ponto de apoio, estado de conservação e o nome do responsável

#### Scenario: Exemplar sem responsável designado aparece assim mesmo

- **WHEN** a lista traz exemplar de ponto de apoio ainda sem responsável pelo acervo
- **THEN** ele aparece, a ausência é apresentada como informação e nada é sinalizado como erro

#### Scenario: Comunidade sem acervo tem texto próprio

- **WHEN** a comunidade escolhida não tem exemplar tombado
- **THEN** a área diz que não há acervo tombado ali, sem apresentar lista vazia

#### Scenario: O Mestre lê o acervo das suas comunidades

- **WHEN** um Mestre em sessão abre a área Acervo
- **THEN** ele lê o acervo, e a recusa do núcleo às comunidades a que não está vinculado é
  apresentada em linguagem simples

### Requirement: O Admin tomba o exemplar permanente pela aplicação

A App 03 SHALL oferecer ao Admin o **tombamento** do exemplar permanente, informando **título**,
**número de tombo**, **ponto de apoio** e **estado de conservação**. A aplicação SHALL apontar o
campo em falta no próprio campo, sem enviar nada ao núcleo, e SHALL apresentar em linguagem
simples a recusa do núcleo ao **número de tombo já usado naquele ponto de apoio**, nunca como
código de erro cru. O caminho do tombamento NEVER SHALL ser oferecido a quem não é Admin.
(`RF-02-52`, `RN-02-21`, PRD-02 §6.5)

#### Scenario: Admin tomba um exemplar

- **WHEN** um Admin informa título, número de tombo, ponto de apoio e estado de conservação e
  confirma
- **THEN** o exemplar passa a existir e aparece na lista do acervo daquela comunidade

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma o tombamento com um dos quatro campos vazio
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

#### Scenario: Tombo repetido é explicado

- **WHEN** o núcleo recusa o tombamento porque o número de tombo já existe naquele ponto de
  apoio
- **THEN** a aplicação diz isso em linguagem simples, e o que foi digitado permanece na tela

#### Scenario: Mestre não tomba

- **WHEN** um Mestre em sessão abre a área Acervo
- **THEN** o caminho do tombamento não lhe é oferecido

### Requirement: A ficha de vida do exemplar é lida na ordem do tempo

A App 03 SHALL apresentar, em cada exemplar, a sua **ficha de vida** completa, da anotação mais
antiga à mais recente, cada anotação com o **teor** — cuidado, perda ou dano —, o **estado de
conservação apurado**, **quem anotou** e **quando**. A aplicação NEVER SHALL oferecer caminho de
editar nem de remover anotação já gravada. Exemplar sem anotação SHALL dizê-lo em texto próprio.
(`RF-02-53`, `RN-02-21`, PRD-02 §6.5)

#### Scenario: A ficha vem completa e em ordem

- **WHEN** o Admin abre um exemplar com várias anotações
- **THEN** todas aparecem, da mais antiga à mais recente, com teor, estado de conservação, autor
  e data e hora

#### Scenario: Não há como editar nem apagar anotação

- **WHEN** a ficha de vida de um exemplar é apresentada
- **THEN** nenhuma anotação oferece caminho de edição ou de remoção

#### Scenario: Exemplar sem anotação

- **WHEN** o Admin abre um exemplar recém-tombado
- **THEN** a ficha diz que ainda não há anotação, sem apresentar lista vazia

### Requirement: A anotação de perda ou dano não cobra de ninguém

A App 03 SHALL oferecer ao **Admin** e ao **Mestre** a anotação na ficha de vida, com o **teor**
— cuidado, perda ou dano — e o **estado de conservação apurado**. A tela da anotação de **perda**
ou **dano** SHALL dizer que o fato não gera débito ao Guerreiro(a) nem à família, e NEVER SHALL
oferecer campo para identificar um Guerreiro(a) responsável pelo fato nem caminho algum de
cobrança. O caminho NEVER SHALL ser oferecido a Apoiador, Guerreiro(a) ou responsável.
(`RF-02-55`, `RN-02-14`, `RN-02-15`, `RN-02-16`, PRD-02 §7, documento 05 §3.6)

#### Scenario: Mestre anota o cuidado do exemplar

- **WHEN** um Mestre em sessão anota o cuidado de um exemplar com o estado de conservação
  apurado
- **THEN** a anotação passa a existir e aparece na ficha de vida, com o nome dele

#### Scenario: A perda não pede culpado

- **WHEN** o Admin escolhe o teor perda ou dano
- **THEN** a tela diz que nada é debitado ao Guerreiro(a) nem à família, e nenhum campo pede um
  Guerreiro(a) responsável pelo fato

#### Scenario: Estado de conservação em falta

- **WHEN** a anotação é confirmada sem o estado de conservação apurado
- **THEN** a aplicação aponta o campo em falta e nada é enviado ao núcleo

### Requirement: A área Acervo não oferece saída do exemplar

A área Acervo NEVER SHALL oferecer **retirada**, **empréstimo**, **devolução** nem
**transferência** de exemplar entre pontos de apoio: no Ciclo 01 o exemplar permanece onde foi
tombado. (`RN-02-18`, PRD-02 §3.2, documento 05 §3.2)

#### Scenario: Nenhum caminho tira o exemplar do lugar

- **WHEN** um Admin abre um exemplar na área Acervo
- **THEN** nenhuma ação de retirada, empréstimo, devolução ou transferência lhe é oferecida

### Requirement: O Admin designa o responsável pelo acervo do ponto de apoio

A App 03 SHALL oferecer ao Admin **designar e trocar** o responsável pelo acervo de um ponto de
apoio, escolhendo entre os **Mestres** e **Apoiadores** cadastrados, e a lista de pontos de apoio
SHALL passar a apresentar o **nome** do designado. A troca SHALL substituir o anterior. O caminho
NEVER SHALL ser oferecido a quem não é Admin, e a recusa do núcleo SHALL ser apresentada em
linguagem simples. (`RF-02-52`, `RF-07-49`, `RN-07-34`, PRD-02 §6.5)

#### Scenario: Admin designa um Mestre

- **WHEN** um Admin escolhe um Mestre como responsável pelo acervo de um ponto de apoio e
  confirma
- **THEN** a lista passa a apresentar o nome dele, e o acervo daquele ponto de apoio também

#### Scenario: A troca substitui o anterior

- **WHEN** o Admin designa outro responsável para ponto de apoio que já tinha um
- **THEN** a lista passa a apresentar o novo, e o anterior não aparece mais como designado

#### Scenario: Mestre não designa

- **WHEN** um Mestre em sessão abre a área Pontos de Apoio
- **THEN** o caminho da designação não lhe é oferecido

## MODIFIED Requirements

### Requirement: O Admin cadastra o ponto de apoio da comunidade

A App 03 SHALL permitir ao Admin cadastrar o ponto de apoio informando **nome** e a
**comunidade** a que ele pertence, e SHALL apresentar os pontos de apoio já cadastrados antes
de oferecer o cadastro, para que ele saiba o que já há. A apresentação SHALL ser **lista
densa**, no temperamento Operação, como a das comunidades.

O ponto de apoio SHALL nascer **sem responsável pelo acervo**, e a aplicação NEVER SHALL
apresentar essa ausência como falha: a designação é ato posterior, oferecido na própria área.
(`RF-07-47`, `RF-07-49`, `RN-07-34`, documento 15 §6)

#### Scenario: Admin cadastra o ponto de apoio

- **WHEN** um Admin em sessão informa nome e comunidade e confirma
- **THEN** o ponto de apoio passa a existir e a aplicação o apresenta entre os existentes

#### Scenario: Campo obrigatório em falta

- **WHEN** o Admin confirma o cadastro com nome ou comunidade vazios
- **THEN** a aplicação aponta o campo em falta, no próprio campo, e nenhum ponto de apoio
  passa a existir

#### Scenario: Ponto de apoio sem responsável não é apresentado como pendência

- **WHEN** a lista apresenta um ponto de apoio ainda sem responsável pelo acervo
- **THEN** a ausência aparece como informação, e não como aviso de erro

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área de pontos de apoio
- **THEN** o caminho de cadastro não lhe é oferecido, e a recusa do núcleo, se ocorrer, é
  apresentada em linguagem simples
