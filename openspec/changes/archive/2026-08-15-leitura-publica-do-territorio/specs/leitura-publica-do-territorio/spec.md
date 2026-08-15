## Purpose

A saída pública do dado do território: a série histórica de uma comunidade, agregada por tipo
de coleta e por local, sem nenhuma identificação de quem coletou. É a contrapartida da guarda
permanente com autoria — o dado é do lugar e volta para o lugar, e a anonimização acontece
aqui, na saída, nunca no armazenamento.

## ADDED Requirements

### Requirement: A leitura pública do território dispensa credencial de persona, nunca a chave

O núcleo SHALL responder às rotas de leitura pública do território **sem token de sessão**, e
SHALL exigir em todas elas a **chave de aplicação válida**, como em qualquer rota de dados sob
o prefixo de versão. A recusa por chave ausente, inválida ou revogada SHALL ser o **401**
indistinto que a capacidade `chave-de-aplicacao` já define. Nenhuma rota desta capacidade SHALL
escrever: todas são de leitura. (`RF-08-16`, `RF-01-02`, `RN-01-32`, `RN-01-33`, PRD-08 §9)

#### Scenario: Consulta pública do território responde sem token de sessão

- **WHEN** chega uma consulta da série pública de uma comunidade com chave de aplicação válida
  e sem token de sessão
- **THEN** o núcleo responde normalmente, e nenhum dado restrito acompanha a resposta

#### Scenario: Consulta pública do território sem chave é recusada

- **WHEN** chega uma consulta da série pública de uma comunidade sem chave de aplicação
- **THEN** o núcleo responde 401, sem diferenciar chave ausente, inválida e revogada

#### Scenario: A leitura pública do território não tem rota de escrita

- **WHEN** se procura nesta capacidade uma rota que crie, altere ou remova registro
- **THEN** nenhuma existe

### Requirement: A série pública é agregada por tipo de coleta e por local, e para no bairro

O núcleo SHALL devolver a série histórica de uma comunidade **agregada** pelo par **tipo de
coleta × local**, e o local mais específico que a saída pública alcança SHALL ser o **bairro**.
Recorte de **rua, condomínio, bloco ou quadra** NEVER SHALL sair por esta rota, qualquer que
seja o parâmetro recebido: registro gravado em local abaixo do bairro SHALL entrar na
agregação do **bairro que o contém**, e o rótulo do local abaixo do bairro NEVER SHALL aparecer
na resposta. Registro cujo local é a própria comunidade SHALL agregar no recorte da comunidade.

A agregação SHALL alcançar apenas registro de situação **válida**. Registro invalidado NEVER
SHALL compor valor, contagem ou contagem de coletores de nenhum recorte publicado.
(`RF-08-16`, `RN-08-13`, `RN-08-09`, invariante 17 do documento 99 §6, PRD-08 §§5.6, 8, 9)

#### Scenario: A série pública sai por tipo de coleta e bairro

- **WHEN** uma consulta pública pede a série de uma comunidade que tem registros de dois tipos
  de coleta em dois bairros
- **THEN** cada medição devolvida vem sob o recorte do seu par de tipo e bairro, e os quatro
  pares aparecem distintos na resposta

#### Scenario: Registro de rua entra no bairro que o contém

- **WHEN** um registro foi gravado num local de nível rua
- **THEN** ele compõe o agregado do bairro acima daquela rua, e o rótulo da rua não aparece na
  resposta

#### Scenario: Nenhum recorte abaixo do bairro é devolvido

- **WHEN** uma consulta pública percorre toda a resposta da série de uma comunidade
- **THEN** nenhum recorte de nível rua, condomínio, bloco ou quadra aparece nela

#### Scenario: Registro invalidado fica fora da agregação

- **WHEN** um registro da comunidade está com situação invalidada
- **THEN** ele não compõe valor, contagem nem contagem de coletores de recorte algum

### Requirement: A saída pública do território nunca leva o coletor

O núcleo NEVER SHALL incluir na resposta pública do território o **identificador**, o **nick**,
o **nome**, o **avatar** ou qualquer outro atributo do Guerreiro(a) que coletou, nem recorte,
filtro ou ordenação que isole um coletor. A contagem de coletores distintos SHALL servir apenas
de guarda interna do piso e NEVER SHALL sair na resposta.

