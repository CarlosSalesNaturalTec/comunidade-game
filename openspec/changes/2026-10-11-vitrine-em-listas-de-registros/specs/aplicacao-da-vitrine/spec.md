# Spec Delta

## ADDED Requirements

### Requirement: A seção de leitura apresenta um registro por linha

A App 06 SHALL apresentar cada seção de leitura como **lista de registros**: uma linha por
registro, com o **avatar** quando o registro tem um e os **dados principais** da carta daquele
papel. A linha NEVER SHALL trazer cabeçalho de coluna, grade de tabela ou coluna que apareça
só a partir de uma largura. (`RF-03-02`, documento 11 §8.2)

#### Scenario: Cada registro ocupa uma linha

- **WHEN** uma seção de leitura é aberta e o núcleo devolve três registros
- **THEN** três linhas aparecem, cada uma com o avatar, quando o registro tem um, e os dados
  principais da carta daquele papel

#### Scenario: A lista não é tabela

- **WHEN** qualquer seção de leitura é aberta, em qualquer largura de tela
- **THEN** nenhuma linha traz cabeçalho de coluna ou grade, e nenhuma coluna aparece ou
  desaparece com a largura

#### Scenario: Registro sem avatar não abre buraco

- **WHEN** a seção de comunidades é aberta, e a Comunidade Virtual não tem avatar
- **THEN** a linha sai sem avatar, com nome, localização e vitalidade, e nenhum espaço vazio
  anuncia a ausência

### Requirement: A lista de leitura pagina em 10 registros, com avançar e voltar

Cada seção de leitura SHALL apresentar **10 registros por página**, com controle de **avançar**
e de **voltar** e a **posição declarada em texto**. Avançar e voltar SHALL percorrer a lista
inteira sem pular nem repetir registro, e NEVER SHALL guardar nada no aparelho do visitante.
(`RF-03-82`, `RN-03-22`)

#### Scenario: A primeira página traz dez registros

- **WHEN** uma seção de leitura é aberta e o núcleo tem mais de dez registros
- **THEN** dez linhas aparecem, com a posição em texto e o controle de avançar

#### Scenario: Avançar e voltar percorrem a lista inteira

- **WHEN** o visitante avança até a última página e volta até a primeira
- **THEN** cada registro apareceu uma vez, nenhum foi pulado e nenhum se repetiu

#### Scenario: A lista curta não oferece paginação

- **WHEN** uma seção de leitura é aberta e o núcleo devolve menos de dez registros
- **THEN** nenhum controle de avançar ou voltar é apresentado

#### Scenario: Percorrer a lista não guarda nada

- **WHEN** o visitante percorre várias páginas e fecha a aba
- **THEN** nada da navegação dele ficou gravado no aparelho ou no servidor

### Requirement: Cada seção de leitura declara a sua ordem

Cada seção de leitura SHALL apresentar os registros na ordem que o `RF-03-83` fixa: o
**ranking** por posição, o **portfólio** por data de validação **decrescente**, e **Mestres**,
**Apoiadores** e **Comunidades Virtuais** em ordem **alfabética** pela identificação que a
linha exibe. (`RF-03-83`)

#### Scenario: O portfólio abre pela criação mais recente

- **WHEN** o visitante abre o portfólio
- **THEN** a primeira linha é a criação validada mais recentemente

#### Scenario: Mestres, Apoiadores e comunidades saem em ordem alfabética

- **WHEN** qualquer das três seções é aberta
- **THEN** as linhas saem em ordem alfabética pela identificação que cada uma exibe

### Requirement: A vitrine não lista Guerreiros e Guerreiras

A App 06 SHALL apresentar a seção **Guerreiros e Guerreiras** com a **consulta por nick exato**
e nada mais, e NEVER SHALL listar, paginar ou rotacionar Guerreiros e Guerreiras em seção
alguma. A seção SHALL dizer, em uma frase, que a vitrine não lista quem está cadastrado.

A App 06 NEVER SHALL consumir a listagem pública de Guerreiros e Guerreiras, que **permanece
servida pelo núcleo** para quem constrói sobre a API. (`RF-03-12`, `RF-03-13`, `RN-03-06`)

#### Scenario: A seção traz a consulta e nenhuma lista

