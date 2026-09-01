# 02 — Conceito do Jogo e Gamificação

O Comunidade Game é um "jogo" cujas partidas acontecem na vida real: aprender, criar, ajudar
os colegas e realizar atividades gera pontos, poderes e reconhecimento.

> Este documento define **o que são** os elementos do jogo. **Como eles se ligam e quanto
> valem** — anatomia da trilha, taxonomia de atividades, tabela de pontos, níveis e badges —
> está no documento 11.

## 1. Os elementos do jogo (personas)

### Guerreiros e Guerreiras (persona primária)

Crianças e jovens moradores de comunidades periféricas.

**Como a persona se chama.** Ela é a **Guerreira** ou o **Guerreiro**, conforme a **forma de
tratamento** que a própria pessoa escolhe no cadastro do onboarding — o mesmo nome da
Comunidade Guerreira Zeferina, onde o Ciclo 01 acontece. As aplicações tratam cada pessoa pela
forma que ela escolheu. Nesta documentação, a referência genérica é **Guerreiro(a)** e o
coletivo é **Guerreiros e Guerreiras**; identificadores técnicos — entidades e rotas — não
levam marca de gênero.

O Guerreiro(a):

- Define seu **Nick** — **único em toda a plataforma** — e as características do seu
  personagem (avatar).
- Escolhe **Poderes** e segue **Trilhas** para desenvolvê-los.
- Só ganha pontos de uma habilidade **na medida em que realiza as atividades propostas pelos
  Mestres** — não há pontos por presença passiva.
- Pode montar **Equipes** e participar de **Batalhas** e **Desafios**.
- Tem **voz e autoria**: cria a partir do que aprende, propõe ideias e sugere melhorias para
  as atividades e para a própria plataforma.

O Guerreiro(a) é a **única persona com autocadastro** na plataforma.

### Admins (Organizadores / Equipe técnica)

Responsáveis pela operação da plataforma e pela logística dos eventos. Editam as seções
institucionais, fazem os lançamentos de atividades e **cadastram Mestres e Apoiadores**.

O **fundador é o primeiro Admin**, semeado na implantação junto com as chaves de aplicação — é
o único cadastro que não passa por outro Admin. **Novos Admins são incluídos manualmente** por
um Admin existente — não há autocadastro nem solicitação aberta de acesso administrativo.

### Mestres (persona secundária)

Especialistas e mentores que orientam e ministram oficinas. Podem ser de **qualquer área do
conhecimento** — tecnologia, educação, artes, esportes, cultura, ciências humanas e sociais:
o motor do jogo é agnóstico de área. Regras de admissão:

- **Todo Mestre é cadastrado exclusivamente pelos Admins.** Não há autocadastro.
- Todo Mestre **tem que ter pelo menos uma habilidade declarada**, e a habilidade é um
  **poder do catálogo** (§2) — não há lista de habilidades à parte.
- A habilidade precisa estar **comprovada por materiais ou artefatos disponibilizados na
  plataforma** — aulas presenciais ou gravadas, atividades propostas, videoaulas, projetos,
  obras, registros de prática, **currículo, portfólio, redes sociais e documentos externos**
  ou qualquer produção verificável da sua área. A prova é pública e verificável por qualquer
  visitante.
- Mestres também podem prover recursos para atividades.
- **Nick e avatar, definidos no primeiro acesso** — sem o piso de moedas, que é regra só do
  Apoiador —, sob a mesma unicidade de nick da plataforma. Até lá, o Mestre existe sem eles.

> **Exemplo de referência — o Mestre fundador.** É mestre em Programação e Robótica porque
> construiu o software da plataforma, propõe as atividades que os Guerreiros e Guerreiras
> realizam e publica conteúdo. É autor das duas primeiras trilhas.

### Apoiadores / Patrocinadores

Pessoas e instituições que financiam ou divulgam o projeto.

- **Cadastrados exclusivamente pelos Admins**, com o mesmo critério dos Mestres: o apoio
  precisa estar **comprovado por materiais ou artefatos registrados na plataforma** —
  incluindo currículo, portfólio, redes sociais e documentos externos da pessoa ou
  instituição.
- **Pré-cadastro na Área do Apoiador**, aberto a quem chega pela vitrine: a pessoa se
  identifica, declara o aporte e anexa o comprovante. Continua sendo **solicitação, não
  cadastro** — quem avalia e cadastra é um Admin.
- **Identificação sem documento**: nome ou razão social, e-mail e WhatsApp bastam. A plataforma
  **não coleta CPF, CNPJ nem documento de identidade**.
- **Nick escolhido no pré-cadastro**, sob a **unicidade de nick** da plataforma — opcional até
  lá. Sem pré-cadastro, ou em colisão de nick, é o Admin quem digita o nick no cadastro. O
  **avatar** é definido depois de aprovado, na App 08: pode ser a logomarca ou outra imagem
  escolhida, e é liberado a partir de **10 moedas acumuladas**; abaixo disso o card exibe o
  avatar padrão do projeto, com o mesmo nick e o mesmo total de moedas.
- **Um usuário por cadastro no Ciclo 01**, inclusive no institucional: a instituição indica
  quem opera a App 08, e é esse usuário que responde pelos atos registrados. Mais de um acesso
  no mesmo cadastro fica para ciclo futuro.
- **Perfil pessoa física ou pessoa jurídica, declarado e não verificado**: quem escolhe é o
  próprio Apoiador, e o que o comprova são os artefatos declarados pelo Admin. O perfil muda a
  escada de valores sugeridos e o destaque do painel de efetividade, nada mais.
