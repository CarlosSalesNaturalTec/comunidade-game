# aplicacao-da-vitrine Specification

## Purpose
A App 06 é a cara pública do projeto e a raiz do domínio da plataforma: a única superfície que
qualquer pessoa alcança sem se identificar, e que por isso não guarda nada de quem visita. Esta
capacidade cobre como a vitrine se apresenta sem login nem cadastro, como ela se identifica ao
núcleo mantendo o visitante anônimo, o que ela deliberadamente não faz — cookie, rastreador,
publicidade, preferência de visitante e autenticação —, os três recortes de leitura como
navegação e o botão "Entrar", que encaminha cada persona à aplicação dela.

## Requirements

### Requirement: A vitrine é pública, abre na raiz do domínio e não tem área restrita

A App 06 SHALL abrir inteira **sem login e sem cadastro**, servida na **raiz do domínio** da
plataforma. NEVER SHALL oferecer tela de cadastro, de área restrita ou de sessão própria, e
NEVER SHALL escrever qualquer coisa sobre um Guerreiro(a). (`RF-03-01`, `RN-03-01`)

#### Scenario: Visitante abre a vitrine

- **WHEN** alguém abre o endereço da raiz do domínio
- **THEN** a vitrine se apresenta inteira, sem pedir login nem cadastro

#### Scenario: Não há área restrita por onde entrar

- **WHEN** o visitante percorre a vitrine
- **THEN** nenhuma tela oferece cadastro, área restrita ou sessão da própria vitrine

### Requirement: A vitrine se identifica por chave de aplicação e o visitante segue anônimo

Toda chamada da App 06 ao núcleo SHALL levar a **chave da própria aplicação**, e NEVER SHALL
levar credencial de persona: a vitrine não tem persona autenticada. (`RN-03-33`)

#### Scenario: A aplicação se identifica com a própria chave

- **WHEN** a App 06 chama uma rota de dados do núcleo
- **THEN** a chamada leva a chave da App 06, e não a de outra aplicação

#### Scenario: Nenhuma chamada carrega credencial de persona

- **WHEN** a App 06 chama qualquer rota do núcleo
- **THEN** a chamada não leva credencial de persona alguma

### Requirement: A vitrine não guarda nada do visitante, no servidor ou no aparelho

A App 06 NEVER SHALL instalar cookie de rastreio, rastreador ou perfilamento do visitante, para
finalidade nenhuma, e NEVER SHALL guardar no aparelho preferência, escolha ou histórico de quem
visita. Havendo medição de audiência, ela SHALL ser agregada e sem identificador de visitante.
(`RF-03-51`, `RN-03-22`, PRD-03 §10)

#### Scenario: Nada é gravado no aparelho depois de uma visita inteira

- **WHEN** o visitante navega pela vitrine, troca de recorte e abre a pergunta do "Entrar"
- **THEN** nada da visita fica guardado no aparelho

#### Scenario: Nenhum rastreador de terceiro é carregado

- **WHEN** a vitrine carrega
- **THEN** nenhum cookie de rastreio, rastreador ou perfilamento é instalado

### Requirement: A vitrine não veicula publicidade nem patrocínio

A App 06 NEVER SHALL exibir publicidade ou patrocínio, e NEVER SHALL reservar espaço de tela
para eles. (`RF-03-50`, `RN-03-21`)

#### Scenario: Nenhuma tela traz anúncio

- **WHEN** o visitante percorre a vitrine
- **THEN** nenhuma tela exibe publicidade ou patrocínio, nem espaço reservado a eles

### Requirement: A vitrine oferece os três recortes de leitura, com sociedade civil como padrão

A App 06 SHALL oferecer os **três recortes de leitura** — sociedade civil, pesquisadores e
gestores públicos — e SHALL abrir no recorte **sociedade civil** sem que o visitante escolha
nada. (`RF-03-25`)

#### Scenario: A vitrine abre no recorte padrão

- **WHEN** o visitante abre a vitrine sem escolher recorte
- **THEN** ele está no recorte sociedade civil

#### Scenario: Os outros dois recortes estão alcançáveis

- **WHEN** o visitante procura outro recorte
- **THEN** pesquisadores e gestores públicos estão oferecidos na navegação

### Requirement: Trocar de recorte é navegação, e não cria área restrita nem coleta dado

A troca de recorte SHALL mudar a porta de entrada e a ordem do que é apresentado, e NEVER SHALL
mudar o conteúdo público disponível nem o direito de acesso. NEVER SHALL criar área restrita,
pedir cadastro, coletar dado do visitante ou guardar o recorte escolhido. (`RF-03-26`,
`RF-03-51`, `RN-03-22`)

#### Scenario: O recorte não muda o direito de acesso

- **WHEN** o visitante troca do recorte sociedade civil para pesquisadores
- **THEN** ele segue na mesma vitrine pública, sem cadastro e sem nada bloqueado

