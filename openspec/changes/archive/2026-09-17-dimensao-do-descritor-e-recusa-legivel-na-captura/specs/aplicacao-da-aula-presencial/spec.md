## MODIFIED Requirements

### Requirement: O termo é exibido e a assinatura é testemunhada antes da captura

A App 01 SHALL exibir o **termo de consentimento** na tela antes de qualquer captura, e SHALL
colher do Mestre ou do Admin presente a confirmação de que o termo impresso foi **assinado pelo
responsável**. Quem confirma SHALL ficar registrado como **testemunha** do consentimento. A
aplicação NEVER SHALL capturar imagem antes de o consentimento estar registrado no núcleo.
(`RF-04-11`, `RF-04-12`, `RF-04-13`, `RN-04-07`, documento 99 §6 invariante 11)

A leitura do termo **em voz alta** depende da modalidade áudio, que ainda não existe na
aplicação: esta fatia entrega a exibição em tela, e a locução acompanha a conversa conduzida por
IA quando ela chegar. (`RF-04-06`, `RF-04-11`)

Recusada a captura, a tela SHALL apresentar **a recusa que o núcleo deu** — a mensagem que a
camada de acesso já entrega —, e NEVER SHALL atribuir ao consentimento uma recusa de outra
causa. A tela SHALL ter frase própria apenas quando não houver corpo de erro do núcleo.
(`RF-04-13`, `RF-04-20`, `RF-01-02`, PRD-01 §2)

#### Scenario: O termo aparece antes da câmera

- **WHEN** o cadastro chega ao passo da imagem com o responsável presente
- **THEN** a aplicação exibe o termo e não abre a câmera enquanto a confirmação não for dada

#### Scenario: Quem confirma fica registrado como testemunha

- **WHEN** o Mestre confirma que o termo impresso foi assinado
- **THEN** o consentimento é registrado no núcleo com ele como testemunha, e só então a câmera é
  aberta

#### Scenario: Captura sem consentimento registrado é recusada

- **WHEN** o envio do descritor é tentado sem consentimento de biometria registrado
- **THEN** o núcleo recusa com 422 e a aplicação apresenta a recusa dele em linguagem simples

#### Scenario: Recusa de outra causa não vira recusa de consentimento

- **WHEN** o núcleo recusa o envio do descritor por motivo diferente do consentimento
- **THEN** a tela apresenta o motivo que o núcleo deu, e não a frase do consentimento

#### Scenario: Falha sem resposta do núcleo tem frase própria

- **WHEN** a captura falha antes de qualquer resposta do núcleo chegar
- **THEN** a tela diz que a captura falhou, sem atribuir ao núcleo uma recusa que ele não deu