- **Apoia em dinheiro, insumo, equipamento, alimento, serviço, conteúdo, divulgação ou
  código** — as modalidades e as portas de cada uma estão no documento 14.
- Cada recurso aportado é registrado e contabilizado no seu **Poder Sustentador**, e a
  progressão de quem apoia — missões, níveis de sustento e selos — vive no documento 14.

### Pais e responsáveis

Adultos responsáveis pelos Guerreiros e Guerreiras. Acompanham a evolução da criança, autorizam
e revogam consentimentos, e têm acesso próprio à plataforma.

- **Cadastrados por um Admin ou por um Mestre** — não há autocadastro nem solicitação aberta.
  O responsável se apresenta **pessoalmente** em atividade presencial, na primeira vez, e
  informa seu e-mail e as crianças sob sua responsabilidade. Espera-se que isso aconteça no
  **primeiro dia de aula da criança**, a quem ele acompanha.
- O vínculo é feito com Guerreiros e Guerreiras **já cadastrados** no onboarding — qualquer um
  deles, não só os das turmas de quem cadastra —, e cada Guerreiro(a) tem no máximo **três
  responsáveis**.
- Todo vínculo declara o **grau de parentesco** do responsável com o Guerreiro(a), em texto
  livre.
- **Qualquer um dos vinculados autoriza ou revoga**, e a **recusa prevalece**: divergindo os
  responsáveis, a autorização fica suspensa até a gestão tratar.
- **Parentes e amigos além dos três responsáveis acompanham como Apoiador**, cadastrados pela
  via normal, e seguem o Guerreiro(a) pelo **nick**, no que é público. **O nick é informação que
  só a família cede** — a **busca** nunca o revela a um adulto: aceita só o nick exato, não
  sugere e não completa. As **exibições públicas** — cards, ranking e portfólio — mostram avatar
  e nick apenas de quem tem **divulgação autorizada** pelo responsável.

### Solicitação de participação (Mestres e Apoiadores)

Pessoas e instituições interessadas no projeto podem **solicitar sua inclusão como Mestre ou
Apoiador** por formulário público da vitrine. A solicitação é gravada e entra na fila de
avaliação dos Admins. **Ela não cria cadastro e não abre exceção à regra**: quem avalia e
cadastra continua sendo um Admin.

**Dados mínimos do formulário:** nome, e-mail, WhatsApp, pretensão (Mestre ou Apoiador) e um
texto livre de apresentação. Instituição representada e links comprobatórios são opcionais.
**Prazo de resposta ao solicitante: 7 dias.**

**A pergunta de entrada é o que a pessoa traz.** A chamada "Quero participar" abre com essa
escolha e encaminha conforme a resposta, pedindo o comprobatório que cabe a cada modalidade —
descrição e foto do bem, disponibilidade do serviço, amostra do conteúdo, repositório e
portfólio de quem apoia em código, artefatos da habilidade de quem quer ensinar. A tabela de
modalidades e destinos está no documento 14.

**Duas portas, conforme o que a pessoa traz.** Quem se apresenta sem transferência em dinheiro
— apoio em material, serviço, conteúdo, código ou divulgação, e quem quer ser Mestre — usa
este formulário da vitrine. Quem vai **aportar em dinheiro** faz o **pré-cadastro na Área do
Apoiador**, onde declara o aporte — uma das **necessidades publicadas**, um **valor sugerido**
ou um **valor livre** — e anexa o **comprovante**, obrigatório no Ciclo 01. As duas portas
terminam na mesma fila de avaliação do Admin, e nenhuma delas cadastra ninguém.

### Público geral / Visitantes

Interessados em acompanhar batalhas, ver o portfólio dos jovens e apoiar o trabalho. Todo o
conteúdo de vitrine é público, sem login.

### O que o cadastro do adulto carrega

O cadastro do Guerreiro(a) está no documento 03 §12, na adesão em duas etapas. O do adulto é
este:

| Persona     | Identidade no cadastro  |
| ----------- | ----------------------- |
| Mestre      | nome, e-mail e WhatsApp |
| Apoiador    | nome, e-mail e WhatsApp |
| Admin       | nome, e-mail e WhatsApp |
| Responsável | nome e e-mail           |

O **WhatsApp é opcional** onde aparece. Mestre e Apoiador têm também **nick e avatar**,
opcionais no cadastro: o Apoiador o traz do pré-cadastro, quando há um; o Mestre o define no
primeiro acesso — os dois sob a mesma unicidade do nick do Guerreiro(a).

O **artefato comprobatório** de Mestre e Apoiador é **link declarado** — endereço e rótulo do
que ele aponta. **Anexo de arquivo fica fora do Ciclo 01**: a prova é verificável por qualquer
visitante, e arquivo guardado na plataforma não é. O que o Admin declara no cadastro **não é
removível pelo próprio adulto**: ele acrescenta e remove só o que publicar depois, e a prova que
sustentou o cadastro permanece.

O Mestre publica o próprio artefato ao declará-lo. O Apoiador não: o que ele declara depois do
cadastro nasce **pendente** e só vai à página pública quando um **Admin o anexa ao cadastro** —
decisão do fundador, 2026-09-01.

### Comunidades Virtuais

A Comunidade Virtual é a **representação digital da comunidade em que o Guerreiro(a) vive na
realidade**.

> Uma Comunidade Virtual **existe na medida em que são registrados dados reais** do território.

**Quem cria.** A criação é **exclusiva dos Admins**. A comunidade nasce como território vazio —
nome, localização e granularidade, sem nenhum dado — e é **preenchida pelos Guerreiros e
Guerreiras**. Não há autocadastro de comunidades, pela mesma razão que não há autocadastro de
Mestres: a unidade territorial é estrutura da plataforma, não conteúdo gerado por usuário.

