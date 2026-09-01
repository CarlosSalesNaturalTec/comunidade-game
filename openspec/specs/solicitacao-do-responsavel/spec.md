## Purpose

O canal pelo qual o responsável exerce, em nome do Guerreiro(a) sob a sua responsabilidade, o
direito de pedir acesso, correção, exclusão ou esclarecimento sobre os dados da criança: cada
pedido nasce com protocolo e prazo de 7 dias, é tratado pela gestão e tem o desfecho registrado
com quem tratou e quando.

## Requirements

### Requirement: O responsável abre a solicitação nos quatro tipos, com protocolo e prazo

O núcleo SHALL registrar a solicitação aberta por um responsável em sessão nos quatro tipos —
**acesso**, **correção**, **exclusão** e **esclarecimento** —, sempre sobre um Guerreiro(a) a que
ele esteja vinculado, com o texto do pedido. O registro SHALL nascer na situação **recebida**,
com **protocolo** e **prazo de 7 dias** contados do registro, e a resposta do envio SHALL trazer
o protocolo e o prazo, e nada mais. O responsável NEVER SHALL abrir solicitação sobre
Guerreiro(a) a que não esteja vinculado: a titularidade não se transfere, e ele exerce o direito
em nome da criança. (`RF-13-22`, `RF-13-24`, `RN-13-13`, `RN-13-14`, 03 §9)

#### Scenario: Pedido de acesso nasce com protocolo e prazo

- **WHEN** um responsável abre solicitação de acesso sobre um Guerreiro(a) a que está vinculado
- **THEN** o núcleo grava a solicitação na situação recebida e devolve o protocolo e o prazo de
  7 dias

#### Scenario: Pedido de exclusão é aceito como qualquer outro tipo

- **WHEN** um responsável abre solicitação do tipo exclusão
- **THEN** o núcleo a registra como as demais, sem recusar o pedido

#### Scenario: Guerreiro(a) não vinculado recusa a abertura

- **WHEN** um responsável abre solicitação sobre um Guerreiro(a) a que não está vinculado
- **THEN** o núcleo recusa com **403** e nada é gravado

#### Scenario: Só o responsável abre a solicitação

- **WHEN** uma persona de outro papel tenta abrir a solicitação do responsável
- **THEN** o núcleo recusa e nada é gravado

### Requirement: Segunda solicitação idêntica em aberto é recusada

O núcleo SHALL recusar com **409** a solicitação do **mesmo responsável**, sobre o **mesmo
Guerreiro(a)** e do **mesmo tipo** quando já houver uma sem desfecho, sem gravar nada. Tratada a
primeira, uma nova do mesmo tipo SHALL ser aceita. (`RF-13-22`, PRD-13 §9)

#### Scenario: Duplicata em aberto não entra na fila

- **WHEN** um responsável abre a segunda solicitação de correção sobre o mesmo Guerreiro(a) com a
  primeira ainda sem desfecho
- **THEN** o núcleo recusa com 409 e a fila segue com uma só

#### Scenario: Tratada a primeira, a nova é aceita

- **WHEN** a primeira solicitação recebeu desfecho e o responsável abre outra do mesmo tipo
- **THEN** o núcleo a registra normalmente, com protocolo e prazo próprios

### Requirement: O responsável acompanha as próprias solicitações

O núcleo SHALL devolver ao responsável em sessão **apenas as próprias** solicitações, com
protocolo, tipo, Guerreiro(a), situação, prazo, a marca de **em atraso** e, quando houver, o
desfecho e a data. Ele NEVER SHALL ler a solicitação de outro responsável. (`RF-13-25`,
`RF-13-26`, `RN-13-13`)

#### Scenario: A família vê protocolo, situação e prazo

- **WHEN** um responsável consulta as próprias solicitações
- **THEN** recebe, de cada uma, protocolo, tipo, situação e prazo

#### Scenario: A consulta não alcança a solicitação de outra família

- **WHEN** um responsável consulta as próprias solicitações
- **THEN** nenhuma solicitação aberta por outro responsável aparece

### Requirement: O atraso é derivado do prazo vencido e não fecha a solicitação

O núcleo SHALL identificar como **em atraso** a solicitação sem desfecho cujo prazo já venceu, e
essa marca SHALL ser **derivada** do prazo e do desfecho — NEVER uma situação gravada. A
solicitação em atraso SHALL permanecer **aberta** e tratável, e o atraso SHALL aparecer tanto
para o responsável quanto na fila do Admin. (`RF-02-66`, `RF-13-26`, `RN-13-14`)

