## ADDED Requirements

### Requirement: O onboarding cadastra o responsável mínimo e o vínculo no ato do encontro

A App 01 SHALL oferecer, no caminho do onboarding, o cadastro do **responsável mínimo** —
apenas o **nome** — e do **vínculo** dele com o Guerreiro(a) recém-cadastrado, com o **grau de
parentesco** declarado ali. O cadastro SHALL acontecer sob a sessão de trabalho do aparelho,
depois de o Guerreiro(a) existir, porque o vínculo só alcança quem já está cadastrado. A App 01
NEVER SHALL colher e-mail, criar credencial de acesso à App 07 ou anexar a digitalização do
termo: os três são atos da gestão. (`RF-04-60`, `RF-01-13`, `RN-01-20`, PRD-04 §§3.2, 5.2)

#### Scenario: O responsável presente é cadastrado com o vínculo

- **WHEN** a criança conclui o cadastro com o responsável presente
- **THEN** a aplicação cadastra o responsável pelo nome e cria o vínculo com o grau de
  parentesco declarado

#### Scenario: O grau de parentesco é exigido na tela

- **WHEN** a tela do responsável é enviada sem o grau de parentesco
- **THEN** a aplicação recusa e pede o grau antes de seguir para o termo

#### Scenario: A tela não pede e-mail nem senha do responsável

- **WHEN** o responsável é cadastrado no encontro
- **THEN** nenhuma tela pede e-mail, senha ou documento, e a orientação diz que o acesso da
  família é resolvido pela gestão

### Requirement: O termo é exibido e a assinatura é testemunhada antes da captura

A App 01 SHALL exibir o **termo de consentimento** na tela antes de qualquer captura, e SHALL
colher do Mestre ou do Admin presente a confirmação de que o termo impresso foi **assinado pelo
responsável**. Quem confirma SHALL ficar registrado como **testemunha** do consentimento. A
aplicação NEVER SHALL capturar imagem antes de o consentimento estar registrado no núcleo.
(`RF-04-11`, `RF-04-12`, `RF-04-13`, `RN-04-07`, documento 99 §6 invariante 11)

A leitura do termo **em voz alta** depende da modalidade áudio, que ainda não existe na
aplicação: esta fatia entrega a exibição em tela, e a locução acompanha a conversa conduzida
por IA quando ela chegar. (`RF-04-06`, `RF-04-11`)

#### Scenario: O termo aparece antes da câmera

- **WHEN** o cadastro chega ao passo da imagem com o responsável presente
- **THEN** a aplicação exibe o termo e não abre a câmera enquanto a confirmação não for dada

#### Scenario: Quem confirma fica registrado como testemunha

- **WHEN** o Mestre confirma que o termo impresso foi assinado
- **THEN** o consentimento é registrado no núcleo com ele como testemunha, e só então a câmera
  é aberta

#### Scenario: Captura sem consentimento registrado é recusada

- **WHEN** o envio do descritor é tentado sem consentimento de biometria registrado
- **THEN** o núcleo recusa com 422 e a aplicação explica a recusa em linguagem simples

### Requirement: O descritor nasce no aparelho, depois da prova de vivacidade

A App 01 SHALL gerar o _template_ no **navegador do próprio aparelho**, na ordem **prova de
vivacidade e, depois, descritor facial**, e SHALL enviar ao núcleo **apenas o descritor**.
A aplicação NEVER SHALL enviar o descritor quando a prova de vivacidade não passar, NEVER SHALL
pôr a fotografia em corpo de requisição, em registro de erro ou em armazenamento do aparelho, e
NEVER SHALL exibir a imagem de um Guerreiro(a) em tela alguma. A fotografia SHALL ser descartada
na geração do descritor. (`RF-04-14`, `RF-04-48`, `RN-04-06`, `RN-04-08`, `RN-04-12`,
`RN-04-14`, documento 03 §3.3, documento 99 §6 invariante 12)

A garantia de que o descritor veio de um rosto presente é **também presencial** — aula agendada,
aparelho do ponto de apoio e Mestre ou Admin na sala —, porque o descritor nasce em código que
roda no aparelho e o núcleo não tem como reconferi-la. (documento 03 §3.3)

#### Scenario: Vivacidade reprovada não gera envio