**Todo Guerreiro(a) pertence a uma comunidade.** O vínculo é **obrigatório** e atribuído
automaticamente no cadastro, **pela comunidade da aula em que a pessoa está entrando** — o
Admin declara a comunidade, a data e o horário de cada aula na gestão, e o onboarding usa a
aula vigente naquele momento. O Guerreiro(a) não informa a comunidade. É esse vínculo que
define a que território os dados coletados são creditados.

**No Ciclo 01 o Guerreiro(a) não muda de comunidade.** A transferência entre comunidades existe
no modelo, com a data da mudança preservada, mas só é operada em ciclo futuro.

**Como se constrói.** Parte das atividades é de coleta de dados locais — temperatura,
precipitação pluviométrica, coleta de resíduos, buracos na via, iluminação pública, trânsito,
transporte público, fotos, vídeos e memórias de pontos de referência.

**Em que granularidade.** O Guerreiro(a) registra no nível em que vive o problema: **comunidade
→ bairro → rua → condomínio → bloco → quadra**. Cada registro adiciona uma peça à comunidade
digital, que vai ganhando corpo conforme a participação cresce.

**A granularidade exigida é do desafio, e é livre.** O Mestre a declara ao criar o desafio, sem
teto: a trilha publicada alcança todas as comunidades, e cada uma tem a sua granularidade
máxima. O teto vale **na abertura da série** — o Guerreiro(a) só abre a sua se a comunidade
dele alcançar o nível exigido.

**Quem cadastra os locais.** Os locais são **cadastrados previamente pelos Admins**, e o
Guerreiro(a) **seleciona** a qual deles o dado se refere. Faltando o local, o Guerreiro(a)
**solicita a inclusão** pelo aplicativo — mesma lógica das demais solicitações: pedido
registrado não é cadastro. A solicitação é aprovada pelo **Mestre da trilha** ou por um
**Admin**, ambos alertados das solicitações em aberto.

**Quem cadastra os tipos de coleta.** O catálogo do que se mede — a forma de registro, a
unidade e a faixa esperada de cada tipo — é **cadastrado pelos Admins**, como os locais. O
Mestre **escolhe** um tipo do catálogo ao criar o desafio; não cria tipo novo.

#### Registro temporal e pontuação enquanto a coleta durar

**Regra vigente.** Os dados gerados nos desafios de coleta são **registrados de forma
temporal** na Comunidade Virtual e **vinculados ao Guerreiro(a) responsável**. A pontuação
correspondente também é temporal:

- Cada série de coleta tem uma **cadência** (diária, semanal, mensal) definida no desafio.
- **A série é individual**: cada Guerreiro(a) abre a sua no ponto que escolheu medir, e a
  Comunidade Virtual é a soma das séries de todos.
- **Enquanto a série se mantém ativa**, cada registro válido no prazo **rende pontos**. É
  pontuação recorrente, não de entrega única.
- **Duas cadências seguidas sem registro interrompem a série** — uma falha isolada não.
- **Interrompida a coleta, interrompe-se o cômputo.** Os pontos já ganhos permanecem, mas a
  série deixa de render.
- A retomada reativa o cômputo, sem recuperar o período parado.
- O registro é **manual** (digitado ou por voz) ou vem de **sensor construído pelo
  Guerreiro(a)**; a origem fica gravada no registro.
- O registro pode ser **foto ou vídeo** — é assim que se registra lixo acumulado, buraco na
  via ou poste apagado, que se medem por evidência e não por número.
- O registro **nasce válido e pontua na hora**, salvo o valor "a conferir", abaixo. O Mestre
  audita por **amostragem semanal**, junto com os lançamentos da semana, e pode invalidar
  registro inverossímil, o que **estorna** os pontos daquele registro — só dele. Valor "a
  conferir" entra obrigatoriamente na amostra.
- A amostra é de **10% dos registros da semana em cada série ativa, com o mínimo de um**. O
  piso garante que nenhuma série passe uma semana sem ser olhada, e o percentual acompanha
  quem registra mais. É o mesmo percentual da auditoria de trilhas e do corpus de apoio.
  **Série ativa é a que está ativa no instante da amostra** — a situação de cada série é
  apurada ali, não aproveitada de uma apuração anterior.
- **Valor fora da faixa declarada no desafio** entra como **a conferir** e não pontua até o
  Mestre validar: é a **confirmação** dele que credita, e o que ele invalida não tem o que
  estornar. É a trava contra dado inventado, e é também momento de ensinar a medir.

É o desenho que traduz o valor real do dado de território: uma medição isolada é curiosidade;
uma **série contínua** é evidência. A plataforma paga pela continuidade, porque é a
continuidade que serve à comunidade.

O valor em pontos do registro está no documento 11.

#### Guarda permanente dos dados, com o coletor identificado

Todos os dados coletados são **armazenados de forma permanente**, para avaliações e análises
futuras — inclusive depois que o Guerreiro(a) que os coletou deixar o projeto. **O vínculo com
o Guerreiro(a) responsável é preservado, sem anonimização.**

Por que a autoria fica: um dado de território sem autor conhecido é um dado sem
**procedência** — não há como auditar a série nem refazer o percurso de uma medição duvidosa.
E o registro é **realização do Guerreiro(a)**: apagar o nome apagaria o crédito.

