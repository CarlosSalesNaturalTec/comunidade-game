## Purpose

A leitura pública é a única superfície do núcleo que responde sem credencial de persona: o
visitante vê o que a plataforma produz sem se identificar, e nunca se identifica. Esta
capacidade cobre as seis rotas de consulta da vitrine, o portão do consentimento de
divulgação que decide quem aparece nelas e a projeção que garante que nada de pessoal
atravesse a fronteira do público.

## Requirements

### Requirement: A rota de vitrine dispensa credencial de persona, nunca a chave

O núcleo SHALL responder a toda rota sob `/v1/vitrine` **sem token de sessão**, e SHALL exigir
em todas elas a **chave de aplicação válida**, como em qualquer rota de dados sob `/v1`. A
recusa por chave ausente, inválida ou revogada SHALL ser o **401** indistinto que a capacidade
`chave-de-aplicacao` já define. Nenhuma rota desta capacidade SHALL escrever: todas são de
leitura. (`RF-01-02`, `RN-01-32`, `RN-01-33`, PRD-01 §9)

#### Scenario: Consulta pública responde sem token de sessão

- **WHEN** chega uma consulta de vitrine com chave de aplicação válida e sem token de sessão
- **THEN** o núcleo responde normalmente, e nenhum dado restrito acompanha a resposta

#### Scenario: Consulta pública sem chave é recusada

- **WHEN** chega uma consulta de vitrine sem chave de aplicação
- **THEN** o núcleo responde 401, sem diferenciar chave ausente, inválida e revogada

#### Scenario: A vitrine não tem rota de escrita

- **WHEN** se procura sob `/v1/vitrine` uma rota que crie, altere ou remova registro
- **THEN** nenhuma existe

### Requirement: Só aparece em público quem tem autorização de divulgação vigente

O núcleo SHALL exibir um Guerreiro(a) em qualquer superfície pública — card, perfil por nick,
ranking, criação original e elenco do jogo — **apenas** quando houver, para ele, autorização de
divulgação **vigente**. Sem ela, o Guerreiro(a) SHALL ficar ausente da listagem, sem lacuna,
contagem ou posição vazia que denuncie a existência dele. A revogação SHALL valer **para
frente** e ter efeito **imediato** na parte pública, sem prejuízo da participação e sem apagar
nada internamente. (`RN-01-10`, `RN-01-21`, invariantes 8 e 12 do documento 99 §6)

#### Scenario: Guerreiro(a) com autorização vigente aparece

- **WHEN** um Guerreiro(a) tem autorização de divulgação vigente e uma consulta pública o
  alcançaria
- **THEN** ele aparece na resposta, por avatar e nick

#### Scenario: Guerreiro(a) sem autorização não aparece em lugar nenhum

- **WHEN** um Guerreiro(a) não tem autorização de divulgação vigente
- **THEN** ele não aparece em card, ranking, criação original nem elenco do jogo

#### Scenario: A ausência não deixa rastro na listagem

- **WHEN** uma listagem pública exclui Guerreiros e Guerreiras sem autorização
- **THEN** a resposta não traz posição vazia, contagem total que os inclua nem qualquer marca
  de que alguém foi omitido

#### Scenario: Revogar tira do público na hora

- **WHEN** o responsável revoga a autorização de divulgação de um Guerreiro(a)
- **THEN** a consulta pública seguinte já não o alcança, e o que ele realizou continua
  registrado internamente

#### Scenario: Sem autorização, a participação continua

- **WHEN** um Guerreiro(a) não tem autorização de divulgação
- **THEN** nenhuma operação de participação dele é recusada por causa disso

### Requirement: A saída pública leva avatar, nick e progressão, e nada de pessoal

O núcleo SHALL projetar todo Guerreiro(a) em saída pública como **avatar e nick** mais a
progressão que aquela rota expõe. A saída pública NEVER SHALL conter nome civil, data de
nascimento, dado de contato, imagem real, valor em reais nem o identificador interno da
comunidade de residência do Guerreiro(a). A mesma projeção SHALL valer em todas as rotas desta
capacidade. (`RN-01-10`, `RN-01-11`, invariantes 12 e 16 do documento 99 §6)

