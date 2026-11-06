## RENAMED Requirements

- FROM: `### Requirement: Nenhum preço de referência fica abaixo de vinte pontos extras`
- TO: `### Requirement: Nenhum preço de referência fica abaixo de vinte e cinco pontos extras`

## MODIFIED Requirements

### Requirement: Nenhum preço de referência fica abaixo de vinte e cinco pontos extras

O núcleo SHALL recusar com **422** todo preço de referência **menor que 25 pontos extras**,
inclusive zero e negativo, indicando o piso. O piso SHALL valer em qualquer vigência, também na
alteração de um preço já registrado. As vigências encerradas antes da elevação do piso
permanecem no histórico com o preço que tinham. (`RF-07-44`, `RN-07-30`, invariante 23)

#### Scenario: Preço no piso é aceito

- **WHEN** um Admin registra um preço de referência de exatamente 25 pontos extras
- **THEN** o núcleo grava a vigência

#### Scenario: Preço abaixo do piso é recusado

- **WHEN** chega um preço de referência de 24 pontos extras
- **THEN** o núcleo responde 422 indicando o piso de 25 e nada é gravado

#### Scenario: Alteração para abaixo do piso é recusada

- **WHEN** um Admin tenta abrir vigência nova com preço menor que 25 para um tipo que já tem
  preço registrado
- **THEN** o núcleo responde 422 e a vigência anterior permanece como estava

## ADDED Requirements

### Requirement: O preço vigente abaixo do piso novo sobe para 25 na entrega

Na entrega do piso de 25, o núcleo SHALL abrir, para **todo tipo de recurso cuja vigência
aberta tem preço menor que 25**, uma vigência nova de **25 pontos extras** com início na data
da entrega, encerrando a anterior nessa mesma data. A vigência anterior NEVER SHALL ser
alterada no preço nem apagada: a troca feita antes da entrega continua lida pelo preço que
cobrou. Tipo com vigência aberta de 25 ou mais NEVER SHALL ganhar vigência nova. (`RF-07-50`,
`RF-07-43`, `RF-07-46`, 02 §8.2)

#### Scenario: Preço de 20 vigente sobe para 25

- **WHEN** a entrega é aplicada a um tipo cuja vigência aberta cobra 20 pontos extras
- **THEN** a vigência de 20 termina na data da entrega e uma vigência de 25 começa nela

#### Scenario: Preço de 40 vigente não muda

- **WHEN** a entrega é aplicada a um tipo cuja vigência aberta cobra 40 pontos extras
- **THEN** nenhuma vigência nova é aberta para ele

#### Scenario: A consulta por data anterior lê o preço antigo

- **WHEN** o preço de referência de um tipo elevado é consultado numa data anterior à entrega
- **THEN** o núcleo devolve o preço que vigorava naquela data