A anonimização vale **na saída, não no armazenamento**: o que sai da plataforma para
pesquisas, painéis públicos e instituições é agregado e anonimizado conforme a finalidade. A
**saída pública agrega até o bairro**; rua, condomínio, bloco e quadra só saem no **conjunto
entregue mediante solicitação aprovada** por um Admin. É essa linha de corte que impede uma
série diária em rua de coletor único de apontar onde a criança mora.

**Piso de três coletores no recorte publicado.** Recorte com menos de **três coletores
distintos** não sai sozinho: soma-se ao nível acima até alcançar o piso. Vale para o painel
público e para o conjunto entregue, que desce abaixo do bairro. É o que protege o bairro de
coletor único, que o corte no bairro sozinho não alcança. O piso é **parâmetro declarado na
implantação**, com três como valor inicial.

**A lista pública de comunidades publica quatro indicadores**: séries abertas, séries ativas ao
fim do ciclo, registros válidos e continuidade. São os mesmos que embasam a avaliação do Poder
do Território, e o piso acima vale para eles — contagem de séries é, na prática, contagem de
coletores.

| Indicador                     | O que conta                                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------- |
| Séries abertas                | Séries abertas na comunidade, qualquer que seja o estado                                 |
| Séries ativas ao fim do ciclo | Séries ativas **no instante da consulta**, com o rótulo do ciclo corrente                |
| Registros válidos             | Registros em situação válida das séries da comunidade                                    |
| Continuidade                  | Média, entre as séries, da fração dos períodos de cadência esperados com registro válido |

O ciclo é rótulo declarado na implantação, sem calendário: enquanto ele corre, "ao fim do ciclo"
se apura **no instante da consulta**, a mesma régua que a auditoria por amostragem já usa.

**O ciclo é encerrado por ato de Admin**, na gestão — ato isolado, que fecha o corrente e nada
mais: o ciclo seguinte é declarado à parte, na implantação. O encerramento dispara o expurgo do
motivo da ocorrência de conduta e a saída dela do ranking, e **não congela indicador**: os
quatro seguem apurados no instante da consulta.

**Comunidade abaixo do piso sai na lista sem os indicadores.** A comunidade é o topo da
hierarquia e não há nível acima a que somá-la: ela permanece na lista, com nome e localização, e
os quatro indicadores não saem. Some o número, nunca a comunidade — quem está começando aparece.

**Revogação despersonaliza, não apaga.** Se o responsável revoga o consentimento, a plataforma
rompe o vínculo de autoria e destrói o mapeamento: o registro segue na série com um **código de
coletor que não corresponde a pessoa alguma**. A medição é dado do lugar e permanece; o dado
pessoal, que era só o vínculo, deixa de existir. A base legal das duas camadas está no
documento 03.

**Para que serve.** Os dados podem ser usados como **insumo para tomada de decisões** — pela
própria comunidade, por associações de moradores, escolas, poder público e pesquisas. O
objetivo é que a plataforma se torne uma **central _Data Driven_ das comunidades onde está
presente**. Uma série de anos só existe se o dado tiver sido guardado desde o primeiro dia —
daí a guarda permanente ser regra, e não opção.

**Por que é educativo.** Alimentar a Comunidade Virtual é, em si, aprendizado de ciência de
dados, método científico, cidadania e meio ambiente.

## 2. Poderes (habilidades)

Catálogo inicial. Os poderes marcados como **(ciclo futuro)** permanecem como direção do
projeto, sem trilha nem atividade previstas para o Ciclo 01.

| Poder                                             | Descrição                                                                                                                                                                                                                                        |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Poder da IA e Robótica**                        | Programação, eletrônica, robótica e IA. Trilhas: Robô Educa (1ª) e Batalha de Laser (2ª)                                                                                                                                                         |
| **Poder do Território**                           | Registro e ciência de dados do território (_Data Science_): sustentar séries de coleta reais da comunidade, com progressão e badges próprios. Todo Guerreiro(a) o exercita, pois toda trilha tem desafio de coleta                               |
| **Poder Sustentador**                             | O quanto Mestres e Apoiadores investiram na plataforma — o poder dos provedores                                                                                                                                                                  |
| **Poder da Rima** _(ciclo futuro)_                | Expressão artística: rima, rap, batalhas de rima. Validado em 2024 na Guerreira Zeferina, dentro do Inova Comunidade                                                                                                                             |
| **Poder das Redes** _(ciclo futuro)_              | Produção de conteúdo / "Monte seu Canal": comunicação digital, geração de áudio e vídeo e letramento crítico sobre riscos                                                                                                                        |
| **Poder da Capoeira** _(ciclo futuro)_            | Cultura e movimento, com análise de movimentos por visão computacional (contador de polichinelos e de movimentos corretos). Também validado em 2024. Sugestão técnica de captação: **MediaPipe**; TensorFlow como alternativa para classificação |
| **Outros conteúdos PNED / BNCC** _(ciclo futuro)_ | Alinhamento com políticas educacionais                                                                                                                                                                                                           |
| **Soft Skills** _(ciclo futuro)_                  | Habilidades socioemocionais                                                                                                                                                                                                                      |

Regras dos poderes:

- Pontos de um poder vêm **apenas das atividades propostas pelos Mestres** daquele poder.
- A **ativação/desbloqueio** de níveis acontece por **quiz ou desafios**.
- Todo poder, mesmo o mais técnico, deve abrir **paralelos com outras áreas do conhecimento e
  com os valores do projeto**.
- **O catálogo é cadastrado por Admin.** O Mestre escolhe entre os poderes cadastrados e não
  cria poder novo ao escrever a trilha.
- **Só poder de Guerreiro(a) recebe trilha.** O Poder Sustentador é derivado do que Mestres e
  Apoiadores aportaram e corre por moedas, selos e níveis de sustento — o Apoiador não pontua.
