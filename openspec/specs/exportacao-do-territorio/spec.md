## Purpose

A saída do dado do território em arquivo, para quem vai levá-lo embora — pesquisador, gestor
público, instituição. É o que transforma a série lida na tela em conjunto citável: formato
aberto, dicionário que explica cada campo, licença declarada e a contribuição à meta 17.18 dita
com o período que a sustenta.

## Requirements

### Requirement: A exportação do território é pública e sai em CSV

O núcleo SHALL expor a exportação da série de uma comunidade em **rota pública** — sem token de
sessão e com **chave de aplicação válida**, como qualquer rota de dados sob o prefixo de versão
—, devolvendo os dados em **CSV**. O CSV SHALL trazer **uma tabela por arquivo**, com
**cabeçalho declarado** na primeira linha, e SHALL usar formato aberto legível em planilha.
Comunidade inexistente SHALL receber **404**. A rota NEVER SHALL escrever. (`RF-08-19`,
`RF-01-02`, `RN-01-32`, documento 03 §12.3, PRD-08 §9)

#### Scenario: A exportação responde sem token de sessão

- **WHEN** chega um pedido de exportação de uma comunidade com chave de aplicação válida e sem
  token de sessão
- **THEN** o núcleo devolve o conjunto em CSV

#### Scenario: A exportação sem chave é recusada

- **WHEN** chega um pedido de exportação sem chave de aplicação
- **THEN** o núcleo responde 401, sem diferenciar chave ausente, inválida e revogada

#### Scenario: O CSV traz cabeçalho declarado na primeira linha

- **WHEN** a exportação de uma comunidade é gerada
- **THEN** a primeira linha nomeia todas as colunas, e cada linha seguinte é um recorte da
  série

#### Scenario: Comunidade inexistente responde 404

- **WHEN** chega um pedido de exportação de uma comunidade que não existe
- **THEN** o núcleo responde 404

### Requirement: A exportação recorta por período e declara o período coberto

O núcleo SHALL aceitar **período** na exportação, recortando pela **data da medição** — nunca
pela data do envio —, e SHALL declarar na saída o **período efetivamente coberto** pelo
conjunto. A declaração SHALL acompanhar o conjunto de forma legível por quem o receber, e NEVER
SHALL ficar apenas implícita nos dados. Pedido sem período SHALL exportar toda a série da
comunidade, e o período coberto declarado SHALL ser o da primeira e da última medição contidas.
(`RF-08-19`, `RF-08-27`, `RF-08-15`, `RF-01-28`)

#### Scenario: O período recorta pela data da medição

- **WHEN** uma exportação pede um período e há medições feitas dentro dele mas enviadas depois
- **THEN** o conjunto inclui essas medições, porque a data da medição é a que vale

#### Scenario: O conjunto declara o período que cobre

- **WHEN** uma exportação é gerada para um período
- **THEN** a saída declara explicitamente o período coberto pelo conjunto

#### Scenario: Exportação sem período cobre a série inteira

- **WHEN** uma exportação é pedida sem período
- **THEN** o conjunto cobre toda a série da comunidade, e o período declarado é o da primeira
  à última medição contida nele

### Requirement: A exportação acompanha um dicionário de dados

O núcleo SHALL entregar, junto do conjunto, um **dicionário de dados** que descreva **cada
campo** exportado, com a **unidade**, a **cadência** e a **origem** do dado. Nenhum campo do
conjunto SHALL ficar fora do dicionário, e o dicionário NEVER SHALL descrever campo que o
conjunto não traz. (`RF-08-19`, documento 03 §12.3)

#### Scenario: Todo campo exportado está no dicionário

- **WHEN** uma exportação é gerada
- **THEN** cada coluna do CSV tem entrada correspondente no dicionário, com unidade, cadência e
  origem

#### Scenario: O dicionário não descreve campo ausente

- **WHEN** se compara o dicionário com o cabeçalho do CSV
- **THEN** os dois conjuntos de campos coincidem exatamente

### Requirement: O conjunto declara a licença CC BY-SA e a contribuição à meta 17.18

O núcleo SHALL declarar, na saída da exportação, que o conjunto é licenciado em **CC BY-SA** e
que ele constitui a contribuição do projeto à **meta 17.18** — dado local, desagregado, datado e
de guarda permanente sobre um território periférico. A declaração da meta SHALL vir acompanhada
do **período coberto**, e NEVER SHALL afirmar movimento de indicador nacional: a contribuição
declarada é o **insumo**, não o resultado. (`RF-08-27`, documento 03 §12.3, documento 04 §4)

#### Scenario: A saída declara a licença do conjunto

- **WHEN** uma exportação é gerada
- **THEN** a saída declara a licença CC BY-SA

#### Scenario: A saída declara a contribuição à meta 17.18 com o período

- **WHEN** uma exportação é gerada
- **THEN** a saída declara a contribuição à meta 17.18 e o período coberto pelo conjunto

### Requirement: A exportação herda integralmente as guardas da leitura pública

O núcleo SHALL aplicar à exportação **as mesmas guardas** da série pública, sem exceção nem
afrouxamento: a agregação SHALL parar no **bairro**; o conjunto NEVER SHALL trazer
identificador, nick, nome, avatar ou qualquer atributo do Guerreiro(a) que coletou, nem a
contagem de coletores; o **piso de coletores distintos** SHALL valer igual, subindo ao nível
acima o recorte que não o alcança e **suprimindo** o que não o alcança nem no topo; e apenas
registro de situação **válida** SHALL compor o conjunto.

O piso SHALL ser apurado **sobre o período exportado**, pela mesma régua da consulta. Um
conjunto que sai em arquivo é mais fácil de cruzar que uma tela, de modo que afrouxar aqui
desfaria a proteção inteira. (`RN-08-12`, `RN-08-13`, `RF-08-28`, `RN-08-24`, `RN-08-09`,
invariante 7 do documento 99 §6, PRD-08 §§11, 12)

#### Scenario: O conjunto exportado não traz coletor

- **WHEN** uma exportação é gerada de uma comunidade cujos registros têm coletores
  identificados
- **THEN** nenhum identificador, nick, nome ou avatar de Guerreiro(a) aparece no conjunto, nem
  a contagem de coletores

#### Scenario: O conjunto exportado não desce abaixo do bairro

- **WHEN** uma exportação alcança registros gravados em locais de nível rua e abaixo
- **THEN** eles compõem o agregado do bairro que os contém, e nenhum rótulo abaixo do bairro
  aparece no conjunto

#### Scenario: O piso de coletores vale na exportação

- **WHEN** um recorte de tipo e bairro reúne menos coletores distintos que o piso no período
  exportado
- **THEN** os registros dele sobem para o nível da comunidade, e nenhum recorte daquele bairro
  aparece no conjunto

#### Scenario: Recorte abaixo do piso nem no topo fica fora do conjunto

- **WHEN** um tipo de coleta na comunidade inteira reúne menos coletores distintos que o piso
- **THEN** nenhum recorte daquele tipo aparece no conjunto exportado

#### Scenario: Registro invalidado fica fora do conjunto

- **WHEN** um registro da comunidade está com situação invalidada
- **THEN** ele não compõe linha, valor nem contagem do conjunto exportado
