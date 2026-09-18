## ADDED Requirements

### Requirement: A captura se prepara antes de reprovar, e a falha de preparo se diz distinta

A App 01 SHALL preparar a câmera e os modelos de biometria **antes** de julgar a vivacidade, e
SHALL distinguir na tela, com frases diferentes, **três desfechos que hoje se confundem**: o
preparo que não se concluiu, a vivacidade que reprovou e a recusa do núcleo. Preparo que falhou
NEVER SHALL ser apresentado como ausência de pessoa diante da câmera. (`RF-04-65`, `RF-04-13`,
`RF-04-48`, documento 03 §3.3)

A preparação SHALL concluir em **aparelho sem aceleração gráfica disponível** — o aparelho do
ponto de apoio é modesto, e a aplicação não escolhe o hardware do encontro. (`RF-04-65`,
documento 03 §3.2)

A distinção NEVER SHALL alcançar a **recusa do núcleo**, que segue indistinguível entre nick
inexistente, Guerreiro(a) sem _template_ e descritor que não confere. (`RF-04-20`, `RN-01-22`)

#### Scenario: Preparo que falha não vira reprovação de vivacidade

- **WHEN** os modelos de biometria não chegam a carregar no aparelho
- **THEN** a tela diz que a captura não pôde ser preparada, com frase distinta da reprovação de
  vivacidade, e não afirma que não há pessoa diante da câmera

#### Scenario: Aparelho sem aceleração gráfica captura do mesmo jeito

- **WHEN** a captura é aberta em aparelho cujo navegador não disponibiliza aceleração gráfica
- **THEN** o preparo conclui, os modelos carregam e a captura acontece

#### Scenario: A recusa do núcleo continua sem revelar a causa

- **WHEN** o núcleo recusa a abertura da sessão por nick e imagem
- **THEN** a frase apresentada segue a mesma para nick inexistente, Guerreiro(a) sem _template_
  e descritor que não confere

## MODIFIED Requirements

### Requirement: O Guerreiro(a) entra por nick e imagem, e a presença é registrada na entrada

A App 01 SHALL oferecer, no caminho das trilhas, a entrada por **nick e imagem**: o nick
informado na tela e o **descritor gerado no próprio aparelho**, na ordem prova de vivacidade e
depois descritor facial. Ao núcleo SHALL ir apenas o descritor; a fotografia SHALL ser
descartada sem sair do aparelho e NEVER SHALL ser gravada nem enviada.

A tela SHALL apresentar o **visor ao vivo** da câmera enquanto a captura acontece, e SHALL
detectar **em laço** até a vivacidade passar ou o tempo se esgotar, em vez de julgar um único
quadro. O **quadro capturado** NEVER SHALL voltar à tela. (`RF-04-64`, `RN-04-34`)

Reconhecido o Guerreiro(a), a aplicação SHALL abrir a sessão dele e SHALL registrar a
**presença do dia no modo reconhecimento**, no mesmo atendimento. Presença já constante do
encontro NEVER SHALL ser duplicada nem tratada como erro: a aplicação SHALL avisar que ela já
existe e voltar à tela inicial. (`RF-04-18`, `RF-04-19`, `RF-04-29`, `RN-04-12`, `RN-04-06`,
PRD-04 §5.4)

#### Scenario: Nick e imagem conferem

- **WHEN** o Guerreiro(a) informa o nick e a câmera captura a imagem dele na chegada
- **THEN** a aplicação abre a sessão do Guerreiro(a) e registra a presença do dia por
  reconhecimento

#### Scenario: A presença do encontro já constava

- **WHEN** um Guerreiro(a) já com presença registrada naquela aula é reconhecido de novo
- **THEN** a aplicação avisa que a presença já existe, não duplica registro algum e volta à
  tela inicial

#### Scenario: Nenhuma imagem de criança sai do aparelho

- **WHEN** a entrada por nick e imagem acontece
- **THEN** nenhuma requisição carrega fotografia, e nenhuma imagem fica gravada no aparelho
  compartilhado

#### Scenario: Quem chega se vê no visor antes de a captura julgar

- **WHEN** a entrada por nick e imagem abre a câmera
- **THEN** o visor ao vivo aparece na tela, e a detecção segue em laço até aprovar ou o tempo
  se esgotar

#### Scenario: Sem câmera, a entrada segue pela confirmação humana

- **WHEN** o aparelho não tem câmera disponível
- **THEN** a aplicação não oferece a captura e encaminha o Guerreiro(a) à confirmação de Mestre
  ou Admin, sem deixá-lo fora da aula

### Requirement: O descritor nasce no aparelho, depois da prova de vivacidade

A App 01 SHALL gerar o _template_ no **navegador do próprio aparelho**, na ordem **prova de
vivacidade e, depois, descritor facial**, e SHALL enviar ao núcleo **apenas o descritor**. A
aplicação NEVER SHALL pôr a fotografia em corpo de requisição, em registro de erro ou em
armazenamento do aparelho. A fotografia SHALL ser descartada na geração do descritor.
(`RF-04-14`, `RF-04-48`, `RN-04-06`, `RN-04-08`, `RN-04-12`, `RN-04-14`, documento 03 §3.3,
documento 99 §6 invariante 12)