#### Scenario: Card traz avatar e nick

- **WHEN** uma consulta pública devolve um Guerreiro(a)
- **THEN** a resposta traz o avatar e o nick dele, e nenhum nome, contato ou imagem

#### Scenario: Nenhuma saída pública traz valor em reais

- **WHEN** qualquer rota desta capacidade responde
- **THEN** nenhum campo da resposta expressa valor em reais

#### Scenario: Nenhuma saída pública traz imagem de criança

- **WHEN** qualquer rota desta capacidade devolve um Guerreiro(a)
- **THEN** nenhuma imagem real acompanha a resposta, e o avatar é a única representação

### Requirement: O perfil público responde por nick exato, e a recusa é sempre a mesma

O núcleo SHALL responder ao perfil público **apenas por correspondência exata** de nick. O
núcleo NEVER SHALL expor nesta capacidade busca parcial, sugestão, completação, ordenação por
semelhança ou contagem de resultados. A recusa por **nick inexistente** e a recusa por **nick
sem autorização de divulgação** SHALL ser o **mesmo 404**, indistinguíveis uma da outra.
(`RF-01-33`, `RF-01-34`, `RN-01-22`, PRD-03 §9)

#### Scenario: Nick exato de quem autorizou devolve o perfil

- **WHEN** chega uma consulta pelo nick exato de um Guerreiro(a) com autorização vigente
- **THEN** o núcleo devolve o perfil público dele

#### Scenario: Nick inexistente devolve 404

- **WHEN** chega uma consulta por um nick que não existe
- **THEN** o núcleo responde 404

#### Scenario: Nick sem autorização devolve o mesmo 404

- **WHEN** chega uma consulta pelo nick exato de um Guerreiro(a) sem autorização vigente
- **THEN** o núcleo responde 404, com corpo idêntico ao do nick inexistente

#### Scenario: Nick parcial não alcança ninguém

- **WHEN** chega uma consulta com parte de um nick existente
- **THEN** o núcleo responde 404, sem sugerir variação nem indicar quantos nicks se pareceriam

### Requirement: O ranking público ordena por ponto regular e alcança só quem autorizou

O núcleo SHALL montar o ranking público a partir do **ponto regular** já creditado, e SHALL
incluir nele **apenas** Guerreiros e Guerreiras com autorização de divulgação vigente. A posição
SHALL ser calculada sobre o conjunto exibido, de modo que a exclusão de quem não autorizou não
abra buraco na numeração. O ranking SHALL aceitar filtro por comunidade e SHALL ser paginado,
como toda listagem. (`RF-01-21`, `RF-01-28`, `RN-01-10`, PRD-03 §9)

O ranking NEVER SHALL contar o débito das **ocorrências de conduta de ciclo já encerrado**: a
ocorrência sai do ranking ao fim do ciclo. O débito SHALL permanecer no saldo de ponto regular
do Guerreiro(a), porque o débito não desfaz percurso, e o lançamento SHALL permanecer
consultável pela gestão e pelo responsável. (`RF-02-100`, documento 11 §5)

#### Scenario: Ranking ordena por ponto regular

- **WHEN** uma consulta pública pede o ranking
- **THEN** os Guerreiros e Guerreiras vêm ordenados pelo ponto regular acumulado

#### Scenario: Quem não autorizou fica fora e a numeração não pula

- **WHEN** um Guerreiro(a) sem autorização teria a segunda maior pontuação
- **THEN** ele não aparece, e quem vem depois dele ocupa a segunda posição

#### Scenario: Ranking filtra por comunidade

- **WHEN** uma consulta pública pede o ranking de uma comunidade
- **THEN** a resposta traz apenas Guerreiros e Guerreiras daquela comunidade

#### Scenario: Ocorrência de ciclo encerrado não pesa no ranking

