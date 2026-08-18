## Purpose

A devolução, a quem sustentou atividade com o próprio bolso, do que a plataforma absorveu em seu
nome — feita apenas quando alguém doa para esse fim, por decisão do Admin e na ordem da
antiguidade. Reverte as moedas do aporte e preserva o registro do ato e o reconhecimento
público, porque o selo é por ter sustentado, não pelo valor.

## Requirements

### Requirement: Os aportes ressarcíveis em aberto são listados por antiguidade

O núcleo SHALL expor a lista dos aportes de forma **absorção** com situação de ressarcimento
**em aberto**, ordenados pela **data do aporte, do mais antigo ao mais novo**. Consultar a lista
SHALL exigir persona **Admin** em sessão; persona de qualquer outro papel SHALL receber **403**.
Cada item SHALL trazer o provedor que absorveu, o tipo de recurso, a quantidade, o ponto de
apoio, o valor em moedas, o **valor em reais** a devolver e a data do aporte. Aporte já
**ressarcido** NÃO SHALL aparecer na lista. A lista SHALL trazer também o **saldo de receita
destinada** ainda em aberto, para que a decisão do Admin seja tomada contra o que existe.
(`RF-07-24`, `RN-07-17`, `RF-01-16`, PRD-07 §§9, 12)

#### Scenario: Admin lê a fila do mais antigo ao mais novo

- **WHEN** um Admin em sessão consulta os aportes ressarcíveis e há três absorções em aberto, de
  datas diferentes
- **THEN** o núcleo devolve as três da mais antiga para a mais nova, cada uma com provedor,
  tipo, quantidade, ponto de apoio, moedas, valor em reais e data

#### Scenario: Aporte ressarcido sai da lista

- **WHEN** uma absorção que estava em aberto é ressarcida e o Admin consulta a lista de novo
- **THEN** aquele aporte não aparece mais, e os demais em aberto seguem na mesma ordem

#### Scenario: Aporte da gestão nunca entra na fila

- **WHEN** um Admin registra um aporte pela rota da gestão e consulta a lista
- **THEN** aquele aporte não aparece, por não ser ressarcível

#### Scenario: Mestre não lê a fila da gestão

- **WHEN** um Mestre em sessão consulta os aportes ressarcíveis
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: O ressarcimento é registrado pelo Admin, com comprovante anexado

O núcleo SHALL registrar o **ressarcimento** de um aporte por absorção com o **aporte
absorvido**, o **valor em reais**, a **receita destinada de origem**, o **Admin pagador**, a
**data** e o **comprovante da transferência** anexado. Registrar ressarcimento SHALL exigir
persona **Admin** em sessão; persona de qualquer outro papel SHALL receber **403**.

Ressarcimento **sem comprovante anexado** SHALL ser recusado com **422**. O comprovante SHALL
aceitar **PDF, JPG ou PNG** e SHALL seguir o mesmo regime de acesso restrito à gestão do
comprovante do aporte: NÃO SHALL ser servido por rota pública nem por rota de persona que não
seja Admin.

**Nenhum campo da API SHALL aceitar chave PIX, banco, agência ou conta.** O dado bancário chega
ao Admin fora da plataforma e não é transcrito para cá.

Ressarcimento sobre aporte que **não seja ressarcível**, ou cuja situação **não esteja em
aberto**, SHALL ser recusado com **422**. Um aporte SHALL ter no máximo **um** ressarcimento.
A escrita SHALL gravar autoria, data e hora com fuso. (`RF-07-22`, `RF-07-25`, `RF-01-16`,
`RF-01-03`, `RF-01-27`, PRD-07 §§9, 11, 12)

#### Scenario: Admin ressarce uma absorção com comprovante

- **WHEN** um Admin em sessão registra o ressarcimento de uma absorção em aberto, declarando a
  receita destinada de origem e anexando o comprovante em PDF
- **THEN** o núcleo grava o ressarcimento com o valor em reais, a receita de origem, o pagador,
  a data e o comprovante, com autor e hora com fuso

#### Scenario: Ressarcimento sem comprovante é recusado

- **WHEN** chega um registro de ressarcimento sem comprovante anexado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: A API não tem onde receber chave PIX

- **WHEN** chega um registro de ressarcimento com um campo de chave PIX, banco ou conta
- **THEN** o núcleo não grava dado bancário algum, e nenhum campo da entidade o guarda

#### Scenario: Aporte não ressarcível não se ressarce

- **WHEN** um Admin tenta ressarcir um aporte registrado pela gestão
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: O mesmo aporte não se ressarce duas vezes

- **WHEN** um Admin tenta ressarcir de novo uma absorção já ressarcida
- **THEN** o núcleo responde 422 e o ressarcimento existente permanece como estava

#### Scenario: Mestre não registra ressarcimento

- **WHEN** um Mestre em sessão tenta registrar um ressarcimento
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O ressarcimento só ocorre havendo receita destinada que o cubra

