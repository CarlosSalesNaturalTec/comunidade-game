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
creditada, projetada como avatar e nick de **cada creditado** — os integrantes da equipe da
trilha, na modalidade em equipe, e o Guerreiro(a) que a entregou, na individual —, e
SHALL aparecer **apenas** quando todos os creditados nela tiverem autorização de divulgação
vigente. A trilha NEVER SHALL ser filtrada por comunidade nesta capacidade: ela é bem comum da
plataforma. (`RF-01-62`, `RF-01-26`, `RF-09-33`, `RN-01-13`, `RN-01-42`, `RN-09-19`, PRD-03 §9)

A criação original pública SHALL trazer também a **data de validação** e o **nome da trilha** de
que ela nasceu, que o portfólio público exibe junto da autoria. A criação original NEVER SHALL
trazer título: o modelo não tem esse campo, e nenhum documento-fonte o define. (`RF-03-08`,
decisão do fundador, 2026-09-28)

Cada poder do catálogo público SHALL trazer os **Mestres responsáveis** dele — os autores das
trilhas publicadas daquele poder —, cada um com o **identificador** que alcança a leitura
individual do Mestre, mais avatar e nick, ou o nome quando a persona não tiver nick. Poder sem
trilha publicada SHALL sair com a lista de Mestres **vazia**, nunca omitida. (`RF-03-02`,
documento 11 §8.2, decisão do fundador, 2026-09-29)

#### Scenario: Catálogo público traz poderes e trilhas

- **WHEN** uma consulta pública pede os poderes
- **THEN** a resposta traz cada poder com as trilhas vinculadas a ele

#### Scenario: O poder traz os Mestres responsáveis

- **WHEN** um poder tem duas trilhas publicadas, de Mestres autores diferentes
- **THEN** a resposta traz os dois Mestres, sem repetição, cada um com o identificador que
  alcança a leitura individual dele

#### Scenario: Poder sem trilha publicada sai com a lista vazia

- **WHEN** um poder ativo não tem trilha publicada alguma
- **THEN** a resposta traz aquele poder com a lista de Mestres responsáveis vazia

#### Scenario: Criação original pública credita a autoria

- **WHEN** uma criação original validada aparece no portfólio público
- **THEN** ela traz o avatar e o nick de cada integrante creditado

#### Scenario: Criação individual pública credita quem a entregou

- **WHEN** uma criação original individual validada aparece no portfólio público
- **THEN** ela traz o avatar e o nick do Guerreiro(a) que a entregou

#### Scenario: Criação com integrante sem autorização não aparece

- **WHEN** uma criação original tem entre os creditados um Guerreiro(a) sem autorização vigente
- **THEN** a criação não aparece no portfólio público

#### Scenario: Criação individual sem autorização não aparece

- **WHEN** uma criação original individual validada é de Guerreiro(a) sem autorização vigente
- **THEN** a criação não aparece no portfólio público

#### Scenario: A criação pública traz data e trilha

- **WHEN** uma criação original validada aparece no portfólio público
- **THEN** ela traz a data em que foi validada e o nome da trilha de que nasceu

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

### Requirement: O card e o perfil públicos levam a carta do Guerreiro(a) inteira

O núcleo SHALL devolver, em `/vitrine/guerreiros` e em `/vitrine/guerreiros/{nick}`, a
composição que a variante Guerreiro(a) do documento 11 §8.2 exige: **avatar**, **nick**,
**badges**, **poderes com o nível alcançado em cada um**, **desempenho** — a posição no ranking
público e os pontos regulares acumulados — e as **criações originais** creditadas a ele. A
projeção SHALL ser **a mesma nas duas rotas**: o que o card mostra é o que a página mostra,
resumido. (`RF-01-21`, `RF-01-28`, `RF-01-33`, `RN-01-10`, `RN-01-11`, documento 11 §§8.1, 8.2,
PRD-03 §9, decisão do fundador, 2026-09-28)

