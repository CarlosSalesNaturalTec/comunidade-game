# 02 — Conceito do Jogo e Gamificação

O Comunidade Game é um "jogo" cuja partida acontece na vida real: aprender, criar, ajudar
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
- Pode montar **Equipes** e participar de **Batalhas**.

O jogador é a **única persona com autocadastro** na plataforma
([03 §5](03-plataforma-e-arquitetura.md#5-frontend-03--onboarding-cadastro-e-registro-de-presença)).

### Admins (Organizadores / Equipe técnica)
Responsáveis pela operação da plataforma e pela logística dos eventos. Editam as seções
institucionais ("Quem somos", "Contatos"), fazem os lançamentos de atividades e
**cadastram Mestres e Apoiadores**.

Regras de admissão:

- O **fundador é o primeiro Admin** da plataforma.
- **Novos Admins são incluídos manualmente** por um Admin existente. Não existe
  autocadastro nem solicitação aberta de acesso administrativo.

### Mestres (persona secundária)
Especialistas/mentores nas áreas de tecnologia, artes e esportes que orientam e ministram
oficinas. Regras de admissão:

- **Todo Mestre é cadastrado exclusivamente pelos Admins da plataforma.** Não há
  autocadastro de Mestres.
- Todo Mestre **tem que ter pelo menos uma habilidade** declarada.
- A habilidade precisa estar **comprovada por materiais ou artefatos disponibilizados na
  plataforma** — aulas presenciais e/ou gravadas, atividades propostas, vídeo-aulas,
  exemplos de código, projetos construídos. A prova é pública e verificável por qualquer
  visitante.
- Mestres também proveem recursos para atividades (ver
  [04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).

> **Exemplo de referência — o Mestre fundador.** É considerado mestre em Programação e
> Robótica porque **construiu o software da plataforma**, propõe as atividades que os
> jogadores realizam e publica conteúdo (vídeo-aulas, exemplos de código). Suas
> atividades-modelo são o [Robô Educa](06-robo-educa.md) e a
> [Batalha de Laser](07-batalha-de-laser.md).

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
realidade**. Ela não vem pronta: **é construída pelo próprio jogador**, à medida que ele
registra dados reais do lugar onde mora.

> Uma Comunidade Virtual **existe na medida em que são registrados dados reais** do
> território.

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

**Para que serve.** Os dados captados **podem ser usados como insumo para tomada de
decisões** — pela própria comunidade, por associações de moradores, escolas, poder público
e pesquisas. O objetivo é que a plataforma se torne uma **central *Data Driven* das
comunidades onde está presente**: quem mora ali passa a ter evidência, não só percepção.

**Por que isso é educativo.** Alimentar a Comunidade Virtual é, em si, aprendizado de
ciência de dados, método científico, cidadania e meio ambiente — e conecta o jogo ao valor
de **território e identidade**
([01-visao-valores-e-proposito.md](01-visao-valores-e-proposito.md#3-valores-e-causas)).

**[Proposta]** Transformar o registro de dados da comunidade em um poder próprio
("Poder do Território"), com desafios de coleta periódica e um painel público por
comunidade, aberto a moradores e instituições.

## 2. Poderes (habilidades)

Catálogo inicial previsto:

| Poder | Descrição |
|---|---|
| **Poder da IA e Robótica** | Programação, eletrônica, robótica e IA — conteúdos do primeiro Mestre. Atividades-modelo: [Robô Educa](06-robo-educa.md) e [Batalha de Laser](07-batalha-de-laser.md) |
| **Poder da Rima** | Expressão artística — rima, rap, batalhas de rima |
| **Poder das Redes** | Produção de conteúdo / "Monte seu Canal" — comunicação digital |
| **Poder da Capoeira** | Cultura e movimento; com componente tecnológico: modelo de ML (TensorFlow) para análise de movimentos — contador de polichinelos e de movimentos executados com sucesso |
| **Poder Econômico** | O quanto Mestres e Apoiadores investiram na plataforma (tempo, recursos etc.) — o poder dos provedores |
| **Outros conteúdos PNED / BNCC** | Alinhamento com políticas educacionais (Política Nacional de Educação Digital e Base Nacional Comum Curricular) |
| **Soft Skills** | Habilidades socioemocionais |

Regras dos poderes:

- Jogador ganha pontos de um poder **apenas realizando as atividades propostas pelos
  Mestres** daquele poder.
- A **ativação/desbloqueio** de poderes acontece por meio de **quiz ou desafios**.
- Todo poder, mesmo o mais técnico, deve abrir **paralelos com outras áreas do
  conhecimento e com os valores do projeto**
  ([01 §4](01-visao-valores-e-proposito.md#4-objetivos)).

**[Proposta]** Poderes alinhados aos valores do projeto: "Poder da Ancestralidade"
(cultura afro-brasileira e povos originários), "Poder do Cuidado" (respeito, combate ao
racismo e à violência de gênero, mediação de conflitos), "Poder do Território" (dados da
comunidade). Assim as causas viram conteúdo jogável, não apenas declaração de princípios.

## 3. Trilhas

- O aluno é **guiado pelos conhecimentos desejados**: cada trilha é uma sequência de
  conteúdos e atividades.
- Ao seguir os pontos da trilha, o jogador vai **adquirindo/desbloqueando
  habilidades/poderes**.
- Trilhas de conhecimento com cadência **mensal**.
- Quanto mais usa a plataforma e realiza atividades/desafios, mais pontos acumula.
- Trilhas podem ser **próprias ou de terceiros** (conteúdos externos curados pelos Mestres).

## 4. Atividades e desafios

**Regra vigente:** as atividades devem ser criadas com **níveis de dificuldade graduais**,
acessíveis por todos os alunos/jogadores **independentemente de sua idade** (faixa de 6 a
16 anos). O jogador progride pelo nível de dificuldade que consegue realizar, não pela
idade que tem.

### Tipos de aula
- **Presenciais com treinamento** (oficinas) — roteiro em
  [05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial).
- **Presenciais para apresentação de trabalhos** (culminância).
- **Assíncronas / on-line**: conteúdo dos desafios e conteúdo entre encontros presenciais.

### Tipos de desafio e pontuação

| Tipo de desafio | Pontos |
|---|---|
| Atividades on-line | 10 |
| Atividades presenciais | 10 |
| Atividades em equipe | 10 |
| Atividades em família | 20 |

- Os desafios são **semanais**.
- A atividade em família vale mais: o engajamento da família é estratégico para a
  permanência da criança no projeto.

### Categorias de atividade

| Categoria | Exemplos |
|---|---|
| Construção / making | Robô Educa, artefatos da Batalha de Laser |
| Programação e IA | Quizzes, alteração de código, prompts |
| Coleta de dados do território | Temperatura, chuva, resíduos, buracos — alimenta a Comunidade Virtual |
| Desplugadas (Computer Science Unplugged) | Lógica e algoritmos sem computador |
| Valores e temas transversais | Racismo, violência contra a mulher, identidade, povos originários |
| Culminância | Apresentação livre do que foi construído/aprendido |

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

## 6. Batalhas

**Batalhas são disputas de ideias e realizações entre os Jogadores** — competições
saudáveis que dão visibilidade ao que foi aprendido e construído. Podem ser:

- Presenciais (ex.: [Batalha de Laser](07-batalha-de-laser.md), batalhas de rima).
- De projetos/ideias (apresentação de trabalhos, culminância).

Os resultados das batalhas alimentam o ranking e o portfólio público dos jogadores.

## 7. Níveis e badges (gamificação)

| Nível | Critério |
|---|---|
| Nível 1 | Inscrito na oficina e assíduo |
| Nível 2 | Bom rendimento |
| Nível 3 | Ótimo rendimento |
| Nível 4 | Apoio aos colegas nas aulas |
| Nível 5 | Instrutor |

Observações:

- A progressão culmina em **Instrutor**: o jogador que chega ao topo passa a ensinar —
  é a engrenagem de formação de multiplicadores
  ([05-implantacao-e-operacao.md](05-implantacao-e-operacao.md#6-formação-de-mestres-e-multiplicadores)).
  O reconhecimento como **Mestre** na plataforma, contudo, continua dependendo de cadastro
  por um Admin e de habilidade comprovada por artefatos publicados.
- **Badges** representam poderes e conquistas, e aparecem nos cards públicos dos jogadores
  ([03-plataforma-e-arquitetura.md](03-plataforma-e-arquitetura.md)).

## 8. Recompensas

Os pontos podem ser trocados por recompensas concretas:

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
("sem miséria").

Prêmios também aparecem no orçamento como **consumíveis** e **duráveis**
([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md#3-despesas-para-funcionamento)).

## 9. Manual do Jogador (fluxo de entrada)

1. **Cadastro livre** — o primeiro acesso não exige autorização de responsável. Informe
   apenas: **nome do jogador, data de nascimento (ou idade), nick e características do
   avatar**. A partir daí o jogador já pode participar das atividades. O cadastro pode ser
   feito por **voz ou chat**, com apoio de IA
   ([03 §5](03-plataforma-e-arquitetura.md#5-frontend-03--onboarding-cadastro-e-registro-de-presença)).
2. (Se houver kit) **Receba/monte seu robô e personalize-o** — [Robô Educa](06-robo-educa.md).
3. **Acesse a plataforma.**
4. **Escolha um Poder.**
5. **Siga uma Trilha.**
6. **Monte equipes** (mistas de até 5 membros, ou Equipe Familiar).
7. **Realize os desafios semanais** (on-line, presenciais, em equipe, em família).
8. **Registre dados da sua comunidade** e ajude a construir sua Comunidade Virtual.
9. **Troque seus pontos por recompensas.**
10. **Peça ajuda para a realização de atividades escolares** (apoio escolar pela
    plataforma/robô assistente).
11. **Autorização dos pais ou responsáveis** — necessária apenas para que o **histórico e
    o perfil do jogador sejam divulgados na plataforma** (vitrine, rankings públicos).
    Sem ela, o jogador continua participando normalmente, mas seus dados não são exibidos
    publicamente.

**[Proposta]** Modelar o estado do jogador em dois níveis: **"ativo"** (cadastro livre,
participa de tudo) e **"público"** (com autorização do responsável, aparece na vitrine e
nos rankings).
