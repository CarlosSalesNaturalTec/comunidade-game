# patrimonio Specification

## Purpose

O patrimônio é o acervo que fica: o exemplar permanente tombado num ponto de apoio, com a sua
ficha de vida — quem cuidou dele e o que lhe aconteceu. É a face do livro-razão que não se
consome, e por isso a única em que o saldo não se gasta, não se reserva e não lastreia nada.

## Requirements

### Requirement: O saldo de natureza durável é inerte

O núcleo SHALL manter o saldo de tipo de recurso de natureza **durável** fora de toda operação
de consumo: ele NÃO SHALL ser reservável por aula e NÃO SHALL servir de lastro a item do
catálogo avulso. O aporte de tipo durável SHALL creditar o Poder Sustentador do provedor como
qualquer outro, e o seu único destino no núcleo SHALL ser o **tombamento**. Nenhum lançamento
de débito SHALL ser emitido por consumo de tipo durável. (`RN-07-07`, `RF-07-11`, PRD-07 §8,
documento 04 §1)

#### Scenario: Aporte durável credita Poder Sustentador

- **WHEN** um aporte de tipo de recurso de natureza durável é registrado e homologado
- **THEN** o Poder Sustentador do provedor sobe pelo valor em moedas do aporte, como em
  qualquer outra natureza

#### Scenario: Saldo durável não é debitado por consumo

- **WHEN** um aporte de tipo durável credita saldo num ponto de apoio
- **THEN** nenhuma operação do núcleo emite lançamento de débito daquele tipo, e o saldo
  derivado permanece o creditado

### Requirement: O exemplar permanente é tombado num ponto de apoio

