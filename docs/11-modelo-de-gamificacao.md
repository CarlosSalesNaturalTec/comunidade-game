# 11 — Modelo de Gamificação Integrado

> **Fonte única do motor do jogo.** Enquanto o documento 02 define **o que são** os elementos
> do Comunidade Game, este formaliza **como eles se ligam e quanto valem** — anatomia da
> trilha, taxonomia de atividades, pontuação, níveis, badges e recompensas — e como tudo isso
> se reflete na vitrine, nos cards dos personagens, na representação visual das Comunidades
> Virtuais e nos jogos construídos sobre o backend.

## 1. Visão geral do motor

O motor é um único fluxo, válido para qualquer poder e qualquer área do conhecimento:

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

Regras estruturais:

1. **Só a realização gera pontos.** Pontos nascem exclusivamente de atividades e desafios
   propostos por Mestres e da coleta de dados do território — nunca de presença passiva e nunca
   de dentro do jogo digital.
2. **A acumulação é por trilha ou poder**, não global.
3. **Todo reflexo público é derivado, nunca editado à mão**: o que aparece na vitrine, nos cards
   e nos painéis é leitura do mesmo motor — uma única fonte de verdade no backend.

## 2. Anatomia da trilha

**A trilha é a unidade de organização do aprendizado.** O modelo é **agnóstico de área do
conhecimento**: vale para uma trilha técnica, de cultura e movimento, de expressão artística ou
de humanas. O que muda é o conteúdo e o que se mede na coleta; a estrutura é a mesma.

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
      ├── ENCONTROS PRESENCIAIS — dinâmica assíncrona
      ├── BATALHA — quando a trilha prevê uma disputa (opcional)
      └── CULMINÂNCIA — apresentação pública da criação original;
          é o ponto final de toda trilha
