## ADDED Requirements

### Requirement: As retomadas em aberto nascem da cadência do Mestre e do desbloqueio do Guerreiro(a)

O núcleo SHALL derivar as **retomadas em aberto** de um Guerreiro(a) da **cadência de retomada**
que o Mestre autor declarou na missão e do **momento em que ele a desbloqueou**: cada dia da
cadência é um **agendamento**, com prazo contado do desbloqueio. Nenhum estado de retomada
SHALL ser persistido — a lista nasce na leitura, como o percurso já nasce.

Um agendamento SHALL estar **em aberto** quando o prazo dele já **venceu** e o Guerreiro(a)
ainda **não entregou produção** daquela missão a partir daquele prazo. Missão **sem cadência
declarada** NEVER SHALL gerar retomada, e missão que ele ainda **não desbloqueou** também não —
não há de onde contar o prazo. Desbloqueio prático ainda **não julgado** pelo Mestre NEVER SHALL
abrir agendamento. (`RF-05-79`, `RF-09-83`, `RF-09-101`, documento 11 §2.2)

#### Scenario: A cadência declarada vira agendamentos contados do desbloqueio

- **WHEN** o Guerreiro(a) desbloqueou uma missão cuja cadência de retomada é de 2, 7 e 21 dias
- **THEN** ele tem três agendamentos, com prazos de 2, 7 e 21 dias contados do desbloqueio dele

#### Scenario: Só o agendamento vencido aparece em aberto

- **WHEN** passaram 3 dias do desbloqueio de uma missão com cadência de 2, 7 e 21 dias, e ele
  não entregou produção alguma
- **THEN** a retomada de 2 dias está em aberto, e as de 7 e 21 dias ainda não

#### Scenario: Missão sem cadência declarada não gera retomada

- **WHEN** o Guerreiro(a) desbloqueia uma missão que o Mestre deixou sem cadência de retomada
- **THEN** nenhuma retomada dela aparece para ele

#### Scenario: Missão não desbloqueada não gera retomada

- **WHEN** uma missão com cadência declarada ainda não foi desbloqueada pelo Guerreiro(a)
- **THEN** nenhuma retomada dela aparece para ele

#### Scenario: Desbloqueio prático ainda não julgado não abre agendamento

- **WHEN** o Guerreiro(a) declarou ter cumprido o desafio prático e o Mestre autor ainda não
  julgou
- **THEN** nenhuma retomada daquela missão aparece para ele

#### Scenario: A retomada é de cada Guerreiro(a), pelo desbloqueio dele

- **WHEN** dois Guerreiros desbloqueiam a mesma missão em dias diferentes
- **THEN** os prazos das retomadas de cada um são contados do desbloqueio dele, e não do colega

### Requirement: A retomada vale uma vez por agendamento, e refazer por conta própria não a reabre

A produção entregue pelo Guerreiro(a) **a partir do prazo** de um agendamento SHALL **fechá-lo**,
e o agendamento fechado NEVER SHALL voltar à lista de retomadas em aberto. Entregar de novo na
mesma missão NEVER SHALL reabrir agendamento algum nem criar agendamento novo: a cadência
declarada pelo Mestre é a única fonte dos agendamentos.

A produção entregue **antes** do prazo do próximo agendamento — refazer por conta própria —
SHALL ser gravada e receber devolutiva como qualquer outra, e NEVER SHALL fechar, antecipar nem
consumir agendamento algum. Nem a retomada nem o refazer creditam ponto: quem lança o resultado
segue sendo o Mestre. (`RF-05-80`, `RN-05-38`, `RN-05-05`, documento 11 §§2.2, 5)

#### Scenario: A produção entregue fecha o agendamento vencido

- **WHEN** o Guerreiro(a) entrega a produção de uma missão cuja retomada de 2 dias está em
  aberto
- **THEN** aquele agendamento sai da lista de retomadas em aberto

#### Scenario: Entregar duas vezes não reabre nem duplica o agendamento

- **WHEN** ele entrega uma segunda produção da mesma missão, ainda antes do próximo prazo
- **THEN** nenhum agendamento volta à lista e nenhum agendamento novo é criado

#### Scenario: Refazer por conta própria não consome agendamento