- **O papel do poder é declarado no catálogo, nunca deduzido do nome.** A coleta de dados do
  território credita o Poder do Território qualquer que seja a trilha em que o desafio nasceu,
  e é o catálogo que marca qual entrada exerce esse papel: o nome é rótulo de exibição e não
  identifica regra.
- **A marca de técnico é declarada no catálogo, nunca deduzida do nome.** Mesmo princípio do
  papel do poder: o Admin marca quais poderes são técnicos, e é essa marca — não o nome nem a
  descrição — que orienta a sugestão de atividade desplugada no template da missão.

**[Proposta]** Novos poderes alinhados aos valores: "Poder da Ancestralidade" (cultura
afro-brasileira e povos originários) e "Poder do Cuidado" (respeito, combate ao racismo e à
violência de gênero, mediação de conflitos).

## 3. Trilhas

- Cada trilha é uma **sequência de missões** — conteúdos e atividades que guiam o Guerreiro(a)
  pelos conhecimentos desejados. A **missão** é a menor unidade de progressão da trilha.
- Cada missão é **obrigatória ou opcional**, conforme o Mestre autor declarar.
- **Toda trilha abre com uma missão de sondagem**, que mede o nível de partida no poder.
- Ao avançar nas missões da trilha, o Guerreiro(a) vai **desbloqueando níveis de poderes**.
- Trilhas podem conter **conteúdos de terceiros**, curados pelos Mestres, e **bibliografia de
  apoio** impressa por missão.
- **Toda trilha deve conter desafios de coleta de dados reais** da comunidade do Guerreiro(a).
- **Toda trilha termina em criação original** apresentada publicamente (§4).
- **A trilha é bem comum da plataforma, não de uma comunidade.** Publicada, alcança todas as
  Comunidades Virtuais; o filtro por comunidade recai sobre o percurso do Guerreiro(a), nunca
  sobre a trilha. É o que faz a licença CC BY-SA valer na prática.
- O Guerreiro(a) é acompanhado pela **Área do Guerreiro(a) (App 05)**, que mostra a próxima
  missão, o que já foi conquistado e o que ainda está bloqueado.

### Regra vigente: toda trilha coleta dados reais

Não é um tipo de trilha — é requisito de **todas** elas. Cada trilha precisa prever ao menos um
desafio em que o Guerreiro(a) registra algo verificável do território onde vive, na Comunidade
Virtual à qual está vinculado. Por que a regra é geral:

- Garante que **toda comunidade ganhe corpo**, qualquer que seja o poder escolhido pelos
  Guerreiros e Guerreiras daquele ponto de apoio.
- Dá ao Guerreiro(a) **pontuação recorrente** que não depende de estar em aula.
- Conecta qualquer conteúdo ao **território e identidade**: nas trilhas técnicas de hoje a
  coleta é medição (temperatura, iluminação, resíduos); numa trilha cultural, seria o registro
  dos espaços, rodas e memórias do bairro. A regra é a mesma; muda o que se mede.

O desafio de coleta é **conteúdo de trilha**, com pontuação como qualquer outro, e é onde a
trilha encontra o método científico: medir, registrar, comparar ao longo do tempo.

### As duas primeiras trilhas da plataforma

Ambas de **autoria do Mestre fundador**, são os artefatos que comprovam sua habilidade em
Programação e Robótica.

| #      | Trilha               | Poder         | Do que se trata                                                                                                                  |
| ------ | -------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **1ª** | **Robô Educa**       | IA e Robótica | Construir o próprio robô com material reciclado ou kit e dar vida a ele com IA por voz; da montagem física à alteração do código |
| **2ª** | **Batalha de Laser** | IA e Robótica | Eletrônica, sensores, MQTT e rede: os Guerreiros e Guerreiras constroem os artefatos e disputam a batalha presencial             |

A 2ª trilha é a **sucessora natural** da 1ª: mesmo poder, um degrau a mais de complexidade.
Juntas demonstram o ciclo completo do jogo — mestre publica a trilha → Guerreiro(a) aprende
construindo → apresentação ou batalha presencial → pontuação e visibilidade.

As duas contam com **material de apoio impresso** do acervo Include, doado pelo
Goethe-Institut (inventário, posse e guarda no documento 05).

### Demais trilhas previstas

| Trilha                                      | Poder             | Conteúdo                                                                                                                                       | Quando       |
| ------------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **Social Media / Áudio e Vídeo para Redes** | Poder das Redes   | Roteiro, captação, edição e publicação; IA para geração de áudio e vídeo; direitos de imagem; **letramento crítico sobre os riscos das redes** | Ciclo futuro |
| **Rima**                                    | Poder da Rima     | Escrita, métrica e batalhas de rima                                                                                                            | Ciclo futuro |
| **Capoeira**                                | Poder da Capoeira | Cultura e movimento, com análise de movimentos por visão computacional                                                                         | Ciclo futuro |

> **Definição vigente:** essas trilhas — e os conteúdos de PNED/BNCC e Soft Skills — serão
> definidas e implementadas em **ciclo futuro**. Não integram o escopo do Ciclo 01, cujas
> trilhas em operação são apenas Robô Educa e Batalha de Laser. Isso também adia as decisões
> técnicas que dependiam delas, como a stack de análise de movimentos. **Rima e Capoeira têm
> validação prévia de campo**: participaram, com o Robô Educa, do projeto **Inova Comunidade**
> (2024, Guerreira Zeferina) — a retomada parte de experiência já testada.

