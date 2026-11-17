## ADDED Requirements

### Requirement: A camada comum sorteia um avatar do catálogo fechado

A camada comum SHALL oferecer o **sorteio** de um avatar completo: um traço **do catálogo
fechado** em cada uma das nove camadas do documento 15 §7.1, escolhido ao acaso entre **todos**
os traços da camada, devolvido no objeto versionado do documento 15 §7.2. O sorteio NEVER SHALL
produzir traço fora do catálogo nem depender de rede, e NEVER SHALL restringir traço por gênero.
É o avatar de quem é cadastrado sem montá-lo — o cadastro direto pela gestão. (`RF-02-01`,
documento 15 §7)

#### Scenario: O avatar sorteado só tem traços do catálogo

- **WHEN** um avatar é sorteado
- **THEN** cada uma das nove camadas traz um traço que o catálogo conhece, na versão vigente do
  objeto

#### Scenario: O sorteio alcança todos os traços

- **WHEN** muitos avatares são sorteados
- **THEN** todo traço de cada camada pode sair, e não só o padrão dela

#### Scenario: O avatar sorteado se desenha como foi sorteado

- **WHEN** o avatar sorteado é gravado como texto e lido de volta
- **THEN** a leitura devolve as mesmas escolhas, sem cair no avatar padrão do projeto