#### Scenario: O recorte escolhido não sobrevive à visita

- **WHEN** o visitante troca de recorte e volta à vitrine depois
- **THEN** a vitrine abre outra vez no recorte sociedade civil

### Requirement: O botão "Entrar" fica sempre visível e pergunta qual persona está entrando

A App 06 SHALL manter o botão **"Entrar"** visível em toda tela pública, e ao ser acionado ele
SHALL perguntar **quem está entrando**, apresentando as personas que têm aplicação: Guerreiro(a),
responsável, Mestre, Apoiador, gestão e o **aparelho da aula**. (`RF-03-58`, PRD-03 §5.9)

#### Scenario: O botão está em toda tela

- **WHEN** o visitante está em qualquer tela pública da vitrine
- **THEN** o botão "Entrar" está visível

#### Scenario: O botão pergunta antes de encaminhar

- **WHEN** o visitante aciona "Entrar"
- **THEN** a vitrine pergunta qual persona está entrando, sem encaminhar ninguém antes da
  resposta

### Requirement: Cada persona é encaminhada à sua aplicação, e a vitrine nunca autentica

Escolhida a persona, a App 06 SHALL encaminhar o visitante ao endereço da aplicação dela —
Guerreiro(a) à App 05, responsável à App 07, Mestre à App 09, Apoiador à App 08, gestão à App 03
e o aparelho da aula à App 01. A vitrine NEVER SHALL conferir nick, imagem, login social, senha
ou qualquer credencial: quem autentica é a aplicação de destino. (`RF-03-59`, `RN-03-27`)

#### Scenario: A persona escolhida chega à aplicação dela

- **WHEN** o visitante declara que é Mestre
- **THEN** ele é encaminhado ao endereço da App 09

#### Scenario: Nenhum campo de credencial existe na vitrine

- **WHEN** o visitante percorre a pergunta do "Entrar" inteira
- **THEN** nenhuma tela pede nick, imagem, senha ou login

### Requirement: A escolha de persona não é guardada

A App 06 NEVER SHALL guardar a persona escolhida, no servidor ou no aparelho: quem volta SHALL
encontrar a mesma pergunta. (`RF-03-60`, `RN-03-22`)

#### Scenario: A pergunta se repete na visita seguinte

- **WHEN** o visitante já escolheu uma persona antes e abre a vitrine outra vez
- **THEN** o "Entrar" pergunta novamente qual persona está entrando, sem escolha pré-marcada

### Requirement: Nenhuma tela de entrada revela nick, conta ou existência de cadastro

As telas do "Entrar" NEVER SHALL apresentar lista de nicks, sugestão, completação ou qualquer
confirmação de que uma conta existe ou não existe na plataforma. (`RF-03-61`)

#### Scenario: A entrada não lista quem existe

- **WHEN** o visitante escolhe a persona Guerreiro(a)
- **THEN** nenhum nick, conta ou cadastro é apresentado ou confirmado

### Requirement: Quem não tem cadastro recebe a orientação da sua persona, sem promessa de acesso

Para cada persona, a App 06 SHALL oferecer a orientação de quem **ainda não tem cadastro**, e
NEVER SHALL prometer acesso: entrar não cria cadastro. A orientação SHALL ser a da própria
persona — **pré-cadastro da App 08** para quem quer ser Apoiador, **formulário de participação da
vitrine**, com link para ele, para quem quer ser Mestre, e **procurar a gestão no encontro** para
responsável e Guerreiro(a). NEVER SHALL apresentar link que não resolve. (`RF-03-62`,
PRD-03 §5.9)

#### Scenario: Quem quer ser Apoiador é levado ao pré-cadastro

- **WHEN** o visitante declara que é Apoiador e diz que não tem cadastro
- **THEN** a orientação o leva ao pré-cadastro da App 08

#### Scenario: Responsável e Guerreiro(a) são orientados a procurar a gestão

- **WHEN** o visitante declara que é responsável, ou Guerreiro(a), e diz que não tem cadastro
- **THEN** a orientação é procurar a gestão no encontro, sem promessa de acesso

#### Scenario: A orientação do Mestre não oferece link quebrado

- **WHEN** o visitante declara que quer ser Mestre e diz que não tem cadastro
- **THEN** a orientação nomeia o formulário de participação e traz o link, que resolve para o
  formulário existente

### Requirement: A seção de Guerreiros e Guerreiras apresenta cards que rotacionam a cada 5 segundos

A App 06 SHALL apresentar, no recorte sociedade civil, a seção **Guerreiros e Guerreiras** com
os cards de quem tem autorização vigente, e os cards SHALL **rotacionar a cada 5 segundos**. A
rotação SHALL parar quando o aparelho declarar `prefers-reduced-motion`, e NEVER SHALL ser a
**única via** ao conteúdo: quem não espera a rotação SHALL alcançar os mesmos Guerreiros e
Guerreiras pela navegação da própria seção. (`RF-03-02`, `RF-03-04`, documento 15 §§5, 8.1)