O vínculo entre registro e coletor SHALL permanecer gravado e inalterado: a anonimização é da
**saída**, nunca do armazenamento. (`RF-08-16`, `RN-08-12`, `RN-08-11`, invariante 7 do
documento 99 §6, PRD-08 §§5.6, 11, 12)

#### Scenario: A resposta pública não traz nick, nome nem avatar

- **WHEN** uma consulta pública pede a série de uma comunidade cujos registros têm coletores
  identificados
- **THEN** nenhum nick, nome, avatar ou identificador de Guerreiro(a) aparece na resposta

#### Scenario: Não há recorte da série pública por coletor

- **WHEN** uma consulta pública tenta recortar a série por um Guerreiro(a)
- **THEN** o núcleo não oferece esse recorte, e nenhuma resposta o produz

#### Scenario: A leitura pública não altera o vínculo de autoria

- **WHEN** a série pública de uma comunidade é consultada
- **THEN** os registros seguem gravados com o coletor de cada um, inalterados

### Requirement: A saída pública não leva a mídia do registro

O núcleo NEVER SHALL devolver, em rota pública do território, a **foto ou o vídeo** do
registro, nem referência que permita alcançá-lo. O PRD-08 §11 condiciona o acesso público à
mídia à **auditoria**, e a auditoria por amostragem do Mestre não existe no núcleo: publicar
antes dela exporia mídia que `RN-08-16` manda invalidar quando contiver pessoa identificável.

O ponto de série cujo tipo de coleta declara a forma **foto** ou **vídeo** SHALL sair mesmo
assim, com a **data e hora da medição** e o recorte a que pertence, e **sem valor numérico** —
a evidência conta como medição, e só o arquivo fica retido. (`RF-08-16`, `RF-08-21`,
`RN-08-16`, PRD-08 §11)

#### Scenario: A resposta pública não traz a mídia nem a referência dela

- **WHEN** uma consulta pública alcança um recorte cujo tipo de coleta declara a forma foto
- **THEN** nenhuma mídia e nenhuma referência de mídia acompanham a resposta

#### Scenario: O registro por mídia entra na série sem valor numérico

- **WHEN** uma consulta pública alcança um registro gravado por foto
- **THEN** o ponto sai com a data e hora da medição e o recorte, sem valor numérico

### Requirement: Recorte com menos coletores que o piso sobe para o nível acima

O núcleo SHALL publicar um recorte apenas quando ele reunir ao menos o **piso de coletores
distintos**. Recorte que não alcança o piso NEVER SHALL sair sozinho: os seus registros SHALL
ser somados ao recorte do **nível imediatamente acima** — do bairro para a comunidade —, e o
recorte que não alcançou o piso NEVER SHALL aparecer na resposta, nem como linha vazia, nem
como contagem, nem como qualquer marca que denuncie a existência dele.

Recorte que não alcança o piso **nem no nível mais alto** — a própria comunidade — NEVER SHALL
ser publicado. Não há nível acima da comunidade para o qual subir, e publicá-lo abaixo do piso
contrariaria a regra que a subida existe para cumprir.

O piso SHALL ser **parâmetro declarado na implantação**, com **três** como valor inicial.
(`RF-08-28`, `RN-08-24`, `RN-08-13`, PRD-08 §§7, 9)

#### Scenario: Bairro com três coletores distintos sai sozinho

- **WHEN** um recorte de tipo e bairro reúne registros de três coletores distintos
- **THEN** o núcleo publica aquele recorte com o seu agregado

#### Scenario: Bairro com dois coletores sobe para a comunidade

- **WHEN** um recorte de tipo e bairro reúne registros de apenas dois coletores distintos
- **THEN** os registros dele compõem o recorte daquele tipo no nível da comunidade, e nenhum
  recorte daquele bairro aparece na resposta

#### Scenario: A subida não deixa rastro do recorte suprimido

- **WHEN** um recorte sobe por não alcançar o piso
- **THEN** a resposta não traz linha vazia, contagem zerada nem rótulo do bairro suprimido

#### Scenario: Recorte que não alcança o piso nem na comunidade não é publicado

- **WHEN** todos os registros de um tipo de coleta na comunidade vêm de dois coletores
  distintos