```

| Componente | O que é |
|---|---|
| **Ponto de trilha** | Menor unidade de progressão: conteúdo + atividades + desafio de desbloqueio |
| **Conteúdo** | Material do Mestre, conteúdo de terceiros curado e bibliografia de apoio por ponto |
| **Atividade** | O que o jogador realiza, classificado pela taxonomia da §4 |
| **Desafio de desbloqueio** | Quiz ou desafio que abre o próximo ponto e ativa níveis do poder |
| **Desafio de coleta** | Série temporal de dados reais do território; requisito de **toda** trilha |
| **Desafio extra** | Proposto por Apoiador, validado pelo Mestre e aprovado por Admin; pontos extras isolados |
| **Encontro presencial** | Marco recorrente; roteiro assíncrono com momentos coletivos âncora |
| **Batalha** | Disputa de ideias e realizações; marco opcional, previsto pela trilha |
| **Culminância** | Apresentação pública da criação original; **ponto final de toda trilha** |

### 2.2 O modelo aplicado — três exemplos

A tabela valida a estrutura contra as duas trilhas existentes e contra uma trilha de área não
técnica, mostrando que o modelo não pressupõe tecnologia:

| Componente | Robô Educa (técnica) | Batalha de Laser (técnica) | Capoeira (cultura e movimento — ciclo futuro) |
|---|---|---|---|
| Conteúdo | Montagem, voz, prompts, código | Eletrônica, sensores, MQTT, lógica | História da capoeira, ritmo, movimentos, roda |
| Atividades práticas | Montar e personalizar o robô | Construir atacante, escudo e torre | Treinar sequências, tocar instrumentos |
| Desafio de desbloqueio | Quiz com o próprio robô | Testar o artefato construído | Executar a sequência diante do Mestre |
| Coleta de dados reais | Registro por voz (temperatura, ocorrências) | Sensor de território construído pelo jogador (LDR → iluminação pública) | Registro dos espaços, rodas, mestres e memórias do bairro |
| Batalha | — (apresentação) | **Batalha de Laser** presencial | Roda / jogo de capoeira entre equipes |
| Culminância | Publicar e apresentar sua versão do robô | Partida final com telemetria no telão | Apresentação da roda para a comunidade |

### 2.3 Distribuição da trilha pelas etapas do ciclo

Toda trilha é **paginada no calendário de um ciclo** (o período letivo da comunidade). O modelo
é o mesmo para qualquer trilha:

| Etapa | O que acontece | Conteúdo e material |
|---|---|---|
| **Abertura** | Onboarding e credenciamento; escolha do poder; **ritual de entrada** — a entrega do livro próprio é a primeira atividade pontuada; abertura das séries de coleta | Ponto 1 da trilha; livro próprio entregue; kit e insumos da primeira montagem |
| **Desenvolvimento** | Encontros presenciais assíncronos avançando os pontos + desafios on-line entre encontros; séries de coleta rendendo pontos; desafios extras de Apoiadores | Pontos intermediários; capítulo recomendado por ponto; acervo permanente em bancada |
| **Marcos** | Batalhas, quando a trilha prevê; Quiz ao Vivo nos encontros | Artefatos construídos no desenvolvimento |
| **Fechamento** | **Culminância**, conferência de inventário do acervo, avaliação do ciclo e das hipóteses | Portfólio, vídeos (com consentimento), prestação de contas |

Diretrizes de paginação para o Mestre (autor da trilha):

- **O ritual de abertura não se adia**: livro próprio na mão e série de coleta aberta já na
  primeira etapa — é o que dá material de trabalho e pontuação recorrente desde o primeiro dia.
- **Um ponto de trilha por encontro é o passo de referência**, mas a dinâmica assíncrona permite
  que cada jogador ou equipe esteja em pontos diferentes: a paginação orienta o planejamento de
  recursos, não o ritmo individual.
- **A bibliografia acompanha o ponto, não a trilha inteira.**
- **Batalha depois da construção, culminância depois de tudo**: os marcos ficam na segunda
  metade do ciclo, quando há o que disputar e o que mostrar.
- **O fechamento é parte da trilha, não apêndice**: a culminância pontua, alimenta o portfólio
  público e produz o material de avaliação do ciclo.

## 3. Papéis no motor

| Persona | Papel |
|---|---|
| **Jogador** | Percorre trilhas, realiza atividades e desafios, **produz criações originais** com autoria creditada, acumula pontos, níveis e badges, troca pontos por recompensas e **propõe melhorias** |
| **Mestre** | Autor da trilha: define pontos, conteúdos, atividades, desafios e a paginação no ciclo; lança resultados; valida desafios extras. Pode ser de **qualquer área do conhecimento** |
| **Apoiador** | Provê lastro e propõe **desafios extras** (abertos ou direcionados); acompanha a efetividade do apoio |
| **Admin** | Aprova desafios extras, opera lançamentos e painéis, cria Comunidades Virtuais |
| **Comunidade Virtual** | Recebe os dados coletados; sua representação visual cresce com a participação |

## 4. Taxonomia de atividades e desafios

Toda atividade é classificada em **três eixos ortogonais**, que se combinam livremente (uma
atividade pode ser *em equipe + presencial + de construção*):

| Eixo | Valores | Observações |
|---|---|---|
| **Modalidade** | Individual · Em equipe (mista, até 5) · Em família (Equipe Familiar) | Define a pontuação-base; família vale mais por ser estratégica para a permanência |
| **Formato** | Presencial (nos encontros) · On-line/assíncrona (entre encontros) | O desafio de coleta é contínuo: atravessa os dois formatos |
| **Natureza** | Construção/making · Programação e IA · **Coleta de dados do território** · Desplugada · Valores e temas transversais · Competição ao vivo (Quiz) · Culminância · **Criação original** | Lista aberta: novas trilhas de outras áreas acrescentam naturezas (expressão artística, movimento e corpo) |

Regras transversais:

- **Dificuldade gradual, independente de idade** (faixa 6–16).
- **Lastro**: nenhuma atividade acontece sem os recursos providos.
- **Resultado lançado pela gestão**: realizada / realizada com mérito / mérito extra por auxílio
  aos colegas.

## 5. Motor de pontuação

Tabela única das fontes de pontos da plataforma:

| Fonte | Pontos | Tipo | Quem lança |
|---|---|---|---|
| Desafio semanal — atividade on-line | 10 | Regular | Mestre/gestão |
| Desafio semanal — atividade presencial | 10 | Regular | Mestre/gestão |
| Desafio semanal — atividade em equipe | 10 | Regular | Mestre/gestão |
| Desafio semanal — atividade em família | 20 | Regular | Mestre/gestão |
| **Coleta de dados do território** | A definir por tipo | **Recorrente** — pontua a cada registro válido enquanto a série está ativa; interrompeu, parou de render | Automático (registro do jogador) |
| **Quiz ao Vivo** | A definir | Regular | Automático (partida) |
| Mérito extra por auxílio aos colegas | A definir | Regular | Mestre/gestão |
| **Criação original** — culminância da trilha | A definir | Regular | Mestre/gestão |
| Badge de conduta (ex.: Guardião do Acervo) | Pontos + badge | Regular | Mestre/gestão |
| **Desafio extra de Apoiador** (aberto ou direcionado) | Definidos no desafio | **Extra** — computado isoladamente | Automático na conclusão validada |
| **Batalha** (resultado e estatísticas) | A definir por batalha | Regular | Automático (ponte Nexus → API) ou gestão |
| Pontuação negativa (má conduta) | Negativo, a definir | Regular | Admin/gestão, conforme o Código de Conduta |

Três naturezas de saldo, que nunca se confundem:

| Saldo | O que é | Regra |
|---|---|---|
| **Pontos regulares** | Da progressão nas trilhas e poderes | Alimentam níveis, ranking e troca por recompensas |
| **Pontos extras** | De desafios extras de Apoiadores | Computados isoladamente; rastreados no histórico do Apoiador |
| **Pontos consumidos** | Débitos por troca de recompensa e por uso dentro do App 04 | O jogo **só debita, nunca credita**; pontos gastos não afetam níveis nem badges já conquistados |

> **A definir:** valores da coleta por tipo, do Quiz ao Vivo, dos méritos, da criação original e
> da pontuação negativa; janela de tolerância e teto da coleta; mecânica antifraude.

## 6. Níveis

Progressão **por trilha ou poder** (nunca global), destravada por quiz ou desafio:

| Nível | Critério | O que destrava |
|---|---|---|
| 1 | Inscrito e assíduo | Participação nas atividades |
| 2 | Bom rendimento | — |
| 3 | Ótimo rendimento | — |
| 4 | Apoio aos colegas | — |
| **5** | **Mestre Aprendiz** | Apto ao treinamento de multiplicador e ao voluntariado no ponto de apoio |

O Nível 5 é a engrenagem de escala do projeto: o jogador que chega ao topo volta como
multiplicador. Ser Mestre Aprendiz **não** equivale a ser Mestre — o reconhecimento como Mestre
exige cadastro por Admin e habilidade comprovada por artefatos.

## 7. Badges

Badges representam poderes e conquistas e são um dos principais elementos dos cards públicos:

| Tipo | Exemplos | Como se conquista |
|---|---|---|
| **De nível** | Badge do poder no nível alcançado | Progressão da §6 |
| **De conquista** | **Mestre Aprendiz** · **Guardião do Acervo** | Conclusão do Nível 5 · cuidado com o material comum |
| **De valores/causas** | Participação em atividades ligadas às causas do projeto | Atividades de natureza "valores e temas transversais" |
| **De território** | Progressão no **Poder do Território** | Manutenção de séries de coleta ativas |
| **De autoria** | Badge de autoria — criações originais apresentadas em culminância | Criação original validada pelo Mestre |

Regra geral: **badge é por trilha ou por poder, não global.**

## 8. Reflexos no ecossistema

Tudo o que o motor produz — pontos, níveis, badges, resultados, séries de coleta — é lido, nunca
reescrito, pelas quatro superfícies públicas do ecossistema.

### 8.1 Vitrine pública (App 06)

| Elemento do motor | Como aparece na vitrine |
|---|---|
| Jogadores (com autorização do responsável) | **Cards rotativos** (a cada 5 s) — composição em §8.2 |
| Poderes | Seção de poderes, com trilhas e Mestres de cada um |
| Trilhas e realizações | Portfólio público dos jogadores autorizados |
| **Criações originais** | Portfólio de autoria: a criação exposta com o nick do autor ou autores |
| **Batalhas** | Resultados e estatísticas de partida alimentando ranking e portfólio |
| **Culminâncias** | Vídeos e registros, com consentimento específico registrado na App 07 |
| Comunidades Virtuais | Painel público por comunidade em série histórica, agregado e anonimizado |
| Mestres | Cards com os **artefatos que comprovam a habilidade** — de qualquer área |
| Apoiadores | Poder Econômico e desafios extras propostos, com as realizações que o apoio produziu |
| Rankings | Somente pontos regulares; jogadores sem autorização não aparecem |

### 8.2 Cards dos personagens

O card é a "carta do personagem" do universo do jogo, e a mesma composição serve de base para o
App 04:

| Card | O que exibe | O que **nunca** exibe |
|---|---|---|
| **Jogador** | Avatar, nick, badges, poderes com níveis, desempenho e **criações originais** | Imagem real, nome civil, redes sociais, qualquer canal de contato |
| **Mestre** | Nome/identidade, áreas de habilidade, artefatos comprobatórios, trilhas de autoria | — |
| **Apoiador** | Identidade, Poder Econômico, desafios propostos e efetividade (agregada, por avatar) | Dados de contato de jogadores |
| **Comunidade Virtual** | Nome, território, representação visual, séries ativas, nº de jogadores vinculados | Granularidade que permita inferir endereço de criança |

### 8.3 Representação visual da Comunidade Virtual

A Comunidade Virtual "ganha corpo" visualmente na medida da participação — o mapeamento entre
dado registrado e elemento visual é requisito de produto:

| O que acontece no motor | Reflexo visual |
|---|---|
| Comunidade criada por Admin | Território **vazio** — nome e contorno, sem preenchimento |
| Primeira série de coleta aberta | O tipo de dado ganha presença no painel (termômetro, pluviômetro, mapa de vias) |
| Registros acumulados em série ativa | O elemento visual **cresce e ganha detalhe**: série histórica visível, granularidade preenchida |
| Série interrompida | Elemento permanece (dados são permanentes), sinalizado como série inativa |
| Fotos e memórias registradas | Galeria e linha do tempo dos pontos de referência do território |
| Jogadores vinculados ativos | Indicador de vitalidade da comunidade (agregado, sem expor indivíduos) |

Princípios: o visual **representa dados reais, nunca decoração**; a saída pública é sempre
**agregada e anonimizada**.

### 8.4 Jogos sobre o backend (App 04 e terceiros)

Contrato entre o motor e qualquer jogo construído sobre a plataforma:

| O jogo pode | O jogo não pode |
|---|---|
| **Ler** o progresso do jogador: avatar, poderes, badges, níveis | **Creditar** pontos — não existe endpoint de crédito para jogos |
| **Debitar** pontos (consumo declarado dentro do jogo) | Alterar níveis, badges ou histórico |
| Usar os cards (§8.2) como base dos personagens | Exibir imagem real ou dados pessoais do jogador |

- O que se conquista aprendendo **desbloqueia e alimenta** o que o jogador pode fazer no jogo;
  jogar muito não sobe ninguém no ranking — e a ausência de endpoint de crédito elimina, por
  construção, a fraude por automação.
- **Batalhas físicas seguem o mesmo padrão**: a ponte Nexus → API da Batalha de Laser envia as
  estatísticas da partida para a API, que **lança a atividade realizada** — o crédito de pontos é
  da atividade validada, não do jogo. É o modelo de referência para qualquer batalha presencial
  futura, de qualquer área.
- A API pública e aberta permite que **terceiros** construam novos jogos sob o mesmo contrato.
- **O protagonismo vale também aqui**: o código do App 04 é aberto e legível, e alterá-lo é
  atividade de trilha — o jogador não é só usuário do jogo, é um dos seus construtores.
