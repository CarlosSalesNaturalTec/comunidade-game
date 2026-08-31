## ADDED Requirements

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