- **WHEN** a prova de vivacidade não passa
- **THEN** nenhum descritor é enviado ao núcleo e a aplicação oferece nova tentativa

#### Scenario: Nenhuma requisição carrega imagem

- **WHEN** a captura é concluída e o descritor é enviado
- **THEN** o corpo da requisição carrega apenas o descritor, e nenhuma imagem aparece em
  requisição, em registro de erro ou no armazenamento do aparelho

#### Scenario: A fotografia não sobrevive à captura

- **WHEN** o descritor é gerado
- **THEN** a fotografia original é descartada no aparelho e não existe em lugar nenhum

### Requirement: Sem câmera, fecha a captura e não o onboarding

A App 01 SHALL verificar a presença de câmera no aparelho e, não havendo, SHALL **oferecer o
onboarding assim mesmo**, concluindo o cadastro ativo e sem imagem pelo caminho do Guerreiro(a)
que chega sem o responsável, com registro de quem confirmou. A aplicação SHALL avisar na tela
que a captura exige outro aparelho. A falta de câmera NEVER SHALL deixar uma criança sem
cadastro no dia do encontro. (`RF-04-04`, `RF-04-15`, `RN-04-03`, `RN-04-09`, documento 99 §6
invariante 11, documento 09 — decisão do fundador, 2026-08-24)

#### Scenario: Aparelho sem câmera cadastra sem imagem

- **WHEN** o onboarding é aberto em aparelho sem câmera
- **THEN** o cadastro é concluído ativo e sem imagem, e a tela avisa que a captura exige outro
  aparelho

#### Scenario: A ausência de câmera não fecha o caminho

- **WHEN** a aplicação detecta que não há câmera
- **THEN** o caminho do onboarding continua oferecido na tela inicial

### Requirement: A App 01 não oferece entrada por imagem nem captura de quem já se cadastrou

A App 01 NEVER SHALL oferecer, nesta fatia, a entrada do Guerreiro(a) por **reconhecimento
facial**, nem a captura de imagem de quem **já se cadastrou sem ela** — a criança cujo
responsável comparece num encontro posterior. Ambas dependem de resolver o Guerreiro(a) a partir
do **nick**, e o `RN-01-22` veda esse alcance a qualquer rota de consulta: a forma de resolvê-lo
é decisão da fatia da câmera na entrada. A criança que chega **sem** o responsável SHALL
continuar atendida por inteiro, e nenhuma recusa SHALL deixar o Guerreiro(a) fora da aula.
(`RF-04-15`, `RF-04-16`, `RF-04-18`, `RN-01-22`, `RN-04-09`, PRD-04 §§3.2, 5.3, documento 99 §6
invariante 11)

#### Scenario: A criança sem o responsável é atendida por inteiro

- **WHEN** uma criança chega ao onboarding sem o responsável
- **THEN** o cadastro é concluído, ativo e sem imagem, e ela participa da aula

#### Scenario: A entrada continua sendo por confirmação humana

- **WHEN** um Guerreiro(a) já cadastrado entra pelo caminho das trilhas
- **THEN** a aplicação pede o nick e a confirmação do Mestre ou do Admin, sem abrir a câmera

#### Scenario: A captura de quem já está cadastrado não é oferecida

- **WHEN** um Guerreiro(a) cadastrado sem imagem volta ao encontro com o responsável
- **THEN** a aplicação não oferece a captura nesta fatia, e o Guerreiro(a) segue participando
  pela confirmação humana

## REMOVED Requirements

### Requirement: A App 01 não oferece captura, consentimento nem entrada por imagem nesta fatia

**Reason**: A fatia que o requisito delimitava terminou. A captura de imagem e o registro de
consentimento passam a ser oferecidos no onboarding da criança que chega com o responsável
(jornada 5.2), e o requisito não descreve mais o comportamento da aplicação.

**Migration**: O que dele continua valendo — a entrada por reconhecimento facial e a captura de
quem já se cadastrou sem imagem, ambas ainda não oferecidas — passa ao requisito "A App 01 não
oferece entrada por imagem nem captura de quem já se cadastrou", acima, com o motivo do adiamento
(`RN-01-22`) explicitado. O atendimento por inteiro da criança sem o responsável segue como
cenário lá.
