# 02 — Conceito do Jogo e Gamificação

O Comunidade Game é um "jogo" cujas partidas acontecem na vida real: aprender, criar, ajudar
os colegas e realizar atividades gera pontos, poderes e reconhecimento.

> Este documento define **o que são** os elementos do jogo. **Como eles se ligam e quanto
> valem** — anatomia da trilha, taxonomia de atividades, tabela de pontos, níveis e badges —
> está no documento 11.

## 1. Os elementos do jogo (personas)

### Jogadores (persona primária)

Crianças e jovens moradores de comunidades periféricas. O jogador:

- Define seu **Nick** e as características do seu personagem (avatar).
- Escolhe **Poderes** e segue **Trilhas** para desenvolvê-los.
- Só ganha pontos de uma habilidade **na medida em que realiza as atividades propostas pelos
  Mestres** — não há pontos por presença passiva.
- Pode montar **Equipes** e participar de **Batalhas** e **Desafios**.
- Tem **voz e autoria**: cria a partir do que aprende, propõe ideias e sugere melhorias para
  as atividades e para a própria plataforma.

O jogador é a **única persona com autocadastro** na plataforma.

### Admins (Organizadores / Equipe técnica)

Responsáveis pela operação da plataforma e pela logística dos eventos. Editam as seções
institucionais, fazem os lançamentos de atividades e **cadastram Mestres e Apoiadores**.

O **fundador é o primeiro Admin**. **Novos Admins são incluídos manualmente** por um Admin
existente — não há autocadastro nem solicitação aberta de acesso administrativo.

### Mestres (persona secundária)

Especialistas e mentores que orientam e ministram oficinas. Podem ser de **qualquer área do
conhecimento** — tecnologia, educação, artes, esportes, cultura, ciências humanas e sociais:
o motor do jogo é agnóstico de área. Regras de admissão:

- **Todo Mestre é cadastrado exclusivamente pelos Admins.** Não há autocadastro.
- Todo Mestre **tem que ter pelo menos uma habilidade declarada**.
- A habilidade precisa estar **comprovada por materiais ou artefatos disponibilizados na
  plataforma** — aulas presenciais ou gravadas, atividades propostas, videoaulas, projetos,
  obras, registros de prática, **currículo, portfólio, redes sociais e documentos externos**
  ou qualquer produção verificável da sua área. A prova é pública e verificável por qualquer
  visitante.
- Mestres também podem prover recursos para atividades.

> **Exemplo de referência — o Mestre fundador.** É mestre em Programação e Robótica porque
> construiu o software da plataforma, propõe as atividades que os jogadores realizam e
> publica conteúdo. É autor das duas primeiras trilhas.

### Apoiadores / Patrocinadores

Pessoas e instituições que financiam ou divulgam o projeto.

- **Cadastrados exclusivamente pelos Admins**, com o mesmo critério dos Mestres: o apoio
  precisa estar **comprovado por materiais ou artefatos registrados na plataforma** —
  incluindo currículo, portfólio, redes sociais e documentos externos da pessoa ou
  instituição.
- Cada recurso aportado é registrado e contabilizado no seu **Poder Econômico**.

### Solicitação de participação (Mestres e Apoiadores)

Pessoas e instituições interessadas no projeto podem **solicitar sua inclusão como Mestre ou
Apoiador** por formulário público da vitrine. A solicitação é gravada e entra na fila de
avaliação dos Admins. **Ela não cria cadastro e não abre exceção à regra**: quem avalia e
cadastra continua sendo um Admin.

### Público geral / Visitantes

Interessados em acompanhar batalhas, ver o portfólio dos jovens e apoiar o trabalho. Todo o
conteúdo de vitrine é público, sem login.

### Comunidades Virtuais

A Comunidade Virtual é a **representação digital da comunidade em que o jogador vive na
realidade**.

> Uma Comunidade Virtual **existe na medida em que são registrados dados reais** do
> território.

**Quem cria.** A criação é **exclusiva dos Admins**. A comunidade nasce como território
vazio — nome, localização e granularidade, sem nenhum dado — e é **preenchida pelos
jogadores**. Não há autocadastro de comunidades, pela mesma razão que não há autocadastro de
Mestres: a unidade territorial é estrutura da plataforma, não conteúdo gerado por usuário.

**Todo jogador pertence a uma comunidade.** O vínculo é **obrigatório** e atribuído
automaticamente no cadastro: o Admin define na gestão a **comunidade default do onboarding**,
e é ela que o jogador recebe — sem precisar informá-la. É esse vínculo que define a que
território os dados coletados são creditados.

**Como se constrói.** Parte das atividades é de coleta de dados locais — temperatura,
precipitação pluviométrica, coleta de resíduos, buracos na via, iluminação pública, trânsito,
transporte público, fotos, vídeos e memórias de pontos de referência.