O núcleo SHALL recusar, com **422**, o ressarcimento cujo valor em reais exceda o que a
**receita destinada de origem** ainda tem em aberto — o valor em reais daquela receita menos a
soma dos ressarcimentos já pagos contra ela. Ressarcimento que declare como origem um aporte de
destinação **lastro**, ou aporte inexistente, SHALL ser recusado com **422**.

O ressarcimento NÃO SHALL ser tratado como direito do provedor nem como dívida da plataforma:
não há fila que se pague sozinha, e sem receita destinada nenhum pagamento é aceito.
(`RF-07-22`, `RN-07-17`, PRD-07 §§5.6, 12)

#### Scenario: Pagamento dentro do que a receita cobre

- **WHEN** uma receita destinada de 500 reais está integralmente em aberto e o Admin ressarce
  uma absorção de 200 reais contra ela
- **THEN** o núcleo grava o ressarcimento e a receita passa a ter 300 reais em aberto

#### Scenario: Pagamento acima do que a receita cobre é recusado

- **WHEN** uma receita destinada tem 100 reais em aberto e o Admin tenta ressarcir contra ela
  uma absorção de 200 reais
- **THEN** o núcleo responde 422, nada é gravado e as moedas do aporte não são revertidas

#### Scenario: Aporte de lastro não financia ressarcimento

- **WHEN** o Admin declara como receita de origem um aporte de destinação lastro
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Sem receita destinada não há pagamento

- **WHEN** não existe nenhum aporte de destinação ressarcimento e o Admin tenta registrar um
  ressarcimento
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O ressarcimento pago reverte as moedas e mantém o registro do ato

O núcleo SHALL, no mesmo ato do registro do ressarcimento, emitir **lançamento de ajuste** sobre
o **lançamento de crédito** do aporte absorvido, revertendo as **moedas** daquele aporte. A
situação de ressarcimento do aporte SHALL passar a **ressarcido**.

O Poder Sustentador do provedor SHALL voltar ao valor anterior àquele aporte. A **contagem de
absorções** daquele provedor NÃO SHALL mudar: o reconhecimento é por ter sustentado a atividade
quando faltou recurso, não pelo valor. O **registro do ressarcimento permanece** e o aporte
segue gravado, íntegro — a reversão é lançamento novo, nunca alteração do lançamento original.

A reversão NÃO SHALL alterar o **saldo de recurso**: o bem chegou e foi consumido, e o que
volta é o dinheiro a quem o adiantou. (`RF-07-25`, `RN-07-18`, `RN-07-15`, `RF-07-19`,
PRD-07 §§8, 12)

#### Scenario: O Poder Sustentador volta ao que era antes do aporte

- **WHEN** um Mestre com Poder Sustentador 30 absorve um recurso de 5 moedas, subindo para 35, e
  esse aporte é depois ressarcido
- **THEN** o Poder Sustentador dele volta a 30

#### Scenario: O selo continua contando a absorção

- **WHEN** a única absorção de um Mestre é ressarcida
- **THEN** a contagem de absorções dele segue em 1, e o Poder Sustentador volta ao anterior

#### Scenario: A reversão não mexe no saldo de recurso

- **WHEN** uma absorção de 4 unidades já consumidas por uma aula é ressarcida
- **THEN** o saldo daquele tipo naquele ponto de apoio permanece exatamente como estava antes do
  ressarcimento

#### Scenario: O aporte original segue intacto

- **WHEN** um aporte é ressarcido
- **THEN** o aporte e o lançamento de crédito permanecem gravados sem alteração, e a reversão
  aparece como lançamento de ajuste que os referencia

#### Scenario: A situação do aporte passa a ressarcido

- **WHEN** o ressarcimento de uma absorção em aberto é registrado
- **THEN** a situação de ressarcimento daquele aporte passa a "ressarcido"

### Requirement: Quem absorveu acompanha a situação dos próprios aportes

O núcleo SHALL expor, à persona **Mestre ou Admin** em sessão, a situação de ressarcimento dos
aportes que ela mesma absorveu — o tipo de recurso, a quantidade, o ponto de apoio, o valor em
moedas, a data e a situação, em aberto ou ressarcido. A leitura SHALL alcançar **apenas os
aportes do próprio provedor em sessão**; persona de qualquer outro papel SHALL receber **403**.

A leitura SHALL ser **somente leitura**: não existe operação que exija, apresse ou reordene o
ressarcimento a pedido de quem absorveu. (`RF-07-24`, `RN-07-17`, PRD-07 §§4, 9)

#### Scenario: Mestre vê a situação do que absorveu

- **WHEN** um Mestre em sessão consulta os aportes que absorveu
- **THEN** o núcleo devolve os aportes dele com tipo, quantidade, ponto de apoio, moedas, data e
  a situação de cada um

#### Scenario: A leitura não alcança aporte de outro provedor

- **WHEN** um Mestre em sessão consulta a rota e há absorções de outro Mestre em aberto
- **THEN** as absorções do outro não aparecem na resposta

#### Scenario: Apoiador não lê a rota de absorções

- **WHEN** um Apoiador em sessão consulta a rota
- **THEN** o núcleo responde 403 e nada é devolvido