#### Scenario: Os cards rotacionam sozinhos

- **WHEN** o visitante abre a vitrine e permanece na seção de Guerreiros e Guerreiras
- **THEN** os cards trocam a cada 5 segundos, sem que ele acione nada

#### Scenario: Quem pede menos movimento não vê rotação

- **WHEN** o aparelho do visitante declara preferência por movimento reduzido
- **THEN** os cards não rotacionam, e todos seguem alcançáveis

#### Scenario: A rotação não é a única via ao conteúdo

- **WHEN** o visitante quer ver um card que ainda não entrou na rotação
- **THEN** ele o alcança pela navegação da seção, sem esperar a troca

### Requirement: Cada card abre a página individual, em endereço próprio

Cada card SHALL abrir a **página individual** do Guerreiro(a), em **endereço próprio**,
compartilhável e alcançável diretamente. A página SHALL detalhar a trajetória nas trilhas, os
badges e níveis por poder e o portfólio de criações originais com a autoria, na composição do
documento 11 §8.2. (`RF-03-03`, PRD-03 §5.1)

#### Scenario: O card leva à página

- **WHEN** o visitante aciona um card de Guerreiro(a)
- **THEN** a página individual daquele Guerreiro(a) abre, em endereço próprio

#### Scenario: O endereço direto resolve

- **WHEN** alguém abre diretamente o endereço da página de um Guerreiro(a) com autorização
  vigente
- **THEN** a página abre com a composição do documento 11 §8.2

### Requirement: Card e página exibem só avatar, nick, badges, poderes e desempenho

O card e a página do Guerreiro(a) SHALL exibir **avatar, nick, badges, poderes com níveis e
desempenho**, mais as criações originais que a variante do documento 11 §8.2 pede. NEVER SHALL
exibir imagem real, nome civil, rede social, canal de contato ou qualquer outro dado da criança,
em tela nenhuma da vitrine. A vitrine NEVER SHALL oferecer canal de contato com o Guerreiro(a)
ou com a família dele. (`RF-03-05`, `RF-03-06`, `RN-03-04`, `RN-03-05`, invariantes 10 e 12 do
documento 99 §6)

Faltando à leitura o que a variante exige, a carta NEVER SHALL ser apresentada pela metade: a
tela SHALL dizer em uma frase o que tem, como o documento 11 §8.2 determina.

#### Scenario: O card mostra só o que é permitido

- **WHEN** o visitante vê um card de Guerreiro(a)
- **THEN** ele vê avatar, nick, badges, poderes e desempenho, e nenhuma imagem real, nome civil,
  rede social ou contato

#### Scenario: A página não abre canal de contato

- **WHEN** o visitante percorre a página individual inteira
- **THEN** nenhuma tela oferece falar com o Guerreiro(a) ou com a família dele

#### Scenario: Carta incompleta não se apresenta

- **WHEN** a leitura não devolve o que a variante Guerreiro(a) exige
- **THEN** a carta não é apresentada, e a tela diz em uma frase o que tem

### Requirement: A busca é por nick exato, sem lista, sugestão ou completação

A App 06 SHALL oferecer busca por **nick exato**, e NEVER SHALL oferecer sugestão, completação,
lista de nicks ou contagem de resultados parecidos. Havendo autorização vigente, a busca SHALL
levar à página pública daquele Guerreiro(a). (`RF-03-11`, `RF-03-12`, `RN-03-06`, PRD-03 §5.6)

#### Scenario: Nick exato leva à página

- **WHEN** o visitante digita o nick exato de um Guerreiro(a) com autorização vigente
- **THEN** a página pública dele abre

#### Scenario: A busca não sugere nem completa

- **WHEN** o visitante digita parte de um nick
- **THEN** nenhuma sugestão, completação ou lista de nicks é apresentada

### Requirement: Nick inexistente e nick sem autorização recebem a mesma resposta

A App 06 SHALL apresentar **a mesma resposta** de "não encontrado" para nick inexistente e para
nick sem autorização de divulgação vigente, sem revelar qual dos dois casos ocorreu — na busca e
no endereço direto da página. (`RF-03-11`, `RN-03-07`, PRD-03 §§5.6, 5.7)

#### Scenario: Os dois casos respondem igual

- **WHEN** o visitante busca um nick que não existe, e depois um nick sem autorização vigente
- **THEN** as duas respostas são idênticas, e nenhuma diz qual caso ocorreu

#### Scenario: O endereço direto também não distingue

- **WHEN** alguém abre o endereço da página de um nick sem autorização vigente
- **THEN** a tela responde "não encontrado", como responderia a um nick inexistente

### Requirement: Quem não tem autorização vigente não aparece, e a revogação o retira na leitura seguinte