- **WHEN** o visitante abre a seção de Guerreiros e Guerreiras
- **THEN** ele encontra o campo de nick exato e a frase de que a vitrine não lista quem está
  cadastrado, e nenhum Guerreiro(a) é apresentado

#### Scenario: Nenhuma tela pública rotaciona conteúdo

- **WHEN** o visitante permanece em qualquer tela pública da vitrine
- **THEN** nada troca sozinho, e nada que ele precise ler depende de animação

#### Scenario: A listagem segue pública para terceiros

- **WHEN** uma aplicação de terceiro com chave válida pede a listagem pública de Guerreiros e
  Guerreiras
- **THEN** o núcleo responde, mesmo que a vitrine não a consuma

### Requirement: Cada linha abre a página individual, em endereço próprio

Cada linha SHALL abrir a **página individual** do personagem, em **endereço próprio**,
compartilhável e alcançável diretamente. A página de Guerreiro(a) SHALL ser alcançada pela
**consulta por nick exato**, pela **linha do ranking** e pelo **nick do autor no portfólio** —
nunca por linha de uma listagem de Guerreiros, que não existe. (`RF-03-03`, PRD-03 §5.1)

#### Scenario: A linha leva à página

- **WHEN** o visitante aciona uma linha de Mestre, de Apoiador ou de comunidade
- **THEN** a página individual daquele personagem abre, em endereço próprio

#### Scenario: A linha do ranking abre a página do Guerreiro(a)

- **WHEN** o visitante aciona uma linha do ranking
- **THEN** a página individual daquele Guerreiro(a) abre, em endereço próprio

#### Scenario: No portfólio, é o nick do autor que abre a página

- **WHEN** o visitante abre o portfólio e aciona o nick de um autor creditado
- **THEN** a página individual daquele Guerreiro(a) abre, e acionar o resto da linha não abre
  página alguma, porque a criação original não tem página individual

#### Scenario: O endereço direto resolve

- **WHEN** alguém abre diretamente o endereço da página de um Guerreiro(a) com autorização
  vigente
- **THEN** a página abre com a composição do documento 11 §8.2

### Requirement: A seção de Mestres apresenta cada Mestre em linha e em página

A App 06 SHALL apresentar a seção **Mestres** com uma linha por Mestre, e cada linha SHALL
abrir a **página individual do Mestre** em endereço próprio, alcançável direto e
compartilhável.

A página SHALL detalhar o que o documento 11 §8.2 atribui a ela: as **habilidades**, as
**trilhas de autoria**, a **prova pública** — currículo, portfólios, redes sociais e
documentos comprobatórios externos, cada um como link com rótulo — e **quantas vezes ele
sustentou atividade que estava sem recurso**, na variante Mestre da carta.

A App 06 NEVER SHALL oferecer edição da página: editar é ato do próprio Mestre, na App 09.
(`RF-03-02`, `RF-03-03`, `RF-03-07`, PRD-03 §4, documento 11 §8.2)

#### Scenario: Cada Mestre sai em linha

- **WHEN** a seção de Mestres é aberta e o núcleo devolve três Mestres
- **THEN** três linhas aparecem, cada uma com avatar, a identificação e as áreas de habilidade

#### Scenario: A linha abre a página do Mestre em endereço próprio

- **WHEN** o visitante aciona a linha de um Mestre
- **THEN** a página daquele Mestre abre em endereço próprio, com a carta dominando a tela, e o
  mesmo endereço, aberto direto, leva à mesma página

#### Scenario: A página traz a prova pública como link

- **WHEN** o visitante abre a página de um Mestre com currículo e portfólio declarados
- **THEN** os dois aparecem como link, cada um com o rótulo do que aponta

#### Scenario: A vitrine não edita a página do Mestre

- **WHEN** o visitante abre a página de um Mestre
- **THEN** nenhuma ação de editar, acrescentar ou remover é apresentada

### Requirement: A seção de Apoiadores apresenta cada Apoiador em linha e em página

A App 06 SHALL apresentar a seção **Apoiadores** com uma linha por Apoiador, levando o
**total em moedas**, e cada linha SHALL abrir a **página individual do Apoiador** em endereço
próprio, alcançável direto e compartilhável.

A página SHALL detalhar o que o documento 11 §8.2 atribui a ela: os **aportes em moedas**, o
**nível de sustento** e os **selos**, os **desafios extras propostos com a efetividade deles**
— trilha, período e quantos concluíram — e a **prova do apoio**, como link com rótulo.

