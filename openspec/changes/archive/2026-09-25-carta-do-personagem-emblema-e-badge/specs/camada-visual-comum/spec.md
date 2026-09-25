# Spec Delta

## ADDED Requirements

### Requirement: A camada comum entrega a carta do personagem

A camada comum SHALL entregar a **carta do personagem**, o átomo de interface comum às oito
aplicações, com os valores do documento 15 §8.1: superfície de carta, borda de 1 px, **raio que vem
do temperamento** da aplicação, avatar **quadrado recortado em círculo ocupando metade da largura**
e nick na família de destaque. (documento 15 §8.1)

A carta SHALL exibir **apenas** o que o documento 11 §8.2 atribui à variante dela, e NEVER SHALL
exibir o que aquela tabela lista como nunca exibido — para a variante Guerreiro(a): nem imagem real,
nem nome civil, nem rede social, nem qualquer canal de contato. (documento 11 §8.2, invariantes 9 e
10)

A camada comum NEVER SHALL oferecer carta **pela metade**: variante cuja leitura não devolve o que a
tabela do documento 11 §8.2 exige SHALL ser apresentada em outra forma, não em carta incompleta.
(documento 11 §8.2, decisão do fundador registrada no documento 09 §1)

Havendo **rotação**, ela SHALL respeitar a preferência por menos movimento e NEVER SHALL ser a única
via ao conteúdo do verso. (documento 15 §§5, 8.1)

#### Scenario: A carta se monta com os valores do documento 15

- **WHEN** uma carta é apresentada
- **THEN** ela traz o avatar em círculo ocupando metade da largura, o nick na família de destaque, e
  o raio que o temperamento da aplicação declara

#### Scenario: A carta do Guerreiro(a) não expõe o que é vedado

- **WHEN** a carta de um Guerreiro(a) é apresentada
- **THEN** nela aparecem avatar, nick, badges, poderes com níveis e criações originais, e não
  aparecem imagem real, nome civil, rede social nem canal de contato

#### Scenario: Sem o dado que a variante exige, não se usa carta

- **WHEN** a leitura disponível não devolve o que a tabela do documento 11 §8.2 exige daquela
  variante
- **THEN** a tela apresenta a informação em outra forma, e nenhuma carta incompleta é apresentada

### Requirement: O emblema de nível é contável e nunca global

A camada comum SHALL apresentar o nível de uma trilha ou poder como **número de marcas na moldura,
igual ao nível** — uma marca no nível 1, cinco no nível 5 —, para que uma criança de 6 anos possa
**contá-lo**, e SHALL ser legível **sem depender de cor**. No nível 5 a moldura SHALL fechar, que é
a marca de **Mestre Aprendiz**. (documento 15 §8.2)

O emblema SHALL ser sempre **de uma trilha ou de um poder**, e a moldura SHALL carregar o nome do
poder. NEVER SHALL existir emblema de nível global. (documento 15 §8.2, `RN-05-03`)

#### Scenario: O nível se conta na moldura

- **WHEN** um emblema de nível 3 é apresentado
- **THEN** a moldura traz três marcas, contáveis, e o nível é reconhecível sem depender de cor

#### Scenario: O nível 5 fecha a moldura

- **WHEN** um emblema de nível 5 é apresentado
- **THEN** a moldura traz cinco marcas e aparece fechada, marcando Mestre Aprendiz

#### Scenario: Não há emblema global

- **WHEN** um emblema de nível é apresentado
- **THEN** ele é de uma trilha ou de um poder, e a moldura carrega o nome do poder

### Requirement: Cada família de badge tem silhueta própria, legível sem cor

A camada comum SHALL entregar **uma silhueta por família de badge** do documento 15 §8.3 — escudo
para nível, estrela para conquista, coração para valores e causas, gota para território, folha com
canto dobrado para autoria e hexágono para protagonismo —, cada uma legível a **`24` px** e
reconhecível **sem depender de cor**. (documento 15 §8.3)

A silhueta SHALL dizer a **família**, nunca o poder: dois badges de nível são ambos escudo. O que os
separa SHALL ser o **glifo do poder**. (documento 15 §§8.3, 8.4)

#### Scenario: A família se reconhece pela forma

- **WHEN** badges de famílias diferentes são apresentados juntos
- **THEN** cada um traz a silhueta da família dele, distinguível a `24` px e sem depender de cor

#### Scenario: Dois badges da mesma família se distinguem pelo poder

- **WHEN** dois badges de nível de poderes diferentes são apresentados
- **THEN** ambos trazem escudo, e o glifo do poder dentro deles é o que os separa

### Requirement: O glifo de poder acompanha o nome do poder e tem genérico

A camada comum SHALL entregar o **glifo de poder** do documento 15 §8.4, desenhado no sistema de
ícone da §11.1, apresentado **dentro da silhueta do badge** e **na moldura de nível**, reconhecível
a `24` px em traço e sem depender de cor. O glifo SHALL acompanhar o **nome do poder** e NEVER SHALL
substituí-lo. (documento 15 §8.4)

A cobertura SHALL ser de **um glifo por poder do catálogo**, e poder sem glifo SHALL cair num
**genérico** que NEVER SHALL quebrar a tela — o catálogo de poderes é dado da gestão e cresce sem
passar por aqui. O poder NEVER SHALL ter cor própria: cor é da grandeza e do estado. (documento 15
§§8.4, 9)

#### Scenario: O glifo nunca aparece sem o nome do poder

- **WHEN** um glifo de poder é apresentado
- **THEN** o nome do poder aparece junto, e o glifo não o substitui

#### Scenario: Poder sem glifo cai no genérico

- **WHEN** o catálogo traz um poder para o qual não há glifo desenhado
- **THEN** o genérico é apresentado, com o nome do poder, e nenhuma tela quebra

#### Scenario: O poder não carrega cor

- **WHEN** glifos de poderes diferentes são apresentados
- **THEN** nenhum deles se distingue por cor própria