A composição SHALL sair **na própria listagem**, sem exigir de quem consome uma consulta por
nick para cada Guerreiro(a) exibido: a consulta por nick tem freio por origem, e montar uma
página de cards com ela seria barrado pelo próprio freio. (`RF-01-65`, `RN-01-27`)

O portão da divulgação SHALL continuar valendo sobre a composição inteira, e a projeção NEVER
SHALL ganhar campo de nome civil, nascimento, contato, imagem real, valor em reais ou
identificador interno de comunidade. A projeção **mínima** de avatar e nick SHALL continuar
sendo a das demais superfícies desta capacidade — a autoria creditada nas criações e o elenco
dos jogos —, que NEVER SHALL mudar por causa desta. (`RN-01-10`, `RN-01-11`, invariantes 8, 12
e 16 do documento 99 §6)

#### Scenario: O card traz a composição inteira

- **WHEN** uma consulta pública pede os Guerreiros e Guerreiras
- **THEN** cada item traz avatar, nick, badges, poderes com nível, desempenho e as criações
  originais creditadas a ele

#### Scenario: A página por nick traz a mesma composição

- **WHEN** uma consulta pública pede o perfil por nick exato de quem tem autorização vigente
- **THEN** a resposta traz a mesma composição que o card daquele Guerreiro(a)

#### Scenario: A composição sai sem consulta por nick

- **WHEN** uma consulta pública pede uma página inteira de Guerreiros e Guerreiras
- **THEN** a composição de todos eles vem naquela resposta, sem que outra consulta seja
  necessária

#### Scenario: O portão da divulgação vale sobre a composição

- **WHEN** um Guerreiro(a) não tem autorização de divulgação vigente
- **THEN** nem ele nem a composição dele aparecem em qualquer das duas rotas

#### Scenario: A composição não traz nada de pessoal

- **WHEN** qualquer das duas rotas responde
- **THEN** nenhum campo traz nome civil, nascimento, contato, imagem real nem valor em reais

#### Scenario: A projeção mínima das outras superfícies não muda

- **WHEN** uma criação original pública credita a autoria, ou o elenco dos jogos devolve um
  Guerreiro(a)
- **THEN** ele continua projetado como avatar e nick, sem a composição do card

### Requirement: A leitura pública de Mestres sai em listagem e por identificador

O núcleo SHALL expor em rota pública a leitura de **Mestres**, na listagem e por
identificador, **sem token de sessão** e sob a chave de aplicação, como toda rota de dados sob
`/v1`. A resposta SHALL trazer, de cada Mestre: **avatar**, **nick**, as **áreas de
habilidade**, os **artefatos comprobatórios** — cada um com endereço e rótulo —, as **trilhas
publicadas de autoria** dele e a **contagem de absorções**, que é o selo de quem sustentou
atividade sem recurso.

As **áreas de habilidade** SHALL ser derivadas da área do conhecimento das trilhas publicadas
de autoria do Mestre, sem campo próprio na persona (decisão do fundador, 2026-09-29).

A resposta NEVER SHALL trazer e-mail, WhatsApp, valor em reais, dado bancário ou qualquer
canal de contato do Mestre, nem alcançar Guerreiro(a) algum. Identificador de persona que não
é Mestre e identificador inexistente SHALL receber **a mesma recusa 404**, de modo que a
resposta não confirme a existência de ninguém. (`RF-03-02`, `RF-03-07`, `RN-03-01`, PRD-03 §9)

#### Scenario: A listagem pública traz os Mestres

- **WHEN** uma consulta pública com chave válida e sem token de sessão pede os Mestres
- **THEN** a resposta traz cada Mestre com avatar, nick, áreas de habilidade, artefatos
  comprobatórios, trilhas de autoria e a contagem de absorções

#### Scenario: As áreas vêm das trilhas publicadas de autoria

