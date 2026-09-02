## ADDED Requirements

### Requirement: A App 08 tem a área de oferta ao catálogo avulso

A App 08 SHALL oferecer ao Apoiador a **oferta de item ao catálogo avulso**, declarando o
**nome**, o **tipo de recurso**, a **quantidade** e o **ponto de apoio** que a lastreia. A tela
NEVER SHALL oferecer campo de preço, e SHALL declarar que o preço em pontos extras vem da
**tabela de referência da gestão**, nunca de quem oferta. (`RF-14-77`, `RF-14-79`, `RN-14-43`,
invariante 23)

#### Scenario: A oferta declara nome, tipo, quantidade e lastro

- **WHEN** o Apoiador preenche nome, tipo de recurso, quantidade e ponto de apoio e envia a
  oferta
- **THEN** a tela registra o item e mostra que a oferta foi recebida

#### Scenario: A tela não tem campo de preço

- **WHEN** o Apoiador percorre a tela de oferta
- **THEN** nenhum campo pede preço, e a tela declara que o preço vem da tabela de referência da
  gestão

### Requirement: A tela declara que só a homologação do Admin põe o item no catálogo

A tela de oferta SHALL declarar, antes do envio, que o item ofertado **entra pendente** e só
aparece no catálogo depois de **homologado por um Admin**. (`RF-14-78`, `RN-14-42`)

#### Scenario: O Apoiador é avisado antes de ofertar

- **WHEN** o Apoiador abre a tela de oferta
- **THEN** a tela declara que o item entra pendente e só vai ao catálogo depois da homologação
  do Admin

### Requirement: O Apoiador acompanha o item que ofertou

A App 08 SHALL exibir, para cada item ofertado pelo Apoiador, a **situação da homologação** —
pendente, homologado ou recusado, com o **motivo** da recusa em linguagem simples —, a marca de
**ativo**, o **estoque restante**, o **preço em pontos extras** da vigência corrente e **quantas
trocas** já foram entregues. O item que não está ativo SHALL mostrar **o que falta**: a
quantidade de lastro ou o preço de referência do tipo. (`RF-14-80`, `RN-14-42`, `RN-14-43`)

#### Scenario: O item pendente aparece na lista de quem o ofertou

- **WHEN** o Apoiador abre a área de catálogo avulso e um item que ofertou segue pendente
- **THEN** a tela mostra o item como pendente de homologação, ainda que ele não esteja no
  catálogo

#### Scenario: O item recusado aparece com o motivo

- **WHEN** o Admin recusa um item ofertado, com motivo
- **THEN** a tela mostra o item como recusado e o motivo em linguagem simples

#### Scenario: O item ativo mostra estoque restante e trocas

- **WHEN** o Apoiador abre um item ofertado que está ativo e já foi trocado
- **THEN** a tela mostra o estoque restante, o preço em pontos extras e quantas trocas foram
  entregues

#### Scenario: O item inativo mostra o que falta

- **WHEN** o Apoiador abre um item ofertado que está homologado e inativo por falta de lastro ou
  de preço de referência
- **THEN** a tela mostra o que falta para que ele fique ativo

### Requirement: Nenhuma tela de catálogo da App 08 identifica quem trocou

Nenhuma tela de catálogo avulso da App 08 SHALL exibir nome, nick, avatar ou dado algum de
identificação de quem trocou o item, nem a aula ou a data de cada troca: o retorno é **agregado**.
NEVER SHALL a tela oferecer campo de mensagem, contato ou resposta a Guerreiro(a), família ou
Mestre. (`RF-14-81`, `RN-14-44`, `RN-14-20`, `RF-14-59`)

#### Scenario: O acompanhamento traz só a contagem

- **WHEN** o Apoiador percorre a área de catálogo avulso com itens já trocados
- **THEN** a tela mostra apenas quantas trocas houve, sem nome, nick, avatar, aula ou data de
  troca individual, e sem qualquer campo de contato
