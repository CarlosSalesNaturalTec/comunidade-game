# Spec Delta

## ADDED Requirements

### Requirement: A entrada pré-carrega os modelos de reconhecimento depois de achar câmera

A aplicação SHALL começar a **pré-carregar os modelos** de reconhecimento facial assim que a
verificação da câmera der certo, antes de a pessoa submeter o rosto, para que o download não
caia sobre a criança já de pé na frente do aparelho. A pré-carga SHALL acontecer **só onde há
câmera disponível**: em aparelho recusado pelo `RF-05-02` ela NEVER SHALL começar, porque ali a
entrada vai ao adulto do `RN-05-02` e descritor nenhum será gerado. (`RF-05-90`, alcançando
`RF-05-01` e `RF-05-02`)

A pré-carga NEVER SHALL bloquear o campo do nick: a pessoa SHALL poder digitar e submeter
enquanto os modelos carregam, e a submissão SHALL esperar o que faltar em vez de ser recusada.

#### Scenario: A pré-carga começa quando há câmera

- **WHEN** a tela de entrada verifica a câmera e a encontra disponível
- **THEN** a pré-carga dos modelos começa, sem que a pessoa tenha pedido nada

#### Scenario: Aparelho sem câmera não pré-carrega nada

- **WHEN** a verificação da câmera falha, ou o acesso é negado
- **THEN** a recusa do `RF-05-02` é apresentada e a pré-carga NEVER começa

#### Scenario: O nick continua utilizável durante a pré-carga

- **WHEN** a pré-carga está em andamento
- **THEN** o campo do nick aceita digitação e a submissão segue disponível

### Requirement: O andamento da pré-carga é informação, nunca erro

A aplicação SHALL apresentar o andamento da pré-carga como **informação**, no mesmo molde do
`RF-04-75` da App 01: anunciada a leitores de tela como estado e não como alerta, narrada quando
a narração estiver ativada, e legível **sem depender de cor**. (`RF-05-90`, PRD-05 §10,
documento 15 §5)

A falha da pré-carga NEVER SHALL interromper a entrada nem vestir a frase do rosto: ela SHALL
ser apresentada como estado local, e a pessoa SHALL seguir podendo submeter o nick e o rosto. O
caminho de erro visível da conferência SHALL continuar sendo o da captura, com as mensagens que
a entrada já tem. (`RN-05-48`, invariante 25)

#### Scenario: O andamento é anunciado como estado

- **WHEN** a pré-carga está em andamento
- **THEN** a tela informa que os modelos estão carregando, como estado e não como alerta, e a
  informação não depende de cor para ser entendida

#### Scenario: A falha não interrompe a entrada

- **WHEN** a pré-carga falha
- **THEN** a tela informa a falha sem interromper, e a entrada por nick e rosto segue disponível

#### Scenario: A falha não usa a frase da recusa do rosto

- **WHEN** a pré-carga falha
- **THEN** a mensagem apresentada não é a da recusa da conferência biométrica

### Requirement: A pré-carga nunca abre a câmera

A pré-carga SHALL carregar **apenas os modelos** e NEVER SHALL abrir a câmera, capturar quadro
nem gerar descritor: no momento em que ela acontece ninguém pediu nada, e câmera aberta fora do
pedido da pessoa contraria o consentimento que o documento 03 §3.3 exige. A verificação de
existência de câmera que a antecede NEVER SHALL ser confundida com captura. (`RN-05-49`,
descendo do `RN-05-01` e do documento 03 §3.3)

Nenhuma imagem SHALL ser gravada no aparelho por causa da pré-carga, e a pré-carga NEVER SHALL
entrar em aviso de coleta, porque não coleta dado algum. (`RF-05-06`)

#### Scenario: Pré-carga não acende a câmera

- **WHEN** a pré-carga dos modelos está em andamento
- **THEN** a câmera permanece desligada e nenhum quadro é capturado

#### Scenario: Pré-carga não grava nada no aparelho

- **WHEN** a pré-carga termina, com sucesso ou com falha
- **THEN** nenhuma imagem de Guerreiro(a) fica guardada no aparelho
