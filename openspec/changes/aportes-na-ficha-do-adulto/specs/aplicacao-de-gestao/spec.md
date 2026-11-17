## ADDED Requirements

### Requirement: A ficha do adulto mostra os aportes de que ele é provedor

A ficha de leitura de um Mestre ou de um Apoiador na App 03 SHALL apresentar a seção
**Aportes** com:

- o **Poder Sustentador** em moedas;
- a tabela dos **aportes homologados**, do mais recente ao mais antigo, com data, tipo de
  recurso, quantidade com a unidade, valor em moedas, ponto de apoio, forma, destinação e se tem
  comprovante. Quando houver valor de origem em reais, ele SHALL aparecer **ao lado** das
  moedas, nunca sozinho;
- a lista das **declarações pendentes** da App 08, separada da tabela, com data, valor
  declarado e origem da escolha.

Os números SHALL sair no formato pt-BR. A seção NEVER SHALL oferecer baixar o comprovante, nem
editar, estornar, homologar ou recusar aporte ou declaração. O valor em reais NEVER SHALL
aparecer em outra tela da App 03. (`RF-02-117`, `RN-02-34`, `RF-02-02`, `RF-02-03`, `RN-02-01`,
documento 04 §1)

#### Scenario: A ficha mostra o aporte registrado

- **WHEN** o Admin abre a ficha de um Apoiador com um aporte homologado em dinheiro
- **THEN** a seção Aportes mostra o Poder Sustentador e a linha do aporte, com o valor em
  moedas e a marca de comprovante

#### Scenario: Reais sempre ao lado das moedas

- **WHEN** o aporte da linha tem valor de origem em reais
- **THEN** a linha mostra o valor em reais junto do equivalente em moedas

#### Scenario: A declaração pendente aparece à parte

- **WHEN** o Apoiador tem uma declaração pendente feita pela App 08
- **THEN** ela aparece na lista das declarações pendentes, fora da tabela dos aportes, e sem
  ação de homologar ou recusar

#### Scenario: Ficha sem aporte

- **WHEN** o Admin abre a ficha de um adulto que nunca aportou
- **THEN** a seção mostra o Poder Sustentador em zero e o aviso de que ainda não há aporte

#### Scenario: A seção não abre edição

- **WHEN** o Admin percorre a seção Aportes
- **THEN** não lhe é oferecido baixar o comprovante, nem campo ou botão para alterar, estornar,
  homologar ou recusar