- **WHEN** o Guerreiro(a) entrega a produção de uma missão no dia seguinte ao desbloqueio, antes
  de qualquer prazo vencer
- **THEN** a produção é gravada com devolutiva, e a retomada de 2 dias aparece em aberto quando
  o prazo dela vencer

#### Scenario: O agendamento seguinte vence normalmente

- **WHEN** o Guerreiro(a) fechou a retomada de 2 dias e chega o 8º dia
- **THEN** a retomada de 7 dias aparece em aberto

#### Scenario: A retomada não credita ponto

- **WHEN** um agendamento é fechado pela produção entregue
- **THEN** nenhum ponto é creditado, nenhum Resultado é gravado e o percurso segue igual

### Requirement: As retomadas em aberto são alcançáveis por HTTP pelo Guerreiro(a) em sessão

O núcleo SHALL expor as retomadas em aberto por `GET /v1/eu/retomadas`, sob a **sessão do
Guerreiro(a)**, devolvendo, para cada agendamento em aberto, a **missão**, a **trilha** e o
**prazo** dele. A leitura SHALL alcançar **apenas** o Guerreiro(a) em sessão: retomada de
terceiro NEVER SHALL aparecer. Persona que não é Guerreiro(a) SHALL receber **403**, e chamada
sem persona em sessão SHALL ser recusada. (`RF-05-79`, `RN-05-21`, PRD-05 §9)

#### Scenario: O Guerreiro(a) lê as próprias retomadas

- **WHEN** o Guerreiro(a) em sessão consulta as retomadas
- **THEN** o núcleo responde com os agendamentos em aberto dele, cada um com missão, trilha e
  prazo

#### Scenario: Sem retomada em aberto a lista vem vazia

- **WHEN** ele consulta as retomadas e nenhum agendamento venceu sem produção
- **THEN** o núcleo responde com a lista vazia, sem erro

#### Scenario: A retomada de terceiro não aparece

- **WHEN** ele consulta as retomadas
- **THEN** nenhum agendamento de outro Guerreiro(a) aparece na resposta

#### Scenario: A gestão não lê retomadas por esta porta

- **WHEN** um Mestre ou um Admin em sessão consulta a rota
- **THEN** o núcleo responde 403

### Requirement: A App 05 entrega a produção da missão nas três formas, avisando o que descarta

A App 05 SHALL oferecer, na missão desbloqueada, a **entrega da produção** nas três formas —
escrever, gravar a fala ou fotografar o que fez à mão (`RF-05-74`) —, com as três apresentadas
lado a lado e nenhuma como padrão obrigatório.

Antes de enviar em áudio ou em foto, a tela SHALL dizer, em linguagem da criança, que a
gravação e a fotografia são **descartadas na leitura** e que ficam guardadas apenas a
transcrição e a devolutiva (`RF-05-76`, `RN-05-36`). A App 05 NEVER SHALL guardar a foto nem o
áudio no aparelho depois do envio. (`RF-05-74`, `RF-05-76`, documento 03 §12.2)

#### Scenario: As três formas aparecem na missão

- **WHEN** o Guerreiro(a) abre uma missão que ele desbloqueou
- **THEN** a tela oferece escrever, gravar a fala e fotografar o que fez à mão

#### Scenario: A tela avisa o descarte antes de enviar

- **WHEN** ele escolhe gravar a fala ou fotografar o manuscrito
- **THEN** a tela diz que a gravação e a foto são descartadas na leitura e que ficam só a
  transcrição e a devolutiva

#### Scenario: O aparelho não fica com a mídia

- **WHEN** o envio termina
- **THEN** a foto e o áudio não permanecem no aparelho

### Requirement: A App 05 mostra a devolutiva como próximo passo e diz que ela não vale ponto

A App 05 SHALL exibir a **devolutiva** da produção como **retorno construtivo** — o que está
bom e qual o próximo passo —, nunca como nota, acerto, erro ou correção (`RF-05-75`).

Na mesma tela, a App 05 SHALL dizer que a devolutiva **não credita ponto** e que o resultado da
atividade fica **"aguardando lançamento"** até o Mestre lançá-lo (`RF-05-77`, `RN-05-05`). A
App 05 NEVER SHALL exibir ponto, nível ou badge como consequência da entrega.