A seção NEVER SHALL apresentar Apoiador sem aporte homologado, NEVER SHALL exibir valor em
reais, NEVER SHALL exibir posição e NEVER SHALL ordenar, classificar, comparar ou oferecer
ordenação de Apoiadores por valor aportado: a ordem é **alfabética** pela identificação que a
linha exibe, e é ela, com a ausência de posição, que impede o pódio. (`RF-03-02`, `RF-03-03`,
`RF-03-07`, `RF-03-10`, `RF-03-55`, `RF-03-56`, `RF-03-57`, `RF-03-66`, `RF-03-80`,
`RN-03-18`, `RN-03-26`, `RN-03-37`, `RN-03-40`, `RN-14-38`)

#### Scenario: Cada Apoiador com aporte homologado sai em linha

- **WHEN** a seção de Apoiadores é aberta e o núcleo devolve dois Apoiadores
- **THEN** duas linhas aparecem, cada uma com avatar, a identificação, o nível de sustento e o
  total em moedas

#### Scenario: Quem não teve aporte homologado não está lá

- **WHEN** a seção de Apoiadores é aberta
- **THEN** nenhum Apoiador sem aporte homologado aparece, e nenhum espaço vazio o anuncia

#### Scenario: A seção não é um pódio

- **WHEN** a seção de Apoiadores é aberta com Apoiadores de totais diferentes
- **THEN** as linhas aparecem em ordem alfabética, sem posição, pódio ou comparação por valor,
  e nenhum controle oferece ordenar por valor

#### Scenario: A página traz os desafios propostos com a efetividade

- **WHEN** o visitante abre a página de um Apoiador que propôs um desafio extra concluído
- **THEN** a página traz a trilha, o período e quantos concluíram, e nenhum dado de quem
  concluiu

### Requirement: A seção de comunidades apresenta cada Comunidade Virtual em linha e em página

A App 06 SHALL apresentar a seção **Comunidades Virtuais** com uma linha por comunidade, **sem
avatar**, e cada linha SHALL abrir a **página da comunidade** em endereço próprio, alcançável
direto e compartilhável. A **representação visual** do documento 11 §8.3 é da página, nunca da
linha.

A seção SHALL aparecer nos três recortes de leitura em que o PRD-03 §5 a descreve, sem mudar o
conteúdo de um recorte para outro. (`RF-03-02`, `RF-03-15`, documento 11 §§8.2, 8.3, PRD-03
§§5.1, 5.2, 5.3)

#### Scenario: Cada comunidade sai em linha

- **WHEN** a seção de comunidades é aberta e o núcleo devolve três comunidades
- **THEN** três linhas aparecem, cada uma com nome, localização e o número de vinculados, e
  nenhuma com avatar

#### Scenario: A linha abre a página da comunidade em endereço próprio

- **WHEN** o visitante aciona a linha de uma comunidade
- **THEN** a página daquela comunidade abre em endereço próprio, com a representação visual, e
  o mesmo endereço, aberto direto, leva à mesma página

#### Scenario: Comunidade sem os indicadores continua em linha

- **WHEN** o núcleo devolve uma comunidade com os quatro indicadores nulos
- **THEN** a linha dela aparece com o que a leitura devolveu, e a ausência de indicador não a
  retira da lista

## MODIFIED Requirements

### Requirement: A vitrine aplica o temperamento Arena do cabeçalho ao rodapé

A App 06 SHALL apresentar toda tela pública no temperamento **Arena**, inclusive o painel
do território e os rankings, e NEVER SHALL reproduzir em tela nenhuma a densidade da
Operação — tabela, lote e painel de declaração são da outra família. A **lista de registros**
das seções de leitura NEVER SHALL contar como essa densidade: ela não tem cabeçalho de coluna,
grade nem coluna que apareça só a partir de uma largura, e a densidade baixa da Arena governa
a tela que **apresenta personagem** — a página individual, onde a carta domina e a tela pede
uma decisão só.

Toda tela pública SHALL trazer a **moldura de fundo de comunidade**: a cor chapada com a
foto da comunidade atrás dela quando houver foto, e **só a cor chapada** quando não
houver. O que a tela comunica NEVER SHALL depender da foto, e os pisos de contraste
SHALL continuar medidos sobre superfície opaca, nunca sobre a fotografia. (documento 15
§§6, 6.3, `RF-03-51`, `RN-03-22`)

