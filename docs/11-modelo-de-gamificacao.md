# 11 — Modelo de Gamificação Integrado

> **Fonte única do motor do jogo.** Enquanto o documento 02 define **o que são** os elementos
> do Comunidade Game, este formaliza **como eles se ligam e quanto valem** — anatomia da
> trilha, taxonomia de atividades, pontuação, níveis, badges e recompensas — e como tudo isso
> se reflete na vitrine, nos cards dos personagens, na representação visual das Comunidades
> Virtuais e nos jogos construídos sobre o backend.

## 1. Visão geral do motor

O motor é um único fluxo, válido para qualquer poder e qualquer área do conhecimento:

```text
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
                │ (progressão)  │  │ (conquistas)  │  │ (marco/extra) │
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

1. **Só a realização gera pontos regulares.** Eles nascem exclusivamente de atividades e
   desafios propostos por Mestres e da coleta de dados do território — nunca de presença
   passiva e nunca de dentro do jogo digital. Os **pontos extras** têm fontes próprias (§5) e
   dependem sempre de um ato humano de validação.
2. **A acumulação é por trilha ou poder**, não global — e o **nível vem do percurso da
   trilha**, não do saldo acumulado (§6).
3. **Todo reflexo público é derivado, nunca editado à mão**: o que aparece na vitrine, nos
   cards e nos painéis é leitura do mesmo motor — uma única fonte de verdade no backend.

## 2. Anatomia da trilha

**A trilha é a unidade de organização do aprendizado.** O modelo é **agnóstico de área do
conhecimento**: vale para uma trilha técnica, de cultura e movimento, de expressão artística ou
de humanas. O que muda é o conteúdo e o que se mede na coleta; a estrutura é a mesma.

### 2.1 Do que uma trilha é composta

```text
TRILHA (autoria de um Mestre, vinculada a um Poder)
│
├── ETIQUETA ODS — ao menos um objetivo da Agenda 2030 que a trilha
│   toca, declarado pelo Mestre autor
│
├── MISSÃO DE SONDAGEM — abre toda trilha; mede de onde a turma parte
│
├── MISSÕES (sequência ordenada, com dificuldade gradual)
│     └── cada uma obrigatória ou opcional, e contendo:
│           ├── CONTEÚDO — próprio do Mestre, de terceiros (curado) e
│           │   bibliografia de apoio (título/capítulo do acervo)
│           ├── ATIVIDADES — o que o Guerreiro(a) produz para aprender
│           ├── DESAFIO DE DESBLOQUEIO — quiz ou desafio que abre a
│           │   próxima missão e os níveis do poder
│           └── RETOMADA — revisão espaçada, na cadência que o Mestre
│               declarar (§2.2)
│
├── DESAFIO(S) DE COLETA DE DADOS REAIS — obrigatório em toda trilha
│     └── série temporal com cadência; pontua enquanto ativa
│
├── DESAFIOS EXTRAS — propostos por Apoiadores ou Mestres, na trilha
│     └── abertos a todos ou direcionados a um Guerreiro(a) específico
│
└── MARCOS — eventos que pontuam o percurso no calendário do ciclo
      ├── ENCONTROS PRESENCIAIS — dinâmica assíncrona
      ├── BATALHA — quando a trilha prevê uma disputa (opcional)
      └── CULMINÂNCIA — apresentação pública da criação original;
          é o encerramento de toda trilha