A App 06 NEVER SHALL exibir em card, página, portfólio ou ranking um Guerreiro(a) sem
autorização de divulgação vigente. Revogada a autorização, ele SHALL desaparecer das quatro
superfícies **na leitura seguinte**, e o endereço direto da página dele SHALL responder "não
encontrado". A vitrine NEVER SHALL guardar em cache no aparelho o que leu de um Guerreiro(a), de
modo que a revogação não sobreviva à leitura seguinte. (`RF-03-13`, `RF-03-14`, `RN-03-02`,
`RN-03-03`, `RN-03-22`, PRD-03 §5.7)

#### Scenario: Sem autorização, não aparece em lugar nenhum

- **WHEN** um Guerreiro(a) não tem autorização vigente
- **THEN** ele não está em card, página, portfólio nem ranking, nem por endereço direto

#### Scenario: A revogação vale na leitura seguinte

- **WHEN** o responsável revoga a autorização e o visitante recarrega a vitrine
- **THEN** o Guerreiro(a) já não aparece em nenhuma das quatro superfícies

#### Scenario: A criação em equipe permanece com os demais autores

- **WHEN** um dos creditados de uma criação em equipe tem a autorização revogada
- **THEN** a vitrine apresenta o que o núcleo devolver, sem citar o revogado

### Requirement: A repetição da busca encontra espera crescente explicada, sem CAPTCHA nem cadastro

Freada a origem pela repetição da busca por nick, a App 06 SHALL explicar em **linguagem
simples** o motivo e **quanto tempo falta esperar**, com o tempo que o núcleo devolveu. NEVER
SHALL pedir CAPTCHA, cadastro ou login para seguir, e NEVER SHALL guardar no aparelho qualquer
marca de quem foi freado. (`RF-03-36`, `RF-03-37`, `RN-03-08`, `RN-03-34`, PRD-03 §§5.6, 12)

#### Scenario: A espera é explicada

- **WHEN** o visitante repete a busca por nick até ser freado
- **THEN** a tela diz por que houve a espera e quanto tempo falta, em linguagem simples

#### Scenario: A espera não pede nada do visitante

- **WHEN** o visitante está esperando o freio passar
- **THEN** nenhuma tela pede CAPTCHA, cadastro ou login

### Requirement: O portfólio público exibe as criações autorizadas com trilha, data e autoria

A App 06 SHALL exibir o **portfólio** das criações originais autorizadas, cada uma com a
**trilha** de que nasceu, a **data** em que foi validada e a **autoria por nick** de cada
creditado. NEVER SHALL exibir criação cujo creditado não tenha autorização vigente. O portfólio
SHALL sair **sem título** enquanto a criação original não tiver esse campo no modelo. (`RF-03-08`,
`RN-03-02`, decisão do fundador, 2026-09-28)

#### Scenario: A criação aparece com trilha, data e autoria

- **WHEN** o visitante abre o portfólio
- **THEN** cada criação traz a trilha, a data de validação e o nick de cada autor creditado

#### Scenario: O portfólio não exibe quem não autorizou

- **WHEN** uma criação tem creditado sem autorização vigente
- **THEN** ela não aparece no portfólio

### Requirement: O ranking público exibe só pontos regulares e só quem autorizou

A App 06 SHALL exibir o ranking público com **apenas pontos regulares** e **apenas** Guerreiros
e Guerreiras com autorização de divulgação vigente. NEVER SHALL exibir ponto extra, saldo de
moedas ou valor em reais no ranking. (`RF-03-09`, `RN-03-02`, invariante 16 do documento 99 §6)

#### Scenario: O ranking é de ponto regular

- **WHEN** o visitante abre o ranking
- **THEN** a pontuação exibida é a de pontos regulares, e nenhuma outra

#### Scenario: Quem não autorizou não está no ranking

- **WHEN** um Guerreiro(a) sem autorização vigente teria posição no ranking
- **THEN** ele não aparece, e a numeração exibida não deixa buraco

### Requirement: A seção de poderes apresenta cada poder com as trilhas dele

A App 06 SHALL apresentar a seção **poderes**, com cada poder e as **trilhas** vinculadas a ele,
e a página do poder com as mesmas trilhas. Os **Mestres responsáveis** do documento 11 §8.2
NEVER SHALL ser prometidos nem apresentados vazios enquanto a rota de Mestres não existir: a
seção sai sem eles. (`RF-03-02`, decisão do fundador, 2026-09-28)

#### Scenario: O poder aparece com as trilhas

- **WHEN** o visitante abre a seção de poderes
- **THEN** cada poder aparece com as trilhas vinculadas a ele

#### Scenario: A seção não promete o que ainda não tem

- **WHEN** o visitante abre a página de um poder
- **THEN** nenhum espaço vazio ou promessa de Mestres responsáveis é apresentado