O núcleo SHALL registrar o **item patrimonial** com **título**, **número de tombo**, **ponto de
apoio**, **estado de conservação** e, opcionalmente, o **aporte de origem**. Tombar SHALL exigir
persona **Admin** em sessão; **Mestre**, **Apoiador**, **Guerreiro(a)** e **responsável** SHALL
receber **403**. Tombamento sem título, sem número de tombo, sem ponto de apoio ou sem estado de
conservação SHALL ser recusado com **422**, indicando o campo em falta. O aporte de origem
declarado SHALL ser de tipo de natureza **durável**; aporte de outra natureza SHALL ser recusado
com **422**. A escrita SHALL gravar autoria, data e hora com fuso. (`RF-07-11`, `RN-07-07`,
`RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Admin tomba exemplar com aporte de origem

- **WHEN** um Admin em sessão tomba um exemplar com título, número de tombo, ponto de apoio,
  estado de conservação e o aporte durável que o trouxe
- **THEN** o núcleo grava o item patrimonial com o autor, a data e a hora com fuso

#### Scenario: Exemplar sem aporte de origem é tombado

- **WHEN** um Admin em sessão tomba um exemplar sem declarar aporte de origem
- **THEN** o núcleo grava o item patrimonial, porque o aporte de origem é opcional

#### Scenario: Mestre não tomba

- **WHEN** um Mestre em sessão tenta tombar um exemplar
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Aporte de origem de natureza não durável é recusado

- **WHEN** chega um tombamento cujo aporte de origem é de tipo de natureza consumível, serviço
  ou financeira
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O número de tombo é digitado e único por ponto de apoio

O **número de tombo** SHALL ser informado por quem tomba, nunca gerado pelo núcleo, e SHALL ser
**único dentro do ponto de apoio** do exemplar. Tombo repetido no mesmo ponto de apoio SHALL ser
recusado com **422**. O mesmo número em pontos de apoio diferentes SHALL ser aceito.
(`RF-07-11`, PRD-07 §8, documento 05 §3)

#### Scenario: Tombo repetido no mesmo ponto de apoio é recusado

- **WHEN** chega um tombamento com número de tombo já usado por outro exemplar do mesmo ponto
  de apoio
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mesmo tombo em pontos de apoio diferentes é aceito

- **WHEN** dois exemplares de pontos de apoio diferentes são tombados com o mesmo número de
  tombo
- **THEN** o núcleo grava os dois

### Requirement: O tombamento não excede a quantidade aportada

O número de itens patrimoniais que referenciam um mesmo **aporte de origem** NÃO SHALL exceder a
**quantidade** daquele aporte. O tombamento que ultrapassaria o teto SHALL ser recusado com
**422**. Item tombado sem aporte de origem NÃO SHALL entrar nessa contagem, e sobre ele não há
teto a conferir. (`RN-07-07`, `RN-07-01`, invariante 9 do documento 99 §6, PRD-07 §8)

#### Scenario: Tombamento além da quantidade aportada é recusado

- **WHEN** um aporte durável de quantidade 3 já tem 3 exemplares tombados e chega um quarto
  tombamento referenciando o mesmo aporte
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Tombamento dentro do aportado é aceito

- **WHEN** um aporte durável de quantidade 46 tem 45 exemplares tombados e chega mais um
- **THEN** o núcleo grava o item patrimonial

### Requirement: O responsável pelo exemplar deriva do ponto de apoio

O item patrimonial NÃO SHALL ter responsável próprio: o responsável pelo exemplar SHALL ser o
**responsável designado pelo acervo do seu ponto de apoio**. A leitura do item SHALL trazer esse
responsável, e a troca do responsável do ponto de apoio SHALL alcançar todos os exemplares ali
tombados, sem escrita em cada um. (`RN-07-10`, `RN-07-34`, `RF-07-49`, documento 05 §3)

#### Scenario: Leitura do item traz o responsável do ponto de apoio

- **WHEN** um item patrimonial de um ponto de apoio com responsável designado é lido
- **THEN** a resposta traz aquele responsável

#### Scenario: Troca do responsável alcança os exemplares já tombados

- **WHEN** o responsável pelo acervo de um ponto de apoio é trocado
- **THEN** a leitura de todo exemplar ali tombado passa a trazer o novo responsável, sem que
  nenhum item tenha sido alterado

### Requirement: A ficha de vida é somente inserção

O núcleo SHALL manter a **ficha de vida** de cada item patrimonial como histórico de **somente
inserção**: cada anotação registra o **exemplar**, o **teor** — quem cuidou dele, perda ou dano
—, o **estado de conservação** apurado e o autor, com data e hora com fuso. Anotação da ficha de
vida NÃO SHALL ser alterada nem removida. Anotar SHALL exigir persona **Admin** ou **Mestre** em
sessão; **Apoiador**, **Guerreiro(a)** e **responsável** SHALL receber **403**. (`RF-07-11`,
`RF-07-48`, `RF-01-03`, `RF-01-27`, PRD-07 §8, documento 05 §3)

#### Scenario: Anotação entra na ficha e não sai

- **WHEN** um Mestre em sessão anota na ficha de vida de um exemplar quem cuidou dele
- **THEN** o núcleo grava a anotação com autor, data e hora com fuso, e nenhuma rota a altera
  nem a remove

#### Scenario: Guerreiro(a) não anota na ficha de vida

- **WHEN** um Guerreiro(a) em sessão tenta anotar na ficha de vida de um exemplar
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Ficha de vida é lida na ordem do tempo

- **WHEN** um exemplar com várias anotações é lido
- **THEN** a ficha de vida vem completa, da anotação mais antiga à mais recente

### Requirement: Perda e dano nunca geram débito ao Guerreiro(a) nem à família

A anotação de **perda** ou **dano** na ficha de vida SHALL produzir apenas o registro e a
atualização do estado de conservação do exemplar. Ela NÃO SHALL emitir lançamento de débito,
NÃO SHALL debitar ponto regular ou extra de Guerreiro(a) algum e NÃO SHALL criar cobrança a
responsável familiar. Nenhuma anotação de perda ou dano SHALL exigir a identificação de um
Guerreiro(a) responsável pelo fato. (`RF-07-48`, `RN-07-09`, PRD-07 §12, documento 05 §3.6)

#### Scenario: Exemplar dado como perdido não gera débito

- **WHEN** um exemplar é anotado como perdido na ficha de vida
- **THEN** o núcleo grava a anotação e o estado de conservação, e nenhum lançamento de débito,
  nenhum débito de ponto e nenhuma cobrança é criada

#### Scenario: Anotação de dano não identifica culpado

- **WHEN** chega uma anotação de dano na ficha de vida de um exemplar
- **THEN** o núcleo a grava sem exigir Guerreiro(a) algum como responsável pelo fato

### Requirement: O exemplar não sai do ponto de apoio

O núcleo NÃO SHALL oferecer operação de **retirada**, **empréstimo** ou **devolução** de item
patrimonial, nem de transferência entre pontos de apoio: no Ciclo 01 o exemplar permanece no
ponto de apoio em que foi tombado. (`RN-07-11`, PRD-07 §3.2, documento 05 §3.2)

#### Scenario: Não há rota de retirada nem de empréstimo

- **WHEN** o contrato da API é consultado
- **THEN** nenhuma rota registra retirada, empréstimo, devolução ou transferência de item
  patrimonial

### Requirement: O acervo é lido pela gestão, filtrado por comunidade

O núcleo SHALL devolver os itens patrimoniais com título, número de tombo, ponto de apoio,
estado de conservação, responsável derivado e a ficha de vida, filtrados pela **comunidade** do
ponto de apoio. A leitura SHALL exigir persona de gestão em sessão: o **Admin** SHALL ler todas
as comunidades e o **Mestre**, apenas as comunidades a que está vinculado. **Apoiador**,
**Guerreiro(a)** e **responsável** SHALL receber **403**. Nenhuma saída SHALL trazer valor em
reais. (`RF-07-11`, `RF-01-16`, `RN-07-05`, invariante 16 do documento 99 §6, PRD-07 §10)

#### Scenario: Mestre lê apenas o acervo das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade lê o acervo
- **THEN** vêm apenas os exemplares dos pontos de apoio daquela comunidade

#### Scenario: Apoiador não lê o acervo da gestão

- **WHEN** um Apoiador em sessão consulta o acervo patrimonial
- **THEN** o núcleo responde 403

#### Scenario: A leitura não traz reais

- **WHEN** o acervo é lido por qualquer persona de gestão
- **THEN** nenhum campo da resposta traz valor em reais
