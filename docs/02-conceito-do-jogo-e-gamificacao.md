# 02 — Conceito do Jogo e Gamificação

O Comunidade Game é um "jogo" cujas partidas acontecem na vida real: aprender, criar, ajudar
os colegas e realizar atividades gera pontos, poderes e reconhecimento. Este documento reúne
todos os elementos do jogo.

## 1. Os elementos do jogo (personas)

### Jogadores (persona primária)
Crianças e jovens moradores de comunidades periféricas — participantes das oficinas,
batalhas e projetos. O jogador:

- Define seu **Nick** e as características do seu personagem (avatar).
- Escolhe **Poderes** e segue **Trilhas** para desenvolvê-los.
- Só ganha pontos de uma habilidade **na medida em que realiza as atividades propostas
  pelos Mestres** — não há pontos por presença passiva.
- Pode montar **Equipes** e participar de **Batalhas** e **Desafios**.
- Tem **voz e autoria**: cria a partir do que aprende
  ([§4](#criações-originais-dos-jogadores)), propõe ideias e sugere melhorias para as
  atividades e para a própria plataforma — o protagonismo do jogador é valor do projeto
  ([01 §3](01-visao-valores-e-proposito.md#3-valores-e-causas)).

O jogador é a **única persona com autocadastro** na plataforma
([03 §3](03-plataforma-e-arquitetura.md#3-app-01--onboarding-cadastro-e-registro-de-presença)).

### Admins (Organizadores / Equipe técnica)
Responsáveis pela operação da plataforma e pela logística dos eventos. Editam as seções
institucionais ("Quem somos", "Contatos"), fazem os lançamentos de atividades e
**cadastram Mestres e Apoiadores**.

Regras de admissão:

- O **fundador é o primeiro Admin** da plataforma.
- **Novos Admins são incluídos manualmente** por um Admin existente. Não existe
  autocadastro nem solicitação aberta de acesso administrativo.

### Mestres (persona secundária)
Especialistas/mentores que orientam e ministram oficinas. Os Mestres podem ser de
**qualquer área do conhecimento** — tecnologia, educação, artes, esportes, cultura,
ciências humanas e sociais — e não necessariamente representam poderes/habilidades
técnicas de TI: o motor do jogo é agnóstico de área
([11 §2](11-modelo-de-gamificacao.md#2-anatomia-da-trilha)). Regras de admissão:

- **Todo Mestre é cadastrado exclusivamente pelos Admins da plataforma.** Não há
  autocadastro de Mestres.
- Todo Mestre **tem que ter pelo menos uma habilidade** declarada.
- A habilidade precisa estar **comprovada por materiais ou artefatos disponibilizados na
  plataforma** — aulas presenciais e/ou gravadas, atividades propostas, videoaulas,
  projetos construídos, obras, registros de prática ou qualquer produção verificável da
  sua área (em tecnologia, por exemplo, exemplos de código; em artes, obras e
  apresentações; em esportes e cultura, registros de prática e formação). A prova é
  pública e verificável por qualquer visitante.
- Mestres também podem prover recursos para atividades (ver
  [04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).

> **Exemplo de referência — o Mestre fundador.** É considerado mestre em Programação e
> Robótica porque **construiu o software da plataforma**, propõe as atividades que os
> jogadores realizam e publica conteúdo (videoaulas, exemplos de código). É autor das
> **duas primeiras trilhas da plataforma** — [Robô Educa](06-robo-educa.md) e
> [Batalha de Laser](07-batalha-de-laser.md) ([§3](#as-duas-primeiras-trilhas-da-plataforma))
> — além da **idealização e implementação da própria plataforma**.

### Apoiadores / Patrocinadores
Pessoas e instituições que financiam ou divulgam o projeto. Regras de admissão:

- **Cadastrados exclusivamente pelos Admins da plataforma**, com o mesmo critério dos
  Mestres: o apoio precisa estar **comprovado por materiais ou artefatos registrados na
  plataforma** (recursos aportados, materiais fornecidos, ações de divulgação).
- Cada recurso aportado é registrado e contabilizado no seu histórico — o
  **"Poder Econômico"** (ver seção 2).

### Público geral / Visitantes
Interessados em acompanhar resultados das batalhas, ver o portfólio dos jovens e apoiar o
trabalho. Todo o conteúdo de vitrine é público, sem login.

### Comunidades Virtuais

A Comunidade Virtual é a **representação digital da comunidade em que o jogador vive na
realidade**. Ela é **criada vazia por um Admin da plataforma** e **preenchida pelos
jogadores**, à medida que eles registram dados reais do lugar onde moram.

> Uma Comunidade Virtual **existe na medida em que são registrados dados reais** do
> território.

**Quem cria.** A criação de uma Comunidade Virtual é **exclusiva dos Admins**, pela App 03
([03 §5](03-plataforma-e-arquitetura.md#5-app-03--gestão-administrativa)). Ela nasce como um
território vazio: nome, localização e granularidade, sem nenhum dado. Não há autocadastro de
comunidades, pela mesma razão que não há autocadastro de Mestres — a unidade territorial é
estrutura da plataforma, não conteúdo gerado por usuário.

**Todo jogador pertence a uma comunidade.** O vínculo do jogador a uma Comunidade Virtual é
**obrigatório** e é colhido já no cadastro
([03 §3](03-plataforma-e-arquitetura.md#3-app-01--onboarding-cadastro-e-registro-de-presença)).
É esse vínculo que define a que território os dados coletados por ele são creditados.

**Como se constrói.** Parte das atividades da plataforma é de coleta de dados locais —
por exemplo:

- temperatura local;
- precipitação pluviométrica;
- coleta de resíduos;
- buracos e problemas na via;
- iluminação pública, trânsito, transporte público;
- fotos e memórias de pontos de referência.

**Em que granularidade.** O jogador registra os dados no nível em que vive o problema:
**comunidade → bairro → rua → condomínio → bloco → quadra**. Cada registro adiciona uma
peça à comunidade digital, que vai "ganhando corpo" conforme a participação cresce.

#### Registro temporal e pontuação enquanto a coleta durar

**Regra vigente.** À medida que o jogador percorre a trilha e conclui os desafios de coleta
referentes à sua comunidade, os dados gerados são **registrados de forma temporal** na
respectiva Comunidade Virtual e **vinculados ao jogador responsável** pela coleta. Esses
dados **contam como pontuação do jogador — também de forma temporal**:

- Cada série de coleta tem uma **cadência** (diária, semanal, mensal) definida no desafio.
- **Enquanto a série se mantém ativa**, cada registro válido no prazo **rende pontos** ao
  jogador. É pontuação recorrente, não pontuação de entrega única.
- **Interrompida a coleta, interrompe-se o cômputo de pontos.** Quem para de medir para de
  pontuar — os pontos já ganhos permanecem, mas a série deixa de render.
- A retomada da série reativa o cômputo, sem recuperar o período em que ficou parada.

É o desenho que traduz o valor real do dado de território: uma medição isolada é curiosidade;
uma **série contínua** é evidência. A plataforma paga pela continuidade, porque é a
continuidade que serve à comunidade.

O acompanhamento das séries ativas do jogador — próxima medição, o que já foi registrado e
quanto a série está rendendo — fica na **App 05**
([03 §7](03-plataforma-e-arquitetura.md#7-app-05--área-do-jogador)).

> **A definir:** cadência e valor em pontos por tipo de coleta; janela de tolerância antes de
> considerar a série interrompida; teto de pontos por período; e mecânica de verificação da
> veracidade do dado
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

#### Guarda permanente dos dados, com o coletor identificado

Todos os dados coletados sobre a comunidade são
**armazenados de forma permanente**, para avaliações e análises futuras —
inclusive depois que o jogador que os coletou deixar o projeto. **O vínculo com o jogador
responsável pela coleta é preservado junto com o dado, sem anonimização.**

Por que a autoria fica: um dado de território sem autor conhecido é um dado sem
**procedência** — não há como auditar a série, refazer o percurso de uma medição duvidosa nem
comparar coletores. E há a razão que mais importa para o jogo: o registro é **realização do
jogador**, parte do histórico que ele construiu. Apagar o nome apagaria o crédito.

A anonimização continua valendo, mas **na saída, não no armazenamento**: o que sai da
plataforma para pesquisas, painéis públicos e instituições é agregado e anonimizado conforme
a finalidade ([03 §10](03-plataforma-e-arquitetura.md#10-proteção-de-dados-em-toda-a-plataforma-lgpd)).

**Para que serve.** Os dados captados **podem ser usados como insumo para tomada de
decisões** — pela própria comunidade, por associações de moradores, escolas, poder público
e pesquisas. O objetivo é que a plataforma se torne uma **central *Data Driven* das
comunidades onde está presente**: quem mora ali passa a ter evidência, não só percepção.
Uma série de anos só existe se o dado tiver sido guardado desde o primeiro dia — daí a
guarda permanente ser regra, e não opção.

**Por que isso é educativo.** Alimentar a Comunidade Virtual é, em si, aprendizado de
ciência de dados, método científico, cidadania e meio ambiente — e conecta o jogo ao valor
de **território e identidade**
([01-visao-valores-e-proposito.md](01-visao-valores-e-proposito.md#3-valores-e-causas)).

**Definição vigente — o registro de dados é um poder próprio.** O registro de dados do
território constitui o **Poder do Território** (registro e ciência de dados — *Data
Science*), com lugar no catálogo de poderes ([§2](#2-poderes-habilidades)): o jogador tem
um caminho de progressão e badges específicos por sustentar séries de coleta, e não apenas
pontos avulsos. Com a coleta obrigatória em toda trilha
([§3](#regra-vigente-toda-trilha-coleta-dados-reais)) e o painel público por comunidade na
vitrine
([03 §8](03-plataforma-e-arquitetura.md#8-app-06--vitrine-pública-apresentação-da-plataforma)),
é o poder que todo jogador exercita, qualquer que seja a trilha escolhida.

## 2. Poderes (habilidades)

Catálogo inicial previsto. Os poderes marcados como **(ciclo futuro)** serão definidos e
implementados depois desta etapa — permanecem no catálogo como direção do projeto, sem
trilha nem atividade previstas para o Ciclo 01
([§3](#demais-trilhas-previstas)).

| Poder | Descrição |
|---|---|
| **Poder da IA e Robótica** | Programação, eletrônica, robótica e IA — conteúdos do primeiro Mestre. Trilhas: [Robô Educa](06-robo-educa.md) (1ª) e [Batalha de Laser](07-batalha-de-laser.md) (2ª), apoiadas pelo acervo Include ([§3](#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut)) |
| **Poder do Território** | Registro e ciência de dados do território (*Data Science*): sustentar séries de coleta de dados reais da comunidade, com progressão e badges próprios. Todo jogador o exercita, pois toda trilha tem desafio de coleta ([§3](#regra-vigente-toda-trilha-coleta-dados-reais)) |
| **Poder da Rima** *(ciclo futuro)* | Expressão artística — rima, rap, batalhas de rima. Integrou, com o Robô Educa, o projeto **Inova Comunidade**, realizado e validado em **2024 na Comunidade Guerreira Zeferina** ([10 §2](10-case-01-guerreira-zeferina.md#2-por-que-guerreira-zeferina)); será retomado em ciclo futuro |
| **Poder das Redes** *(ciclo futuro)* | Produção de conteúdo / "Monte seu Canal" — comunicação digital, geração de áudio e vídeo para redes sociais e letramento crítico sobre seus riscos (trilha em [§3](#demais-trilhas-previstas)) |
| **Poder da Capoeira** *(ciclo futuro)* | Cultura e movimento; com componente tecnológico: análise de movimentos por visão computacional — contador de polichinelos e de movimentos executados com sucesso. Integrou, com o Robô Educa, o projeto **Inova Comunidade** (2024, Guerreira Zeferina); será retomado em ciclo futuro. **Sugestão técnica para a captação dos movimentos: biblioteca [MediaPipe](https://ai.google.dev/edge/mediapipe) (Python)**, que já entrega detecção de pose pronta; TensorFlow fica como alternativa para modelos próprios de classificação sobre os pontos captados |
| **Poder Econômico** | O quanto Mestres e Apoiadores investiram na plataforma (tempo, recursos etc.) — o poder dos provedores |
| **Outros conteúdos PNED / BNCC** *(ciclo futuro)* | Alinhamento com políticas educacionais (Política Nacional de Educação Digital e Base Nacional Comum Curricular) |
| **Soft Skills** *(ciclo futuro)* | Habilidades socioemocionais |

Regras dos poderes:

- Jogador ganha pontos de um poder **apenas realizando as atividades propostas pelos
  Mestres** daquele poder.
- A **ativação/desbloqueio** de níveis de poderes acontece por meio de **quiz ou desafios**.
- Todo poder, mesmo o mais técnico, deve abrir **paralelos com outras áreas do
  conhecimento e com os valores do projeto**
  ([01 §4](01-visao-valores-e-proposito.md#4-objetivos)).

**[Proposta]** Outros poderes alinhados aos valores do projeto: "Poder da Ancestralidade"
(cultura afro-brasileira e povos originários) e "Poder do Cuidado" (respeito, combate ao
racismo e à violência de gênero, mediação de conflitos). Assim as causas viram conteúdo
jogável, não apenas declaração de princípios — como já ocorre com o **Poder do Território**
e o valor de território e identidade.

## 3. Trilhas

> A **anatomia formal da trilha** — do que ela é composta (conteúdo, atividades, desafios,
> encontros presenciais, batalhas, culminâncias), como pontua e como se distribui pelas
> etapas de um ciclo — está no
> **[modelo de gamificação integrado](11-modelo-de-gamificacao.md#2-anatomia-da-trilha)**,
> em modelo agnóstico de área do conhecimento.

- O aluno é **guiado pelos conhecimentos desejados**: cada trilha é uma sequência de
  conteúdos e atividades.
- Ao seguir os pontos da trilha, o jogador vai **adquirindo/desbloqueando
  níveis de habilidades/poderes**.
- Quanto mais usa a plataforma e realiza atividades/desafios, mais pontos acumula.
- Trilhas podem conter conteúdos de **terceiros** (conteúdos externos curados pelos Mestres).
- **Toda trilha deve conter desafios de coleta de dados reais** da comunidade do jogador —
  ver abaixo.
- O jogador é acompanhado na trilha pela **Área do Jogador (App 05)**, que mostra o próximo
  ponto, o que já foi conquistado e o que ainda está bloqueado, além de apoiá-lo
  ([03 §7](03-plataforma-e-arquitetura.md#7-app-05--área-do-jogador)).

### Regra vigente: toda trilha coleta dados reais

**As trilhas devem possuir desafios relacionados à coleta de dados reais.** Não é um tipo de
trilha — é requisito de **todas** elas, das que já existem às que vierem. Cada trilha precisa
prever ao menos um desafio em que o jogador registra algo verificável do território onde
vive, na Comunidade Virtual à qual está vinculado ([§1](#comunidades-virtuais)).

Por que a regra é geral e não opcional:

- É o que garante que **toda comunidade ganhe corpo**, independentemente de qual poder os
  jogadores daquele ponto de apoio escolheram seguir.
- Dá ao jogador uma **pontuação recorrente** que não depende de estar em aula: enquanto a
  série de coleta se mantém ativa, ela rende pontos ([§1](#registro-temporal-e-pontuação-enquanto-a-coleta-durar)).
- Conecta qualquer conteúdo ao **território e identidade**, um dos valores do projeto
  ([01 §3](01-visao-valores-e-proposito.md#3-valores-e-causas)) — nas trilhas técnicas de
  hoje, a coleta é medição (temperatura, iluminação, resíduos); numa trilha de conteúdo
  cultural, seria o registro dos espaços, rodas e memórias do bairro. A regra é a mesma; muda
  o que se mede.

O desafio de coleta é **conteúdo de trilha**, com pontuação como qualquer outro, e é onde a
trilha técnica encontra o método científico: medir, registrar, comparar ao longo do tempo.

### As duas primeiras trilhas da plataforma

**Robô Educa** e **Batalha de Laser** são as duas primeiras trilhas da plataforma, ambas de
**autoria do Mestre fundador**, autor deste repositório, e são os artefatos que comprovam sua
habilidade em Programação e Robótica
([01 §7](01-visao-valores-e-proposito.md#7-o-fundador-primeiro-admin-e-primeiro-mestre)).

| # | Trilha | Poder associado | Do que se trata | Detalhamento |
|---|---|---|---|---|
| **1ª** | **Robô Educa** | Poder da IA e Robótica | Construir o próprio robô com material reciclado ou kit e dar vida a ele com IA por voz; da montagem física à leitura e alteração do código | [06-robo-educa.md](06-robo-educa.md) |
| **2ª** | **Batalha de Laser** | Poder da IA e Robótica | Eletrônica, sensores, MQTT e rede: os jogadores constroem os artefatos e disputam a batalha presencial | [07-batalha-de-laser.md](07-batalha-de-laser.md) |

A 2ª trilha é a **sucessora natural** da 1ª: mesmo poder, um degrau a mais de complexidade.
Juntas, demonstram o ciclo completo do jogo — mestre publica a trilha → jogador aprende
construindo → apresentação ou batalha presencial → pontuação e visibilidade na plataforma.

### Acervo didático de apoio — coleção Include e kits MDF (Goethe-Institut)

O projeto recebeu do **Goethe-Institut (Salvador)** — que passa a ser um dos **primeiros
Apoiadores da plataforma** ([04 §1](04-modelo-economico-e-sustentabilidade.md#1-a-economia-de-recursos-da-plataforma))
— uma coleção de livros do projeto **Include**, da **Campus Party**, e **30 kits em MDF**
para as trilhas do Robô Educa.

> **Formalização.** A doação da coleção de livros foi feita por meio de um **Termo de Doação
> assinado** entre o **Goethe-Institut (Salvador)** e a **Robô Educa — Kits Robóticos
> Educacionais** (CNPJ 51.730.395/0001-19), pessoa jurídica vinculada ao projeto
> ([01 §7](01-visao-valores-e-proposito.md#pessoa-jurídica-vinculada-ao-projeto)). O termo é
> o documento comprobatório do aporte no livro-razão da plataforma.

> **Definição vigente:** os livros são **material de apoio** das trilhas
> [Robô Educa](06-robo-educa.md) e [Batalha de Laser](07-batalha-de-laser.md), usados como
> referência de consulta nos pontos de trilha em que o conteúdo se encaixa. O vínculo é
> **ponto de trilha → capítulo recomendado**.
>
> O acervo está **vinculado ao MVP do [Case 01 — Comunidade Guerreira Zeferina](10-case-01-guerreira-zeferina.md#5-o-acervo-include-e-os-kits-mdf-neste-mvp)**:
> é no Ciclo 01 (ago–dez/2026) que ele entra em uso pela primeira vez.

| Título | Exemplares | Apoia principalmente |
|---|---:|---|
| Robótica Educativa — **Eletrônica** (Alpha) | 110 | Batalha de Laser |
| Robótica Educativa — **Sensores** (Alpha) | 73 | Batalha de Laser |
| Robótica Educativa — **Mecânica** (Alpha) | 69 | Robô Educa (montagem do corpo) |
| Include — **Programação I** | 25 | Robô Educa (código) |
| Include — **Sensores I** | 10 | Batalha de Laser |
| Include — **Mecânica I** | 7 | Robô Educa |
| Include — **Eletrônica I** | 4 | Batalha de Laser |
| **Total** | **298** | |

O acervo **aprofunda** os pontos das duas trilhas: quem quiser ir além do que a aula cobre
tem o livro na mão.

**Observações operacionais extraídas do inventário:**

- Os três títulos da linha **Alpha** (252 exemplares) têm volume suficiente para **um livro
  por jogador** em turmas inteiras e em mais de um ponto de apoio.
- Os títulos da linha **Include I** (46 exemplares, sendo apenas 4 de Eletrônica I) são
  **material escasso**: servem melhor como referência de bancada, uso compartilhado em
  equipe ou formação de mestres, voluntários e multiplicadores — não como distribuição
  individual.
- Cada exemplar é um **recurso aportado por Apoiador** e entra no livro-razão da plataforma,
  compondo o **Poder Econômico** do Goethe-Institut
  ([04 §1](04-modelo-economico-e-sustentabilidade.md#1-a-economia-de-recursos-da-plataforma)).

#### Os 30 kits em MDF

Além dos livros, o Goethe-Institut doou **30 kits em MDF** para as trilhas do
[Robô Educa](06-robo-educa.md). São o **corpo do robô** na versão kit — a alternativa à
garrafa PET —, o que permite atender turmas inteiras sem custo de material para o jogador.
Como qualquer recurso, entram no livro-razão e compõem o Poder Econômico do Apoiador
([04 §1](04-modelo-economico-e-sustentabilidade.md#primeiro-aporte-registrado--acervo-didático-e-kits-do-goethe-institut)).

Por serem **30 unidades**, os kits dimensionam na prática o tamanho da primeira turma que
pode montar o robô em MDF simultaneamente — a partir daí, ou se repõe o estoque, ou a
montagem volta a ser em material reciclado.

#### Posse dos livros — regime misto

Os exemplares seguem **regime misto**, aproveitando a assimetria do inventário:

| Linha | Exemplares | Destino |
|---|---:|---|
| **Alpha** (Eletrônica, Sensores, Mecânica) | 252 | **Doados ao jogador quando ele começa a trilha** — o livro é dele desde o primeiro dia |
| **Include I** (Programação, Sensores, Mecânica, Eletrônica) | 46 | **Acervo permanente do ponto de apoio** — material escasso, consulta em bancada |

O livro abundante é entregue **na entrada da trilha**, e não como prêmio de conclusão: ele é
**material de trabalho** do jogador durante todo o percurso, e é dele para sempre, conclua
ou não. O material escasso fica, e continua servindo às turmas seguintes.

Consequências: guarda e conservação em
[05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação); registro no
livro-razão em
[04 §1](04-modelo-economico-e-sustentabilidade.md#primeiro-aporte-registrado--acervo-didático-e-kits-do-goethe-institut).

### Demais trilhas previstas

| Trilha | Poder associado | Conteúdo | Quando |
|---|---|---|---|
| **Social Media / Geração de Áudio e Vídeo para Redes Sociais** | Poder das Redes | Roteiro, captação, edição e publicação; uso de ferramentas de IA para geração e edição de áudio e vídeo; direitos de imagem e proteção de dados; **letramento crítico sobre os riscos das redes sociais** | **Ciclo futuro** |
| **Rima** | Poder da Rima | Escrita, métrica e batalhas de rima. Integrou o **Inova Comunidade** (2024, Guerreira Zeferina) ao lado do Robô Educa | **Ciclo futuro** |
| **Capoeira** | Poder da Capoeira | Cultura e movimento, com análise de movimentos por visão computacional (captação sugerida: **MediaPipe**). Integrou o **Inova Comunidade** (2024, Guerreira Zeferina) ao lado do Robô Educa | **Ciclo futuro** |

> **Definição vigente:** as trilhas de **Social Media (Poder das Redes)**, **Rima** e
> **Capoeira** — e os demais conteúdos de **PNED/BNCC** e **Soft Skills** — serão
> **definidas e implementadas em ciclo futuro**. Não integram o escopo do
> [Ciclo 01](10-case-01-guerreira-zeferina.md), cujas trilhas em operação são apenas
> [Robô Educa](06-robo-educa.md) e [Batalha de Laser](07-batalha-de-laser.md). Seguem no
> catálogo como direção assumida do projeto, não como entrega desta etapa — o que também
> adia as decisões técnicas que dependiam delas, como a stack de análise de movimentos
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)). **Rima e Capoeira
> têm validação prévia de campo**: participaram, junto com o Robô Educa, do projeto
> **Inova Comunidade**, realizado em **2024 na própria Comunidade Guerreira Zeferina**
> ([10 §2](10-case-01-guerreira-zeferina.md#2-por-que-guerreira-zeferina)) — a retomada em
> ciclo futuro parte de experiência já testada, não do zero.

A trilha de **Social Media** tem função dupla: forma o jogador em produção de conteúdo e
alimenta a **equipe de divulgação do projeto nas redes**, produzindo material real. Nela vale
integralmente
a regra de LGPD do projeto: os jogadores aparecem por seus **avatares**, nunca por imagens
reais, e qualquer publicação com criança identificável exige consentimento específico do
responsável.

## 4. Atividades e desafios

> A **taxonomia completa** (modalidade × formato × natureza) e a **tabela única de todas
> as fontes de pontos** estão no
> [modelo de gamificação integrado](11-modelo-de-gamificacao.md#4-taxonomia-de-atividades-e-desafios).

As atividades devem ser criadas com **níveis de dificuldade graduais**,
acessíveis por todos os alunos/jogadores **independentemente de sua idade** (faixa de 6 a
16 anos). O jogador progride pelo nível de dificuldade que consegue realizar, não pela
idade que tem.

### Tipos de atividades
- **Presenciais** roteiro em
  [05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial).
- **Assíncronas / on-line**: a serem realizadas no intervalo entre os encontros preenciais.

### Tipos de desafio e pontuação

| Tipo de desafio | Pontos |
|---|---|
| Atividades on-line | 10 |
| Atividades presenciais | 10 |
| Atividades em equipe | 10 |
| Atividades em família | 20 |
| **Coleta de dados do território** | **Recorrente** — pontua a cada registro válido enquanto a série se mantiver ativa ([§1](#registro-temporal-e-pontuação-enquanto-a-coleta-durar)) |

- Os desafios são **semanais**.
- A atividade em família vale mais: o engajamento da família é estratégico para a
  permanência da criança no projeto.
- O desafio de **coleta de dados** é o único de pontuação **recorrente**: não se conclui, se
  mantém. Toda trilha tem ao menos um ([§3](#regra-vigente-toda-trilha-coleta-dados-reais)).

### Desafios extras propostos por Apoiadores

Além dos desafios semanais dos Mestres, **Apoiadores podem propor desafios extras** ao longo
de um ciclo, sempre **vinculados a uma trilha em andamento**. Concluir um desafio extra dá
direito a **recompensas extras**, custeadas pelo próprio Apoiador que o propôs, **e a pontos
extras** na plataforma.

**Definições vigentes:**

| Questão | Definição |
|---|---|
| **O desafio extra vale pontos?** | **Sim** — vale **pontos além da recompensa**. Os pontos são computados **isoladamente, como pontos extras**, sem se confundir com a pontuação regular da trilha |
| **Há teto de desafios extras simultâneos por trilha?** | **Não.** O controle não é numérico: cada desafio é **aprovado ou não pelos Admins**, caso a caso, depois da validação pedagógica do Mestre da trilha. A curadoria é o limite |
| **A recompensa extra pode ser exclusiva?** | **Nos desafios abertos, não** — o desafio é **aberto a todos os que concluírem**; o que é limitado é a **quantidade** de recompensas. A exceção controlada é o **desafio extra direcionado** (abaixo) |
| **Quantas recompensas?** | Uma **única** (para quem cumprir primeiro o desafio com sucesso) **ou várias** — todos que concluírem recebem, até esgotar a quantidade que o Apoiador disponibilizou |

A distinção entre "aberto a todos" e "quantidade limitada" é o ponto que sustenta a regra:
ninguém é impedido de disputar, e a escassez, quando existe, é declarada de antemão na
publicação do desafio — o jogador sabe, antes de começar, quantas recompensas existem e por
qual critério serão atribuídas.

#### Desafio extra direcionado

O Apoiador pode **direcionar um desafio extra a um jogador específico**: somente esse
jogador pode conseguir a respectiva recompensa, caso atinja os requisitos do desafio. É o
caminho para o apoio de interesse direto e legítimo — por exemplo, um **parente próximo**
(tio ou tia, padrinho ou madrinha) que propõe um desafio para um jogador da sua parentela.

Regras do desafio direcionado:

- Como os demais desafios extras, está **sujeito à validação pedagógica do Mestre da
  trilha e à aprovação de um Admin** — e, no direcionado, a aprovação exige
  **justificativa registrada** do vínculo ou interesse do proponente (ex.: parentesco).
- Vale a regra de lastro (recompensa provida antes da publicação) e a regra de mediação:
  **nenhum contato direto** entre Apoiador e jogador — proposta, entrega e reconhecimento
  passam pela plataforma
  ([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras)).
- Os pontos são **extras**, computados isoladamente, como em qualquer desafio extra.
- O rastro é o mesmo: o desafio, a justificativa aprovada e a realização do jogador ficam
  registrados no histórico do Apoiador.

O ponto central é o **rastro**: tanto a recompensa oferecida quanto as **realizações dos
jogadores** naquele desafio ficam registradas **no histórico do Apoiador**. Com isso é
possível acompanhar, ao longo do tempo, **a efetividade do apoio oferecido** — não só quanto
alguém aportou, mas o que aconteceu por causa daquele aporte.

Regras que se aplicam:

- O desafio extra é **conteúdo de trilha**, não paralelo a ela — precisa ser **validado pelo
  Mestre** responsável pela trilha e **aprovado por um Admin** antes de ir ao ar
  ([03 §5](03-plataforma-e-arquitetura.md#5-app-03--gestão-administrativa)).
- Vale a regra de lastro: a recompensa extra precisa estar **provida** antes de o desafio ser
  publicado ([04 §1](04-modelo-economico-e-sustentabilidade.md#1-a-economia-de-recursos-da-plataforma)).
- Vale a regra de proteção de menores: **nenhum contato direto** entre Apoiador e jogador —
  a proposta, a entrega e o reconhecimento passam pela plataforma
  ([04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras)).

Mecânica e histórico detalhados em
[04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras).

### Criações originais dos jogadores

**Definição vigente — toda trilha desemboca em criação original.** A culminância de cada
trilha é a apresentação pública de algo **criado pelo jogador (ou pela equipe) a partir do
conteúdo aprendido** — a versão própria do robô, um artefato remixado, um trecho de código
alterado, uma ideia nova sobre o que a trilha ensinou. A criação original é o que distingue
quem **aprendeu** de quem apenas **executou**: aplicar o conteúdo em algo seu é a prova mais
forte de aprendizado que o jogo reconhece — e é ela que o jogo destaca e incentiva.

Regras da criação original:

- **Autoria sempre creditada** — a criação carrega o nick do autor (ou dos autores, em
  equipe) por toda a vida do registro, pela mesma razão que vale para a coleta de dados:
  apagar o nome apagaria o crédito
  ([§1](#guarda-permanente-dos-dados-com-o-coletor-identificado)).
- **Vitrine pública** — as criações de jogadores autorizados compõem o portfólio público na
  vitrine ([03 §8](03-plataforma-e-arquitetura.md#8-app-06--vitrine-pública-apresentação-da-plataforma);
  [11 §8.1](11-modelo-de-gamificacao.md#81-vitrine-pública-app-06)).
- Em **equipe**, o crédito é da equipe **e** de cada membro, com o papel que cada um teve na
  criação ([§5](#5-equipes)).
- A criação original **pontua e rende badge de autoria**
  ([11 §5](11-modelo-de-gamificacao.md#5-motor-de-pontuação);
  [11 §7](11-modelo-de-gamificacao.md#7-badges)).

> **A definir:** valor em pontos da criação original e critérios do badge de autoria
> ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)).

### Categorias de atividade

| Categoria | Exemplos |
|---|---|
| Construção / making | Robô Educa, artefatos da Batalha de Laser |
| Programação e IA | Quizzes, alteração de código, prompts |
| Coleta de dados do território | Temperatura, chuva, resíduos, buracos — alimenta a Comunidade Virtual |
| Desplugadas (Computer Science Unplugged) | Lógica e algoritmos sem computador |
| Valores e temas transversais | Racismo, violência contra a mulher, identidade, povos originários |
| Competição ao vivo | **Quiz ao Vivo** entre equipes na aula presencial ([05 §4](05-implantacao-e-operacao.md#4-atividade-modelo-quiz-ao-vivo)) |
| Culminância | Apresentação livre do que foi construído/aprendido — a **criação original** do jogador ou da equipe ([acima](#criações-originais-dos-jogadores)) |

### Resultados de atividade (lançados pela gestão)
Cada participação em atividade realizada recebe um resultado:

- **Realizada**
- **Realizada com mérito**
- **Mérito extra por auxílio aos colegas** — colaborar vale mais que competir.

### Pontuação negativa
Está prevista pontuação negativa, por exemplo: mau comportamento, agressões verbais e/ou
físicas, descumprimento de regras. É a aplicação prática do código de conduta e dos valores
do projeto.

### Condição de existência da atividade
> **Cada atividade só acontece se tiver os recursos necessários providos por Mestre ou
> Apoiador** (hora-aula, lanche, recompensas, insumos). Ver
> [04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md).

## 5. Equipes

- Equipes **mistas** com até **5 membros**.
- **Equipe Familiar** — modalidade específica para jogar com a família.

**Definição vigente — "mista" inclui a mistura de idades.** A equipe é o principal
instrumento do jogo para transformar a diferença de idades da faixa (6 a 16 anos) em força:

- As equipes **misturam idades e níveis deliberadamente**. A progressão individual segue
  sendo por nível de dificuldade ([§4](#4-atividades-e-desafios)); é a convivência que é
  heterogênea de propósito.
- **Cada membro tem papel ativo** na atividade — quem constrói, quem registra, quem
  apresenta, quem media — e os papéis giram entre as atividades, para que ninguém fique
  sempre no mesmo lugar.
- Jogadores **mais velhos ou mais avançados atuam como mediadores dos mais novos** — o
  exercício prático do "colaborar vale mais que competir"
  ([§4](#resultados-de-atividade-lançados-pela-gestão)) e o primeiro degrau do caminho de
  multiplicador ([05 §7](05-implantacao-e-operacao.md#7-formação-de-mestres-e-multiplicadores)).
- **O crédito individual é preservado**: a realização é da equipe, e o registro guarda o
  papel de cada membro — ninguém desaparece no coletivo
  ([§4](#criações-originais-dos-jogadores)).

## 6. Batalhas

**Batalhas são disputas de ideias e realizações entre os Jogadores** — competições
saudáveis que dão visibilidade ao que foi aprendido e construído. Podem ser:

- Presenciais (ex.: [Batalha de Laser](07-batalha-de-laser.md); batalhas de rima quando a
  trilha correspondente entrar, em ciclo futuro).
- De projetos/ideias (apresentação de trabalhos, culminância).

Os resultados das batalhas alimentam o ranking e o portfólio público dos jogadores. O
padrão de integração entre uma batalha física e o backend (telemetria → API → lançamento
da atividade) está em
[11 §8.4](11-modelo-de-gamificacao.md#84-jogos-sobre-o-backend-app-04-e-terceiros).

## 7. Níveis e badges (gamificação)

| Nível | Critério | O que destrava |
|---|---|---|
| Nível 1 | Inscrito na oficina e assíduo | Participação nas atividades |
| Nível 2 | Bom rendimento | — |
| Nível 3 | Ótimo rendimento | — |
| Nível 4 | Apoio aos colegas nas aulas | — |
| **Nível 5** | **Mestre Aprendiz** | Ao concluir este nível, o jogador é considerado **Mestre Aprendiz** e fica **apto ao treinamento de multiplicador** |

Observações:

- A progressão culmina no **Mestre Aprendiz**: o jogador que chega ao topo de um poder ou
  de uma trilha passa a poder ensinar — é a engrenagem de formação de multiplicadores
  ([05 §7](05-implantacao-e-operacao.md#7-formação-de-mestres-e-multiplicadores)).
  Ser Mestre Aprendiz **não** equivale a ser Mestre: o reconhecimento como **Mestre** na
  plataforma continua dependendo de cadastro por um Admin e de habilidade comprovada por
  artefatos publicados ([§1](#1-os-elementos-do-jogo-personas)).
- O **badge de Mestre Aprendiz é por trilha ou por poder**, não global — um jogador pode ser
  Mestre Aprendiz na trilha Robô Educa e estar no Nível 2 na Batalha de Laser.
- O badge de Mestre Aprendiz também é o critério para a **formação de voluntários de suporte
  diário nos pontos de apoio**
  ([05 §7](05-implantacao-e-operacao.md#7-formação-de-mestres-e-multiplicadores)).
- **Badges** representam poderes e conquistas, e aparecem nos cards públicos dos jogadores
  ([03-plataforma-e-arquitetura.md](03-plataforma-e-arquitetura.md)). Catálogo de badges
  por tipo e composição dos cards em
  [11 §7](11-modelo-de-gamificacao.md#7-badges) e
  [11 §8.2](11-modelo-de-gamificacao.md#82-cards-dos-personagens).

## 8. Recompensas

**Regra vigente:** à medida que avançam nas trilhas, os jogadores **acumulam pontos, e esses
pontos podem ser trocados por recompensas**. É o que fecha o vínculo entre o jogo e a vida
real: o esforço de aprender converte-se em algo concreto na mão do jogador.

Catálogo inicial:

| Recompensa | Custo em pontos (a definir) |
|---|---|
| Kit alimentos 1 (3 itens) | 20 |
| Kit alimentos 2 (6 itens) | 20 |

**Definição vigente:** a pontuação dos kits de alimentos e das demais recompensas **ainda
é uma sugestão, a ser definida** — a tabela acima é referência provisória, não regra
fechada.

**[Proposta]** Ao definir a tabela, ampliar o catálogo com recompensas não alimentares
(material escolar, componentes de robótica, ingressos culturais), mantendo o cuidado de
que a troca de pontos por alimento é sensível socialmente e deve ser tratada com dignidade
— no espírito do **"sem miséria"** baiano: fartura, bem-estar, ambiente agradável,
alimentos em abundância. A recompensa celebra a conquista do jogador; nunca pode soar como
assistencialismo.

Prêmios também aparecem no orçamento como **consumíveis** e **duráveis**
([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).

## 9. Manual do Jogador (fluxo de entrada)

1. **Cadastro livre** — o primeiro acesso não exige autorização de responsável. Informe
   apenas: **nome do jogador, data de nascimento (ou idade), nick, a sua Comunidade Virtual
   e características do avatar**. A partir daí o jogador já pode participar das atividades.
   O cadastro pode ser feito por **voz ou chat**, com apoio de IA
   ([03 §3](03-plataforma-e-arquitetura.md#3-app-01--onboarding-cadastro-e-registro-de-presença)).
2. (Se houver kit) **Receba/monte seu robô e personalize-o** — [Robô Educa](06-robo-educa.md).
3. **Acesse a plataforma.**
4. **Escolha um Poder.**
5. **Siga uma Trilha** — e receba o **livro de apoio** da linha Alpha, que passa a ser seu
   ([§3](#posse-dos-livros--regime-misto)).
6. **Monte equipes** (mistas de até 5 membros, ou Equipe Familiar).
7. **Realize os desafios semanais** (on-line, presenciais, em equipe, em família).
8. **Registre dados da sua comunidade** e ajude a construir sua Comunidade Virtual — a
   coleta rende pontos **enquanto você a mantiver**
   ([§1](#registro-temporal-e-pontuação-enquanto-a-coleta-durar)).
9. **Crie algo seu a partir do que aprendeu e apresente** — toda trilha termina com uma
   criação original, com o seu crédito de autoria
   ([§4](#criações-originais-dos-jogadores)).
10. **Troque seus pontos por recompensas.**
11. **Peça ajuda para a realização de atividades escolares** (apoio escolar pela
    plataforma/robô assistente).
12. **Autorização dos pais ou responsáveis** — necessária apenas para que o **histórico e
    o perfil do jogador sejam divulgados na plataforma** (vitrine, rankings públicos).
    Sem ela, o jogador continua participando normalmente, mas seus dados não são exibidos
    publicamente. A autorização é dada — e pode ser revogada — na **App 07**
    ([03 §9](03-plataforma-e-arquitetura.md#9-app-07--área-dos-pais-e-responsáveis)).

**[Proposta]** Modelar o estado do jogador em dois níveis: **"ativo"** (cadastro livre,
participa de tudo) e **"público"** (com autorização do responsável, aparece na vitrine e
nos rankings).
