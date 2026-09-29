## MODIFIED Requirements

### Requirement: Quem não tem cadastro recebe a orientação da sua persona, sem promessa de acesso

Para cada persona, a App 06 SHALL oferecer a orientação de quem **ainda não tem cadastro**, e
NEVER SHALL prometer acesso: entrar não cria cadastro. A orientação SHALL ser a da própria
persona — **pré-cadastro da App 08** para quem quer ser Apoiador, **formulário de participação da
vitrine**, com link para ele, para quem quer ser Mestre, e **procurar a gestão no encontro** para
responsável e Guerreiro(a). NEVER SHALL apresentar link que não resolve. (`RF-03-62`,
PRD-03 §5.9)

#### Scenario: Quem quer ser Apoiador é levado ao pré-cadastro

- **WHEN** o visitante declara que é Apoiador e diz que não tem cadastro
- **THEN** a orientação o leva ao pré-cadastro da App 08

#### Scenario: Responsável e Guerreiro(a) são orientados a procurar a gestão

- **WHEN** o visitante declara que é responsável, ou Guerreiro(a), e diz que não tem cadastro
- **THEN** a orientação é procurar a gestão no encontro, sem promessa de acesso

#### Scenario: A orientação do Mestre não oferece link quebrado

- **WHEN** o visitante declara que quer ser Mestre e diz que não tem cadastro
- **THEN** a orientação nomeia o formulário de participação e traz o link, que resolve para o
  formulário existente

## ADDED Requirements

### Requirement: O formulário de participação pede o mínimo e declara o que a solicitação não faz

A App 06 SHALL oferecer o **formulário de solicitação de participação** em endereço próprio,
que exige **nome, e-mail, WhatsApp, pretensão (Mestre ou Apoiador) e apresentação**, e aceita
**instituição** e **links comprobatórios** como opcionais. **Antes do envio**, a tela SHALL
declarar que a solicitação **não cria cadastro nem acesso**, que quem avalia é um **Admin** e
que o prazo de resposta é de **7 dias**. A solicitação SHALL ser enviada ao núcleo, que a grava
na fila da App 03. (`RF-03-27`, `RF-03-28`, `RF-03-29`, `RF-03-30`, `RF-03-31`, `RN-03-11`,
`RN-03-12`, PRD-03 §5.4)

#### Scenario: Os avisos aparecem antes do envio

- **WHEN** o visitante abre o formulário de participação
- **THEN** a tela diz que a solicitação não cria cadastro nem acesso, que um Admin avalia e que
  o prazo é de 7 dias, antes de qualquer envio

#### Scenario: Campo obrigatório em falta aponta o campo

- **WHEN** o visitante envia sem um dos cinco campos obrigatórios
- **THEN** a tela aponta o campo em falta e nada é enviado

#### Scenario: Instituição e links são opcionais

- **WHEN** o visitante envia com os cinco campos obrigatórios e sem instituição nem links
- **THEN** o envio segue ao núcleo

### Requirement: O formulário de dados declara as condições da entrega

A App 06 SHALL oferecer o **formulário de solicitação de dados** em endereço próprio, que exige
**solicitante, instituição, e-mail e finalidade declarada**, e o **recorte pedido** que o núcleo
registra junto. A tela SHALL declarar, antes do envio, que a entrega é **gratuita, anonimizada,
licenciada em CC BY-SA, depende de aprovação de um Admin e é respondida em 7 dias**. (`RF-03-32`,
`RF-03-33`, `RN-03-12`, `RN-03-13`, `RN-03-14`, PRD-03 §5.2)

#### Scenario: As condições aparecem antes do envio

- **WHEN** o visitante abre o formulário de dados
- **THEN** a tela declara a entrega gratuita, anonimizada, em CC BY-SA, dependente de aprovação
  e respondida em 7 dias

#### Scenario: Campo obrigatório em falta aponta o campo

- **WHEN** o visitante envia sem solicitante, instituição, e-mail, finalidade ou recorte
- **THEN** a tela aponta o campo em falta e nada é enviado

### Requirement: O envio confirma o registro e nunca devolve dado, arquivo ou acesso

Registrada a solicitação, a App 06 SHALL confirmar na tela o **protocolo e o prazo** que o núcleo
devolveu e dizer que o retorno virá pelo **contato declarado**, sem e-mail automático da
plataforma. NEVER SHALL apresentar dado, arquivo, link de download, chave ou acesso no ato, em
nenhum dos dois formulários. (`RF-03-31`, `RF-03-34`, `RN-03-11`, `RN-03-13`, PRD-03 §§5.4, 5.2)

#### Scenario: Confirmação mostra protocolo e prazo

- **WHEN** o núcleo registra a solicitação
- **THEN** a tela mostra o protocolo e o prazo e diz que o retorno vem pelo contato declarado

#### Scenario: Solicitação de dados não entrega nada

- **WHEN** a solicitação de dados é registrada
- **THEN** a tela não oferece arquivo nem link de download e diz que a entrega depende de
  aprovação de um Admin

### Requirement: O envio repetido encontra espera crescente explicada, sem CAPTCHA nem cadastro

Freada a origem pelo envio repetido de qualquer dos dois formulários, a App 06 SHALL explicar
em **linguagem simples** o motivo e **quanto tempo falta**, com o tempo que o núcleo devolveu,
e SHALL manter o que o visitante já preencheu. NEVER SHALL pedir CAPTCHA, cadastro ou login, e
NEVER SHALL guardar no aparelho marca de quem foi freado nem o conteúdo digitado. (`RF-03-35`,
`RF-03-37`, `RN-03-08`, `RN-03-34`, PRD-03 §5.4)

#### Scenario: A espera é explicada nos dois formulários

- **WHEN** o núcleo recusa o envio com 429 e o tempo de espera
- **THEN** a tela diz por que houve a espera e quanto falta, em linguagem simples, e o que foi
  digitado continua no formulário

#### Scenario: A espera não pede nada e não deixa rastro

- **WHEN** o visitante espera o freio passar
- **THEN** nenhuma tela pede CAPTCHA, cadastro ou login, e nada é gravado no aparelho
