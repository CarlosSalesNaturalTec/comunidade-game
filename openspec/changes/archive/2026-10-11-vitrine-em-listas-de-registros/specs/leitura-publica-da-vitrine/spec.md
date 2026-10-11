# Spec Delta

## MODIFIED Requirements

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

O portfólio público SHALL responder em ordem **decrescente** por data de validação, da criação
mais recente para a mais antiga, e a paginação por cursor SHALL percorrer essa ordem sem pular
nem repetir criação. (`RF-03-83`, decisão do fundador, 2026-10-11)

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

#### Scenario: O portfólio responde da mais recente para a mais antiga

- **WHEN** uma consulta pública pede o portfólio de criações originais
- **THEN** a primeira criação da resposta é a validada mais recentemente

#### Scenario: A paginação do portfólio não pula nem repete

- **WHEN** uma consulta pública percorre o portfólio inteiro por cursor, em páginas de dez
- **THEN** cada criação apareceu uma vez, em ordem decrescente de data de validação

### Requirement: A leitura pública de Mestres sai em listagem e por identificador

O núcleo SHALL expor em rota pública a leitura de **Mestres**, na listagem e por
identificador, **sem token de sessão** e sob a chave de aplicação, como toda rota de dados sob
`/v1`. A resposta SHALL trazer, de cada Mestre: **avatar**, **nick**, as **áreas de
habilidade**, os **artefatos comprobatórios** — cada um com endereço e rótulo —, as **trilhas
publicadas de autoria** dele e a **contagem de absorções**, que é o selo de quem sustentou
atividade sem recurso.

As **áreas de habilidade** SHALL ser derivadas da área do conhecimento das trilhas publicadas
de autoria do Mestre, sem campo próprio na persona (decisão do fundador, 2026-09-29).

A listagem SHALL responder em ordem **alfabética** pela **identificação pública** de cada
Mestre — o nick quando há, o nome quando não —, e a paginação por cursor SHALL percorrer essa
ordem sem pular nem repetir Mestre. (`RF-03-83`, `RF-03-79`, decisão do fundador, 2026-10-11)

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

#### Scenario: A listagem de Mestres sai em ordem alfabética

- **WHEN** uma consulta pública pede os Mestres, e há Mestre com nick e Mestre só com nome
- **THEN** a resposta sai em ordem alfabética pela identificação pública de cada um, com nick e
  nome na mesma ordenação

#### Scenario: A paginação de Mestres não pula nem repete

- **WHEN** uma consulta pública percorre os Mestres por cursor, em páginas de dez
- **THEN** cada Mestre apareceu uma vez, em ordem alfabética

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

A listagem SHALL responder em ordem **alfabética** pela **identificação pública** de cada
Apoiador — o nick quando há, o nome quando não —, e a paginação por cursor SHALL percorrer essa
ordem sem pular nem repetir Apoiador. É essa ordem, e não a omissão do total em moedas, que
cumpre a proibição de pódio. (`RF-03-83`, `RF-03-79`, `RN-03-40`, decisão do fundador,
2026-10-11)

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

#### Scenario: A listagem de Apoiadores sai em ordem alfabética

- **WHEN** uma consulta pública pede os Apoiadores, e há Apoiador com nick e Apoiador só com
  nome
- **THEN** a resposta sai em ordem alfabética pela identificação pública de cada um, com nick e
  nome na mesma ordenação

#### Scenario: A paginação de Apoiadores não pula nem repete

- **WHEN** uma consulta pública percorre os Apoiadores por cursor, em páginas de dez
- **THEN** cada Apoiador apareceu uma vez, em ordem alfabética, e nenhum totalizou posição
