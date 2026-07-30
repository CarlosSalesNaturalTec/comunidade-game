# 11 — Modelo de Gamificação Integrado

> **Fonte única do motor do jogo.** Este documento formaliza como os elementos do
> Comunidade Game — trilhas, conteúdos, atividades, desafios, encontros presenciais,
> batalhas, culminâncias, pontuações, níveis, badges e recompensas — se compõem entre si,
> e como tudo isso se reflete na **Vitrine Pública**, nos **cards dos personagens**, na
> **representação visual das Comunidades Virtuais** e nos **jogos construídos sobre o
> backend** da plataforma.
>
> O conceito de cada elemento está em
> [02-conceito-do-jogo-e-gamificacao.md](02-conceito-do-jogo-e-gamificacao.md); aqui está
> a **mecânica que os liga** e a
> [matriz de rastreabilidade](#9-matriz-de-rastreabilidade--prds) que alimenta os PRDs
> ([08-base-para-prds.md](08-base-para-prds.md)).

## 1. Visão geral do motor

O motor do jogo é um único fluxo, que vale para qualquer poder e qualquer área do
conhecimento:

```
                      ┌──────────────────────────────────────────────┐
                      │                  TRILHA                      │
                      │  conteúdo → atividades → desafios → marcos   │
                      └──────────────────┬───────────────────────────┘
                                         │ realização registrada
                                         ▼
                      ┌──────────────────────────────────────────────┐
                      │                  PONTOS                      │
                      │  regulares · recorrentes (coleta) · extras   │
                      └──────────────────┬───────────────────────────┘
                                         │ acumulação por trilha/poder
                                         ▼
                ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
                │  NÍVEIS 1–5   │  │    BADGES     │  │  RECOMPENSAS  │
                │ (progressão)  │  │ (conquistas)  │  │ (troca/extra) │
                └───────┬───────┘  └───────┬───────┘  └───────┬───────┘
                        └──────────────────┼──────────────────┘
                                           ▼
                      ┌──────────────────────────────────────────────┐
                      │          REFLEXOS NO ECOSSISTEMA             │
                      │  Vitrine · cards · Comunidade Virtual visual │
                      │  · App 04 e jogos sobre o backend            │
                      └──────────────────────────────────────────────┘
```

Regras estruturais do fluxo:

1. **Só a realização gera pontos.** Pontos nascem exclusivamente de atividades e desafios
   propostos por Mestres e da coleta de dados do território — nunca de presença passiva e
   nunca de dentro do jogo digital
   ([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)).
2. **A acumulação é por trilha/poder**, não global: níveis e badges são conquistados no
   conteúdo específico em que o jogador se destacou
   ([02 §7](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação)).
3. **Todo reflexo público é derivado, nunca editado à mão**: o que aparece na vitrine, nos
   cards e nos painéis é leitura do mesmo motor — uma única fonte de verdade no backend
   (PRD-01).

## 2. Anatomia da trilha

**A trilha é a unidade de organização do aprendizado.** O modelo abaixo é **agnóstico de
área do conhecimento**: vale para uma trilha técnica ([Robô Educa](06-robo-educa.md)),
para uma trilha de cultura e movimento (Capoeira), de expressão artística (Rima) ou de
qualquer outra área — inclusive humanas. O que muda de uma área para outra é o conteúdo e o
que se mede na coleta de dados; a estrutura é a mesma.

### 2.1 Do que uma trilha é composta

```
TRILHA (autoria de um Mestre, vinculada a um Poder)
│
├── PONTOS DE TRILHA (sequência ordenada, com dificuldade gradual)
│     └── cada ponto contém:
│           ├── CONTEÚDO — próprio do Mestre, de terceiros (curado) e
│           │   bibliografia de apoio (título/capítulo do acervo)
│           ├── ATIVIDADES — o que o jogador realiza para aprender
│           └── DESAFIO DE DESBLOQUEIO — quiz ou desafio que abre o
│               próximo ponto e os níveis do poder
│
├── DESAFIO(S) DE COLETA DE DADOS REAIS — obrigatório em toda trilha
│     └── série temporal com cadência; pontua enquanto ativa
│
├── DESAFIOS EXTRAS — propostos por Apoiadores, vinculados à trilha
│     └── abertos a todos ou direcionados a um jogador específico
│
└── MARCOS — eventos que pontuam o percurso no calendário do ciclo
      ├── ENCONTROS PRESENCIAIS — dinâmica assíncrona; é onde as
      │   atividades presenciais da trilha acontecem
      ├── BATALHA — quando a trilha prevê uma disputa (opcional)
      └── CULMINÂNCIA — apresentação pública do que foi construído;
          é o ponto final de toda trilha
```

| Componente | O que é | Definição-fonte |
|---|---|---|
| **Ponto de trilha** | Menor unidade de progressão: conteúdo + atividades + desafio de desbloqueio | [02 §3](02-conceito-do-jogo-e-gamificacao.md#3-trilhas) |
| **Conteúdo** | Material do Mestre, conteúdo de terceiros curado e bibliografia de apoio por ponto (título/capítulo) | [02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut) |
| **Atividade** | O que o jogador realiza — classificada pela taxonomia da [§4](#4-taxonomia-de-atividades-e-desafios) | [02 §4](02-conceito-do-jogo-e-gamificacao.md#4-atividades-e-desafios) |
| **Desafio de desbloqueio** | Quiz ou desafio que abre o próximo ponto e ativa níveis do poder | [02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades) |
| **Desafio de coleta** | Série temporal de dados reais do território; requisito de **toda** trilha | [02 §3](02-conceito-do-jogo-e-gamificacao.md#regra-vigente-toda-trilha-coleta-dados-reais) |
| **Desafio extra** | Proposto por Apoiador, validado pelo Mestre e aprovado por Admin; pontos extras isolados | [04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras) |
| **Encontro presencial** | Marco recorrente; roteiro assíncrono com momentos coletivos âncora | [05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial) |
| **Batalha** | Disputa de ideias e realizações; marco opcional, previsto pela trilha | [02 §6](02-conceito-do-jogo-e-gamificacao.md#6-batalhas) |
| **Culminância** | Apresentação pública do construído/aprendido; **ponto final de toda trilha** | [02 §4](02-conceito-do-jogo-e-gamificacao.md#categorias-de-atividade) |

### 2.2 O modelo aplicado — três exemplos

A tabela valida a estrutura contra as duas trilhas existentes e contra uma trilha de área
não técnica (Capoeira, ciclo futuro), mostrando que o modelo não pressupõe tecnologia:

| Componente | Robô Educa (técnica) | Batalha de Laser (técnica) | Capoeira (cultura e movimento — ciclo futuro) |
|---|---|---|---|
| Conteúdo | Montagem, voz, prompts, código ([06 §4](06-robo-educa.md#4-pontos-da-trilha-poder-da-ia-e-robótica)) | Eletrônica, sensores, MQTT, lógica ([07](07-batalha-de-laser.md#integração-com-a-plataforma-proposta)) | História da capoeira, ritmo, movimentos, roda |
| Atividades práticas | Montar e personalizar o robô | Construir atacante, escudo e torre | Treinar sequências de movimentos, tocar instrumentos |
| Desafio de desbloqueio | Quiz com o próprio robô | Testar o artefato construído | Executar a sequência diante do Mestre |
| Coleta de dados reais | Registro por voz (temperatura, ocorrências) | Sensor de território construído pelo jogador (LDR → iluminação pública) | Registro dos espaços, rodas, mestres e memórias do bairro |
| Batalha | — (apresentação) | **Batalha de Laser** presencial | Roda / jogo de capoeira entre equipes |
| Culminância | Publicar e apresentar sua versão do robô | Partida final com telemetria no telão | Apresentação da roda para a comunidade |

### 2.3 Distribuição da trilha pelas etapas do ciclo

Toda trilha é **paginada no calendário de um ciclo** (o período letivo da comunidade, ex.:
[Ciclo 01](10-case-01-guerreira-zeferina.md)). O modelo de distribuição é o mesmo para
qualquer trilha:

| Etapa do ciclo | O que acontece | Conteúdo e material |
|---|---|---|
| **Abertura** | Onboarding e credenciamento; escolha do poder; **ritual de entrada na trilha** — a entrega do livro próprio (linha doada) é a primeira atividade pontuada; abertura das séries de coleta de dados | Ponto 1 da trilha; livro próprio entregue; kit/insumos da primeira montagem |
| **Desenvolvimento** | Encontros presenciais (assíncronos) avançando os pontos da trilha + desafios on-line entre encontros; séries de coleta rendendo pontos de forma recorrente; desafios extras de Apoiadores entram aqui | Pontos intermediários; **capítulo recomendado por ponto** (bibliografia de apoio); acervo permanente em bancada |
| **Marcos** | Batalha(s), quando a trilha prevê; Quiz ao Vivo nos encontros | Artefatos construídos no desenvolvimento |
| **Fechamento** | **Culminância** (apresentação pública), conferência de inventário do acervo, avaliação do ciclo e das hipóteses | Portfólio, vídeos (com consentimento), prestação de contas |

Diretrizes de paginação para o Mestre (autor da trilha):

- **O ritual de abertura não se adia**: livro próprio na mão e série de coleta aberta já na
  primeira etapa — é o que dá ao jogador material de trabalho e pontuação recorrente desde
  o primeiro dia.
- **Um ponto de trilha por encontro é o passo de referência**, mas a dinâmica assíncrona
  permite que cada jogador/equipe esteja em pontos diferentes
  ([05 §3](05-implantacao-e-operacao.md#definição-vigente-o-encontro-é-assíncrono)) — a
  paginação orienta o planejamento de recursos (lastro), não o ritmo individual.
- **A bibliografia acompanha o ponto, não a trilha inteira**: cada ponto indica o
  título/capítulo que o aprofunda; o material escasso (acervo permanente) é usado em
  bancada na etapa em que o assunto está vivo.
- **Batalha depois da construção, culminância depois de tudo**: os marcos ficam na segunda
  metade do ciclo, quando há o que disputar e o que mostrar.
- **O fechamento é parte da trilha, não apêndice**: culminância pontua, alimenta o
  portfólio público e produz o material de avaliação do ciclo.

A aplicação concreta desse modelo ao Ciclo 01 (trilhas 1 e 2 + acervo Include) está em
[10 §5](10-case-01-guerreira-zeferina.md#51-proposta-distribuição-das-trilhas-e-do-acervo-no-ciclo-01).

## 3. Papéis no motor

| Persona | Papel no motor do jogo |
|---|---|
| **Jogador** | Percorre trilhas, realiza atividades e desafios, **produz criações originais** com autoria creditada ([02 §4](02-conceito-do-jogo-e-gamificacao.md#criações-originais-dos-jogadores)), acumula pontos/níveis/badges, troca pontos por recompensas e **propõe melhorias** para atividades e para a própria plataforma ([03 §7](03-plataforma-e-arquitetura.md#7-app-05--área-do-jogador)) |
| **Mestre** | Autor da trilha: define pontos, conteúdos, atividades, desafios e a paginação no ciclo; lança resultados; valida desafios extras. Mestres podem ser de **qualquer área do conhecimento** — exatas, humanas, artes, esportes, cultura — com habilidade comprovada por artefatos publicados |
| **Apoiador** | Provê lastro e propõe **desafios extras** (abertos ou direcionados); acompanha a efetividade do apoio |
| **Admin** | Aprova desafios extras, opera lançamentos e painéis, cria Comunidades Virtuais |
| **Comunidade Virtual** | Recebe os dados coletados; sua representação visual cresce com a participação ([§8.3](#83-representação-visual-da-comunidade-virtual)) |

## 4. Taxonomia de atividades e desafios

Toda atividade da plataforma é classificada em **três eixos ortogonais** — os três se
combinam livremente (uma atividade pode ser, por exemplo, *em equipe + presencial + de
construção*):

| Eixo | Valores | Observações |
|---|---|---|
| **Modalidade** | **Individual** · **Em equipe** (mista, até 5) · **Em família** (Equipe Familiar) | A modalidade define a pontuação-base ([§5](#5-motor-de-pontuação)); família vale mais por ser estratégica para a permanência |
| **Formato** | **Presencial** (nos encontros) · **On-line/assíncrona** (entre encontros) | O desafio de coleta é contínuo: atravessa os dois formatos |
| **Natureza** | Construção/making · Programação e IA · **Coleta de dados do território** · Desplugada · Valores e temas transversais · Competição ao vivo (Quiz) · Culminância · **Criação original** ([02 §4](02-conceito-do-jogo-e-gamificacao.md#criações-originais-dos-jogadores)) | Lista aberta: novas trilhas de outras áreas acrescentam naturezas (ex.: expressão artística, movimento e corpo) |

Regras transversais:

- **Dificuldade gradual, independente de idade** (faixa 6–16): o jogador progride pelo
  nível que consegue realizar
  ([02 §4](02-conceito-do-jogo-e-gamificacao.md#4-atividades-e-desafios)).
- **Lastro**: nenhuma atividade acontece sem os recursos providos
  ([04 §1](04-modelo-economico-e-sustentabilidade.md#1-a-economia-de-recursos-da-plataforma)).
- **Resultado lançado pela gestão**: realizada / realizada com mérito / mérito extra por
  auxílio aos colegas ([02 §4](02-conceito-do-jogo-e-gamificacao.md#resultados-de-atividade-lançados-pela-gestão)).

## 5. Motor de pontuação

Tabela única das fontes de pontos da plataforma:

| Fonte | Pontos | Tipo | Quem lança |
|---|---|---|---|
| Desafio semanal — atividade on-line | 10 | Regular | Mestre/gestão |
| Desafio semanal — atividade presencial | 10 | Regular | Mestre/gestão |
| Desafio semanal — atividade em equipe | 10 | Regular | Mestre/gestão |
| Desafio semanal — atividade em família | 20 | Regular | Mestre/gestão |
| **Coleta de dados do território** | A definir por tipo de coleta | **Recorrente** — pontua a cada registro válido enquanto a série está ativa; interrompeu, parou de render ([02 §1](02-conceito-do-jogo-e-gamificacao.md#registro-temporal-e-pontuação-enquanto-a-coleta-durar)) | Automático (registro do jogador) |
| **Quiz ao Vivo** | A definir | Regular | Automático (partida) |
| Mérito extra por auxílio aos colegas | A definir | Regular | Mestre/gestão |
| **Criação original** — culminância da trilha com autoria creditada | A definir | Regular | Mestre/gestão ([02 §4](02-conceito-do-jogo-e-gamificacao.md#criações-originais-dos-jogadores)) |
| Badge de conduta (ex.: Guardião do Acervo) | Pontos + badge | Regular | Mestre/gestão |
| **Desafio extra de Apoiador** (aberto ou direcionado) | Definidos no desafio | **Extra** — computado isoladamente, não se mistura à pontuação regular da trilha | Automático na conclusão validada |
| **Batalha** (resultado/estatísticas) | A definir por batalha | Regular | Automático (ex.: ponte Nexus → API) ou gestão |
| Pontuação negativa (má conduta) | Negativo, a definir | Regular | Admin/gestão, conforme [Código de Conduta](13-codigo-de-conduta-versao-previa.md) |

Três naturezas de saldo, que nunca se confundem:

| Saldo | O que é | Regra |
|---|---|---|
| **Pontos regulares** | Da progressão nas trilhas/poderes | Alimentam níveis, ranking e troca por recompensas |
| **Pontos extras** | De desafios extras de Apoiadores | Computados isoladamente; rastreados no histórico do Apoiador (efetividade) |
| **Pontos consumidos** | Débitos por troca de recompensa e por uso dentro do App 04 | O jogo **só debita, nunca credita** ([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)) — pontos gastos não afetam níveis nem badges já conquistados |

> **A definir** ([09 §1](09-topicos-em-aberto-e-sugestoes.md#1-decisões-pendentes)):
> valores da coleta por tipo, do Quiz ao Vivo, dos méritos, da criação original e da
> pontuação negativa; janela de tolerância e teto da coleta; mecânica antifraude.

## 6. Níveis

Progressão **por trilha/poder** (nunca global), destravada por quiz/desafio:

| Nível | Critério | O que destrava |
|---|---|---|
| 1 | Inscrito e assíduo | Participação nas atividades |
| 2 | Bom rendimento | — |
| 3 | Ótimo rendimento | — |
| 4 | Apoio aos colegas | — |
| **5** | **Mestre Aprendiz** | Apto ao treinamento de multiplicador e ao voluntariado no ponto de apoio ([05 §7](05-implantacao-e-operacao.md#7-formação-de-mestres-e-multiplicadores)) |

O Nível 5 é a engrenagem de escala do projeto: o jogador que chega ao topo volta como
multiplicador. Ser Mestre Aprendiz **não** equivale a ser Mestre — o reconhecimento como
Mestre exige cadastro por Admin e habilidade comprovada por artefatos
([02 §1](02-conceito-do-jogo-e-gamificacao.md#1-os-elementos-do-jogo-personas)).

## 7. Badges

Catálogo por tipo — badges representam poderes e conquistas e são um dos principais
elementos exibidos nos cards públicos ([§8.2](#82-cards-dos-personagens)):

| Tipo | Exemplos | Como se conquista |
|---|---|---|
| **De nível** | Badge do poder no nível alcançado | Progressão da [§6](#6-níveis) |
| **De conquista** | **Mestre Aprendiz** (por trilha ou poder) · **Guardião do Acervo** | Conclusão do Nível 5 · cuidado com o material comum ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)) |
| **De valores/causas** | Participação em atividades ligadas às causas do projeto ([01 §3](01-visao-valores-e-proposito.md#3-valores-e-causas)) | Atividades de natureza "valores e temas transversais" |
| **De território** | Progressão no **Poder do Território** — séries de coleta sustentadas | Manutenção de séries ativas ([02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)) |
| **De autoria/criação** | Badge de autoria — criações originais apresentadas em culminância | Criação original validada pelo Mestre ([02 §4](02-conceito-do-jogo-e-gamificacao.md#criações-originais-dos-jogadores)) |

Regra geral: **badge é por trilha ou por poder, não global** — um jogador pode ser Mestre
Aprendiz no Robô Educa e estar no Nível 2 na Batalha de Laser.

## 8. Reflexos no ecossistema

Tudo o que o motor produz (pontos, níveis, badges, resultados, séries de coleta) é lido —
nunca reescrito — pelas quatro superfícies públicas do ecossistema.

### 8.1 Vitrine Pública (App 06)

| Elemento do motor | Como aparece na vitrine |
|---|---|
| Jogadores (com autorização do responsável) | **Cards rotativos** (rotação a cada 5 s) — composição em [§8.2](#82-cards-dos-personagens) |
| Poderes | Seção de poderes, com trilhas e Mestres de cada um |
| Trilhas e realizações | Portfólio público dos jogadores autorizados |
| **Criações originais** | Portfólio de autoria: a criação exposta com o nick do autor (ou dos autores, em equipe) ([02 §4](02-conceito-do-jogo-e-gamificacao.md#criações-originais-dos-jogadores)) |
| **Batalhas** | Resultados e estatísticas de partida (ex.: telemetria do Nexus) alimentando ranking e portfólio |
| **Culminâncias** | Vídeos e registros (com consentimento específico registrado na App 07) |
| Comunidades Virtuais | **Painel público por comunidade em série histórica**, com dados agregados e anonimizados |
| Mestres | Cards com os **artefatos que comprovam a habilidade** — de qualquer área do conhecimento |
| Apoiadores | Poder Econômico e desafios extras propostos, com as realizações que o apoio produziu |
| Rankings | Somente pontos regulares (aprendizado e realização); jogadores sem autorização não aparecem |

### 8.2 Cards dos personagens

Composição de cada card público — o card é a "carta do personagem" do universo do jogo, e a
mesma composição serve de base para o App 04 ([§8.4](#84-jogos-sobre-o-backend-app-04-e-terceiros)):

| Card | O que exibe | O que **nunca** exibe |
|---|---|---|
| **Jogador** | Avatar, nick, badges, poderes adquiridos com níveis, desempenho na plataforma e **criações originais** do portfólio | Imagem real, nome civil, redes sociais, qualquer canal de contato (LGPD/proteção de menores) |
| **Mestre** | Nome/identidade, área(s) de habilidade, artefatos comprobatórios, trilhas de autoria | — |
| **Apoiador** | Identidade, Poder Econômico, desafios extras propostos e efetividade (agregada, por avatar) | Dados de contato de jogadores |
| **Comunidade Virtual** | Nome, território, representação visual ([§8.3](#83-representação-visual-da-comunidade-virtual)), séries ativas, nº de jogadores vinculados | Granularidade que permita inferir endereço de criança |

### 8.3 Representação visual da Comunidade Virtual

A Comunidade Virtual "ganha corpo" visualmente na medida da participação — o mapeamento
entre dado registrado e elemento visual é requisito de produto (PRD-08 e PRD-03):

| O que acontece no motor | Reflexo visual na comunidade |
|---|---|
| Comunidade criada por Admin | Território **vazio** — nome e contorno, sem preenchimento |
| Primeira série de coleta aberta | O tipo de dado ganha presença no painel (ex.: termômetro, pluviômetro, mapa de vias) |
| Registros acumulados em série ativa | O elemento visual **cresce/ganha detalhe**: série histórica visível, granularidade (comunidade → bairro → rua → condomínio → bloco → quadra) preenchida |
| Série interrompida | Elemento permanece (dados são permanentes), sinalizado como série inativa |
| Fotos e memórias registradas | Galeria/linha do tempo dos pontos de referência do território |
| Jogadores vinculados ativos | Indicador de vitalidade da comunidade (agregado, sem expor indivíduos) |

Princípios: o visual **representa dados reais, nunca decoração** (a comunidade existe na
medida em que registra dados —
[02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)); a saída pública é
sempre **agregada e anonimizada**
([03 §10](03-plataforma-e-arquitetura.md#10-proteção-de-dados-em-toda-a-plataforma-lgpd)).

### 8.4 Jogos sobre o backend (App 04 e terceiros)

Contrato entre o motor e qualquer jogo construído sobre a plataforma:

| O jogo pode | O jogo não pode |
|---|---|
| **Ler** o progresso do jogador: avatar, poderes, badges, níveis | **Creditar** pontos — não existe endpoint de crédito para jogos |
| **Debitar** pontos (consumo declarado dentro do jogo) | Alterar níveis, badges ou histórico |
| Usar os cards ([§8.2](#82-cards-dos-personagens)) como base dos personagens | Exibir imagem real ou dados pessoais do jogador |

- O que se conquista aprendendo **desbloqueia e alimenta** o que o jogador pode fazer no
  jogo; jogar muito não sobe ninguém no ranking — e a ausência de endpoint de crédito
  elimina, por construção, a fraude por automação
  ([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)).
- **Batalhas físicas seguem o mesmo padrão de integração**: a ponte **Nexus → API** da
  [Batalha de Laser](07-batalha-de-laser.md#integração-com-a-plataforma-proposta) envia as
  estatísticas da partida (MVP, tiros, defesas, penalidades) para a API, que **lança a
  atividade realizada** — o crédito de pontos é da atividade validada, não do jogo. É o
  modelo de referência para qualquer jogo/batalha presencial futura, de qualquer área.
- A API pública e aberta permite que **terceiros** construam novos jogos sob o mesmo
  contrato ([03 §1](03-plataforma-e-arquitetura.md#1-princípios-de-arquitetura)).
- **O protagonismo dos jogadores vale também aqui**: o código do App 04 é aberto e legível,
  alterá-lo é atividade de trilha
  ([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)) — o jogador não é
  só usuário do jogo, é um dos seus construtores, e a plataforma está sempre em evolução
  com essa participação ([01 §3](01-visao-valores-e-proposito.md#3-valores-e-causas)).

## 9. Matriz de rastreabilidade → PRDs

Cada conceito do motor, onde está definido e quais PRDs o implementam
([08-base-para-prds.md](08-base-para-prds.md)):

| Conceito | Definição | PRDs |
|---|---|---|
| Trilha e pontos de trilha (anatomia, [§2](#2-anatomia-da-trilha)) | [02 §3](02-conceito-do-jogo-e-gamificacao.md#3-trilhas) + este doc | PRD-01, PRD-09, PRD-05 |
| Conteúdo e bibliografia por ponto | [02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-e-kits-mdf-goethe-institut) | PRD-09, PRD-07 |
| Atividades e taxonomia ([§4](#4-taxonomia-de-atividades-e-desafios)) | [02 §4](02-conceito-do-jogo-e-gamificacao.md#4-atividades-e-desafios) + este doc | PRD-01, PRD-02, PRD-05 |
| Desafios de desbloqueio | [02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades) | PRD-01, PRD-09, PRD-05 |
| Desafio de coleta (série temporal) | [02 §1](02-conceito-do-jogo-e-gamificacao.md#registro-temporal-e-pontuação-enquanto-a-coleta-durar) | PRD-01, PRD-08, PRD-05, PRD-06 |
| Desafios extras (abertos e direcionados) | [04 §5](04-modelo-economico-e-sustentabilidade.md#5-interação-apoiadores-x-jogadores-desafios-extras) | PRD-01, PRD-02, PRD-07, PRD-09 |
| Encontros presenciais (dinâmica assíncrona) | [05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial) | PRD-02, PRD-04, PRD-05 |
| Batalhas e telemetria | [02 §6](02-conceito-do-jogo-e-gamificacao.md#6-batalhas), [07](07-batalha-de-laser.md) | PRD-10, PRD-01 |
| Culminância | [02 §4](02-conceito-do-jogo-e-gamificacao.md#categorias-de-atividade), [05 §3](05-implantacao-e-operacao.md#momentos-do-encontro) | PRD-10, PRD-02, PRD-03 |
| Motor de pontuação ([§5](#5-motor-de-pontuação)) | [02 §4](02-conceito-do-jogo-e-gamificacao.md#tipos-de-desafio-e-pontuação) + este doc | PRD-01, PRD-02, PRD-05 |
| Níveis 1–5 / Mestre Aprendiz ([§6](#6-níveis)) | [02 §7](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação) | PRD-01, PRD-05 |
| Badges ([§7](#7-badges)) | [02 §7](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação) + este doc | PRD-01, PRD-03, PRD-05, PRD-12 |
| Recompensas e troca de pontos | [02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas) | PRD-01, PRD-05, PRD-07 |
| Vitrine e rankings ([§8.1](#81-vitrine-pública-app-06)) | [03 §8](03-plataforma-e-arquitetura.md#8-app-06--vitrine-pública-apresentação-da-plataforma) + este doc | PRD-03 |
| Cards dos personagens ([§8.2](#82-cards-dos-personagens)) | Este doc | PRD-03, PRD-12 |
| Representação visual da comunidade ([§8.3](#83-representação-visual-da-comunidade-virtual)) | Este doc + [02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais) | PRD-08, PRD-03 |
| Contrato dos jogos ([§8.4](#84-jogos-sobre-o-backend-app-04-e-terceiros)) | [03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript) + este doc | PRD-12, PRD-01, PRD-10 |
| Distribuição da trilha no ciclo ([§2.3](#23-distribuição-da-trilha-pelas-etapas-do-ciclo)) | Este doc + [10 §5](10-case-01-guerreira-zeferina.md#5-o-acervo-include-e-os-kits-mdf-neste-mvp) | PRD-09, PRD-02 |
| Criação original e protagonismo do jogador ([§4](#4-taxonomia-de-atividades-e-desafios), [§5](#5-motor-de-pontuação), [§7](#7-badges)) | [02 §4](02-conceito-do-jogo-e-gamificacao.md#criações-originais-dos-jogadores) + [01 §3](01-visao-valores-e-proposito.md#3-valores-e-causas) + este doc | PRD-01, PRD-02, PRD-03, PRD-05, PRD-09, PRD-12 |
| Canal de sugestões do jogador | [03 §7](03-plataforma-e-arquitetura.md#7-app-05--área-do-jogador) + [13 §5](13-codigo-de-conduta-versao-previa.md#5-como-este-código-evolui) | PRD-01, PRD-02, PRD-05 |
