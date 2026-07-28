# 05 — Implantação e Operação

## 1. Estratégia de implantação

O projeto será implantado **inicialmente em uma comunidade próxima à residência do
fundador** (piloto), e deve servir de **modelo de implantação para qualquer comunidade do
país**.

> **Case de referência: [Comunidade Guerreira Zeferina](10-case-01-guerreira-zeferina.md)**,
> em Salvador (BA) — **Ciclo 01, de agosto a dezembro de 2026**. A comunidade já foi palco da
> edição de 2024 do Robô Educa (então chamada *Inova Comunidade*), o que significa começar
> com relação prévia e memória do território. Hipóteses, metas e critérios de avaliação do
> ciclo estão no [documento 10](10-case-01-guerreira-zeferina.md).

A implantação combina presença física (pontos de apoio, encontros) com presença digital
(Web App responsivo, acessível pelo celular), justamente porque o público-alvo tem acesso
desigual a equipamentos.

## 2. Estrutura física — Pontos de apoio

- **Pontos de apoio nas comunidades**: hackerspace, fab lab, coworking.
- São a base para aulas presenciais, montagem de kits, batalhas e atividades de culminância.
- **Equipamentos disponíveis no ponto de apoio** — notebooks, smartphones e tablets — são o
  que viabiliza a **dinâmica assíncrona dos encontros** (§3): o jogador usa o aparelho
  disponível quando chega a sua vez, sem exigir que cada um traga o seu. O parque de
  equipamentos é recurso com lastro como qualquer outro
  ([04](04-modelo-economico-e-sustentabilidade.md)) e é uma das finalidades previstas de
  campanha de financiamento
  ([04 §2](04-modelo-economico-e-sustentabilidade.md#2-fontes-de-receita)).
- Custo operacional previsto: diária do professor para o ponto de apoio
  ([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md#3-despesas-para-funcionamento)).
- **Guarda do acervo didático.** Os 298 livros doados pelo Goethe-Institut ficam distribuídos
  entre os pontos de apoio, com **controle de quantos exemplares estão em cada local e em que
  estado**, dimensionado pelo tamanho das turmas de cada ponto (ver abaixo).

### Acervo didático: guarda e conservação

Os livros são **material de apoio** das trilhas [Robô Educa](06-robo-educa.md) e
[Batalha de Laser](07-batalha-de-laser.md)
([02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-goethe-institut)).

**Decisão pendente: doar ou reaproveitar.** Não está definido se os exemplares serão
**doados aos jogadores** ou **reaproveitados** entre turmas. As duas hipóteses:

| | Doação ao jogador | Reaproveitamento |
|---|---|---|
| Efeito no jogador | Livro próprio em casa; a família ganha um bem cultural | Acesso durante o módulo; devolve ao final |
| Alcance | ~298 jogadores, uma única vez | Turmas sucessivas, por anos |
| Registro no ledger | Baixa definitiva do acervo | Patrimônio permanente, com controle de guarda |
| Risco | Acervo se esgota; turmas seguintes ficam sem material | Perda e desgaste ao longo do tempo |

**Encaminhamento sugerido — regime misto**, que aproveita a assimetria do inventário:

- **Linha Alpha (252 exemplares, volume alto):** empréstimo com **doação ao final da
  trilha** para quem a concluir. O livro vira **recompensa e troféu**, não item de controle.
- **Linha Include I (46 exemplares, escassa):** **acervo permanente do ponto de apoio**,
  consulta em bancada, sem saída.

Assim o jogador leva um livro para casa como marca da conquista, e o material raro continua
disponível para todas as turmas seguintes.

#### Estratégia de conservação (caso haja reaproveitamento)

O princípio é **conservação por cuidado e orgulho, não por medo de punição**:

1. **Tombamento e ficha de vida.** Cada exemplar recebe um número de tombo e um registro na
   gestão (App 03): título, ponto de apoio, estado de conservação e histórico de quem o
   usou. O jogador vê na Área do Jogador (App 05) **quais jogadores cuidaram daquele livro
   antes dele** — o exemplar carrega uma linhagem, e ninguém quer ser o elo que quebrou a
   corrente.
2. **Primeira aula do módulo = ritual de posse.** Encapar o livro, identificar o exemplar e
   registrar o estado em que o recebeu é a **primeira atividade pontuada** da trilha. Ensina
   cuidado com material e coloca o jogador como responsável desde o início.
3. **Empréstimo registrado no painel do dia.** Retirada e devolução são lançadas pelo Mestre
   na gestão; o painel do dia mostra as **devoluções pendentes** antes do fim da aula
   ([03 §3](03-plataforma-e-arquitetura.md#3-frontend-01--gestão-app-03)).
4. **Badge "Guardião do Acervo".** Devolver em bom estado ao fim do módulo rende badge e
   pontos. Guardiões reincidentes ganham prioridade para **levar livro para casa** e podem
   ser convidados a **cuidar do acervo do ponto de apoio** como voluntários
   ([§7](#7-formação-de-mestres-e-multiplicadores)).
5. **Guarda compartilhada pela equipe.** Cada equipe responde por um conjunto de exemplares,
   como já responde por um desafio. Cuidar do material do colega conta como
   **mérito extra por auxílio aos colegas**
   ([02 §4](02-conceito-do-jogo-e-gamificacao.md#resultados-de-atividade-lançados-pela-gestão)).
6. **Kit de conservação com lastro.** Papel para encapar, fita e etiquetas são **recursos
   como qualquer outro**: precisam ser providos por Mestre ou Apoiador para a atividade
   acontecer ([04](04-modelo-economico-e-sustentabilidade.md)).
7. **Reposição solidária, nunca cobrança à família.** Perda ou dano **não gera dívida para o
   jogador nem para os responsáveis** e não impede a participação. A reposição entra como
   **necessidade de recurso** a ser aportada por Apoiador. Cobrar de família em situação de
   vulnerabilidade contradiz o "sem miséria" e afastaria justamente quem o projeto quer
   alcançar.
8. **Conferência de inventário a cada módulo**, com o resultado publicado na prestação de
   contas do acervo — transparência que também presta contas ao Apoiador que doou.

> **Sobre pontuação negativa:** o descuido reiterado e deliberado com o material é
> descumprimento de regra e cabe no dispositivo já previsto
> ([02 §4](02-conceito-do-jogo-e-gamificacao.md#pontuação-negativa)). Livro rasgado por
> acidente, chuva ou casa sem espaço adequado **não é infração** — é custo previsto de operar
> em território real. A distinção precisa estar explícita no código de conduta, senão a regra
> vira instrumento de exclusão.

## 3. Roteiro da aula presencial

### Definição vigente: o encontro é assíncrono

**Os encontros presenciais têm dinâmica assíncrona.** Não há uma turma única avançando em
bloco: **à medida que os jogadores vão chegando** e se organizando em equipes, eles **começam
a realizar as atividades da trilha em que estão atuando, no seu próprio ritmo**, usando os
**notebooks, smartphones e tablets disponíveis**, com a ajuda do(s) **Mestre(s) presente(s)**.

Por que assim:

- **A chegada é escalonada na vida real** — transporte, escola, tarefa de casa, irmão menor.
  Um roteiro em bloco pune quem chega atrasado; o assíncrono simplesmente o acolhe no ponto
  em que ele está.
- **Cada jogador está em um ponto diferente da trilha.** A progressão do jogo é por
  **nível de dificuldade, não por idade nem por data de entrada**
  ([02 §4](02-conceito-do-jogo-e-gamificacao.md#4-atividades-e-desafios)) — o encontro
  precisa refletir isso.
- **Os equipamentos são compartilhados e limitados.** Atividade assíncrona distribui o uso
  dos aparelhos ao longo do encontro, em vez de exigir um dispositivo por jogador ao mesmo
  tempo.
- **O Mestre vira mentor de bancada**, e não palestrante: circula entre equipes, atende quem
  travou e libera quem está adiantado — que passa a ajudar o colega, o que já é
  **mérito extra por auxílio aos colegas**
  ([02 §4](02-conceito-do-jogo-e-gamificacao.md#resultados-de-atividade-lançados-pela-gestão)).

Consequências operacionais:

- O **onboarding roda continuamente** durante o encontro, não só na abertura — a App 01
  atende quem chega a qualquer hora ([03 §5](03-plataforma-e-arquitetura.md#5-frontend-03--onboarding-cadastro-e-registro-de-presença)).
- A **App 05 (Área do Jogador)** é o que sustenta a autonomia: é ela que diz a cada jogador
  qual é o próximo ponto da sua trilha, sem depender do Mestre para saber o que fazer
  ([03 §2.1.4](03-plataforma-e-arquitetura.md#214-app-05--área-do-jogador)).
- O **painel do dia** (App 03) é o instrumento de controle do encontro assíncrono: quem
  chegou, quem está em qual atividade, o que já foi lançado e o que ainda falta
  ([03 §3](03-plataforma-e-arquitetura.md#3-frontend-01--gestão-app-03)).

### Momentos do encontro

Os momentos abaixo compõem o encontro, mas **nem todos são simultâneos para todos**. Os
momentos **2 e 5 são assíncronos** — cada equipe os realiza quando chega e no seu ritmo. Os
momentos **3, 4 e 6 são coletivos**, com horário marcado dentro do encontro, e é neles que a
turma inteira se junta.

Não é camisa de força — é a espinha dorsal que garante que cada aula tenha acolhimento,
prática, inspiração e voz do jogador.

| # | Momento | Ritmo | O que acontece |
|---|---|---|---|
| 1 | **Onboarding** | **Contínuo** | Cadastro de novos jogadores e registro de presença, pela **App 01** — interação por áudio ou texto, conforme os jogadores chegam ([03 §5](03-plataforma-e-arquitetura.md#5-frontend-03--onboarding-cadastro-e-registro-de-presença)) |
| 2 | **Atividades práticas — Computer Science Unplugged** | **Assíncrono** | Lógica, algoritmos e pensamento computacional **sem computador**: papel, corpo, jogos, materiais do dia a dia. Boa porta de entrada para quem chegou e ainda não pegou um aparelho |
| 3 | **Bate-papo on-line com mentores e convidados** | Coletivo | Conversa ao vivo com profissionais e referências — aproxima o mundo da tecnologia da realidade do jogador |
| 4 | **Momento GOAT / The Best / "Podemos nos tornar os melhores"** | Coletivo | Vídeo ou slides sobre personalidades **mulheres, negras e indígenas** que impactaram positivamente a sociedade. Momento inspirador e de identificação ([01 §4](01-visao-valores-e-proposito.md#o-lema)) |
| 5 | **Trabalho de trilha / Desafio do dia** | **Assíncrono** | O grosso do encontro: cada equipe avança nos **pontos da sua trilha** e na atividade pontuada — individual, em equipe, de coleta de dados do território — com apoio do Mestre. O **Quiz ao Vivo** (§4) é a exceção coletiva deste momento |
| 6 | **Encerramento com apresentação livre** | Coletivo | Cada jogador (ou equipe) mostra o que construiu e/ou aprendeu na aula. Fecha o ciclo e treina expressão pública |

Observações operacionais:

- **Os momentos coletivos são âncoras, não interrupções arbitrárias.** Convém concentrá-los
  na segunda metade do encontro, quando a maior parte da turma já chegou — assim quem chega
  cedo não fica esperando e quem chega tarde não perde o essencial.

- O **momento GOAT** é onde os valores do projeto (antirracismo, combate à violência
  contra a mulher, valorização dos povos originários, identidade) entram de forma direta e
  concreta, ligados a pessoas reais.
- O **encerramento** alimenta o portfólio: é dele que saem fotos, vídeos e registros de
  culminância (sempre respeitando as regras de consentimento e LGPD).
- Cada aula só acontece com os **recursos providos** por mestres/apoiadores
  ([04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md)).

## 4. Atividade-modelo: Quiz ao Vivo

Exemplo de atividade para as aulas presenciais, encaixável no **"Desafio do dia"** (momento 5
do roteiro da §3). É uma competição rápida entre equipes, com pontuação lançada
automaticamente na plataforma.

**Como funciona:**

1. Os jogadores presentes na aula são organizados em **equipes**.
2. As perguntas são **pré-cadastradas pelo curador da aula (Mestre)**, em formato de
   múltipla escolha: a) resposta 1; b) resposta 2; c) resposta 3; etc.
3. Ao dar o *start* no quiz, **uma pergunta é exibida e enviada simultaneamente para todos
   os dispositivos logados na aula**.
4. Cada equipe **se consulta internamente**, define qual considera a resposta correta e
   clica na opção escolhida.
5. O sistema identifica a **primeira equipe que respondeu corretamente** e **registra a
   pontuação** correspondente.

**Por que funciona bem no presencial:** a etapa de consulta dentro da equipe é onde o
aprendizado acontece — quem sabe explica para quem não sabe, o que se conecta diretamente ao
**mérito extra por auxílio aos colegas**
([02 §4](02-conceito-do-jogo-e-gamificacao.md#resultados-de-atividade-lançados-pela-gestão)).

**O que a atividade exige das aplicações:**

- **App 03 (gestão)** — cadastro do banco de perguntas pelo curador e condução da partida
  (start, avanço de pergunta, encerramento, apuração)
  ([03 §3](03-plataforma-e-arquitetura.md#3-frontend-01--gestão-app-03)).
- **App 05 (área do jogador)** — recebimento da pergunta e envio da resposta pelo celular da
  equipe.
- **Sincronização em tempo real** entre os dispositivos logados na aula e critério de
  desempate por **ordem de chegada da resposta** — com tolerância a rede instável, que é a
  regra nos pontos de apoio.

> **A definir:** pontuação atribuída à vitória no quiz e às respostas corretas subsequentes;
> se responde a equipe inteira ou um representante; comportamento quando duas respostas
> chegam praticamente juntas; se o quiz roda com um único dispositivo por equipe ou um por
> jogador.

## 5. Formatos de atividade

| Formato | Descrição |
|---|---|
| Encontros presenciais | Oficinas e treinamentos nos pontos de apoio |
| Atividades on-line | Conteúdo entre encontros; trilhas |
| Desafios on-line | Semanais, pontuados |
| Desafios presenciais | Semanais, pontuados; batalhas |
| Coleta de dados do território | Contínua, alimenta a Comunidade Virtual |
| Quiz ao Vivo | Competição entre equipes durante a aula presencial (§4) |
| Atividades de culminância | Apresentação pública de trabalhos, encerramento de módulos |

## 6. Cursos presenciais

- **Duração:** conforme as trilhas.
- **Formato:** aulas presenciais + desafios.
- **Material didático:** as trilhas do Poder da IA e Robótica contam com o **acervo Include
  doado pelo Goethe-Institut** — 252 exemplares da linha Alpha permitem **um livro por
  jogador** em turmas inteiras; os 46 exemplares da linha Include I são material escasso, de
  uso compartilhado ou de formação de mestres e voluntários
  ([02 §3](02-conceito-do-jogo-e-gamificacao.md#acervo-didático-de-apoio--coleção-include-goethe-institut)).
- **Custos a levantar por curso:** professor + material + ajuda de custo para
  estagiários + lanche.
- **Gratuitos para os alunos** das comunidades (financiados por parceiros/doações —
  ver [04-modelo-economico-e-sustentabilidade.md](04-modelo-economico-e-sustentabilidade.md#4-parcerias)).
- Ao final dos módulos, alunos gravam vídeo com realizações e agradecimentos aos parceiros.

## 7. Formação de Mestres e multiplicadores

- **Formação de mentores** é linha de ação explícita do projeto.
- O caminho natural é a própria gamificação: o jogador Nível 4 (apoia os colegas) evolui
  para o **Nível 5**. **Ao concluir o Nível 5, o jogador é considerado *Mestre Aprendiz* e
  está apto ao treinamento de multiplicador**
  ([02 §7](02-conceito-do-jogo-e-gamificacao.md#7-níveis-e-badges-gamificação)).
- O reconhecimento é **por trilha ou por poder**: o badge de Mestre Aprendiz é conquistado
  no conteúdo específico em que o jogador se destacou.
- **Multiplicadores** formados abrem novos cursos em novas comunidades — é o mecanismo de
  escala do projeto.
- **Admissão como Mestre na plataforma** exige dois requisitos, sem exceção:
  1. **Cadastro feito por um Admin** (Organizadores/Equipe técnica) — não há autocadastro;
  2. **Habilidade comprovada por materiais ou artefatos publicados na plataforma**
     (atividades propostas, aulas presenciais e/ou gravadas, videoaulas, exemplos de
     código, projetos construídos).
- O mesmo vale para **Apoiadores**: cadastro por Admin, com o apoio comprovado e
  registrado ([02 §1](02-conceito-do-jogo-e-gamificacao.md#1-os-elementos-do-jogo-personas)).
- **Estagiários** locais recebem ajuda de custo — porta de entrada remunerada para jovens
  da própria comunidade.

### Voluntários de suporte nos pontos de apoio

- **Formação de voluntários para o suporte diário nos pontos de apoio**, recrutados entre os
  **jogadores que atingirem o badge de Mestre Aprendiz** em trilhas ou poderes específicos.
- O voluntário dá suporte no dia a dia do ponto de apoio — recepção, apoio ao uso das
  aplicações, ajuda nas atividades práticas — sempre sob supervisão de um Mestre ou Admin.
- É o degrau entre "jogador avançado" e "multiplicador": experiência prática de ensino antes
  de assumir uma turma.
- Aplicam-se as regras de salvaguarda das atividades presenciais — nenhum adulto ou
  voluntário sozinho com criança, e canal de denúncia disponível
  ([09 §2](09-topicos-em-aberto-e-sugestoes.md#proteção-da-criança-e-do-adolescente-prioridade-máxima)).

## 8. Comunicação e divulgação

- **Formação de equipe de divulgação nas redes sociais** (linha de ação explícita).
- Canais: Instagram, Facebook, YouTube e TikTok — **canais institucionais** de divulgação do
  projeto, não canais de uso da plataforma (os cards dos jogadores não exibem redes sociais
  pessoais, por proteção de menores/LGPD).
- Narrativa/personagens: **os irmãos Susy e Otávio, os Rôbróders e o professor Carlos
  Trenell** (vídeo de apresentação da plataforma).
- O **"Poder das Redes"** conecta divulgação e formação: os próprios jogadores aprendem
  produção de conteúdo produzindo para o projeto. A trilha correspondente é a de
  **Social Media / Geração de Áudio e Vídeo para Redes Sociais**
  ([02 §3](02-conceito-do-jogo-e-gamificacao.md#demais-trilhas-previstas)), que forma a equipe de
  divulgação com os próprios jogadores.
- Vídeos de culminância dos alunos são material de divulgação e prestação de contas.

## 9. Papel dos responsáveis e da família

- Envio da **evolução do aluno aos responsáveis pela própria plataforma** (área do
  responsável no Web App e/ou e-mail).
- **Atividades em família** valem pontuação dobrada (20 pts) — engajar a família é
  estratégia de permanência.
- **Equipe Familiar** como modalidade de equipe.
- Consentimentos sob responsabilidade da família: divulgação do perfil na vitrine e
  captura de imagem para registro de presença
  ([03 §5.3](03-plataforma-e-arquitetura.md#53-requisitos-de-proteção-de-dados-lgpd-aplicada)).

## 10. Replicabilidade

Condições para que qualquer comunidade replique o modelo:

1. **Código open source** ([03-plataforma-e-arquitetura.md](03-plataforma-e-arquitetura.md)).
2. **Backend como API aberta** para novos frontends locais.
3. **Comunidades Virtuais** como unidade de organização — cada território tem sua
   representação e sua base de dados.
4. **Modelo econômico com lastro local**: atividades só acontecem com recursos providos
   por mestres/apoiadores da própria rede.
5. **Trilhas prontas** para o primeiro ciclo: [Robô Educa](06-robo-educa.md) e
   [Batalha de Laser](07-batalha-de-laser.md).
6. **Multiplicadores** formados pela gamificação.

**[Proposta]** Criar um **"Kit de Implantação"** (playbook): passo a passo documentado
para uma nova comunidade — requisitos mínimos (ponto de apoio, 1 mestre, 1 apoiador),
checklist legal (termos de consentimento, LGPD/ECA), materiais de divulgação editáveis e
orçamento-modelo de um primeiro ciclo de oficinas. É o documento que transforma "open
source" em "replicável de fato".

**[Proposta]** Definir a **entidade jurídica/governança** da iniciativa (associação,
OSCIP, coletivo com fiscal sponsor) — necessária para receber doações, firmar parcerias e
participar de editais.

## 11. Fases sugeridas de implantação do piloto **[Proposta]**

Todas as entregas de software desta etapa são **Web Apps responsivos, Mobile First**
([03 §2](03-plataforma-e-arquitetura.md#2-canais--meios-de-acesso)).

O piloto a que estas fases se referem é o
**[Case 01 — Guerreira Zeferina](10-case-01-guerreira-zeferina.md)**. O **Ciclo 01
(ago–dez/2026)** tem como meta o **MVP**: credenciamento de jogadores, cadastro da comunidade
digital e as **trilhas 1 e 2** em operação de agosto a novembro — o que corresponde, em
termos das fases abaixo, a **chegar até a Fase 3** dentro do ciclo. As fases seguintes ficam
para ciclos posteriores.

| Fase | Entrega | Depende de |
|---|---|---|
| 0 — Fundação | Código de conduta, termos de consentimento, identidade visual, comunidade piloto definida | — |
| 1 — Onboarding + vitrine | **App 01** (cadastro/presença por áudio ou texto) + vitrine pública + API de personas | PRD-01/02/03 ([08-base-para-prds.md](08-base-para-prds.md)) |
| 2 — Jogo mínimo | **App 03** (gestão, entradas manuais e painéis do dia), poderes e a **1ª trilha — Robô Educa** publicada e pontuando | Fase 1 |
| 3 — Primeiro ciclo presencial completo | Aulas com o roteiro da §3 + **App 02** (assistente por voz e Modo Ouvinte) + Quiz ao Vivo + **2ª trilha — Batalha de Laser** + culminância com vídeo | Fase 2 + ponto de apoio + recursos com lastro |
| 3.5 — Acervo em operação | Tombamento dos livros, mapeamento capítulo → ponto de trilha e estratégia de conservação implantada | Fase 2 + decisão doação x reaproveitamento |
| 4 — Área do jogador e jogo | **App 05** (guia das trilhas) e **App 04** (jogo em JavaScript) | Fase 2 |
| 5 — Comunidade Virtual | Coleta de dados do território e painel público por comunidade | Fase 2 |
| 6 — Economia visível | Livro-razão público, Poder Econômico, relatórios de transparência | Fase 3 |
| 7 — Escala | Personalização por IA, formação de multiplicadores e voluntários, kit de implantação para a 2ª comunidade | Fases 3–6 |