```

| Componente                 | O que é                                                                                   |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| **Etiqueta ODS**           | Objetivos da Agenda 2030 que a trilha toca; opcional no Ciclo 01, obrigatória do Ciclo 02 |
| **Missão**                 | Menor unidade de progressão: conteúdo + atividades + desafio de desbloqueio               |
| **Missão de sondagem**     | Primeira missão de toda trilha; quiz que mede o nível de partida no poder                 |
| **Conteúdo**               | Material do Mestre, conteúdo de terceiros curado e bibliografia de apoio por missão       |
| **Atividade**              | O que o Guerreiro(a) realiza, classificado pela taxonomia da §4                           |
| **Desafio de desbloqueio** | Quiz ou desafio que abre a próxima missão e ativa níveis do poder                         |
| **Retomada**               | Revisão espaçada de missão já cumprida, na cadência declarada pelo Mestre                 |
| **Desafio de coleta**      | Série temporal de dados reais do território; requisito de **toda** trilha                 |
| **Desafio extra**          | Proposto por Apoiador ou Mestre, aprovado por Admin; até 10 pontos extras isolados        |
| **Encontro presencial**    | Marco recorrente; roteiro assíncrono com momentos coletivos âncora                        |
| **Batalha**                | Disputa de ideias e realizações; marco opcional, previsto pela trilha                     |
| **Culminância**            | Apresentação pública da criação original; **encerramento de toda trilha**                 |

**Marco concede recompensa.** Desbloqueio de missão, conclusão de etapa, batalha e culminância
são os momentos em que a recompensa é entregue — o Mestre autor declara qual marco concede o
quê, conforme a regra do documento 02.

#### Inscrição na trilha

**Quem põe o Guerreiro(a) no percurso de uma trilha é a inscrição dele**, nunca o lançamento de
um resultado. A trilha precisa estar **publicada**, e a inscrição é a primeira das duas
condições do nível 1 (§6).

- **Várias ao mesmo tempo**, sem limite: a escolha do poder é o caminho até as trilhas dele,
  não um teto de uma trilha por poder.
- **Uma inscrição por trilha** — inscrever-se de novo na mesma trilha não cria vínculo novo.
- **Não se desfaz e não obriga a concluir.** Quem para no meio fica com a evolução limitada às
  etapas realizadas, e o nível já conquistado não regride (§6).

#### Etiqueta ODS da trilha

O Mestre autor declara quais **Objetivos de Desenvolvimento Sustentável** a trilha toca: o
número do objetivo, com a meta (`4.7`, `13.3`, `17.18`) quando ele souber. A etiqueta é da
trilha inteira e do poder a que ela se vincula. É rótulo descritivo, e por isso não pesa no
motor:

- **Não pontua e não é poder.** Nada na progressão do Guerreiro(a) depende dela.
- **Uma etiqueta por trilha basta.** Etiquetar missão a missão continua possível e é
  **opcional em qualquer ciclo** — só vale a pena quando a missão toca objetivo diferente do
  da trilha. Sem etiqueta própria, a missão responde pela da trilha.
- **Opcional no Ciclo 01, obrigatória a partir do Ciclo 02.** No primeiro ciclo o template
  sugere e a trilha publica sem ela; do Ciclo 02 em diante, **trilha sem etiqueta não
  publica** — cobertura pela metade não sustenta número diante de edital.
- **Sobe por agregação** — trilha, poder, comunidade e ciclo —, sem lançamento manual. É assim
  que a cobertura cresce sozinha à medida que novos Mestres e poderes entram.
- O **desafio de coleta** herda a etiqueta da missão que o criou ou, na falta dela, a da
  trilha: medição ambiental ou urbana numa trilha, patrimônio e memória do bairro em outra.
- O **desafio extra**, de Apoiador ou de Mestre, herda pela mesma regra a etiqueta da missão a
  que se vincula.
- A cobertura é publicada **agregada por comunidade e por ciclo, nunca por Guerreiro(a)** —
  criança não é rotulada por objetivo de desenvolvimento.

### 2.2 Anatomia da missão

**Só aprende quem faz.** A missão existe para o Guerreiro(a) quebrar a cabeça: exercitar o que
foi ensinado escrevendo, falando ou construindo, errar e refazer até acertar. Missão em que se
apenas consome conteúdo não é missão.

Toda missão declara:

| Elemento                    | Regra                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------ |
| **Obrigatória ou opcional** | Declarado pelo Mestre. Só as obrigatórias contam no percurso do nível (§6)                 |
| **Conteúdo**                | O que se ensina, com a bibliografia de apoio                                               |
| **Ao menos uma atividade**  | E toda atividade exige **produção** do Guerreiro(a): escrever, falar ou construir          |
| **Desafio de desbloqueio**  | Quiz ou desafio prático que abre a missão seguinte — fato do Guerreiro(a) na trilha        |
| **Retomada**                | Cadência da revisão espaçada, quando o Mestre a declara                                    |
| **Recompensa**              | Quando o Mestre declara que aquele desbloqueio libera algo concreto                        |
| **Etiqueta ODS**            | Opcional em qualquer ciclo; só quando a missão toca objetivo diferente do da trilha (§2.1) |

Cinco regras fecham o modelo:

- **Sondagem antes de ensinar.** Toda trilha abre com uma missão de sondagem, e sem ela a
  trilha não publica. Ela mede de onde a turma parte; **não define nível**, que é percurso (§6).
- **Repetir para fixar.** A retomada traz de volta o que já foi cumprido, na cadência que o
  Mestre declara — o mesmo vocabulário do desafio de coleta. Ela pontua **uma vez por
  agendamento**; refazer por conta própria não rende ponto novo. O _template_ de missão sugere
  como padrão **três retomadas, em 2, 7 e 21 dias** contados do desbloqueio: intervalos
  crescentes, com a primeira ainda perto da aprendizagem. É sugestão — o Mestre declara a sua.
- **A análise da produção é hipótese, não resultado.** A plataforma lê o que o Guerreiro(a)
  escreveu ou falou e devolve retorno **sempre construtivo**, apontando o caminho em vez do
  erro. **Quem lança o resultado é o Mestre** — a leitura automática nunca pontua sozinha.
- **Poder técnico começa desplugado.** Em trilha de tecnologia, o modelo pede ao menos uma
  atividade desplugada: lógica e algoritmo com papel e corpo abrem a porta para quem ainda não
  pegou um aparelho.
- **O desbloqueio é do Guerreiro(a) na trilha, nunca da equipe.** No quiz, o núcleo afere a
  submissão sozinho. No desafio prático, sem critério que o núcleo possa aferir, o
  Guerreiro(a) declara que cumpriu e o **Mestre autor julga**; enquanto não julga, a missão
  aguarda, nunca reprovada.

### 2.3 O modelo aplicado — três exemplos

A tabela valida a estrutura contra as duas trilhas existentes e contra uma trilha de área não
técnica, mostrando que o modelo não pressupõe tecnologia:

| Componente             | Robô Educa (técnica)                        | Batalha de Laser (técnica)                                                   | Capoeira (cultura e movimento — ciclo futuro)             |
| ---------------------- | ------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------- |
| Conteúdo               | Montagem, voz, prompts, código              | Eletrônica, sensores, MQTT, lógica                                           | História da capoeira, ritmo, movimentos, roda             |
| Atividades práticas    | Montar e personalizar o robô                | Construir atacante, escudo e torre                                           | Treinar sequências, tocar instrumentos                    |
| Desafio de desbloqueio | Quiz com o próprio robô                     | Testar o artefato construído                                                 | Executar a sequência diante do Mestre                     |
| Coleta de dados reais  | Registro por voz (temperatura, ocorrências) | Sensor de território construído pelo Guerreiro(a) (LDR → iluminação pública) | Registro dos espaços, rodas, mestres e memórias do bairro |
| Batalha                | — (apresentação)                            | **Batalha de Laser** presencial                                              | Roda / jogo de capoeira entre equipes                     |
| Culminância            | Publicar e apresentar sua versão do robô    | Partida final com telemetria no telão                                        | Apresentação da roda para a comunidade                    |

### 2.4 Distribuição da trilha pelas etapas do ciclo

Toda trilha é **paginada no calendário de um ciclo** (o período letivo da comunidade). O modelo
é o mesmo para qualquer trilha:

| Etapa               | O que acontece                                                                                                                                                   | Conteúdo e material                                                                   |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Abertura**        | Onboarding e credenciamento; escolha do poder; **ritual de entrada** — a entrega do livro próprio é a primeira atividade pontuada; abertura das séries de coleta | Missão de sondagem; livro próprio entregue; kit e insumos da primeira montagem        |
| **Desenvolvimento** | Encontros presenciais assíncronos avançando as missões + desafios on-line entre encontros; séries de coleta rendendo pontos; desafios extras de Apoiadores       | Missões intermediárias; capítulo recomendado por missão; acervo permanente em bancada |
| **Marcos**          | Batalhas, quando a trilha prevê; Quiz ao Vivo nos encontros                                                                                                      | Artefatos construídos no desenvolvimento                                              |
| **Fechamento**      | **Culminância**, conferência de inventário do acervo, avaliação do ciclo e das hipóteses                                                                         | Portfólio, vídeos (com consentimento), prestação de contas                            |

Diretrizes de paginação para o Mestre (autor da trilha):

- **O ritual de abertura não se adia**: livro próprio na mão e série de coleta aberta já na
  primeira etapa — é o que dá material de trabalho e pontuação recorrente desde o primeiro dia.
- **Uma missão por encontro é o passo de referência**, mas a dinâmica assíncrona
  permite que cada Guerreiro(a) ou equipe esteja em missões diferentes: a paginação orienta o
  planejamento de recursos, não o ritmo individual.
- **A bibliografia acompanha a missão, não a trilha inteira.**
- **Batalha depois da construção, culminância depois de tudo**: os marcos ficam na segunda
  metade do ciclo, quando há o que disputar e o que mostrar.
- **O fechamento é parte da trilha, não apêndice**: a culminância pontua, alimenta o portfólio
  público e produz o material de avaliação do ciclo.

## 3. Papéis no motor

| Persona                | Papel                                                                                                                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Guerreiro(a)**       | Percorre trilhas, realiza atividades e desafios, **produz criações originais** com autoria creditada, acumula pontos, níveis e badges, conquista recompensas nos marcos e **propõe melhorias** |
| **Mestre**             | Autor da trilha: define missões, conteúdos, atividades, desafios e a paginação no ciclo; lança resultados; valida desafios extras. Pode ser de **qualquer área do conhecimento**               |
| **Apoiador**           | Provê lastro e propõe **desafios extras** (abertos ou direcionados); acompanha a efetividade do apoio                                                                                          |
| **Admin**              | Aprova desafios extras, opera lançamentos e painéis, cria Comunidades Virtuais                                                                                                                 |
| **Comunidade Virtual** | Recebe os dados coletados; sua representação visual cresce com a participação                                                                                                                  |

**O Apoiador não pontua.** Este documento é o motor de pontos, níveis e badges do
Guerreiro(a). A progressão de quem apoia — missões, níveis de sustento e selos — corre em
moedas, não em pontos, e está no documento 14.

## 4. Taxonomia de atividades e desafios

Toda atividade é classificada em **três eixos ortogonais**, que se combinam livremente (uma
atividade pode ser _em equipe + presencial + de construção_):

| Eixo           | Valores                                                                                                                                                                                                             | Observações                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Modalidade** | Individual · Em equipe (grupo livre, até 5) · Em equipe com familiar (no máximo 1, com 17 anos ou mais)                                                                                                             | Define a pontuação-base; a presença do familiar vale mais por ser estratégica para a permanência           |
| **Formato**    | Presencial (nos encontros) · On-line/assíncrona (entre encontros)                                                                                                                                                   | Presencial: desplugada, construção, Quiz ao Vivo. On-line: quiz e desafios entre encontros                 |
| **Natureza**   | **Sondagem** · Construção/making · Programação e IA · **Coleta de dados do território** · Desplugada · Valores e temas transversais · Competição ao vivo (Quiz) · **Retomada** · Culminância · **Criação original** | Lista aberta: novas trilhas de outras áreas acrescentam naturezas (expressão artística, movimento e corpo) |

Regras transversais:

- **Toda atividade de trilha pertence a uma missão** e é autorada pelo Mestre, que
  declara a modalidade e o formato. Atividade avulsa, fora de trilha, é cadastro da gestão.
- **Toda atividade exige produção** do Guerreiro(a) — escrever, falar ou construir (§2.2).
- **Dificuldade gradual, independente de idade** (faixa 6–16).
- **Um Guerreiro(a) pode integrar mais de uma equipe** e pontua em **todas** as atividades em
  que participa e colabora — no Quiz ao Vivo, por ser simultâneo, joga por uma equipe só,
  ainda que várias equipes disputem a partida.
- **Lastro**: nenhuma atividade acontece sem os recursos providos.
- **Resultado lançado pela gestão**: realizada / realizada com mérito / mérito extra por
  auxílio aos colegas.

## 5. Motor de pontuação

Tabela única das fontes de pontos da plataforma:

| Fonte                                                       | Pontos                                                                         | Tipo                                                                                        | Quem lança                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------ |
| Desafio semanal — atividade on-line                         | 10                                                                             | Regular                                                                                     | Mestre/gestão                              |
| Desafio semanal — atividade presencial                      | 10                                                                             | Regular                                                                                     | Mestre/gestão                              |
| Desafio semanal — atividade em equipe                       | 10                                                                             | Regular                                                                                     | Mestre/gestão                              |
| Desafio semanal — atividade em equipe com familiar          | 20                                                                             | Regular                                                                                     | Mestre/gestão                              |
| Atividade **realizada com mérito**                          | +5 sobre o valor da atividade **e +5 extras**                                  | Regular **e Extra**                                                                         | Mestre/gestão                              |
| **Mérito extra por auxílio aos colegas**                    | +10 sobre o valor da atividade **e +10 extras**                                | Regular **e Extra**                                                                         | Mestre/gestão                              |
| **Coleta de dados do território**                           | 5 por registro válido                                                          | **Recorrente** — pontua enquanto a série está ativa, sem teto; interrompeu, parou de render | Automático (registro do Guerreiro(a))      |
| **Quiz ao Vivo**                                            | 1 por acerto da equipe, +1 à primeira a acertar; teto de 10 por partida        | Regular                                                                                     | Automático (partida)                       |
| **Criação original** — culminância da trilha                | 50, integrais a cada integrante                                                | Regular                                                                                     | Mestre autor, ao validar                   |
| **Batalha**                                                 | 10 por disputar, +10 à equipe vencedora, +5 ao melhor desempenho na telemetria | Regular                                                                                     | Automático (ponte Nexus → API) ou gestão   |
| Badge de conduta (ex.: Guardião do Acervo)                  | 20 + **20 extras** + badge, uma vez por ciclo                                  | Regular **e Extra**                                                                         | Mestre/gestão                              |
| **Conservação e uso do bem recebido** (livro, camisa, kit)  | 1 por item apresentado, por encontro presencial                                | **Extra** — computado isoladamente                                                          | Mestre, a pedido do Guerreiro(a) na aula   |
| **Valorizar a criação dos colegas e cuidar dos mais novos** | 5, uma vez por encontro presencial                                             | **Extra** — computado isoladamente                                                          | Mestre, ao observar                        |
| **Pactuação do Código de Conduta** da comunidade            | 10, uma vez por ciclo                                                          | **Extra** — computado isoladamente                                                          | Mestre/gestão, ao registrar o código       |
| **Desafio extra** de Apoiador ou de Mestre                  | Definidos no desafio, **até 10**                                               | **Extra** — computado isoladamente                                                          | Automático na conclusão validada           |
| **Proposta de evolução adotada** pela gestão                | 20 + badge                                                                     | **Extra** — computado isoladamente                                                          | Gestão, ao adotar a proposta               |
| Pontuação negativa (má conduta)                             | −5 por ocorrência, teto de −10 por aula presencial                             | Regular                                                                                     | Admin/gestão, conforme o Código de Conduta |

Duas naturezas de saldo, que nunca se confundem:

| Saldo                | O que é                                                                                               | Regra                                                                                                |
| -------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Pontos regulares** | Da progressão nas trilhas e poderes                                                                   | Alimentam níveis e ranking. **Nunca se gastam**                                                      |
| **Pontos extras**    | Do mérito, do auxílio aos colegas, do cuidado com o que recebeu, de desafios extras e do protagonismo | Computados isoladamente; não alimentam níveis; os de desafio são rastreados no histórico do Apoiador |

**Ponto regular é percurso; ponto extra é caráter.** O regular vem de avançar na trilha; o
extra vem do que se faz além dela — cuidar, colaborar, propor. É o que separa as duas naturezas
e o critério para classificar fonte nova.

**Esta tabela é a única fonte do valor.** Quem cadastra atividade — Mestre na App 09, gestão na
App 03 para a atividade avulsa — **escolhe o tipo** e a pontuação vem daqui; ninguém arbitra
valor no cadastro. É a mesma régua da tabela de preços do catálogo avulso (documento 02 §8.2):
a mesma atividade não vale 10 numa comunidade e 30 na vizinha.

**Ponto regular não se gasta; debita só por fato desfeito.** Gastar é trocar por recompensa, e
isso só o saldo de pontos extras faz. Debitam o regular apenas dois fatos: a **ocorrência de
conduta** lançada e o **estorno do registro de coleta invalidado** na auditoria do Mestre. Fora
esses dois, ele só cresce.

**Ponto extra tem duas contas**, que nunca se confundem:

| Conta                | O que é                                       | Comportamento                                                                                       |
| -------------------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Acumulado**        | Tudo o que o Guerreiro(a) já ganhou em extras | **Nunca decresce.** É o que a vitrine, os cards, o ranking, o histórico do Apoiador e o App 04 leem |
| **Saldo disponível** | O que ainda não foi trocado                   | Debita na troca por recompensa avulsa; nunca fica negativo                                          |

Trocar **não enfraquece o personagem** no App 04 nem apaga histórico: o jogo lê o acumulado,
não o saldo, e segue **sem debitar nada** (§8.4).

**Recompensa de marco nunca é comprada** — continua conquistada ao atingir o marco da trilha,
como manda o documento 02 §8. O que a troca alcança é a **recompensa avulsa** do catálogo, que
é outra coisa: item de prateleira, com lastro e estoque, entregue no encontro presencial.

A coleta vale o mesmo por registro, qualquer que seja o tipo medido, e **não tem teto**:
**quantos registros de um mesmo período de cadência pontuam é declarado no desafio** pelo
Mestre que o cria.

**O +5 da batalha sai por papel.** Cada papel disputado tem a sua métrica na telemetria —
precisão do Caçador, acertos absorvidos sem penalidade do Defensor —, declarada pelo Mestre no
cadastro da batalha, e o melhor de cada papel na partida leva os 5 pontos. Papéis diferentes
não disputam a mesma régua, e **batalha sem telemetria não distribui o +5**: ficam de pé os 10
por disputar e os 10 da equipe vencedora.

**Cuidar do que recebeu pontua, e quem pede é o Guerreiro(a).** Apresentar ao Mestre, no
encontro presencial, o livro, a camisa, o kit ou outro bem recebido **em bom estado e em uso**
vale **1 ponto extra por item**. O Guerreiro(a) pede a validação durante a aula, o Mestre
confere e lança — não há conferência automática nem lançamento de ofício. **Cada item pontua
uma vez por encontro**: quem leva livro, camisa e kit em bom estado soma 3 no dia, e o mesmo
livro não pontua duas vezes no mesmo encontro. O badge **Guardião do Acervo** segue sendo o
reconhecimento do cuidado com o **material comum**, uma vez por ciclo (§7), e rende pontos
regulares **e extras** — cuidar do que é de todos vale tanto quanto cuidar do que é seu.

**Sondagem e retomada valem como qualquer atividade** do seu formato — não têm tabela própria.
A retomada pontua **uma vez por agendamento**; refazer por conta própria não rende ponto novo.
O resultado da sondagem não credita nem define nível: ela mede o ponto de partida, e a
devolutiva automática da produção **nunca pontua sozinha** — quem lança o resultado é o Mestre.

**O débito não desfaz percurso.** O saldo da trilha **nunca fica negativo**, nível e badge já
conquistados **não regridem**, e a ocorrência de conduta **sai do ranking ao fim do ciclo**,
devolvendo **o que foi debitado de fato** — nunca o valor nominal do lançamento, e nunca virando
crédito líquido —; o registro permanece para a gestão e o responsável. Vale para a pontuação
negativa e para o estorno da coleta: é consequência no jogo, não porta de saída.

### 5.1 Integridade dos pontos

O desenho já elimina as duas fraudes mais prováveis: o jogo **não escreve nada** e o
Guerreiro(a) entra em toda aplicação com login **por nick e imagem**, de modo que a atividade é
comprovadamente dele. As demais travas:

| Risco                             | Trava                                                                                                                            |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Dado de coleta inventado          | Valor fora da faixa declarada no desafio entra como **a conferir** e só pontua com validação do Mestre                           |
| Registro em massa                 | Pontua o número de registros por cadência declarado no desafio; o excedente fica sem crédito                                     |
| Registro inverossímil             | Auditoria por amostragem do Mestre; a invalidação **estorna apenas aquele registro**                                             |
| Resposta de quiz por outra equipe | Cada Guerreiro(a) joga por uma só equipe na partida, e a resposta é registrada pela equipe — a plataforma não controla aparelhos |
| Lançamento indevido               | Só o Mestre autor lança; lançamento não é editável e a correção referencia o original                                            |

Nenhuma dessas travas depende de infraestrutura sofisticada — antifraude que não roda na rede
do ponto de apoio não é antifraude.

## 6. Níveis

Progressão **por trilha ou poder** (nunca global), destravada por quiz ou desafio.

**Nível é percurso, não volume de pontos.** O que faz subir é avançar na trilha — não o total
acumulado. A razão é dupla: a coleta é recorrente e sem teto, e amarrar nível a saldo faria
alguém subir sustentando séries sem percorrer a trilha; e ponto acumula com tempo, o que
condenaria quem entra no meio do ciclo, contra a dinâmica assíncrona dos encontros.

| Nível | Critério            | Condição verificável                                                           |
| ----- | ------------------- | ------------------------------------------------------------------------------ |
| 1     | Inscrito e assíduo  | Inscrito na trilha e com a primeira atividade realizada                        |
| 2     | Bom rendimento      | **1/3** das missões obrigatórias desbloqueadas                                 |
| 3     | Ótimo rendimento    | **2/3** desbloqueadas **e** série de coleta ativa                              |
| 4     | Apoio aos colegas   | Todas as obrigatórias desbloqueadas **e** ao menos um mérito extra por auxílio |
| **5** | **Mestre Aprendiz** | **Culminância validada** pelo Mestre autor da trilha                           |

**Só a missão obrigatória conta no percurso.** A opcional pontua e pode render badge, mas fica
fora do denominador — quem faz o mínimo não trava, e quem faz tudo ganha por ter feito.

**A fração arredonda para cima.** Quando o total de obrigatórias não divide exato por 3, o
limiar mínimo de missões desbloqueadas é o teto da fração — ex.: 4 obrigatórias exigem 2 para
o nível 2. Garante que cada nível sempre exija progresso real, mesmo com poucas missões.

**Nível conquistado não regride**: série que se interrompe depois, ou pontuação negativa
lançada em seguida, não derrubam o nível já alcançado.

O Nível 5 é a engrenagem de escala do projeto: o Guerreiro(a) que chega ao topo volta como
multiplicador. Ser Mestre Aprendiz **não** equivale a ser Mestre — o reconhecimento como Mestre
exige cadastro por Admin e habilidade comprovada por artefatos.

## 7. Badges

Badges representam poderes e conquistas e são um dos principais elementos dos cards públicos:

| Tipo                  | Exemplos                                                          | Como se conquista                                     |
| --------------------- | ----------------------------------------------------------------- | ----------------------------------------------------- |
| **De nível**          | Badge do poder no nível alcançado                                 | Progressão da §6                                      |
| **De conquista**      | **Mestre Aprendiz** · **Guardião do Acervo**                      | Conclusão do Nível 5 · cuidado com o material comum   |
| **De valores/causas** | Participação em atividades ligadas às causas do projeto           | Atividades de natureza "valores e temas transversais" |
| **De território**     | Progressão no **Poder do Território**                             | Manutenção de séries de coleta ativas                 |
| **De autoria**        | Badge de autoria — criações originais apresentadas em culminância | Criação original validada pelo Mestre                 |
| **De protagonismo**   | Proposta de evolução da plataforma adotada                        | Sugestão do Guerreiro(a) adotada pela gestão          |

Regra geral: **badge é por trilha ou por poder, não global.** A **única exceção é o badge de
protagonismo**: a proposta que o rende é sobre a plataforma inteira, não sobre uma trilha.

## 8. Reflexos no ecossistema

Tudo o que o motor produz — pontos, níveis, badges, resultados, séries de coleta — é lido,
nunca reescrito, pelas quatro superfícies públicas do ecossistema.

### 8.1 Vitrine pública (App 06)

| Elemento do motor                                        | Como aparece na vitrine                                                                       |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Guerreiros e Guerreiras (com autorização do responsável) | **Cards rotativos** (a cada 5 s) — composição em §8.2                                         |
| Poderes                                                  | Seção de poderes, com trilhas e Mestres de cada um                                            |
| Trilhas e realizações                                    | Portfólio público dos Guerreiros e Guerreiras autorizados                                     |
| **Criações originais**                                   | Portfólio de autoria: a criação exposta com o nick do autor ou autores                        |
| **Batalhas**                                             | Resultados e estatísticas de partida alimentando ranking e portfólio                          |
| **Culminâncias**                                         | Vídeos e registros, com consentimento específico registrado na App 07                         |
| Comunidades Virtuais                                     | Painel público por comunidade em série histórica, agregado e anonimizado                      |
| **Etiquetas ODS**                                        | Painel de cobertura da Agenda 2030 por comunidade e por ciclo, com destaque para a meta 17.18 |
| Mestres                                                  | Cards com os **artefatos que comprovam a habilidade** — de qualquer área                      |
| Apoiadores                                               | Poder Sustentador e desafios extras propostos, com as realizações que o apoio produziu        |
| Rankings                                                 | Somente pontos regulares; Guerreiros e Guerreiras sem autorização não aparecem                |

### 8.2 Cards e páginas individuais dos personagens

O card é a "carta do personagem" do universo do jogo, e a mesma composição serve de base para o
App 04. A tabela abaixo define **o que cada card exibe**; a aparência dele — cor, tipografia,
moldura e emblema — está no documento 15:

| Card                   | O que exibe                                                                                                                            | O que **nunca** exibe                                             |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Guerreiro(a)**       | Avatar, nick, badges, poderes com níveis, desempenho e **criações originais**                                                          | Imagem real, nome civil, redes sociais, qualquer canal de contato |
| **Mestre**             | **Avatar, nick**, áreas de habilidade, artefatos comprobatórios, trilhas de autoria e **selo de quem sustentou atividade sem recurso** | —                                                                 |
| **Apoiador**           | **Avatar, nick e total de moedas em destaque**, nível de sustento, selos, desafios propostos e efetividade agregada                    | Dados de contato de Guerreiros e Guerreiras; valores em reais     |
| **Comunidade Virtual** | Nome, território, representação visual, séries ativas, nº de Guerreiros e Guerreiras vinculados                                        | Granularidade que permita inferir endereço de criança             |

**Definição vigente — todo card abre uma página individual.** O card é o resumo; a página é a
versão detalhada, com as mesmas restrições de exibição da tabela acima:

| Página individual      | O que detalha                                                                                                                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Guerreiro(a)**       | Trajetória nas trilhas, badges e níveis por poder, portfólio de criações originais com autoria e participação em batalhas                                                                         |
| **Mestre**             | Habilidades, trilhas de autoria, a prova pública — **currículo, portfólios, redes sociais e documentos comprobatórios externos** — e quantas vezes sustentou uma atividade que estava sem recurso |
| **Poder**              | Trilhas do poder, Mestres responsáveis, níveis e badges possíveis                                                                                                                                 |
| **Apoiador**           | Aportes em moedas, nível de sustento e selos conquistados, desafios extras propostos com sua efetividade e a prova do apoio: **currículo, portfólios, redes sociais e comprobatórios**            |
| **Comunidade Virtual** | Séries históricas do território, representação visual, vitalidade e criações originais dos Guerreiros e Guerreiras vinculados                                                                     |

**Identidade visual comum do card de Apoiador.** Os avatares dos Apoiadores são logomarcas e
imagens de origens diferentes, e a vitrine os apresenta em **um só formato**: **moldura comum**,
avatar **centralizado** em proporção fixa, nick abaixo e o **total de moedas em destaque**. É o
que impede que a marca maior domine a página e mantém a leitura de coleção de cards.

**Piso do avatar personalizado.** O avatar próprio — logomarca ou imagem escolhida — é liberado
a partir de **10 moedas acumuladas** em aportes homologados. Abaixo disso o card exibe o
**avatar padrão do projeto**, na mesma moldura, com o nick e o total de moedas do Apoiador e
nenhuma outra marca de diferença. Alcançado o piso, o direito **não regride**, e o nick é
sempre do Apoiador, em qualquer faixa. É o que impede a página pública de virar mural de marca
a custo baixo sem apagar quem aportou pouco.

### 8.3 Representação visual da Comunidade Virtual

A Comunidade Virtual "ganha corpo" visualmente na medida da participação — o mapeamento entre
dado registrado e elemento visual é requisito de produto:

| O que acontece no motor                   | Reflexo visual                                                                                  |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Comunidade criada por Admin               | Território **vazio** — nome e contorno, sem preenchimento                                       |
| Primeira série de coleta aberta           | O tipo de dado ganha presença no painel (termômetro, pluviômetro, mapa de vias)                 |
| Registros acumulados em série ativa       | O elemento visual **cresce e ganha detalhe**: série histórica visível, granularidade preenchida |
| Série interrompida                        | Elemento permanece (dados são permanentes), sinalizado como série inativa                       |
| Fotos e memórias registradas              | Galeria e linha do tempo dos pontos de referência do território                                 |
| Guerreiros e Guerreiras vinculados ativos | Indicador de vitalidade da comunidade (agregado, sem expor indivíduos)                          |

Princípios: o visual **representa dados reais, nunca decoração**; a saída pública é sempre
**agregada e anonimizada**. Cor, forma e medida desses elementos estão no documento 15.

### 8.4 Jogos sobre o backend (App 04 e terceiros)

**Definição vigente — o jogo é somente leitura.** Ele lê o progresso do Guerreiro(a) para
montar o personagem da partida e **não escreve nada de volta**: não credita, não debita, não
registra resultado. Ganhar ou perder mil partidas não muda uma linha do perfil. O App 04 é
**público e sem login**, e só oferece como personagem quem tem **divulgação autorizada** —
mesma regra da vitrine.

| O jogo pode                                                                     | O jogo não pode                                                 |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Ler** o progresso: avatar, poderes, badges, níveis e os dois saldos de pontos | **Creditar** pontos — não existe endpoint de crédito para jogos |
| **Compor o personagem** da partida a partir desse progresso                     | **Debitar** pontos ou consumir saldo de qualquer natureza       |
| Usar os cards (§8.2) como base dos personagens                                  | Escrever resultado de partida, nível, badge ou histórico        |
|                                                                                 | Exibir imagem real ou dados pessoais do Guerreiro(a)            |

- **A evolução real é a força do personagem.** Pontos regulares, pontos extras, poderes e
  badges entram na partida como as "virtudes" do personagem: quem evoluiu mais na vida real
  começa mais forte e se distingue dos demais. É o que dá utilidade lúdica ao aprendizado.
- Jogar muito não sobe ninguém no ranking, e a **ausência de qualquer endpoint de escrita**
  elimina, por construção, a fraude por automação: não há o que automatizar.
- **Batalhas físicas seguem o mesmo padrão**: a ponte Nexus → API da Batalha de Laser envia as
  estatísticas da partida para a API, que **lança a atividade realizada** — o crédito de
  pontos é da atividade validada, não do jogo. É o modelo de referência para qualquer batalha
  presencial futura, de qualquer área.
- A API pública e aberta permite que **terceiros** construam novos jogos sob o mesmo contrato.
- **O protagonismo vale também aqui**: o código do App 04 é aberto e legível, e alterá-lo é
  atividade de trilha — o Guerreiro(a) não é só usuário do jogo, é um dos seus construtores.

#### Como a virtude vira atributo

**Definição vigente — mapa fixo, igual para todo personagem.** Toda virtude que o jogo lê tem
destino declarado na partida, e nenhuma fica de fora:

| Virtude lida do Guerreiro(a) | Atributo do personagem na partida                                   |
| ---------------------------- | ------------------------------------------------------------------- |
| Pontos regulares             | **Vitalidade** — quanto o personagem aguenta antes de ser derrotado |
| Pontos extras                | **Energia** — o que custeia o uso das habilidades na partida        |
| Nível do poder (1–5)         | **Escalonamento** — multiplica vitalidade, energia e dano           |
| Poder conquistado            | **Habilidade especial** — uma por poder, com efeito próprio         |
| Badge                        | **Passiva** — efeito permanente enquanto a partida durar            |

Três exigências acompanham o mapa:

- **Monotonia.** Evoluir na vida real nunca produz personagem pior em atributo nenhum.
- **Transparência.** A tela de escolha mostra de qual virtude veio cada atributo — é o que
  faz da partida uma leitura do próprio progresso.
- **Balanceamento é conteúdo, não regra de plataforma.** Os números que convertem virtude em
  atributo vivem no código aberto do jogo e mudam em atividade de trilha; o que a plataforma
  fixa é o mapa acima e as duas exigências anteriores.
