## ADDED Requirements

### Requirement: O Admin cadastra e substitui o contorno da comunidade

O núcleo SHALL permitir que **apenas um Admin** em sessão cadastre o **contorno** de uma
Comunidade Virtual já criada — o polígono copiado do OpenStreetMap (OSM) — junto do **elemento
de origem** no OSM. O núcleo SHALL gravar a **data e a hora da cópia**, com fuso. Cadastrar de
novo SHALL **substituir** o contorno anterior, com o elemento de origem e a data da nova cópia.
Persona de qualquer outro papel SHALL receber **403**, e comunidade inexistente SHALL receber
**404**. (`RF-08-33`, PRD-08 §§5.1, 8, 9, documento 02 §1)

O contorno SHALL ser **geometria GeoJSON** do tipo polígono ou multipolígono, em longitude e
latitude, com cada anel fechado. Geometria de outro tipo, anel aberto ou com menos de quatro
posições, coordenada fora da faixa de longitude e latitude e elemento de origem que não seja
uma via ou uma relação do OSM SHALL ser recusados com **422**, indicando o campo, e nada SHALL
ser gravado.

O contorno SHALL pertencer à **comunidade** e a nenhum local abaixo dela, e NEVER SHALL
carregar local, série ou registro de coleta. (`RN-08-32`, documento 99 §6 invariante 7)

#### Scenario: Admin cadastra o contorno copiado do OSM

- **WHEN** um Admin em sessão grava o contorno de uma comunidade com o polígono e o elemento
  de origem `relation/12582832`
- **THEN** o núcleo grava o contorno, o elemento de origem e a data e a hora da cópia

#### Scenario: Cadastrar de novo substitui o contorno

- **WHEN** um Admin grava um segundo contorno para a mesma comunidade
- **THEN** o núcleo guarda só o segundo, com o elemento de origem e a data da nova cópia

#### Scenario: Geometria inválida é recusada

- **WHEN** chega um contorno do tipo ponto, ou com anel aberto, ou com coordenada fora da
  faixa de longitude e latitude
- **THEN** o núcleo responde 422, indicando o campo, e o contorno anterior permanece

#### Scenario: Elemento de origem fora do padrão do OSM é recusado

- **WHEN** chega um contorno cujo elemento de origem não é `way/<número>` nem
  `relation/<número>`
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Persona que não é Admin não grava contorno

- **WHEN** um Mestre, um Guerreiro(a), um responsável ou um Apoiador tenta gravar o contorno
- **THEN** o núcleo responde 403, e a comunidade permanece como estava

#### Scenario: Comunidade inexistente responde 404

- **WHEN** um Admin grava contorno numa comunidade que não existe
- **THEN** o núcleo responde 404