Não vindo a devolutiva, a tela SHALL confirmar que a produção **foi guardada** e dizer que o
retorno não veio agora — nunca deixar a criança sem saber se o que escreveu se perdeu.
(`RF-05-75`, `RF-05-77`, `RN-05-35`)

#### Scenario: A devolutiva aponta o próximo passo

- **WHEN** a produção é entregue e a devolutiva volta
- **THEN** a tela a exibe como o que está bom e qual o próximo passo

#### Scenario: A tela diz que a devolutiva não vale ponto

- **WHEN** a devolutiva é exibida
- **THEN** a tela diz, na mesma altura, que ela não vale ponto e que o resultado aguarda o
  lançamento do Mestre

#### Scenario: Nenhum ponto aparece por causa da entrega

- **WHEN** a entrega termina
- **THEN** nenhum ponto, nível ou badge novo é exibido como consequência dela

#### Scenario: Devolutiva que não veio não deixa dúvida

- **WHEN** a produção é guardada e a devolutiva não vem
- **THEN** a tela confirma que a produção foi guardada e diz que o retorno não veio agora

### Requirement: A App 05 não obriga foto nem áudio e mostra o caminho do encontro

A App 05 SHALL apresentar, junto às três formas de entrega, o caminho **"entrego ao Mestre no
encontro"**, com o mesmo destaque das demais — nunca como opção escondida, secundária ou de
exceção.

A tela SHALL dizer que quem não quer ser fotografado nem gravado **não perde a missão**, e a
App 05 NEVER SHALL bloquear a missão, esconder o conteúdo dela nem sinalizar pendência por
falta de produção entregue. (`RF-05-78`, `RN-05-37`, documento 03 §3.3)

#### Scenario: O caminho do encontro aparece com as outras formas

- **WHEN** o Guerreiro(a) abre a entrega da produção
- **THEN** "entrego ao Mestre no encontro" aparece com o mesmo destaque de escrever, gravar e
  fotografar

#### Scenario: A tela diz que ninguém perde a missão

- **WHEN** ele escolhe entregar ao Mestre no encontro
- **THEN** a tela diz que ele não perde a missão e nada é bloqueado

#### Scenario: Missão sem produção não vira pendência acusatória

- **WHEN** uma missão desbloqueada segue sem produção entregue
- **THEN** a tela não a marca como pendência nem esconde o conteúdo dela

### Requirement: A App 05 mostra as retomadas e explica que rever fixa

A App 05 SHALL mostrar, ao Guerreiro(a), as **retomadas em aberto** — a missão, a trilha e o
prazo de cada uma —, com a explicação, em linguagem da criança, de que **rever o que já foi
feito fixa o aprendizado** (`RF-05-79`). Sem retomada em aberto, a tela SHALL dizer isso — nunca
lista vazia muda.

Entregue a produção da retomada, ela SHALL sair da lista. A App 05 SHALL manter o caminho de
refazer a missão por conta própria pela tela dela, e SHALL dizer que refazer assim **não rende
ponto novo** (`RF-05-80`, `RN-05-38`). A App 05 NEVER SHALL apresentar a retomada como punição,
atraso ou dívida.

#### Scenario: As retomadas aparecem com missão, trilha e prazo

- **WHEN** o Guerreiro(a) abre o bloco das retomadas com agendamentos em aberto
- **THEN** cada retomada aparece com a missão, a trilha e o prazo dela

#### Scenario: A tela explica para que serve a retomada

- **WHEN** a lista de retomadas é exibida
- **THEN** a tela diz que rever o que já foi feito fixa o aprendizado

#### Scenario: Sem retomada, a tela diz que não há

- **WHEN** nenhum agendamento está em aberto
- **THEN** a tela diz que não há retomada agora, em vez de mostrar lista vazia muda

#### Scenario: A retomada entregue sai da lista

- **WHEN** ele entrega a produção de uma retomada em aberto
- **THEN** ela deixa de aparecer na lista

#### Scenario: A tela diz que refazer por conta própria não rende ponto novo

- **WHEN** ele abre uma missão já cumprida para refazer fora de agendamento
- **THEN** a tela diz que refazer por conta própria não rende ponto novo

#### Scenario: A retomada não é apresentada como castigo

- **WHEN** uma retomada é exibida
- **THEN** nenhuma palavra de atraso, dívida ou punição aparece