### Requirement: A seção de comunidades apresenta cada Comunidade Virtual em card e em página

A App 06 SHALL apresentar a seção **Comunidades Virtuais** com um card por comunidade, na
variante Comunidade Virtual da carta, e cada card SHALL abrir a **página da comunidade** em
endereço próprio, alcançável direto e compartilhável. Comunidade cuja leitura não devolve o que
a carta exige SHALL ser apresentada em outra forma, nunca em carta incompleta.

A seção SHALL aparecer nos três recortes de leitura em que o PRD-03 §5 a descreve, sem mudar o
conteúdo de um recorte para outro. (`RF-03-02`, `RF-03-15`, documento 11 §8.2, PRD-03 §§5.1,
5.2, 5.3)

#### Scenario: Cada comunidade sai em card

- **WHEN** a seção de comunidades é aberta e o núcleo devolve três comunidades
- **THEN** três cards aparecem, cada um com nome, território, representação visual, séries
  ativas e o número de vinculados

#### Scenario: O card abre a página da comunidade em endereço próprio

- **WHEN** o visitante abre o card de uma comunidade
- **THEN** a página daquela comunidade abre em endereço próprio, e o mesmo endereço, aberto
  direto, leva à mesma página

#### Scenario: Comunidade sem os indicadores não vira card incompleto

- **WHEN** o núcleo devolve uma comunidade com os quatro indicadores nulos
- **THEN** ela aparece na seção em outra forma, com o que a leitura devolveu, e nenhum card
  incompleto é apresentado

### Requirement: O painel da comunidade exibe as séries do território agregadas até o bairro

A página da comunidade SHALL exibir as **séries históricas do território**, agregadas até o
**bairro**, com a evolução no tempo. Nenhuma tela da vitrine SHALL exibir nick, nome, avatar ou
código de coletor, e nenhuma SHALL oferecer recorte, filtro ou ordenação por coletor.

O painel NEVER SHALL pedir nem apresentar granularidade abaixo do bairro; quem precisa do
conjunto completo SHALL ser encaminhado ao formulário de solicitação de dados. (`RF-03-15`,
`RF-03-16`, `RN-03-09`, `RN-03-10`, invariantes 7 e 12 do documento 99 §6, PRD-03 §5.2)

#### Scenario: A série aparece por tipo de coleta e bairro

- **WHEN** a página de uma comunidade com registros de dois tipos de coleta em dois bairros é
  aberta
- **THEN** o painel apresenta os recortes por tipo e bairro, com a evolução no tempo de cada um

#### Scenario: Nenhuma tela do painel identifica quem coletou

- **WHEN** o visitante percorre o painel inteiro de uma comunidade
- **THEN** nenhum nick, nome, avatar ou código de coletor aparece, e não há como recortar a
  série por uma pessoa

#### Scenario: O painel não oferece granularidade abaixo do bairro

- **WHEN** o visitante procura no painel um recorte de rua, condomínio, bloco ou quadra
- **THEN** nenhum existe, e a tela diz que a granularidade fina sai pela solicitação do
  conjunto de dados

### Requirement: Cada recorte do painel declara a metodologia e os registros válidos

O painel SHALL declarar, para cada recorte publicado, **o que se mede** com a unidade, a
**cadência**, o **período coberto**, a **origem da medição** — registro manual, por voz ou por
sensor construído na trilha — e o **número de registros válidos** do período apresentado.

A declaração SHALL acompanhar o recorte na própria tela, em linguagem legível por quem não
conhece a plataforma, e NEVER SHALL exigir que o visitante abra outra página para saber o que
está olhando. (`RF-03-17`, `RF-03-18`, PRD-03 §5.2)

#### Scenario: O recorte apresenta a metodologia junto do gráfico

- **WHEN** o visitante abre um recorte do painel
- **THEN** ele lê ali o que se mede com a unidade, a cadência, o período coberto, a origem da
  medição e quantos registros válidos sustentam aquele recorte

#### Scenario: A metodologia acompanha o período apresentado

- **WHEN** o painel apresenta um período mais estreito que a série inteira
- **THEN** o período coberto e a contagem de registros válidos exibidos são os daquele período

### Requirement: O recorte inativo aparece sinalizado, sem sumir do painel

O painel SHALL apresentar o recorte cuja coleta parou **sinalizado como inativo**, mantendo os
pontos já registrados e a metodologia dele — o dado é permanente, e o que muda é o sinal. O
recorte inativo NEVER SHALL ser removido, ocultado por padrão ou apresentado como ausência de
dado. (`RF-03-19`, documento 11 §8.3, invariante 7 do documento 99 §6)

#### Scenario: A série interrompida continua no painel, marcada

- **WHEN** um recorte da comunidade está inativo
- **THEN** ele aparece no painel com os seus pontos, marcado como inativo

#### Scenario: A marca de inativo é legível sem depender de cor