- **THEN** nenhum recorte daquele tipo aparece na resposta

#### Scenario: O piso vale pelo valor declarado na implantação

- **WHEN** a implantação declara um piso diferente de três
- **THEN** o núcleo aplica o valor declarado em toda decisão de publicar ou subir o recorte

### Requirement: A série pública é paginada e recorta por período

O núcleo SHALL paginar a série pública no mesmo contrato das demais listagens: SHALL aceitar
**cursor** e **tamanho de página**, SHALL devolver os itens da página junto do **cursor
seguinte** — nulo na última página — e SHALL recusar com **422** o tamanho acima do teto e o
**parâmetro que não declara**.

O item paginado SHALL ser o **ponto da série** — a medição, com a data e hora em que aconteceu
—, e cada ponto SHALL carregar o **recorte** a que pertence: o tipo de coleta e o local
publicado. A ordenação SHALL ser estável, de modo que nenhum ponto se repita entre páginas nem
falte a alguma delas.

A consulta SHALL aceitar **período**, recortando pela **data da medição** — a mesma que toda
regra do registro dependente de tempo já usa, nunca a data do envio. O piso de coletores SHALL
ser apurado **sobre o período consultado**, não sobre a série inteira: o recorte que alcança o
piso no total e não o alcança no período pedido NEVER SHALL ser publicado naquele período.
(`RF-01-28`, `RF-08-15`, `RF-08-16`, `RN-08-24`)

#### Scenario: A consulta devolve uma página com o cursor seguinte

- **WHEN** uma consulta pública pede a série de uma comunidade com mais pontos do que o
  tamanho de página pedido
- **THEN** o núcleo devolve só o tamanho pedido, acompanhado do cursor da página seguinte

#### Scenario: O cursor percorre todos os pontos sem repetir nenhum

- **WHEN** a consulta percorre as páginas seguindo o cursor devolvido até ele vir nulo
- **THEN** o núcleo terá devolvido cada ponto publicável uma única vez, sem repetição e sem
  falta

#### Scenario: O piso não muda de página para página

- **WHEN** um recorte é suprimido por não alcançar o piso e a consulta percorre todas as
  páginas
- **THEN** nenhum ponto daquele recorte aparece sob o rótulo do bairro em nenhuma página

#### Scenario: Parâmetro não declarado é recusado

- **WHEN** chega uma consulta pública com um parâmetro que a rota não declara
- **THEN** o núcleo responde 422 apontando o parâmetro, e nada é devolvido

#### Scenario: O período recorta pela data da medição

- **WHEN** uma consulta pública pede um período em que houve medições registradas depois dele
- **THEN** o núcleo inclui as medições cuja **data da medição** cai no período, qualquer que
  seja a data em que foram enviadas

#### Scenario: O piso é apurado dentro do período consultado

- **WHEN** um recorte reúne três coletores distintos na série inteira e apenas dois dentro do
  período pedido
- **THEN** o núcleo não publica aquele recorte naquele período, e sobe os registros dele

### Requirement: A comunidade responde em leitura pública com os locais até o bairro

O núcleo SHALL expor em leitura pública a **comunidade**, com os seus **locais até o bairro** e
os **tipos de coleta ativos** nela — os tipos sobre os quais há desafio com série aberta
naquela comunidade. Local de nível **rua ou abaixo** NEVER SHALL aparecer nesta rota, pela
mesma linha de corte da série. Comunidade inexistente SHALL receber **404**. (`RF-08-16`,
`RN-08-13`, PRD-08 §9)

#### Scenario: A comunidade pública traz os seus bairros

- **WHEN** uma consulta pública pede uma comunidade que tem bairros e ruas cadastrados
- **THEN** o núcleo devolve a comunidade com os locais de nível comunidade e bairro, e nenhum
  de nível rua ou abaixo

#### Scenario: A comunidade pública traz os tipos de coleta ativos nela

- **WHEN** uma consulta pública pede uma comunidade em que há séries abertas de dois tipos de
  coleta
- **THEN** o núcleo devolve aqueles dois tipos, e não os tipos do catálogo sem série ali

#### Scenario: Comunidade inexistente responde 404

- **WHEN** uma consulta pública pede uma comunidade que não existe
- **THEN** o núcleo responde 404