#### Scenario: Prazo vencido sem desfecho marca o atraso

- **WHEN** passam 7 dias do registro sem desfecho
- **THEN** a solicitação aparece em atraso, para o responsável e para o Admin, e continua aberta

#### Scenario: Desfecho registrado encerra o atraso

- **WHEN** o Admin trata uma solicitação vencida
- **THEN** ela deixa de aparecer em atraso, com o desfecho e a data gravados

### Requirement: O Admin lê a fila e registra o desfecho com quem tratou e quando

O núcleo SHALL expor ao **Admin** a fila das solicitações do responsável, com protocolo, tipo,
responsável, Guerreiro(a), texto, situação, prazo e a marca de em atraso, da mais antiga para a
mais recente. O Admin SHALL registrar o desfecho — **aceita** ou **recusada** —, com o texto do
que foi tratado, e o núcleo SHALL gravar **quem tratou** e **quando**. Solicitação já tratada
NEVER SHALL receber segundo desfecho, e a fila NEVER SHALL ser alcançada por outro papel.
(`RF-02-23`, `RF-02-24`, `RN-13-14`)

#### Scenario: A fila chega ao Admin com o que a tela precisa

- **WHEN** o Admin lê a fila das solicitações do responsável
- **THEN** cada item traz protocolo, tipo, situação, prazo e a marca de em atraso

#### Scenario: O desfecho grava quem tratou e quando

- **WHEN** o Admin registra o desfecho de uma solicitação
- **THEN** o núcleo grava a situação final, o texto do desfecho, o Admin que tratou e a data e
  hora

#### Scenario: Solicitação tratada não recebe segundo desfecho

- **WHEN** o Admin tenta tratar uma solicitação que já tem desfecho
- **THEN** o núcleo recusa e o desfecho original permanece

#### Scenario: Mestre não alcança a fila do responsável

- **WHEN** um Mestre tenta ler a fila das solicitações do responsável ou registrar desfecho
- **THEN** o núcleo recusa

### Requirement: O desfecho registra o tratamento e não executa o pedido por si

O desfecho gravado nesta fila SHALL ser **registro do tratamento**, e NEVER SHALL, por si só,
apagar, despersonalizar ou alterar dado do Guerreiro(a) — **com uma exceção**: o desfecho
**aceito** de uma solicitação do tipo **exclusão** SHALL marcar o _template_ biométrico daquele
Guerreiro(a) para apagamento em **5 dias** (`RF-13-43`, `RN-13-22`). É a única execução que o
desfecho dispara, e ela alcança apenas o _template_.

A **despersonalização do registro de dado do território** (`RN-13-12`) NEVER SHALL ser presumida
como efeito do desfecho: ela é o **limite declarado** que a App 07 apresenta antes do aceite, e a
sua execução ficou para o Ciclo 02 (decisão do fundador, 2026-09-01, documento 09 §1). Desfecho
**recusado**, e desfecho aceito de qualquer outro tipo, NEVER SHALL marcar apagamento algum.
(`RF-02-24`, `RF-13-43`, `RN-13-12`, `RN-13-22`)

#### Scenario: Desfecho aceito de exclusão marca o _template_

- **WHEN** o Admin registra o desfecho aceito de uma solicitação de exclusão de um Guerreiro(a)
  com _template_ gravado
- **THEN** o núcleo grava o desfecho e o _template_ fica marcado para apagamento em 5 dias

#### Scenario: Desfecho de exclusão não apaga nada por si

- **WHEN** o Admin registra o desfecho aceito de uma solicitação de exclusão
- **THEN** nenhum registro de território é apagado nem despersonalizado, e nenhum outro dado do
  Guerreiro(a) é alterado por esse ato

#### Scenario: Desfecho recusado não marca nada

- **WHEN** o Admin registra o desfecho recusado de uma solicitação de exclusão
- **THEN** o desfecho é gravado e nenhum _template_ é marcado para apagamento

#### Scenario: Desfecho de outro tipo não marca nada

- **WHEN** o Admin aceita uma solicitação de acesso, correção ou esclarecimento
- **THEN** o desfecho é gravado e nenhum _template_ é marcado para apagamento

### Requirement: A suspensão por divergência abre a solicitação na fila da App 03