- **WHEN** o recorte inativo é apresentado
- **THEN** a condição de inativo se lê em texto, não só por cor

### Requirement: A comunidade sem dado aparece vazia, e o desenho cresce com o dado

A App 06 SHALL apresentar a comunidade recém-criada como **território vazio**, com nome e
contorno, em vez de omiti-la ou de apresentar erro, e SHALL fazer a representação visual
**crescer** conforme os registros acumulam, pela representação da camada comum.

Nenhum elemento do desenho SHALL aparecer sem fato que o sustente. (`RF-03-20`, `RF-03-21`,
documento 11 §8.3, documento 15 §5)

#### Scenario: Comunidade sem registro aparece vazia, não ausente

- **WHEN** uma comunidade criada por Admin ainda não tem registro algum
- **THEN** ela aparece na seção com nome e contorno, como território vazio

#### Scenario: O território ganha corpo conforme o dado chega

- **WHEN** a mesma comunidade passa a ter séries e registros válidos
- **THEN** a representação dela cresce e ganha detalhe na medida desse acúmulo

### Requirement: A cobertura da Agenda 2030 é da comunidade e do ciclo, nunca de um Guerreiro(a)

A App 06 SHALL apresentar o painel de **cobertura da Agenda 2030** agregado por **comunidade** e
por **ciclo**, com o rótulo do ciclo a que os números se referem. A cobertura NEVER SHALL
aparecer vinculada a um Guerreiro(a), nem por nick, avatar ou qualquer recorte que isole
alguém: a etiqueta é descritiva e agregada.

O painel SHALL destacar a contribuição do projeto à **meta 17.18** — dado local desagregado do
território — e SHALL registrar o **ODS 18** como **adoção voluntária do Brasil**, nunca como
objetivo oficial da ONU. (`RF-03-22`, `RF-03-23`, `RF-03-24`, `RN-03-19`, `RN-03-20`, PRD-03
§5.3)

#### Scenario: A cobertura sai por comunidade e por ciclo

- **WHEN** o painel de cobertura é aberto
- **THEN** ele apresenta, por comunidade, os objetivos que as trilhas e os desafios daquela
  comunidade tocaram, com o rótulo do ciclo

#### Scenario: Nenhuma etiqueta aparece por Guerreiro(a)

- **WHEN** o visitante percorre o painel de cobertura inteiro
- **THEN** nenhuma etiqueta ODS aparece ligada a uma pessoa

#### Scenario: A meta 17.18 e o ODS 18 saem com a redação correta

- **WHEN** o painel de cobertura é apresentado
- **THEN** a meta 17.18 aparece como a contribuição própria do projeto, e o ODS 18 aparece
  declarado como adoção voluntária do Brasil, não como objetivo da ONU

### Requirement: O recorte de gestores públicos abre com o bloco sobre a utilidade ao município

O recorte **gestores públicos** SHALL abrir com um **bloco em destaque**, **antes** do painel,
que traduza a plataforma para quem decide: que dado ela produz e para que serve, com **usos
concretos** do dado, o **caminho para pedir o conjunto completo**, como apoiar e como replicar o
modelo, já que o código é aberto.

O mesmo bloco SHALL declarar os limites: o dado é **agregado e anonimizado, nunca por
Guerreiro(a)**, e **não substitui indicador oficial** — é evidência produzida por moradores
sobre o próprio lugar. (`RF-03-63`, `RF-03-64`, `RF-03-65`, `RN-03-28`, PRD-03 §5.3)

#### Scenario: O bloco abre o recorte, antes do painel

- **WHEN** o visitante entra pelo recorte de gestores públicos
- **THEN** o bloco em destaque é a primeira coisa da tela, e o painel do território vem abaixo
  dele

#### Scenario: O bloco nomeia usos concretos e o caminho do conjunto completo

- **WHEN** o bloco é apresentado
- **THEN** ele lista usos concretos do dado e diz por onde se pede o conjunto completo

#### Scenario: O bloco declara os dois limites

- **WHEN** o bloco é apresentado
- **THEN** ele diz que o dado é agregado e nunca sai por Guerreiro(a), e que não substitui
  indicador oficial

### Requirement: O formulário de participação pede o mínimo e declara o que a solicitação não faz

A App 06 SHALL oferecer o **formulário de solicitação de participação** em endereço próprio,
que exige **nome, e-mail, WhatsApp, pretensão (Mestre ou Apoiador) e apresentação**, e aceita
**instituição** e **links comprobatórios** como opcionais. **Antes do envio**, a tela SHALL
declarar que a solicitação **não cria cadastro nem acesso**, que quem avalia é um **Admin** e
que o prazo de resposta é de **7 dias**. A solicitação SHALL ser enviada ao núcleo, que a grava
na fila da App 03. (`RF-03-27`, `RF-03-28`, `RF-03-29`, `RF-03-30`, `RF-03-31`, `RN-03-11`,
`RN-03-12`, PRD-03 §5.4)