#### Scenario: Toda tela pública traz a moldura da Arena

- **WHEN** qualquer tela pública da vitrine é aberta
- **THEN** ela é apresentada dentro da moldura de fundo de comunidade

#### Scenario: Sem foto, a tela é exatamente a mesma

- **WHEN** a comunidade não tem foto escolhida, ou a foto não carrega
- **THEN** a tela apresenta só a cor chapada, e nada do que ela comunica se perde

#### Scenario: A moldura não busca recurso de terceiro

- **WHEN** a moldura é apresentada
- **THEN** nenhuma requisição sai para domínio que não seja o próprio

#### Scenario: A lista de registros não traz a densidade da Operação

- **WHEN** uma seção de leitura é aberta em qualquer largura de tela
- **THEN** nenhuma linha traz cabeçalho de coluna ou grade, nenhuma coluna aparece ou
  desaparece com a largura, e a página individual segue sendo onde a carta domina

### Requirement: Card e página exibem só avatar, nick, badges, poderes e desempenho

O card e a página do Guerreiro(a) SHALL exibir **avatar, nick, badges, poderes com níveis e
desempenho**, mais as criações originais que a variante do documento 11 §8.2 pede. NEVER SHALL
exibir imagem real, nome civil, rede social, canal de contato ou qualquer outro dado da criança,
em tela nenhuma da vitrine. A vitrine NEVER SHALL oferecer canal de contato com o Guerreiro(a)
ou com a família dele. A **linha do ranking** e a do **portfólio** NEVER SHALL ir além de
avatar, nick e o que o requisito daquela seção já exige. (`RF-03-05`, `RF-03-06`, `RN-03-04`,
`RN-03-05`, invariantes 10 e 12 do documento 99 §6)

Faltando à leitura o que a variante exige, a carta NEVER SHALL ser apresentada pela metade: a
tela SHALL dizer em uma frase o que tem, como o documento 11 §8.2 determina.

#### Scenario: O card mostra só o que é permitido

- **WHEN** o visitante vê o card de um Guerreiro(a), na página individual dele
- **THEN** ele vê avatar, nick, badges, poderes e desempenho, e nenhuma imagem real, nome civil,
  rede social ou contato

#### Scenario: A linha não mostra mais que o card

- **WHEN** o visitante vê uma linha do ranking ou do portfólio
- **THEN** ela não traz nada de criança além de avatar e nick, mais o que o requisito daquela
  seção exige

#### Scenario: A página não abre canal de contato

- **WHEN** o visitante percorre a página individual inteira
- **THEN** nenhuma tela oferece falar com o Guerreiro(a) ou com a família dele

#### Scenario: Carta incompleta não se apresenta

- **WHEN** a leitura não devolve o que a variante Guerreiro(a) exige
- **THEN** a carta não é apresentada, e a tela diz em uma frase o que tem

### Requirement: O portfólio público exibe as criações autorizadas com trilha, data e autoria

A App 06 SHALL exibir o **portfólio** das criações originais autorizadas, cada uma em **uma
linha**, com a **trilha** de que nasceu, a **data** em que foi validada e a **autoria por
nick** de cada creditado, com o **avatar** de cada um. Cada **nick creditado** SHALL abrir a
página individual daquele Guerreiro(a). NEVER SHALL exibir criação cujo creditado não tenha
autorização vigente. O portfólio SHALL sair **sem título** enquanto a criação original não
tiver esse campo no modelo, e SHALL sair em ordem **decrescente** por data de validação.
(`RF-03-08`, `RF-03-83`, `RN-03-02`, decisão do fundador, 2026-09-28)

#### Scenario: A criação aparece com trilha, data e autoria

- **WHEN** o visitante abre o portfólio
- **THEN** cada linha traz a trilha, a data de validação e o avatar e o nick de cada autor
  creditado

#### Scenario: O portfólio não exibe quem não autorizou

- **WHEN** uma criação tem creditado sem autorização vigente
- **THEN** ela não aparece no portfólio

#### Scenario: A criação mais recente abre o portfólio

- **WHEN** o visitante abre o portfólio
- **THEN** a primeira linha é a criação validada mais recentemente