A trilha de **Social Media** terá função dupla: forma o Guerreiro(a) em produção de conteúdo e
alimenta a equipe de divulgação do projeto nas redes. Nela vale integralmente a regra de LGPD:
Guerreiros e Guerreiras aparecem por **avatares**, nunca por imagens reais, e qualquer
publicação com criança identificável exige a autorização do responsável.

## 4. Atividades e desafios

As atividades devem ser criadas com **níveis de dificuldade graduais**, acessíveis por todos
**independentemente da idade** (6 a 16 anos). O Guerreiro(a) progride pelo nível de dificuldade
que consegue realizar, não pela idade que tem.

**Tipos:** **presenciais** (nos encontros) e **assíncronas / on-line** (no intervalo entre os
encontros presenciais). Os desafios são **semanais**, exceto a coleta de dados, que é
contínua.

**Toda atividade exige produção do Guerreiro(a)** — escrever, falar ou construir. Só se aprende
fazendo, errando e refazendo; consumir conteúdo não conclui missão. A plataforma lê o que foi
produzido e devolve retorno construtivo, mas **quem lança o resultado é o Mestre**: a leitura
automática é hipótese sobre o aprendizado, não veredito.

### Categorias de atividade

| Categoria                                  | Exemplos                                                              |
| ------------------------------------------ | --------------------------------------------------------------------- |
| Construção / making                        | Robô Educa, artefatos da Batalha de Laser                             |
| Programação e IA                           | Quizzes, alteração de código, prompts                                 |
| Coleta de dados do território              | Temperatura, chuva, resíduos, buracos — alimenta a Comunidade Virtual |
| Desplugadas (_Computer Science Unplugged_) | Lógica e algoritmos sem computador                                    |
| Valores e temas transversais               | Racismo, violência contra a mulher, identidade, povos originários     |
| Competição ao vivo                         | **Quiz ao Vivo** entre equipes na aula presencial                     |
| Culminância                                | Apresentação da **criação original** do Guerreiro(a) ou da equipe     |

### Criações originais dos Guerreiros e Guerreiras

**Definição vigente — toda trilha desemboca em criação original.** A culminância de cada
trilha é a apresentação pública de algo **criado pelo Guerreiro(a) (ou pela equipe) a partir do
conteúdo aprendido**: a versão própria do robô, um artefato remixado, um trecho de código
alterado, uma ideia nova sobre o que a trilha ensinou. A criação original distingue quem
**aprendeu** de quem apenas **executou**.

- **Autoria sempre creditada** — a criação carrega o nick do autor (ou dos autores) por toda
  a vida do registro, pela mesma razão que vale para a coleta de dados.
- **Vitrine pública** — as criações de Guerreiros e Guerreiras autorizados compõem o portfólio
  público.
- **Individual ou em equipe.** Entrega o Guerreiro(a) sozinho ou qualquer integrante da
  equipe fixa da trilha (§5), valendo pela equipe inteira; em equipe, o crédito é da equipe
  **e** de cada membro, com o papel que teve.
- **A entrega aceita texto, imagem, vídeo, arquivo e link.**
- A criação original **pontua e rende badge de autoria**, com o valor em pontos creditado
  **integralmente a cada integrante** da equipe — dividir puniria justamente a colaboração.
  Validá-la é ato do Mestre autor da trilha, e o valor está no documento 11.

### Desafios extras propostos por Apoiadores e Mestres

Além dos desafios semanais, **Apoiadores e Mestres podem propor desafios extras** ao longo de
um ciclo, sempre vinculados a uma trilha em andamento, **presenciais ou on-line**, com
**recompensa custeada** e **pontos extras** computados isoladamente, **até 10 por desafio**.
Existem duas modalidades — **aberto** (a todos os Guerreiros e Guerreiras da trilha) e
**direcionado** (a um Guerreiro(a) específico, mediante justificativa registrada). Todo desafio
extra exige **aprovação de um Admin** e recompensa **provida antes da publicação**; a
**validação pedagógica do Mestre da trilha** é exigida de todo proponente, menos do próprio
Mestre autor. Segue valendo **nenhum contato direto** entre Apoiador e Guerreiro(a).

> Regras completas, mecânica no ciclo e rastreio de efetividade: documento 04.

### Resultados de atividade (lançados pela gestão)

- **Realizada**
- **Realizada com mérito**
- **Mérito extra por auxílio aos colegas** — colaborar vale mais que competir.

### Pontuação negativa

Está prevista pontuação negativa por mau comportamento, agressões verbais ou físicas e
descumprimento de regras. É a aplicação prática do código de conduta e dos valores do projeto.

**Quem lança.** O **Mestre**, pela App 09, e o **Admin**, pela App 03. O lançamento exige
motivo registrado e **não depende de revisão de outro Admin** — quem estava na sala é quem
viu o que aconteceu.

### Condição de existência da atividade

> **Cada atividade só acontece se tiver os recursos necessários providos por Mestre ou
> Apoiador** (hora-aula, lanche, recompensas, insumos).

## 5. Equipes

**Definição vigente.** Equipes são **grupos livres de até 5 pessoas**, formados de maneira
espontânea pelos Guerreiros e Guerreiras **no App 01** — a gestão acompanha no painel e não
altera composição. Há dois tempos de vida:

| Equipe        | Serve a                                 | Termina                                 |
| ------------- | --------------------------------------- | --------------------------------------- |
| **Da aula**   | Atividades do dia e o Quiz ao Vivo      | Com a aula presencial, sem reaproveitar |
| **Da trilha** | A criação original que encerra a trilha | Com a culminância da trilha             |