#### Scenario: Os avisos aparecem antes do envio

- **WHEN** o visitante abre o formulário de participação
- **THEN** a tela diz que a solicitação não cria cadastro nem acesso, que um Admin avalia e que
  o prazo é de 7 dias, antes de qualquer envio

#### Scenario: Campo obrigatório em falta aponta o campo

- **WHEN** o visitante envia sem um dos cinco campos obrigatórios
- **THEN** a tela aponta o campo em falta e nada é enviado

#### Scenario: Instituição e links são opcionais

- **WHEN** o visitante envia com os cinco campos obrigatórios e sem instituição nem links
- **THEN** o envio segue ao núcleo

### Requirement: O formulário de dados declara as condições da entrega

A App 06 SHALL oferecer o **formulário de solicitação de dados** em endereço próprio, que exige
**solicitante, instituição, e-mail e finalidade declarada**, e o **recorte pedido** que o núcleo
registra junto. A tela SHALL declarar, antes do envio, que a entrega é **gratuita, anonimizada,
licenciada em CC BY-SA, depende de aprovação de um Admin e é respondida em 7 dias**. (`RF-03-32`,
`RF-03-33`, `RN-03-12`, `RN-03-13`, `RN-03-14`, PRD-03 §5.2)

#### Scenario: As condições aparecem antes do envio

- **WHEN** o visitante abre o formulário de dados
- **THEN** a tela declara a entrega gratuita, anonimizada, em CC BY-SA, dependente de aprovação
  e respondida em 7 dias

#### Scenario: Campo obrigatório em falta aponta o campo

- **WHEN** o visitante envia sem solicitante, instituição, e-mail, finalidade ou recorte
- **THEN** a tela aponta o campo em falta e nada é enviado

### Requirement: O envio confirma o registro e nunca devolve dado, arquivo ou acesso

Registrada a solicitação, a App 06 SHALL confirmar na tela o **protocolo e o prazo** que o núcleo
devolveu e dizer que o retorno virá pelo **contato declarado**, sem e-mail automático da
plataforma. NEVER SHALL apresentar dado, arquivo, link de download, chave ou acesso no ato, em
nenhum dos dois formulários. (`RF-03-31`, `RF-03-34`, `RN-03-11`, `RN-03-13`, PRD-03 §§5.4, 5.2)

#### Scenario: Confirmação mostra protocolo e prazo

- **WHEN** o núcleo registra a solicitação
- **THEN** a tela mostra o protocolo e o prazo e diz que o retorno vem pelo contato declarado

#### Scenario: Solicitação de dados não entrega nada

- **WHEN** a solicitação de dados é registrada
- **THEN** a tela não oferece arquivo nem link de download e diz que a entrega depende de
  aprovação de um Admin

### Requirement: O envio repetido encontra espera crescente explicada, sem CAPTCHA nem cadastro

Freada a origem pelo envio repetido de qualquer dos dois formulários, a App 06 SHALL explicar
em **linguagem simples** o motivo e **quanto tempo falta**, com o tempo que o núcleo devolveu,
e SHALL manter o que o visitante já preencheu. NEVER SHALL pedir CAPTCHA, cadastro ou login, e
NEVER SHALL guardar no aparelho marca de quem foi freado nem o conteúdo digitado. (`RF-03-35`,
`RF-03-37`, `RN-03-08`, `RN-03-34`, PRD-03 §5.4)

#### Scenario: A espera é explicada nos dois formulários

- **WHEN** o núcleo recusa o envio com 429 e o tempo de espera
- **THEN** a tela diz por que houve a espera e quanto falta, em linguagem simples, e o que foi
  digitado continua no formulário

#### Scenario: A espera não pede nada e não deixa rastro

- **WHEN** o visitante espera o freio passar
- **THEN** nenhuma tela pede CAPTCHA, cadastro ou login, e nada é gravado no aparelho

### Requirement: "Quem somos" exibe o texto publicado, a nota de transparência sobre IA e o bloco "Licenças"

A App 06 SHALL exibir a seção **"Quem somos"** com o texto publicado, e a **nota de
transparência sobre IA** SHALL viver **dentro dela**, e não em seção própria, com **endereço
estável** a que o texto reescrito por IA nas demais aplicações possa apontar. O bloco
**"Licenças"** SHALL aparecer na mesma seção, e a nota SHALL remeter a ele quanto ao gerado com
auxílio de IA. Seção sem texto publicado SHALL dizer que o conteúdo **ainda não foi publicado**.
(`RF-03-45`, `RF-03-48`, PRD-03 §3.1)

#### Scenario: A nota aparece dentro de "Quem somos"

- **WHEN** o visitante abre "Quem somos" com a nota publicada
- **THEN** a nota e o bloco "Licenças" aparecem dentro da seção, cada um sob o seu título