**Em que granularidade.** O jogador registra no nível em que vive o problema: **comunidade →
bairro → rua → condomínio → bloco → quadra**. Cada registro adiciona uma peça à comunidade
digital, que vai ganhando corpo conforme a participação cresce.

**Quem cadastra os locais.** Os locais são **cadastrados previamente pelos Admins**, e o
jogador **seleciona** a qual deles o dado se refere. Faltando o local, o jogador **solicita a
inclusão** pelo aplicativo, e a gestão avalia — mesma lógica das demais solicitações: pedido
registrado não é cadastro.

#### Registro temporal e pontuação enquanto a coleta durar

**Regra vigente.** Os dados gerados nos desafios de coleta são **registrados de forma
temporal** na Comunidade Virtual e **vinculados ao jogador responsável**. A pontuação
correspondente também é temporal:

- Cada série de coleta tem uma **cadência** (diária, semanal, mensal) definida no desafio.
- **A série é individual**: cada jogador abre a sua no ponto que escolheu medir, e a
  Comunidade Virtual é a soma das séries de todos.
- **Enquanto a série se mantém ativa**, cada registro válido no prazo **rende pontos**. É
  pontuação recorrente, não de entrega única.
- **Duas cadências seguidas sem registro interrompem a série** — uma falha isolada não.
- **Interrompida a coleta, interrompe-se o cômputo.** Os pontos já ganhos permanecem, mas a
  série deixa de render.
- A retomada reativa o cômputo, sem recuperar o período parado.
- O registro é **manual** (digitado ou por voz) ou vem de **sensor construído pelo jogador**;
  a origem fica gravada no registro.
- O registro pode ser **foto ou vídeo** — é assim que se registra lixo acumulado, buraco na
  via ou poste apagado, que se medem por evidência e não por número.
- O registro **nasce válido e pontua na hora**. O Mestre audita por **amostragem** e pode
  invalidar registro inverossímil, o que retira os pontos correspondentes.

É o desenho que traduz o valor real do dado de território: uma medição isolada é curiosidade;
uma **série contínua** é evidência. A plataforma paga pela continuidade, porque é a
continuidade que serve à comunidade.

O valor em pontos do registro está no documento 11.

#### Guarda permanente dos dados, com o coletor identificado

Todos os dados coletados são **armazenados de forma permanente**, para avaliações e análises
futuras — inclusive depois que o jogador que os coletou deixar o projeto. **O vínculo com o
jogador responsável é preservado, sem anonimização.**

Por que a autoria fica: um dado de território sem autor conhecido é um dado sem
**procedência** — não há como auditar a série nem refazer o percurso de uma medição duvidosa.
E o registro é **realização do jogador**: apagar o nome apagaria o crédito.

A anonimização vale **na saída, não no armazenamento**: o que sai da plataforma para
pesquisas, painéis públicos e instituições é agregado e anonimizado conforme a finalidade. A
saída pública chega **até o nível da rua**; condomínio, bloco e quadra ficam para uso interno
e para entregas com acordo formal.

> **A definir:** como evitar que uma série diária em rua com um único coletor indique onde a
> criança mora.

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
| **Poder do Território**                           | Registro e ciência de dados do território (_Data Science_): sustentar séries de coleta reais da comunidade, com progressão e badges próprios. Todo jogador o exercita, pois toda trilha tem desafio de coleta                                    |
| **Poder Econômico**                               | O quanto Mestres e Apoiadores investiram na plataforma — o poder dos provedores                                                                                                                                                                  |
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

**[Proposta]** Novos poderes alinhados aos valores: "Poder da Ancestralidade" (cultura
afro-brasileira e povos originários) e "Poder do Cuidado" (respeito, combate ao racismo e à
violência de gênero, mediação de conflitos).

## 3. Trilhas

- Cada trilha é uma **sequência de conteúdos e atividades** que guia o jogador pelos
  conhecimentos desejados.
- Ao avançar nos pontos da trilha, o jogador vai **desbloqueando níveis de poderes**.
- Trilhas podem conter **conteúdos de terceiros**, curados pelos Mestres, e **bibliografia de
  apoio** impressa por ponto de trilha.
- **Toda trilha deve conter desafios de coleta de dados reais** da comunidade do jogador.
- **Toda trilha termina em criação original** apresentada publicamente (§4).
- O jogador é acompanhado pela **Área do Jogador (App 05)**, que mostra o próximo ponto, o
  que já foi conquistado e o que ainda está bloqueado.

### Regra vigente: toda trilha coleta dados reais

Não é um tipo de trilha — é requisito de **todas** elas. Cada trilha precisa prever ao menos
um desafio em que o jogador registra algo verificável do território onde vive, na Comunidade
Virtual à qual está vinculado. Por que a regra é geral:

- Garante que **toda comunidade ganhe corpo**, qualquer que seja o poder escolhido pelos
  jogadores daquele ponto de apoio.
- Dá ao jogador **pontuação recorrente** que não depende de estar em aula.
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
| **2ª** | **Batalha de Laser** | IA e Robótica | Eletrônica, sensores, MQTT e rede: os jogadores constroem os artefatos e disputam a batalha presencial                           |

A 2ª trilha é a **sucessora natural** da 1ª: mesmo poder, um degrau a mais de complexidade.
Juntas demonstram o ciclo completo do jogo — mestre publica a trilha → jogador aprende
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
> validação prévia de campo**: participaram, com o Robô Educa, do projeto **Inova
> Comunidade** (2024, Guerreira Zeferina) — a retomada parte de experiência já testada.

A trilha de **Social Media** terá função dupla: forma o jogador em produção de conteúdo e
alimenta a equipe de divulgação do projeto nas redes. Nela vale integralmente a regra de
LGPD: jogadores aparecem por **avatares**, nunca por imagens reais, e qualquer publicação com
criança identificável exige consentimento específico do responsável.

## 4. Atividades e desafios

As atividades devem ser criadas com **níveis de dificuldade graduais**, acessíveis por todos
**independentemente da idade** (6 a 16 anos). O jogador progride pelo nível de dificuldade
que consegue realizar, não pela idade que tem.

**Tipos:** **presenciais** (nos encontros) e **assíncronas / on-line** (no intervalo entre os
encontros presenciais). Os desafios são **semanais**, exceto a coleta de dados, que é
contínua.

### Categorias de atividade

| Categoria                                  | Exemplos                                                              |
| ------------------------------------------ | --------------------------------------------------------------------- |
| Construção / making                        | Robô Educa, artefatos da Batalha de Laser                             |
| Programação e IA                           | Quizzes, alteração de código, prompts                                 |
| Coleta de dados do território              | Temperatura, chuva, resíduos, buracos — alimenta a Comunidade Virtual |
| Desplugadas (_Computer Science Unplugged_) | Lógica e algoritmos sem computador                                    |
| Valores e temas transversais               | Racismo, violência contra a mulher, identidade, povos originários     |
| Competição ao vivo                         | **Quiz ao Vivo** entre equipes na aula presencial                     |
| Culminância                                | Apresentação da **criação original** do jogador ou da equipe          |

### Criações originais dos jogadores

**Definição vigente — toda trilha desemboca em criação original.** A culminância de cada
trilha é a apresentação pública de algo **criado pelo jogador (ou pela equipe) a partir do
conteúdo aprendido**: a versão própria do robô, um artefato remixado, um trecho de código
alterado, uma ideia nova sobre o que a trilha ensinou. A criação original distingue quem
**aprendeu** de quem apenas **executou**.

- **Autoria sempre creditada** — a criação carrega o nick do autor (ou dos autores) por toda
  a vida do registro, pela mesma razão que vale para a coleta de dados.
- **Vitrine pública** — as criações de jogadores autorizados compõem o portfólio público.
- Em **equipe**, o crédito é da equipe **e** de cada membro, com o papel que teve.
- A criação original **pontua e rende badge de autoria**.

> **A definir:** valor em pontos da criação original e critérios do badge de autoria.

### Desafios extras propostos por Apoiadores

Além dos desafios semanais dos Mestres, **Apoiadores podem propor desafios extras** ao longo
de um ciclo, sempre vinculados a uma trilha em andamento, com **recompensa custeada pelo
proponente** e **pontos extras** computados isoladamente. Existem duas modalidades — **aberto**
(a todos os jogadores da trilha) e **direcionado** (a um jogador específico, mediante
justificativa registrada do vínculo). Todo desafio extra exige **validação pedagógica do
Mestre da trilha e aprovação de um Admin**, recompensa **provida antes da publicação** e
**nenhum contato direto** entre Apoiador e jogador.

> Regras completas, mecânica no ciclo e rastreio de efetividade: documento 04.

### Resultados de atividade (lançados pela gestão)

- **Realizada**
- **Realizada com mérito**
- **Mérito extra por auxílio aos colegas** — colaborar vale mais que competir.

### Pontuação negativa

Está prevista pontuação negativa por mau comportamento, agressões verbais ou físicas e
descumprimento de regras. É a aplicação prática do código de conduta e dos valores do projeto.

### Condição de existência da atividade

> **Cada atividade só acontece se tiver os recursos necessários providos por Mestre ou
> Apoiador** (hora-aula, lanche, recompensas, insumos).

## 5. Equipes

**Definição vigente.** Equipes são **grupos livres de até 5 pessoas**, formados de maneira
espontânea pelos jogadores:

- Cada jogador pode participar de **uma ou mais equipes** e **pontua em todas as atividades
  em que participar e colaborar**.
- As equipes são **cadastradas pelo Admin na App 03**, conforme o plano de aulas e a formação
  livre dos jogadores.
- A composição segue o que a **atividade, o desafio ou a batalha determinar**: só jogadores
  **ou** com **no máximo 1 familiar, de 17 anos ou mais**.

**A equipe mistura idades.** É o principal instrumento do jogo para transformar a diferença
de idades (6 a 16 anos) em força:

- As equipes **misturam idades e níveis deliberadamente**. A progressão individual segue por
  nível de dificuldade; é a convivência que é heterogênea de propósito.
- **Cada membro tem papel ativo** — quem constrói, quem registra, quem apresenta, quem
  media — e os papéis giram entre as atividades.
- Jogadores **mais velhos ou mais avançados mediam os mais novos**: exercício prático do
  "colaborar vale mais que competir" e primeiro degrau do caminho de multiplicador.
- **O crédito individual é preservado**: a realização é da equipe, e o registro guarda o
  papel de cada membro.

## 6. Batalhas

**Batalhas são disputas de ideias e realizações entre os Jogadores** — competições saudáveis
que dão visibilidade ao que foi aprendido e construído:

- **Presenciais** (ex.: Batalha de Laser; batalhas de rima, em ciclo futuro).
- **De projetos e ideias** (apresentação de trabalhos, culminância).

Os resultados alimentam o ranking e o portfólio público dos jogadores.

## 7. Níveis e badges

A progressão vai do **Nível 1** (inscrito e assíduo) ao **Nível 5 — Mestre Aprendiz**, que
deixa o jogador **apto ao treinamento de multiplicador** e ao voluntariado nos pontos de
apoio. Duas regras estruturais:

- **Níveis e badges são por trilha ou por poder, nunca globais** — um jogador pode ser Mestre
  Aprendiz no Robô Educa e estar no Nível 2 na Batalha de Laser.
- Ser Mestre Aprendiz **não** equivale a ser Mestre: o reconhecimento como Mestre continua
  dependendo de cadastro por Admin e de habilidade comprovada por artefatos publicados.

> Critérios de cada nível, catálogo de badges e tabela de pontuação: documento 11.

## 8. Recompensas

**Regra vigente:** à medida que avançam nas trilhas, os jogadores **acumulam pontos, e esses
pontos podem ser trocados por recompensas**. É o que fecha o vínculo entre o jogo e a vida
real: o esforço de aprender converte-se em algo concreto na mão do jogador.

Catálogo inicial — **valores ainda são sugestão, a definir**:

| Recompensa                | Custo em pontos (a definir) |
| ------------------------- | --------------------------- |
| Kit alimentos 1 (3 itens) | 20                          |
| Kit alimentos 2 (6 itens) | 20                          |

**[Proposta]** Ao definir a tabela, ampliar o catálogo com recompensas não alimentares
(material escolar, componentes de robótica, ingressos culturais). A troca de pontos por
alimento é socialmente sensível e deve ser tratada com dignidade, no espírito do **"sem
miséria"** baiano: a recompensa celebra a conquista do jogador; nunca pode soar como
assistencialismo.

## 9. Manual do Jogador (fluxo de entrada)

1. **Cadastro livre** — sem autorização de responsável. Informe apenas nome, data de
   nascimento (ou idade), nick e características do avatar; sua Comunidade Virtual já vem
   definida pela gestão. O cadastro pode ser feito por **voz ou chat**, com apoio de IA.
2. (Se houver kit) **Receba e monte seu robô, e personalize-o.**
3. **Acesse a plataforma.**
4. **Escolha um Poder.**
5. **Siga uma Trilha** — e receba o **livro de apoio** que passa a ser seu.
6. **Monte equipes** — grupos livres de até 5 pessoas; você pode estar em mais de uma.
7. **Realize os desafios semanais** (on-line, presenciais, em equipe, em equipe com familiar).
8. **Registre dados da sua comunidade** — a coleta rende pontos **enquanto você a mantiver**.
9. **Crie algo seu a partir do que aprendeu e apresente** — toda trilha termina com uma
   criação original, com o seu crédito de autoria.
10. **Troque seus pontos por recompensas.**
11. **Peça ajuda para as atividades escolares** ao robô assistente.
12. **Autorização dos pais ou responsáveis** — necessária apenas para que o **histórico e o
    perfil sejam divulgados publicamente**. Sem ela, o jogador participa normalmente, mas não
    aparece na vitrine nem nos rankings. A autorização é dada — e revogada — na App 07.

**[Proposta]** Modelar o estado do jogador em dois níveis: **"ativo"** (cadastro livre,
participa de tudo) e **"público"** (com autorização do responsável, aparece na vitrine).