- **WHEN** o ranking é consultado depois do encerramento do ciclo, para um Guerreiro(a) que
  sofreu ocorrência de conduta naquele ciclo
- **THEN** a posição dele é calculada sem o débito daquela ocorrência

#### Scenario: Ocorrência do ciclo corrente segue pesando

- **WHEN** o ranking é consultado e há ocorrência de conduta lançada depois do último
  encerramento de ciclo
- **THEN** o débito daquela ocorrência continua contando na posição

#### Scenario: Sair do ranking não devolve ponto ao saldo

- **WHEN** o encerramento do ciclo tira do ranking a ocorrência de um Guerreiro(a)
- **THEN** o saldo de ponto regular dele permanece como ficou depois do débito

### Requirement: Poderes, trilhas e criações originais respondem em leitura pública

O núcleo SHALL expor em rota pública o **catálogo de poderes** com as trilhas vinculadas a cada
um, e o **portfólio de criações originais** validadas. A criação original SHALL trazer a autoria
creditada, projetada como avatar e nick de cada integrante da equipe da trilha que a entregou, e
SHALL aparecer **apenas** quando todos os creditados nela tiverem autorização de divulgação
vigente. A trilha NEVER SHALL ser filtrada por comunidade nesta capacidade: ela é bem comum da
plataforma. (`RF-01-62`, `RF-01-26`, `RN-01-13`, `RN-01-42`, PRD-03 §9)

#### Scenario: Catálogo público traz poderes e trilhas

- **WHEN** uma consulta pública pede os poderes
- **THEN** a resposta traz cada poder com as trilhas vinculadas a ele

#### Scenario: Criação original pública credita a autoria

- **WHEN** uma criação original validada aparece no portfólio público
- **THEN** ela traz o avatar e o nick de cada integrante creditado

#### Scenario: Criação com integrante sem autorização não aparece

- **WHEN** uma criação original tem entre os creditados um Guerreiro(a) sem autorização vigente
- **THEN** a criação não aparece no portfólio público

### Requirement: A cobertura de ODS sai em rota pública, agregada por comunidade e ciclo

O núcleo SHALL expor a cobertura de ODS em rota pública, **sempre agregada** por comunidade e
por ciclo. A cobertura NEVER SHALL ser exposta por Guerreiro(a) individual, nem permitir recorte
que chegue a um. O **ciclo** SHALL ser o rótulo declarado na implantação, e a resposta SHALL
carregá-lo explicitamente. (`RF-01-43`, `RF-01-42`, `RN-01-24`, invariante 20 do documento 99 §6)

A rota SHALL refletir as **duas fontes** da cobertura por comunidade — as trilhas com Resultado
registrado e os **desafios de coleta com série aberta** —, e SHALL alcançar a comunidade cuja
única atividade é a coleta. O contrato da rota NEVER SHALL mudar por causa da fonte nova:
segue agregada por comunidade e ciclo, e segue sem recorte por Guerreiro(a). (`RF-08-26`,
`RN-08-22`)

#### Scenario: Cobertura pública vem agregada por comunidade e ciclo

- **WHEN** uma consulta pública pede a cobertura de ODS
- **THEN** a resposta traz os objetivos distintos por comunidade, com o rótulo do ciclo

#### Scenario: A cobertura pública inclui o objetivo vindo da coleta

- **WHEN** uma comunidade tem série aberta sobre desafio de coleta etiquetado
- **THEN** a resposta pública daquela comunidade inclui o objetivo do desafio

#### Scenario: Comunidade só com coleta aparece na cobertura pública

- **WHEN** uma comunidade não tem Resultado registrado e tem série aberta sobre desafio
  etiquetado
- **THEN** ela aparece na resposta pública, com o objetivo do desafio

#### Scenario: Não há recorte de cobertura por Guerreiro(a)

- **WHEN** uma consulta pública tenta recortar a cobertura por um Guerreiro(a)
- **THEN** o núcleo não oferece esse recorte, e nenhuma resposta o produz