#### Scenario: O endereço da nota leva direto a ela

- **WHEN** o visitante abre o endereço da nota de transparência
- **THEN** a vitrine mostra "Quem somos" com a nota em foco

#### Scenario: Seção sem texto não inventa conteúdo

- **WHEN** o núcleo devolve a seção sem texto
- **THEN** a tela diz que o conteúdo ainda não foi publicado, e nenhum texto de exemplo aparece

### Requirement: O vídeo de apresentação é um acesso, e nunca um player de terceiro embutido

Havendo link de vídeo em "Quem somos", a App 06 SHALL oferecer o **acesso ao vídeo de
apresentação** por link, e NEVER SHALL embutir player nem carregar recurso de terceiro ao abrir
a página, para não instalar cookie ou rastreador. Sem link, a seção SHALL sair sem espaço
vazio. (`RF-03-49`, `RF-03-51`, `RN-03-22`)

#### Scenario: Com link, a tela oferece o vídeo sem carregar terceiro

- **WHEN** "Quem somos" chega com o link do vídeo
- **THEN** a tela oferece o acesso ao vídeo, e nenhuma requisição a terceiro parte da vitrine
  antes de o visitante acionar o link

#### Scenario: Sem link, a seção não deixa espaço vazio

- **WHEN** "Quem somos" chega sem link de vídeo
- **THEN** nada aparece no lugar do vídeo

### Requirement: "Contatos" e "Como apoiar" exibem o que foi publicado, e "Como apoiar" traz a chave PIX

A App 06 SHALL exibir a seção **"Contatos"** e a seção **"Como apoiar"** com o texto publicado,
na ordem do recorte, sem publicidade nem patrocínio. Em "Como apoiar" SHALL aparecer a **chave
PIX da pessoa jurídica vinculada**, com o titular. A exibição SHALL vir do que o núcleo devolve,
e nenhum valor SHALL ficar escrito na aplicação. (`RF-03-45`, `RF-03-46`, `RN-03-21`)

#### Scenario: A chave PIX aparece em "Como apoiar"

- **WHEN** o visitante abre "Como apoiar" com o texto semeado
- **THEN** a tela mostra a chave PIX e o titular

#### Scenario: A chave publicada é a que o Admin editou

- **WHEN** o Admin republica "Como apoiar" com outra chave
- **THEN** a tela mostra a chave nova, sem depender de nova versão da aplicação

#### Scenario: Seção não publicada diz isso

- **WHEN** "Contatos" não tem texto publicado
- **THEN** a tela diz que o conteúdo ainda não foi publicado

### Requirement: Toda tela traz o aviso de coleta, com acesso à área detalhada

A App 06 SHALL exibir, em **toda tela**, incluindo a página individual, a da comunidade e os
formulários, um aviso **discreto** de que a vitrine **não coleta dado de quem visita** e de que
só os formulários gravam o que a pessoa digita, com acesso à **área detalhada**. O aviso NEVER
SHALL bloquear a tela nem exigir confirmação, e NEVER SHALL guardar no aparelho que foi visto ou
acionado. (`RN-03-23`, `RF-03-51`, PRD-03 §11)

#### Scenario: O aviso está em toda tela

- **WHEN** o visitante abre um recorte, a página de um Guerreiro(a), a página de uma comunidade
  ou um formulário
- **THEN** cada uma traz o aviso, com o acesso à área detalhada

#### Scenario: O aviso não interrompe e não deixa rastro

- **WHEN** o visitante usa a tela sem acionar o aviso
- **THEN** nada é bloqueado ou pedido, e nada é gravado no aparelho

### Requirement: A área detalhada explica o que a plataforma coleta, de quem, para quê e por quanto tempo

A App 06 SHALL oferecer a **área detalhada** em endereço próprio, explicando em **linguagem
simples**, para cada dado, **o que a plataforma coleta, de quem, para quê e por quanto tempo**,
e SHALL declarar que a **vitrine não coleta dado do visitante**: sem login, sem cadastro, sem
cookie de rastreio e sem perfilamento. SHALL declarar também que a conversa com o assistente do
Desenvolvedor não é guardada. (`RF-03-52`, `RF-03-53`, `RN-03-22`, PRD-03 §11)

#### Scenario: A área detalhada traz a tabela de coleta em linguagem simples

- **WHEN** o visitante abre a área detalhada
- **THEN** ela lista cada dado com de quem é, para quê serve e por quanto tempo é guardado

#### Scenario: A área declara que a vitrine não coleta do visitante

- **WHEN** o visitante lê a área detalhada
- **THEN** ela declara que a vitrine não coleta dado de quem visita, não instala cookie de
  rastreio nem perfila

#### Scenario: Abrir a área não deixa rastro

- **WHEN** o visitante abre a área detalhada e recarrega a página
- **THEN** `localStorage`, `sessionStorage` e cookie seguem vazios