O núcleo SHALL abrir, por conta própria, uma `SolicitacaoDoResponsavel` no mesmo instante em que
a recusa de um responsável faz o estado da autorização única de um Guerreiro(a) passar a
**suspensa** — a divergência entre responsáveis, que a gestão trata com a família. A solicitação
SHALL nascer:

- do tipo **`esclarecimento`**, um dos quatro que a fila já conhece (decisão do fundador,
  2026-08-31, documento 09 §1);
- **em nome de quem recusou**, sobre o Guerreiro(a) da divergência;
- com **texto escrito pelo núcleo**, em linguagem simples, dizendo que a autorização ficou
  suspensa por divergência entre os responsáveis;
- na situação **recebida**, com **protocolo** e o mesmo **prazo de 7 dias** de toda solicitação.

A abertura NEVER SHALL depender de ato do responsável, e a recusa NEVER SHALL ser rejeitada
porque a solicitação não pôde nascer. (`RF-13-19`, `RN-13-14`, PRD-13 §5.4)

Estado que passa a `nao_autorizada` — recusa sem concessão de nenhum outro responsável — NEVER
SHALL abrir solicitação: não há divergência a tratar. (`RF-13-17`, `RF-13-19`)

#### Scenario: Recusa que suspende abre a solicitação

- **WHEN** um responsável recusa a autorização de um Guerreiro(a) que outro responsável havia
  concedido
- **THEN** o núcleo grava a recusa e abre uma solicitação de esclarecimento em nome de quem
  recusou, na situação recebida, com protocolo e prazo de 7 dias

#### Scenario: A solicitação aparece na fila do Admin

- **WHEN** o Admin lê a fila depois de uma suspensão por divergência
- **THEN** a solicitação aberta pela suspensão aparece entre as demais, com o texto que o núcleo
  escreveu

#### Scenario: Recusa isolada não abre solicitação

- **WHEN** o único responsável que decidiu recusa, sem concessão de nenhum outro
- **THEN** o estado é `nao_autorizada` e nenhuma solicitação é aberta

#### Scenario: Concessão nunca abre solicitação

- **WHEN** um responsável concede a autorização
- **THEN** nenhuma solicitação é aberta por esse ato

### Requirement: Uma só solicitação de divergência por Guerreiro(a) enquanto estiver em aberto

O núcleo SHALL abrir **uma só** solicitação de divergência por Guerreiro(a) enquanto houver uma
**sem desfecho**: havendo uma em aberto, a suspensão que se repete — segunda recusa, ou recusa
nova depois de uma concessão — NEVER SHALL abrir outra, e a recusa SHALL ser gravada do mesmo
jeito. A gestão trata o caso, não cada ato. Recebido o desfecho da primeira, uma suspensão nova
SHALL abrir a sua. (decisão do fundador, 2026-08-31, documento 09 §1)

A guarda da divergência SHALL alcançar apenas as solicitações que o próprio núcleo abriu:
solicitação de esclarecimento escrita pelo responsável NEVER SHALL impedir que a divergência
entre na fila, e a solicitação da divergência NEVER SHALL impedir que o responsável abra as
suas. (`RF-13-22`, `RF-13-19`)

#### Scenario: Segunda recusa com a primeira em aberto

- **WHEN** um segundo responsável recusa a autorização do mesmo Guerreiro(a) com a solicitação
  da divergência ainda sem desfecho
- **THEN** a recusa é gravada e nenhuma segunda solicitação de divergência é aberta

#### Scenario: Tratada a primeira, a suspensão nova abre a sua

- **WHEN** a solicitação da divergência recebeu desfecho e uma suspensão nova acontece sobre o
  mesmo Guerreiro(a)
- **THEN** o núcleo abre outra solicitação de divergência, com protocolo e prazo próprios

#### Scenario: Esclarecimento do responsável não bloqueia a divergência

- **WHEN** o responsável já tem uma solicitação de esclarecimento em aberto sobre aquele
  Guerreiro(a) e uma suspensão por divergência acontece
- **THEN** a solicitação da divergência é aberta, e as duas convivem na fila

#### Scenario: A divergência não bloqueia o pedido do responsável

- **WHEN** o responsável abre uma solicitação de esclarecimento com a solicitação da divergência
  ainda em aberto
- **THEN** o núcleo a registra normalmente, com protocolo e prazo próprios