- **WHEN** um Mestre é autor de duas trilhas publicadas, de áreas do conhecimento diferentes
- **THEN** a leitura pública dele traz as duas áreas, sem repetição

#### Scenario: A leitura pública do Mestre não traz contato

- **WHEN** um Mestre com e-mail e WhatsApp cadastrados aparece na leitura pública
- **THEN** a resposta traz avatar, nick e a prova declarada, e nenhum e-mail, WhatsApp ou
  canal de contato

#### Scenario: Persona que não é Mestre recebe a mesma recusa que a inexistente

- **WHEN** a leitura individual usa o identificador de uma persona de Guerreiro(a), de
  responsável ou de Admin
- **THEN** o núcleo responde 404, com a mesma recusa que daria a um identificador inexistente

### Requirement: A leitura pública de Apoiadores só alcança quem tem aporte homologado

O núcleo SHALL expor em rota pública a leitura de **Apoiadores**, na listagem e por
identificador, **sem token de sessão** e sob a chave de aplicação. A resposta SHALL trazer, de
cada Apoiador: **avatar**, **nick**, o **total em moedas**, o **nível de sustento**, os
**selos** conquistados, os **desafios extras propostos** e os **artefatos comprobatórios**,
cada um com endereço e rótulo.

Apoiador **sem aporte homologado** NEVER SHALL aparecer: fica fora da listagem, e a leitura
individual dele SHALL receber **o mesmo 404** do identificador inexistente. Nenhuma leitura
desta capacidade SHALL ordenar, classificar ou comparar Apoiadores por valor aportado — o que
se coleciona é selo e nível (`RN-14-38`).

A resposta NEVER SHALL trazer valor em reais, comprovante, dado bancário, e-mail, WhatsApp ou
dado de contato de Guerreiro(a) algum. (`RF-03-02`, `RF-03-07`, `RF-03-57`, `RN-03-26`,
PRD-03 §9)

#### Scenario: A listagem pública traz os Apoiadores com aporte homologado

- **WHEN** uma consulta pública com chave válida pede os Apoiadores
- **THEN** a resposta traz cada Apoiador com aporte homologado, com avatar, nick, total em
  moedas, nível de sustento, selos, desafios propostos e artefatos comprobatórios

#### Scenario: Apoiador sem aporte homologado não aparece

- **WHEN** um Apoiador cadastrado não tem nenhum aporte homologado
- **THEN** ele não aparece na listagem, e a leitura individual dele responde 404, a mesma
  recusa do identificador inexistente

#### Scenario: O aporte declarado e ainda não homologado não publica ninguém

- **WHEN** um Apoiador tem apenas declaração de aporte pendente de homologação
- **THEN** ele segue fora da leitura pública

#### Scenario: Nenhuma leitura ordena por valor

- **WHEN** a listagem pública de Apoiadores é consultada
- **THEN** a resposta não traz posição, pódio nem ordenação por valor aportado

### Requirement: O total do Apoiador sai em moedas, e o piso de 10 moedas decide o avatar

A leitura pública do Apoiador SHALL trazer o total **em moedas da plataforma**, medido pelas
**moedas acumuladas em aportes homologados** — o acumulado que não regride —, e NEVER SHALL
trazer valor em reais, nem em campo auxiliar algum.

Abaixo do piso de **10 moedas acumuladas**, a leitura SHALL declarar que o avatar a exibir é o
**avatar padrão do projeto**, com o mesmo nick e o mesmo total em moedas e nenhuma outra marca
de diferença. Alcançado o piso, o direito **NEVER SHALL regredir**. O avatar padrão SHALL
ocupar também o lugar de qualquer avatar que falte. (`RF-03-10`, `RF-03-55`, `RF-03-66`,
`RN-03-18`, `RN-03-26`, `RN-14-11`, documentos 11 §8.2 e 15 §7.3)

#### Scenario: O total sai em moedas