A tela SHALL apresentar o **visor ao vivo** da câmera — que mostra a pessoa a si mesma antes de
existir captura, não guarda e não reexibe — e SHALL confirmar por **retorno abstrato** que há
rosto enquadrado e que a vivacidade passou. A **imagem capturada** NEVER SHALL ser exibida, em
tela alguma, antes ou depois de gerar o descritor: quadro congelado devolvido à tela é proibido.
(`RF-04-64`, `RN-04-34`, documento 03 §3.3, documento 99 §6 invariante 12)

A detecção SHALL correr **em laço** até a vivacidade passar ou o tempo se esgotar, e NEVER SHALL
julgar um único quadro colhido no instante do acionamento. (`RF-04-64`)

A garantia de que o descritor veio de um rosto presente é **também presencial** — aula agendada,
aparelho do ponto de apoio e Mestre ou Admin na sala —, porque o descritor nasce em código que
roda no aparelho e o núcleo não tem como reconferi-la. (documento 03 §3.3)

#### Scenario: Nenhuma requisição carrega imagem

- **WHEN** a captura é concluída e o descritor é enviado
- **THEN** o corpo da requisição carrega apenas o descritor, e nenhuma imagem aparece em
  requisição, em registro de erro ou no armazenamento do aparelho

#### Scenario: A fotografia não sobrevive à captura

- **WHEN** o descritor é gerado
- **THEN** a fotografia original é descartada no aparelho e não existe em lugar nenhum

#### Scenario: O visor mostra a pessoa a si mesma

- **WHEN** a captura do onboarding abre a câmera
- **THEN** o visor ao vivo aparece na tela, e o retorno de rosto enquadrado e de vivacidade
  confirmada é abstrato, nunca a fotografia

#### Scenario: O quadro capturado não volta à tela

- **WHEN** o descritor é gerado a partir do quadro aprovado
- **THEN** nenhuma tela apresenta aquele quadro, nem antes nem depois da geração

### Requirement: O Mestre mede no aparelho a distância entre descritores

A App 01 SHALL oferecer ao **Mestre ou ao Admin em sessão de trabalho** uma tela que captura
descritores no aparelho, compara-os entre si e apresenta a **distância** na mesma unidade que o
núcleo usa para comparar — a medição que calibra o limiar de comparação. A tela NEVER SHALL
enviar descritor, imagem ou distância ao núcleo: a medição inteira acontece no aparelho, e o
que sai dela é o **número lido na tela** por quem opera. (`RF-04-63`, documento 03 §3.3)

A tela SHALL guardar **um** descritor de referência por vez. Cada captura seguinte SHALL ser
comparada com ele e **descartada no mesmo ato** — os dois coexistem apenas durante o cálculo —,
e a tela NEVER SHALL apresentar nem persistir o descritor, só a distância. (`RN-04-32`,
documento 99 §6 invariante 12)

A tela SHALL apresentar o **visor ao vivo** enquanto captura, com o mesmo retorno abstrato das
demais telas de câmera, e NEVER SHALL devolver o quadro capturado. (`RF-04-64`, `RN-04-34`)

Sobre **Guerreiro(a)**, a medição SHALL ser oferecida **apenas dentro do onboarding, depois de
o consentimento de biometria ter sido registrado naquela mesma sessão**. Fora do onboarding, a
tela SHALL medir somente quem opera, e NEVER SHALL abrir a câmera sobre um Guerreiro(a).
(`RN-04-33`, `RN-04-07`, documento 99 §6 invariante 11)

A tela SHALL permanecer na aplicação depois da calibração, como ferramenta de diagnóstico de
quem conduz o encontro. (`RF-04-63`, decisão do fundador, 2026-09-17)

#### Scenario: A distância aparece na unidade do núcleo

- **WHEN** o Mestre captura duas vezes e pede a comparação
- **THEN** a tela apresenta a distância entre os dois descritores, no mesmo cálculo que o núcleo
  usa para decidir se confere

#### Scenario: Só um descritor de referência fica guardado

- **WHEN** uma terceira captura é comparada com a referência
- **THEN** a segunda já havia sido descartada, e em nenhum momento houve mais de um descritor
  de referência guardado

#### Scenario: A medição não fala com o núcleo

- **WHEN** a medição inteira é executada
- **THEN** nenhuma requisição sai do aparelho, e nem descritor nem distância chegam ao núcleo

#### Scenario: A bancada mede com o visor aberto

- **WHEN** a bancada captura a referência ou uma comparação
- **THEN** o visor ao vivo aparece na tela, e o quadro capturado não é devolvido

#### Scenario: Fora do onboarding a câmera não se abre sobre criança

- **WHEN** a tela é alcançada fora do onboarding
- **THEN** ela mede apenas quem opera, e não oferece caminho que capture um Guerreiro(a)

#### Scenario: Dentro do onboarding, mede depois do consentimento

- **WHEN** o onboarding chega ao passo da imagem com o consentimento já registrado
- **THEN** a medição é oferecida ali, sobre o Guerreiro(a) daquele cadastro