- A **equipe da trilha é fixa**: os Guerreiros e Guerreiras a formam e o **Mestre a homologa
  em encontro presencial, na App 01**, o mesmo aparelho em que ela é formada; da homologação em
  diante ninguém entra nem sai. Cada Guerreiro(a) tem **uma equipe da trilha por trilha** que percorre.
- Cada Guerreiro(a) pode participar de **uma ou mais equipes** e **pontua em todas as
  atividades em que participar e colaborar**. **No Quiz ao Vivo joga por uma única equipe**,
  porque a partida é simultânea — a disputa segue sendo entre várias equipes, o que é único é a
  equipe de cada jogador.
- A composição segue o que a **atividade, o desafio ou a batalha determinar**: só Guerreiros e
  Guerreiras **ou** com **no máximo 1 familiar, de 17 anos ou mais**.

**A equipe mistura idades.** É o principal instrumento do jogo para transformar a diferença
de idades (6 a 16 anos) em força:

- As equipes **misturam idades e níveis deliberadamente**. A progressão individual segue por
  nível de dificuldade; é a convivência que é heterogênea de propósito.
- **Cada membro tem papel ativo** — quem constrói, quem registra, quem apresenta, quem
  media — e os papéis giram entre as atividades. O papel é **declarado na formação da equipe**,
  no App 01, e vale para o encontro inteiro.
- Guerreiros e Guerreiras **mais velhos ou mais avançados mediam os mais novos**: exercício
  prático do "colaborar vale mais que competir" e primeiro degrau do caminho de multiplicador.
- **O crédito individual é preservado**: a realização é da equipe, e o registro guarda o
  papel de cada membro.

## 6. Batalhas

**Batalhas são disputas de ideias e realizações entre os Guerreiros e Guerreiras** —
competições saudáveis que dão visibilidade ao que foi aprendido e construído:

- **Presenciais** (ex.: Batalha de Laser; batalhas de rima, em ciclo futuro).
- **De projetos e ideias** (apresentação de trabalhos, culminância).

Os resultados alimentam o ranking e o portfólio público dos Guerreiros e Guerreiras.

**A batalha é marco de trilha.** O Mestre autor a declara na trilha, como qualquer marco, e ela
acontece no encontro que a gestão agenda; na sala, as equipes que disputam são as da aula,
formadas no App 01. A batalha de projetos usa o mesmo cadastro, sem telemetria.

## 7. Níveis e badges

A progressão vai do **Nível 1** (inscrito e assíduo) ao **Nível 5 — Mestre Aprendiz**, que
deixa o Guerreiro(a) **apto ao treinamento de multiplicador** e ao voluntariado nos pontos de
apoio. Duas regras estruturais:

- **Níveis e badges são por trilha ou por poder, nunca globais** — um Guerreiro(a) pode ser
  Mestre Aprendiz no Robô Educa e estar no Nível 2 na Batalha de Laser.
- Ser Mestre Aprendiz **não** equivale a ser Mestre: o reconhecimento como Mestre continua
  dependendo de cadastro por Admin e de habilidade comprovada por artefatos publicados.

> Critérios de cada nível, catálogo de badges e tabela de pontuação: documento 11.

## 8. Recompensas

Há **duas espécies de recompensa**, que nunca se confundem:

| Espécie      | Como se obtém                             | Custa pontos?              |
| ------------ | ----------------------------------------- | -------------------------- |
| **De marco** | Conquistada ao atingir um marco da trilha | **Não** — nunca é comprada |
| **Avulsa**   | Trocada por pontos extras no catálogo     | Sim, **só pontos extras**  |

### 8.1 Recompensa de marco

**Regra vigente:** a recompensa é **conquistada ao atingir um marco da trilha** — desbloqueio
de uma missão, conclusão de etapa, batalha ou culminância —, **nunca comprada com saldo de
pontos**. É o que fecha o vínculo entre o jogo e a vida real: o esforço de aprender converte-se
em algo concreto na mão do Guerreiro(a), no momento em que a conquista acontece.

O **Mestre autor declara, na trilha, qual marco concede qual recompensa** — o Guerreiro(a) sabe
desde o começo o que cada conquista lhe rende. A trilha é bem comum e não tem ponto de apoio: o
lastro do recurso **não** é exigido na publicação, e a garantia de que a recompensa está provida
passa a valer no ato da entrega.

| Regra                | Definição                                                                                                                       |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Quem confirma        | O **Mestre vinculado à comunidade do Guerreiro(a)**, que escolhe o ponto de apoio de onde o recurso sai; o Admin nunca confirma |
| Lastro               | **Reverificado no ato da entrega**, contra o saldo do ponto de apoio escolhido                                                  |
| Marco alcançado      | Conferido contra o percurso já derivado da pontuação (missões concluídas)                                                       |
| Baixa no livro-razão | Sai **nesse ato**, junto da entrega, sem aula declarada e sem devolução possível                                                |

**A missão é o marco de uso corrente.** Ao cadastrar uma missão, o Mestre declara se o
desbloqueio dela libera recompensa — e é por aí que saem **as camisas, os livros e os kits do
acervo**, além dos kits de alimentos. Etapa, batalha e culminância continuam valendo como
marcos, para o que faz sentido entregar só no fim.

Catálogo inicial — **quais recompensas em quais marcos ainda é a definir**:

| Recompensa                  | Marco que concede (a definir) |
| --------------------------- | ----------------------------- |
| Kit alimentos 1 (3 itens)   | —                             |
| Kit alimentos 2 (6 itens)   | —                             |
| Camisa do projeto           | —                             |
| Livro próprio (linha Alpha) | —                             |
| Kit de montagem em MDF      | —                             |