- **WHEN** um Apoiador com aportes registrados em reais aparece na leitura pública
- **THEN** a resposta traz apenas o total em moedas, sem campo algum com o valor em reais

#### Scenario: Abaixo do piso vale o avatar padrão

- **WHEN** um Apoiador tem 5 moedas acumuladas e avatar próprio gravado
- **THEN** a leitura pública declara o avatar padrão do projeto, com o nick e o total em
  moedas

#### Scenario: Alcançado o piso o avatar próprio aparece

- **WHEN** um Apoiador tem 10 moedas acumuladas ou mais e avatar próprio gravado
- **THEN** a leitura pública traz o avatar próprio dele

#### Scenario: O direito alcançado não regride

- **WHEN** o Apoiador já acumulou 10 moedas e um ressarcimento derruba o Poder Sustentador
  dele
- **THEN** a leitura pública segue trazendo o avatar próprio, porque o acumulado não regride

### Requirement: O adulto sem nick aparece em público pelo nome

A leitura pública de Mestre e de Apoiador SHALL trazer o **nome** da persona no lugar do nick
quando a persona **ainda não tiver nick**, e SHALL declarar qual dos dois está sendo servido,
para que a superfície não apresente nome como se fosse nick. O nick é opcional para adulto, e
o documento 11 §8.2 exige as duas variantes da carta com identificação (decisão do fundador,
2026-09-29).

Esta regra NEVER SHALL alcançar Guerreiro(a): o nome civil de criança ou adolescente não
aparece em superfície pública alguma, em hipótese nenhuma. (`RF-03-07`, `RN-03-04`,
`RF-03-79`, `RN-03-36`, invariantes 9 e 12 do documento 99 §6)

#### Scenario: Mestre sem nick aparece pelo nome

- **WHEN** um Mestre que ainda não definiu nick aparece na leitura pública
- **THEN** a resposta traz o nome dele, declarado como nome e não como nick

#### Scenario: Tendo nick, é o nick que sai

- **WHEN** um Mestre que já definiu nick aparece na leitura pública
- **THEN** a resposta traz o nick, e não o nome

#### Scenario: A regra nunca alcança Guerreiro(a)

- **WHEN** um Guerreiro(a) com autorização vigente aparece em qualquer leitura pública
- **THEN** a resposta traz o nick dele e nenhum nome civil, mesmo que a persona tenha nome
  gravado

### Requirement: A efetividade pública do Apoiador é agregada e não alcança quem concluiu

A leitura pública do Apoiador SHALL trazer, de cada **desafio extra proposto** por ele: a
**trilha** a que se vincula, o **período** em que correu e **quantos concluíram**. A resposta
NEVER SHALL trazer nick, avatar, nome ou dado algum de quem concluiu, NEVER SHALL trazer valor
em reais e NEVER SHALL abrir o recorte direcionado, em que o proponente vê apenas que houve
conclusão.

O painel completo de efetividade segue sendo **do próprio Apoiador e de mais ninguém**, na
App 08: esta é uma projeção pública agregada, não aquele painel (decisão do fundador,
2026-09-29). (`RF-03-80`, `RN-03-37`, `RN-03-01`, `RN-14-38`, documento 11 §8.2)

#### Scenario: O desafio proposto sai com trilha, período e contagem

- **WHEN** um Apoiador propôs um desafio extra que três Guerreiros e Guerreiras concluíram
- **THEN** a leitura pública traz a trilha, o período e a contagem de três conclusões

#### Scenario: Quem concluiu não aparece

- **WHEN** a leitura pública traz um desafio extra proposto e concluído
- **THEN** nela não aparece nick, avatar nem dado algum de quem concluiu

#### Scenario: O direcionado não se abre em público

- **WHEN** o desafio extra proposto é da modalidade direcionada
- **THEN** a leitura pública traz apenas que houve conclusão, sem alcançar o destinatário