#### Scenario: O nick creditado abre a página do autor

- **WHEN** o visitante aciona o nick de um autor creditado
- **THEN** a página individual daquele Guerreiro(a) abre, em endereço próprio

### Requirement: O ranking público exibe só pontos regulares e só quem autorizou

A App 06 SHALL exibir o ranking público com **apenas pontos regulares** e **apenas** Guerreiros
e Guerreiras com autorização de divulgação vigente. NEVER SHALL exibir ponto extra, saldo de
moedas ou valor em reais no ranking. Cada posição SHALL sair em **uma linha**, com **avatar**,
nick, posição e pontos regulares, e a linha SHALL abrir a **página individual** daquele
Guerreiro(a). (`RF-03-09`, `RF-03-03`, `RN-03-02`, invariante 16 do documento 99 §6)

#### Scenario: O ranking é de ponto regular

- **WHEN** o visitante abre o ranking
- **THEN** a pontuação exibida é a de pontos regulares, e nenhuma outra

#### Scenario: Quem não autorizou não está no ranking

- **WHEN** um Guerreiro(a) sem autorização vigente teria posição no ranking
- **THEN** ele não aparece, e a numeração exibida não deixa buraco

#### Scenario: A linha do ranking traz o avatar e abre a página

- **WHEN** o visitante abre o ranking e aciona uma linha
- **THEN** a linha trazia avatar, nick, posição e pontos regulares, e a página individual
  daquele Guerreiro(a) abre

## REMOVED Requirements

### Requirement: A seção de Guerreiros e Guerreiras apresenta cards que rotacionam a cada 5 segundos

**Reason**: A seção perde a listagem e fica só com a consulta por nick exato, e sem cards não
há o que rotacionar. Decisão do fundador de 2026-10-11, descida ao documento 03 §8, ao
documento 11 §8.1 e ao documento 09 §1 antes desta change; o `RF-03-04` foi removido do PRD-03,
e o número não é reaproveitado.

**Migration**: A seção passa a cumprir "A vitrine não lista Guerreiros e Guerreiras". Quem tem
divulgação autorizada segue público pelo **ranking** e pelo **portfólio**, agora com avatar e
com a página individual a um clique. A garantia de que o conteúdo não depende de movimento
deixa de ser exceção e passa a valer por construção, porque nada mais rotaciona.

### Requirement: Cada card abre a página individual, em endereço próprio

**Reason**: A porta da página individual deixa de ser o card e passa a ser a linha da lista;
para o Guerreiro(a), as portas passam a ser a consulta por nick, a linha do ranking e o nick do
autor no portfólio. O enunciado nomeava o card como porta, e o card deixou de ser porta.

**Migration**: Substituído por "Cada linha abre a página individual, em endereço próprio", que
mantém tudo o que este exigia — endereço próprio, compartilhável, alcançável direto e com a
composição do documento 11 §8.2 — e acrescenta de onde se chega.

### Requirement: A seção de Mestres apresenta cada Mestre em card e em página

**Reason**: A seção passa a apresentar cada Mestre em **linha**, não em card. O que a página
detalha não muda.

**Migration**: Substituído por "A seção de Mestres apresenta cada Mestre em linha e em página",
que preserva o conteúdo da página, a proibição de editar pela vitrine e o endereço próprio.

### Requirement: A seção de Apoiadores apresenta cada Apoiador em card e em página

**Reason**: A seção passa a apresentar cada Apoiador em **linha**, com o total em moedas na
linha, e a proibição de pódio ganha a ausência de posição e de controle de ordenação, que o
`RN-03-40` fixou.

**Migration**: Substituído por "A seção de Apoiadores apresenta cada Apoiador em linha e em
página", que preserva o conteúdo da página, o portão do aporte homologado, a proibição de reais
e a ordem alfabética.

### Requirement: A seção de comunidades apresenta cada Comunidade Virtual em card e em página

**Reason**: A seção passa a apresentar cada comunidade em **linha e sem avatar**, e a
representação visual do documento 11 §8.3 passa a ser só da página — na medida de um avatar ela
não se lê, e a foto da comunidade não existe na plataforma.

**Migration**: Substituído por "A seção de comunidades apresenta cada Comunidade Virtual em
linha e em página", que preserva o endereço próprio, a presença nos três recortes e o
tratamento da comunidade sem indicador.