**[Proposta]** Ao definir a tabela, ampliar o catálogo com recompensas não alimentares
(material escolar, componentes de robótica, ingressos culturais). Entregar alimento é
socialmente sensível e deve ser tratado com dignidade, no espírito do **"sem miséria"** baiano:
a recompensa celebra a conquista do Guerreiro(a); nunca pode soar como assistencialismo.

### 8.2 Recompensa avulsa, trocada por pontos extras

O Guerreiro(a) troca **pontos extras** — nunca regulares — por item de um **catálogo avulso**.
Alimento entra no catálogo: em comunidade periférica a falta é urgente, e quem ajuda o colega
também pode ser ajudado. A troca é ato do Guerreiro(a), não entrega de ofício.

| Regra                | Definição                                                                                                                                                                                                                                                                                                   |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Moeda da troca       | **Saldo disponível de pontos extras**; o acumulado não decresce                                                                                                                                                                                                                                             |
| Quem cadastra        | **Mestre**, direto; **Apoiador**, com homologação de Admin                                                                                                                                                                                                                                                  |
| Lastro               | Saldo do tipo de recurso no ponto de apoio do item **igual ou maior** que o estoque declarado — item sem lastro fica inativo, nunca é recusado; **exceção**: item de tipo de natureza **durável** é recusado no cadastro, porque o saldo durável é patrimônio (documento 04 §1) e nunca lastreia recompensa |
| Estoque              | Declarado no cadastro; item sem estoque não aparece para troca                                                                                                                                                                                                                                              |
| Encontro registrado  | A **Aula** do PRD-01, registrada pelo Mestre; o núcleo não verifica o estado dela nem a presença do Guerreiro(a) nela                                                                                                                                                                                       |
| Comunidade exigida   | O Guerreiro(a) precisa ser da **mesma comunidade do item**, senão a troca é recusada                                                                                                                                                                                                                        |
| Janela de troca      | **A App 01 abre e fecha** o momento de troca no encerramento do encontro; garantia da aplicação, o núcleo não a verifica                                                                                                                                                                                    |
| Entrega              | **No ato da troca**, ao final do encontro presencial, pelas mãos do Mestre                                                                                                                                                                                                                                  |
| Baixa no livro-razão | Na entrega, como na recompensa de marco                                                                                                                                                                                                                                                                     |

**O preço em pontos não deriva do valor em moedas nem em reais.** Ele é fixado em **esforço** —
quantos atos de cuidado e colaboração o item representa —, e o custo real segue no livro-razão,
invisível para a criança. Espelhar o preço em dinheiro ensinaria à criança quanto custa a comida
da casa dela, contra o mesmo "sem miséria" da seção anterior.

**O preço sai de uma tabela de referência**, mantida pela gestão e versionada por vigência, do
mesmo modo que a tabela de moedas do documento 04 §1. Quem cadastra item escolhe o tipo e o
preço vem da tabela — nem o Mestre nem o Apoiador arbitram valor. É o que impede que a mesma
caixa custe 20 pontos numa comunidade e 60 na vizinha.

**O piso é de 20 pontos extras.** Nenhum item vale menos, e é esse o valor que **desbloqueia a
primeira recompensa avulsa**. A régua de esforço é o encontro presencial, que rende no máximo
**18 pontos extras** a um Guerreiro(a) — 10 do auxílio aos colegas, 5 de valorizar colegas e
cuidar dos mais novos e 3 da conservação de três bens —, ou **28** quando corre um desafio
extra presencial. O piso é, portanto, pouco mais de um encontro exemplar.

> **A definir:** o preço de cada item da tabela acima do piso, e quantos encontros cada um
> representa. Depende do calendário do Ciclo 01, e é cadastro da gestão, não regra de
> documentação.

## 9. Manual do Guerreiro(a) (fluxo de entrada)

1. **Cadastro livre** — sem autorização de responsável. Informe apenas nome, data de
   nascimento (ou idade), nick e características do avatar; sua Comunidade Virtual já vem
   definida pela gestão. O cadastro pode ser feito por **voz ou chat**, com apoio de IA.
2. (Se houver kit) **Receba e monte seu robô, e personalize-o.**
3. **Acesse a plataforma.**
4. **Escolha um Poder.**
5. **Siga uma Trilha**, missão a missão — e receba o **livro de apoio** que passa a ser seu.
6. **Monte equipes** no app da aula — grupos livres de até 5 pessoas, válidos para aquele
   encontro; você pode estar em mais de uma.
7. **Realize os desafios semanais** (on-line, presenciais, em equipe, em equipe com familiar).
8. **Registre dados da sua comunidade** — a coleta rende pontos **enquanto você a mantiver**.
9. **Crie algo seu a partir do que aprendeu e apresente** — toda trilha termina com uma
   criação original, com o seu crédito de autoria.
10. **Conquiste recompensas nos marcos da trilha** — elas não se compram com pontos (§8).
11. **Peça ajuda para as atividades escolares** ao robô assistente.
12. **Autorização dos pais ou responsáveis** — uma só, dada e revogada na App 07, libera a
    divulgação pública do histórico, do perfil e das criações, a imagem em fotos e vídeos de
    eventos e a captação da sua produção por foto ou áudio. Sem ela, você participa
    normalmente — entregando a produção ao Mestre no encontro —, mas não aparece na vitrine
    nem nos rankings.

**[Proposta]** Modelar o estado do Guerreiro(a) em dois níveis: **"ativo"** (cadastro livre,
participa de tudo) e **"público"** (com autorização do responsável, aparece na vitrine).
