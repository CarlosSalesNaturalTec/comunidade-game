# 09 — Tópicos em Aberto e Propostas

Este documento reúne (a) pontos que ainda dependem de decisão do fundador e (b) propostas
de novos tópicos e abordagens. Nada aqui é decisão tomada — é pauta.

## 1. Decisões pendentes

| Tema | Situação / encaminhamento |
|---|---|
| Nome do projeto | Adotado: **Comunidade Game**. Alternativa em avaliação: **Inova Comunidade**. Decidir antes de registrar domínio, marca e identidade visual. |
| Lema "GOAT / The Best / Podemos ser os melhores" | Já é momento fixo da aula presencial ([05 §3](05-implantacao-e-operacao.md#3-roteiro-da-aula-presencial)). Decidir se vira também slogan oficial de comunicação e se a versão longa precisa de uma forma curta para peças gráficas (ex.: **"Vamos ser os melhores"**, **"O melhor se constrói"**). |
| Pontuação das recompensas | Kits de alimentos e demais recompensas: valores atuais são apenas sugestão ([02 §8](02-conceito-do-jogo-e-gamificacao.md#8-recompensas)). |
| Provedor de IA e de reconhecimento facial do onboarding | Custo, privacidade e processamento no dispositivo x nuvem ([08 PRD-04](08-base-para-prds.md#prd-04--app-01-onboarding-cadastro-e-registro-de-presença)). |
| Prazo de retenção da foto de presença | Definir número em dias/meses e rotina de exclusão automática. |
| **Modo Ouvinte do App 02** | O assistente acompanha o que é falado na aula. Definir formalmente: critério de acionamento, o que é transcrito e por quanto tempo é retido, base legal e forma do aviso/consentimento a jogadores e responsáveis, e a alternativa para quem recusar ([03 §4](03-plataforma-e-arquitetura.md#4-app-02--assistente-por-voz-e-modo-ouvinte)). **Prioridade alta** — envolve captação de voz de crianças. |
| ~~Canal de comunicação com os responsáveis~~ | **Decidido:** a **App 07 — Área dos pais e responsáveis** é o canal oficial ([03 §9](03-plataforma-e-arquitetura.md#9-app-07--área-dos-pais-e-responsáveis), [08 PRD-13](08-base-para-prds.md#prd-13--app-07-área-dos-pais-e-responsáveis)). Segue em aberto **apenas**: se o acesso é por login próprio do responsável ou por vínculo ao cadastro do jogador; prazos formais de resposta às solicitações; se há notificação ativa por e-mail além da consulta no Web App; e como atender responsável sem smartphone ou sem e-mail. |
| **Pontuação da coleta de dados do território** | A coleta pontua de forma **recorrente enquanto a série se mantiver ativa** ([02 §1](02-conceito-do-jogo-e-gamificacao.md#registro-temporal-e-pontuação-enquanto-a-coleta-durar)). Falta definir os números: **cadência e valor em pontos por tipo de coleta**, **janela de tolerância** antes de considerar a série interrompida, **teto de pontos por período** e a **mecânica de verificação da veracidade** do dado. **Prioridade alta** — é a mecânica que sustenta a Comunidade Virtual e a que mais convida à fraude. |
| Pontuação e regras do Quiz ao Vivo | Pontos da vitória, formato de resposta (equipe x representante), critério de desempate e nº de dispositivos por equipe ([05 §4](05-implantacao-e-operacao.md#4-atividade-modelo-quiz-ao-vivo)). |
| Mecânica do jogo (App 04) | **Decidido:** o jogo **não gera pontuação na plataforma, apenas a consome** ([03 §6](03-plataforma-e-arquitetura.md#6-app-04--jogo-em-javascript)). Seguem em aberto: **gênero e mecânica** do jogo, o que os pontos compram dentro dele e a confirmação da **engine Phaser.js** ([08 PRD-12](08-base-para-prds.md#prd-12--app-04-jogo-em-javascript)). |
| Stack de análise de movimentos (Poder da Capoeira) | **Adiado — ciclo futuro.** As trilhas de **Rima** e **Capoeira** só serão definidas e implementadas depois desta etapa ([02 §3](02-conceito-do-jogo-e-gamificacao.md#demais-trilhas-previstas)), então a escolha da stack sai do caminho crítico. Quando voltar à pauta: **sugestão MediaPipe (Python)** para captação da pose, TensorFlow como alternativa para classificar os movimentos, e a decisão pendente de processar **no dispositivo ou no servidor** — é vídeo de criança, e a resposta muda a exposição de dados. |
| **Desafios extras de Apoiadores** | **Decidido:** valem **pontos extras** além da recompensa, computados isoladamente; **sem teto** de desafios simultâneos, porque cada um é **aprovado ou não por um Admin**; nos desafios **abertos**, a disputa é para **todos os que concluírem**, com **quantidade** de recompensas declarada (uma, para quem concluir primeiro, ou várias, até esgotar); existe também a modalidade **direcionada** — desafio destinado a um jogador específico, com justificativa do vínculo registrada e aprovada por Admin ([04 §5](04-modelo-economico-e-sustentabilidade.md#definições-vigentes-dos-desafios-extras), [02 §4](02-conceito-do-jogo-e-gamificacao.md#desafio-extra-direcionado)). Segue em aberto **apenas** o **formato do relatório de efetividade** entregue ao Apoiador. |
| **Poder do Território** | **Decidido:** o registro de dados do território é um **poder próprio** — "Poder do Território" (registro e ciência de dados, *Data Science*), com progressão e badges por sustentar séries de coleta ([02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)). |
| **Código de Conduta** | **Decidido:** co-criado com os jogadores na **primeira interação presencial**; a **versão prévia (modelo básico)** está em [13-codigo-de-conduta-versao-previa.md](13-codigo-de-conduta-versao-previa.md), a ser discutida, revisada e complementada com a turma. |
| ~~Acervo Include: doar ou reaproveitar~~ | **Decidido: regime misto.** Os 252 exemplares da **linha Alpha são doados ao jogador quando ele começa a trilha**; os 46 da **linha Include I ficam como acervo permanente** do ponto de apoio ([02 §3](02-conceito-do-jogo-e-gamificacao.md#posse-dos-livros--regime-misto), [05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)). |
| Estratégia de conservação do acervo permanente | Validar a estratégia da linha Include I (tombamento, ficha de vida do exemplar, uso de bancada com retirada registrada, badge "Guardião do Acervo", guarda por equipe, reposição solidária) ([05 §2](05-implantacao-e-operacao.md#b-acervo-permanente-do-ponto-de-apoio--linha-include-i-46-exemplares)). A **distinção entre descuido deliberado e dano acidental** está no [Código de Conduta — versão prévia](13-codigo-de-conduta-versao-previa.md#descuido-deliberado--dano-acidental). |
| Valoração e guarda do acervo e dos kits | Como o acervo e os **30 kits MDF** entram no livro-razão (valor de mercado, simbólico ou contagem física) e quem responde pela guarda em cada ponto de apoio ([04 §1](04-modelo-economico-e-sustentabilidade.md#primeiro-aporte-registrado--acervo-didático-e-kits-do-goethe-institut)). |
| Mapeamento dos livros nas trilhas | Identificar o conteúdo de cada título e indicar **qual capítulo apoia qual ponto** das trilhas Robô Educa e Batalha de Laser. Trabalho de leitura, não de criação de trilha nova. |
| Licenças | Código (AGPL/MIT?) e conteúdo educacional (Creative Commons?). |
| Orquestrador "do explore ao merge" | Automação do fluxo de desenvolvimento com agentes de IA. Definir se entra em `CONTRIBUTING.md`/automação do repositório. |
| Uso do Slack no fluxo de desenvolvimento | Ferramenta de comunicação do time. Decidir. |
| Git como canal entre agentes e humanos | Proposta: GitHub Issues + labels como canal padrão; Discussions para debate; Projects para roadmap. |
| Submarcas | **Rôbróders** e **Robô Educa** podem nomear subprodutos (ex.: os kits "Rôbróders"). |
| Universo dos personagens | Susy, Otávio, Rôbróders e prof. Carlos Trenell — formalizar roteiro e identidade da narrativa. |
| **Case 01 — Guerreira Zeferina** | Documentado em [10](10-case-01-guerreira-zeferina.md). Pendentes do case: ponto de apoio físico, calendário do Ciclo 01 (ago–dez/2026), tamanho da turma, **metas numéricas das hipóteses H1 e H2** e resgate da memória da edição de 2024 (Inova Comunidade) ([10 §7](10-case-01-guerreira-zeferina.md#7-pontos-a-definir-do-case)). |

## 2. Propostas de novos tópicos **[Proposta]**

### Proteção da criança e do adolescente (prioridade máxima)
- **Já definido:** LGPD considerada em TODO o projeto; jogadores representados por avatares
  (nunca imagem real) na vitrine; **adesão em duas etapas** — cadastro livre já permite
  participar, e a **divulgação pública do histórico/perfil** exige autorização dos pais ou
  responsáveis; cards de jogadores **sem links para redes sociais nem contato direto**;
  foto de presença com **finalidade única** e alternativa para quem recusar
  ([03 §3.3](03-plataforma-e-arquitetura.md#33-requisitos-de-proteção-de-dados-lgpd-aplicada));
  **App 07** como canal em que o responsável concede e **revoga** autorizações, exerce
  direitos de recusa e vê **quais dados da criança estão armazenados**
  ([03 §9](03-plataforma-e-arquitetura.md#9-app-07--área-dos-pais-e-responsáveis)).
- A detalhar: política de privacidade formal; papel de "encarregado de dados" (DPO).
- A detalhar: **guarda permanente dos dados de território com o coletor identificado** — a
  regra vigente é manter a série **e a autoria**, sem anonimização no armazenamento, com
  anonimização apenas na saída
  ([02 §1](02-conceito-do-jogo-e-gamificacao.md#guarda-permanente-dos-dados-com-o-coletor-identificado)).
  Falta definir: **base legal** para retenção indefinida e nominal de dado produzido por
  criança; o que exatamente a plataforma responde a um **pedido de exclusão** do responsável,
  já que a série do território não é apagada; e como a **agregação de saída** impede
  reidentificação a partir da granularidade fina do registro (bloco, quadra).
- A detalhar: consentimento específico para vídeos de culminância e fotos de eventos com
  jogadores — vale também para o material produzido na trilha de **Social Media**
  ([02 §3](02-conceito-do-jogo-e-gamificacao.md#demais-trilhas-previstas)).
- A detalhar: **captação de voz em sala** pelo Modo Ouvinte do App 02 — a mesma exigência de
  finalidade declarada, minimização, retenção definida e alternativa para quem recusar que
  se aplica à foto de presença.
- A detalhar: **verificação e supervisão dos voluntários** recrutados entre jogadores
  Mestres Aprendizes, muitos deles ainda menores de idade
  ([05 §7](05-implantacao-e-operacao.md#7-formação-de-mestres-e-multiplicadores)).
- Mediação de toda interação adulto–criança pela plataforma (incl. patrocinadores).
- Política de salvaguarda (*safeguarding*) para atividades presenciais: verificação de
  mestres/voluntários, adulto nunca sozinho com criança, canal de denúncia.
- **Dados de território x privacidade**: registrar rua/bloco/quadra sem permitir inferir o
  endereço de uma criança específica.

### Governança open source
- `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`.
- Modelo de decisão (quem aprova mudanças de rumo) e marca (quem pode usar o nome do
  projeto ao replicar).

### Entidade jurídica e compliance
- **Já definido:** a pessoa jurídica vinculada ao projeto é a **Robô Educa — Kits Robóticos
  Educacionais** (CNPJ 51.730.395/0001-19), responsável legal **Carlos Antonio Sales**, o
  próprio fundador. É ela que recebe doações (PIX) e assina termos — como o **Termo de
  Doação do acervo Include**, firmado com o Goethe-Institut (Salvador)
  ([04 §1](04-modelo-economico-e-sustentabilidade.md#pessoa-jurídica-vinculada-ao-projeto)).
- **Ainda em aberto:** forma jurídica **sem fins lucrativos** para editais e recursos
  públicos (associação, OSCIP, fiscal sponsor), que normalmente não aceitam empresa como
  proponente. Os dois arranjos podem coexistir — decidir quando e como.
- **Ainda em aberto:** separação contábil entre a atividade comercial da empresa e os
  recursos do projeto — sem ela, a "transparência radical" do livro-razão fica sem
  contrapartida no mundo real.
- Prestação de contas formal conectada ao ledger de transparência
  ([04](04-modelo-economico-e-sustentabilidade.md)).

### Indicadores de impacto
- Métricas de aprendizado, retenção, atividades realizadas, dados de território
  registrados e recursos movimentados — definidas antes do piloto para permitir comparação
  (baseline).

### Acessibilidade e inclusão
- Acessibilidade digital (WCAG) e de conteúdo (linguagem simples).
- Estratégia para jogadores sem smartphone próprio (contas familiares, ponto de apoio).
- Recorte de gênero: metas de participação de meninas, coerente com a causa
  antifeminicídio; mestras mulheres como referência.

### Segurança física nas atividades
- Normas de segurança para laser, eletrônica e ferramentas nas oficinas
  ([07](07-batalha-de-laser.md#integração-com-a-plataforma-proposta)).

### Poderes alinhados aos valores
- "Poder da Ancestralidade" e "Poder do Cuidado"
  ([02 §2](02-conceito-do-jogo-e-gamificacao.md#2-poderes-habilidades)) — o **Poder do
  Território** já integra o catálogo como definição vigente.

### Currículo de temas transversais
- Como cada atividade técnica abre paralelo com outras áreas do conhecimento e com os
  temas do projeto (racismo, violência contra mulheres, identidade, povos originários) —
  um guia prático para os Mestres, não apenas princípio no papel.

### Kit de Implantação (playbook de replicação)
- O documento que torna o modelo replicável de fato
  ([05 §10](05-implantacao-e-operacao.md#10-replicabilidade)).

### Parcerias institucionais
- Escolas públicas: protocolo de parceria com secretarias de educação; alinhamento
  PNED/BNCC como argumento.
- Universidades: estagiários/extensão como força de trabalho e pesquisa.
- Instituições que possam **consumir os dados** das Comunidades Virtuais (prefeitura,
  defesa civil, associações de moradores) — devolvendo valor ao território.

## 3. Próximos passos sugeridos **[Proposta]**

1. Validar esta documentação e corrigir o que estiver incoerente com a visão do fundador.
2. Decidir os itens da tabela §1 — em especial nome do projeto, licenças e provedor de IA.
3. Rodar a Fase 1 de elicitação de PRD com o
   [PRD-01 (API)](08-base-para-prds.md#prd-01--backend-api-núcleo) e o
   [PRD-04 (Onboarding)](08-base-para-prds.md#prd-04--app-01-onboarding-cadastro-e-registro-de-presença).
4. Redigir o termo de autorização dos responsáveis e o termo de consentimento para captura
   de imagem (necessários antes da primeira aula com onboarding). A versão prévia do
   Código de Conduta está em
   [13-codigo-de-conduta-versao-previa.md](13-codigo-de-conduta-versao-previa.md), para
   pactuação com os jogadores no primeiro encontro.
5. Escrever o roteiro pedagógico da oficina do [Robô Educa](06-robo-educa.md), primeira
   trilha do piloto.
6. **Cadastrar o Goethe-Institut como Apoiador** e registrar os aportes — **298 livros e 30
   kits MDF** — no inventário, com o **Termo de Doação** anexado como artefato
   comprobatório. É o primeiro caso real da economia de recursos
   ([04 §1](04-modelo-economico-e-sustentabilidade.md#primeiro-aporte-registrado--acervo-didático-e-kits-do-goethe-institut)).
7. **Tombar os 46 exemplares da linha Include I** e implantar a estratégia de conservação
   antes da primeira turma; preparar a **entrega dos exemplares da linha Alpha** na abertura
   de cada trilha ([05 §2](05-implantacao-e-operacao.md#acervo-didático-guarda-e-conservação)).
8. **Ler o acervo Include**, título a título, e mapear qual capítulo apoia qual ponto das
   trilhas Robô Educa e Batalha de Laser.
9. **Criar as Comunidades Virtuais do piloto** (Admin) antes do primeiro onboarding — sem
   comunidade cadastrada não há como vincular jogador
   ([02 §1](02-conceito-do-jogo-e-gamificacao.md#comunidades-virtuais)).
10. **Definir os números da coleta de dados** — cadência, pontos por registro, janela de
    tolerância e teto por período —, sem os quais os desafios de coleta obrigatórios de cada
    trilha não podem ser publicados.
11. **Fechar o planejamento do [Ciclo 01](10-case-01-guerreira-zeferina.md)** antes de agosto
    de 2026: ponto de apoio definido, calendário dos encontros, metas numéricas das hipóteses
    H1 e H2 e conferência do lastro necessário (H3).
12. **Resgatar a memória da edição de 2024** (Inova Comunidade) na Guerreira Zeferina — o que
    existe de registro, contatos e aprendizados — como linha de base do relacionamento com a
    comunidade.
